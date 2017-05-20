import unittest
from scan_and_retweet import tweet_matches_rules

class TestTweetMatchesRules(unittest.TestCase):

    def test_basic(self):
        screen_name = "natbat"
        full_text = "I like #hedgehogs"
        rules = {"natbat": ["hedgehogs"]}
        self.assertTrue(tweet_matches_rules(screen_name, full_text, rules))


# TODO break if the config file is valid

if __name__ == '__main__':
    unittest.main()