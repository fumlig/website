index=www/index.html
articles=www/snoopers/index.html www/marching/index.html www/sitegen/index.html

documents=$(index) $(articles)
pages=$(patsubst %index.html,%,$(patsubst www/%.html,/%.html,$(documents)))
domain=https://www.oskarlundin.com


all: $(documents) www/sitemap.txt 

www/sitemap.txt: $(html)
	printf "%s\n" $(patsubst %,$(domain)%,$(pages)) | sort > $@

www/%.html: src/%.html
	cp $< $@

www/%.html: src/%.md src/style.css templates/article.html
	mkdir -p $(shell dirname $@)
	pandoc --verbose --self-contained --table-of-contents --citeproc --mathjax \
		--data-dir=. \
		--template=article \
		--css=src/style.css \
		--resource-path=$(shell dirname $<) \
		--output=$@ \
		$<

www/%.html: src/%.tex src/style.css templates/article.html
	mkdir -p $(shell dirname $@)
	pandoc --verbose --self-contained --table-of-contents --citeproc --mathjax \
		--data-dir=. \
		--template=article \
		--css=src/style.css \
		--resource-path=$(shell dirname $<) \
		--lua-filter=tikz.lua \
		--output=$@ \
		$<

www/%.html: src/%.ipynb src/%.yaml src/style.css templates/article.html
	mkdir -p $(shell dirname $@)
	$(if $(NB_EXECUTE),jupyter nbconvert --to notebook --inplace --execute $<)
	pandoc --verbose --self-contained --table-of-contents --citeproc --mathjax \
		--data-dir=. \
		--template=article \
		--css=src/style.css \
		--resource-path=$(shell dirname $<) \
		--metadata-file=$(word 2,$^) \
		--output=$@ \
		$<

.PHONY: clean
clean:
	rm $(documents)
