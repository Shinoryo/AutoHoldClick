import logging
import sys


class LoggerHelper:
    """
    ログ出力を補助するクラス。

    logging.Logger オブジェクトをラップし、
    info/debug/exceptionの各ログ出力メソッドを提供します。
    loggerがNoneの場合はprintで出力します。

    Args:
        logger (Optional[logging.Logger]): ログ出力に使用するLogger。
            Noneの場合はprint出力。
    """

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """
        Args:
            logger (Optional[logging.Logger]):
                ログ出力に使用するLogger。Noneの場合はprint出力。
        """
        self.logger = logger

    def info(self, message: str) -> None:
        """
        INFOレベルのログを出力します。

        Args:
            message (str): ログメッセージ。
        """
        if self.logger:
            self.logger.info(message)
        else:
            print(f"[INFO] {message}")

    def exception(self, message: str) -> None:
        """
        例外情報を含むログを出力します。

        Args:
            message (str): ログメッセージ。
        """
        if self.logger:
            self.logger.exception(message)
        else:
            print(f"[EXCEPTION] {message}", file=sys.stderr)

    def debug(self, message: str) -> None:
        """
        DEBUGレベルのログを出力します。

        Args:
            message (str): ログメッセージ。
        """
        if self.logger:
            self.logger.debug(message)
        else:
            print(f"[DEBUG] {message}")
