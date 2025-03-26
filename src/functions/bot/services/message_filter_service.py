class MessageFilterService:
    def __init__(self):
        # フィルタリングしたいキーワードを配列で定義
        self.keywords = [
            "年金保険料計算"
            ,"活用方法概要"
            ,"初回"
            ,"フリーランス連盟への加入を検討中"
            ,"協業代理店パートナーになりたい"
            ,"フリーランス連盟とは？"
            ,"詳しく聞きたい！無料説明会の予約"
            ,"連盟の活用方法"
        ]

    def validate(self, message):
        # メッセージ内にキーワードが含まれているかチェック
        for keyword in self.keywords:
            if keyword in message:
                return False  # キーワードが見つかった場合はFalseを返す
        return True  # キーワードが見つからなかった場合はTrueを返す