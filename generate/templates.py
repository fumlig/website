import jinja2

env = jinja2.Environment(
    loader=jinja2.PackageLoader("website")
)