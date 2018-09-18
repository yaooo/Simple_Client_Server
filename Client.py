import numpy as mypy
import threading

import socket as mysoc

def client():
    try:
        cs = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

# Define the port on which you want to connect to the server
    port = 6666
    sa_sameas_myaddr = mysoc.gethostbyname(mysoc.gethostname())
    # connect to the server on local machine
    server_binding = (sa_sameas_myaddr, port)
    cs.connect(server_binding)

    #READ FILE
    with open('HW1test.txt') as f:
        lines = f.readlines()
    f.close()
    print(lines)

    output_file = open("HW1out.txt","w")

    for i in lines:
        cs.sendall(i.encode('utf-8'))
        data_from_server = cs.recv(100)
        msg_decoding = data_from_server.decode('utf-8')
        print("Getting message from server:", msg_decoding)
        output_file.write(msg_decoding)

    output_file.close()

    # close the client socket
    cs.close()
    exit()

t2 = threading.Thread(name='client', target=client)
t2.start()

print("Hit ENTER to exit")
input("Hit ENTER  to exit")
exit()
