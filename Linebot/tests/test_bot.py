import os
import sys
sys.path.append(os.getcwd())

from dotenv import load_dotenv
load_dotenv()
from linebot.services.llama_service import LlamaService
from linebot.services.file_service import FileService

import unittest

class Test_TestFindAnswer(unittest.TestCase):
    def test_find_answer1(self):
        user_message = "確定拠出年金(国民年金基金連合会)の法人型から個人型への変更について教えてください。"
        fileService = FileService()
        file_path = "tests\datas"
        file_name = "qaemb.json"
        embeddings = fileService.read_json_from_file(file_path, file_name)

        llamaService = LlamaService()
        llamaService.add_embeddings(embeddings)
        ai_response = llamaService.find_best_answer(user_message)
        print(ai_response)

if __name__ == '__main__':
    unittest.main()