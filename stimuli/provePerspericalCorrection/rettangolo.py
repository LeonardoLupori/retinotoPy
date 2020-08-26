from psychopy import core, visual, event, data, monitors

from psychopy.tools import monitorunittools as mt

from psychopy.visual.windowwarp import Warper

# ------------------------------------------------------------------------------
# Monitor specifications
monitorUsed = 'tryMonitor'
frameRate = 60.0
distCm = 15.0

# Periodic stimulations
period = 5.0

# Inner plaid contrast reversal
spFreq = 0.3
temporalFreq = 2
contrast = 0.9

# ------------------------------------------------------------------------------

reversalClock = core.Clock()

mon = monitors.Monitor(monitorUsed)

screenSizeDeg = [mt.pix2deg(1920/2,mon,correctFlat=False)*2, mt.pix2deg(1200/2,mon,correctFlat=False)*2]


stimWin = visual.Window(
    [1920,1200],
    screen = 0,
    fullscr = True,
    monitor = monitorUsed,
    units = "deg",
    blendmode = 'add',
    allowStencil = True,
    useFBO = True
    )

warper = Warper(
    stimWin,
    warp = 'spherical',
    warpGridsize = 64,
    eyepoint = [0.5, 0.5]
    )
warper.dist_cm = distCm
warper.changeProjection("spherical")
                
gratingBack = visual.GratingStim(
    stimWin,
    tex = 'sqrXsqr',
    mask = 'none',
    maskParams = None,
    units = 'deg',
    pos = (0.0, 0.0),
    size = [90],
    sf = spFreq,
    ori = 0.0,
    phase = (0.0, 0.0),
    texRes = 128,
    contrast = contrast,
    opacity = 1.0,
    blendmode = 'avg',
    autoDraw = False
    )                
                
rectH = visual.Rect(
    stimWin,
    units = "deg",
    width = 5,
    height = screenSizeDeg[1],
    fillColor = [1,1,1],
    pos = [-screenSizeDeg[0]/2 , 0]
    )
            
rectV = visual.Rect(
    stimWin,
    units = "deg",
    width = screenSizeDeg[0],
    height = 5,
    fillColor = [1,1,1],
    pos = [0, -screenSizeDeg[1]/2]
    )

reversalClock.reset()


# ------------------------------------------------------------------------------
#   STIMULATION LOOP
# ------------------------------------------------------------------------------

for i in range(360):
    if reversalClock.getTime() >= 1/temporalFreq:
        gratingBack.phase = gratingBack.phase + [0, .5]
        reversalClock.reset()
    
    gratingBack.draw()
    # gratingV.draw()


    # rectH.draw()
    # rectH.pos += (0.2,0)
    # rectV.draw()
    # rectV.pos += (0,0.2)
    stimWin.flip()