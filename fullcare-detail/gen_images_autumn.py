"""B-11③ 동행임장 — 초가을 방향 변주 3장 (v4).

v3에서 초가을이 가장 좋았음. 유지할 것:
  - 초가을 (warmFilm 팔레트와 안 싸우는 유일한 계절)
  - 서류를 사이에 둔 두 사람, 뒷모습, 얼굴 안 보임
  - 읽을 수 있는 글자 없음

v4에서 새로 넣는 조건:
  모바일 본문 폭이 335px라 v3는 인물이 화면의 1/3이라 줄이면 묻힌다.
  → 인물을 프레임에서 더 크게, 하늘·원경 비중을 줄인다.

사용법:
    zsh -ic 'python3 ~/Desktop/donbora_site/fullcare-detail/gen_images_autumn.py'
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

SEASON = (
    "계절은 초가을 — 잎이 아직 대부분 남아 있고 색이 막 바래기 시작함. "
    "흐린 오후의 차분한 빛. 얇은 니트나 재킷 차림."
)

FRAMING = (
    "구도: 두 사람의 상반신이 화면 높이의 절반 이상을 차지하도록 가까이서 촬영. "
    "하늘과 먼 배경은 최소로. 세로로 긴 화면에 잘라 넣어도 인물이 살아 있어야 함."
)

SHOTS = [
    (
        "b11-3_v4_a_서류",
        "한국의 아파트 단지 안, 두 사람이 나란히 서서 함께 서류 한 장을 내려다보며 "
        "이야기하는 모습. 한 사람이 서류의 한 지점을 손가락으로 짚고 있음. "
        "둘 다 뒷모습이고 얼굴은 보이지 않음. 뒤로 아파트 동과 조경이 흐릿하게 보임.",
    ),
    (
        "b11-3_v4_b_가리킴",
        "한국의 아파트 단지 안, 두 사람 중 한 사람이 서류를 든 채 다른 손으로 "
        "건물 쪽을 가리키며 설명하고, 다른 한 사람이 그 방향을 바라보는 모습. "
        "둘 다 뒷모습이고 얼굴은 보이지 않음. 아파트 동이 화면 위쪽을 채움.",
    ),
    (
        "b11-3_v4_c_현관",
        "한국 아파트 동 현관 앞에 두 사람이 멈춰 서서, 한 사람이 서류를 펼쳐 보이고 "
        "다른 한 사람이 고개를 숙여 들여다보는 모습. "
        "둘 다 뒷모습이고 얼굴은 보이지 않음. 현관 구조물과 조경이 배경.",
    ),
]

NEGATIVES = (
    "얼굴이 보이지 않게 할 것. 건물 동 번호, 단지명, 간판, 현수막, 서류 위의 글씨 등 "
    "읽을 수 있는 글자를 넣지 말 것. 로고, 워터마크 없음. "
    "럭셔리 분양 광고 느낌 금지. 너무 선명하거나 쨍한 색감 금지. "
    "웃거나 카메라를 보는 모습 금지. 두 사람이 연인처럼 붙어 있지 않게 할 것. "
    "겨울 금지 — 잎 없는 앙상한 나뭇가지, 눈, 두꺼운 패딩 금지."
)


def main():
    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY 없음 — 'zsh -ic' 로 실행하세요.")
    client = OpenAI()
    for name, scene in SHOTS:
        prompt = (
            f"{scene}\n{SEASON}\n{FRAMING}\n"
            f"{WARM_FILM.strip()}\n\n제약:\n{NEGATIVES}\n"
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
