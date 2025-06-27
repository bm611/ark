import os
import uuid
import boto3
import logging
import base64
import requests
from datetime import datetime
from botocore.exceptions import ClientError
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class R2StorageService:
    def __init__(self):
        self.access_key = os.getenv("R2_ACCESS_KEY_ID")
        self.secret_key = os.getenv("R2_SECRET_ACCESS_KEY")
        self.bucket_name = os.getenv("R2_BUCKET_NAME")
        self.endpoint_url = os.getenv("R2_ENDPOINT_URL")

        if not all(
            [self.access_key, self.secret_key, self.bucket_name, self.endpoint_url]
        ):
            raise ValueError(
                "Missing R2 configuration. Please set R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_BUCKET_NAME, and R2_ENDPOINT_URL"
            )

        self.client = boto3.client(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name="auto",
        )

    def upload_file(
        self, file_path: str, file_content: bytes, content_type: str, user_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Upload a file to R2 storage

        Args:
            file_path: Local file path (for generating key)
            file_content: File content as bytes
            content_type: MIME type of the file
            user_id: User ID for organizing files

        Returns:
            Dict with file metadata or None if upload failed
        """
        try:
            # Generate unique file key
            file_extension = os.path.splitext(file_path)[1]
            file_id = str(uuid.uuid4())
            file_key = f"uploads/{user_id}/{file_id}{file_extension}"

            # Upload to R2
            self.client.put_object(
                Bucket=self.bucket_name,
                Key=file_key,
                Body=file_content,
                ContentType=content_type,
                Metadata={
                    "uploaded_at": datetime.utcnow().isoformat(),
                    "user_id": user_id,
                    "original_filename": os.path.basename(file_path),
                },
            )

            logger.info(f"Successfully uploaded file {file_key} to R2")

            return {
                "file_id": file_id,
                "file_key": file_key,
                "original_filename": os.path.basename(file_path),
                "content_type": content_type,
                "size": len(file_content),
                "uploaded_at": datetime.utcnow(),
            }

        except ClientError as e:
            logger.error(f"Failed to upload file to R2: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error uploading file: {e}")
            return None

    def delete_file(self, file_key: str) -> bool:
        """
        Delete a file from R2 storage

        Args:
            file_key: The R2 object key

        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.delete_object(Bucket=self.bucket_name, Key=file_key)
            logger.info(f"Successfully deleted file {file_key} from R2")
            return True

        except ClientError as e:
            logger.error(f"Failed to delete file from R2: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error deleting file: {e}")
            return False

    def generate_presigned_url(
        self, file_key: str, expiration: int = 86400
    ) -> Optional[str]:
        """
        Generate a presigned URL for file access

        Args:
            file_key: The R2 object key
            expiration: URL expiration time in seconds (default: 24 hours)

        Returns:
            Presigned URL or None if generation failed
        """
        try:
            url = self.client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": file_key},
                ExpiresIn=expiration,
            )
            return url

        except ClientError as e:
            logger.error(f"Failed to generate presigned URL: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error generating presigned URL: {e}")
            return None

    def delete_user_files(self, user_id: str) -> bool:
        """
        Delete all files for a specific user

        Args:
            user_id: User ID

        Returns:
            True if successful, False otherwise
        """
        try:
            # List all objects with user prefix
            response = self.client.list_objects_v2(
                Bucket=self.bucket_name, Prefix=f"uploads/{user_id}/"
            )

            if "Contents" not in response:
                return True  # No files to delete

            # Batch delete objects
            objects_to_delete = [{"Key": obj["Key"]} for obj in response["Contents"]]

            self.client.delete_objects(
                Bucket=self.bucket_name, Delete={"Objects": objects_to_delete}
            )

            logger.info(
                f"Successfully deleted {len(objects_to_delete)} files for user {user_id}"
            )
            return True

        except ClientError as e:
            logger.error(f"Failed to delete user files: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error deleting user files: {e}")
            return False

    def delete_chat_files(self, file_keys: list[str]) -> bool:
        """
        Delete multiple files associated with a chat

        Args:
            file_keys: List of R2 object keys

        Returns:
            True if successful, False otherwise
        """
        if not file_keys:
            return True

        try:
            objects_to_delete = [{"Key": key} for key in file_keys]

            self.client.delete_objects(
                Bucket=self.bucket_name, Delete={"Objects": objects_to_delete}
            )

            logger.info(f"Successfully deleted {len(file_keys)} chat files from R2")
            return True

        except ClientError as e:
            logger.error(f"Failed to delete chat files: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error deleting chat files: {e}")
            return False

    def download_and_encode_pdf(self, presigned_url: str, filename: str) -> Optional[str]:
        """
        Download a PDF from a presigned URL and encode it to base64 for OpenRouter
        
        Args:
            presigned_url: The presigned URL to download from
            filename: Original filename for logging
            
        Returns:
            Base64 encoded PDF data URL or None if failed
        """
        try:
            # Download PDF content from presigned URL
            response = requests.get(presigned_url, timeout=30)
            response.raise_for_status()
            
            # Encode to base64
            encoded_content = base64.b64encode(response.content).decode('utf-8')
            base64_data_url = f"data:application/pdf;base64,{encoded_content}"
            
            logger.info(f"Successfully downloaded and encoded PDF: {filename}")
            return base64_data_url
            
        except requests.RequestException as e:
            logger.error(f"Failed to download PDF {filename} from presigned URL: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error processing PDF {filename}: {e}")
            return None


# Global instance
r2_storage = R2StorageService()


# Convenience functions
def upload_file(
    file_path: str, file_content: bytes, content_type: str, user_id: str
) -> Optional[Dict[str, Any]]:
    """Upload a file to R2 storage"""
    return r2_storage.upload_file(file_path, file_content, content_type, user_id)


def delete_file(file_key: str) -> bool:
    """Delete a file from R2 storage"""
    return r2_storage.delete_file(file_key)


def generate_presigned_url(file_key: str, expiration: int = 86400) -> Optional[str]:
    """Generate a presigned URL for file access"""
    return r2_storage.generate_presigned_url(file_key, expiration)


def delete_user_files(user_id: str) -> bool:
    """Delete all files for a specific user"""
    return r2_storage.delete_user_files(user_id)


def delete_chat_files(file_keys: list[str]) -> bool:
    """Delete multiple files associated with a chat"""
    return r2_storage.delete_chat_files(file_keys)


def download_and_encode_pdf(presigned_url: str, filename: str) -> Optional[str]:
    """Download a PDF from presigned URL and encode to base64"""
    return r2_storage.download_and_encode_pdf(presigned_url, filename)
