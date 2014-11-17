import maya.cmds as cmds
from functools import partial
from string import *
import re
import maya.mel

'''MG rigging modules'''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons License'
'http://creativecommons.org/licenses/by-sa/3.0/au/'


class ColourPalet(object):
    '''--------------------------------------------------------------------------------------------------------------------------------------
    Interface Layout
    --------------------------------------------------------------------------------------------------------------------------------------'''          
    def __init__(self, winName="Colours"):
        self.winTitle = "Colours"
        self.winName = winName

    def create_colour_window(self, winName="Colors"):
        global colMenu
        if cmds.window(self.winName, exists=True):
                cmds.deleteUI(self.winName)

        self.window = cmds.window(self.winName, title=self.winTitle, tbm=1, w=150, h=100 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=150)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        
        cmds.rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(100, 20))
        colMenu=cmds.optionMenu( label='Colors')
        cmds.menuItem( label='Red' )
        cmds.menuItem( label='Blue' )
        cmds.menuItem( label='Green' )
        cmds.menuItem( label='Yellow' )
        cmds.menuItem( label='DarkYellow' )    
        cmds.menuItem( label='ForestGreen' )        
        cmds.menuItem( label='DarkRed' )        
        cmds.menuItem( label='Maroon' )    
        cmds.menuItem( label='Torquise' )             
        cmds.button (label='Change Selection', p='listBuildButtonLayout', command = self._change_colour)
        cmds.showWindow(self.window)

    def _change_colour(self, arg=None):
        '''----------------------------------------------------------------------------------
        Common add to list function
        ----------------------------------------------------------------------------------'''  
        queryColor=cmds.optionMenu(colMenu, q=1, sl=1)
        getSel=cmds.ls(sl=1)
        if queryColor==1:
            color=13          
        elif queryColor==2:
            color=6   
        elif queryColor==3:
            color=14
        elif queryColor==4:
            color=22
        elif queryColor==5:
            color=25
        elif queryColor==6:
            color=23    
        elif queryColor==7:
            color=4
        elif queryColor==8:
            color=31
        elif queryColor==9:
            color=28          
        for each in getSel:
            cmds.setAttr(each+".overrideEnabled", 1)
            cmds.setAttr(each+".overrideColor", color)            
            
inst = ColourPalet()
inst.create_colour_window()