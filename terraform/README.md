# Terraform Configuration for Linebot

このフォルダには、Linebotプロジェクトのインフラストラクチャを管理するためのTerraformスクリプトが含まれています。

## 構成内容

- **main.tf**: メインのTerraform設定ファイル。リソースの定義が含まれています。
- **variables.tf**: 変数の定義ファイル。プロジェクトで使用される変数が含まれています。
- **outputs.tf**: 出力値の定義ファイル。適用後に出力される値が含まれています。

## 前提条件

1. Terraformがインストールされていること。
2. 必要なクラウドプロバイダーの認証情報が設定されていること。

## 使用方法

1. このリポジトリをクローンします:
    ```sh
    git clone https://github.com/KayD0/Linebot.git
    cd Linebot/terraform
    ```

2. Terraformを初期化します:
    ```sh
    terraform init
    ```

3. 変数ファイルを作成し、必要な値を設定します。例:
    ```sh
    cp terraform.tfvars.example terraform.tfvars
    vi terraform.tfvars
    ```

4. Terraformプランを作成します:
    ```sh
    terraform plan
    ```

5. Terraformを適用してインフラストラクチャを構築します:
    ```sh
    terraform apply
    ```

## 注意事項

- 事前にクラウドプロバイダーの認証情報を設定しておく必要があります。
- 実行前に設定内容を十分に確認してください。

## ライセンス

このプロジェクトはMITライセンスの下でライセンスされています。