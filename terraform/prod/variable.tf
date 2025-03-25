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
  default     = "prod-linebot"
}

variable "project_id" {
  type        = string
  description = "プロジェクトID"
  default     = "prod-{作成したプロジェクトのプロジェクトIDを入力}"
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

variable "embeddings_file_name" {
  type        = string
  description = "ベクトル化QAファイル名"
  default     = "qaemb.json"
}

variable "line_channel_secret" {
  type        = string
  description = "LINE_CHANNEL_SECRET"
  default     = "{ラインチャネルシークレットを入力}"
}

variable "line_access_token" {
  type        = string
  description = "LINE_ACCESS_TOKEN"
  default     = "{ラインアクセストークンを入力}"
}

variable "openai_api_key" {
  type        = string
  description = "OPENAI_API_KEY"
  default     = "{OpenAI APIキーを入力}"
}