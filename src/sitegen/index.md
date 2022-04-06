---
title: Static Site Generator in 24 Lines
lang: en
date: 2022-03-27
abstract: |
  There is a multitude of static site generators available.
keywords:
- make
- makefile
- static site generator
...

This is a condensed version of the source code for generating this website.

``` {.makefile .number-lines}
html=www/index.html www/snoopers/index.html www/marching/index.html

all: $(html)

www/%.html: src/%.md src/style.css src/templates/article.html
	mkdir -p $(shell dirname $@)
	pandoc --verbose --self-contained --table-of-contents --citeproc --mathjax \
		--data-dir=src \
		--template=article \
		--css=src/style.css \
		--resource-path=$(shell dirname $<) \
		--output=$@ \
		$<

.PHONY: clean serve publish

clean:
	rm $(documents)

serve:
    python3 -m http.server --directory www

publish:
    scp ...
```

