<p align="center">
  <img src="../assets/logo.png" width="132" alt="nano-banana 로고: 남색 정사각형 위에 작은 가격표가 달린 노란 바나나">
</p>

<h1 align="center">nano-banana</h1>

<p align="center">
  <em>코딩 에이전트로 만드는 이미지, 비용은 손에 쥔 채로.</em>
</p>

<p align="center">
  <a href="https://github.com/jakubcurik/nano-banana/actions/workflows/tests.yml"><img alt="Tests" src="https://img.shields.io/github/actions/workflow/status/jakubcurik/nano-banana/tests.yml?branch=main&style=flat-square&label=tests&labelColor=0f1b2d"></a>
  <a href="https://github.com/jakubcurik/nano-banana/actions/workflows/validate.yml"><img alt="Validate" src="https://img.shields.io/github/actions/workflow/status/jakubcurik/nano-banana/validate.yml?branch=main&style=flat-square&label=validate&labelColor=0f1b2d"></a>
  <a href="https://github.com/jakubcurik/nano-banana/releases"><img alt="Release" src="https://img.shields.io/github/v/release/jakubcurik/nano-banana?style=flat-square&label=release&labelColor=0f1b2d&color=ffd54a"></a>
  <a href="../LICENSE"><img alt="라이선스: MIT" src="https://img.shields.io/badge/license-MIT-ffd54a?style=flat-square&labelColor=0f1b2d"></a>
  <a href="https://github.com/jakubcurik/nano-banana/stargazers"><img alt="스타" src="https://img.shields.io/github/stars/jakubcurik/nano-banana?style=flat-square&labelColor=0f1b2d&color=ffd54a"></a>
</p>

<p align="center">
  <img alt="Claude Code 플러그인" src="https://img.shields.io/badge/Claude_Code-plugin-ffd54a?style=flat-square&labelColor=0f1b2d">
  <a href="https://agentskills.io"><img alt="Agent Skills 형식" src="https://img.shields.io/badge/Agent_Skills-compatible-ffd54a?style=flat-square&labelColor=0f1b2d"></a>
  <img alt="Python 3.11 이상" src="https://img.shields.io/badge/python-3.11%2B-ffd54a?style=flat-square&labelColor=0f1b2d">
  <img alt="Gemini API" src="https://img.shields.io/badge/Gemini_API-Nano_Banana-ffd54a?style=flat-square&labelColor=0f1b2d">
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
  <img src="../assets/hero.jpg" width="880" alt="동그란 안경을 쓴 만화 속 바나나가 책상 위 작은 이젤에 풍경화를 그리고 있고, 옆에는 긴 종이 영수증과 금화 몇 개가 놓여 있습니다. 제목은 nano-banana입니다.">
</p>

nano-banana는 Claude Code를 비롯한 코딩 에이전트가 Google의 Nano Banana 모델로 이미지를 만들고 편집할 수 있게 해 주는 에이전트 스킬입니다. 이때 드는 비용도 함께 추적합니다.

에이전트에 히어로 이미지를 요청하면 이미지가 나옵니다. 그런데 "변형을 몇 개 더 시도해 줘"라고 하면, 일반 API 호출은 첫 번째 결과를 보고 있는 동안 4K 이미지를 열두 장쯤 생성해 버릴 수 있습니다. 이미지마다 요금이 청구되는데, 채팅에서는 그 금액을 알 수 없습니다.

이 스킬은 호출 전에 예상 가격을, 호출 후에 실제 비용을 출력합니다. 선택한 옵션이 해당 모델에서 지원되는지도 확인하므로, 잘못된 크기나 지원하지 않는 thinking 수준은 API에서 오류가 나는 것이 아니라 로컬에서 먼저 실패합니다. 그 밖에는 에이전트가 따를 짧은 절차를 제공합니다. 이미지를 어디에 쓸지 묻고, 대상이 실제 사물처럼 보여야 하면 참고 사진을 확보하고, 프롬프트는 영어로 작성하고, 완료라고 하기 전에 결과를 직접 확인합니다.

<sub>비공식 프로젝트입니다. Google과 제휴 관계가 아니며 Google의 승인을 받지 않았습니다. "Nano Banana"와 "Gemini"는 Google이 자사의 이미지 모델과 API에 붙인 이름입니다.</sub>

## 실행 모습

<p align="center">
  <img src="../assets/terminal.png" width="880" alt="이미지 한 장을 생성할 때의 터미널 출력: 모델, 예상 비용 0.0504 USD, 인터랙션 ID, 이미지 토큰 1680개 사용에 0.0504 USD, 저장된 파일 경로.">
