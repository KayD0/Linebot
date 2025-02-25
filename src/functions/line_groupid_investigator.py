import functions_framework

@functions_framework.http
def investigator(request):
    # グループIDを取得
    line_event = request.json['events'][0]
    group_id = line_event.get('source', {}).get('groupId')
    if group_id:
        print(f"メッセージ送信元のグループID: {group_id}")
    else:
        print("グループIDが見つかりません。個人チャットの可能性があります。")