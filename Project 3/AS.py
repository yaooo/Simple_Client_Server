import numpy as np
import socket as mysoc
import threading
import sys
import hmac

TS1_host = ""
TS2_host =""

TS1_hostname = "kill.cs.rutgers.edu"
TS2_hostname = "grep.cs.rutgers.edu"
port_RS = 5002
port_TS1 = 6001
port_TS2 = 7001


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

def server():
    """
    # connect to TS1: com
    try:
        cs1 = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))
    # Define the port on which you want to connect to the server
    sa_sameas_myaddr1 = mysoc.gethostbyname(TS1_host)
    # connect to the server on local machine
    server_binding1 = (sa_sameas_myaddr1, port_TS1)
    cs1.connect(server_binding1)

    # connect to TS2
    try:
        cs2 = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))
    # Define the port on which you want to connect to the server
    sa_sameas_myaddr2 = mysoc.gethostbyname(TS2_host)
    # connect to the server on local machine
    server_binding2 = (sa_sameas_myaddr2, port_TS2)
    cs2.connect(server_binding2)

    print("Connect to" , TS1_host, ",", TS2_host, ".\n")
    """

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


    # get message
    while 1:
        data_from_client = csockid.recv(100)
        if not data_from_client: break
        msg_decoding = data_from_client.decode('utf-8')
        print("message from client:", msg_decoding)

    ss.close()
    exit()

t1 = threading.Thread(name='rs_server', target=server)
t1.start()

input("Hit ENTER  to exit\n")
exit()
