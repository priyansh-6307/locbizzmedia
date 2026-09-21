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
assert len(pages)==3,len(pages)
for file in pages:
    text=file.read_text(encoding='utf-8')
    assert 'Lunchbox' not in text and 'lunchbox' not in text,file
    assert 'Already Trusted' not in text,file
    parser.file=file;parser.feed(text)
projects=json.loads((root.parent/'content/projects.json').read_text(encoding='utf-8'))
assert len(projects)==12 and len({x['slug'] for x in projects})==12
assert {x['category'] for x in projects}=={'Automotive','Gaming','Product'}
home=(root/'index.html').read_text(encoding='utf-8')
for removed_route in ('/projects/','/about/','/blog/'):
    assert f'href="{removed_route}"' not in home, f'Exposed removed route {removed_route}'
assert home.count('class="project-card"')==4
for title,clip,logo in [('Kia Showcase','/public/motion/2.mp4','/assets/kia-logo.svg'),('Audi - RS6','/public/motion/4.mp4','/assets/audi-logo.svg'),('Toyota Supra','/public/motion/8.mp4','/assets/toyota-logo.svg'),('Ford Mustang','/public/motion/3.mp4','/assets/ford-logo.svg')]:
    assert title in home and clip in home and logo in home
    assert (root/clip.lstrip('/')).exists(), f'Missing featured clip {clip}'
    assert (root/logo.lstrip('/')).exists(), f'Missing featured logo {logo}'
motion=['/public/motion/1.mov','/public/motion/2.mp4','/public/motion/3.mp4','/public/motion/4.mp4','/public/motion/5.mp4','/public/motion/6.mov','/public/motion/7.mp4']
assert home.count('class="reel-panel"')==14
assert home.find(motion[0]) < home.find(motion[1]) < home.find(motion[2]) < home.find(motion[3]) < home.find(motion[4]) < home.find(motion[5]) < home.find(motion[6])
for clip in motion:
    assert (root/clip.lstrip('/')).exists(), f'Missing motion clip {clip}'
print(f'PASS: {len(pages)} pages, all internal routes and assets, project data, LOCBIZZ branding, excluded section.')
