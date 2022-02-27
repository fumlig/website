#!/usr/bin/env bash

user=oskar
host=oskar-server

src=www
dst=/srv/http/www.oskarlundin.com

rsync -r ${src}/ ${user}@${host}:${dst}
ssh -t ${user}@${host} sudo chown -R http:http ${dst}
