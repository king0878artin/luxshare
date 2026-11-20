from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from config import COLORS

class SettingsScreen(BoxLayout):
    def __init__(self,app=None,**kwargs):
        super().__init__(orientation="vertical",padding=dp(20),spacing=dp(12),**kwargs)
        self.app=app
        self.add_widget(Label(text="[b]Settings[/b]",markup=True,font_size="22sp",size_hint_y=None,height=dp(48),color=COLORS["text"]))
        self.add_widget(Label(text="Device name",color=COLORS["muted"],size_hint_y=None,height=dp(28)))
        self.name_input=TextInput(text=app.device_name,multiline=False,size_hint_y=None,height=dp(48))
        self.add_widget(self.name_input)
        self.folder_label=Label(text="Receive folder:\n"+app.receive_directory,color=COLORS["muted"])
        self.add_widget(self.folder_label)
        save=Button(text="Save settings",size_hint_y=None,height=dp(52));save.bind(on_release=lambda *_:self.save());self.add_widget(save)
        back=Button(text="Back",size_hint_y=None,height=dp(48));back.bind(on_release=lambda *_:app.open_screen("home"));self.add_widget(back)
        self.status=Label(text="",color=COLORS["secondary"]);self.add_widget(self.status)
    def save(self):
        name=self.name_input.text.strip()[:32]
        if not name:self.status.text="Enter a device name.";return
        self.app.device_name=name;self.app.save_settings();self.app.restart_discovery();self.status.text="Settings saved."
