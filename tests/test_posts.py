"""Integration tests for post operations."""

import pytest

from linkedin_sdk import LinkedInClient


def test_create_and_delete_post(client: LinkedInClient, cleanup_urns: list[str]):
    """Create a text post, verify it, then delete."""
    result = client.create_post("SDK integration test - safe to delete")
    assert result["postUrn"]
    assert result["statusCode"] in (200, 201)
    cleanup_urns.append(result["postUrn"])


def test_get_my_posts(client: LinkedInClient):
    """Get the user's posts."""
    result = client.get_my_posts(limit=5)
    assert "elements" in result


def test_create_post_with_link(client: LinkedInClient, cleanup_urns: list[str]):
    """Create a post with an article link."""
    result = client.create_post_with_link(
        commentary="SDK link test - safe to delete",
        url="https://example.com",
        title="Example",
    )
    assert result["postUrn"]
    cleanup_urns.append(result["postUrn"])
