import datetime
import os
from process_comments import update_comments_csv
from process_symbols import process_symbols_df, SYMBOLS_PATH
from slack_message import send_file, send_notification

if __name__ == '__main__':
    try:
        update_comments_csv()
        process_symbols_df()
        symbols_df_path = SYMBOLS_PATH.format(datetime=datetime.datetime.now().strftime("%Y_%m_%d_%H"))
        if os.path.exists(symbols_df_path):
            send_file(symbols_df_path)
        else:
            send_notification('SYMBOLS DF WASNT CREATED')
    except Exception as e:
        send_notification(message="Hourly run failed \n Exception: {}".format(str(e)))
