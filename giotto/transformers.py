import json
from typing import Any

from pydantic import BaseModel
import urllib3


class Transformer(BaseModel):
    data: Any

    @classmethod
    def from_api(cls, url: str):
        http = urllib3.PoolManager()
        resp = http.request("GET", url)
        data = json.loads(resp.data)
        return cls(data=data)

    @classmethod
    def from_dict(cls, data: Any):
        return cls(data=data)