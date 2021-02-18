from typing import List
from dominate.tags import div, option, select
from dominate.dom_tag import dom_tag
from pydantic import BaseModel

class tag_hyphenate(type):
    def __new__(cls, name, bases, dict):
        return type.__new__(cls, name.replace("_", "-"), bases, dict)


class turbo_frame(dom_tag, metaclass=tag_hyphenate):
    pass

class svg(dom_tag): 
    pass

#in theory this should be abstract class
class Partial(BaseModel):
    is_frame: bool = False

    def to_tag(self):
        pass

class path(dom_tag): 
    pass

class Select(Partial):
    options: List

    #@frame(url=..., whatever=...)
    def to_tag(self):
        tag = div(_class="relative inline-flex")
        _svg = svg(_class="w-2 h-2 absolute top-0 right-0 m-4 pointer-events-none", xmlns="http://www.w3.org/2000/svg", viewBox="0 0 412 232")
        _svg.add(path(d="M206 171.144L42.678 7.822c-9.763-9.763-25.592-9.763-35.355 0-9.763 9.764-9.763 25.592 0 35.355l181 181c4.88 4.882 11.279 7.323 17.677 7.323s12.796-2.441 17.678-7.322l181-181c9.763-9.764 9.763-25.592 0-35.355-9.763-9.763-25.592-9.763-35.355 0L206 171.144z", fill="#648299", fill_rule="nonzero"))
        tag.add(_svg)
        _class = """"border border-gray-300 text-gray-600 h-10 pl-5 pr-10 bg-white hover:border-gray-400 focus:outline-none appearance-none"""
        _select = select(_class=_class)
        for text in self.options:
            _select.add(option(text))
        tag.add(_select)
        if self.is_frame:
            tag = turbo_frame(tag)
        return tag

print(Select(options=["oranges", "apples", "bananas"], is_frame=True).to_tag().render())
