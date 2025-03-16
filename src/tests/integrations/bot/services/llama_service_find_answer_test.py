import sys
import unittest
import os
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','..','..')))
from functions.bot.services.llama_service import LlamaService
from common.file_service import FileService

class TestLlamaServiceIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        file_service = FileService()
        embeddings = file_service.read_json_from_file('tests\integrations\data', 'embeddings.json')
        # サービス初期化とデータ投入
        cls.service = LlamaService()
        cls.service.add_embeddings(embeddings)

    def test_統合テスト_正常な検索(self):
        # arrange
        query = '必要書類の住民票'

        # act
        results = self.service.find_answer(query)

        # assert
        for result in results:
            print(result.node.metadata['answer'])            

if __name__ == '__main__':
    # 実際のOpenAI APIキーを設定
    os.environ['OPENAI_API_KEY'] = ''
    unittest.main()
