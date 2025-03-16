from openai import OpenAI

class OpenAiService:
    def __init__(self):
        self.openai = OpenAI()  # OpenAIのAPIキーを使用してインスタンスを初期化

    async def generate_qa_embeddings(self, qa_data):
        """
        QAデータ（質問と回答のペア）を埋め込み（ベクトル形式）に変換するメソッド
        :param qa_data: 質問と回答のペアのリスト。各要素は { 'question': str, 'answer': str } の辞書。
        :return: 埋め込みデータを含むリスト。各質問が埋め込みベクトルとともに保存される。
        """
        embeddings = []

        for qa_pair in qa_data:
            question_response = await self.generate_embeddings(self, qa_pair["question"])
            answer_response = await self.generate_embeddings(self, qa_pair["answer"])
            embeddings.append({
                'question': qa_pair['question'],
                'answer': qa_pair['answer'],
                'question_embedding': question_response,
                'answer_embedding': answer_response
            })

        return embeddings

    async def generate_embeddings(self, text):
        response = await self.openai.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response.data[0].embedding