from __future__ import annotations

import base64
import hashlib
import json
import os
import secrets
import tempfile
import tomllib
import webbrowser
from collections.abc import Callable
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Self
from urllib.parse import urlencode

import httpx

API = "https://api.dropboxapi.com/2"
CONTENT_API = "https://content.dropboxapi.com/2"
AUTH_URL = "https://www.dropbox.com/oauth2/authorize"
TOKEN_URL = "https://api.dropboxapi.com/oauth2/token"
KEYRING_SERVICE = "jarvis-dropbox"
UPLOAD_LIMIT = 150 * 1024 * 1024
UPLOAD_CHUNK = 8 * 1024 * 1024


@dataclass(frozen=True)
class DropboxSettings:
    app_key: str
    account_id: str
    folder_id: str
    folder_path: str
    folder_name: str
    shared_link: str


@dataclass(frozen=True)
class RemoteFile:
    id: str
    path: str
    name: str
    rev: str
    content_hash: str
    server_modified: str


def settings_path(root: Path) -> Path:
    return root / ".jarvis" / "settings.toml"


def load_settings(root: Path) -> DropboxSettings:
    path = settings_path(root)
    if not path.exists():
        raise FileNotFoundError("Dropbox is not configured; run `jarvis setup --dropbox-link URL`")
    with path.open("rb") as stream:
        raw = tomllib.load(stream)
    data = raw.get("dropbox", {})
    return DropboxSettings(**data)


def save_settings(root: Path, settings: DropboxSettings) -> Path:
    path = settings_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["version = 1", "", "[dropbox]"]
    lines.extend(f"{key} = {json.dumps(value)}" for key, value in asdict(settings).items())
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
        temporary = Path(f.name)
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)
    return path


def project_app_key(configured: str = "") -> str:
    app_key = os.getenv("JARVIS_DROPBOX_APP_KEY", configured).strip()
    if not app_key:
        raise ValueError("Missing Dropbox app key; set JARVIS_DROPBOX_APP_KEY or [dropbox].app_key")
    return app_key


def _keyring():
    try:
        import keyring
        from keyring.errors import KeyringError, NoKeyringError
    except ImportError as exc:
        raise RuntimeError("Install Jarvis with the keyring dependency to use Dropbox") from exc
    return keyring, (KeyringError, NoKeyringError)


def save_refresh_token(account_id: str, token: str) -> None:
    keyring, errors = _keyring()
    try:
        keyring.set_password(KEYRING_SERVICE, account_id, token)
    except errors as exc:
        raise RuntimeError(
            "No secure OS credential store is available; configure one and authorize again"
        ) from exc


def load_refresh_token(account_id: str) -> str:
    keyring, errors = _keyring()
    try:
        token = keyring.get_password(KEYRING_SERVICE, account_id)
    except errors as exc:
        raise RuntimeError("Could not read the Dropbox token from the OS keyring") from exc
    if not token:
        raise RuntimeError("Dropbox authorization is missing; run `jarvis setup` again")
    return token


def _pkce_pair() -> tuple[str, str]:
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).decode()
    return verifier, challenge.rstrip("=")


def authorize(
    app_key: str,
    *,
    input_code: Callable[[str], str] = input,
    open_browser: Callable[[str], object] = webbrowser.open,
    client: httpx.Client | None = None,
) -> tuple[str, str]:
    """Authorize with no redirect, returning refresh token and account ID."""
    verifier, challenge = _pkce_pair()
    url = (
        AUTH_URL
        + "?"
        + urlencode(
            {
                "client_id": app_key,
                "response_type": "code",
                "token_access_type": "offline",
                "code_challenge_method": "S256",
                "code_challenge": challenge,
            }
        )
    )
    open_browser(url)
    code = input_code("Paste the Dropbox authorization code: ").strip()
    if not code:
        raise ValueError("Dropbox authorization code must not be empty")
    owned = client is None
    client = client or httpx.Client(timeout=60)
    try:
        response = client.post(
            TOKEN_URL,
            data={
                "code": code,
                "grant_type": "authorization_code",
                "client_id": app_key,
                "code_verifier": verifier,
            },
        )
        response.raise_for_status()
        token = response.json()
        refresh_token = token.get("refresh_token")
        access_token = token.get("access_token")
        account_id = token.get("account_id")
        if not refresh_token or not access_token:
            raise RuntimeError("Dropbox did not return offline credentials")
        if not account_id:
            account = _rpc(client, access_token, "users/get_current_account", None)
            account_id = account["account_id"]
        return str(refresh_token), str(account_id)
    finally:
        if owned:
            client.close()


def _rpc(client: httpx.Client, token: str, endpoint: str, data: dict | None) -> dict:
    response = client.post(
        f"{API}/{endpoint}",
        headers={"Authorization": f"Bearer {token}"},
        json=data,
    )
    response.raise_for_status()
    return response.json()


