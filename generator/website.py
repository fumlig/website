import os
import shutil
import jinja2
import markdown

import generator


class Website:
    """Website class."""

    def __init__(self, path, config):
        self.path = path
        self.content_path = os.path.join(self.path, config.CONTENT_DIR)
        self.generated_path = os.path.join(self.path, config.GENERATED_DIR)
        self.static_path = os.path.join(self.path, config.STATIC_DIR)
        self.templates_path = os.path.join(self.path, config.TEMPLATES_DIR)

        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                searchpath=self.templates_path,
                encoding="utf-8",
                followlinks=True
            ),
            autoescape=jinja2.select_autoescape(["html", "xml"])
        )
        self.env.filters.update()
        self.md = markdown.Markdown(extensions=["codehilite", "full_yaml_metadata"])


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
                # get template
                template = self.env.get_template(os.path.relpath(template_file, self.templates_path))
                # clean up content_file and template_file
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
