import os
from configparser import ConfigParser
from praw import Reddit
from tqdm import tqdm

class Upvoter:
    _api = None

    @property
    def api(self):
        if not self._api:
            self._api = Reddit(client_id=self.config['reddit']['client_id'],
                               client_secret=self.config['reddit']['client_secret'],
                               user_agent=self.config['reddit']['user_agent'],
                               username=self.config['reddit']['username'],
                               password=self.config['reddit']['password'])

        return self._api

    def upvote(self):
        for submission in self.api.subreddit(self.config['reddit']['subreddit']).stream.submissions():
            print('Processing thread {}.'.format(submission.title))
            submission.upvote()
            for comment in tqdm(submission.comments):
                comment.upvote()
            print()

    def __init__(self, settings='settings.ini'):
        self.config = ConfigParser(os.environ)
        self.config.read(settings)


if __name__ == '__main__':
    upvoter = Upvoter()
    upvoter.upvote()
