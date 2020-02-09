#!/usr/bin/env bash

perl -i -pe 's/<a.*?href="([^"]+)".*?>([^<]+)<\/a>/[\2](https:\/\/netrunnerdb.com\1)/g' "$1"
