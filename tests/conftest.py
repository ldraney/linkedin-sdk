"""Shared fixtures for LinkedIn SDK tests."""

from __future__ import annotations

import os

import pytest

from linkedin_sdk import LinkedInClient


@pytest.fixture(scope="session")
def client() -> LinkedInClient:
    """Session-scoped LinkedIn client for integration tests."""
    token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
    person_id = os.environ.get("LINKEDIN_PERSON_ID")

    if not token or not person_id:
        pytest.skip(
            "Set LINKEDIN_ACCESS_TOKEN and LINKEDIN_PERSON_ID to run integration tests"
        )

    return LinkedInClient(access_token=token, person_id=person_id)


@pytest.fixture
def cleanup_urns(client: LinkedInClient):
    """Collect post URNs during a test and delete them after."""
    urns: list[str] = []
    yield urns
    for urn in urns:
        try:
            client.delete_post(urn)
        except Exception:
            pass
