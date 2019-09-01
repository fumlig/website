import os
import shutil
import jinja2
import markdown
import yaml

import generator


class Website:
    """Website class."""

    def __init__(
        self, 
        path,
        drafts_enabled
    ):
        self.path = path
        with open(os.path.join(self.path, "config.yaml")) as f:
            try:
                config = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                print(exc)

        content_path = config.get("content_path")
        if not content_path:
            content_path = "content"
        self.content_path = os.path.join(path, content_path)

        generated_path = config.get("generated_path")
        if not generated_path:
            generated_path = "generated"
        self.generated_path = os.path.join(path, generated_path)

        static_path = config.get("static_path")
        if not static_path:
            static_path = "static"
        self.static_path = os.path.join(path, static_path)

        templates_path = config.get("templates_path")
        if not templates_path:
            templates_path = "content"
        self.templates_path = os.path.join(path, templates_path)

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
                "attr_list",
                # third party
                "full_yaml_metadata",
                "markdown_captions",
                "markdown_include.include"
            ],
            extension_configs={
                "codehilite": {
                    "linenums": None
                },
                "toc": {
                    "title": "Contents",
                    "permalink": True
                },
                "markdown_include.include": {
                    "base_path": os.path.abspath(self.content_path)
                }
            }
        )

        print()


    def pages(self):
        """Website pages"""
        # generate a page for each content markdown
        for root, dirs, files in os.walk(self.content_path):
            for f in files:
                if os.path.splitext(f)[1] == ".md":
                    content_file = os.path.join(root, f)
                    page = generator.Page(self, content_file)
                    yield page


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


    def clean(self):
        """Clear generated path."""
        for item in os.listdir(self.generated_path):
            path = os.path.join(self.generated_path, item)
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)


    def generate(self):
        """Generate website."""
        self.clean()
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
        # get site data
        with open(os.path.join(self.path, "site.yaml")) as f:
            try:
                site = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                print(exc)

        # store groups
        groups = {}
        for page in self.pages():
            # ignore drafts
            if not self.drafts_enabled and page.draft:
                continue
            for g in page.groups:
                if not g in groups:
                    groups[g] = []
                groups[g].append(page)

        # render pages
        for page in self.pages():
            # ignore drafts
            if not self.drafts_enabled and page.draft:
                continue
            # determine template file
            template_dir = os.path.join(self.templates_path, os.path.dirname(os.path.relpath(page.content_file, self.content_path)))
            template_file = os.path.join(template_dir, os.path.splitext(os.path.basename(page.content_file))[0] + ".html")
            while not os.path.exists(template_file):
                template_file = os.path.join(template_dir, "default.html")
                if os.path.normpath(os.path.join(template_dir, os.pardir)) == os.path.normpath(os.path.join(self.templates_path, os.pardir)):
                    break;
                template_dir = os.path.normpath(os.path.join(template_dir, os.pardir))

            if not os.path.exists(template_file):
                print("no template file found for page " + page.uri)
                continue
            
            # render page
            template = self.env.get_template(os.path.relpath(template_file, self.templates_path))
            render = template.render(page=page, site=site, groups=groups)
            dir_path = os.path.join(self.generated_path, page.uri[1:])
            file_path = os.path.join(dir_path, "index.html")
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            with open(file_path, 'w') as f:
                f.write(render)
