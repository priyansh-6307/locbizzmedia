"""Build the LOCBIZZ MEDIA static site. Python standard library; no framework required."""
from pathlib import Path
import html, json

ROOT=Path(__file__).parent
OUT=ROOT/'dist'
DATA=ROOT/'content'
projects=json.loads((DATA/'projects.json').read_text(encoding='utf-8'))
blogs=json.loads((DATA/'blogs.json').read_text(encoding='utf-8'))
e=html.escape
email='priyanshyadav364@gmail.com'
icon='<img class="brand-mark" src="/assets/locbizz-media-logo.png" alt="LOCBIZZ MEDIA">'
wordmark='<img class="wordmark" src="/assets/locbizz-media-logo.png" alt="LOCBIZZ MEDIA" width="1774" height="887">'

featured_projects=[
    {'title':'Kia Showcase','slug':'kia-showcase','description':'A cinematic Kia showcase built around precision, movement, and polished automotive detail.','date':'','vimeo':'/public/motion/2.mp4','video':'/public/motion/2.mp4','poster':'/assets/kia-showcase.jpg','logo':'/assets/kia-logo.svg','category':'Automotive','heading':'Kia, shaped by motion.','story':'A focused automotive visual built for a bold, modern reveal.','detailPath':'/#featured-work','route':'/projects/kia-showcase/'},
    {'title':'Audi - RS6','slug':'audi-rs6','description':'A high-energy Audi RS6 showcase with sharp surfaces, dramatic light, and controlled speed.','date':'','vimeo':'/public/motion/4.mp4','video':'/public/motion/4.mp4','poster':'/assets/audi-rs6.jpg','logo':'/assets/audi-logo.svg','category':'Automotive','heading':'Performance in every frame.','story':'A performance-led study in reflections, stance, and velocity.','detailPath':'/#featured-work','route':'/projects/audi-rs6/'},
    {'title':'Toyota Supra','slug':'toyota-supra','description':'A sleek Toyota Supra film driven by sculpted form, contrast, and kinetic camera movement.','date':'','vimeo':'/public/motion/8.mp4','video':'/public/motion/8.mp4','poster':'/assets/toyota-supra.jpg','logo':'/assets/toyota-logo.svg','category':'Automotive','heading':'A classic, reimagined.','story':'A stylized Supra showcase balancing iconic shape with contemporary motion.','detailPath':'/#featured-work','route':'/projects/toyota-supra/'},
    {'title':'Ford Mustang','slug':'ford-mustang','description':'A cinematic Ford Mustang showcase with muscular lines, deep shadows, and a confident presence.','date':'','vimeo':'/public/motion/3.mp4','video':'/public/motion/3.mp4','poster':'/assets/ford-mustang.jpg','logo':'/assets/ford-logo.svg','category':'Automotive','heading':'Built to make an entrance.','story':'A bold automotive portrait built around attitude, light, and movement.','detailPath':'/#featured-work'},
]

def form(contact=False):
    prefix='contact' if contact else 'footer'
    labels=lambda name: f'<label for="{prefix}-{name.lower()}">{name}</label>' if contact else ''
    return f'''<form class="inquiry {'contact-form' if contact else ''}" action="mailto:{email}" method="get">
    <h3>{'Send a message' if contact else 'Project Inquiries.'}</h3>
    <div class="form-row"><div>{labels('Name')}<input id="{prefix}-name" name="name" aria-label="Name" autocomplete="name" placeholder="Name" maxlength="120" required></div><div>{labels('Email')}<input id="{prefix}-email" name="email" aria-label="Email" type="email" autocomplete="email" placeholder="Email" maxlength="254" required></div></div>
    {labels('Message')}<textarea id="{prefix}-message" name="message" aria-label="Message" placeholder="Message" maxlength="5000" required></textarea>
    <div class="form-actions"><button class="send" type="submit">SEND ↗</button></div>
    <p class="form-note" role="status">Opens your email app to send your inquiry.</p></form>'''

def footer():
    return f'''<footer class="footer shell"><div class="footer-top"><a href="/" aria-label="LOCBIZZ MEDIA home">{icon}</a><a class="email-link" href="mailto:{email}">EMAIL ↗</a></div><div class="footer-main"><h4 class="footer-intro">Have a project in mind?<br>We'd love to hear from you.</h4>{form()}</div><div class="footer-bottom"><nav aria-label="Footer navigation"><a href="/contact/">Contact</a></nav><p>( ©26 LOCBIZZ MEDIA )</p></div></footer>'''

