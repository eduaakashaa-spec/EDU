"""Cloudflare R2 (S3-compatible) object storage for private files — currently
the College Guide resumes.

Uploads are server-side (browser → Flask → R2) so the bucket stays private:
no CORS and no public URL needed. Admins read a file through a short-lived
presigned GET link (see alumni.admin_resume). Configure via env vars:

    R2_ENDPOINT          https://<account>.r2.cloudflarestorage.com/<bucket>
    R2_ACCESS_KEY_ID     from an R2 API token (Object Read & Write)
    R2_SECRET_ACCESS_KEY  "        "
    R2_BUCKET            eduaakashaa   (defaults to the path in R2_ENDPOINT)

If the vars are unset, is_configured() is False and callers surface a clear
error rather than crashing.
"""
import os
import threading

_client = None
_lock = threading.Lock()


def _bucket():
    b = os.environ.get('R2_BUCKET')
    if b:
        return b
    # fall back to the last path segment of the endpoint (…/eduaakashaa)
    ep = os.environ.get('R2_ENDPOINT', '').rstrip('/')
    return ep.rsplit('/', 1)[-1] if '/' in ep else ''


def is_configured():
    return bool(os.environ.get('R2_ENDPOINT')
                and os.environ.get('R2_ACCESS_KEY_ID')
                and os.environ.get('R2_SECRET_ACCESS_KEY')
                and _bucket())


def _get_client():
    """Lazily build one boto3 S3 client (thread-safe, reused across requests)."""
    global _client
    if _client is not None:
        return _client
    with _lock:
        if _client is None:
            import boto3
            from botocore.config import Config
            # R2 needs the bucket in the path, not the endpoint host, so strip
            # the trailing /<bucket> the dashboard shows in the S3 API string.
            endpoint = os.environ['R2_ENDPOINT'].rstrip('/')
            if endpoint.rsplit('/', 1)[-1] == _bucket():
                endpoint = endpoint.rsplit('/', 1)[0]
            _client = boto3.client(
                's3', endpoint_url=endpoint,
                aws_access_key_id=os.environ['R2_ACCESS_KEY_ID'],
                aws_secret_access_key=os.environ['R2_SECRET_ACCESS_KEY'],
                region_name='auto',
                config=Config(signature_version='s3v4'))
    return _client


def upload(data, key, content_type):
    """Store bytes at `key`. Raises on failure (caller turns it into a 502)."""
    _get_client().put_object(Bucket=_bucket(), Key=key, Body=data,
                             ContentType=content_type or 'application/octet-stream')
    return key


def presigned_get(key, expires=300, download_name=None, inline=True):
    """Short-lived GET URL. Served from R2's own domain (not our origin), so
    inline is safe — PDFs open in the browser tab; DOC/DOCX download anyway
    since browsers can't render them. Pass inline=False to force a download."""
    disp = 'inline' if inline else 'attachment'
    params = {'Bucket': _bucket(), 'Key': key}
    if download_name:
        params['ResponseContentDisposition'] = f'{disp}; filename="{download_name}"'
    else:
        params['ResponseContentDisposition'] = disp
    return _get_client().generate_presigned_url(
        'get_object', Params=params, ExpiresIn=expires)
