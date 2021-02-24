from typing import Any, Dict, List

from pydantic import BaseModel

from giotto.elements import Box, Input, Table, Text, Button
from giotto.navigation import Sidebar
from giotto.templates import AppLayout, FrameTemplate
from giotto.transformers import Transformer
from giotto.utils import turbo_frame
from giotto.icons import IconSearch, IconDetails, IconStop, IconPlay
import mockapis

inp = Input(placeholder="Search Job...")
description_btn = Button(
    description="", color="blue", icon=IconDetails(), action="swap", is_flex=True
)


def transform_data_jobs(data: Dict):
    data = data["data"]

    def remove_first_and_last(x):
        return str(x)[1:-1]

    cols_for_strip = ["func_args", "crons", "upstream", "downstream", "func_kwargs"]
    formatter = {
        "created_at": lambda x: x[:10],
        **{k: remove_first_and_last for k in cols_for_strip},
    }
    new_data = []
    for row in data:
        new_row = dict()
        new_row["action"] = Button(
            description="",
            color="blue",
            name=row["name"] + "_details",
            icon=IconDetails(),
            action="swap",
            is_flex=True,
        )
        for key, value in row.items():
            new_key = key.replace("_", " ").title()
            new_row[new_key] = value
            if key in formatter:
                new_row[new_key] = formatter[key](value)
        new_data.append(new_row)
    return new_data


def transform_data_jobruns(data: Dict):
    data = data["data"]
    return data


jobs_data = Transformer.from_dict(mockapis.jobs).apply(transform_data_jobs).data
jobruns_data = Transformer.from_dict(mockapis.jobruns).apply(transform_data_jobruns).data

table_jobs = Table(data=jobs_data)
table_jobruns2 = Table(data=jobruns_data)

# Frame
class JobrunsFrame(FrameTemplate):
    route = "/someurl"
    content: List[BaseModel] = []

    def to_html(self, name: str = "", route: str = ""):
        if route == "":
            route = self.route
        tag = turbo_frame(_id="frametest", src=route)
        if name[-8:] == "_details":
            run_btn = Button(
                description="", color="green", icon=IconPlay(), action="run", is_flex=True
            )
            stop_btn = Button(
                description="", color="red", icon=IconStop(), action="stop", is_flex=True
            )
            box = Box(contents=[run_btn, stop_btn]).to_tag()
            table_jobruns = Table(data=jobruns_data["name"]).to_tag()
            tag.add(box)
            tag.add(table_jobruns)
        return tag.render()


# Page
content = Box(contents=[inp, table_jobs])


class SchedulerAppLayout(AppLayout):
    route = "/scheduler"
    sidebar = Sidebar(items=mockapis.sidebar_items)
    content: List[BaseModel] = [content, JobrunsFrame()]
    site_name = "Scheduler App"
