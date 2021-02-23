from typing import Any, Callable, Dict, List

from pydantic import BaseModel


class Transformer(BaseModel):
    data: Any

    @classmethod
    def from_api(cls, url):
        pass

    @classmethod
    def from_dict(cls, data: Any):
        return cls(data=data)

    def apply(self, func: Callable):
        self.data = func(self.data)
        return self


# # 1
# def to_dropdown_schema(values):
#     pass


# data = Transformer.from_api(url).apply(to_dropdown_schema).to_dict()
# Dropdown.from_dict(data)
# in theory this should be abstract class

# 2
# Dropdown.from_api(url)