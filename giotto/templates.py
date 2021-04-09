import inspect
from typing import Any, Callable, Dict, List, Literal

from dominate import document
from dominate.tags import body, div, form, head, html_tag, input_, link, main, script
from fastapi import Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, validator

from giotto.base import Action, Partial
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
    autorefresh: bool = False
    target: str = ""
    type_: Literal["form", "div"] = "div"
    class_: str = ""
    response: Any = List[Partial]

    @validator("class_", always=True)
    def set_class_(cls, v):
        return v or "flex flex-row items-center m-4 border"

    @property
    def arguments(self):
        return list(inspect.signature(self.func).parameters)

    def get_content(self, **form_kwargs) -> List[Partial]:
        """Return list of frame's inside tags."""
        func_kwargs = {}
        for arg in self.arguments:
            if arg in form_kwargs:
                func_kwargs[arg] = form_kwargs[arg]
        content = self.func(**func_kwargs)
        self._validate_func_output(content)
        tags = self.add_post(content)
        return tags

    @staticmethod
    def _validate_func_output(output: Any):
        mess = "Output of a frame should be a list of Partials"
        assert isinstance(output, list), mess
        assert all([isinstance(el, Partial) for el in output]), mess

    def to_tag(self, **form_kwargs) -> html_tag:
        """Return full frame in tag form."""
        content = self.get_content(**form_kwargs)
        tags = [tag for el in content for tag in el.to_tags()]
        tag = eval(self.type_)
        tag = tag(tags, _id=self.id_, _class=self.class_)
        return tag

    def add_post(self, content: List[Partial]):
        if self.type_ == "form":
            if self.autorefresh:
                for el in content:
                    el.action = Action(
                        url=f"/receiver?func_name={self.id_}",
                        target=f"#{self.id_}",
                        swap=None,
                    )
                    print(el)

            if self.target:
                btn = Button(
                    description="Submit",
                    action=Action(
                        url=f"/receiver?func_name={self.target}",
                        target=f"#{self.target}",
                        swap=None,
                    ),
                    height=10,
                )
                content.append(btn)
        return content


class App(BaseModel):
    app: Any
    sidebar: Sidebar
    frames: Dict[str, Frame] = {}

    def register(self):
        self.app.add_api_route(
            "/receiver", self.receiver, methods=["POST"], response_class=HTMLResponse
        )
        self.app.add_api_route("/", self.to_html, methods=["GET"], response_class=HTMLResponse)
        return self

    async def receiver(self, request: Request, func_name: str):
        form = await request.form()
        # print(form, func_name, "\nFRAMES:")
        # pprint({k: v.dict() for k, v in self.frames.items()})
        frame = self.frames[func_name]
        content = frame.get_content(**form)
        tags = [tag for el in content for tag in el.to_tags()]
        return "\n".join([tag.render() for tag in tags])

    def to_html(self):
        site = AppSite(sidebar=self.sidebar)
        site.content = div(*[frame.to_tag() for frame in self.frames.values()])
        return site.to_html()

    def frame(
        self, autorefresh: bool = False, target: str = "", type_: str = "div", class_: str = ""
    ):
        def decorator(func):
            func_name = func.__name__
            self.frames[func_name] = Frame(
                **{
                    "id_": func_name,
                    "func": func,
                    "autorefresh": autorefresh,
                    "target": target,
                    "type_": type_,
                    "class_": class_,
                }
            )

        return decorator
