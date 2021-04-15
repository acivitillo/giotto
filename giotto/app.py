import inspect
from typing import Any, Callable, Dict, List, Literal, Optional

from dominate import document
from dominate.tags import body, div, form, head, html_tag, input_, link, main, script
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, validator

from giotto.base import HXAction, Partial, Style
from giotto.navigation import Sidebar, TopBar


class AppFunction(BaseModel):
    id_: str
    func: Callable
    prefix: str
    target: str = ""

    @property
    def arguments(self) -> List[str]:
        """List of names of function's parameters."""
        return list(inspect.signature(self.func).parameters)

    def get_hx_action(self, func_kwargs: Dict[str, str] = None) -> HXAction:
        """Get HXAction based on instance attributes and function keyword arguments."""
        target = f"#{self.target}" if self.target else None
        if func_kwargs:
            kwargs = "&".join([f"{k}={v}" for k, v in func_kwargs.items()])
            kwargs = f"&{kwargs}"
        else:
            kwargs = ""
        return HXAction(url=f"{self.prefix}/receiver?func_name={self.id_}{kwargs}", target=target)

    def run(self, **func_kwargs) -> Any:
        """Run function with provided keyword arguments."""
        return self.func(**func_kwargs)


class AppAction(AppFunction):
    pass


class Frame(AppFunction):
    type_: Literal["form", "div"] = "div"
    class_: str = ""
    style: Optional[Style] = None

    @validator("class_", always=True)
    def set_class_(cls, v):
        return v or "flex flex-row items-center mb-2 shadow sm:rounded"

    def to_partials(self, **func_kwargs) -> List[Partial]:
        """Return list of frame's inner partials."""
        valid_kwargs = {}
        for arg in self.arguments:
            if arg in func_kwargs:
                valid_kwargs[arg] = func_kwargs[arg]
        content = self.func(**valid_kwargs)
        self._validate_func_output(content)
        for partial in content:
            partial.style = partial.style or self.style
        return content

    @staticmethod
    def _validate_func_output(output: List[Partial]) -> None:
        """Validate frame's output."""
        mess = "Output of a frame should be a list of Partials"
        assert isinstance(output, list), mess
        assert all([isinstance(el, Partial) for el in output]), mess

    def to_tags(self, **func_kwargs) -> List[html_tag]:
        """Return list of frame's inner tags."""
        content = self.to_partials(**func_kwargs)
        tags = [tag for el in content for tag in el.to_tags()]
        return tags

    def to_tag(self, **func_kwargs) -> html_tag:
        """Return full frame in tag form."""
        tags = self.to_tags(**func_kwargs)
        tag = eval(self.type_)
        tag = tag(tags, _id=self.id_, _class=self.class_, autocomplete="off")
        return tag

    def run(self, **func_kwargs) -> str:
        """Render frame to html str."""
        tags = self.to_tags(**func_kwargs)
        return "\n".join([tag.render() for tag in tags])


class Site(BaseModel):
    title: str = "Giotto"
    site_name: str = "Site Name"
    topbar: Optional[TopBar] = None
    sidebar: Optional[Sidebar] = None
    content: Any = div()

    @property
    def head(self) -> str:
        h = head()
        h.add(script(src="/giotto-statics/main.js", defer=True))
        h.add(script(src="https://unpkg.com/htmx.org@1.2.1"))
        h.add(link(href="/giotto-statics/styles.css", rel="stylesheet"))
        return h

    @property
    def body(self) -> str:
        b = body()
        if self.topbar:
            b.add(self.topbar.to_tag())
        b.add(self.body_container)
        return b

    @property
    def body_container(self):
        m = main(self.content, _class="pt-8 px-8 overflow-x-auto flex-1")
        container = div(_class="flex", _style="height: 95vh")
        if self.sidebar:
            container.add(self.sidebar.to_tag())
        container.add(m)
        return container

    def render(self) -> str:
        """Render site to html str."""
        d = document(title=self.title)
        d.add(self.head, self.body)
        return d.render()

    def to_html(self) -> str:
        """Alias for render method."""
        return self.render()


class BaseApp(BaseModel):
    app: Any
    prefix: str = ""
    actions: Dict[str, AppAction] = {}
    frames: Dict[str, Frame] = {}
    style: Optional[Style] = None
    topbar: Optional[TopBar] = None
    sidebar: Optional[Sidebar] = None

    def add_api_routes(self):
        self.app.add_api_route(
            "/receiver", self.receiver, methods=["POST"], response_class=HTMLResponse
        )
        self.app.add_api_route("/", self.to_html, methods=["GET"], response_class=HTMLResponse)

    @property
    def functions(self) -> Dict[str, AppFunction]:
        """Utility property to get both actions and frames merged."""
        return {**self.actions, **self.frames}

    async def receiver(self, request: Request, func_name: str) -> Any:
        form = await request.form()
        func = self.functions[func_name]
        kwargs = {**form, **request.query_params}
        del kwargs["func_name"]
        return func.run(**kwargs)

    def render(self) -> str:
        """Render app to html str."""
        content = div(*[frame.to_tag() for frame in self.frames.values()])
        site = Site(sidebar=self.sidebar, topbar=self.topbar, content=content)
        return site.to_html()

    def to_html(self) -> str:
        """Alias for render method."""
        return self.render()

    def action(self, target: str = ""):
        """Decorator for registering new app action."""

        def decorator(func):
            func_name = func.__name__
            self.actions[func_name] = AppAction(
                **{"id_": func_name, "func": func, "prefix": self.prefix, "target": target}
            )

        return decorator

    def frame(self, type_: str = "div", class_: str = "", style: Style = None):
        """Decorator for registering new app frame."""

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
                    "style": style or self.style,
                }
            )

        return decorator

    def get_action(self, name: str, func_kwargs: Dict[str, str] = None) -> HXAction:
        return self.functions[name].get_hx_action(func_kwargs=func_kwargs)


class App(BaseApp):
    app: Any = None
    prefix: str

    def __init__(self, **data: Any):
        super().__init__(**data)

        self.app = self.app or APIRouter(prefix=self.prefix)
        self.add_api_routes()


class MainApp(BaseApp):
    app: Any = None
    apps: List[App] = []

    def __init__(self, **data: Any):
        super().__init__(**data)

        self.app = self.app or FastAPI()
        self.add_api_routes()

        for app in self.apps:
            self.app.include_router(app.app)

        self.app.mount("/giotto-statics", StaticFiles(packages=["giotto"]))
