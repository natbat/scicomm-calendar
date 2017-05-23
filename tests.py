import unittest
from scan_and_retweet import tweet_matches_rules

class TestTweetMatchesRules(unittest.TestCase):

    # All hashtags by the time they get to the tweet_matches_rules have been 
    # already lowercased, so no need to test that

    def test_rule(self):
        screen_name = "natbat"
        full_text = "I like #hedgehogs"
        rules = {"natbat": ["hedgehogs"]}
        self.assertTrue(tweet_matches_rules(screen_name, full_text, rules))

    def test_rule_case_insensitive_hashtag(self):
        screen_name = "natbat"
        full_text = "I like #HedgehogOrNot"
        rules = {"natbat": ["hedgehogornot"]}
        self.assertTrue(tweet_matches_rules(screen_name, full_text, rules))

    def test_rule_case_insensitive_screen_name(self):
        screen_name = "NatBat"
        full_text = "I like #HedgehogOrNot"
        rules = {"natbat": ["hedgehogornot"]}
        self.assertTrue(tweet_matches_rules(screen_name, full_text, rules))

    def test_rule_no_matching_hashtag(self):
        screen_name = "natbat"
        full_text = "I like Racoons"
        rules = {"natbat": ["hedgehogornot"]}
        self.assertFalse(tweet_matches_rules(screen_name, full_text, rules))

    def test_rule_no_matching_screen_name(self):
        screen_name = "frog"
        full_text = "I like #hedgehogornot"
        rules = {"natbat": ["hedgehogornot"]}
        self.assertFalse(tweet_matches_rules(screen_name, full_text, rules))

    def test_rule_no_hash_on_hashtag(self):
        screen_name = "natbat"
        full_text = "I like HedgehogOrNot"
        rules = {"natbat": ["hedgehogornot"]}
        self.assertFalse(tweet_matches_rules(screen_name, full_text, rules))


if __name__ == '__main__':
    unittest.main()