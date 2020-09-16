from psychopy import visual, core, monitors, event, parallel
import numpy as np
import sys

# Custom modules
import stimuli.warpStimuli as wStim

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# USER PARAMETERS
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# Monitor specifications
monitorUsed = 'tryMonitor'  # Monitor Name
frameRate = 60.0            # The default, a more accurate will be calculated after
distCm = 20                 # Distance eye-monitor

# Periodic bar drifting
bar_repetitions = 3         # number of bar swipes
bar_orientation = 'h'       # 'h' or 'v'
bar_dir = True              # True:  False:
bar_period = 5              # sec
bar_width = 12              # deg
bar_textRes = 512           # a power of 2 - tradeoff between preallocation speed
                            # and graphical accuracy

# Inner plaid contrast reversal
gr_spFreq = 0.05
gr_temporalFreq = 5
gr_contrast = 0.9
gr_orientation = 'hv'       # 'h' 'v' or 'hv'
gr_waveform = 'sqr'         # 'sqr' or 'sin'
gr_textRes = 1024           # a power of 2 - tradeoff between preallocation speed
                            # and graphical accuracy

#  TPC/IP Communication
TCP_ip = 'localhost'        # IP address of the recording machine
TCP_port = 80               # 
TCP_buffSize = 4096

# ------------------------------------------------------------------------------
# DO NOT EDIT PAST THIS POINT
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------


reversalClock = core.Clock()    # Control the contrast reversal of the background
expDurationClock = core.Clock() # Measures the actual duration of the experiment

# Setup the Monitor object based on the "monitor used template"
mon = monitors.Monitor(monitorUsed)
mon.setDistance(distCm)


# ------------------------------------------------------------------------------
# Initialize various objects
# ------------------------------------------------------------------------------

# WINDOW (Same size as the monitor in FullScreen Mode)
stimWin = visual.Window(
    mon.getSizePix(),       # Size of the current monitor in pixels
    screen = 0,
    fullscr = False,
    monitor = mon,
    units = 'deg'
    )

# WARPED GRATING OBJ (to generate the warped texture)
warpGrating = wStim.warpedGrating(
    stimWin,
    sf = gr_spFreq,
    ori = gr_orientation,
    waveform = gr_waveform,
    phase = 0)

# WARPED BAR OBJ (to generate the warped bar to use as a mask for the grating texture)
warpBar = wStim.WarpedBar(
    stimWin,
    center = 0,
    ori = bar_orientation,
    barWidth = bar_width,
    includeBarWidth = True,
    nVert = 200)

# MAIN GRATINGS (list of 2 grating objects with different phases)
gratings = []
print('Pre-computing Warped grating texture...',end='')
gratings.append(visual.GratingStim(
    stimWin,
    units = 'pix',
    size = mon.getSizePix(),
    contrast = gr_contrast,
    tex = warpGrating.createTexture(gr_textRes)
))
warpGrating.phase = 0.5
gratings.append(visual.GratingStim(
    stimWin,
    units = 'pix',
    size = mon.getSizePix(),
    contrast = gr_contrast,
    tex = warpGrating.createTexture(gr_textRes)
))
print(' done.')
txtToUse = 0


# ------------------------------------------------------------------------------
# Compute some experiment parameters
# ------------------------------------------------------------------------------

#Measure the actual framerate of the screen
print('Measuring actual monitor framerate...'),
measuredFrameRate = stimWin.getActualFrameRate(nIdentical=50, nMaxFrames=500, nWarmUpFrames=50, threshold=1)
if measuredFrameRate == None:
    print(' Unable to measure a consistent framerate for this monitor.')
    sys.exit()
else:
    print(' Measured framerate: {}'.format(measuredFrameRate))
    frameRate = measuredFrameRate


nFrames = frameRate * bar_period    # set the total numb of frames for each cycle
nFrames = int(nFrames)

if not bar_dir:                     # start from the opposite side of the screen
    warpBar.center = 1

# ------------------------------------------------------------------------------
# Pre-Compute the coordinates of the warped bar for every frame (for speed)
# ------------------------------------------------------------------------------
textMasks = np.zeros((bar_textRes,bar_textRes,nFrames))

for i in range(nFrames):
    if bar_dir:
        warpBar.center += 1/nFrames
    else:
        warpBar.center -= 1/nFrames

    textMasks[:,:,i] = warpBar.getTextureMask(bar_textRes)

    if (i+1)%100 == 0 or i+1 == nFrames:
        print('Pre-computing frames... {}/{}'.format(i+1,nFrames))


# ------------------------------------------------------------------------------
# MAIN STIMULATION LOOP
# ------------------------------------------------------------------------------

stimWin.recordFrameIntervals = True
expDurationClock.reset()    

for frame in range(nFrames * bar_repetitions):

    if reversalClock.getTime() >= 1/gr_temporalFreq:
        txtToUse = (txtToUse+1) % 2
        reversalClock.reset()

    gratings[txtToUse].mask = textMasks[:,:,frame%nFrames]
    gratings[txtToUse].draw()
    stimWin.flip()

experimentDuration = expDurationClock.getTime()

# ------------------------------------------------------------------------------
# PLOT TIMING PERFORMANCE
# ------------------------------------------------------------------------------

# Experiment total duration
expectedDuration = (1/frameRate) * nFrames * bar_repetitions
print('EXP DURATION - measured: {:.3f}s | expected: {:.3f}s. | difference: {:.3f}s.'
    .format(experimentDuration,expectedDuration,experimentDuration-expectedDuration))

# Timing for all the frames
t = np.array(stimWin.frameIntervals)*1000
print('FRAME TIMING - avg: {:.1f}ms | min: {:.1f}ms | max: {:.1f}ms.'.
    format(np.average(t),np.min(t),np.max(t)))
if np.max(t) >= 20:
    import matplotlib.pyplot as plt

    print('avgerage time: {:.3f}ms'.format(np.average(t)))
    print('max time: {:.3f} ms'.format(np.max(t)))
    print('min time: {:.3f} ms'.format(np.min(t)))
    plt.plot(t)
    plt.ylim([0,40])
    plt.xlabel('Frame Number')
    plt.ylabel('Frame interval (ms)')
    plt.title('Timing for every stimulation frame')
    plt.show()