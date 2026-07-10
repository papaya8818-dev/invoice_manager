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
2. スプレッドシートへ接続
3. 請求データを辞書形式で作成
4. 列順に合わせてリストへ変換
5. `append_row()` で末尾へ追加

### データモデル

|項目|型|
|---|---|
|請求書No|string|
|送付日|string|
|支払期限|string|
|取引先|string|
|案件名|string|
|金額|integer|
|入金日|string|


## フォルダ構成
invoice-manager/
├── docs/
│   └── system_design.md
├── src/
│   └── register_invoice.py
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