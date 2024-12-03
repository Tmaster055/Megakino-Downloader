import npyscreen
from common import get_html_from_search, get_episodes, clear, get_titles
from download import download
from syncplay import syncplay
from watch import watch
from voe import voe_get_direct_link

HTML_CONTENT = get_html_from_search()
Episodes = get_episodes(HTML_CONTENT)
print(Episodes)
Titles = get_titles(Episodes)
Series = dict(zip(Titles, Episodes))
print(Series)

class MegakinoForm(npyscreen.ActionForm):
    def create(self):
        self.action = self.add(npyscreen.TitleSelectOne, name="Action:", max_height=6, values=["Watch", "Download", "Syncplay"], scroll_exit=True, value=1)

        self.episodes = self.add(npyscreen.TitleMultiSelect, name="Choose Episodes:", values=Titles, scroll_exit=True)

    def on_ok(self):
        selected_action = self.action.get_selected_objects()
        selected_episodes = self.episodes.get_selected_objects()
        titles_list = list(selected_episodes)
        links = {}
        for name in titles_list:
            if name in Series:
                links[name] = Series[name]
            else:
                links[name] = "Kein Link gefunden"
        selected_action = selected_action[0]
        clear()

        print(links)
        direct_links = []
        for episode in list(links):
            link = voe_get_direct_link(episode)
            direct_links.append(link)


        if selected_action == "Watch":
            print(links)
            print(direct_links)
        elif selected_action == "Download":
            download(direct_links)
        elif selected_action == "Syncplay":
            syncplay(direct_links)

        self.parentApp.switchForm(None)

    def on_cancel(self):
        exit()

class MegakinoApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.form = self.addForm("MAIN", MegakinoForm, name="Megakino-Downloader")


app = MegakinoApp()
app.run()
