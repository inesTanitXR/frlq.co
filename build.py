#!/usr/bin/env python3
"""Build frlq.co — full rebuild, aligned with the 2026 Ameren deck story.

Outputs:
  docs/        — index.html, 404.html, assets/ (GitHub Pages ready)
  preview.html — single-file version with data-URI images (artifact preview)

Brand: Froliq logo purple #9b02ff -> blue #20bdff.
Type:  Bricolage Grotesque (display) / Instrument Sans (body) / IBM Plex Mono (labels).
"""
import base64, os, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, 'assets')
OUT = os.path.join(ROOT, 'docs')

LOGO_SVG = open(os.path.join(ASSETS, 'froliq-logo.svg')).read()
# make the inline logo scale + drop fixed ids that could collide
LOGO_SVG = LOGO_SVG.replace('id="Layer_1-534353042"', 'class="logo-mark" aria-hidden="true"')

TYPEFORM = "https://zpryme.typeform.com/to/sZe6vb"

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Instrument+Sans:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">'

CSS = r"""
:root{
  --ground:#f7f5fc; --card:#ffffff; --card-2:#f1ecfa;
  --ink:#191036; --body:#4a4066; --muted:#8b81a6; --line:#e5dff2;
  --purple:#9b02ff; --blue:#20bdff;
  --purple-soft:#f2e4ff; --blue-soft:#e0f6ff;
  --grad:linear-gradient(115deg,#9b02ff 10%,#20bdff 90%);
  --shadow:0 14px 40px rgba(45,20,90,.10);
  --nav-bg:rgba(247,245,252,.82);
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --ground:#0f0a1e; --card:#191131; --card-2:#211846;
    --ink:#f3eeff; --body:#c9c0e2; --muted:#8d82ab; --line:#2c2350;
    --purple:#bb5cff; --blue:#4fcbff;
    --purple-soft:#2c1a4d; --blue-soft:#122c44;
    --grad:linear-gradient(115deg,#bb5cff 10%,#4fcbff 90%);
    --shadow:0 14px 40px rgba(0,0,0,.45);
    --nav-bg:rgba(15,10,30,.82);
  }
}
:root[data-theme="dark"]{
  --ground:#0f0a1e; --card:#191131; --card-2:#211846;
  --ink:#f3eeff; --body:#c9c0e2; --muted:#8d82ab; --line:#2c2350;
  --purple:#bb5cff; --blue:#4fcbff;
  --purple-soft:#2c1a4d; --blue-soft:#122c44;
  --grad:linear-gradient(115deg,#bb5cff 10%,#4fcbff 90%);
  --shadow:0 14px 40px rgba(0,0,0,.45);
  --nav-bg:rgba(15,10,30,.82);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0;background:var(--ground);color:var(--body);
  font-family:"Instrument Sans",-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;
  font-size:17px;line-height:1.65;
}
h1,h2,h3{font-family:"Bricolage Grotesque","Instrument Sans",Helvetica,sans-serif;color:var(--ink);letter-spacing:-.015em;line-height:1.12;text-wrap:balance;margin:0 0 14px}
h1{font-size:clamp(40px,6vw,68px);font-weight:800}
h2{font-size:clamp(28px,3.6vw,40px);font-weight:800}
h3{font-size:20px;font-weight:700}
p{margin:0 0 14px}
a{color:var(--ink)}
img{max-width:100%;display:block}
.wrap{max-width:1120px;margin:0 auto;padding:0 24px}
.mono{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace}
.eyebrow{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--purple);margin:0 0 14px}
.grad-text{background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
section{padding:88px 0}
.sec-head{max-width:640px;margin-bottom:44px}
.sec-head p{color:var(--body)}

/* nav */
.nav{position:sticky;top:0;z-index:50;background:var(--nav-bg);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
.nav-in{display:flex;align-items:center;gap:26px;height:66px}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;margin-right:auto}
.brand svg{height:30px;width:auto}
.brand b{font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:21px;letter-spacing:.01em;background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.nav a.lnk{text-decoration:none;color:var(--body);font-weight:500;font-size:15px}
.nav a.lnk:hover{color:var(--ink)}
.btn{display:inline-block;padding:12px 22px;border-radius:999px;font-weight:600;font-size:15.5px;text-decoration:none;transition:transform .15s ease,box-shadow .15s ease}
.btn:active{transform:scale(.98)}
.btn-grad{background:var(--grad);color:#fff;box-shadow:0 6px 20px rgba(155,2,255,.28)}
.btn-grad:hover{transform:translateY(-1px);box-shadow:0 10px 26px rgba(155,2,255,.36)}
.btn-ghost{border:1.5px solid var(--line);color:var(--ink);background:var(--card)}
.btn-ghost:hover{border-color:var(--purple)}
.nav .btn{padding:9px 18px}
@media(max-width:860px){.nav a.lnk{display:none}}

/* hero */
.hero{position:relative;padding:96px 0 72px;overflow:hidden}
.hero::before{content:"";position:absolute;inset:0;z-index:-1;
  background-image:radial-gradient(var(--line) 1.2px, transparent 1.2px);
  background-size:26px 26px;
  -webkit-mask-image:radial-gradient(720px 460px at 74% 10%,#000 0%,transparent 72%);
  mask-image:radial-gradient(720px 460px at 74% 10%,#000 0%,transparent 72%);
}
.hero::after{content:"";position:absolute;z-index:-2;width:560px;height:560px;right:-160px;top:-220px;border-radius:50%;
  background:radial-gradient(closest-side,var(--purple-soft),transparent 70%)}
.hero h1{max-width:760px}
.hero .lede{font-size:19.5px;max-width:620px;color:var(--body)}
.hero-cta{display:flex;gap:14px;flex-wrap:wrap;margin:30px 0 0}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:64px}
.stat{border-top:2.5px solid transparent;border-image:var(--grad) 1;padding-top:16px}
.stat b{display:block;font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:32px;color:var(--ink);font-variant-numeric:tabular-nums}
.stat span{font-size:13.5px;color:var(--muted)}
@media(max-width:860px){.stats{grid-template-columns:repeat(2,1fr)}}

/* clients */
.clients{padding:34px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.clients .label{text-align:center;font-family:"IBM Plex Mono",monospace;font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);margin-bottom:18px}
.chip-row{display:flex;flex-wrap:wrap;justify-content:center;gap:10px 12px}
.chip{font-family:"Bricolage Grotesque",sans-serif;font-weight:700;font-size:15.5px;color:var(--ink);
  padding:8px 18px;border:1.5px solid var(--line);border-radius:999px;background:var(--card)}

/* services */
.svc-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.svc{background:var(--card);border:1px solid var(--line);border-radius:20px;padding:26px 24px;display:flex;flex-direction:column;gap:8px}
.svc .num{font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--muted);letter-spacing:.1em}
.svc h3{margin:2px 0 2px}
.svc p{font-size:15.5px;margin:0;color:var(--body)}
.svc .tag{margin-top:auto;padding-top:14px;font-family:"IBM Plex Mono",monospace;font-size:12.5px;color:var(--purple)}
.svc:nth-child(1){grid-column:span 2;background:linear-gradient(135deg,var(--purple-soft),var(--card) 55%)}
@media(max-width:860px){.svc-grid{grid-template-columns:1fr}.svc:nth-child(1){grid-column:auto}}

/* featured work */
.work-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.work{background:var(--card);border:1px solid var(--line);border-radius:20px;position:relative;overflow:hidden;display:flex;flex-direction:column}
.work::after{content:"";position:absolute;left:0;right:0;top:0;height:4px;background:var(--grad);opacity:0;transition:opacity .2s}
.work:hover::after{opacity:1}
.work>img{width:100%;aspect-ratio:16/9;object-fit:cover}
.work .body{padding:22px 24px 24px;display:flex;flex-direction:column;flex:1;gap:0}
.work .client{font-family:"IBM Plex Mono",monospace;font-size:12.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--blue)}
.work h3{font-size:23px;margin:8px 0 8px}
.work p{font-size:15.5px;margin:0 0 16px}
.work .pills{margin-top:auto}
.pill{display:inline-block;font-family:"IBM Plex Mono",monospace;font-size:12.5px;color:var(--ink);
  background:var(--card-2);border-radius:999px;padding:6px 13px;margin:0 6px 6px 0}
a.pill-watch{background:var(--grad);color:#fff;text-decoration:none}
.work-hero{grid-column:1/-1;flex-direction:row}
.work-hero>img{width:44%;aspect-ratio:auto;min-height:100%}
.work-hero .body{padding:30px 32px}
.work-hero h3{font-size:28px}
@media(max-width:860px){.work-grid{grid-template-columns:1fr}.work-hero{flex-direction:column}.work-hero>img{width:100%;aspect-ratio:16/9;min-height:0}}

/* app library */
.lib{background:var(--card-2);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.lib-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.app{background:var(--card);border:1px solid var(--line);border-radius:16px;overflow:hidden;transition:transform .18s ease,box-shadow .18s ease;text-decoration:none;display:block}
.app:hover{transform:translateY(-3px);box-shadow:var(--shadow)}
.app .shot{position:relative}
.app img{aspect-ratio:4/3;object-fit:cover;width:100%}
.app .play{position:absolute;right:10px;bottom:10px;width:36px;height:36px;border-radius:50%;
  background:rgba(15,10,30,.72);color:#fff;display:grid;place-items:center;font-size:13px;padding-left:2px}
.app:hover .play{background:var(--purple)}
.app .meta{padding:13px 15px;display:flex;align-items:center;justify-content:space-between;gap:8px}
.app .meta b{font-size:14.5px;color:var(--ink);font-weight:600;line-height:1.3}
.app .xr{flex:none;font-family:"IBM Plex Mono",monospace;font-size:11px;padding:3px 9px;border-radius:999px;color:#fff;background:var(--purple)}
.app .xr.ar{background:var(--blue)}
@media(max-width:980px){.lib-grid{grid-template-columns:repeat(2,1fr)}}

/* process */
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;counter-reset:step}
.step{position:relative;background:var(--card);border:1px solid var(--line);border-radius:20px;padding:24px}
.step::before{counter-increment:step;content:"0" counter(step);
  font-family:"IBM Plex Mono",monospace;font-size:13px;font-weight:500;
  background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.step h3{font-size:18.5px;margin:10px 0 6px}
.step p{font-size:15px;margin:0;color:var(--body)}
@media(max-width:860px){.steps{grid-template-columns:1fr}}

/* about / team */
.about-grid{display:grid;grid-template-columns:1.1fr .9fr;gap:48px;align-items:start}
.team{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.member{display:flex;gap:13px;align-items:center;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:14px 16px}
.member .av{flex:none;width:46px;height:46px;border-radius:50%;background:var(--grad);color:#fff;display:grid;place-items:center;
  font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:16px}
.member b{display:block;color:var(--ink);font-size:15.5px}
.member span{font-size:13.5px;color:var(--muted)}
@media(max-width:860px){.about-grid{grid-template-columns:1fr}.team{grid-template-columns:1fr}}

/* contact */
.cta{background:var(--ink);border-radius:28px;padding:64px 40px;text-align:center;position:relative;overflow:hidden}
.cta::before{content:"";position:absolute;inset:0;
  background-image:radial-gradient(rgba(255,255,255,.14) 1.2px, transparent 1.2px);background-size:24px 24px;
  -webkit-mask-image:radial-gradient(500px 320px at 50% 0%,#000,transparent 75%);
  mask-image:radial-gradient(500px 320px at 50% 0%,#000,transparent 75%)}
:root[data-theme="dark"] .cta{background:var(--card)}
.cta h2{color:#fff;position:relative}
:root[data-theme="dark"] .cta h2{color:var(--ink)}
.cta p{color:#cfc5ea;max-width:520px;margin:0 auto 26px;position:relative}
.cta .btn{position:relative}
.socials{display:flex;justify-content:center;gap:20px;margin-top:26px;position:relative}
.socials a{color:#cfc5ea;font-size:14px;text-decoration:none;font-family:"IBM Plex Mono",monospace}
.socials a:hover{color:#fff}

/* footer */
footer{padding:34px 0 48px;font-size:14px;color:var(--muted)}
.foot{display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap;align-items:center}
footer a{color:var(--muted);text-decoration:none}
footer a:hover{color:var(--ink)}

a:focus-visible,.btn:focus-visible{outline:3px solid var(--blue);outline-offset:2px;border-radius:8px}
@media (prefers-reduced-motion: reduce){
  html{scroll-behavior:auto}
  .btn,.app,.work::after{transition:none}
}
"""

