from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from config import COLORS
class HomeScreen(BoxLayout):
    def __init__(self,app=None,**kwargs):
        super().__init__(orientation="vertical",padding=dp(24),spacing=dp(16),**kwargs);self.app=app
        self.add_widget(Label(text="[b]LuxShare[/b]\nOffline file sharing",markup=True,font_size="28sp",color=COLORS["text"],halign="center"))
        self.add_widget(Label(text="Share files up to 5 GB over the same Wi-Fi or hotspot. No internet required.",color=COLORS["muted"],halign="center"))
        for label,name in (("Send files","send"),("Receive files","receive"),("Settings","settings")):
            b=Button(text=label,size_hint_y=None,height=dp(58),background_normal="",background_color=COLORS["primary"] if name!="settings" else COLORS["surface_light"]);b.bind(on_release=lambda _b,n=name:self.app.open_screen(n));self.add_widget(b)
