NativeCAM for LinuxCNC - realtime CAM

NativeCAM as a deb package can now be used with new stable release of LinuxCNC (2.7.9)
It will be automatically updated after changes are published.

DO NOT USE AS A NONDEB_SETUP ANYMORE

Pre-requisite is python-lxml package installed.
If not install with 'sudo apt-get install python-lxml'

-Open a normal user terminal window.
-Copy this command :
	curl -s https://packagecloud.io/install/repositories/FernV/NativeCAM/script.deb.sh | sudo bash
	and enter pwd when asked
-Copy this command :
	sudo apt-get install nativecam
	and enter pwd when asked
You are done


Type : ncam -h
Important readme files are catalogs/customize and catalogs/translating


1.	Stand alone mode
--------------------------------------------------------------------------------
1.	Using the command : 'ncam' will create and use ~/nativecam directory
	and copy support files and links in the sub-directory ncam
	However it is not meant to be usefull unless LinuxCNC
	was/is loaded with the right SUBROUTINE_PATH except to
	explore it's features
	
	
2.	Embedded
--------------------------------------------------------------------------------
1.	Use with any of the supplied example from LinuxCNC Configuration Selector
	
2.	To use with your own inifile, it must first be edited.
	From a normal user terminal, change directory to the one that contains your inifile
	Using the command : ncam -i(inifilename) -c('mill' | 'plasma' | 'lathe')
	will automatically create a backup and modify your file.
	It will also prepare the sub-directory with needed files and links.
    If you use axis and -t option it will be embedded in a tab
	
3.	Start LinuxCNC normally with this command :
	linuxcnc inifilename
	
4.	Open an example project
	
	
3.	Tutorials
--------------------------------------------------------------------------------
1.	Use menu help->NativeCAM on YouTube
	
	or follow this link
		
	https://www.youtube.com/channel/UCjOe4VxKL86HyVrshTmiUBQ
	
	
4.	Translation
--------------------------------------------------------------------------------
	Available French (fr) and German (de)
	

