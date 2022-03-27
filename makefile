html=$(shell find www -type f -name '*.html')
pages=$(patsubst %index.html,%,$(patsubst www/%.html,https://www.oskarlundin.com/%.html,$(html)))

www/sitemap.txt: $(html)
	printf "%s\n" $(pages) | sort > $@

www/%.html: src/%.md src/style.css src/templates/article.html
	mkdir -p $(shell dirname $@)
	pandoc \
		--verbose \
		--self-contained \
		--table-of-contents \
		--citeproc \
		--data-dir=src \
		--template=article \
		--css=src/style.css \
		--mathjax \
		--resource-path=$(shell dirname $<) \
		--output=$@ \
		$<

www/%.html: src/%.ipynb src/%.yaml src/style.css src/templates/article.html
	mkdir -p $(shell dirname $@)
#	jupyter nbconvert --to notebook --inplace --execute $<
	pandoc \
		--verbose \
		--self-contained \
		--table-of-contents \
		--citeproc \
		--data-dir=src \
		--template=article \
		--css=src/style.css \
		--mathjax \
		--resource-path=$(shell dirname $<) \
		--metadata-file=$(word 2,$^) \
		--output=$@ \
		$<
