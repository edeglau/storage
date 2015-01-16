import maya.cmds as cmds
from functools import partial
from string import *
import re
import maya.mel
import os, subprocess, sys, platform, logging, signal, PyQt4, webbrowser, urllib, re, getpass, datetime
from os  import popen
from sys import stdin
import subprocess
import os
import random
from random import randint
from pymel.core import *
#import win32clipboard
import operator
from sys import argv
from datetime import datetime
from operator import itemgetter

OSplatform=platform.platform()
getFolderName=getpass.getuser()

trans=[".tx", ".ty", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz"]  

'''MG rigging tool functions'''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons License'
'http://creativecommons.org/licenses/by-sa/3.0/au/'

photoshop = r"C:\\Program Files\\Adobe\\Adobe Photoshop CC 2014\\Photoshop.exe"
gimp="C:\\Program Files\\GIMP 2\\bin\\gimp-2.6.exe"


BbxName="eyeDirGuide"
BbxFilepath="G:\\_PIPELINE_MANAGEMENT\\Published\\maya\\"+BbxName+".ma"

getfilePath=str(__file__)
filepath= os.getcwd()

sys.path.append(str(filepath))
import baseFunctions_maya
reload (baseFunctions_maya)
getClass=baseFunctions_maya.BaseClass()

gtepiece=getfilePath.split("/")
getguideFilepath='/'.join(gtepiece[:-2])+"/guides/"
sys.path.append(str(getguideFilepath))

getrenamerFilepath='/'.join(gtepiece[:-2])+"/renamer/"
sys.path.append(str(getrenamerFilepath))

getValueFilepath='/'.join(gtepiece[:-2])+"/Values/"
sys.path.append(str(getValueFilepath))

getSelArrayPath='/'.join(gtepiece[:-2])+"/selectArray/"
sys.path.append(str(getSelArrayPath))

getSSDArrayPath='/'.join(gtepiece[:-2])+"/SSD/"
sys.path.append(str(getSSDArrayPath))

getToolArrayPath='/'.join(gtepiece[:-2])+"/tools/"
sys.path.append(str(getToolArrayPath))

class ToolFunctions(object):
    '''--------------------------------------------------------------------------------------------------------------------------------------
    Interface Layout
    --------------------------------------------------------------------------------------------------------------------------------------'''          
                
    def _bone_rivet(self, arg=None): 
        winName = "Bone Rivets"
        winTitle = winName
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=400, h=100 )
        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=400)
        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        cmds.rowLayout  (' rMainRow ', w=400, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(200, 20))
        RivetName=cmds.textField(w=120, h=25, p='listBuildButtonLayout')    
        cmds.button (label='Create Bone Rivet', p='listBuildButtonLayout', command = lambda *args:self._add_bone_rivet(queryRivet=cmds.textField(RivetName, q=1, text=1) ))        
        cmds.showWindow(window)
        
    def _add_bone_rivet(self, queryRivet):
        selObj=cmds.ls(sl=1, fl=1)
        getLists=zip(selObj[::2], selObj[1::2])
        for each in getLists:
            cmds.select(each[0])
            cmds.select(each[1], add=1)
            maya.mel.eval( "rivet;" )
            getRiv=cmds.ls(sl=1)
            cmds.rename(getRiv[0], queryRivet)
            getNewRiv=cmds.ls(sl=1)
            getClass.makeJoint()
            cmds.parent(getNewRiv[0]+"_jnt", getNewRiv[0]) 
        
    def chain_rig(self, arg=None):
        import ChainWork
        reload (ChainWork)
        result = cmds.promptDialog( 
                    title='Building a chainrig', 
                    message="Enter dimensions for chain - EG:", 
                    text="name, Y, 10", 
                    button=['Continue','Cancel'],
                    defaultButton='Continue', 
                    cancelButton='Cancel', 
                    dismissString='Cancel' )
        if result == 'Continue':
            resultInfo=cmds.promptDialog(q=1)
            if resultInfo:
                pass
            else:
                print "nothing collected"
            getInfo=resultInfo.split(', ')
            getDir=getInfo[1]
            mainName=getInfo[0]
            if getDir=="X":
                nrx=1
                nry=0
                nrz=0  
            if getDir=="Y":
                nrx=0
                nry=1
                nrz=0   
            if getDir=="Z":
                nrx=0
                nry=0
                nrz=1
            ControllerSize=int(getInfo[2])
            getClass=ChainWork.ChainRig(nrz, nry, nrx, mainName, ControllerSize) 

               

    def _add_to_set(self, querySet):
        getSel=cmds.ls(sl=1)
        for each in getSel:
            cmds.sets(each, add=querySet)
            
    def _remove_from_set(self, querySet):
        getSel=cmds.ls(sl=1)
        for each in getSel:
            cmds.sets(each, rm=querySet)            
            
    def _add_to_nset(self, dropDownData):
        getSel=cmds.ls(sl=1)
        for each in getSel:
            cmds.select(dropDownData, add=1)
            maya.mel.eval( 'dynamicConstraintMembership "add";' )

    def _remove_from_nset(self, dropDownData):
        getSel=cmds.ls(sl=1)
        for each in getSel:
            cmds.select(dropDownData, add=1)
            maya.mel.eval( 'dynamicConstraintMembership "remove";' )            

    def _edit_nsets_win(self, arg=None):
        titleName="Dynamic Sets"
        getAllSets=[(each) for each in cmds.ls(typ="dynamicConstraint")]
        self._dynsets_win(titleName, getAllSets)
        
    def _dynsets_win(self, titleName, getAllSets):
        winName = titleName
        winTitle = winName
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=600, h=100 )
        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' windowMenuRow ', nr=1, w=600)
        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='windowMenuRow')
        cmds.rowLayout  (' rMainRow ', w=600, numberOfColumns=6, p='windowMenuRow')
        cmds.columnLayout ('windowMenuColumn', parent = 'rMainRow')
        cmds.setParent ('windowMenuColumn')
        cmds.separator(h=10, p='windowMenuColumn')
        cmds.gridLayout('listBuildLayout', p='windowMenuColumn', numberOfColumns=1, cellWidthHeight=(600, 20))
        setMenu=cmds.optionMenu( label='joints')
        for each in getAllSets:
            cmds.menuItem( label=each)        
        cmds.gridLayout('nsetButtonLayout', p='windowMenuColumn', numberOfColumns=2, cellWidthHeight=(275, 20))
        cmds.button (label='Add relatives', p='nsetButtonLayout', command = lambda *args:self._add_to_nset(dropDownData=optionMenu(setMenu, q=1, v=1)))
        cmds.button (label='remove relatives', p='nsetButtonLayout', command = lambda *args:self._remove_from_nset(dropDownData=optionMenu(setMenu, q=1, v=1)))
        cmds.showWindow(window)  


    def _edit_sets_win(self, arg=None):
        getAllSets=[(each) for each in cmds.ls(typ="objectSet") if "tweak" not in each]
        winName = "Sets"
        winTitle = winName
        if cmds.window(winName, exists=True):
            cmds.deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=400, h=100 )
        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout (' windowMenuRow ', nr=1, w=400)
        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='windowMenuRow')
        cmds.rowLayout (' rMainRow ', w=400, numberOfColumns=6, p='windowMenuRow')
        cmds.columnLayout ('windowMenuColumn', parent = 'rMainRow')
        cmds.setParent ('windowMenuColumn')
        cmds.separator(h=10, p='windowMenuColumn')
        cmds.gridLayout('setBuildButtonLayout', p='windowMenuColumn', numberOfColumns=1, cellWidthHeight=(200, 20))
        setMenu=cmds.optionMenu( label='joints')
        for each in getAllSets:
            cmds.menuItem( label=each)
        cmds.button (label='Add to set', p='setBuildButtonLayout', command = lambda *args:self._add_to_set(querySet=cmds.optionMenu(setMenu, q=1, v=1)))
        cmds.button (label='remove from set', p='setBuildButtonLayout', command = lambda *args:self._remove_from_set(querySet=cmds.optionMenu(setMenu, q=1, v=1)))
        cmds.showWindow(window)
        
    def _open_texture_file_gmp(self, arg=None):
        try:
            selObj=cmds.ls(sl=1, fl=1)[0]
            pass
        except:
            print "nothing selected"
            return
        getNodeType=cmds.nodeType(selObj)
        if getNodeType=="file":
            Attr=cmds.listAttr(selObj)
            for each in Attr:
                if "fileTextureName" in each and "Pattern" not in each:
                    getValue=cmds.getAttr(selObj+'.'+each)   
                    if "Windows" in OSplatform:
                        subprocess.Popen([gimp, getValue])
                    if "Linux" in OSplatform: 
                        subprocess.Popen('gimp "%s"' % getValue, stdout=subprocess.PIPE, shell=True)                     
