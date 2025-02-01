```mermaid
sequenceDiagram
    participant GAS as LinebotQAEmbeddings
    participant Functions as LinebotQAEmbeddings
    participant OpenAI as OpenAI
    participant GCS as Google Cloud Storage

    GAS->>Functions: Functionsを呼び出す
    Functions->>OpenAI: データを送信
    OpenAI->>Functions: ベクトル化データを返す
    Functions->>GCS: ベクトル化したQAを登録
```
