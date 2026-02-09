"""OAuth authentication operations."""

from __future__ import annotations

from typing import Any
from urllib.parse import urlencode


class AuthMixin:
    """Mixin providing OAuth API methods."""

    @staticmethod
    def get_auth_url(
        client_id: str,
        redirect_uri: str,
        scopes: list[str] | None = None,
        state: str = "",
    ) -> str:
        """Build a LinkedIn OAuth 2.0 authorization URL.

        Args:
            client_id: LinkedIn app client ID.
            redirect_uri: Callback URL.
            scopes: OAuth scopes (default: openid, profile, email, w_member_social).
            state: CSRF state parameter.

        Returns:
            The authorization URL.
        """
        if scopes is None:
            scopes = ["openid", "profile", "email", "w_member_social"]

        params = {
            "response_type": "code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scope": " ".join(scopes),
        }
        if state:
            params["state"] = state

        return f"https://www.linkedin.com/oauth/v2/authorization?{urlencode(params)}"

    @classmethod
    def exchange_code(
        cls,
        code: str,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
    ) -> dict[str, Any]:
        """Exchange an authorization code for an access token.

        Args:
            code: Authorization code from the callback.
            client_id: LinkedIn app client ID.
            client_secret: LinkedIn app client secret.
            redirect_uri: The same redirect URI used in the auth request.

        Returns:
            {"access_token": "...", "expires_in": ..., "scope": "...", ...}
        """
        return cls._oauth_post(
            "/oauth/v2/accessToken",
            {
                "grant_type": "authorization_code",
                "code": code,
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
            },
        )

    @classmethod
    def refresh_token(
        cls,
        refresh_token: str,
        client_id: str,
        client_secret: str,
    ) -> dict[str, Any]:
        """Refresh an expired access token.

        Args:
            refresh_token: The refresh token.
            client_id: LinkedIn app client ID.
            client_secret: LinkedIn app client secret.

        Returns:
            {"access_token": "...", "expires_in": ..., ...}
        """
        return cls._oauth_post(
            "/oauth/v2/accessToken",
            {
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": client_id,
                "client_secret": client_secret,
            },
        )
