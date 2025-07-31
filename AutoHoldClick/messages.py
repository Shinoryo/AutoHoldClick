class Messages:
    """メッセージ定数をまとめたクラス。

    このクラスは、アプリケーション内で使用されるメッセージを一元管理します。
    """

    # 一般メッセージ
    START_PROCESS = "処理開始"
    END_PROCESS = "処理終了"
    WAIT_FOR_TOGGLE_KEY = "トグルキーでクリックON/OFFします（Ctrl+Cで終了）"
    CTRL_C_PRESSED = "Ctrl+C が押されました"

    # 設定関連メッセージ
    CONFIG_LOAD_SUCCESS = "設定ファイルの読み込みに成功しました: トグルキー={toggle_key}, マウスボタン={mouse_button}"
    CONFIG_FILE_NOT_FOUND = "設定ファイルが見つかりません。パス：{file_path}"
    CONFIG_INVALID_JSON = "設定ファイルのJSON形式が不正です。パス：{file_path}"
    CONFIG_LOAD_IO_ERROR = "設定ファイルの読み込み中にIOエラーが発生しました: {error}"
    CONFIG_KEY_NOT_FOUND = "設定項目が見つかりません。設定項目：{key}"
    CONFIG_EMPTY_VALUE = "設定項目の値が空です。設定項目：{key}"
    CONFIG_INVALID_VALUE = "設定項目の値が不正です。設定項目：{key}, 設定値：{value}"

    # クリック関連メッセージ
    CLICK_START_LOG = "{button_name}クリックを開始しました。"
    CLICK_STOP_LOG = "{button_name}クリックを解除しました。"

    # ログ関連メッセージ
    LOGGER_LOAD_SPECIFIC_ERROR = (
        "ログ設定ファイルの読み込み中に例外が発生しました。パス：{file_path}"
    )
    LOGGER_LOAD_UNEXPECTED_ERROR = (
        "ログ設定ファイルの読み込み中に予期せぬ例外が発生しました。パス：{file_path}"
    )
    LOGGER_FILE_NOT_FOUND = "ログ設定ファイルが見つかりません。パス：{file_path}"
    LOGGER_INVALID_JSON = "ログ設定ファイルのJSON形式が不正です。パス：{file_path}"
    LOGGER_LOAD_IO_ERROR = (
        "ログ設定ファイルの読み込み中にIOエラーが発生しました。パス：{file_path}"
    )

    # 例外メッセージ
    UNEXPECTED_ERROR = (
        "ツール実行中に予期せぬ例外が発生しました。エラーメッセージ：{error}"
    )
    SPECIFIC_ERROR = "ツール実行中に例外が発生しました。エラーメッセージ：{error}"
