import socket as mysoc
import threading
import time
import hmac

import sys
Port_TS1 = 7000
TS2_hostname = "grep.cs.rutgers.edu"
DNSTS = "PROJ3-TLDS2.txt"
key = "PROJ3-KEY2.txt"

def read_file(file_name):
    with open(file_name) as f:
        lines = f.readlines()
    f.close()
    return lines


# Example
# d2 = hmac.new("k3522".encode(), c1.encode("utf-8"))
# print(d2.hexdigest())
def compute_key(message, key):
    d2 = hmac.new(key.encode(), message.encode("utf-8"))
    hexdigest = d2.hexdigest()
    return d2, hexdigest




def lookup(hostname_string):
    if hostname_string.startswith("www."):
        hostname_string = hostname_string[4:].strip("\n")
    lines = read_file(DNSTS)
    for i in lines:
        i = i.lower()
        if i.find(hostname_string.lower()) != -1:
            if not i.endswith("\n"):
                return i + "\n"
            return i
    return "ERROR\n"

def server2():
    try:
        ss = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: RS Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))
    server_binding = ('', Port_TS1)
    ss.bind(server_binding)
    ss.listen(1)
    host = mysoc.gethostname()
    print("[RS]: Server host name is: ", host)
    localhost_ip = (mysoc.gethostbyname(host))
    print("[RS]: Server IP address is  ", localhost_ip)
    csockid, addr = ss.accept()
    print("[RS]: Got a connection request from a client at", addr)

    # Receiving message and reverse the message
    while 1:
        data_from_client = csockid.recv(100)
        if not data_from_client:
            if not data_from_client: break
        msg_decoding = data_from_client.decode('utf-8')

        if not len(msg_decoding.strip("\n")) == 0:
            print("Hostname from client:", msg_decoding)
            text = lookup(msg_decoding)
            print("Test:" + text)
            csockid.send(text.encode('utf-8'))
        time.sleep(1)
    ss.close()
    exit()

t1 = threading.Thread(name='server1', target=server2)
t1.start()

input("Hit ENTER  to exit\n")
exit()