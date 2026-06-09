import streamlit as st
import streamlit.components.v1 as components
import re, base64
from pathlib import Path

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG — edit everything here
# ══════════════════════════════════════════════════════════════════════════════

PARTNER_NAMES    = "Name Surname & Name Surname"
ANNIVERSARY_TEXT = "One Year Of"
SUBTITLE         = "Endless Love"
DATE_LINE        = "SUNDAY, 26 APRIL 2025"
CITY_LINE        = "CITY, STREET, COUNTRY"
VOL_LINE         = "VOL. 1"

# Two main paragraphs — replace these with your actual story
PARA_1 = (
    "From the very first moment we met, something shifted — quietly, almost without notice, "
    "the way morning light changes a room. This year has been filled with shared coffee cups, "
    "long walks, unexpected laughter, and the kind of warmth that stays. "
    "Every adventure we have taken together has written itself into who we are. "
    "The moments big and small, all of it — ours."
)

PARA_2 = (
    "Love isn't one grand gesture. It lives in the details: a note left on the counter, "
    "a song played for no reason, a hand found in the dark. "
    "We've collected these moments like pressed flowers — fragile, beautiful, kept. "
    "There is no ending here — only the next chapter, and the one after that. "
    "The best part? We write it together."
)

ALWAYS_YOURS_ITEMS = [
    "Every morning with you",
    "Every laugh we've shared",
    "Every mile we've walked",
    "Every dream we've built",
    "Every moment still ahead",
]

# ── COLORS ───────────────────────────────────────────────────────────────────
PAGE_BG   = "#ba99c5"   # deep purple backdrop
PAPER_BG  = "#f7f2fa"   # light plum-tinted paper
INK       = "#3b1f4e"   # dark plum ink
INK_LIGHT = "#6b4a82"   # medium purple for body text
ACCENT    = "#ddd0eb"   # soft lavender tint

# ── PHOTOS ────────────────────────────────────────────────────────────────────
# Option A (default): put photo_01.jpg … photo_04.jpg in Base/Media/
# Option B: paste 4 Google Drive URLs here:
#   PHOTO_URLS = ["https://drive.google.com/uc?export=view&id=ID1", ...]
PHOTO_URLS = None

# ── VIDEO ─────────────────────────────────────────────────────────────────────
GOOGLE_DRIVE_VIDEO_URL = "https://drive.google.com/file/d/YOUR_FILE_ID_HERE/view?usp=sharing"

# ══════════════════════════════════════════════════════════════════════════════
# INTERNALS
# ══════════════════════════════════════════════════════════════════════════════

st.set_page_config(page_title="The Love Gazette", layout="wide",
                   initial_sidebar_state="collapsed")

st.markdown("""
<style>
[data-testid="stHeader"]{display:none;}
.block-container{padding:0!important;max-width:100%!important;}
footer{display:none;}
[data-testid="stAppViewContainer"]{background:#2d1f3d;}
</style>""", unsafe_allow_html=True)

BASE_DIR  = Path(__file__).resolve().parent.parent
MEDIA_DIR = BASE_DIR / "Media"

def _local_photos():
    return sorted(
        sorted(MEDIA_DIR.glob("photo_*.jpg")) +
        sorted(MEDIA_DIR.glob("photo_*.png")),
        key=lambda p: p.name
    )

def gdrive_embed_url(url):
    m = re.search(r"/d/([a-zA-Z0-9_-]+)", url)
    if not m:
        m = re.search(r"[?&]id=([a-zA-Z0-9_-]+)", url)
    return f"https://drive.google.com/file/d/{m.group(1)}/preview" if m else None

def photo_src(idx):
    if PHOTO_URLS and idx < len(PHOTO_URLS):
        return PHOTO_URLS[idx]
    local = _local_photos()
    if idx < len(local):
        p = local[idx]
        mime = "jpeg" if p.suffix.lower() in (".jpg", ".jpeg") else "png"
        data = base64.b64encode(p.read_bytes()).decode()
        return f"data:image/{mime};base64,{data}"
    return ""

def photo_tag(idx):
    src = photo_src(idx)
    if src:
        return (f'<img src="{src}" style="width:100%;height:auto;display:block;'
                f'margin:0;border:1px solid {ACCENT};" />')
    return (f'<div style="width:100%;aspect-ratio:4/3;background:{ACCENT};'
            f'display:flex;align-items:center;justify-content:center;'
            f'color:{INK_LIGHT};font-style:italic;font-size:0.75rem;">'
            f'Photo {idx+1}</div>')

