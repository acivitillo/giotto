import inspect
from fastapi import Form, Request
from fastapi.responses import HTMLResponse
from typing import List, Dict, Any
from dominate import tags
from dominate.tags import h1, select, option, div, body, head, script, form
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

    def append_function(self, func, target=""):
        func_name = func.__name__
        arguments = [arg for arg in inspect.signature(func).parameters]
        print(arguments)
        self.functions[func_name] = {"func": func, "target": target, "args": arguments}
        return self

    async def receiver(self, request: Request, func_name: str):
        form = await request.form()

        def to_tag():
            func = self.functions[func_name]["func"]
            args = self.functions[func_name]["args"]
            func_args = []
            print(form)
            for arg in args:
                try:
                    func_args.append(form[arg])
                except KeyError:
                    raise KeyError(f"Value {arg} in function {func_name} not in form data")
            result = func(*func_args)
            return result

        tag = to_tag()
        return tag.render()

    def register(self):
        self.app.add_api_route(
            "/receiver", self.receiver, methods=["POST"], response_class=HTMLResponse
        )
        self.app.add_api_route("/", self.render, methods=["GET"], response_class=HTMLResponse)
        return self

    def input(self, frame_name: str, target: str = ""):
        def decorator(func):
            func_name = func.__name__
            self.append_function(func, target)
            if target != "":
                if target == func_name:
                    _id = "this"
                else:
                    _id = f"#{target}"
                route = f"/receiver?func_name={target}"
            else:
                route = f"/receiver?func_name={func_name}"

            tag = func()
            tag["hx-target"] = _id
            tag["hx-post"] = route
            self.append_frame(frame_name, tag, "form")
            return tag

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
    options: List[Any]

    @classmethod
    def from_list(cls, name: str, options: List):
        out_options = []
        for opt in options:
            out_options.append(option(opt))
        return cls(name=name, options=out_options)

    def to_tag(self):
        sel = select(name=self.name)
        for opt in self.options:
            sel.add(opt)
        return sel
