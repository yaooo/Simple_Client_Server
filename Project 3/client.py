import threading
import socket as mysoc
import time
import hmac

port_RS = 5000
port_TS1 = 6001
port_TS2 = 7001
hostname_file = "PROJ3-HNS.txt"
TS2_hostname = "java.cs.rutgers.edu"
TS1_hostname = "cpp.cs.rutgers.edu"

def read_file(file_name):
    with open(file_name) as f:
        lines = f.readlines()
    f.close()
    return lines

def choose_TL(name, TL1, TL2):
    if name == TL1:
        return 1
    if name == TL2:
        return 2
    return -1

def compute_key(message, key):
    d2 = hmac.new(key.encode(), message.encode("utf-8"))
    hexdigest = d2.hexdigest()
    return  hexdigest, key, message


def client():
    try:
        cs = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    sa_sameas_myaddr = mysoc.gethostbyname(mysoc.gethostname())
    server_binding = (sa_sameas_myaddr, port_RS)
    cs.connect(server_binding)

    # Connect to TL1
    try:
        cs1 = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))
    sa_sameas_myaddr1 = mysoc.gethostbyname(TS1_hostname)
    cs1.connect((sa_sameas_myaddr1, port_TS1))

    # Connect to TL2
    try:
        cs2 = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))
    sa_sameas_myaddr2 = mysoc.gethostbyname(TS2_hostname)
    cs2.connect((sa_sameas_myaddr2, port_TS2))

    # READ FILE
    hostnames = read_file(hostname_file)

    # Make the output file
    output_file = open("RESOLVED.txt", "w")
    for i in hostnames:
        temp = i.strip("\n").split()
        hexdigest, key, message = compute_key(temp[1], temp[0])
        msg_to_TL = temp[2]
        sent_msg = message + "," + hexdigest + "\n"
        cs.send(sent_msg.encode('utf-8'))
        data_from_server = cs.recv(100)
        msg_decoding = data_from_server.decode('utf-8')
        TL_number = choose_TL(msg_decoding, TS1_hostname, TS2_hostname)

        if TL_number == 1:
            cs2.sendall("-1".encode('utf-8'))
            cs1.sendall(msg_to_TL.encode('utf-8'))
            print("To TL1: ", msg_to_TL)
            m = cs1.recv(100).decode('utf-8')
            output_file.write("TLDS1 " + m)

        elif TL_number ==2:
            cs1.sendall("-1".encode('utf-8'))
            cs2.sendall(msg_to_TL.encode('utf-8'))
            print("To TL2: ", msg_to_TL)
            m = cs2.recv(100).decode('utf-8')
            output_file.write("TLDS2 " + m)

    cs.send("disconnecting".encode('utf-8'))

    output_file.close()


    # close the client socket
    cs1.close()
    cs2.close()
    cs.close()
    exit()

if __name__ == "__main__":

        t2 = threading.Thread(name='client', target=client)
        t2.start()

        input("Hit ENTER  to exit\n")
        exit()
