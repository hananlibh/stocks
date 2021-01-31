import datetime
import json
import logging
import os
import schedule
import logging
import logging.config
import time

from process_comments import update_comments_csv
from process_symbols import process_symbols_df, SYMBOLS_PATH
from slack_message import send_file, send_notification

logger = logging.getLogger(__name__)


def main_function():
    try:
        comments_df = update_comments_csv()
        if comments_df is None:
            logger.info("No daily discussion")
            return None
        process_symbols_df(comments_df)
        symbols_df_path = SYMBOLS_PATH.format(datetime=datetime.datetime.now().strftime("%Y_%m_%d_%H"))
        if os.path.exists(symbols_df_path):
            send_file(symbols_df_path)
        else:
            send_notification('SYMBOLS DF WASNT CREATED')
    except Exception as e:
        logger.info('Main Error', exc_info=True)
        send_notification(message="Hourly run failed \n Exception: {}".format(str(e)))


def init_logger():
    with open('logger_config.json') as logger_config_file:
        config_dict = json.load(logger_config_file)
    logging.config.dictConfig(config_dict)


if __name__ == '__main__':
    init_logger()
    schedule.every().hour.do(main_function)
    while True:
        schedule.run_pending()
        time.sleep(1)
