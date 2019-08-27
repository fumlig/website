import markdown


md = markdown.Markdown(extensions=["codehilite"])

html = md.convertFile(input="content/test.md", output="public/test.html", encoding="utf-8")