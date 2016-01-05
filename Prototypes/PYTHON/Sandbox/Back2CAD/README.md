#Back2CAD

This folder is for all development on the conversion of output data of Peters' scheme (mainly control points and patch distribution) to a standartd CAD format (```.step``` or ```.iges```).

##How to run
We are heavily relying on the **FreeCAD API**. Therefore you first have to install FreeCAD via ```apt-get install freecad```. Then you have to run our scripts either 

- directly from the FreeCAD python interpreter via ```/usr/bin/freecadcmd``` or
- copy the FreeCAD sourcecode directly into this folder and run the script from an arbitrary python interpreter. The sourcecode can be found at ```/usr/lib/freecad/Mod``` and should be copied into a folder named ```FreeCAD```.