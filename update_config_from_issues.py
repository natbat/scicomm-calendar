import re
import json
import requests
from collections import OrderedDict

# Here's the documentation for the GitHub issues API:
# https://developer.github.com/v3/issues/#list-repository-issues

hashtag_re = re.compile(r"#([a-zA-Z0-9_]+)")
atname_re = re.compile(r"@([a-zA-Z0-9_]+)")


def add_game(atnames, hashtags, config):
    for name in atnames:
        name = name.lower()
        if name not in config:
            config[name] = []
        for hashtag in hashtags:
            hashtag = hashtag.lower()
            if hashtag not in config[name]:
                config[name].append(hashtag)


def get_issues():
    return requests.get(
        "https://api.github.com/repos/natbat/scicomm-calendar/issues"
    ).json()


def run():
    issues = get_issues()
    issues_to_add = [
        issue
        for issue in issues
        if "game suggestion" in [l["name"] for l in issue["labels"]]
        and issue["user"]["login"] == "natbat"
    ]

    # load the config
    config = json.load(open("config.json"), object_pairs_hook=OrderedDict)

    for open_issue in issues_to_add:
        issue_text = open_issue["title"] + " " + open_issue["body"]
        hashtags = hashtag_re.findall(issue_text)
        atnames = atname_re.findall(issue_text)
        add_game(atnames, hashtags, config)

    # save the config
    open("config.json", "w").write(json.dumps(config, indent=4))


if __name__ == "__main__":
    run()
