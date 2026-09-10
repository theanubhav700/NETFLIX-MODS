"""
NETMUSIC Logo Generator
Recreates the logo: rounded-triangle play button (white/grey gradient)
with black "N" + music note inside, "NETMUSIC" text below.
Outputs all required sizes for Android app icons + web favicon.
"""

from PIL import Image, ImageDraw, ImageFont
import math, os, struct, zlib

# ─── Output dirs ──────────────────────────────────────────────
BASE    = os.path.dirname(os.path.abspath(__file__))
ANDROID = os.path.join(BASE, "frontend", "android", "app", "src", "main", "res")
PUBLIC  = os.path.join(BASE, "frontend", "public")
ASSETS  = os.path.join(BASE, "frontend", "src", "assets")

os.makedirs(PUBLIC, exist_ok=True)
os.makedirs(ASSETS, exist_ok=True)

# ─── Draw the logo on a canvas of given size ──────────────────
def draw_logo(size, bg_white=True):
    """
    size : int  – canvas side length (square)
    bg_white : bool – True = white bg (for web), False = transparent (for app icons)
    """
    img  = Image.new("RGBA", (size, size), (255, 255, 255, 255) if bg_white else (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = size / 2, size * 0.42   # centre of play-button shape
    # play button occupies top 65% of canvas
    shape_r = size * 0.38             # radius of bounding circle

    # ── 1. Rounded triangle (play button) ──
    # Vertices of equilateral-ish play triangle pointing right
    # We rotate it slightly so it looks like the logo (tilted right)
    tip_angle  = 0          # pointing right = 0°
    back_angle1 = 140       # top-left corner
    back_angle2 = 220       # bottom-left corner

    def pt(angle_deg, r_scale=1.0):
        a = math.radians(angle_deg)
        return (cx + shape_r * r_scale * math.cos(a),
                cy + shape_r * r_scale * math.sin(a))

    tip   = pt(tip_angle,   1.05)
    top   = pt(back_angle1, 1.0)
    bot   = pt(back_angle2, 1.0)

    # corner radius for the rounded triangle
    cr = size * 0.10

    def lerp(p1, p2, t):
        return (p1[0] + (p2[0] - p1[0]) * t, p1[1] + (p2[1] - p1[1]) * t)

    def dist(p1, p2):
        return math.hypot(p2[0]-p1[0], p2[1]-p1[1])

    # Build rounded-triangle polygon points (approximation via many segments)
    verts = [top, tip, bot]
    poly  = []
    n     = len(verts)
    for i in range(n):
        A = verts[(i - 1) % n]
        B = verts[i]
        C = verts[(i + 1) % n]
        d1, d2 = dist(A, B), dist(B, C)
        t1, t2 = min(cr / d1, 0.45), min(cr / d2, 0.45)
        p1 = lerp(A, B, 1 - t1)
        p2 = lerp(B, C, t2)
        # arc approximation — 12 steps
        for s in range(13):
            tt = s / 12
            # quadratic bezier through B
            bx = (1-tt)**2 * p1[0] + 2*(1-tt)*tt * B[0] + tt**2 * p2[0]
            by = (1-tt)**2 * p1[1] + 2*(1-tt)*tt * B[1] + tt**2 * p2[1]
            poly.append((bx, by))

    # White/light-grey gradient fill — simulate with two draws
    # Draw outer lighter shape
    draw.polygon(poly, fill=(240, 240, 240, 255))
    # Draw inner slightly darker shape (inset)
    inset = size * 0.025
    inner = [(x + (cx - x) * inset / shape_r * 0.6,
              y + (cy - y) * inset / shape_r * 0.6) for x, y in poly]
    draw.polygon(inner, fill=(210, 210, 210, 255))
    # White highlight on the shape
    draw.polygon(poly, fill=(248, 248, 248, 200))

    # Subtle border
    draw.line(poly + [poly[0]], fill=(180, 180, 180, 180), width=max(1, size//150))

    # ── 2. Black "N" + music note inside the triangle ──
    # "N" occupies left ~55% of the shape horizontally
    # music note (filled circle + stem) on the right side

    # N position & size
    n_x   = cx - shape_r * 0.52    # left edge of N
    n_top = cy - shape_r * 0.55
    n_bot = cy + shape_r * 0.52
    n_w   = shape_r * 0.38          # width of each vertical bar
    bar_w = max(2, int(n_w * 0.30)) # bar thickness

    # Left vertical bar
    draw.rectangle([n_x, n_top, n_x + bar_w, n_bot], fill=(20, 20, 20, 255))
    # Right vertical bar
    rx = n_x + n_w - bar_w
    draw.rectangle([rx, n_top, rx + bar_w, n_bot], fill=(20, 20, 20, 255))
    # Diagonal stroke (top-left → bottom-right)
    draw.line([(n_x, n_top), (rx + bar_w, n_bot)], fill=(20, 20, 20, 255),
              width=bar_w)

    # Music note — J-shape (stem + note head)
    note_x  = cx + shape_r * 0.08   # stem left edge
    note_top = cy - shape_r * 0.52
    note_bot = cy + shape_r * 0.28
    stem_w   = max(2, int(size * 0.038))

    # Stem (vertical)
    draw.rectangle([note_x, note_top, note_x + stem_w, note_bot],
                   fill=(20, 20, 20, 255))

    # Curved bottom of J (arc going left)
    arc_r  = stem_w * 2.2
    arc_cx = note_x - arc_r + stem_w
    arc_cy = note_bot
    arc_box = [arc_cx - arc_r, arc_cy - arc_r,
               arc_cx + arc_r, arc_cy + arc_r]
    draw.arc(arc_box, start=90, end=300, fill=(20, 20, 20, 255),
             width=max(2, stem_w))

    # Note head (filled circle at bottom of J)
    nh_r  = int(size * 0.055)
    nh_cx = int(note_x - nh_r * 0.6)
    nh_cy = int(note_bot + nh_r * 0.55)
    draw.ellipse([nh_cx - nh_r, nh_cy - nh_r,
                  nh_cx + nh_r, nh_cy + nh_r],
                 fill=(245, 245, 245, 255))
    # Note head dark outline
    draw.ellipse([nh_cx - nh_r, nh_cy - nh_r,
                  nh_cx + nh_r, nh_cy + nh_r],
                 outline=(20, 20, 20, 200), width=max(1, stem_w // 2))

    return img


def make_app_icon(size, bg_color=(0, 0, 0, 255)):
    """App icon: dark/black background + logo centred"""
    canvas = Image.new("RGBA", (size, size), bg_color)
    logo   = draw_logo(int(size * 0.92), bg_white=False)
    logo   = logo.resize((int(size * 0.88), int(size * 0.88)), Image.LANCZOS)
    offset = (size - logo.width) // 2
    canvas.paste(logo, (offset, offset), logo)
    return canvas.convert("RGB")


# ─── Android mipmap sizes ─────────────────────────────────────
MIPMAP = {
    "mipmap-mdpi":    48,
    "mipmap-hdpi":    72,
    "mipmap-xhdpi":   96,
    "mipmap-xxhdpi":  144,
    "mipmap-xxxhdpi": 192,
}

print("Generating Android icons...")
for folder, px in MIPMAP.items():
    out_dir = os.path.join(ANDROID, folder)
    os.makedirs(out_dir, exist_ok=True)
    icon = make_app_icon(px)
    icon.save(os.path.join(out_dir, "ic_launcher.png"))
    icon.save(os.path.join(out_dir, "ic_launcher_round.png"))
    # foreground (on transparent)
    fg = draw_logo(px, bg_white=False).convert("RGBA")
    fg.save(os.path.join(out_dir, "ic_launcher_foreground.png"))
    print(f"  ✓ {folder} ({px}px)")

# ─── Web favicon (public/favicon.png) ─────────────────────────
print("Generating web favicon...")
favicon = draw_logo(512, bg_white=True).convert("RGBA")
favicon.save(os.path.join(PUBLIC, "favicon.png"))
favicon.resize((32, 32), Image.LANCZOS).save(os.path.join(PUBLIC, "favicon-32.png"))
print("  ✓ public/favicon.png (512px)")
print("  ✓ public/favicon-32.png (32px)")

# ─── Website logo asset ───────────────────────────────────────
print("Generating website logo asset...")
web_logo = draw_logo(400, bg_white=False).convert("RGBA")
web_logo.save(os.path.join(ASSETS, "netmusic-logo.png"))
print("  ✓ src/assets/netmusic-logo.png (400px)")

print("\n✅ All logo files generated successfully!")
