"""B-11③ 동행임장 — b 구도로 계절만 바꿔 뽑기.

v2에서 셋 다 겨울로 나온 원인:
warmFilm 프리셋(낮은 채도) + "흐림" 지시가 겹치면 모델이 채도를 낮추는
가장 쉬운 방법으로 잎을 지운다. 계절은 반드시 명시할 것.

사용법:
    zsh -ic 'python3 ~/Desktop/donbora_site/fullcare-detail/gen_images_season.py'
"""
import base64
import os
import sys
from pathlib import Path

from openai import OpenAI

OUT = Path(__file__).parent / "images"
OUT.mkdir(parents=True, exist_ok=True)

MODEL = "gpt-image-2"

WARM_FILM = """
Visual style:
Warm Korean editorial lifestyle image. Soft overcast daylight, low contrast,
desaturated warm gray, beige, pale olive and faded blue palette. Visible fine 35mm film grain,
subtle haze, quiet negative space, cozy but modern. Not glossy, not luxury-ad style.
"""

BASE = (
    "한국의 아파트 단지 산책로를 두 사람이 함께 걸으며 이야기하는 모습. "
    "한 사람이 서류를 들고 있고 다른 한 사람은 그쪽으로 고개를 기울임. "
    "둘 다 뒷모습, 얼굴 안 보임. 다큐멘터리 톤, 연출된 포즈 아님."
)

SEASONS = [
    (
        "b11-3_v3_늦봄",
        "계절은 늦봄 — 나무에 잎이 완전히 나 있고 조경이 초록이지만, "
        "흐린 날이라 초록이 차분하게 가라앉아 있음. 얇은 겉옷 차림.",
    ),
    (
        "b11-3_v3_초여름",
        "계절은 초여름 — 잎이 무성하고 나무 그늘이 드리움. "
        "흐린 오후라 그림자가 부드럽고 대비가 낮음. 긴팔 셔츠 차림.",
    ),
    (
        "b11-3_v3_초가을",
        "계절은 초가을 — 잎이 아직 대부분 남아 있고 색이 막 바래기 시작함. "
        "흐린 오후의 차분한 빛. 얇은 니트나 재킷 차림.",
    ),
]

NEGATIVES = (
    "얼굴이 보이지 않게 할 것. 건물 동 번호, 단지명, 간판, 현수막 등 "
    "읽을 수 있는 글자를 넣지 말 것. 로고, 워터마크 없음. "
    "럭셔리 분양 광고 느낌 금지. 너무 선명하거나 쨍한 색감 금지. "
    "웃거나 카메라를 보는 모습 금지. "
    "겨울 금지 — 잎 없는 앙상한 나뭇가지, 눈, 두꺼운 패딩 금지."
)


def main():
    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY 없음 — 'zsh -ic' 로 실행하세요.")
    client = OpenAI()
    for name, season in SEASONS:
        prompt = (
            f"{BASE}\n{season}\n{WARM_FILM.strip()}\n\n제약:\n{NEGATIVES}\n"
        )
        print(f"생성 중: {name} ...", flush=True)
        r = client.images.generate(
            model=MODEL,
            prompt=prompt,
            size="1536x1024",
            quality="high",
            output_format="png",
            n=1,
        )
        path = OUT / f"{name}.png"
        path.write_bytes(base64.b64decode(r.data[0].b64_json))
        print(f"  → {path}  ({path.stat().st_size // 1024} KB)", flush=True)
    print("\n완료 — 3장")


if __name__ == "__main__":
    main()
