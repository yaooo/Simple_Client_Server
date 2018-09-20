import numpy as mypy
import threading

import socket as mysoc

# reverse the string but not the line break
def reversed_string(a_string):
    t = a_string.rstrip()
    return t[::-1] + "\n"

def server():
    try:
        ss = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))
    server_binding = ('', 6666)
    ss.bind(server_binding)
    ss.listen(1)
    host = mysoc.gethostname()
    print("[S]: Server host name is: ", host)
    localhost_ip = (mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ", localhost_ip)
    csockid, addr = ss.accept()
    print("[S]: Got a connection request from a client at", addr)
    # send a intro  message to the client.

    while 1:
        data_from_client = csockid.recv(100)
        if not data_from_client: break
        msg_decoding = data_from_client.decode('utf-8')
        print("Recieving data from client:", msg_decoding)
        csockid.send(reversed_string(msg_decoding).encode('utf-8'))

    ss.close()
    exit()

t1 = threading.Thread(name='server', target=server)
t1.start()

input("Hit ENTER  to exit\n")
exit()