import streamlit as st
import streamlit.components.v1 as components
import re, base64
from pathlib import Path

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG — edit everything here
# ══════════════════════════════════════════════════════════════════════════════

PARTNER_NAMES    = "Hussein & Abhineet"
ANNIVERSARY_TEXT = "One Year"
SUBTITLE         = ""
DATE_LINE        = "SATURDAY, 26 APRIL 2025"
CITY_LINE        = "Mohali, Plaksha"
VOL_LINE         = "VOL. 1"

OUR_STORY_HEADLINE = "OUR DEAREST"
OUR_STORY_SUBHEAD  = "Journey"
OUR_STORY_BODY = (
    "From the very first moment we met, something shifted — quietly, almost without notice, "
    "the way morning light changes a room. This year has been filled with shared coffee cups, "
    "long walks, unexpected laughter, and the kind of warmth that stays. "
    "Every adventure we have taken together has written itself into who we are. "
    "The moments big and small, all of it — ours."
)

LOVE_ALL_HEADLINE = "LOVE ALL"
LOVE_ALL_SUBHEAD  = "Around"
LOVE_ALL_BODY = (
    "Love isn't one grand gesture. It lives in the details: a note left on the counter, "
    "a song played for no reason, a hand found in the dark. "
    "We've collected these moments like pressed flowers — fragile, beautiful, kept."
)

