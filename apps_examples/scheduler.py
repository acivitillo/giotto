from copy import deepcopy
import os
from typing import List

from pydantic import BaseModel

from giotto.elements import Box, Button, Table, Text
from giotto.icons import IconBin, IconDetails, IconPlay, IconStop
from giotto.navigation import Sidebar
from giotto.templates import AppLayout, FrameTemplate
from giotto.transformers import Transformer
from giotto.utils import turbo_frame
import mockapis

domain = os.getenv("DOMAIN")


class JobsTransformer(Transformer):
    def transform(self):
        data = deepcopy(self.data["data"])

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


class JobRunsTransformer(Transformer):
    def transform(self):
        data = deepcopy(self.data["data"])
        return data


jobs_tr = JobsTransformer.from_dict(mockapis.jobs)
# jobs_tr = JobsTransformer.from_api(url=f"{domain}/api/scheduler/job")
jobs_data = jobs_tr.transform()

table_jobs = Table(data=jobs_data)


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
            box = Box(contents=[title, run_btn, stop_btn, unregister_btn]).to_tag()

            # jobruns_tr = JobRunsTransformer.from_api(
            #     url=f"{domain}/api/scheduler/jobrun/{job_name}"
            # )
            # data = jobruns_tr.transform()
            data = mockapis.jobruns_raw[job_name]["data"]
            table_jobruns = Table(data=data).to_tag()
            tag.add(box)
            tag.add(table_jobruns)
            return tag.render()
        else:
            tag = turbo_frame(_id="schedulerframe")
            return tag.render()


class SchedulerAppLayout(AppLayout):
    route = "/scheduler"
    sidebar = Sidebar(items=mockapis.sidebar_items)
    content: List[BaseModel] = [table_jobs, JobrunsFrame()]
    site_name = "Scheduler App"
