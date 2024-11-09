import json

def handler(event, context):
    # リクエストボディを解析
    try:
        body = json.loads(event['body'])
        line_event = body['events'][0]
    except (KeyError, json.JSONDecodeError, IndexError):
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid request body')
        }

    # グループIDを取得
    group_id = line_event.get('source', {}).get('groupId')
    if group_id:
        print(f"メッセージ送信元のグループID: {group_id}")
    else:
        print("グループIDが見つかりません。個人チャットの可能性があります。")

    # レスポンスを返す
    return {
        'statusCode': 200,
        'body': json.dumps('OK')
    }