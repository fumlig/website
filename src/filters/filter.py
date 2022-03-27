#!/usr/bin/env python3

import pandocfilters as f

def redact(key, value, format, meta):
    if key == "Str":
        return f.Str(value.upper())

if __name__ == "__main__":
    f.toJSONFilter(redact)


#awk '{gsub(/[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/,"[redacted ip]")}1' > snoopers.html
#sed -i 's/SEARCH_REGEX/REPLACEMENT/g' index.ipynb
