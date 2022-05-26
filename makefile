files=www/index.html www/snoopers/index.html www/marching/index.html www/sitegen/index.html
pages=$(patsubst %index.html,%,$(patsubst www/%.html,/%.html,$(files)))

domain=https://www.fumlig.se/~oskar


.PHONY: all clean serve publish

all: $(files) www/sitemap.txt 

clean:
	rm $(files) www/sitemap.txt

serve:
	python3 -m http.server --directory www

publish:
	scp -r www/* oskar@oskar-server:public

www/sitemap.txt: $(html)
	printf "%s\n" $(patsubst %,$(domain)%,$(pages)) | sort > $@

www/%.html: src/%.html
	cp $< $@

www/%.html: src/%.md styles/article.css templates/article.html
	mkdir -p $(shell dirname $@)
	pandoc --verbose --self-contained --table-of-contents --section-divs --citeproc --mathjax \
		--data-dir=. \
		--template=article \
		--css=styles/article.css \
		--resource-path=$(shell dirname $<) \
		--output=$@ \
		$<

www/%.html: src/%.tex styles/article.css templates/article.html
	mkdir -p $(shell dirname $e@)
	pandoc --verbose --self-contained --table-of-contents --section-divs --citeproc --mathjax \
		--data-dir=. \
		--template=article \
		--css=$(style) \
		--resource-path=$(shell dirname $<) \
		--lua-filter=tikz.lua \
		--output=$@ \
		$<

www/%.html: src/%.ipynb src/%.yaml styles/article.css templates/article.html
	mkdir -p $(shell dirname $@)
	$(if $(NB_EXECUTE),jupyter nbconvert --to notebook --inplace --execute $<)
	pandoc --verbose --self-contained --table-of-contents --section-divs --citeproc --mathjax \
		--data-dir=. \
		--template=article \
		--css=styles/article.css \
		--resource-path=$(shell dirname $<) \
		--metadata-file=$(word 2,$^) \
		--output=$@ \
		$<

