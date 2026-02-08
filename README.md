# AutoHoldClick

## 概要

- AutoHoldClickは、指定したトグルキーを押すことで、マウスの左クリックまたは右クリックを保持し続けるツールです。
- トグルキーを再度押すことで、クリックの保持を解除できます。
- このツールは、繰り返し行うクリック操作の自動化や、長時間マウスボタンを保持する必要がある場合に便利です。

## 入力

- 設定ファイル：`config.json`
  - `toggle_key`：クリックの開始・停止を切り替えるためのキー。Pythonのkeyboardモジュールでの指定方法に従う。
  - `mouse_button`：マウスの左クリック（`left`）または右クリック（`right`）。
- ログ設定ファイル：`log_settings.json`
  - 読み込みに成功した場合、ログファイルを出力します。
  - 読み込みに失敗した場合、ログファイルは出力されません。
- トグルキー：クリックの開始・停止を切り替えるためのキー。

## 出力

- マウス操作：トグルキーで切り替えると、クリックの保持を開始・停止します。
- ログファイル：動作状況やエラーのログを記録します。
- 標準出力：現在の状態（クリック開始・停止など）を表示します。

## 想定実行環境

- Windows OSのPC
- Python 3.8以降
- 必要なPythonライブラリー
  - pynput
  - six

## 実行方法

1. 必要なPythonライブラリをインストールします（初回のみ）:

   ```powershell
   pip install -r requirements.txt
   ```

2. ツールを実行します:

    ```powershell
    python auto_hold_click/main.py --config config/config.json --log-settings config/log_settings.json
    ```

    - `--config` は必須です。設定ファイルのパスを指定してください。
    - `--log-settings` は任意です。指定しない場合は標準出力のみでログファイルは生成されません。

3. 設定ファイルやログ設定ファイルは、`config`フォルダー内の`config.json`および`log_settings.json`を編集してください。

## 処理詳細

1. ログ設定ファイルを読み込む。
    - 読み込みに成功した場合、ログファイルを出力する。
    - 次の場合、ログファイルは出力しない。
        - ログ設定ファイルが見つからない場合。
        - ログ設定ファイルのJSON形式が不正である場合。
        - ログ設定ファイルの読み込み中にIOエラーが発生した場合。
        - ログファイルの親フォルダーが存在しない場合。
1. 設定ファイルを読み込み、設定項目（`toggle_key`、`mouse_button`）の設定値を取得する。
    - 次の場合、エラーログを出力し、ツールを終了する。
        - 設定ファイルが見つからない場合。
        - 設定ファイルのJSON形式が不正である場合。
        - 設定ファイルの読み込み中にIOエラーが発生した場合。
        - 設定項目（`toggle_key`、`mouse_button`）のいずれかが存在しない場合。
        - 設定項目（`toggle_key`、`mouse_button`）のいずれかの設定値が空文字列である場合。
        - 設定項目（`toggle_key`、`mouse_button`）のいずれかの設定値が不正である場合。
1. 指定されたトグルキーの入力を受け付ける。
    - トグルキーが入力された場合、クリックの保持を開始または解除する。
1. Ctrl+Cが入力された場合、ツールを終了する。

## ファイル仕様

### 設定ファイル

| 項目 | 説明 |
| --- | --- |
| ファイルパス(実行フォルダーからの相対) | `config/config.json` |
| ファイル形式 | テキスト(JSON) |
| 文字コード | UTF-8(BOMなし) |

記載例：

```JSON
{
    "toggle_key": "f6",
    "mouse_button": "left"
}
```

### ログ設定ファイル

| 項目 | 説明 |
| --- | --- |
| ファイルパス(実行フォルダーからの相対) | `config/log_settings.json` |
| ファイル形式 | テキスト(JSON) |
| 文字コード | UTF-8(BOMなし) |

記載例：

```JSON
{
    "version": 1,
    "disable_existing_loggers": false,
    "formatters": {
        "fileFormatter": {
            "format": "%(asctime)s [%(levelname)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },

    "handlers": {
        "fileHandler": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "formatter": "fileFormatter",
            "filename": "./log/AutoHoldClick.log",
            "when": "midnight",
            "interval": 1,
            "encoding": "utf-8"
        }
    },

    "loggers": {
        "__main__": {
            "level": "DEBUG",
            "handlers": ["fileHandler"],
            "propagate": false
        }
    },

    "root": {
        "level": "DEBUG"
    }
}
```

### ログファイル

