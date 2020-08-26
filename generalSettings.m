% -------------------------------------------------------------------------
% BLACKFLY CAMERA SETTINGS
% -------------------------------------------------------------------------
% if NaN, the default values ar going to be set

settings.camera.adaptor = 'pointgrey';                  % AdaptorName. See the folder camera_support for installing the adaptor
settings.camera.deviceID = 1;                           % In case there are multiple cameras
settings.camera.format = 'F7_Mono12_320x240_Mode5';     % Acquisition format (1x1, 2x2,4x4 binning; various bit-depth)
% **********************************
%       AVAILABLE FORMATS
% 
%     {'F7_Mono12_1288x964_Mode0'}
%     {'F7_Mono12_320x240_Mode5' }
%     {'F7_Mono12_644x482_Mode1' }
%     {'F7_Mono16_1288x964_Mode0'}
%     {'F7_Mono16_320x240_Mode5' }
%     {'F7_Mono16_644x482_Mode1' }
%     {'F7_Mono8_1288x964_Mode0' }
%     {'F7_Mono8_320x240_Mode5'  }
%     {'F7_Mono8_644x482_Mode1'  }
% **********************************

settings.camera.Brightness = NaN;                   % Adjust the black level of the camera
settings.camera.ExposureMode = 'off';               % Automatic exposure level
settings.camera.GammaMode = 'off';                  % Gamma correction for display
settings.camera.SharpnessMode = 'off';              % Postprocessing for increased sharpness
settings.camera.FrameRateMode = 'Manual';           % 'Manual' or 'Auto'
settings.camera.ShutterMode = 'Manual';             % 'Manual' or 'Auto'
settings.camera.gainMode = 'Manual';                % 'Manual' or 'Auto'

settings.camera.TriggerMode = 'Manual';             % 'immediate', 'manual' or 'hardware'
settings.camera.TriggerCondition = 'risingEdge';    % Only if mode = hardware 'risingEdge' or 'fallingEdge'
settings.camera.TriggerSource = 'externalTriggerMode0-Source0';
% **********************************
%       AVAILABLE SOURCES
% 
%     'externalTriggerMode0-Source0'                Standard External Trigger 
%     'externalTriggerMode1-Source0'                Bulb Shutter Trigger
%     'externalTriggerMode13-Source0'               Low Smear Trigger
%     'externalTriggerMode14-Source0'               Overlapped Exposure Readout Trigger 
%     'externalTriggerMode15-Source0'               Multi-Shot Trigger
% **********************************

settings.camera.FrameRate = NaN;                    % Rate of acquisition (Hz)
settings.camera.Gain = NaN;                         % Gain level in the range [0   23.9905
settings.camera.Shutter = NaN;                      % in MATLAB I could not get the shutter value
settings.camera.confidenceMargin = 2;               % Additional time in ms for data transfer to image buffer
% (exposure time) to be constained by the selected framerate and vice vera,
% so for this reason these two parameters need to be adjusted explicitly
% here in MATLAB so that 1/framerate > shutter + confidenceMargin.
% A confidenceMargin of a few milliseconds is added to allow for data
% transfer to the image buffer

% -------------------------------------------------------------------------
% GRATING STIMULUS SETTINGS
% -------------------------------------------------------------------------
settings.gratingStim.rows = 2;
settings.gratingStim.columns = 4;
settings.gratingStim.spFreq = 0.03;
settings.gratingStim.tempFreq = 2;
settings.gratingStim.dist = 30;
settings.gratingStim.ori = 0;

% -------------------------------------------------------------------------
% CONTINOUS BAR STIMULUS SETTINGS
% -------------------------------------------------------------------------
settings.barStim.ori = 0;
settings.barStim.width = 5;
settings.barStim.tempFreq = 10;
settings.barStim.checkerboardSpFreq = 0.5;
settings.barStim.checkerboardtempFreq = 2;
settings.barStim.dist = 30;                     % in cm

% -------------------------------------------------------------------------
% EXPERIMENT SETTINGS
% -------------------------------------------------------------------------
settings.repetitions = 20;
settings.preStim = 1;                           % in seconds
settings.postStim = 5;                          % in seconds
settings.interStim = 5;                         % in seconds

% Folder where to save the result of the experiments
settings.savingFolder = 'C:\Users\Leonardo\Documents\';

% -------------------------------------------------------------------------
% TCP/IP SETTINGS
% -------------------------------------------------------------------------
settings.tcp.address = 'localhost';
settings.tcp.port = 80;
settings.tcp.role = 'server';
settings.tcp.bufferSize = 4096;
settings.tcp.connTimeout = 60;