#                        os.system('gimp "%s"' % getValue)                  
        else:
            print "need to select a texture node"

    def _view_texture_file(self, arg=None):
        try:
            selObj=cmds.ls(sl=1, fl=1)[0]
            pass
        except:
            print "nothing selected"
            return
        getNodeType=cmds.nodeType(selObj)
        if getNodeType=="file":
            Attr=cmds.listAttr(selObj)
            for each in Attr:
                if "fileTextureName" in each and "Pattern" not in each:
                    getValue=cmds.getAttr(selObj+'.'+each)   
                    if "Windows" in OSplatform:
                        subprocess.Popen(getValue)
                    if "Linux" in OSplatform:  
                       os.system('xdg-open "%s"' % getValue)                  
        else:
            print "need to select a texture node"

    def _open_texture_file_gmpV1(self, arg=None):
        try:
            selObj=cmds.ls(sl=1, fl=1)[0]
            pass
        except:
            print "nothing selected"
            return
        getNodeType=cmds.nodeType(selObj)
        if getNodeType=="file":
            Attr=cmds.listAttr(selObj)
            for each in Attr:
                if "fileTextureName" in each and "Pattern" not in each:
                    getValue=cmds.getAttr(selObj+'.'+each)   
                    subprocess.Popen([gimp, getValue])
        else:
            print "need to select a texture node"
            
    def _open_work_folder(self, arg=None):
        getScenePath=cmds.file(q=1, location=1)
        getPathSplit=getScenePath.split("/")
        folderPath='\\'.join(getPathSplit[:-1])+"\\"        
        if "Windows" in OSplatform:
            print "windows"
            folderPath=re.sub(r'/',r'\\', folderPath)
            os.startfile(folderPath)
        
        if "Linux" in OSplatform:
            print "Linux"
            newfolderPath=re.sub(r'\\',r'/', folderPath)
            os.system('xdg-open "%s"' % newfolderPath) 


    def _open_work_folderV1(self, arg=None):
        destImagePath=folderPath
        print destImagePath
        self.get_path(destImagePath)    
        
    def get_path(self, path):
        print path
        if '\\\\' in path:
            newpath=re.sub(r'\\\\',r'\\', path)
            os.startfile(r'\\'+newpath[1:])    
        else:
            os.startfile(path)            
            
    def _open_texture_file_ps(self, arg=None):
        try:
            selObj=cmds.ls(sl=1, fl=1)[0]
            pass
        except:
            print "nothing selected"
        getNodeType=cmds.nodeType(selObj)
        if getNodeType=="file":
            Attr=cmds.listAttr(selObj)
            for each in Attr:
                if "fileTextureName" in each and "Pattern" not in each:
                    getValue=cmds.getAttr(selObj+'.'+each)   
                    getpath=getValue.split("/")
                    getpPath="\\".join(getpath[:-1])
                    getFile=getpath[-1:]
                    getValue=getpPath+"\\"+getFile[0]
                    getValue = r"%s"%getValue         
                    if "Windows" in OSplatform:
                        subprocess.Popen([photoshop, getValue])
                    if "Linux" in OSplatform:  
                        os.system('photoshop "%s"' % getValue)                         
                    
        else:
            print "need to select a texture node"

        
    def _eye_directions(self, arg=None):
        cmds.file(BbxFilepath, i=1,  type="mayaAscii", iv=1, mnc=0, gr=1, gn="FaceRig", op=1, rpr="ControlBox")
        try:
            getBox=cmds.ls("BigBox_CC_grp") 
        except:
            getBox=cmds.ls("*:BigBox_CC_grp")  
        getTranslation, getRotation=getClass.locationXForm(getHeadCtrl)
        cmds.move(getTranslation[0]+40, getTranslation[1], getTranslation[2], getBox)
        cmds.parentConstraint(getHeadCtrl,getBox, mo=1)
        print "Eye Direction Present"
        
    def addEyeDir(self, arg=None):
        '''this sandwitches a circle control to another control for an easy override switch(face controllers for SDK keys)'''
        colour=6
        size=1 
        selObj=("EyeOrient_L_jnt", "EyeOrient_R_jnt")
        for each in selObj:
            selObjParent=cmds.listRelatives( each, allParents=True )
            transformWorldMatrix, rotateWorldMatrix=getClass.locationXForm(each)        
            nrx, nry, nrz = 0.0, 0.0, 1.0 
            getcolour=cmds.getAttr(each+".overrideColor")
            name=each.split("_jnt")[0]+"_dir"
            grpname=each.split("_jnt")[0]+"_dir_grp"
            getClass.buildCtrl(each, name, grpname, transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)   
            cmds.parent(name, each)      
    def _rivet(self, arg=None):
        maya.mel.eval( "rivet;" )

    def _rivet_obj(self, arg=None): 
        selObj=cmds.ls(sl=1, fl=1)
        getFirst=selObj[:-1]
        constrainObj=selObj[-1]
        maya.mel.eval( "rivet" )
        getRiv=cmds.ls(sl=1)
        cmds.parent(constrainObj, getRiv)
        
    def _disappear(self, arg=None):
        getSel=cmds.ls(sl=1)
        for item in getSel:
            for each in trans:
