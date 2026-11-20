import threading
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from config import COLORS

class ReceiveScreen(BoxLayout):
    def __init__(self,app=None,**kwargs):
        super().__init__(orientation="vertical",padding=dp(20),spacing=dp(12),**kwargs)
        self.app=app
        self.add_widget(Label(text="[b]Receive files[/b]",markup=True,font_size="22sp",size_hint_y=None,height=dp(48),color=COLORS["text"]))
        self.status=Label(text="Receiver is stopped.",color=COLORS["muted"]);self.add_widget(self.status)
        self.progress=Label(text="",color=COLORS["secondary"]);self.add_widget(self.progress)
        start=Button(text="Start receiving",size_hint_y=None,height=dp(54));start.bind(on_release=lambda *_:self.start_receiver());self.add_widget(start)
        stop=Button(text="Stop receiving",size_hint_y=None,height=dp(54));stop.bind(on_release=lambda *_:self.stop_receiver());self.add_widget(stop)
        back=Button(text="Back",size_hint_y=None,height=dp(48));back.bind(on_release=lambda *_:self.app.open_screen("home"));self.add_widget(back)
    def start_receiver(self):
        try:
            self.app.start_server();self.status.text="Ready to receive from devices on this network."
        except Exception as e:self.status.text=f"Could not start: {e}"
    def stop_receiver(self):self.app.stop_server();self.status.text="Receiver is stopped."
    def confirm_request(self,ip,name,size):
        event=threading.Event();answer={"ok":False}
        def show(_dt):
            content=BoxLayout(orientation="vertical",padding=dp(12),spacing=dp(8))
            content.add_widget(Label(text=f"{ip} wants to send {name}\n{size:,} bytes",color=COLORS["text"]))
            row=BoxLayout(size_hint_y=None,height=dp(48),spacing=dp(8))
            popup=Popup(title="Incoming file",content=content,size_hint=(.9,.4),auto_dismiss=False)
            def choose(value):answer["ok"]=value;popup.dismiss();event.set()
            yes=Button(text="Accept");yes.bind(on_release=lambda *_:choose(True));no=Button(text="Decline");no.bind(on_release=lambda *_:choose(False))
            row.add_widget(yes);row.add_widget(no);content.add_widget(row);popup.open()
        Clock.schedule_once(show,0);event.wait(timeout=120);return answer["ok"]
    def update_progress(self,current,total):Clock.schedule_once(lambda _dt:setattr(self.progress,"text",f"Receiving: {current/total*100:.1f}%" if total else "Receiving…"),0)
