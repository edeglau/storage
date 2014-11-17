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

Brow_R_CC="Brow_R_CC"
Brow_L_CC="Brow_L_CC"
Emot_R_CC="Emot_R_CC"
Emot_L_CC="Emot_L_CC"
Jaw_CC="JawCtrl_CC"
Foot_IK_L="Footheel_IK_L_Ctrl"
Hoof_Rear_IK_L="Heel_rear_L_IK_Ctrl"
Foot_IK_R="Footheel_IK_R_Ctrl"
Hoof_Rear_IK_R="Heel_rear_R_IK_Ctrl"
Hand_IK_R="Armhand_IK_R_Ctrl"
Hoof_Front_IK_R="Heel_front_R_IK_Ctrl"
Hand_IK_L="Armhand_IK_L_Ctrl"
Hoof_Front_IK_L="Heel_front_L_IK_Ctrl"
ArmCollar_L="Armcollar_IK_L_Ctrl"
ArmCollar_R="Armcollar_IK_R_Ctrl"
BipedBody="UpperBody_Ctrl"
QuadBody="LowerBody_Ctrl"
Phonemes="Phonemes_CC"
EyeMask="EyeMask_Ctrl"
Hips="Hips_Ctrl"
Master="Master_Ctrl"
Main="Main_Ctrl"    
Knee_Pole_L="Knee_PoleVector_Left_Ctrl"
Knee_Pole_R="Knee_PoleVector_Right_Ctrl" 
Elbow_Pole_L= "elbow_L_PoleVector_Ctrl"
Elbow_Pole_R= "elbow_R_PoleVector_Ctrl" 
Neck="Neck_Ctrl"
Chest_IK="Chest_IK_Ctrl"     
Hand_Fingers_L="Hand_L_Fingers_Ctrl"        
Hand_Fingers_R="Hand_R_Fingers_Ctrl"
Head="Head_Ctrl"   
Elbow_L="Elbow_L_Ctrl"
Elbow_R="Elbow_R_Ctrl"
Shoulder_L="Shoulder_L_Ctrl"
Shoulder_R="Shoulder_R_Ctrl"     
Talus_L="Talus_L_Ctrl"
Talus_R="Talus_R_Ctrl"
Knee_L="Knee_L_Ctrl"
Knee_R="Knee_R_Ctrl"
Hip_L="Hip_L_Ctrl"
Hip_R="Hip_R_Ctrl"
Wrist_L="Wrist_L_Ctrl"
Wrist_R="Wrist_R_Ctrl"  
Finger_Index_L="Index_Finger_L_Ctrl"                
Finger_Mid_L="Mid_Finger_L_Ctrl"                
Finger_Ring_L="Ring_Finger_L_Ctrl"                
Finger_Pinky_L="Pinky_Finger_L_Ctrl"                
Thumb_Base_L="Thumbbase_L_Ctrl"                
Thumb_Mid_L="Thumbmid_L_Ctrl"                
Finger_Index_R="Index_Finger_R_Ctrl"                
Finger_Mid_R="Mid_Finger_R_Ctrl"                
Finger_Ring_R="Ring_Finger_R_Ctrl"                
Finger_Pinky_R="Pinky_Finger_R_Ctrl"                
Thumb_Base_R="Thumbbase_R_Ctrl"                
Thumb_Mid_R="Thumbmid_R_Ctrl"                
Brow_5_R="Brow05_R_Ctrl"
Brow_4_R="Brow04_R_Ctrl"      
Brow_3_R="Brow03_R_Ctrl" 
Brow_2_R="Brow02_R_Ctrl"
Brow_1_R="Brow01_R_Ctrl"    
Brow_5_L="Brow05_L_Ctrl"
Brow_4_L="Brow04_L_Ctrl" 
Brow_3_L="Brow03_L_Ctrl"
Brow_2_L="Brow02_L_Ctrl"  
Brow_1_L="Brow01_L_Ctrl"     
Lid_2_B_L="Lid_Open02_B_L_Ctrl"
Lid_3_B_L="Lid_Open03_B_L_Ctrl"
Lid_4_B_L="Lid_Open04_B_L_Ctrl"
Lid_5_B_L="Lid_Open05_B_L_Ctrl"
Lid_4_T_L="Lid_Open04_T_L_Ctrl"
Lid_3_T_L="Lid_Open03_T_L_Ctrl"
Lid_2_T_L="Lid_Open02_T_L_Ctrl"           
Lid_2_B_R="Lid_Open02_B_R_Ctrl"
Lid_3_B_R="Lid_Open03_B_R_Ctrl"
Lid_4_B_R="Lid_Open04_B_R_Ctrl"
Lid_5_B_R="Lid_Open05_B_R_Ctrl"
Lid_4_T_R="Lid_Open04_T_R_Ctrl"
Lid_3_T_R="Lid_Open03_T_R_Ctrl"
Lid_2_T_R="Lid_Open02_T_R_Ctrl"      
CheekBone_R="CheekBone_R_Ctrl"
Cheek_R="Cheek_R_Ctrl"
Cheek_T_R="Cheek_T_R_Ctrl"
Nose_R="Nose_R_Ctrl"
CheekBone_L="CheekBone_L_Ctrl"
Cheek_L="Cheek_L_Ctrl"
Cheek_T_L="Cheek_T_L_Ctrl"
Nose_L="Nose_L_Ctrl"
Nose="Nose_Ctrl"                  
Jaw_L="Jaw_L_Ctrl"
Jaw_R="Jaw_R_Ctrl"                          
Lip_T="Lip_T_Ctrl"
Lip_T_L="Lip_T_L_Ctrl"
Lip_C_L="Lip_Corner_L_Ctrl"
Lip_B_R="Lip_B_R_Ctrl"
Lip_B="Lip_B_Ctrl"
Lip_B_L="Lip_B_L_Ctrl" 
Lip_C_R="Lip_Corner_R_Ctrl"
Lip_T_R="Lip_T_R_Ctrl"  
Teeth_B="Teeth_Handle_B_Ctrl"
Teeth_T ="Teeth_Handle_T_Ctrl"   
Tongue_5="Tongue05_Ctrl"      
Tongue_4="Tongue04_Ctrl"       
Tongue_3="Tongue03_Ctrl"  
Tongue_2="Tongue02_Ctrl"      
Tongue_1="Tongue01_Ctrl"  
Tongue_Main="Tongue_Master_Ctrl"  
Chin="Chin_Ctrl"    
BodySet="BodyControllers"
FaceSet="FaceControllers"
FaceAnimControls="FaceAnimCtrls"
FaceControlBoxSet="FaceControlBBox"
Lashes_R=[
        "Lash_T_R_3_LSH_Ctrl",
        "Lash_M_R_3_LSH_Ctrl",
        "Lash_M_R_2_LSH_Ctrl",
        "Lash_B_R_3_LSH_Ctrl",
        "Lash_B_R_2_LSH_Ctrl",
        "Lash_T_R_2_LSH_Ctrl",
        "Lash_T_R_1_LSH_Ctrl",
        "Lash_M_R_1_LSH_Ctrl",
        "Lash_B_R_1_LSH_Ctrl",
        ]
Lashes_L=[
        "Lash_T_L_1_LSH_Ctrl",
        "Lash_M_L_1_LSH_Ctrl",
        "Lash_B_L_1_LSH_Ctrl",
        "Lash_B_L_2_LSH_Ctrl",
        "Lash_M_L_2_LSH_Ctrl",
        "Lash_T_L_2_LSH_Ctrl",
        "Lash_T_L_3_LSH_Ctrl",
        "Lash_M_L_3_LSH_Ctrl",
        "Lash_B_L_3_LSH_Ctrl",
        ]

