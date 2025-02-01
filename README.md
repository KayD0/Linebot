# Linebot

このリポジトリには、ユーザーのクエリに対してインテリジェントな応答を提供するLineボットが含まれています。

## 機能

- **埋め込み生成**: OpenAiServiceを使用して埋め込みを生成し、Google Cloud Storageに保存します。
- **クエリ応答**: ユーザーのクエリを処理し、LlamaServiceを使用して保存された埋め込みを利用して最適な回答を見つけます。

## インストール

1. リポジトリをクローンします:
    ```sh
    git clone https://github.com/KayD0/Linebot.git
    ```
2. プロジェクトディレクトリに移動します:
    ```sh
    cd Linebot
    ```
3. 必要な依存関係をインストールします:
    ```sh
    pip install -r requirements.txt
    ```

## 使い方

1. 環境変数を設定します:
    - `LINE_CHANNEL_SECRET`
    - `LINE_ACCESS_TOKEN`
    - `BUCKET_NAME`
    - `QA_EMBEDDINGS_FILE_NAME`

2. 関数をデプロイします:
    Functions Frameworkのデプロイ手順に従ってください。

## コントリビューション

コントリビューションは歓迎します！イシューを作成するか、プルリクエストを送信してください。

## ライセンス

このプロジェクトはMITライセンスの下でライセンスされています。
