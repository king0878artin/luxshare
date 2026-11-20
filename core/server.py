"""Background TCP receiver."""
import socket,threading
from .transfer import receive_file
from config import TRANSFER_PORT,SERVER_BACKLOG
class LuxShareServer:
    def __init__(self,save_directory,on_request=None,on_progress=None,device_name="LuxShare"):
        self.save_directory=save_directory;self.on_request=on_request;self.on_progress=on_progress;self.device_name=device_name;self.stop_event=threading.Event();self.listener=None;self.thread=None;self.clients=[];self.lock=threading.Lock()
    def start(self):
        if self.thread and self.thread.is_alive():return
        self.stop_event.clear();self.listener=socket.socket(socket.AF_INET,socket.SOCK_STREAM);self.listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1);self.listener.bind(("",TRANSFER_PORT));self.listener.listen(SERVER_BACKLOG);self.listener.settimeout(.5);self.thread=threading.Thread(target=self._accept,daemon=True);self.thread.start()
    def _accept(self):
        while not self.stop_event.is_set():
            try:sock,addr=self.listener.accept()
            except socket.timeout:continue
            except OSError:break
            with self.lock:self.clients.append(sock)
            threading.Thread(target=self._handle,args=(sock,addr),daemon=True).start()
    def _handle(self,sock,addr):
        try:
            sock.settimeout(None)
            def ask(name,size):return True if not self.on_request else bool(self.on_request(addr[0],name,size))
            receive_file(sock,self.save_directory,ask,self.on_progress)
        except Exception as e:print("LuxShare transfer:",e)
        finally:
            with self.lock:
                if sock in self.clients:self.clients.remove(sock)
            try:sock.close()
            except OSError:pass
    def stop(self):
        self.stop_event.set()
        if self.listener:
            try:self.listener.close()
            except OSError:pass
            self.listener=None
        with self.lock:clients=list(self.clients)
        for sock in clients:
            try:sock.shutdown(socket.SHUT_RDWR)
            except OSError:pass
            try:sock.close()
            except OSError:pass
        if self.thread and self.thread.is_alive():self.thread.join(1)
