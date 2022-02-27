#!/usr/bin/env bash

jupyter nbconvert \
    --TemplateExporter.extra_template_basedirs=../../templates \
    --to html \
    --template nbarticle \
    --execute \
    --stdout \
    snoopers.ipynb | awk '{gsub(/[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/,"[redacted ip]")}1' > snoopers.html