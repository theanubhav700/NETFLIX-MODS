"""
NETMUSIC — Netflix-style app icon
Black background, bold red "NM" text, clean & simple
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, numpy as np

BASE    = os.path.dirname(os.path.abspath(__file__))
ANDROID = os.path.join(BASE, "android", "app", "src", "main", "res")
PUBLIC  = os.path.join(BASE, "frontend", "public")

FONT_CANDIDATES = [
    "C:/Windows/Fonts/arialbd.ttf",
    "C:/Windows/Fonts/bahnschrift.ttf",
    "C:/Windows/Fonts/impact.ttf",
    "C:/Windows/Fonts/calibrib.ttf",
]

def get_font(size):
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: continue
    return ImageFont.load_default()

def make_icon(size):
    img  = Image.new('RGB', (size, size), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    # subtle dark-red centre glow
    arr  = np.array(img, dtype=np.float32)
    Y, X = np.mgrid[0:size, 0:size]
    dist = np.sqrt((X-size/2)**2 + (Y-size/2)**2) / (size*0.55)
    gv   = np.clip(1-dist, 0, 1) * 18
    arr[:,:,0] += gv * 1.8   # slight red tint
    arr[:,:,1] += gv * 0.2
    arr[:,:,2] += gv * 0.2
    img  = Image.fromarray(np.clip(arr,0,255).astype(np.uint8),'RGB')
    draw = ImageDraw.Draw(img)

    text = "NM"
    fs   = int(size * 0.56)
    font = get_font(fs)

    bbox = draw.textbbox((0,0), text, font=font)
    tw = bbox[2]-bbox[0]
    th = bbox[3]-bbox[1]
    tx = (size - tw)//2 - bbox[0]
    ty = (size - th)//2 - bbox[1] - int(size*0.03)

    # glow
    glow = Image.new('RGBA', (size,size), (0,0,0,0))
    gd   = ImageDraw.Draw(glow)
    gd.text((tx, ty), text, font=font, fill=(229,9,20,80))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=max(2,size//16)))
    img  = Image.alpha_composite(img.convert('RGBA'), glow).convert('RGB')
    draw = ImageDraw.Draw(img)

    # shadow
    draw.text((tx+max(1,size//80), ty+max(1,size//60)), text, font=font, fill=(80,0,0))
    # main red text
    draw.text((tx, ty), text, font=font, fill=(229, 9, 20))

    return img

MIPMAP = {
    "mipmap-mdpi":    48,
    "mipmap-hdpi":    72,
    "mipmap-xhdpi":   96,
    "mipmap-xxhdpi":  144,
    "mipmap-xxxhdpi": 192,
}

print("Generating Netflix-style NM icons...")
for folder, px in MIPMAP.items():
    out = os.path.join(ANDROID, folder)
    os.makedirs(out, exist_ok=True)
    ic = make_icon(px)
    ic.save(os.path.join(out, "ic_launcher.png"))
    ic.save(os.path.join(out, "ic_launcher_round.png"))
    ic.convert('RGBA').save(os.path.join(out, "ic_launcher_foreground.png"))
    print(f"  ✓ {folder} ({px}px)")

# favicon
os.makedirs(PUBLIC, exist_ok=True)
fav = make_icon(512)
fav.save(os.path.join(PUBLIC, "favicon.png"))
fav.resize((32,32), Image.LANCZOS).save(os.path.join(PUBLIC, "favicon-32.png"))
print("  ✓ favicon.png (512px)")
print("\n✅ Done!")
