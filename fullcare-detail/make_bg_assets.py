"""돈보라 상세페이지 배경 에셋 생성.

카드뉴스·그레인 스타일(피그마 82:50)에서 뽑은 질감을 타일 가능한 PNG로 만든다.
피그마에는 jsDelivr URL로 불러오고, 아임웹 HTML에서도 같은 파일을 쓴다.

    python3 ~/Desktop/donbora_site/fullcare-detail/make_bg_assets.py
"""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

OUT = Path(__file__).parent / "images"
OUT.mkdir(parents=True, exist_ok=True)

SIZE = 512
random.seed(7)          # 재현 가능하게

BRAND = {
    "GREEN": (36, 134, 120),
    "LIME": (192, 249, 136),
    "SKY": (238, 244, 250),
    "POWDER": (202, 217, 235),
    "INK": (7, 8, 12),
}


def grain(alpha_max=26, name="bg_grain.png"):
    """투명 배경 위 단색 노이즈 — 어떤 바탕에도 얹을 수 있는 오버레이."""
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    px = img.load()
    for y in range(SIZE):
        for x in range(SIZE):
            v = random.randint(0, 255)
            a = int(abs(v - 128) / 128 * alpha_max)
            tone = 255 if v > 128 else 0
            px[x, y] = (tone, tone, tone, a)
    img.save(OUT / name)
    return name


def paper(name="bg_paper.png"):
    """종이 질감 — 그레인보다 굵고 부드럽다. 후기·인증 구간용."""
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    px = img.load()
    for y in range(SIZE):
        for x in range(SIZE):
            v = random.randint(0, 255)
            a = int(abs(v - 128) / 128 * 40)
            tone = 255 if v > 128 else 90
            px[x, y] = (tone, tone, tone, a)
    img = img.filter(ImageFilter.GaussianBlur(0.6))
    img.save(OUT / name)
    return name


def soft_mesh(name="bg_mesh.png", w=750, h=900):
    """흰→SKY→LIME 대각 메시 그라디언트 + 그레인. 구간 전환용 바탕."""
    base = Image.new("RGB", (w, h))
    px = base.load()
    c_hi = (255, 255, 255)
    c_mid = BRAND["SKY"]
    c_lo = BRAND["POWDER"]
    c_acc = BRAND["LIME"]
    for y in range(h):
        for x in range(w):
            t = (x / w * 0.62 + y / h * 0.38)
            if t < 0.5:
                k = t / 0.5
                c = tuple(int(c_hi[i] + (c_mid[i] - c_hi[i]) * k) for i in range(3))
            else:
                k = (t - 0.5) / 0.5
                c = tuple(int(c_mid[i] + (c_lo[i] - c_mid[i]) * k) for i in range(3))
            # 우하단에 라임 기운
            d = math.hypot(x - w * 0.92, y - h * 0.88) / (w * 0.75)
            if d < 1:
                k = (1 - d) ** 2 * 0.5
                c = tuple(int(c[i] + (c_acc[i] - c[i]) * k) for i in range(3))
            px[x, y] = c
    base = base.convert("RGBA")
    g = Image.open(OUT / "bg_grain.png").resize((w, h))
    base.alpha_composite(g)
    base.save(OUT / name)
    return name


def grid(name="bg_grid.png", gap=48, w=750, h=900):
    """SKY 바탕 + POWDER 격자 + 그레인. donbora-deck bg_grid 의 상세페이지판."""
    img = Image.new("RGBA", (w, h), BRAND["SKY"] + (255,))
    d = ImageDraw.Draw(img)
    line = BRAND["POWDER"] + (115,)
    for x in range(gap, w, gap):
        d.line([(x, 0), (x, h)], fill=line, width=1)
    for y in range(gap, h, gap):
        d.line([(0, y), (w, y)], fill=line, width=1)
    g = Image.open(OUT / "bg_grain.png").resize((w, h))
    img.alpha_composite(g)
    img.save(OUT / name)
    return name


def deep(name="bg_deep.png", w=750, h=900):
    """INK 그라디언트 + GREEN 격자 + 중앙 하단 글로우 + 그레인. 최종 CTA용."""
    img = Image.new("RGBA", (w, h))
    px = img.load()
    a, b = BRAND["INK"], (14, 35, 32)
    for y in range(h):
        for x in range(w):
            k = (x / w * 0.5 + y / h * 0.5)
            px[x, y] = tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3)) + (255,)
    d = ImageDraw.Draw(img)
    line = BRAND["GREEN"] + (46,)
    for x in range(48, w, 48):
        d.line([(x, 0), (x, h)], fill=line, width=1)
    for y in range(48, h, 48):
        d.line([(0, y), (w, y)], fill=line, width=1)
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    r = int(w * 0.55)
    gd.ellipse([w // 2 - r, h - r, w // 2 + r, h + r], fill=BRAND["GREEN"] + (120,))
    glow = glow.filter(ImageFilter.GaussianBlur(90))
    img.alpha_composite(glow)
    g = Image.open(OUT / "bg_grain.png").resize((w, h))
    img.alpha_composite(g)
    img.save(OUT / name)
    return name


if __name__ == "__main__":
    made = [grain(), paper(), soft_mesh(), grid(), deep()]
    for m in made:
        p = OUT / m
        print(f"  → {p}  ({p.stat().st_size // 1024} KB)")
    print(f"\n완료 — {len(made)}장")