class SchematicSelect(object):
    '''--------------------------------------------------------------------------------------------------------------------------------------
    Interface Layout
    --------------------------------------------------------------------------------------------------------------------------------------'''          
    def __init__(self, winName="Body Controls"):
        self.winTitle = "Character Ctrl Menu"
        self.winName = winName

    def create(self):
        global SeModeMenu
        if cmds.window(self.winName, exists=True):
                cmds.deleteUI(self.winName)
        
        self.window = cmds.window(self.winName, title=self.winTitle, tbm=1, w=250, h=760 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=200)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')

        cmds.rowLayout  (' rMainRow ', w=350, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('bodyButton', p='selectArrayColumn', numberOfColumns=1, cellWidthHeight=(240, 18)) 
        SeModeMenu=cmds.optionMenu( label='Select Mode')
        cmds.menuItem( label='Replace' )
        cmds.menuItem( label='Add' )       
        cmds.button (label='Select body', bgc=[.1, .1,.1], p='bodyButton', command = self._selectBody)          
        cmds.button (label='Select whole body', bgc=[.1, .1,.1], p='bodyButton', command = self._selectBodyWhole)          
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(120, 18))
        cmds.button (label='Phonemes*', bgc=[.5, 0.0, 0.0], p='listBuildButtonLayout', command = self.Phonemes)  
        cmds.button (label='EyeMask*', bgc=[.5, .5, 0.0], p='listBuildButtonLayout', command = self._eyemask)               
        cmds.button (label='Chin', bgc=[.5, .5, 0.0], p='listBuildButtonLayout', command = self.Chin_Ctrl)        
        cmds.button (label='Head_Ctrl', bgc=[0.0, .5, .5], p='listBuildButtonLayout', command = self._head) 
        cmds.button (label='Neck_Ctrl', bgc=[0.0, .5, .5], p='listBuildButtonLayout', command = self._neck)        
        cmds.button (label='Chest_Ctrl', bgc=[0.0, .5, .5], p='listBuildButtonLayout', command = self._chest_ik) 
        cmds.button (label='Body_Ctrl', bgc=[0.0, .5, .5], p='listBuildButtonLayout', command = self._body) 
        cmds.button (label='Hips_Ctrl*', p='listBuildButtonLayout', bgc=[0.0, .5, .5], command = self._hips_select)         
        cmds.button (label='Main_Ctrl', p='listBuildButtonLayout', bgc=[0.0, .5, .5], command = self._main_select)        
        cmds.button (label='Master_Ctrl', p='listBuildButtonLayout', bgc=[0.0, .5, .5], command = self._master_select)                     
        cmds.button (label='Armcollar_R_Ctrl*', bgc=[.5, 0.0, 0.0], p='listBuildButtonLayout', command = self._arm_R_Collar) 
        cmds.button (label='Armcollar_L_Ctrl*', bgc=[.5, 0.0, 0.0], p='listBuildButtonLayout', command = self._arm_L_Collar)        
        cmds.text(label="IK limbs")              
        cmds.text(label="")              
        cmds.button (label='Arm_Pole_R_Ctrl', bgc=[0.5, 0.0, 0.0],p='listBuildButtonLayout', command = self._pole_R_arm) 
        cmds.button (label='Arm_Pole_L_Ctrl', bgc=[0.5, 0.0, 0.0],p='listBuildButtonLayout', command = self._pole_L_arm) 
        cmds.button (label='Armhand_IK_R_Ctrl', bgc=[0.5, 0.0, 0.0],p='listBuildButtonLayout', command = self._arm_R_hand) 
        cmds.button (label='Armhand_IK_L_Ctrl', bgc=[0.5, 0.0, 0.0],p='listBuildButtonLayout', command = self._arm_L_hand) 
        cmds.button (label='Knee_Pole_R_Ctrl', bgc=[0.5, 0.0, 0.0],p='listBuildButtonLayout', command = self._pole_R_leg)  
        cmds.button (label='Knee_Pole_L_Ctrl', bgc=[0.5, 0.0, 0.0],p='listBuildButtonLayout', command = self._pole_L_leg) 
        cmds.button (label='Footheel_IK_R_Ctrl', bgc=[0.5, 0.0, 0.0],p='listBuildButtonLayout', command = self._Foot_IK_R_heel)
        cmds.button (label='Footheel_IK_L_Ctrl', bgc=[0.5, 0.0, 0.0],p='listBuildButtonLayout', command = self._Foot_IK_L_heel)         
        cmds.text(label="FK limbs")              
        cmds.text(label="")              
        cmds.button (label='Shoulder_R_Ctrl', bgc=[0.0, 0.0, .5], p='listBuildButtonLayout', command = self._Shoulder_R) 
        cmds.button (label='Shoulder_L_Ctrl', bgc=[0.0, 0.0, .5], p='listBuildButtonLayout', command = self._Shoulder_L)
        cmds.button (label='Elbow_R_Ctrl', bgc=[0.0, 0.0, .5],p='listBuildButtonLayout', command = self._elbow_R) 
        cmds.button (label='Elbow_L_Ctrl', bgc=[0.0, 0.0, .5],p='listBuildButtonLayout', command = self._elbow_L) 
        cmds.button (label='Wrist_R_Ctrl', bgc=[0.0, 0.0, .5],p='listBuildButtonLayout', command = self._wrist_R) 
        cmds.button (label='Wrist_L_Ctrl', bgc=[0.0, 0.0, .5],p='listBuildButtonLayout', command = self._wrist_L) 
        cmds.button (label='Hip_R_Ctrl', bgc=[0.0, 0.0, .5],p='listBuildButtonLayout', command = self._hip_R) 
        cmds.button (label='Hip_L_Ctrl', bgc=[0.0, 0.0, .5],p='listBuildButtonLayout', command = self._hip_L)         
        cmds.button (label='Knee_R_Ctrl', bgc=[0.0, 0.0, .5],p='listBuildButtonLayout', command = self._knee_R)
        cmds.button (label='Knee_L_Ctrl', bgc=[0.0, 0.0, .5],p='listBuildButtonLayout', command = self._knee_L)         
        cmds.button (label='Talus_R_Ctrl', bgc=[0.0, 0.0, .5],p='listBuildButtonLayout', command = self._talus_R)
        cmds.button (label='Talus_L_Ctrl', bgc=[0.0, 0.0, .5],p='listBuildButtonLayout', command = self._talus_L)
        cmds.text(label="Hands")              
        cmds.text(label="")         
        cmds.gridLayout('HandList', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(120, 18))
        cmds.button (label='Hand_R_Fingers_Ctrl*', bgc=[.5, .5, 0.0], p='HandList', command = self._hand_R)        
        cmds.button (label='Hand_L_Fingers_Ctrl*', bgc=[.5, .5, 0.0], p='HandList', command = self._hand_L) 
        cmds.button (label='Select R Fingers', bgc=[.5, .5, 0.0], p='HandList', command = self._fingers_R) 
        cmds.button (label='Select L Fingers', bgc=[.5, .5, 0.0], p='HandList', command = self._fingers_L)
        cmds.gridLayout('fingerList', p='selectArrayColumn', numberOfColumns=13, cellWidthHeight=(18, 18))
        cmds.button (label='P', bgc=[0.7, .7, 0.0], p='fingerList', command = self.Finger_Pinky_R)
        cmds.button (label='R', bgc=[0.7, .7, 0.0], p='fingerList', command = self.Finger_Ring_R) 
        cmds.button (label='M', bgc=[0.7, .7, 0.0], p='fingerList', command = self.Finger_Mid_R) 
        cmds.button (label='I', bgc=[0.7, .7, 0.0], p='fingerList', command = self.Finger_Index_R) 
        cmds.button (label='TK', bgc=[0.7, .7, 0.0], p='fingerList', command = self.Thumb_Mid_R) 
        cmds.button (label='TB', bgc=[0.7, .7, 0.0], p='fingerList', command = self.Thumb_Base_R) 
        cmds.text(label="", p='fingerList')
        cmds.button (label='TB', bgc=[0.7, .7, 0.0], p='fingerList', command = self.Thumb_Base_L)
        cmds.button (label='TK', bgc=[0.7, .7, 0.0], p='fingerList', command = self.Thumb_Mid_L) 
        cmds.button (label='I', bgc=[0.7, .7, 0.0], p='fingerList', command = self.Finger_Index_L) 
        cmds.button (label='M', bgc=[0.7, .7, 0.0], p='fingerList', command = self.Finger_Mid_L) 
        cmds.button (label='R', bgc=[0.7, .7, 0.0], p='fingerList', command = self.Finger_Ring_L) 
        cmds.button (label='P', bgc=[0.7, .7, 0.0], p='fingerList', command = self.Finger_Pinky_L)
        cmds.text(label="", p='selectArrayColumn')  
        cmds.text(label="Face", p='selectArrayColumn')   
        cmds.gridLayout('faceButton', p='selectArrayColumn', numberOfColumns=1, cellWidthHeight=(240, 18))         
        cmds.button (label='Select Face', bgc=[.1, .1, .1], p='faceButton', command = self._selectFace)              
        cmds.button (label='Select Whole Face', bgc=[.1, .1, .1], p='faceButton', command = self._selectFaceWhole)              
        cmds.button (label='Select Upper Face', bgc=[.1, .1, .1], p='faceButton', command = self._selectFaceUpper)              
        cmds.button (label='Select ControlBox', bgc=[.1, .1, .1], p='faceButton', command = self._selectControlBox)              
        cmds.separator(p='selectArrayColumn')       
        cmds.text(label="Brows", p='selectArrayColumn')  
        cmds.gridLayout('BrowsSelect', p='selectArrayColumn', numberOfColumns=1, cellWidthHeight=(240, 18))         
        cmds.button (label='Select Brows', bgc=[.2, 0.4, 0.2], p='BrowsSelect', command = self._selectBrows)         
        cmds.gridLayout('browButton', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(120, 18))         
        cmds.button (label='Select R Brow', bgc=[.2, 0.4, 0.2], p='browButton', command = self._selectRBrow)           
        cmds.button (label='Select L Brow', bgc=[.2, 0.4, 0.2], p='browButton', command = self._selectLBrow)           
        cmds.gridLayout('faceList', p='selectArrayColumn', numberOfColumns=11, cellWidthHeight=(22, 18))
        cmds.button (label='R', bgc=[0.0, .5, 0.0], p='faceList', command = self._brow05_R)
        cmds.button (label='R', bgc=[0.0, .5, 0.0], p='faceList', command = self._brow04_R) 
        cmds.button (label='R', bgc=[0.0, .5, 0.0], p='faceList', command = self._brow03_R) 
        cmds.button (label='R', bgc=[0.0, .5, 0.0], p='faceList', command = self._brow02_R) 
        cmds.button (label='R', bgc=[0.0, .5, 0.0], p='faceList', command = self._brow01_R) 
        cmds.text(label="", p='faceList')
        cmds.button (label='L', bgc=[0.0, .5, 0.0], p='faceList', command = self._brow01_L) 
        cmds.button (label='L', bgc=[0.0, .5, 0.0], p='faceList', command = self._brow02_L) 
        cmds.button (label='L', bgc=[0.0, .5, 0.0], p='faceList', command = self._brow03_L) 
        cmds.button (label='L', bgc=[0.0, .5, 0.0], p='faceList', command = self._brow04_L) 
        cmds.button (label='L', bgc=[0.0, .5, 0.0], p='faceList', command = self._brow05_L) 
        cmds.text(label="", p='selectArrayColumn')  
        cmds.text(label="eyes", p='selectArrayColumn')              
        cmds.gridLayout('EyeSButton', p='selectArrayColumn', numberOfColumns=1, cellWidthHeight=(240, 18))         
        cmds.button (label='Blink', bgc=[.5, 0.0, 0.3], p='EyeSButton', command = self._Blink)           
        cmds.button (label='Select Eyes', bgc=[.5, 0.0, 0.3], p='EyeSButton', command = self._selectEyes)           
        cmds.gridLayout('EyeButton', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(120, 18))         
        cmds.button (label='Select R Lash', bgc=[.5, 0.0, 0.3], p='EyeButton', command = self._Lash_R)           
        cmds.button (label='Select L Lash', bgc=[.5, 0.0, 0.3], p='EyeButton', command = self._Lash_L)           
        cmds.button (label='Select R Eye', bgc=[.5, 0.0, 0.3], p='EyeButton', command = self._selectREye)           
        cmds.button (label='Select L Eye', bgc=[.5, 0.0, 0.3], p='EyeButton', command = self._selectLEye)  
        cmds.gridLayout('eyeList', p='selectArrayColumn', numberOfColumns=9, cellWidthHeight=(27, 18))
        cmds.text(label="", p='eyeList')        
        cmds.button (label='R', bgc=[.5, 0.0, .5], p='eyeList', command = self.Lid_Open02_T_R_Ctrl) 
        cmds.button (label='R', bgc=[.5, 0.0, .5], p='eyeList', command = self.Lid_Open03_T_R_Ctrl) 
        cmds.button (label='R', bgc=[.5, 0.0, .5], p='eyeList', command = self.Lid_Open04_T_R_Ctrl)
        cmds.text(label="", p='eyeList')
        cmds.button (label='L', bgc=[.5, 0.0, .5], p='eyeList', command = self.Lid_Open04_T_L_Ctrl) 
        cmds.button (label='L', bgc=[.5, 0.0, .5], p='eyeList', command = self.Lid_Open03_T_L_Ctrl) 
        cmds.button (label='L', bgc=[.5, 0.0, .5], p='eyeList', command = self.Lid_Open02_T_L_Ctrl) 
        cmds.gridLayout('eyeBotList', p='selectArrayColumn', numberOfColumns=9, cellWidthHeight=(27, 18))
        cmds.button (label='R', bgc=[.5, 0.0, .5], p='eyeBotList', command = self.Lid_Open02_B_R_Ctrl)
        cmds.button (label='R', bgc=[.5, 0.0, .5], p='eyeBotList', command = self.Lid_Open03_B_R_Ctrl)
        cmds.button (label='R', bgc=[.5, 0.0, .5], p='eyeBotList', command = self.Lid_Open04_B_R_Ctrl)
        cmds.button (label='R', bgc=[.5, 0.0, .5], p='eyeBotList', command = self.Lid_Open05_B_R_Ctrl) 
        cmds.text(label="", p='eyeBotList')
        cmds.button (label='L', bgc=[.5, 0.0, .5], p='eyeBotList', command = self.Lid_Open05_B_L_Ctrl) 
        cmds.button (label='L', bgc=[.5, 0.0, .5], p='eyeBotList', command = self.Lid_Open04_B_L_Ctrl) 
        cmds.button (label='L', bgc=[.5, 0.0, .5], p='eyeBotList', command = self.Lid_Open03_B_L_Ctrl) 
        cmds.button (label='L', bgc=[.5, 0.0, .5], p='eyeBotList', command = self.Lid_Open02_B_L_Ctrl) 
        cmds.text(label="", p='selectArrayColumn')         
        cmds.text(label="cheeks", p='selectArrayColumn')              
        cmds.gridLayout('cheekList', p='selectArrayColumn', numberOfColumns=11, cellWidthHeight=(35, 18))
        cmds.button (label='R', bgc=[.5, 0.0, 0.0], p='cheekList', command = self.CheekBone_R_Ctrl) 
        cmds.button (label='R', bgc=[.5, 0.0, 0.0], p='cheekList', command = self.Cheek_T_R_Ctrl) 
        cmds.button (label='R', bgc=[.5, 0.0, 0.0], p='cheekList', command = self.Nose_R_Ctrl) 
        cmds.button (label='N', bgc=[.5, 0.0, .5], p='cheekList', command = self.Nose_Ctrl) 
        cmds.button (label='L', bgc=[.5, 0.0, 0.0], p='cheekList', command = self.Nose_L_Ctrl) 
        cmds.button (label='L', bgc=[.5, 0.0, 0.0], p='cheekList', command = self.Cheek_T_L_Ctrl) 
        cmds.button (label='L', bgc=[.5, 0.0, 0.0], p='cheekList', command = self.CheekBone_L_Ctrl)
        cmds.gridLayout('jawList', p='selectArrayColumn', numberOfColumns=7, cellWidthHeight=(35, 18))
        cmds.text(label="", p='jawList') 
        cmds.button (label='R', bgc=[.5, 0.0, 0.0], p='jawList', command = self.Jaw_R_Ctrl)         
        cmds.button (label='R', bgc=[.5, 0.0, 0.0], p='jawList', command = self.Cheek_R_Ctrl)
        cmds.text(label="", p='jawList')  
        cmds.button (label='L', bgc=[.5, 0.0, 0.0], p='jawList', command = self.Cheek_L_Ctrl)
        cmds.button (label='L', bgc=[.5, 0.0, 0.0], p='jawList', command = self.Jaw_L_Ctrl)
