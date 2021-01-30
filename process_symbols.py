import datetime
import pandas as pd
from process_comments import COMMENTS_PATH
SYMBOLS_PATH = 'daily_comments/wallstreetbets_symbols_{datetime}.csv'


def get_symbols_df():
    comments_df = pd.read_csv(COMMENTS_PATH.format(day=datetime.datetime.now().strftime("%Y_%m_%d")), index_col=0)
    comments_df.dropna(subset=['symbols'], inplace=True)
    symbols_df = comments_df.assign(symbols=comments_df.symbols.str.split('_')).explode('symbols').reset_index(drop=True)
    return symbols_df.drop(['body'], axis=1)


def process_symbols_df():
    df = pd.DataFrame()
    symbols_df = get_symbols_df()
    symbols_groupby = symbols_df.groupby('symbols')
    df['total_mentions'] = symbols_groupby['author'].count()
    df['total_users_mentioned'] = symbols_groupby['author'].nunique()
    symbols_df['created_time'] = pd.to_datetime(symbols_df['created_time'])
    symbols_df_hour = symbols_df[symbols_df.created_time > datetime.datetime.now() - datetime.timedelta(hours=1)]
    symbols_hour_groupby = symbols_df_hour.groupby('symbols')
    df['hourly_mentions'] = symbols_hour_groupby['author'].count()
    df['hourly_users_mentioned'] = symbols_hour_groupby['author'].nunique()
    df.to_csv(SYMBOLS_PATH.format(datetime=datetime.datetime.now().strftime("%Y_%m_%d_%H")))
