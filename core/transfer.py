"""Chunked file transfer with SHA-256 verification."""
import os,hashlib
from pathlib import Path
from .protocol import send_json,recv_json,recv_exact,CHUNK_SIZE,MAX_FILE_SIZE

def _hash(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(CHUNK_SIZE),b""):h.update(b)
    return h.hexdigest()

def send_file(sock,file_path,on_progress=None,cancel_event=None):
    p=Path(file_path);size=p.stat().st_size
    if not p.is_file() or size>MAX_FILE_SIZE:raise ValueError("File invalid or exceeds 5 GB")
    digest=_hash(p);send_json(sock,{"type":"file","name":p.name,"size":size,"sha256":digest})
    reply=recv_json(sock)
    if reply.get("status")!="ready":raise RuntimeError(reply.get("message","Receiver declined file"))
    done=0
    with open(p,"rb") as f:
        while done<size:
            if cancel_event and cancel_event.is_set():raise InterruptedError("Transfer cancelled")
            block=f.read(min(CHUNK_SIZE,size-done))
            if not block:raise IOError("File changed during transfer")
            sock.sendall(block);done+=len(block)
            if on_progress:on_progress(done,size)
    result=recv_json(sock)
    if result.get("status")!="complete":raise IOError(result.get("message","Transfer verification failed"))
    return result

def receive_file(sock,folder,on_request=None,on_progress=None,cancel_event=None):
    m=recv_json(sock)
    if m.get("type")!="file":raise ValueError("Unsupported data")
    name=Path(str(m.get("name","received_file"))).name;size=int(m.get("size",-1))
    if size<0 or size>MAX_FILE_SIZE:
        send_json(sock,{"status":"rejected","message":"Invalid file size"});raise ValueError("Invalid file size")
    if on_request and not on_request(name,size):
        send_json(sock,{"status":"rejected","message":"Transfer declined"});return None
    os.makedirs(folder,exist_ok=True);target=os.path.join(folder,name);stem,ext=os.path.splitext(target);n=1
    while os.path.exists(target):target=f"{stem} ({n}){ext}";n+=1
    temp=target+".luxpart";send_json(sock,{"status":"ready"});h=hashlib.sha256();got=0
    try:
        with open(temp,"wb") as f:
            while got<size:
                if cancel_event and cancel_event.is_set():raise InterruptedError("Transfer cancelled")
                block=recv_exact(sock,min(CHUNK_SIZE,size-got));f.write(block);h.update(block);got+=len(block)
                if on_progress:on_progress(got,size)
        if h.hexdigest()!=m.get("sha256"):raise IOError("SHA-256 verification failed")
        os.replace(temp,target);send_json(sock,{"status":"complete","name":os.path.basename(target)});return target
    except Exception as e:
        try:os.remove(temp)
        except OSError:pass
        try:send_json(sock,{"status":"error","message":str(e)[:160]})
        except Exception:pass
        raise
