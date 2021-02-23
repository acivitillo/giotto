# from typing import List

# from pydantic import BaseModel


# class DropdownTransformer(BaseModel):
#     data: List[str]

#     @classmethod
#     def from_api(cls, url):
#         pass

#     def transform(self):
#         return self.data


# class CustomTransformer(BaseModel):
#     data: JobAll

#     @classmethod
#     def from_api(cls, url):
#         pass

#     def transform(self):
#         names = []
#         for job in data:
#             names.append(job.name)
#         return names


# class Dropdown(Partial):
#     transformer: DropdownTransformer


# class Transformer(BaseModel):
#     def from_api(self):
#         pass

#     def apply(self):
#         pass


# # 1
# def to_dropdown_schema(values):
#     pass


# data = Transformer.from_api(url).apply(to_dropdown_schema).to_dict()
# Dropdown.from_dict(data)
# in theory this should be abstract class

# 2
# Dropdown.from_api(url)