def video_tag():
    embed = gdrive_embed_url(GOOGLE_DRIVE_VIDEO_URL)
    if embed and "YOUR_FILE_ID_HERE" not in GOOGLE_DRIVE_VIDEO_URL:
        return f"""
        <div style="max-width:520px;margin:0 auto;">
          <div style="position:relative;padding-bottom:56.25%;height:0;
               overflow:hidden;background:#111;border:1px solid {INK};">
            <iframe src="{embed}"
              style="position:absolute;top:0;left:0;width:100%;height:100%;border:none;"
              allowfullscreen allow="autoplay"></iframe>
          </div>
        </div>"""
    return f"""
      <div style="max-width:520px;margin:0 auto;padding:52px 16px;
           background:#1a0f24;border:1px solid {INK};text-align:center;
           color:{INK_LIGHT};font-style:italic;font-size:0.82rem;">
        Paste your Google Drive link into<br>
        <code style="color:{INK};font-size:0.75rem;">GOOGLE_DRIVE_VIDEO_URL</code> in app.py
      </div>"""

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700&family=IM+Fell+English:ital@0;1&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{
    background: {PAGE_BG};
    font-family: 'Libre Baskerville', Georgia, serif;
    color: {INK};
    padding: 28px 16px 60px;
  }}
  .page {{
    max-width: 860px;
    margin: 0 auto 32px auto;
    background: {PAPER_BG};
    border: 1.5px solid {INK};
  }}
  .masthead {{
    padding: 10px 18px 6px;
    text-align: center;
    border-bottom: 2.5px solid {INK};
  }}
  .masthead-title {{
    font-family: 'UnifrakturMaguntia', cursive;
    font-size: clamp(1.6rem, 5vw, 3.2rem);
    line-height: 1;
    color: {INK};
  }}
  .masthead-meta {{
    display: flex;
    justify-content: space-between;
    font-size: 0.52rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: {INK_LIGHT};
    padding: 4px 0 2px;
    border-top: 0.75px solid {INK};
    border-bottom: 0.75px solid {INK};
    margin-top: 5px;
  }}
  .hero-block {{
    text-align: center;
    padding: 16px 24px 12px;
    border-bottom: 1.5px solid {INK};
  }}
  .hero-kicker {{
    font-family: 'Playfair Display', serif;
    font-size: clamp(0.75rem, 2vw, 1.1rem);
    font-weight: 700;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: {INK_LIGHT};
  }}
  .hero-head {{
    font-family: 'Playfair Display', serif;
    font-size: clamp(2rem, 7vw, 4.4rem);
    font-weight: 900;
    line-height: 1;
    letter-spacing: -0.01em;
    color: {INK};
  }}
  .hero-sub {{
    font-family: 'IM Fell English', serif;
    font-style: italic;
    font-size: clamp(1rem, 2.5vw, 1.45rem);
    color: {INK_LIGHT};
    margin-top: 4px;
  }}
  .video-slot {{
    padding: 18px 24px;
    border-bottom: 2px solid {INK};
  }}
  .byline {{
    text-align: center;
    font-family: 'IM Fell English', serif;
    font-style: italic;
    font-size: clamp(0.9rem, 2vw, 1.2rem);
    letter-spacing: 0.05em;
    padding: 10px 0 12px;
    color: {INK};
  }}

  /* ── 2-col spread ── */
  .spread {{
    display: grid;
    grid-template-columns: 1fr 1.5px 1fr;
    border-top: 1px solid {INK};
  }}
  .spread-col {{ padding: 16px 18px; }}
  .spread-divider {{ background: {INK}; }}

  /* ── story page: photo row + text below ── */
  .story-head {{
    text-align: center;
    padding: 14px 24px 10px;
    border-bottom: 2px solid {INK};
    font-family: 'Playfair Display', serif;
    font-size: clamp(1.6rem, 4.5vw, 2.8rem);
    font-weight: 900;
    color: {INK};
  }}
  .photo-row {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
    border-bottom: 1.5px solid {INK};
  }}
  .photo-row img, .photo-row div {{
    display: block;
    width: 100%;
  }}
  .photo-row > *:first-child {{
    border-right: 0.75px solid {INK};
  }}
  .text-block {{
    display: grid;
    grid-template-columns: 1fr 1.5px 1fr;
    border-bottom: 1px solid {INK};
  }}
  .text-col {{ padding: 16px 18px; }}
  .body-p {{
    font-size: 0.75rem;
    line-height: 1.8;
    color: {INK_LIGHT};
    text-align: justify;
    hyphens: auto;
  }}

  /* ── Always Yours ── */
  .always-yours {{
    border-top: 1px solid {INK};
    padding: 14px 18px 18px;
    text-align: center;
  }}
  .always-head {{
    font-family: 'Playfair Display', serif;
    font-weight: 900;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    border-bottom: 1px solid {INK};
    padding-bottom: 6px;
    margin-bottom: 10px;
    color: {INK};
  }}
  .always-item {{
    font-family: 'IM Fell English', serif;
    font-style: italic;
    font-size: 0.82rem;
    color: {INK_LIGHT};
    padding: 4px 0;
    border-bottom: 0.5px solid {ACCENT};
  }}
  .always-item:last-child {{ border-bottom: none; }}

  .footer {{
    max-width: 860px;
    margin: 0 auto;
    text-align: center;
    font-size: 0.52rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: {ACCENT};
    padding: 14px 0;
    opacity: 0.7;
  }}
