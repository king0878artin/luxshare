import os,threading
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.metrics import dp
from core import LuxShareClient
from utils.file_manager import validate_file
from config import COLORS

class SendScreen(BoxLayout):
    def __init__(self,app=None,**kwargs):
        super().__init__(orientation="vertical",padding=dp(12),spacing=dp(8),**kwargs);self.app=app;self.selected_device=None;self.file_path=None
        self.add_widget(Label(text="[b]Send a file[/b]",markup=True,size_hint_y=None,height=dp(42),color=COLORS["text"]))
        self.status=Label(text="Choose a file, then select a nearby device.",color=COLORS["muted"],size_hint_y=None,height=dp(44));self.add_widget(self.status)
        self.file_label=Label(text="No file selected",color=COLORS["text"],size_hint_y=None,height=dp(32));self.add_widget(self.file_label)
        pick=Button(text="Choose file",size_hint_y=None,height=dp(50));pick.bind(on_release=lambda *_:self.pick_file());self.add_widget(pick)
        refresh=Button(text="Refresh nearby devices",size_hint_y=None,height=dp(46));refresh.bind(on_release=lambda *_:self.refresh_devices());self.add_widget(refresh)
        self.devices_box=BoxLayout(orientation="vertical",spacing=dp(4));self.add_widget(self.devices_box)
        self.progress=Label(text="",size_hint_y=None,height=dp(30),color=COLORS["secondary"]);self.add_widget(self.progress)
        send=Button(text="Send file",size_hint_y=None,height=dp(52));send.bind(on_release=lambda *_:self.send_now());self.add_widget(send)
        back=Button(text="Back",size_hint_y=None,height=dp(46));back.bind(on_release=lambda *_:self.app.open_screen("home"));self.add_widget(back)
    def pick_file(self):
        try:
            from plyer import filechooser
            filechooser.open_file(on_selection=self._picked)
        except Exception:
            chooser=FileChooserListView(path=os.path.expanduser("~"))
            from kivy.uix.popup import Popup
            box=BoxLayout(orientation="vertical");box.add_widget(chooser);ok=Button(text="Select",size_hint_y=None,height=dp(48));box.add_widget(ok)
            popup=Popup(title="Choose a file",content=box,size_hint=(.95,.9))
            def choose(*_):
                if chooser.selection:self._picked(chooser.selection)
                popup.dismiss()
            ok.bind(on_release=choose);popup.open()
    def _picked(self,selection):
        if not selection:return
        try:
            info=validate_file(selection[0]);self.file_path=info["path"];self.file_label.text=f'{info["name"]} • {info["size"]:,} bytes';self.status.text="File selected."
        except Exception as e:self.status.text=str(e)
    def refresh_devices(self):
        self.devices_box.clear_widgets();devices=self.app.discovery.get_devices() if self.app.discovery else {}
        for dev in devices.values():
            b=Button(text=f'{dev["name"]}  •  {dev["ip"]}',size_hint_y=None,height=dp(44));b.bind(on_release=lambda _b,d=dev:self.select_device(d));self.devices_box.add_widget(b)
        if not devices:self.devices_box.add_widget(Label(text="No devices found. Both devices must share the same reachable Wi-Fi/hotspot.",color=COLORS["muted"]))
    def select_device(self,device):self.selected_device=device;self.status.text="Selected: "+device["name"]
    def send_now(self):
        if not self.file_path or not self.selected_device:self.status.text="Choose a file and a device first.";return
        path,device=self.file_path,self.selected_device;self.status.text="Connecting…"
        def work():
            try:
                client=LuxShareClient().connect(device);client.send_file(path,lambda a,b:Clock.schedule_once(lambda _dt:self.update_progress(a,b),0));Clock.schedule_once(lambda _dt:setattr(self.status,"text","Transfer complete."),0)
            except Exception as e:Clock.schedule_once(lambda _dt:setattr(self.status,"text",f"Transfer failed: {e}"),0)
        threading.Thread(target=work,daemon=True).start()
    def update_progress(self,current,total):self.progress.text=f"{current/total*100:.1f}%" if total else "0%"
