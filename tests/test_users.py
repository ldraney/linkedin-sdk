"""Integration tests for user operations."""

from linkedin_sdk import LinkedInClient


def test_get_user_info(client: LinkedInClient):
    """Get user info and verify sub field."""
    info = client.get_user_info()
    assert "sub" in info
    assert info["sub"]
