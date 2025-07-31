import atexit
import logging
import time

from pynput import keyboard, mouse

from .config import Config
from .logger import LoggerHelper
from .messages import Messages


class AutoClicker:
    """自動クリックを管理するクラス

    Attributes:
        config (Config): 設定クラスのインスタンス。
        logger (logging.Logger): ログ出力用のロガー。
        mouse_controller (pynput.mouse.Controller): マウス操作用のコントローラー。
        clicking (bool): クリック状態を示すフラグ。
    """

    def __init__(self, config: Config, logger: logging.Logger) -> None:
        """初期化メソッド

        Args:
            config (Config): 設定クラスのインスタンス。
            logger (logging.Logger): ログ出力用のロガー。
        """
        self.config = config
        self.logger_helper = LoggerHelper(logger)
        self.mouse_controller = mouse.Controller()
        self.clicking = False

    def run(self) -> None:
        """自動クリックを開始するメソッド

        トグルキーが押されたときにクリックをON/OFFする。
        Ctrl+Cで終了する。
        """
        self.logger_helper.info(Messages.WAIT_FOR_TOGGLE_KEY)
        atexit.register(self.release_click)

        with keyboard.Listener(on_press=self.on_press):
            try:
                while True:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                print(f"\n[{Messages.CTRL_C_PRESSED}]")
                self.logger_helper.info(Messages.CTRL_C_PRESSED)
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
        """
        クリック状態がONならOFFにする。
        プログラム終了時の後処理用。
        """
        if self.clicking:
            self._stop_clicking()

    def _start_clicking(self) -> None:
        """
        マウスボタンを押し続ける状態にする。
        """
        self.mouse_controller.press(self.config.mouse_button)
        self.clicking = True
        self.logger_helper.debug(
            Messages.CLICK_START_LOG.format(button_name=self.config.mouse_button.name)
        )

    def _stop_clicking(self) -> None:
        """
        マウスボタンの押下を解除する。
        """
        self.mouse_controller.release(self.config.mouse_button)
        self.clicking = False
        self.logger_helper.debug(
            Messages.CLICK_STOP_LOG.format(button_name=self.config.mouse_button.name)
        )