| 項目 | 説明 |
| --- | --- |
| ファイルパス(実行フォルダーからの相対) | `log/AutoHoldClick.log` |
| ファイル形式 | テキスト |
| 文字コード | UTF-8(BOMなし) |

出力例：

```log
2025-05-07 03:34:07 [INFO] 処理開始
2025-05-07 03:34:07 [INFO] 設定ファイルの読み込みに成功しました: トグルキー=f6, マウスボタン=left
2025-05-07 03:34:07 [INFO] トグルキーでクリックON/OFFします（Ctrl+Cで終了）
2025-05-07 03:34:08 [INFO] Ctrl+C が押されました
2025-05-07 03:34:08 [INFO] 処理終了
```

## ログメッセージ

| No. | 種別   | ログ内容(表示/記録される内容) |
|----|--------|----------------------------------------------|
| 1 | 情報   | 処理開始 |
| 2 | 情報   | 設定ファイルの読み込みに成功しました:トグルキー={toggle_key}, マウスボタン={mouse_button} |
| 3 | 情報   | トグルキーでクリックON/OFFします（Ctrl+Cで終了） |
| 4 | 情報   | 処理終了 |
| 5 | デバッグ | {button_name}クリックを開始しました。 |
| 6 | デバッグ | {button_name}クリックを解除しました。 |
| 7 | エラー  | ツール実行中に予期せぬ例外が発生しました。エラーメッセージ：{error} |
| 8 | エラー  | ツール実行中に例外が発生しました。エラーメッセージ：{error} |
| 9 | エラー  | ログ設定ファイルの読み込み中に例外が発生しました。パス：{file_path} |
| 10 | エラー  | ログ設定ファイルの読み込み中に予期せぬ例外が発生しました。パス：{file_path} |
| 11 | エラー  | ログ設定ファイルの読み込み中にIOエラーが発生しました。パス：{file_path} |
| 12 | エラー  | ログ設定ファイルが見つかりません。パス：{file_path} |
| 13 | エラー  | ログ設定ファイルのJSON形式が不正です。パス：{file_path} |
| 14 | エラー  | 設定ファイルが見つかりません。パス：{file_path} |
| 15 | エラー  | 設定ファイルのJSON形式が不正です。パス：{file_path} |
| 16 | エラー  | 設定ファイルの読み込み中にIOエラーが発生しました: {error} |
| 17 | エラー  | 設定項目が見つかりません。設定項目：{key} |
| 18 | エラー  | 設定項目の値が空です。設定項目：{key} |
| 19 | エラー  | 設定項目の値が不正です。設定項目：{key}, 設定値：{value} |

## 終了コード

| 終了コード | 名前 | 説明 |
|---|---|---|
| 0 | SUCCESS | 正常に終了した場合 |
| 1 | SPECIFIC_ERROR | 例外が発生した場合 |
| 2 | UNEXPECTED_ERROR | 予期しない例外が発生した場合 |

## ライセンス

### 本プログラムのライセンス

- このプログラムはMITライセンスに基づいて提供されます。

### 使用ライブラリーのライセンス

| ライブラリ名 | バージョン | ライセンス |
| ---- | ---- | ---- |
| pynput | 1.8.1 | GNU Lesser General Public License v3 |
| six | 1.17.0 | MIT License |

### 使用ライブラリーのライセンス(ビルド用)

| ライブラリ名 | バージョン | ライセンス |
| ---- | ---- | ---- |
| altgraph | 0.17.4 | MIT License |
| packaging | 25.0 | Apache License 2.0 |
| pefile | 2023.2.7 | MIT License |
| pyinstaller | 6.14.2 | GNU General Public License v2 |
| pyinstaller-hooks-contrib | 2025.8 | GNU General Public License v2 |
| pywin32-ctypes | 0.2.3 | BSD-3-Clause |
| setuptools | 80.9.0 | MIT License |

## 検証環境

- OS：Microsoft Windows 11 Home
- CPU：Intel64 Family 6 Model 154 Stepping 3 GenuineIntel ~2100 Mhz
- メモリー：16 GB
- Python 3.12.10
- 使用ライブラリー
  - pynput==1.8.1
  - six==1.17.0

## 改訂履歴

| バージョン | 日付 | 内容 |
| ----- | ---------- | -------------- |
| 1.0.1 | 2025-07-31 | ビルドできるように修正 by @Shinoryo in #5 <br> ログフォルダーが存在しない場合の挙動を注意制限事項に追記 by @Shinoryo in #6 <br> pyinstallerコマンドに--nameオプションを追加し、手順を更新 by @Shinoryo in #7 |
| 1.0.0 | 2025-07-31 | 初版リリース |