SERVICES = [
    ("Digital Twins & VR Facility Tours",
     "Fully modeled, animated, and functional replicas of real facilities — walk the gas turbine room without a hard hat. Built for internal training, stakeholder engagement, and career-fair buzz.",
     "Vistra · Midlothian Power Plant"),
    ("3D Scanning & Reality Capture",
     "Photogrammetry and next-generation scanning that turn a real facility into a 3D model you can step inside — then deploy to web, VR, or AR for training and visual simulation.",
     "Davis-Besse Nuclear Power Plant"),
    ("Educational XR Games",
     "Mini-game worlds with shared hubs, live leaderboards, and player profiles. Students don't watch the lesson — they live it, then replay to level up.",
     "Recyclotopia · BungaLoad · FantasticWinds"),
    ("AR & Live-Data Experiences",
     "Augmented reality that overlays real-time data on the real world — from Oracle's Connected Hub to location-based storytelling and projection games that draw a crowd.",
     "Oracle · StEVie · Sustainaball"),
    ("Events & Community Outreach",
     "We show up with headsets, staff, and experiences that create lines around the booth — career fests, school days, museums, and community events.",
     "Ameren Shawnee · Career Fests · MOSAC"),
]

FEATURED = [
    # (client, title, blurb, pills, image, video_url_or_None, hero)
    ("Smithsonian × Oracle", "FUTURES Exhibit VR",
     "A fully immersive journey through the lifecycle of energy and water — guests interact with everything hands-on and leave understanding their role in a clean energy future.",
     ["10,000 guests", "600K exhibition visitors"], "smithsonian.jpg", None, True),
    ("Oracle", "Connected Hub — Digital Model",
     "The digital side of Oracle's miniature living utility: AR overlays and apps for iOS, Windows, and Apple Vision Pro that turn complex utility scenarios into one simple visual story, shown at customer meetings worldwide.",
     ["iOS · Windows · Vision Pro", "Shown worldwide"], "oracle.jpg", None, False),
    ("Vistra", "Midlothian Digital Twin",
     "A VR tour of a combined-cycle power plant with fully modeled, animated enclosures — see the inner workings of systems almost nobody gets to visit in person.",
     ["Used by plant leadership", "Training + engagement"], "vistra.jpg", None, False),
    ("Exelon", "STEM Academy",
     "A five-year program across all six Exelon utilities: career fairs and classroom experiences with VR simulations of real utility roles — a proven pathway from STEM exposure to real careers.",
     ["6 utilities", "5-year program"], "exelon.jpg", None, False),
    ("SMUD", "Hydropower VR Tour",
     "A virtual tour of a hydroelectric facility that brings the plant to the people — featured for a full year at the Museum of Science and Curiosity.",
     ["~180K visitors / yr"], "smud.jpg", "https://youtu.be/AEKrfJVdzuQ", False),
    ("National Energy Foundation", "Energy Mini-Game Series",
     "Recyclotopia, BungaLoad, and FantasticWinds in one shared hub — live leaderboards, player profiles, and status badges that keep students replaying to level up.",
     ["3 games, 1 hub", "Career fests + TX schools"], "nef-hub.jpg", None, False),
    ("Vistra", "Davis-Besse Reality Capture",
     "We scanned the turbine deck, cooling tower, and more with next-generation cameras — turning a real nuclear facility into a 3D model you can step inside, on web, VR, or AR.",
     ["PortalCam capture", "Web · VR · AR"], "davis-besse.jpg", None, False),
]

