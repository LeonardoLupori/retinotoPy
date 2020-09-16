import math
import numpy as np
from PIL import Image, ImageDraw

# ------------------------------------------------------------------------------
# WARPED BAR
# Class for creating a sweeping bar warped according to spherical coordinates
# ------------------------------------------------------------------------------
class WarpedBar:
    def __init__(self,
                win,
                center=0.5,
                includeBarWidth=True,
                barWidth=10,
                ori='h',
                nVert=100):
        
        # Bar Attributes
        self.center = center
        self.includeBarWidth = includeBarWidth
        self.barWidth = barWidth
        self.ori = ori
        self.nVert = nVert

        # Infos about the stim windows and the monitor for calculating parameters
        # useful for the spherical correction. This is only done at initialization
        # because it can be computationally intensive
        self._win = win

        monitor = win.monitor
        self._mon = monitor
        self._viewDist = monitor.getDistance()
        self._monSizePix = monitor.getSizePix()
        self._monWidthCm = monitor.getWidth()
        # Pixel size calibration
        self._pixSize = self._monWidthCm / self._monSizePix[0]

        # Get window coordinates in radians
        windowSizePix = self._win.size
        windowSizeCm = [x*self._pixSize for x in windowSizePix]
        self._halfWidthRad = math.atan((windowSizeCm[0]/2) / self._viewDist)
        self._halfHeightRad = math.atan((windowSizeCm[1]/2)/self._viewDist)

        # Get barwidth in radians
        self._barWidthRad = math.radians(self.barWidth)

        # Aspetc ratio of the bar
        if ori=='h':
            aspectRatio = (self._halfWidthRad*2)/self._barWidthRad
        elif ori=='v':
            aspectRatio = self._barWidthRad/(self._halfHeightRad*2)
        else:
            raise NameError('Unrecognized ori parameter. Expected "h" or "v"')

        self._numWidthPoints = round((aspectRatio*self.nVert/2) / (1+aspectRatio))
        self._numheightPoints = round((self.nVert/2) / (aspectRatio+1))


    # Return a nVert-by-2 npArray of x,y coordinates for the contours of the bar
    # in RADIANS in the cartesian space of the monitor
    # --------------------------------------------------------------------------
    def getBarCoordRadians(self):
        barCoord = self._rectangleCoord()
        return barCoord


    # Return a nVert-by-2 npArray of x,y coordinates for the contours of the bar
    # in DEGREES in the cartesian space of the monitor
    # --------------------------------------------------------------------------
    def getBarCoordDegrees(self):
        barCoord = self._rectangleCoord()
        return np.degrees(barCoord)


    # Return a nVert-by-2 npArray of x,y coordinates for the contours of the bar
    # in CENTIMETERS in the cartesian space of the monitor
    # --------------------------------------------------------------------------
    def getBarCoordCm(self):
        barCoord = self._rectangleCoord()

        barCoordCm = np.zeros(barCoord.shape)
        barCoordCm[:,0] = self._viewDist * np.tan(barCoord[:,0])
        barCoordCm[:,1] = self._viewDist / np.cos(barCoord[:,0]) * np.tan(barCoord[:,1])
        return barCoordCm


    # Return a nVert-by-2 npArray of x,y coordinates for the contours of the bar
    # in PIXELS in the cartesian space of the monitor
    # --------------------------------------------------------------------------
    def getBarCoordPix(self):
        barCoordCm = self.getBarCoordCm()
        barCoordPix = np.zeros(barCoordCm.shape)

        barCoordPix[:,0] = np.round(barCoordCm[:,0] / self._pixSize) + (self._win.size[0]/2)
        barCoordPix[:,1] = np.round(barCoordCm[:,1] / self._pixSize) + (self._win.size[1]/2)
        return barCoordPix



    # Returns a logical npArray of the same size of the parent window that has 
    # True values only inside the bar
    # --------------------------------------------------------------------------
    def getBarBinaryMask(self):
        barCoordPix = self.getBarCoordPix()

        img = Image.new('1', (int(self._win.size[0]), int(self._win.size[1])), 0)
        polygon = barCoordPix.flatten().tolist()
        ImageDraw.Draw(img).polygon(polygon, outline=1, fill=1)
        mask = np.asarray(img)
        mask = mask.astype('int')
        # mask = mask>0
        mask = (mask*2)-1
        return mask


    # Takes a grayscale image as a npArray and returns another npArray where all 
    # the pixels outsize of the bar are set to 0
    # --------------------------------------------------------------------------
    def superImposeToImg(self,img):
        mask = self.getBarBinaryMask()

        maskedImage = np.copy(img)
        maskedImage[mask==-1] = 0
        return maskedImage


    def getTextureMask(self, textRes=128):
        barCoordPix = self.getBarCoordPix()

        barCoordPix[:,0] = barCoordPix[:,0] * textRes / self._win.size[0]
        barCoordPix[:,1] = barCoordPix[:,1] * textRes / self._win.size[1]

        img = Image.new('1', (textRes,textRes), 0)
        polygon = barCoordPix.flatten().tolist()
        ImageDraw.Draw(img).polygon(polygon, outline=1, fill=1)
        mask = np.asarray(img)
        mask = mask.astype('int')
        # mask = mask>0
        textureMask = (mask*2)-1
        return textureMask


    # Internal function
    # Converts the center attribute of the bar (which is given in a 0-1 range, 
    # meaning beginning-end of screen) to a value in radians
    # --------------------------------------------------------------------------
    def _normalizedPos2rad(self, normPos):
        # Bar width inclusion
        if self.includeBarWidth:
            barSize = self._barWidthRad/2
        else:
            barSize = 0

        # Orientation of the bar
        if self.ori=='h':
            halfWinSize = self._halfHeightRad
        elif self.ori=='v':
            halfWinSize = self._halfWidthRad
        else:
            raise NameError('Unrecognized ori parameter. Expected "h" or "v"')

        # Actual calculation of the final position in radians
        posRadians = (normPos*(halfWinSize+barSize)*2) - (halfWinSize+barSize)
        return posRadians


    # Internal Function
    # Calculates an N-by-2 npArray with the x,y values in spherical coordinates 
    # of a rectangle, given the parent window, barwidth, orientation and center
    # --------------------------------------------------------------------------
    def _rectangleCoord(self):
        # Define a 2D point for the center of the bar for internal procesing
        # based on the bar orientation
        pos = self._normalizedPos2rad(self.center%1)
        if self.ori == 'h':
            center = np.array([0,pos])
            halfWidth = self._halfWidthRad
            halfHeight = self._barWidthRad/2
        elif self.ori == 'v':
            center = np.array([pos,0])
            halfWidth = self._barWidthRad/2
            halfHeight = self._halfHeightRad
        else:
            raise NameError('Unrecognized ori parameter. Expected "h" or "v"')

        # Create the rectangle vertices
        vertices = np.zeros([4,2])
        # southwest
        vertices[0,:] = [center[0]-(halfWidth), center[1]-(halfHeight)]
        # northwest
        vertices[1,:] = [center[0]-(halfWidth), center[1]+(halfHeight)]
        # northeast
        vertices[2,:] = [center[0]+(halfWidth), center[1]+(halfHeight)]
        # southeast
        vertices[3,:] = [center[0]+(halfWidth), center[1]-(halfHeight)]

        # The actual output 2D array of coordinates in spherical units
        rectSphcoord = np.concatenate((
            np.linspace(vertices[0,:],vertices[1,:],self._numheightPoints),
            np.linspace(vertices[1,:],vertices[2,:],self._numWidthPoints),
            np.linspace(vertices[2,:],vertices[3,:],self._numheightPoints),
            np.linspace(vertices[3,:],vertices[0,:],self._numWidthPoints),
            ), axis=0)
        return rectSphcoord



