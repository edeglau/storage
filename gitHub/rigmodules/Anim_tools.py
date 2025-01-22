import maya.cmds as cmds
from functools import partial
from string import *
import re
import maya.mel
import os, subprocess, sys, platform
from os  import popen
from sys import stdin
import sys
#import win32clipboard
import operator

'''MG rigging modules '''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons License'
'http://creativecommons.org/licenses/by-sa/3.0/au/'

filepath= os.getcwd()
sys.path.append(str(filepath))
import baseFunctions_maya
reload (baseFunctions_maya)
getBaseClass=baseFunctions_maya.BaseClass()

class AnimMoveTools(object):
    '''--------------------------------------------------------------------------------------------------------------------------------------
    Interface Layout
    --------------------------------------------------------------------------------------------------------------------------------------'''          
    def __init__(self, winName="Anim Tools"):
        self.winTitle = "Anim Tool Modules"
        self.winName = winName

    def create(self):
        
        if cmds.window(self.winName, exists=True):
                cmds.deleteUI(self.winName)

        self.window = cmds.window(self.winName, title=self.winTitle, tbm=1, w=320, h=600 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=200)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')

        cmds.rowLayout  (' rMainRow ', w=320, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(120, 20))
        cmds.button (label='Schematic', p='listBuildButtonLayout', ann="This will open a schematic for selected character", command = self._schematic)         
        cmds.button (label='CombineSelectMirror', p='listBuildButtonLayout', ann="This will add opposite control to the selection", command = self._combine_select)         
        cmds.button (label='MirrorTransform', p='listBuildButtonLayout', ann="This will mirror the transform to the opposite controller", command = self._mirror_transform) 
#         cmds.button (label='MirrorTransformFace', p='listBuildButtonLayout', ann="This will mirror the transform to the opposite controller", command = self._mirror_transform_face) 
        cmds.button (label='MatchTransform', p='listBuildButtonLayout', ann="This will match the relative transform of the first selection", command = self._match_transform) 
        cmds.button (label='MatchMatrix', p='listBuildButtonLayout', ann="This will match the exact matrix of the first selection", command = self._match_matrix) 
        #cmds.button (label='SelectMouth', p='listBuildButtonLayout', ann="This will select the characters mouth",command = self._select_mouth) 
        cmds.button (label='mirrorSelect', p='listBuildButtonLayout',  ann="This will change the selection to the mirror controller of the current selected",command = self._mirror_select) 
        cmds.button (label='mirrorMouth', p='listBuildButtonLayout', ann="This will mirror one side of the mouth to the other(will not affect control box attributes)", command = self._mirror_mouth) 
        cmds.button (label='mirrorBrows', p='listBuildButtonLayout', ann="This will mirror a brow position to the other(will not affect control box attributes)", command = self._mirror_brows)  
        cmds.button (label='mirrorEyes', p='listBuildButtonLayout', ann="This will mirror an eye position to the other", command = self._mirror_eyes)  
        cmds.button (label='mirrorFace', p='listBuildButtonLayout', ann="This will mirror the entire face to the other(will not affect control box attributes)", command = self._mirror_face)  
        cmds.button (label='ResetMouth', p='listBuildButtonLayout', ann="This will reset the mouth positions(anim transform controls only - will not affect control box attributes)",command = self._reset_mouth) 
        cmds.button (label='ResetSelected', p='listBuildButtonLayout', ann="This will reset the selected to 0.0(transforms only - will not affect control box attributes)", command = self._reset_selected)
        cmds.button (label='DisplayAnim', p='listBuildButtonLayout', ann="This sets the viewport to show only poly and curve", command = self._display_anim)
#         cmds.button (label='Shapes', p='listBuildButtonLayout', command = self._make_shape)           
        #cmds.text(label="")
        cmds.text(label="FK=IK")
        #cmds.separator()
        cmds.text(label="")
        cmds.button (label='ArmIK_2_FK', p='listBuildButtonLayout', ann="This will match the arm IK chain to the FK position",command = self._ikToFK_Arm)
        cmds.button (label='ArmFK_2_IK', p='listBuildButtonLayout', ann="This will match the arm FK chain to the IK position", command = self._fkToIK_Arm)
        cmds.button (label='LegIK_2_FK', p='listBuildButtonLayout', ann="This will match the leg IK chain to the FK position",command = self._ikToFK_Leg)
        cmds.button (label='LegFK_2_IK', p='listBuildButtonLayout', ann="This will match the leg FK chain to the IK position", command = self._fkToIK_Leg)
        cmds.text(label="other tools")
        cmds.text(label="")
        cmds.button (label='SelectArray', p='listBuildButtonLayout', ann="This is a custom tool to build up a user selection array or search and filter for specific nodes/names", command = self._select_array)        
        cmds.button (label='Switch Arm Cnst', p='listBuildButtonLayout', ann="resets arm in position on constraint switch", command = self._switch_arm_ik_cnstrnt)        
        #cmds.symbolButton (p='listBuildButtonLayout', command = self.Face, image="D:\myGraphics\icons\SP.jpg")      
        cmds.showWindow(self.window)

    def _display_anim(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.displayViewAnim()

    def _schematic(self, arg=None): 
        import Schematic
        reload (Schematic)
        getClass=Schematic.SchematicSelect() 
           
    def _mirror_blend(self, arg=None): 
        getBaseClass.mirrorBlendshape()        

    def _mirror_transform(self, arg=None): 
        getBaseClass.mirrorXform()
        
    def _mirror_transform_face(self, arg=None): 
        getBaseClass.mirrorXformface()

    def _make_shape(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.makeShape()
    def _switch_arm_ik_cnstrnt(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.switchArmIKConst()

    def _select_TRN(self, arg=None): 
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup() 
        getClass.select_trn()

    def _get_controller(self, arg=None):
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup()    
        getClass.controller()  
        
    def _mirror_mouth(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.mirrorMouth()
        
    def _mirror_brows(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.mirrorAnimBrows()
    def _mirror_eyes(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.mirrorAnimEyes()
    def _mirror_face(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.mirrorAnimFace()
        
    def _mirror_placed(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass() 
        #getClass.mirrorXform()
        getClass.mirrorController()    
          
    def _match_transform(self, arg=None):
#         getBaseClass.xformmove() 
        getBaseClass.xformmatch()     
    def _match_matrix(self, arg=None):
        getBaseClass.xformmove()     
         
    def _mirror_select(self, arg=None):
        getBaseClass.mirrorSelection()   
           
    def _combine_select(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass() 
        getClass.combineSelect()      


    def _select_mouth(self, arg=None):
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup()    
        getClass.selectAnimMouth()      
        
    def _reset_mouth(self, arg=None):
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup()    
        getClass.mouth_Reset()     
         
    def _reset_selected(self, arg=None):
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup()    
        getClass.Reset()      
        
    def _set_any(self, arg=None):
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup()    
        getClass.TR_SDKKeys()      
    def _ikToFK_Arm(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()    
        getClass.ikToFK_Arm()
    def _fkToIK_Arm(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()    
        getClass.fkToIK_Arm()
    def _ikToFK_Leg(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()    
        getClass.ikToFK_Leg()
    def _fkToIK_Leg(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()    
        getClass.fkToIK_Leg()
    def _select_array(self, arg=None):
        nfilepath=('G:\\_PIPELINE_MANAGEMENT\\Published\\maya\\AutoRig_MG\\selectArray\\')
        sys.path.append(str(nfilepath))
        import selectArray
        reload (selectArray)
        selectArray.SelectionPalettUI()  

inst = AnimMoveTools()
inst.create()


