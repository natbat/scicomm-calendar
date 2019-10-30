import unittest
import json
import unicodedata
import re
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

    def test_rule_empty_list_means_wildcard(self):
        screen_name = "AllYourHedgehogs"
        full_text = "One hedgehog to rule them all!"
        rules = {"allyourhedgehogs": []}
        self.assertTrue(tweet_matches_rules(screen_name, full_text, rules))



class TestSanityCheckConfig(unittest.TestCase):

    def test_config_is_valid_json(self):
        try:
            json.load(open('config.json'))
        except ValueError as e:
            self.fail('Invalid JSON in config file')

    def test_config_has_no_weird_characters(self):
        """
        On occasion, editing code on a phone can accidentally introduce weird
        invisible characters which break the bot. Check that the config file
        only includes alphanumeric characters and JSON punctuation.
        """
        allowed_chars_regex = re.compile(r'[^a-zA-Z0-9\[\]\{\}\s":,_]')
        with open('config.json') as fp:
            contents = fp.read().decode('utf8')
        match = allowed_chars_regex.search(contents)
        if match:
            weird_char = match.group(0)
            line_number = contents[:match.start()].count('\n') + 1
            self.fail('config.json contains a weird character on line %d: %s %r' % (
                line_number, unicodedata.name(weird_char), weird_char
            ))


if __name__ == '__main__':
    unittest.main()
