from psychopy import monitors
from psychopy.visual import Window, GratingStim
from psychopy.visual.windowwarp import Warper

monitorUsed = 'tryMonitor'


monitor = monitors.Monitor(monitorUsed)
monitor.setDistance(10.0)

win = Window(
    size = [1920, 1200],
    monitor='tryMonitor',
    screen=0,
    fullscr=True,
    useFBO = True
    ) 

warper = Warper(
    win,
    warpGridsize = 64,
    eyepoint = [0.5, 0.5],
    flipHorizontal = False,
    flipVertical = False
    )
warper.dist_cm = monitor.getDistance()
warper.changeProjection("spherical")

grating = GratingStim(
    win=win,
    mask='none',
    size=50,
    pos=[0,0],
    sf=0.3)


for i in range(300):
    grating.setPhase(0.05, '+')
    grating.draw()
    win.flip()