import socket
import time 
import json

TCP_ip = 'localhost'
TCP_port = 80
TCP_buffSize = 4096

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_ip, TCP_port))
print('connected!')

keepGoing = True

while keepGoing:    
    try:
        print('Waiting for server message...')
        msg = s.recv(TCP_buffSize)
        print('recieved.')
        msg = json.loads(msg)

        if type(msg) is not dict:
            keepGoing = False
            print('Termination message recieved. Closing connection...')
            s.close()
            print('Connection closed.')
            break

        reps = msg['repetitions']
        rows = msg['rows']
        cols = msg['columns']
        trials = reps*rows*cols

        print('Current Exp consists of {} reps, with stimuli in {} rows and {} columns'.format(reps,rows,cols))
        print('Total of {} trials'.format(trials))
    except:
        print('Error in TCP/IP message recieving. Closing connection...')
        s.close()
        print('Connection closed.')
        keepGoing = False
        break
