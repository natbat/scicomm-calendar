import json
import time
import os
import sys

Hello from Simon!

import requests
import twitter

# Number of home timeline tweets to fetch in each batch of pagination
BATCH_SIZE = 200


def fetch_rules():
    return json.loads(
        # Read the local config file and convert to lower case
        open("config.json").read().lower()
    )


def tweet_matches_rules(screen_name, full_text, rules):
    # Extract information about the tweet
    screen_name = screen_name.lower()
    full_text = full_text.lower()

    if screen_name in rules:

        # For this User, what list of hashtags are we looking at
        hashtags = rules[screen_name]

        # Retweet everything from an account if we have configured it
        # with a wildcard, represented as an empty list
        if [] == hashtags:
            return True

        # If any of the above hashtags is present in the text then it matches
        for hashtag in hashtags:
            if ("#"+hashtag) in full_text:
                return True

    # If we get here then no hashtags matched that tweet for that usert
    return False


def get_tweets(api, num_pages_to_fetch=1):
    # Fetch BATCH_SIZE recent tweets from users we follow
    max_id = None
    tweets = []
    for i in range(num_pages_to_fetch):
        print 'max_id: %r' % max_id
        tweets.extend(
            api.GetHomeTimeline(
                count=BATCH_SIZE,
                max_id=max_id
            )
        )
        max_id = min([tweet.id for tweet in tweets]) - 1
    print "FETCHED %d tweets" % len(tweets)
    print
    return tweets


def scan_and_retweet(tweets):
    # Fetch our rules
    rules = fetch_rules()
    print "LOADED %d rules" % len(rules)

    # For every tweet, see if it matches a rule
    for tweet in reversed(tweets):
        print
        print tweet.AsJsonString()
        print "CONSIDER @%s \"%r\"" % (tweet.user.screen_name, tweet.full_text)

        # Have we retweeted this already?
        if tweet.retweeted:
            print "...  SKIPPING, we have retweeted already"
            continue

        # Does it match a rule?
        elif tweet_matches_rules(tweet.user.screen_name, tweet.full_text, rules):
            print "...  TWEETING Matched a rule! Gonna retweet it"
            # Retweet it!
            print api.PostRetweet(tweet.id)
            # Sleep before next possible retweet
            time.sleep(2.5)
        else:
            print "...  IGNORING"


if __name__ == '__main__':
    api = twitter.Api(
        tweet_mode='extended',
        consumer_key=os.environ['CONSUMER_KEY'],
        consumer_secret=os.environ['CONSUMER_SECRET'],
        access_token_key=os.environ['ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['ACCESS_TOKEN_SECRET'],
    )
    num_pages_to_fetch = 1

    if '--backfill' in sys.argv:
        print "Running backfill (last 800 tweets)"
        num_pages_to_fetch = 4

    tweets = get_tweets(api, num_pages_to_fetch)
    scan_and_retweet(tweets)