def page(content,title='LOCBIZZ MEDIA — CGI, VFX & AI Studio',path='/',kind='',show_footer=True):
    project_json=json.dumps((featured_projects+projects) if kind=='home' else projects).replace('<','\\u003c')
    nav=''.join(f'<a href="/{url}/"'+(' aria-current="page"' if path==f'/{url}/' else '')+f'>{label}</a>' for url,label in [('contact','CONTACT')])
    links=''.join(f'<a class="menu-link" href="{url}"><span>( _0{i} )</span><strong>{label}</strong></a>' for i,(url,label) in enumerate([('/','Home'),('/contact/','Contact')],1))
    return f'''<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title><meta name="description" content="LOCBIZZ MEDIA creative studio. Cinematic CGI, VFX and AI content for modern brands."><meta name="theme-color" content="#000000"><link rel="icon" type="image/svg+xml" href="/favicon.svg"><link rel="canonical" href="https://locbizz-studio.diskcuser.chatgpt.site{path}"><link rel="preload" href="/assets/inter-display-medium.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="/style.css"><script src="/app.js" defer></script></head><body class="{kind}"><a class="skip" href="#main">Skip to content</a>
    <header class="topbar"><a href="/" aria-label="LOCBIZZ MEDIA home">{icon}</a><nav class="toplinks" aria-label="Primary navigation">{nav}</nav><button class="menu-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="menu"><span></span><span></span></button></header>
    <div class="menu" id="menu" hidden><nav aria-label="Menu">{links}</nav><div class="menu-bottom"><a class="menu-email" href="mailto:{email}">{email}</a><span class="mono">LOCBIZZ MEDIA</span></div></div>
    <main id="main">{content}</main>{footer() if show_footer else ''}
    <dialog class="modal" id="project-modal" aria-labelledby="modal-title"><button class="modal-close" aria-label="Close preview">×</button><div class="modal-grid"><div><video class="modal-video" playsinline controls preload="none"></video><a class="modal-full" href="/#featured-work" target="_blank" rel="noopener noreferrer">WATCH FULL FILM ↗</a></div><div><img class="modal-logo" alt=""><h2 id="modal-title"></h2><p class="modal-description"></p><a class="modal-link" href="/#featured-work">BACK TO FEATURED WORK</a></div></div></dialog>
    <script id="project-data" type="application/json">{project_json}</script></body></html>'''

def card(p):
    return f'''<button class="project-card" data-project="{e(p['slug'])}" data-category="{p['category'].lower()}" aria-label="Open {e(p['title'])} preview"><img class="poster" src="{e(p['poster'])}" alt="{e(p['title'])}" width="1920" height="1080" loading="lazy"><video src="{e(p['video'])}" muted loop playsinline preload="none" aria-hidden="true"></video><img class="client-logo" src="{e(p['logo'])}" alt="" loading="lazy"><span class="project-label">{e(p['title'])}</span></button>'''

def grid(items):return '<div class="project-grid">'+''.join(card(p) for p in items)+'</div>'
def write(path,body,title,kind='',show_footer=True):
    target=OUT/path.strip('/')/'index.html' if path!='/' else OUT/'index.html'
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(page(body,title,path,kind,show_footer),encoding='utf-8')

motion_clips=['/public/motion/1.mov','/public/motion/2.mp4','/public/motion/3.mp4','/public/motion/4.mp4','/public/motion/5.mp4','/public/motion/6.mov','/public/motion/7.mp4']
reels=''.join(f'<div class="reel-panel"><video src="{clip}" muted loop playsinline preload="metadata" aria-hidden="true"></video></div>' for clip in motion_clips*2)
home=f'''<section class="hero"><div class="hero-brand">{wordmark}<h1 class="hero-tagline">Creative studio. CGI, VFX &amp; AI.</h1></div><div class="reel-window"><div class="reel-track">{reels}</div><a href="#featured-work" class="scroll-cue" aria-label="Explore featured work"></a></div><button class="motion-toggle" aria-pressed="false">PAUSE MOTION</button></section><section class="work shell" id="featured-work"><h2>Featured Work.</h2>{grid(featured_projects)}</section>'''
write('/',home,'LOCBIZZ MEDIA — CGI, VFX & AI Studio','home')
write('/contact/',f'<section class="contact-page shell"><div class="contact-heading reveal"><h1>Got a project in mind? Let’s chat and bring it to life.</h1></div><div class="contact-body"><div><h4>Get in touch</h4><a class="email-link" href="mailto:{email}">{email}</a></div>{form(True)}</div></section>','Contact — LOCBIZZ MEDIA',show_footer=False)

