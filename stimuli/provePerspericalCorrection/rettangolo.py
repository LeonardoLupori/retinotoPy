from psychopy import core, visual, event, parallel, data, monitors
from psychopy.tools import monitorunittools as mt
import numpy as np
import operator
from psychopy.visual.windowwarp import Warper

temporalFreq = 3;
frameRate = 60;

reversalClock = core.Clock()

mon = monitors.Monitor(name = 'testMonitor')


mk = np.ones((128,128))

stimWin = visual.Window([1920,1080],
            screen = 0,
            fullscr = True,
            monitor="testMonitor",
            units="deg",
            blendmode = 'add',
            allowStencil=True,
            useFBO = True)

warper = Warper(stimWin,
                warp='cylindrical',
                warpfile = "",
                warpGridsize = 64,
                eyepoint = [0.5, 0.5],
                flipHorizontal = False,
                flipVertical = False)
                
                
                
screenSizeDeg = [mt.pix2deg(1920/2,mon,correctFlat=True)*2, mt.pix2deg(1080/2,mon,correctFlat=True)*2]


rectH = visual.Rect(stimWin,
            units = "deg",
            width=5,
            height=screenSizeDeg[1],
            fillColor = [1,1,1],
            pos = [-screenSizeDeg[0]/2 , 0])
            
rectV = visual.Rect(stimWin,
            units = "deg",
            width=screenSizeDeg[0],
            height=5,
            fillColor = [1,1,1],
            pos = [0, -screenSizeDeg[1]/2])

reversalClock.reset()

for i in range(800):
    if reversalClock.getTime() >= 1/temporalFreq:
        reversalClock.reset()
    
    #rectH.draw()
    #rectH.pos += (0.2,0)
    rectV.draw()
    rectV.pos += (0,0.2)
    
    
    stimWin.flip()