BEST_PART_HEADLINE = "THE BEST PART OF OUR STORY"
BEST_PART_BODY = (
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
# Change these hex values to restyle the whole gazette.
#
#   PAGE_BG   : outer background behind the newspaper
#   PAPER_BG  : the newspaper page itself
#   INK       : headlines, borders, main text
#   INK_LIGHT : body copy, captions, meta text
#   ACCENT    : placeholder boxes, subtle tints
#
PAGE_BG   = "#ede4f0"
PAPER_BG  = "#f7f2fa"
INK       = "#3b1f4e"
INK_LIGHT = "#6b4a82"
ACCENT    = "#ddd0eb"

# ── PHOTOS ────────────────────────────────────────────────────────────────────
# Option A (default): local files in Base/Media/
#   Name them photo_01.jpg … photo_06.jpg  (or .png)
#   They are embedded as base64 — no server needed.
#
# Option B: Google Drive / any public image URL
#   Replace None below with the direct image URL, e.g.:
#   PHOTO_URLS = [
#       "https://drive.google.com/uc?export=view&id=FILE_ID_1",
#       "https://drive.google.com/uc?export=view&id=FILE_ID_2",
#       ...  (6 entries total)
#   ]
#   For Google Drive: share the file publicly, then use
#   https://drive.google.com/uc?export=view&id=YOUR_FILE_ID
#
PHOTO_URLS = None   # set to a list of 6 URLs to use Drive instead of local files

# ── VIDEO ─────────────────────────────────────────────────────────────────────
# 1. Upload your .mp4 to Google Drive
# 2. Right-click → Share → "Anyone with the link can view" → Copy link
# 3. Paste that link below
GOOGLE_DRIVE_VIDEO_URL = "https://drive.google.com/file/d/1QD3ng198KXxSXWjBAEt_9ytau2C5-Qb7/view?usp=drive_link"

# ══════════════════════════════════════════════════════════════════════════════
# INTERNALS
# ══════════════════════════════════════════════════════════════════════════════

st.set_page_config(page_title="The Love Gazette", layout="wide",
                   initial_sidebar_state="collapsed")

# Hide Streamlit chrome
st.markdown("""
<style>
[data-testid="stHeader"]{display:none;}
.block-container{padding:0!important;max-width:100%!important;}
footer{display:none;}
[data-testid="stAppViewContainer"]{background:#2a2a2a;}
</style>""", unsafe_allow_html=True)

BASE_DIR  = Path(__file__).resolve().parent.parent
MEDIA_DIR = BASE_DIR / "Media"

def _local_photos():
    paths = sorted(MEDIA_DIR.glob("photo_*.jpg")) + sorted(MEDIA_DIR.glob("photo_*.png"))
    return sorted(paths, key=lambda p: p.name)

def gdrive_embed_url(url: str):
    m = re.search(r"/d/([a-zA-Z0-9_-]+)", url)
    if not m:
        m = re.search(r"[?&]id=([a-zA-Z0-9_-]+)", url)
    return f"https://drive.google.com/file/d/{m.group(1)}/preview" if m else None

def photo_src(idx: int) -> str:
    """Return an img src — either a URL (Drive) or base64 (local)."""
    if PHOTO_URLS and idx < len(PHOTO_URLS):
        return PHOTO_URLS[idx]
    local = _local_photos()
    if idx < len(local):
        p = local[idx]
        mime = "jpeg" if p.suffix.lower() in (".jpg", ".jpeg") else "png"
        data = base64.b64encode(p.read_bytes()).decode()
        return f"data:image/{mime};base64,{data}"
    return ""   # no image available

def photo_tag(idx: int, height="200px") -> str:
    src = photo_src(idx)
    if src:
        return (f'<img src="{src}" style="width:100%;height:auto;'
                f'display:block;margin:8px 0;border:1px solid {ACCENT};" />')
    return (f'<div style="width:100%;height:{height};background:{ACCENT};'
            f'display:flex;align-items:center;justify-content:center;'
            f'margin:8px 0;color:{INK_LIGHT};font-style:italic;font-size:0.75rem;">'
            f'Photo {idx+1}</div>')

def video_tag() -> str:
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
           background:#111;border:1px solid {INK};text-align:center;
           color:#777;font-style:italic;font-size:0.82rem;">
        Paste your Google Drive link into<br>
        <code style="color:#aaa;font-size:0.75rem;">GOOGLE_DRIVE_VIDEO_URL</code> in app.py
      </div>"""

def always_yours() -> str:
    rows = "".join(
        f'<div style="padding:5px 0;border-bottom:0.5px solid {ACCENT};">'
        f'&#8226;&nbsp; {item}</div>'
        for item in ALWAYS_YOURS_ITEMS
    )
    return rows

# ── Build the full HTML document ──────────────────────────────────────────────
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700&family=IM+Fell+English:ital@0;1&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: {PAGE_BG};
    font-family: 'Libre Baskerville', Georgia, serif;
    color: {INK};
    padding: 28px 16px 60px;
  }}

  /* ── Newspaper page wrapper ── */
  .page {{
    max-width: 860px;
    margin: 0 auto 32px auto;
    background: {PAPER_BG};
    border: 1.5px solid {INK};
  }}

  /* ── Masthead ── */
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

  /* ── Hero headline block ── */
  .hero-block {{
    text-align: center;
    padding: 16px 24px 10px;
    border-bottom: 1.5px solid {INK};
  }}
  .hero-kicker {{
    font-family: 'Playfair Display', serif;
    font-size: clamp(0.75rem, 2vw, 1.1rem);
    font-weight: 700;
    letter-spacing: 0.35em;
    text-transform: uppercase;
  }}
  .hero-head {{
    font-family: 'Playfair Display', serif;
    font-size: clamp(2rem, 7vw, 4.4rem);
    font-weight: 900;
    line-height: 1;
    letter-spacing: -0.01em;
  }}
  .hero-sub {{
    font-family: 'IM Fell English', serif;
    font-style: italic;
    font-size: clamp(1rem, 2.5vw, 1.45rem);
    color: {INK_LIGHT};
    margin-top: 3px;
  }}

  /* ── Video slot ── */
  .video-slot {{
    padding: 18px 24px;
    border-bottom: 2px solid {INK};
  }}

  /* ── Byline ── */
  .byline {{
    text-align: center;
    font-family: 'IM Fell English', serif;
    font-style: italic;
    font-size: clamp(0.9rem, 2vw, 1.2rem);
    letter-spacing: 0.05em;
    padding: 10px 0 12px;
    border-top: 0.75px solid {INK};
  }}

  /* ── Two-column spread ── */
  .spread {{
    display: grid;
    grid-template-columns: 1fr 1.5px 1fr;
  }}
  .spread-col {{
    padding: 14px 16px;
  }}
  .spread-divider {{
    background: {INK};
  }}
  .spread-border {{
    border-bottom: 2px solid {INK};
  }}

  /* ── Section heads ── */
  .sec-head {{
    font-family: 'Playfair Display', serif;
    font-size: clamp(0.82rem, 1.8vw, 1rem);
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    border-bottom: 1px solid {INK};
    padding-bottom: 3px;
    margin-bottom: 7px;
  }}
  .sec-sub {{
    font-family: 'IM Fell English', serif;
    font-style: italic;
    font-size: clamp(0.9rem, 2vw, 1.2rem);
    margin-bottom: 6px;
  }}
  .body-p {{
    font-size: 0.72rem;
    line-height: 1.72;
    color: {INK_LIGHT};
    text-align: justify;
    hyphens: auto;
    margin: 7px 0;
  }}

  /* ── Sidebar box ── */
  .sidebar-box {{
    border: 1px solid {INK};
    padding: 10px 12px;
    margin-top: 14px;
  }}
  .sidebar-box-head {{
    font-family: 'Playfair Display', serif;
    font-weight: 900;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    text-align: center;
    border-bottom: 1px solid {INK};
    padding-bottom: 5px;
    margin-bottom: 8px;
  }}
  .sidebar-box-item {{
    font-size: 0.65rem;
    line-height: 1;
    color: {INK_LIGHT};
    text-align: center;
    padding: 5px 0;
    border-bottom: 0.5px solid {ACCENT};
  }}
  .sidebar-box-item:last-child {{ border-bottom: none; }}

  /* ── Mini headline (pages 2 & 3) ── */
  .mini-headline {{
    text-align: center;
    padding: 9px 16px 7px;
    border-bottom: 1px solid {INK};
  }}
  .mini-kicker {{
    font-family: 'Playfair Display', serif;
    font-size: clamp(0.6rem, 1.5vw, 0.8rem);
    font-weight: 700;
    letter-spacing: 0.3em;
    text-transform: uppercase;
  }}
  .mini-head {{
    font-family: 'Playfair Display', serif;
    font-size: clamp(1.4rem, 4vw, 2.5rem);
    font-weight: 900;
    line-height: 1.05;
  }}
  .mini-sub {{
    font-family: 'IM Fell English', serif;
    font-style: italic;
    font-size: clamp(0.85rem, 2vw, 1rem);
    color: {INK_LIGHT};
  }}

  /* ── Page 3 story head ── */
  .story-head {{
    text-align: center;
    padding: 14px 24px 10px;
    border-bottom: 2px solid {INK};
    font-family: 'Playfair Display', serif;
    font-size: clamp(1.6rem, 4.5vw, 2.8rem);
    font-weight: 900;
    line-height: 1;
    letter-spacing: 0.01em;
  }}

  /* ── Footer ── */
  .footer {{
    max-width: 860px;
    margin: 0 auto;
    text-align: center;
    font-size: 0.52rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: {INK_LIGHT};
    padding: 14px 0 4px;
    opacity: 0.7;
  }}
</style>
</head>
<body>

<!-- ═══════════════════════════════════════════
     PAGE 1 — FRONT COVER
════════════════════════════════════════════ -->
<div class="page">

  <div class="masthead">
    <div class="masthead-title">The Love Gazette</div>
    <div class="masthead-meta">
      <span>{VOL_LINE}</span>
      <span>{DATE_LINE}</span>
      <span>{CITY_LINE}</span>
    </div>
  </div>

  <div class="hero-block">
    <div class="hero-kicker">{ANNIVERSARY_TEXT}</div>
    <div class="hero-head">{ANNIVERSARY_TEXT.upper()}</div>
    <div class="hero-sub">{SUBTITLE}</div>
  </div>

  <div class="video-slot">
    {video_tag()}
  </div>

  <div class="byline">{PARTNER_NAMES}</div>

</div>


<!-- ═══════════════════════════════════════════
     PAGE 2 — INSIDE SPREAD
════════════════════════════════════════════ -->
<div class="page">

  <div class="masthead" style="font-size:0.85em;">
    <div class="masthead-title" style="font-size:clamp(1.2rem,3.5vw,1.9rem);">The Love Gazette</div>
    <div class="masthead-meta">
      <span>{VOL_LINE}</span><span>{DATE_LINE}</span><span>{CITY_LINE}</span>
    </div>
  </div>

  <div class="mini-headline">
    <div class="mini-kicker">{ANNIVERSARY_TEXT}</div>
    <div class="mini-head">{ANNIVERSARY_TEXT.upper()}</div>
    <div class="mini-sub">{SUBTITLE}</div>
  </div>

  <div class="spread spread-border">

    <div class="spread-col">
      <div class="sec-head">{OUR_STORY_HEADLINE}</div>
      <div class="sec-sub">{OUR_STORY_SUBHEAD}</div>
      {photo_tag(0, "210px")}
      <p class="body-p">{OUR_STORY_BODY}</p>
      {photo_tag(1, "210px")}
    </div>

    <div class="spread-divider"></div>

    <div class="spread-col">
      <div class="sec-head">{LOVE_ALL_HEADLINE}</div>
      <div class="sec-sub">{LOVE_ALL_SUBHEAD}</div>
      {photo_tag(2, "210px")}
      <p class="body-p">{LOVE_ALL_BODY}</p>
      <div class="byline" style="font-size:0.82rem;margin-top:10px;">{PARTNER_NAMES}</div>
    </div>

  </div>

</div>


<!-- ═══════════════════════════════════════════
     PAGE 3 — THE STORY OF US
════════════════════════════════════════════ -->
<div class="page">

  <div class="masthead" style="font-size:0.85em;">
    <div class="masthead-title" style="font-size:clamp(1.2rem,3.5vw,1.9rem);">The Love Gazette</div>
    <div class="masthead-meta">
      <span>{VOL_LINE}</span><span>{DATE_LINE}</span><span>{CITY_LINE}</span>
    </div>
  </div>

  <div class="story-head">THE STORY OF US</div>

  <div class="spread">

    <div class="spread-col">
      <div class="sec-head">OUR BEST CHAPTER</div>
      {photo_tag(3, "200px")}
      <p class="body-p">{OUR_STORY_BODY}</p>
      {photo_tag(4, "200px")}
      <p class="body-p">{LOVE_ALL_BODY}</p>
    </div>

    <div class="spread-divider"></div>

    <div class="spread-col">
      <div class="sec-head">{BEST_PART_HEADLINE}</div>
      {photo_tag(5, "200px")}
      <p class="body-p">{BEST_PART_BODY}</p>

      <div class="sidebar-box">
        <div class="sidebar-box-head">ALWAYS YOURS</div>
        {"".join(f'<div class="sidebar-box-item">&#8226;&nbsp;{item}</div>' for item in ALWAYS_YOURS_ITEMS)}
      </div>
    </div>

  </div>

</div>

<div class="footer">The Love Gazette &nbsp;·&nbsp; Printed with Love</div>

</body>
</html>"""

# Render as a true iframe — bypasses Streamlit's HTML sanitizer
components.html(html, height=3800, scrolling=False)