# ------------------------------------------------------------------------------
# WARPED GRATING
# Class for creating an horizontal, vertical or checkerboard grating 
# ------------------------------------------------------------------------------
class warpedGrating:
    def __init__(self,
                win,
                sf=1.0,
                ori='h',
                waveform='sqr',
                phase=0.0):
        
        # Attributes from the initialization
        self.win = win
        self.sf = sf
        self.ori = ori
        self.waveform = waveform
        self.phase = phase

        # Convert spatial frequency from Cyc/deg to Cyc/rad
        self.sfRad = self.sf * (360/(2*math.pi))

        # Convert the phase from [0:1] to 0:2pi
        phase = phase*math.pi*2

        # Infos about the stim windows and the monitor for calculating parameters
        # useful for the spherical correction. This is only done at initialization
        # because it can be computationally intensive
        self._win = win

        monitor = win.monitor
        self._mon = monitor
        self._viewDist = monitor.getDistance()
        self._monSizePix = monitor.getSizePix()
        self._monWidthCm = monitor.getWidth()
        # Pixel size calibration
        self._pixSize = self._monWidthCm / self._monSizePix[0]

        # Get window coordinates in radians
        windowSizePix = self._win.size
        self._windowSizeCm = [x*self._pixSize for x in windowSizePix]
        self._halfWidthRad = math.atan((self._windowSizeCm[0]/2) / self._viewDist)
        self._halfHeightRad = math.atan((self._windowSizeCm[1]/2)/self._viewDist)
        


    # Internal Function
    # Converts the coordinate of a pixel in cm
    # --------------------------------------------------------------------------
    def _pix2Cm(self,pixel, totalPixSize):
         # Center the value to get 0 in the center of the screen
        centeredPixel = (pixel) - (totalPixSize-1)/2

        cm = centeredPixel*self._pixSize
        return cm



    # Creates a square texture of a given resolution such that when it will be
    # used as a text in a GratingStim and streched to the full resolution of the
    # window, things will appear normal
    # --------------------------------------------------------------------------
    def createTexture(self,textRes=128):
        texture = np.zeros((textRes,textRes))

        # Convert the phase from [0:1] to 0:2pi
        phase = self.phase*math.pi*2

        for x in range(textRes):
            for y in range(textRes):
                # Center and normalize the pixel coordinates. The end result are
                # values from -0.5 to 0.5
                normX = x  / (textRes-1)
                normY = y  / (textRes-1)
                normX = normX - 0.5
                normY = normY - 0.5

                # Get the position in cm of where the pixels are gonna be in the 
                # final stimulus
                cmX = normX * self._windowSizeCm[0]
                cmY = normY * self._windowSizeCm[1]

                phi = math.atan(cmX/self._viewDist)
                teta = math.atan(cmY/self._viewDist * math.cos(phi))

                if self.ori=='v':
                    texture[y,x] = math.sin(2 * math.pi * self.sfRad * phi + phase)
                elif self.ori=='h':
                    texture[y,x] = math.sin(2 * math.pi * self.sfRad * teta + phase)
                elif self.ori=='hv' or self.ori == 'vh':
                    s_v = math.sin(2 * math.pi * self.sfRad * phi + phase)
                    s_h = math.sin(2 * math.pi * self.sfRad * teta)
                    texture[y,x] = s_v * s_h
                else:
                    raise NameError('Unrecognized ori parameter. Expected "h", "v" or "hv"')

        # Convert the stimulus to square wave      
        if self.waveform == 'sqr':
            texture[texture>=0] = 1
            texture[texture<0] = -1

        return texture


    # Creates a full image (same resolution as the window) as an npArray (-1:black
    # 1:white). Can be very slow (few seconds)
    # --------------------------------------------------------------------------
    def createStimulus(self):

        stimSize = self._win.size
        stim = np.zeros((stimSize[1],stimSize[0]))

        # Convert the phase from [0:1] to 0:2pi
        phase = self.phase*math.pi*2

        # Calculates the stimulus Pixel By Pixel
        for x in range(stimSize[0]):
            for y in range(stimSize[1]):
                # Get the (y,z) position of the pixel in cm relative to the center
                # 0 is the midline (center of the screen), values above or to the 
                # right of the midline are positive. Values below or to the left of
                # the midline are negative
                xCm = self._pix2Cm(x,self._win.size[0])
                yCm = self._pix2Cm(y,self._win.size[1])

                # Convert spherical coordinates (viewDistCm, phi, teta) in
                # cartesian coordinates on the monitor plane (y,z)
                phi = math.atan(xCm/self._viewDist)
                teta = math.atan(yCm/self._viewDist * math.cos(phi))

                if self.ori=='v':
                    stim[y,x] = math.sin(2 * math.pi * self.sfRad * phi + phase)
                elif self.ori=='h':
                    stim[y,x] = math.sin(2 * math.pi * self.sfRad * teta + phase)
                elif self.ori=='hv' or self.ori == 'vh':
                    s_v = math.sin(2 * math.pi * self.sfRad * phi + phase)
                    s_h = math.sin(2 * math.pi * self.sfRad * teta + phase)
                    stim[y,x] = s_v * s_h
                else:
                    raise NameError('Unrecognized ori parameter. Expected "h", "v" or "hv"')

        # Convert the stimulus to square wave      
        if self.waveform == 'sqr':
            stim[stim>=0] = 1
            stim[stim<0] = -1
        
        return stim




# ------------------------------------------------------------------------------
# MAIN - For testing purposes
# ------------------------------------------------------------------------------

if __name__ == "__main__":

    from timeit import default_timer as timer
    from psychopy import visual, monitors
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    # --------------------------------
    enableBar = True
    nFrames = 120
    # --------------------------------

    stimWin = visual.Window([800,500],
        monitor='tryMonitor',
        )
    
    # Initialize a warped stimulus
    WarpG = warpedGrating(stimWin,
                            sf=1,
                            ori='vh',
                            waveform='sqr',
                            phase=0)

    if enableBar:
        # Initialize a warped bar object
        warpBar = WarpedBar(stimWin,
                        center=0.8,
                        ori='v',
                        barWidth=2,
                        includeBarWidth=True,
                        nVert=200)
        # Superimpose the bar to the grating image 
        stimulus = warpBar.superImposeToImg(WarpG.stim)
        warpBar.getBarBinaryMask()
    else:
        stimulus = WarpG.stim

    # Initialize the Image that will be used as a stimulus
    imStim = visual.ImageStim(stimWin,
                            image=stimulus,
                            units='pix',
                            size=stimWin.size)


    for i in range(nFrames):
        imStim.draw()
        stimWin.flip()