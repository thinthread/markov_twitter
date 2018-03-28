"""A Markov chain generator that can tweet random messages."""

import os
import sys

from random import choice
import twitter

import io

def open_and_read_file(filenames):
    """Take a list of files. Open them, read them, and return one long string."""

    body = ""

    for filename in filenames:
        text_file = io.open(filename, encoding="utf-8")
        body = body + text_file.read()
        text_file.close()

    return body


def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains."""

    chains = {}

    words = text_string.split()
    print words
    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        value = words[i + 2]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)

        # or could replace the last three lines with:
        #    chains.setdefault(key, []).append(value)

    return chains


def make_text(chains):
    """Take dictionary of Markov chains; return random text."""

    key = choice(chains.keys())
    words = [key[0], key[1]]
    while key in chains:
        word = choice(chains[key])
        if len(" ".join(words)) + len(word) < 140:
            words.append(word)
            key = (key[1], word)
        else:
            break

    return " ".join(words)


def tweet(chains):
    """Create a tweet and send it to the Twitter account to post."""

    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    while True:
        status = api.PostUpdate(make_text(chains))
        print status.text
        print  # blank line
        response = raw_input("Press the 'enter' key to tweet, or 'q' to  quit program: ")
        if response.lower() == 'q':
            break


filenames = sys.argv[1:]

text = open_and_read_file(filenames)

chains = make_chains(text)

tweet(chains)
