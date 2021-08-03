#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# The configuration file format:
"""
[twitter]
consumer_key=consumer_key
consumer_secret=consumer_secret
access_token_key=access_token_key
access_token_secret=access_token_secret
"""

import argparse
import configparser
import os

import tweepy


def split_message(message):
    """Split a message into 280-character chunks for splitting across tweets.
    """

    words = message.split()
    line = ""
    for word in words:
        if len(line + word) > 278:
            yield line + "\u2026"
            line = word
        else:
            line += f" {word}"
    yield line


class Tweet():
    def __init__(self, config):
        self.consumer_key = config.get('twitter', 'consumer_key')
        self.consumer_secret = config.get('twitter', 'consumer_secret')
        self.access_token_key = config.get('twitter', 'access_token_key')
        self.access_token_secret = config.get('twitter', 'access_token_secret')

        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token_key, self.access_token_secret)
        self.api = tweepy.API(auth)

    def send(self, msg):
        if len(msg) > 280:
            last = None
            for line in split_message(msg):
                if last is not None:
                    last = self.api.update_status(
                        status=line,
                        in_reply_to_status_id=last.id,
                        auto_populate_reply_metadata=True,
                    )
                else:
                    last = self.api.update_status(status=line)

        else:
            self.api.update_status(status=msg)


def main():
    parser = argparse.ArgumentParser(description='Twitter bot')
    parser.add_argument(
        'message', type=str, help="What's happening?")
    args = parser.parse_args()
    config = configparser.ConfigParser()
    config.read(os.path.expanduser('~/.tweetrc'))

    tweet = Tweet(config)
    tweet.send(args.message)


if __name__ == '__main__':
    main()
