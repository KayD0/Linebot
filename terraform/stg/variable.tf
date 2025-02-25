variable "environment_prefix" {
  type        = string
  description = "環境名プレフィックス"
  default     = "stg"
}

variable "app_name_prefix" {
  type        = string
  description = "アプリケーションメイプレフィックス"
  default     = "linebot"
}