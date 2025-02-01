# LineAutobotEmbeddings

このプロジェクトは、受信元がLINEボットだけではなく、他のデータソースから受信したQAデータをOpenAIのAPIを使用して埋め込みベクトルに変換し、Google Cloud Storageに保存するためのPythonアプリケーションです。

## 概要

このプロジェクトは、以下の主要な機能を提供します:
- 受信したQAデータの解析（LINE Messaging APIや他のデータソースから）
- OpenAIのAPIを使用して埋め込みベクトルを生成
- 生成した埋め込みベクトルをGoogle Cloud Storageに保存

## インストール方法

1. リポジトリをクローンします:
    ```sh
    git clone https://github.com/KayD0/Linebot.git
    ```
2. プロジェクトディレクトリに移動します:
    ```sh
    cd Linebot/LineAutobotEmbeddings
    ```
3. 必要な依存関係をインストールします:
    ```sh
    pip install -r requirements.txt
    ```
4. `.env`ファイルを設定します。以下のように環境変数を設定してください:
    ```env
    QA_EMBEDDINGS_FILE_NAME=your_embeddings_file_name
    BUCKET_NAME=your_bucket_name
    ```

## デプロイ方法 (GCP)

1. Google Cloud SDKをインストールし、認証します:
    ```sh
    gcloud init
    gcloud auth application-default login
    ```
2. Google Cloud Functionsをデプロイします:
    ```sh
    gcloud functions deploy embeddings \
    --runtime python310 \
    --trigger-http \
    --allow-unauthenticated \
    --entry-point embeddings
    ```
3. デプロイが完了すると、関数のエンドポイントURLが表示されます。このURLをLINE Messaging APIのWebhook設定に登録してください。

## 使用方法

メッセージが受信されると、このプロジェクトがイベントを処理し、QAデータを埋め込みベクトルに変換してGoogle Cloud Storageに保存します。受信元はLINEボットだけではなく、他のデータソースもサポートしています。

## 解析するJSONフォーマット

プロジェクトが受け入れるJSONフォーマットは以下の通りです:
```json
{
    "qaData": [
        {
            "question": "質問のテキスト",
            "answer": "回答のテキスト"
        },
        ...
    ]
}
