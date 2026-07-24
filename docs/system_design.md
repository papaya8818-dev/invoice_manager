# 請求・入金管理システム

## 目的

業務委託で発生する請求データの登録・管理および入金管理を効率化する。

## 導入前の課題

・Excelで請求書を作成
・請求履歴管理が煩雑
・入金状況を管理していない

## システム構成

```
Excel請求書（xlsm）
  ↓
VBAマクロ
  ↓
Python
（Excel読み込み・データ整形）
  ↓
Google Sheets API
  ↓
Googleスプレッドシート
（請求データ管理）
  ↓
AppSheet
（請求一覧・入金管理・売上分析）
```


## 主な機能

### 実装済み

- Excel VBAからPython処理を起動
- xlsx / xlsm形式の請求書読み込み対応
- Excel請求書から請求データ取得
- Googleスプレッドシートへの自動登録
- 請求書No重複チェック
- AppSheetによる請求一覧表示
- 未入金一覧表示
- 入金日更新
- 入金状態管理

### 今後実装予定

- 月別売上集計

## Googleスプレッドシート連携

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


## AppSheet連携

### 機能

- Googleスプレッドシートをデータソースとして利用
- 請求一覧表示
- 未入金一覧表示
- 入金日更新
- 年間売上集計
- 対象年による集計条件切替

### 仮想列

入金状態判定用の仮想列をAppSheet側で管理する。
詳細は後述。

## AppSheet Automation

### 未入金アラート

支払期限を超過した未入金データを検知し、
メール通知を行う。

判定条件：
- 入金日なし
- 支払期限 < TODAY()

処理：
1. 請求データのステータス判定
2. 条件一致データをAutomationで検知
3. メール通知を実行

### 定期チェック機能

支払期限超過データを定期的に確認するScheduled Eventを作成。

ただし、AppSheet FreeプランではScheduled Eventが利用できないため、
現在はデータ変更時の通知機能を利用。

有料プラン利用時には定期通知へ拡張可能。


## 売上分析機能

### 目的

指定した対象年の請求金額を集計し、年間売上を確認できるようにする。

### 集計方法

表示設定テーブルの対象年を条件として、請求データの送付日から対象年のデータを抽出し、金額を合計する。

### データ構成

表示設定

|項目|内容|
|-|-|
|ID|設定識別子|
|対象年|集計対象年|

### 計算方法

AppSheet仮想列でSUM(SELECT())を使用して集計する。


## 現在の実装状況

- Google Sheets APIによる接続
- サービスアカウント認証
- Excel請求書から請求データ取得
- 請求データをGoogleスプレッドシートへ登録
- 請求書No重複チェック
- エラー処理
- 処理結果通知（SUCCESS/DUPLICATE/ERROR）
- ログ出力
- 設定ファイル（config.ini）による設定管理
- AppSheetによる請求管理画面
- 入金状態の自動判定
- AppSheet Automationによる未入金アラート通知
- 対象年による年間売上集計
- 売上分析画面
- AppSheetアプリをDeploy状態へ移行
- 運用利用を想定した設定を実施

## 請求データ登録処理

### 処理フロー

1. Excel VBAからPython処理を起動
2. 請求書ファイルパスを取得
3. 設定ファイルを読み込む
4. Google Sheets APIで認証
5. Excel請求書を読み込む
6. 請求データを取得する
7. 請求書Noの重複チェックを実施
8. Googleスプレッドシートへ登録
9. 処理結果をログへ登録
10. 登録エラーを処理

### 処理結果管理

Python処理結果を以下の3種類で管理する。

|結果|内容|
|-|-|
|SUCCESS|請求データ登録成功|
|DUPLICATE|請求書No重複により登録なし|
|ERROR|処理エラー|

VBA側ではPythonの終了コードを取得し、SUCCESS/DUPLICATE/ERRORに応じて利用者へ処理結果を通知する。

### Excel取得項目

|項目|セル|
|---|---|
|請求書No|F2|
|送付日|F3|
|支払期限|F4|
|取引先|B3|
|案件名|B4|
|金額|F31|

### AppSheet仮想列

ステータスはGoogleスプレッドシート上には保存せず、
AppSheet側の仮想列として管理する。

判定：
- 入金日あり → 入金済
- 入金日なし かつ 支払期限超過 → 期限超過
- 入金日なし かつ 支払期限内 → 未入金

## エラー処理設計

### 目的

処理中に発生する異常を検知し、原因確認ができるようにする。

### 対応済みエラー

#### Googleスプレッドシート関連

- 認証ファイルなし
- スプレッドシートなし
- 登録権限不足
- API接続エラー

#### Excel関連

- ファイルなし
- シートなし
- 読込エラー

#### 設定関連

- 設定ファイルなし
- 設定項目不足
- 設定値読み込みエラー

### 設定管理

#### 設定ファイル

環境依存の設定値はconfig.iniで管理する。

設定ファイル：
config/config.ini

管理項目：
|項目|内容|
|---|---|
|spreadsheet_id|GoogleスプレッドシートID|
|invoice_dir|請求書ファイル保存フォルダ|

#### 設定取得処理

処理フロー：
1. config.iniを読み込む
2. 必要な設定値を取得
3. 各処理へ設定値を渡す

設定ファイルが存在しない場合や設定項目が不足している場合は、ログへエラーを出力し処理を終了する。

#### 設定ファイル構成

Git管理対象：
config/config.ini.example

Git管理対象外：
config/config.ini

実際の実行環境ではexampleファイルをコピーして設定する。

## ログ設計

### 目的

処理結果およびエラー発生状況を後から確認できるよう、loggingによるログ出力を実装する。

### ログ出力先

logs/invoice_manager.log

### ログレベル

|レベル|用途|
|---|---|
|INFO|正常処理結果|
|WARNING|注意が必要な処理|
|ERROR|処理失敗|

### 出力例

2026-07-14 14:00:25 INFO Google Sheetsへ接続できました
2026-07-14 14:01:10 WARNING 登録済みの請求書Noです
2026-07-14 14:02:15 ERROR Excel読み込みエラー


## モジュール構成

|ファイル|役割|
|-|-|
|register_invoice.py|処理起動・引数受付|
|excel_reader.py|Excel請求書読み込み|
|sheets_client.py|Googleスプレッドシート接続|
|invoice_service.py|請求データ登録処理|
|config.py|設定管理|
|logger.py|ログ管理|


## フォルダ構成

invoice-manager/  
├── docs/  
│   └── system_design.md  
├── src/  
│   ├── register_invoice.py  
│   ├── invoice_service.py 
│   ├── excel_reader.py 
│   ├── sheets_client.py 
│   ├── config.py  
│   └── logger.py 
├── invoices/  
│   └── 請求書ファイル（xlsx / xlsm）  
├── config/  
│   ├── config.ini.example  (Git管理)
│   └── config.ini          (Git管理外) 
├── logs/  
│   └── （実行時生成）  
├── credentials.json  （Git管理外）
├── .gitignore  
└── README.md  


## 今後の開発予定

- [x] Googleスプレッドシートへ請求データ登録
- [x] Excel請求書からデータ取得
- [x] エラー処理追加
- [x] ログ出力追加
- [x] 設定ファイル管理追加
- [x] AppSheetによる請求一覧・入金日管理
- [x] 未入金アラート
- [ ] 月別売上集計
