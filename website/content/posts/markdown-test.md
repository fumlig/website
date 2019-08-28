---
title: Markdown Test
lead: A test of all markdown features.
author: Oskar Lundin
date: 27-08-2019
modified: 28-08-2019
tags:
  - markdown
lists:
  - posts
draft: false
---


# Markdown Test

This is a test markdown file.

## Extensions

### Official

#### Abbreviations

The HTML specification
is maintained by the W3C.

*[HTML]: Hyper Text Markup Language
*[W3C]:  World Wide Web Consortium

#### Definition Lists

Apple
:   Pomaceous fruit of plants of the genus Malus in
    the family Rosaceae.

Orange
:   The fruit of an evergreen tree of the genus Citrus.

#### Fenced Code Blocks

This is a paragraph introducing:

~~~~~~~~~~~~~~~~~~~~~
a one-line code block
~~~~~~~~~~~~~~~~~~~~~

~~~~{.python}
# python code
~~~~

~~~~.html
<p>HTML Document</p>
~~~~

```python
# more python code
```

~~~~{.python hl_lines="1 3"}
# This line is emphasized
# This line isn't
# This line is emphasized
~~~~

```python hl_lines="1 3"
# This line is emphasized
# This line isn't
# This line is emphasized
```

#### Footnotes

Footnotes[^1] have a label[^@#$%] and the footnote's content.

[^1]:
    The first paragraph of the definition.

    Paragraph two of the definition.

    > A blockquote with
    > multiple lines.

        a code block

    A final paragraph.
[^@#$%]: A footnote on the label: "@#$%".

#### Tables

First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell

#### Admonition

!!! type "optional explicit title within double quotes"
    Any number of other indented markdown elements.

    This is the second paragraph.

!!! note
    You should note that the title will be automatically capitalized.

!!! danger "Don't try this at home"
    ...

!!! important ""
    This is an admonition box without a title.

#### Codehilite

Shebang (with path)

    #!/usr/bin/python
    # Code goes here ...

Shebang (no path)

    #!python
    # Code goes here ...

Colons

    :::python
    # Code goes here ...


    :::python hl_lines="1 3"
    # This line is emphasized
    # This line isn't
    # This line is emphasized

When No Language is Defined

    # Code goes here ...

#### Sane Lists

1. Apples
2. Oranges
3. Pears

#### Table of Contents

[TOC]

### Third Party

#### YAML metadata extension

[GitHub](https://github.com/sivakov512/python-markdown-full-yaml-metadata)
