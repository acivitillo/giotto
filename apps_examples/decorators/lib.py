import inspect
from fastapi import Form, Request
from fastapi.responses import HTMLResponse
from typing import List, Dict, Any, Callable, Literal
from dominate.tags import h1, select, option, div, body, head, script, form, button
from dominate import document
from pydantic import BaseModel
from pprint import pprint


class Frame(BaseModel):
    id_: str
    func: Callable
    target: str = ""
    out_target: str = ""
    type_: Literal["form", "div"] = "div"

    @property
    def arguments(self):
        return list(inspect.signature(self.func).parameters)

    def to_tag(self, **form_kwargs):
        func_kwargs = {}
        for arg in self.arguments:
            if arg in form_kwargs:
                func_kwargs[arg] = form_kwargs[arg]
        tags = self.func(**func_kwargs)
        tags = self.add_post(tags)
        tag = eval(self.type_)
        tag = tag(tags, _id=self.id_)
        return tag

    def add_post(self, tags):
        if self.target:
            for tag in tags:
                tag["hx-target"] = f"#{self.target}"
                tag["hx-post"] = f"/receiver?func_name={self.target}"

        if self.out_target:
            btn = button(
                "Submit",
                data_hx_post=f"/receiver?func_name={self.out_target}",
                data_hx_target=f"#{self.out_target}",
            )
            tags.append(btn)
        return tags


class App(BaseModel):
    app: Any
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
        tag = frame.to_tag(**form)
        return tag.render()

    def render(self):
        doc = document()
        _head = head(script(src="https://unpkg.com/htmx.org@1.3.2"))
        _body = body(*[frame.to_tag() for frame in self.frames.values()])
        doc.add(_head, _body)
        return doc.render()

    def input(self, target: str = "", out_target: str = ""):
        def decorator(func):
            self.append_frame(func, target, out_target, "form")

        return decorator

    def output(self):
        def decorator(func):
            self.append_frame(func)

        return decorator

    def append_frame(self, func, target: str = "", out_target: str = "", frame_type: str = "div"):
        func_name = func.__name__
        self.frames[func_name] = Frame(
            **{
                "id_": func_name,
                "func": func,
                "target": target,
                "out_target": out_target,
                "type_": frame_type,
            }
        )
        return self


class Select(BaseModel):
    name: str = ""
    options: List[str]
    selected: str = ""

    @classmethod
    def from_list(cls, name: str, options: List, selected: str = ""):
        return cls(name=name, options=options, selected=selected)

    def to_tag(self):
        sel = select(name=self.name)
        for opt in self.options:
            if opt == self.selected:
                sel.add(option(opt, selected=True))
            else:
                sel.add(option(opt))
        return sel