</p>

실제 실행 결과입니다. 기본 모델에서 2K 이미지 한 장은 약 5센트(미국 달러 기준)이며, 호출 전과 후에 금액을 확인할 수 있습니다.

<a id="gallery"></a>

## 갤러리

텍스트와 터미널 스크린샷을 제외하면, 이 README의 이미지는 모두 이 스킬로 만들었습니다. 프롬프트는 [`assets/prompts`](../assets/prompts)에 있습니다.

<p align="center">
  <img src="../assets/gallery/1-illustration.jpg" width="760" alt="햇살이 드는 창가의 나무 카운터 위에 김이 나는 커피 잔과 크루아상이 놓인 플랫 일러스트. 오른쪽에는 제목을 넣을 빈 공간이 있습니다.">
  <br>
  <sub><b>텍스트에서 이미지로.</b> 모델 2.1, 2K, 16:9, 약 5센트.</sub>
</p>

<p align="center">
  <img src="../assets/gallery/2a-edit-before.jpg" width="372" alt="밝은 회색 스튜디오 배경 위의 평범한 흰색 도자기 머그잔.">
  <img src="../assets/gallery/2b-edit-after.jpg" width="372" alt="햇살이 드는 창가의 소박한 나무 테이블 위에 놓인 같은 흰색 머그잔과, 그 옆의 작은 커피콩 그릇.">
  <br>
  <sub><b><code>--follow-up</code>으로 편집.</b> 같은 머그잔, 새로운 장면. 모델 2.1, 2K, 이미지당 약 5센트.</sub>
</p>

