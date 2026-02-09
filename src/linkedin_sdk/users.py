"""User operations."""

from __future__ import annotations

from typing import Any


class UsersMixin:
    """Mixin providing user API methods."""

    def get_user_info(self) -> dict[str, Any]:
        """GET /v2/userinfo — Get the authenticated user's profile.

        Returns:
            {"sub": "...", "name": "...", "email": "...", "picture": "...", ...}
        """
        return self._get_v2("/userinfo")
