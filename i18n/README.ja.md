<p align="center">
  <img src="../assets/logo.png" width="132" alt="nano-banana のロゴ：ダークグラファイト色の正方形の上で手を振る、つやのある黄色いバナナのキャラクター">
</p>

<h1 align="center">nano-banana</h1>

<p align="center">
  <em>コーディングエージェントから画像を生成。請求額は把握したままで。</em>
</p>

<p align="center">
  <a href="https://github.com/jakubcurik/nano-banana/actions/workflows/tests.yml"><img alt="テスト" src="https://github.com/jakubcurik/nano-banana/actions/workflows/tests.yml/badge.svg?branch=main"></a>
  <a href="https://github.com/jakubcurik/nano-banana/actions/workflows/validate.yml"><img alt="検証" src="https://github.com/jakubcurik/nano-banana/actions/workflows/validate.yml/badge.svg?branch=main"></a>
  <a href="https://github.com/jakubcurik/nano-banana/releases"><img alt="リリース" src="../assets/badges/release.svg"></a>
  <a href="../LICENSE"><img alt="ライセンス: MIT" src="../assets/badges/license-mit.svg"></a>
  <a href="https://github.com/jakubcurik/nano-banana/stargazers"><img alt="スター" src="../assets/badges/stars.svg"></a>
</p>

<p align="center">
  <img alt="Claude Code プラグイン" src="../assets/badges/claude-code-plugin.svg">
  <a href="https://agentskills.io"><img alt="Agent Skills 形式" src="../assets/badges/agent-skills.svg"></a>
  <img alt="Python 3.11 以上" src="../assets/badges/python.svg">
  <img alt="Gemini API" src="../assets/badges/gemini-api.svg">
</p>

<p align="center">
  <a href="#install">インストール</a> &middot;
  <a href="#quick-start">クイックスタート</a> &middot;
  <a href="#gallery">ギャラリー</a> &middot;
  <a href="#how-it-works">仕組み</a> &middot;
  <a href="#models-and-prices">モデルと料金</a> &middot;
  <a href="#faq">よくある質問</a>
</p>

<p align="center">
  <sub><a href="../README.md">English</a> &middot;
  <a href="README.zh-CN.md">简体中文</a> &middot;
  <a href="README.es.md">Español</a> &middot;
  日本語 &middot;
  <a href="README.pt-BR.md">Português (Brasil)</a> &middot;
  <a href="README.de.md">Deutsch</a> &middot;
  <a href="README.fr.md">Français</a> &middot;
  <a href="README.ko.md">한국어</a> &middot;
  <a href="README.cs.md">Čeština</a></sub>
</p>

<p align="center">
  <img src="../assets/hero.jpg" width="880" alt="つやのある3Dバナナのキャラクターが小さなイーゼルに日差しの風景を描いていて、その横に長い紙のレシートと数枚の金貨があります。タイトルは nano-banana です。">
</p>

nano-banana は、Claude Code などのコーディングエージェントが Google の Nano Banana モデルで画像を作成・編集できるようにするエージェントスキルです。かかった費用も記録します。

エージェントにヒーロー画像を頼めば、1枚作ってくれます。ただ「バリエーションをもう少し試して」と頼むと、素の API 呼び出しでは、最初の1枚をまだ眺めているうちに 4K の生成が12回ほど走ることがあります。画像は1枚ごとに課金されますが、チャットのどこにも金額は表示されません。

このスキルは、呼び出しの前に見積もり価格を、呼び出しの後に thinking と入力のトークンを含めた実際の費用を表示します。見積もりが上限（別の値を設定しない限り 0.50 USD）を超える実行は、何も送信しないうちに止まります。指定したオプションが選んだモデルで使えるかも事前にチェックするので、サイズの間違いや未対応の thinking レベルは、API ではなく手元のマシン上で失敗します。それ以外の部分では、エージェントに短い手順を与えます。画像の用途を把握する、被写体が実在のものに似ている必要があるときは参考写真を集める、プロンプトは英語で書く、結果を確認してから完了とする、という流れです。

