"""Integration tests for media operations.

These tests require real API access and valid files.
They are skipped unless LINKEDIN_ACCESS_TOKEN is set.
"""

import pytest

from linkedin_sdk import LinkedInClient


def test_init_image_upload(client: LinkedInClient):
    """Initialize an image upload and verify we get a URL and URN."""
    result = client.init_image_upload()
    assert "uploadUrl" in result
    assert "imageUrn" in result
    assert result["uploadUrl"].startswith("https://")
    assert "urn:li:image:" in result["imageUrn"]
