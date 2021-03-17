from copy import deepcopy
from typing import Any, Dict, List

from dominate.tags import div
from pydantic import BaseModel

from giotto.base import Action
from giotto.elements import Box, Button, Table, Text, ClickableIcon, Row
from giotto.icons import IconBin, IconDetails, IconPlay, IconRefresh, IconStop


class BaseView(BaseModel):
    data: Dict = {}
    url_prefix: str = ""

    def to_tag(self):
        return div()

    def to_html(self):
        return self.to_tag().render()


class JobsTable(BaseView):
    @classmethod
    def from_dict(cls, url_prefix: str, data: Any):
        new_data = cls.format_data(url_prefix, data)
        return cls(data={"table": new_data}, url_prefix=url_prefix)

    @staticmethod
    def format_data(url_prefix: str, data: Any) -> List[Dict]:
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
            job_name = row["name"]
            action = Action(url=f"/{url_prefix}/jobruns/{job_name}", target="#jobs_table")
            new_row["Action"] = ClickableIcon(icon=IconDetails(), action=action)

            for key, value in row.items():
                new_key = key.replace("_", " ").title()
                new_row[new_key] = value
                if key in formatter:
                    new_row[new_key] = formatter[key](value)
            new_data.append(new_row)
        return new_data

    def to_tag(self):
        tag = Table(data=self.data["table"], max_rows=5).to_tag()
        return tag


class JobRunsTable(BaseView):
    jobrun_status: str = ""
    job_name: str

    @classmethod
    def from_dict(cls, job_name: str, data: Any, url_prefix: str = ""):
        data = cls.format_data(data)
        return cls(data={"table": data}, job_name=job_name, url_prefix=url_prefix)

    @staticmethod
    def format_data(data: Any) -> List[Dict]:
        data = deepcopy(data["data"])
        data.sort(key=lambda item: item.get("created_at"))
        return data

    def to_tag(self):
        tag = div(_id="jobs_table")
        data = self.data["table"]
        url_prefix = self.url_prefix
        job_name = self.job_name
        title = Text(value=job_name, size="4xl", weight="bold")
        if self.jobrun_status != "":  # mock "running" case
            record = data[0]
            record["status"] = self.jobrun_status
            data.append(record)

        run_btn = Button(
            description="Run",
            color="green",
            icon=IconPlay(),
            action=Action(url=f"/{url_prefix}/jobs/{job_name}/run", target="#jobs_table"),
        )

        stop_btn = Button(
            description="Stop",
            color="red",
            icon=IconStop(),
            action=Action(url="/tbd", target="#tbd"),
        )

        unregister_btn = Button(
            description="Unregister",
            color="purple",
            icon=IconBin(),
            action=Action(url="/tbd", target="#tbd"),
        )

        refresh_btn = Button(
            description="Refresh",
            color="purple",
            icon=IconRefresh(),
            action=Action(url=f"/{url_prefix}/jobruns/{job_name}/refresh", target="#jobs_table"),
        )
        table_jobruns = Table(data=data, max_rows=5).to_tag()
        box = Box(contents=[title, run_btn, stop_btn, unregister_btn, refresh_btn]).to_tag()
        tag.add(box, table_jobruns)
        return tag
