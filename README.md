# 反応予測AI こうすけくん

このプロジェクトは、化学反応の予測を行うデモンストレーション用のシンプルなアプリケーションです。
フロントエンドでは SMILES 文字列を入力し、バックエンドに問い合わせて生成モデル（seq2seq + Attention）で産物を予測し、その結果を描画しています。

1. プロジェクト構成
pgsql
コピーする
編集する
Reaction_prediction_Kosuke
├─ .devcontainer
│   ├─ Dockerfile
│   ├─ devcontainer.json
│   └─ requirements.txt
├─ backend
│   ├─ api.py
│   ├─ main.py
│   ├─ model_with_embedding.h5     ← 学習済みモデル
│   ├─ predict_utils.py            ← 推論用関数
│   └─ vocab_data.pkl              ← 語彙データなど
└─ frontend
    ├─ index.html
    ├─ robot-image.png
    └─ script.js
1.1 .devcontainer フォルダ
Dockerfile
Python 3.9-slim ベースのコンテナを作るためのDockerfile。
必要に応じて追加ツール（build-essential など）をインストールしています。

devcontainer.json
VSCode の Remote Containers / Dev Containers 用設定ファイル。

requirements.txt
コンテナ内で pip install するライブラリ一覧。

makefile
コピーする
編集する
tensorflow==2.18.0
keras==3.8.0
numpy==2.0.2
fastapi
uvicorn
1.2 backend フォルダ
api.py
FastAPI でエンドポイント (/predict) を定義。
フロントエンド (index.html) から SMILES 文字列を送信すると、推論結果を返します。

main.py
スクリプトとして単体で動かす場合のサンプル。
python main.py とすると、predict_utils.py 内の関数を呼び出し、推論結果を出力します。

model_with_embedding.h5
学習済み Keras モデル (seq2seq + Attention) を保存したファイル。

predict_utils.py
学習済みモデルと語彙データを読み込み、入力 SMILES のトークン列→推論→産物 SMILES を返す。
カスタムの softmax や、ID列との変換等を行うユーティリティが含まれています。

vocab_data.pkl
学習時に使った語彙やパラメータの辞書。

arduino
コピーする
編集する
{
  "reactants_vocab": {...},
  "products_vocab": {...},
  "inv_products_vocab": {...},
  "Tx": 18,
  "Ty":  （出力の最大長）,
  "n_a": 256,
  "n_s": 512,
  "embedding_dim": 256
}
1.3 frontend フォルダ
index.html
簡易的なチャットUIと SMILES 描画用の <canvas> があるページ。
Script 内部で smiles-drawer.js (CDN) を利用して構造式を描画。
ボタンを押すと http://localhost:8000/predict にリクエストし、返ってきた産物 SMILES を再度描画します。

robot-image.png
左パネルに表示されるロボットのイメージ画像。

script.js
代わりに index.html の <script> 直書きでも構築可能ですが、分割した場合のサンプル。
SMILES 入力を分割してCanvasに表示 → APIにリクエスト → 推論結果を受け取りCanvasに表示、という流れ。

<br>
2. 実行方法
以下では VSCode 上の Dev Container で開発する想定の流れを例示します。
適宜ご自身の環境に合わせて読み替えてください。

(VSCode) Dev Container を起動

このリポジトリを開き、Remote-Containers: Open Folder in Container などで Docker コンテナ内の開発環境に入る。

(Terminal 1) フロントエンドを起動

```bash

cd /workspaces/docker-python/simple_smiles_drawer  # フォルダ名は適宜読み替え
python -m http.server 5500
```

これで http://localhost:5500/frontend/index.html にアクセスできるようになります
(ただし VSCode のポートフォワーディング設定が必要です)。

(Terminal 2) バックエンドを起動

```bash

cd /workspaces/docker-python/simple_smiles_drawer/backend
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```
FastAPI が http://localhost:8000 で起動します。

ブラウザでアクセス

ブラウザで http://localhost:5500/frontend/index.html (あるいはポートフォワーディングで割り当てたURL) を開きます。

テキストボックスに SMILES を入力して「送信」ボタンを押します。

例: C O . Cl C c 1 c n 2 c c c c c 2 n 1

入力分子AとB（「.」で区切り）を左に描画し、少し待つと右に生成結果が表示されます。

<br>
3. 学習方法
学習データ

US特許公報 (1976-Sep2016) の反応事例をペア (原料, 生成物) として抽出した CSV データを使用。

「例: input_text[反応物] -> target_text[生成物]」形式で数十万〜百万件程度を取り扱う。

学習スクリプトの例
README に示した通り、Google Colab 上で以下のように実行しました。

python
コピーする
編集する
# Google Drive へのマウント
from google.colab import drive
drive.mount('/content/drive')

# ... Colab での学習スクリプト ...
# model_with_embedding.h5 と vocab_data.pkl を /content/drive/MyDrive/nmt_model_files に保存
学習モデル

Encoder (Bi-LSTM) + Attention + Decoder (LSTM) の一般的な seq2seq。

SMILES トークンを Embedding → Bi-LSTM (Tx=18) → Decoder LSTM → Dense(出力語彙数, softmax)。

詳細は predict_utils.py など参照。

参考文献やソース

Neural Machine Translation of Organic Chemistry Reactions (2017)

GitHub: organic-chemistry-reaction-prediction-using-NMT

<br>
4. 使い方のポイント
SMILES表現
入力テキストボックスにはスペース区切りでトークン化した SMILES を想定しています。
例: C O . Cl C c 1 c n 2 c c c c c 2 n 1
「.」で分子を区切ると複数分子の反応を想定した予測ができます。

注意

学習したモデルは簡易的でデータクレンジングも限定的なので、化学的に正しい保証はありません。

あくまでデモや研究用途としてお使いください。

予測が上手く動かない場合は、SMILES のトークン化や文字列の整形を見直してください。

<br>
5. ライセンスやクレジット
このプロジェクトは学術研究・デモ用であり、いかなる化学反応の正確性や安全性を保証するものではありません。

参考にしたデータや論文、リポジトリの著作権表示に従います。

ご質問や不明点がある場合はお気軽にお問合せください。