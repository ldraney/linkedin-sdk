"""Tests for convenience methods.

Most convenience tests are integration-level (require API access + files).
This file includes unit tests for helper functions.
"""

import os
import tempfile

import pytest

from linkedin_sdk.convenience import _get_mime, _IMAGE_MIMES, _DOCUMENT_MIMES, _VIDEO_MIMES


def test_image_mime_types():
    assert _get_mime("photo.png", _IMAGE_MIMES) == "image/png"
    assert _get_mime("photo.jpg", _IMAGE_MIMES) == "image/jpeg"
    assert _get_mime("photo.jpeg", _IMAGE_MIMES) == "image/jpeg"
    assert _get_mime("photo.gif", _IMAGE_MIMES) == "image/gif"
    assert _get_mime("photo.bmp", _IMAGE_MIMES) == "application/octet-stream"


def test_document_mime_types():
    assert _get_mime("doc.pdf", _DOCUMENT_MIMES) == "application/pdf"
    assert _get_mime("doc.pptx", _DOCUMENT_MIMES) == "application/vnd.openxmlformats-officedocument.presentationml.presentation"


def test_video_mime_types():
    assert _get_mime("vid.mp4", _VIDEO_MIMES) == "video/mp4"
    assert _get_mime("vid.mov", _VIDEO_MIMES) == "video/quicktime"
    assert _get_mime("vid.webm", _VIDEO_MIMES) == "video/webm"


def test_read_file_not_found():
    from linkedin_sdk.convenience import ConvenienceMixin
    with pytest.raises(FileNotFoundError):
        ConvenienceMixin._read_file("/nonexistent/file.png")


def test_read_file_success():
    from linkedin_sdk.convenience import ConvenienceMixin
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
        f.write(b"test content")
        f.flush()
        try:
            data = ConvenienceMixin._read_file(f.name)
            assert data == b"test content"
        finally:
            os.unlink(f.name)
