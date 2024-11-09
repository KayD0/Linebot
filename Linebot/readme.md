# Lambda API テンプレート

これはRESTAPIを構築するためのテンプレートです。AWSECRにコンテナをデプロイし、それを使用してAWS Lambdaをセットアップし、RESTAPIを作成することが含まれます。

## 目次

- [概要](#概要)
- [セットアップ](#セットアップ)
- [ローカルテスト](#ローカルテスト)
- [デプロイメント](#デプロイメント)
- [起動](#起動)
- [ライセンス](#ライセンス)
- [作者](#作者)

## 概要

このテンプレートは、AWS Lambdaを使用してRESTAPIを構築するための基本的なセットアップを提供します。コンテナ化されたアプリケーションをAWS ECR（Elastic Container Registry）にデプロイし、それをAWS Lambdaで使用することで、スケーラブルなRESTAPIを簡単に構築できます。

## セットアップ

1. **RIEのダウンロード**
    ```bash
    curl -Lo aws-lambda-rie https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie
    ```

    ```bash
    chmod +x aws-lambda-rie
    ```

2. **requirements.txtの更新**

   （必要に応じて）"requirements.txt"にPythonライブラリを追加してください。

3. **イメージのビルド**
    ```bash
    docker build -t lambda-api .
    ```

## ローカルテスト

1. **コンテナの実行**
    ```bash
    docker run --rm -p 8000:8080 lambda-api:latest
    ```

   その後、`localhost:8000/2015-03-31/functions/function/invocations`にPOSTリクエストが可能になります。
   （テンプレートのリクエストボディは"{}"です。）

## デプロイメント

1. **環境変数の設定**
    ```bash
    REGION="ap-northeast-1"
    ACCOUNT_ID=$(aws sts get-caller-identity --output text --query Account)
    ECR_REPO_NAME="lambda-api"
    ```

2. **ログイン**
    ```bash
    aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com
    ```

3. **ECRリポジトリの作成（初回のみ）**

   このコマンドは初回のみ実行してください。
    ```bash
    aws ecr create-repository --repository-name $ECR_REPO_NAME
    ```

4. **Dockerタグの追加**
    ```bash
    docker tag lambda-api:latest ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${ECR_REPO_NAME}:latest
    ```

5. **イメージのプッシュ**
    ```bash
    docker push ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${ECR_REPO_NAME}:latest
    ```

## 起動（GUI）

1. **Lambdaの作成（初回のみ）**

   デプロイされたイメージに基づいて、GUIから新しいAWS Lambdaを作成します。

2. **API Gatewayへの接続（初回のみ）**

   GUIから、Lambdaに接続する新しいAWS API Gatewayを作成します。

   [AWS API Gateway ドキュメント](https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway.html)