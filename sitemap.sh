#!/usr/bin/env bash

shopt -s globstar

files=$(ls www/**/*.html)
pages=$(printf "%s\n" "$files" | sed -e "s/^www/https:\/\/www.oskarlundin.com/g" | sed -e "s/index.html$//g")

printf "%s\n" "$pages" > www/sitemap.txt
