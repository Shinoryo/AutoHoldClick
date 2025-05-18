# AutoHoldClick

## 概要
- AutoHoldClickは、指定されたトグルキーを押すことで、マウスの左クリックまたは右クリックを保持し続けるツールである。
- トグルキーをもう一度押すことで、クリックを解除できる。
- このツールは、繰り返し行うクリック操作を自動化したり、長時間マウスボタンを保持する必要がある場合に便利である。

## 入力
- 設定ファイル：`config.json`
    - `toggle_key`：クリックのオン/オフを切り替えるためのキー。Pythonのkeyboardモジュールでの指定方法に従う。
    - `mouse_button`：マウスの左クリック(`left`)または右クリック(`right`)。
- ログ設定ファイル：`log_settings.json`
    - 読み込みに成功した場合、ログファイルを出力する。
    - 読み込みに失敗した場合、ログファイルを出力しない。
- トグルキー：クリックのオン/オフを切り替えるためのキー。

## 出力
- マウス操作：トグルキーでトグルされると、クリックを開始・停止する。
- ログファイル：動作状況・エラーのログを記録する。
- 標準出力：現在の状態(クリック開始・停止など)を表示する。

## 想定実行環境
- Windows OSのPC
- Python 3.8以降
- 次のPythonライブラリー
    - pynput

## 検証環境
- OS：Microsoft Windows 11 Home
- CPU：Intel64 Family 6 Model 154 Stepping 3 GenuineIntel ~2100 Mhz
- メモリー：16 GB
- Python 3.11.4
- 次のPythonライブラリー
    - pynput==1.8.1

## 処理詳細
1. ログ設定ファイルを読み込む。
    - 読み込みに成功した場合、ログファイルを出力する。
    - 次の場合、ログファイルを出力しない。
        - ログ設定ファイルが見つからない場合。
        - ログ設定ファイルのJSON形式が不正である場合。
        - ログ設定ファイルの読み込み中にエラーが発生した場合。
1. 設定ファイルを読み込み、設定項目(`toggle_key`、`mouse_button`)の設定値を取得する。
    - 次の場合、エラーログを出力し、ツールを終了する。
        - 設定ファイルが見つからない場合。
        - 設定ファイルのJSON形式が不正である場合。
        - 設定ファイルの読み込み中にエラーが発生した場合。
        - 設定項目(`toggle_key`、`mouse_button`)のいずれかが存在しない場合。
        - 設定項目(`toggle_key`、`mouse_button`)のいずれかの設定値が空文字列である場合。
        - 設定項目(`toggle_key`、`mouse_button`)のいずれかの設定値が不正である場合。
1. 指定されたトグルキーの入力を受け付ける。
    - トグルキーが入力されると、クリックを開始または解除する。
1. Ctrl+Cが入力されると、ツールを終了する。

## ファイル仕様

### 設定ファイル

| 項目 | 説明 |
| --- | --- |
| ファイルパス(実行フォルダーからの相対) | `config.json` |
| ファイル形式 | テキスト(JSON) |
| 文字コード | UTF-8(BOMなし) |

記載例：
```JSON
{
    "toggle_key": "F6",
    "mouse_button": "left"
}
```

### ログ設定ファイル

| 項目 | 説明 |
| --- | --- |
| ファイルパス(実行フォルダーからの相対) | `config.json` |
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
| ファイルパス(実行フォルダーからの相対) | `log\AutoHoldClick.log` |
| ファイル形式 | テキスト |
| 文字コード | UTF-8(BOMなし) |

出力例：
```
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
| 13 | エラー  | ログ設定ファイルがJSON形式ではありません。パス：{file_path} |
| 14 | エラー  | 設定ファイルが見つかりません。パス：{file_path} |
| 15 | エラー  | 設定ファイルのJSON形式が正しくありません。パス：{file_path} |
| 16 | エラー  | 設定ファイルの読み込み中にIOエラーが発生しました:{error} |
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
このプログラムは、MITライセンスの下で提供されます。

このプログラムは、以下の外部ライブラリーを利用して動作します。

### pynput 1.8.1

- 著作権者: (C) 2015-2024 Moses Palmér
- ライセンス: GNU Lesser General Public License v3 (LGPLv3)
- URL: https://github.com/moses-palmer/pynput

```
                   GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007-2024 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.


  This version of the GNU Lesser General Public License incorporates
the terms and conditions of version 3 of the GNU General Public
License, supplemented by the additional permissions listed below.

  0. Additional Definitions.

  As used herein, "this License" refers to version 3 of the GNU Lesser
General Public License, and the "GNU GPL" refers to version 3 of the GNU
General Public License.

  "The Library" refers to a covered work governed by this License,
other than an Application or a Combined Work as defined below.

  An "Application" is any work that makes use of an interface provided
by the Library, but which is not otherwise based on the Library.
Defining a subclass of a class defined by the Library is deemed a mode
of using an interface provided by the Library.

  A "Combined Work" is a work produced by combining or linking an
