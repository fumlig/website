import os
import datetime


class Page:
    """Page class."""
    def __init__(
        self,
        website,
        content_file
    ):
        """Init page."""
        # determine target url
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
    
        # get title from meta data or file name
        title = meta.get("title")
        if not title:
            title = ' '.join(map(str.capitalize, os.path.basename(os.path.normpath(url)).split('-')))
        # get date created from meta data or file (not cross platform)
        created = meta.get("created")
        if not created:
            created = datetime.datetime.fromtimestamp(os.path.getctime(content_file))
        # get date modified from meta data or file (not cross platform)
        modified = meta.get("modified")
        if not modified:
            modified = datetime.datetime.fromtimestamp(os.path.getmtime(content_file))
        # get whether or not content file is a draft
        draft = meta.get("draft")
        if not draft:
            draft = False
        # get groups content belongs to
        groups = meta.get("groups")
        if not groups:
            groups = []
        # get page description
        description = meta.get("description")
        if not description:
            description = content[:155]
        
        # TODO: avoid this
        self.content_file = content_file
        # mandatory content fields
        self.url = url
        self.content = content
        self.title = title
        self.created = created
        self.modified = modified
        self.draft = draft
        self.groups = groups
        self.description = description
        # meta data field
        self.meta = meta
