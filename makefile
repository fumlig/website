html=$(shell find www -type f -name '*.html')
pages=$(patsubst %index.html,%,$(patsubst www/%.html,https://www.oskarlundin.com/%.html,$(html)))

www/sitemap.txt: $(html)
	printf "%s\n" $(pages) | sort > $@

www/%.html: src/%.md src/style.css src/templates/article.html
	mkdir -p $(shell dirname $@)
	pandoc \
		--self-contained \
		--data-dir=src \
		--template=article \
		--css=src/style.css \
		--output=$@ \
		$<

www/%.html: src/%.ipynb src/%.yaml src/style.css src/notebook.css src/templates/article.html
	mkdir -p $(shell dirname $@)
#	jupyter nbconvert --to notebook --inplace --execute $<
	pandoc \
		--verbose \
		--self-contained \
		--table-of-contents \
		--data-dir=src \
		--template=article \
		--css=src/style.css \
		--css=src/notebook.css \
		--highlight-style=src/syntax.theme \
		--mathjax \
		--output=$@ \
		--metadata-file=$(word 2,$^) \
		$<
