import os
import datetime


class Page:
    """Page class."""
    def __init__(
        self, 
        website,
        content_file,
        template_file,
    ):
        """Init page."""
        url, ext = os.path.splitext(os.path.relpath(content_file, website.content_path))
        if not ext == ".md":
            raise ValueError("content_file '{}' must be a markdown file".format(content_file))
        # clean up url
        if url.endswith("index"):
            url = url[:-len("index")]
        if not url.startswith('/'):
            url = '/' + url
        if not url.endswith('/'):
            url += '/'
        # parse content
        with open(content_file, 'r') as f:
            content = website.md.convert(f.read())
            meta = website.md.Meta
            website.md.reset()
        # get template
        self.template = website.env.get_template(os.path.relpath(template_file, website.templates_path))
        # set data
        self.data = {
            "url": url,
            "content": content,
            **meta
        }
        if not "title" in self.data:
            title = os.path.basename(os.path.normpath(url))
            title = title.split('-')
            title = ' '.join([word.capitalize() for word in title])
            self.data["title"] = title
        if not "created" in self.data:
            c_unixtime = os.path.getctime(content_file)
            c_datetime = datetime.datetime.fromtimestamp(c_unixtime)
            self.data["created"] = c_datetime
        if not "modified" in self.data:
            m_unixtime = os.path.getmtime(content_file)
            m_datetime = datetime.datetime.fromtimestamp(m_unixtime)
            self.data["modified"] = m_datetime
        if not "draft" in self.data:
            self.data["draft"] = False
        if not "lists" in self.data:
            self.data["lists"] = []
