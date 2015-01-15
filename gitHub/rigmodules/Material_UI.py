import maya.cmds as cmds
from functools import partial
from string import *
import re, os, subprocess, sys
import maya.mel
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons License'
'http://creativecommons.org/licenses/by-sa/3.0/au/'

photoshop = r"C:\\Program Files\\Adobe\\Adobe Photoshop CC 2014\\Photoshop.exe"
gimp="C:\\Program Files\\GIMP 2\\bin\\gimp-2.8.exe"
getScenePath=cmds.file(q=1, location=1)
getPathSplit=getScenePath.split("/")
folderPath='\\'.join(getPathSplit[:-1])+"\\"


import Tools
reload (Tools)
toolClass=Tools.ToolFunctions()

class Mat_Namer(object):
    '''--------------------------------------------------------------------------------------------------------------------------------------
    Interface Layout
    --------------------------------------------------------------------------------------------------------------------------------------'''          
    def __init__(self, winName="Material ID"):
        self.winTitle = "MaterialID"
        self.winName = winName
    def create_MATID_win(self, winName="MaterialID"):
        global colMenu
        if cmds.window(self.winName, exists=True):
                cmds.deleteUI(self.winName)

        self.window = cmds.window(self.winName, title=self.winTitle, tbm=1, w=300, h=250 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=300)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        
        cmds.rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))
        colMenu=cmds.optionMenu( label='ID')
        cmds.menuItem( label='Skin' )
        cmds.menuItem( label='Eye' )
        cmds.menuItem( label='Spec' )
        cmds.menuItem( label='Lash' )
        cmds.menuItem( label='Brows' )    
        cmds.menuItem( label='Hair' )        
        cmds.menuItem( label='Mouth' )        
        cmds.menuItem( label='Other' )    
        cmds.menuItem( label='Costume' )             
        cmds.button (label='Mat ID', p='listBuildButtonLayout', command =lambda *args:self._add_id(queryColor=cmds.optionMenu(colMenu, q=1, sl=1)))
        cmds.button (label='Add CH Pref', p='listBuildButtonLayout', command = self._add_pref)
        cmds.button (label='Add type Suf', p='listBuildButtonLayout', command = self._add_suf)
        cmds.button (label='ShadeNetworkSel', p='listBuildButtonLayout', command = self._shade_network)
        cmds.button (label='selectMissingID', p='listBuildButtonLayout', command = self._select_nonID)
        cmds.button (label='vray gamma', p='listBuildButtonLayout', command = self._vray_gamma)     
        cmds.button (label='FTM', p='listBuildButtonLayout', command = self._file_texture_manager)     
        cmds.button (label='Open work folder', p='listBuildButtonLayout', command = self._open_work_folder) 
        cmds.button (label='Open texture folder', p='listBuildButtonLayout', command = self._open_texture_folder)   
        cmds.button (label='Open Image in PS', p='listBuildButtonLayout', command = self._open_texture_file_ps)  
        cmds.button (label='Open Image in Gimp', p='listBuildButtonLayout', command = self._open_texture_file_gmp) 

        cmds.showWindow(self.window)
    def _file_texture_manager(self, arg=None):
        maya.mel.eval( "FileTextureManager;" )
        
    def _open_texture_file_ps(self, arg=None):
        toolClass._open_texture_file_ps()
        
    def _open_texture_folder(self, arg=None):
        toolClass._open_texture_folder()
        
    def _open_work_folder(self, arg=None):
        toolClass._open_work_folder()
           
    def _open_texture_file_gmp(self, arg=None):
        toolClass._open_texture_file_gmp()
        
    def _add_id(self, queryColor):
        toolClass._add_id(queryColor)

            
    def _vray_gamma(self, arg=None):
        toolClass._vray_gamma() 

    def _add_suf(self, arg=None):
        toolClass._add_suf()
                
                
    def _shade_network(self, arg=None):
        toolClass._shade_network()

            
    def _add_pref(self, arg=None):
        toolClass._add_pref()
        
    def _select_nonID(self, arg=None):
        toolClass._select_nonID()


inst = Mat_Namer()
inst.create_MATID_win()
