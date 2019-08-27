import os
import shutil
import jinja2
import markdown


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
        self.md = markdown.Markdown(extensions=["codehilite", "full_yaml_metadata"])

        self.content = {}


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

        # create data
        self.copy_static()
        self.store_content()
        self.render_templates()

    
    def copy_static(self):
        """Copy static files to generate directory."""
        # copy files from static path to generated path
        for item in os.listdir(self.static_path):
            src = os.path.join(self.static_path, item)
            dst = os.path.join(self.generated_path, item)
            if os.path.isdir(src):
                shutil.copytree(src, dst, symlinks=True, ignore=None)
            else:
                shutil.copy2(src, dst)


    def store_content(self):
        """Store content before rendering."""
        # generate a page for each content markdown
        for root, dirs, files in os.walk(self.content_path):
            for f in files:
                path = os.path.join(root, f)
                url, ext = os.path.splitext(os.path.relpath(path, self.content_path))
                # ignore if not markdown
                if not ext == ".md":
                    continue
                # clean up url
                if url.endswith("index"):
                    url = url[:-len("index")]
                if not url.startswith('/'):
                    url = '/' + url
                if not url.endswith('/'):
                    url += '/'

                # create page content
                with open(path, 'r') as f:
                    self.content[url] = {
                        "html": self.md.convert(f.read()),
                        "meta": self.md.Meta
                    }
        print(self.content)


    def generate_page(self, content_file, template_file, generate_path=None):
        """Generate a page."""
        print("Generating " + content_file + " with " + template_file + ".")
        content = {}
        # parse markdown
        with open(content_file, 'r') as f:
            content["contents"] = self.md.convert(f.read())
            content["meta"] = self.md.Meta
        
        # render template
        template = self.env.get_template(os.path.relpath(template_file, self.templates_path))
        render = template.render(content=content)

        print(render)
    

    def render_templates(self):
        """Render templates with content."""
        pass
            
        """
        # paths for potential templates
        specific_tmpl = os.path.join(self.templates_path, pre + ".html")
        default_tmpl = os.path.join(self.templates_path, dirname, "default.html")
        # decide which template to use
        if os.path.exists(specific_tmpl):
            # use specific template
            self.generate_page(path, specific_tmpl)
        elif os.path.exists(default_tmpl):
            # use default tempate
            self.generate_page(path, default_tmpl)
        else:
            # no template found
            print("No template found for " + path + ", ignoring")
        """
