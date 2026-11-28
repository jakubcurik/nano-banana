<p align="center">
  <img src="../assets/logo.png" width="132" alt="nano-banana 로고: 짙은 흑연색 정사각형 위에서 손을 흔드는 윤기 나는 노란 바나나 캐릭터">
</p>

<h1 align="center">nano-banana</h1>

<p align="center">
  <em>코딩 에이전트로 만드는 이미지, 비용은 손에 쥔 채로.</em>
</p>

<p align="center">
  <a href="https://github.com/jakubcurik/nano-banana/actions/workflows/tests.yml"><img alt="Tests" src="https://github.com/jakubcurik/nano-banana/actions/workflows/tests.yml/badge.svg?branch=main"></a>
  <a href="https://github.com/jakubcurik/nano-banana/actions/workflows/validate.yml"><img alt="Validate" src="https://github.com/jakubcurik/nano-banana/actions/workflows/validate.yml/badge.svg?branch=main"></a>
  <a href="https://github.com/jakubcurik/nano-banana/releases"><img alt="Release" src="../assets/badges/release.svg"></a>
  <a href="../LICENSE"><img alt="라이선스: MIT" src="../assets/badges/license-mit.svg"></a>
  <a href="https://github.com/jakubcurik/nano-banana/stargazers"><img alt="스타" src="../assets/badges/stars.svg"></a>
</p>

<p align="center">
  <img alt="Claude Code 플러그인" src="../assets/badges/claude-code-plugin.svg">
  <a href="https://agentskills.io"><img alt="Agent Skills 형식" src="../assets/badges/agent-skills.svg"></a>
  <img alt="Python 3.11 이상" src="../assets/badges/python.svg">
  <img alt="Gemini API" src="../assets/badges/gemini-api.svg">
</p>

<p align="center">
  <a href="#install">설치</a> &middot;
  <a href="#quick-start">빠른 시작</a> &middot;
  <a href="#gallery">갤러리</a> &middot;
  <a href="#how-it-works">작동 방식</a> &middot;
  <a href="#models-and-prices">모델과 가격</a> &middot;
  <a href="#faq">자주 묻는 질문</a>
</p>

<p align="center">
  <sub><a href="../README.md">English</a> &middot;
  <a href="README.zh-CN.md">简体中文</a> &middot;
  <a href="README.es.md">Español</a> &middot;
  <a href="README.ja.md">日本語</a> &middot;
  <a href="README.pt-BR.md">Português (Brasil)</a> &middot;
  <a href="README.de.md">Deutsch</a> &middot;
  <a href="README.fr.md">Français</a> &middot;
  한국어 &middot;
  <a href="README.cs.md">Čeština</a></sub>
</p>

<p align="center">
  <img src="../assets/hero.jpg" width="880" alt="윤기 나는 3D 바나나 캐릭터가 작은 이젤에 햇살 가득한 풍경을 그리고 있고, 옆에는 긴 종이 영수증과 금화 몇 개가 있습니다. 제목은 nano-banana입니다.">
</p>

nano-banana는 Claude Code를 비롯한 코딩 에이전트가 Google의 Nano Banana 모델로 이미지를 만들고 편집할 수 있게 해 주는 에이전트 스킬입니다. 이때 드는 비용도 함께 추적합니다.

에이전트에 히어로 이미지를 요청하면 이미지가 나옵니다. 그런데 "변형을 몇 개 더 시도해 줘"라고 하면, 일반 API 호출은 첫 번째 결과를 보고 있는 동안 4K 이미지를 열두 장쯤 생성해 버릴 수 있습니다. 이미지마다 요금이 청구되는데, 채팅에서는 그 금액을 알 수 없습니다.

