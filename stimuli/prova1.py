import socket
import time 
import json

TCP_ip = '192.168.0.2'
TCP_port = 40000
TCP_buffSize = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_ip, TCP_port))
print('connected!')

keepGoing = True

while keepGoing:    
    try:
        print('Waiting for server message...', end= ' ')
        msg = s.recv(TCP_buffSize)
        print('recieved.')
        # print(msg.decode('UTF-8'))
        msg = json.loads(msg)

        if type(msg) is not dict:
            keepGoing = False
            print('Termination message recieved. Closing connection...')
            s.close()
            print('Connection closed.')
            break

        # print(msg)
        barSettings = msg['barStim']
        print(barSettings)

    except:
        print('Error in TCP/IP message recieving. Closing connection...')
        s.close()
        print('Connection closed.')
        keepGoing = False
        break