APPS = [
    # (name, AR/VR, image, youtube id)
    ("Sustainaball", "AR", "sustainaball.jpg", "lU-qdaFcKII"),
    ("Transmission Line Repair", "VR", "transmission-line.jpg", "QuTk28Wv9ug"),
    ("Electric Drive", "VR", "electric-drive.jpg", "etZPdetz3YM"),
    ("Water for Humanity", "VR", "water-for-humanity.jpg", "ZhWtqANRsO8"),
    ("Bucket Truck", "VR", "bucket-truck.jpg", "9gcM_seGdkg"),
    ("Electrify San Antonio", "AR", "electrify-san-antonio.jpg", "M1GIMDRdtUw"),
    ("Lineman Challenge", "VR", "lineman-challenge.jpg", "JbaT1e1XYbM"),
    ("Light Bulb Challenge", "VR", "light-bulb-challenge.jpg", "5RKfX1Lu_xM"),
    ("History of Energy", "VR", "history-of-energy.jpg", "Xa_Zfa1RtRs"),
    ("Solar Tracker", "VR", "solar-tracker.jpg", "Buht7EHT2Wk"),
    ("Virtual Avatar", "VR", "virtual-avatar.jpg", "OzOYFWjIEqM"),
    ("Not It — Short VR Film", "VR", "not-it.jpg", "HdmBgofsnm4"),
]

