import json
import os

import urllib3

from giotto.app import App
from giotto.app import Style
from giotto.elements import Text
from giotto.navigation import Sidebar

from . import mockapis


webapp = App(
    prefix="/ghpage",
    sidebar=Sidebar(
        items=mockapis.sidebar_items,
        selected={"lev1": "Documentation", "lev2": "Giotto Readme"},
    ),
)

# FRAMES
# ------


@webapp.frame()
def index():
    proxy_url = os.getenv("HTTP_PROXY", "")
    readme_md = get_readme(owner="acivitillo", repo="giotto", proxy_url=proxy_url, path="README.md")
    text = Text(value=readme_md, style=Style(margin=5))
    return [text]


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
    out = ""
    for item in data:
        if item["name"] == path:
            resp = con.request("GET", item["download_url"], headers=headers)
            out = resp.data.decode("utf-8")
    return out
