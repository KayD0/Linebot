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
  location = "${var.location}"
  project =  "${var.project_id}"
  uniform_bucket_level_access = true
  labels = {
    "app" = var.labels
  }
}

# zipアーカイブをストレージバケットにアップロードします
resource "google_storage_bucket_object" "bot_object" {
  name   = "bot.zip"
  bucket = google_storage_bucket.default.name
  source = "./bot.zip" # zipアーカイブのパスを指定
}

# zipアーカイブをストレージバケットにアップロードします
resource "google_storage_bucket_object" "embeddings_object" {
  name   = "embeddings.zip"
  bucket = google_storage_bucket.default.name
  source = "./embeddings.zip" # zipアーカイブのパスを指定
}

# bot用のCloud Functionを作成します
resource "google_cloudfunctions2_function" "bot" {
  name        = "${var.environment_prefix}-${var.app_name_prefix}-bot"
  location = "${var.location}"
  description = ""
  project =  "${var.project_id}"

  build_config {
    runtime     = "${var.runtime}"
    entry_point = "${var.entry_point}"
    source {
      storage_source {
        bucket = google_storage_bucket.default.name
        object = google_storage_bucket_object.bot_object.name
      }
    }
  }

  service_config {
    max_instance_count = 1
    available_memory   = "1024M"
    timeout_seconds    = 60
    environment_variables = {
      BUCKET_NAME = google_storage_bucket.default.name       
      QA_EMBEDDINGS_FILE_NAME = "${var.embeddings_file_name}"      
      LINE_CHANNEL_SECRET = "${var.line_channel_secret}"
      LINE_ACCESS_TOKEN = "${var.line_access_token}"
      OPENAI_API_KEY = "${var.openai_api_key}"
    }
  }

  labels = {
    "app" = var.labels
  }
}

# パブリックアクセスを許可するIAM設定
resource "google_cloud_run_service_iam_member" "public_access" {
  project  = var.project_id
  location = google_cloudfunctions2_function.bot.location
  service  = google_cloudfunctions2_function.bot.name
  role     = "roles/run.invoker"
  member   = "allUsers"

  depends_on = [
    google_cloudfunctions2_function.bot
  ]
}

# embeddings用のCloud Functionを作成します
resource "google_cloudfunctions2_function" "embeddings" {
  name        = "${var.environment_prefix}-${var.app_name_prefix}-embeddings"
  location    = "${var.location}"
  description = ""
  project =  "${var.project_id}"

  build_config {
    runtime     = "${var.runtime}"
    entry_point = "${var.entry_point}"
    source {
      storage_source {
        bucket = google_storage_bucket.default.name
        object = google_storage_bucket_object.embeddings_object.name
      }
    }
  }

  service_config {
    max_instance_count = 1
    available_memory   = "1024M"
    timeout_seconds    = 60
    environment_variables = {
      BUCKET_NAME = google_storage_bucket.default.name
      QA_EMBEDDINGS_FILE_NAME = "${var.embeddings_file_name}"      
      OPENAI_API_KEY = "${var.openai_api_key}"
    }
  }

  labels = {
    "app" = var.labels
  }
}