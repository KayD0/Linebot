```mermaid
sequenceDiagram
    participant User
    participant LineBot
    participant OpenAI
    participant GCS as Google Cloud Storage

    User->>LineBot: メッセージ送信
    LineBot->>OpenAI: メッセージベクトル化
    OpenAI->>LineBot: ベクトル化メッセージ取得
    LineBot->>GCS: ベクトル化されたQAを参照
    LineBot->>LineBot: LlamaindexによるQAインデックス作成
    LineBot->>LineBot: LlamaindexによるQAベクトル検索
    LineBot->>User: 応答メッセージ送信
```
