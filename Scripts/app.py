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
CITY_LINE        = "Plaksha, Mohali"
VOL_LINE         = "VOL. 1"

PARA_1 = (
    "The past year has been super crazy. "
    "The first time I saw you singing riptide I never would've thought we'd end up together and thats such a surreal feeling. "
    "Started to talk cuz we were part of the same band and kept talking cuz of music first then gradually more because someone started to catch feelings. "
    "Staying up till 5 am after studying just yapping together and then in the next sem the never ending walks. "
    "I never thought I could enjoy being with someone this much, laughing at every small stupid thing and sharing my autistic memes."
)

PARA_2 = (
    "And it's only gotten better since we got together. Staying together till dawn, "
    "talking all the time and often just enjoying each others company in silence — all of it has to be my fav time of the day. "
    "Everytime you've come to me for help and vice-versa, gone to the music room to jamm and sing, "
    "ordering and sharing food, making silly faces and doing silly trends we found on reels — "
    "all of it has been magical and I'm so happy that I fell in love with you. Happy Anniversary love."
)

ALWAYS_YOURS_ITEMS = [
    "Every silly moment with you",
    "Every laugh we've had",
    "Every lap of the campus we've taken",
    "All the food we've shared",
    "Every moment still ahead",
]

GATE_BG          = "#ffb6c1"   # pink background
GATE_CARD_BG     = "#fff0f5"   # card background
GATE_INK         = "#8b0057"   # dark text / button color
GATE_INK_LIGHT   = "#c2185b"   # lighter text
GATE_BUTTON_BG   = "#ff1493"   # hot pink button
GATE_BUTTON_TEXT = "#ffffff"
GATE_TITLE       = "For The Man Of My Life 🎀"
GATE_SUBTITLE    = "Enter our special date to unlock"
GATE_PLACEHOLDER = "DD / MM / YYYY"
GATE_BUTTON_TEXT_LABEL = "Unlock MY Heart"
GATE_ERROR_TEXT  = "Hmm, that's not quite right... try again 💜"

ACCEPTED = {
    "2025-04-26", "26-04-2025", "26/04/2025", "2025/04/26",
    "26042025", "26 april 2025", "april 26 2025",
    "26 apr 2025", "apr 26 2025", "2604", "26april", "april26"
}

# ── COLORS ───────────────────────────────────────────────────────────────────
PAGE_BG   = "#ba99c5"
PAPER_BG  = "#f7f2fa"
INK       = "#3b1f4e"
INK_LIGHT = "#6b4a82"
ACCENT    = "#ddd0eb"

# ── PHOTOS ───────────────────────────────────────────────────────────────────
PHOTO_URLS = None

# ── VIDEO ─────────────────────────────────────────────────────────────────────
GOOGLE_DRIVE_VIDEO_URL = "https://drive.google.com/file/d/1QD3ng198KXxSXWjBAEt_9ytau2C5-Qb7/view?usp=drive_link"

