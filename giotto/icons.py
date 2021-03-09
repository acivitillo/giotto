from dominate.svg import svg, path

from .base import Partial


class Icon(Partial):
    pass


class IconHMenu(Icon):
    def _to_tag(self):
        tag = svg(
            xmlns="http://www.w3.org/2000/svg",
            fill="none",
            viewBox="0 0 24 28",
            stroke="currentColor",
        )
        _path = path(
            color="white",
            stroke_linecap="round",
            stroke_linejoin="round",
            d="M4 6h16M4 12h16M4 18h16",
        )
        tag.add(_path)
        return tag


class IconDownarrow(Icon):
    def _to_tag(self):
        tag = svg(
            _class="w-2 h-2 m-4 pointer-events-none",
            xmlns="http://www.w3.org/2000/svg",
            viewBox="0 0 412 232",
        )
        _path = path(
            d=(
                "M206 171.144L42.678 7.822c-9.763-9.763-25.592-9.763-35.355 0-9"
                ".763 9.764-9.763 25.592 0 35.355l181 181c4.88 4.882 11.279 7.3"
                "23 17.677 7.323s12.796-2.441 17.678-7.322l181-181c9.763-9.764 "
                "9.763-25.592 0-35.355-9.763-9.763-25.592-9.763-35.355 0L206 17"
                "1.144z"
            ),
            fill="#648299",
            fill_rule="nonzero",
        )
        tag.add(_path)
        return tag


class IconFiles(Icon):
    def _to_tag(self):
        tag = svg(
            _class="h-5 w-5", viewBox="0 0 24 24", fill="none", xmlns="http://www.w3.org/2000/svg"
        )
        _path = path(
            d=(
                "M19 11H5M19 11C20.1046 11 21 11.8954 21 13V19C21 20.1046 20.10"
                "46 21 19 21H5C3.89543 21 3 20.1046 3 19V13C3 11.8954 3.89543 1"
                "1 5 11M19 11V9C19 7.89543 18.1046 7 17 7M5 11V9C5 7.89543 5.89"
                "543 7 7 7M7 7V5C7 3.89543 7.89543 3 9 3H15C16.1046 3 17 3.8954"
                "3 17 5V7M7 7H17"
            ),
            stroke="currentColor",
            stroke_width="2",
            stroke_linecap="round",
            stroke_linejoin="round",
        )
        tag.add(_path)
        return tag


class IconSearch(Icon):
    def _to_tag(self):
        tag = svg(
            _class="w-4 h-5 m-3 absolute top-0 right-0 pointer-events-none",
            xmlns="http://www.w3.org/2000/svg",
            fill="none",
            viewBox="0 0 24 24",
            stroke="currentColor",
        )
        _path = path(
            strokeLinecap="round",
            strokeLinejoin="round",
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z",
        )
        tag.add(_path)
        return tag


class IconDetails(Icon):
    def _to_tag(self):
        tag = svg(
            _class="w-5 h-5 m-1 pointer-events-none",
            xmlns="http://www.w3.org/2000/svg",
            fill="none",
            viewBox="0 0 24 24",
            stroke="white",
        )
        _path = path(
            stroke_linecap="round",
            stroke_linejoin="round",
            fill="white",
            d="M4 6h16M4 10h16M4 14h16M4 18h16",
        )
        tag.add(_path)
        return tag


class IconPlay(Icon):
    def _to_tag(self):
        tag = svg(
            _class="w-auto h-6 m-1 inline-block pointer-events-none",
            xmlns="http://www.w3.org/2000/svg",
            fill="currentColor",
            viewBox="0 0 20 20",
        )
        _path = path(
            fill_rule="evenodd",
            clip_rule="evenodd",
            d=(
                "M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 "
                "1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z"
            ),
        )
        tag.add(_path)
        return tag


class IconStop(Icon):
    def _to_tag(self):
        tag = svg(
            _class="w-auto h-6 m-1 inline-block",
            xmlns="http://www.w3.org/2000/svg",
            fill="currentColor",
            viewBox="0 0 20 20",
        )
        _path = path(
            fill_rule="evenodd",
            clip_rule="evenodd",
            d=(
                "M10 18a8 8 0 100-16 8 8 0 000 16zM8 7a1 1 0 00-1 1v4a1 1 0 001"
                " 1h4a1 1 0 001-1V8a1 1 0 00-1-1H8z"
            ),
        )
        tag.add(_path)
        return tag


