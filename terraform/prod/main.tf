terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.34.0"
    }
  }
}

resource "google_storage_bucket" "default" {
  name                        = "${var.environment_prefix}-${var.app_name_prefix}-storage" # Every bucket name must be globally unique
  location                    = "ASIA-NORTHEAST1"
  uniform_bucket_level_access = true
}

data "archive_file" "default" {
  type        = "zip"
  output_path = "/tmp/function-source.zip"
  source_dir  = "functions/linebot/"
}
resource "google_storage_bucket_object" "object" {
  name   = "function-source.zip"
  bucket = google_storage_bucket.default.name
  source = data.archive_file.default.output_path # Add path to the zipped function source code
}

resource "google_cloudfunctions2_function" "default" {
  name        = "${var.environment_prefix}-${var.app_name_prefix}-bot"
  location    = "asia-northeast1"
  description = ""

  build_config {
    runtime     = "python312"
    entry_point = "bot" # Set the entry point
    source {
      storage_source {
        bucket = google_storage_bucket.default.name
        object = google_storage_bucket_object.object.name
      }
    }
  }

  service_config {
    max_instance_count = 1
    available_memory   = "256M"
    timeout_seconds    = 60
  }
}

resource "google_cloudfunctions2_function" "default" {
  name        = "${var.environment_prefix}-${var.app_name_prefix}-embeddings"
  location    = "asia-northeast1"
  description = ""

  build_config {
    runtime     = "python312"
    entry_point = "embeddings" # Set the entry point
    source {
      storage_source {
        bucket = google_storage_bucket.default.name
        object = google_storage_bucket_object.object.name
      }
    }
  }

  service_config {
    max_instance_count = 1
    available_memory   = "256M"
    timeout_seconds    = 60
  }
}

resource "google_cloudfunctions2_function" "default" {
  name        = "${var.environment_prefix}-${var.app_name_prefix}-investigator"
  location    = "asia-northeast1"
  description = ""

  build_config {
    runtime     = "python312"
    entry_point = "investigator" # Set the entry point
    source {
      storage_source {
        bucket = google_storage_bucket.default.name
        object = google_storage_bucket_object.object.name
      }
    }
  }

  service_config {
    max_instance_count = 1
    available_memory   = "256M"
    timeout_seconds    = 60
  }
}

resource "google_cloud_run_service_iam_member" "member" {
  location = google_cloudfunctions2_function.default.location
  service  = google_cloudfunctions2_function.default.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

output "function_uri" {
  value = google_cloudfunctions2_function.default.service_config[0].uri
}