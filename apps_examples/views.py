from copy import deepcopy
from pydantic import BaseModel
from typing import Any, Dict, List

from dominate.tags import div, p, script, head, body, button, input_
from dominate.util import raw
from dominate import document as doc

from giotto.elements import Box, Button, Table, Text
from giotto.icons import IconBin, IconDetails, IconPlay, IconStop


class BaseView(BaseModel):
    data: Dict = {}
    url_prefix: str = ""


class JobsTable(BaseView):
    data: Dict = {}
    url_prefix: str = ""

    @classmethod
    def from_dict(cls, url_prefix: str, data: Any):
        cls.url_prefix = url_prefix

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
            name = row["name"] + "_details"
            new_row["Action"] = Button(
                description="",
                color="blue",
                name=name,
                icon=IconDetails(),
                is_flex=True,
                hx_post=f"/{url_prefix}/jobruns?name={name}",
                hx_target="#jobs_table",
            )
            for key, value in row.items():
                new_key = key.replace("_", " ").title()
                new_row[new_key] = value
                if key in formatter:
                    new_row[new_key] = formatter[key](value)
            new_data.append(new_row)
        return cls(data={"table": new_data}, url_prefix=url_prefix)

    @property
    def tag(self):
        tag = Table(data=self.data["table"]).to_tag()
        return tag


class JobRunsTable(BaseView):
    jobrun_status: str = ""

    @classmethod
    def from_dict(cls, job_name: str, data: Any, url_prefix: str = ""):
        tabledata = deepcopy(data["data"])
        tabledata.sort(key=lambda item: item.get("created_at"))
        data = {"table": tabledata, "job_name": job_name, "url_prefix": url_prefix}
        return cls(data=data, url_prefix=url_prefix)

    @property
    def tag(self):
        tag = div(_id="jobs_table")
        data = self.data["table"]
        prefix = self.data["url_prefix"]
        if "details" in self.data["job_name"]:
            job_name = self.data["job_name"][:-8]
        else:
            job_name = self.data["job_name"]
        title = Text(value=job_name, size="4xl", weight="bold")
        if self.jobrun_status != "":  # mock "running" case
            record = data[0]
            record["status"] = self.jobrun_status
            data.append(record)
        run_btn = Button(
            description="Run",
            color="green",
            icon=IconPlay(),
            hx_post=f"/{prefix}/job_run?job_name={job_name}",
            hx_target="#jobs_table",
        )
        stop_btn = Button(
            description="Stop", color="red", icon=IconStop(), hx_post="/tbd", hx_target="tbd"
        )
        unregister_btn = Button(
            description="Unregister",
            color="purple",
            icon=IconBin(),
            hx_post="/tbd",
            hx_target="tbd",
        )
        refresh_btn = Button(
            description="Refresh",
            color="purple",
            icon=IconBin(),
            hx_post=f"/{prefix}/job_refresh?job_name={job_name}",
            hx_target="#jobs_table",
        )
        table_jobruns = Table(data=data, max_rows=5).to_tag()
        box = Box(contents=[title, run_btn, stop_btn, unregister_btn, refresh_btn]).to_tag()
        tag.add(box, table_jobruns)
        return tag