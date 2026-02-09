"""Media upload operations (images, documents, videos)."""

from __future__ import annotations

from typing import Any


class MediaMixin:
    """Mixin providing media upload API methods."""

    def init_image_upload(self) -> dict[str, str]:
        """POST /rest/images?action=initializeUpload — Get a pre-signed upload URL for an image.

        Returns:
            {"uploadUrl": "...", "imageUrn": "urn:li:image:..."}
        """
        resp = self._post(
            "/images?action=initializeUpload",
            json={"initializeUploadRequest": {"owner": self.person_urn}},
        )
        body = resp.json()
        return {
            "uploadUrl": body["value"]["uploadUrl"],
            "imageUrn": body["value"]["image"],
        }

    def init_document_upload(self) -> dict[str, str]:
        """POST /rest/documents?action=initializeUpload — Get a pre-signed upload URL for a document.

        Returns:
            {"uploadUrl": "...", "documentUrn": "urn:li:document:..."}
        """
        resp = self._post(
            "/documents?action=initializeUpload",
            json={"initializeUploadRequest": {"owner": self.person_urn}},
        )
        body = resp.json()
        return {
            "uploadUrl": body["value"]["uploadUrl"],
            "documentUrn": body["value"]["document"],
        }

    def init_video_upload(self, file_size_bytes: int) -> dict[str, str]:
        """POST /rest/videos?action=initializeUpload — Get a pre-signed upload URL for a video.

        Args:
            file_size_bytes: Size of the video file in bytes.

        Returns:
            {"uploadUrl": "...", "videoUrn": "urn:li:video:..."}
        """
        resp = self._post(
            "/videos?action=initializeUpload",
            json={
                "initializeUploadRequest": {
                    "owner": self.person_urn,
                    "fileSizeBytes": file_size_bytes,
                    "uploadCaptions": False,
                    "uploadThumbnail": False,
                }
            },
        )
        body = resp.json()
        return {
            "uploadUrl": body["value"]["uploadInstructions"][0]["uploadUrl"],
            "videoUrn": body["value"]["video"],
        }

    def upload_binary(self, upload_url: str, data: bytes, content_type: str) -> dict[str, Any]:
        """PUT binary data to a LinkedIn upload URL.

        Args:
            upload_url: Pre-signed upload URL from init_*_upload.
            data: Raw file bytes.
            content_type: MIME type of the file.

        Returns:
            {"statusCode": 200, "etag": "..."} (etag only for video uploads)
        """
        resp = self._put_binary(upload_url, data, content_type)
        return {
            "statusCode": resp.status_code,
            "etag": resp.headers.get("etag", ""),
        }

    def finalize_video(self, video_urn: str, etag: str) -> int:
        """POST /rest/videos?action=finalizeUpload — Finalize a video upload.

        Args:
            video_urn: The video URN from init_video_upload.
            etag: The etag from upload_binary response.

        Returns:
            HTTP status code.
        """
        resp = self._post(
            "/videos?action=finalizeUpload",
            json={
                "finalizeUploadRequest": {
                    "video": video_urn,
                    "uploadToken": "",
                    "uploadedPartIds": [etag],
                }
            },
        )
        return resp.status_code
