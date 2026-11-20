"""UDP broadcast discovery on the current local network."""
import json,socket,threading,time,uuid
from config import DISCOVERY_PORT,DISCOVERY_INTERVAL,DEVICE_TIMEOUT,TRANSFER_PORT,APP_NAME
class DeviceDiscovery:
    def __init__(self,device_name="LuxShare Device",callback=None):
        self.device_name=device_name;self.callback=callback;self.device_id=str(uuid.uuid4());self.devices={};self.stop_event=threading.Event();self.thread=None;self.sock=None
    def start(self):
        if self.thread and self.thread.is_alive():return
        self.stop_event.clear();self.sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM);self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1);self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1);self.sock.bind(("",DISCOVERY_PORT));self.sock.settimeout(.4);self.thread=threading.Thread(target=self._run,daemon=True);self.thread.start()
    def _run(self):
        last=0
        while not self.stop_event.is_set():
            now=time.time()
            if now-last>=DISCOVERY_INTERVAL:
                try:self.sock.sendto(json.dumps({"app":APP_NAME,"id":self.device_id,"name":self.device_name,"port":TRANSFER_PORT}).encode("utf-8"),("255.255.255.255",DISCOVERY_PORT))
                except OSError:pass
                last=now
            try:
                raw,addr=self.sock.recvfrom(4096);m=json.loads(raw.decode("utf-8"))
                if m.get("app")==APP_NAME and m.get("id")!=self.device_id:
                    d={"id":str(m.get("id",addr[0])),"name":str(m.get("name","Device"))[:64],"ip":addr[0],"port":int(m.get("port",TRANSFER_PORT)),"last_seen":now};self.devices[d["id"]]=d
                    if self.callback:self.callback(dict(d))
            except socket.timeout:pass
            except (OSError,ValueError,TypeError,KeyError):pass
            cutoff=time.time()-DEVICE_TIMEOUT;self.devices={k:v for k,v in self.devices.items() if v["last_seen"]>=cutoff}
    def get_devices(self):return dict(self.devices)
    def stop(self):
        self.stop_event.set()
        if self.sock:
            try:self.sock.close()
            except OSError:pass
            self.sock=None
        if self.thread and self.thread.is_alive():self.thread.join(1)
