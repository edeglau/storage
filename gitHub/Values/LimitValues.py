import maya.cmds as cmds
from functools import partial
from string import *
import re, glob
import maya.mel
import os, subprocess, sys, platform
from os  import popen
from sys import stdin
#import win32clipboard
import operator

'''MG rigging modules'''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons License'
'http://creativecommons.org/licenses/by-sa/3.0/au/'


pipelineguides="G:\\_PIPELINE_MANAGEMENT\\Published\\maya\\values\\"
filepath= os.getcwd()

sys.path.append(str(filepath))
getfilePath=str(__file__)
gtepiece=getfilePath.split("\\")
getRigModPath='\\'.join(gtepiece[:-2])+"\\rigmodules\\"

#filepath=( 'D:\\code\\git\\LiquidGit\\Liquid_egit\\guides\\' )

getScenePath=cmds.file(q=1, location=1)
getPathSplit=getScenePath.split("/")
folderPath='\\'.join(getPathSplit[:-1])+"\\"

sys.path.append(str(getRigModPath))
import baseFunctions_maya
reload (baseFunctions_maya)
getClass=baseFunctions_maya.BaseClass()

guideFolderPath=folderPath+"Guides\\"
valueFolderPath=folderPath+"Values\\"
infFolderPath=folderPath+"Influences\\"
xmlFolderPath=folderPath+"XMLskinWeights\\"
# filepath= os.getcwd()
# sys.path.append(str(filepath))

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
Chin="Chin_Ctrl"    
BodySet="BodyControllers"
FaceSet="FaceControllers"
FaceAnimControls="FaceAnimCtrls"
FaceControlBoxSet="FaceControlBBox"


