from psychopy import core, visual, event, parallel, data
import pandas
import json
import random, socket, select

# Parallel port variables
endScan_pin = 2         # Pin to which the Scanning PC sends a TTL acknowledging the end of the scan

#Define window, backgroud and grating objects 
stimWin = visual.Window([1920,1080],
            screen = 0,
            fullscr = True,
            monitor="testMonitor",
            units="deg",
            color = [1,1,1])

grating = visual.GratingStim(stimWin, 
            pos=[0,0],
            size=[3,3],
            tex='sin',
            mask=None,
            #maskParams={'fringeWidth': 1},
            #maskParams={'sd':10},
            sf=[0.5],
            ori=0,
            phase=0,
            contrast=0.9,
            colorSpace = 'rgb',
            color=[1,1,1],
            autoDraw = False)

background = visual.ShapeStim(stimWin,
            pos=[0,0],
            units='norm',
            vertices=((1,1),(-1,1),(-1,-1),(1,-1)),
            closeShape= True,
            lineWidth=0,
            fillColor=[0,0,0],
            fillColorSpace='rgb',
            autoDraw = False)

#make the mouse invisible
event.Mouse(visible=False)

#Open communication with the parallel port
pPort = parallel.ParallelPort(address=0xd100)
pPort.setData(int('00000000',2))
print('Parallel port initialized')

#Measure the actual framerate of the screen
print('Measuring actual monitor framerate...'),
frameRate = stimWin.getActualFrameRate(nIdentical=50, nMaxFrames=1000, nWarmUpFrames=50, threshold=1)
if frameRate == None:
    print(' Unable to measure a consistent framerate for this monitor.')
    quit()
else:
    print(' Measured framerate: {}'.format(frameRate))


#----------------------------------------------
# DEFINING THE STIMULI
#----------------------------------------------
preStimFrames = 60
stimFrames = 300
postStimFrames = 60
stimuli = [{'spatialFreq': 0.05, 'orientation': 0, 'contrast': 0.8, 'temporalFreq': 1},
{'spatialFreq': 0.05, 'orientation': 45, 'contrast': 0.8, 'temporalFreq': 1},
{'spatialFreq': 0.05, 'orientation': 90, 'contrast': 0.8, 'temporalFreq': 1},
{'spatialFreq': 0.05, 'orientation': 135, 'contrast': 0.8, 'temporalFreq': 1},
{'spatialFreq': 0.05, 'orientation': 180, 'contrast': 0.8, 'temporalFreq': 1},
{'spatialFreq': 0.05, 'orientation': 225, 'contrast': 0.8, 'temporalFreq': 1},
{'spatialFreq': 0.05, 'orientation': 270, 'contrast': 0.8, 'temporalFreq': 1},
{'spatialFreq': 0.05, 'orientation': 315, 'contrast': 0.8, 'temporalFreq': 1}]



#----------------------------------------------
# MAIN LOOP
#----------------------------------------------
keepGoing = True

while keepGoing:
    
    for thisStimulus in stimuli:
        # Break the stimulation loop if the experimenter presses "q" or "esc"
        if len(event.getKeys(keyList=('escape','q'))) > 0:
            event.clearEvents('keyboard')
            #stimWin.close()
            keepGoing = False
            break
            
        # PRE-STIMULUS  
        pPort.setData(int('10000000',2))        #Trigger for the pre-stimulus
        for frameN in range(preStimFrames):
            background.draw()
            stimWin.flip()
        pPort.setData(int('00000000',2))
            
        # Update stimulus parameters with the current trial
        grating.sf = thisStimulus['spatialFreq']
        grating.ori = thisStimulus['orientation']
        grating.contrast = thisStimulus['contrast']
        temporalFreq = thisStimulus['temporalFreq']
        
        # STIMULUS
        pPort.setData(int('10000000',2))        #Trigger for the stimulation
        for frameN in range(stimFrames):
            grating.setPhase(1/float(frameRate)*temporalFreq, '+')
            grating.draw()
            stimWin.flip()
        pPort.setData(int('00000000',2))
        
        # POST STIMULATION
        for frame in range(postStimFrames):
            background.draw()
            stimWin.flip()
    
stimWin.close()