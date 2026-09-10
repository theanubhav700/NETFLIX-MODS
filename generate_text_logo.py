"""
NETMUSIC — Premium Text Logo Generator
Style: Bold modern typography, gradient fill, subtle glow
No icons — just the word "NETMUSIC" looking ultra clean
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os, math

BASE    = os.path.dirname(os.path.abspath(__file__))
PUBLIC  = os.path.join(BASE, "frontend", "public")
ASSETS  = os.path.join(BASE, "frontend", "src", "assets")
ANDROID = os.path.join(BASE, "android", "app", "src", "main", "res")
os.makedirs(PUBLIC, exist_ok=True)
os.makedirs(ASSETS, exist_ok=True)

# ─────────────────────────────────────────────────────────────
# FONT PICKER — best available bold font on Windows
# ─────────────────────────────────────────────────────────────
FONT_CANDIDATES = [
    "C:/Windows/Fonts/bahnschrift.ttf",   # modern geometric — best
    "C:/Windows/Fonts/arialbd.ttf",       # Arial Bold
    "C:/Windows/Fonts/impact.ttf",        # Impact
    "C:/Windows/Fonts/calibrib.ttf",      # Calibri Bold
    "C:/Windows/Fonts/verdanab.ttf",      # Verdana Bold
    "C:/Windows/Fonts/tahoma.ttf",        # Tahoma
]

def get_font(size):
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size), p
            except Exception:
                continue
    return ImageFont.load_default(), "default"

# ─────────────────────────────────────────────────────────────
# GRADIENT HELPER — horizontal left→right on a text mask
# ─────────────────────────────────────────────────────────────
def apply_gradient_to_text(img_rgba, text_mask, color_left, color_right):
    """Paint a left→right gradient only where text_mask is white."""
    W, H   = img_rgba.size
    arr    = np.array(img_rgba, dtype=np.float32)
    mask   = np.array(text_mask, dtype=np.float32) / 255.0   # (H,W)

    xs     = np.linspace(0, 1, W)[np.newaxis, :]             # (1,W)

    for ch, (cl, cr) in enumerate(zip(color_left[:3], color_right[:3])):
        grad = cl * (1 - xs) + cr * xs                       # (1,W) broadcast→(H,W)
        arr[:,:,ch] = arr[:,:,ch] * (1 - mask) + grad * mask

    # alpha: keep existing + paint text fully opaque
    arr[:,:,3] = np.clip(arr[:,:,3] * (1-mask) + 255 * mask, 0, 255)
    return Image.fromarray(arr.astype(np.uint8), 'RGBA')


# ─────────────────────────────────────────────────────────────
# RENDER WEBSITE BANNER  (wide, dark bg, glowing text)
# ─────────────────────────────────────────────────────────────
def render_website_logo(W=1600, H=400):
    img  = Image.new('RGBA', (W, H), (0, 0, 0, 255))

    # Subtle dark-radial background glow
    arr  = np.array(img, dtype=np.float32)
    Y, X = np.mgrid[0:H, 0:W]
    dist = np.sqrt(((X - W//2)/(W*0.5))**2 + ((Y - H//2)/(H*0.5))**2)
    gv   = np.clip(1 - dist, 0, 1) * 22          # 0-22 brightness boost
    arr[:,:,0] += gv; arr[:,:,1] += gv; arr[:,:,2] += gv
    img  = Image.fromarray(np.clip(arr,0,255).astype(np.uint8), 'RGBA')

    font_size = int(H * 0.62)
    font, fpath = get_font(font_size)
    print(f"  font: {os.path.basename(fpath)}  size={font_size}")

    text = "NETMUSIC"
    draw = ImageDraw.Draw(img)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw   = bbox[2] - bbox[0]
    th   = bbox[3] - bbox[1]
    tx   = (W - tw) // 2 - bbox[0]
    ty   = (H - th) // 2 - bbox[1] - int(H * 0.03)

    # ── Layer 1: deep shadow ──────────────────────────────────
    shadow = Image.new('RGBA', (W, H), (0,0,0,0))
    sd     = ImageDraw.Draw(shadow)
    sd.text((tx+6, ty+8), text, font=font, fill=(0,0,0,200))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=16))
    img    = Image.alpha_composite(img, shadow)

    # ── Layer 2: outer glow (white bloom) ─────────────────────
    for blur_r, alpha in [(30, 40), (16, 60), (8, 80)]:
        glow_lyr = Image.new('RGBA', (W, H), (0,0,0,0))
        gd       = ImageDraw.Draw(glow_lyr)
        gd.text((tx, ty), text, font=font, fill=(255,255,255,alpha))
        glow_lyr = glow_lyr.filter(ImageFilter.GaussianBlur(radius=blur_r))
        img      = Image.alpha_composite(img, glow_lyr)

    # ── Layer 3: gradient text  ────────────────────────────────
    # White → light-grey gradient, top brighter
    text_mask = Image.new('L', (W, H), 0)
    md        = ImageDraw.Draw(text_mask)
    md.text((tx, ty), text, font=font, fill=255)

    # vertical gradient array
    grad_arr  = np.zeros((H, W, 4), dtype=np.float32)
    t_vert    = np.linspace(0, 1, H)[:, np.newaxis]
    # top: pure white (255), bottom: cool silver-grey (180)
    top_c, bot_c = 255, 175
    lum = top_c * (1-t_vert) + bot_c * t_vert
    for ch in range(3):
        grad_arr[:,:,ch] = lum
    grad_arr[:,:,3]  = 255
    grad_img = Image.fromarray(grad_arr.astype(np.uint8), 'RGBA')
    grad_img.putalpha(text_mask)
    img = Image.alpha_composite(img, grad_img)

    # ── Layer 4: thin specular highlight (top edge of letters) ─
    highlight = Image.new('RGBA', (W, H), (0,0,0,0))
    hd        = ImageDraw.Draw(highlight)
    hd.text((tx, ty-2), text, font=font, fill=(255,255,255,90))
    highlight = highlight.filter(ImageFilter.GaussianBlur(radius=2))
    img       = Image.alpha_composite(img, highlight)

    # ── Layer 5: bottom reflection ────────────────────────────
    text_layer = Image.new('RGBA', (W, H), (0,0,0,0))
    tld        = ImageDraw.Draw(text_layer)
    tld.text((tx, ty), text, font=font, fill=(255,255,255,255))
    reflected  = text_layer.transpose(Image.FLIP_TOP_BOTTOM)
    ref_arr    = np.array(reflected, dtype=np.float32)
    # fade out downward
    ref_top    = H - ty - th - int(H*0.02)
    fade_h     = int(th * 0.55)
    for row in range(H):
        dist_from_top = row - ref_top
        if dist_from_top < 0:
            ref_arr[row,:,3] = 0
        elif dist_from_top < fade_h:
            ref_arr[row,:,3] *= (1 - dist_from_top/fade_h) * 0.35
        else:
            ref_arr[row,:,3]  = 0
    img = Image.alpha_composite(img,
          Image.fromarray(np.clip(ref_arr,0,255).astype(np.uint8),'RGBA'))

    return img.convert('RGBA')


# ─────────────────────────────────────────────────────────────
# RENDER SQUARE APP ICON  (dark bg, large letter, very clean)
# ─────────────────────────────────────────────────────────────
def render_app_icon(size=512):
    pad  = int(size * 0.08)
    img  = Image.new('RGBA', (size, size), (0, 0, 0, 255))

    # subtle radial glow centre
    arr  = np.array(img, dtype=np.float32)
    Y, X = np.mgrid[0:size, 0:size]
    dist = np.sqrt((X-size//2)**2 + (Y-size//2)**2) / (size*0.6)
    gv   = np.clip(1-dist,0,1) * 30
    arr[:,:,0]+=gv; arr[:,:,1]+=gv; arr[:,:,2]+=gv
    img  = Image.fromarray(np.clip(arr,0,255).astype(np.uint8),'RGBA')

    # Two-line layout: "NET" top, "MUSIC" bottom
    draw = ImageDraw.Draw(img)

    line1, line2 = "NET", "MUSIC"
    avail_w = size - pad * 2

    # Find font size that fits "MUSIC" (wider word) in avail_w
    fs = int(size * 0.38)
    while fs > 10:
        f, _ = get_font(fs)
        b    = draw.textbbox((0,0), line2, font=f)
        if b[2]-b[0] <= avail_w:
            break
        fs -= 2
    font, fpath = get_font(fs)

    b1  = draw.textbbox((0,0), line1, font=font)
    b2  = draw.textbbox((0,0), line2, font=font)
    w1  = b1[2]-b1[0]; h1 = b1[3]-b1[1]
    w2  = b2[2]-b2[0]; h2 = b2[3]-b2[1]
    gap = int(fs * 0.12)
    total_h = h1 + gap + h2

    x1  = (size - w1)//2 - b1[0]
    x2  = (size - w2)//2 - b2[0]
    y1  = (size - total_h)//2 - b1[1] - int(size*0.02)
    y2  = y1 + h1 + gap

    def draw_text_with_glow(draw_img, x, y, text, font, blur_r=6, glow_alpha=55):
        for br, ga in [(blur_r*3, glow_alpha//3), (blur_r, glow_alpha)]:
            gl = Image.new('RGBA', (size,size), (0,0,0,0))
            gd = ImageDraw.Draw(gl)
            gd.text((x, y), text, font=font, fill=(255,255,255,ga))
            gl = gl.filter(ImageFilter.GaussianBlur(radius=br))
            draw_img = Image.alpha_composite(draw_img, gl)
        return draw_img

    img = draw_text_with_glow(img, x1, y1, line1, font, blur_r=int(size*0.012))
    img = draw_text_with_glow(img, x2, y2, line2, font, blur_r=int(size*0.012))
    draw = ImageDraw.Draw(img)

    # Shadow
    draw.text((x1+int(size*0.008), y1+int(size*0.01)), line1, font=font, fill=(0,0,0,160))
    draw.text((x2+int(size*0.008), y2+int(size*0.01)), line2, font=font, fill=(0,0,0,160))

    # Vertical gradient text mask
    for (x, y, txt) in [(x1,y1,line1),(x2,y2,line2)]:
        mask = Image.new('L', (size, size), 0)
        md   = ImageDraw.Draw(mask)
        md.text((x, y), txt, font=font, fill=255)
        mask_arr = np.array(mask)
        grad_arr = np.zeros((size,size,4), dtype=np.float32)
        t_v      = np.linspace(0,1,size)[:,np.newaxis]
        lum      = 255*(1-t_v) + 185*t_v
        for ch in range(3): grad_arr[:,:,ch] = lum
        grad_arr[:,:,3] = 255
        gi = Image.fromarray(grad_arr.astype(np.uint8),'RGBA')
        gi.putalpha(mask)
        img = Image.alpha_composite(img, gi)

    # thin divider line between NET and MUSIC
    lx1 = (size - int(size*0.55))//2
    lx2 = size - lx1
    ly  = y2 - gap//2 - 1
    draw = ImageDraw.Draw(img)
    draw.line([(lx1, ly),(lx2, ly)], fill=(255,255,255,40), width=max(1,int(size*0.004)))

    return img.convert('RGBA')


# ─────────────────────────────────────────────────────────────
# GENERATE ALL FILES
# ─────────────────────────────────────────────────────────────

print("=" * 50)
print("  NETMUSIC Text Logo Generator")
print("=" * 50)

print("\n📐 Website logo (1600×400)...")
web = render_website_logo(1600, 400)
web.convert('RGBA').save(os.path.join(ASSETS, "netmusic-logo.png"))
print("  ✓ src/assets/netmusic-logo.png")

# Navbar version — tighter (560×140)
print("\n📐 Navbar logo (560×140)...")
nav = render_website_logo(560, 140)
nav.convert('RGBA').save(os.path.join(ASSETS, "netmusic-nav.png"))
print("  ✓ src/assets/netmusic-nav.png")

print("\n🔖 Favicon (512px square)...")
icon = render_app_icon(512)
icon.convert('RGBA').save(os.path.join(PUBLIC, "favicon.png"))
icon.resize((32,32), Image.LANCZOS).save(os.path.join(PUBLIC, "favicon-32.png"))
print("  ✓ public/favicon.png")
print("  ✓ public/favicon-32.png")

print("\n📱 Android mipmap icons...")
MIPMAP = {
    "mipmap-mdpi":    48,
    "mipmap-hdpi":    72,
    "mipmap-xhdpi":   96,
    "mipmap-xxhdpi":  144,
    "mipmap-xxxhdpi": 192,
}
for folder, px in MIPMAP.items():
    out_dir = os.path.join(ANDROID, folder)
    os.makedirs(out_dir, exist_ok=True)
    ic = render_app_icon(px)
    bg = Image.new('RGB', (px, px), (0,0,0))
    bg.paste(ic, (0,0), ic)
    bg.save(os.path.join(out_dir, "ic_launcher.png"))
    bg.save(os.path.join(out_dir, "ic_launcher_round.png"))
    ic.save(os.path.join(out_dir, "ic_launcher_foreground.png"))
    print(f"  ✓ {folder} ({px}px)")

print("\n✅ All done!")