</style>
</head>
<body>

<!-- PAGE 1 — FRONT COVER -->
<div class="page">
  <div class="masthead">
    <div class="masthead-title">The Love Gazette</div>
    <div class="masthead-meta">
      <span>{VOL_LINE}</span><span>{DATE_LINE}</span><span>{CITY_LINE}</span>
    </div>
  </div>
  <div class="hero-block">
    <div class="hero-kicker">{ANNIVERSARY_TEXT}</div>
    <div class="hero-head">{ANNIVERSARY_TEXT.upper()}</div>
    <div class="hero-sub">{SUBTITLE}</div>
  </div>
  <div class="video-slot">{video_tag()}</div>
  <div class="byline">{PARTNER_NAMES}</div>
</div>


<!-- PAGE 2 — PHOTOS + STORY -->
<div class="page">
  <div class="masthead">
    <div class="masthead-title" style="font-size:clamp(1.2rem,3.5vw,2rem);">The Love Gazette</div>
    <div class="masthead-meta">
      <span>{VOL_LINE}</span><span>{DATE_LINE}</span><span>{CITY_LINE}</span>
    </div>
  </div>

  <!-- top: two photos at fixed equal height -->
  <div style="display:grid;grid-template-columns:1fr 1.5px 1fr;border-bottom:1.5px solid {INK};">
    <div style="overflow:hidden;height:300px;"><img src="{photo_src(0)}" style="width:100%;height:100%;object-fit:cover;object-position:center;display:block;" /></div>
    <div style="background:{INK};"></div>
    <div style="overflow:hidden;height:300px;"><img src="{photo_src(1)}" style="width:100%;height:100%;object-fit:cover;object-position:center;display:block;" /></div>
  </div>

  <!-- bottom: two text columns -->
  <div class="text-block">
    <div class="text-col">
      <p class="body-p">{PARA_1}</p>
    </div>
    <div style="background:{INK};"></div>
    <div class="text-col">
      <p class="body-p">{PARA_2}</p>
    </div>
  </div>

  <div class="byline">{PARTNER_NAMES}</div>
</div>


<!-- PAGE 3 — THE STORY OF US -->
<div class="page">
  <div class="masthead">
    <div class="masthead-title" style="font-size:clamp(1.2rem,3.5vw,2rem);">The Love Gazette</div>
    <div class="masthead-meta">
      <span>{VOL_LINE}</span><span>{DATE_LINE}</span><span>{CITY_LINE}</span>
    </div>
  </div>

  <div class="story-head">The Story of Us</div>

  <!-- top: two photos at fixed equal height -->
  <div style="display:grid;grid-template-columns:1fr 1.5px 1fr;border-bottom:1.5px solid {INK};">
    <div style="overflow:hidden;height:320px;"><img src="{photo_src(2)}" style="width:100%;height:100%;object-fit:cover;object-position:center;display:block;" /></div>
    <div style="background:{INK};"></div>
    <div style="overflow:hidden;height:320px;"><img src="{photo_src(3)}" style="width:100%;height:100%;object-fit:cover;object-position:center;display:block;" /></div>
  </div>

  <!-- three photos in equal columns -->
  <div style="display:grid;grid-template-columns:1fr 1.5px 1fr 1.5px 1fr;border-top:1.5px solid {INK};">
    <div style="overflow:hidden;height:280px;"><img src="{photo_src(4)}" style="width:100%;height:100%;object-fit:cover;object-position:center;display:block;" /></div>
    <div style="background:{INK};"></div>
    <div style="overflow:hidden;height:280px;"><img src="{photo_src(5)}" style="width:100%;height:100%;object-fit:cover;object-position:center;display:block;" /></div>
    <div style="background:{INK};"></div>
    <div class="always-yours" style="border-top:none;">
      <div class="always-head">Always Yours</div>
      {"".join(f'<div class="always-item">&#8226;&nbsp; {item}</div>' for item in ALWAYS_YOURS_ITEMS)}
    </div>
  </div>
</div>

<div class="footer">The Love Gazette &nbsp;·&nbsp; Printed with Love</div>
</body>
</html>"""

components.html(html, height=3600, scrolling=False)
