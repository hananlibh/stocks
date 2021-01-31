import datetime
from symbol_scraper import get_companies_df
from nltk.corpus import stopwords
import re

STOP_WORDS = set(stopwords.words('english'))
SYMBOLS = list(get_companies_df().company_ticker)  # to be queried only once


class RedditComment:
    def __init__(self, praw_comment):
        self.author_name = praw_comment.author.name
        self.body = praw_comment.body
        self.created_time = datetime.datetime.fromtimestamp(praw_comment.created_utc)
        self.score = praw_comment.score
        self.symbols = set(self.extract_symbols(self.body))

    def __eq__(self, other):
        if not isinstance(other, RedditComment):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.author_name == other.author_name and self.created_time == other.created_time

    def to_dict(self):
        return {
            'author': self.author_name,
            'body': self.body,
            'created_time': self.created_time,
            'score': self.score,
            'symbols': '_'.join(self.symbols) if len(self.symbols) > 0 else ''
        }

    @classmethod
    def extract_symbols(cls, text):
        user_symbols = []
        text_withour_special_charecters = re.sub('[^A-Za-z0-9 ]+', '', text)
        text_list = text_withour_special_charecters.split()
        text_list = [word for word in text_list if word.lower() not in STOP_WORDS]
        for symbol in SYMBOLS:
            if len(symbol) == 1:
                # Ignore one letter symbols for now
                continue
            for word in text_list:
                # Examples: Let Go NOK | $BB, $NOK, $AMC LET'S GO | Tomorrow nok will fly to the moon 🚀🚀🚀🚀
                if symbol == word or f'${symbol.lower()}' == word.lower():
                    user_symbols.append(symbol)
        return user_symbols

