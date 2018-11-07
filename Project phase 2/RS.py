import numpy as np
import socket as mysoc
import threading
import sys

DNSRS = "PROJ2-DNSRS.txt"
TS_come_host = ""
TS_edu_host =""
port_RS = 5001
port_TS1 = 6000
port_TS2 = 7000


def read_file(file_name):
    with open(file_name) as f:
        lines = f.readlines()
    f.close()
    return lines


def lookup(hostname_string):
    if hostname_string.startswith("www."):
        hostname_string = hostname_string[4:].strip("\n")
    lines = read_file(DNSRS)
    for i in lines:
        if i.find(hostname_string.lower()) != -1:
            if not i.endswith("\n"):
                return i + "\n"
            return i
    return "ERROR\n"

def server():
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

    # connect to TS1
    try:
        cs1 = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))
    # Define the port on which you want to connect to the server
    sa_sameas_myaddr1 = mysoc.gethostbyname(mysoc.gethostname())
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
    sa_sameas_myaddr2 = mysoc.gethostbyname(mysoc.gethostname())
    # connect to the server on local machine
    server_binding2 = (sa_sameas_myaddr2, port_TS2)
    cs2.connect(server_binding2)


    # Receiving message and reverse the message
    while 1:
        data_from_client = csockid.recv(100)
        if not data_from_client: break
        msg_decoding = data_from_client.decode('utf-8')
        print("Hostname from client:", msg_decoding)
        text = lookup(msg_decoding)

        if text=="ERROR\n":
            if(msg_decoding.endswith(".com") or msg_decoding.endswith(".com\n")):
                temp1 = msg_decoding.strip("\n")
                cs1.sendall(temp1.encode('utf-8'))
                data_from_server1 = cs1.recv(100)
                text = data_from_server1.decode('utf-8')
            elif (msg_decoding.endswith(".edu") or msg_decoding.endswith(".edu\n")):
                temp2 = msg_decoding.strip("\n")
                cs2.sendall(temp2.encode('utf-8'))
                data_from_server2 = cs2.recv(100)
                text = data_from_server2.decode('utf-8')
        csockid.send(text.encode('utf-8'))
    ss.close()
    exit()


if __name__ == "__main__":
    DNSRS = sys.argv[3]
    TS_come_host = sys.argv[1]
    TS_edu_host = sys.argv[2]

    t1 = threading.Thread(name='server1', target=server)
    t1.start()

    input("Hit ENTER  to exit\n")
    exit()
