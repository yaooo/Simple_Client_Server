import socket as mysoc
import threading
import time
Port_RS = 5001
Port_TS = 6000
DNSTS = "PROJI-DNSTS.txt"


def read_file(file_name):
    with open(file_name) as f:
        lines = f.readlines()
    f.close()
    return lines


def lookup(hostname_string):
    lines = read_file(DNSTS)
    for i in lines:
        if len(i) < 3:
            break
        if i.startswith(hostname_string.lower()):
            if not i.endswith("\n"):
                return i + "\n"
            return i
    return hostname_string + " - ERROR: HOST NOT FOUND\n"

def server():
    try:
        ss = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: RS Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))
    server_binding = ('', Port_TS)
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


t1 = threading.Thread(name='server', target=server)
t1.start()

input("Hit ENTER  to exit\n")
exit()