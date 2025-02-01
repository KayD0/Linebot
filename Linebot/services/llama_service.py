from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, PromptTemplate
from llama_index.core.vector_stores import SimpleVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.schema import Document

class LlamaService:
    def __init__(self):
        self.embed_model = OpenAIEmbedding()
        self.vector_store = SimpleVectorStore(stores_text=True)
        self.index = None
        # 会社のQAボット用のプロンプトテンプレートを定義
        self.qa_template = PromptTemplate(
            """
            以下は弊社に関する情報です：\n
            ---------------------\n
            1.設立背景と目的\n
            - フリーランス連盟は、経営経験のある創業メンバーによって設立された非営利性の慈恵団体です。\n
            - 人口減少が進む現代社会において、「ヒト」という希少な資源を最大限に活用し、\n
            - フリーランスという働き方を尊重・支援することを目的としています。\n

            2.対象者\n
            - フリーランス、個人事業主、一人社長、副業ワーカーなど、自分の名前で仕事を獲得し業務を進める方。\n
            - 法人代表者でも、従業員を雇っていない場合は対象。\n
            - 将来フリーランスを目指す方やパラレルキャリア志向の会社員も含まれる。\n

            3.主な活動内容\n
            - コミュニティ運営\n
              - フリーランス同士の交流を深め、協業機会やキャリア形成を支援。\n
              - 会員サイトでプロフィールやポートフォリオを共有し、新たな仕事獲得のチャンスを提供。\n

            - 福利厚生プログラム
              - 健康診断補助や社会保険制度への切り替えサポート。\n
              - 賠償保険（自動付帯）や所得補償保険（任意加入）などの安心制度。\n

            - 営業・キャリア支援\n
              - 営業スキル向上のための講座や1on1サポート。\n
              - 法人クライアントとのビジネスマッチングサービス。\n

            - セーフティ・プレイスの提供\n
              - 法律、保険、財務面などの専門的相談窓口を設置。\n
              - 顧問弁護士や税理士など専門家への取り次ぎ。\n

            4. 加入条件\n
            - 社会保険に加入している法人や会社員は原則対象外。ただし例外あり。\n
            - 年間事業所得が約270万円以上の場合、毎月の支払い削減が可能な場合が多い。\n

            5. 注意事項\n
            - 会費滞納が2ヶ月続くと強制退会となる場合がある。\n
            - 年齢により会費が異なる（39歳以下と40歳以上で区分）。\n

            6. 目指す姿\n
            - フリーランス連盟は、フリーランスが安心して働ける環境を整備しつつ、\n
            - 企業側との協調も図ることで「秩序あるプロフェッショナルコミュニティ」を目指しています。\n
            - フリーランスという働き方が社会的に認知され、その価値が最大化される未来を創造します。\n
            ---------------------\n
            {context_str}
            \n---------------------\n
            この情報を踏まえて、以下の質問にお答えください：{query_str}\n
            回答の際は以下の点に注意してください：\n
            1. 弊社の広報担当者として丁寧かつ簡潔に回答してください。\n
            2. 回答は必ず完全な文章で行い、単語や数字だけの回答は避けてください。\n
            3. 会社に関する情報を提供する際は、「弊社」という言葉を使用してください。\n
            4. 質問の意図が不明確な場合は、丁寧に確認を求めてください。\n
            5. 回答は提供された情報の範囲内でのみ行い、推測や追加の情報提供はしないでください。\n
            6. 職業に関する質問には、具体的な職種を複数でも列挙して回答してください。単に「フリーランス」とだけ答えるのは避けてください。\n
            7.同一質問には常に同一の回答を提供してください。\n
            それでは、質問にお答えください：\n
            """
        )

    """
    埋め込みベクトルをインデックスに追加する
    :param embeddings: 追加する埋め込みベクトルのリスト。各要素は'answer'と'embedding'キーを持つ辞書
    :return: None
    """
    def add_embeddings(self, embeddings):
        # 各埋め込みベクトルをDocumentオブジェクトに変換
        docs = []
        for item in embeddings:
            doc = Document(
                text=item['answer'],
                extra_info={'question': item['question']},
                embedding=item['embedding']
            )
            docs.append(doc)
        
        # ベクトルストアにドキュメントを追加
        self.vector_store.add(docs)
        if self.index is None:
            # インデックスが未初期化の場合、新しいインデックスを作成
            storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
            self.index = VectorStoreIndex(
                docs,
                storage_context=storage_context
            )

    """
    ユーザーのメッセージに最も適した回答を見つける
    :param user_message: ユーザーからの質問メッセージ
    :param similarity_threshold: 類似度の閾値（デフォルト: 0.85）
    :return: 最適な回答または規定のメッセージ
    """
    def find_best_answer(self, user_message, similarity_threshold=0.85):
        # クエリエンジンを初期化（上位1件の結果を取得）
        query_engine = self.index.as_query_engine(
            text_qa_template= self.qa_template,
            similarity_top_k=1,
            vector_store_query_mode="default",
            max_tokens=500,
        )

        # ユーザーメッセージに対してクエリを実行
        response = query_engine.query(user_message)
        
        # 類似度が閾値を超える回答が見つかった場合はその回答を返す
        if response.source_nodes and response.source_nodes[0].score > similarity_threshold:
            return response.response
        else:
            return "当連盟以外の質問については回答することはできません。"