Application with the Library.  The particular version of the Library
with which the Combined Work was made is also called the "Linked
Version".

  The "Minimal Corresponding Source" for a Combined Work means the
Corresponding Source for the Combined Work, excluding any source code
for portions of the Combined Work that, considered in isolation, are
based on the Application, and not on the Linked Version.

  The "Corresponding Application Code" for a Combined Work means the
object code and/or source code for the Application, including any data
and utility programs needed for reproducing the Combined Work from the
Application, but excluding the System Libraries of the Combined Work.

  1. Exception to Section 3 of the GNU GPL.

  You may convey a covered work under sections 3 and 4 of this License
without being bound by section 3 of the GNU GPL.

  2. Conveying Modified Versions.

  If you modify a copy of the Library, and, in your modifications, a
facility refers to a function or data to be supplied by an Application
that uses the facility (other than as an argument passed when the
facility is invoked), then you may convey a copy of the modified
version:

   a) under this License, provided that you make a good faith effort to
   ensure that, in the event an Application does not supply the
   function or data, the facility still operates, and performs
   whatever part of its purpose remains meaningful, or

   b) under the GNU GPL, with none of the additional permissions of
   this License applicable to that copy.

  3. Object Code Incorporating Material from Library Header Files.

  The object code form of an Application may incorporate material from
a header file that is part of the Library.  You may convey such object
code under terms of your choice, provided that, if the incorporated
material is not limited to numerical parameters, data structure
layouts and accessors, or small macros, inline functions and templates
(ten or fewer lines in length), you do both of the following:

   a) Give prominent notice with each copy of the object code that the
   Library is used in it and that the Library and its use are
   covered by this License.

   b) Accompany the object code with a copy of the GNU GPL and this license
   document.

  4. Combined Works.

  You may convey a Combined Work under terms of your choice that,
taken together, effectively do not restrict modification of the
portions of the Library contained in the Combined Work and reverse
engineering for debugging such modifications, if you also do each of
the following:

   a) Give prominent notice with each copy of the Combined Work that
   the Library is used in it and that the Library and its use are
   covered by this License.

   b) Accompany the Combined Work with a copy of the GNU GPL and this license
   document.

   c) For a Combined Work that displays copyright notices during
   execution, include the copyright notice for the Library among
   these notices, as well as a reference directing the user to the
   copies of the GNU GPL and this license document.

   d) Do one of the following:

       0) Convey the Minimal Corresponding Source under the terms of this
       License, and the Corresponding Application Code in a form
       suitable for, and under terms that permit, the user to
       recombine or relink the Application with a modified version of
       the Linked Version to produce a modified Combined Work, in the
       manner specified by section 6 of the GNU GPL for conveying
       Corresponding Source.

       1) Use a suitable shared library mechanism for linking with the
       Library.  A suitable mechanism is one that (a) uses at run time
       a copy of the Library already present on the user's computer
       system, and (b) will operate properly with a modified version
       of the Library that is interface-compatible with the Linked
       Version.

   e) Provide Installation Information, but only if you would otherwise
   be required to provide such information under section 6 of the
   GNU GPL, and only to the extent that such information is
   necessary to install and execute a modified version of the
   Combined Work produced by recombining or relinking the
   Application with a modified version of the Linked Version. (If
   you use option 4d0, the Installation Information must accompany
   the Minimal Corresponding Source and Corresponding Application
   Code. If you use option 4d1, you must provide the Installation
   Information in the manner specified by section 6 of the GNU GPL
   for conveying Corresponding Source.)

  5. Combined Libraries.

  You may place library facilities that are a work based on the
Library side by side in a single library together with other library
facilities that are not Applications and are not covered by this
License, and convey such a combined library under terms of your
choice, if you do both of the following:

   a) Accompany the combined library with a copy of the same work based
   on the Library, uncombined with any other library facilities,
   conveyed under the terms of this License.

   b) Give prominent notice with the combined library that part of it
   is a work based on the Library, and explaining where to find the
   accompanying uncombined form of the same work.

  6. Revised Versions of the GNU Lesser General Public License.

  The Free Software Foundation may publish revised and/or new versions
of the GNU Lesser General Public License from time to time. Such new
versions will be similar in spirit to the present version, but may
differ in detail to address new problems or concerns.

  Each version is given a distinguishing version number. If the
Library as you received it specifies that a certain numbered version
of the GNU Lesser General Public License "or any later version"
applies to it, you have the option of following the terms and
conditions either of that published version or of any later version
published by the Free Software Foundation. If the Library as you
received it does not specify a version number of the GNU Lesser
General Public License, you may choose any version of the GNU Lesser
General Public License ever published by the Free Software Foundation.

  If the Library as you received it specifies that a proxy can decide
whether future versions of the GNU Lesser General Public License shall
apply, that proxy's public statement of acceptance of any version is
permanent authorization for you to choose that version for the
Library.
```
