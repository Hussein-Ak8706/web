import streamlit as st
import os
import re
from pathlib import Path

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="The Love Gazette",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).resolve().parent.parent   # Base/
MEDIA_DIR  = BASE_DIR / "Media"

PHOTO_PATHS = sorted(MEDIA_DIR.glob("photo_*.jpg")) + sorted(MEDIA_DIR.glob("photo_*.png"))

# ── Google Drive video ────────────────────────────────────────────────────────
# Paste your Google Drive share link here.
# Make sure the file is shared as "Anyone with the link can view".
# Supported formats:
#   https://drive.google.com/file/d/FILE_ID/view?usp=sharing
#   https://drive.google.com/open?id=FILE_ID
GOOGLE_DRIVE_VIDEO_URL = "https://drive.google.com/file/d/1QD3ng198KXxSXWjBAEt_9ytau2C5-Qb7/view?usp=drive_link"

def gdrive_embed_url(share_url: str) -> str | None:
    """Convert a Google Drive share link to a direct embed URL."""
    match = re.search(r"/d/([a-zA-Z0-9_-]+)", share_url)
    if not match:
        match = re.search(r"[?&]id=([a-zA-Z0-9_-]+)", share_url)
    if match:
        file_id = match.group(1)
        return f"https://drive.google.com/file/d/{file_id}/preview"
    return None

# ── Config (edit these) ───────────────────────────────────────────────────────
PARTNER_NAMES   = "Hussein & Abhineet"
ANNIVERSARY_TEXT = "One Year"
SUBTITLE         = ""
DATE_LINE        = "26 APRIL 2025"
CITY_LINE        = ""
VOL_LINE         = ""

OUR_STORY_HEADLINE = ""
OUR_STORY_SUBHEAD  = ""
OUR_STORY_BODY     = """

"""

LOVE_ALL_HEADLINE  = "LOVE YOU"
LOVE_ALL_SUBHEAD   = ""
LOVE_ALL_BODY      = """
"""

BEST_PART_HEADLINE = ""
BEST_PART_BODY     = """
"""

ALWAYS_YOURS_TEXT = "ALWAYS YOURS"
ALWAYS_YOURS_BODY = """
• Every morning with you\n• Every laugh we've shared\n• Every lap we've taken around campus\n• Every moment still ahead
"""

# ── Helpers ───────────────────────────────────────────────────────────────────
def photo_placeholder(label="Photo"):
    """Returns an SVG placeholder string."""
    return f"""
    <div class="photo-placeholder">
        <svg viewBox="0 0 80 60" xmlns="http://www.w3.org/2000/svg">
            <rect width="80" height="60" fill="#f0ece4" rx="2"/>
            <polyline points="0,60 25,30 45,45 60,25 80,50 80,60" fill="#d8d0c4" stroke="none"/>
            <circle cx="22" cy="18" r="7" fill="#c8bfb0"/>
            <text x="40" y="55" text-anchor="middle" font-size="6" fill="#999">{label}</text>
        </svg>
    </div>
    """

def render_photo(idx, width="100%"):
    """Render a real photo if available, otherwise a placeholder."""
    if idx < len(PHOTO_PATHS):
        return f'<img src="{PHOTO_PATHS[idx].as_uri()}" style="width:{width};object-fit:cover;" />'
    return photo_placeholder(f"Photo {idx+1}")

def render_video():
    embed_url = gdrive_embed_url(GOOGLE_DRIVE_VIDEO_URL)
    if embed_url and "YOUR_FILE_ID_HERE" not in GOOGLE_DRIVE_VIDEO_URL:
        st.markdown(f"""
        <div style="position:relative; padding-bottom:56.25%; height:0; overflow:hidden; background:#111;">
            <iframe
                src="{embed_url}"
                style="position:absolute; top:0; left:0; width:100%; height:100%; border:none;"
                allowfullscreen
                allow="autoplay"
            ></iframe>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:#1a1a1a; color:#888; text-align:center;
             padding:60px 20px; font-family:Georgia,serif; font-style:italic; font-size:0.85rem;">
            Paste your Google Drive share link into<br>
            <code style="color:#aaa;">GOOGLE_DRIVE_VIDEO_URL</code> in app.py
        </div>
        """, unsafe_allow_html=True)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700&family=IM+Fell+English:ital@0;1&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap');

