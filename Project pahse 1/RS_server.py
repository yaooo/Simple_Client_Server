import numpy as np
import socket as mysoc
import threading

DNSRS = "PROJ1-DNSRS.txt"
port_RS = 6666


def read_file(file_name):
    with open(file_name) as f:
        lines = f.readlines()
    f.close()
    return lines


def lookup(hostname_string):
    lines = read_file(DNSRS)
    for i in lines:
        x = i.split()
        if hostname_string.lower() == x[0].lower():
            return i.strip("\n") + " A\n"
    return "TS_hostname - NS\n"


print(lookup("supremenewyork.com"))


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
    print("[S]: Server host name is: ", host)
    localhost_ip = (mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ", localhost_ip)
    csockid, addr = ss.accept()
    print("[S]: Got a connection request from a client at", addr)

    # Receiving message and reverse the message
    while 1:
        data_from_client = csockid.recv(100)
        if not data_from_client: break
        msg_decoding = data_from_client.decode('utf-8')
        print("Hostname from client:", msg_decoding)
        text = lookup(msg_decoding)
        csockid.send(text.encode('utf-8'))
    ss.close()
    exit()


t1 = threading.Thread(name='server', target=server)
t1.start()

input("Hit ENTER  to exit\n")
exit()
