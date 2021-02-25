from typing import Any, Dict, List

from pydantic import BaseModel

from giotto.elements import Box, Input, Table, Text, Button, Row
from giotto.navigation import Sidebar
from giotto.templates import AppLayout, FrameTemplate
from giotto.transformers import Transformer
from giotto.utils import turbo_frame
from giotto.icons import IconSearch, IconDetails, IconStop, IconPlay, IconBin
import mockapis


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
        new_row["Action"] = Button(
            description="",
            color="blue",
            name=row["name"] + "_details",
            icon=IconDetails(),
            action="swap",
            is_flex=True,
            target_frame="schedulerframe",
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


jobs_data = transform_data_jobs(mockapis.jobs)
jobruns_data = Transformer.from_dict(mockapis.jobruns).apply(transform_data_jobruns).data


inp = Input(placeholder="Search Job...")
table_jobs = Table(data=jobs_data)
table_jobruns2 = Table(data=jobruns_data)
# class
# route = "/some/api"
# job_name = ...
# get /some/api?job_name=...
# transform jobs into [{}]
# from_dict
# Table.from_function(transform_data_jobruns, "/some/api", params)
# Frame
class JobrunsFrame(FrameTemplate):
    route = "/frameurl"
    content: List[BaseModel] = []
    name = "schedulerframe"

    def to_html(self, name: str = "", route: str = ""):
        if route == "":
            route = self.route
        tag = turbo_frame(_id="schedulerframe", src=route)
        if name[-8:] == "_details":
            job_name = name[:-8]
            title = Text(value=job_name, size="4xl", weight="bold")
            run_btn = Button(
                description="Run",
                color="green",
                icon=IconPlay(),
                action="swap",
                name=job_name + "_run",
            )
            stop_btn = Button(
                description="Stop",
                color="red",
                icon=IconStop(),
                action="swap",
                name=job_name + "_stop",
            )
            unregister_btn = Button(
                description="Unregister",
                color="purple",
                icon=IconBin(),
                action="swap",
                name=job_name + "_unregister",
            )
            # buttons = Row(contents=[run_btn, stop_btn])
            box = Box(contents=[title, run_btn, stop_btn, unregister_btn]).to_tag()
            table_jobruns = Table(data=mockapis.jobruns_raw[job_name]["data"]).to_tag()
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
