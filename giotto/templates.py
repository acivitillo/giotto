from typing import Any

from dominate import document as doc
from dominate.tags import body, div, head, link, main, script
from pydantic import BaseModel

from giotto.navigation import Sidebar, TopBar


class AppSite(BaseModel):
    title: str = "Giotto"
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
        container = div(_class="flex")
        m = main(_class="p-8 overflow-x-auto")
        m.add(self.content)
        container.add(self.sidebar.to_tag(), m)
        b.add(container)
        return b

    def to_html(self):
        d = doc(title=self.title)
        d.add(self.head, self.body)
        return d.render()
