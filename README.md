NativeCAM for LinuxCNC - realtime CAM

Prefer cloning over downloading.

This release is a major update and will change the directory structure.
Instead of copying everything, it will copy only files you may want to edit
and lib, cfg, graphics will be links to original files.
This will prevent redundancy and protect your edited files from being
overwritten.

Important files are catalogs/customize and catalogs/translating

NativeCAM is now a deb package supplied with LinuxCNC meaning it can
be automatically updated after changes are published
(if not released yet, be patient)

Open a terminal window in the cloned directory and type : ./ncam.py -h

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
	You may have to redo it after LinuxCNC updates
	
2.	To use with your own inifile, it must first be edited.
	Using the command : ./ncam.py -i(inifilename) -c('mill' | 'plasma' | 'lathe')
	will automatically create a backup and modify your file.
	It will also prepare the sub-directory with needed files and links.
	
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
	

