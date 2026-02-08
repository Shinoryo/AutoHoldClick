"""auto_hold_click/exit_codes.py

Copyright (c) 2026 Shinoryo
Licensed under the MIT License
"""

class ExitCodes:
    """
    終了コードを定数として管理するクラス。

    Attributes:
        SUCCESS (int): 正常終了。
        SPECIFIC_ERROR (int): 特定のエラー。
        UNEXPECTED_ERROR (int): 予期しないエラー。
    """

    SUCCESS: int = 0  # 正常終了
    SPECIFIC_ERROR: int = 1  # 特定のエラー
    UNEXPECTED_ERROR: int = 2  # 予期しないエラー
