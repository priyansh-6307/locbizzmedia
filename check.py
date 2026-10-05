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
assert len(pages)==7,len(pages)
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
assert home.count('class="project-card"')==5
assert 'data-project="bmw-showcase"' in home and '/assets/bmwshowcase.webp' in home
assert '"route": "/projects/bmw-showcase/"' in home
for title,clip,logo in [('Kia Showcase','/public/motion/2.mp4','/assets/kia-logo.svg'),('Audi - RS6','/public/motion/4.mp4','/assets/audi-logo.svg'),('Toyota Supra','/public/motion/8.mp4','/assets/toyota-logo.svg'),('Ford Mustang','/public/motion/3.mp4','/assets/ford-logo.svg')]:
    assert title in home and clip in home and logo in home
    assert (root/clip.lstrip('/')).exists(), f'Missing featured clip {clip}'
    assert (root/logo.lstrip('/')).exists(), f'Missing featured logo {logo}'
motion=[f'/public/motion/{i}.mp4' for i in range(1,12)]
hero=home.split('<section class="work shell"',1)[0]
assert hero.count('class="reel-panel"')==len(motion)*2
assert all(hero.find(motion[i]) < hero.find(motion[i+1]) for i in range(len(motion)-1))
for clip in motion: assert hero.count(clip)==2, f'Motion clip is not repeated for a seamless loop: {clip}'
style=(root/'style.css').read_text(encoding='utf-8')
assert 'cursor:grab' in style and 'transform:translate3d(var(--reel-x,-230px),0,0)' in style
app=(root/'app.js').read_text(encoding='utf-8')
assert "reelWindow.addEventListener('pointerdown'" in app and "reelWindow.addEventListener('pointermove'" in app
for clip in motion:
    assert (root/clip.lstrip('/')).exists(), f'Missing motion clip {clip}'
kia=(root/'projects'/'kia-showcase'/'index.html').read_text(encoding='utf-8')
kia_clips=[f'/public/KIa/{i}.mp4' for i in range(1,13)]
assert kia.count('class="kia-video-card"')==12
assert kia.count('muted loop controls playsinline preload="none" data-autoplay="true"')==12
assert all(kia.find(kia_clips[i]) < kia.find(kia_clips[i+1]) for i in range(11))
for clip in kia_clips: assert (root/clip.lstrip('/')).exists(), f'Missing Kia clip {clip}'
audi=(root/'projects'/'audi-rs6'/'index.html').read_text(encoding='utf-8')
audi_clips=[f'/public/audi/{i}.mp4' for i in range(1,7)]
assert audi.count('class="audi-video-card"')==6
assert audi.count('muted loop controls playsinline preload="none" data-autoplay="true"')==6
assert all(audi.find(audi_clips[i]) < audi.find(audi_clips[i+1]) for i in range(5))
for clip in audi_clips: assert (root/clip.lstrip('/')).exists(), f'Missing Audi clip {clip}'
bmw=(root/'projects'/'bmw-showcase'/'index.html').read_text(encoding='utf-8')
bmw_clips=[f'/public/bmw/{i}.mp4' for i in range(1,9)]
assert bmw.count('class="bmw-video-card"')==8
assert bmw.count('muted loop controls playsinline preload="none" data-autoplay="true"')==8
assert all(bmw.find(bmw_clips[i]) < bmw.find(bmw_clips[i+1]) for i in range(7))
assert 'video[data-autoplay="true"]' in app
for clip in bmw_clips: assert (root/clip.lstrip('/')).exists(), f'Missing BMW clip {clip}'
supra=(root/'projects'/'toyota-supra'/'index.html').read_text(encoding='utf-8')
supra_images=[f'/public/supra/New%20Project%20%28{i}%29.webp' for i in range(2,7)]
assert 'youtube-nocookie.com/embed/qKkCl0MyXwU?autoplay=1&amp;mute=1' in supra
assert supra.count('class="supra-image-card"')==5
assert all(supra.find(supra_images[i]) < supra.find(supra_images[i+1]) for i in range(4))
for image in supra_images: assert (root/unquote(image.lstrip('/'))).exists(), f'Missing Supra image {image}'
print(f'PASS: {len(pages)} pages, all internal routes and assets, project data, LOCBIZZ branding, excluded section.')
