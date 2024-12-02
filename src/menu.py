import npyscreen
from common import get_html_from_search, get_episodes

HTML_CONTENT = get_html_from_search()
Episodes = get_episodes(HTML_CONTENT)
print(Episodes)


class MegakinoForm(npyscreen.ActionForm):
    def create(self):
        self.action = self.add(npyscreen.TitleSelectOne, name="Action:", max_height=6, values=["Watch", "Download", "Syncplay"], scroll_exit=True, value=1)

        self.episodes = self.add(npyscreen.TitleMultiSelect, name="Choose Episodes:", values=Episodes, scroll_exit=True)

    def on_ok(self):
        selected_action = self.action.get_selected_objects()
        selected_episoden = self.episodes.get_selected_objects()

        if selected_action:
            print(f"Ausgewählte Aktion: {selected_action[0]}")
        if selected_episoden:
            episoden_liste = list(selected_episoden)
            print(f"Ausgewählte Episoden (Liste): {episoden_liste}")

        self.parentApp.switchForm(None)

    def on_cancel(self):
        exit()

class MegakinoApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.form = self.addForm("MAIN", MegakinoForm, name="Aktionen und Episoden auswählen")


app = MegakinoApp()
app.run()