<sub>非公式です。Google とは無関係で、Google による承認も受けていません。「Nano Banana」と「Gemini」は、Google が画像モデルと API につけている名称です。</sub>

## 動作例

<p align="center">
  <img src="../assets/terminal.png" width="880" alt="1回の生成のターミナル出力: モデル名、見積もり費用 0.0504 USD、インタラクション ID、画像トークン 1680 個の使用量で 0.0504 USD、保存されたファイルのパス。">
</p>

これはバージョン 1.0 での実際の実行結果です。デフォルトのモデルで 2K の画像を作ると、約5米セントかかります。その金額が呼び出しの前にも後にも表示されます。1.1 からは、呼び出し後の費用に thinking と入力のトークンも含まれるため見積もりより少し高くなり、呼び出しにかかった時間も表示されます。

<a id="gallery"></a>

## ギャラリー

テキストとターミナルのスクリーンショットを除き、このREADMEの画像はすべてこのスキルで作成しました。画像に写っている人物、場所、物はすべてAIが生成したものです。プロンプトは [`assets/prompts`](../assets/prompts) にあります。

<p align="center">
  <img src="../assets/gallery/photo-gallery-wall.jpg" width="266" alt="白いギャラリーの壁に銀色のダクトテープで貼られた1本のバナナを、スマホで撮った写真です。隣には何も書かれていない白いカードがあり、ピントの合っていない背景で来場者2人が真剣に眺めています。">
  <img src="../assets/gallery/photo-shopping-cart.jpg" width="266" alt="赤いシートベルトで、スーパーのショッピングカートの子ども用シートに固定されたバナナをスマホで撮った写真です。">
  <img src="../assets/gallery/photo-car-seat.jpg" width="266" alt="運転席からスマホで撮った写真です。助手席にバナナがまっすぐ座り、シートベルトが締められています。">
  <br>
  <sub><b>スマホで撮ったような写真。</b>ギャラリーの壁にテープで貼られたバナナ、ショッピングカートにベルトで固定されたバナナ、車のシートにシートベルトで固定されたバナナです。Model 2.1、2K、3:4、1枚あたり約5セント。</sub>
</p>

<p align="center">
  <img src="../assets/gallery/edit-before-night-flash.jpg" width="372" alt="夜、ショップのウィンドウの前を歩く女性が、カメラの強いフラッシュに照らされています。半分皮をむいたバナナを持ち、左を向いています。">
  <img src="../assets/gallery/edit-after-sunny-day.jpg" width="372" alt="青空の下、午後の明るい日差しで撮った同じ写真です。同じ女性、同じポーズ、同じバナナ、同じショップのウィンドウです。">
  <br>
  <sub><b><code>--image</code> での編集。</b>夜にフラッシュで撮った写真を、晴れた日の午後の写真に変えました。光以外はすべて同じままです。Model 2.1、1K、約3セント。</sub>
</p>

<p align="center">
  <img src="../assets/gallery/graphic-infographic.jpg" width="760" alt="「Anatomy of a banana」というタイトルのインフォグラフィックです。暗い背景に光沢のあるバナナがあり、4つのラベルが Stem、Peel、Fruit、Tip を指しています。">
  <br>
  <img src="../assets/gallery/graphic-poster.jpg" width="300" alt="BANANA ISLAND と Visit the sunny side の文字が入ったレトロな旅行ポスターです。バナナの形をした島、ヤシの木、夕日の中のヨットが描かれています。">
  <img src="../assets/gallery/graphic-vector.jpg" width="375" alt="黄色とアンバーの幾何学的な図形で作ったバナナのフラットなベクターイラストです。背景は柔らかいティールです。">
  <br>
  <sub><b>グラフィック。</b>インフォグラフィックとテキストポスターは Model Pro（2K、1枚あたり約13セント）、フラットなベクターイラストは Model 2.1（2K、約5セント）で作りました。</sub>