class ValueClass(object):
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
        global txcheckMin
        global minTXValue
        global maxTXValue
        global txcheckMax
        global txcheckCB
        global txcheckkey
        global txchecklock
        global tycheckMin
        global minTYValue
        global maxTYValue
        global tycheckMax
        global tycheckCB
        global tycheckkey
        global tychecklock
        global tzcheckMin
        global minTZValue
        global maxTZValue
        global tzcheckMax
        global tzcheckCB
        global tzcheckkey
        global tzchecklock
        global rxcheckMin
        global minrxValue
        global maxRXValue
        global rxcheckMax
        global rxcheckCB
        global rxcheckkey
        global rxchecklock 
        global rycheckMin
        global minRYValue
        global maxRYValue
        global rycheckMax
        global rycheckCB
        global rycheckkey
        global rychecklock
        global rzcheckMin
        global minRZValue
        global maxRZValue
        global rzcheckMax
        global rzcheckCB
        global rzcheckkey
        global rzchecklock
        self.window = cmds.window(self.winName, title=self.winTitle, tbm=1, w=300, h=800 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=300)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')

        cmds.rowLayout  (' rMainRow ', w=350, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('txvalues', p='selectArrayColumn', numberOfColumns=14,cellWidthHeight=(37, 18))  
        cmds.text(label="", w=10)
        cmds.text(label="min")  
        cmds.text(label="min") 
        cmds.text(label="") 
        cmds.text(label="max")
        cmds.text(label="max")  
        cmds.text(label="cb")  
        cmds.text(label="key") 
        cmds.text(label="lock")  
        cmds.gridLayout('txvaluemeter', p='selectArrayColumn', numberOfColumns=14, cellWidthHeight=(30, 18)) 
        cmds.text(label="tx") 
        cmds.text(label="")
        self.txcheckMin=cmds.checkBox(label="", p='txvaluemeter',w=1, al="middle")
        self.minTXValue=cmds.textField(w=40, h=25, p='txvaluemeter')
        cmds.text(label="")
        self.maxTXValue=cmds.textField(w=40, h=25, p='txvaluemeter')
        cmds.text(label="")
        self.txcheckMax=cmds.checkBox(label="", p='txvaluemeter')
        self.txcheckCB=cmds.checkBox(label="", p='txvaluemeter',value=1)
        self.txcheckkey=cmds.checkBox(label="", p='txvaluemeter', value=1)
        self.txchecklock=cmds.checkBox(label="", p='txvaluemeter', value=0)
        cmds.gridLayout('tyvaluemeter', p='selectArrayColumn', numberOfColumns=14, cellWidthHeight=(30, 18)) 
        cmds.text(label="ty") 
        cmds.text(label="")
        self.tycheckMin=cmds.checkBox(label="", p='tyvaluemeter',w=1, al="middle")
        self.minTYValue=cmds.textField(w=10, h=25, p='tyvaluemeter')
        cmds.text(label="")
        self.maxTYValue=cmds.textField(w=10, h=25, p='tyvaluemeter')
        cmds.text(label="")
        self.tycheckMax=cmds.checkBox(label="", p='tyvaluemeter')
        self.tycheckCB=cmds.checkBox(label="", p='tyvaluemeter',value=1)
        self.tycheckkey=cmds.checkBox(label="", p='tyvaluemeter', value=1)
        self.tychecklock=cmds.checkBox(label="", p='tyvaluemeter', value=0)
        cmds.gridLayout('tzvaluemeter', p='selectArrayColumn', numberOfColumns=14, cellWidthHeight=(30, 18)) 
        cmds.text(label="tz") 
        cmds.text(label="")
        self.tzcheckMin=cmds.checkBox(label="", p='tzvaluemeter',w=1, al="middle")
        self.minTZValue=cmds.textField(w=10, h=25, p='tzvaluemeter')
        cmds.text(label="")
        self.maxTZValue=cmds.textField(w=10, h=25, p='tzvaluemeter')
        cmds.text(label="")
        self.tzcheckMax=cmds.checkBox(label="", p='tzvaluemeter')
        self.tzcheckCB=cmds.checkBox(label="", p='tzvaluemeter',value=1)
        self.tzcheckkey=cmds.checkBox(label="", p='tzvaluemeter', value=1)
        self.tzchecklock=cmds.checkBox(label="", p='tzvaluemeter', value=0)
        cmds.gridLayout('rxvaluemeter', p='selectArrayColumn', numberOfColumns=14, cellWidthHeight=(30, 18)) 
        cmds.text(label="rx") 
        cmds.text(label="")
        self.rxcheckMin=cmds.checkBox(label="", p='rxvaluemeter',w=1, al="middle")
        self.minRXValue=cmds.textField(w=10, h=25, p='rxvaluemeter')
        cmds.text(label="")
        self.maxRXValue=cmds.textField(w=10, h=25, p='rxvaluemeter')
        cmds.text(label="")
        self.rxcheckMax=cmds.checkBox(label="", p='rxvaluemeter')
        self.rxcheckCB=cmds.checkBox(label="", p='rxvaluemeter',value=1)
        self.rxcheckkey=cmds.checkBox(label="", p='rxvaluemeter', value=1)
        self.rxchecklock=cmds.checkBox(label="", p='rxvaluemeter', value=0)
        cmds.gridLayout('ryvaluemeter', p='selectArrayColumn', numberOfColumns=14, cellWidthHeight=(30, 18)) 
        cmds.text(label="ry") 
        cmds.text(label="")
        self.rycheckMin=cmds.checkBox(label="", p='ryvaluemeter',w=1, al="middle")
        self.minRYValue=cmds.textField(w=10, h=25, p='ryvaluemeter')
        cmds.text(label="")
        self.maxRYValue=cmds.textField(w=10, h=25, p='ryvaluemeter')
        cmds.text(label="")
        self.rycheckMax=cmds.checkBox(label="", p='ryvaluemeter')
        self.rycheckCB=cmds.checkBox(label="", p='ryvaluemeter',value=1)
        self.rycheckkey=cmds.checkBox(label="", p='ryvaluemeter', value=1)
        self.rychecklock=cmds.checkBox(label="", p='ryvaluemeter', value=0)
        cmds.gridLayout('rzvaluemeter', p='selectArrayColumn', numberOfColumns=14, cellWidthHeight=(30, 18)) 
        cmds.text(label="rz") 
        cmds.text(label="")
        self.rzcheckMin=cmds.checkBox(label="", p='rzvaluemeter',w=1, al="middle")
        self.minRZValue=cmds.textField(w=10, h=25, p='rzvaluemeter')
        cmds.text(label="")
        self.maxRZValue=cmds.textField(w=10, h=25, p='rzvaluemeter')
        cmds.text(label="")
        self.rzcheckMax=cmds.checkBox(label="", p='rzvaluemeter')
        self.rzcheckCB=cmds.checkBox(label="", p='rzvaluemeter',value=1)
        self.rzcheckkey=cmds.checkBox(label="", p='rzvaluemeter', value=1)
        self.rzchecklock=cmds.checkBox(label="", p='rzvaluemeter', value=0)
        cmds.gridLayout('valuebutton', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(120, 18))    
        cmds.button (label='GetValues', w=240, bgc=[0.7, 0.7, 0.7], p='valuebutton', command = lambda *args:self.getValues())    
        cmds.button (label='SetValues', w=240, bgc=[0.7, 0.7, 0.7], p='valuebutton', command = lambda *args:self.setValues())
        cmds.text(label="values", p='selectArrayColumn') 
        cmds.gridLayout('listValueButtons' , p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(120, 20))                          
        cmds.button (label='Clean Values ',bgc=[0.7, 0.7, 0.7], p='listValueButtons', command = self._clean_values)                          
        cmds.button (label='Reset channels ',bgc=[0.7, 0.7, 0.7], p='listValueButtons', command = self._reset_cb)                          
        cmds.button (label='Save Values',bgc=[0.6, 0.65, 0.65], p='listValueButtons', command = self.save_guides)
        cmds.button (label='Open Values',bgc=[0.6, 0.65, 0.65], p='listValueButtons', command = self.open_guides)            
        cmds.gridLayout('dropdown', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(240, 18)) 
        SeModeMenu=cmds.optionMenu( label='Select Mode')
        cmds.menuItem( label='Replace' )
        cmds.menuItem( label='Add' )       
        cmds.text(label="")
        cmds.gridLayout('bodyButton', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(120, 18)) 
        cmds.button (label='Select body', bgc=[.1, .1,.1], p='bodyButton', command = self._selectBody)          
        cmds.button (label='Select whole body', bgc=[.1, .1,.1], p='bodyButton', command = self._selectBodyWhole)          
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(120, 18))
        cmds.button (label='EyeMask*', bgc=[.5, .5, 0.0], p='listBuildButtonLayout', command = self._eyemask)               
        cmds.button (label='Chin', bgc=[.5, .5, 0.0], p='listBuildButtonLayout', command = self.Chin_Ctrl)        
        cmds.button (label='Head_Ctrl', bgc=[0.0, .5, .5], p='listBuildButtonLayout', command = self._head) 
        cmds.button (label='Neck_Ctrl', bgc=[0.0, .5, .5], p='listBuildButtonLayout', command = self._neck)        
        cmds.button (label='Chest_Ctrl', bgc=[0.0, .5, .5], p='listBuildButtonLayout', command = self._chest_ik) 
        cmds.button (label='Body_Ctrl', bgc=[0.0, .5, .5], p='listBuildButtonLayout', command = self._body) 
        cmds.button (label='Hips_Ctrl*', p='listBuildButtonLayout', bgc=[0.0, .5, .5], command = self._hips_select)                             
        cmds.button (label='Armcollar_R_Ctrl*', bgc=[.5, 0.0, 0.0], p='listBuildButtonLayout', command = self._arm_R_Collar) 
        cmds.button (label='Armcollar_L_Ctrl*', bgc=[.5, 0.0, 0.0], p='listBuildButtonLayout', command = self._arm_L_Collar)        
        cmds.text(label="")
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
        cmds.text (label='Author: Elise Deglau',w=120, al='left', p='selectArrayColumn')
      
        #cmds.separator()
        cmds.text(label="")
              
        cmds.showWindow(self.window)




    def select_function_add(self, bodyPart):
        getAsset=cmds.ls(bodyPart[0])
        if getAsset==None:
            getBodyPart=cmds.ls(bodyPart)            
            if len(getBodyPart)>0:
                cmds.select(bodyPart, add=1)
        else:                
            getBodyPart=cmds.ls(getAsset+bodyPart) 
            if len(getBodyPart)>0:
                cmds.select(getAsset+bodyPart, add=1)

        
    def getRigName(self, arg=None):
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
        querySel=cmds.optionMenu(SeModeMenu, q=1, sl=1)
        if querySel==1:
            cmds.select(bodyPart)      
        elif querySel==2:          
            cmds.select(bodyPart, add=1)
                    
    def deselect_function(self, bodyPart): 
        cmds.select(bodyPart, d=1)

    def select_function_multi(self, bodyPart):
        querySel=cmds.optionMenu(SeModeMenu, q=1, sl=1)
        if querySel==1:
            cmds.select(bodyPart[0])
            for each in bodyPart[1:]:
                cmds.select(each, add=1)                       
        elif querySel==2:          
            cmds.select(bodyPart[0], add=1)
            for each in bodyPart[1:]:
                cmds.select(each, add=1)
                        
    def select_double_function(self, firstBodyPart, secondaryBodyPart):
        if cmds.ls(firstBodyPart):
            getAsset=cmds.ls(firstBodyPart)
        elif cmds.ls(secondaryBodyPart):
            getAsset=cmds.ls(secondaryBodyPart)
        querySel=cmds.optionMenu(SeModeMenu, q=1, sl=1)
        if querySel==1:                
            cmds.select(getAsset) 
        if querySel==2:                         
            cmds.select(getAsset, add=1) 

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

    def Chin_Ctrl(self, arg=None):  
        self.select_function(Chin) 

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
            getAsset=self.getRigName() 
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
            getAsset=self.getRigName() 
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




           
            

    def save_guides(self, arg=None):  
        winName = "Save guides filename"
        winTitle = winName
        global fileName
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)

        window = cmds.window(winName, title=winTitle, tbm=1, w=250, h=200 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=250)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        
        cmds.rowLayout  (' rMainRow ', w=250, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=1, cellWidthHeight=(200, 20))    
        fileName=cmds.textField(w=200, h=25, p='listBuildButtonLayout')    
        cmds.button (label='SaveInProject', p='listBuildButtonLayout', command = lambda *args:self._save_guide_function())
        cmds.button (label='SaveInPipelineGuides', p='listBuildButtonLayout', command = lambda *args:self._save_to_pipeline())        
        cmds.button (label='Open folder', p='listBuildButtonLayout', command = lambda *args:self._launch_exp_open(valueFolderPath))
        cmds.showWindow(window)            

    def _launch_exp_save(self, folderPath):
        destImagePath=cmds.textField(fileName, q=1, text=True)
        print destImagePath
        self.get_path(destImagePath)    
        
    def get_path(self, path):
        print path
        if '\\\\' in path:
            newpath=re.sub(r'\\\\',r'\\', path)
            print newpath
            os.startfile(r'\\'+newpath[1:])    
        else:
            os.startfile(path)
                     
    def _save_guide_function(self):
        filename=cmds.file(q=1, location=1)
        if getScenePath =="unknown":
            print "This file has not been saved into a location yet. Cannot determine where you want to put this."
            return
        else:
            pass        
        filename=cmds.textField(fileName, q=1, text=True)
        if filename:
            pass
        else:
            print "you need to give it a name"
            return    
        printFolder=valueFolderPath+filename+".txt"
        if not os.path.exists(valueFolderPath): os.makedirs(valueFolderPath)         
        self.guide_writer(printFolder)
        
    def _save_to_pipeline(self):
        filename=cmds.textField(fileName, q=1, text=True)
        if filename:
            pass
        else:
            print "you need to give it a name"
            return    
        printFolder=pipelineguides+filename+".txt"
        self.guide_writer(printFolder)
        

        
        #open file function
        if '\\\\' in printFolder:
            newpath=re.sub(r'\\\\',r'\\', printFolder)
            os.startfile(r'\\'+newpath[1:])    
        else:
            os.startfile(printFolder)
                        
    def open_guides(self, arg=None):    
        if valueFolderPath:
            pathFolder=valueFolderPath
            getPath=valueFolderPath+"*.*"
        else:
            getPath=folderPath+"*.*"
            pathFolder=folderPath
        print pathFolder
        files=glob.glob(getPath)   
        makeBucket=[] 
        for each in files:
            getfileName=each.split("\\")
            getFile=getfileName[-1:][0]
            makeBucket.append(getFile)
        winName = "Open guides filename"
        winTitle = winName
        global fileName
