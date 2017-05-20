import unittest
from scan_and_retweet import tweet_matches_rule


class FakeUser(object):
    def __init__(self, screen_name):
        self.screen_name = screen_name


class FakeTweet(object):
    def __init__(self, screen_name, full_text):
        self.user = FakeUser(screen_name)
        self.full_text = full_text


class TestTweetMatchesRule(unittest.TestCase):
    def test_basic(self):
        tweet = FakeTweet('natbat', 'I like #hedgehogs')
        rule = {'user': 'natbat', 'hashtag': 'hedgehogs'}
        self.assertTrue(tweet_matches_rule(tweet, rule))


if __name__ == '__main__':
    unittest.main()