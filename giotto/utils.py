from dominate.dom_tag import dom_tag


class tag_hyphenate(type):
    def __new__(cls, name, bases, dict):
        return type.__new__(cls, name.replace("_", "-"), bases, dict)


class svg(dom_tag):
    pass


class turbo_frame(dom_tag, metaclass=tag_hyphenate):
    pass


class path(dom_tag):
    pass
