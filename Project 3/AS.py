import numpy as np
import socket as mysoc
import threading
import hmac
import time

TS1_host = ""
TS2_host =""

TS2_hostname = "java.cs.rutgers.edu"
TS1_hostname = "cpp.cs.rutgers.edu"

port_RS = 5000
port_TS1 = 6000
port_TS2 = 7000


# Example
# d2 = hmac.new("k3522".encode(), c1.encode("utf-8"))
# print(d2.hexdigest())
def compute_key(message, key):
    d2 = hmac.new(key.encode(), message.encode("utf-8"))
    hexdigest = d2.hexdigest()
    return d2, hexdigest

def read_file(file_name):
    with open(file_name) as f:
        lines = f.readlines()
    f.close()
    return lines

def choose_TL(digest_stored, digest_from_TL1, digest_from_TL2):
    if digest_from_TL1 == digest_stored:
        return TS1_hostname
    if digest_from_TL2 == digest_stored:
        return TS2_hostname
    return "Digest Not Match"

def server():

    # connect to TS1: com
    try:
        cs1 = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))
    # Define the port on which you want to connect to the server
    sa_sameas_myaddr1 = mysoc.gethostbyname(TS1_hostname)
    # connect to the server on local machine
    server_binding1 = (sa_sameas_myaddr1, port_TS1)

    # server_binding1 = (mysoc.gethostbyname(mysoc.gethostname()), port_TS1)
    cs1.connect(server_binding1)

    # connect to TS2
    try:
        cs2 = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))
    # Define the port on which you want to connect to the server
    sa_sameas_myaddr2 = mysoc.gethostbyname(TS2_hostname)
    # connect to the server on local machine
    server_binding2 = (sa_sameas_myaddr2, port_TS2)
    # server_binding2 = (mysoc.gethostbyname(mysoc.gethostname()), port_TS2)
    cs2.connect(server_binding2)

    print("Connect to" , TS1_host, ",", TS2_host, ".\n")

# Connect to client
    try:
        ss = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: RS Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    server_binding = ('', port_RS)
    ss.bind(server_binding)
    ss.listen(1)
    host = mysoc.gethostname()
    print("[RS]: Server host name is: ", host)
    localhost_ip = (mysoc.gethostbyname(host))
    print("[RS]: Server IP address is  ", localhost_ip)
    csockid, addr = ss.accept()
    print("[RS]: Got a connection request from a client at", addr)


    more_messages = True
    while more_messages:
        msg_decoding = csockid.recv(100).decode('utf-8')
        if msg_decoding == "disconnecting":
            cs1.send("disconnecting".encode('utf-8'))
            cs2.send("disconnecting".encode('utf-8'))
            more_messages = False
        else:
            print("message from client:", msg_decoding)
            message_from_client = msg_decoding.strip("\n").split(',')
            message_to_TL = message_from_client[0]
            digest_to_keep = message_from_client[1]
            # time.sleep(2.5)

            cs1.send(message_to_TL.encode('utf-8'))
            cs2.send(message_to_TL.encode('utf-8'))

            print("Message send to tl1 and tl2....")
            digest_from_TL1 = cs1.recv(100).decode('utf-8')
            digest_from_TL2 = cs2.recv(100).decode('utf-8')


            hostname_to_client = choose_TL(digest_to_keep, digest_from_TL1, digest_from_TL2)
            csockid.send(hostname_to_client.encode('utf-8'))

    ss.close()
    exit()

t1 = threading.Thread(name='rs_server', target=server)
t1.start()

input("Hit ENTER  to exit\n")
exit()
