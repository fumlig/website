class Page:
    """Page class."""

    def __init__(self, url, content, meta, template):
        """Init page."""
        self.url = url
        self.content = content
        self.meta = meta
        self.template = template

    def data(self):
        """Page data."""
        return {
            "url": self.url,
            "content": self.content,
            "meta": self.meta
        }
