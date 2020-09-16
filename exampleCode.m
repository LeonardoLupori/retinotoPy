% Information on the available adaptors. The adaptor "pointgrey" should
% show up here in the printed list.
imaqhwinfo


% If the 'pointgrey' adaptor is present then this commands will print some
% useful information about the device ID and the supported recording
% formats.
%
% Mode 0: Full resolution
% Mode 1: 2x2 binning (increase in framerate and brightness)
% Mode 5: 4x4 binning (increase in framerate and brightness)
camInfo = imaqhwinfo('pointgrey');
disp(camInfo.DeviceInfo.SupportedFormats')

%% Actually load the camera

% Loads the camera with a 4x4 binning in order to maximize framerate and
% brightness
vid = videoinput('pointgrey', 1, 'F7_Mono12_320x240_Mode5');
src = getselectedsource(vid);


%%
vid.FramesPerTrigger = 1;
vid.timeout;
vid.VideoResolution
vid.FramesAcquired
vid.FramesAvailable
triggerconfig(vid, 'manual')
%%

% Disable useless automatic image adjustments and enhancements
% -----------------------
% Brightness
tmp = propinfo(src,'Brightness');
src.Brightness = tmp.ConstraintValue(1);    % Set minimum brightness level
% Exposure
src.ExposureMode = 'off';
% Gamma
src.GammaMode = 'off';
% Sharpness
src.SharpnessMode = 'off';
% -----------------------

% Set to the default the relevant image parameters
% -----------------------
% Framerate
src.FrameRateMode = 'Manual';
tmp = propinfo(src,'FrameRate');
% limits = tmp.ConstraintValue;
src.FrameRate = tmp.DefaultValue;
% Gain
src.GainMode = 'Manual';
tmp = propinfo(src,'Gain');
% limits = tmp.ConstraintValue;
src.Gain = tmp.DefaultValue;
% ShutterSpeed
src.ShutterMode = 'Manual';
tmp = propinfo(src,'Shutter');
% limits = tmp.ConstraintValue;
src.Shutter = tmp.DefaultValue;
% -----------------------



%% Capture and display Images

start(vid)





