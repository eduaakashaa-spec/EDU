"""Stack a question's stem and option images into one PNG for a quick look. python tools/iat/sheet.py <dir> <year> <prefix> <out.png>"""
import json
import os
import sys
from PIL import Image

d, year, pre, out = sys.argv[1:5]
base = os.path.join(d, year)
fs = [pre + '_s.webp'] + ['%s_o%d.webp' % (pre, i) for i in range(4)]
fs = [f for f in fs if os.path.exists(os.path.join(base, f))] or [f for f in os.listdir(base) if f.startswith(pre + '_full')]
ims = [Image.open(os.path.join(base, f)).convert('RGB') for f in fs]
w = max(i.width for i in ims)
h = sum(i.height + 12 for i in ims)
c = Image.new('RGB', (w, h), (225, 225, 225))
y = 0
for i in ims:
    c.paste(i, (0, y))
    y += i.height + 12
c.save(out)
