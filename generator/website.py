import os
import shutil
import jinja2


class Website:
    """Website class."""

    def __init__(self, path, config):
        self.path = path
        self.content_path = os.path.join(self.path, config.CONTENT_DIR)
        self.generated_path = os.path.join(self.path, config.GENERATED_DIR)
        self.static_path = os.path.join(self.path, config.STATIC_DIR)
        self.templates_path = os.path.join(self.path, config.TEMPLATES_DIR)

        self.environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                searchpath=self.templates_path,
                encoding="utf-8",
                followlinks=True
            ),
            autoescape=jinja2.select_autoescape(["html", "xml"])
        )


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

        # generate new files
        self.generate_static()
        self.generate_content()

    
    def generate_static(self):
        """Generate static."""
        # copy files from static path to generated path
        for item in os.listdir(self.static_path):
            src = os.path.join(self.static_path, item)
            dst = os.path.join(self.generated_path, item)
            if os.path.isdir(src):
                shutil.copytree(src, dst, symlinks=True, ignore=None)
            else:
                shutil.copy2(src, dst)


    def generate_content(self):
        """Generate content."""
        # generate a page for each content markdown
        for root, dirs, files in os.walk(self.content_path):
            for f in files:
                path = os.path.join(root, f)
                relpath = os.path.relpath(path, self.content_path)
                dirname = os.path.dirname(relpath)
                pre, ext = os.path.splitext(relpath)
                # ignore if not markdown
                if not ext == ".md":
                    continue
                # paths for potential templates
                specific_tmpl = os.path.join(self.templates_path, pre + ".html")
                default_tmpl = os.path.join(self.templates_path, dirname, "default.html")
                # decide which template to use
                if os.path.exists(specific_tmpl):
                    # use specific template
                    self.generate_page(path, specific_tmpl)
                    pass
                elif os.path.exists(default_tmpl):
                    # use default tempate
                    self.generate_page(path, default_tmpl)
                    pass
                else:
                    # no template found
                    print("No template found for " + path + ", ignoring")
    

    def generate_page(self, content_path, template_path):
        """Generate a page."""
        print("Generating " + content_path + " with " + template_path + ".")


    def parse_content(self):
        """Parse content file to dictionary usable in templates."""
        pass