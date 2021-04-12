from giotto.base import Action
from giotto.elements import Box, Button, ClickableIcon, Table, Text
from giotto.icons import IconBin, IconDetails, IconPlay, IconRefresh, IconStop
from giotto.navigation import Sidebar
from giotto.templates import App

from . import mockapis

prefix = "scheduler"
webapp = App(prefix="/scheduler", sidebar=Sidebar(items=mockapis.sidebar_items))


@webapp.frame(type_="form")
def jobs():
    return get_jobs_frame()


@webapp.frame(class_="flex flex-col m-4 border")
def jobruns(job_name: str = ""):
    if job_name:
        return get_jobruns_frame(job_name=job_name)
    else:
        return []


def get_jobs_frame():
    data = get_jobs_data()
    data = format_jobs_data(data)
    table = Table(data=data, max_rows=5)
    return [table]


def get_jobs_data():
    return mockapis.jobs["data"]


def format_jobs_data(data):
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
        action = Action(
            url=f"/{prefix}/receiver?func_name=jobruns&job_name={job_name}",
            target="#jobruns",
            swap=None,
        )
        new_row["Action"] = ClickableIcon(icon=IconDetails(), action=action)

        for key, value in row.items():
            new_key = key.replace("_", " ").title()
            new_row[new_key] = value
            if key in formatter:
                new_row[new_key] = formatter[key](value)
        new_data.append(new_row)
    return new_data


def get_jobruns_frame(job_name: str):
    data = get_jobruns_data(job_name=job_name)
    title = Text(value=f"## {job_name}")

    run_btn = Button(
        description="Run",
        color="green",
        icon=IconPlay(),
        action=Action(url=f"/{prefix}/jobs/{job_name}/run", target="#jobs_table"),
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
        action=Action(url=f"/{prefix}/jobruns/{job_name}/refresh", target="#jobs_table"),
    )
    table_jobruns = Table(data=data, max_rows=5)
    box = Box(contents=[title, run_btn, stop_btn, unregister_btn, refresh_btn])
    return [box, table_jobruns]


def get_jobruns_data(job_name: str):
    return mockapis.jobruns_raw.get(job_name, {}).get("data", [])


# @router.post("/jobruns/{job_name}/refresh", response_class=HTMLResponse, tags=["JobRunsTable"])
# def refresh_jobruns(job_name: str):
#     view = JobRunsTable.from_dict(url_prefix=prefix, job_name=job_name, data=mockapis.jobruns)
#     view.jobrun_status = "success"
#     return view.to_html()


# @router.post("/jobs/{job_name}/run", response_class=HTMLResponse, tags=["JobRunsTable"])
# def run_job(job_name: str):
#     view = JobRunsTable.from_dict(url_prefix=prefix, job_name=job_name, data=mockapis.jobruns)
#     view.jobrun_status = "running"
#     return view.to_html()