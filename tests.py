import unittest
from scan_and_retweet import tweet_matches_rules


class FakeUser(object):
    def __init__(self, screen_name):
        self.screen_name = screen_name


class FakeTweet(object):
    def __init__(self, screen_name, full_text):
        self.user = FakeUser(screen_name)
        self.full_text = full_text


class TestTweetMatchesRules(unittest.TestCase):
    def test_basic(self):
        tweet = FakeTweet('natbat', 'I like #hedgehogs')
        rules = {"natbat": ["hedgehogs"]}
        self.assertTrue(tweet_matches_rules(tweet, rules))


# TODO break if the config file is valid

if __name__ == '__main__':
    unittest.main()