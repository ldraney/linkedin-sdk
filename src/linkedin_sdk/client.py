"""Main LinkedIn API client."""

from __future__ import annotations

import os
from typing import Any
from urllib.parse import quote

import httpx
from dotenv import load_dotenv

from .posts import PostsMixin
from .media import MediaMixin
from .engagement import EngagementMixin
from .users import UsersMixin
from .auth import AuthMixin
from .convenience import ConvenienceMixin

load_dotenv()

LINKEDIN_REST_BASE = "https://api.linkedin.com/rest"
LINKEDIN_V2_BASE = "https://api.linkedin.com/v2"
LINKEDIN_OAUTH_HOST = "https://www.linkedin.com"
DEFAULT_API_VERSION = "202510"


class LinkedInClient(
    PostsMixin,
    MediaMixin,
    EngagementMixin,
    UsersMixin,
    AuthMixin,
    ConvenienceMixin,
):
    """Synchronous Python client for the LinkedIn API v202510."""

    def __init__(
        self,
        access_token: str | None = None,
        person_id: str | None = None,
        api_version: str = DEFAULT_API_VERSION,
    ):
        if access_token is None:
            access_token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
        if person_id is None:
            person_id = os.environ.get("LINKEDIN_PERSON_ID")

        self.access_token = access_token
        self.person_id = person_id
        self.api_version = api_version

        # REST client for /rest/ endpoints
        headers: dict[str, str] = {
            "Content-Type": "application/json",
            "LinkedIn-Version": self.api_version,
            "X-Restli-Protocol-Version": "2.0.0",
        }
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"

        self._http = httpx.Client(
            base_url=LINKEDIN_REST_BASE,
            headers=headers,
            timeout=60.0,
        )

        # V2 client for /v2/ endpoints (userinfo)
        v2_headers: dict[str, str] = {"Content-Type": "application/json"}
        if self.access_token:
            v2_headers["Authorization"] = f"Bearer {self.access_token}"

        self._http_v2 = httpx.Client(
            base_url=LINKEDIN_V2_BASE,
            headers=v2_headers,
            timeout=30.0,
        )

    @property
    def person_urn(self) -> str:
        """Return the full person URN."""
        if not self.person_id:
            raise ValueError(
                "No person_id set. Pass person_id= or set LINKEDIN_PERSON_ID env var."
            )
        return f"urn:li:person:{self.person_id}"

    # ---- low-level helpers ------------------------------------------------

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        resp = self._http.get(path, params=params)
        resp.raise_for_status()
        return resp.json() if resp.text.strip() else {}

    def _post(
        self,
        path: str,
        json: dict[str, Any] | None = None,
        extra_headers: dict[str, str] | None = None,
    ) -> httpx.Response:
        """POST to a /rest/ endpoint. Returns the full Response for header access."""
        resp = self._http.post(path, json=json or {}, headers=extra_headers)
        resp.raise_for_status()
        return resp

    def _delete(self, path: str) -> int:
        resp = self._http.delete(path)
        resp.raise_for_status()
        return resp.status_code

    def _get_v2(self, path: str) -> dict[str, Any]:
        resp = self._http_v2.get(path)
        resp.raise_for_status()
        return resp.json()

    def _put_binary(
        self,
        url: str,
        data: bytes,
        content_type: str,
    ) -> httpx.Response:
        """PUT binary data to an upload URL (S3 pre-signed)."""
        headers = {
            "Content-Type": content_type,
        }
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        resp = httpx.put(url, content=data, headers=headers, timeout=300.0)
        resp.raise_for_status()
        return resp

    @staticmethod
    def _oauth_post(path: str, params: dict[str, str]) -> dict[str, Any]:
        """POST form-encoded data to the LinkedIn OAuth endpoint."""
        resp = httpx.post(
            f"{LINKEDIN_OAUTH_HOST}{path}",
            data=params,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=30.0,
        )
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def _encode_urn(urn: str) -> str:
        """URL-encode a LinkedIn URN for use in paths."""
        return quote(urn, safe="")

    def close(self) -> None:
        self._http.close()
        self._http_v2.close()