#                 cmds.setAttr(item+each, l=1)
                cmds.setAttr(item+each, k=0)
                cmds.setAttr(item+".visibility", 0)
                
    def char_light_cleanup(self):
        try:    
            cmds.pointConstraint("*:Master_Ctrl", "*:LA0095_CharBaseLighting_Master:Lights", mo=1)
        except:
            print "no CharBased lighting present. Passing on relinking it."
            pass        
        try:
            if cmds.ls("*:LA0095_CharBaseLighting_Master:LightCtrl"):
                getLightObj=cmds.ls("*:LA0095_CharBaseLighting_Master:LightCtrl")
                for each in getLightObj:
                    getChildConstraint=[(each) for each in cmds.listRelatives(each, ad=1, typ="parentConstraint")]
                    if len(getChildConstraint)>0:
                        cmds.delete(getChildConstraint[0])
        except:
            pass        
    def _clean_up(self, arg=None): 
        self.char_light_cleanup()
        if cmds.ls("*Skirtvtx*jnt") :                      
            getSel=cmds.ls("*Skirtvtx*jnt") 
            for item in getSel:
                    cmds.setAttr(item+"_parentConstraint1.interpType", 0 )    
                    print item+" -set joint interpolation type to No Flip"    
        if cmds.ls("*Dressvtx*jnt") :                      
            getSel=cmds.ls("*Dressvtx*jnt") 
            for item in getSel:
                    cmds.setAttr(item+"_parentConstraint1.interpType", 0 )    
                    print item+" -set joint interpolation type to No Flip"    
        if cmds.ls(typ="locator") :                      
            getSel=cmds.ls(typ="locator")
            for item in getSel:
                getTransform=cmds.listRelatives(item, ap=1)[0]
                for each in trans:
                    try:
                        cmds.setAttr(getTransform+each, k=0)
                    except:
                        print "cannot set keyable state in this file for "+getTransform+each
                        pass
                    try:
                        cmds.setAttr(item+".visibility", 0)
                    except:
                        print "unable to set visibility on shape node of locator: " +getTransform
                        pass        
        if cmds.ls("Lash*RIV"):
            getSel=cmds.ls("Lash*RIV")
            getSel.append("Lash_attribute_holder")
            for item in getSel:
                for each in trans:
                    try:
                        cmds.setAttr(item+each, k=0)
                        print "keyframe ability turned off for : "+item+each
                    except:
                        pass
                    try:
                        cmds.setAttr(item+".visibility", 0)
                        print "hid "+item
                    except:
                        pass
        if cmds.ls("Eye_*_scptStretchOrigin"):
            getSel=cmds.ls("Eye_*_scptStretchOrigin") 
            for item in getSel:
                for each in trans:
                    cmds.setAttr(item+each, k=0)
                    print "keyframe ability turned off for : "+item+each
                    cmds.setAttr(item+".visibility", 0)   
            getSel=cmds.ls("Eye_*_scpt.en") 
            for item in getSel:                 
                cmds.setAttr(item, l=1)  
                print "locked "+item
        if cmds.ls("Eyes_txt_CC") :                      
            getSel=cmds.ls("Eyes_txt_CC")  
            getEye=cmds.ls("Eyes_select")  
            getSel=getSel+getEye
            for item in getSel:
                for each in trans:
                    cmds.setAttr(item+each, k=0)
                    print "keyframe ability turned off for : "+item+each
                    cmds.setAttr(item+".visibility", 0)    
                    print "hid "+item            
