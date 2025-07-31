
import json

from exceptions import AutoHoldClickException
from logger import LoggerHelper
from messages import Messages
from pynput import keyboard, mouse


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
        self, config_file: str = "config\config.json", logger=None
    ) -> None:
        """初期化メソッド

        Args:
            config_file (str): 設定ファイルのパス。デフォルトは 'config.json'。
            logger (logging.Logger): ログ出力用のロガー。
        """
        self.config_file = config_file
        self.logger_helper = LoggerHelper(logger)
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
                self.logger_helper.info(
                    Messages.CONFIG_LOAD_SUCCESS.format(
                        toggle_key=self.toggle_key.name,
                        mouse_button=self.mouse_button.name,
                    )
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
                Messages.CONFIG_LOAD_IO_ERROR.format(error=e)
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
