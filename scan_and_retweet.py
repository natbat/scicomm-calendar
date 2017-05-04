import json
import time
import os

import requests
import twitter


api = twitter.Api(
    consumer_key=os.environ['CONSUMER_KEY'],
    consumer_secret=os.environ['CONSUMER_SECRET'],
    access_token_key=os.environ['ACCESS_TOKEN_KEY'],
    access_token_secret=os.environ['ACCESS_TOKEN_SECRET'],
)


def fetch_rules():
    return json.loads(
        requests.get(
            'https://api.github.com/repos/natbat/scicomm-calendar/contents/config.json'
        ).json()['content'].decode('base64')
    )


def tweet_matches_rules(tweet, rules):
    for rule in rules:
        if tweet_matches_rule(tweet, rule):
            return True
    return False


def tweet_matches_rule(tweet, rule):
    screen_name = tweet.user.screen_name.lower()
    text = tweet.text.lower()
    return (screen_name == rule['user'].lower()) and (rule['hashtag'].lower() in text)


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
        print "Considering %r" % tweet.text
        # Have we retweeted this already?
        if tweet.retweeted:
            print "  Skipping, we have retweeted already"
            continue
        # Does it match a rule?
        elif tweet_matches_rules(tweet, rules):
            print "  Matched a rule! Gonna retweet it"
            # Retweet it!
            print api.PostRetweet(tweet.id)
            # Sleep before next possible retweet
            time.sleep(2.5)


if __name__ == '__main__':
    scan_and_retweet()
