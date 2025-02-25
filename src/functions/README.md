# Linebot

このプロジェクトは、LINEボットを利用したアプリケーションです。主にLINE Messaging APIを使用して、ユーザーからのメッセージを受け取り、適切な応答を返します。

## 概要

このプロジェクトでは、主に以下の機能を提供します:
- LINEメッセージの受信と応答
- メッセージの解析と処理
- 外部APIとの連携

## インストール方法

1. リポジトリをクローンします:
    ```sh
    git clone https://github.com/KayD0/Linebot.git
    ```
2. プロジェクトディレクトリに移動します:
    ```sh
    cd Linebot/Linebot
    ```
3. 必要な依存関係をインストールします:
    ```sh
    pip install -r requirements.txt
    ```
4. `.env`ファイルを設定します。以下のように環境変数を設定してください:
    ```env
    LINE_CHANNEL_SECRET=your_line_channel_secret
    LINE_ACCESS_TOKEN=your_line_access_token
    ```

## デプロイ方法 (GCP)

1. Google Cloud SDKをインストールし、認証します:
    ```sh
    gcloud init
    gcloud auth application-default login
    ```
2. Google Cloud Functionsをデプロイします:
    ```sh
    gcloud functions deploy linebot_handler \
    --runtime python310 \
    --trigger-http \
    --allow-unauthenticated \
    --entry-point main
    ```
3. デプロイが完了すると、関数のエンドポイントURLが表示されます。このURLをLINE Messaging APIのWebhook設定に登録してください。

## 使用方法

LINEボットがメッセージを受信すると、このプロジェクトがイベントを処理し、適切な応答を返します。メッセージの解析や外部APIとの連携などの処理は`main.py`内で行われます。

## ライセンス

このプロジェクトはMITライセンスの下でライセンスされています。
