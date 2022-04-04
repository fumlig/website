
html=www/index.html www/snoopers/index.html www/marching/index.html
domain=https://www.oskarlundin.com
pages=$(patsubst %index.html,%,$(patsubst www/%.html,$(domain)/%.html,$(html)))


all: $(html) www/sitemap.txt 

www/sitemap.txt: $(html)
	printf "%s\n" $(pages) | sort > $@

www/%.html: src/%.md src/style.css src/templates/article.html
	mkdir -p $(shell dirname $@)
	pandoc \
		--verbose \
		--self-contained \
		--table-of-contents \
		--citeproc \
		--mathjax \
		--data-dir=src \
		--template=article \
		--css=src/style.css \
		--resource-path=$(shell dirname $<) \
		--output=$@ \
		$<

www/%.html: src/%.ipynb src/%.yaml src/style.css src/templates/article.html
	mkdir -p $(shell dirname $@)
	$(if $(NB_EXECUTE),jupyter nbconvert --to notebook --inplace --execute $<)
	pandoc \
		--verbose \
		--self-contained \
		--table-of-contents \
		--citeproc \
		--mathjax \
		--data-dir=src \
		--template=article \
		--css=src/style.css \
		--resource-path=$(shell dirname $<) \
		--metadata-file=$(word 2,$^) \
		--output=$@ \
		$<

.PHONY: clean
clean:
	rm $(html)