#         cmds.text(label="", p='jawList')  
        cmds.text(label="lips", p='selectArrayColumn') 
        cmds.gridLayout('mouthbutton', p='selectArrayColumn', numberOfColumns=1, cellWidthHeight=(240, 18))         
        cmds.button (label='All Mouth', bgc=[.4, 0.1, 0.1], p='mouthbutton', command = self._select_all_mouth)        
        cmds.button (label='Select Mouth', bgc=[.4, 0.1, 0.1], p='mouthbutton', command = self._select_mouth)        
        cmds.gridLayout('lipsListTop', p='selectArrayColumn', numberOfColumns=5, cellWidthHeight=(48, 18))
        cmds.button (label='CR', bgc=[.6, 0.2, 0.2], p='lipsListTop', command = self.Lip_Corner_R_Ctrl)
        cmds.button (label='TR', bgc=[.6, 0.2, 0.2], p='lipsListTop', command = self.Lip_T_R_Ctrl) 
        cmds.button (label='T', bgc=[.6, 0.2, 0.2], p='lipsListTop', command = self.Lip_T_Ctrl) 
        cmds.button (label='TL', bgc=[.6, 0.2, 0.2], p='lipsListTop', command = self.Lip_T_L_Ctrl) 
        cmds.button (label='CL', bgc=[.6, 0.2, 0.2], p='lipsListTop', command = self.Lip_Corner_L_Ctrl)  
        cmds.gridLayout('lipsListBot', p='selectArrayColumn', numberOfColumns=5, cellWidthHeight=(48, 18))
        cmds.text(label="", p='lipsListBot')         
        cmds.button (label='BR', bgc=[.6, 0.2, 0.2], p='lipsListBot', command = self.Lip_B_R_Ctrl)
        cmds.button (label='B', bgc=[.6, 0.2, 0.2], p='lipsListBot', command = self.Lip_B_Ctrl) 
        cmds.button (label='BL', bgc=[.6, 0.2, 0.2], p='lipsListBot', command = self.Lip_B_L_Ctrl)     
        cmds.text(label="", p='lipsListBot') 
        cmds.text(label="", p='selectArrayColumn')  
        cmds.text(label="Tongue", p='selectArrayColumn') 
        cmds.gridLayout('tongueList', p='selectArrayColumn', numberOfColumns=6, cellWidthHeight=(40, 18))
        cmds.button (label='M', bgc=[1.0, 1.0, 0.0], p='tongueList', command = self.Tongue_Master_Ctrl)
        cmds.button (label='01', bgc=[.7, 0.7, 0.0], p='tongueList', command = self.Tongue05_Ctrl)
        cmds.button (label='02', bgc=[.7, 0.7, 0.0], p='tongueList', command = self.Tongue04_Ctrl) 
        cmds.button (label='03', bgc=[.7, 0.7, 0.0], p='tongueList', command = self.Tongue03_Ctrl) 
        cmds.button (label='04', bgc=[.7, 0.7, 0.0], p='tongueList', command = self.Tongue02_Ctrl) 
        cmds.button (label='05', bgc=[.7, 0.7, 0.0], p='tongueList', command = self.Tongue01_Ctrl) 
        cmds.text(label="", p='selectArrayColumn')  
        cmds.gridLayout('teethList', p='selectArrayColumn', numberOfColumns=1, cellWidthHeight=(240, 18))        
        cmds.button (label='Top Teeth', bgc=[1.0, 1.0, 1.0], p='teethList', command = self.Teeth_Handle_T_Ctrl) 
        cmds.button (label='Bottom Teeth', bgc=[1.0, 1.0, 1.0], p='teethList', command = self.Teeth_Handle_B_Ctrl) 
        cmds.button (label='Tail_FK', bgc=[.0, .0, .0], p='teethList', command = self.tail) 

      
        #cmds.separator()
        cmds.text(label="")
              
        cmds.showWindow(self.window)

    def select_function_add(self, bodyPart):
        getAsset=self.getName()   
        if getAsset==None:
            getBodyPart=cmds.ls(bodyPart)            
            if len(getBodyPart)>0:
                cmds.select(bodyPart, add=1)
        else:                
            getBodyPart=cmds.ls(getAsset+bodyPart) 
            if len(getBodyPart)>0:
                cmds.select(getAsset+bodyPart, add=1)

        
    def getName(self, arg=None):
        try:
            getSel=cmds.ls(sl=1)[0]
            pass
        except:
            print "select something"
            return
        if ":" in getSel:
            if "Anim" in getSel:
                if "Rig" in getSel:
                    if "Polly_Rig" in getSel:
                        getParent=getSel.split(":")  
                        getPort=':'.join(getParent[:-1])                
                        #getPArt="Polly_Rig"