STEPS = [
    ("Discovery", "A first meeting about your goals, your challenges, and where XR can actually help."),
    ("Concept", "We explore directions together and pick the strongest one."),
    ("Prototype", "An early build you can get your hands on — feedback before anything is locked in."),
    ("Build & refine", "Full experience development, shaped with your team along the way."),
    ("Test & deploy", "User testing plus deployment support — including on-site staffing for your events."),
    ("Keep it fresh", "Short check-ins during development, and quick updates after launch."),
]

TEAM = [
    ("Jason Rodriguez", "Co-Founder & CEO", "JR"),
    ("Mark Ishac", "Creative Lead", "MI"),
    ("Ines Said", "Lead XR Developer", "IS"),
    ("Kelly Zhang", "3D Designer / Developer", "KZ"),
    ("Sam Kodo", "Sr. Software Engineer", "SK"),
]

CLIENTS = ["Smithsonian", "Oracle", "Exelon", "SMUD", "Vistra", "Ameren",
           "Austin Energy", "CPS Energy", "BGE", "NREL", "Toyota",
           "National Energy Foundation", "E4 Youth"]

SOCIALS = [
    ("LinkedIn", "https://linkedin.com/company/froliqmedia"),
    ("Instagram", "https://instagram.com/froliqmedia"),
    ("Twitter/X", "https://twitter.com/froliqmedia"),
    ("Facebook", "https://facebook.com/froliqmedia"),
]


