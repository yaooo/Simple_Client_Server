import threading
import socket as mysoc

port_DS = 9631
port_RS = 6666
hostname_file = "PROJ1-HNS.txt"


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

    sa_sameas_myaddr = mysoc.gethostbyname(mysoc.gethostname())
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
        data_from_server = cs.recv(1024)
        msg_decoding = data_from_server.decode('utf-8')
        print("Message sent by the client: ", i)
        print("**Message Received by the client: ", msg_decoding)
        output_file.write(msg_decoding)
    output_file.close()

    # close the client socket
    cs.close()
    exit()


t2 = threading.Thread(name='client', target=client)
t2.start()

input("Hit ENTER  to exit\n")
exit()
