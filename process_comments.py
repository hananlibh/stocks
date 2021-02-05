import praw
import datetime
from Comment import RedditComment
import pandas as pd
import os
from typing import List, Union
import logging

WALLSTREETBETS_SUBREDDIT = "wallstreetbets"
COMMENTS_PATH = 'daily_comments/wallstreetbets_{day}.csv'
DAILY_DISCUSSION = f'Daily Discussion Thread for {datetime.datetime.now().strftime("%B %d, %Y")}'
WEEKEND_DISCUSSION = f'Weekend Discussion Thread for the Weekend of '

logger = logging.getLogger(__name__)

reddit = praw.Reddit(
    client_id="Fs5hchYYgDmXfQ",
    client_secret="4dlFt60-aPJvwpuDHMqy_YzeQnstbw",
    user_agent="testscript by u/alextesy"
)


def get_daily_discussion():
    # Assuming daily discussion is always hottest
    hot_submissions = list(reddit.subreddit(WALLSTREETBETS_SUBREDDIT).hot(limit=3))
    return hot_submissions[0]
    # TODO: Resolve what to do with other submissions
    # for submission in hot_submissions:
    #     # Daily Discussion Thread for January 29, 2021 - Pt. II
    #     if DAILY_DISCUSSION in submission.title or WEEKEND_DISCUSSION in submission.title:
    #         return submission


def process_comments() -> Union[List[dict], None]:
    submission = get_daily_discussion()
    if not submission:
        return None
    submission.comments.replace_more(limit=0)
    comments_list = []
    # This is giving us only top level comments not the full comment tree:
    # https://praw.readthedocs.io/en/latest/tutorials/comments.html
    # Fails to bring all the comments
    # TODO: check multi processing to query multiple times
    for i, comment in enumerate(submission.comments):
        if i % 50 == 0:
            logger.info(f'Processing {i}s comment')
        if comment.body != '[deleted]' and comment.author is not None:
            comments_list.append(RedditComment(comment).to_dict())
    return comments_list


def update_comments_csv():
    comments_path = COMMENTS_PATH.format(day=datetime.datetime.now().strftime("%Y_%m_%d"))
    if os.path.exists(comments_path):
        df_results = pd.read_csv(comments_path, index_col=0)
        logger.info("Daily comment file found, updating")
    else:
        df_results = pd.DataFrame({'author': pd.Series([], dtype='str'),
                                   'body': pd.Series([], dtype='str'),
                                   'created_time': pd.Series([], dtype='datetime64[ns]'),
                                   'symbols': pd.Series([], dtype='str'),  # as str for csv to save easily
                                   'score': pd.Series([], dtype='float')})
        logger.info("Creating new daily comment file")
    comments_list = process_comments()
    if comments_list is None:
        return None
    new_df = pd.DataFrame(comments_list)
    df_results = df_results.append(new_df).drop_duplicates(subset=['author', 'created_time'])
    safely_create_folder(comments_path.split('/')[0])
    df_results.to_csv(comments_path)
    return df_results


def safely_create_folder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
