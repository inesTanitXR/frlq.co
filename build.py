#!/usr/bin/env python3
"""Build frlq.co — multi-page static site aligned with the 2026 Froliq story.

Outputs:
  docs/        — index/work/apps/services/about/contact.html,
                 project-<slug>.html detail pages, 404.html, assets/
  preview.html — single-file version with hash routing + data-URI images

Brand: Froliq logo purple #9b02ff -> blue #20bdff.
Type:  Bricolage Grotesque (display) / Instrument Sans (body) / IBM Plex Mono (labels).
"""
import base64, mimetypes, os, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, 'assets')
OUT = os.path.join(ROOT, 'docs')

LOGO_SVG = open(os.path.join(ASSETS, 'froliq-logo.svg')).read()
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
  --chip-bg:#ffffff;
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
    --chip-bg:#f3eeff;
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
  --chip-bg:#f3eeff;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0;background:var(--ground);color:var(--body);
  font-family:"Instrument Sans",-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;
  font-size:17px;line-height:1.65;
}
h1,h2,h3{font-family:"Bricolage Grotesque","Instrument Sans",Helvetica,sans-serif;color:var(--ink);letter-spacing:-.015em;line-height:1.12;text-wrap:balance;margin:0 0 14px}
h1{font-size:clamp(38px,5.6vw,62px);font-weight:800}
h2{font-size:clamp(28px,3.6vw,40px);font-weight:800}
h3{font-size:20px;font-weight:700}
p{margin:0 0 14px}
a{color:var(--ink)}
img{max-width:100%;display:block}
.wrap{max-width:1120px;margin:0 auto;padding:0 24px}
.mono{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace}
.eyebrow{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--purple);margin:0 0 14px}
.grad-text{background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
section{padding:64px 0}
.sec-head{max-width:640px;margin-bottom:40px}
.sec-head p{color:var(--body)}
.sec-foot{margin-top:28px}
.arrow-lnk{font-weight:600;text-decoration:none;color:var(--purple)}
.arrow-lnk:hover{text-decoration:underline}

/* nav */
.nav{position:sticky;top:0;z-index:50;background:var(--nav-bg);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
.nav-in{display:flex;align-items:center;gap:24px;height:66px}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;margin-right:auto}
.brand svg{height:30px;width:auto}
.brand b{font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:21px;letter-spacing:.01em;background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.nav a.lnk{text-decoration:none;color:var(--body);font-weight:500;font-size:15px;padding:4px 2px;border-bottom:2px solid transparent}
.nav a.lnk:hover{color:var(--ink)}
.nav a.lnk.on{color:var(--ink);border-bottom-color:var(--purple)}
.btn{display:inline-block;padding:12px 22px;border-radius:999px;font-weight:600;font-size:15.5px;text-decoration:none;transition:transform .15s ease,box-shadow .15s ease}
.btn:active{transform:scale(.98)}
.btn-grad{background:var(--grad);color:#fff;box-shadow:0 6px 20px rgba(155,2,255,.28)}
.btn-grad:hover{transform:translateY(-1px);box-shadow:0 10px 26px rgba(155,2,255,.36)}
.btn-ghost{border:1.5px solid var(--line);color:var(--ink);background:var(--card)}
.btn-ghost:hover{border-color:var(--purple)}
.nav .btn{padding:9px 18px}
@media(max-width:900px){.nav a.lnk{display:none}.nav-mob{display:flex !important}}
.nav-mob{display:none;gap:16px;overflow-x:auto;padding:10px 24px;border-top:1px solid var(--line)}
.nav-mob a{text-decoration:none;color:var(--body);font-weight:500;font-size:14px;white-space:nowrap}

/* page head (subpages) */
.page-head{padding:64px 0 8px}
.page-head p.sub{font-size:18.5px;max-width:620px;color:var(--body)}

/* hero (home) */
.hero{position:relative;padding:88px 0 64px;overflow:hidden}
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
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:56px}
.stat{border-top:2.5px solid transparent;border-image:var(--grad) 1;padding-top:16px}
.stat b{display:block;font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:32px;color:var(--ink);font-variant-numeric:tabular-nums}
.stat span{font-size:13.5px;color:var(--muted)}
@media(max-width:860px){.stats{grid-template-columns:repeat(2,1fr)}}

/* client logo strip */
.clients{padding:34px 0 42px;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.clients .label{text-align:center;font-family:"IBM Plex Mono",monospace;font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);margin-bottom:20px}
.logo-row{display:flex;flex-wrap:wrap;justify-content:center;gap:12px}
.logo-chip{background:var(--chip-bg);border:1px solid var(--line);border-radius:14px;padding:12px 20px;display:flex;align-items:center;justify-content:center}
.logo-chip img{height:34px;width:auto;max-width:150px;object-fit:contain}

/* services */
.svc-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.svc{background:var(--card);border:1px solid var(--line);border-radius:20px;padding:26px 24px;display:flex;flex-direction:column;gap:8px}
.svc .num{font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--muted);letter-spacing:.1em}
.svc h3{margin:2px 0 2px}
.svc p{font-size:15.5px;margin:0;color:var(--body)}
.svc .tag{margin-top:auto;padding-top:14px;font-family:"IBM Plex Mono",monospace;font-size:12.5px;color:var(--purple)}
.svc:nth-child(1){grid-column:span 2;background:linear-gradient(135deg,var(--purple-soft),var(--card) 55%)}
@media(max-width:860px){.svc-grid{grid-template-columns:1fr}.svc:nth-child(1){grid-column:auto}}

/* work cards */
.work-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}
a.work{background:var(--card);border:1px solid var(--line);border-radius:20px;position:relative;overflow:hidden;display:flex;flex-direction:column;text-decoration:none;transition:transform .18s ease,box-shadow .18s ease}
a.work:hover{transform:translateY(-3px);box-shadow:var(--shadow)}
.work::after{content:"";position:absolute;left:0;right:0;top:0;height:4px;background:var(--grad);opacity:0;transition:opacity .2s}
.work:hover::after{opacity:1}
.work>img{width:100%;aspect-ratio:16/9;object-fit:cover}
.work .body{padding:22px 24px 24px;display:flex;flex-direction:column;flex:1}
.work .client{font-family:"IBM Plex Mono",monospace;font-size:12.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--blue)}
.work h3{font-size:23px;margin:8px 0 8px}
.work p{font-size:15.5px;margin:0 0 16px}
.work .pills{margin-top:auto}
.pill{display:inline-block;font-family:"IBM Plex Mono",monospace;font-size:12.5px;color:var(--ink);
  background:var(--card-2);border-radius:999px;padding:6px 13px;margin:0 6px 6px 0}
