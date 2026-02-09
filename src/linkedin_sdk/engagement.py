"""Engagement operations (comments, reactions)."""

from __future__ import annotations

from typing import Any


class EngagementMixin:
    """Mixin providing social action API methods."""

    def add_comment(self, post_urn: str, text: str) -> dict[str, Any]:
        """POST /rest/socialActions/{postUrn}/comments — Add a comment to a post.

        Args:
            post_urn: The URN of the post to comment on.
            text: Comment text (max 1250 chars).

        Returns:
            {"commentUrn": "...", "statusCode": 201}
        """
        encoded = self._encode_urn(post_urn)
        resp = self._post(
            f"/socialActions/{encoded}/comments",
            json={
                "actor": self.person_urn,
                "message": {"text": text},
            },
        )
        return {
            "commentUrn": resp.headers.get("x-restli-id", ""),
            "statusCode": resp.status_code,
        }

    def add_reaction(self, post_urn: str, reaction_type: str) -> int:
        """POST /rest/reactions — Add a reaction to a post.

        Args:
            post_urn: The URN of the post to react to.
            reaction_type: One of LIKE, PRAISE, EMPATHY, INTEREST, APPRECIATION, ENTERTAINMENT.

        Returns:
            HTTP status code.
        """
        actor_urn = self._encode_urn(self.person_urn)
        resp = self._post(
            f"/reactions?actor={actor_urn}",
            json={
                "root": post_urn,
                "reactionType": reaction_type,
            },
        )
        return resp.status_code
