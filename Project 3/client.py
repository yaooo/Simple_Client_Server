import threading
import socket as mysoc
import sys
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


# Example
# d2 = hmac.new("k3522".encode(), c1.encode("utf-8"))
# print(d2.hexdigest())
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
    sa_sameas_myaddr = mysoc.gethostbyname(mysoc.gethostname())
    cs1.connect((sa_sameas_myaddr, port_TS1))

    # Connect to TL2
    try:
        cs2 = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))
    sa_sameas_myaddr = mysoc.gethostbyname(mysoc.gethostname())
    cs2.connect((sa_sameas_myaddr, port_TS2))


    # READ FILE
    hostnames = read_file(hostname_file)

    # Make the output file
    output_file = open("RESOLVED.txt", "w")
    time.sleep(2)
    for i in hostnames:
        temp = i.strip("\n").split()
        hexdigest, key, message = compute_key(temp[1], temp[0])
        msg_to_TL = temp[2]

        sent_msg = message + "," + hexdigest + "\n"
        print("Sending msg to AS...")
        cs.send(sent_msg.encode('utf-8'))
        time.sleep(1)

        data_from_server = cs.recv(100)
        msg_decoding = data_from_server.decode('utf-8')
        print("Message sent by the client: ", temp)
        print("**Message Received by the client: ", msg_decoding)



        TL_number = choose_TL(msg_decoding, TS1_hostname, TS2_hostname)
        if TL_number == 1:
            cs1.send(msg_to_TL.encode('utf-8'))
            d1 = cs1.recv(100)
            m = d1.decode('utf-8')
            print("To TL1: ", msg_to_TL)
            print("**Message Received by the client from TL1: ", m)
        # elif TL_number ==2:
        #     cs2.send(msg_to_TL.encode('utf-8'))
        #     d2 = cs2.recv(100)
        #     m = d2.decode('utf-8')
        #     print("To TL2: ", msg_to_TL)
        #     print("**Message Received by the client from TL2: ", m)
        # print("HERE\n")

        # if(msg_decoding == "ERROR\n"):
        #     msg_decoding = "ERROR: HOST NOT FOUND\n"
        # output_file.write(msg_decoding)
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