class IconBin(Icon):
    def _to_tag(self):
        tag = svg(
            _class="w-auto h-6 m-1 inline-block",
            xmlns="http://www.w3.org/2000/svg",
            fill="currentColor",
            viewBox="0 0 20 20",
        )
        _path = path(
            fill_rule="evenodd",
            clip_rule="evenodd",
            d=(
                "M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a"
                "2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7"
                " 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 "
                "0V8a1 1 0 00-1-1z"
            ),
        )
        tag.add(_path)
        return tag


class IconFirstPage(Icon):
    def _to_tag(self):
        tag = svg(
            _class="w-6 h-6 m-1 pointer-events-none",
            xmlns="http://www.w3.org/2000/svg",
            fill="currentColor",
            viewBox="0 0 24 24",
        )
        _path = path(
            d=(
                "M17.7 15.89L13.82 12l3.89-3.89c.39-.39.39-1.02 0-1.41-.39-.39-"
                "1.02-.39-1.41 0l-4.59 4.59c-.39.39-.39 1.02 0 1.41l4.59 4.59c."
                "39.39 1.02.39 1.41 0 .38-.38.38-1.02-.01-1.4zM7 6c.55 0 1 .45 "
                "1 1v10c0 .55-.45 1-1 1s-1-.45-1-1V7c0-.55.45-1 1-1z"
            ),
        )
        tag.add(_path)
        return tag


class IconPreviousPage(Icon):
    def _to_tag(self):
        tag = svg(
            _class="w-6 h-6 m-1 pointer-events-none",
            xmlns="http://www.w3.org/2000/svg",
            fill="currentColor",
            viewBox="0 0 24 24",
        )
        _path = path(
            d=(
                "M14.71 6.71c-.39-.39-1.02-.39-1.41 0L8.71 11.3c-.39.39-.39 1.0"
                "2 0 1.41l4.59 4.59c.39.39 1.02.39 1.41 0 .39-.39.39-1.02 0-1.4"
                "1L10.83 12l3.88-3.88c.39-.39.38-1.03 0-1.41z"
            ),
        )
        tag.add(_path)
        return tag


class IconNextPage(Icon):
    def _to_tag(self):
        tag = svg(
            _class="w-6 h-6 m-1 pointer-events-none",
            xmlns="http://www.w3.org/2000/svg",
            fill="currentColor",
            viewBox="0 0 24 24",
        )
        _path = path(
            d=(
                "M9.29 6.71c-.39.39-.39 1.02 0 1.41L13.17 12l-3.88 3.88c-.39.39"
                "-.39 1.02 0 1.41.39.39 1.02.39 1.41 0l4.59-4.59c.39-.39.39-1.0"
                "2 0-1.41L10.7 6.7c-.38-.38-1.02-.38-1.41.01z"
            ),
        )
        tag.add(_path)
        return tag


class IconLastPage(Icon):
    def _to_tag(self):
        tag = svg(
            _class="w-6 h-6 m-1 pointer-events-none",
            xmlns="http://www.w3.org/2000/svg",
            fill="currentColor",
            viewBox="0 0 24 24",
        )
        _path = path(
            d=(
                "M6.29 8.11L10.18 12l-3.89 3.89c-.39.39-.39 1.02 0 1.41.39.39 1"
                ".02.39 1.41 0l4.59-4.59c.39-.39.39-1.02 0-1.41L7.7 6.7c-.39-.3"
                "9-1.02-.39-1.41 0-.38.39-.38 1.03 0 1.41zM17 6c.55 0 1 .45 1 1"
                "v10c0 .55-.45 1-1 1s-1-.45-1-1V7c0-.55.45-1 1-1z"
            )
        )
        tag.add(_path)
        return tag


class IconRefresh(Icon):
    def _to_tag(self):
        tag = svg(
            _class="w-auto h-6 m-1 inline-block",
            xmlns="http://www.w3.org/2000/svg",
            fill="none",
            viewBox="0 0 24 24",
            stroke="currentColor",
        )
        _path = path(
            stroke_linecap="round",
            stroke_linejoin="round",
            stroke_width="2",
            d=(
                "M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-."
                "581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
            ),
        )
        tag.add(_path)
        return tag
