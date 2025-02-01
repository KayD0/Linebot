const { OpenAI } = require('openai');

class OpenAiService {
  constructor() {
    this.openai = new OpenAI(); // OpenAIのAPIキーを使用してインスタンスを初期化
  }

  /**
   * QAデータ（質問と回答のペア）を埋め込み（ベクトル形式）に変換するメソッド
   * @param {Array} qaData - 質問と回答のペアのリスト。各要素は { question, answer } のオブジェクト。
   * @returns {Promise<Array>} 埋め込みデータを含む配列。各質問が埋め込みベクトルとともに保存される。
   */
  async generateEmbeddings(qaData) {
    const embeddings = [];

    for (const { question, answer } of qaData) {
      const response = await this.openai.embeddings.create({
        model: "text-embedding-ada-002",
        input: question,
      });

      embeddings.push({
        question,
        answer,
        embedding: response.data[0].embedding,
      });
    }

    return embeddings;
  }
}

module.exports = OpenAiService;