from pydantic import BaseModel
from typing import List
from dominate.tags import div, nav, ul, li, a, h1, img, aside, span

from .icons import IconHMenu, IconFiles


class TopBar(BaseModel):
    value: str = "Site Name"

    def to_tag(self):
        tag = div(_class="flex-1 flex flex-col")
        n = nav(_class="px-4 flex justify-between bg-dark h-16 border-b-2 border-cgrey_200")
        uleft = ul(_class="flex items-center")
        l = li(_class="h-6 w-8")
        icon = IconHMenu().to_tag()
        mlink = a(href="#")
        mlink.add(icon)
        l.add(mlink)
        uleft.add(l)
        ucenter = ul(_class="flex items-center")
        l = li()
        l.add(h1(self.value, _class="pl-8 lg:pl-0 text-white font-bold"))
        ucenter.add(l)
        uright = ul(_class="flex items-center")
        l = li(_class="h-10 w-10")
        im = img(
            _class="h-full w-full rounded-full mx-auto",
            src="https://avatars.githubusercontent.com/u/54931660?s=400&u=dcf5550498aee3550f2b2f835345d802fabe1833&v=4&_sm_au_=iNVf4trk1MFNLSNnVsBFjK664v423",
            alt="profile boss",
        )
        l.add(im)
        uright.add(l)
        n.add(uleft)
        n.add(ucenter)
        n.add(uright)
        tag.add(n)
        return tag


class Sidebar(BaseModel):
    items: List

    def to_tag(self):
        tag = aside(_class="hidden md:flex bg-dark w-44 h-screen pt-5 sm:mt-0")
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
                    lev2 = a(
                        _class="flex w-44 items-center py-2 pl-10 text-white bg-cgrey_200 hidden hover:text-dark border-t-2",
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