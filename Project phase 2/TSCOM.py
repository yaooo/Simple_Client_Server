import socket as mysoc
import threading
import time
import sys
Port_TS1 = 6000
DNSTS = ""


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
        if i.find(hostname_string.lower()) != -1:
            if not i.endswith("\n"):
                return i + "\n"
            return i
    return "ERROR\n"

def server1():
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


if __name__ == "__main__":
    DNSTS = sys.argv[1]

    t1 = threading.Thread(name='server1', target=server1)
    t1.start()

    input("Hit ENTER  to exit\n")
    exit()


