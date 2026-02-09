"""Post operations."""

from __future__ import annotations

from typing import Any


class PostsMixin:
    """Mixin providing post API methods."""

    def create_post(
        self,
        commentary: str,
        visibility: str = "PUBLIC",
        content: dict[str, Any] | None = None,
        is_reshare_disabled: bool = False,
    ) -> dict[str, Any]:
        """POST /rest/posts — Create a new LinkedIn post.

        Args:
            commentary: Post text (max 3000 chars).
            visibility: PUBLIC, CONNECTIONS, LOGGED_IN, or CONTAINER.
            content: Optional content dict (article, media, multiImage, poll).
            is_reshare_disabled: Whether resharing is disabled.

        Returns:
            {"postUrn": "urn:li:share:...", "statusCode": 201}
        """
        body: dict[str, Any] = {
            "author": self.person_urn,
            "commentary": commentary,
            "visibility": visibility,
            "distribution": {"feedDistribution": "MAIN_FEED"},
            "lifecycleState": "PUBLISHED",
        }
        if content:
            body["content"] = content
        if is_reshare_disabled:
            body["isReshareDisabledByAuthor"] = True

        resp = self._post("/posts", json=body)
        return {
            "postUrn": resp.headers.get("x-restli-id", ""),
            "statusCode": resp.status_code,
        }

    def get_my_posts(
        self,
        limit: int = 10,
        offset: int = 0,
    ) -> dict[str, Any]:
        """GET /rest/posts?q=author — Get the authenticated user's posts.

        Args:
            limit: Number of posts to return (max 100).
            offset: Pagination offset.

        Returns:
            {"elements": [...], "paging": {...}}
        """
        encoded_urn = self._encode_urn(self.person_urn)
        return self._get(
            f"/posts?author={encoded_urn}&q=author&start={offset}&count={limit}"
        )

    def delete_post(self, post_urn: str) -> int:
        """DELETE /rest/posts/{postUrn} — Delete a post.

        Args:
            post_urn: The URN of the post to delete.

        Returns:
            HTTP status code (204 on success).
        """
        encoded = self._encode_urn(post_urn)
        return self._delete(f"/posts/{encoded}")

    def update_post(
        self,
        post_urn: str,
        commentary: str | None = None,
        content_call_to_action_label: str | None = None,
        content_landing_page: str | None = None,
    ) -> int:
        """POST /rest/posts/{postUrn} — Partial update a post.

        Args:
            post_urn: The URN of the post to update.
            commentary: New post text.
            content_call_to_action_label: New CTA label.
            content_landing_page: New landing page URL.

        Returns:
            HTTP status code.
        """
        set_fields: dict[str, str] = {}
        if commentary is not None:
            set_fields["commentary"] = commentary
        if content_call_to_action_label is not None:
            set_fields["contentCallToActionLabel"] = content_call_to_action_label
        if content_landing_page is not None:
            set_fields["contentLandingPage"] = content_landing_page

        encoded = self._encode_urn(post_urn)
        resp = self._post(
            f"/posts/{encoded}",
            json={"patch": {"$set": set_fields}},
            extra_headers={"X-RestLi-Method": "PARTIAL_UPDATE"},
        )
        return resp.status_code
