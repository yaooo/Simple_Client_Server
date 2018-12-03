import socket as mysoc
import threading
import time
import hmac

import sys
Port_TS1 = 6000
Port_TS1_client = 6001

TS1_hostname = "cpp.cs.rutgers.edu"
DNSTS = "PROJ3-TLDS1.txt"
key_file1 = "PROJ3-KEY1.txt"
key1 = ""

# Example
# d2 = hmac.new("k3522".encode(), c1.encode("utf-8"))
# print(d2.hexdigest())
def compute_key(message, key):
    d2 = hmac.new(key.encode(), message.encode("utf-8"))
    hexdigest = d2.hexdigest()
    return hexdigest

def get_key():
    with open(key_file1) as f:
        lines = f.readlines()
    f.close()
    return lines[0].strip('\n').strip()


def read_file(file_name):
    with open(file_name) as f:
        lines = f.readlines()
    f.close()
    return lines


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

def server1():
    key1 = get_key()
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

    try:
        ss1 = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: RS Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))
    server_binding1 = ('', Port_TS1_client)
    ss1.bind(server_binding1)
    ss1.listen(1)
    csockid1, addr1 = ss1.accept()
    print("[RS]: Got a connection request from a client at", addr1)

    # Receiving message and reverse the message

    more_messages = True
    while more_messages:
        print("Recieving msg from AS...")
        data_from_client = csockid.recv(100)
        msg_decoding = data_from_client.decode('utf-8')

        if (msg_decoding.strip('\n').strip() == "disconnecting"):  # If disconnecting, break out of the loop
            more_messages = False
        else:
            text = compute_key(msg_decoding, key1)
            csockid.send(text.encode('utf-8'))
            print("encrypt:" + text + "\n")
            time.sleep(1)


    ss1.close()
    ss.close()
    exit()

t1 = threading.Thread(name='server1', target=server1)
t1.start()

input("Hit ENTER  to exit\n")
exit()


