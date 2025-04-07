FROM python:3.9-slim

# 必要に応じて追加ツールを入れる
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 1) requirements.txt をコンテナにコピー
COPY requirements.txt /app/

# 2) ライブラリをインストール
RUN pip install --no-cache-dir -r requirements.txt

CMD ["/bin/bash"]
