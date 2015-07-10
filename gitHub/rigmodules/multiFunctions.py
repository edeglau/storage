import maya.cmds as cmds
from functools import partial
from string import *
import re
import maya.mel

'''MG rigging modules'''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons Attribution 4.0 International 4.0 (CC BY 4.0)'
# 'This work is licensed under a Creative Commons Attribution-ShareAlike 3.0 Australia (CC BY-SA 3.0 AU)'
'http://creativecommons.org/licenses/by-sa/3.0/au/'


class MultiFunctionClass(object):
    '''--------------------------------------------------------------------------------------------------------------------------------------
    Interface Layout
    --------------------------------------------------------------------------------------------------------------------------------------'''          
    def __init__(self, winName="MultiFunctions"):
        self.winTitle = "Multi Functions"
        self.winName = winName

    def multi_function_window(self, winName="Colors"):
        global colMenu
        if cmds.window(self.winName, exists=True):
                cmds.deleteUI(self.winName)

        self.window = cmds.window(self.winName, title=self.winTitle, tbm=1, w=300, h=100 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=300)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        
        cmds.rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildLayout', p='selectArrayColumn', numberOfColumns=1, cellWidthHeight=(300, 20))
        colMenu=cmds.optionMenu( label='Functions', w=300)
        cmds.menuItem( label="orient_constraint" )#1
        cmds.menuItem( label="aim_constraint")#2
        cmds.menuItem( label="parent_constraint")#3
        cmds.menuItem( label="point_constraint" )#4
        cmds.menuItem( label="extrude_tube")#5    
        cmds.menuItem( label="extrude_path")#5          
        cmds.menuItem( label="xform")#6 
        cmds.gridLayout('dimensions', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))
        cmds.text("length spans(extrude)")
        self.selfU=cmds.textField(text="12")
        cmds.text("width spans(extrude)")
        self.selfV=cmds.textField(text="1")
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=1, cellWidthHeight=(300, 20))
        cmds.button (label='Go', w=150, p='listBuildButtonLayout', command = lambda *args:self.perform_multi_function(selfU=cmds.textField(self.selfU, q=1,text=1), selfV=cmds.textField(self.selfV, q=1,text=1)))
        # cmds.button (label='Go', w=150, p='listBuildButtonLayout', command = self.perform_multi_function)
        cmds.showWindow(self.window)



    def perform_multi_function(self, selfU, selfV):
        '''----------------------------------------------------------------------------------
        Common add to list function
        ----------------------------------------------------------------------------------''' 
        # maya.mel.eval( 'nurbsToPolygonsPref -un %d -vn %d;',  %(selfU, ) %(selfV, )
        cmds.nurbsToPolygonsPref(un=selfU, vn=selfV)
        # nurbsToPolygonsPref -un 1 -vn 90
        ConstraintType=cmds.optionMenu(colMenu, q=1, sl=1)
        getObj=cmds.ls(sl=1)
        getParent=getObj[0]
        # cmds.nurbsToPolygonsPref(un=selfU, uv=selfV)
        for each in getObj[1:]: 
            if ConstraintType==1:#orient
                cmds.orientConstraint(getParent, each, mo=1)   
            elif ConstraintType==2:#aim
                cmds.aimConstraint(getParent, each, mo=1)   
            elif ConstraintType==3:#parent
                cmds.parentConstraint(getParent, each, mo=1) 
            elif ConstraintType==4:#point
                cmds.pointConstraint(getParent, each, mo=1)  
            elif ConstraintType==5:#extrude_tube
                cmds.extrude(getParent, each, ch=1, rn=0, po=1, et=2, ucp=1, fpt=1, upn=1, rsp=1, rotation=0, scale=1)
                # nurbsToPoly -mnd 1  -ch 1 -f 2 -pt 1 -pc 81 -chr 0.99 -ft 0.01 -mel 0.001 -d 0.1 -ut 1 -un 24 -vt 1 -vn 1 -uch 1 -ucr 1 -cht 0.2 -es 0 -ntr 0 -mrt 0 -uss 1 "extrudedSurface3"; 
            elif ConstraintType==6:#extrude_path
                cmds.nurbsToPolygonsPref(un=selfU, vn=selfV)
                cmds.extrude(getParent, each, ch=1, rn=0, po=1, et=1, ucp=1, fpt=1, upn=1, rotation=0, scale=1, rsp=1) 
                # cmds.extrude(getParent, each, ch=1, rn=0, po=1, et=0, fpt=1, upn=1, rotation=0, scale=1) 
            elif ConstraintType==7:#xform
                getTranslation, getRotation=self.locationXForm(getParent)
                each.setTranslation(getTranslation)
                each.setTranslation(getRotation)
            else:
                print "nothing performed"         
            
inst = MultiFunctionClass()
inst.multi_function_window()
