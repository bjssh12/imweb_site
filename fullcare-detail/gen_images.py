"""돈보라 풀케어 상세페이지 — 이미지 생성

기존 하네스 방식을 그대로 따름:
  ~/Documents/Codex/2026-06-28/new-chat/make_image.py
  ~/Documents/Codex/2026-06-28/new-chat/image_style_maker.html
  → 모델 gpt-image-2 · 한글 씬 + 영문 Visual style 블록 · warmFilm 프리셋

사용법:
    zsh -ic 'python3 ~/Desktop/donbora_site/fullcare-detail/gen_images.py b11-3'

생성 금지 자산은 여기 넣지 말 것 (기획서 B-11①②⑤, B-13 인증):
"실물이 아니면 증거가 아니라 조작이다"
"""
import base64
import os
import sys
from pathlib import Path

from openai import OpenAI

OUT = Path(__file__).parent / "images"
OUT.mkdir(parents=True, exist_ok=True)

MODEL = "gpt-image-2"

# image_style_maker.html 의 프리셋 원문
STYLES = {
    "warmFilm": """
Visual style:
Warm Korean editorial lifestyle image. Soft overcast daylight, low contrast,
desaturated warm gray, beige, pale olive and faded blue palette. Visible fine 35mm film grain,
subtle haze, quiet negative space, cozy but modern. Not glossy, not luxury-ad style.
""",
    "rainySeoul": """
Visual style:
Quiet rainy Seoul mood. Cloudy apartment skyline outside the window, muted gray-blue sky,
soft reflections, low saturation, editorial film photograph feeling, gentle grain.
""",
}

BATCHES = {
    # B-11③ 동행임장 현장 사진 — 기획서: 실물 없으면 생성 가능, 얼굴 비식별
    "b11-3": {
        "style": "warmFilm",
        "size": "1536x1024",
        "quality": "high",
        "items": [
            (
                "b11-3_동행임장_v2_a",
                "한국의 아파트 단지 안, 코치와 의뢰인 두 사람이 나란히 서서 "
                "한 사람이 손을 들어 건물 위쪽을 가리키며 설명하는 모습. "
                "둘 다 뒷모습이고 얼굴은 보이지 않음. 평일 낮, 흐린 하늘. "
                "다큐멘터리처럼 자연스럽게 포착된 순간, 연출된 포즈 아님.",
            ),
            (
                "b11-3_동행임장_v2_b",
                "한국의 아파트 단지 산책로를 두 사람이 함께 걸으며 이야기하는 모습. "
                "한 사람이 서류를 들고 있고 다른 한 사람은 그쪽으로 고개를 기울임. "
                "둘 다 뒷모습, 얼굴 안 보임. 흐린 오후, 낮은 채도의 조경. "
                "다큐멘터리 톤, 광고 느낌 없음.",
            ),
            (
                "b11-3_동행임장_v2_c",
                "한국 아파트 동 현관 앞에서 두 사람이 잠시 멈춰 서서 건물을 올려다보는 모습. "
                "뒷모습이고 얼굴은 보이지 않음. 흐린 겨울 오후의 차분한 빛. "
                "조용하고 진지한 분위기, 밝고 활기찬 느낌 아님.",
            ),
        ],
        # 전 배치에서 실제로 문제가 됐던 것들
        "negatives": (
            "얼굴이 보이지 않게 할 것. 건물 동 번호, 단지명, 간판, 현수막 등 "
            "읽을 수 있는 글자를 넣지 말 것. 로고, 워터마크 없음. "
            "럭셔리 분양 광고 느낌 금지. 너무 선명하거나 쨍한 색감 금지. "
            "웃거나 카메라를 보는 모습 금지."
        ),
    },
}


def build_prompt(scene, style_key, negatives):
    return f"{scene.strip()}\n{STYLES[style_key].strip()}\n\n제약:\n{negatives.strip()}\n"


def run(batch_name):
    batch = BATCHES[batch_name]
    client = OpenAI()
    made = []
    for name, scene in batch["items"]:
        prompt = build_prompt(scene, batch["style"], batch["negatives"])
        print(f"생성 중: {name} ...", flush=True)
        r = client.images.generate(
            model=MODEL,
            prompt=prompt,
            size=batch["size"],
            quality=batch["quality"],
            output_format="png",
            n=1,
        )
        path = OUT / f"{name}.png"
        path.write_bytes(base64.b64decode(r.data[0].b64_json))
        made.append(path)
        print(f"  → {path}  ({path.stat().st_size // 1024} KB)", flush=True)
    return made


if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY 없음 — 'zsh -ic' 로 실행하세요.")
    which = sys.argv[1] if len(sys.argv) > 1 else "b11-3"
    if which not in BATCHES:
        sys.exit(f"모르는 배치: {which} (가능: {', '.join(BATCHES)})")
    files = run(which)
    print(f"\n완료 — {len(files)}장")
