from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from config import COLORS
class HomeScreen(Screen):
 def __init__(self,**kwargs):
  super().__init__(**kwargs); box=BoxLayout(orientation="vertical",padding=28,spacing=18); box.add_widget(Label(text="[b]LuxShare[/b]\nOffline file sharing",markup=True,font_size="28sp",color=COLORS["text"]));
  for title,target in [("Send files","send"),("Receive files","receive"),("Settings","settings")]:
   b=Button(text=title,size_hint_y=None,height=58,background_normal="",background_color=COLORS["primary"]);b.bind(on_release=lambda _,t=target:setattr(self.manager,"current",t));box.add_widget(b)
  self.add_widget(box)
