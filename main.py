"""AutoHoldClick"""

import atexit
import json
import logging
import logging.config
import sys
import time

from pynput import keyboard, mouse


class AutoHoldClickException(Exception):
    """AutoHoldClickの独自例外クラス"""

    def __init__(self, message):
        super().__init__(message)


class Config:
    """設定を管理するクラス

    JSON設定ファイル（デフォルトは 'config.json'）からトグルキーとマウスボタンの設定を読み込む。
    このクラスから、トグルキーとマウスボタンの設定を取得できる。

    設定ファイルの例：
    {
        "toggle_key": "f6",
        "mouse_button": "left"
    }

    Attributes:
        config_file (str): 設定ファイルのパス。
        logger (logging.Logger): ログ出力用のロガー。
        toggle_key (keyboard.Key): トグルキー。
        mouse_button (mouse.Button): マウスボタン。
    """

    TOGGLE_KEY_KEY = "toggle_key"
    MOUSE_BUTTON_KEY = "mouse_button"
    CONFIG_FILE_ENCODING = "utf-8"

    def __init__(
        self, config_file: str = "config.json", logger: logging.Logger = None
    ) -> None:
        """初期化メソッド

        Args:
            config_file (str): 設定ファイルのパス。デフォルトは 'config.json'。
            logger (logging.Logger): ログ出力用のロガー。
        """
        self.config_file = config_file
        self.logger = logger
        self.toggle_key = None
        self.mouse_button = None
        self._config = None

    def load(self) -> None:
        """設定ファイルを読み込むメソッド

        設定ファイルからトグルキーとマウスボタンの設定を読み込む。

        Raises:
            AutoHoldClickException: 設定ファイルの読み込みに失敗した場合。
        """
        try:
            with open(self.config_file, "r", encoding=self.CONFIG_FILE_ENCODING) as f:
                self._config = json.load(f)
                self.toggle_key = self._get_config_value_as_key(self.TOGGLE_KEY_KEY)
                self.mouse_button = self._get_config_value_as_button(
                    self.MOUSE_BUTTON_KEY
                )
                print(
                    Messages.CONFIG_LOAD_SUCCESS.format(
                        toggle_key=self.toggle_key.name,
                        mouse_button=self.mouse_button.name,
                    )
                )
                log_info(
                    self.logger,
                    Messages.CONFIG_LOAD_SUCCESS.format(
                        toggle_key=self.toggle_key, mouse_button=self.mouse_button
                    ),
                )
        except FileNotFoundError as e:
            raise AutoHoldClickException(
                Messages.CONFIG_FILE_NOT_FOUND.format(file_path=self.config_file)
            ) from e
        except json.JSONDecodeError as e:
            raise AutoHoldClickException(
                Messages.CONFIG_INVALID_JSON.format(file_path=self.config_file)
            ) from e
        except IOError as e:
            raise AutoHoldClickException(
                Messages.CONFIG_LOAD_ERROR.format(error=e)
            ) from e

    def _get_config_value(self, key: str) -> str:
        """設定値を取得するメソッド

        Args:
            key (str): 設定項目のキー。

        Returns:
            str: 設定値。
        """
        value = self._config.get(key)
        if value is None:
            raise AutoHoldClickException(Messages.CONFIG_KEY_NOT_FOUND.format(key=key))
        if value == "":
            raise AutoHoldClickException(Messages.CONFIG_EMPTY_VALUE.format(key=key))
        return value

    def _get_config_value_as_key(self, key: str) -> keyboard.Key:
        """設定値をkeyboard.Keyとして取得するメソッド

        Args:
            key (str): 設定項目のキー。

        Returns:
            keyboard.Key: キー。
        """
        value = self._get_config_value(key)
        try:
            return getattr(keyboard.Key, value.lower())
        except AttributeError as e:
            raise AutoHoldClickException(
                Messages.CONFIG_INVALID_VALUE.format(key=key, value=value)
            ) from e

    def _get_config_value_as_button(self, key: str) -> mouse.Button:
        """設定値をmouse.Buttonとして取得するメソッド

        Args:
            key (str): 設定項目のキー。

        Returns:
            mouse.Button: ボタン。
        """
        value = self._get_config_value(key)
        try:
            return getattr(mouse.Button, value.lower())
        except AttributeError as e:
            raise AutoHoldClickException(
                Messages.CONFIG_INVALID_VALUE.format(key=key, value=value)
            ) from e