#         if cmds.ls("rivet*") :                      
#             getSel=cmds.ls("rivet*") 
#             for item in getSel:
#                 for each in trans:
#                     cmds.setAttr(item+each, k=0)
#                     print "keyframe ability turned off for : "+item+each
#                     cmds.setAttr(item+".visibility", 0)    
#                     print "hid "+item            
        if cmds.nodeType(typ="locator") :                      
            getSel=mds.nodeType(typ="locator")
            for item in getSel:
                print item
                for each in trans:
                    cmds.setAttr(item+each, k=0)
                    print "keyframe ability turned off for : "+item+each
                    cmds.setAttr(item+".visibility", 0)      
                    print "hid "+item  
                            
    def _clean_up_rig(self, arg=None):
        getTransShoulder=[".tx", ".ty", ".tz"]
        if cmds.ls("Shoulder_*_Ctrl"):
            getSel=cmds.ls("Shoulder_*_Ctrl")
            for item in getSel:
                for each in getTransShoulder:
                    cmds.setAttr(item+each, cb=0)
                    cmds.setAttr(item+each, l=1)
                    cmds.setAttr(item+each, k=0)
        if cmds.ls("Hips_Ctrl"):
            getSel=cmds.ls("Hips_Ctrl")   
            for item in getSel: 
                cmds.setAttr(item+".spineFK_IK", 0)                
        if cmds.ls(typ="locator") :                      
            getSel=cmds.ls(typ="locator")
            for item in getSel:
                getTransform=cmds.listRelatives(item, ap=1)[0]
                for each in trans:
                    try:
                        cmds.setAttr(getTransform+each, k=0)
                        print "keyframe ability turned off for : "+getTransform+each
                    except:
                        print "cannot set keyable state in this file"
                        pass
                    try:
                        cmds.setAttr(item+".visibility", 0)
                        print "hid "+item
                    except:
                        print "unable to set visibility on shape node of locator: " +getTransform
                        pass        
        if cmds.ls("Hand_*_Fingers_Ctrl"):
            selObj=cmds.ls("Hand_*_Fingers_Ctrl")
            for each in selObj:
                cmds.addAttr(each+".SpreadFingers", e=1, min=-0, max=90)
                print "reset " +each+".SpreadFingers"
                cmds.addAttr(each+".CurlFingers", e=1, min=-160, max=0)
                print "reset " +each+".CurlFingers"
        if cmds.ls("*_Finger_*_Ctrl"):
            selObj=cmds.ls("*_Finger_*_Ctrl")
            for each in selObj:
                if "|" not in each:
                    cmds.addAttr(each+".MiddleJoint", e=1, min=-160, max=0)
                    print "reset " +each+".MiddleJoint"
                    cmds.addAttr(each+".LastJoint", e=1, min=-160, max=0)
                    print "reset " +each+".LastJoint"
                    cmds.addAttr(each+".FingerFullCurl", e=1, min=-160, max=0)  
                    print "reset " +each+".FingerFullCurl"     
        Side=["Right", "Left"]
        for eachSide in Side:
            try:
                SDK_Fingers=("Index_Finger_"+eachSide+"_M_Ctrl.rotateY",
                            "Mid_Finger_"+eachSide+"_M_Ctrl.rotateY",
                            "Ring_Finger_"+eachSide+"_M_Ctrl.rotateY",
                            "Pinky_Finger_"+eachSide+"_M_Ctrl.rotateY",
                            "Thumbmid_"+eachSide+"_M_Ctrl.rotateY",
                            "Thumbbase_"+eachSide+"_M_Ctrl.rotateY",
                            "Index_Finger_"+eachSide+"_M_Ctrl.ry")
                for each in SDK_Fingers:
                    cmds.setAttr(each, lock=1) 
                    print each+" attribute has been locked"
            except:
                pass    


    def _blend_colour_window(self, arg=None):
        getSel=cmds.ls(sl=1)        
        global attributeSel
        geteattr=cmds.listAttr (getSel[0], ud=1)        
        winName = "select attribute to link the switch constraint driven key to"
        winTitle = winName
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)

        window = cmds.window(winName, title=winTitle, tbm=1, w=300, h=100 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=150)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        
        cmds.rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))
        attributeSel=cmds.optionMenu( label='user attribute')
        for each in geteattr:
            cmds.menuItem( label=each)            
        cmds.button (label='Go', p='listBuildButtonLayout', command = self._blend_colour)
        cmds.showWindow(window)   
          
    def _blend_colour(self, arg=None):
        geteattr=cmds.optionMenu(attributeSel, q=1, v=1)          
        selObj=cmds.ls(sl=1)
        if len(selObj)>3:
            pass
        else:
            print "select a controller with a user attribute, a follow object, then a '0' rotate/scale leading object and a '1' rotate/scale leading object"
            return
        Controller=selObj[0]
        firstChild=selObj[1]
        secondChild=selObj[2]
        thirdChild=selObj[3]  
        Controller=Controller+"."+geteattr      
        getClass.blendColors_callup(Controller, firstChild, secondChild, thirdChild)  
        
    def _quickCconnect_window(self, arg=None):
        getSel=cmds.ls(sl=1)  
        getFirst=getSel[:-1]
        print getFirst
        getSecond=getSel[-1] 
        print getSecond        
#        getFirst=getSel[0]      
#        getSecond=getSel[1] 
        global attributeFirstSel
        global attributeSecondSel        
        getFirstAttr=cmds.listAttr (getFirst[0])      
        getFirstAttr=sorted(getFirstAttr)
        getSecondAttr=cmds.listAttr (getSecond)
        getSecondAttr=sorted(getSecondAttr)         
        winName = "Quick connect attributes"
        winTitle = winName
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)

        window = cmds.window(winName, title=winTitle, tbm=1, w=350, h=100 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=150)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        cmds.rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))
        cmds.text(label=getFirst[0])
        cmds.text(label=getSecond)        
        attributeFirstSel=cmds.optionMenu( label='From')
        for each in getFirstAttr:
            cmds.menuItem( label=each) 
        attributeSecondSel=cmds.optionMenu( label='To')               
        for each in getSecondAttr:
            cmds.menuItem( label=each)                    
        cmds.button (label='Go', p='listBuildButtonLayout', command=lambda *args:self._quickCconnect(getFirst, getSecond))
        cmds.showWindow(window)   
          
    def _quickCconnect(self, getFirst, getSecond):
        getFirstattr=cmds.optionMenu(attributeFirstSel, q=1, v=1)          
        getSecondattr=cmds.optionMenu(attributeSecondSel, q=1, v=1) 
        getFirstAttr=getFirst[0]  
        for each in getFirst:    
            cmds.connectAttr(getSecond+"."+getSecondattr, each+"."+getFirstattr, f=1)

    def _quickCopy_single_Attr_window(self, arg=None):
        getSel=cmds.ls(sl=1)  
        getChildren=getSel[1:]
        getParent=getSel[:1]
        global attributeFirstSel
        global attributeSecondSel        
        getFirstAttr=cmds.listAttr (getChildren[0])      
        getFirstAttr=sorted(getFirstAttr)
        getSecondAttr=cmds.listAttr (getParent)
        getSecondAttr=sorted(getSecondAttr)         
        winName = "Quick transfer single attribute"
        winTitle = winName
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)

        window = cmds.window(winName, title=winTitle, tbm=1, w=350, h=100 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=150)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        cmds.rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))
        cmds.text(label=getParent[0])
        cmds.text(label=getChildren[0])        
        attributeFirstSel=cmds.optionMenu( label='From')
        for each in getFirstAttr:
            cmds.menuItem( label=each) 
        attributeSecondSel=cmds.optionMenu( label='To')               
        for each in getSecondAttr:
            cmds.menuItem( label=each)                    
        cmds.button (label='Go', p='listBuildButtonLayout', command=lambda *args:self._copy_single_attr(getChildren, getParent))
        cmds.showWindow(window)   
        
    def _copy_single_attr(self, getChildren, getParent):
        getParentAttr=cmds.optionMenu(attributeFirstSel, q=1, v=1)
        getChildAttr=cmds.optionMenu(attributeSecondSel, q=1, v=1)
        getSel=cmds.ls(sl=1)  
        getChildren=getSel[1:]
        getParent=getSel[:1]      
        getValue=getAttr(getParent[0]+'.'+getParentAttr)    
        for each in getChildren:
            get=cmds.keyframe(getParent[0]+'.'+getParentAttr, q=1, kc=1) 
            if get!=0:
                try:
                    getSource=connectionInfo(getParent[0]+'.'+getParentAttr, sfd=1)
                    newAnimSrce=duplicate(getSource) 
                    lognm=newAnimSrce[0].replace(str(getParent[0]), str(each))
                    #===========================================================
                    # remove numbers at end
                    #===========================================================
                    newname=re.sub("\d+$", "", lognm)
                    cmds.rename(newAnimSrce, newname)
                    getChangeAttr=each+'.'+getChildAttr
                    connectAttr(newname+'.output', getChangeAttr, f=1)
                except:
                    pass
            else:
                try:                    
                    getChangeAttr=each+'.'+getChildAttr
                    setAttr(getChangeAttr, getValue)
                except:
                    pass
        
    def _createAlias_window(self, arg=None):
        getSel=ls(sl=1)  
        if len(getSel)>1:
            pass
        else:
            print "need to select 2 or more items" 
            return       
        getFirst=getSel[0]
        global attributeFirstSel
        global makeAttr        
        getFirstAttr=listAttr (getFirst, w=1, a=1, s=1,u=1)      
        getFirstAttr=sorted(getFirstAttr)        
        winName = "Quick connect attributes"
        winTitle = winName
        if cmds.window(winName, exists=True):
                deleteUI(winName)

        window = cmds.window(winName, title=winTitle, tbm=1, w=350, h=100 )

        menuBarLayout(h=30)
        rowColumnLayout  (' selectArrayRow ', nr=1, w=150)

        frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        
        rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        columnLayout ('selectArrayColumn', parent = 'rMainRow')
        setParent ('selectArrayColumn')
        separator(h=10, p='selectArrayColumn')
        gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))
        attributeFirstSel=optionMenu( label='From')
        for each in getFirstAttr:
            menuItem( label=each)                
        makeAttr=textField()
        button (label='Go', p='listBuildButtonLayout', command = self._create_alias)
        showWindow(window)   
          
    def _create_alias(self, arg=None):
        getSel=ls(sl=1)
        getFirstattr=optionMenu(attributeFirstSel, q=1, v=1)       
        floater=textField(makeAttr, q=1, text=1)
        getFirst=getSel[:-1]
        getSecond=getSel[-1]  
        for each in getFirst:
            get=cmds.keyframe(each+'.'+getFirstattr, q=1, kc=1)
            if get>0:
                getSource=connectionInfo(each+'.'+getFirstattr, sfd=1) 
                addAttr([getSecond], ln=floater, at="double", k=1, nn=floater)
                connectAttr(getSource, getSecond+"."+floater, f=1)
                connectAttr(getSecond+"."+floater, each+"."+getFirstattr, f=1)
            else:
                getValue=getattr(each,getFirstattr).get()
                addAttr([getSecond], ln=floater, at="double", k=1, nn=floater)
                connectAttr(getSecond+"."+floater, each+"."+getFirstattr, f=1)
                getChangeAttr=getattr(getSecond,floater)
                getChangeAttr.set(getValue)
