from psychopy import monitors, visual, tools
from psychopy.visual.windowwarp import Warper

monitorList = monitors.getAllMonitors()


stimFrames = 60
temporalFreq = 3
frameRate = 60.0
monitorUsed = 'tryMonitor'

columns = 2
rows = 2

monitor = monitors.Monitor(monitorUsed)
screenSize = monitor.getSizePix()
# monitor.setDistance(2.0)


widthDeg = tools.monitorunittools.pix2deg(
    screenSize[0], monitor, correctFlat=False)
widthIncrement = widthDeg/(columns+2)

heightDeg = tools.monitorunittools.pix2deg(
    screenSize[1], monitor, correctFlat=False)
heightIncrement = heightDeg/(rows+2)

stimWin = visual.Window(
    #WinType = 'pyglet',
    size=screenSize,
    screen=0,
    fullscr=True,
    monitor="tryMonitor",
    units="deg",
    useFBO = True)

warper = Warper(stimWin,
                warp='spherical',
                # warpfile = "",
                warpGridsize = 64,
                eyepoint = [0.5, 0.5],
                flipHorizontal = False,
                flipVertical = False)

warper.dist_cm = 2.0
#warper.changeProjection("spherical")


grating = visual.GratingStim(stimWin,
    pos=[0, 0],
    size=[50],
    tex='sqr',
    mask='raisedCos',
    maskParams={'fringeWidth': 0.5},
    #maskParams={'sd':3},
    sf=[0.5],
    ori=0,
    phase=0,
    contrast=0.8,
    colorSpace='rgb',
    color=[1, 1, 1],
    autoDraw=True)



conditions = columns*rows
x = [-heightIncrement, -heightIncrement, heightIncrement, heightIncrement]
y = [-widthIncrement, widthIncrement, -widthIncrement, widthIncrement]



for i in range(conditions):

    grating.pos = [y[i], x[i]]

    for frameN in range(stimFrames):
        grating.draw()
        stimWin.flip()

    for frameN in range(stimFrames):
        grating.setPhase(1/frameRate*temporalFreq, '+')
        grating.draw()
        stimWin.flip()
