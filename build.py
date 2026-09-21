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
    return f'''<footer class="footer shell"><div class="footer-top"><a href="/" aria-label="LOCBIZZ MEDIA home">{icon}</a><a class="email-link" href="mailto:{email}">EMAIL ↗</a></div><div class="footer-main"><h4 class="footer-intro">Have a project in mind?<br>We'd love to hear from you.</h4>{form()}</div><div class="footer-bottom"><nav aria-label="Footer navigation"><a href="/projects/">Projects</a><a href="/about/">About</a><a href="/contact/">Contact</a></nav><p>( ©26 LOCBIZZ MEDIA )</p></div></footer>'''

def page(content,title='LOCBIZZ MEDIA — CGI, VFX & AI Studio',path='/',kind='',show_footer=True):
    project_json=json.dumps(projects).replace('<','\\u003c')
    nav=''.join(f'<a href="/{url}/"'+(' aria-current="page"' if path==f'/{url}/' else '')+f'>{label}</a>' for url,label in [('projects','PROJECTS'),('about','ABOUT'),('contact','CONTACT')])
    links=''.join(f'<a class="menu-link" href="{url}"><span>( _0{i} )</span><strong>{label}</strong></a>' for i,(url,label) in enumerate([('/','Home'),('/projects/','Works'),('/about/','About'),('/blog/','Blog'),('/contact/','Contact')],1))
    return f'''<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title><meta name="description" content="LOCBIZZ MEDIA creative studio. Cinematic CGI, VFX and AI content for modern brands."><meta name="theme-color" content="#000000"><link rel="icon" type="image/svg+xml" href="/favicon.svg"><link rel="canonical" href="https://locbizz-studio.diskcuser.chatgpt.site{path}"><link rel="preload" href="/assets/inter-display-medium.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="/style.css"><script src="/app.js" defer></script></head><body class="{kind}"><a class="skip" href="#main">Skip to content</a>
    <header class="topbar"><a href="/" aria-label="LOCBIZZ MEDIA home">{icon}</a><nav class="toplinks" aria-label="Primary navigation">{nav}</nav><button class="menu-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="menu"><span></span><span></span></button></header>
    <div class="menu" id="menu" hidden><nav aria-label="Menu">{links}</nav><div class="menu-bottom"><a class="menu-email" href="mailto:{email}">{email}</a><span class="mono">LOCBIZZ MEDIA</span></div></div>
    <main id="main">{content}</main>{footer() if show_footer else ''}
    <dialog class="modal" id="project-modal" aria-labelledby="modal-title"><button class="modal-close" aria-label="Close preview">×</button><div class="modal-grid"><div><video class="modal-video" playsinline controls preload="none"></video><a class="modal-full" href="/projects/" target="_blank" rel="noopener noreferrer">WATCH FULL FILM ↗</a></div><div><img class="modal-logo" alt=""><h2 id="modal-title"></h2><p class="modal-description"></p><a class="modal-link" href="/projects/">FULL PROJECT</a></div></div></dialog>
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
home=f'''<section class="hero"><div class="hero-brand">{wordmark}<h1 class="hero-tagline">Creative studio. CGI, VFX &amp; AI.</h1></div><div class="reel-window"><div class="reel-track">{reels}</div><a href="#featured-work" class="scroll-cue" aria-label="Explore featured work"></a></div><button class="motion-toggle" aria-pressed="false">PAUSE MOTION</button></section><section class="work shell" id="featured-work"><h2>Featured Work.</h2>{grid(projects[:6])}<div class="all-projects"><a href="/projects/">View All Projects&nbsp; -&gt;</a></div></section>'''
write('/',home,'LOCBIZZ MEDIA — CGI, VFX & AI Studio','home')
filters=''.join(f'<a data-filter="{name.lower()}" href="/projects/{"?category="+name.lower() if name!="All" else ""}" aria-current="{str(name=="All").lower()}">{name}</a>' for name in ['All','Automotive','Gaming','Product'])
write('/projects/',f'<div class="shell"><div class="page-heading projects-heading reveal"><h1>Projects.</h1><nav class="filters" aria-label="Project categories">{filters}</nav></div><section class="work"><p class="filter-count" role="status" aria-live="polite">12 projects</p>{grid(projects)}</section></div>','Projects — LOCBIZZ MEDIA','projects-page')
about='''<section class="about-hero"><video src="https://framerusercontent.com/assets/AGFM8JWT8BuczHUVcPxzdzqiqk.mp4" poster="/assets/about-poster.jpg" muted loop playsinline preload="metadata" aria-hidden="true"></video><h1>We’re LOCBIZZ MEDIA — a creative studio blending CGI, AI, and emerging technology to create next-generation visual content.</h1></section><section class="about-story shell">'''+icon+'''<h4>Filmmaking is at the heart of our approach. We bring together cinematic storytelling, 3D craft, and new production tools to turn ambitious ideas into images that move people.<br><br>From automotive films to product worlds, we explore what’s possible at the meeting point of imagination and technology.</h4></section>'''
write('/about/',about,'About — LOCBIZZ MEDIA')
write('/contact/',f'<section class="contact-page shell"><div class="contact-heading reveal"><h1>Got a project in mind? Let’s chat and bring it to life.</h1></div><div class="contact-body"><div><h4>Get in touch</h4><a class="email-link" href="mailto:{email}">{email}</a></div>{form(True)}</div></section>','Contact — LOCBIZZ MEDIA',show_footer=False)

for i,p in enumerate(projects):
    more=[x for x in projects if x['slug']!=p['slug']][:2]
    body=f'''<article class="project-detail shell"><iframe class="detail-video" src="{e(p['embed'])}" title="{e(p['title'])} — full film" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen loading="lazy"></iframe><div class="project-intro"><h1>{e(p['title'])}</h1><div><p>{e(p['description'])}</p><a class="modal-link" href="{e(p['vimeo'])}" target="_blank" rel="noopener noreferrer">WATCH FULL FILM ↗</a></div></div><div class="project-story"><h3>{e(p.get('heading','Behind the film.'))}</h3><p>{e(p.get('story',p['description']))}</p></div><section class="work"><h2>More projects.</h2>{grid(more)}</section></article>'''
    write('/projects/'+p['slug']+'/',body,p['title']+' — LOCBIZZ MEDIA')

def blog_card(b):return f'<a class="blog-card" href="{e(b["path"])}/"><img src="{e(b["image"])}" alt="{e(b["title"])}" width="1000" height="690" loading="lazy"><time>{e(b["date"])}</time><h2>{e(b["title"])}</h2></a>'
blog_body='<div class="shell"><div class="page-heading blog-intro reveal"><h1>Creative Dispatch</h1><p>Every color, word, and pixel comes from a clear strategy built to help you grow.</p></div><section class="blog-grid">'+''.join(blog_card(b) for b in blogs)+'</section></div>'
write('/blog/',blog_body,'Creative Dispatch — LOCBIZZ MEDIA')
for b in blogs:
    copy=''.join(f'<h2>{e(section[0])}</h2><p>{e(section[1])}</p>' for section in b['sections'])
    article=f'<article class="article shell"><header class="article-header"><time class="mono">{e(b["date"])}</time><h1>{e(b["title"])}</h1></header><img class="article-image" src="{e(b["image"])}" alt="{e(b["title"])}"><div class="article-copy">{copy}<a href="/blog/">← BACK TO DISPATCH</a></div></article>'
    write(b['path']+'/',article,b['title']+' — LOCBIZZ MEDIA')
(OUT/'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" rx="9"/><rect x="6" y="5" width="28" height="30" rx="6" fill="none" stroke="white" stroke-width="2.5"/><path d="M14 12v16h12M24 13h3v10h-7" fill="none" stroke="white" stroke-width="2.5"/></svg>',encoding='utf-8')
(OUT/'404.html').write_text(page('<section class="contact-page shell"><h1>Page not found.</h1><p style="margin-top:35px"><a class="modal-link" href="/">BACK TO LOCBIZZ MEDIA →</a></p></section>','Page not found — LOCBIZZ MEDIA',show_footer=False),encoding='utf-8')
print('Built',len(list(OUT.rglob('*.html'))),'HTML pages.')
