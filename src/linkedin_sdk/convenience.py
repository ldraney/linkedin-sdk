"""Convenience methods that combine multiple API calls."""

from __future__ import annotations

import os
from typing import Any


# MIME type maps
_IMAGE_MIMES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
}

_DOCUMENT_MIMES = {
    ".pdf": "application/pdf",
    ".doc": "application/msword",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".ppt": "application/vnd.ms-powerpoint",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
}

_VIDEO_MIMES = {
    ".mp4": "video/mp4",
    ".mov": "video/quicktime",
    ".avi": "video/x-msvideo",
    ".wmv": "video/x-ms-wmv",
    ".webm": "video/webm",
    ".mkv": "video/x-matroska",
    ".m4v": "video/x-m4v",
    ".flv": "video/x-flv",
}


def _get_mime(file_path: str, mime_map: dict[str, str]) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    return mime_map.get(ext, "application/octet-stream")


class ConvenienceMixin:
    """Mixin providing high-level convenience methods."""

    def create_post_with_link(
        self,
        commentary: str,
        url: str,
        title: str | None = None,
        description: str | None = None,
        visibility: str = "PUBLIC",
    ) -> dict[str, Any]:
        """Create a post with an article link preview.

        Args:
            commentary: Post text.
            url: Article URL.
            title: Article title (defaults to URL).
            description: Article description.
            visibility: Post visibility.

        Returns:
            {"postUrn": "...", "statusCode": 201}
        """
        article: dict[str, str] = {"source": url, "title": title or url}
        if description:
            article["description"] = description

        return self.create_post(
            commentary=commentary,
            visibility=visibility,
            content={"article": article},
        )

    def create_post_with_image(
        self,
        commentary: str,
        image_path: str,
        alt_text: str | None = None,
        visibility: str = "PUBLIC",
    ) -> dict[str, Any]:
        """Create a post with an uploaded image.

        Args:
            commentary: Post text.
            image_path: Path to the image file.
            alt_text: Alt text for the image.
            visibility: Post visibility.

        Returns:
            {"postUrn": "...", "imageUrn": "...", "statusCode": 201}
        """
        data = self._read_file(image_path)
        content_type = _get_mime(image_path, _IMAGE_MIMES)

        upload = self.init_image_upload()
        self.upload_binary(upload["uploadUrl"], data, content_type)

        media: dict[str, str] = {"id": upload["imageUrn"]}
        if alt_text:
            media["altText"] = alt_text

        result = self.create_post(
            commentary=commentary,
            visibility=visibility,
            content={"media": media},
        )
        result["imageUrn"] = upload["imageUrn"]
        return result

    def create_post_with_document(
        self,
        commentary: str,
        document_path: str,
        title: str | None = None,
        visibility: str = "PUBLIC",
    ) -> dict[str, Any]:
        """Create a post with an uploaded document.

        Args:
            commentary: Post text.
            document_path: Path to the document file.
            title: Document title (defaults to filename).
            visibility: Post visibility.

        Returns:
            {"postUrn": "...", "documentUrn": "...", "statusCode": 201}
        """
        data = self._read_file(document_path)
        content_type = _get_mime(document_path, _DOCUMENT_MIMES)

        upload = self.init_document_upload()
        self.upload_binary(upload["uploadUrl"], data, content_type)

        doc_title = title or os.path.basename(document_path)
        result = self.create_post(
            commentary=commentary,
            visibility=visibility,
            content={"media": {"id": upload["documentUrn"], "title": doc_title}},
        )
        result["documentUrn"] = upload["documentUrn"]
        return result

    def create_post_with_video(
        self,
        commentary: str,
        video_path: str,
        title: str | None = None,
        visibility: str = "PUBLIC",
    ) -> dict[str, Any]:
        """Create a post with an uploaded video.

        Args:
            commentary: Post text.
            video_path: Path to the video file.
            title: Video title (defaults to filename).
            visibility: Post visibility.

        Returns:
            {"postUrn": "...", "videoUrn": "...", "statusCode": 201}
        """
        data = self._read_file(video_path)
        content_type = _get_mime(video_path, _VIDEO_MIMES)

        upload = self.init_video_upload(len(data))
        upload_result = self.upload_binary(upload["uploadUrl"], data, content_type)
        self.finalize_video(upload["videoUrn"], upload_result["etag"])

        video_title = title or os.path.basename(video_path)
        result = self.create_post(
            commentary=commentary,
            visibility=visibility,
            content={"media": {"id": upload["videoUrn"], "title": video_title}},
        )
        result["videoUrn"] = upload["videoUrn"]
        return result

    def create_poll(
        self,
        question: str,
        options: list[str],
        commentary: str = "",
        duration: str = "THREE_DAYS",
        visibility: str = "PUBLIC",
    ) -> dict[str, Any]:
        """Create a poll post.

        Args:
            question: Poll question.
            options: 2-4 poll option texts.
            commentary: Optional post text.
            duration: ONE_DAY, THREE_DAYS, SEVEN_DAYS, or FOURTEEN_DAYS.
            visibility: Post visibility.

        Returns:
            {"postUrn": "...", "statusCode": 201}
        """
        return self.create_post(
            commentary=commentary,
            visibility=visibility,
            content={
                "poll": {
                    "question": question,
                    "options": [{"text": opt} for opt in options],
                    "settings": {
                        "duration": duration,
                        "voteSelectionType": "SINGLE_VOTE",
                        "isVoterVisibleToAuthor": True,
                    },
                }
            },
        )

    def create_post_with_multi_images(
        self,
        commentary: str,
        image_paths: list[str],
        alt_texts: list[str] | None = None,
        visibility: str = "PUBLIC",
    ) -> dict[str, Any]:
        """Create a post with multiple images (2-20).

        Args:
            commentary: Post text.
            image_paths: Paths to image files.
            alt_texts: Optional alt texts (matched by index).
            visibility: Post visibility.

        Returns:
            {"postUrn": "...", "imageUrns": [...], "statusCode": 201}
        """
        image_urns: list[str] = []
        for i, img_path in enumerate(image_paths):
            data = self._read_file(img_path)
            content_type = _get_mime(img_path, _IMAGE_MIMES)

            upload = self.init_image_upload()
            self.upload_binary(upload["uploadUrl"], data, content_type)
            image_urns.append(upload["imageUrn"])

        images = []
        for i, urn in enumerate(image_urns):
            img: dict[str, str] = {"id": urn}
            if alt_texts and i < len(alt_texts) and alt_texts[i]:
                img["altText"] = alt_texts[i]
            images.append(img)

        result = self.create_post(
            commentary=commentary,
            visibility=visibility,
            content={"multiImage": {"images": images}},
        )
        result["imageUrns"] = image_urns
        return result

    @staticmethod
    def _read_file(file_path: str) -> bytes:
        """Read a file and return its bytes."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, "rb") as f:
            return f.read()
