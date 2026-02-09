"""Integration tests for engagement operations.

These tests require an existing post URN to interact with.
They are designed to be run manually with a known post URN.
"""

import os

import pytest

from linkedin_sdk import LinkedInClient


@pytest.fixture
def post_urn() -> str:
    """Get a post URN from env for engagement tests."""
    urn = os.environ.get("LINKEDIN_TEST_POST_URN")
    if not urn:
        pytest.skip("Set LINKEDIN_TEST_POST_URN for engagement tests")
    return urn


def test_add_reaction(client: LinkedInClient, post_urn: str):
    """Add a LIKE reaction to a post."""
    status = client.add_reaction(post_urn, "LIKE")
    assert status in (200, 201)
