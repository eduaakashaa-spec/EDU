"""Assemble app/data/jee_mock/app.html: the EduAakashaa mock-centre stylesheet (shared with the UCEED centre) + the JEE app script."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(ROOT, 'app', 'data', 'uceed_mock', 'app.html'), encoding='utf-8').read()
js = open(os.path.join(HERE, 'jee_app.js'), encoding='utf-8').read()
head = src[:src.index('<body>')]
head = head.replace('EduAakashaa UCEED Mock Test Centre (members)', 'EduAakashaa JEE Main Mock Test Centre (members)').replace('<title>UCEED Mock Test Centre</title>', '<title>JEE Main Mock Test Centre</title>')
head = re.sub(r'  Upload this file together.*?-->', '  Served by the portal at /edupulse-jee/mock/app with its data under /edupulse-jee/mock/data/.\n-->', head, count=1, flags=re.S)
extra = '''
/* JEE additions: negative-marking tracker, pending papers, subject tabs */
.pos{color:var(--ok)}.neg{color:var(--bad)}
.negnote{margin:10px 0 0;padding:8px 12px;border-left:3px solid var(--bad);background:var(--bad-soft);border-radius:6px;font-size:13px}
.negpanel .scroll{overflow-x:auto}
.ntab{width:100%;border-collapse:collapse;font-size:13.5px;margin-top:10px}
.ntab th{background:var(--sunk);text-align:left;font-weight:700;padding:7px 9px;border-bottom:1px solid var(--line);white-space:nowrap}
.ntab td{padding:7px 9px;border-bottom:1px solid var(--line)}
.ntab .num{text-align:right;font-family:var(--f-mono)}
.negnotes{margin:12px 0 0;padding-left:18px;line-height:1.6}.negnotes li{margin:4px 0}
.negpanel .sm{font-size:12.5px;color:var(--muted);margin:6px 0 0}
.yr.pend{opacity:.7}
.tabs button{white-space:nowrap}
'''
head = head.replace('</style>\n\n</head>', extra + '</style>\n\n</head>')
assert extra in head, 'style block not found'
out = head + '<body>\n<div id="app"></div>\n\n<script>\n' + js + '\n</script>\n\n</body>\n</html>\n'
dst = os.path.join(ROOT, 'app', 'data', 'jee_mock', 'app.html')
open(dst, 'w', encoding='utf-8').write(out)
print('wrote', dst, len(out))
