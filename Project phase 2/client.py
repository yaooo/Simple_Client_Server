import threading
import socket as mysoc
import sys
import time

port_RS = 5002
hostname_file = "PROJ2-HNS.txt"
RS_host_name = ""

def read_file(file_name):
    with open(file_name) as f:
        lines = f.readlines()
    f.close()
    return lines


def client():
    try:
        cs = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    # Define the port on which you want to connect to the server
    # connect to the server on local machine
    sa_sameas_myaddr = mysoc.gethostbyname(RS_host_name)
    server_binding = (sa_sameas_myaddr, port_RS)
    cs.connect(server_binding)

    # READ FILE
    hostnames = read_file(hostname_file)

    # Make the output file
    output_file = open("RESOLVED.txt", "w")
    time.sleep(2)
    for i in hostnames:
        temp = i.strip("\n")
        cs.send(temp.encode('utf-8'))
        time.sleep(1)

        data_from_server = cs.recv(100)
        msg_decoding = data_from_server.decode('utf-8')
        print("Message sent by the client: ", temp)
        print("**Message Received by the client: ", msg_decoding)

        if(msg_decoding == "ERROR\n"):
            msg_decoding = "ERROR: HOST NOT FOUND\n"
        output_file.write(msg_decoding)
    output_file.close()
    # close the client socket
    cs.close()
    exit()

if __name__ == "__main__":
        hostname_file = sys.argv[2]
        RS_host_name = sys.argv[1]
        t2 = threading.Thread(name='client', target=client)
        t2.start()

        input("Hit ENTER  to exit\n")
        exit()