#         global fileSaveName
        global fileDropName
        openFolderPath=folderPath+"\\"
#         files=glob.glob(getPath)       
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)

        window = cmds.window(winName, title=winTitle, tbm=1, w=500, h=280 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=500)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        
        cmds.rowLayout  (' rMainRow ', w=500, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=1, cellWidthHeight=(480, 20))      
        fileDropName=cmds.optionMenu( label='files')
        for each in makeBucket:
            cmds.menuItem( label=each) 
        fileName=cmds.textField(w=120, h=25, p='listBuildButtonLayout')    
        cmds.button (label='refresh', p='listBuildButtonLayout', command = lambda *args:self._refresh_function())
        cmds.button (label='PipelineGuides', p='listBuildButtonLayout', command = lambda *args:self._pipeline_guides())
        cmds.button (label='Open', p='listBuildButtonLayout', command = lambda *args:self._open_guide_function())
        cmds.button (label='Open folder', p='listBuildButtonLayout', command = lambda *args:self._launch_exp_open(openFolderPath))
        cmds.showWindow(window)                 
    def _launch_exp_open(self, folderPath):
#         os.system('explorer'+folderPath)
        destImagePath=cmds.textField(fileName, q=1, text=True)
#         destImagePath=folderPath
        print destImagePath
        self.get_path(destImagePath)            
