NativeCAM for LinuxCNC - realtime CAM

NativeCAM is now a deb package supplied with LinuxCNC meaning it can
be automatically updated after changes are published
(if not released yet, it is a matter of days)

Open a terminal window and type : ncam -h

1.	Stand alone mode
--------------------------------------------------------------------------------
1.	Using the command : ncam  will create and use ~/nativecam directory
	and copy all support files in the sub-directory ncam
	However it is not meant to be usefull unless LinuxCNC
	was/is loaded with the right SUBROUTINE_PATH except to
	explore it's features
	
	
2.	Embedded
--------------------------------------------------------------------------------
1.	To use with your own inifile, you MUST first edit the file.
	Using the command : ncam -i(inifilename) -c('mill' | 'plasma' | 'lathe')
	will automatically create a backup and modify your file.
	
2.	Start LinuxCNC normally with this commands :
	linuxcnc inifilename
	
	Open a project in the examples directory
	
	
3.	Tutorials
--------------------------------------------------------------------------------
1.	Use menu help->NativeCAM on YouTube
	
	or follow this link
		
	https://www.youtube.com/channel/UCjOe4VxKL86HyVrshTmiUBQ
	
	
4.	Translation
--------------------------------------------------------------------------------
1.	Under development
	

