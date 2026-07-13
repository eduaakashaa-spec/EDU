"""Self-check for the R2 resume upload swap: magic-byte validation and the
R2 endpoint/bucket derivation. Run: python tests/test_resume_r2.py"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from werkzeug.datastructures import FileStorage
from app.routes.alumni import _validate_resume
from app.services import r2


def fs(name, body):
    return FileStorage(stream=io.BytesIO(body), filename=name)


# --- _validate_resume ------------------------------------------------------
data, mime, err = _validate_resume(fs('cv.pdf', b'%PDF-1.7\n...'))
assert err is None and mime == 'application/pdf', (mime, err)

_, _, err = _validate_resume(fs('cv.docx', b'PK\x03\x04junk'))
assert err is None, err

# extension not allowed
_, _, err = _validate_resume(fs('cv.exe', b'%PDF-1.7'))
assert err and 'PDF, DOC or DOCX' in err, err

# right extension, wrong bytes (an HTML file renamed .pdf)
_, _, err = _validate_resume(fs('cv.pdf', b'<html>gotcha</html>'))
assert err and 'valid PDF' in err, err

# oversize
_, _, err = _validate_resume(fs('cv.pdf', b'%PDF-' + b'x' * (5 * 1024 * 1024 + 1)))
assert err and '5 MB' in err, err

# no file → no error, no data (field is optional at this layer)
d, m, err = _validate_resume(fs('', b''))
assert (d, m, err) == (None, None, None)

# --- r2 bucket / endpoint derivation ---------------------------------------
os.environ['R2_ENDPOINT'] = 'https://acct123.r2.cloudflarestorage.com/eduaakashaa'
os.environ.pop('R2_BUCKET', None)
assert r2._bucket() == 'eduaakashaa', r2._bucket()

# not configured without credentials
os.environ.pop('R2_ACCESS_KEY_ID', None)
os.environ.pop('R2_SECRET_ACCESS_KEY', None)
assert r2.is_configured() is False

os.environ['R2_ACCESS_KEY_ID'] = 'k'
os.environ['R2_SECRET_ACCESS_KEY'] = 's'
assert r2.is_configured() is True

print('all resume/R2 self-checks passed')
