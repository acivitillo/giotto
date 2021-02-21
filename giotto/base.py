from fastapi.responses import HTMLResponse
from fastapi import APIRouter

from typing import Any, Dict, Optional

from dominate.tags import div
from pydantic import BaseModel

from typing import Any
from .utils import turbo_frame

router = APIRouter()


@router.get("/frames", response_class=HTMLResponse)
def frames():
    return "hello"


class Frame(BaseModel):
    name: str
    src: str

    def register_url(self, app: Any, func: any, methods=["get"]):
        app.add_api_route(self.src, func, methods=methods, response_class=HTMLResponse)
        return True

    def wrap(self, *args):
        """Wrap component into turbo frame."""
        return turbo_frame(*args, _id=self.name, src=self.src)


class Partial(BaseModel):
    frame: Optional[Frame] = None

    @classmethod
    def from_api(cls, url):
        # data = from_api()
        # return cls(**data)
        pass

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(**data)

    def _to_tag(self):
        # abstract method, needs to be implemented in child
        return div()

    def to_tag(self):
        tag = self._to_tag()
        if self.frame:
            return self.frame.wrap(tag)
        else:
            return tag

    def render(self):
        return self.to_tag().render()

    def to_html_jj(self):
        import jinja2 as jj

        jinja_env = jj.Environment(loader=jj.FileSystemLoader("templates"))
        name = self.__class__.__name__.lower()
        template = jinja_env.get_template(f"{name}.html")
        html = template.render(**self.dict())
        return html

    def _repr_html_(self):
        return self.render()
        # return self.to_html_jj()