이 스킬은 호출 전에 예상 가격을, 호출 후에 thinking 및 입력 토큰까지 포함한 실제 비용을 출력합니다. 예상 비용이 한도(따로 정하지 않으면 0.50 USD)를 넘는 실행은 아무것도 보내기 전에 멈춥니다. 선택한 옵션이 해당 모델에서 지원되는지도 확인하므로, 잘못된 크기나 지원하지 않는 thinking 수준은 API에서 오류가 나는 것이 아니라 로컬에서 먼저 실패합니다. 그 밖에는 에이전트가 따를 짧은 절차를 제공합니다. 이미지를 어디에 쓸지 파악하고, 대상이 실제 사물처럼 보여야 하면 참고 사진을 확보하고, 프롬프트는 영어로 작성하고, 완료라고 하기 전에 결과를 직접 확인합니다.

<sub>비공식 프로젝트입니다. Google과 제휴 관계가 아니며 Google의 승인을 받지 않았습니다. "Nano Banana"와 "Gemini"는 Google이 자사의 이미지 모델과 API에 붙인 이름입니다.</sub>

## 실행 모습

<p align="center">
  <img src="../assets/terminal.png" width="880" alt="한 번의 생성에 대한 터미널 출력: 모델, 예상 비용 0.0336 USD, 17.9초 만의 API 응답, 저장된 파일 경로, 모델의 짧은 답변, 인터랙션 ID, 그리고 이미지·thinking·텍스트·입력 토큰으로 나눈 실제 비용 0.0426 USD.">
</p>

실제 실행 결과입니다. 기본 모델에서 1K 이미지 자체의 예상 비용은 0.0336 USD입니다. 호출 후 실제 비용에는 thinking, 모델의 짧은 텍스트 답변, 프롬프트가 더해져 여기서는 0.0426 USD이며, 호출에 18초가 걸렸다는 것도 출력에 나옵니다.

<a id="gallery"></a>

## 갤러리

텍스트와 터미널 스크린샷을 제외하면 이 README의 모든 이미지는 이 스킬로 만들었습니다. 이미지에 나오는 사람, 장소, 사물은 모두 AI가 생성한 것입니다. 프롬프트는 [`assets/prompts`](../assets/prompts)에서 볼 수 있습니다.

<p align="center">
  <img src="../assets/gallery/photo-gallery-wall.jpg" width="266" alt="휴대폰으로 찍은 사진. 바나나 한 개가 은색 덕트 테이프로 흰 갤러리 벽에 붙어 있고, 옆에는 빈 흰색 카드가 있습니다. 초점이 흐린 배경에서는 관람객 두 명이 진지하게 바나나를 살펴봅니다.">
  <img src="../assets/gallery/photo-shopping-cart.jpg" width="266" alt="휴대폰으로 찍은 사진. 바나나가 슈퍼마켓 쇼핑 카트의 아이 좌석에 빨간 안전벨트로 고정되어 있습니다.">
  <img src="../assets/gallery/photo-car-seat.jpg" width="266" alt="운전석에서 휴대폰으로 찍은 사진. 바나나가 조수석에 똑바로 앉아 있고 안전벨트가 가로질러 채워져 있습니다.">
  <br>
  <sub><b>휴대폰으로 찍은 듯한 사진.</b> 갤러리 벽에 테이프로 붙인 바나나, 쇼핑 카트에 벨트로 고정한 바나나, 자동차 시트에 안전벨트를 맨 바나나입니다. Model 2.1, 2K, 3:4, 이미지당 약 5센트.</sub>
</p>

<p align="center">
  <img src="../assets/gallery/edit-before-night-flash.jpg" width="372" alt="한 여성이 밤에 상점 쇼윈도 앞을 지나갑니다. 카메라의 강한 플래시가 비추고 있고, 반쯤 껍질을 벗긴 바나나를 들고 왼쪽을 바라봅니다.">
  <img src="../assets/gallery/edit-after-sunny-day.jpg" width="372" alt="같은 사진을 파란 하늘 아래 밝은 오후 햇빛으로 바꾼 이미지. 같은 여성, 같은 자세, 같은 바나나, 같은 쇼윈도입니다.">
  <br>
  <sub><b><code>--image</code>로 편집.</b> 밤에 플래시를 터뜨려 찍은 사진을 화창한 오후로 바꿨습니다. 조명 외에는 모두 그대로입니다. Model 2.1, 1K, 약 3센트.</sub>
