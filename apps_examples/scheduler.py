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
    table_jobs = JobsTable.from_dict(prefix, mockapis.jobs["data"]).to_tag()
    site.content = div(table_jobs, div(_id="jobs_table"))
    return site.to_html()


@router.post("/jobruns/{job_name}", response_class=HTMLResponse, tags=["JobRunsTable"])
def read_jobruns(job_name: str):
    view = JobRunsTable.from_dict(url_prefix=prefix, job_name=job_name, data=mockapis.jobruns)
    return view.to_html()


@router.post("/jobruns/{job_name}/refresh", response_class=HTMLResponse, tags=["JobRunsTable"])
def refresh_jobruns(job_name: str):
    view = JobRunsTable.from_dict(url_prefix=prefix, job_name=job_name, data=mockapis.jobruns)
    view.jobrun_status = "success"
    return view.to_html()


@router.post("/jobs/{job_name}/run", response_class=HTMLResponse, tags=["JobRunsTable"])
def run_job(job_name: str):
    view = JobRunsTable.from_dict(url_prefix=prefix, job_name=job_name, data=mockapis.jobruns)
    view.jobrun_status = "running"
    return view.to_html()
