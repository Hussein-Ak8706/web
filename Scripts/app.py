import streamlit as st
import re
import base64
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

OUR_STORY_HEADLINE = "OUR DEAREST"
OUR_STORY_SUBHEAD  = "Journey"
OUR_STORY_BODY     = (
    "From the very first moment we met, something shifted — quietly, almost without notice, "
    "the way morning light changes a room. This year has been filled with shared coffee cups, "
    "long walks, unexpected laughter, and the kind of warmth that stays. "
    "Every adventure we have taken together has written itself into who we are. "
    "The moments big and small, all of it — ours."
)

LOVE_ALL_HEADLINE = "LOVE ALL"
LOVE_ALL_SUBHEAD  = "Around"
LOVE_ALL_BODY     = (
    "Love isn't one grand gesture. It lives in the details: a note left on the counter, "
    "a song played for no reason, a hand found in the dark. "
    "We've collected these moments like pressed flowers — fragile, beautiful, kept."
)

BEST_PART_HEADLINE = "THE BEST PART OF OUR STORY"
BEST_PART_BODY     = (
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

# ── COLORS — change these to restyle the whole site ──────────────────────────
#
#   PAGE_BG      : outer page background
#   PAPER_BG     : newspaper paper color
#   INK          : main text / borders
#   INK_LIGHT    : secondary text (meta, captions)
#   ACCENT       : subtle tint (placeholders, sidebar bg)
#
PAGE_BG   = "#f5f0e8"   # warm off-white backdrop
PAPER_BG  = "#faf6ee"   # slightly warmer newsprint
INK       = "#1a1a1a"   # near-black ink
INK_LIGHT = "#555555"   # lighter ink for meta text
ACCENT    = "#e8e2d8"   # tinted areas

# ── Google Drive video ────────────────────────────────────────────────────────
# 1. Upload your .mp4 to Google Drive
# 2. Right-click → Share → "Anyone with the link can view" → Copy link
# 3. Paste it below
GOOGLE_DRIVE_VIDEO_URL = "https://drive.google.com/file/d/YOUR_FILE_ID_HERE/view?usp=sharing"

# ══════════════════════════════════════════════════════════════════════════════
# INTERNALS — no need to edit below this line
# ══════════════════════════════════════════════════════════════════════════════

st.set_page_config(page_title="The Love Gazette", layout="wide",
                   initial_sidebar_state="collapsed")

BASE_DIR  = Path(__file__).resolve().parent.parent
MEDIA_DIR = BASE_DIR / "Media"
PHOTO_PATHS = (
    sorted(MEDIA_DIR.glob("photo_*.jpg")) +
    sorted(MEDIA_DIR.glob("photo_*.png"))
)

def gdrive_embed_url(url: str):
    m = re.search(r"/d/([a-zA-Z0-9_-]+)", url)
    if not m:
        m = re.search(r"[?&]id=([a-zA-Z0-9_-]+)", url)
    return f"https://drive.google.com/file/d/{m.group(1)}/preview" if m else None

def img_b64(path: Path) -> str:
    ext = path.suffix.lower().lstrip(".")
    mime = "jpeg" if ext in ("jpg", "jpeg") else "png"
    data = base64.b64encode(path.read_bytes()).decode()
    return f"data:image/{mime};base64,{data}"

def photo_html(idx: int, height="180px") -> str:
    if idx < len(PHOTO_PATHS):
        src = img_b64(PHOTO_PATHS[idx])
        return (f'<img src="{src}" style="width:100%;height:{height};'
                f'object-fit:cover;display:block;margin:8px 0;" />')
    # SVG placeholder
    return f"""
    <div style="background:{ACCENT};height:{height};display:flex;align-items:center;
         justify-content:center;margin:8px 0;color:{INK_LIGHT};
         font-family:Georgia,serif;font-style:italic;font-size:0.7rem;">
      Photo {idx+1}
    </div>"""

def video_html() -> str:
    embed = gdrive_embed_url(GOOGLE_DRIVE_VIDEO_URL)
    if embed and "YOUR_FILE_ID_HERE" not in GOOGLE_DRIVE_VIDEO_URL:
        return f"""
        <div style="width:100%;max-width:480px;margin:0 auto;">
          <div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;
               background:#111;border:1px solid {INK};">
            <iframe src="{embed}"
              style="position:absolute;top:0;left:0;width:100%;height:100%;border:none;"
              allowfullscreen allow="autoplay"></iframe>
          </div>
        </div>"""
    return f"""
        <div style="width:100%;max-width:480px;margin:0 auto;background:#1a1a1a;
             padding:48px 16px;text-align:center;color:#888;
             font-family:Georgia,serif;font-style:italic;font-size:0.8rem;
             border:1px solid {INK};">
          Paste your Google Drive link into<br>
          <code style="color:#aaa;font-size:0.75rem;">GOOGLE_DRIVE_VIDEO_URL</code>
          in app.py
        </div>"""

def always_yours_items() -> str:
    rows = "".join(
        f'<div style="padding:3px 0;border-bottom:0.5px solid {ACCENT};">'
        f'&#8226; {item}</div>'
        for item in ALWAYS_YOURS_ITEMS
    )
    return rows

# ── Shared CSS injected once ──────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700&family=IM+Fell+English:ital@0;1&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap');

[data-testid="stAppViewContainer"] {{ background:{PAGE_BG}; }}
[data-testid="stHeader"] {{ display:none; }}
.block-container {{ padding:0 !important; max-width:100% !important; }}
footer {{ display:none; }}
[data-testid="stVerticalBlock"] > div {{ gap:0 !important; }}
</style>
""", unsafe_allow_html=True)

# ── Helpers for consistent component HTML strings ─────────────────────────────
def masthead(small=False) -> str:
    size = "1.55rem" if small else "clamp(2rem,6vw,3.4rem)"
    return f"""
    <div style="border-bottom:2.5px solid {INK};padding:10px 18px 6px;text-align:center;
         background:{PAPER_BG};">
      <div style="font-family:'UnifrakturMaguntia',cursive;font-size:{size};
           letter-spacing:0.04em;line-height:1;color:{INK};">The Love Gazette</div>
      <div style="display:flex;justify-content:space-between;font-size:0.52rem;
           letter-spacing:0.12em;text-transform:uppercase;color:{INK_LIGHT};
           padding:4px 0 2px;border-top:0.75px solid {INK};
           border-bottom:0.75px solid {INK};margin-top:5px;">
        <span>{VOL_LINE}</span><span>{DATE_LINE}</span><span>{CITY_LINE}</span>
      </div>
    </div>"""

def wrapper(inner: str) -> str:
    return f"""
    <div style="max-width:900px;margin:28px auto 0 auto;
         background:{PAPER_BG};border:1.5px solid {INK};
         font-family:'Libre Baskerville',Georgia,serif;color:{INK};">
      {inner}
    </div>"""

def sec_head(text: str) -> str:
    return f"""
    <div style="font-family:'Playfair Display',serif;font-size:clamp(0.85rem,2vw,1.1rem);
         font-weight:900;text-transform:uppercase;letter-spacing:0.08em;
         border-bottom:1px solid {INK};margin-bottom:6px;padding-bottom:3px;">
      {text}
    </div>"""

def sec_subhead(text: str) -> str:
    return f"""
    <div style="font-family:'IM Fell English',serif;font-style:italic;
         font-size:clamp(0.95rem,2vw,1.25rem);margin-bottom:6px;color:{INK};">
      {text}
    </div>"""

def body_p(text: str) -> str:
    return f"""
    <p style="font-size:0.72rem;line-height:1.7;color:{INK_LIGHT};
       text-align:justify;hyphens:auto;margin:6px 0;">{text}</p>"""

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — FRONT COVER
# ══════════════════════════════════════════════════════════════════════════════
p1 = wrapper(f"""
  {masthead()}

  <div style="text-align:center;padding:18px 24px 10px;
       border-bottom:1.5px solid {INK};background:{PAPER_BG};">
    <div style="font-family:'Playfair Display',serif;font-size:clamp(0.8rem,2.5vw,1.2rem);
         font-weight:700;letter-spacing:0.35em;text-transform:uppercase;">{ANNIVERSARY_TEXT}</div>
    <div style="font-family:'Playfair Display',serif;font-size:clamp(2rem,7vw,4.6rem);
         font-weight:900;line-height:1;letter-spacing:-0.01em;">{ANNIVERSARY_TEXT.upper()}</div>
    <div style="font-family:'IM Fell English',serif;font-style:italic;
         font-size:clamp(1rem,3vw,1.5rem);color:{INK_LIGHT};margin-top:2px;">{SUBTITLE}</div>
  </div>

  <div style="padding:18px 24px;border-bottom:2px solid {INK};background:{PAPER_BG};">
    {video_html()}
  </div>

  <div style="text-align:center;font-family:'IM Fell English',serif;font-style:italic;
       font-size:clamp(0.9rem,2vw,1.2rem);letter-spacing:0.06em;
       padding:10px 0 12px;border-top:0.75px solid {INK};background:{PAPER_BG};">
    {PARTNER_NAMES}
  </div>
""")
st.markdown(p1, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — INSIDE SPREAD
# ══════════════════════════════════════════════════════════════════════════════
p2 = wrapper(f"""
  {masthead(small=True)}

  <div style="text-align:center;padding:10px 16px 8px;border-bottom:1px solid {INK};">
    <div style="font-family:'Playfair Display',serif;font-size:clamp(0.7rem,2vw,0.9rem);
         font-weight:700;letter-spacing:0.3em;text-transform:uppercase;">{ANNIVERSARY_TEXT}</div>
    <div style="font-family:'Playfair Display',serif;font-size:clamp(1.6rem,5vw,2.8rem);
         font-weight:900;line-height:1.05;">{ANNIVERSARY_TEXT.upper()}</div>
    <div style="font-family:'IM Fell English',serif;font-style:italic;
         font-size:clamp(0.9rem,2vw,1.1rem);color:{INK_LIGHT};">{SUBTITLE}</div>
  </div>

  <div style="display:grid;grid-template-columns:1fr 2px 1fr;border-bottom:2px solid {INK};">

    <div style="padding:14px;">
      {sec_head(OUR_STORY_HEADLINE)}
      {sec_subhead(OUR_STORY_SUBHEAD)}
      {photo_html(0)}
      {body_p(OUR_STORY_BODY)}
      {photo_html(1)}
    </div>

    <div style="background:{INK};"></div>

    <div style="padding:14px;">
      {sec_head(LOVE_ALL_HEADLINE)}
      {sec_subhead(LOVE_ALL_SUBHEAD)}
      {photo_html(2)}
      {body_p(LOVE_ALL_BODY)}
      <div style="text-align:center;font-family:'IM Fell English',serif;font-style:italic;
           font-size:0.85rem;padding:8px 0 2px;border-top:0.75px solid {INK};margin-top:10px;">
        {PARTNER_NAMES}
      </div>
    </div>

  </div>
""")
st.markdown(p2, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — THE STORY OF US
# ══════════════════════════════════════════════════════════════════════════════
p3 = wrapper(f"""
  {masthead(small=True)}

  <div style="text-align:center;padding:14px 24px 10px;border-bottom:2px solid {INK};">
    <div style="font-family:'Playfair Display',serif;font-size:clamp(1.8rem,5vw,3rem);
         font-weight:900;line-height:1;">THE STORY OF US</div>
  </div>

  <div style="display:grid;grid-template-columns:1fr 2px 1fr;">

    <div style="padding:14px;">
      {sec_head("OUR BEST CHAPTER")}
      {photo_html(3)}
      {body_p(OUR_STORY_BODY)}
      {photo_html(4)}
      {body_p(LOVE_ALL_BODY)}
    </div>

    <div style="background:{INK};"></div>

    <div style="padding:14px;">
      {sec_head(BEST_PART_HEADLINE)}
      {photo_html(5)}
      {body_p(BEST_PART_BODY)}

      <div style="border:1px solid {INK};padding:10px;margin-top:14px;background:{PAPER_BG};">
        <div style="font-family:'Playfair Display',serif;font-weight:900;font-size:0.72rem;
             text-transform:uppercase;letter-spacing:0.1em;text-align:center;
             border-bottom:1px solid {INK};margin-bottom:6px;padding-bottom:4px;">
          ALWAYS YOURS
        </div>
        <div style="font-size:0.65rem;line-height:2;color:{INK_LIGHT};text-align:center;">
          {always_yours_items()}
        </div>
      </div>
    </div>

  </div>
""")
st.markdown(p3, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="max-width:900px;margin:0 auto 48px auto;text-align:center;
     color:{INK_LIGHT};font-size:0.55rem;letter-spacing:0.15em;
     text-transform:uppercase;padding:14px 0;">
  The Love Gazette &nbsp;·&nbsp; Printed with Love
</div>
""", unsafe_allow_html=True)
