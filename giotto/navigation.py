from typing import List

from dominate.tags import a, aside, div, h1, img, li, nav, span, ul
from pydantic import BaseModel

from .icons import IconFiles, IconHMenu


class TopBar(BaseModel):
    value: str = "Site Name"

    @property
    def _ul_left(self):
        icon = IconHMenu().to_tag()
        mlink = a(icon, href="#")
        li_ = li(mlink, _class="h-6 w-8")
        ul_left = ul(li_, _class="flex items-center")
        return ul_left

    @property
    def _ul_center(self):
        h1_ = h1(self.value, _class="pl-8 lg:pl-0 text-white font-bold")
        li_ = li(h1_)
        ul_center = ul(li_, _class="flex items-center")
        return ul_center

    @property
    def _ul_right(self):
        img_ = img(
            _class="h-full w-full rounded-full mx-auto",
            src=(
                "https://avatars.githubusercontent.com/u/54931660?s=400&u=dcf55"
                "50498aee3550f2b2f835345d802fabe1833&v=4&_sm_au_=iNVf4trk1MFNLS"
                "NnVsBFjK664v423"
            ),
            alt="profile boss",
        )
        li_ = li(img_, _class="h-10 w-10")
        ul_right = ul(li_, _class="flex items-center")
        return ul_right

    def to_tag(self):
        uls = (self._ul_left, self._ul_center, self._ul_right)
        nav_ = nav(*uls, _class="p-4 flex justify-between bg-dark h-full border-cgrey_200")
        tag = div(nav_, _class="flex-1 flex flex-col overflow-hidden", _style="height: 5vh")
        return tag


class Sidebar(BaseModel):
    items: List
    selected: dict = {}

    def to_tag(self):
        tag = aside(_class="hidden md:flex bg-dark w-44 pt-5 sm:mt-0")
        _nav = nav()
        for item in self.items:
            _item = div(data_action="click->collapse#unhide", data_controller="collapse")
            lev1 = a(
                _class=(
                    "flex w-44 items-center py-2  pl-2 mt-2 "
                    "text-white border-r-4 border-gray-100 "
                    "hover:bg-cgrey_200 hover:border-white "
                ),
                href="#",
                data_turbo="false",
                data_collapse_target="levelone",
            )
            icon = IconFiles().to_tag()
            _span = span(item["text"], _class="mx-4 font-medium")
            lev1.add(icon, _span)
            if "subheaders" in item:
                for subitem in item["subheaders"]:
                    style = "flex w-44 items-center py-2 pl-10 text-white bg-cgrey_200 hover:text-dark border-t-2"
                    if item["text"] == self.selected.get("lev1"):
                        if subitem["text"] == self.selected.get("lev2"):
                            style += " selected"
                    else:
                        style += " hidden"
                    lev2 = a(
                        _class=style,
                        href=subitem["href"],
                        data_collapse_target="leveltwo",
                    )
                    _span = span(subitem["text"], _class="mx-4")
                    lev2.add(_span)
                    lev1.add(lev2)
            _item.add(lev1)
            _nav.add(_item)
        tag.add(_nav)
        return tag