#                setAttr(getSecond+"."+floater, getValue)

    def _transfer_anim_attr(self, arg=None):
        getSel=ls(sl=1)
        getChildren=getSel[1:]
        getParent=getSel[:1]
        for each in getChildren:
            getFirstattr=listAttr (getParent[0], w=1, a=1, s=1, u=1, m=0)
            for item in getFirstattr:
                if "." not in item:
                    get=cmds.keyframe(getParent[0]+'.'+item, q=1, kc=1) 
                    if get!=0:
                        try:
                            getSource=connectionInfo(getParent[0]+'.'+item, sfd=1)
                            newAnimSrce=duplicate(getSource) 
                            lognm=newAnimSrce[0].replace(str(getParent[0]), str(each))
                            #===========================================================
                            # remove numbers at end
                            #===========================================================
                            newname=re.sub("\d+$", "", lognm)
                            cmds.rename(newAnimSrce, newname)
                            getChangeAttr=getSecond+'.'+item                        
                            connectAttr(newname+'.output', getChangeAttr, f=1)                             
#                            connectAttr(getSource, each+"."+item, f=1)
                        except:
                            pass
                    else:
                        try:
                            getValue=getattr(getParent[0],item).get()
                            getChangeAttr=getattr(each,item)
                            getChangeAttr.set(getValue)
                        except:
                            pass

    def _findAttr_window(self, arg=None):  
        getSel=ls(sl=1)     
        getFirst=getSel[0]
        global attributeFirstSel
        global makeAttr        
        getFirstAttr=listAttr (getFirst, w=1, a=1, s=1,u=1)      
        getFirstAttr=sorted(getFirstAttr)        
        winName = "find attributes"
        winTitle = winName
        if cmds.window(winName, exists=True):
                deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=450, h=100 )
        menuBarLayout(h=30)
        rowColumnLayout  (' selectArrayRow ', nr=1, w=450)
        frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        rowLayout  (' rMainRow ', w=450, numberOfColumns=6, p='selectArrayRow')
        columnLayout ('selectArrayColumn', parent = 'rMainRow')
        setParent ('selectArrayColumn')
        separator(h=10, p='selectArrayColumn')
        gridLayout('listBuildLayout', p='selectArrayColumn', numberOfColumns=1, cellWidthHeight=(450, 20))      
        attributeFirstSel=optionMenu( label='Find')
        for each in getFirstAttr:
            menuItem( label=each)
        gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(225, 20))
        findAttr=textField(AttributeName, text="use a full or partial name EG:'translate'")
        button (label='Find', p='listBuildButtonLayout', command = lambda *args:self._find_att(getSel, getFirstattr=optionMenu(attributeFirstSel, q=1, ill=1), attribute=textField(findAttr, q=1, text=1)))
        makeAttr=textField(text="fill with number EG:'50' and apply attribute")
        button (label='Apply', p='listBuildButtonLayout', command = lambda *args:self._apply_att(getSel, getFirstattr=optionMenu(attributeFirstSel, q=1, ils=1), makeAttr=textField(makeAttr, q=1, text=1)))
        showWindow(window)   
        
    def _find_att(self, getSel, getFirstattr, attribute):
        collectAttr=[]
        for each in getFirstattr:
            find=menuItem(each, q=1, label=1)
            if attribute in find:
                print find
                collectAttr.append(find)
#                select(getSel[0]+'.'+find)         
                optionMenu(attributeFirstSel, e=1, v=find) 
                getChangeAttr=getattr(getSel[0],find).get()
                print getChangeAttr
