"""Length-prefixed JSON protocol helpers."""
import json, struct
MAX_HEADER_SIZE=64*1024
MAX_FILE_SIZE=5*1024*1024*1024
CHUNK_SIZE=1024*1024

def recv_exact(sock,size):
    parts=[]
    while size:
        data=sock.recv(min(size,262144))
        if not data: raise ConnectionError("Connection closed unexpectedly")
        parts.append(data); size-=len(data)
    return b"".join(parts)

def send_json(sock,obj):
    raw=json.dumps(obj,ensure_ascii=False).encode("utf-8")
    if len(raw)>MAX_HEADER_SIZE: raise ValueError("Header too large")
    sock.sendall(struct.pack("!I",len(raw))+raw)

def recv_json(sock):
    size=struct.unpack("!I",recv_exact(sock,4))[0]
    if not 2<=size<=MAX_HEADER_SIZE: raise ValueError("Invalid header length")
    obj=json.loads(recv_exact(sock,size).decode("utf-8"))
    if not isinstance(obj,dict): raise ValueError("Invalid message")
    return obj
