/**
 * スプレッドシートからQAデータを取得し、埋め込み処理のためのAPIエンドポイントに送信する関数。
 * 
 * この関数は以下の処理を行います：
 * 1. 指定されたスプレッドシートからQAデータ（質問と回答）を読み取ります。
 * 2. 読み取ったデータをJSON形式に変換します。
 * 3. 設定されたAPIエンドポイントにデータをPOSTリクエストで送信します。
 * 4. APIからのレスポンスをログに記録します。
 * 
 * エラーが発生した場合は、エラーメッセージをログに記録します。
 */
function requestEmbeddings() {
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
    
    // APIのURLを指定
    const url = PropertiesService.getScriptProperties().getProperty("API_EMBEDDING_ENDPOINT");
  
    // リクエストオプション
    const options = {
      method: 'post',
      contentType: 'application/json',
      payload: JSON.stringify(jsonData),
      headers: {
        'Authorization': `Bearer ${PropertiesService.getScriptProperties().getProperty("API_KEY")}` // ここに適切なトークンを入れてください
      }
    };
  
    // Google Cloud Functionを呼び出し
    try {
      const response = UrlFetchApp.fetch(url, options);
      Logger.log(response.getContentText());  // レスポンスをログに出力
    } catch (error) {
      Logger.log('Error: ' + error.message);
    }
    
  }
  
