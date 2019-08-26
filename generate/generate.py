import os
import jinja2


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

    # compile templates
    env.compile_templates(
        target=os.path.join(path, "public")
    )