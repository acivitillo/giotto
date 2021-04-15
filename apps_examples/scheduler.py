from typing import Any, Dict, List

from fastapi.responses import HTMLResponse

from giotto.base import Style
from giotto.elements import Button, ClickableIcon, Column, Row, Table, Text
from giotto.icons import IconBin, IconDetails, IconPlay, IconRefresh, IconStop
from giotto.navigation import Sidebar
from giotto.app import App

from . import mockapis

prefix = "scheduler"
webapp = App(prefix="/scheduler", sidebar=Sidebar(items=mockapis.sidebar_items))

# FRAMES
# ------


@webapp.frame()
def jobs():
    data = get_jobs_data()
    data = format_jobs_data(data)
    table = Table(
        data=data,
        max_rows=5,
        column_width={"Action": "70px", "Created At": "100px", "Crons": "130px"},
    )
    return [table]


@webapp.frame(class_="flex flex-col mb-4 shadow sm:rounded-lg", style=Style(margin=1))
def jobruns(job_name: str = "", message: str = ""):
    if job_name:
        return get_jobruns_frame(job_name=job_name, message=message)
    else:
        return []


def get_jobruns_frame(job_name: str, message: str):
    data = get_jobruns_data(job_name=job_name)
    jobs_data = get_jobs_data(job_name=job_name)[0]
    text = (
        f"# {job_name}\n"
        f"**Description**: {jobs_data['description']}<br>"
        f"**Timeout**: {jobs_data['timeout']}<br>"
        f"**Function**: {jobs_data['function']}<br>"
        f"**Function Args**: {jobs_data['func_args']}<br>"
        f"**Function Kwargs**: {jobs_data['func_kwargs']}<br>"
    )
    title = Text(value=text)
    style = Style(margin=1, rounded=True, height=12)

    action = webapp.get_action("run_job", func_kwargs={"job_name": job_name})
    action.confirm = f"Are you sure you want to run {job_name}?"
    run_btn = Button(description="Run", color="green", icon=IconPlay(), action=action, style=style)

    action = webapp.get_action("stop_job", func_kwargs={"job_name": job_name})
    action.confirm = f"Are you sure you want to stop {job_name}?"
    stop_btn = Button(description="Stop", color="red", icon=IconStop(), action=action, style=style)

    action = webapp.get_action("jobruns", func_kwargs={"job_name": job_name})
    refresh_btn = Button(
        description="Refresh", color="indigo", icon=IconRefresh(), action=action, style=style
    )

    action = webapp.get_action("unregister_job", func_kwargs={"job_name": job_name})
    action.confirm = f"Are you sure you want to unregister {job_name}?"
    unregister_btn = Button(
        description="Unregister", color="purple", icon=IconBin(), action=action, style=style
    )

    text = Text(value=message, style=Style(margin=1))
    table_jobruns = Table(data=data, max_rows=5)
    buttons = Row(contents=[run_btn, stop_btn, unregister_btn, refresh_btn, text])
    box = Column(contents=[title, buttons])
    return [box, table_jobruns]


# ACTIONS
# -------


@webapp.action(target="jobruns")
def run_job(job_name: str):
    status = post_job_action(job_name, "run")
    status_mapper = {
        True: f"Job {job_name} successfully enqueued",
        False: f"Job {job_name} is already running",
    }
    return webapp.frames["jobruns"].run(job_name=job_name, message=status_mapper.get(status))


@webapp.action(target="jobruns")
def stop_job(job_name: str):
    status = post_job_action(job_name, "stop")
    status_mapper = {
        True: f"Job {job_name} successfully stopped",
        False: f"Job {job_name} is not running",
    }
    return webapp.frames["jobruns"].run(job_name=job_name, message=status_mapper.get(status))


@webapp.action()
def unregister_job(job_name: str):
    status = post_job_action(job_name, "unregister")
    response = HTMLResponse(content=webapp.to_html(), headers={"HX-Refresh": "true"})
    return response


# LOADING AND FORMATTING DATA
# ---------------------------


def get_jobs_data(job_name: str = None):
    data = mockapis.jobs["data"]
    if job_name:
        for job in data:
            if job["name"] == job_name:
                return [job]
    return data


def format_jobs_data(data: List[Dict[str, Any]]):
    def remove_first_and_last(x):
        return str(x)[1:-1]

    cols_to_remove = ["description", "timeout", "function", "func_args", "func_kwargs"]
    cols_for_strip = ["crons", "upstream", "downstream"]
    formatter = {
        "created_at": lambda x: x[:10],
        **{k: remove_first_and_last for k in cols_for_strip},
    }
    new_data = []
    for row in data:
        new_row = dict()
        job_name = row["name"]
        action = webapp.get_action("jobruns", func_kwargs={"job_name": job_name})
        new_row["Action"] = ClickableIcon(icon=IconDetails(), action=action)
        for key, value in row.items():
            if key in cols_to_remove:
                continue
            new_key = key.replace("_", " ").title()
            new_row[new_key] = value
            if key in formatter:
                new_row[new_key] = formatter[key](value)
        new_data.append(new_row)
    return new_data


def get_jobruns_data(job_name: str):
    return mockapis.jobruns_raw.get(job_name, {}).get("data", [])


# UTILS
# -----


def post_job_action(job_name: str, action: str):
    return True