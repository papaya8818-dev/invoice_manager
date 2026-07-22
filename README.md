# Invoice Manager（請求・入金管理システム）

## 概要

業務委託で発生する請求データの管理・入金管理を効率化するためのシステム。

Excelで作成した請求書から請求データを取得し、Googleスプレッドシートへ自動登録することで請求管理業務を効率化。
さらにAppSheetを利用して請求一覧・未入金一覧・入金管理機能を実装し、請求状況を可視化できるシステムとして開発。

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
（請求一覧・入金管理）
```


## 使用技術

- Python
- Googleスプレッドシート
- Google Sheets API
- AppSheet
- Excel
- Git / GitHub
- openpyxl
- gspread
- pytest
- Excel VBA


## 設定管理

環境依存の設定値は `config.ini` で管理する。

GitHub公開用に設定例ファイルを用意している。
config/config.ini.example

実行環境では設定例をコピーして利用する。
config/config.ini

## 実行方法

### Pythonから直接実行する場合

請求書ファイル名を指定して実行する。

```bash
python -m src.register_invoice 請求書ファイル名.xlsx
```
（プロジェクト直下で実行）

対応形式：
- .xlsx
- .xlsm

### Excel VBAから実行する場合

請求書Excelファイルに設定したVBAマクロからPython処理を起動する。

処理フロー：
```
Excel VBA
    ↓
Python起動
    ↓
請求データ取得
    ↓
Googleスプレッドシート登録
    ↓
終了コード返却
    ↓
VBAで結果表示
    ↓
成功 / 重複 / エラー通知
```

利用者はExcel上の操作のみで請求登録処理を実行できる。


## 機能一覧

### 請求データ登録

- Excel請求書から請求データを取得
- Google Sheetsへ自動登録
- 請求書Noの重複チェック
- 設定ファイル（config.ini）による環境設定管理

### 処理結果通知

- Python処理結果を終了コードで返却
- VBA側で処理結果を判定
- 成功・重複・エラーをメッセージ表示

### AppSheetによる請求管理

- Googleスプレッドシートをデータソースとして利用
- 請求一覧画面を作成
- 未入金一覧ビューを作成
- 入金日をAppSheetから更新可能
- 入金日をもとに入金状態を自動判定

### AppSheet Automation

- 入金日未入力かつ支払期限超過データを検知
- 未入金請求をメール通知
- 入金漏れ防止を支援

### 動作確認済みフロー

以下の一連の処理を実データ形式（xlsm）で確認済み。

```
Excel請求書（xlsm）
    ↓
VBAからPython起動
    ↓
Excel請求データ取得
    ↓
Googleスプレッドシート登録
    ↓
AppSheet請求一覧表示
    ↓
AppSheetから入金日更新
    ↓
入金状態反映
    ↓
支払期限超過データ検知
    ↓
未入金アラートメール送信
```

確認内容：
- VBAからPython起動
- xlsx / xlsmファイル読み込み
- Google Sheets API登録
- ログ出力
- 処理結果通知（成功・重複・エラー）
- AppSheet表示・更新

### エラー処理

以下の処理に対する例外処理を実装。

- Google Sheets API認証エラー
- スプレッドシート接続エラー
- Google Sheets登録エラー
- Excelファイル読み込みエラー
- Excelシート取得エラー
- 設定ファイル読み込みエラー


### ログ出力

Python標準ライブラリ `logging` を利用し、処理結果やエラー情報をログファイルへ記録。

ログ出力内容：

- Google Sheets接続結果
- 請求データ登録結果
- 請求書No重複による登録中止
- エラー発生内容

ログファイル：

logs/invoice_manager.log

## テスト

pytestによる単体テストを実装。

### 実行方法

プロジェクト直下で以下を実行する。

```bash
pytest
```

### テスト対象

現在は以下の処理をテスト対象としている。

- Excel請求データ読み込み
- 請求データ登録処理
- 請求書No重複チェック
- 請求書No未入力チェック
- 設定ファイル読み込み処理
- ファイル存在チェック

現在21件のテストが実行され、すべて成功している。
Python処理部分をpytestで検証し、AppSheet側は画面・データ連携による動作確認を実施。


## プロジェクト構成
```
invoice_manager/ 
│ 
├── src/ 
│   ├── register_invoice.py 
│   ├── invoice_service.py 
│   ├── excel_reader.py 
│   ├── sheets_client.py 
│   ├── config.py 
│   └── logger.py 
│ 
├── tests/ 
│   ├── test_register_invoice.py 
│   ├── test_invoice_service.py 
│   └── test_config.py 
│ 
├── config/ 
│   └── config.ini.example 
│ 
└── logs/ 
    └── （実行時生成）
```


## Git管理

Gitでソースコードおよびドキュメントの変更履歴を管理。

以下はGit管理対象外。

- `logs/`
- `invoices/`
- `credentials.json`
- `config/config.ini`

理由：

- `logs/`：実行時生成ファイルのため
- `invoices/`：実データ保護のため
- `credentials.json`：認証情報保護のため
- `config/config.ini`：環境依存設定のため


## 開発履歴

- 2026-07-10 Git/GitHub環境構築
- 2026-07-10 システム設計書を作成
- 2026-07-10 Google Sheets API接続を実装
- 2026-07-10 請求データ登録機能を実装
- 2026-07-13 Excel請求書から請求データを取得してGoogleスプレッドシートへ登録する機能を実装
- 2026-07-14 請求書No重複チェック機能を追加
- 2026-07-14 Google Sheets・Excel処理のエラー処理を追加
- 2026-07-14 ログ出力機能を追加
- 2026-07-14 設定ファイル（config.ini）対応を追加
- 2026-07-14 設定読み込み処理を関数化し、設定エラー処理を追加
- 2026-07-15 設定ファイルサンプル（config.ini.example）を追加
- 2026-07-21 処理機能をモジュール分割し、責務ごとに整理（Excel処理・Sheets処理・設定管理・ログ管理）
- 2026-07-21 モジュール分割後の単体テストを追加（21件）
- 2026-07-21 AppSheet連携を実装（請求一覧・未入金一覧・入金管理機能）
- 2026-07-22 VBA連携による請求登録処理の動作確認を実施
- 2026-07-22 実データによるExcel→Python→Sheets→AppSheet連携を確認
- 2026-07-22 処理結果通知機能を追加（成功・重複・エラー判定）
- 2026-07-22 AppSheet Automationによる未入金アラート機能を追加