</p>

<p align="center">
  <img src="../assets/gallery/mascot-hammock.jpg" width="372" alt="サングラスをかけた光沢のある3Dバナナのマスコットが、熱帯のビーチで2本のヤシの木の間のハンモックでくつろいでいます。">
  <img src="../assets/gallery/mascot-surf.jpg" width="372" alt="光沢のある3Dバナナのマスコットが、ターコイズ色の波の上で小さなサーフボードに乗っています。バランスを取るために両腕を広げています。">
  <br>
  <sub><b>同じマスコットで新しいシーン。</b><code>--follow-up</code> を使いました。Model 2.1、1K、1枚あたり約3セント。</sub>
</p>

<a id="install"></a>

## インストール

Claude Code の場合は、プラグインマーケットプレイスから入れます。

```
/plugin marketplace add jakubcurik/nano-banana
/plugin install nano-banana@nano-banana
```

`SKILL.md` 形式のスキルを読めるエージェントなら、[`npx skills`](https://github.com/vercel-labs/skills) で入れられます。

```bash
npx skills add jakubcurik/nano-banana
```

手動でもかまいません。`skills/nano-banana/` を、お使いのエージェントのスキルフォルダにコピーしてください。たとえば Claude Code なら `~/.claude/skills/`、Codex、Gemini CLI、Cursor なら `~/.agents/skills/` です。

そのほかに必要なものは次のとおりです。

- [`uv`](https://docs.astral.sh/uv/)。`google-genai` と Python 3.11 以上を自動で取得してくれます。使わない場合は、Python 3.11 以上を入れて `pip install "google-genai>=3.6,<4"` を実行してください。
- [Google AI Studio](https://aistudio.google.com/apikey) の Gemini API キー。課金を有効にしておく必要があります。画像モデルに無料枠はありません。

キーは環境変数でスクリプトに渡すか、リポジトリの外に一度だけ保存します。

```bash
export GEMINI_API_KEY="your-key"
# or
mkdir -p ~/.config/nano-banana && printf '%s' "your-key" > ~/.config/nano-banana/api-key
```

<a id="quick-start"></a>

## クイックスタート

エージェントにこう頼んでみてください。「コーヒーショップのサイト用にヒーロー画像を作って、16:9で」「この写真から車を消して」「この2枚の写真を合成して」。スキルは自動で起動します。画像の用途を尋ね、プロンプトを書き、金額が無視できない場合は価格を伝え、スクリプトを実行して結果を確認します。

スクリプトを自分で呼び出すこともできます。

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

画像は `.cache/nano-banana/` に保存され、それぞれの隣に、プロンプト、オプション、インタラクション ID、呼び出しの所要時間と費用を記した `.txt` ファイルが置かれます。このフォルダには専用の `.gitignore` が作られるので、中身が git に入ることはありません。

バッチジョブは最大8分（`--wait`）待ち、その後スクリプトは終了して結果の受け取り方を表示します。`--batch-result` はジョブが完了していれば画像を保存します。もう一度実行してもファイルは重複しません。

<details>
<summary>すべてのオプション</summary>

| オプション | 意味 |
|---|---|
| `-m 2.1 / 2 / pro / lite` | モデル。デフォルトは `2.1` |
| `-s 512 / 1K / 2K / 4K` | 解像度。デフォルトは `1K`（512 はモデル `2` のみ） |
| `-a 16:9` | アスペクト比: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9。2.1 と 2 では 1:4, 4:1, 1:8, 8:1 も使えます |
| `-i photo.jpg` | 編集用、または参考用の入力画像。複数指定でき、最大14枚 |
| `-t minimal / medium / high` | thinking レベル。モデルによって異なります |
| `--search` | Google 検索によるグラウンディング（画像検索を含む）。`lite` では使えません |
| `--follow-up [IMAGE or ID]` | 直前の結果、選んだ画像（ID はその `.txt` にあります）、または指定したインタラクションから続ける |
| `-n 4` | 画像の枚数。1枚ごとに課金されます |
| `-o folder` | 出力フォルダ |
| `--name hero` | プロンプトの冒頭の代わりに使うファイル名 |
| `--format png / jpeg` | 出力ファイルの形式 |
| `--prompt-file file` | ファイルからプロンプトを読み込む |
| `--no-store` | インタラクションを保存しないよう Google に依頼する（そのインタラクションには続きの編集ができなくなります） |
| `--delete IMAGE or ID` | Google に保存されたインタラクションを削除する |
| `--batch` | 半額、最大24時間（モデル 2.1 と lite） |
| `--wait 8` | 終了する前にバッチジョブを待つ分数。`0` は送信だけして終了 |
| `--batch-result [JOB]` | バッチジョブの結果を受け取る。デフォルトは出力フォルダに最後に送信したジョブ |
| `--estimate` | 見積もり価格を表示して終了する |
| `--max-cost 0.50` | 見積もりがこの USD を超えるときは呼び出し前に止める |
| `--currency CZK` | この通貨でも価格を表示する（レートはチェコ国立銀行のもの） |

`--currency` と `--max-cost` は、`NANO_BANANA_CURRENCY` と `NANO_BANANA_MAX_COST`、または `~/.config/nano-banana/config.json`（`{"currency": "EUR", "max_cost": 1}`）からも指定できます。優先順位はコマンドライン、環境変数、ファイルの順です。

`finish.py` は `--size WxH`（埋めるように拡大縮小して切り抜き、`--keep` で残す部分を選ぶ）、`--format webp / avif / jpeg / png`、`--quality`、`--transparent [COLOR]` に対応しています。

</details>

<a id="how-it-works"></a>

## 仕組み

このスキルは、エージェントを決まった順序で動かします。まず、依頼内容とプロジェクトから画像の用途を読み取り、足りない点だけを尋ねます。実在する種、製品、場所を描く必要がある場合は、参考写真を2〜3枚用意し、あなたに確認してもらいます。次に英語でプロンプトを書いて料金を見積もります。0.50 USD を超える場合はスクリプト自体が実行を拒否し、エージェントはあなたが同意したときだけ上限を引き上げます。5枚以上生成する場合も先に確認します。生成後は結果を確認し、細かい修正はやり直さずに follow-up で行い、掲載するページに合わせて画像を切り抜いたり変換したりもできます。

ワークフロー全体は [`SKILL.md`](../skills/nano-banana/SKILL.md) にあります。プロンプトのテンプレート、編集用テンプレート、よくある間違いの一覧は [`references/prompting.md`](../skills/nano-banana/references/prompting.md) にあります。

<a id="models-and-prices"></a>

## モデルと料金

2026年11月28日時点、1枚あたりの USD です。thinking と入力のトークンは別途かかりますが、通常は1枚あたり1セント未満です。

| モデル | 向いている用途 | 1K | 2K | 4K |
|---|---|---|---|---|
| `2.1` (`gemini-nano-banana-2.1`) | ほぼすべて | 0.034 | 0.050 | 0.113 |
| `2` (`gemini-3.1-flash-image`) | 512 px。Google が非推奨にしているが、終了日は未定 | 0.067 | 0.101 | 0.151 |
| `pro` (`gemini-3-pro-image`) | 難しいプロンプト、文字が多いもの | 0.134 | 0.134 | 0.240 |
| `lite` (`gemini-3.1-flash-lite-image`) | 単純な画像を大量に。1K のみ、検索なし | 0.034 | n/a | n/a |

料金とモデルのデータは [`models.json`](../skills/nano-banana/scripts/models.json) にあります。Google が[料金表](https://ai.google.dev/gemini-api/docs/pricing)を変えたとき、スクリプトが料金を読むのはこのファイルだけです。ここや `SKILL.md` の表と食い違うとテストが失敗します。`--search` は別途課金されます。グラウンディング付きのプロンプトは月5,000件まで無料で、それを超えると検索クエリ1,000件あたり14 USD です。

## 知っておくと便利なこと

- 続きの編集ができるように、Google はインタラクションを保存しています。保存期間は、有料プロジェクトで55日、無料枠で1日です。センシティブな写真には `--no-store` を使うか、後から `--delete` で削除してください。
- 生成された画像にはすべて、目に見えない SynthID の透かしが入ります。
- モデルは細部を勝手に作り出します。実在の種、製品、建物に合わせた画像が必要なときは、`-i` で参考写真を2〜3枚渡してください。このスキルのワークフローでも、それを必須にしています。
- エラーの後、スクリプトは再試行しても安全かどうかを表示します。拒否されたリクエスト（4xx。オプションの誤り、キーの不足、クォータなど）は課金されていません。サーバーエラーやタイムアウトは課金されている可能性があるため、スクリプトは自動で再試行しません。
- 1回の生成にはおおよそ10〜30秒かかります。シェル呼び出しがタイムアウトしたエージェントは、支払い済みの画像を失います。そのためスキルは、十分な時間を確保するか、長いジョブはバックグラウンドで実行するよう指示します。
- `finish.py --transparent` は単色の背景を1色だけ取り除きます。柔らかい影やグラデーションは残り、モデル自体が透過画像を出力するかは未検証です。無地の背景を指定して、輪郭を確認してください。
- `--search` で作った出力を公開する場合、Google は検索候補の表示を義務づけています。スクリプトは、それを画像の隣に保存します。

<a id="faq"></a>

## よくある質問

**Google には独自の `gemini-api` CLI があります。なぜこれを使うのですか？**
CLI は API 呼び出しを行い、その点はしっかりこなします。このスキルが加えるのは、呼び出しの周りのことです。両方使いたくなるかもしれません。

| | Google の `gemini-api` CLI とスキル | nano-banana |
|---|---|---|
| 事前の価格見積もり、事後の実費 | なし | あり |
| 上限を上げるまで高額な実行は止まる | なし | あり（`--max-cost`） |
| 失敗した呼び出しが課金された可能性を示す | なし | あり |
| オプションをモデルに照らして検証 | なし（API が拒否する） | あり |
| ID をコピーせずに続きの編集 | 手動 | `--follow-up` |
| 各画像の隣にプロンプトとオプションを保存 | なし | あり |
| バッチの結果を後の実行で受け取れる | なし | `--batch-result` |
| Web 用の切り抜き、変換、背景の透過 | なし | `finish.py` |
| プロンプトのガイドとテンプレート | なし | あり |

CLI はベータ版で変化が速いので、選ぶ前に両方を確認してください。

**Claude Code 以外でも動きますか？**
このスキルはオープンな [Agent Skills](https://agentskills.io) 形式に従っているので、`SKILL.md` ファイルを読み込むほかのエージェントでも使えます。ただし、動作を確認したのは Claude Code だけです。

**料金が変わりました。何を編集すればいいですか？**
`skills/nano-banana/scripts/models.json` と、`SKILL.md`、この README、各翻訳の表です。どれかを更新し忘れるとテストが教えてくれます。

**なぜ参考写真を求めてくるのですか？**
参考写真がないと、モデルは実在するものの細部を想像で埋めてしまい、もっともらしいのに間違った結果になります。

## コントリビュート

Issue と Pull Request を歓迎します。特に、Google がモデル、料金、API を変更したときはお願いします。`models.json`、`SKILL.md` の表、この README は、まとめて更新してください。

この日本語訳は AI の助けを借りて作成しました。誤りがあれば、修正をお待ちしています。

オフラインテストには、API キーもネットワークも必要ありません（`finish.py` のテストは Pillow がインストールされていれば実行され、なければスキップされます）。

```bash
python -m unittest discover -s tests
```

## ライセンス

[MIT](../LICENSE)
