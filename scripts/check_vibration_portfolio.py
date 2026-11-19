"""Check new report links, anchors, image descriptions and project separation."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from collections import Counter
import subprocess

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids, self.refs, self.labels, self.images = [], [], [], []
        self.feed(path.read_text(encoding='utf-8'))

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        self.refs.extend(a[k] for k in ('href', 'src') if k in a)
        self.labels.extend(a.get('aria-controls', '').split())
        self.labels.extend(a.get('aria-labelledby', '').split())
        if tag == 'img':
            self.images.append(a)


folders = [p for p in (ROOT/'assets/projects').iterdir() if p.name.startswith(('Pr06-', 'Pr07-', 'Pr08-'))]
assert len(folders) == 3
pages = [ROOT/'index.html'] + [p for folder in folders for p in folder.glob('*.html')]
assert len(pages) == 7
for path in pages:
    page = Page(path)
    assert all(count == 1 for count in Counter(page.ids).values()), f'Duplicate IDs: {path}'
    assert all(label in page.ids for label in page.labels), f'Missing ARIA target: {path}'
    assert all('alt' in img for img in page.images), f'Missing image alt: {path}'
    for ref in page.refs:
        url = urlsplit(ref)
        if url.scheme or url.netloc:
            continue
        target = (path.parent/unquote(url.path)).resolve() if url.path else path
        assert target.exists(), f'Missing target: {path} -> {ref}'
        if target.suffix == '.html' and url.fragment:
            assert url.fragment in Page(target).ids, f'Missing anchor: {path} -> {ref}'
for folder in folders:
    for p in folder.rglob('*'):
        assert p.is_file() and p.suffix in ('.html', '.png'), f'Non-presentation artifact: {p}'
assert not list((ROOT/'assets/projects').rglob('.git'))
gitlinks = [line for line in subprocess.check_output(['git', 'ls-files', '--stage'], cwd=ROOT, text=True).splitlines() if line.startswith('160000')]
assert not gitlinks, gitlinks
print('PASS: 7 pages, local links and anchors, unique IDs, image alt text, ARIA targets, 3 documentation-only folders, no nested Git or gitlinks.')
