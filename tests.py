import unittest
from scan_and_retweet import tweet_matches_rules

class TestTweetMatchesRules(unittest.TestCase):

    # All hashtags by the time they get to the tweet_matches_rules have been 
    # already lowercased, so no need to test that

    def test_basicRetweet(self):
        screen_name = "natbat"
        full_text = "I like #hedgehogs"
        rules = {"natbat": ["hedgehogs"]}
        self.assertTrue(tweet_matches_rules(screen_name, full_text, rules))

    def test_basicRetweetCaps(self):
        screen_name = "natbat"
        full_text = "I like #HedgehogOrNot"
        rules = {"natbat": ["hedgehogornot"]}
        self.assertTrue(tweet_matches_rules(screen_name, full_text, rules))

    def test_basicNoRetweet(self):
        screen_name = "natbat"
        full_text = "I like Racoons"
        rules = {"natbat": ["hedgehogornot"]}
        self.assertFalse(tweet_matches_rules(screen_name, full_text, rules))

    def test_noHashNoRetweet(self):
        screen_name = "natbat"
        full_text = "I like HedgehogOrNot"
        rules = {"natbat": ["hedgehogornot"]}
        self.assertFalse(tweet_matches_rules(screen_name, full_text, rules))


    # TODO break if the config file is valid

if __name__ == '__main__':
    unittest.main()