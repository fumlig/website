import jinja2


def generate(website):
    env = jinja2.Environment(
        loader=jinja2.PackageLoader(website, "templates"),
        autoescape=jinja2.select_autoescape(["html", "xml"])
    )

    tmpl = env.get_template("base.html")