"""AutoHoldClick

Copyright (c) 2025 Shinoryo
Licensed under the MIT License
"""

import argparse
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
        log_settings_file_path (str): ログ設定ファイルのパス

    Returns:
        logging.Logger: 設定済みのロガー

    Raises:
        AutoHoldClickException: ログ設定ファイルが存在しない、JSON形式でない、または読み込みエラー発生時
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


def parse_arguments() -> argparse.Namespace:
    """
    コマンドライン引数をパースする。

    Returns:
        argparse.Namespace: パースされた引数
    """
    parser = argparse.ArgumentParser(description="AutoHoldClick")
    parser.add_argument(
        "--config", type=str, required=True, help="設定ファイルのパス (必須)"
    )
    parser.add_argument(
        "--log-settings",
        type=str,
        required=False,
        help="ログ設定ファイルのパス (任意)。指定しない場合は標準出力のみでログファイルは生成されません。",
    )
    # 未定義の引数が指定されても無視する
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
        except AutoHoldClickException as e:
            print(Messages.LOGGER_LOAD_SPECIFIC_ERROR.format(file_path=log_file_path))
            print(f"エラーメッセージ：{e}")
            logger = None
        except Exception as e:
            print(Messages.LOGGER_LOAD_UNEXPECTED_ERROR.format(file_path=log_file_path))
            print(f"エラーメッセージ：{e}")
            logger = None
    return logger


def main() -> None:
    """
    AutoHoldClickのメイン処理を実行する。

    Returns:
        None
    """
    try:
        # 引数の取得と設定ファイルパスの抽出
        args = parse_arguments()
        log_file_path = args.log_settings
        config_file_path = args.config

        # ロガーの初期化（ファイル指定時はファイル設定、未指定時は標準出力のみ）
        logger = initialize_logger(log_file_path)
        logger_helper = LoggerHelper(logger)
        return_code = ExitCodes.SUCCESS

        # プロセス開始ログ（処理開始の記録）
        logger_helper.info(Messages.START_PROCESS)

        # 設定ファイルのロード（ユーザー設定の反映）
        config = Config(logger_helper=logger_helper, config_file=config_file_path)
        config.load()

        # 自動クリック処理の実行（メイン機能）
        auto_clicker = AutoClicker(config=config, logger=logger)
        auto_clicker.run()
    except AutoHoldClickException as e:
        # 想定された例外のログ出力と終了コード設定
        logger_helper.exception(Messages.SPECIFIC_ERROR.format(error=e))
        return_code = ExitCodes.SPECIFIC_ERROR
    except Exception as e:
        # 想定外の例外のログ出力と終了コード設定
        logger_helper.exception(Messages.UNEXPECTED_ERROR.format(error=e))
        return_code = ExitCodes.UNEXPECTED_ERROR
    finally:
        # プロセス終了ログ（処理終了の記録）
        logger_helper.info(Messages.END_PROCESS)

    sys.exit(return_code)


if __name__ == "__main__":
    main()
