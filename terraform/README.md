# Terraform Configuration for Linebot

このフォルダには、Linebotプロジェクトのインフラストラクチャを管理するためのTerraformスクリプトが含まれています。

## 構成内容

- **main.tf**: メインのTerraform設定ファイル。リソースの定義が含まれています。
- **variables.tf**: 変数の定義ファイル。プロジェクトで使用される変数が含まれています。

## 前提条件

1. Google Cloudでプロジェクトを作成してあること
2. Google Cloudで作成したプロジェクトに必要なAPIを有効化していること
  -  以下有効化必要なAPI
    - Cloud Functions API
    - Compute Engine API
3. Google Cloud Shellで実行すること

## 使用方法

1. このリポジトリをクローンします:
    ```sh
    git clone https://github.com/KayD0/Linebot.git
    cd Linebot/terraform
    ```
2. variable.tfに変数を入力する
  - `project_id`
    - 作成したプロジェクトのプロジェクトIDを入力
  - `line_channel_secret`
    - ラインチャネルシークレットを入力
  - `line_access_token`
    - ラインアクセストークンを入力
  - `openai_api_key`
    - OpenAI APIキーを入力

3. Google Cloud Shellにアプロード
  - zipper_{app}.ps1を使ってプロジェクトをzip化する
    - src/functions/bot
    - src/functions/embeddings
  - zip化したファイルを以下に格納し、Google Cloud Shellにアップロード
    - terraform/{env}

4. Terraformを初期化します:
    ```sh
    terraform init
    ```

5. Terraformプランを作成します:
    ```sh
    terraform plan
    ```

6. Terraformを適用してインフラストラクチャを構築します:
    ```sh
    terraform apply
    ```

## 注意事項

- 実行前に設定内容を十分に確認してください。

## ライセンス

このプロジェクトはMITライセンスの下でライセンスされています。