def img_src(fname, inline, folder='work'):
    if not inline:
        return f"assets/{folder}/{fname}"
    raw = open(os.path.join(ASSETS, folder, fname), 'rb').read()
    return "data:image/jpeg;base64," + base64.b64encode(raw).decode()


def page(inline_images=False):
    svc = ""
    for i, (t, d, tag) in enumerate(SERVICES, 1):
        svc += f'<div class="svc"><span class="num">S{i}</span><h3>{t}</h3><p>{d}</p><span class="tag">{tag}</span></div>\n'

    work = ""
    for client, title, blurb, pills, img, video, hero in FEATURED:
        p = "".join(f'<span class="pill">{x}</span>' for x in pills)
        if video:
            p += f'<a class="pill pill-watch" href="{video}" rel="noopener" target="_blank">▶ Watch</a>'
        cls = "work work-hero" if hero else "work"
        work += (f'<article class="{cls}"><img src="{img_src(img, inline_images, "featured")}" alt="{client} — {title}" loading="lazy">'
                 f'<div class="body"><span class="client">{client}</span><h3>{title}</h3><p>{blurb}</p>'
                 f'<div class="pills">{p}</div></div></article>\n')

    apps = ""
    for name, kind, img, yt in APPS:
        cls = "xr ar" if kind == "AR" else "xr"
        apps += (f'<a class="app" href="https://youtu.be/{yt}" rel="noopener" target="_blank">'
                 f'<span class="shot"><img src="{img_src(img, inline_images)}" alt="{name} — screenshot" loading="lazy"><span class="play">▶</span></span>'
                 f'<div class="meta"><b>{name}</b><span class="{cls}">{kind}</span></div></a>\n')

    steps = ""
    for t, d in STEPS:
        steps += f'<div class="step"><h3>{t}</h3><p>{d}</p></div>\n'

    team = ""
    for name, role, init in TEAM:
        team += f'<div class="member"><span class="av">{init}</span><span><b>{name}</b><span>{role}</span></span></div>\n'

    chips = "".join(f'<span class="chip">{c}</span>' for c in CLIENTS)
    socials = "".join(f'<a href="{u}" rel="noopener">{n}</a>' for n, u in SOCIALS)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Froliq — XR Studio</title>
<meta name="description" content="Froliq builds digital twins, VR training, and educational XR games for energy, utilities, and education. Austin, TX.">
{FONTS}
<style>{CSS}</style>
</head>
<body>

<nav class="nav"><div class="wrap nav-in">
  <a class="brand" href="#top" aria-label="Froliq home">{LOGO_SVG}<b>FROLIQ</b></a>
  <a class="lnk" href="#work">Work</a>
  <a class="lnk" href="#services">Services</a>
  <a class="lnk" href="#apps">Apps</a>
  <a class="lnk" href="#process">Process</a>
  <a class="lnk" href="#about">About</a>
  <a class="btn btn-grad" href="{TYPEFORM}" rel="noopener">Request a demo</a>
</div></nav>

