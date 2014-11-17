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

'''MG rigging modules'''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons License'
'http://creativecommons.org/licenses/by-sa/3.0/au/'

filepath= os.getcwd()
sys.path.append(str(filepath))
import baseFunctions_maya
reload (baseFunctions_maya)
getBaseClass=baseFunctions_maya.BaseClass()

class FaceRigger(object):
    '''--------------------------------------------------------------------------------------------------------------------------------------
    Interface Layout
    --------------------------------------------------------------------------------------------------------------------------------------'''          
    def __init__(self, winName="Rig Face"):
        self.winTitle = "Face Rig Modules"
        self.winName = winName

    def create(self):
        
        if cmds.window(self.winName, exists=True):
                cmds.deleteUI(self.winName)

        self.window = cmds.window(self.winName, title=self.winTitle, tbm=1, w=270, h=450, bgc=[0.45, 0.45, 0.45]  )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=300)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')

        cmds.rowLayout  (' rMainRow ', w=350, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', bgc=[0.7, 0.7, 0.7] , p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))
#         cmds.button (label='Brows', p='listBuildButtonLayout', command = self._get_curves)
#         cmds.button (label='Eye', p='listBuildButtonLayout', command = self._eye_cavity)
        cmds.text(label="Setup", bgc=[0.45, 0.45, 0.45])
        cmds.text(label="", bgc=[0.45, 0.45, 0.45])        
        cmds.button (label='SavePlacement', ann="Saves the placement of the face rig prior to connections(shapes named 'TRN' saves location)", bgc=[0.8, 0.8, 0.8], p='listBuildButtonLayout', command = self._save_placement) 
        cmds.button (label='loadPlacement', ann="loads a saved placement of the face rig prior to connections(shapes named 'TRN' saves location)", bgc=[0.8, 0.8, 0.8], p='listBuildButtonLayout', command = self._load_placement) 
        cmds.text(label="Rig", bgc=[0.45, 0.45, 0.45])
        cmds.text(label="", bgc=[0.45, 0.45, 0.45])        
        cmds.button (label='Controller', ann="Adds the BBox controller and faceRig (external file)", bgc=[0.8, 0.8, 0.8], p='listBuildButtonLayout', command = self._get_controller) 
        cmds.button (label='Connect', ann="Connects the BBox controller and faceRig to the rig", p='listBuildButtonLayout', command = self._connect)                
        cmds.button (label='Disconnect', ann="Disconnects face Rig from current rig(have only one rig loaded)", p='listBuildButtonLayout', command = self._disconnect)                
        cmds.button (label='Reconnect', ann="Reconnects the face Rig to current rig(have only one rig loaded)", p='listBuildButtonLayout', command = self._reconnect)                
        cmds.button (label='SkinFace', ann="Add the face rig joints to the selected mesh and sets up internal skinning (tongue, teeth, eyes - adhere to naming convention on meshes for this to work, have only one character mesh loaded)", p='listBuildButtonLayout', command = self._skin_face)        
        cmds.button (label='CleanFace', ann="Cleans up the outliner and removes TRN shapes", p='listBuildButtonLayout', command = self._clean_face) 
        cmds.button (label='skin int face', ann="Reconnects internal face skinning separatly(tongue, teeth, eyes)", p='listBuildButtonLayout', command = self._reskin_int_face) 
        cmds.text(label="", bgc=[0.45, 0.45, 0.45])
        cmds.text(label="Shape", bgc=[0.45, 0.45, 0.45])
        cmds.text(label="", bgc=[0.45, 0.45, 0.45])
        cmds.button (label='MirrorBlend', ann="Select blend shape and main mesh to mirror a blend shape to opposite side (X) axis", p='listBuildButtonLayout', command = self._mirror_blend)   
        cmds.text(label="", bgc=[0.45, 0.45, 0.45])               
        cmds.text(label="Blinks and lashes", bgc=[0.45, 0.45, 0.45])
        cmds.text(label="", bgc=[0.45, 0.45, 0.45])
#         cmds.button (label='**lid fix', bgc=[0, 0, 0], p='listBuildButtonLayout', command = self._lid_fix)        
#         cmds.button (label='**Additional Attr Mask', bgc=[0, 0, 0],p='listBuildButtonLayout', command = self._add_lash_attr_mask)
#         cmds.button (label='Add lid Attr Mask', p='listBuildButtonLayout', command = self._lid_attrs)
#         cmds.button (label='**Add face updates', bgc=[0, 0, 0], p='listBuildButtonLayout', command = self._lid_sdk)
#         cmds.button (label='**Blink Sculpt SDK', bgc=[0, 0, 0], p='listBuildButtonLayout', command = self._blink_SDK)  
#         cmds.button (label='Add lid SDK', p='listBuildButtonLayout', command = self._lid_sdk)
        cmds.button (label='Blink Sculpt', ann="Adds a sculpt to the eyelids to hold volume during blink - select face mesh",p='listBuildButtonLayout', command = self._blink_sculpt)
        cmds.button (label='Lash rivet', ann="Creates named rivets to connect the eyelash rig", p='listBuildButtonLayout', command = self._eye_lash_rivet)            
#         cmds.button (label='Add Anim Lash Ctrl1', p='listBuildButtonLayout', command = self._add_anim_lash1_ctrl)         
#         cmds.button (label='Add Anim Lash Ctrl2', p='listBuildButtonLayout', command = self._add_anim_lash2_ctrl)   
        cmds.button (label='Add Lash Rig', ann="Imports the eyelash rig and attaches it to face", p='listBuildButtonLayout', command = self._add_lash) 
        cmds.button (label='Add Anim Lash Ctrl', ann="Adds controllers to the eyelashes for animators", p='listBuildButtonLayout', command = self._add_anim_lash_ctrl)         
#         cmds.button (label='HBlinkAdd', p='listBuildButtonLayout', command = self._add_h_blink)        
#         cmds.button (label='reconnect Blnk', p='listBuildButtonLayout', command = self._recon_blnk)        
        cmds.button (label='Recreate Blink', ann="Recreates the connection to the blink shapes(follow name convention for blink shapes that are already present for this to work)", p='listBuildButtonLayout', command = self._recrt_blnk)   
#         cmds.text(label="", bgc=[0.45, 0.45, 0.45])
#         cmds.text(label="transforms", bgc=[0.45, 0.45, 0.45])
#         cmds.text(label="", bgc=[0.45, 0.45, 0.45])
#         cmds.button (label='MirrorTransform', p='listBuildButtonLayout', command = self._mirror_transform) 
#         cmds.button (label='MatchTransform', p='listBuildButtonLayout', command = self._match_transform) 
#         cmds.button (label='SelectMouth', p='listBuildButtonLayout', command = self._select_mouth) 
        #cmds.button (label='mirrorTransform', p='listBuildButtonLayout', command = self._mirror_placed) 
#         cmds.button (label='mirrorSelect', p='listBuildButtonLayout', command = self._mirror_select) 
#         cmds.button (label='combineSelectMirror', p='listBuildButtonLayout', command = self._combine_select) 
#         cmds.button (label='mirrorMouth', p='listBuildButtonLayout', command = self._mirror_mouth) 
#         cmds.button (label='mirrorBrows', p='listBuildButtonLayout', command = self._mirror_brows) 
#         cmds.button (label='mirrorLashRL', p='listBuildButtonLayout', command = self._mirror_LashRL) 
#         cmds.button (label='mirrorLashLR', p='listBuildButtonLayout', command = self._mirror_LashLR) 
#         cmds.button (label='ResetMouth', p='listBuildButtonLayout', command = self._reset_mouth) 
#         cmds.button (label='ResetSelected', p='listBuildButtonLayout', command = self._reset_selected)  
#         cmds.button (label='transferAttr', p='listBuildButtonLayout', command = self._tran_att)  
        cmds.text(label="", bgc=[0.45, 0.45, 0.45])
        cmds.text(label="Set SDK", bgc=[0.45, 0.45, 0.45])
        cmds.text(label="", bgc=[0.45, 0.45, 0.45])
        cmds.button (label='SDKphonemes', ann="Creates set driven key on the translation/rotation of selected face parts to be driven by the phoneme (in the BBox)", p='listBuildButtonLayout', command = self._phoneme_key)         
#         cmds.button (label='SDKAny', p='listBuildButtonLayout', command = self._set_any) 
        cmds.button (label='SDKMouthBlends', ann="Connects preset shapes (adhering to name convention) to the BBox controllers.(if using for simplified chars not requiring a full face skinned rig)", p='listBuildButtonLayout', command = self._sdk_mouthBlends) 
        cmds.button (label='BottLip_Attr', ann="Adds the bottom fat lip attribute to the Chin control on the Rig(add to rig file, not anim)", p='listBuildButtonLayout', command = self._blip_Attr) 
        cmds.button (label='BottLip_Blend', ann="Reconnects the bottom fat lip shape blend", p='listBuildButtonLayout', command = self._blip_Blend) 
#         cmds.text(label="facecams", bgc=[0.45, 0.45, 0.45])
#         cmds.text(label="", bgc=[0.45, 0.45, 0.45])
#         cmds.button (label='Add FaceCam', p='listBuildButtonLayout', command = self._face_cam) 
#         cmds.button (label='unlock FC', p='listBuildButtonLayout', command = self._unlock_face_cam) 
        cmds.text (label='Author: Elise Deglau',w=120, al='left', p='selectArrayColumn')      
        cmds.showWindow(self.window)


        
    def _blink_sculpt(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.BlinkSculpt()
        self._blink_SDK()
        
    def _lid_updown(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.BlinkSculpt()
        

    def _mirror_blend(self, arg=None): 
        getBaseClass.mirrorBlendshape()        

    
    def _mirror_transform(self, arg=None): 
        getBaseClass.mirrorXformRig()
          
    def _select_TRN(self, arg=None): 
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup() 
        getClass.select_trn()  
#     def Chin_Attr(self, arg=None): 
#         import FaceRig
#         reload (FaceRig)
#         getClass=FaceRig.FaceSetup() 
#         getClass.Chin_attr()  
#     def Chin_Blend(self, arg=None): 
#         import FaceRig
#         reload (FaceRig)
#         getClass=FaceRig.FaceSetup() 
#         getClass.Chin_Blends()  
    def _lid_attrs(self, arg=None): 
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup() 
        getClass.lid_attrs()  
    def _lid_sdk(self, arg=None): 
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup() 
        getClass.lid_sdk()  
        getClass.scaleMouthCorners()
        self._add_anim_lash_ctrl()
    def _lid_fix(self, arg=None): 
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup() 
        getClass.lidfix()  
        
    def _eye_lash_rivet(self, arg=None): 
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup() 
        getClass._lash_win()  
        
    def _reskin_int_face(self, arg=None): 
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup() 
        getClass.reskinFaceInternal()  
    def _face_cam(self, arg=None): 
        import FaceCam
        #reload (FaceCam)
        getClass=FaceCam.FaceCamera()  
        getClass.create()
    def _unlock_face_cam(self, arg=None): 
        import FaceCam
        #reload (FaceCam)
        getClass=FaceCam.FaceCamera()  
        getClass.unlock()
    def _save_placement(self, arg=None): 
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup() 
        getClass.save_placement()     
    def _recon_blnk(self, arg=None): 
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup() 
        getClass.reconnect_blinks()     
    def _recrt_blnk(self, arg=None): 
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup() 
        getClass.recreate_blinks()     
            
    def _load_placement(self, arg=None): 
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup() 
        getClass.load_placement()        

    def _connect(self, arg=None):
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup() 
        getClass.connect_to_head()        
    def _disconnect(self, arg=None):
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup() 
        getClass.disconnect_to_head()        
    def _reconnect(self, arg=None):
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup() 
        getClass.reconnect_to_head()        

    def _face_layout(self, arg=None):
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.Face()
        #getClass.HandRig()
            
    def _skin_face(self, arg=None):
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup()    
        getClass.skinning_face()        
        
    def _clean_face(self, arg=None):
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup()    
        getClass.clean_face()      

    def _get_controller(self, arg=None):
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup()    
        getClass.controller()  
    def _add_lash(self, arg=None):
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup()    
        getClass.AddLash()  
        self._add_anim_lash_ctrl()
#     def _skin_lash(self, arg=None):
#         import FaceRig
#         reload (FaceRig)
#         getClass=FaceRig.FaceSetup()    
#         getClass.skinLash()  
    def _blink_SDK(self, arg=None):
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup()    
        getClass.Blink_SDK()  
    def _mirror_mouth(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.mirrorSDKMouth()
    def _mirror_brows(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.mirrorBrows()
    def _mirror_LashRL(self, arg=None):
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup()
        getClass.mirrorLashRL()
    def _mirror_LashLR(self, arg=None):
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup()
        getClass.mirrorLashLR()
        
    def _add_lash_attr_mask(self, arg=None):
        cmds.addAttr("EyeMask_Ctrl", ln="showLashCtrls", min=0, max=1, at="double", k=1, nn="showLashCtrls")
        self._lid_attrs()
        
    def _add_anim_lash_ctrl(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getLash=cmds.ls("Lash_*_3_LSH")
        typeCtrl=""
        size=.5
        colour=22
        for each in getLash:
            getClass.sandwichControlFunct(colour, size, each,typeCtrl)
        getLash=cmds.ls("Lash_*_3_LSH_Ctrl")
        for item in getLash:
            cmds.select(item)
            cmds.showHidden(a=1)
        getLash=cmds.ls("Lash_*_LSH")
        for item in getLash:
            cmds.setAttr(item+"Shape.visibility", 0)
        getLash=cmds.ls("Lash_*_3_LSH_Ctrl")
        for item in getLash:
            cmds.connectAttr("*:EyeMask_Ctrl.showLashCtrls", item+".visibility", f=1) 
        self._add_anim_lash2_ctrl()                
        self._add_anim_lash1_ctrl()                
        
    def _add_anim_lash2_ctrl(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getLash=cmds.ls("Lash_*_2_LSH")
        typeCtrl=""   
        size=.3
        colour=22
        for each in getLash:
            getClass.sandwichControlFunct(colour, size, each,typeCtrl)
        getLash=cmds.ls("Lash_*_2_LSH_Ctrl")
        for item in getLash:
            cmds.select(item)
            cmds.showHidden(a=1)
        getLash=cmds.ls("Lash_*_LSH")
        for item in getLash:
            cmds.setAttr(item+"Shape.visibility", 0)
        getLash=cmds.ls("Lash_*_2_LSH_Ctrl")
        for item in getLash:
            cmds.connectAttr("*:EyeMask_Ctrl.showLashCtrls", item+".visibility", f=1)            

    def _add_anim_lash1_ctrl(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getLash=cmds.ls("Lash_*_1_LSH")
        typeCtrl=""   
        size=.2
        colour=22
        for each in getLash:
            getClass.sandwichControlFunct(colour, size, each,typeCtrl)
        getLash=cmds.ls("Lash_*_1_LSH_Ctrl")
        for item in getLash:
            cmds.select(item)
            cmds.showHidden(a=1)
        getLash=cmds.ls("Lash_*_LSH")
        for item in getLash:
            cmds.setAttr(item+"Shape.visibility", 0)
        getLash=cmds.ls("Lash_*_1_LSH_Ctrl")
        for item in getLash:
            cmds.connectAttr("*:EyeMask_Ctrl.showLashCtrls", item+".visibility", f=1)            
                 
    def _mirror_placed(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass() 
        #getClass.mirrorXform()
        getClass.mirrorController()      
    def _match_transform(self, arg=None):
        getBaseClass.xformmatch()      
    def _mirror_select(self, arg=None):
        getBaseClass.mirrorSelection()      
    def _combine_select(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass() 
        getClass.combineSelect()      
    def _tran_att(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass() 
        getClass.massTransfer()      
    def _phoneme_key(self, arg=None):
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup()    
        getClass.phonemeSDKKeys()      
    def _select_mouth(self, arg=None):
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup()    
        getClass.selectMouth()      
    def _reset_mouth(self, arg=None):
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup()    
        getClass.mouthSDK_Reset()      
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
    def _sdk_mouthBlends(self, arg=None):
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup()    
        getClass.connectBlendMouth()      
    def _blip_Blend(self, arg=None):
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup()    
        getClass.BottLip_Blends()      
    def _blip_Attr(self, arg=None):
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup()    
        getClass.BottLip_Attr()      
    def _add_h_blink(self, arg=None):
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup()    
        getClass.blendShapeHighBlink()      

inst = FaceRigger()
inst.create()

