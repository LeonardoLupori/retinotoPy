from psychopy import core, visual, clock, event
import time

win = visual.Window([400,400])

for i in range(5):
    print(event.getKeys(None))
    #print('prova')
    time.sleep(1)