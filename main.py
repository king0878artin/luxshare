"""LuxShare Android application entry point."""
import json,os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager,Screen,FadeTransition
from kivy.core.window import Window
from kivy.clock import Clock
from config import APP_NAME,COLORS
from core import DeviceDiscovery,LuxShareServer
from utils.file_manager import get_receive_directory
from screens import HomeScreen,SendScreen,ReceiveScreen,SettingsScreen
class LuxShareApp(App):
    def build(self):
        self.title=APP_NAME;Window.clearcolor=COLORS["background"];self.settings_path=os.path.join(self.user_data_dir,"settings.json");self.device_name="LuxShare Device"
        try:
            with open(self.settings_path,"r",encoding="utf-8") as f:self.device_name=json.load(f).get("device_name",self.device_name)
        except Exception:pass
        self.receive_directory=get_receive_directory(self.user_data_dir);self.server=None;self.discovery=None
        self.manager=ScreenManager(transition=FadeTransition())
        for name,widget in (("home",HomeScreen(self)),("send",SendScreen(self)),("receive",ReceiveScreen(self)),("settings",SettingsScreen(self))):
            page=Screen(name=name);page.add_widget(widget);self.manager.add_widget(page)
        if platform_is_android():Clock.schedule_once(self.request_android_permissions,1)
        Clock.schedule_once(lambda _dt:self.start_discovery(),1);return self.manager
    def request_android_permissions(self,_dt):
        try:
            from android.permissions import request_permissions
            request_permissions(["android.permission.INTERNET","android.permission.ACCESS_NETWORK_STATE","android.permission.ACCESS_WIFI_STATE","android.permission.CHANGE_WIFI_MULTICAST_STATE","android.permission.NEARBY_WIFI_DEVICES"])
        except Exception as e:print("Permission request:",e)
    def open_screen(self,name):self.manager.current=name
    def save_settings(self):
        with open(self.settings_path,"w",encoding="utf-8") as f:json.dump({"device_name":self.device_name},f)
    def start_discovery(self):
        try:
            if self.discovery:self.discovery.stop()
            self.discovery=DeviceDiscovery(self.device_name);self.discovery.start()
        except Exception as e:print("Discovery unavailable:",e)
    def restart_discovery(self):self.start_discovery()
    def start_server(self):
        self.stop_server();receiver=self.manager.get_screen("receive").children[0]
        self.server=LuxShareServer(self.receive_directory,on_request=receiver.confirm_request,on_progress=receiver.update_progress,device_name=self.device_name);self.server.start()
    def stop_server(self):
        if self.server:self.server.stop();self.server=None
    def on_stop(self):
        self.stop_server()
        if self.discovery:self.discovery.stop()
def platform_is_android():
    try:
        from kivy.utils import platform
        return platform=="android"
    except Exception:return False
if __name__=="__main__":LuxShareApp().run()
