"""auto_hold_click/main.py

Copyright (c) 2026 Shinoryo
Licensed under the MIT License
"""

import argparse
import json
import logging
import logging.config
import sys
from pathlib import Path

from auto_clicker import AutoClicker
from exceptions import AutoHoldClickError
from exit_codes import ExitCodes
from logger import LoggerHelper
from messages import Messages

from config import Config


def get_logger(log_settings_file_path: str) -> logging.Logger:
    """
    ログ設定ファイルを読み込み、ロガーを返す。

    Args:
        log_settings_file_path (str): ログ設定ファイルのパス

    Returns:
        logging.Logger: 設定済みのロガー

    Raises:
        AutoHoldClickError:
            ログ設定ファイルが存在しない、
            JSON形式でない、
            または読み込みエラー発生時
    """
    try:
        with Path.open(log_settings_file_path, encoding="utf-8") as log_settings_file:
            log_settings = json.load(log_settings_file)
        logging.config.dictConfig(log_settings)
        return logging.getLogger(__name__)
    except FileNotFoundError as e:
        raise AutoHoldClickError(
            Messages.LOGGER_FILE_NOT_FOUND.format(file_path=log_settings_file_path),
        ) from e
    except json.JSONDecodeError as e:
        raise AutoHoldClickError(
            Messages.LOGGER_INVALID_JSON.format(file_path=log_settings_file_path),
        ) from e
    except OSError as e:
        raise AutoHoldClickError(
            Messages.LOGGER_LOAD_IO_ERROR.format(file_path=log_settings_file_path),
        ) from e


def parse_arguments() -> argparse.Namespace:
    """
    コマンドライン引数をパースする。

    Returns:
        argparse.Namespace: パースされた引数

    Raises:
        SystemExit: 必須引数が不足している場合
    """
    parser = argparse.ArgumentParser(
        description="AutoHoldClick",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="設定ファイルのパス (必須)",
        metavar="CONFIG_FILE",
    )
    parser.add_argument(
        "--log-settings",
        type=str,
        required=False,
        help=(
            "ログ設定ファイルのパス (任意)。"
            "指定しない場合は標準出力のみでログファイルは生成されません。"
        ),
        metavar="LOG_CONFIG_FILE",
    )

    args, _ = parser.parse_known_args()
    return args


def initialize_logger(log_file_path: str | None) -> logging.Logger | None:
    """
    ロガーを初期化する。

    Args:
        log_file_path (str | None): ログ設定ファイルのパス

    Returns:
        logging.Logger | None: 初期化されたロガー
    """
    logger = None
    if log_file_path:
        try:
            logger = get_logger(log_file_path)
        except AutoHoldClickError as e:
            print(Messages.LOGGER_LOAD_SPECIFIC_ERROR.format(file_path=log_file_path))
            print(f"エラーメッセージ: {e}")
            logger = None
        except Exception as e:
            print(Messages.LOGGER_LOAD_UNEXPECTED_ERROR.format(file_path=log_file_path))
            print(f"エラーメッセージ: {e}")
            logger = None
    return logger


def main() -> None:
    """
    AutoHoldClickのメイン処理を実行する。

    Returns:
        None
    """
    logger_helper = None
    return_code = ExitCodes.SUCCESS

    # 引数の取得と設定ファイルパスの抽出
    args = parse_arguments()
    log_file_path = args.log_settings
    config_file_path = args.config

    try:
        # ロガーの初期化(ファイル指定時はファイル設定、未指定時は標準出力のみ)
        logger = initialize_logger(log_file_path)
        logger_helper = LoggerHelper(logger)

        # 処理開始ログ
        logger_helper.info(Messages.START_PROCESS)

        # 設定ファイルの読み込み
        config = Config(logger_helper=logger_helper, config_file=config_file_path)
        config.load()

        # AutoClickerのインスタンス化と実行
        auto_clicker = AutoClicker(config=config, logger=logger)
        auto_clicker.run()
    except AutoHoldClickError as e:
        # 想定された例外のログ出力と終了コード設定
        logger_helper.exception(Messages.SPECIFIC_ERROR.format(error=e))
        return_code = ExitCodes.SPECIFIC_ERROR
    except Exception as e:
        # 想定外の例外のログ出力と終了コード設定
        logger_helper.exception(Messages.UNEXPECTED_ERROR.format(error=e))
        return_code = ExitCodes.UNEXPECTED_ERROR
    finally:
        # プログラム終了時の後処理
        logger_helper.info(Messages.END_PROCESS)

    sys.exit(return_code)


if __name__ == "__main__":
    main()
