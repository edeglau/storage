import maya.cmds as cmds
import maya.mel
import sys, os
filepath= os.getcwd()
sys.path.append(str(filepath))
import baseFunctions_maya
reload (baseFunctions_maya)
getClass=baseFunctions_maya.BaseClass()

import stretchIK
reload (stretchIK)
getIKClass=stretchIK.stretchIKClass()

'''MG rigging modules'''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons License'
'http://creativecommons.org/licenses/by-sa/3.0/au/'

class PFaceConn(object):
    def __init__(self): 
        cmds.parent("Jaw_Ctrl_nod_grp", "head01_jnt")

        cmds.parent("EyeMask_Ctrl_grp", "EyeMask_Offset_Ctrl")
        try:
            cmds.parent("EyeMask_Offset_grp", "UpperBody_Ctrl")
        except:
            cmds.parent("EyeMask_Offset_grp", "LowerBody_Ctrl")
        cmds.parentConstraint("Head_Ctrl", "EyeMask_Offset_Ctrl", mo=1)
        
 
        