#         result = cmds.promptDialog( 
#                     title='Confirm', 
#                     message='open file', 
#                     button=['Continue','Cancel'],
#                     defaultButton='Continue', 
#                     cancelButton='Cancel', 
#                     dismissString='Cancel' )
#         if result == 'Continue':
#             filename=cmds.promptDialog(q=1)

    def _refresh_function(self):
        fileTextname=cmds.textField(fileName, q=1, text=True)
        fileTextname=fileTextname+"\\*.txt"
        files=glob.glob(fileTextname)
        makeBucket=[] 
        for each in files:
            getfileName=each.split("\\")
            getFile=getfileName[-1:][0]
            makeBucket.append(getFile)        
        cmds.optionMenu(fileDropName, e=1)
        for each in makeBucket:
            cmds.menuItem( label=each)
    def _pipeline_guides(self):
        fileTextname=pipelineguides+"\\*.txt"
        cmds.textField(fileName, edit=True, text=pipelineguides)
        files=glob.glob(fileTextname)
        makeBucket=[] 
        for each in files:
            getfileName=each.split("\\")
            getFile=getfileName[-1:][0]
            makeBucket.append(getFile)        
        cmds.optionMenu(fileDropName, e=1)
        for each in makeBucket:
            cmds.menuItem( label=each)        


    def guide_writer(self, printFolder):
        getGuides=cmds.ls(sl=1)
        getValueBucket=[]
        for each in getGuides:
            gettxValueInfo=cmds.transformLimits(each,  q=1,tx=1)
            gettxSwitchInfo=cmds.transformLimits(each, q=1, etx=1)
            get_tx_Value=[cmds.getAttr(each+'.tx', l=1 )]
            get_tx_Value.append(cmds.getAttr(each+'.tx', k=1 ))
            get_tx_Value.append(cmds.getAttr(each+'.tx', cb=1 ))
            get_tx_Value=str(get_tx_Value)
            gettyValueInfo=cmds.transformLimits(each,  q=1,ty=1)
            gettySwitchInfo=cmds.transformLimits(each, q=1, ety=1)
            get_ty_Value=[cmds.getAttr(each+'.ty', l=1 )]
            get_ty_Value.append(cmds.getAttr(each+'.ty', k=1 ))
            get_ty_Value.append(cmds.getAttr(each+'.ty', cb=1 ))
            get_ty_Value=str(get_ty_Value)
            gettzValueInfo=cmds.transformLimits(each,  q=1,tz=1)
            gettzSwitchInfo=cmds.transformLimits(each, q=1, etz=1)
            get_tz_Value=[cmds.getAttr(each+'.tz', l=1 )]
            get_tz_Value.append(cmds.getAttr(each+'.tz', k=1 ))
            get_tz_Value.append(cmds.getAttr(each+'.tz', cb=1 ))  
            get_tz_Value=str(get_tz_Value)         
            getrxValueInfo=cmds.transformLimits(each,  q=1,rx=1)
            getrxSwitchInfo=cmds.transformLimits(each, q=1, erx=1)
            get_rx_Value=[cmds.getAttr(each+'.rx', l=1 )]
            get_rx_Value.append(cmds.getAttr(each+'.rx', k=1 ))
            get_rx_Value.append(cmds.getAttr(each+'.rx', cb=1 ))
            get_rx_Value=str(get_rx_Value)  
            getryValueInfo=cmds.transformLimits(each,  q=1,ry=1)
            getrySwitchInfo=cmds.transformLimits(each, q=1, ery=1)
            get_ry_Value=[cmds.getAttr(each+'.ry', l=1 )]
            get_ry_Value.append(cmds.getAttr(each+'.ry', k=1 ))
            get_ry_Value.append(cmds.getAttr(each+'.ry', cb=1 ))
            get_ry_Value=str(get_ry_Value)  
            getrzValueInfo=cmds.transformLimits(each,  q=1,rz=1)
            getrzSwitchInfo=cmds.transformLimits(each, q=1, erz=1)
            get_rz_Value=[cmds.getAttr(each+'.rz', l=1 )]
            get_rz_Value.append(cmds.getAttr(each+'.rz', k=1 ))
            get_rz_Value.append(cmds.getAttr(each+'.rz', cb=1 ))
            get_rz_Value=str(get_rz_Value)
            getValue=each+":"+str(gettxValueInfo)+">>"+str(gettxSwitchInfo)+"<<"+get_tx_Value+":"+str(gettyValueInfo)+">>"+str(gettySwitchInfo)+"<<"+get_ty_Value+":"+str(gettzValueInfo)+">>"+str(gettzSwitchInfo)+"<<"+get_tz_Value+":"+str(getrxValueInfo)+">>"+str(getrxSwitchInfo)+"<<"+get_rx_Value+":"+str(getryValueInfo)+">>"+str(getrySwitchInfo)+"<<"+get_ry_Value+":"+str(getrzValueInfo)+">>"+str(getrzSwitchInfo)+"<<"+get_rz_Value
            getValueBucket.append(getValue)
        inp=open(printFolder, 'w+')            
        getName=each.split("|")[0]
        for item in getValueBucket:
            inp.write(str(item)+'\r\n')
        inp.close()  
        print "saved as "+printFolder

    def _open_guide_function(self):   
        guideDict={}
        getPath=cmds.textField(fileName, q=1, text=True)
        if getPath:
            pass
        else:
            print "no path entered"
            return
        filename=cmds.optionMenu(fileDropName, q=1, v=1)
        printFolder=getPath+"\\"+filename
