from functools import wraps
from typing import List
from dominate.tags import div, option, select, _input
from dominate.dom_tag import dom_tag
from pydantic import BaseModel


class tag_hyphenate(type):
    def __new__(cls, name, bases, dict):
        return type.__new__(cls, name.replace("_", "-"), bases, dict)


class turbo_frame(dom_tag, metaclass=tag_hyphenate):
    pass


def frame(url: str = ""):
    def deco_wrap(f):
        @wraps(f)
        def wrapped(self, *args, **kwargs):
            func_out = f(self, *args, **kwargs)
            return turbo_frame(func_out, url=url)

        return wrapped

    return deco_wrap


class svg(dom_tag):
    pass


# in theory this should be abstract class
class Partial(BaseModel):
    def to_tag(self):
        pass

    def to_html_jj(self):
        import jinja2 as jj

        jinja_env = jj.Environment(loader=jj.FileSystemLoader("templates"))
        name = self.__class__.__name__.lower()
        template = jinja_env.get_template(f"{name}.html")
        html = template.render(**self.dict())
        return html


class path(dom_tag):
    pass


class Select(Partial):
    options: List

    @frame()
    def to_tag(self):
        tag = div(_class="relative inline-flex")
        _svg = svg(
            _class="w-2 h-2 absolute top-0 right-0 m-4 pointer-events-none",
            xmlns="http://www.w3.org/2000/svg",
            viewBox="0 0 412 232",
        )
        d = (
            "M206 171.144L42.678 7.822c-9.763-9.763-25.592-9.763-35.355 0-9.763"
            " 9.764-9.763 25.592 0 35.355l181 181c4.88 4.882 11.279 7.323 17.677"
            " 7.323s12.796-2.441 17.678-7.322l181-181c9.763-9.764 9.763-25.592"
            " 0-35.355-9.763-9.763-25.592-9.763-35.355 0L206 171.144z"
        )
        _svg.add(path(d=d, fill="#648299", fill_rule="nonzero"))
        tag.add(_svg)
        _class = (
            "border border-gray-300 text-gray-600 h-10 pl-5 pr-10 bg-white"
            " hover:border-gray-400 focus:outline-none appearance-none"
        )
        _select = select(_class=_class)
        for text in self.options:
            _select.add(option(text))
        tag.add(_select)
        return tag

    def _repr_html_(self):
        # return self.to_tag().render()
        return self.to_html_jj()


class Input(Partial):
    def to_tag(self):

        tag = div(_class="relative inline-flex")
        input_ = _input(
            type="search",
            _class=(
                "border border-gray-300 text-gray-600 h-10 pl-5 pr-10 bg-white"
                " hover:border-gray-400 focus:outline-none appearance-none"
            ),
            placeholder="Search by name...",
        )
        _svg = svg(
            _class="w-4 h-5 absolute top-0 right-0 m-3 pointer-events-none",
            xmlns="http://www.w3.org/2000/svg",
            fill="none",
            viewBox="0 0 24 24",
            stroke="currentColor",
        )
        _path = path(
            strokeLinecap="round",
            strokeLinejoin="round",
            strokeWidth="{2}",  # TODO: here we shouldn't have quotes
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z",
        )
        _svg.add(_path)
        tag.add(input_)
        tag.add(_svg)
        return tag


class TableAction(Partial):
    action_name: str