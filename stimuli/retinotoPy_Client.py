import socket
import sys
import json
from psychopy import core, visual, clock, event



# These settings need to be the same as the one for the MATLAB server, specified
# in the file 'generalSettings.m' under the section 'TCP/IP SETTINGS'
TCP_ip = 'localhost'
TCP_port = 80
TCP_buffSize = 4096

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.connect((TCP_ip, TCP_port))
tcp.settimeout(None)

win = visual.Window([400,400])
clock.wait(1)

while True:
    # Break the stimulation loop if the experimenter presses "q" or "esc"
    if len(event.getKeys(keyList=('escape','q'))) > 0:
        event.clearEvents('keyboard')
        tcp.close()
        print('Communication Closed')
        break
    message = tcp.recv(TCP_buffSize)
    print(message.decode('utf-8'))