clearvars, clc
retinotoPy_fullPath = 'C:\Users\Leonardo\Documents\MATLAB\retinotoPy';

%% Startup

addpath(genpath(retinotoPy_fullPath));

fprintf('RetinotoPy starting...')
% Load the experiment settings defined in the file "generalSettings.m"
generalSettings
fprintf('\t Settings loaded successfully...\n')


%% Connect to the camera and initialize it

fprintf('*** CAMERA CONNECTION ***\n')

% Check whether the camera adaptor selected in the settings is installed
fprintf(['Checking camera adaptor "' settings.camera.adaptor '"...'])
info = imaqhwinfo;
if ismember(settings.camera.adaptor, info.InstalledAdaptors)
    fprintf(' found. \n')
else
    fprintf(' not found. Aborting the experiment \n')
    return
end

% Check whether the format selected in the settings is valid
fprintf('Checking camera format...')
info = imaqhwinfo(settings.camera.adaptor);
if ismember(settings.camera.format, info.DeviceInfo.SupportedFormats)
    fprintf([' selected format: ' settings.camera.format '\n'])
else
    fprintf(' not found. Aborting the experiment\n')
    return
end

% Try to connect to the camera
fprintf('Connecting to the camera [deviceID #%u]...', settings.camera.deviceID)
try
    vid = videoinput('pointgrey', settings.camera.deviceID , 'F7_Mono12_320x240_Mode5');
    src = getselectedsource(vid);
    fprintf(' Connected.\n')
catch me
    fprintf(' Failed. Aborting the experiment\n')
    return
end

% Setup the Camera acquisition parameters
fprintf('Setting up the camera acquisition settings...')
% -----------------------
% Brightness
if isnan(settings.camera.Brightness)
    tmp = propinfo(src,'Brightness');
    src.Brightness = tmp.ConstraintValue(1);    % Set minimum brightness level
else
    src.Brightness = settings.camera.Brightness;
end
% Exposure
src.ExposureMode = settings.camera.ExposureMode;
% Gamma
src.GammaMode = settings.camera.GammaMode;
% Sharpness
src.SharpnessMode = settings.camera.SharpnessMode;
% Framerate
src.FrameRateMode = settings.camera.FrameRateMode;
if isnan(settings.camera.FrameRate)
    tmp = propinfo(src,'FrameRate');
    src.FrameRate = tmp.DefaultValue;       % Set default Framerate
    settings.camera.FrameRate = tmp.DefaultValue;
else
    src.FrameRate = settings.camera.FrameRate;
end
% Gain
src.GainMode = settings.camera.gainMode;
if isnan(settings.camera.Gain)
    tmp = propinfo(src,'Gain');
    src.Gain = tmp.DefaultValue;            % Set default Gain
    settings.camera.Gain = tmp.DefaultValue; 
else
    src.Gain = settings.camera.Gain;
end
% ShutterSpeed
src.ShutterMode = settings.camera.ShutterMode;
if isnan(settings.camera.Shutter)
    tmp = propinfo(src,'Shutter');
    src.Shutter = tmp.DefaultValue;
    settings.camera.Shutter = tmp.DefaultValue;
else
    src.Shutter = settings.camera.Shutter;
end

fprintf(' done\n')


%% Setup TCP/IP connection with the psychopy instance on localhost

fprintf('*** TCP/IP CONNECTION ***\n')

fprintf(['Starting TCP/IP server on [Address: ' settings.tcp.address...
    ' - Port: %u]...'], settings.tcp.port)

try
    tcp = tcpip(settings.tcp.address, settings.tcp.port, 'NetworkRole', 'server');
    fprintf(' started.\n')
catch me
    fprintf(' failed.  Aborting the experiment \n')
end

set(tcp, 'InputBufferSize', settings.tcp.bufferSize);
fprintf('Waiting for connection to Psychopy client...')
fopen(tcp);
pause(0.2);         % Delay to prepare for operations after the initial handshake
fprintf(' connected.\n\n')


%% Preview Camera and adjust acquisition parameters

cameraPreview(vid,src,settings)

%% Cleanup

% Clean TCP/IP communication
if exist('tcp','var') && strcmpi(tcp.Status,'open')
    fclose(tcp);
    fprintf('TCP/IP closed.\n')
else
    fprintf('TCP/IP was already properly closed.\n')
end

% Clean Camera connection 
if exist('vid','var') && isvalid(vid)
    delete(vid);
    fprintf('Camera videoinput object deleted.\n')
else
    fprintf('Camea connection was already properly closed.\n')
end





