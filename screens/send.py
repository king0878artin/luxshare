import os, threading
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.metrics import dp
from core import LuxShareClient
from utils.file_manager import validate_file
from config import COLORS

class SendScreen(BoxLayout):
    def __init__(self, app=None, **kwargs):
        super().__init__(orientation="vertical", padding=dp(12), spacing=dp(8), **kwargs)
        self.app=app; self.selected_device=None; self.file_path=None
        self.add_widget(Label(text="[b]Send a file[/b]", markup=True, size_hint_y=None, height=dp(42), color=COLORS["text"]))
        self.chooser=FileChooserListView(path=os.path.expanduser("~"), filters=["!*"], size_hint_y=0.55)
        self.add_widget(self.chooser)
        self.status=Label(text="Choose a file, then select a nearby device.", color=COLORS["muted"], size_hint_y=None, height=dp(42))
        self.add_widget(self.status)
        row=BoxLayout(size_hint_y=None,height=dp(48),spacing=dp(6))
        for text,fn in (("Use selected file",self.choose_file),("Refresh devices",self.refresh_devices)):
            b=Button(text=text); b.bind(on_release=lambda _b,f=fn:f()); row.add_widget(b)
        self.add_widget(row)
        self.devices_box=BoxLayout(orientation="vertical",spacing=dp(4))
        self.add_widget(self.devices_box)
        self.progress=Label(text="",size_hint_y=None,height=dp(30),color=COLORS["secondary"]); self.add_widget(self.progress)
        row2=BoxLayout(size_hint_y=None,height=dp(48),spacing=dp(6))
        send=Button(text="Send"); send.bind(on_release=lambda *_:self.send_now()); row2.add_widget(send)
        back=Button(text="Back"); back.bind(on_release=lambda *_:self.app.open_screen("home")); row2.add_widget(back); self.add_widget(row2)
    def on_enter(self): self.refresh_devices()
    def choose_file(self):
        if not self.chooser.selection: self.status.text="Select a file first."; return
        try:
            info=validate_file(self.chooser.selection[0]); self.file_path=info["path"]; self.status.text=f'{info["name"]} ({info["size"]:,} bytes)'
        except Exception as e:self.status.text=str(e)
    def refresh_devices(self):
        self.devices_box.clear_widgets()
        devices=self.app.discovery.get_devices() if self.app.discovery else {}
        for dev in devices.values():
            b=Button(text=f'{dev["name"]}  •  {dev["ip"]}',size_hint_y=None,height=dp(42))
            b.bind(on_release=lambda _b,d=dev:self.select_device(d)); self.devices_box.add_widget(b)
        if not devices:self.devices_box.add_widget(Label(text="No devices found yet. Keep both devices on the same Wi-Fi/hotspot.",color=COLORS["muted"]))
    def select_device(self, device):
        self.selected_device=device; self.status.text="Selected: "+device["name"]
    def send_now(self):
        if not self.file_path or not self.selected_device:self.status.text="Choose a file and a device.";return
        path,device=self.file_path,self.selected_device
        self.status.text="Connecting…"
        def work():
            try:
                client=LuxShareClient().connect(device)
                result=client.send_file(path,lambda a,b:Clock.schedule_once(lambda _dt:self.update_progress(a,b),0))
                Clock.schedule_once(lambda _dt:setattr(self.status,"text","Transfer complete."),0)
            except Exception as e:Clock.schedule_once(lambda _dt:setattr(self.status,"text",f"Transfer failed: {e}"),0)
        threading.Thread(target=work,daemon=True).start()
    def update_progress(self,current,total):self.progress.text=f"{current/total*100:.1f}%" if total else "0%"