#         if fileSaveName:
#             printFolder=fileSaveName
#         else:
#             printFolder=folderPath+filename
        print printFolder
        getName=filename.split(".")[0]
        inp=open(printFolder, 'r')
        
        List = open(printFolder).readlines()
        
        for each in List:   
            getDictParts=each.split(':')
            getDictValues=getDictParts[1:]
            divideCBStuff=getDictValues[0].split("<<")
            getCBValues=self.breakCBvalues(divideCBStuff[1])
            divideLimitValues=divideCBStuff[0].split(">>")
            getTwoLimitValues, getTwoLimitStates=self.breakUp(divideLimitValues)
            cmds.transformLimits(getDictParts[0], tx=[getTwoLimitValues[0], getTwoLimitValues[1]], etx=[getTwoLimitStates[0], getTwoLimitStates[1]])
            cmds.setAttr(getDictParts[0]+'.tx', lock=getCBValues[0])
            cmds.setAttr(getDictParts[0]+'.tx', cb=getCBValues[2])
            cmds.setAttr(getDictParts[0]+'.tx', k=getCBValues[1])            
            divideCBStuff=getDictValues[1].split("<<")
            getCBValues=self.breakCBvalues(divideCBStuff[1])
            divideLimitValues=divideCBStuff[0].split(">>")
            getTwoLimitValues, getTwoLimitStates=self.breakUp(divideLimitValues)
            cmds.transformLimits(getDictParts[0], ty=[getTwoLimitValues[0], getTwoLimitValues[1]], ety=[getTwoLimitStates[0], getTwoLimitStates[1]])
            cmds.setAttr(getDictParts[0]+'.ty', lock=getCBValues[0])
            cmds.setAttr(getDictParts[0]+'.ty', cb=getCBValues[2])  
            cmds.setAttr(getDictParts[0]+'.ty', k=getCBValues[1])                      
            divideCBStuff=getDictValues[2].split("<<")
            getCBValues=self.breakCBvalues(divideCBStuff[1])
            divideLimitValues=divideCBStuff[0].split(">>")
            getTwoLimitValues, getTwoLimitStates=self.breakUp(divideLimitValues)
            cmds.transformLimits(getDictParts[0], tz=[getTwoLimitValues[0], getTwoLimitValues[1]], etz=[getTwoLimitStates[0], getTwoLimitStates[1]])
            cmds.setAttr(getDictParts[0]+'.tz', lock=getCBValues[0])
            cmds.setAttr(getDictParts[0]+'.tz', cb=getCBValues[2])  
            cmds.setAttr(getDictParts[0]+'.tz', k=getCBValues[1])                         
            divideCBStuff=getDictValues[3].split("<<")
            getCBValues=self.breakCBvalues(divideCBStuff[1])
            divideLimitValues=divideCBStuff[0].split(">>")
            getTwoLimitValues, getTwoLimitStates=self.breakUp(divideLimitValues)
            cmds.transformLimits(getDictParts[0], rx=[getTwoLimitValues[0], getTwoLimitValues[1]], erx=[getTwoLimitStates[0], getTwoLimitStates[1]])
            cmds.setAttr(getDictParts[0]+'.rx', lock=getCBValues[0])
            cmds.setAttr(getDictParts[0]+'.rx', cb=getCBValues[2])   
            cmds.setAttr(getDictParts[0]+'.rx', k=getCBValues[1])             
            divideCBStuff=getDictValues[4].split("<<")
            getCBValues=self.breakCBvalues(divideCBStuff[1])
            divideLimitValues=divideCBStuff[0].split(">>")
            getTwoLimitValues, getTwoLimitStates=self.breakUp(divideLimitValues)
            cmds.transformLimits(getDictParts[0], ry=[getTwoLimitValues[0], getTwoLimitValues[1]], ery=[getTwoLimitStates[0], getTwoLimitStates[1]])
            cmds.setAttr(getDictParts[0]+'.ry', lock=getCBValues[0])
            cmds.setAttr(getDictParts[0]+'.ry', cb=getCBValues[2])     
            cmds.setAttr(getDictParts[0]+'.ry', k=getCBValues[1])           
            divideCBStuff=getDictValues[5].split("<<")
            getCBValues=self.breakCBvaluesLast(divideCBStuff[1])
            divideLimitValues=divideCBStuff[0].split(">>")
            getTwoLimitValues, getTwoLimitStates=self.breakUp(divideLimitValues)
            cmds.transformLimits(getDictParts[0], rz=[getTwoLimitValues[0], getTwoLimitValues[1]], erz=[getTwoLimitStates[0], getTwoLimitStates[1]])
            cmds.setAttr(getDictParts[0]+'.rz', lock=getCBValues[0])
            cmds.setAttr(getDictParts[0]+'.rz', cb=getCBValues[2])   
            cmds.setAttr(getDictParts[0]+'.rz', k=getCBValues[1])            

    def breakUp(self, divideLimitValues):
        getTXValues=divideLimitValues[0].strip('[]')
        getTwoLimitValues=getTXValues.split(', ')
        getTXLimits=divideLimitValues[1].strip('[]')
        getTwoLimitStates=getTXLimits.split(', ')
        getNewLimitNumberState=[]
        for each in getTwoLimitStates:
            if each=="False":
                each=int(0)
            elif each=="True":
                each=int(1)
            getNewLimitNumberState.append(each)
        return getTwoLimitValues, getNewLimitNumberState
    def breakCBvalues(self, divideLimitValues):
        getTXLimits=divideLimitValues.strip('[]')
        getCBtates=getTXLimits.split(', ')
        getNewLimitNumberState=[]
        for each in getCBtates:
            if each=="False":
                each=int(0)
            elif each=="True":
                each=int(1)
            getNewLimitNumberState.append(each)
        getNewLimitNumberState        
        return getNewLimitNumberState
    def breakCBvaluesLast(self, divideLimitValues):
        getTXLimits=divideLimitValues.strip('[]]\r\n')
        getCBtates=getTXLimits.split(', ')
        getNewLimitNumberState=[]
        for each in getCBtates:
            if each=="False":
                each=int(0)
            elif each=="True":
                each=int(1)
            getNewLimitNumberState.append(each)
        getNewLimitNumberState        
        return getNewLimitNumberState
