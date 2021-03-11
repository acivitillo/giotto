from typing import Any, Dict, Optional

from dominate.tags import div
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

router = APIRouter()


@router.get("/frames", response_class=HTMLResponse)
def frames():
    return "hello"


class Frame(BaseModel):
    src: str

    def register_url(self, app: Any, func: Any, methods=["get"]):
        app.add_api_route(self.src, func, methods=methods, response_class=HTMLResponse)
        return True


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
        return tag

    def render(self):
        return self.to_tag().render()

    def _repr_html_(self):
        return self.render()
        # return self.to_html_jj()
