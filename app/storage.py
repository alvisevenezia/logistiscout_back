import os
import io
from typing import Optional
from minio import Minio
from minio.error import S3Error

MINIO_ENDPOINT = os.environ.get("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.environ.get("MINIO_ROOT_USER")
MINIO_SECRET_KEY = os.environ.get("MINIO_ROOT_PASSWORD")
MINIO_SECURE = os.environ.get("MINIO_SECURE", "false").lower() in ("1", "true", "yes")
MINIO_PUBLIC_ENDPOINT = os.environ.get("MINIO_PUBLIC_ENDPOINT", None)

_client: Optional[Minio] = None

def get_client() -> Minio:
    global _client
    if _client is None:
        if not MINIO_ACCESS_KEY or not MINIO_SECRET_KEY:
            raise RuntimeError("MINIO_ROOT_USER and MINIO_ROOT_PASSWORD must be set in environment")
        _client = Minio(
            MINIO_ENDPOINT,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=MINIO_SECURE,
        )
    return _client

def ensure_bucket(bucket_name: str):
    client = get_client()
    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)

def upload_bytes(bucket_name: str, object_name: str, data: bytes, content_type: Optional[str] = None):
    client = get_client()
    ensure_bucket(bucket_name)
    bio = io.BytesIO(data)
    bio.seek(0)
    client.put_object(bucket_name, object_name, bio, length=len(data), content_type=content_type)

def get_public_url(bucket_name: str, object_name: str) -> str:
    # If a public endpoint is provided, use it; otherwise derive from MINIO_ENDPOINT
    if MINIO_PUBLIC_ENDPOINT:
        base = MINIO_PUBLIC_ENDPOINT.rstrip("/")
        scheme = "https" if MINIO_SECURE else "http"
        if base.startswith("http://") or base.startswith("https://"):
            return f"{base}/{bucket_name}/{object_name}"
        return f"{scheme}://{base}/{bucket_name}/{object_name}"
    scheme = "https" if MINIO_SECURE else "http"
    return f"{scheme}://{MINIO_ENDPOINT}/{bucket_name}/{object_name}"