#        select(getSel[0]+'.'+collectAttr[0], r=1)
#        for each in collectAttr[1:]:
#            select(getSel[0]+'.'+each, add=1)

    def _apply_att(self,getSel, getFirstattr, makeAttr):
        getAttri=optionMenu(attributeFirstSel, q=1, v=1)
        getChangeAttr=getattr(getSel[0],getAttri)
        try:
            makeAttr=float(makeAttr)
        except:
            print "field must have number"
        getChangeAttr.set(makeAttr)
       

    def _erase_anim(self, arg=None):
        getSel=cmds.ls(sl=1, fl=1)
        for each in getSel:
            getFirstattr=listAttr (each, w=1, a=1, s=1, u=1, m=0)
            for item in getFirstattr:
                if "." not in item:
                    get=cmds.keyframe(each+'.'+item, q=1, kc=1)
                    if get>0:
                        getSource=connectionInfo(each+'.'+item, sfd=1) 
                        delete(getSource.split(".")[0])
                    else:
                        pass

    def _reset(self, arg=None):
        getSel=cmds.ls(sl=1, fl=1)
        for each in getSel:
            print each
            getFirstattr=[(item) for item in cmds.listAttr (each, w=1, a=1, s=1, u=1, k=1, v=1, m=0) if "visibility" not in item and "scaleX" not in item and "scaleY" not in item and "scaleZ" not in item] 
            for item in getFirstattr:
                print item
                if "." not in item:
                    get=cmds.keyframe(each+'.'+item, q=1, kc=1)
                    if get>0:
                        setAttr(each+'.'+item, 0)
                    else:
                        setAttr(each+'.'+item, 1)
  
                    
                        
    def _copy_into_grp(self, arg=None):
        getSel=ls(sl=1)
        getFirst=getSel[:-1]
        getGrp=getSel[-1]
        for each in getFirst:
            newDupe=duplicate(each)
            parent(newDupe, getGrp)
            rename(newDupe[0], each)

    def _createSDK_alias_window(self, arg=None):
        getSel=ls(sl=1)  
        if len(getSel)>1:
            pass
        else:
            print "need to select 2 or more items" 
            return       
        getFirst=getSel[0]
        global attributeFirstSel
        global makeAttr   
        global firstMinValue
        global firstMaxValue
        global secondMinValue
        global secondMaxValue
        getFirstAttr=listAttr (getFirst, w=1, a=1, s=1,u=1)      
        getFirstAttr=sorted(getFirstAttr)        
        winName = "Quick SDK alias"
        winTitle = winName
        if cmds.window(winName, exists=True):
                deleteUI(winName)

        window = cmds.window(winName, title=winTitle, tbm=1, w=350, h=100 )

        menuBarLayout(h=30)
        rowColumnLayout  (' selectArrayRow ', nr=1, w=150)

        frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        
        rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        columnLayout ('selectArrayColumn', parent = 'rMainRow')
        setParent ('selectArrayColumn')
        separator(h=10, p='selectArrayColumn')
        gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))
        attributeFirstSel=optionMenu( label='From')
        for each in getFirstAttr:
            menuItem( label=each)                
        makeAttr=textField()
        cmds.gridLayout('txvaluemeter', p='selectArrayColumn', numberOfColumns=3, cellWidthHeight=(80, 18)) 
        cmds.text(label="1st min/max", w=80, h=25) 
        self.firstMinValue=cmds.textField(w=40, h=25, p='txvaluemeter', text="0")
        self.firstMaxValue=cmds.textField(w=40, h=25, p='txvaluemeter', text="1")  
        cmds.text(label="2nd min/max", w=80, h=25) 
        self.secondMinValue=cmds.textField(w=40, h=25, p='txvaluemeter', text="0")
        self.secondMaxValue=cmds.textField(w=40, h=25, p='txvaluemeter', text="1")
        gridLayout('BuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))             
        button (label='Go', p='BuildButtonLayout', command = lambda *args:self._create_SDK_alias(firstMinValue=float(textField(self.firstMinValue,q=1, text=1)), firstMaxValue=float(textField(self.firstMaxValue,q=1, text=1)), secondMinValue=float(textField(self.secondMinValue,q=1, text=1)), secondMaxValue=float(textField(self.secondMaxValue,q=1, text=1)), getFirstattr=optionMenu(attributeFirstSel, q=1, v=1), floater=optionMenu(makeAttr, q=1, v=1)))
        showWindow(window)   
          
    def _create_SDK_alias(self, firstMinValue, firstMaxValue, secondMinValue, secondMaxValue, getFirstattr, floater):
        getSel=ls(sl=1)
        firstMinValue=float(textField(self.firstMinValue,q=1, text=1))
        firstMaxValue=float(textField(self.firstMaxValue,q=1, text=1))
        secondMinValue=float(textField(self.secondMinValue,q=1, text=1))
        secondMaxValue=float(textField(self.secondMaxValue,q=1, text=1))
        getFirstattr=optionMenu(attributeFirstSel, q=1, v=1)
        floater=textField(makeAttr, q=1, text=1)
        getFirst=getSel[:-1]
        getSecond=getSel[-1]
        anAttr=addAttr([getSecond], ln=floater, min=0, max=1, at="double", k=1, nn=floater)
        Controller=getSecond+"."+floater
        for each in getFirst:
            Child=each+"."+getFirstattr
            setAttr(Child, lock=0) 
            setAttr(Controller, secondMinValue)
            setAttr(Child,firstMinValue)
            setDrivenKeyframe(Child, cd=Controller)
            setAttr(Controller, secondMaxValue)
            setAttr(Child, firstMaxValue)
            setDrivenKeyframe(Child, cd=Controller)
            setAttr(Controller, secondMinValue)
            setAttr(Child, lock=1)        


    def _range_attr_window(self, arg=None):
        getSel=ls(sl=1, fl=1)  
        if len(getSel)>2:
            pass
        else:
            print "need to select 3 or more items" 
            return       
        getFirst=getSel[0]
        global attributeFirstSel
        global makeAttr
        getFirstAttr=[]
        getAttrs=listAttr (getFirst, w=1, a=1, s=1,u=1) 
        for each in getAttrs:
            if ']' in each:
                getNewEach=each.split('.')[-1:]
                getFirstAttr.append(getNewEach[0])
            else:
                getFirstAttr.append(each)
        getFirstAttr=sorted(getFirstAttr)        
        winName = "Randomize/Increment Attribute on Multi Select"
        winTitle = winName
        if cmds.window(winName, exists=True):
                deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=350, h=100 )
        menuBarLayout(h=30)
        rowColumnLayout  (' selectArrayRow ', nr=1, w=150)
        frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        columnLayout ('selectArrayColumn', parent = 'rMainRow')
        setParent ('selectArrayColumn')
        separator(h=10, p='selectArrayColumn')
        gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))
        attributeFirstSel=optionMenu( label='From')
        for each in getFirstAttr:
            menuItem( label=each)                
        self.randomized=checkBox(label="randomize", ann="If on, number within range is randomized. If off, numbers will increment via percentage based on selection against the range")
        cmds.gridLayout('txvaluemeter', p='selectArrayColumn', numberOfColumns=3, cellWidthHeight=(80, 18)) 
        cmds.text(label="range", w=80, h=25) 
        self.firstMinValue=cmds.textField(w=40, h=25, p='txvaluemeter', text="0.0")
        self.firstMaxValue=cmds.textField(w=40, h=25, p='txvaluemeter', text="1.0")  
        gridLayout('BuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))             
        button (label='Go', p='BuildButtonLayout', command = lambda *args:self._range_attr(getSel, randomized=cmds.checkBox(self.randomized,q=True, value=1), getFirstattr=optionMenu(attributeFirstSel, q=1, v=1), firstMinValue=float(textField(self.firstMinValue,q=1, text=1)), firstMaxValue=float(textField(self.firstMaxValue,q=1, text=1))))
        showWindow(window)
        
    def _range_attr(self, getSel, randomized, getFirstattr, firstMinValue, firstMaxValue):
        if randomized==False:
            self._range_inc(getSel, getFirstattr, firstMinValue, firstMaxValue)
        else:
            self._range_random(getSel, getFirstattr, firstMinValue, firstMaxValue)
            
    
    def _range_inc(self, getSel, getFirstattr, firstMinValue, firstMaxValue):
        BucketValue=getClass.Percentages(getSel, firstMinValue, firstMaxValue)
        for each, item in map(None, getSel, BucketValue):
            getChangeAttr=each+'.'+getFirstattr
            cmds.setAttr(getChangeAttr, item)

    def _range_random(self, getSel, getFirstattr, firstMinValue, firstMaxValue):
        for each in getSel:
            getChangeAttr=each+'.'+getFirstattr
            getVal=random.uniform(firstMinValue,firstMaxValue)
            cmds.setAttr(getChangeAttr, getVal)

      

    def _connSDK_alias_window(self, arg=None):
        getSel=ls(sl=1)  
        if len(getSel)>1:
            pass
        else:
            print "need to select 2 or more items" 
            return       
#        global attributeFirstSel
#        global makeAttr   
#        global firstMinValue
#        global firstMaxValue
#        global secondMinValue
#        global secondMaxValue
        getSel=cmds.ls(sl=1)  
        getFirst=getSel[0]      
        getSecond=getSel[1]      
        getFirstAttr=listAttr (getFirst, w=1, a=1, s=1,u=1)     
        getFirstAttr=sorted(getFirstAttr)
        getSecondAttr=cmds.listAttr (getSecond)
        getSecondAttr=sorted(getSecondAttr)         
        winName = "Quick SDK alias"
        winTitle = winName
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=350, h=100 )
        menuBarLayout(h=30)
        rowColumnLayout  (' selectArrayRow ', nr=1, w=150)
        frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        columnLayout ('selectArrayColumn', parent = 'rMainRow')
        setParent ('selectArrayColumn')
        separator(h=10, p='selectArrayColumn')
        gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))
        attributeFirstSel=optionMenu( label='From')
        for each in getFirstAttr:
            menuItem( label=each)                
