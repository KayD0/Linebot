# 必要なプロバイダーを指定します
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.34.0"
    }
  }
}

# 組織IDとしてランダムなIDを生成します
resource "random_id" "org_id" {
  byte_length = 16
}

# Google Cloud Storageバケットを作成します
resource "google_storage_bucket" "default" {
  name     = "${var.environment_prefix}-${var.app_name_prefix}-storage" # バケット名はグローバルに一意である必要があります
  location = "ASIA-NORTHEAST1"
  uniform_bucket_level_access = true
  labels   = var.labels
}

# zipアーカイブをストレージバケットにアップロードします
resource "google_storage_bucket_object" "object" {
  name   = "functions.zip"
  bucket = google_storage_bucket.default.name
  source = "./functions.zip" # zipアーカイブのパスを指定
}

# bot用のCloud Functionを作成します
resource "google_cloudfunctions2_function" "bot" {
  name        = "${var.environment_prefix}-${var.app_name_prefix}-bot"
  location    = "asia-northeast1"
  description = ""

  build_config {
    runtime     = "python312"
    entry_point = "bot" # エントリーポイントを設定
    source {
      storage_source {
        bucket = google_storage_bucket.default.name
        object = google_storage_bucket_object.object.name
      }
    }
    environment_variables = {
      GOOGLE_FUNCTION_SOURCE = "bot.py"
    }
  }

  service_config {
    max_instance_count = 1
    available_memory   = "512M"
    timeout_seconds    = 60
  }

  labels   = var.labels
}

# embeddings用のCloud Functionを作成します
resource "google_cloudfunctions2_function" "embeddings" {
  name        = "${var.environment_prefix}-${var.app_name_prefix}-embeddings"
  location    = "asia-northeast1"
  description = ""

  build_config {
    runtime     = "python312"
    entry_point = "embeddings" # エントリーポイントを設定
    source {
      storage_source {
        bucket = google_storage_bucket.default.name
        object = google_storage_bucket_object.object.name
      }
    }
    environment_variables = {
      GOOGLE_FUNCTION_SOURCE = "embeddings.py"
    }
  }

  service_config {
    max_instance_count = 1
    available_memory   = "256M"
    timeout_seconds    = 60
  }

  labels   = var.labels
}

# investigator用のCloud Functionを作成します
resource "google_cloudfunctions2_function" "investigator" {
  name        = "${var.environment_prefix}-${var.app_name_prefix}-investigator"
  location    = "asia-northeast1"
  description = ""

  build_config {
    runtime     = "python312"
    entry_point = "investigator" # エントリーポイントを設定
    source {
      storage_source {
        bucket = google_storage_bucket.default.name
        object = google_storage_bucket_object.object.name
      }
    }
    environment_variables = {
      GOOGLE_FUNCTION_SOURCE = "investigator.py"
    }
  }

  service_config {
    max_instance_count = 1
    available_memory   = "256M"
    timeout_seconds    = 60
  }

  labels   = var.labels
}

# IAMポリシーを設定して、Cloud Functionへの公開アクセスを許可します
# ただし、`google_cloudfunctions2_function.default` は存在しないため、正しいリソース名を指定する必要があります
resource "google_cloud_run_service_iam_member" "embeddings_member" {
  location = google_cloudfunctions2_function.embeddings.location # botのロケーションを使用
  service  = google_cloudfunctions2_function.embeddings.name # botの名前を使用
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# terraform import google_cloudfunctions2_function.bot projects/freelance-federation/locations/asia-northeast1/functions/stg-linebot-bot
# terraform import google_cloudfunctions2_function.embeddings projects/freelance-federation/locations/asia-northeast1/functions/stg-linebot-embeddings
# terraform import google_cloudfunctions2_function.investigator projects/freelance-federation/locations/asia-northeast1/functions/stg-linebot-investigator