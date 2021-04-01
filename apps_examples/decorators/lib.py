import inspect
from fastapi import Form, Request
from fastapi.responses import HTMLResponse
from typing import List, Dict, Any
from dominate import tags
from dominate.tags import h1, select, option, div, body, head, script, form, button
from dominate import document
from pydantic import BaseModel
from functools import wraps


class App(BaseModel):
    app: Any
    frames: Dict = {}
    functions: Dict = {}

    def form(self, name):
        def decorator(func):
            self.register_url(f"/{name}", func)
            try:
                tag = func()
            except TypeError:
                tag = func
            # tag = div(out, _id=name)
            try:
                self.frames[name].append(tag)
            except KeyError:
                self.frames[name] = []
                self.frames[name].append(tag)
            return func

        return decorator

    def append_frame(self, name: str, tag: Any, frame_type=""):
        try:
            self.frames[name]["tags"].append(tag)
        except KeyError:
            self.frames[name] = {"tags": [], "type": frame_type}
            self.frames[name]["tags"].append(tag)
        return self

    def append_function(self, func, route: str = "", target=""):
        func_name = func.__name__
        arguments = [arg for arg in inspect.signature(func).parameters]
        print(arguments)
        self.functions[func_name] = {
            "route": route,
            "func": func,
            "target": target,
            "args": arguments,
        }
        return self

    async def receiver(self, request: Request, func_name: str):
        form = await request.form()

        def to_tag():
            func = self.functions[func_name]["func"]
            args = self.functions[func_name]["args"]
            route = self.functions[func_name]["route"]
            target = self.functions[func_name]["target"]
            func_args = []
            for arg in args:
                try:
                    func_args.append(form[arg])
                except KeyError:
                    raise KeyError(f"Value {arg} in function {func_name} not in form data")
            tags = func(*func_args)
            out_tags = self.add_post(route, target, "message", tags)
            return out_tags

        html_items = [tag.render() for tag in to_tag()]
        print(html_items)
        return "\n".join(html_items)

    def register(self):
        self.app.add_api_route(
            "/receiver", self.receiver, methods=["POST"], response_class=HTMLResponse
        )
        self.app.add_api_route("/", self.render, methods=["GET"], response_class=HTMLResponse)
        return self

    def add_post(self, hx_post: str, hx_target: str, out_hx_target: str, tags: list):
        out_tags = []
        for tag in tags:
            tag["hx-target"] = hx_target
            tag["hx-post"] = hx_post
            out_tags.append(tag)
        btn = button(
            "Submit",
            data_hx_post=f"/receiver?func_name={out_hx_target}",
            data_hx_target=f"#{out_hx_target}",
        )
        out_tags.append(btn)
        return out_tags

    def input(self, frame_name: str, target: str = "", out_target: str = ""):
        def decorator(func):
            func_name = func.__name__
            if target != "":
                _target = f"#{target}"
                route = f"/receiver?func_name={target}"
            else:
                route = f"/receiver?func_name={func_name}"

            tags = func()
            out_tags = self.add_post(route, _target, out_target, tags)
            self.append_function(func, route, _target)
            _ = [self.append_frame(frame_name, tag, "form") for tag in out_tags]
            return out_tags

        return decorator

    def output(self, frame_name: str):
        def decorator(func):
            self.append_function(func)
            tag = func()
            self.append_frame(frame_name, tag)
            return tag

        return decorator

    def render(self):
        doc = document()
        _head = head(script(src="https://unpkg.com/htmx.org@1.3.2"))
        _body = body()
        for frame in self.frames:
            if self.frames[frame]["type"] == "form":
                parent_tag = form(_id=frame)
            else:
                parent_tag = div(_id=frame)
            for element in self.frames[frame]["tags"]:
                parent_tag.add(element)
            _body.add(parent_tag)
        doc.add(_head, _body)
        return doc.render()


class Select(BaseModel):
    name: str = ""
    options: List[str]
    selected: str = ""

    @classmethod
    def from_list(cls, name: str, options: List):
        return cls(name=name, options=options)

    def to_tag(self):
        sel = select(name=self.name)
        for opt in self.options:
            if opt == self.selected:
                sel.add(option(opt, selected=True))
            else:
                sel.add(option(opt))
        return sel
