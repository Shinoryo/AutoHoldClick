import sys


class LoggerHelper:
    """
    ログ出力を補助するオブジェクト指向クラス。
    logger: logging.Logger をラップし、info/debug/exception出力を提供。
    loggerがNoneの場合はprint出力。
    """
    def __init__(self, logger=None):
        self.logger = logger

    def info(self, message: str) -> None:
        """INFOログ出力メソッド"""
        if self.logger:
            self.logger.info(message)
        else:
            print(f"[INFO] {message}")

    def exception(self, message: str) -> None:
        """EXCEPTIONログ出力メソッド"""
        if self.logger:
            self.logger.exception(message)
        else:
            print(f"[EXCEPTION] {message}", file=sys.stderr)

    def debug(self, message: str) -> None:
        """DEBUGログ出力メソッド"""
        if self.logger:
            self.logger.debug(message)
        else:
            print(f"[DEBUG] {message}")
