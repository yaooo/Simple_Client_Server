* Yao Shi
* Chris Oles

## Prerequisites
Python 3 required.

## Run the code

As always, first start the two TS servers, then the RS server(root server) and then the client program.

* I will start both TS servers followed by the name of the input file(on two random ilab machines)
like this:
```
python ./TSCOM.py ./PROJ2-DNSCOM.txt
python ./TSEDU.py ./PROJ2-DNSEDU.txt
```

* I will start the RS server and pass it a command line argument containing the hostname of the .com server followed by the hostname of the .edu server  followed by the name of the input file(On a third Ilab machine)
like this:
```
python ./RS.py $TSCOMHOSTNAME $TSEDUHOSTNAME  PROJ2-DNSRS.txt
(Replace $TSCOMHOSTNAME with the hostname of the computer you started the COM ts server on)
(Replace $TSEDUHOSTNAME with the hostname of the computer you started the EDU ts server on)

EX: python3 ./RS.py kill.cs.rutgers.edu grep.cs.rutgers.edu PROJ2-NDSRS.txt
```

* I will start the client on a fourth ilab machine passing the hostname of the RS server as a command line argument followed by the name of the input file
like this
```
python ./CLIENT.py $RSHOSNAME PROJ2-HNS.txt
(Replace $RSHOSNAME with the hostname of the computer you started the RS server on)
```

* Note the correct answers should be one answer per line  either hostname ipadress A or Error: HOST NOT FOUND)
