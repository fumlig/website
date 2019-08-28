import os
import shutil
import jinja2
import markdown

import generator


class Website:
    """Website class."""

    def __init__(
        self, 
        path, 
        content_path=None, 
        generated_path=None, 
        static_path=None, 
        templates_path=None,
        drafts_enabled=False
    ):
        self.path = path
        self.content_path = os.path.join(path, "content") if not content_path else content_path
        self.generated_path = os.path.join(path, "generated") if not generated_path else generated_path
        self.static_path = os.path.join(path, "static") if not static_path else static_path
        self.templates_path = os.path.join(path, "templates") if not templates_path else templates_path

        self.drafts_enabled = drafts_enabled

        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                searchpath=self.templates_path,
                encoding="utf-8",
                followlinks=True
            ),
            autoescape=jinja2.select_autoescape(["html", "xml"])
        )

        self.md = markdown.Markdown(
            # https://python-markdown.github.io/extensions/
            extensions=[
                # official
                "abbr",
                "def_list",
                "fenced_code",
                "footnotes",
                "tables",
                "admonition",
                "codehilite",
                "sane_lists",
                "toc",
                # third party
                "full_yaml_metadata"
            ],
            extension_configs={
                "codehilite": {
                    "linenums": True
                },
                "toc": {
                    "title": "Contents",
                    "permalink": True
                }
            }
        )


    def pages(self):
        """Website pages"""
        # generate a page for each content markdown
        for root, dirs, files in os.walk(self.content_path):
            for f in files:
                path = os.path.join(root, f)
                url, ext = os.path.splitext(os.path.relpath(path, self.content_path))
                # ignore if not markdown
                if not ext == ".md":
                    continue
                # store paths to content and template
                content_file = path
                template_file = os.path.join(self.templates_path, url + ".html")
                if not os.path.exists(template_file):
                    template_file = os.path.join(os.path.split(template_file)[0], "default.html")
                    if not os.path.exists(template_file):
                        print("No template found for " + content_file)
                        continue
                # clean up url
                if url.endswith("index"):
                    url = url[:-len("index")]
                if not url.startswith('/'):
                    url = '/' + url
                if not url.endswith('/'):
                    url += '/'
                # parse content and meta data
                with open(content_file, 'r') as f:
                    content = self.md.convert(f.read())
                    meta = self.md.Meta
                    self.md.reset()
                # ignore if draft and drafts not enabled
                if not self.drafts_enabled and meta.get("draft"):
                    continue
                # get template
                template = self.env.get_template(os.path.relpath(template_file, self.templates_path))

                yield generator.Page(url, content, meta, template)


    def create(self):
        """Create website."""
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        if not os.path.exists(self.content_path):
            os.makedirs(self.content_path)
        if not os.path.exists(self.generated_path):
            os.makedirs(self.generated_path)
        if not os.path.exists(self.static_path):
            os.makedirs(self.static_path)
        if not os.path.exists(self.templates_path):
            os.makedirs(self.templates_path)


    def generate(self):
        """Generate website."""
        # delete old files
        for item in os.listdir(self.generated_path):
            path = os.path.join(self.generated_path, item)
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)

        # create new files
        self.generate_static()
        self.generate_pages()

    
    def generate_static(self):
        """Copy static files to generate directory."""
        # copy files from static path to generated path
        for item in os.listdir(self.static_path):
            src = os.path.join(self.static_path, item)
            dst = os.path.join(self.generated_path, item)
            if os.path.isdir(src):
                shutil.copytree(src, dst, symlinks=True, ignore=None)
            else:
                shutil.copy2(src, dst)


    def generate_pages(self):
        """Render templates with content."""
        # populate lists dict
        lists = {}
        for page in self.pages():
            if not page.meta or not "lists" in page.meta:
                continue
            for l in page.meta["lists"]:
                if not l in lists:
                    lists[l] = []
                lists[l].append(page.data())
        
        # render pages
        for page in self.pages():
            render = page.template.render(page=page.data(), lists=lists)
            # write page to file
            dir_path = self.generated_path if page.url == '/' else os.path.join(self.generated_path, page.url[1:])
            file_path = os.path.join(dir_path, "index.html")
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            with open(file_path, 'w') as f:
                f.write(render)
