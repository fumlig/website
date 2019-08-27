import os
import jinja2

import config


def init(path):
    """Initialize new website."""
    # create directories
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(os.path.join(path, "content")):
        os.makedirs(os.path.join(path, "content"))
    if not os.path.exists(os.path.join(path, "public")):
        os.makedirs(os.path.join(path, "public"))
    if not os.path.exists(os.path.join(path, "static")):
        os.makedirs(os.path.join(path, "static"))
    if not os.path.exists(os.path.join(path, "templates")):
        os.makedirs(os.path.join(path, "templates"))


def generate(path, filters=None, tests=None, globals=None, policies=None):
    """Generate website in directory dir."""
    # create jinja2 environment
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(
            searchpath=os.path.join(path, "templates"),
            encoding="utf-8",
            followlinks=True
        ),
        autoescape=jinja2.select_autoescape(["html", "xml"])
    )

    # https://jinja.palletsprojects.com/en/2.10.x/api/#jinja2.Environment.filters
    if filters:
        env.filters.update(filters)
    
    # https://jinja.palletsprojects.com/en/2.10.x/api/#jinja2.Environment.tests
    if tests:
        env.tests.update(tests)

    # https://jinja.palletsprojects.com/en/2.10.x/api/#jinja2.Environment.globals
    if globals:
        env.globals.update(globals)
    
    # https://jinja.palletsprojects.com/en/2.10.x/api/#jinja2.Environment.policies
    if policies:
        env.globals.update(policies)

    # render templates
    templates = [t for t in env.list_templates()]
    template = env.get_template("home.html")
    render = template.render(
        posts=["post 1", "post 2", "post 3", "post 4"]
    )
    print(render)