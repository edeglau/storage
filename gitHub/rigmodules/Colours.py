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

        self.window = cmds.window(self.winName, title=self.winTitle, tbm=1, w=300, h=100 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=150)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        
        cmds.rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))
        colMenu=cmds.optionMenu( label='Colors', w=150)
        cmds.menuItem( label='Bright Red' )#1
        cmds.menuItem( label='Bright Blue' )#2
        cmds.menuItem( label='Bright Green' )#3
        cmds.menuItem( label='Bright Yellow' )#4
        cmds.menuItem( label='Dark Yellow' )#5    
        cmds.menuItem( label='Dark Green' )#6     
        cmds.menuItem( label='Dark Red' )#7    
        cmds.menuItem( label='Maroon' )#8
        cmds.menuItem( label='Torquise' )#9             
        cmds.menuItem( label='Light Pink' )  
        cmds.menuItem( label='Skin' )         
        cmds.menuItem( label='Light Brown' )
        cmds.menuItem( label='Forest Green' )
        cmds.menuItem( label='Teal Green' )
        cmds.menuItem( label='Purple' )
        cmds.menuItem( label='Light Blue' )
        cmds.menuItem( label='Dark Blue' )
        cmds.menuItem( label='Darkest Blue' )
        cmds.menuItem( label='Brown' )
        cmds.button (label='Change Selection', w=150, p='listBuildButtonLayout', command = self._change_colour)
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
            color=25#Dark Yellow
        elif queryColor==6:
            color=23#Dark Green
        elif queryColor==7:
            color=4#Dark Red
        elif queryColor==8:
            color=31
        elif queryColor==9:
            color=28#Sky Blue    
        elif queryColor==10:
            color=20#Pink
        elif queryColor==11:
            color=21#Orange       
        elif queryColor==12:
            color=24#LBrown
        elif queryColor==13:
            color=26#Forest Green
        elif queryColor==14:
            color=27#Light Teal
        elif queryColor==15:
            color=30#Purple
        elif queryColor==16:
            color=29#Light Blue
        elif queryColor==17:
            color=15#Dark Blue
        elif queryColor==18:
            color=5#Darkest Blue            
        elif queryColor==19:
            color=10#Brown
        for each in getSel:
            cmds.setAttr(each+".overrideEnabled", 1)
            cmds.setAttr(each+".overrideColor", color)            
            
inst = ColourPalet()
inst.create_colour_window()
