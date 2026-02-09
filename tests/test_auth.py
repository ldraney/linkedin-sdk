"""Unit tests for auth URL building (no HTTP needed)."""

from linkedin_sdk import LinkedInClient


def test_get_auth_url_basic():
    url = LinkedInClient.get_auth_url(
        client_id="test_id",
        redirect_uri="http://localhost:8080/callback",
    )
    assert "response_type=code" in url
    assert "client_id=test_id" in url
    assert "redirect_uri=" in url
    assert "scope=" in url
    assert "linkedin.com/oauth/v2/authorization" in url


def test_get_auth_url_custom_scopes():
    url = LinkedInClient.get_auth_url(
        client_id="id",
        redirect_uri="http://localhost/cb",
        scopes=["openid", "profile"],
    )
    assert "openid" in url
    assert "profile" in url
    assert "w_member_social" not in url


def test_get_auth_url_with_state():
    url = LinkedInClient.get_auth_url(
        client_id="id",
        redirect_uri="http://localhost/cb",
        state="my_state_123",
    )
    assert "state=my_state_123" in url
