# 請求・入金管理システム

## 目的

業務委託で発生する請求書の管理を効率化する。

## 現状

・Excelで請求書作成
・請求履歴管理が面倒
・入金管理していない

## システム構成

Excel
↓
Python
↓
Googleスプレッドシート
↓
AppSheet

## 主な機能（予定）

- 請求データ登録
- 入金管理
- 未入金アラート
- 売上集計

## Google Sheets連携

### 認証方式
- Google Sheets API
- サービスアカウント認証
- 認証情報は `credentials.json` を使用
- `credentials.json` は `.gitignore` に登録し、GitHubには含めない

### 接続方法
- スプレッドシートIDを指定して接続
- `open_by_key()` を使用する
  - スプレッドシート名変更の影響を受けない
  - Drive APIへのアクセスが不要
  - 実務でも保守しやすい

### データ構成

|項目|
|---|
|請求書No|
|送付日|
|支払期限|
|取引先|
|案件名|
|金額|
|入金日|

### 現在の実装状況
- Google Sheets APIによる接続確認完了
- Pythonからスプレッドシートへアクセス可能
- 次回は請求データ1件登録機能を実装予定

## 請求データ登録処理

### 処理フロー

1. Google Sheets APIで認証
2. Excel請求書を読み込む
3. 請求データを取得する
4. 請求書Noの重複チェックを実施する
5. 重複している場合は登録処理を中止する
6. 未登録の場合はGoogle Sheetsへ登録する

### Excel取得項目

|項目|セル|
|---|---|
|請求書No|F2|
|送付日|F3|
|支払期限|F4|
|取引先|B3|
|案件名|B4|
|金額|F31|

### モジュール構成

- authenticate()
- read_invoice_from_excel()
- register_invoice()
- main()


## フォルダ構成
invoice-manager/
├── docs/
│   └── system_design.md
├── src/
│   └── register_invoice.py
├── invoices/
│   └── yymm-??_取引先_案件名.xlsx
├── credentials.json
├── .gitignore
└── README.md


## 実装済み
### Google Sheets API

## 今後実装予定
- 請求データ登録
- Excel請求書からデータ取得
- AppSheetによる入金登録
- 未入金アラート
- 月別売上集計


## 今後の開発予定
- [ ] Googleスプレッドシートへ請求データ登録
- [ ] Excel請求書からデータ取得
- [ ] AppSheetによる入金登録
- [ ] 未入金アラート
- [ ] 月別売上集計