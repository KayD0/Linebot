
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

variable "labels" {
  type = map(string)
  default = {
    environment = "stg-linebot"
    managed_by  = "terraform"
  }
}