class AutoClicker:
    """自動クリックを管理するクラス

    Attributes:
        config (Config): 設定クラスのインスタンス。
        logger (logging.Logger): ログ出力用のロガー。
        mouse_controller (pynput.mouse.Controller): マウス操作用のコントローラー。
        clicking (bool): クリック状態を示すフラグ。
    """

    def __init__(self, config: Config, logger: logging.Logger = None) -> None:
        """初期化メソッド

        Args:
            config (Config): 設定クラスのインスタンス。
            logger (logging.Logger): ログ出力用のロガー。
        """
        self.config = config
        self.logger = logger
        self.mouse_controller = mouse.Controller()
        self.clicking = False

    def run(self) -> None:
        """自動クリックを開始するメソッド

        トグルキーが押されたときにクリックをON/OFFする。
        Ctrl+Cで終了する。
        """
        print(Messages.WAIT_FOR_TOGGLE_KEY)
        log_info(self.logger, Messages.WAIT_FOR_TOGGLE_KEY)
        atexit.register(self.release_click)

        with keyboard.Listener(on_press=self.on_press):
            try:
                while True:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                print(f"\n[{Messages.CTRL_C_PRESSED}]")
                log_info(self.logger, Messages.CTRL_C_PRESSED)
                self.release_click()

    def on_press(self, key: keyboard.Key) -> None:
        """キーが押されたときの処理

        クリック状態を切り替える。
        クリックがONのときはOFFに、OFFのときはONにする。

        Args:
            key (keyboard.Key): 押されたキー。
        """
        if key == self.config.toggle_key:
            if not self.clicking:
                self._start_clicking()
            else:
                self._stop_clicking()

    def release_click(self) -> None:
        """クリックを解除するメソッド

        クリックがONのときはOFFにする。
        """
        if self.clicking:
            self._stop_clicking()

    def _start_clicking(self) -> None:
        """クリックを開始するヘルパーメソッド。"""
        self.mouse_controller.press(self.config.mouse_button)
        self.clicking = True
        print(Messages.CLICK_START.format(button_name=self.config.mouse_button.name))
        log_debug(
            self.logger,
            Messages.CLICK_START_LOG.format(button_name=self.config.mouse_button.name),
        )

    def _stop_clicking(self) -> None:
        """クリックを停止するヘルパーメソッド。"""
        self.mouse_controller.release(self.config.mouse_button)
        self.clicking = False
        print(Messages.CLICK_STOP.format(button_name=self.config.mouse_button.name))
        log_debug(
            self.logger,
            Messages.CLICK_STOP_LOG.format(button_name=self.config.mouse_button.name),
        )


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
    CONFIG_INVALID_JSON = "設定ファイルのJSON形式が正しくありません。パス：{file_path}"
    CONFIG_LOAD_ERROR = "設定ファイルの読み込み中にエラーが発生しました: {error}"
    CONFIG_KEY_NOT_FOUND = "設定項目が見つかりません。設定項目：{key}"
    CONFIG_EMPTY_VALUE = "設定項目の値が空です。設定項目：{key}"
    CONFIG_INVALID_VALUE = "設定項目の値が不正です。設定項目：{key} 設定値：{value}"

    # クリック関連メッセージ
    CLICK_START = "[{button_name}クリック開始]"
    CLICK_STOP = "[{button_name}クリック解除]"
    CLICK_START_LOG = "{button_name}クリックを開始しました。"
    CLICK_STOP_LOG = "{button_name}クリックを解除しました。"

    # ログ関連メッセージ
    LOGGER_LOAD_ERROR = (
        "ログ設定ファイルの読み込み中にエラーが発生しました。パス：{file_path}"
    )
    LOGGER_FILE_NOT_FOUND = "ログ設定ファイルが見つかりません。パス：{file_path}"
    LOGGER_INVALID_JSON = "ログ設定ファイルがJSON形式ではありません。パス：{file_path}"

    # 例外メッセージ
    UNEXPECTED_ERROR = (
        "ツール実行中に予期せぬ例外が発生しました。エラーメッセージ：{error}"
    )
    SPECIFIC_ERROR = "ツール実行中に例外が発生しました。エラーメッセージ：{error}"