#        makeAttr=textField()
        makeAttr=cmds.optionMenu( label='To')               
        for each in getSecondAttr:
            cmds.menuItem( label=each)   
        cmds.gridLayout('txvaluemeter', p='selectArrayColumn', numberOfColumns=3, cellWidthHeight=(80, 18)) 
        cmds.text(label="1st min/max", w=80, h=25) 
        self.firstMinValue=cmds.textField(w=40, h=25, p='txvaluemeter', text="0")
        self.firstMaxValue=cmds.textField(w=40, h=25, p='txvaluemeter', text="1")  
        cmds.text(label="2nd min/max", w=80, h=25) 
        self.secondMinValue=cmds.textField(w=40, h=25, p='txvaluemeter', text="0")
        self.secondMaxValue=cmds.textField(w=40, h=25, p='txvaluemeter', text="1")
        gridLayout('BuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))             
        button (label='Go', p='BuildButtonLayout', command = lambda *args:self._conn_SDK_alias(firstMinValue=float(textField(self.firstMinValue,q=1, text=1)), firstMaxValue=float(textField(self.firstMaxValue,q=1, text=1)), secondMinValue=float(textField(self.secondMinValue,q=1, text=1)), secondMaxValue=float(textField(self.secondMaxValue,q=1, text=1)), getFirstattr=optionMenu(attributeFirstSel, q=1, v=1), floater=optionMenu(makeAttr, q=1, v=1)))
        showWindow(window)   
          
    def _conn_SDK_alias(self, firstMinValue, firstMaxValue, secondMinValue, secondMaxValue, getFirstattr, floater):
        getSel=ls(sl=1)
#        firstMinValue=float(textField(self.firstMinValue,q=1, text=1))
#        firstMaxValue=float(textField(self.firstMaxValue,q=1, text=1))
#        secondMinValue=float(textField(self.secondMinValue,q=1, text=1))
#        secondMaxValue=float(textField(self.secondMaxValue,q=1, text=1))
#        getFirstattr=optionMenu(attributeFirstSel, q=1, v=1)
#        floater=optionMenu(makeAttr, q=1, v=1)
        getFirst=getSel[:-1]
        getSecond=getSel[-1]
        #anAttr=addAttr([getSecond], ln=floater, min=0, max=1, at="double", k=1, nn=floater)
        Controller=getSecond+"."+floater
        print Controller
        for each in getFirst:
            Child=each+"."+getFirstattr
            setAttr(Child, lock=0) 
            setAttr(Controller, secondMinValue)
            setAttr(Child,firstMinValue)
            setDrivenKeyframe(Child, cd=Controller)
            setAttr(Controller, secondMaxValue)
            setAttr(Child, firstMaxValue)
            setDrivenKeyframe(Child, cd=Controller)
            setAttr(Controller, secondMinValue)
            setAttr(Child, lock=1)  
            
    def _switch_driven_key_window(self, arg=None):
        getSel=cmds.ls(sl=1)        
        geteattr=cmds.listAttr (getSel[0], ud=1)        
        winName = "select attribute to link the switch constraint driven key to"
        winTitle = winName
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=300, h=100 )
        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=150)
        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        cmds.rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))
        attributeSel=cmds.optionMenu( label='user attribute')
        for each in geteattr:
            cmds.menuItem( label=each)            
        cmds.button (label='Go', p='listBuildButtonLayout', command = lambda *args:self._switch_driven_key(geteattr=cmds.optionMenu(attributeSel, q=1, v=1)))
        cmds.showWindow(window)   
                
    def _switch_driven_key(self, geteattr):
        getSel=cmds.ls(sl=1)
        if getSel:
            pass
        else:
            print "make sure to select a controller with a user attribute and an object with two constraints to switch between"
            return        
        Child=getSel[1]
        firstValue=0
        print firstValue
        secondValue=1
        print secondValue
        Wbucket=[]
        getChild=[(each) for each in cmds.listRelatives(Child, ad=1) if "Constraint" in each]
        print getChild
        for wach in getChild:
            childGetAttr=cmds.listAttr(wach)
            print childGetAttr
        for item in childGetAttr:
            if "W0" in item or "W1" in item :
                Wbucket.append(item)
        if Wbucket:
            print Wbucket
        else:
            print "not enough constraints on child object"
        child_one_constraint=getChild[0]+"."+Wbucket[0]  
        child_two_constraint=getChild[0]+"."+Wbucket[1] 
        print child_two_constraint+" is the first value"        
        print child_one_constraint+" is the second value"
