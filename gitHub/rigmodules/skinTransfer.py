import maya.cmds as cmds
from functools import partial
from string import *
import re
import maya.mel
import os, subprocess, sys, platform
from os  import popen
from sys import stdin
import sys, getpass
#import win32clipboard
import operator
getFolderName=getpass.getuser()
from functools import partial

'''MG rigging modules'''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons License'
'http://creativecommons.org/licenses/by-sa/3.0/au/'

filepath= os.getcwd()
sys.path.append(str(filepath))
import baseFunctions_maya
reload (baseFunctions_maya)
getClass=baseFunctions_maya.BaseClass()

class skinTrans(object):
    '''--------------------------------------------------------------------------------------------------------------------------------------
    Interface Layout
    --------------------------------------------------------------------------------------------------------------------------------------'''          
    def __init__(self, winName="XML Path"):
        self.winTitle = "XML Path"
        self.winName = winName

    def performTranferV1(self):
        getMesh=cmds.ls(sl=1)
        if len(getMesh)<2:
            print "select a skinned mesh group and an unskinned target mesh group"
            return
        else:
            pass
        getMeshController=getMesh[0]
        getMeshTarget=getMesh[1]
        getChildrenController=cmds.listRelatives(getMeshController, c=1, typ="transform")
        if getChildrenController==None:
            getChildrenController=([getMeshController])
        getChildrenTarget=cmds.listRelatives(getMeshTarget, c=1, typ="transform")
        if getChildrenTarget==None:
            getChildrenTarget=([getMeshTarget])
        result = cmds.promptDialog( 
                    title='find XML', 
                    message="Enter path", 
                    text="C:\Users\\"+str(getFolderName)+"\Documents\maya\projects\default\scenes\\", 
                    button=['Continue','Cancel'],
                    defaultButton='Continue', 
                    cancelButton='Cancel', 
                    dismissString='Cancel' )
        if result == 'Continue':
            skinPath=cmds.promptDialog(q=1)
            if skinPath:
                pass
            else:
                print "nothing collected"
        self.callJointsWin(getChildrenController, getChildrenTarget, skinPath)

        
        
    def performTransfer(self):
        getMesh=cmds.ls(sl=1)
        if len(getMesh)<2:
            print "select a skinned mesh group and an unskinned target mesh group"
            return
        else:
            pass
        getMeshController=getMesh[0]
        getMeshTarget=getMesh[1]
        getChildrenController=cmds.listRelatives(getMeshController, c=1, typ="transform")
        if getChildrenController==None:
            getChildrenController=([getMeshController])
        getChildrenTarget=cmds.listRelatives(getMeshTarget, c=1, typ="transform")
        if getChildrenTarget==None:
            getChildrenTarget=([getMeshTarget])

        ####Window
        #folderPath="G:\\_PIPELINE_MANAGEMENT\\Published\\maya\\guides\\"
        winName = "Save xml"
        winTitle = winName
        global skinPath
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)

        window = cmds.window(winName, title=winTitle, tbm=1, w=300, h=100 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=300)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        
        cmds.rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=1, cellWidthHeight=(300, 20))      
        skinPath=cmds.textField(w=250, h=25, p='listBuildButtonLayout', tx="C:\Users\\"+str(getFolderName)+"\Documents\maya\projects\default\scenes\\")
        cmds.button (w=80, label='Proceed', p='listBuildButtonLayout', command = lambda *args:self.callJointsWin(getChildrenController, getChildrenTarget, skinPath))
        cmds.button (w=80,label='Open folder', p='listBuildButtonLayout', command = lambda *args:self.get_path(skinPath))
        cmds.showWindow(window)     
        ###Window
        
        
        #self.callJointsWin(getChildrenController, getChildrenTarget, skinPath)
#     def launchExp(skinPath):
#         os.system('explorer "c:\program files"')


    def _launch_exp(self, folderPath):
