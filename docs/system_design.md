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

理由：
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
4. 請求書Noの重複チェックを実施
5. Google Sheetsへ登録
6. 処理結果をログへ登録
7. 登録エラーを処理

### Excel取得項目

|項目|セル|
|---|---|
|請求書No|F2|
|送付日|F3|
|支払期限|F4|
|取引先|B3|
|案件名|B4|
|金額|F31|


# エラー処理設計

## 目的
処理中に発生する異常を検知し、原因確認ができるようにする。

## 対応済みエラー

### Google Sheets関連

- 認証ファイルなし
- スプレッドシート不存在
- 登録権限不足
- API接続エラー


### Excel関連

- ファイル不存在
- シート不存在
- 読込エラー


# ログ設計

## 目的

処理結果およびエラー発生状況を後から確認できるよう、loggingによるログ出力を実装する。


## ログ出力先
logs/invoice_manager.log



## ログレベル

|レベル|用途|
|---|---|
|INFO|正常処理結果|
|WARNING|注意が必要な処理|
|ERROR|処理失敗|


## 出力例

2026-07-14 14:00:25 INFO Google Sheetsへ接続できました
2026-07-14 14:01:10 WARNING 登録済みの請求書Noです
2026-07-14 14:02:15 ERROR Excel読み込みエラー



### モジュール構成

- authenticate()
- read_invoice_from_excel()
- is_duplicate_invoice_no()
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
├── logs/
│   └──invoice_manager.log
├── credentials.json
├── .gitignore
└── README.md


## 実装済み
### Google Sheets API
- API接続
- サービスアカウント認証
- スプレッドシート登録

## 請求データ登録
- Excel請求書読込
- 請求データ取得
- 請求書No重複チェック
- Google Sheets登録

## エラー処理
- Google Sheets接続時の例外処理
- Excel読込時の例外処理
- 登録処理エラー処理

## ログ出力
- loggingによるログ管理
- UTF-8形式でログ保存
- INFO/WARNING/ERRORによる分類

# 今後実装予定
- AppSheetによる入金登録
- 未入金アラート
- 月別売上集計
- ログ機能改善
- 設定値外部化
- テストコード追加

## 今後の開発予定
- [x] Googleスプレッドシートへ請求データ登録
- [x] Excel請求書からデータ取得
- [x] エラー処理追加
- [x] ログ出力追加
- [ ] AppSheetによる入金登録
- [ ] 未入金アラート
- [ ] 月別売上集計