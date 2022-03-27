#!/usr/bin/env bash

awk '{gsub(/[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/,"[redacted ip]")}1' > snoopers.html