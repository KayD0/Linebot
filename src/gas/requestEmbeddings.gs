function requestLinebotEnbeddings() {
  // スプレッドシートIDとシート名を指定
  const spreadsheetId = PropertiesService.getScriptProperties().getProperty("QA_SHEET_ID");  // スプレッドシートIDを指定
  const sheetName = 'QAシート';  // シート名を指定
  const sheet = SpreadsheetApp.openById(spreadsheetId).getSheetByName(sheetName);

  // 特定の列のデータを取得（例: A列）
  const range = sheet.getRange('A3:B100');  // A3からB32までの範囲を指定
  const values = range.getValues().filter(row => row[0] && row[1]);; // 空のセルを除外

  // A列（質問）とB列（回答）をキーとしてJSONオブジェクトの配列に変換
  const jsonData = {
    qaData: values.map(row => ({
      question: row[0],  // A列の値を'question'キーに
      answer: row[1]     // B列の値を'answer'キーに
    }))
  };
  
  // Cloud FunctionのURLを指定
  const url = PropertiesService.getScriptProperties().getProperty("GCF_API_EMBEDDINGS_ENDPOINT");
  // リクエストオプション
  const options = {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify(jsonData),
    headers: {
      'Authorization': `Bearer ${ScriptApp.getIdentityToken()}` // ここに適切なトークンを入れてください
    }
  };

  // Google Cloud Functionを呼び出し
  try {
    const response = UrlFetchApp.fetch(url, options);
    const responseText = response.getContentText('UTF-8');
    const parsedResponse = JSON.parse(responseText);
    Logger.log(parsedResponse.body);
    Browser.msgBox("登録に成功しました。");
  } catch (error) {
    Logger.log('Error: ' + error.message);
    Browser.msgBox("登録に失敗しました。");
  }
}
