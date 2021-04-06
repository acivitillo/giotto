import inspect
from fastapi import Form, Request
from fastapi.responses import HTMLResponse
from typing import List, Dict, Any, Callable, Literal
from dominate.tags import h1, select, option, div, body, head, script, form, button
from dominate import document
from pydantic import BaseModel
from functools import wraps


class Frame(BaseModel):
    id_: str
    func: Callable
    target: str = ""
    arguments: List[str] = []
    out_target: str = ""
    tags: List[Any] = []
    type_: Literal["form", "div"] = "div"

    def to_tag(self):
        tag = eval(self.type_)
        tag = tag(self.tags, _id=self.id_)
        return tag


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
        # How is this request generated ???
        form = await request.form()
        print(form)

        def to_tag():
            from pprint import pprint

            print(func_name)
            print("\nFRAMES:")
            pprint({k: v.dict() for k, v in self.frames.items()})
            frame = self.frames[func_name]
            func_args = []
            for arg in frame.arguments:
                try:
                    func_args.append(form[arg])
                except KeyError:
                    raise KeyError(f"Value {arg} in function {func_name} not in form data")
            tags = frame.func(*func_args)
            self.add_post(tags, frame.target, frame.out_target)
            return tags

        html_items = [tag.render() for tag in to_tag()]
        # print(html_items)
        return "\n".join(html_items)

    @staticmethod
    def add_post(tags: list, hx_target: str, out_hx_target: str):
        for tag in tags:
            if hx_target:
                tag["hx-target"] = f"#{hx_target}"
                tag["hx-post"] = f"/receiver?func_name={hx_target}"

        if out_hx_target:
            btn = button(
                "Submit",
                data_hx_post=f"/receiver?func_name={out_hx_target}",
                data_hx_target=f"#{out_hx_target}",
            )
            tags.append(btn)
        return tags

    def render(self):
        doc = document()
        _head = head(script(src="https://unpkg.com/htmx.org@1.3.2"))
        _body = body(*[frame.to_tag() for frame in self.frames.values()])
        doc.add(_head, _body)
        return doc.render()

    def input(self, target: str = "", out_target: str = ""):
        def decorator(func):
            tags = func()
            self.add_post(tags, target, out_target)
            self.append_frame(func, tags, target, out_target, "form")
            return tags

        return decorator

    def output(self):
        def decorator(func):
            tags = func()
            self.append_frame(func, tags)
            return tags

        return decorator

    def append_frame(
        self, func, tags: Any, target: str = "", out_target: str = "", frame_type: str = "div"
    ):
        func_name = func.__name__
        arguments = [arg for arg in inspect.signature(func).parameters]
        self.frames[func_name] = Frame(
            **{
                "id_": func_name,
                "func": func,
                "target": target,
                "arguments": arguments,
                "out_target": out_target,
                "tags": tags,
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
