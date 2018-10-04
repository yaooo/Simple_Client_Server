import threading
import socket as mysoc
import time
port_TS = 6000
port_RS = 5001
hostname_file = "PROJI-HNS.txt"

class attr:
    count_TS = 0
    CS = None


def read_file(file_name):
    with open(file_name) as f:
        lines = f.readlines()
    f.close()
    return lines

def connect_to_TS(hostname):
    try:
        cs = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    # Define the port on which you want to connect to the server
    sa_sameas_myaddr = mysoc.gethostbyname(hostname)
    # connect to the server on local machine
    server_binding = (sa_sameas_myaddr, port_TS)
    cs.connect(server_binding)

    return cs


def client():
    try:
        cs = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    # Define the port on which you want to connect to the server

    sa_sameas_myaddr = mysoc.gethostbyname("man.cs.rutgers.edu")
    # connect to the server on local machine
    server_binding = (sa_sameas_myaddr, port_RS)
    cs.connect(server_binding)

    # READ FILE
    hostnames = read_file(hostname_file)

    # Make the output file
    output_file = open("RESOLVED.txt", "w")

    for i in hostnames:
        temp = i.strip("\n")
        cs.sendall(temp.encode('utf-8'))
        data_from_server = cs.recv(100)
        msg_decoding = data_from_server.decode('utf-8')
        print("Message sent by the client: ", temp)
        print("**Message Received by the client: ", msg_decoding)

        if msg_decoding.endswith("NS\n") or msg_decoding.endswith("NS"):
            if attr.CS is None:
                TS_name = msg_decoding.split()
                attr.CS = connect_to_TS(TS_name[0])

            attr.CS.sendall(temp.encode('utf-8'))
            time.sleep(2)
            data_from_server1 = attr.CS.recv(100)
            msg_decoding1 = data_from_server1.decode('utf-8')
            print("Message from TS:" + msg_decoding1)
            output_file.write(msg_decoding1)
        else:
            output_file.write(msg_decoding)
    output_file.close()

    # close the client socket
    cs.close()
    if attr.CS is not None:
        attr.CS.close()
    exit()


t2 = threading.Thread(name='client', target=client)
t2.start()

input("Hit ENTER  to exit\n")
exit()
