#!/usr/bin/env bash

jupyter nbconvert --to html --template basic --execute --stdout ssh.ipynb | awk '{gsub(/[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/,"[redacted ip]")}1' > ssh.html