#         os.system('explorer'+folderPath)
        destImagePath=folderPath
        self.get_path(destImagePath)    
        
    def get_path(self, skinPath):
        path=cmds.textField(skinPath, q=1, text=True)
        print path
        if '\\\\' in path:
            newpath=re.sub(r'\\\\',r'\\', path)
            os.startfile(r'\\'+newpath[1:])    
        else:
            os.startfile(path)
            
    def callJointsWin(self, getChildrenController, getChildrenTarget, skinPath):
        skinPath=cmds.textField(skinPath, q=1, text=True)
        try:
            getallnames=cmds.ls("*Rig:*")
        except:
            print "No rig is loaded. Please ensure 'Rig' is at the end of the name"
        bucket=[]
        for each in  getallnames:
            foundFirst=each.split(":")[0]
            bucket.append(foundFirst)
        bucket=set(bucket)
        global jointSelect
        winName = "Swap Influence select"
        winTitle = winName
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)

        window = cmds.window(winName, title=winTitle, tbm=1, w=300, h=100 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=300)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        
        cmds.rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))
        jointSelect=cmds.optionMenu( label='joints')
        for each in bucket:
            cmds.menuItem( label=each)        
        #cmds.button (label='set joint', p='listBuildButtonLayout', command = partial(self.transferFunction(getChildrenController, getChildrenTarget, skinPath)))
        cmds.button (label='set mass', p='listBuildButtonLayout', command = lambda *args:self.transferFunction(getChildrenController, getChildrenTarget, skinPath))
        cmds.button (label='set single', p='listBuildButtonLayout', command = lambda *args:self.transferSingleFunction(getChildrenController, getChildrenTarget, skinPath))

        cmds.showWindow(window)

    def transferFunction(self, getChildrenController, getChildrenTarget, skinPath):
        queryJoint=cmds.optionMenu(jointSelect, q=1, v=1)
        queryJoint=queryJoint+":"
        for each, item in map(None, getChildrenController, getChildrenTarget):
            try:
                newname, skinID=getClass.getSkinWeightsforXML(each)
                cmds.deformerWeights (newname+".xml", p=skinPath,  ex=True, deformer=skinID)
                print "deformer weights have been exported from "+each
            except:
                print "shape missing"  
                pass
            try:
                GetPath=skinPath+newname+".xml"
            except:
                print  each+" does not have a skinCluster to reference from"
            getCtrlItemName=each.split(":")
            getTgtItemName=item.split(":")
            getOldMeshNameSpace=':'.join(getCtrlItemName[:-1])+":"
            newAssetsNamespace=':'.join(getTgtItemName[:-1])+":"
            if getCtrlItemName[-1:][0] ==getTgtItemName[-1:][0]:
                try:
                    getSkinCluster=cmds.skinCluster(each, q=1, dt=1)
                    skinID, getInf=getClass.skinClust(getSkinCluster, each)   
                    getJointNameSpace=getInf[0].split(":")
                    getOldJointNameSpace=':'.join(getJointNameSpace[:-1])+":"
                    dataFromTextFile=open(GetPath).read()
                    dataFromTextFile=dataFromTextFile.replace(getOldJointNameSpace, queryJoint)
                    if "face" in getOldJointNameSpace:
                        dataFromTextFile=dataFromTextFile.replace(getOldJointNameSpace, "")
                    replacedDataTextFile=open(GetPath, 'w')
                    replacedDataTextFile.write(dataFromTextFile)
                    replacedDataTextFile.close() 
                    print "xml has been updated with new joint names"                             
                    pass
                except:
                    print "shape is missing - passed"
                    pass
                if getInf:
                    getJointBucket=[]
                    for jointItem in getInf:
                        getJointName=jointItem.split(":")
                        getJoint=getJointName[-1:][0]
                        getNewJoint=queryJoint+getJoint
                        getJointBucket.append(getNewJoint)
                    try:
                        cmds.select(item)
                    except:
                        pass
                    try:
                        cmds.skinCluster(item,getJointBucket[0], tsb=1, nw=1)
                        print item+" has been successfully bound to "+getJointBucket[0]
                        if len(getJointBucket)>1:
                            for eachjoint in getJointBucket[1:]:
                                try:
                                    cmds.skinCluster(item, e=1, ai=eachjoint, tsb=1, nw=1) 
                                    print eachjoint+" has been successfully added to "+item
                                except:
                                    pass              
                    except:
                        print item+" is already bound"      
                    try:                
                        newItemName, newskinID=getClass.getSkinWeightsforXML(item)
                        cmds.deformerWeights (newname+".xml", p=skinPath, im=True, deformer=newskinID) 
                        print "deformer weights have been applied to "+newItemName
                    except:
                        print "can't find object for "+item
                        pass
    def transferSingleFunction(self, getChildrenController, getChildrenTarget, skinPath):
        print "here is "+getChildrenController[0], getChildrenTarget[0]
        queryJoint=cmds.optionMenu(jointSelect, q=1, v=1)
        queryJoint=queryJoint+":"
        try:
            newname, skinID=getClass.getSkinWeightsforXML(getChildrenController[0])
            cmds.deformerWeights (newname+".xml", p=skinPath,  ex=True, deformer=skinID)
            print "deformer weights have been exported from "+getChildrenController[0]
        except:
            print "shape missing"  
            pass
        try:
            GetPath=skinPath+newname+".xml"
        except:
            print  getChildrenController[0]+" does not have a skinCluster to reference from"
        getCtrlgetChildrenTargetName=getChildrenController[0].split(":")
        getTgtgetChildrenTargetName=getChildrenTarget[0].split(":")
        getOldMeshNameSpace=':'.join(getCtrlgetChildrenTargetName[:-1])+":"
        try:
            getSkinCluster=cmds.skinCluster(getChildrenController[0], q=1, dt=1)
            skinID, getInf=getClass.skinClust(getSkinCluster, getChildrenController[0])   
            getJointNameSpace=getInf[0].split(":")
            getOldJointNameSpace=':'.join(getJointNameSpace[:-1])+":"
            dataFromTextFile=open(GetPath).read()
            dataFromTextFile=dataFromTextFile.replace(getOldJointNameSpace, queryJoint)
            if "face" in getOldJointNameSpace:
                dataFromTextFile=dataFromTextFile.replace(getOldJointNameSpace, "")            
            replacedDataTextFile=open(GetPath, 'w')
            replacedDataTextFile.write(dataFromTextFile)
            replacedDataTextFile.close() 
            print "xml has been updated with new joint names"                             
            pass
        except:
            print "shape is missing - passed"
            pass
        getJointBucket=[]
        for jointItem in getInf:
            getJointName=jointItem.split(":")
            getJoint=getJointName[-1:][0]
            getNewJoint=queryJoint+getJoint
            getJointBucket.append(getNewJoint)
        cmds.select(getChildrenTarget[0])
        try:
            cmds.skinCluster(getChildrenTarget[0],getJointBucket[0], tsb=1, nw=1)
            print getChildrenTarget[0]+" has been successfully bound to "+getJointBucket[0]
            if len(getJointBucket)>1:
                for eachjoint in getJointBucket[1:]:
                    try:
                        cmds.skinCluster(getChildrenTarget[0], e=1, ai=eachjoint, tsb=1, nw=1) 
                        print eachjoint+" has been successfully added to "+getChildrenTarget[0]
                    except:
                        pass              
        except:
            print getChildrenTarget[0]+" is already bound"                      
        newgetChildrenTargetName, newskinID=getClass.getSkinWeightsforXML(getChildrenTarget[0])
        cmds.deformerWeights (newname+".xml", p=skinPath, im=True, deformer=newskinID) 
        print "deformer weights have been applied to "+newgetChildrenTargetName
