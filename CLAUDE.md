# Development Guide

## Project Structure

```
src/linkedin_sdk/
  __init__.py          # exports LinkedInClient
  client.py            # LinkedInClient with _get, _post, _delete, _put_binary, _get_v2, _oauth_post
  posts.py             # PostsMixin: create_post, get_my_posts, delete_post, update_post
  media.py             # MediaMixin: init_image/doc/video_upload, upload_binary, finalize_video
  engagement.py        # EngagementMixin: add_comment, add_reaction
  users.py             # UsersMixin: get_user_info
  auth.py              # AuthMixin: get_auth_url (static), exchange_code (classmethod), refresh_token (classmethod)
  convenience.py       # ConvenienceMixin: create_post_with_image/doc/video/link/poll/multi_images
```

## Setup

```bash
# Install dependencies
uv sync

# Run tests (requires LINKEDIN_ACCESS_TOKEN + LINKEDIN_PERSON_ID)
uv run pytest
```

## Architecture

- **Mixin pattern**: Each API domain is a separate mixin class composed into `LinkedInClient`
- **Two HTTP clients**: `_http` for `/rest/` endpoints (LinkedIn-Version header), `_http_v2` for `/v2/` (userinfo)
- **OAuth as classmethods**: `exchange_code()` and `refresh_token()` don't need an authenticated client
- **API version pinned to 202510**: v202601 broke partner-only endpoints
- **URN encoding**: Handled internally (callers pass raw URNs)

## Releasing

CI auto-publishes on push to `main` when version is bumped in `pyproject.toml`.
Uses PyPI Trusted Publishers (OIDC) - no API tokens needed.
