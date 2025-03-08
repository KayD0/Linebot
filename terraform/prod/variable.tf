variable "environment_prefix" {
  type        = string
  description = "環境名プレフィックス"
  default     = "prod"
}

variable "app_name_prefix" {
  type        = string
  description = "アプリケーションメイプレフィックス"
  default     = "linebot"
}

variable "labels" {
  type        = string
  description = "ラベル"
  default     = "stg-linebot"
}

variable "project_id" {
  type        = string
  description = "プロジェクトID"
  default     = "freelance-federation"
}

variable "location" {
  type        = string
  description = "リージョン"
  default     = "asia-northeast1"
}

variable "runtime" {
  type        = string
  description = "ランタイム"
  default     = "python312"
}

variable "entry_point" {
  type        = string
  description = "エントリーポイント"
  default     = "run"
}