const functions = require('@google-cloud/functions-framework');
const StorageService = require('./storageService');
const OpenAiService = require('./openAiService');

functions.http('createindex2', async (req, res) => {  
  // リクエストボディからQAデータを取得
  const data = req.body;  
  if (!data || !data.qaData) {
    return res.status(400).send('リクエストボディにQAデータが含まれていません。');
  }

  // INDEX化
  let embeddings;
  try {
    const openAiService = new OpenAiService();
    embeddings = await openAiService.generateEmbeddings(data.qaData);
  } catch (error) {
    console.error('Open Ai Api エラー');
    console.error('Error occurred', error);
    return res.status(500).send('Error occurred');
  }

  // INDEX化ファイルを保存
  const storageService = new StorageService();
  const indexFileName = process.env.QA_INDEX_FILE_NAME;
  const qaIndexBucketName = process.env.QA_INDEX_BUCKET_NAME;
  try {
    await storageService.writeJsonToFile(qaIndexBucketName, 'qa', indexFileName, embeddings);
    res.status(200).send('INDEX化に成功しました。');
  } catch (error) {
    console.error('Cloud Storage Write エラー');
    console.error('Error occurred', error);
    return res.status(500).send('Error occurred');
  }
});