from typing import Optional

from fastapi.responses import HTMLResponse


# lib templates.py
from pydantic import BaseModel
from typing import List, Any
from dominate.tags import head, body, script, link, div, h1, main
from dominate.util import raw
from dominate import document as doc
from giotto.elements import Select, Button
from giotto.navigation import TopBar, Sidebar
from giotto.utils import turbo_frame


class AppSite(BaseModel):
    site_name: str = "Site Name"
    sidebar: Sidebar
    content: Any = div()

    @property
    def head(self):
        h = head()
        h.add(script(src="/giotto-statics/main.js", defer=True))
        h.add(script(src="https://unpkg.com/htmx.org@1.2.1"))
        h.add(link(href="/giotto-statics/styles.css", rel="stylesheet"))
        return h

    @property
    def body(self):
        b = body()
        topbar = TopBar(value=self.site_name).to_tag()
        b.add(topbar)
        container = div(_class="flex overflow-hidden")
        m = main(_class="p-8")
        m.add(self.content)
        container.add(self.sidebar.to_tag(), m)
        b.add(container)
        return b

    def to_html(self):
        d = doc()
        d.add(self.head, self.body)
        return d.render()
