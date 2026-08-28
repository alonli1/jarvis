# Shared Dropbox library

Dropbox is the canonical group document store. Jarvis uses OAuth 2 PKCE so each researcher acts
through their own Dropbox account; a shared download link alone cannot upload changes.

## One-time group setup

1. Create a scoped Dropbox app with Full Dropbox access and offline refresh tokens.
2. Grant only the file metadata/content read-write scopes needed by Jarvis.
3. Put the public app key in `[dropbox].app_key` in `assistant.toml`. Never commit a client
   secret, access token, or refresh token.
4. Share the canonical folder with group members as editors.

The folder contains `papers/`, `books/`, `notes/`, and `manuscripts/`. Jarvis creates missing
category folders after successful editor authorization.

## Researcher onboarding

```bash
uv sync
uv run jarvis setup --dropbox-link "https://www.dropbox.com/scl/fo/..."
```

The browser authorization uses PKCE. The refresh token is stored in the OS credential vault;
`.jarvis/settings.toml` contains only the public app key, account ID, folder ID/path, and link.
Setup downloads the library and builds the local index.

Run `jarvis doctor` first and require `OK OS keyring`. Linux sessions need an unlocked Secret
Service-compatible vault such as GNOME Keyring; Jarvis refuses plaintext-token fallback.

## Daily use

```bash
uv run jarvis library add ~/Downloads/paper.pdf --category papers
uv run jarvis library status
uv run jarvis library sync --dry-run
uv run jarvis library sync
```

`library add` validates and copies the document, creates or preserves its `.meta.yaml` sidecar,
uploads both, and ingests the local document. Files copied manually into managed folders upload
on the next sync.

Synchronization compares the last local SHA-256 and Dropbox revision/content hash:

- one-sided changes propagate;
- simultaneous changes become conflicts;
- local deletions are restored from Dropbox;
- Dropbox deletions are reported but not mirrored or automatically resurrected;
- no operation silently overwrites a newer Dropbox revision.

Resolve a reviewed conflict explicitly:

```bash
uv run jarvis library resolve papers/example.pdf --use local
uv run jarvis library resolve papers/example.pdf --use dropbox
uv run jarvis library resolve papers/example.pdf --use keep-both
```

`keep-both` saves the local version with a timestamp and restores Dropbox to the canonical path;
the renamed local copy uploads as a separate document on the next sync.

## Mounted-folder compatibility

The old pull-only interface remains available for Dropbox Desktop, Nextcloud, or a network mount:

```bash
uv run jarvis library-sync /path/to/Jarvis --provider synced-folder --dry-run
uv run jarvis library-sync /path/to/Jarvis --provider synced-folder
```

It does not provide bidirectional API synchronization or OAuth state.
