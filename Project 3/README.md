# Simple Client Server Project Phase 2

## Prerequisites
Python 3 required.

## Run the code

As always, first start the two TS servers, then the AS server(root server) and then the client program.

TLDS1 should run in cpp.cs.rutgers.edu and TLDS2 should run in java.cs.rutgers.edu. The client and AS server should not run in the same computer as TLDS1 and TLDS2 (e.g., do not use cpp.cs.rutgers.edu and  java.cs.rutgers.edu for them).

In java.cs.rutgers.edu, run:
```
python3 TS2.py
```

In cpp.cs.rutgers.edu, run:
```
python3 TS1.py
```

Client and AS server should run in the same computer, run
```
python3 AS.py
(then in a different terminal, run:)
python3 client.py
```

If there is a NS entry in the test files ignore them.

## Author
* Yao Shi
* Chris Oles
