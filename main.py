from apps_examples import mockapis
from apps_examples.connected_frames import webapp as connected_frames
from apps_examples.ghpages import webapp as ghpage
from apps_examples.scheduler import webapp as scheduler
from giotto.elements import Text
from giotto.navigation import Sidebar
from giotto.app import MainApp

apps = [connected_frames, ghpage, scheduler]
webapp = MainApp(sidebar=Sidebar(items=mockapis.sidebar_items), apps=apps)


@webapp.frame()
def index():
    text = "### Index page needs improvement."
    box = Text(value=text)
    return [box]
