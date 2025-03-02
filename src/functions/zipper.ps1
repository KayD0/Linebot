# ソースディレクトリとZIPファイルの出力先を指定
$sourceDir = "."
$destinationZip = "functions.zip"

# ZIP化する項目のリストを定義
$itemsToInclude = @(
    "services",
    "bot.py",
    "embeddings.py",
    "investigator.py",
    "requirements.txt"
)

# 一時ディレクトリを作成（システムの一時フォルダ内に作成）
$tempDir = New-Item -ItemType Directory -Path ".\tmp" -Force

# 指定された項目をソースディレクトリから一時ディレクトリにコピー
foreach ($item in $itemsToInclude) {
    $sourcePath = Join-Path $sourceDir $item
    if (Test-Path $sourcePath) {
        Copy-Item -Path $sourcePath -Destination $tempDir -Recurse -Force
    }
}

# 一時ディレクトリの内容をZIP化
Compress-Archive -Path "$tempDir\*" -DestinationPath $destinationZip -Force

# 一時ディレクトリを削除
Remove-Item -Path $tempDir -Recurse -Force

# ZIP化が成功したことを通知
Write-Host "Zip file created successfully: $destinationZip"
