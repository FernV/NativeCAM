To setup your current system to use NativeCAM you need do the following

Copy the lines from a ini file that closely matches your system either
		axis
		gmoccapy
	and
		mill
		lathe
		plasma

from configs/sim/axis/ncam_demo or configs/sim/gmoccapy/ncam_demo directories
	
The lines are marked with
#******** required 'NativeCAM' items
and are in [RS274NGC] and [DISPLAY] sections

You can omit : -U --catalog='your choice of catalog'
it is not required anymore

Copy ncam.ui into the same directory as your ini file
OR you can specify the relative path to that file like
	../../ncam.ui
	(be aware that gmoccapy does not support reference by ~/)
or the absolute path

NativeCAM will use the tool table specified in your ini file