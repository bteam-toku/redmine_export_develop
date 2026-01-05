# ベースイメージとしてPythonの公式イメージを使用
FROM python:3.13-slim

# Gitをインストール
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリを/appに設定
WORKDIR /app

# requirements.txtをコンテナにコピー
COPY requirements.txt .

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# スクリプトをコンテナにコピー
COPY ./redmine_export ./redmine_export
COPY ./redmine_export_setup ./redmine_export_setup

# コンテナ起動時のデフォルトコマンド
ENTRYPOINT ["python", "-m"]

# メタデータの追加
LABEL org.opencontainers.image.source="https://github.com/bteam-toku/redmine_export_develop.git"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.description="Redmineチケット一覧出力（Dockerコンテナ）"