kia_dir=OUT/'public'/'KIa'
kia_videos=sorted((path for path in kia_dir.iterdir() if path.suffix.lower() in {'.mp4','.mov'}),key=lambda path:int(path.stem))
kia_items=''.join(f'<article class="kia-video-card"><video src="/public/KIa/{video.name}" autoplay muted loop controls playsinline preload="metadata"></video><p class="mono">KIA SHOWCASE / {int(video.stem):02d}</p></article>' for video in kia_videos)
kia_body=f'''<article class="project-detail shell kia-project"><div class="project-intro"><h1>Kia Showcase</h1><div><p>A cinematic study of Kia design, motion, and performance.</p><a class="modal-link" href="/#featured-work">← BACK TO FEATURED WORK</a></div></div><section class="kia-video-grid" aria-label="Kia Showcase videos">{kia_items}</section></article>'''
write('/projects/kia-showcase/',kia_body,'Kia Showcase — LOCBIZZ MEDIA')

audi_dir=OUT/'public'/'audi'
audi_videos=sorted((path for path in audi_dir.iterdir() if path.suffix.lower() in {'.mp4','.mov'}),key=lambda path:int(path.stem))
audi_items=''.join(f'<article class="audi-video-card"><video src="/public/audi/{video.name}" autoplay muted loop controls playsinline preload="metadata"></video><p class="mono">AUDI RS6 / {int(video.stem):02d}</p></article>' for video in audi_videos)
audi_body=f'''<article class="project-detail shell audi-project"><div class="project-intro"><h1>Audi - RS6</h1><div><p>A performance-led Audi RS6 film built from speed, light, and precision.</p><a class="modal-link" href="/#featured-work">← BACK TO FEATURED WORK</a></div></div><section class="audi-video-grid" aria-label="Audi RS6 videos">{audi_items}</section></article>'''
write('/projects/audi-rs6/',audi_body,'Audi - RS6 — LOCBIZZ MEDIA')

supra_dir=OUT/'public'/'supra'
supra_images=sorted(supra_dir.glob('*'),key=lambda path:int(path.stem.rsplit('(',1)[1].rstrip(')')))
supra_items=''.join(f'<figure class="supra-image-card"><img src="/public/supra/{image.name.replace(" ","%20").replace("(","%28").replace(")","%29")}" alt="Toyota Supra frame {index}" loading="lazy"><figcaption class="mono">SUPRA / {index:02d}</figcaption></figure>' for index,image in enumerate(supra_images,2))
supra_body=f'''<article class="project-detail shell supra-project"><div class="project-intro"><h1>Toyota Supra</h1><div><p>A cinematic Toyota Supra film followed by selected frames from the build.</p><a class="modal-link" href="/#featured-work">← BACK TO FEATURED WORK</a></div></div><iframe class="supra-film" src="https://www.youtube-nocookie.com/embed/qKkCl0MyXwU?autoplay=1&amp;mute=1&amp;playsinline=1&amp;rel=0" title="Toyota Supra film" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe><section class="supra-image-grid" aria-label="Toyota Supra frames">{supra_items}</section></article>'''
write('/projects/toyota-supra/',supra_body,'Toyota Supra — LOCBIZZ MEDIA')

(OUT/'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" rx="9"/><rect x="6" y="5" width="28" height="30" rx="6" fill="none" stroke="white" stroke-width="2.5"/><path d="M14 12v16h12M24 13h3v10h-7" fill="none" stroke="white" stroke-width="2.5"/></svg>',encoding='utf-8')
(OUT/'404.html').write_text(page('<section class="contact-page shell"><h1>Page not found.</h1><p style="margin-top:35px"><a class="modal-link" href="/">BACK TO LOCBIZZ MEDIA →</a></p></section>','Page not found — LOCBIZZ MEDIA',show_footer=False),encoding='utf-8')
print('Built',len(list(OUT.rglob('*.html'))),'HTML pages.')
