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


class Template(BaseModel):
    route: str

    @property
    def doc(self):
        return doc()

    @property
    def head(self):
        h = head()
        h.add(script(src="assets/dist/main.js", defer=True))
        h.add(link(href="assets/dist/styles.css", rel="stylesheet"))
        return h

    @property
    def body(self):
        return body()

    def to_register(self):
        result = {}
        result["path"] = self.route
        result["endpoint"] = self.to_html
        result["methods"] = ["get"]
        result["response_class"] = HTMLResponse
        return result

    # def register_url(self, app: Any, methods=["get"]):
    #    print("here", app, self.route)
    #    app.add_api_route(self.route, self.to_html, methods=methods, response_class=HTMLResponse)
    #    return True

    def _to_tag(self):
        pass

    def to_tag(self):
        tag = self._to_tag()
        return tag

    def to_html(self):
        content = self.to_tag()
        h = self.head
        b = self.body
        doc = self.doc
        if h is not None:
            doc.add(h)
        if b is not None:
            b.add(content)
            doc.add(b)
        return doc.render()


class AppLayout(Template):
    sidebar: Sidebar
    content: List[BaseModel]
    site_name: str = "Site Name"

    @property
    def body(self):
        b = body()
        topbar = TopBar(value=self.site_name).to_tag()
        b.add(topbar)
        return b

    @property
    def _content(self):
        tag = div(_class="flex overflow-hidden")
        # sidebar = Sidebar().to_tag()
        tag.add(self.sidebar.to_tag())
        return tag

    def _to_tag(self):
        tag = self._content
        _main = main(_class="flex flex-1 flex-col p-3")
        for item in self.content:
            _main.add(item.to_tag())
        tag.add(_main)
        return tag


class FrameTemplate(Template):
    content: List[BaseModel]
    name: str = "schedulerframe"

    @property
    def head(self):
        return None

    @property
    def body(self):
        return None

    def _to_tag(self):  # to improve
        tag = turbo_frame(_id=self.name, src=self.route, _class="p-2")
        return tag
