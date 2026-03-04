import re

html = "<div><p>正文内容</p></div>"
clean_text = re.sub(r"<[^>]+>", "", html)