<p align="center">
  <img src="../assets/gallery/3-poster-text.jpg" width="400" alt="평평한 커피 잔 위에 FRESH COFFEE라고 쓰여 있고, 그 아래에 Open daily from 8 to 18 문구가 있는 미니멀한 카페 포스터.">
  <br>
  <sub><b>이미지 속 텍스트.</b> 모델 Pro, 2K, 4:5, 약 13센트.</sub>
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
```

이미지는 `.cache/nano-banana/`에 저장되며, 각 이미지 옆에 프롬프트, 옵션, 인터랙션 ID가 담긴 `.txt` 파일이 함께 생깁니다.

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
| `--follow-up [ID]` | 마지막 결과 또는 지정한 인터랙션에서 이어서 진행 |
| `-n 4` | 이미지 수, 이미지마다 따로 과금 |
| `-o folder` | 출력 폴더 |
| `--format png / jpeg` | 출력 파일 형식 |
| `--prompt-file file` | 파일에서 프롬프트 읽기 |
| `--no-store` | Google에 인터랙션을 저장하지 않도록 요청 (이 경우 해당 인터랙션에서는 후속 편집을 할 수 없음) |
| `--batch` | 절반 가격, 최대 24시간 소요 (모델 2.1과 lite) |
| `--estimate` | 예상 가격을 출력하고 종료 |
| `--currency CZK` | 해당 통화로도 가격 표시 (환율은 체코 국립은행 기준) |

</details>

<a id="how-it-works"></a>

## 작동 방식

이 스킬은 에이전트가 정해진 순서로 일하게 합니다. 먼저 이미지를 어디에 쓸지 묻습니다. 실제 종, 제품, 장소를 보여 줘야 한다면 참고 사진 두세 장을 구하고 사용자에게 확인을 받습니다. 그다음 영어로 프롬프트를 쓰고 가격을 추정하며, 약 0.50달러를 넘거나 이미지가 네 장보다 많으면 먼저 사용자에게 묻습니다. 생성한 뒤에는 결과를 살펴보고, 사소한 수정은 처음부터 다시 만들지 않고 후속 편집으로 처리합니다.

전체 워크플로는 [`SKILL.md`](../skills/nano-banana/SKILL.md)에 있습니다. 프롬프트 템플릿, 편집 템플릿, 흔한 실수 목록은 [`references/prompting.md`](../skills/nano-banana/references/prompting.md)에 있습니다.

<a id="models-and-prices"></a>

## 모델과 가격

2026년 11월 26일 기준, 이미지당 USD입니다.

| 모델 | 적합한 용도 | 1K | 2K | 4K |
|---|---|---|---|---|
| `2.1` (`gemini-nano-banana-2.1`) | 거의 모든 작업 | 0.034 | 0.050 | 0.113 |
| `2` (`gemini-3.1-flash-image`) | 512 px. Google이 지원 중단 예정으로 표시했으며, 종료일은 아직 없음 | 0.067 | 0.101 | 0.151 |
| `pro` (`gemini-3-pro-image`) | 가장 까다로운 프롬프트, 텍스트가 많은 이미지 | 0.134 | 0.134 | 0.240 |
| `lite` (`gemini-3.1-flash-lite-image`) | 단순한 이미지를 많이 만들 때, 1K만 지원, 검색 없음 | 0.034 | n/a | n/a |

가격과 모델 데이터는 [`models.json`](../skills/nano-banana/scripts/models.json)에 있습니다. Google이 [가격표](https://ai.google.dev/gemini-api/docs/pricing)를 바꿀 때 수정할 파일은 이것 하나입니다. `--search`는 별도로 과금됩니다. 그라운딩 프롬프트 월 5,000건은 무료이고, 그 이후에는 검색 쿼리 1,000건당 14 USD입니다.

## 알아두면 좋은 점

- Google은 후속 편집이 가능하도록 인터랙션을 저장합니다. 유료 프로젝트는 55일, 무료 등급은 1일입니다. 민감한 사진에는 `--no-store`를 사용하세요.
- 생성된 모든 이미지에는 눈에 보이지 않는 SynthID 워터마크가 들어갑니다.
- 모델은 세부 묘사를 지어냅니다. 이미지가 실제 종, 제품, 건물과 일치해야 하면 `-i`로 참고 사진 2-3장을 함께 주세요. 스킬의 워크플로도 이를 필수로 요구합니다.
- 타임아웃된 요청도 이미 과금되었을 수 있으므로, 스크립트는 스스로 재시도하지 않습니다.
- `--search`로 만든 결과물을 공개하는 경우 Google은 검색 제안을 표시하도록 요구합니다. 스크립트는 이를 이미지 옆에 저장합니다.

<a id="faq"></a>

## 자주 묻는 질문

**Google에는 자체 `gemini-api` CLI가 있습니다. 왜 이걸 써야 하나요?**
CLI는 호출을 수행하고, 그 일을 잘 해냅니다. 이 스킬은 호출을 둘러싼 부분을 더해 줍니다. 둘 다 필요할 수 있습니다.

| | Google `gemini-api` CLI와 스킬 | nano-banana |
|---|---|---|
| 호출 전 가격 추정, 호출 후 실제 비용 | 아니요 | 예 |
| 비용이 큰 실행 전에 에이전트가 먼저 확인 | 아니요 | 예 |
| 모델에 맞는지 옵션 검사 | 아니요, API가 거부함 | 예 |
| ID를 복사하지 않는 후속 편집 | 수동 | `--follow-up` |
| 이미지마다 프롬프트와 옵션을 옆에 저장 | 아니요 | 예 |
| 프롬프트 작성 가이드와 템플릿 | 아니요 | 예 |

CLI는 빠르게 변하는 베타 버전이므로, 선택하기 전에 둘 다 확인해 보세요.

**Claude Code 밖에서도 작동하나요?**
이 스킬은 공개 [Agent Skills](https://agentskills.io) 형식을 따르므로, `SKILL.md` 파일을 불러오는 다른 에이전트에서도 사용할 수 있습니다. 다만 Claude Code에서만 테스트했습니다.

**가격이 바뀌었습니다. 무엇을 수정해야 하나요?**
`skills/nano-banana/scripts/models.json`과, `SKILL.md` 및 이 문서의 표를 수정하세요.

**왜 참고 사진을 요구하나요?**
참고 사진이 없으면 모델이 실제 대상의 세부 모습을 상상으로 채우기 때문에, 결과물이 그럴듯해 보이지만 틀립니다.

## 기여하기

이슈와 풀 리퀘스트를 환영합니다. 특히 Google이 모델, 가격, API를 바꿨을 때 도움이 됩니다. `models.json`과 `SKILL.md`, 이 README의 표는 함께 수정해 주세요.

이 번역은 AI의 도움을 받아 작성되었으며, 수정 제안을 환영합니다.

오프라인 테스트에는 API 키도 네트워크도 필요하지 않습니다.

```bash
python -m unittest discover -s tests
```

## 라이선스

[MIT](../LICENSE)

## 스타 기록

<a href="https://www.star-history.com/jakubcurik/nano-banana#history">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=jakubcurik/nano-banana&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=jakubcurik/nano-banana&type=Date" />
    <img alt="스타 기록 차트" src="https://api.star-history.com/chart?repos=jakubcurik/nano-banana&type=Date" />
  </picture>
</a>