# ── MUSIC ─────────────────────────────────────────────────────────────────────
# 1. Upload an mp3 to Google Drive
# 2. Share it as "Anyone with the link can view"
# 3. Paste the share link below
# Set MUSIC_AUTOPLAY = True to start playing automatically on page load
# Set MUSIC_AUTOPLAY = False to show a play button instead
GOOGLE_DRIVE_MUSIC_URL = "https://drive.google.com/file/d/1GfcTF6OGsSIB0rqMCI7tBtN10AnPqS3h/view?usp=sharing"
MUSIC_AUTOPLAY = True

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
[data-testid="stAppViewContainer"]{background:#ba99c5;}
</style>""", unsafe_allow_html=True)

BASE_DIR  = Path(__file__).resolve().parent.parent
MEDIA_DIR = BASE_DIR / "Media"

def _local_photos():
    return sorted(
        sorted(MEDIA_DIR.glob("photo_*.jpg")) +
        sorted(MEDIA_DIR.glob("photo_*.png")),
        key=lambda p: p.name
    )

def gdrive_direct_url(url):
    """Convert any Drive share link to a direct streamable URL."""
    m = re.search(r"/d/([a-zA-Z0-9_-]+)", url)
    if not m:
        m = re.search(r"[?&]id=([a-zA-Z0-9_-]+)", url)
    return f"https://drive.google.com/uc?export=open&id={m.group(1)}" if m else None

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
      
def music_tag():
    if "YOUR_MUSIC_FILE_ID_HERE" in GOOGLE_DRIVE_MUSIC_URL:
        return ""
    embed = gdrive_embed_url(GOOGLE_DRIVE_MUSIC_URL)
    return f"""
    <!-- Hidden Drive audio iframe -->
    <iframe id="audio-frame"
      src=""
      style="position:absolute;width:1px;height:1px;opacity:0;pointer-events:none;"
      allow="autoplay">
    </iframe>

    <!-- Sticky top-right button -->
    <div style="position:sticky;top:16px;z-index:9999;
                display:flex;justify-content:flex-end;
                pointer-events:none;margin-bottom:-52px;">
      <div id="music-btn" onclick="toggleMusic()" style="
        width:44px;height:44px;border-radius:50%;
        background:{INK};border:2px solid {ACCENT};
        display:flex;align-items:center;justify-content:center;
        cursor:pointer;pointer-events:all;
        box-shadow:0 2px 12px rgba(0,0,0,0.35);
        transition:transform 0.15s ease;
        margin-right:16px;">
        <span id="music-icon" style="font-size:1.2rem;">▶</span>
      </div>
    </div>

    <script>
      var frame   = document.getElementById('audio-frame');
      var icon    = document.getElementById('music-icon');
      var btn     = document.getElementById('music-btn');
      var playing = false;
      var src     = "{embed}";

      function toggleMusic() {{
        if (!playing) {{
          frame.src = src;
          icon.textContent = '⏸';
          playing = true;
        }} else {{
          frame.src = '';
          icon.textContent = '▶';
          playing = false;
        }}
        btn.style.transform = 'scale(0.9)';
        setTimeout(function(){{ btn.style.transform = 'scale(1)'; }}, 120);
      }}
    </script>"""
    
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
  .spread {{
    display: grid;
    grid-template-columns: 1fr 1.5px 1fr;
    border-top: 1px solid {INK};
  }}
  .spread-col {{ padding: 16px 18px; }}
  .spread-divider {{ background: {INK}; }}
  .story-head {{
    text-align: center;
    padding: 14px 24px 10px;
    border-bottom: 2px solid {INK};
    font-family: 'Playfair Display', serif;
    font-size: clamp(1.6rem, 4.5vw, 2.8rem);
    font-weight: 900;
    color: {INK};
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

{music_tag()}

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
  <div style="display:grid;grid-template-columns:1fr 1.5px 1fr;border-bottom:1.5px solid {INK};">
    <div style="overflow:hidden;height:300px;"><img src="{photo_src(0)}" style="width:100%;height:100%;object-fit:cover;object-position:center;display:block;" /></div>
    <div style="background:{INK};"></div>
    <div style="overflow:hidden;height:300px;"><img src="{photo_src(1)}" style="width:100%;height:100%;object-fit:cover;object-position:center;display:block;" /></div>
  </div>
  <div class="text-block">
    <div class="text-col"><p class="body-p">{PARA_1}</p></div>
    <div style="background:{INK};"></div>
    <div class="text-col"><p class="body-p">{PARA_2}</p></div>
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
  <div style="display:grid;grid-template-columns:1fr 1.5px 1fr;border-bottom:1.5px solid {INK};">
    <div style="overflow:hidden;height:320px;"><img src="{photo_src(2)}" style="width:100%;height:100%;object-fit:cover;object-position:center;display:block;" /></div>
    <div style="background:{INK};"></div>
    <div style="overflow:hidden;height:320px;"><img src="{photo_src(3)}" style="width:100%;height:100%;object-fit:cover;object-position:center;display:block;" /></div>
  </div>
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

# ══════════════════════════════════════════════════════════════════════════════
# GATE
# ══════════════════════════════════════════════════════════════════════════════

if "unlocked" not in st.session_state:
    st.session_state.unlocked = False

if not st.session_state.unlocked:
    gate_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=IM+Fell+English:ital@1&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{
    min-height:100vh;
    background:{GATE_BG};
    display:flex; align-items:center; justify-content:center;
    font-family:'Playfair Display', Georgia, serif;
    padding:24px;
  }}
  .card {{
    background:{GATE_CARD_BG};
    border:1.5px solid {GATE_INK};
    border-radius:16px;
    padding:40px 32px 36px;
    max-width:380px;
    width:100%;
    text-align:center;
    box-shadow:0 4px 24px rgba(139,0,87,0.10);
  }}
  .hearts {{ font-size:2rem; margin-bottom:14px; }}
  .title {{
    font-size:1.5rem;
    font-weight:900;
    color:{GATE_INK};
    margin-bottom:8px;
  }}
  .sub {{
    font-family:'IM Fell English', serif;
    font-style:italic;
    font-size:0.95rem;
    color:{GATE_INK_LIGHT};
    margin-bottom:28px;
  }}
  .label {{
    font-size:0.7rem;
    text-transform:uppercase;
    letter-spacing:0.14em;
    color:{GATE_INK_LIGHT};
    margin-bottom:10px;
  }}
  input {{
    width:100%;
    padding:13px 16px;
    border:1.5px solid {GATE_INK};
    border-radius:10px;
    background:white;
    font-size:1rem;
    font-family:Georgia, serif;
    color:{GATE_INK};
    text-align:center;
    letter-spacing:0.08em;
    outline:none;
    margin-bottom:16px;
  }}
  input:focus {{ border-color:{GATE_BUTTON_BG}; }}
  button {{
    width:100%;
    padding:14px;
    background:{GATE_BUTTON_BG};
    color:{GATE_BUTTON_TEXT};
    border:none;
    border-radius:50px;
    font-family:'Playfair Display', serif;
    font-size:1rem;
    font-weight:700;
    cursor:pointer;
    letter-spacing:0.04em;
    transition:opacity 0.15s;
    margin-bottom:12px;
  }}
  button:hover {{ opacity:0.88; }}
  .err {{
    font-family:'IM Fell English', serif;
    font-style:italic;
    font-size:0.82rem;
    color:#c0392b;
    min-height:20px;
    margin-top:4px;
  }}
</style>
</head>
<body>
<div class="card">
  <div class="hearts">🎀 🎀</div>
  <div class="title">{GATE_TITLE}</div>
  <div class="sub">{GATE_SUBTITLE}</div>
  <div class="label">Our Anniversary Date</div>
  <input id="d" type="text" placeholder="{GATE_PLACEHOLDER}"
    autocomplete="off" onkeydown="if(event.key==='Enter')check()" />
  <button onclick="check()">{GATE_BUTTON_TEXT_LABEL}</button>
  <div class="err" id="err"></div>
</div>
<script>
  var norm = function(v){{ return v.toLowerCase().replace(/[\\s\\-\\/]/g,'').trim(); }};
  var accepted = {str([a.lower().replace(" ","").replace("-","").replace("/","") for a in ACCEPTED])};
  function check(){{
    var v = norm(document.getElementById('d').value);
    if(accepted.indexOf(v) !== -1){{
      window.location.href = window.location.href.split('?')[0] + '?unlocked=1';
    }} else {{
      document.getElementById('err').textContent = v==='' ? 'Please enter a date 💜' : '{GATE_ERROR_TEXT}';
      document.getElementById('d').style.borderColor='#c0392b';
      setTimeout(function(){{ document.getElementById('d').style.borderColor='{GATE_INK}'; }},1200);
    }}
  }}
</script>
</body>
</html>"""

    # Check if they just submitted via URL param
    params = st.query_params
    if params.get("unlocked") == "1":
        st.session_state.unlocked = True
        st.query_params.clear()
        st.rerun()
    else:
        components.html(gate_html, height=600, scrolling=False)
        st.stop()

# ── shown only after unlock ───────────────────────────────────────────────────
# components.html(html, height=3600, scrolling=False)

components.html(html, height=3600, scrolling=False)
