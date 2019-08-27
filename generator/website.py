import os
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
        """Create website directories and files."""
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
        