</p>

<p align="center">
  <img src="../assets/gallery/graphic-infographic.jpg" width="760" alt="Anatomy of a banana라는 제목의 인포그래픽. 어두운 배경 위의 윤기 나는 바나나에 라벨 네 개가 Stem, Peel, Fruit, Tip을 가리킵니다.">
  <br>
  <img src="../assets/gallery/graphic-poster.jpg" width="300" alt="BANANA ISLAND와 Visit the sunny side라는 문구가 적힌 복고풍 여행 포스터. 바나나 모양의 섬, 야자수, 석양 속 돛단배가 있습니다.">
  <img src="../assets/gallery/graphic-vector.jpg" width="375" alt="기하학적 도형으로 만든 바나나의 플랫 벡터 일러스트. 은은한 청록색 배경에 노란색과 황갈색을 사용했습니다.">
  <br>
  <sub><b>그래픽.</b> 인포그래픽과 텍스트 포스터는 Model Pro(2K, 개당 약 13센트), 플랫 벡터 일러스트는 Model 2.1(2K, 약 5센트)로 만들었습니다.</sub>
</p>

<p align="center">
  <img src="../assets/gallery/mascot-hammock.jpg" width="372" alt="선글라스를 쓴 윤기 나는 3D 바나나 마스코트가 열대 해변의 야자수 두 그루 사이 해먹에서 쉬고 있습니다.">
  <img src="../assets/gallery/mascot-surf.jpg" width="372" alt="윤기 나는 3D 바나나 마스코트가 청록색 파도 위에서 작은 서핑보드를 타고, 균형을 잡으려고 팔을 벌리고 있습니다.">
  <br>
  <sub><code>--follow-up</code>으로 <b>같은 마스코트를 새로운 장면에</b> 등장시켰습니다. Model 2.1, 1K, 이미지당 약 3센트.</sub>
</p>

<a id="install"></a>

## 설치

Claude Code에서는 플러그인 마켓플레이스로 설치합니다.

```
/plugin marketplace add jakubcurik/nano-banana
/plugin install nano-banana@nano-banana
```

