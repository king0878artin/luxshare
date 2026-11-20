import socket
from .transfer import send_file
from config import CONNECTION_TIMEOUT
class LuxShareClient:
    def __init__(self,timeout=CONNECTION_TIMEOUT):self.timeout=timeout;self.sock=None
    def connect(self,device):
        self.close();self.sock=socket.create_connection((device["ip"],int(device.get("port",37021))),self.timeout);self.sock.settimeout(None);return self
    def send_file(self,path,progress_callback=None,cancel_event=None):
        if not self.sock:raise RuntimeError("Not connected")
        try:return send_file(self.sock,path,progress_callback,cancel_event)
        finally:self.close()
    def close(self):
        if self.sock:
            try:self.sock.shutdown(socket.SHUT_RDWR)
            except OSError:pass
            try:self.sock.close()
            except OSError:pass
            self.sock=None
