NativeCAM for LinuxCNC - realtime CAM

This is reading for any installer but if you are a 
	linuxcnc developper you should also read README-DEV


Clone or extract in a ~/sub-directory of your choice with read/write rights

Open a terminal window in the same directory

Make sure these files are executabbes :
	ncam.py
	uninstall-features (to restore the modified files after you delete the old version)
		
You need to install python-lxml if not allready installed, the command is :
	sudo apt-get install python-lxml


1.	Simple usage - Stand alone mode
--------------------------------------------------------------------------------
1.	 Copy then paste one of these commands :
	
	./ncam.py -iconfigs/sim/axis/ncam_demo/mill.ini
	./ncam.py -iconfigs/sim/axis/ncam_demo/mill-mm.ini
	./ncam.py -iconfigs/sim/gmoccapy/ncam_demo/mill.ini
	./ncam.py -iconfigs/sim/gmoccapy/ncam_demo/mill-mm.ini

	However it is not meant to be usefull stand alone unless LinuxCNC
		was/is loaded with the right SUBROUTINE_PATH


2.	Best way - Run embedded
--------------------------------------------------------------------------------
1.	Issue / copy then paste the following command
	
	sudo python setup.py
	
	This will create required links and modify files.
	You do not do this more than once except maybe after lcnc updates
	because it will replace the files and erase the link,
	until NativeCAM is integrated in the distribution
	To restore the system, simply issue the command : 'sudo python setup.py c'

2.	Start LinuxCNC with one of these commands (copy/paste) :

	linuxcnc configs/sim/axis/ncam_demo/mill.ini
	linuxcnc configs/sim/axis/ncam_demo/mill-mm.ini
	linuxcnc configs/sim/gmoccapy/ncam_demo/mill.ini
	linuxcnc configs/sim/gmoccapy/ncam_demo/mill-mm.ini

3.	Open a project in the examples directory
	
	Basic spacer.xml
	Fun wheel demo.xml

4.	Open one of those ini files to learn how to setup your own system
	Note that you need ncam.ui in the same directory as the ini file
	
	
3.	Tutorials
--------------------------------------------------------------------------------
1.	Use menu help->NativeCAM on YouTube
	
	or follow this link
		
	https://www.youtube.com/channel/UCjOe4VxKL86HyVrshTmiUBQ


4.	Translation
--------------------------------------------------------------------------------
1.	Still needs some development. Will follow.
