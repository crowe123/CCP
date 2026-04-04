from PIL import Image, ImageDraw, ImageFilter, ImageFont
import random, math, os

OUT = "/home/user/CCP/website/images"
os.makedirs(OUT, exist_ok=True)

def make_gradient(w, h, colors, direction="vertical"):
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    if direction == "vertical":
        for y in range(h):
            t = y / h
            r = int(colors[0][0] + (colors[1][0] - colors[0][0]) * t)
            g = int(colors[0][1] + (colors[1][1] - colors[0][1]) * t)
            b = int(colors[0][2] + (colors[1][2] - colors[0][2]) * t)
            draw.line([(0, y), (w, y)], fill=(r, g, b))
    else:
        for x in range(w):
            t = x / w
            r = int(colors[0][0] + (colors[1][0] - colors[0][0]) * t)
            g = int(colors[0][1] + (colors[1][1] - colors[0][1]) * t)
            b = int(colors[0][2] + (colors[1][2] - colors[0][2]) * t)
            draw.line([(x, 0), (x, h)], fill=(r, g, b))
    return img

def add_noise(img, amount=15):
    pixels = img.load()
    w, h = img.size
    for _ in range(w * h // 4):
        x, y = random.randint(0, w-1), random.randint(0, h-1)
        r, g, b = pixels[x, y]
        n = random.randint(-amount, amount)
        pixels[x, y] = (max(0, min(255, r+n)), max(0, min(255, g+n)), max(0, min(255, b+n)))
    return img

def draw_city_silhouette(draw, w, h, base_y, color):
    x = 0
    while x < w:
        bw = random.randint(20, 60)
        bh = random.randint(40, int(h * 0.45))
        top = base_y - bh
        draw.rectangle([x, top, x + bw, base_y + 20], fill=color)
        # windows
        for wy in range(top + 8, base_y - 5, 12):
            for wx in range(x + 5, x + bw - 5, 10):
                if random.random() > 0.5:
                    wc = random.choice([(60, 55, 40), (80, 70, 45), (40, 38, 30)])
                    draw.rectangle([wx, wy, wx+4, wy+5], fill=wc)
        x += bw + random.randint(2, 8)

def draw_person_silhouette(draw, cx, cy, scale=1.0, color=(10, 10, 15)):
    s = scale
    # head
    draw.ellipse([cx-12*s, cy-95*s, cx+12*s, cy-65*s], fill=color)
    # hat brim
    draw.rectangle([cx-18*s, cy-75*s, cx+18*s, cy-70*s], fill=color)
    # hat top
    draw.rectangle([cx-12*s, cy-90*s, cx+12*s, cy-75*s], fill=color)
    # body/coat
    draw.polygon([
        (cx-20*s, cy-65*s), (cx+20*s, cy-65*s),
        (cx+28*s, cy+20*s), (cx-28*s, cy+20*s)
    ], fill=color)
    # coat bottom/legs
    draw.polygon([
        (cx-28*s, cy+20*s), (cx-10*s, cy+20*s),
        (cx-12*s, cy+60*s), (cx-22*s, cy+60*s)
    ], fill=color)
    draw.polygon([
        (cx+10*s, cy+20*s), (cx+28*s, cy+20*s),
        (cx+22*s, cy+60*s), (cx+12*s, cy+60*s)
    ], fill=color)

def draw_magnifying_glass(draw, cx, cy, r=60, color=(180, 170, 150)):
    # glass circle
    for i in range(4):
        draw.ellipse([cx-r-i, cy-r-i, cx+r+i, cy+r+i], outline=color)
    # handle
    hx, hy = cx + int(r * 0.7), cy + int(r * 0.7)
    for i in range(-3, 4):
        draw.line([(cx + int(r*0.6)+i, cy + int(r*0.6)), (hx + 40+i, hy + 40)], fill=color, width=6)

# ========== IMAGE 1: Hero - Dark city surveillance scene ==========
img = make_gradient(1200, 700, [(8, 12, 25), (20, 25, 45)])
draw = ImageDraw.Draw(img)
# Moon/light
for r in range(80, 0, -1):
    alpha = int(20 + (80 - r) * 1.5)
    c = (alpha, alpha, int(alpha * 1.2))
    draw.ellipse([900-r, 80-r, 900+r, 80+r], fill=c)
draw.ellipse([880, 60, 920, 100], fill=(200, 195, 180))
# City skyline
draw_city_silhouette(draw, 1200, 700, 500, (12, 15, 25))
draw_city_silhouette(draw, 1200, 700, 530, (8, 10, 18))
# Street/ground
draw.rectangle([0, 560, 1200, 700], fill=(15, 18, 28))
# Street light glow
for r in range(120, 0, -2):
    a = max(5, int(25 * (120 - r) / 120))
    draw.ellipse([200-r, 480-r, 200+r, 480+r], fill=(a+10, a+8, a))
# Person silhouette
draw_person_silhouette(draw, 350, 520, 1.2)
# Lamp post
draw.rectangle([195, 350, 205, 560], fill=(20, 22, 30))
draw.ellipse([185, 345, 215, 365], fill=(35, 30, 20))
add_noise(img, 8)
img = img.filter(ImageFilter.GaussianBlur(0.8))
img.save(f"{OUT}/hero-surveillance-city.jpg", "JPEG", quality=90)
print("1/7 hero done")

# ========== IMAGE 2: Surveillance binoculars view ==========
img = make_gradient(800, 500, [(5, 8, 15), (15, 20, 35)])
draw = ImageDraw.Draw(img)
# Binocular frame (two circles with dark border)
# Left lens
for r in range(180, 170, -1):
    draw.ellipse([120-r, 250-r, 120+r, 250+r], fill=(3, 5, 10))
# Right lens
for r in range(180, 170, -1):
    draw.ellipse([680-r, 250-r, 680+r, 250+r], fill=(3, 5, 10))
# Inner view - slightly lighter (through the lens)
draw.ellipse([120-165, 250-165, 120+165, 250+165], fill=(12, 18, 30))
draw.ellipse([680-165, 250-165, 680+165, 250+165], fill=(12, 18, 30))
# Small buildings in the distance through lenses
for lens_cx in [120, 680]:
    for bx in range(lens_cx - 140, lens_cx + 140, 25):
        bh = random.randint(20, 60)
        draw.rectangle([bx, 300-bh, bx+18, 300], fill=(18, 24, 40))
        for wy in range(300-bh+5, 295, 8):
            for wx in range(bx+3, bx+15, 6):
                if random.random() > 0.4:
                    draw.rectangle([wx, wy, wx+2, wy+3], fill=(50, 45, 30))
# Bridge between lenses
draw.rectangle([280, 200, 520, 300], fill=(3, 5, 10))
# Outer area (mask)
mask = Image.new("L", (800, 500), 0)
md = ImageDraw.Draw(mask)
md.ellipse([120-170, 250-170, 120+170, 250+170], fill=255)
md.ellipse([680-170, 250-170, 680+170, 250+170], fill=255)
md.rectangle([280, 200, 520, 300], fill=255)
bg = Image.new("RGB", (800, 500), (2, 3, 6))
img = Image.composite(img, bg, mask)
add_noise(img, 6)
img.save(f"{OUT}/surveillance-binoculars.jpg", "JPEG", quality=90)
print("2/7 binoculars done")

# ========== IMAGE 3: Documents/case file ==========
img = make_gradient(800, 500, [(25, 22, 18), (40, 35, 28)])
draw = ImageDraw.Draw(img)
# Desk surface texture
for i in range(500):
    x, y = random.randint(0, 799), random.randint(0, 499)
    c = random.randint(25, 45)
    draw.rectangle([x, y, x+random.randint(1,3), y+1], fill=(c, c-3, c-6))
# Folder
draw.rectangle([100, 80, 500, 400], fill=(160, 140, 100))
draw.rectangle([95, 75, 300, 90], fill=(170, 150, 110)) # tab
draw.line([(100, 80), (500, 80)], fill=(140, 120, 80), width=2)
# Papers sticking out
draw.rectangle([120, 100, 480, 380], fill=(220, 215, 205))
draw.rectangle([130, 110, 470, 370], fill=(230, 225, 215))
# Text lines on paper
for ly in range(130, 350, 14):
    lw = random.randint(150, 320)
    draw.line([(145, ly), (145 + lw, ly)], fill=(140, 135, 125), width=1)
# Magnifying glass on top
draw_magnifying_glass(draw, 580, 300, 55, (120, 110, 90))
# Pen
draw.line([(550, 150), (650, 380)], fill=(30, 25, 20), width=5)
draw.polygon([(648, 378), (655, 390), (645, 388)], fill=(30, 25, 20))
add_noise(img, 10)
img = img.filter(ImageFilter.GaussianBlur(0.5))
img.save(f"{OUT}/case-files-desk.jpg", "JPEG", quality=90)
print("3/7 case files done")

# ========== IMAGE 4: Digital/OSINT theme ==========
img = make_gradient(800, 500, [(8, 15, 25), (5, 10, 20)])
draw = ImageDraw.Draw(img)
# Monitor/screen glow
for r in range(250, 0, -2):
    a = max(2, int(15 * (250 - r) / 250))
    draw.ellipse([400-r, 250-r, 400+r, 250+r], fill=(a, a+3, a+8))
# Grid lines (like data visualization)
for x in range(50, 750, 40):
    draw.line([(x, 50), (x, 450)], fill=(15, 25, 40), width=1)
for y in range(50, 450, 40):
    draw.line([(50, y), (750, y)], fill=(15, 25, 40), width=1)
# Data points connected
points = [(100, 350), (180, 280), (260, 320), (340, 200), (420, 250), (500, 180), (580, 220), (660, 150), (720, 190)]
for i in range(len(points)-1):
    draw.line([points[i], points[i+1]], fill=(40, 100, 160), width=2)
for p in points:
    draw.ellipse([p[0]-4, p[1]-4, p[0]+4, p[1]+4], fill=(60, 140, 200))
# Search/magnifying glass icon
draw_magnifying_glass(draw, 400, 250, 80, (30, 70, 120))
# Binary/code rain effect
for x in range(20, 780, 30):
    for y in range(0, 500, 20):
        if random.random() > 0.85:
            c = random.randint(15, 40)
            draw.text((x, y), random.choice(["0", "1"]), fill=(c, c+15, c+25))
add_noise(img, 5)
img.save(f"{OUT}/digital-investigation.jpg", "JPEG", quality=90)
print("4/7 digital done")

# ========== IMAGE 5: Child custody / family ==========
img = make_gradient(800, 500, [(20, 25, 40), (35, 40, 55)])
draw = ImageDraw.Draw(img)
# Courthouse/building
draw.rectangle([250, 120, 550, 420], fill=(45, 48, 60))
# Columns
for cx in range(280, 540, 50):
    draw.rectangle([cx, 160, cx+15, 380], fill=(55, 58, 70))
# Triangle top (pediment)
draw.polygon([(240, 160), (560, 160), (400, 90)], fill=(50, 53, 65))
# Steps
for i in range(4):
    sy = 380 + i * 12
    draw.rectangle([230 - i*15, sy, 570 + i*15, sy+10], fill=(40+i*3, 43+i*3, 55+i*3))
# Scale of justice icon
jx, jy = 400, 135
draw.line([(jx, jy-15), (jx, jy+5)], fill=(150, 140, 120), width=2)
draw.line([(jx-25, jy), (jx+25, jy)], fill=(150, 140, 120), width=2)
# Pans
draw.arc([jx-35, jy+5, jx-15, jy+20], 0, 180, fill=(150, 140, 120), width=2)
draw.arc([jx+15, jy+5, jx+35, jy+20], 0, 180, fill=(150, 140, 120), width=2)
draw.line([(jx-25, jy), (jx-25, jy+10)], fill=(150, 140, 120), width=1)
draw.line([(jx+25, jy), (jx+25, jy+10)], fill=(150, 140, 120), width=1)
# Ground
draw.rectangle([0, 430, 800, 500], fill=(25, 28, 40))
add_noise(img, 8)
img = img.filter(ImageFilter.GaussianBlur(0.7))
img.save(f"{OUT}/courthouse-justice.jpg", "JPEG", quality=90)
print("5/7 courthouse done")

# ========== IMAGE 6: Metairie street/neighborhood ==========
img = make_gradient(800, 500, [(15, 20, 35), (25, 30, 50)])
draw = ImageDraw.Draw(img)
# Road
draw.polygon([(300, 500), (500, 500), (420, 200), (380, 200)], fill=(30, 32, 40))
# Road lines
for y in range(220, 480, 30):
    lw = int(2 + (y - 200) * 0.02)
    cx = 400
    draw.rectangle([cx-lw, y, cx+lw, y+15], fill=(60, 58, 45))
# Houses on sides
for hx in [80, 160, 560, 640]:
    hw, hh = random.randint(50, 70), random.randint(40, 70)
    hy = 350 + random.randint(-20, 20)
    draw.rectangle([hx, hy-hh, hx+hw, hy], fill=(35, 38, 48))
    # Roof
    draw.polygon([(hx-5, hy-hh), (hx+hw+5, hy-hh), (hx+hw//2, hy-hh-25)], fill=(40, 35, 30))
    # Window with light
    if random.random() > 0.3:
        draw.rectangle([hx+15, hy-hh+12, hx+30, hy-hh+25], fill=(60, 55, 35))
# Oak trees (silhouettes)
for tx in [50, 250, 530, 720]:
    # Trunk
    draw.rectangle([tx-3, 280, tx+3, 380], fill=(15, 18, 25))
    # Canopy
    for r in range(50, 0, -1):
        c = max(8, 20 - r//5)
        draw.ellipse([tx-r, 250-r//2, tx+r, 250+r//2], fill=(c, c+3, c))
# Street lamp
draw.rectangle([345, 240, 350, 370], fill=(40, 42, 50))
for r in range(40, 0, -1):
    a = max(3, int(30 * (40 - r) / 40))
    draw.ellipse([347-r, 235-r, 347+r, 235+r], fill=(a+8, a+6, a))
add_noise(img, 7)
img = img.filter(ImageFilter.GaussianBlur(0.6))
img.save(f"{OUT}/metairie-neighborhood.jpg", "JPEG", quality=90)
print("6/7 neighborhood done")

# ========== IMAGE 7: Contact/consultation ==========
img = make_gradient(800, 500, [(15, 18, 30), (10, 12, 22)])
draw = ImageDraw.Draw(img)
# Phone icon large
pcx, pcy = 400, 220
# Phone body
draw.rounded_rectangle([pcx-40, pcy-70, pcx+40, pcy+70], radius=12, fill=(45, 50, 65))
draw.rounded_rectangle([pcx-35, pcy-60, pcx+35, pcy+45], radius=5, fill=(25, 35, 55))
# Screen glow
for r in range(60, 0, -1):
    a = max(2, int(12 * (60 - r) / 60))
    draw.ellipse([pcx-r, pcy-10-r, pcx+r, pcy-10+r], fill=(a, a+3, a+8))
# Shield/trust icon
sx, sy = 400, 380
draw.polygon([(sx, sy-30), (sx+25, sy-18), (sx+25, sy+5), (sx, sy+20), (sx-25, sy+5), (sx-25, sy-18)], fill=(35, 55, 80))
draw.polygon([(sx, sy-25), (sx+20, sy-15), (sx+20, sy+2), (sx, sy+15), (sx-20, sy+2), (sx-20, sy-15)], fill=(25, 45, 70))
# Check mark inside shield
draw.line([(sx-8, sy-3), (sx-2, sy+5), (sx+10, sy-10)], fill=(60, 140, 100), width=3)
# Decorative dots/circles
for _ in range(30):
    dx, dy = random.randint(50, 750), random.randint(50, 450)
    dr = random.randint(1, 3)
    dc = random.randint(20, 40)
    draw.ellipse([dx-dr, dy-dr, dx+dr, dy+dr], fill=(dc, dc+5, dc+10))
add_noise(img, 6)
img.save(f"{OUT}/consultation-contact.jpg", "JPEG", quality=90)
print("7/7 contact done")

print("\nAll images generated successfully!")
