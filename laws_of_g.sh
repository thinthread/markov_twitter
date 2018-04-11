#!/bin/bash

VENV=$(dirname $0)
cd $VENV

source ./secrets.sh

echo -e "q" | ./env-$(uname)/bin/python markov_tweet.py laws_of_g.txt