#         geteattr=cmds.listAttr (getSel[0], ud=1, st="*IK")
#         getIKItem=[]
#         for item in geteattr:
#             getIKItem=item   
#         Controller=getSel[0]+"."+getIKItem
#         Controller=getSel[0]+"."+geteattr[0]
        Controller=getSel[0]+"."+geteattr
        print Controller+ " is the Control value I hook up to"
        Child=getChild[0]
        print Child+" is the attribute that is being driven"
        getClass.doubleSetDrivenKey_constraint(Controller, Child, child_one_constraint, child_two_constraint, firstValue, secondValue)


    def _file_texture_manager(self, arg=None):
        maya.mel.eval( "FileTextureManager;" )
    def _open_texture_file_ps(self, arg=None):
        try:
            selObj=cmds.ls(sl=1, fl=1)[0]
            pass
        except:
            print "nothing selected"
        getNodeType=cmds.nodeType(selObj)
        if getNodeType=="file":
            Attr=cmds.listAttr(selObj)
            for each in Attr:
                if "fileTextureName" in each and "Pattern" not in each:
                    getValue=cmds.getAttr(selObj+'.'+each)   
                    getpath=getValue.split("/")
                    getpPath="\\".join(getpath[:-1])
                    getFile=getpath[-1:]
                    getValue=getpPath+"\\"+getFile[0]
                    getValue = r"%s"%getValue           
                    subprocess.Popen([photoshop, getValue])
        else:
            print "need to select a texture node"
    def _open_texture_folder(self, arg=None):
        try:
            selObj=cmds.ls(sl=1, fl=1)[0]
            pass
        except:
            print "nothing selected"
            return
        getNodeType=cmds.nodeType(selObj)
        if getNodeType=="file":
            Attr=cmds.listAttr(selObj)
            for each in Attr:
                if "fileTextureName" in each and "Pattern" not in each:
                    getValue=cmds.getAttr(selObj+'.'+each)  
                    getpath=getValue.split("/")
                    getpPath="\\".join(getpath[:-1])+"\\"
                    print getpPath
                    self.get_path(getpPath)
        else:
            print "need to select a texture node"
    def _open_work_folder(self, arg=None):
        destImagePath=folderPath
        print destImagePath
        self.get_path(destImagePath)  
    def get_path(self, path):
        print path
        if '\\\\' in path:
            newpath=re.sub(r'\\\\',r'\\', path)
            os.startfile(r'\\'+newpath[1:])    
        else:
            os.startfile(path)            
    def _open_texture_file_gmp(self, arg=None):
        try:
            selObj=cmds.ls(sl=1, fl=1)[0]
            pass
        except:
            print "nothing selected"
            return
        getNodeType=cmds.nodeType(selObj)
        if getNodeType=="file":
            Attr=cmds.listAttr(selObj)
            for each in Attr:
                if "fileTextureName" in each and "Pattern" not in each:
                    getValue=cmds.getAttr(selObj+'.'+each)   
                    subprocess.Popen([gimp, getValue])
        else:
            print "need to select a texture node"
    def _add_id(self, queryColor):
        '''----------------------------------------------------------------------------------
        Common add to list function
        ----------------------------------------------------------------------------------'''  
        if queryColor==1:
            color=int(1)      
        elif queryColor==2:
            color=int(6)  
        elif queryColor==3:
            color=int(7)
        elif queryColor==4:
            color=int(8)
        elif queryColor==5:
            color=int(9)
        elif queryColor==6:
            color=int(10  ) 
        elif queryColor==7:
            color=int(16)
        elif queryColor==8:
            color=int(20)
        elif queryColor==9:
            color=int(30)
        selObj=cmds.ls(sl=1)
        for each in range(len(selObj)):
            try:
                cmds.vray("addAttributesFromGroup", selObj[each], "vray_material_id", 1)
            except:
                pass
            try:
                cmds.setAttr (selObj[each]+".vrayMaterialId", color+each)
            except:
                pass        
            
    def _vray_gamma(self, arg=None):
        selObj=cmds.ls(sl=1)
        for each in selObj:
            getNodeType=cmds.nodeType(each)
            if getNodeType=="file":           
                try:
                    cmds.vray("addAttributesFromGroup", each, "vray_file_gamma", 1)
                except:
                    pass       

    def _add_suf(self, arg=None):
        selObj=cmds.ls(sl=1)
        for each in selObj:
            getNode=cmds.nodeType(each)
            if "shadingEngine" in getNode:
                getNode="SG"
            elif "VRay" in getNode or "phong" in getNode or "blinn" in getNode:
                getNode="Shader"
            elif "file" in getNode:
                getNode="FileTexture"
            else:
                getNode=getNode
            if getNode not in each:
                getnewname=each+'_'+getNode
                cmds.rename(each, getnewname)
                
                
    def _shade_network(self, arg=None):
        selObj=cmds.ls(sl=1)[0]
        cmds.hyperShade(selObj, smn=1)
        maya.mel.eval('hyperShadePanelGraphCommand("hyperShadePanel1", "showUpAndDownstream");')
            
    def _add_pref(self, arg=None):
        selObj=cmds.ls(sl=1)        
        getMeshController=cmds.ls("Mesh")[0]
        getChildrenController=cmds.listRelatives(getMeshController, c=1, typ="transform")[0]
        cutName=getChildrenController.split("_")[0:2]
        getNewName='_'.join(cutName)
        for each in selObj:
            if getNewName not in each:
                getnewname=getNewName+'_'+each
                cmds.rename(each, getnewname)
                
    def _select_nonID(self, arg=None):
        try:
            selObj=cmds.ls(sl=1, fl=1)
            pass
        except:
            print "nothing selected"  
        Attr=[(each) for each in selObj if "vrayMaterialId" not in cmds.listAttr(each)]    
        if Attr:
            cmds.select(Attr[0])            
            for each in Attr[1:]:
                cmds.select(each, add=1)
        else:
            print "no missing material ID"