<header class="hero" id="top"><div class="wrap">
  <p class="eyebrow">XR Studio · Austin, TX</p>
  <h1>Step inside the <span class="grad-text">future of energy</span>.</h1>
  <p class="lede">Froliq builds digital twins, immersive training, and educational XR games for utilities, museums, and communities — turning the most complex systems into experiences anyone can walk through.</p>
  <div class="hero-cta">
    <a class="btn btn-grad" href="{TYPEFORM}" rel="noopener">Request a demo</a>
    <a class="btn btn-ghost" href="#work">See the work</a>
  </div>
  <div class="stats">
    <div class="stat"><b>10,000</b><span>guests through our Smithsonian VR experience</span></div>
    <div class="stat"><b>6</b><span>Exelon utilities in our five-year STEM program</span></div>
    <div class="stat"><b>180K</b><span>annual museum visitors reached with SMUD</span></div>
    <div class="stat"><b>12+</b><span>XR apps shipped for energy &amp; education</span></div>
  </div>
</div></header>

<div class="clients"><div class="wrap">
  <p class="label">Trusted by</p>
  <div class="chip-row">{chips}</div>
</div></div>

<section id="services"><div class="wrap">
  <div class="sec-head">
    <p class="eyebrow">What we do</p>
    <h2>Complex systems, made playable.</h2>
    <p>Five ways we put people inside the story — from power-plant floors to classroom headsets.</p>
  </div>
  <div class="svc-grid">{svc}</div>
</div></section>

<section id="work"><div class="wrap">
  <div class="sec-head">
    <p class="eyebrow">Featured work</p>
    <h2>Built with world-class partners.</h2>
    <p>From the Smithsonian to the plant floor — a few of the projects we're proudest of.</p>
  </div>
  <div class="work-grid">{work}</div>
</div></section>

<section class="lib" id="apps"><div class="wrap">
  <div class="sec-head">
    <p class="eyebrow">The app library</p>
    <h2>Every app, ready for the field.</h2>
    <p>A dozen shipped experiences across VR and AR — training sims, challenges, films, and games. Tap any app to watch it in action.</p>
  </div>
  <div class="lib-grid">{apps}</div>
</div></section>

<section id="process"><div class="wrap">
  <div class="sec-head">
    <p class="eyebrow">How we work</p>
    <h2>A simple process, start to ship.</h2>
    <p>You see it early, you shape it often, and we're there on the day it goes live.</p>
  </div>
  <div class="steps">{steps}</div>
</div></section>

<section id="about"><div class="wrap about-grid">
  <div>
    <p class="eyebrow">About Froliq</p>
    <h2>Born in Austin. At home in headsets.</h2>
    <p>Froliq was founded in Austin, Texas in 2022 to build next-generation education, engagement, and training experiences. A lot of our work is digital twins and training tools for energy, utilities, and infrastructure — and just as much is educational XR for nonprofits and communities who want complex topics made simple and fun.</p>
    <p>We show up in person, too: outreach events, conferences, schools. At the core it's always the same — learning, safety, and helping the next generation feel confident stepping into complex fields.</p>
  </div>
  <div>
    <h3 style="margin-bottom:14px">The team</h3>
    <div class="team">{team}</div>
  </div>
</div></section>

<section id="contact"><div class="wrap">
  <div class="cta">
    <h2>It's Froliq time!</h2>
    <p>Tell us about your facility, your program, or your event — we'll bring the headsets.</p>
    <a class="btn btn-grad" href="{TYPEFORM}" rel="noopener">Request a demo</a>
    <div class="socials">{socials}</div>
  </div>
</div></section>

<footer><div class="wrap foot">
  <span>© 2026 Froliq · Austin, TX</span>
  <span><a href="#top">Back to top ↑</a></span>
</div></footer>

</body>
</html>
"""


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, 'assets'))
    shutil.copytree(os.path.join(ASSETS, 'work'), os.path.join(OUT, 'assets', 'work'))
    shutil.copytree(os.path.join(ASSETS, 'featured'), os.path.join(OUT, 'assets', 'featured'))
    shutil.copy(os.path.join(ASSETS, 'froliq-logo.svg'), os.path.join(OUT, 'assets'))

    open(os.path.join(OUT, 'index.html'), 'w').write(page(inline_images=False))
    open(os.path.join(OUT, '404.html'), 'w').write(
        page(inline_images=False).replace('<body>', '<body><div class="wrap" style="padding:40px 24px 0"><p class="eyebrow">404 — page not found</p></div>', 1))
    open(os.path.join(ROOT, 'preview.html'), 'w').write(page(inline_images=True))
    print("built docs/ and preview.html")


if __name__ == '__main__':
    main()
