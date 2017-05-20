import json
import time
import os

import requests
import twitter


api = twitter.Api(
    tweet_mode='extended',
    consumer_key=os.environ['CONSUMER_KEY'],
    consumer_secret=os.environ['CONSUMER_SECRET'],
    access_token_key=os.environ['ACCESS_TOKEN_KEY'],
    access_token_secret=os.environ['ACCESS_TOKEN_SECRET'],
)


def fetch_rules():
    return json.loads(
        # Read the local config file and convert to lower case
        open("config.json").read().lower()
    )


def tweet_matches_rules(tweet, rules):
    # Extract information about the tweet
    screen_name = tweet.user.screen_name.lower()
    text = tweet.full_text.lower()

    if screen_name in rules:

        # For this User, what list of hashtags are we looking at
        hashtags = rules[screen_name]

        # If any of the above hashtags is present in the text then it matches
        for hashtag in hashtags:
            if hashtag in text:
                return True

    # If we get here then no hashtags matched that tweet for that usert
    return False


def scan_and_retweet():
    # Fetch 200 recent tweets from users we follow
    tweets = api.GetHomeTimeline(count=200)
    print "Fetched %d tweets" % len(tweets)

    # Fetch our rules from github
    rules = fetch_rules()
    print "Fetched %d rules" % len(rules)

    # For every tweet, see if it matches a rule
    for tweet in reversed(tweets):
        print
        print "CONSIDER @%s \"%r\"" % (tweet.user.screen_name, tweet.full_text)

        # Have we retweeted this already?
        if tweet.retweeted:
            print "  SKIPPING, we have retweeted already"
            continue

        # Does it match a rule?
        elif tweet_matches_rules(tweet, rules):
            print "  TWEETING Matched a rule! Gonna retweet it"
            # Retweet it!
            print api.PostRetweet(tweet.id)
            # Sleep before next possible retweet
            time.sleep(2.5)


if __name__ == '__main__':
    scan_and_retweet()
