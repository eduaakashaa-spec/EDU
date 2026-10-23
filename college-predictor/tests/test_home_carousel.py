"""Homepage banner carousel: six linked slides at the top, assets present, links resolve. Run: python tests/test_home_carousel.py"""
import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')
from app import create_app

app = create_app()
app.config['TESTING'] = True
c = app.test_client()
page = c.get('/').get_data(as_text=True)
assert 'class="hc"' in page and page.count('class="hc-slide"') == 6 and 'aria-roledescription="carousel"' in page
assert page.index('class="hc"') < page.index('class="aw-hero"') if 'class="aw-hero"' in page else True       # carousel is above the hero
assert 'css/home_carousel.css' in page and 'js/home_carousel.js' in page
slides = re.findall(r'<a class="hc-slide" href="([^"]+)".*?<img src="([^"]+)".*?alt="([^"]+)"', page, re.S)
assert len(slides) == 6 and all(len(alt) > 30 for _, _, alt in slides)                                             # real descriptions, not empty alt
for href, src, _alt in slides:
    assert c.get(href).status_code in (200, 302), href                                                          # every slide leads somewhere that works
    r = c.get(src)
    assert r.status_code == 200 and r.mimetype == 'image/webp' and len(r.data) > 20_000, src
for asset in ('/static/css/home_carousel.css', '/static/js/home_carousel.js'):
    assert c.get(asset).status_code == 200
assert page.count('fetchpriority="high"') == 1 and page.count('loading="lazy"') >= 5                              # only the first slide is eager
try:
    os.unlink(_db)
except OSError:
    pass
print('home carousel checks passed')
