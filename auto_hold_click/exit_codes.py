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