#                         getAsset=getPort+":"+getPArt+":"
                        getAsset=getPort+":"
                    else:
                        getParent=getSel.split(":")
                        getAsset=':'.join(getParent[:-1])+":"
                if "Rig" not in getSel:
                    getParent=cmds.listRelatives(getSel, f=1)
                    getnames=getParent[0].split("|")
                    reduce=getnames[1].split(":")
                    getAsset=":".join(reduce[:-1])+":"             
            else:
                getParent=getSel.split(":")
                getAsset=':'.join(getParent[:-1])+":"
                if "Rig" not in getSel:
                    getParent=cmds.listRelatives(getSel, f=1)
                    getnames=getParent[0].split("|")
                    reduce=getnames[1].split(":")
                    getAsset=":".join(reduce[:-1])+":"                   
        else:
            getallnames=cmds.ls("*Rig:*")
            getParent=getallnames[0].split(":")[0]
            getAsset=getParent+":"
        return getAsset


    def getFaceName(self, arg=None):
        try:
            getSel=cmds.ls(sl=1)[0]
            pass
        except:
            print "select something"
            return
        if ":" in getSel:
            getParent=getSel.split(":")[0]
            getAsset= getParent+":"
        else:
            getAsset=None
        return getAsset     
    
    def select_function(self, bodyPart):
        getAsset=self.getName()
        querySel=cmds.optionMenu(SeModeMenu, q=1, sl=1)
        if querySel==1:
            if getAsset==None:
                getBodyPart=cmds.ls(bodyPart)            
                if len(getBodyPart)>0:
                    cmds.select(bodyPart)
            else:                
                getBodyPart=cmds.ls(getAsset+bodyPart) 
                if len(getBodyPart)>0:
                    cmds.select(getAsset+bodyPart)      
        elif querySel==2:          
            if getAsset==None:
                getBodyPart=cmds.ls(bodyPart)            
                if len(getBodyPart)>0:
                    cmds.select(bodyPart, add=1)
            else:                
                getBodyPart=cmds.ls(getAsset+bodyPart) 
                if len(getBodyPart)>0:
                    cmds.select(getAsset+bodyPart, add=1)
    def deselect_function(self, bodyPart): 
        getAsset=self.getName()    
        if getAsset==None:
            getBodyPart=cmds.ls(bodyPart)            
            if len(getBodyPart)>0:
                cmds.select(bodyPart, d=1)
        else:                
            getBodyPart=cmds.ls(getAsset+bodyPart) 
            if len(getBodyPart)>0:
                cmds.select(getAsset+bodyPart, d=1)


    def select_function_multi(self, bodyPart):
        getAsset=self.getName()
        querySel=cmds.optionMenu(SeModeMenu, q=1, sl=1)
        if querySel==1:
            if getAsset==None:
                getBodyPart=cmds.ls(bodyPart[0])            
                if len(getBodyPart)>0:
                    cmds.select(bodyPart[0])
                    for each in bodyPart[1:]:
                        cmds.select(each, add=1)
            else:                
                getBodyPart=cmds.ls(getAsset+bodyPart[0]) 
                if len(getBodyPart)>0:
                    cmds.select(getAsset+bodyPart[0])
                    for each in bodyPart[1:]:
                        cmds.select(getAsset+each, add=1)                         
        elif querySel==2:          
            if getAsset==None:
                getBodyPart=cmds.ls(bodyPart[0])            
                if len(getBodyPart)>0:
                    cmds.select(bodyPart[0], add=1)
                    for each in bodyPart[1:]:
                        cmds.select(each, add=1)
            else:                
                getBodyPart=cmds.ls(getAsset+bodyPart[0]) 
                if len(getBodyPart)>0:
                    cmds.select(getAsset+bodyPart[0], add=1)
                    for each in bodyPart[1:]:
                        cmds.select(getAsset+each, add=1)
                         
    def tail(self, arg=None):
        if cmds.ls("*:tail*"):
            bodyPart="tail"
            endPart="_FK_ctrl"
            self.select_function_tail(bodyPart, endPart)
        elif cmds.ls("*:*:tail*"):
            bodyPart="tail"
            endPart="_FK_ctrl"
            self.select_function_tail(bodyPart, endPart)
        elif cmds.ls("*:*:Tail*"):
            bodyPart="Tail"
            endPart="_FK_Ctrl"
            self.select_function_tail(bodyPart, endPart)
        elif cmds.ls("*:Tail*"):
            bodyPart="Tail"
            endPart="_FK_Ctrl"
            self.select_function_tail(bodyPart, endPart)
        
    def select_function_tail(self, bodyPart, endPart):
        getAsset=self.getName()
        querySel=cmds.optionMenu(SeModeMenu, q=1, sl=1)
        if querySel==1:
            if getAsset==None:
                getBodyPart=cmds.ls(bodyPart+"*"+endPart)            
                if len(getBodyPart)>0:
                    cmds.select(bodyPart)
                    for each in bodyPart[1:]:
                        cmds.select(each, add=1)
            else:      
                getBodyPart=cmds.ls(getAsset+bodyPart+"*"+endPart) 
                print len(getBodyPart)
                if len(getBodyPart)>0:
                    cmds.select(getBodyPart[0])
                    for each in getBodyPart[1:]:
                        cmds.select(each, add=1)                         
        elif querySel==2:          
            if getAsset==None:
                getBodyPart=cmds.ls(bodyPart+"*"+endPart)            
                if len(getBodyPart)>0:
                    cmds.select(getBodyPart[0], add=1)
                    for each in getBodyPart[1:]:
                        cmds.select(each, add=1)
            else:                
                getBodyPart=cmds.ls(getAsset+bodyPart+"*"+endPart) 
                if len(getBodyPart)>0:
                    cmds.select(getBodyPart[0], add=1)
                    for each in getBodyPart[1:]:
                        cmds.select(each, add=1) 
                        
    def tail_deselect(self, arg=None):
        if cmds.ls("*:tail*"):
            bodyPart="tail"
            endPart="_FK_ctrl"
            self.select_function_tail(bodyPart, endPart)
        elif cmds.ls("*:*:tail*"):
            bodyPart="tail"
            endPart="_FK_ctrl"
            self.select_function_tail(bodyPart, endPart)
        elif cmds.ls("*:*:Tail*"):
            bodyPart="Tail"
            endPart="_FK_Ctrl"
            self.select_function_tail(bodyPart, endPart)
        elif cmds.ls("*:Tail*"):
            bodyPart="Tail"
            endPart="_FK_Ctrl"
            self.select_function_tail(bodyPart, endPart)
        
    def deselect_function_tail(self, bodyPart, endPart):
        getAsset=self.getName()       
        if getAsset==None:
            getBodyPart=cmds.ls(bodyPart+"*"+endPart)            
            if len(getBodyPart)>0:
                cmds.select(getBodyPart[0], add=1)
                for each in getBodyPart[1:]:
                    cmds.select(each, d=1)
        else:                
            getBodyPart=cmds.ls(getAsset+bodyPart+"*"+endPart) 
            if len(getBodyPart)>0:
                cmds.select(getBodyPart[0], add=1)
                for each in getBodyPart[1:]:
                    cmds.select(each, d=1) 
                        
    def select_face_function_multi(self, bodyPart):
        getAsset=self.getFaceName()
        querySel=cmds.optionMenu(SeModeMenu, q=1, sl=1)  
        if querySel==1:                 
            if getAsset==None:
                getBodyPart=cmds.ls(bodyPart[0])            
                if len(getBodyPart)>0:
                    cmds.select(bodyPart[0])
                    for each in bodyPart[1:]:
                        cmds.select(each, add=1)
            else:                
                getBodyPart=cmds.ls(getAsset+bodyPart[0]) 
                if len(getBodyPart)>0:
                    cmds.select(getAsset+bodyPart[0])
                    for each in bodyPart[1:]:
                        cmds.select(getAsset+each, add=1)  
        if querySel==2:                      
            if getAsset==None:
                getBodyPart=cmds.ls(bodyPart[0])            
                if len(getBodyPart)>0:
                    cmds.select(bodyPart[0], add=1)
                    for each in bodyPart[1:]:
                        cmds.select(each, add=1)
            else:                
                getBodyPart=cmds.ls(getAsset+bodyPart[0]) 
                if len(getBodyPart)>0:
                    cmds.select(getAsset+bodyPart[0], add=1)
                    for each in bodyPart[1:]:
                        cmds.select(getAsset+each, add=1) 

    def select_double_function(self, firstBodyPart, secondaryBodyPart):
        getAsset=self.getName()
        querySel=cmds.optionMenu(SeModeMenu, q=1, sl=1)
        if querySel==1:                
            if getAsset==None:
                getRightHand=cmds.ls(firstBodyPart) 
                getRightHoof=cmds.ls(secondaryBodyPart)            
                if len(getRightHand)>0:
                    cmds.select(firstBodyPart)
                elif len(getRightHoof)>0:
                    cmds.select(secondaryBodyPart)  
            else:                
                getRightHand=cmds.ls(getAsset+firstBodyPart) 
                getRightHoof=cmds.ls(getAsset+secondaryBodyPart) 
                if len(getRightHand)>0:
                    cmds.select(getAsset+firstBodyPart)
                elif len(getRightHoof)>0:
                    cmds.select(getAsset+secondaryBodyPart) 
        if querySel==2:                      
            if getAsset==None:
                getRightHand=cmds.ls(firstBodyPart) 
                getRightHoof=cmds.ls(secondaryBodyPart)            
                if len(getRightHand)>0:
                    cmds.select(firstBodyPart, add=1)
                elif len(getRightHoof)>0:
                    cmds.select(secondaryBodyPart, add=1)  
            else:                
                getRightHand=cmds.ls(getAsset+firstBodyPart) 
                getRightHoof=cmds.ls(getAsset+secondaryBodyPart) 
                if len(getRightHand)>0:
                    cmds.select(getAsset+firstBodyPart, add=1)
                elif len(getRightHoof)>0:
                    cmds.select(getAsset+secondaryBodyPart, add=1)
                      
    def select_face_function(self, bodyPart):
        getAsset=self.getFaceName()
        querySel=cmds.optionMenu(SeModeMenu, q=1, sl=1)  
        if querySel==1:                 
            if getAsset==None:
                getBodyPart=cmds.ls(bodyPart)            
                if len(getBodyPart)>0:
                    cmds.select(bodyPart)
            else:                
                getBodyPart=cmds.ls(getAsset+bodyPart) 
                if len(getBodyPart)>0:
                    cmds.select(getAsset+bodyPart)
        if querySel==2:                      
            if getAsset==None:
                getBodyPart=cmds.ls(bodyPart)            
                if len(getBodyPart)>0:
                    cmds.select(bodyPart, add=1)
            else:                
                getBodyPart=cmds.ls(getAsset+bodyPart) 
                if len(getBodyPart)>0:
                    cmds.select(getAsset+bodyPart, add=1)
    def deselect_face_function(self, bodyPart):
        getAsset=self.getFaceName()                      
        if getAsset==None:
            getBodyPart=cmds.ls(bodyPart)            
            if len(getBodyPart)>0:
                cmds.select(bodyPart, d=1)
        else:                
            getBodyPart=cmds.ls(getAsset+bodyPart) 
            if len(getBodyPart)>0:
                cmds.select(getAsset+bodyPart, d=1)
    def select_face_function_add(self, bodyPart):
        getAsset=self.getFaceName()                      
        if getAsset==None:
            getBodyPart=cmds.ls(bodyPart)            
            if len(getBodyPart)>0:
                cmds.select(bodyPart, add=1)
        else:                
            getBodyPart=cmds.ls(getAsset+bodyPart) 
            if len(getBodyPart)>0:
                cmds.select(getAsset+bodyPart, add=1)
 
                
    def _select_all_mouth(self, arg=None):
        groupSelect=[
                    Lip_T,
                    Lip_T_L,
                    Lip_C_L,
                    Lip_B_R,
                    Lip_B,
                    Lip_B_L, 
                    Lip_C_R,
                    Lip_T_R,
                    Teeth_B,
                    Teeth_T, 
                    Tongue_5,     
                    Tongue_4,       
                    Tongue_3, 
                    Tongue_2,    
                    Tongue_1,
                    Tongue_Main,
                    Emot_R_CC,
                    Emot_L_CC,
                    Jaw_CC,
                    CheekBone_R,
                    Cheek_R,
                    Cheek_T_R,
                    Nose_R,
                    CheekBone_L,
                    Cheek_L,
                    Cheek_T_L,
                    Nose_L,
                    Nose,                  
                    Jaw_L,
                    Jaw_R,
                    Phonemes,                             
                    ]
        self.select_face_function_multi(groupSelect)       
        self.select_function_add(Chin)
       
    def _select_mouth(self, arg=None):
        groupSelect=[
                    Lip_T,
                    Lip_T_L,
                    Lip_C_L,
                    Lip_B_R,
                    Lip_B,
                    Lip_B_L, 
                    Lip_C_R,
                    Lip_T_R,
#                     Teeth_B,
#                     Teeth_T, 
#                     Tongue_5,     
#                     Tongue_4,       
#                     Tongue_3, 
#                     Tongue_2,    
#                     Tongue_1,
#                     Tongue_Main,  
#                     Chin,              
                    ]
        self.select_face_function_multi(groupSelect)


    def _selectFaceUpper(self, arg=None):
        groupSelect=[
                    Brow_5_R,
                    Brow_4_R,
                    Brow_3_R,
                    Brow_2_R,
                    Brow_1_R,
                    Brow_5_L,
                    Brow_4_L,
                    Brow_3_L,
                    Brow_2_L,
                    Brow_1_L,
                    Brow_R_CC,
                    Brow_L_CC,
                    Lid_2_B_R,
                    Lid_3_B_R,
                    Lid_4_B_R,
                    Lid_5_B_R,
                    Lid_4_T_R,
                    Lid_3_T_R,
                    Lid_2_T_R,
                    Lid_2_B_L,
                    Lid_3_B_L,
                    Lid_4_B_L,
                    Lid_5_B_L,
                    Lid_4_T_L,
                    Lid_3_T_L,
                    Lid_2_T_L                    
                    ]
        groupSelect=groupSelect+Lashes_R
        groupSelect=groupSelect+Lashes_L
        self.select_face_function_multi(groupSelect)
        self.select_function_add(EyeMask)
        
    def _selectBrows(self, arg=None):
        groupSelect=[
                    Brow_5_R,
                    Brow_4_R,
                    Brow_3_R,
                    Brow_2_R,
                    Brow_1_R,
                    Brow_5_L,
                    Brow_4_L,
                    Brow_3_L,
                    Brow_2_L,
                    Brow_1_L,
                    Brow_R_CC,
                    Brow_L_CC
                    ]
        self.select_face_function_multi(groupSelect)
    def _selectRBrow(self, arg=None):
        groupSelect=[
                    Brow_5_R,
                    Brow_4_R,
                    Brow_3_R,
                    Brow_2_R,
                    Brow_1_R
                    ]
        self.select_face_function_multi(groupSelect)
        
    def _selectLBrow(self, arg=None):
        groupSelect=[
                    Brow_5_L,
                    Brow_4_L,
                    Brow_3_L,
                    Brow_2_L,
                    Brow_1_L
                    ]
        self.select_face_function_multi(groupSelect)

    def _selectEyes(self, arg=None):
        groupSelect=[
                    Lid_2_B_R,
                    Lid_3_B_R,
                    Lid_4_B_R,
                    Lid_5_B_R,
                    Lid_4_T_R,
                    Lid_3_T_R,
                    Lid_2_T_R,
                    Lid_2_B_L,
                    Lid_3_B_L,
                    Lid_4_B_L,
                    Lid_5_B_L,
                    Lid_4_T_L,
                    Lid_3_T_L,
                    Lid_2_T_L                    
                    ]
        self.select_face_function_multi(groupSelect)
    def _selectREye(self, arg=None):
        groupSelect=[
                    Lid_2_B_R,
                    Lid_3_B_R,
                    Lid_4_B_R,
                    Lid_5_B_R,
                    Lid_4_T_R,
                    Lid_3_T_R,
                    Lid_2_T_R
                    ]
        self.select_face_function_multi(groupSelect)
        
    def _selectLEye(self, arg=None):
        groupSelect=[
                    Lid_2_B_L,
                    Lid_3_B_L,
                    Lid_4_B_L,
                    Lid_5_B_L,
                    Lid_4_T_L,
                    Lid_3_T_L,
                    Lid_2_T_L
                    ]
        self.select_face_function_multi(groupSelect)

    def _fingers_L(self, arg=None):
        groupSelect=[
                    Finger_Mid_L,
                    Finger_Index_L,
                    Finger_Ring_L,
                    Finger_Pinky_L,
                    Thumb_Base_L,
                    Thumb_Mid_L
                    ]
        self.select_function_multi(groupSelect)
        
    def _fingers_R(self, arg=None):
        groupSelect=[
                    Finger_Mid_R,
                    Finger_Index_R,
                    Finger_Ring_R,
                    Finger_Pinky_R,
                    Thumb_Base_R,
                    Thumb_Mid_R
                    ]
        self.select_function_multi(groupSelect)
    def _Lash_R(self, arg=None):
        print Lashes_R
        self.select_face_function_multi(Lashes_R)
    def _Lash_L(self, arg=None):
        print Lashes_L
        self.select_face_function_multi(Lashes_L)
    def _Blink(self, arg=None):
        groupSelect=[
                    Lid_2_B_L,
                    Lid_3_B_L,
                    Lid_4_B_L,
                    Lid_5_B_L,
                    Lid_4_T_L,
                    Lid_3_T_L,
                    Lid_2_T_L,        
                    Lid_2_B_R,
                    Lid_3_B_R,
                    Lid_4_B_R,
                    Lid_5_B_R,
                    Lid_4_T_R,
                    Lid_3_T_R,
                    Lid_2_T_R,
                    ]
        groupSelect=groupSelect+Lashes_L
        groupSelect=groupSelect+Lashes_R   
        print groupSelect    
        self.select_face_function_multi(groupSelect)
        self.select_function_add(EyeMask)
                 

    def Phonemes(self, arg=None): 
        self.select_face_function(Phonemes)  
        
    def Teeth_Handle_B_Ctrl(self, arg=None):                                
        self.select_face_function(Teeth_B)
          
    def Teeth_Handle_T_Ctrl(self, arg=None):   
        self.select_face_function(Teeth_T)
        
    def Tongue05_Ctrl(self, arg=None): 
        self.select_face_function(Tongue_5)
        
          
    def Tongue04_Ctrl(self, arg=None): 
        self.select_face_function(Tongue_4)    
         
    def Tongue03_Ctrl(self, arg=None): 
        self.select_face_function(Tongue_3) 
          
    def Tongue02_Ctrl(self, arg=None): 
        self.select_face_function(Tongue_2) 
        
    def Tongue01_Ctrl(self, arg=None): 
        self.select_face_function(Tongue_1)
          
    def Tongue_Master_Ctrl(self, arg=None): 
        self.select_face_function(Tongue_Main)
        
    def Chin_Ctrl(self, arg=None):  
        self.select_function(Chin) 
    
    def Lip_Corner_R_Ctrl(self, arg=None):        
        self.select_face_function(Lip_C_R)
    
    def Lip_T_R_Ctrl(self, arg=None):   
        self.select_face_function(Lip_T_R)
    
    def Lip_T_Ctrl(self, arg=None):     
        self.select_face_function(Lip_T)
    
    def Lip_T_L_Ctrl(self, arg=None):        
        self.select_face_function(Lip_T_L)
    
    def Lip_Corner_L_Ctrl(self, arg=None):         
        self.select_face_function(Lip_C_L)
        
    def Lip_B_R_Ctrl(self, arg=None):        
        self.select_face_function(Lip_B_R)  
           
    def Lip_B_Ctrl(self, arg=None):        
        self.select_face_function(Lip_B)    
    
    def Lip_B_L_Ctrl(self, arg=None):      
        self.select_face_function(Lip_B_L)
    
    def Nose_Ctrl(self, arg=None): 
        self.select_face_function(Nose)


    def CheekBone_R_Ctrl(self, arg=None):      
        self.select_face_function(CheekBone_R)
        
    def Cheek_R_Ctrl(self, arg=None):     
        self.select_face_function(Cheek_R)
        
    def Cheek_T_R_Ctrl(self, arg=None):      
        self.select_face_function(Cheek_T_R)
        
    def Nose_R_Ctrl(self, arg=None):      
        self.select_face_function(Nose_R)


    def CheekBone_L_Ctrl(self, arg=None):       
        self.select_face_function(CheekBone_L)
        
    def Cheek_L_Ctrl(self, arg=None):      
        self.select_face_function(Cheek_L)
        
    def Cheek_T_L_Ctrl(self, arg=None):       
        self.select_face_function(Cheek_T_L)
        
    def Nose_L_Ctrl(self, arg=None):       
        self.select_face_function(Nose_L)
        
    def Jaw_L_Ctrl(self, arg=None):   
        self.select_face_function(Jaw_L)
    def Jaw_R_Ctrl(self, arg=None): 
        self.select_face_function(Jaw_R)


    def Lid_Open02_B_R_Ctrl(self, arg=None): 
        self.select_face_function(Lid_2_B_R)  
                  
    def Lid_Open03_B_R_Ctrl(self, arg=None):               
        self.select_face_function(Lid_3_B_R)  

    def Lid_Open04_B_R_Ctrl(self, arg=None):       
        self.select_face_function(Lid_4_B_R)         
        
    def Lid_Open05_B_R_Ctrl(self, arg=None):     
        self.select_face_function(Lid_5_B_R) 

    def Lid_Open04_T_R_Ctrl(self, arg=None):       
        self.select_face_function(Lid_4_T_R) 
                
    def Lid_Open03_T_R_Ctrl(self, arg=None):     
        self.select_face_function(Lid_3_T_R)        
        
    def Lid_Open02_T_R_Ctrl(self, arg=None): 
        self.select_face_function(Lid_2_T_R)

        
    def Lid_Open02_B_L_Ctrl(self, arg=None): 
        self.select_face_function(Lid_2_B_L)  
                  
    def Lid_Open03_B_L_Ctrl(self, arg=None):               
        self.select_face_function(Lid_3_B_L)  

    def Lid_Open04_B_L_Ctrl(self, arg=None):       
        self.select_face_function(Lid_4_B_L)         
        
    def Lid_Open05_B_L_Ctrl(self, arg=None):     
        self.select_face_function(Lid_5_B_L) 

    def Lid_Open04_T_L_Ctrl(self, arg=None):       
        self.select_face_function(Lid_4_T_L) 
                
    def Lid_Open03_T_L_Ctrl(self, arg=None):     
        self.select_face_function(Lid_3_T_L)        
        
    def Lid_Open02_T_L_Ctrl(self, arg=None): 
        self.select_face_function(Lid_2_T_L)

    def _brow05_R(self, arg=None): 
        self.select_face_function(Brow_5_R)
                
    def _brow04_R(self, arg=None): 
        self.select_face_function(Brow_4_R)
        
    def _brow03_R(self, arg=None): 
        self.select_face_function(Brow_3_R)
        
    def _brow02_R(self, arg=None): 
        self.select_face_function(Brow_2_R)
        
    def _brow01_R(self, arg=None): 
        self.select_face_function(Brow_1_R)

        
    def _brow05_L(self, arg=None): 
        self.select_face_function(Brow_5_L)
                
    def _brow04_L(self, arg=None): 
        self.select_face_function(Brow_4_L)
        
    def _brow03_L(self, arg=None): 
        self.select_face_function(Brow_3_L)
        
    def _brow02_L(self, arg=None): 
        self.select_face_function(Brow_2_L)
        
    def _brow01_L(self, arg=None): 
        self.select_face_function(Brow_1_L)

    def _talus_L(self, arg=None):    
        self.select_function(Talus_L)
        
    def _talus_R(self, arg=None):        
        self.select_function(Talus_R)
        
    def _knee_L(self, arg=None):    
        self.select_function(Knee_R)
        
    def _knee_R(self, arg=None):    
        self.select_function(Knee_R)
        
    def _hip_L(self, arg=None):    
        self.select_function(Hip_L)
        
    def _hip_R(self, arg=None):       
        self.select_function(Hip_R)        
        
    def _wrist_L(self, arg=None): 
        self.select_function(Wrist_L)
        
    def _wrist_R(self, arg=None): 
        self.select_function(Wrist_R)

    def _elbow_L(self, arg=None):      
        self.select_function(Elbow_L)
        
    def _elbow_R(self, arg=None):        
        self.select_function(Elbow_R)
        
    def _Shoulder_L(self, arg=None):        
        self.select_function(Shoulder_L)
        
    def _Shoulder_R(self, arg=None): 
        self.select_function(Shoulder_R)
        
    def _hand_L(self, arg=None): 
        self.select_function(Hand_Fingers_L)
        
    def _hand_R(self, arg=None):       
        self.select_function(Hand_Fingers_R)

    def _head(self, arg=None): 
        self.select_function(Head)
        
    def _neck(self, arg=None):   
        self.select_function(Neck)
        
    def _chest_ik(self, arg=None): 
        self.select_function(Chest_IK)
        
    def _body(self, arg=None): 
        self.select_double_function(BipedBody, QuadBody)

    def _pole_L_arm(self, arg=None):       
        self.select_function(Elbow_Pole_L)

    def _pole_R_arm(self, arg=None): 
        self.select_function(Elbow_Pole_R)

    def _pole_L_leg(self, arg=None):        
        self.select_function(Knee_Pole_L)

    def _pole_R_leg(self, arg=None):
        self.select_function(Knee_Pole_R)

    def _main_select(self, arg=None): 
        self.select_function(Main)
        
    def _master_select(self, arg=None):   
        self.select_function(Master)
        
    def _hips_select(self, arg=None):         
        self.select_function(Hips)
        
    def _eyemask(self, arg=None): 
        self.select_function(EyeMask)
        
    def _arm_L_Collar(self, arg=None): 
        self.select_function(ArmCollar_R)
                    
    def _arm_R_Collar(self, arg=None): 
        self.select_function(ArmCollar_L)

    def Finger_Index_L(self, arg=None): 
        self.select_function(Finger_Index_L)

    def Finger_Mid_L(self, arg=None): 
        self.select_function(Finger_Mid_L)

    def Finger_Ring_L(self, arg=None): 
        self.select_function(Finger_Ring_L)
        
    def Finger_Pinky_L(self, arg=None): 
        self.select_function(Finger_Pinky_L)
        
    def Thumb_Base_L(self, arg=None): 
        self.select_function(Thumb_Base_L)
        
    def Thumb_Mid_L(self, arg=None): 
        self.select_function(Thumb_Mid_L)
    def Finger_Index_R(self, arg=None): 
        self.select_function(Finger_Index_R)

    def Finger_Mid_R(self, arg=None): 
        self.select_function(Finger_Mid_R)

    def Finger_Ring_R(self, arg=None): 
        self.select_function(Finger_Ring_R)
        
    def Finger_Pinky_R(self, arg=None): 
        self.select_function(Finger_Pinky_R)
        
    def Thumb_Base_R(self, arg=None): 
        self.select_function(Thumb_Base_R)
        
    def Thumb_Mid_R(self, arg=None): 
        self.select_function(Thumb_Mid_R)


        
    def _arm_R_hand(self, arg=None): 
        self.select_double_function(Hand_IK_R, Hoof_Front_IK_R)           
                     
    def _arm_L_hand(self, arg=None): 
        self.select_double_function(Hand_IK_L, Hoof_Front_IK_L)
                  
    def _Foot_IK_L_heel(self, arg=None): 
        self.select_double_function(Foot_IK_L, Hoof_Rear_IK_L)
                        
    def _Foot_IK_R_heel(self, arg=None):
        self.select_double_function(Foot_IK_R, Hoof_Rear_IK_R)   
                

    def select_function_sets(self, arg=None):
        print "nothing"


    def _selectBody(self, arg=None):
        try:
            getSel=cmds.ls(sl=1)[0]
            if len(getSel)>0:
                pass
        except:
            print "select something"
            return
        testSceneType=cmds.ls("Armcollar_IK_L_Ctrl")            
        if len(testSceneType)>0:
            cmds.select("BodyControllers") 
            cmds.select("FaceControllers", add=1) 
        else:           
            getAsset=self.getName() 
            cmds.select(getAsset+"BodyControllers")
            cmds.select(getAsset+"FaceControllers", add=1)                          
        self.deselect_function(Chin)                          

    def _selectBodyWhole(self, arg=None):
        try:
            getSel=cmds.ls(sl=1)[0]
            if len(getSel)>0:
                pass
        except:
            print "select something"
            return
        testSceneType=cmds.ls("Brow01_R_Ctrl")
        if len(testSceneType)>0:
            cmds.select("FaceAnimCtrls")
            cmds.select("FaceControlBBox", add=1)
        else:
            getAsset=self.getFaceName()  
            cmds.select(getAsset+"FaceAnimCtrls")
            cmds.select(getAsset+"FaceControlBBox", add=1) 
        testSceneType=cmds.ls("Armcollar_IK_L_Ctrl")            
        if len(testSceneType)>0:
            cmds.select("BodyControllers", add=1) 
            cmds.select("FaceControllers", add=1) 
        else:           
            getAsset=self.getName() 
            cmds.select(getAsset+"BodyControllers", add=1)
            cmds.select(getAsset+"FaceControllers", add=1)      
        self.tail_deselect()
                   
    def _selectFaceWhole(self, arg=None):
        try:
            getSel=cmds.ls(sl=1)[0]
            if len(getSel)>0:
                pass
        except:
            print "select something"
            return
        testSceneType=cmds.ls("Brow01_R_Ctrl")
        if len(testSceneType)>0:
            cmds.select("FaceAnimCtrls")
            cmds.select("FaceControlBBox", add=1)           
            self.select_function_add(Chin)
            self.select_function_add(EyeMask)
            for each in Lashes_R:
                self.select_face_function_add(each)
            for each in Lashes_L:
                self.select_face_function_add(each)
            self.deselect_face_function("BigBox_CC")
        else:
            getAsset=self.getFaceName()  
            cmds.select(getAsset+"FaceAnimCtrls")
            cmds.select(getAsset+"FaceControlBBox", add=1)            
            self.select_function_add(Chin)
            self.select_function_add(EyeMask)
            for each in Lashes_R:
                self.select_face_function_add(each)
            for each in Lashes_L:
                self.select_face_function_add(each)
            self.deselect_face_function("BigBox_CC")
            
    def _selectFace(self, arg=None):
        self.select_face_function(FaceAnimControls)
        self.select_function_add(Chin) 

    def _selectControlBox(self, arg=None):
        self.select_face_function(FaceControlBoxSet)


    def _select_mouth(self, arg=None):
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup()    
        getClass.selectAnimMouth()
         
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


inst = SchematicSelect()
inst.create()