.pill-grad{background:var(--grad);color:#fff}
.work-hero{grid-column:1/-1;flex-direction:row}
.work-hero>img{width:44%;aspect-ratio:auto;min-height:100%}
.work-hero .body{padding:30px 32px}
.work-hero h3{font-size:28px}
@media(max-width:860px){.work-grid{grid-template-columns:1fr}.work-hero{flex-direction:column}.work-hero>img{width:100%;aspect-ratio:16/9;min-height:0}}

/* app grid */
.lib-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
a.app{background:var(--card);border:1px solid var(--line);border-radius:16px;overflow:hidden;transition:transform .18s ease,box-shadow .18s ease;text-decoration:none;display:block}
a.app:hover{transform:translateY(-3px);box-shadow:var(--shadow)}
.app .shot{position:relative;display:block}
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
.team{display:grid;grid-template-columns:1fr;gap:14px}
.member{display:flex;gap:13px;align-items:center;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:14px 16px}
.member .av{flex:none;width:46px;height:46px;border-radius:50%;background:var(--grad);color:#fff;display:grid;place-items:center;
  font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:16px}
.member b{display:block;color:var(--ink);font-size:15.5px}
.member span{font-size:13.5px;color:var(--muted)}
@media(max-width:860px){.about-grid{grid-template-columns:1fr}}

/* project detail */
.detail{max-width:860px;margin:0 auto;padding:0 24px}
.detail-head{padding:56px 0 26px}
.detail-hero{border-radius:22px;overflow:hidden;border:1px solid var(--line);margin-bottom:30px}
.detail-hero img{width:100%}
.video{position:relative;border-radius:22px;overflow:hidden;border:1px solid var(--line);margin:0 0 30px;aspect-ratio:16/9;background:#000}
.video iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.video-link{position:relative;display:block;border-radius:22px;overflow:hidden;border:1px solid var(--line);margin-bottom:30px}
.video-link img{width:100%;aspect-ratio:16/9;object-fit:cover}
.video-link .play{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:70px;height:70px;border-radius:50%;
  background:rgba(15,10,30,.75);color:#fff;display:grid;place-items:center;font-size:24px;padding-left:4px}
.video-link:hover .play{background:var(--purple)}
.detail .prose{font-size:17.5px}
.detail .prose p{margin-bottom:18px}
.back-row{padding:22px 0 0;display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap}
.detail-cta{margin:44px 0 64px;background:var(--card-2);border:1px solid var(--line);border-radius:22px;padding:30px;display:flex;align-items:center;justify-content:space-between;gap:18px;flex-wrap:wrap}
.detail-cta b{font-family:"Bricolage Grotesque",sans-serif;font-size:21px;color:var(--ink)}

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
.socials{display:flex;justify-content:center;gap:20px;margin-top:26px;position:relative;flex-wrap:wrap}
.socials a{color:#cfc5ea;font-size:14px;text-decoration:none;font-family:"IBM Plex Mono",monospace}
.socials a:hover{color:#fff}

footer{padding:34px 0 48px;font-size:14px;color:var(--muted);border-top:1px solid var(--line);margin-top:64px}
.foot{display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap;align-items:center}
footer a{color:var(--muted);text-decoration:none;margin-left:16px}
footer a:hover{color:var(--ink)}

a:focus-visible,.btn:focus-visible{outline:3px solid var(--blue);outline-offset:2px;border-radius:8px}
@media (prefers-reduced-motion: reduce){
  html{scroll-behavior:auto}
  .btn,a.app,a.work,.work::after{transition:none}
}
"""

# ---------------------------------------------------------------- content

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

LOGOS = ["smithsonian.png", "oracle.png", "exelon.png", "smud.png", "vistra.png",
         "ameren.png", "austin-energy.svg", "cps.svg", "bge.svg", "nrel.svg", "sew.svg"]

SOCIALS = [
    ("LinkedIn", "https://linkedin.com/company/froliqmedia"),
    ("Instagram", "https://instagram.com/froliqmedia"),
    ("Twitter/X", "https://twitter.com/froliqmedia"),
    ("Facebook", "https://facebook.com/froliqmedia"),
]

# featured=True projects render as big cards on work.html; others on apps.html
PROJECTS = [
    dict(slug="smithsonian-futures", featured=True, hero_card=True,
         client="Smithsonian × Oracle", title="FUTURES Exhibit VR", xr="VR",
         img=("featured", "smithsonian.jpg"), video=None,
         card="A fully immersive journey through the lifecycle of energy and water — guests interact with everything hands-on and leave understanding their role in a clean energy future.",
         pills=["10,000 guests", "600K exhibition visitors"],
         paras=[
             "For the Smithsonian's FUTURES exhibition, we built a fully immersive virtual reality experience with Oracle exploring the lifecycle of energy and water — how we make it, how we use it, and how to conserve it.",
             "Guests stepped into the headset and interacted with everything hands-on. Around 10,000 guests went through the experience, inside an exhibition that welcomed 600,000 visitors.",
             "The goal was simple: help people understand how they use energy — and their own role in building a clean energy future."]),
    dict(slug="oracle-connected-hub", featured=True,
         client="Oracle", title="Connected Hub — Digital Model", xr="AR",
         img=("featured", "oracle.jpg"), video=None,
         card="The digital side of Oracle's miniature living utility: AR overlays and apps for iOS, Windows, and Apple Vision Pro, shown at customer meetings worldwide.",
         pills=["iOS · Windows · Vision Pro", "Shown worldwide"],
         paras=[
             "Oracle's Connected Hub is a miniature living utility neighborhood — real solar panels, wind turbines, EV chargers, and smart homes, all wired into Oracle's actual utility software with live, real-time data.",
             "Froliq built the digital side: the augmented reality overlays and the Connected Hub apps for iOS, Windows, and Apple Vision Pro that let the hub travel anywhere in the world.",
             "It turns complex utility scenarios — an outage from prediction all the way to resolution, a neighborhood full of EVs charging at once — into one simple visual story anyone can follow. Oracle shows it at customer meetings, lab visits, and conferences worldwide."]),
    dict(slug="vistra-midlothian", featured=True,
         client="Vistra", title="Midlothian Digital Twin", xr="VR",
         img=("featured", "vistra.jpg"), video=None,
         card="A VR tour of a combined-cycle power plant with fully modeled, animated enclosures — see the inner workings of systems almost nobody gets to visit in person.",
         pills=["Used by plant leadership", "Training + engagement"],
         paras=[
             "An immersive tour of Vistra's Midlothian combined-cycle power plant. Almost nobody gets to walk into the gas turbine room — the heart of the whole plant — so we brought it into VR, where students, employees, and stakeholders can experience it firsthand, safely.",
             "To build something this accurate we used photogrammetry: hundreds of photos of the real equipment, stitched together into a super detailed 3D model. The enclosures are fully modeled, animated, and functional — down to systems like the lube oil system.",
             "And it isn't a demo on a shelf. Plant managers, directors, and leaders at Vistra use it for internal training, stakeholder engagement, and career-fair buzz."]),
    dict(slug="exelon-stem", featured=True,
         client="Exelon", title="STEM Academy", xr="VR",
         img=("featured", "exelon.jpg"), video=None,
         card="A five-year program across all six Exelon utilities: career fairs and classroom experiences with VR simulations of real utility roles.",
         pills=["6 utilities", "5-year program"],
         paras=[
             "A five-year partnership with Exelon's STEM academy, spanning all six Exelon utilities — Washington DC, Maryland, Pennsylvania, and beyond.",
             "We bring VR simulations of real utility roles to career fairs and classrooms, so students actually get to try the jobs instead of just hearing about them.",
             "It's a proven pathway: students go from STEM exposure to real Exelon careers."]),
    dict(slug="smud-hydropower", featured=True,
         client="SMUD", title="Hydropower VR Tour", xr="VR",
         img=("featured", "smud.jpg"), video="AEKrfJVdzuQ",
         card="A virtual tour of a hydroelectric facility that brings the plant to the people — featured for a full year at the Museum of Science and Curiosity.",
         pills=["~180K visitors / yr"],
         paras=[
             "A VR tour of SMUD's hydroelectric facility, built to meet people where they're at — not everyone can make the trip out to walk a dam, so we bring the facility to them.",
             "The experience was featured at the Museum of Science and Curiosity for a full year, in front of roughly 180,000 annual visitors.",
             "Accessibility and workforce development in one."]),
    dict(slug="nef-minigames", featured=True,
         client="National Energy Foundation", title="Energy Mini-Game Series", xr="VR",
         img=("featured", "nef-hub.jpg"), video=None,
         card="Recyclotopia, BungaLoad, and FantasticWinds in one shared hub — live leaderboards, player profiles, and status badges that keep students replaying to level up.",
         pills=["3 games, 1 hub", "Career fests + TX schools"],
         paras=[
             "A Mario Party-inspired series of energy-education mini-games, all living inside one shared VR hub: students spawn in the middle, see three doors, and point-and-click into whichever game they want.",
             "Recyclotopia puts players in front of a conveyor belt of mixed waste — grab items and sort them into the right bins before they slide past, with a new bin added every level.",
             "BungaLoad turns students into home energy auditors: four rooms, two minutes each, find the energy-wasters and drive the home's meter below 30% to win.",
             "FantasticWinds gives a bird's-eye view of a wind farm — fan the turbines from the front and watch homes light up with every spin.",
             "A live leaderboard tracks the top three players in real time, and every student gets a profile with cumulative stats and status badges — kids replay to level up, and teachers get a quick read on who's engaging. Shown at career fests, Texas schools, and workforce events."]),
    dict(slug="davis-besse-scan", featured=True,
         client="Vistra", title="Davis-Besse Reality Capture", xr="3D SCAN",
         img=("featured", "davis-besse.jpg"), video=None,
         card="We scanned the turbine deck, cooling tower, and more with next-generation cameras — turning a real nuclear facility into a 3D model you can step inside.",
         pills=["PortalCam capture", "Web · VR · AR"],
         paras=[
             "We took next-generation scanning to the Davis-Besse nuclear power plant, capturing the turbine deck, cooling tower, and other facilities with PortalCam.",
             "The scans process into an explorable 3D model — basically a 3D photo of the facility that you can step inside.",
             "From there, it can be built out on web, VR, or AR — whatever fits — for training and visual simulation."]),
    # ------- app library -------
    dict(slug="sustainaball", client="Austin Energy · Austin FC", title="Sustainaball", xr="AR",
         img=("work", "sustainaball.jpg"), video="lU-qdaFcKII",
         card="Projection-based interactive soccer.",
         pills=["~100 students"],
         paras=[
             "Our projection-based interactive soccer game: augmented reality with motion detection, multiplayer-friendly, and a natural crowd magnet at events.",
             "Around 100 students — from 7th grade all the way to college — have played it, picking up sustainability lessons while they compete."]),
    dict(slug="transmission-line-repair", client="Froliq Training", title="Transmission Line Repair", xr="VR",
         img=("work", "transmission-line.jpg"), video="QuTk28Wv9ug",
         card="High-voltage repair training in VR.", pills=[],
         paras=["A VR training experience for transmission line repair — practicing high-risk work in a safe, repeatable virtual environment."]),
    dict(slug="electric-drive", client="Austin Energy", title="Electric Drive", xr="VR",
         img=("work", "electric-drive.jpg"), video="etZPdetz3YM",
         card="An electric-vehicle VR experience.", pills=[],
         paras=["An electric vehicle VR experience built with Austin Energy — putting people behind the wheel of the EV transition."]),
    dict(slug="water-for-humanity", client="Froliq Originals", title="Water for Humanity", xr="VR",
         img=("work", "water-for-humanity.jpg"), video="ZhWtqANRsO8",
         card="An empathy-driven VR story about water.", pills=[],
         paras=["An empathy-driven VR experience that takes the perspective of a water-starved community and their efforts to survive."]),
    dict(slug="bucket-truck", client="Froliq Training", title="Bucket Truck", xr="VR",
         img=("work", "bucket-truck.jpg"), video="9gcM_seGdkg",
         card="Aerial work platform training in VR.", pills=[],
         paras=["Our Aerial Work Platform VR experience puts trainees inside a fully working bucket truck — controls, height, and all — without ever leaving the ground."]),
    dict(slug="electrify-san-antonio", client="San Antonio", title="Electrify San Antonio", xr="AR",
         img=("work", "electrify-san-antonio.jpg"), video="M1GIMDRdtUw",
         card="An AR look at powering San Antonio.", pills=[],
         paras=["An augmented reality experience about electrifying San Antonio — bringing the power system out of the substation and into your hands."]),
    dict(slug="lineman-challenge", client="Froliq Training", title="Lineman Challenge", xr="VR",
         img=("work", "lineman-challenge.jpg"), video="JbaT1e1XYbM",
         card="Step into a lineman's boots.", pills=[],
         paras=["A VR skills challenge that puts players in a lineman's boots — one of the toughest and most important jobs in the utility world."]),
    dict(slug="light-bulb-challenge", client="Froliq Originals", title="Light Bulb Challenge", xr="VR",
         img=("work", "light-bulb-challenge.jpg"), video="5RKfX1Lu_xM",
         card="A fast VR game about efficiency.", pills=[],
         paras=["A fast-paced VR challenge about lighting and energy efficiency — small choices, visible impact."]),
    dict(slug="history-of-energy", client="Froliq Originals", title="History of Energy", xr="VR",
         img=("work", "history-of-energy.jpg"), video="Xa_Zfa1RtRs",
         card="A VR journey through energy's story.", pills=[],
         paras=["A VR journey through how humans have made and used energy — from the first fires to the modern grid."]),
    dict(slug="solar-tracker", client="Froliq Originals", title="Solar Tracker", xr="VR",
         img=("work", "solar-tracker.jpg"), video="Buht7EHT2Wk",
         card="Follow the sun in VR.", pills=[],
         paras=["A VR experience about capturing solar energy — and what it takes to follow the sun."]),
    dict(slug="virtual-avatar", client="Froliq Labs", title="Virtual Avatar", xr="VR",
         img=("work", "virtual-avatar.jpg"), video="OzOYFWjIEqM",
         card="Real-time virtual character presence.", pills=[],
         paras=["A Froliq Labs experiment in real-time virtual avatars and character presence."]),
    dict(slug="not-it", client="Froliq Originals", title="Not It — Short VR Film", xr="VR",
         img=("work", "not-it.jpg"), video="HdmBgofsnm4",
         card="A short cinematic VR film.", pills=[],
         paras=["A short cinematic VR film from the Froliq team — storytelling you sit inside of."]),
]

NAV_ITEMS = [("work", "Work"), ("apps", "Apps"), ("services", "Services"),
             ("about", "About"), ("contact", "Contact")]

# ---------------------------------------------------------------- helpers

def img_src(folder, fname, inline):
    if not inline:
        return f"assets/{folder}/{fname}"
    raw = open(os.path.join(ASSETS, folder, fname), 'rb').read()
    mime = mimetypes.guess_type(fname)[0] or 'image/jpeg'
    return f"data:{mime};base64," + base64.b64encode(raw).decode()


def href(page, inline):
    if page == "index":
        return "#/" if inline else "index.html"
    return f"#/{page}" if inline else f"{page}.html"


def phref(slug, inline):
    return f"#/p/{slug}" if inline else f"project-{slug}.html"


def nav(active, inline):
    links = "".join(
        f'<a class="lnk{" on" if key == active else ""}" href="{href(key, inline)}">{label}</a>'
        for key, label in NAV_ITEMS)
    mob = "".join(f'<a href="{href(key, inline)}">{label}</a>' for key, label in NAV_ITEMS)
    return (f'<nav class="nav"><div class="wrap nav-in">'
            f'<a class="brand" href="{href("index", inline)}" aria-label="Froliq home">{LOGO_SVG}<b>FROLIQ</b></a>'
            f'{links}<a class="btn btn-grad" href="{TYPEFORM}" rel="noopener">Request a demo</a></div>'
            f'<div class="nav-mob wrap">{mob}</div></nav>')


def footer(inline):
    return (f'<footer><div class="wrap foot"><span>© 2026 Froliq · Austin, TX</span>'
            f'<span><a href="{href("work", inline)}">Work</a><a href="{href("contact", inline)}">Contact</a></span>'
            f'</div></footer>')


def shell(title, body, active, inline):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="Froliq builds digital twins, VR training, and educational XR games for energy, utilities, and education. Austin, TX.">
{FONTS}
<style>{CSS}</style>
</head>
<body>
{nav(active, inline)}
{body}
{footer(inline)}
</body>
</html>
"""


def work_card(p, inline, hero=False):
    pills = "".join(f'<span class="pill">{x}</span>' for x in p["pills"])
    if p.get("video"):
        pills += '<span class="pill pill-grad">▶ Video</span>'
    cls = "work work-hero" if hero else "work"
    f, fn = p["img"]
    return (f'<a class="{cls}" href="{phref(p["slug"], inline)}">'
            f'<img src="{img_src(f, fn, inline)}" alt="{p["client"]} — {p["title"]}" loading="lazy">'
            f'<div class="body"><span class="client">{p["client"]}</span><h3>{p["title"]}</h3>'
            f'<p>{p["card"]}</p><div class="pills">{pills}</div></div></a>')


def app_card(p, inline):
    f, fn = p["img"]
    cls = "xr ar" if p["xr"] == "AR" else "xr"
    play = '<span class="play">▶</span>' if p.get("video") else ''
    return (f'<a class="app" href="{phref(p["slug"], inline)}">'
            f'<span class="shot"><img src="{img_src(f, fn, inline)}" alt="{p["title"]} — screenshot" loading="lazy">'
            f'{play}</span>'
            f'<div class="meta"><b>{p["title"]}</b><span class="{cls}">{p["xr"]}</span></div></a>')


def logo_strip(inline, label="Trusted by"):
    chips = "".join(
        f'<div class="logo-chip"><img src="{img_src("logos", l, inline)}" alt="{l.rsplit(".",1)[0].replace("-"," ").title()} logo" loading="lazy"></div>'
        for l in LOGOS)
    return f'<div class="clients"><div class="wrap"><p class="label">{label}</p><div class="logo-row">{chips}</div></div></div>'


def cta_block(inline):
    socials = "".join(f'<a href="{u}" rel="noopener">{n}</a>' for n, u in SOCIALS)
    return (f'<div class="cta"><h2>It\'s Froliq time!</h2>'
            f'<p>Tell us about your facility, your program, or your event — we\'ll bring the headsets.</p>'
            f'<a class="btn btn-grad" href="{TYPEFORM}" rel="noopener">Request a demo</a>'
            f'<div class="socials">{socials}</div></div>')

# ---------------------------------------------------------------- pages

def page_index(inline):
    featured = [p for p in PROJECTS if p.get("featured")]
    teaser = "".join(work_card(p, inline) for p in featured[:4])
    svc = "".join(
        f'<div class="svc"><span class="num">S{i}</span><h3>{t}</h3><p>{d}</p><span class="tag">{tag}</span></div>'
        for i, (t, d, tag) in enumerate(SERVICES[:3], 1))
    body = f"""
<header class="hero"><div class="wrap">
  <p class="eyebrow">XR Studio · Austin, TX</p>
  <h1>Step inside the <span class="grad-text">future of energy</span>.</h1>
  <p class="lede">Froliq builds digital twins, immersive training, and educational XR games for utilities, museums, and communities — turning the most complex systems into experiences anyone can walk through.</p>
  <div class="hero-cta">
    <a class="btn btn-grad" href="{TYPEFORM}" rel="noopener">Request a demo</a>
    <a class="btn btn-ghost" href="{href('work', inline)}">See the work</a>
  </div>
  <div class="stats">
    <div class="stat"><b>10,000</b><span>guests through our Smithsonian VR experience</span></div>
    <div class="stat"><b>6</b><span>Exelon utilities in our five-year STEM program</span></div>
    <div class="stat"><b>180K</b><span>annual museum visitors reached with SMUD</span></div>
    <div class="stat"><b>12+</b><span>XR apps shipped for energy &amp; education</span></div>
  </div>
</div></header>
{logo_strip(inline)}
<section><div class="wrap">
  <div class="sec-head"><p class="eyebrow">Featured work</p><h2>Built with world-class partners.</h2></div>
  <div class="work-grid">{teaser}</div>
  <p class="sec-foot"><a class="arrow-lnk" href="{href('work', inline)}">See all work →</a></p>
</div></section>
<section><div class="wrap">
  <div class="sec-head"><p class="eyebrow">What we do</p><h2>Complex systems, made playable.</h2></div>
  <div class="svc-grid">{svc}</div>
  <p class="sec-foot"><a class="arrow-lnk" href="{href('services', inline)}">All five services →</a></p>
</div></section>
<section><div class="wrap">{cta_block(inline)}</div></section>"""
    return shell("Froliq — XR Studio", body, None, inline)


def page_work(inline):
    featured = [p for p in PROJECTS if p.get("featured")]
    cards = "".join(work_card(p, inline, hero=p.get("hero_card", False)) for p in featured)
    body = f"""
<header class="page-head"><div class="wrap">
  <p class="eyebrow">Featured work</p>
  <h1>Built with world-class partners.</h1>
  <p class="sub">From the Smithsonian to the plant floor — every project has its own page. Click through for the full story.</p>
</div></header>
<section style="padding-top:34px"><div class="wrap"><div class="work-grid">{cards}</div>
<p class="sec-foot">Looking for the games and training sims? <a class="arrow-lnk" href="{href('apps', inline)}">Browse the app library →</a></p>
</div></section>"""
    return shell("Work — Froliq", body, "work", inline)


def page_apps(inline):
    apps = [p for p in PROJECTS if not p.get("featured")]
    cards = "".join(app_card(p, inline) for p in apps)
    body = f"""
<header class="page-head"><div class="wrap">
  <p class="eyebrow">The app library</p>
  <h1>Every app, ready for the field.</h1>
  <p class="sub">A dozen shipped experiences across VR and AR — training sims, challenges, films, and games. Every app has its own page with a video.</p>
</div></header>
<section style="padding-top:34px"><div class="wrap"><div class="lib-grid">{cards}</div></div></section>"""
    return shell("Apps — Froliq", body, "apps", inline)


def page_services(inline):
    svc = "".join(
        f'<div class="svc"><span class="num">S{i}</span><h3>{t}</h3><p>{d}</p><span class="tag">{tag}</span></div>'
        for i, (t, d, tag) in enumerate(SERVICES, 1))
    steps = "".join(f'<div class="step"><h3>{t}</h3><p>{d}</p></div>' for t, d in STEPS)
    body = f"""
<header class="page-head"><div class="wrap">
  <p class="eyebrow">What we do</p>
  <h1>Complex systems, made playable.</h1>
  <p class="sub">Five ways we put people inside the story — from power-plant floors to classroom headsets.</p>
</div></header>
<section style="padding-top:34px"><div class="wrap"><div class="svc-grid">{svc}</div></div></section>
<section><div class="wrap">
  <div class="sec-head"><p class="eyebrow">How we work</p><h2>A simple process, start to ship.</h2>
  <p>You see it early, you shape it often, and we're there on the day it goes live.</p></div>
  <div class="steps">{steps}</div>
</div></section>
<section><div class="wrap">{cta_block(inline)}</div></section>"""
    return shell("Services — Froliq", body, "services", inline)


def page_about(inline):
    team = "".join(
        f'<div class="member"><span class="av">{init}</span><span><b>{name}</b><span>{role}</span></span></div>'
        for name, role, init in TEAM)
    body = f"""
<header class="page-head"><div class="wrap">
  <p class="eyebrow">About Froliq</p>
  <h1>Born in Austin. At home in headsets.</h1>
</div></header>
<section style="padding-top:24px"><div class="wrap about-grid">
  <div>
    <p>Froliq was founded in Austin, Texas in 2022 to build next-generation education, engagement, and training experiences. A lot of our work is digital twins and training tools for energy, utilities, and infrastructure — and just as much is educational XR for nonprofits and communities who want complex topics made simple and fun.</p>
    <p>We show up in person, too: outreach events, conferences, schools. At the core it's always the same — learning, safety, and helping the next generation feel confident stepping into complex fields.</p>
  </div>
  <div><h3 style="margin-bottom:14px">The team</h3><div class="team">{team}</div></div>
</div></section>
{logo_strip(inline, label="Partners & clients")}
<section><div class="wrap">{cta_block(inline)}</div></section>"""
    return shell("About — Froliq", body, "about", inline)


def page_contact(inline):
    body = f"""
<header class="page-head"><div class="wrap">
  <p class="eyebrow">Contact</p>
  <h1>Let's build something people remember.</h1>
  <p class="sub">A facility to scan, a program to gamify, an event that needs a line around the booth — tell us what you're planning.</p>
</div></header>
<section style="padding-top:34px"><div class="wrap">{cta_block(inline)}</div></section>"""
    return shell("Contact — Froliq", body, "contact", inline)


def page_project(p, inline):
    f, fn = p["img"]
    pills = "".join(f'<span class="pill">{x}</span>' for x in p["pills"])
    prose = "".join(f"<p>{para}</p>" for para in p["paras"])
    if p.get("video"):
        if inline:
            media = (f'<a class="video-link" href="https://youtu.be/{p["video"]}" rel="noopener" target="_blank">'
                     f'<img src="{img_src(f, fn, inline)}" alt="{p["title"]}"><span class="play">▶</span></a>')
        else:
            media = (f'<div class="video"><iframe src="https://www.youtube.com/embed/{p["video"]}" '
                     f'title="{p["title"]} — video" loading="lazy" allowfullscreen '
                     f'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe></div>')
    else:
        media = f'<div class="detail-hero"><img src="{img_src(f, fn, inline)}" alt="{p["title"]}"></div>'
    back = href("work", inline) if p.get("featured") else href("apps", inline)
    back_label = "← All work" if p.get("featured") else "← App library"
    body = f"""
<div class="detail">
  <div class="detail-head">
    <p class="eyebrow">{p["client"]} · {p["xr"]}</p>
    <h1>{p["title"]}</h1>
    <div class="pills">{pills}</div>
  </div>
  {media}
  <div class="prose">{prose}</div>
  <div class="detail-cta"><b>Want something like this?</b><a class="btn btn-grad" href="{TYPEFORM}" rel="noopener">Request a demo</a></div>
  <div class="back-row"><a class="arrow-lnk" href="{back}">{back_label}</a><a class="arrow-lnk" href="{href('contact', inline)}">Get in touch →</a></div>
</div>"""
    return shell(f'{p["title"]} — Froliq', body, "work" if p.get("featured") else "apps", inline)

# ---------------------------------------------------------------- build

PAGES = {
    "index": page_index, "work": page_work, "apps": page_apps,
    "services": page_services, "about": page_about, "contact": page_contact,
}


def extract_body(html):
    """Body content between nav and footer for the single-file preview router."""
    start = html.index('</nav>') + len('</nav>')
    end = html.index('<footer>')
    return html[start:end]


def build_preview():
    """Single file: every page as a hidden route, hash routing (#/page, #/p/slug)."""
    sections = []
    for key, fn in PAGES.items():
        body = extract_body(fn(inline=True))
        sections.append(f'<div class="route" id="route-{key}" hidden>{body}</div>')
    for p in PROJECTS:
        body = extract_body(page_project(p, inline=True))
        sections.append(f'<div class="route" id="route-p-{p["slug"]}" hidden>{body}</div>')

    router = """
<script>
(function(){
  function route(){
    var h = location.hash.replace(/^#\\/?/, '');
    var id = 'route-index';
    if (h) id = h.indexOf('p/') === 0 ? 'route-p-' + h.slice(2) : 'route-' + h;
    var target = document.getElementById(id) || document.getElementById('route-index');
    document.querySelectorAll('.route').forEach(function(el){ el.hidden = true; });
    target.hidden = false;
    document.querySelectorAll('.nav a.lnk').forEach(function(a){
      a.classList.toggle('on', a.getAttribute('href') === '#/' + h);
    });
    window.scrollTo(0, 0);
  }
  addEventListener('hashchange', route);
  route();
})();
</script>"""
    html = shell("Froliq — XR Studio", "\n".join(sections) + router, None, inline=True)
    open(os.path.join(ROOT, 'preview.html'), 'w').write(html)


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, 'assets'))
    for sub in ('work', 'featured', 'logos'):
        shutil.copytree(os.path.join(ASSETS, sub), os.path.join(OUT, 'assets', sub))
    shutil.copy(os.path.join(ASSETS, 'froliq-logo.svg'), os.path.join(OUT, 'assets'))

    for key, fn in PAGES.items():
        open(os.path.join(OUT, f'{key}.html'), 'w').write(fn(inline=False))
    for p in PROJECTS:
        open(os.path.join(OUT, f'project-{p["slug"]}.html'), 'w').write(page_project(p, inline=False))
    open(os.path.join(OUT, '404.html'), 'w').write(page_index(inline=False).replace(
        '<h1>Step inside', '<h1>404 — page not found. Step inside', 1))

    build_preview()
    n = len(PAGES) + len(PROJECTS)
    print(f"built {n} pages -> docs/, plus preview.html")


if __name__ == '__main__':
    main()
