from copy import deepcopy
from pydantic import BaseModel
from typing import List, Any
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from dominate.tags import div, p, script, head, body, button, input_
from dominate.util import raw
from dominate import document as doc

from giotto.templates import AppSite
from giotto.navigation import Sidebar
from giotto.icons import IconBin, IconDetails, IconPlay, IconStop
from giotto.elements import Box, Button, Table, Text
from .views import JobRunsTable, JobsTable
import mockapis

prefix = "scheduler"
router = APIRouter(prefix=f"/{prefix}")


@router.get("/", response_class=HTMLResponse)
def index():
    site = AppSite(sidebar=Sidebar(items=mockapis.sidebar_items))
    table_jobs = JobsTable.from_dict(prefix, mockapis.jobs["data"]).tag
    site.content = div(table_jobs, div(_id="jobs_table"))
    return site.html


@router.post("/jobruns", response_class=HTMLResponse)
def jobruns(name: str):
    tag = JobRunsTable.from_dict(url_prefix=prefix, job_name=name, data=mockapis.jobruns).tag
    return tag.render()


@router.post("/job_refresh", response_class=HTMLResponse)
def jobruns_refresh(job_name: str):
    view = JobRunsTable.from_dict(url_prefix=prefix, job_name=job_name, data=mockapis.jobruns)
    view.jobrun_status = "success"
    return view.tag.render()


@router.post("/job_run", response_class=HTMLResponse)
def run_job(job_name: str):
    view = JobRunsTable.from_dict(url_prefix=prefix, job_name=job_name, data=mockapis.jobruns)
    view.jobrun_status = "running"
    return view.tag.render()