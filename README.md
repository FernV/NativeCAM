NativeCAM for LinuxCNC - realtime CAM

WARNING : NEVER USE A SUPERUSER TERMINAL FOR INSTALLING LINUXCNC OR NATIVECAM
   YOU MAY HAVE NO WRITE PERMISSIONS TO FILES OR SUB-DIRECTORIES
   USE A REGULAR USER TERMINAL AND PREFIX WITH 'SUDO' ONLY WHEN REQUIRED

Prefer cloning over downloading.

Important files are catalogs/customize and catalogs/translating

NativeCAM as a deb package will be supplied with next stable release of LinuxCNC (2.9)
It will be automatically updated after changes are published.
In the meantime, it is available with the pre-release version. However you can use it
as a non-deb with the following instructions.
Follow them EXACTLY for immediate no-pain success.

Pre-requisite is python-lxml package installed.
If not install with 'sudo apt-get install python-lxml'

-Open a normal user terminal window in your home directory.
-Clone with : git clone https://github.com/FernV/NativeCAM.git
-Change directory to NativeCAM : cd NativeCAM
-Type : ./ncam.py -h

1.	Stand alone mode
--------------------------------------------------------------------------------
1.	Using the command : ./ncam.py  will create and use ~/nativecam directory
	and copy support files and links in the sub-directory ncam
	However it is not meant to be usefull unless LinuxCNC
	was/is loaded with the right SUBROUTINE_PATH except to
	explore it's features
	
	
2.	Embedded (non deb setup)
--------------------------------------------------------------------------------
1.	Run first from ncam directory : sudo ./nondeb_setup.py
	You WILL have to redo it after LinuxCNC updates
	
2.	To use with your own inifile, it must first be edited.
	Using the command : ./ncam.py -i(inifilename) -c('mill' | 'plasma' | 'lathe')
	will automatically create a backup and modify your file.
	It will also prepare the sub-directory with needed files and links.
    If you use axis and -t option it will be embedded in a tab
	
2.	Start LinuxCNC normally with this commands :
	linuxcnc inifilename
	
	Open an example project
	
	
3.	Tutorials
--------------------------------------------------------------------------------
1.	Use menu help->NativeCAM on YouTube
	
	or follow this link
		
	https://www.youtube.com/channel/UCjOe4VxKL86HyVrshTmiUBQ
	
	
4.	Translation
--------------------------------------------------------------------------------
	Available French (fr) and German (de)
	

