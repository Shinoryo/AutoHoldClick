class AutoHoldClickException(Exception):
    """AutoHoldClickの独自例外クラス"""
    def __init__(self, message):
        super().__init__(message)
