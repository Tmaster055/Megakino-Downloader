import npyscreen
from .common import get_html_from_search, clear, get_megakino_episodes, get_title
from .download import download
from .megakino import megakino_get_direct_link
from .voe import voe_get_direct_link
from .syncplay import syncplay
from .watch import watch


def main():
    HTML_CONTENT = get_html_from_search()
    episodes = get_title(HTML_CONTENT)
    titles = list(episodes.keys())

    class MegakinoForm(npyscreen.ActionForm):
        def create(self):
            self.action = self.add(npyscreen.TitleSelectOne, name="Action:", max_height=6, values=["Watch", "Download", "Syncplay"], scroll_exit=True, value=1)

            self.provider = self.add(npyscreen.TitleSelectOne, name="Provider:", max_height=5, values=["Megakino", "VOE"], scroll_exit=True, value=0)

            self.episodes = self.add(npyscreen.TitleMultiSelect, name="Choose Episodes:", values=titles, scroll_exit=True)

        def on_ok(self):
            selected_action = self.action.get_selected_objects()
            selected_provider = self.provider.get_selected_objects()
            selected_episodes = self.episodes.get_selected_objects()


            chosen_episodes = list(selected_episodes)
            selected_action = selected_action[0]
            selected_provider = selected_provider[0]
            clear()

            direct_links = []
            if selected_provider == "Megakino":
                megakino_list = get_megakino_episodes(HTML_CONTENT)
                if megakino_list:
                    for episode in megakino_list:
                        link = megakino_get_direct_link(episode)
                        direct_links.append(link)

            elif selected_provider == "VOE" or not direct_links:
                urls = [episodes[name] for name in chosen_episodes]
                if urls:
                    for episode in urls:
                        link = voe_get_direct_link(episode)
                        direct_links.append(link)
            print(direct_links)
            if selected_action == "Watch":
                watch(direct_links, chosen_episodes)
            elif selected_action == "Download":
                download(direct_links, chosen_episodes)
            elif selected_action == "Syncplay":
                syncplay(direct_links, chosen_episodes)

            self.parentApp.switchForm(None)

        def on_cancel(self):
            exit()

    class MegakinoApp(npyscreen.NPSAppManaged):
        def onStart(self):
            self.form = self.addForm("MAIN", MegakinoForm, name="Megakino-Downloader")


    app = MegakinoApp()
    app.run()


if __name__ == "__main__":
    main()