`SKILL.md` 스킬을 읽는 다른 에이전트에서는 [`npx skills`](https://github.com/vercel-labs/skills)로 설치합니다.

```bash
npx skills add jakubcurik/nano-banana
```

또는 `skills/nano-banana/`를 사용하는 에이전트의 스킬 폴더에 직접 복사해도 됩니다. 예를 들어 Claude Code는 `~/.claude/skills/`, Codex, Gemini CLI, Cursor는 `~/.agents/skills/`입니다.

다음도 필요합니다.

- [`uv`](https://docs.astral.sh/uv/): `google-genai`와 Python 3.11+를 알아서 가져옵니다. uv가 없으면 Python 3.11+를 설치하고 `pip install "google-genai>=3.6,<4"`를 실행하세요.
- [Google AI Studio](https://aistudio.google.com/apikey)에서 발급받은 Gemini API 키(결제 활성화 필요). 이미지 모델에는 무료 등급이 없습니다.

키는 환경 변수로 스크립트에 전달하거나, 저장소 밖에 한 번만 저장해 두세요.

```bash
export GEMINI_API_KEY="your-key"
# or
mkdir -p ~/.config/nano-banana && printf '%s' "your-key" > ~/.config/nano-banana/api-key
```

<a id="quick-start"></a>

## 빠른 시작

에이전트에 이렇게 요청해 보세요. "내 커피숍 사이트에 쓸 히어로 이미지를 16:9로 만들어 줘", "이 사진에서 자동차를 지워 줘", "이 사진 두 장을 합쳐 줘". 스킬은 저절로 실행됩니다. 이미지를 어디에 쓸지 묻고, 프롬프트를 작성하고, 가격이 무시할 수준이 아니면 알려 준 뒤, 스크립트를 실행해 결과를 확인합니다.

스크립트를 직접 호출할 수도 있습니다.

```bash
S=skills/nano-banana/scripts/generate.py

uv run --script $S "A flat illustration of a red apple on a white table" --estimate
uv run --script $S "A flat illustration of a red apple on a white table" -a 16:9 -s 2K --format jpeg
uv run --script $S "Make the apple green. Keep everything else the same." --follow-up
uv run --script $S "Put this product on a marble table" -i product.jpg -m pro -s 2K
uv run --script $S "A banner with the text \"Open daily\"" --batch -n 4 --currency EUR
uv run --script $S --batch-result
uv run --script $S "Same scene at dusk. Keep everything else the same." --follow-up .cache/nano-banana/20261128-101500-a-flat-illustration-2.png

F=skills/nano-banana/scripts/finish.py
uv run --script $F .cache/nano-banana/hero.png --size 1200x630 --format webp
uv run --script $F .cache/nano-banana/icon.png --transparent
```

이미지는 `.cache/nano-banana/`에 저장되며, 각 이미지 옆에 프롬프트, 옵션, 인터랙션 ID, 호출 시간과 비용이 담긴 `.txt` 파일이 함께 생깁니다. 이 폴더에는 자체 `.gitignore`가 만들어지므로 안의 파일이 git에 들어가지 않습니다.

배치 작업은 최대 8분(`--wait`)까지 기다린 뒤 스크립트가 종료되고, 결과를 받아 오는 방법을 알려 줍니다. `--batch-result`는 작업이 끝났으면 이미지를 저장하며, 다시 실행해도 파일이 중복되지 않습니다.

<details>
<summary>전체 옵션</summary>

| 옵션 | 의미 |
|---|---|
| `-m 2.1 / 2 / pro / lite` | 모델, 기본값은 `2.1` |
| `-s 512 / 1K / 2K / 4K` | 해상도, 기본값은 `1K` (512는 모델 `2`에서만 가능) |
| `-a 16:9` | 화면 비율: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9. 2.1과 2에서는 1:4, 4:1, 1:8, 8:1도 가능 |
| `-i photo.jpg` | 편집 대상 또는 참고용 입력 이미지, 여러 번 지정 가능, 최대 14장 |
| `-t minimal / medium / high` | 사고(thinking) 수준, 모델에 따라 다름 |
| `--search` | 이미지 검색을 포함한 Google Search 그라운딩 (`lite`에서는 사용 불가) |
| `--follow-up [IMAGE or ID]` | 마지막 결과, 고른 이미지(ID는 해당 `.txt`에 있음) 또는 지정한 인터랙션에서 이어서 진행 |
| `-n 4` | 이미지 수, 이미지마다 따로 과금 |
| `-o folder` | 출력 폴더 |
| `--name hero` | 프롬프트 앞부분 대신 쓸 파일 이름 |
| `--format png / jpeg` | 출력 파일 형식. 2.1, 2, lite는 JPEG만 반환하므로 `png`는 거부됨 |
| `--prompt-file file` | 파일에서 프롬프트 읽기 |
| `--no-store` | Google에 인터랙션을 저장하지 않도록 요청 (이 경우 해당 인터랙션에서는 후속 편집을 할 수 없음) |
| `--delete IMAGE or ID` | Google에 저장된 인터랙션 삭제 |
| `--batch` | 절반 가격, 최대 24시간 소요 (모델 2.1과 lite) |
| `--wait 8` | 종료하기 전에 배치 작업을 기다릴 시간(분), `0`은 제출만 하고 종료 |
| `--batch-result [JOB]` | 배치 작업 결과 받기, 기본값은 출력 폴더에 마지막으로 제출한 작업 |
| `--estimate` | 예상 가격을 출력하고 종료 |
| `--max-cost 0.50` | 예상 비용이 이 USD 금액을 넘으면 호출 전에 중단 |
| `--currency CZK` | 해당 통화로도 가격 표시 (환율은 체코 국립은행 기준) |

`--currency`와 `--max-cost`는 `NANO_BANANA_CURRENCY`와 `NANO_BANANA_MAX_COST`, 또는 `~/.config/nano-banana/config.json`(`{"currency": "EUR", "max_cost": 1}`)에서도 지정할 수 있습니다. 명령줄이 가장 우선이고, 그다음 환경 변수, 마지막이 파일입니다.

`finish.py`는 `--size WxH`(채우도록 크기를 맞춘 뒤 잘라 내기, `--keep`으로 남길 부분 선택), `--format webp / avif / jpeg / png`, `--quality`, `--transparent [COLOR]`를 지원합니다.

</details>

<a id="how-it-works"></a>

## 작동 방식

이 스킬은 에이전트가 정해진 순서로 일하게 합니다. 먼저 요청과 프로젝트에서 이미지의 용도를 파악하고, 빠진 것만 묻습니다. 실제 종, 제품, 장소를 보여 줘야 한다면 참고 사진 두세 장을 구하고 사용자에게 확인을 받습니다. 그다음 영어로 프롬프트를 쓰고 가격을 추정합니다. 0.50 USD를 넘으면 스크립트가 스스로 실행을 거부하고, 에이전트는 사용자가 동의할 때만 한도를 올립니다. 이미지가 네 장보다 많을 때도 먼저 묻습니다. 생성한 뒤에는 결과를 살펴보고, 사소한 수정은 처음부터 다시 만들지 않고 후속 편집으로 처리하며, 이미지를 들어갈 페이지에 맞게 자르고 변환할 수도 있습니다.

전체 워크플로는 [`SKILL.md`](../skills/nano-banana/SKILL.md)에 있습니다. 프롬프트 템플릿, 편집 템플릿, 흔한 실수 목록은 [`references/prompting.md`](../skills/nano-banana/references/prompting.md)에 있습니다.

<a id="models-and-prices"></a>

## 모델과 가격

2026년 11월 28일 기준, 이미지당 USD입니다. thinking 및 입력 토큰은 별도이며, 보통 이미지당 1센트 미만입니다.

| 모델 | 적합한 용도 | 1K | 2K | 4K |
|---|---|---|---|---|
| `2.1` (`gemini-nano-banana-2.1`) | 거의 모든 작업 | 0.034 | 0.050 | 0.113 |
| `2` (`gemini-3.1-flash-image`) | 512 px. Google이 지원 중단 예정으로 표시했으며, 종료일은 아직 없음 | 0.067 | 0.101 | 0.151 |
| `pro` (`gemini-3-pro-image`) | 가장 까다로운 프롬프트, 텍스트가 많은 이미지 | 0.134 | 0.134 | 0.240 |
| `lite` (`gemini-3.1-flash-lite-image`) | 단순한 이미지를 많이 만들 때, 1K만 지원, 검색 없음 | 0.034 | n/a | n/a |

가격과 모델 데이터는 [`models.json`](../skills/nano-banana/scripts/models.json)에 있습니다. Google이 [가격표](https://ai.google.dev/gemini-api/docs/pricing)를 바꿀 때 스크립트가 가격을 읽는 파일은 이것 하나이며, 이 문서와 `SKILL.md`의 표가 이 파일과 어긋나면 테스트가 실패합니다. `--search`는 별도로 과금됩니다. 그라운딩 프롬프트 월 5,000건은 무료이고, 그 이후에는 검색 쿼리 1,000건당 14 USD입니다.

## 알아두면 좋은 점

- Google은 후속 편집이 가능하도록 인터랙션을 저장합니다. 유료 프로젝트는 55일, 무료 등급은 1일입니다. 민감한 사진에는 `--no-store`를 사용하거나, 나중에 `--delete`로 삭제하세요.
- 생성된 모든 이미지에는 눈에 보이지 않는 SynthID 워터마크가 들어갑니다.
- 모델은 세부 묘사를 지어냅니다. 이미지가 실제 종, 제품, 건물과 일치해야 하면 `-i`로 참고 사진 2-3장을 함께 주세요. 스킬의 워크플로도 이를 필수로 요구합니다.
- 오류가 나면 스크립트가 다시 시도해도 안전한지 알려 줍니다. 거부된 요청(4xx, 예를 들어 잘못된 옵션, 없는 키, 할당량)은 과금되지 않았습니다. 서버 오류나 타임아웃은 과금되었을 수 있으므로, 스크립트는 스스로 재시도하지 않습니다.
- 1.1의 실제 테스트에서 모델 2.1의 1K 이미지 한 장은 11.5~17.9초가 걸렸습니다. 셸 호출이 시간 초과로 끊긴 에이전트는 이미 비용을 낸 이미지를 잃게 되므로, 스킬은 충분한 시간을 주거나 긴 작업은 백그라운드에서 실행하라고 안내합니다.
- 모델은 투명한 이미지를 반환할 수 없습니다. 결과는 JPEG이고, 투명 배경을 요청하면 가짜 체크무늬를 그립니다. 단색 배경을 요청한 뒤 `finish.py --transparent`로 잘라 내세요. 단색 한 가지만 제거하므로 부드러운 그림자와 그라데이션은 남습니다.
- `--search`로 만든 결과물을 공개하는 경우 Google은 검색 제안을 표시하도록 요구합니다. 스크립트는 이를 이미지 옆에 저장합니다.

<a id="faq"></a>

## 자주 묻는 질문

**Google에는 자체 `gemini-api` CLI가 있습니다. 왜 이걸 써야 하나요?**
CLI는 호출을 수행하고, 그 일을 잘 해냅니다. 이 스킬은 호출을 둘러싼 부분을 더해 줍니다. 둘 다 필요할 수 있습니다.

| | Google `gemini-api` CLI와 스킬 | nano-banana |
|---|---|---|
| 호출 전 가격 추정, 호출 후 실제 비용 | 아니요 | 예 |
| 한도를 올리기 전까지 비용이 큰 실행은 멈춤 | 아니요 | 예(`--max-cost`) |
| 실패한 호출이 과금되었을 수 있는지 알려 줌 | 아니요 | 예 |
| 모델에 맞는지 옵션 검사 | 아니요, API가 거부함 | 예 |
| ID를 복사하지 않는 후속 편집 | 수동 | `--follow-up` |
| 이미지마다 프롬프트와 옵션을 옆에 저장 | 아니요 | 예 |
| 배치 결과를 나중 실행에서 받아 오기 | 아니요 | `--batch-result` |
| 웹용 자르기, 변환, 배경 투명화 | 아니요 | `finish.py` |
| 프롬프트 작성 가이드와 템플릿 | 아니요 | 예 |

CLI는 빠르게 변하는 베타 버전이므로, 선택하기 전에 둘 다 확인해 보세요.

**Claude Code 밖에서도 작동하나요?**
이 스킬은 공개 [Agent Skills](https://agentskills.io) 형식을 따르므로, `SKILL.md` 파일을 불러오는 다른 에이전트에서도 사용할 수 있습니다. 다만 Claude Code에서만 테스트했습니다.

**가격이 바뀌었습니다. 무엇을 수정해야 하나요?**
`skills/nano-banana/scripts/models.json`과, `SKILL.md`, 이 문서, 각 번역의 표를 수정하세요. 하나라도 빠지면 테스트가 알려 줍니다.

**왜 참고 사진을 요구하나요?**
참고 사진이 없으면 모델이 실제 대상의 세부 모습을 상상으로 채우기 때문에, 결과물이 그럴듯해 보이지만 틀립니다.

## 기여하기

이슈와 풀 리퀘스트를 환영합니다. 특히 Google이 모델, 가격, API를 바꿨을 때 도움이 됩니다. `models.json`과 `SKILL.md`, 이 README의 표는 함께 수정해 주세요.

이 번역은 AI의 도움을 받아 작성되었으며, 수정 제안을 환영합니다.

오프라인 테스트에는 API 키도 네트워크도 필요하지 않습니다(`finish.py` 테스트는 Pillow가 설치되어 있으면 실행되고, 없으면 건너뜁니다).

```bash
python -m unittest discover -s tests
```

## 라이선스

[MIT](../LICENSE)
