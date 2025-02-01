# LinebotGroupIdInvestigator

`LinebotGroupIdInvestigator`は、LINEボットから受信したイベントからグループIDを取得し、ログに記録するためのPythonプロジェクトです。

## 概要

このプロジェクトは、LINE Messaging APIからのイベントを受け取り、イベントの送信元グループIDを抽出してログに記録します。グループIDが見つからない場合は、個人チャットである可能性があることを示します。

## インストール方法

1. リポジトリをクローンします:
    ```sh
    git clone https://github.com/KayD0/Linebot.git
    ```
2. プロジェクトディレクトリに移動します:
    ```sh
    cd Linebot/LinebotGroupIdInvestigator
    ```
3. 必要な依存関係をインストールします:
    ```sh
    pip install -r requirements.txt
    ```

## デプロイ方法 (GCP)

1. Google Cloud SDKをインストールし、認証します:
    ```sh
    gcloud init
    gcloud auth application-default login
    ```
2. Google Cloud Functionsをデプロイします:
    ```sh
    gcloud functions deploy investigator \
    --runtime python310 \
    --trigger-http \
    --allow-unauthenticated \
    --entry-point investigator
    ```
3. デプロイが完了すると、関数のエンドポイントURLが表示されます。このURLをLINE Messaging APIのWebhook設定に登録してください。

## 環境変数の設定

- `LINE_CHANNEL_SECRET`
- `LINE_ACCESS_TOKEN`

これらの環境変数は、Google Cloud Functionsのデプロイ時に設定するか、関数内で直接設定してください。

## 使用方法

LINEボットがメッセージを受信すると、このプロジェクトがイベントを処理し、グループIDをログに記録します。グループIDが見つからない場合は、ログにその旨が記録されます。

## ライセンス

このプロジェクトはMITライセンスの下でライセンスされています。