#     def breakUpLast(self, divideLimitValues):
#         getTXValues=divideLimitValues[0].strip('[]')
#         getTwoLimitValues=getTXValues.split(', ')
#         getTXLimits=divideLimitValues[1].strip('[]]\r\n')
#         getCBtates=getTXLimits.split(', ')
#         getNewLimitNumberState=[]
#         for each in getCBtates:
#             if each=="False":
#                 each=int(0)
#             elif each=="True":
#                 each=int(1)
#             getNewLimitNumberState.append(each)
#         print getNewLimitNumberState        
#         return getTwoLimitValues, getNewLimitNumberState

    def _clean_values(self, arg=None):
        getSel=cmds.ls(sl=1)
        for each in getSel:
            cmds.transformLimits(each, tx=[-1, 1], etx=[0,0])
            cmds.transformLimits(each, ty=[-1, 1], ety=[0,0])
            cmds.transformLimits(each, tz=[-1, 1], etz=[0,0])
            cmds.transformLimits(each, rx=[-1, 1], erx=[0,0])
            cmds.transformLimits(each, ry=[-1, 1], ery=[0,0])
            cmds.transformLimits(each, rz=[-1, 1], erz=[0,0])
            
    def _reset_cb(self, arg=None):
        ChildAttributes=(".tx", ".ty", ".tz" , ".rx", ".ry", ".rz")
        getSel=cmds.ls(sl=1)
        for each in getSel:
            for item in ChildAttributes:
                cmds.setAttr(each+str(item), cb=True)
                cmds.setAttr(each+str(item), l=False)  
                cmds.setAttr(each+str(item), k=True)
                