/* ── Reset Streamlit chrome ── */
[data-testid="stAppViewContainer"] { background: #f5f0e8; }
[data-testid="stHeader"] { display: none; }
.block-container { padding: 0 !important; max-width: 100% !important; }
footer { display: none; }
[data-testid="stVerticalBlock"] > div { gap: 0 !important; }

/* ── Newspaper shell ── */
.gazette-wrapper {
    max-width: 960px;
    margin: 32px auto 60px auto;
    background: #faf6ee;
    border: 1.5px solid #1a1a1a;
    font-family: 'Libre Baskerville', Georgia, serif;
    color: #1a1a1a;
}

/* ── Masthead ── */
.masthead {
    border-bottom: 2.5px solid #1a1a1a;
    padding: 10px 16px 6px;
    text-align: center;
}
.masthead-title {
    font-family: 'UnifrakturMaguntia', cursive;
    font-size: clamp(2rem, 6vw, 3.6rem);
    letter-spacing: 0.04em;
    line-height: 1;
    color: #1a1a1a;
}
.masthead-meta {
    display: flex;
    justify-content: space-between;
    font-size: 0.55rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #444;
    padding: 4px 0 2px;
    border-top: 0.75px solid #1a1a1a;
    border-bottom: 0.75px solid #1a1a1a;
    margin-top: 4px;
}

/* ── Hero headline ── */
.hero-headline-block {
    text-align: center;
    padding: 18px 24px 8px;
    border-bottom: 1px solid #1a1a1a;
}
.hero-kicker {
    font-family: 'Playfair Display', serif;
    font-size: clamp(0.9rem, 3vw, 1.5rem);
    font-weight: 700;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    margin-bottom: 2px;
}
.hero-headline {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.2rem, 7vw, 5rem);
    font-weight: 900;
    line-height: 1.0;
    letter-spacing: -0.01em;
}
.hero-subtitle {
    font-family: 'IM Fell English', Georgia, serif;
    font-style: italic;
    font-size: clamp(1rem, 3vw, 1.6rem);
    margin-top: 2px;
    color: #333;
}

