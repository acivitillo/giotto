import inspect
from typing import Any, Callable, Dict, List, Literal

from dominate import document
from dominate.tags import body, div, form, head, html_tag, input_, link, main, script
from fastapi import Request
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, validator
from fastapi import APIRouter

from giotto.base import Action, Partial
from giotto.elements import Button
from giotto.navigation import Sidebar, TopBar


class Frame(BaseModel):
    id_: str
    func: Callable
    prefix: str
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

    def get_content(self, **kwargs) -> List[Partial]:
        """Return list of frame's inside tags."""
        func_kwargs = {}
        for arg in self.arguments:
            if arg in kwargs:
                func_kwargs[arg] = kwargs[arg]
                print(arg, kwargs[arg])
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
                        url=f"{self.prefix}/receiver?func_name={self.id_}",
                        target=f"#{self.id_}",
                        swap=None,
                    )

            if self.target:
                btn = Button(
                    description="Submit",
                    action=Action(
                        url=f"{self.prefix}/receiver?func_name={self.target}",
                        target=f"#{self.target}",
                        swap=None,
                    ),
                    height=10,
                )
                content.append(btn)
        return content


class AppSite(BaseModel):
    title: str = "Giotto"
    site_name: str = "Site Name"
    sidebar: Sidebar = None
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
        topbar = TopBar(value=self.site_name).to_tag()
        m = main(self.content, _class="pt-8 px-8 overflow-x-auto flex-1")
        container = div(_class="flex", _style="height: 95vh")
        if self.sidebar:
            container.add(self.sidebar.to_tag())
        container.add(m)
        b = body(topbar, container)
        return b

    def to_html(self):
        d = document(title=self.title)
        d.add(self.head, self.body)
        return d.render()


class App(BaseModel):
    prefix: str
    app: Any = None
    sidebar: Sidebar = None
    frames: Dict[str, Frame] = {}

    def __init__(self, **data: Any):
        super().__init__(**data)

        self.app = self.app or APIRouter()

        self.app.add_api_route(
            f"{self.prefix}/receiver",
            self.receiver,
            methods=["POST", "GET"],
            response_class=HTMLResponse,
        )
        self.app.add_api_route(
            f"{self.prefix}/", self.to_html, methods=["GET"], response_class=HTMLResponse
        )

    # try to fetch params from request
    async def receiver(self, request: Request, func_name: str) -> str:
        form = await request.form()
        frame = self.frames[func_name]
        kwargs = {**form, **request.query_params}
        print(kwargs)
        content = frame.get_content(**kwargs)
        tags = [tag for el in content for tag in el.to_tags()]
        return "\n".join([tag.render() for tag in tags])

    def to_html(self):
        content = div(*[frame.to_tag() for frame in self.frames.values()])
        site = AppSite(sidebar=self.sidebar, content=content)
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
                    "prefix": self.prefix,
                    "autorefresh": autorefresh,
                    "target": target,
                    "type_": type_,
                    "class_": class_,
                }
            )

        return decorator


class MainApp(App):
    apps: List[App] = []
    prefix: str = ""

    def __init__(self, **data: Any):
        data["app"] = FastAPI()
        super().__init__(**data)

        for app in self.apps:
            if app.sidebar is None:
                app.sidebar = self.sidebar
            self.app.include_router(app.app)

        self.app.mount("/giotto-statics", StaticFiles(packages=["giotto"]))
