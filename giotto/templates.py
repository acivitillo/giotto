import inspect
from typing import Any, Callable, Dict, Literal, List

from dominate import document
from dominate.tags import body, div, form, head, link, main, script, input_, html_tag
from fastapi import Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from giotto.base import Action
from giotto.elements import Button
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
        container = div(_class="flex", _style="height: 95vh")
        m = main(_class="pt-8 px-8 overflow-x-auto flex-1")
        m.add(self.content)
        container.add(self.sidebar.to_tag(), m)
        b.add(container)
        return b

    def to_html(self):
        d = document(title=self.title)
        d.add(self.head, self.body)
        return d.render()


class Frame(BaseModel):
    id_: str
    func: Callable
    target: str = ""
    out_target: str = ""
    type_: Literal["form", "div"] = "div"
    class_: str = ""
    _defualt_class = "flex flex-row items-center m-4 border"

    @property
    def arguments(self):
        return list(inspect.signature(self.func).parameters)

    def get_tags(self, **form_kwargs) -> List[html_tag]:
        """Return list of frame's inside tags."""
        func_kwargs = {}
        for arg in self.arguments:
            if arg in form_kwargs:
                func_kwargs[arg] = form_kwargs[arg]
        tags = self.func(**func_kwargs)
        tags = self.add_post(tags)
        return tags

    def to_tag(self, **form_kwargs) -> html_tag:
        """Return full frame in tag form."""
        tags = self.get_tags(**form_kwargs)
        tag = eval(self.type_)
        tag = tag(tags, _id=self.id_, _class=self.class_ or self._defualt_class)
        return tag

    def add_post(self, tags: List[html_tag]):
        if self.type_ == "form":
            if self.target:
                for tag in tags:
                    tag["hx-target"] = f"#{self.target}"
                    tag["hx-post"] = f"/receiver?func_name={self.target}"

            if self.out_target:
                btn = Button(
                    description="Submit",
                    action=Action(
                        url=f"/receiver?func_name={self.out_target}",
                        target=f"#{self.out_target}",
                        swap=None,
                    ),
                    height=10,
                ).to_tag()
                tags.append(btn)
        return tags


class App(BaseModel):
    app: Any
    sidebar: Sidebar
    frames: Dict[str, Frame] = {}

    def register(self):
        self.app.add_api_route(
            "/receiver", self.receiver, methods=["POST"], response_class=HTMLResponse
        )
        self.app.add_api_route("/", self.render, methods=["GET"], response_class=HTMLResponse)
        return self

    async def receiver(self, request: Request, func_name: str):
        form = await request.form()
        # print(form, func_name, "\nFRAMES:")
        # pprint({k: v.dict() for k, v in self.frames.items()})
        frame = self.frames[func_name]
        tags = frame.get_tags(**form)
        return "\n".join([tag.render() for tag in tags])

    def render(self):
        site = AppSite(sidebar=self.sidebar)
        site.content = div(*[frame.to_tag() for frame in self.frames.values()])
        return site.to_html()

    def input(self, target: str = "", out_target: str = "", class_: str = ""):
        def decorator(func):
            self.add_frame(func, target, out_target, "form", class_)

        return decorator

    def output(self, class_: str = ""):
        def decorator(func):
            self.add_frame(func, class_)

        return decorator

    def add_frame(
        self,
        func,
        target: str = "",
        out_target: str = "",
        frame_type: str = "div",
        class_: str = "",
    ):
        func_name = func.__name__
        self.frames[func_name] = Frame(
            **{
                "id_": func_name,
                "func": func,
                "target": target,
                "out_target": out_target,
                "type_": frame_type,
                "class_": class_,
            }
        )