class ExitCodes:
    """終了コードを定数として管理するクラス"""

    SUCCESS = 0
    SPECIFIC_ERROR = 1
    UNEXPECTED_ERROR = 2


def get_logger(log_settings_file_path: str) -> logging.Logger:
    """
    ログ設定ファイルを読み込み、ロガーを返す。

    Args:
        log_settings_file_path (String): ログ設定ファイルのパス

    Raises:
        AutoHoldClickException: ログ設定ファイルが存在しない、JSON形式でない、または読み込みエラー発生時

    Returns:
        logging.Logger: ロガー
    """
    try:
        with open(log_settings_file_path, "r", encoding="utf_8") as log_settings_file:
            log_settings = json.load(log_settings_file)
        logging.config.dictConfig(log_settings)
        return logging.getLogger(__name__)
    except FileNotFoundError as e:
        raise AutoHoldClickException(
            Messages.LOGGER_FILE_NOT_FOUND.format(file_path=log_settings_file_path)
        ) from e
    except json.JSONDecodeError as e:
        raise AutoHoldClickException(
            Messages.LOGGER_INVALID_JSON.format(file_path=log_settings_file_path)
        ) from e
    except IOError as e:
        raise AutoHoldClickException(
            Messages.LOGGER_LOAD_ERROR.format(file_path=log_settings_file_path)
        ) from e


def main() -> None:
    """メイン関数"""
    try:
        logger = get_logger("log_settings.json")
    except AutoHoldClickException as e:
        print(Messages.LOGGER_LOAD_ERROR.format(file_path="log_settings.json"))
        print(f"エラーメッセージ：{e}")
        logger = None
    except Exception as e:
        print(Messages.UNEXPECTED_ERROR.format(error=e))
        logger = None

    return_code = ExitCodes.SUCCESS
    try:
        log_info(logger, Messages.START_PROCESS)
        config = Config(logger=logger)
        config.load()

        auto_clicker = AutoClicker(config=config, logger=logger)
        auto_clicker.run()
    except AutoHoldClickException as e:
        log_exception(logger, Messages.SPECIFIC_ERROR.format(error=e))
        return_code = ExitCodes.SPECIFIC_ERROR
    except Exception as e:
        log_exception(logger, Messages.UNEXPECTED_ERROR.format(error=e))
        return_code = ExitCodes.UNEXPECTED_ERROR
    finally:
        log_info(logger, Messages.END_PROCESS)

    sys.exit(return_code)


def log_info(logger: logging.Logger, message: str) -> None:
    """INFOログ出力メソッド

    Args:
        message (str): ログメッセージ。
    """
    if logger:
        logger.info(message)


def log_exception(logger: logging.Logger, message: str) -> None:
    """EXCEPTIONログ出力メソッド

    Args:
        message (str): ログメッセージ。
    """
    if logger:
        logger.exception(message)


def log_debug(logger: logging.Logger, message: str) -> None:
    """DEBUGログ出力メソッド

    Args:
        message (str): ログメッセージ。
    """
    if logger:
        logger.debug(message)


if __name__ == "__main__":
    main()