class DropboxClient:
    def __init__(
        self,
        settings: DropboxSettings,
        *,
        refresh_token: str | None = None,
        access_token: str | None = None,
        client: httpx.Client | None = None,
    ):
        self.settings = settings
        self.refresh_token = refresh_token
        self.access_token = access_token
        self.client = client or httpx.Client(timeout=120)

    @classmethod
    def from_repo(cls, root: Path) -> DropboxClient:
        settings = load_settings(root)
        return cls(settings, refresh_token=load_refresh_token(settings.account_id))

    def close(self) -> None:
        self.client.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_args) -> None:
        self.close()

    def _token(self) -> str:
        if self.access_token:
            return self.access_token
        if not self.refresh_token:
            raise RuntimeError("Dropbox refresh token is unavailable")
        response = self.client.post(
            TOKEN_URL,
            data={
                "refresh_token": self.refresh_token,
                "grant_type": "refresh_token",
                "client_id": self.settings.app_key,
            },
        )
        response.raise_for_status()
        self.access_token = str(response.json()["access_token"])
        return self.access_token

    def rpc(self, endpoint: str, data: dict | None = None) -> dict:
        return _rpc(self.client, self._token(), endpoint, data)

    def resolve_shared_folder(self, shared_link: str) -> dict:
        link = self.rpc("sharing/get_shared_link_metadata", {"url": shared_link})
        path = link.get("path_lower")
        if not path:
            raise PermissionError(
                "Join the Dropbox folder with editor access, then run setup again"
            )
        metadata = self.rpc("files/get_metadata", {"path": path})
        if metadata.get("sharing_info", {}).get("read_only"):
            raise PermissionError("Dropbox folder access is read-only; editor access is required")
        return {
            "id": str(metadata.get("id") or link.get("id") or ""),
            "path": str(metadata["path_lower"]),
            "name": str(metadata["name"]),
        }

    def ensure_layout(self) -> None:
        existing = {
            entry.get("name", "").lower()
            for entry in self.rpc("files/list_folder", {"path": self.settings.folder_path}).get(
                "entries", []
            )
            if entry.get(".tag") == "folder"
        }
        for category in ("papers", "books", "notes", "manuscripts"):
            if category not in existing:
                self.rpc(
                    "files/create_folder_v2",
                    {
                        "path": f"{self.settings.folder_path.rstrip('/')}/{category}",
                        "autorename": False,
                    },
                )

    def list_files(self) -> dict[str, RemoteFile]:
        data = self.rpc(
            "files/list_folder",
            {"path": self.settings.folder_path, "recursive": True, "include_deleted": False},
        )
        entries = list(data.get("entries", []))
        while data.get("has_more"):
            data = self.rpc("files/list_folder/continue", {"cursor": data["cursor"]})
            entries.extend(data.get("entries", []))
        prefix = self.settings.folder_path.rstrip("/") + "/"
        files: dict[str, RemoteFile] = {}
        for entry in entries:
            if entry.get(".tag") != "file":
                continue
            full_path = str(entry["path_lower"])
            if not full_path.startswith(prefix):
                continue
            relative = full_path[len(prefix) :]
            files[relative] = RemoteFile(
                id=str(entry["id"]),
                path=full_path,
                name=str(entry["name"]),
                rev=str(entry["rev"]),
                content_hash=str(entry.get("content_hash", "")),
                server_modified=str(entry.get("server_modified", "")),
            )
        return files

    def download(self, path: str) -> bytes:
        response = self.client.post(
            f"{CONTENT_API}/files/download",
            headers={
                "Authorization": f"Bearer {self._token()}",
                "Dropbox-API-Arg": json.dumps({"path": path}),
            },
        )
        response.raise_for_status()
        return response.content

    def upload(self, relative: str, content: bytes, rev: str | None = None) -> RemoteFile:
        path = str(PurePosixPath(self.settings.folder_path) / PurePosixPath(relative))
        mode: str | dict = {".tag": "update", "update": rev} if rev else "add"
        commit = {"path": path, "mode": mode, "autorename": False, "mute": False}
        if len(content) <= UPLOAD_LIMIT:
            response = self._content_request("files/upload", commit, content)
        else:
            response = self._session_upload(content, commit)
        entry = response.json()
        return RemoteFile(
            id=str(entry["id"]),
            path=str(entry["path_lower"]),
            name=str(entry["name"]),
            rev=str(entry["rev"]),
            content_hash=str(entry.get("content_hash", "")),
            server_modified=str(entry.get("server_modified", "")),
        )

    def _content_request(self, endpoint: str, argument: dict, content: bytes):
        response = self.client.post(
            f"{CONTENT_API}/{endpoint}",
            headers={
                "Authorization": f"Bearer {self._token()}",
                "Content-Type": "application/octet-stream",
                "Dropbox-API-Arg": json.dumps(argument),
            },
            content=content,
        )
        response.raise_for_status()
        return response

    def _session_upload(self, content: bytes, commit: dict):
        first = self._content_request(
            "files/upload_session/start", {"close": False}, content[:UPLOAD_CHUNK]
        )
        session_id = first.json()["session_id"]
        offset = min(len(content), UPLOAD_CHUNK)
        while len(content) - offset > UPLOAD_CHUNK:
            block = content[offset : offset + UPLOAD_CHUNK]
            self._content_request(
                "files/upload_session/append_v2",
                {"cursor": {"session_id": session_id, "offset": offset}, "close": False},
                block,
            )
            offset += len(block)
        return self._content_request(
            "files/upload_session/finish",
            {"cursor": {"session_id": session_id, "offset": offset}, "commit": commit},
            content[offset:],
        )
