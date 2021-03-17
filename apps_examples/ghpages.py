import urllib3
import json
from dominate.tags import div
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import os

from giotto.navigation import Sidebar
from giotto.templates import AppSite
from giotto.elements import Text, Box

from . import mockapis
from .views import JobRunsTable, JobsTable
from .local_configs import proxy_url


proxy_url = proxy_url or os.getenv("HTTP_PROXY", "")
prefix = "ghpage"
router = APIRouter(prefix=f"/{prefix}")


def get_readme(owner: str, repo: str, path: str, proxy_url: str = "", token: str = ""):
    host = "https://api.github.com"
    url = f"{host}/repos/{owner}/{repo}/contents/"
    if proxy_url != "":
        con = urllib3.ProxyManager(proxy_url=proxy_url)
    else:
        con = urllib3.PoolManager()
    headers = {"User-Agent": "Accept: application/vnd.github.v3+json"}
    if token != "":
        headers["Authorization"] = f"token {token}"
    resp = con.request("GET", url, headers=headers)
    data = json.loads(resp.data)
    print("here", path)
    for item in data:
        if item["name"] == path:
            resp = con.request("GET", item["download_url"], headers=headers)
            out = resp.data.decode("utf-8")
    return out


@router.get("/", response_class=HTMLResponse)
def index(path: str, selected: str = ""):
    site = AppSite(
        sidebar=Sidebar(
            items=mockapis.sidebar_items,
            selected={"lev1": "Documentation", "lev2": "Giotto Readme"},
        )
    )
    readme_md = get_readme(owner="acivitillo", repo="giotto", proxy_url=proxy_url, path=path)
    text = Box(contents=[Text(value=readme_md)], centered=True).to_tag()
    site.content = div(text)
    return site.to_html()