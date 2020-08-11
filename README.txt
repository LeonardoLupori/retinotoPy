INSTRUCTIONS ON HOW TO READ THE BLACKFLY BFLY-U3-13S2M CAMERA

----------------------------------------------------------------------
This instruction list works with MATLAB 2019a by installing the 
FlyCap v2.11 sdk (later versions or the Spinnaker SDK are not proven 
to work). Make sure there are no other version of FlyCap installed on
your machine. After this procedure, the pointgray-1 adaptor should
show up in your Hardware Browser in imaqtool.


The .zip folder with the code and files required can be downloaded from
these 2 sources. There are version fro 2018b and 2019a but I tested
only the 2019a version. In case the link become dead I also included
these .zip folders here.

2019a version:
https://flir.app.box.com/s/1kces8va7p64u419ya7ks39tl5laiwn1
2018b version:
https://flir.app.box.com/s/ih7wtx104htmhr9kdfkymb0b51w3g2tm
----------------------------------------------------------------------


1 -Make sure there are no other versions of FlyCap installed on your 
machine

2 -Download the folder from: https://flir.app.box.com/s/1kces8va7p64u419ya7ks39tl5laiwn1
You should also find the required files locally in this repository in
a .zip file in case the link will die.

3 -Extract in your location of choice

4 -Installation (this steps are also explained in better detail in the
README file inside the .zip folder. The "Interactive installer" method
that I report here worked for me. 
	
	From the README file:
	
	The interactive installer will start MATLAB and then the installer 
	in a separate window. The executable takes a single argument; 
	the path to the location of the previously downloaded files. All 
	available support packages in the specified download folder are presented.
	
	In a command prompt (e.g., windows powershell), type the following:
	
	cd DRIVE:\<MATLAB_PATH>\bin\win64
	install_supportsoftware.exe -archives <path_to_download_folder> [-matlabroot DRIVE:\MATLAB_PATH]

	For example:

	cd C:\MATLAB\R2018b\bin\win64
	install_supportsoftware.exe -archives C:\Users\jsmith\Downloads\MathWorks\SupportPackages\R2018b\
	
5 -Restart the computer and you should be able to read the camera from
imaqtool 


----------------------------------------------------------------------
INSTRUCTIONS FOR 2020a
----------------------------------------------------------------------

1 -Make sure there are no other FlyCap drivers installed.

2 -From the 'Get Add-Ons' menu search for MATLAB support for point grey 
cameras (official release from the matlab team)

3 -Install the Add-On. It should automatically install also the correct version
of the FlyCap SDK (v.2.11). If there are problems, you can download the 
correct version here:
https://flir.app.box.com/s/2dk4t2d6jinsfdqisbtu0m5fvc3g9fh1

