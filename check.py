"""Check generated routes, internal links, assets, branding and excluded content."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json
root=Path(__file__).parent/'dist'
class Links(HTMLParser):
    def handle_starttag(self,tag,attrs):
        for name,value in attrs:
            if name not in ('href','src') or not value or not value.startswith('/'):continue
            target=root/unquote(urlsplit(value).path).lstrip('/')
            if target.is_dir():target=target/'index.html'
            assert target.exists(),f'Missing {value} in {self.file}'
parser=Links()
pages=list(root.rglob('*.html'))
assert len(pages)==26,len(pages)
for file in pages:
    text=file.read_text(encoding='utf-8')
    assert 'Lunchbox' not in text and 'lunchbox' not in text,file
    assert 'Already Trusted' not in text,file
    parser.file=file;parser.feed(text)
projects=json.loads((root.parent/'content/projects.json').read_text(encoding='utf-8'))
assert len(projects)==12 and len({x['slug'] for x in projects})==12
assert {x['category'] for x in projects}=={'Automotive','Gaming','Product'}
print(f'PASS: {len(pages)} pages, all internal routes and assets, project data, LOCBIZZ branding, excluded section.')
