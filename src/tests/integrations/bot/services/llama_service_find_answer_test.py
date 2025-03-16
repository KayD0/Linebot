import sys
import unittest
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','..','..')))
from functions.bot.services.llama_service import LlamaService
from common.file_service import FileService

class TestLlamaServiceIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        file_service = FileService()
        embeddings = file_service.read_json_from_file('tests/integrations/data', 'embeddings.json')
        cls.service = LlamaService()
        cls.service.add_embeddings(embeddings)

    def test_統合テスト_正常な検索(self):
        for query, expected in self.test_cases:
            # arrange & act
            result = self.service.find_answer(query)
            # assert
            print(f"Testing query: {query}, Expected: {expected}")
            self.assertEqual(result.node.metadata['answer'], expected)

    @property
    def test_cases(self):
        """
        テストケースをプロパティとして定義。
        :return: テストケースのリスト
        """
        return [
            ("会社員は対象外ですか？", "社会保険に加入している会社員は対象外です。"),
            ("法人は対象外ですか？", "社会保険に加入している法人格は対象外です。ただし、法人の代表者が社会保険に加入していない場合は対象となります。"),
            ("システムエンジニアは対象ですか？", "対象です。"),
            ("デザイナーは対象ですか？", "対象です。"),
            ("税理士は対象ですか？", "対象です。")
        ]

if __name__ == '__main__':
    # 実際のOpenAI APIキーを設定
    os.environ['OPENAI_API_KEY'] = ''
    unittest.main()