/* ── Front page body ── */
.front-body {
    display: grid;
    grid-template-columns: 1fr;
    padding: 16px;
    gap: 12px;
    border-bottom: 2px solid #1a1a1a;
}
.video-frame {
    border: 1px solid #bbb;
    background: #111;
    min-height: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.byline {
    text-align: center;
    font-family: 'IM Fell English', Georgia, serif;
    font-style: italic;
    font-size: clamp(1rem, 2.5vw, 1.3rem);
    letter-spacing: 0.06em;
    padding: 8px 0 4px;
    border-top: 0.75px solid #1a1a1a;
}

/* ── Hairline dividers ── */
.h-rule { border: none; border-top: 1px solid #1a1a1a; margin: 0; }
.h-rule-thick { border: none; border-top: 2px solid #1a1a1a; margin: 0; }

/* ── Inside spread ── */
.spread {
    display: grid;
    grid-template-columns: 1fr 2px 1fr;
    gap: 0;
    border-bottom: 2px solid #1a1a1a;
}
.spread-col {
    padding: 14px;
}
.spread-divider { background: #1a1a1a; }

/* ── Story page ── */
.story-spread {
    display: grid;
    grid-template-columns: 1fr 2px 1fr;
    gap: 0;
}
.story-col { padding: 14px; }

/* ── Section headline ── */
.sec-head {
    font-family: 'Playfair Display', serif;
    font-size: clamp(0.9rem, 2.5vw, 1.3rem);
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    border-bottom: 1px solid #1a1a1a;
    margin-bottom: 6px;
    padding-bottom: 3px;
}
.sec-subhead {
    font-family: 'IM Fell English', serif;
    font-style: italic;
    font-size: clamp(1rem, 2.5vw, 1.4rem);
    margin-bottom: 6px;
    color: #222;
}
.body-text {
    font-size: 0.72rem;
    line-height: 1.65;
    color: #222;
    text-align: justify;
    hyphens: auto;
}
.photo-placeholder {
    background: #e8e2d8;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 8px 0;
}
.photo-placeholder svg { width: 100%; height: auto; display: block; }

/* ── Always Yours sidebar ── */
.sidebar-box {
    border: 1px solid #1a1a1a;
    padding: 10px;
    margin-top: 10px;
}
.sidebar-box-head {
    font-family: 'Playfair Display', serif;
    font-weight: 900;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    text-align: center;
    border-bottom: 1px solid #1a1a1a;
    margin-bottom: 6px;
    padding-bottom: 4px;
}
.sidebar-box-body {
    font-size: 0.65rem;
    line-height: 2;
    color: #333;
    text-align: center;
}

/* ── Partner page ── */
.partner-page {
    display: grid;
    grid-template-columns: 1fr 2px 1fr;
}
.partner-col { padding: 14px; text-align: center; }
.partner-name {
    font-family: 'IM Fell English', serif;
    font-style: italic;
    font-size: clamp(0.9rem, 2vw, 1.15rem);
    margin-top: 8px;
    color: #333;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1  –  FRONT COVER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="gazette-wrapper">

  <!-- MASTHEAD -->
  <div class="masthead">
    <div class="masthead-title">The Love Gazette</div>
    <div class="masthead-meta">
      <span>{VOL_LINE}</span>
      <span>{DATE_LINE}</span>
      <span>{CITY_LINE}</span>
    </div>
  </div>

  <!-- HERO HEADLINE -->
  <div class="hero-headline-block">
    <div class="hero-kicker">{ANNIVERSARY_TEXT}</div>
    <div class="hero-headline">{ANNIVERSARY_TEXT.upper()}</div>
    <div class="hero-subtitle">{SUBTITLE}</div>
  </div>

  <!-- VIDEO SLOT -->
  <div class="front-body">
""", unsafe_allow_html=True)

# Streamlit-native video (must be outside raw HTML)
render_video()

st.markdown(f"""
    <div class="byline">{PARTNER_NAMES}</div>
  </div>

</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2  –  INSIDE SPREAD (small photos + story columns)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="gazette-wrapper">

  <!-- MASTHEAD (condensed) -->
  <div class="masthead">
    <div class="masthead-title" style="font-size:1.6rem;">The Love Gazette</div>
    <div class="masthead-meta">
      <span>{VOL_LINE}</span>
      <span>{DATE_LINE}</span>
      <span>{CITY_LINE}</span>
    </div>
  </div>

  <!-- MINI HEADLINE STRIP -->
  <div style="text-align:center; padding:10px 16px; border-bottom:1px solid #1a1a1a;">
    <div class="hero-kicker" style="font-size:0.75rem;">{ANNIVERSARY_TEXT}</div>
    <div class="hero-headline" style="font-size:2.4rem;">{ANNIVERSARY_TEXT.upper()}</div>
    <div class="hero-subtitle" style="font-size:1rem;">{SUBTITLE}</div>
  </div>

  <div class="spread">
    <!-- LEFT COLUMN -->
    <div class="spread-col">
      <div class="sec-head">{OUR_STORY_HEADLINE}</div>
      <div class="sec-subhead">{OUR_STORY_SUBHEAD}</div>
      {render_photo(0)}
      <p class="body-text">{OUR_STORY_BODY.strip()}</p>
      {render_photo(1)}
    </div>

    <div class="spread-divider"></div>

    <!-- RIGHT COLUMN -->
    <div class="spread-col">
      <div class="sec-head">{LOVE_ALL_HEADLINE}</div>
      <div class="sec-subhead">{LOVE_ALL_SUBHEAD}</div>
      {render_photo(2)}
      <p class="body-text">{LOVE_ALL_BODY.strip()}</p>
      <div class="byline" style="font-size:0.85rem;">{PARTNER_NAMES}</div>
    </div>
  </div>

</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3  –  THE STORY OF US
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="gazette-wrapper">

  <!-- STORY HEADLINE -->
  <div class="masthead">
    <div class="masthead-title" style="font-size:1.6rem;">The Love Gazette</div>
    <div class="masthead-meta">
      <span>{VOL_LINE}</span><span>{DATE_LINE}</span><span>{CITY_LINE}</span>
    </div>
  </div>

  <div style="text-align:center; padding:14px 24px 10px; border-bottom:2px solid #1a1a1a;">
    <div class="hero-headline" style="font-size:2.8rem;">THE STORY OF US</div>
  </div>

  <div class="story-spread">

    <!-- LEFT -->
    <div class="story-col">
      <div class="sec-head">OUR BEST CHAPTER</div>
      {render_photo(3)}
      <p class="body-text">{OUR_STORY_BODY.strip()}</p>
      {render_photo(4)}
      <p class="body-text">{LOVE_ALL_BODY.strip()}</p>
    </div>

    <div class="spread-divider"></div>

    <!-- RIGHT -->
    <div class="story-col">
      <div class="sec-head">{BEST_PART_HEADLINE}</div>
      {render_photo(5)}
      <p class="body-text">{BEST_PART_BODY.strip()}</p>

      <div class="sidebar-box">
        <div class="sidebar-box-head">{ALWAYS_YOURS_TEXT}</div>
        <div class="sidebar-box-body">{ALWAYS_YOURS_BODY.strip()}</div>
      </div>
    </div>

  </div>

</div>
""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; color:#888; font-size:0.6rem;
     letter-spacing:0.15em; text-transform:uppercase; padding:24px 0 40px;">
  The Love Gazette &nbsp;·&nbsp; Printed with Love
</div>
""", unsafe_allow_html=True)
