"""AutoHoldClick

Copyright (c) 2025 Shinoryo
Licensed under the MIT License
"""

import json
import logging
import logging.config
import sys

from auto_clicker import AutoClicker
from exceptions import AutoHoldClickException
from exit_codes import ExitCodes
from logger import LoggerHelper
from messages import Messages

from config import Config


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
        with open(log_settings_file_path, "r", encoding="utf-8") as log_settings_file:
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
            Messages.LOGGER_LOAD_IO_ERROR.format(file_path=log_settings_file_path)
        ) from e


def main() -> None:
    """メイン関数"""
    log_file_path = "config\log_settings.json"
    try:
        logger = get_logger(log_file_path)
    except AutoHoldClickException as e:
        print(Messages.LOGGER_LOAD_SPECIFIC_ERROR.format(file_path=log_file_path))
        print(f"エラーメッセージ：{e}")
        logger = None
    except Exception as e:
        print(
            Messages.LOGGER_LOAD_UNEXPECTED_ERROR.format(file_path="log_settings.json")
        )
        print(f"エラーメッセージ：{e}")
        logger = None

    logger_helper = LoggerHelper(logger)
    return_code = ExitCodes.SUCCESS
    try:
        logger_helper.info(Messages.START_PROCESS)
        config = Config(logger=logger)
        config.load()

        auto_clicker = AutoClicker(config=config, logger=logger)
        auto_clicker.run()
    except AutoHoldClickException as e:
        logger_helper.exception(Messages.SPECIFIC_ERROR.format(error=e))
        return_code = ExitCodes.SPECIFIC_ERROR
    except Exception as e:
        logger_helper.exception(Messages.UNEXPECTED_ERROR.format(error=e))
        return_code = ExitCodes.UNEXPECTED_ERROR
    finally:
        logger_helper.info(Messages.END_PROCESS)

    sys.exit(return_code)


if __name__ == "__main__":
    main()
