import inspect
from typing import Any, Callable, Dict, List, Literal, Optional

from dominate import document
from dominate.tags import body, div, form, head, html_tag, input_, link, main, script
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, validator

from giotto.base import Action, Partial, Style
from giotto.navigation import Sidebar, TopBar


class AppAction(BaseModel):
    id_: str
    func: Callable
    prefix: str
    target: str = ""

    def get_hx_action(self, func_kwargs: Dict[str, str] = None) -> Action:
        target = f"#{self.target}" if self.target else None
        if func_kwargs:
            kwargs = "&".join([f"{k}={v}" for k, v in func_kwargs.items()])
            kwargs = f"&{kwargs}"
        else:
            kwargs = ""
        return Action(url=f"{self.prefix}/receiver?func_name={self.id_}{kwargs}", target=target)

    @property
    def arguments(self):
        return list(inspect.signature(self.func).parameters)

    def run(self, **kwargs) -> Any:
        return self.func(**kwargs)


class Frame(AppAction):
    type_: Literal["form", "div"] = "div"
    class_: str = ""
    style: Optional[Style] = None

    @validator("class_", always=True)
    def set_class_(cls, v):
        return v or "flex flex-row items-center mb-2 shadow sm:rounded"

    def to_partials(self, **kwargs) -> List[Partial]:
        """Return list of frame's inner partials."""
        func_kwargs = {}
        for arg in self.arguments:
            if arg in kwargs:
                func_kwargs[arg] = kwargs[arg]
        content = self.func(**func_kwargs)
        self._validate_func_output(content)
        for partial in content:
            partial.style = partial.style or self.style
        return content

    @staticmethod
    def _validate_func_output(output: List[Partial]):
        mess = "Output of a frame should be a list of Partials"
        assert isinstance(output, list), mess
        assert all([isinstance(el, Partial) for el in output]), mess

    def to_tags(self, **kwargs) -> List[html_tag]:
        """Return list of frame's inner tags."""
        content = self.to_partials(**kwargs)
        tags = [tag for el in content for tag in el.to_tags()]
        return tags

    def to_tag(self, **kwargs) -> html_tag:
        """Return full frame in tag form."""
        tags = self.to_tags(**kwargs)
        tag = eval(self.type_)
        tag = tag(tags, _id=self.id_, _class=self.class_)
        return tag

    def run(self, **kwargs) -> str:
        tags = self.to_tags(**kwargs)
        return "\n".join([tag.render() for tag in tags])


class AppSite(BaseModel):
    title: str = "Giotto"
    site_name: str = "Site Name"
    sidebar: Optional[Sidebar] = None
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
    sidebar: Optional[Sidebar] = None
    actions: Dict[str, AppAction] = {}
    frames: Dict[str, Frame] = {}

    @property
    def functions(self):
        return {**self.actions, **self.frames}

    def __init__(self, **data: Any):
        super().__init__(**data)

        self.app = self.app or APIRouter(prefix=self.prefix)

        self.app.add_api_route(
            "/receiver",
            self.receiver,
            methods=["POST", "GET"],
            response_class=HTMLResponse,
        )
        self.app.add_api_route("/", self.to_html, methods=["GET"], response_class=HTMLResponse)

    # try to fetch params from request
    async def receiver(self, request: Request, func_name: str) -> str:
        form = await request.form()
        print(form)
        func = self.functions[func_name]
        kwargs = {**form, **request.query_params}
        del kwargs["func_name"]
        return func.run(**kwargs)

    def to_html(self):
        content = div(*[frame.to_tag() for frame in self.frames.values()])
        site = AppSite(sidebar=self.sidebar, content=content)
        return site.to_html()

    def action(self, target: str = ""):
        def decorator(func):
            func_name = func.__name__
            self.actions[func_name] = AppAction(
                **{"id_": func_name, "func": func, "prefix": self.prefix, "target": target}
            )

        return decorator

    def frame(self, type_: str = "div", class_: str = "", style: Style = None):
        def decorator(func):
            func_name = func.__name__
            self.frames[func_name] = Frame(
                **{
                    "id_": func_name,
                    "func": func,
                    "prefix": self.prefix,
                    "target": func_name,
                    "type_": type_,
                    "class_": class_,
                    "style": style,
                }
            )

        return decorator

    def get_action(self, name: str, func_kwargs: Dict[str, str] = None):
        return self.functions[name].get_hx_action(func_kwargs=func_kwargs)


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
