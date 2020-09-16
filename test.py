from typing import Container
from psychopy import visual, core, monitors, event

import numpy as np

# import stimuli.visModules.warpedStimuli as warp

# from PIL import Image, ImageDraw

import stimuli.warpStimuli as wStim

# import time


framerate = 60
period = 10

temporalFreq = 1


reversalClock = core.Clock()

mon = monitors.Monitor('tryMonitor')


stimWin = visual.Window(
    mon.getSizePix(),       # Size of the current monitor in pixels
    screen = 0,
    fullscr = False,
    monitor = mon,
    units = 'deg',
    blendMode='avg',
    allowStencil = True,    # Essential for the aperture to work
    useFBO = True,           # Essential for the warper to work
    )


wBar = wStim.WarpedBar(
    stimWin,
    center=0.5,
    ori='h',
    barWidth=4,
    includeBarWidth=True,
    nVert=100)

WarpG = wStim.warpedGrating(
    stimWin,
    sf=1,
    ori='hv',
    waveform='sqr',
    phase=0)

txMaskRes = 512

im = WarpG.createTexture(textRes=1024)

mask = wBar.getTextureMask(textRes=txMaskRes)

# dummy = np.full((128,128),-1)
# dummy[32:-32,32:-32] = 1

gr = visual.GratingStim(
    stimWin,
    # sf=None,
    # tex = im,
    units = 'pix',
    size=[1920,1200],
    # mask = mask,
    contrast=0.3
)


nframes = 100

txMaskRes = 512
txMasks = np.zeros((txMaskRes,txMaskRes,nframes))

for i in range(nframes):
    wBar.center += 1/nframes
    txMasks[:,:,i] = wBar.getTextureMask(textRes=txMaskRes)
    print('CalculatingFrame #{}/{}'.format(i+1,nframes))


# ------------------------------------------------------------------------------

stimWin.recordFrameIntervals = True
for i in range(nframes):

    gr.mask = txMasks[:,:,i]
    gr.draw()
    
    # frames[i].draw()
    stimWin.flip()


# ------------------------------------------------------------------------------


import matplotlib.pyplot as plt
t = np.array(stimWin.frameIntervals)
print('avgerage time: {:.3f}ms'.format(np.average(t)*1000))
print('max time: {:.3f} ms'.format(np.max(t)*1000))
print('min time: {:.3f} ms'.format(np.min(t)*1000))
plt.plot(t*1000)
plt.ylim([0,30])
plt.show()