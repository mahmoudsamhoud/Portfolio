from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
from collections import Counter

class Audit(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.ids, self.images = [], [], []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        self.refs.extend(a[k] for k in ('href', 'src') if k in a)
        if tag == 'img':
            self.images.append(a)

root = Path(__file__).resolve().parents[3]
pages = [root/'index.html', root/'assets/projects/Pr04-Orbit-Analyzer/summary.html', root/'assets/projects/Pr04-Orbit-Analyzer/work-08.html']
pages.extend(root/path for path in ['assets/projects/Pr01-ExtruCAD/work-06.html', 'assets/projects/Pr02-Motion-Analysis/work-07.html', 'assets/projects/Pr03-Nesting-Plates/work-05.html'])
errors = []
for p in pages:
    audit = Audit()
    audit.feed(p.read_text(encoding='utf-8'))
    errors.extend((p.name, 'duplicate id', k) for k,v in Counter(audit.ids).items() if v > 1)
    for ref in audit.refs:
        u = urlsplit(ref)
        if u.scheme or u.netloc:
            continue
        dest = (p.parent/unquote(u.path)).resolve() if u.path else p
        if not dest.exists():
            errors.append((p.name, ref, 'missing target'))
        elif u.fragment and dest.suffix == '.html':
            target = Audit()
            target.feed(dest.read_text(encoding='utf-8'))
            if u.fragment not in target.ids:
                errors.append((p.name, ref, 'missing anchor'))
    errors.extend((p.name, i.get('src'), 'missing alt') for i in audit.images if 'alt' not in i)
    print(p.name, len(audit.images), 'images;', len(audit.ids), 'unique IDs checked')
print('Errors:', errors)
assert not errors
for p in pages[1:]:
    content = p.read_text(encoding='utf-8')
    assert '<pre' not in content
    assert 'href="../../../orbit-analyzer/' not in content
    audit = Audit()
    audit.feed(content)
    assert not any(urlsplit(ref).path.endswith('.py') for ref in audit.refs)
print('All local links, anchors, image descriptions and IDs passed; no full-source links in project pages.')
