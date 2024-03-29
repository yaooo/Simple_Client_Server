import socket as mysoc
import threading
import time
import hmac

import sys
Port_TS2 = 7000
Port_TS2_client = 7001

TS2_hostname = "java.cs.rutgers.edu"
DNSTS = "PROJ3-TLDS2.txt"
key_file2 = "PROJ3-KEY2.txt"
key2 = ""

def read_file(file_name):
    with open(file_name) as f:
        lines = f.readlines()
    f.close()
    return lines

def get_key():
    with open(key_file2) as f:
        lines = f.readlines()
    f.close()
    return lines[0].strip('\n').strip()

# Example
# d2 = hmac.new("k3522".encode(), c1.encode("utf-8"))
# print(d2.hexdigest())
def compute_key(message, key):
    d2 = hmac.new(key.encode(), message.encode("utf-8"))
    hexdigest = d2.hexdigest()
    return hexdigest


def lookup(hostname_string):
    if hostname_string.startswith("www."):
        hostname_string = hostname_string[4:].strip("\n")
    lines = read_file(DNSTS)
    for i in lines:
        t = i
        i = i.lower()
        if i.find(hostname_string.lower()) != -1:
            if not i.endswith("\n"):
                return t + "\n"
            return t
    return "ERROR:HOST NOT FOUND\n"

def server2():
    key2 = get_key()
    try:
        ss = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: RS Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))
    server_binding = ('', Port_TS2)
    ss.bind(server_binding)
    ss.listen(1)
    host = mysoc.gethostname()
    print("[RS]: Server host name is: ", host)
    localhost_ip = (mysoc.gethostbyname(host))
    print("[RS]: Server IP address is  ", localhost_ip)
    csockid, addr = ss.accept()
    print("[RS]: Got a connection request from a client at", addr)

    try:
        ss2 = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: RS Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))
    server_binding2 = ('', Port_TS2_client)
    ss2.bind(server_binding2)
    ss2.listen(1)
    csockid2, addr2 = ss2.accept()
    print("[RS]: Got a connection request from a client at", addr2)

    more_messages = True
    while more_messages:
        print("Recieving msg from AS...")
        data_from_client = csockid.recv(100)
        msg_decoding = data_from_client.decode('utf-8')

        if (msg_decoding.strip("\n").strip() == "disconnecting"):  # If disconnecting, break out of the loop
            more_messages = False
        else:
            text = compute_key(msg_decoding, key2)
            csockid.send(text.encode('utf-8'))
            print("encrypt:" + text + "\n")
            time.sleep(1)

        m_client = csockid2.recv(100).decode('utf-8')
        if not(m_client == "-1"):
            x = lookup(m_client)
            csockid2.send(x.encode('utf-8'))

    ss2.close()
    ss.close()
    exit()

t1 = threading.Thread(name='server1', target=server2)
t1.start()

input("Hit ENTER  to exit\n")
exit()