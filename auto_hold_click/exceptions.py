"""auto_hold_click/exceptions.py

Copyright (c) 2026 Shinoryo
Licensed under the MIT License
"""

class AutoHoldClickError(Exception):
    """
    AutoHoldClick用の独自例外クラス。

    Args:
        message (str): 例外メッセージ。
    """
    def __init__(self, message: str) -> None:
        """
        Args:
            message (str): 例外メッセージ。
        """
        super().__init__(message)
