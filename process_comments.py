import praw
import datetime
from Comment import RedditComment
import pandas as pd
import os
from typing import List

WALLSTREETBETS_SUBREDDIT = "wallstreetbets"
COMMENTS_PATH = 'daily_comments/wallstreetbets_{day}.csv'
DAILY_DISCUSSION = f'Daily Discussion Thread for {datetime.datetime.now().strftime("%B %d, %Y")}'
WEEKEND_DISCUSSION = f'Weekend Discussion Thread for the Weekend of '

reddit = praw.Reddit(
    client_id="Fs5hchYYgDmXfQ",
    client_secret="4dlFt60-aPJvwpuDHMqy_YzeQnstbw",
    user_agent="testscript by u/alextesy"
)


def get_daily_discussion():
    # Assuming that daily discussion is always in the top 5
    hot_submissions = list(reddit.subreddit(WALLSTREETBETS_SUBREDDIT).hot(limit=5))
    for submission in hot_submissions:
        # Daily Discussion Thread for January 29, 2021 - Pt. II
        if DAILY_DISCUSSION in submission.title or WEEKEND_DISCUSSION in submission.title:
            return submission


def process_comments() -> List[dict]:
    submission = get_daily_discussion()
    submission.comments.replace_more(limit=0)
    comments_list = []
    # This is giving us only top level comments not the full comment tree:
    # https://praw.readthedocs.io/en/latest/tutorials/comments.html
    # Fails to bring all the comments
    # TODO: check multi processing to query multiple times
    for i, comment in enumerate(submission.comments):
        if i % 50 == 0:
            print(f'Processing {i}s comment')
        if comment.body != '[deleted]':
            comments_list.append(RedditComment(comment).to_dict())
    return comments_list


def update_comments_csv():
    comments_path = COMMENTS_PATH.format(day=datetime.datetime.now().strftime("%Y_%m_%d"))
    if os.path.exists(comments_path):
        df_results = pd.read_csv(comments_path, index_col=0)
    else:
        df_results = pd.DataFrame({'author': pd.Series([], dtype='str'),
                                   'body': pd.Series([], dtype='str'),
                                   'created_time': pd.Series([], dtype='datetime64[ns]'),
                                   'symbols': pd.Series([], dtype='str'),  # as str for csv to save easily
                                   'score': pd.Series([], dtype='float')})
    new_df = pd.DataFrame(process_comments())
    df_results = df_results.append(new_df).drop_duplicates(subset=['author', 'created_time'])
    safely_create_folder(comments_path.split('/')[0])
    df_results.to_csv(comments_path)


def process_companies():
    comments_path = COMMENTS_PATH.format(day=datetime.datetime.now().strftime("%Y_%m_%d"))
    comments = pd.read_csv(comments_path)
    comments.groupby([comments.created_time.hour])


def safely_create_folder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
