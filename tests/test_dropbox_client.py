from jarvis.dropbox_client import (
    DropboxClient,
    DropboxSettings,
    authorize,
    load_settings,
    save_settings,
)


class Response:
    def __init__(self, data):
        self.data = data

    def raise_for_status(self):
        return None

    def json(self):
        return self.data


class Client:
    def __init__(self):
        self.posts = []

    def post(self, url, **kwargs):
        self.posts.append((url, kwargs))
        return Response(
            {"refresh_token": "refresh", "access_token": "access", "account_id": "dbid:1"}
        )


def test_authorize_uses_pkce_and_requests_offline_token(monkeypatch):
    opened = []
    monkeypatch.setattr("jarvis.dropbox_client._pkce_pair", lambda: ("verifier", "challenge"))

    refresh, account = authorize(
        "app-key",
        input_code=lambda _: "authorization-code",
        open_browser=opened.append,
        client=Client(),
    )

    assert (refresh, account) == ("refresh", "dbid:1")
    assert "token_access_type=offline" in opened[0]
    assert "code_challenge=challenge" in opened[0]


def test_local_settings_are_toml_and_contain_no_credentials(tmp_path):
    settings = DropboxSettings(
        "public-key", "dbid:1", "id:folder", "/jarvis", "Jarvis", "https://dropbox/link"
    )

    path = save_settings(tmp_path, settings)

    assert path.name == "settings.toml"
    assert load_settings(tmp_path) == settings
    assert "refresh_token" not in path.read_text()


def test_list_files_preserves_dropbox_display_case():
    settings = DropboxSettings(
        "public-key", "dbid:1", "id:folder", "/jarvis", "Jarvis", "https://dropbox/link"
    )
    client = DropboxClient(settings, access_token="access", client=Client())
    client.rpc = lambda *_args, **_kwargs: {
        "entries": [
            {
                ".tag": "file",
                "id": "id:readme",
                "name": "README.md",
                "path_lower": "/jarvis/manuscripts/example_project/readme.md",
                "path_display": "/Jarvis/manuscripts/example_project/README.md",
                "rev": "1",
                "content_hash": "hash",
                "server_modified": "2026-08-28T00:00:00Z",
            }
        ],
        "has_more": False,
    }

    files = client.list_files()

    assert "manuscripts/example_project/README.md" in files
    assert files["manuscripts/example_project/README.md"].path.endswith("/readme.md")
