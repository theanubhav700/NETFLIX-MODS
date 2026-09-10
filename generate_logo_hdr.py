"""
NETMUSIC — 4K HDR Smooth Logo Generator
3D glossy play-button with N+note, white glow, reflection, "NETMUSIC" text
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math, os

BASE    = os.path.dirname(os.path.abspath(__file__))
PUBLIC  = os.path.join(BASE, "frontend", "public")
ASSETS  = os.path.join(BASE, "frontend", "src", "assets")
ANDROID = os.path.join(BASE, "frontend", "android", "app", "src", "main", "res")
os.makedirs(PUBLIC, exist_ok=True)
os.makedirs(ASSETS, exist_ok=True)

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────
def lerp(a, b, t):
    return a + (b - a) * t

def clamp(v, lo=0, hi=255):
    return max(lo, min(hi, v))

def pt_on_circle(cx, cy, r, deg):
    a = math.radians(deg)
    return (cx + r * math.cos(a), cy + r * math.sin(a))

def rounded_triangle_poly(cx, cy, r, corner_r, steps=60):
    """Right-pointing rounded triangle centred at (cx,cy)."""
    # three vertices
    verts = [
        pt_on_circle(cx, cy, r,   0),    # tip  (right)
        pt_on_circle(cx, cy, r, 135),    # top-left
        pt_on_circle(cx, cy, r, 225),    # bot-left
    ]
    poly = []
    n = len(verts)
    for i in range(n):
        A = verts[(i-1) % n]
        B = verts[i]
        C = verts[(i+1) % n]
        dAB = math.hypot(B[0]-A[0], B[1]-A[1])
        dBC = math.hypot(C[0]-B[0], C[1]-B[1])
        t1  = min(corner_r / dAB, 0.45)
        t2  = min(corner_r / dBC, 0.45)
        P1  = (A[0]+(B[0]-A[0])*(1-t1), A[1]+(B[1]-A[1])*(1-t1))
        P2  = (B[0]+(C[0]-B[0])*t2,     B[1]+(C[1]-B[1])*t2)
        for s in range(steps+1):
            tt = s / steps
            bx = (1-tt)**2*P1[0] + 2*(1-tt)*tt*B[0] + tt**2*P2[0]
            by = (1-tt)**2*P1[1] + 2*(1-tt)*tt*B[1] + tt**2*P2[1]
            poly.append((bx, by))
    return poly

def radial_gradient(size, cx, cy, r_inner, r_outer, c_inner, c_outer):
    """Numpy radial gradient, returns RGBA Image."""
    W, H = size
    Y, X = np.mgrid[0:H, 0:W]
    dist  = np.sqrt((X - cx)**2 + (Y - cy)**2)
    t     = np.clip((dist - r_inner) / (r_outer - r_inner), 0, 1)
    arr   = np.zeros((H, W, 4), dtype=np.uint8)
    for ch in range(4):
        arr[:,:,ch] = np.clip(c_inner[ch]*(1-t) + c_outer[ch]*t, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, 'RGBA')

def linear_gradient_img(size, start_col, end_col, vertical=True):
    W, H = size
    arr  = np.zeros((H, W, 4), dtype=np.float32)
    if vertical:
        t = np.linspace(0, 1, H)[:,None]
    else:
        t = np.linspace(0, 1, W)[None,:]
    for ch in range(4):
        arr[:,:,ch] = start_col[ch]*(1-t) + end_col[ch]*t
    return Image.fromarray(np.clip(arr,0,255).astype(np.uint8), 'RGBA')

# ─────────────────────────────────────────────────────────────
# MAIN LOGO RENDERER
# ─────────────────────────────────────────────────────────────
def render_logo(W=2048, H=1024, for_icon=False):
    """
    W,H   : canvas size
    for_icon : square crop, no text, transparent bg
    """
    if for_icon:
        W = H = max(W, H)

    img = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    # ── Background: pure black with very subtle centre glow ──
    if not for_icon:
        # radial dark-grey glow at centre-left
        glow = radial_gradient(
            (W, H),
            cx=W*0.38, cy=H*0.44,
            r_inner=0, r_outer=H*0.95,
            c_inner=(28, 28, 28, 255),
            c_outer=(0,  0,  0,  255)
        )
        img = Image.alpha_composite(img, glow)
        draw = ImageDraw.Draw(img)

    # ── Play-button geometry ──────────────────────────────────
    cx  = W * 0.36 if not for_icon else W * 0.50
    cy  = H * 0.42 if not for_icon else H * 0.45
    R   = H * 0.33
    CR  = R * 0.30         # corner radius

    poly = rounded_triangle_poly(cx, cy, R, CR, steps=80)

    # ── Layer 1: deep shadow behind shape ────────────────────
    shadow_layer = Image.new('RGBA', (W, H), (0,0,0,0))
    sd = ImageDraw.Draw(shadow_layer)
    sd.polygon(poly, fill=(0,0,0,200))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=int(R*0.18)))
    # offset shadow down-right
    sx, sy = int(R*0.06), int(R*0.10)
    img = Image.alpha_composite(img, Image.fromarray(
        np.roll(np.roll(np.array(shadow_layer), sy, axis=0), sx, axis=1)
    ))
    draw = ImageDraw.Draw(img)

    # ── Layer 2: base shape – dark fill ──────────────────────
    base = Image.new('RGBA', (W, H), (0,0,0,0))
    bd   = ImageDraw.Draw(base)
    bd.polygon(poly, fill=(12, 12, 12, 255))
    img  = Image.alpha_composite(img, base)

    # ── Layer 3: 3D white/silver glossy overlay ───────────────
    # We paint a gradient mask over the shape
    grad_layer = linear_gradient_img(
        (W, H),
        start_col=(255, 255, 255, 210),   # bright top
        end_col  =(120, 120, 130,  60),   # dim bottom
        vertical=True
    )
    shape_mask = Image.new('L', (W, H), 0)
    md = ImageDraw.Draw(shape_mask)
    md.polygon(poly, fill=255)
    grad_layer.putalpha(shape_mask)
    img = Image.alpha_composite(img, grad_layer)
    draw = ImageDraw.Draw(img)

    # ── Layer 4: inner bevel / edge shine ─────────────────────
    # Slightly inset lighter polygon on top half
    inset_f  = 0.96
    poly_in  = [(cx+(x-cx)*inset_f, cy+(y-cy)*inset_f) for x,y in poly]
    top_half = [(x, y) for x, y in poly_in if y < cy]
    if len(top_half) >= 3:
        shine = Image.new('RGBA', (W, H), (0,0,0,0))
        sd2   = ImageDraw.Draw(shine)
        sd2.polygon(poly_in, fill=(255, 255, 255, 80))
        shine = shine.filter(ImageFilter.GaussianBlur(radius=int(R*0.04)))
        img   = Image.alpha_composite(img, shine)

    # ── Layer 5: outer white glow / bloom ─────────────────────
    glow_shape = Image.new('RGBA', (W, H), (0,0,0,0))
    gd         = ImageDraw.Draw(glow_shape)
    gd.polygon(poly, fill=(255, 255, 255, 60))
    for blur_r in [int(R*0.08), int(R*0.18), int(R*0.35)]:
        blurred = glow_shape.filter(ImageFilter.GaussianBlur(radius=blur_r))
        img = Image.alpha_composite(img, blurred)

    draw = ImageDraw.Draw(img)

    # ── Layer 6: sharp white border ───────────────────────────
    border = Image.new('RGBA', (W, H), (0,0,0,0))
    brd    = ImageDraw.Draw(border)
    bw     = max(3, int(R * 0.025))
    brd.line(poly + [poly[0]], fill=(255, 255, 255, 230), width=bw)
    img = Image.alpha_composite(img, border)
    draw = ImageDraw.Draw(img)

    # ─── "N" letter inside the shape ──────────────────────────
    # Position: left 55% of the triangle interior
    # We draw directly with thick strokes for clean look
    n_left  = cx - R * 0.50
    n_top   = cy - R * 0.52
    n_bot   = cy + R * 0.45
    n_right = cx - R * 0.05
    bw2     = max(4, int(R * 0.095))   # bar width

    def draw_rect_shadow(x1,y1,x2,y2,col,blur=6):
        lyr = Image.new('RGBA',(W,H),(0,0,0,0))
        ld  = ImageDraw.Draw(lyr)
        ld.rectangle([x1,y1,x2,y2], fill=col)
        if blur:
            lyr = lyr.filter(ImageFilter.GaussianBlur(radius=blur))
        return lyr

    # Shadow pass for N
    for dx,dy in [(4,6)]:
        s = draw_rect_shadow(n_left+dx, n_top+dy, n_left+bw2+dx, n_bot+dy,
                              (0,0,0,180), blur=8)
        img = Image.alpha_composite(img, s)

    draw = ImageDraw.Draw(img)

    # Left bar of N – white
    draw.rectangle([n_left, n_top, n_left+bw2, n_bot], fill=(255,255,255,255))
    # Right bar of N – white
    draw.rectangle([n_right-bw2, n_top, n_right, n_bot], fill=(255,255,255,255))
    # Diagonal – white (thick polyline)
    draw.line([(n_left, n_top), (n_right, n_bot)], fill=(255,255,255,255),
              width=int(bw2*1.15))

    # ─── Music note (J shape) ─────────────────────────────────
    note_lx  = cx + R * 0.08    # left edge of stem
    note_top = cy - R * 0.50
    note_bot = cy + R * 0.28
    sw       = max(4, int(R * 0.09))   # stem width

    # Stem shadow
    s = draw_rect_shadow(note_lx+4, note_top+6, note_lx+sw+4, note_bot+6,
                          (0,0,0,160), blur=7)
    img = Image.alpha_composite(img, s)
    draw = ImageDraw.Draw(img)

    # Stem
    draw.rectangle([note_lx, note_top, note_lx+sw, note_bot],
                   fill=(255,255,255,255))

    # J-curve at bottom (arc going left-down)
    arc_r  = sw * 2.4
    arc_cx = note_lx - arc_r + sw * 0.5
    arc_cy = note_bot
    ab     = [arc_cx-arc_r, arc_cy-arc_r*0.9, arc_cx+arc_r, arc_cy+arc_r*0.9]
    draw.arc(ab, start=80, end=290, fill=(255,255,255,255), width=sw)

    # Note head (filled ellipse)
    nh_r = int(R * 0.095)
    nh_cx = int(note_lx - nh_r * 0.55)
    nh_cy = int(note_bot + nh_r * 0.70)
    # Shadow
    draw.ellipse([nh_cx-nh_r+4, nh_cy-nh_r*0.8+6,
                  nh_cx+nh_r+4, nh_cy+nh_r*0.8+6],
                 fill=(0,0,0,150))
    # Filled white note head
    draw.ellipse([nh_cx-nh_r, nh_cy-int(nh_r*0.8),
                  nh_cx+nh_r, nh_cy+int(nh_r*0.8)],
                 fill=(255,255,255,255))
    # Specular highlight on note head
    draw.ellipse([nh_cx-nh_r//3, nh_cy-int(nh_r*0.55),
                  nh_cx+nh_r//4, nh_cy-int(nh_r*0.05)],
                 fill=(255,255,255,180))

    # ── Specular highlight on whole shape (top-left shine) ────
    shine2 = Image.new('RGBA', (W,H), (0,0,0,0))
    sd3    = ImageDraw.Draw(shine2)
    # ellipse in top-left quadrant of the triangle
    ex = cx - R*0.30
    ey = cy - R*0.28
    ew = R*0.55
    eh = R*0.28
    sd3.ellipse([ex-ew, ey-eh, ex+ew, ey+eh], fill=(255,255,255,90))
    shine2 = shine2.filter(ImageFilter.GaussianBlur(radius=int(R*0.08)))
    # mask to shape
    shine_arr = np.array(shine2).copy()
    mask_arr  = np.array(shape_mask) / 255.0
    shine_arr[:,:,3] = np.clip(shine_arr[:,:,3].astype(np.float32) * mask_arr, 0, 255).astype(np.uint8)
    shine2 = Image.fromarray(shine_arr, 'RGBA')
    img = Image.alpha_composite(img, shine2)
    draw = ImageDraw.Draw(img)

    # ── "NETMUSIC" text ───────────────────────────────────────
    if not for_icon:
        font_size = int(H * 0.175)
        try:
            # Try bold system fonts
            for fpath in [
                "C:/Windows/Fonts/arialbd.ttf",
                "C:/Windows/Fonts/calibrib.ttf",
                "C:/Windows/Fonts/verdanab.ttf",
                "C:/Windows/Fonts/impact.ttf",
            ]:
                if os.path.exists(fpath):
                    font = ImageFont.truetype(fpath, font_size)
                    break
            else:
                font = ImageFont.load_default()
        except Exception:
            font = ImageFont.load_default()

        text  = "NETMUSIC"
        bbox  = draw.textbbox((0,0), text, font=font)
        tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
        tx = (W - tw) // 2
        ty = int(H * 0.70)

        # Text shadow / glow
        txt_glow = Image.new('RGBA', (W,H), (0,0,0,0))
        tg       = ImageDraw.Draw(txt_glow)
        tg.text((tx, ty), text, font=font, fill=(255,255,255,90))
        txt_glow = txt_glow.filter(ImageFilter.GaussianBlur(radius=18))
        img = Image.alpha_composite(img, txt_glow)
        draw = ImageDraw.Draw(img)

        # White text with subtle gradient illusion (draw twice: lighter top)
        # Bottom shadow
        draw.text((tx+4, ty+6), text, font=font, fill=(0,0,0,180))
        # Main white text
        draw.text((tx,   ty),   text, font=font, fill=(255,255,255,255))

        # Reflection (flipped, faded)
        txt_layer = Image.new('RGBA', (W,H), (0,0,0,0))
        tr        = ImageDraw.Draw(txt_layer)
        tr.text((tx, ty), text, font=font, fill=(255,255,255,255))
        reflected = txt_layer.transpose(Image.FLIP_TOP_BOTTOM)
        # Shift down so reflection starts just below text
        ref_arr = np.array(reflected, dtype=np.float32)
        shift   = int(ty + th + 12)
        # fade gradient mask
        fade = np.linspace(0.35, 0, th*2 if th*2 > 0 else 1)
        fade = np.clip(fade, 0, 1)
        for row in range(min(len(fade), H-shift)):
            ref_arr[H-shift-row-1, :, 3] *= fade[row] * 0.5
        reflected = Image.fromarray(np.clip(ref_arr,0,255).astype(np.uint8),'RGBA')
        img = Image.alpha_composite(img, reflected)

    return img.convert('RGBA')


# ─────────────────────────────────────────────────────────────
# GENERATE ALL FILES
# ─────────────────────────────────────────────────────────────

print("🎨 Rendering 4K HDR logo (2048×1024)...")
logo_4k = render_logo(W=2048, H=1024, for_icon=False)
logo_4k.convert('RGB').save(os.path.join(ASSETS, "netmusic-logo.png"), quality=100)
print("  ✓ src/assets/netmusic-logo.png  (2048×1024)")

print("🌐 Web banner (1280×640)...")
logo_web = render_logo(W=1280, H=640, for_icon=False)
logo_web.convert('RGBA').save(os.path.join(PUBLIC, "netmusic-banner.png"))
print("  ✓ public/netmusic-banner.png")

print("🔖 Favicon (512×512 square icon version)...")
icon_512 = render_logo(W=512, H=512, for_icon=True)
icon_512.convert('RGBA').save(os.path.join(PUBLIC, "favicon.png"))
icon_512.resize((32,32), Image.LANCZOS).convert('RGBA').save(
    os.path.join(PUBLIC, "favicon-32.png"))
print("  ✓ public/favicon.png (512px)")
print("  ✓ public/favicon-32.png (32px)")

print("📱 Android mipmap icons...")
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
    icon = render_logo(W=px, H=px, for_icon=True)
    # Black background for launcher icon
    bg = Image.new('RGB', (px, px), (0, 0, 0))
    bg.paste(icon, (0,0), icon)
    bg.save(os.path.join(out_dir, "ic_launcher.png"))
    bg.save(os.path.join(out_dir, "ic_launcher_round.png"))
    icon.save(os.path.join(out_dir, "ic_launcher_foreground.png"))
    print(f"  ✓ {folder} ({px}px)")

print("\n✅ All NETMUSIC logo files generated — 4K HDR quality!")
print(f"   Main logo → frontend/src/assets/netmusic-logo.png")
print(f"   Favicon   → frontend/public/favicon.png")