#     def getValues(self, txcheckMin, minTXValue, maxTXValue, txcheckMax, txcheckCB, txcheckkey, txchecklock,
#                   tycheckMin, minTYValue, maxTYValue, tycheckMax, tycheckCB, tycheckkey, tychecklock,     
#                   tzcheckMin, minTZValue, maxTZValue, tzcheckMax, tzcheckCB, tzcheckkey, tzchecklock,    
#                   rxcheckMin, minrxValue, maxRXValue, rxcheckMax, rxcheckCB, rxcheckkey, rxchecklock, 
#                   rycheckMin, minRYValue, maxRYValue, rycheckMax, rycheckCB, rycheckkey, rychecklock,    
#                   rzcheckMin, minRZValue, maxRZValue, rzcheckMax, rzcheckCB, rzcheckkey, rzchecklock):
    def getValues(self):
        each=cmds.ls(sl=1)[0]
        gettxValueInfo=cmds.transformLimits(each,  q=1, tx=1)
        gettxSwitchInfo=cmds.transformLimits(each, q=1, etx=1)
        txchecklock=cmds.getAttr(each+'.tx', l=1)
        txcheckkey=cmds.getAttr(each+'.tx', k=1 )
        txcheckCB=cmds.getAttr(each+'.tx', cb=1 )  
        cmds.textField(self.minTXValue,e=True, text=gettxValueInfo[0])
        cmds.textField(self.maxTXValue,e=True, text=gettxValueInfo[1])
        cmds.checkBox(self.txcheckMin,e=True, v=gettxSwitchInfo[0])
        cmds.checkBox(self.txcheckMax,e=True, v=gettxSwitchInfo[1])
        cmds.checkBox(self.txchecklock, e=True, v=txchecklock)
        cmds.checkBox(self.txcheckkey, e=True, v=txcheckkey)
        cmds.checkBox(self.txcheckCB, e=True, v=txcheckCB)
        gettyValueInfo=cmds.transformLimits(each,  q=1, ty=1)
        gettySwitchInfo=cmds.transformLimits(each, q=1, ety=1)
        tychecklock=cmds.getAttr(each+'.ty', l=1 )
        tycheckkey=cmds.getAttr(each+'.ty', k=1 )
        tycheckCB=cmds.getAttr(each+'.ty', cb=1 )  
        cmds.textField(self.minTYValue,e=True, text=gettyValueInfo[0])
        cmds.textField(self.maxTYValue,e=True, text=gettyValueInfo[1])
        cmds.checkBox(self.tycheckMin,e=True, v=gettySwitchInfo[0])
        cmds.checkBox(self.tycheckMax,e=True, v=gettySwitchInfo[1])
        cmds.checkBox(self.tychecklock, e=True, v=tychecklock)
        cmds.checkBox(self.tycheckkey, e=True, v=tycheckkey)
        cmds.checkBox(self.tycheckCB, e=True, v=tycheckCB)
        gettzValueInfo=cmds.transformLimits(each,  q=1, tz=1)
        gettzSwitchInfo=cmds.transformLimits(each, q=1, etz=1)
        tzchecklock=cmds.getAttr(each+'.tz', l=1 )
        tzcheckkey=cmds.getAttr(each+'.tz', k=1 )
        tzcheckCB=cmds.getAttr(each+'.tz', cb=1 )  
        cmds.textField(self.minTZValue,e=True, text=gettzValueInfo[0])
        cmds.textField(self.maxTZValue,e=True, text=gettzValueInfo[1])
        cmds.checkBox(self.tzcheckMin,e=True, v=gettzSwitchInfo[0])
        cmds.checkBox(self.tzcheckMax,e=True, v=gettzSwitchInfo[1])
        cmds.checkBox(self.tzchecklock, e=True, v=tzchecklock)
        cmds.checkBox(self.tzcheckkey, e=True, v=tzcheckkey)
        cmds.checkBox(self.tzcheckCB, e=True, v=tzcheckCB)
        getrxValueInfo=cmds.transformLimits(each,  q=1, rx=1)
        getrxSwitchInfo=cmds.transformLimits(each, q=1, erx=1)
        rxchecklock=cmds.getAttr(each+'.rx', l=1 )
        rxcheckkey=cmds.getAttr(each+'.rx', k=1 )
        rxcheckCB=cmds.getAttr(each+'.rx', cb=1 )  
        cmds.textField(self.minRXValue,e=True, text=getrxValueInfo[0])
        cmds.textField(self.maxRXValue,e=True, text=getrxValueInfo[1])
        cmds.checkBox(self.rxcheckMin,e=True, v=getrxSwitchInfo[0])
        cmds.checkBox(self.rxcheckMax,e=True, v=getrxSwitchInfo[1])
        cmds.checkBox(self.rxchecklock, e=True, v=rxchecklock)
        cmds.checkBox(self.rxcheckkey, e=True, v=rxcheckkey)
        cmds.checkBox(self.rxcheckCB, e=True, v=rxcheckCB)
        getryValueInfo=cmds.transformLimits(each,  q=1, ry=1)
        getrySwitchInfo=cmds.transformLimits(each, q=1, ery=1)
        rychecklock=cmds.getAttr(each+'.ry', l=1 )
        rycheckkey=cmds.getAttr(each+'.ry', k=1 )
        rycheckCB=cmds.getAttr(each+'.ry', cb=1 )  
        cmds.textField(self.minRYValue,e=True, text=getryValueInfo[0])
        cmds.textField(self.maxRYValue,e=True, text=getryValueInfo[1])
        cmds.checkBox(self.rycheckMin,e=True, v=getrySwitchInfo[0])
        cmds.checkBox(self.rycheckMax,e=True, v=getrySwitchInfo[1])
        cmds.checkBox(self.rychecklock, e=True, v=rychecklock)
        cmds.checkBox(self.rycheckkey, e=True, v=rycheckkey)
        cmds.checkBox(self.rycheckCB, e=True, v=rycheckCB)
        getrzValueInfo=cmds.transformLimits(each,  q=1, rz=1)
        getrzSwitchInfo=cmds.transformLimits(each, q=1, erz=1)
        rzchecklock=cmds.getAttr(each+'.rz', l=1 )
        rzcheckkey=cmds.getAttr(each+'.rz', k=1 )
        rzcheckCB=cmds.getAttr(each+'.rz', cb=1 )  
        cmds.textField(self.minRZValue,e=True, text=getrzValueInfo[0])
        cmds.textField(self.maxRZValue,e=True, text=getrzValueInfo[1])
        cmds.checkBox(self.rzcheckMin,e=True, v=getrzSwitchInfo[0])
        cmds.checkBox(self.rzcheckMax,e=True, v=getrzSwitchInfo[1])
        cmds.checkBox(self.rzchecklock, e=True, v=rzchecklock)
        cmds.checkBox(self.rzcheckkey, e=True, v=rzcheckkey)
        cmds.checkBox(self.rzcheckCB, e=True, v=rzcheckCB)
            


                    
    def setValues(self):
        getSel=cmds.ls(sl=1)    
        for each in getSel:
            txcheckMin=cmds.checkBox(self.txcheckMin,q=True, value=1)
            minTXValue=float(cmds.textField(self.minTXValue,q=True, text=True))
            maxTXValue=float(cmds.textField(self.maxTXValue,q=True, text=True))
            txcheckMax=cmds.checkBox(self.txcheckMax,q=True, value=1)
            txcheckCB=cmds.checkBox(self.txcheckCB,q=True, value=1)
            txcheckkey=cmds.checkBox(self.txcheckkey,q=True, value=1)
            txchecklock=cmds.checkBox(self.txchecklock,q=True, value=1)
            cmds.transformLimits(each, tx=[minTXValue, maxTXValue], etx=[txcheckMin,txcheckMax]) 
            cmds.setAttr(each+".tx", cb=txcheckCB)
            cmds.setAttr(each+".tx", l=txchecklock)  
            cmds.setAttr(each+".tx", k=txcheckkey)
            tycheckMin=cmds.checkBox(self.tycheckMin,q=True, value=1)
            minTYValue=float(cmds.textField(self.minTYValue,q=True, text=True))
            maxTYValue=float(cmds.textField(self.maxTYValue,q=True, text=True))
            tycheckMax=cmds.checkBox(self.tycheckMax,q=True, value=1)
            tycheckCB=cmds.checkBox(self.tycheckCB,q=True, value=1)
            tycheckkey=cmds.checkBox(self.tycheckkey,q=True, value=1)
            tychecklock=cmds.checkBox(self.tychecklock,q=True, value=1)
            cmds.transformLimits(each, ty=[minTYValue, maxTYValue], ety=[tycheckMin,tycheckMax]) 
            cmds.setAttr(each+".ty", cb=tycheckCB)
            cmds.setAttr(each+".ty", l=tychecklock)  
            cmds.setAttr(each+".ty", k=tycheckkey)
            tzcheckMin=cmds.checkBox(self.tzcheckMin,q=True, value=1)
            minTZValue=float(cmds.textField(self.minTZValue,q=True, text=True))
            maxTZValue=float(cmds.textField(self.maxTZValue,q=True, text=True))
            tzcheckMax=cmds.checkBox(self.tzcheckMax,q=True, value=1)
            tzcheckCB=cmds.checkBox(self.tzcheckCB,q=True, value=1)
            tzcheckkey=cmds.checkBox(self.tzcheckkey,q=True, value=1)
            tzchecklock=cmds.checkBox(self.tzchecklock,q=True, value=1)
            cmds.transformLimits(each, tz=[minTZValue, maxTZValue], etz=[tzcheckMin,tzcheckMax]) 
            cmds.setAttr(each+".tz", cb=tzcheckCB)
            cmds.setAttr(each+".tz", l=tzchecklock)  
            cmds.setAttr(each+".tz", k=tzcheckkey)
            rxcheckMin=cmds.checkBox(self.rxcheckMin,q=True, value=1)
            minRXValue=float(cmds.textField(self.minRXValue,q=True, text=True))
            maxRXValue=float(cmds.textField(self.maxRXValue,q=True, text=True))
            rxcheckMax=cmds.checkBox(self.rxcheckMax,q=True, value=1)
            rxcheckCB=cmds.checkBox(self.rxcheckCB,q=True, value=1)
            rxcheckkey=cmds.checkBox(self.rxcheckkey,q=True, value=1)
            rxchecklock=cmds.checkBox(self.rxchecklock,q=True, value=1)
            cmds.transformLimits(each, rx=[minRXValue, maxRXValue], erx=[rxcheckMin,rxcheckMax]) 
            cmds.setAttr(each+".rx", cb=rxcheckCB)
            cmds.setAttr(each+".rx", l=rxchecklock)  
            cmds.setAttr(each+".rx", k=rxcheckkey)
            rycheckMin=cmds.checkBox(self.rycheckMin,q=True, value=1)
            minRYValue=float(cmds.textField(self.minRYValue,q=True, text=True))
            maxRYValue=float(cmds.textField(self.maxRYValue,q=True, text=True))
            rycheckMax=cmds.checkBox(self.rycheckMax,q=True, value=1)
            rycheckCB=cmds.checkBox(self.rycheckCB,q=True, value=1)
            rycheckkey=cmds.checkBox(self.rycheckkey,q=True, value=1)
            rychecklock=cmds.checkBox(self.rychecklock,q=True, value=1)
            cmds.transformLimits(each, ry=[minRYValue, maxRYValue], ery=[rycheckMin,rycheckMax]) 
            cmds.setAttr(each+".ry", cb=rycheckCB)
            cmds.setAttr(each+".ry", l=rychecklock)  
            cmds.setAttr(each+".ry", k=rycheckkey)
            rzcheckMin=cmds.checkBox(self.rzcheckMin,q=True, value=1)
            minRZValue=float(cmds.textField(self.minRZValue,q=True, text=True))
            maxRZValue=float(cmds.textField(self.maxRZValue,q=True, text=True))
            rzcheckMax=cmds.checkBox(self.rzcheckMax,q=True, value=1)
            rzcheckCB=cmds.checkBox(self.rzcheckCB,q=True, value=1)
            rzcheckkey=cmds.checkBox(self.rzcheckkey,q=True, value=1)
            rzchecklock=cmds.checkBox(self.rzchecklock,q=True, value=1)
            cmds.transformLimits(each, rz=[minRZValue, maxRZValue], erz=[rzcheckMin,rzcheckMax]) 
            cmds.setAttr(each+".rz", cb=rzcheckCB)
            cmds.setAttr(each+".rz", l=rzchecklock)  
            cmds.setAttr(each+".rz", k=rzcheckkey)
inst = ValueClass()
inst.create()
