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
getClass = baseFunctions_maya.BaseClass()


import stretchIK
reload (stretchIK)
getIKClass = stretchIK.stretchIKClass()  
BbxName="ControlBox"
BbxFilepath="G:\\_PIPELINE_MANAGEMENT\\Published\\maya\\ControlBox\\"+BbxName+".ma"
LashFile="EyeLash"
LashPath="G:\\_PIPELINE_MANAGEMENT\\Published\\maya\\eyelash\\"+LashFile+".ma"

getFace=[(each) for each in cmds.ls("face*_guide",) if "Teeth" not in each and "Tongue" not in each and "Brow" not in each]
# try:
#     getHead=cmds.ls("*:head02_jnt")
# except:
#     getHead=cmds.ls("*head02_jnt")     
# try:
#     getHeadJnt1=cmds.ls("*:head01_jnt")
# except:
#     getHeadJnt1=cmds.ls("*head01_jnt")             
# try:
#     getJaw=cmds.ls("*:Jaw_jnt")
# except:
#     getJaw=cmds.ls("Jaw_jnt")   
# try:
#     getEyeMask=cmds.ls("*:EyeMask_Ctrl")
# except:
#     getEyeMask=cmds.ls("EyeMask_Ctrl")   
# try:
#     getJawNod=cmds.ls("*:Jaw_Ctrl_nod")
# except:
#     getJawNod=cmds.ls("Jaw_Ctrl_nod")
# try:
#     getChin=cmds.ls("*:Chin_Ctrl")
# except:
#     getChin=cmds.ls("Chin_Ctrl")
# try:
#     getChinSDK=cmds.ls("*:Chin_SDK")
# except:
#     getChinSDK=cmds.ls("Chin_SDK")
# try:
#     getHeadCtrl=cmds.ls("*:Head_Ctrl")
# except:
#     getHeadCtrl=cmds.ls("Head_Ctrl")
                        
if cmds.ls("*:head01_jnt"):
    getHeadJnt1=cmds.ls("*:head01_jnt")[0]
elif cmds.ls("head01_jnt"):
    getHeadJnt1=cmds.ls("head01_jnt")[0]
    
if cmds.ls("*:head02_jnt"):
    getHead=cmds.ls("*:head02_jnt")[0]
elif cmds.ls("head02_jnt"):
    getHead=cmds.ls("head02_jnt")[0]
    
if cmds.ls("*:Jaw_jnt"):
    getJaw=cmds.ls("*:Jaw_jnt")[0]
elif cmds.ls("Jaw_jnt"):
    getJaw=cmds.ls("Jaw_jnt")[0]
                        
if cmds.ls("*:EyeMask_Ctrl"):
    getEyeMask=cmds.ls("*:EyeMask_Ctrl")[0]
elif cmds.ls("EyeMask_Ctrl"):
    getEyeMask=cmds.ls("EyeMask_Ctrl")[0]
    
if cmds.ls("*:Head_Ctrl"):
    getHeadCtrl=cmds.ls("*:Head_Ctrl")[0]
elif cmds.ls("Head_Ctrl"):
    getHeadCtrl=cmds.ls("Head_Ctrl")[0]
    
if cmds.ls("*:Chin_SDK"):
    getChinSDK=cmds.ls("*:Chin_SDK")[0]
elif cmds.ls("Chin_SDK"):
    getChinSDK=cmds.ls("Chin_SDK")[0]
    
if cmds.ls("*:Chin_Ctrl"):
    getChin=cmds.ls("*:Chin_Ctrl")[0]
elif cmds.ls("Chin_Ctrl"):
    getChin=cmds.ls("Chin_Ctrl")[0]
    
if cmds.ls("*:Jaw_Ctrl_nod"):
    getJawNod=cmds.ls("*:Jaw_Ctrl_nod")[0]
elif cmds.ls("Jaw_Ctrl_nod"):
    getJawNod=cmds.ls("Jaw_Ctrl_nod")[0]


class FaceSetup(object):
    '''--------------------------------------------------------------------------------------------------------------------------------------
    Interface Layout
    -------------------------------------------------------------------------------------------------------------------------------------'''          
        
        
    def controller(self):
        #cmds.file(BbxFilepath,  r=1, sns=["ControlBox:",""], type="mayaAscii", iv=1, gl=1, gr=1, gn="ControlBox",mnc=0,  op=1)
        cmds.file(BbxFilepath, i=1,  type="mayaAscii", iv=1, mnc=0, gr=1, gn="FaceRig", op=1, rpr=BbxName)
        try:
            getBox=cmds.ls("BigBox_CC_grp") 
        except:
            getBox=cmds.ls("*:BigBox_CC_grp")  
        getTranslation, getRotation=getClass.locationXForm(getHeadCtrl)
        cmds.move(getTranslation[0]+40, getTranslation[1]+15, getTranslation[2], getBox)
        cmds.parentConstraint(getHeadCtrl,getBox, mo=1)
        print "Controller box present"
        

    def _lash_win(self, arg=None):
        getAllSets=["LashTopRight_RIV", "LashMidRight_RIV", "LashBotRight_RIV", "LashTopLeft_RIV", "LashMidLeft_RIV", "LashBotLeft_RIV"]
        global rivetSelect
        winName = "EyeLash Rivets"
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
        rivetSelect=cmds.optionMenu( label='LashRivets')
        for each in getAllSets:
            cmds.menuItem( label=each)        
        cmds.button (label='Create Lash Rivet', p='listBuildButtonLayout', command = lambda *args:self._add_lash_rivet())

        cmds.showWindow(window)

    def _add_lash_rivet(self, arg=None):
        queryRivet=cmds.optionMenu(rivetSelect, q=1, v=1)       
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
                   
    def AddLash(self):
        TopRight=[
                "Lash_T_R_1_grp",
                "Lash_T_R_2_grp",
                "Lash_T_R_3_grp"
                ]
        MidRight=[                  
                "Lash_M_R_1_grp",
                "Lash_M_R_2_grp",
                "Lash_M_R_3_grp",
                ]
        BotRight=[
                "Lash_B_R_1_grp",
                "Lash_B_R_2_grp",
                "Lash_B_R_3_grp",
                ]
        BotLeft=[
                "Lash_B_L_1_grp",
                "Lash_B_L_2_grp",
                "Lash_B_L_3_grp",
                ]        
        MidLeft=[
                "Lash_M_L_1_grp",
                "Lash_M_L_2_grp",
                "Lash_M_L_3_grp",
                ]        
        TopLeft=[
                "Lash_T_L_1_grp",
                "Lash_T_L_2_grp",
                "Lash_T_L_3_grp"
                ]        
        #cmds.file(BbxFilepath,  r=1, sns=["ControlBox:",""], type="mayaAscii", iv=1, gl=1, gr=1, gn="ControlBox",mnc=0,  op=1)
        getLashGroupsForRemove=TopRight+MidRight+BotRight+TopLeft+MidLeft+BotLeft
        if cmds.ls(getLashGroupsForRemove):
            for each in getLashGroupsForRemove:
                cmds.delete(each)
        else:
            pass
        if cmds.ls("eyeLashRig"):
            getEyeRigForDelete=cmds.ls("eyeLashRig")
            cmds.delete(getEyeRigForDelete)                
        else:
            pass
        cmds.file(LashPath, i=1,  type="mayaAscii", iv=1, mnc=0, op=1, rpr=LashFile)
        cmds.parent("eyeLashRig","FaceRig")
        #skin left lash
        self.skinLash()
        cmds.connectAttr("*:EyeMask_Ctrl.Blink_Left", "Lash_attribute_holder.Blink_Left")
        cmds.connectAttr("*:EyeMask_Ctrl.Blink_Right", "Lash_attribute_holder.Blink_Right")
        cmds.connectAttr( "*:EyeMask_Ctrl.LeftBlinkHeight", "Lash_attribute_holder.LeftBlinkHeight")
        cmds.connectAttr( "*:EyeMask_Ctrl.RightBlinkHeight", "Lash_attribute_holder.RightBlinkHeight")  

        for each in TopRight:
            cmds.parent(each, "LashTopRight_RIV")  
        try:
            cmds.parent("LashTopRight_RIV","FaceRig")
        except:
            pass

        for each in MidRight:
            cmds.parent(each, "LashMidRight_RIV")  
        try:
            cmds.parent("LashMidRight_RIV","FaceRig")
        except:
            pass                 

        for each in BotRight:
            cmds.parent(each, "LashBotRight_RIV") 
        try:
            cmds.parent("LashBotRight_RIV","FaceRig")
        except:
            pass               

        for each in BotLeft:
            cmds.parent(each,"LashBotLeft_RIV")
        try:
            cmds.parent("LashBotLeft_RIV","FaceRig")
        except:
            pass                          
        for each in MidLeft:
            cmds.parent(each, "LashMidLeft_RIV")
        try:
            cmds.parent("LashMidLeft_RIV","FaceRig")
        except:
            pass                                 
        for each in TopLeft:
            cmds.parent(each,  "LashTopLeft_RIV")
        try:                
            cmds.parent("LashTopLeft_RIV","FaceRig")
        except:
            pass             
        print "Lashes connected"
        
    def skinLash(self):
        LeftLashJoints=[
                        "Lash_B_L_1_jnt",
                        "Lash_B_L_2_jnt",
                        "Lash_B_L_3_jnt",
                        "Lash_M_L_1_jnt",
                        "Lash_M_L_2_jnt",
                        "Lash_M_L_3_jnt",
                        "Lash_T_L_1_jnt",
                        "Lash_T_L_2_jnt",
                        "Lash_T_L_3_jnt"
                        ]
        RightLashJoints=[
                        "Lash_M_R_1_jnt",
                        "Lash_M_R_2_jnt",
                        "Lash_M_R_3_jnt",
                        "Lash_B_R_1_jnt",
                        "Lash_B_R_2_jnt",
                        "Lash_B_R_3_jnt",
                        "Lash_T_R_1_jnt",
                        "Lash_T_R_2_jnt",
                        "Lash_T_R_3_jnt"
                        ]        
        getLeftLashMesh=cmds.ls("*Mesh:*EyeLash_L") 
        if not getLeftLashMesh:
            getLeftLashMesh=cmds.ls("*Mesh*:*EyeLash_L")       
        try:
            cmds.skinCluster(getLeftLashMesh, e=1, ub=1)
        except:
            pass
        cmds.skinCluster(getLeftLashMesh,LeftLashJoints[0])
        for each in LeftLashJoints[1:]:
            try:
                cmds.skinCluster(getLeftLashMesh, e=1, ai=each)    
            except:
                pass    
        getSkinCluster=cmds.skinCluster(getLeftLashMesh, q=1, dt=1)
        for item in getSkinCluster:
            if "GroupId" in item:
                destSkinID_L=[eachDefObj for eachDefObj in cmds.listConnections(item, s=1) if cmds.nodeType(eachDefObj)=="skinCluster"][0]   
        getSkinCluster=cmds.skinCluster("EyeLash_L_SKN", q=1, dt=1)
        for item in getSkinCluster:
            if "GroupId" in item:
                srcSkinID=[eachDefObj for eachDefObj in cmds.listConnections(item, s=1) if cmds.nodeType(eachDefObj)=="skinCluster"][0]            
        cmds.copySkinWeights(ss=srcSkinID, ds=destSkinID_L, nm=1, sa="closestPoint", ia="closestJoint")     
        cmds.setAttr(destSkinID_L+".skinningMethod", 1)  
        #skin right lash
        getRightLashMesh=cmds.ls("*Mesh:*EyeLash_R") 
        if not getRightLashMesh:
            getRightLashMesh=cmds.ls("*Mesh*:*EyeLash_R")  
        try:
            cmds.skinCluster(getRightLashMesh, e=1, ub=1)
        except:
            pass
        cmds.skinCluster(getRightLashMesh,RightLashJoints[0])
        for each in RightLashJoints[1:]:
            try:
                cmds.skinCluster(getRightLashMesh, e=1, ai=each)    
            except:
                pass     
        getSkinCluster=cmds.skinCluster(getRightLashMesh, q=1, dt=1)
        for item in getSkinCluster:
            if "GroupId" in item:
                destSkinID_R=[eachDefObj for eachDefObj in cmds.listConnections(item, s=1) if cmds.nodeType(eachDefObj)=="skinCluster"][0]             
        getSkinCluster=cmds.skinCluster("EyeLash_R_SKN", q=1, dt=1)         
        for item in getSkinCluster:
            if "GroupId" in item:
                SrcSkinID=[eachDefObj for eachDefObj in cmds.listConnections(item, s=1) if cmds.nodeType(eachDefObj)=="skinCluster"][0]      
        cmds.copySkinWeights(ss=SrcSkinID, ds=destSkinID_R, nm=1, sa="closestPoint", ia="closestJoint")
        cmds.setAttr(destSkinID_R+".skinningMethod", 1)          
#         cmds.copySkinWeights(ss=SrcSkinID, ds=destSkinID_R, nm=1, sa="closestPoint", ia="closestJoint")
                        
    def save_placement(self):
        result = cmds.promptDialog( 
                    title='Confirm', 
                    message='filename', 
                    button=['Continue','Cancel'],
                    defaultButton='Continue', 
                    cancelButton='Cancel', 
                    dismissString='Cancel' )
        if result == 'Continue':
            filename=cmds.promptDialog(q=1)
        else:
            print "nothing collected"
        printFolder="G:\\_PIPELINE_MANAGEMENT\\Published\\maya\\guides\\FaceLayout\\"+filename+"_TRN.txt"
        getGuides=cmds.ls("*_TRN")
        inp=open(printFolder, 'w+')
        for each in getGuides:
            transform=cmds.xform(each , q=True, ws=1, t=True)
            if transform==[0, 0, 0]:
                transformWorldMatrix = cmds.xform(each, q=True, wd=1, sp=True)  
                rotateWorldMatrix = cmds.xform(each, q=True, wd=1, ra=True) 
            else:
                transformWorldMatrix = cmds.xform(each, q=True, wd=1, t=True)  
                rotateWorldMatrix = cmds.xform(each, q=True, wd=1, ro=True) 
                print str(each)+":"+str(transformWorldMatrix)+":"+str(rotateWorldMatrix)
            inp=open(printFolder, 'a+')
            inp.write(str(each)+":"+str(transformWorldMatrix)+":"+str(rotateWorldMatrix)+'\r\n')
        inp.close()  
        
        
        if '\\\\' in printFolder:
            newpath=re.sub(r'\\\\',r'\\', printFolder)
            os.startfile(r'\\'+newpath[1:])    
        else:
            os.startfile(printFolder)  
        print "saved face nodes placement"

    def load_placement(self, arg=None):    
        guideDict={}
        result = cmds.promptDialog( 
                    title='Confirm', 
                    message='open file', 
                    button=['Continue','Cancel'],
                    defaultButton='Continue', 
                    cancelButton='Cancel', 
                    dismissString='Cancel' )
        if result == 'Continue':
            filename=cmds.promptDialog(q=1)
            
        printFolder="G:\\_PIPELINE_MANAGEMENT\\Published\\maya\\guides\\FaceLayout\\"+filename+"_TRN.txt"
        
#         Ggrp=cmds.CreateEmptyGroup()
#         cmds.rename(Ggrp, "Guides_"+filename+"_grp")
        print printFolder
        inp=open(printFolder, 'r')
        
        List = open(printFolder).readlines()
        
        
        for each in List:
            newlocbucket=[]
            newrotbucket=[]    
            getDictParts=each.split(':')
            getlocpart=getDictParts[1].strip('[]')
            getlocpart=getlocpart.split(', ')
            for item in getlocpart:
                newlocbucket.append(item)
            getrotpart=getDictParts[2].strip('[]]\r\n')
            getrotpart=getrotpart.split(', ')
            for item in getrotpart:
                getit=item.split('.')
                getint=int(getit[0])
                newrotbucket.append(getint)
            newlocbucket.append(newrotbucket)
            makeDict={getDictParts[0]:newlocbucket}
            guideDict.update(makeDict)
                           
        for key, value in guideDict.items():
#             colour1, colour2, colour3=17, 17, 17
            transformWorldMatrix, rotateWorldMatrix=[value[0], value[1], value[2]], value[3]
            cmds.move(value[0], value[1], value[2], key)
            cmds.rotate(value[3][0], value[3][1],value[3][2], key)
            #getClass.guideBuild(key, transformWorldMatrix, rotateWorldMatrix, colour1, colour2, colour3)
            #cmds.parent(key,"Guides_"+filename+"_grp")
            print "loaded placenodes placement"
            
    def connect_to_head(self):
        faceSDKToRigGroup=(
            "faceCheekBone_R_grp",
            "faceCheek_T_R_grp",
            "faceLip_T_R_grp",
            "faceNose_grp",
            "faceCheekBone_L_grp",
            "faceCheek_T_L_grp",
            "faceLip_Corner_L_grp",
            "faceCheek_R_grp",
            "faceLip_Corner_R_grp",
            "faceLip_T_grp",
            "faceNose_R_grp",
            "faceCheek_L_grp",
            "faceLip_T_L_grp",
            "faceNose_L_grp")
        HeadGrp=(
             #"faceLid_Open05_T_R_grp",
            "faceLid_Open04_T_R_grp",
            "faceLid_Open02_T_R_grp",
            "faceLid_Open04_T_L_grp",
            "faceLid_Open03_T_L_grp",
            "faceLid_Open02_T_L_grp",
            "faceLid_Open04_B_R_grp",
            "faceLid_Open03_B_R_grp",
            "faceLid_Open02_B_R_grp",
            "faceLid_Open05_B_L_grp",
            "faceLid_Open04_B_L_grp",
            "faceLid_Open03_B_L_grp",
            "faceLid_Open02_B_L_grp",
            "faceLid_Open05_B_R_grp",
            "faceLid_Open03_T_R_grp",
            "Teeth_Handle_T_Ctrl_grp")
        for each in HeadGrp:
            cmds.parent(each, getHeadCtrl)
        lidPivot=(
            #"faceLid_Open05_T_R_lctrLid_Pivot_jnt",
            "faceLid_Open04_T_R_lctrLid_Pivot_jnt",
            "faceLid_Open03_T_R_lctrLid_Pivot_jnt",
            "faceLid_Open02_T_R_lctrLid_Pivot_jnt",
            "faceLid_Open01_T_R_lctrLid_Pivot_jnt",
            "faceLid_Closed05_R_lctrLid_Pivot_jnt",
            "faceLid_Closed04_R_lctrLid_Pivot_jnt",
            "faceLid_Closed03_R_lctrLid_Pivot_jnt",
            "faceLid_Closed02_R_lctrLid_Pivot_jnt",
            "faceLid_Closed01_R_lctrLid_Pivot_jnt",
            #"faceLid_Open05_T_L_lctrLid_Pivot_jnt",
            "faceLid_Open04_T_L_lctrLid_Pivot_jnt",
            "faceLid_Open03_T_L_lctrLid_Pivot_jnt",
            "faceLid_Open02_T_L_lctrLid_Pivot_jnt",
            "faceLid_Open01_T_L_lctrLid_Pivot_jnt",
            "faceLid_Closed05_L_lctrLid_Pivot_jnt",
            "faceLid_Closed04_L_lctrLid_Pivot_jnt",
            "faceLid_Closed03_L_lctrLid_Pivot_jnt",
            "faceLid_Closed02_L_lctrLid_Pivot_jnt",
            "faceLid_Closed01_L_lctrLid_Pivot_jnt")
        for each in lidPivot:
            cmds.parent(each, getHeadJnt1)
        faceControllers=(
            "faceCheekBone_R_grp",
            "faceCheek_T_R_grp",
            "faceLip_T_R_grp",
            "faceNose_grp",
            "faceCheekBone_L_grp",
            "faceCheek_T_L_grp",
            "faceLip_Corner_L_grp",
            "faceCheek_R_grp",
            "faceLip_Corner_R_grp",
            "faceLip_T_grp",
            "faceNose_R_grp",
            "faceCheek_L_grp",
            "faceLip_T_L_grp",
            "faceNose_L_grp")
        for each in faceControllers:
            cmds.parentConstraint(getHead, each, mo=1) 
        getBrows=cmds.ls("faceBrow*_grp")
        for each in getBrows:
            cmds.parent(each, getHead)
        lowerLip=("faceLip_B_L_grp", "faceLip_B_grp", "faceLip_B_R_grp")
        for each in lowerLip:
            if "faceLip_B_grp" in each:
                cmds.parentConstraint(getJaw, each, mo=1, w=1)
            else:
                cmds.parentConstraint(getHeadJnt1, each, mo=1, w=.2) 
                cmds.parentConstraint(getJaw, each, mo=1, w=.8) 
            #cmds.parent(each, "faceRig")

        cmds.parent("faceTongue_Master_grp", getJaw)
#         cmds.select("Chin_TRN_lctr")
#         cmds.select(getChinSDK, add=1)
#         cmds.copyAttr(v=1, ic=1 , ksc=1, cpc=1, rtc=1)
        getEyes=cmds.ls("*Pivot_jnt")
        for each in getEyes:
            getEnd=cmds.listRelatives(each, c=1, typ="joint")
            getConst=cmds.listRelatives(getEnd, c=1, type="parentConstraint")#find current constraint parent
            getConnection=cmds.listConnections(getConst,s=1, d=0, p=1, t="parentConstraint")
            getDest=cmds.connectionInfo(getConnection[0], ges=1)
            cmds.delete(getConst)
            createHandle=cmds.ikHandle(n=each+"_ik", sj=each, ee=getEnd[0], sol="ikSCsolver")#create IK handle
            getObject=getDest.split(".")[1]
            isolateParent=getObject.split("W")[0]
            getTrueParent=isolateParent.split("face")[1]
            lognm=getTrueParent.replace("TRN_Ctrl", "Ctrl")
            cmds.parent(createHandle[0], lognm)
        cmds.parent("Teeth_Handle_B_Ctrl_grp",getJaw)
        cmds.parent("faceJaw_R_grp", getJaw)
        cmds.parent("faceJaw_L_grp", getJaw)

        Controller=str(getChin[0])+".translateY"
        Child="Jaw_R_SDK_grp.translateX"
        cmds.setAttr(Controller, 0)
        cmds.setAttr(Child,0)
        cmds.setDrivenKeyframe(Child, cd=Controller)
        cmds.setAttr(Controller, -7)
        cmds.setAttr(Child, -1.5)
        cmds.setDrivenKeyframe(Child, cd=Controller)
        cmds.setAttr(Controller, 0)
        cmds.setAttr(Child, lock=1)
            
        Controller=str(getChin[0])+".translateY"
        Child="Jaw_L_SDK_grp.translateX"
        cmds.setAttr(Controller, 0)
        cmds.setAttr(Child,0)
        cmds.setDrivenKeyframe(Child, cd=Controller)
        cmds.setAttr(Controller, -7)
        cmds.setAttr(Child, 1.5)
        cmds.setDrivenKeyframe(Child, cd=Controller)
        cmds.setAttr(Controller, 0)
        cmds.setAttr(Child, lock=1) 
        cmds.select("Chin_TRN_lctr")
        cmds.select("*:Chin_SDK", add=1)
        cmds.copyAttr(values=1, inConnections=1, containerParentChild=1)
        getTongue=cmds.ls("faceTongue*_TRN")
        for each in getTongue:
            cmds.parent(each,"faceTongue_Master_Ctrl")        
        cmds.parentConstraint(getHead, "faceLip_Corner_R_grp", mo=1, w=.5)
        cmds.parentConstraint(getJaw, "faceLip_Corner_R_grp", mo=1, w=.5)
        cmds.parentConstraint(getHead, "faceLip_Corner_L_grp", mo=1, w=.5)
        cmds.parentConstraint(getJaw, "faceLip_Corner_L_grp", mo=1, w=.5)
        cmds.connectAttr("*:EyeMask_Ctrl.CheekLeftUp","Phonemes_CC.CheekLeftUp")
        cmds.connectAttr("*:EyeMask_Ctrl.CheekRightUp","Phonemes_CC.CheekRightUp") 
        cmds.setAttr("Phonemes_CC.CheekLeftUp", cb=0, k=0)
        cmds.setAttr("Phonemes_CC.CheekRightUp", cb=0, k=0)
        cmds.setAttr("BigBox_CC.ShowSDKControls", 0)
        cmds.select( "*:BodyControllers" )
        cmds.pickWalk(d="Down")
        getBodyCtrls=[(each) for each in cmds.ls(sl=1) if "*:Eye*" not in each and "Waist" not in each and "Hand_L_Ctrl" not in each and "Hand_R_Ctrl" not in each]
        for each in getBodyCtrls:
            cmds.connectAttr("BigBox_CC.ShowBodyControls", each+".visibility")
        faceCtrl=cmds.ls("faceCheek*_grp")
        for each in faceCtrl:
            cmds.parent(each, getHeadCtrl)    
        faceCtrl=cmds.ls("faceLip*_grp")
        for each in faceCtrl:
            cmds.parent(each, getHeadCtrl)   
        faceCtrl=cmds.ls("faceNose*_grp")
        for each in faceCtrl:
            cmds.parent(each, getHeadCtrl)         
        print "connected controller box to head"

    def reconnect_to_head(self):
        faceSDKToRigGroup=(
            "faceCheekBone_R_grp",
            "faceCheek_T_R_grp",
            "faceLip_T_R_grp",
            "faceNose_grp",
            "faceCheekBone_L_grp",
            "faceCheek_T_L_grp",
            "faceLip_Corner_L_grp",
            "faceCheek_R_grp",
            "faceLip_Corner_R_grp",
            "faceLip_T_grp",
            "faceNose_R_grp",
            "faceCheek_L_grp",
            "faceLip_T_L_grp",
            "faceNose_L_grp")
        HeadGrp=(
             #"faceLid_Open05_T_R_grp",
            "faceLid_Open04_T_R_grp",
            "faceLid_Open02_T_R_grp",
            "faceLid_Open04_T_L_grp",
            "faceLid_Open03_T_L_grp",
            "faceLid_Open02_T_L_grp",
            "faceLid_Open04_B_R_grp",
            "faceLid_Open03_B_R_grp",
            "faceLid_Open02_B_R_grp",
            "faceLid_Open05_B_L_grp",
            "faceLid_Open04_B_L_grp",
            "faceLid_Open03_B_L_grp",
            "faceLid_Open02_B_L_grp",
            "faceLid_Open05_B_R_grp",
            "faceLid_Open03_T_R_grp",
            "Teeth_Handle_T_Ctrl_grp")
        for each in HeadGrp:
            cmds.parent(each, getHeadCtrl)
        lidPivot=(
            #"faceLid_Open05_T_R_lctrLid_Pivot_jnt",
            "faceLid_Open04_T_R_lctrLid_Pivot_jnt",
            "faceLid_Open03_T_R_lctrLid_Pivot_jnt",
            "faceLid_Open02_T_R_lctrLid_Pivot_jnt",
            "faceLid_Open01_T_R_lctrLid_Pivot_jnt",
            "faceLid_Closed05_R_lctrLid_Pivot_jnt",
            "faceLid_Closed04_R_lctrLid_Pivot_jnt",
            "faceLid_Closed03_R_lctrLid_Pivot_jnt",
            "faceLid_Closed02_R_lctrLid_Pivot_jnt",
            "faceLid_Closed01_R_lctrLid_Pivot_jnt",
            #"faceLid_Open05_T_L_lctrLid_Pivot_jnt",
            "faceLid_Open04_T_L_lctrLid_Pivot_jnt",
            "faceLid_Open03_T_L_lctrLid_Pivot_jnt",
            "faceLid_Open02_T_L_lctrLid_Pivot_jnt",
            "faceLid_Open01_T_L_lctrLid_Pivot_jnt",
            "faceLid_Closed05_L_lctrLid_Pivot_jnt",
            "faceLid_Closed04_L_lctrLid_Pivot_jnt",
            "faceLid_Closed03_L_lctrLid_Pivot_jnt",
            "faceLid_Closed02_L_lctrLid_Pivot_jnt",
            "faceLid_Closed01_L_lctrLid_Pivot_jnt")
        for each in lidPivot:
            cmds.parent(each, getHeadJnt1)
        faceControllers=(
            "faceCheekBone_R_grp",
            "faceCheek_T_R_grp",
            "faceLip_T_R_grp",
            "faceNose_grp",
            "faceCheekBone_L_grp",
            "faceCheek_T_L_grp",
            "faceLip_Corner_L_grp",
            "faceCheek_R_grp",
            "faceLip_Corner_R_grp",
            "faceLip_T_grp",
            "faceNose_R_grp",
            "faceCheek_L_grp",
            "faceLip_T_L_grp",
            "faceNose_L_grp")
        for each in faceControllers:
            cmds.parentConstraint(getHead, each, mo=1) 
        getBrows=cmds.ls("faceBrow*_grp")
        for each in getBrows:
            cmds.parent(each, getHead)
        lowerLip=("faceLip_B_L_grp", "faceLip_B_grp", "faceLip_B_R_grp")
        for each in lowerLip:
            if "faceLip_B_grp" in each:
                cmds.parentConstraint(getJaw, each, mo=1, w=1)
            else:
                cmds.parentConstraint(getHeadJnt1, each, mo=1, w=.2) 
                cmds.parentConstraint(getJaw, each, mo=1, w=.8) 
            #cmds.parent(each, "faceRig")
        cmds.parent("faceJaw_R_grp", getJaw)
        cmds.parent("faceJaw_L_grp", getJaw)
        cmds.parent("faceTongue_Master_grp", getJaw)
#         cmds.select("Chin_TRN_lctr")
#         cmds.select(getChinSDK, add=1)
#         cmds.copyAttr(v=1, ic=1 , ksc=1, cpc=1, rtc=1)
        getEyes=cmds.ls("*Pivot_jnt")
        cmds.parent("Teeth_Handle_B_Ctrl_grp",getJaw)
        
        getTongue=cmds.ls("faceTongue*_TRN")
        for each in getTongue:
            cmds.parent(each,"faceTongue_Master_Ctrl")        
        cmds.parentConstraint(getHead, "faceLip_Corner_R_grp", mo=1, w=.5)
        cmds.parentConstraint(getJaw, "faceLip_Corner_R_grp", mo=1, w=.5)
        cmds.parentConstraint(getHead, "faceLip_Corner_L_grp", mo=1, w=.5)
        cmds.parentConstraint(getJaw, "faceLip_Corner_L_grp", mo=1, w=.5)
        cmds.select( "*:BodyControllers" )
        cmds.pickWalk(d="Down")
        getBodyCtrls=[(each) for each in cmds.ls(sl=1) if "*:Eye*" not in each and "Waist" not in each and "Hand_L_Ctrl" not in each and "Hand_R_Ctrl" not in each]
        for each in getBodyCtrls:
            try:
                cmds.connectAttr("BigBox_CC.ShowBodyControls", each+".visibility")
            except:
                print "skipping "+each
                pass
        faceCtrl=cmds.ls("faceCheek*_grp")
        for each in faceCtrl:
            cmds.parent(each, getHeadCtrl)    
        faceCtrl=cmds.ls("faceLip*_grp")
        for each in faceCtrl:
            cmds.parent(each, getHeadCtrl)   
        faceCtrl=cmds.ls("faceNose*_grp")
        for each in faceCtrl:
            cmds.parent(each, getHeadCtrl)
        try:
            getBox=cmds.ls("BigBox_CC_grp") 
        except:
            getBox=cmds.ls("*:BigBox_CC_grp")  
        getTranslation, getRotation=getClass.locationXForm(getHeadCtrl)
        cmds.move(getTranslation[0]+40, getTranslation[1]+15, getTranslation[2], getBox)
        cmds.parentConstraint(getHeadCtrl,getBox, mo=1)  
        cmds.select("Chin_SDK_holder")
        cmds.select("*:Chin_SDK", add=1)
        cmds.copyAttr(values=1, inConnections=1, outConnections=1, containerParentChild=1)  
        cmds.select("EyeMask_SDK_Holder")
        cmds.select("*:EyeMask_Ctrl", add=1)
        cmds.copyAttr(values=1, inConnections=1, outConnections=1, containerParentChild=1)
#         cmds.delete("EyeMask_SDK_Holder")  
#         cmds.delete("Chin_SDK_holder")  
        print "reconnected controller box to head"
        
    def disconnect_to_head(self):
        cmds.spaceLocator(n="Chin_SDK_holder")
        cmds.addAttr("Chin_SDK_holder", ln="FullBottLip", min=0, max=1, at="double", k=1, nn="FullBottLip")
        cmds.select("*:Chin_SDK")
        cmds.select("Chin_SDK_holder", add=1)
        cmds.copyAttr(values=1, inConnections=1, outConnections=1, containerParentChild=1)               
        cmds.spaceLocator(n="EyeMask_SDK_Holder")
        cmds.addAttr("EyeMask_SDK_Holder", ln="RightLidDown", min=0, max=1, at="double", k=1, nn="RightLidDown")
        cmds.addAttr("EyeMask_SDK_Holder", ln="LeftLidDown", min=0, max=1, at="double", k=1, nn="LeftLidDown")
        cmds.addAttr("EyeMask_SDK_Holder", ln="RightLidUp", min=0, max=1, at="double", k=1, nn="RightLidUp")
        cmds.addAttr("EyeMask_SDK_Holder", ln="LeftLidUp", min=0, max=1, at="double", k=1, nn="LeftLidUp")
        cmds.addAttr("EyeMask_SDK_Holder", ln="showLashCtrls", min=0, max=1, at="double", k=1, nn="showLashCtrls")
        cmds.addAttr("EyeMask_SDK_Holder", ln="Blink_Left", min=0, max=1, at="double", k=1, nn="Blink_Left")
        cmds.addAttr("EyeMask_SDK_Holder", ln="Blink_Right", min=0, max=1, at="double", k=1, nn="Blink_Right")
        cmds.addAttr("EyeMask_SDK_Holder", ln="RightBlinkHeight", min=0, max=1, at="double", k=1, nn="RightBlinkHeight")
        cmds.addAttr("EyeMask_SDK_Holder", ln="LeftBlinkHeight", min=0, max=1, at="double", k=1, nn="LeftBlinkHeight")
        cmds.addAttr("EyeMask_SDK_Holder", ln="CheekLeftUp", min=0, max=1, at="double", k=1, nn="CheekLeftUp")
        cmds.addAttr("EyeMask_SDK_Holder", ln="CheekRightUp", min=0, max=1, at="double", k=1, nn="CheekRightUp")        
        cmds.select("*:EyeMask_Ctrl")
        cmds.select("EyeMask_SDK_Holder", add=1)
        cmds.copyAttr(values=1, inConnections=1, outConnections=1, containerParentChild=1)             
        try:
            getBox=cmds.ls("BigBox_CC_grp") 
        except:
            getBox=cmds.ls("*:BigBox_CC_grp") 
        if cmds.ls(getBox[0]+"_parentConstraint1"):
            cmds.delete(getBox[0]+"_parentConstraint1")
        faceSDKToRigGroup=(
            "faceCheekBone_R_grp",
            "faceCheek_T_R_grp",
            "faceLip_T_R_grp",
            "faceNose_grp",
            "faceCheekBone_L_grp",
            "faceCheek_T_L_grp",
            "faceLip_Corner_L_grp",
            "faceCheek_R_grp",
            "faceLip_Corner_R_grp",
            "faceLip_T_grp",
            "faceNose_R_grp",
            "faceCheek_L_grp",
            "faceLip_T_L_grp",
            "faceNose_L_grp")
        HeadGrp=(
             #"faceLid_Open05_T_R_grp",
            "faceLid_Open04_T_R_grp",
            "faceLid_Open02_T_R_grp",
            "faceLid_Open04_T_L_grp",
            "faceLid_Open03_T_L_grp",
            "faceLid_Open02_T_L_grp",
            "faceLid_Open04_B_R_grp",
            "faceLid_Open03_B_R_grp",
            "faceLid_Open02_B_R_grp",
            "faceLid_Open05_B_L_grp",
            "faceLid_Open04_B_L_grp",
            "faceLid_Open03_B_L_grp",
            "faceLid_Open02_B_L_grp",
            "faceLid_Open05_B_R_grp",
            "faceLid_Open03_T_R_grp",
            "Teeth_Handle_T_Ctrl_grp")
        for each in HeadGrp:
            cmds.parent(each, w=1)
        lidPivot=(
            #"faceLid_Open05_T_R_lctrLid_Pivot_jnt",
            "faceLid_Open04_T_R_lctrLid_Pivot_jnt",
            "faceLid_Open03_T_R_lctrLid_Pivot_jnt",
            "faceLid_Open02_T_R_lctrLid_Pivot_jnt",
            "faceLid_Open01_T_R_lctrLid_Pivot_jnt",
            "faceLid_Closed05_R_lctrLid_Pivot_jnt",
            "faceLid_Closed04_R_lctrLid_Pivot_jnt",
            "faceLid_Closed03_R_lctrLid_Pivot_jnt",
            "faceLid_Closed02_R_lctrLid_Pivot_jnt",
            "faceLid_Closed01_R_lctrLid_Pivot_jnt",
            #"faceLid_Open05_T_L_lctrLid_Pivot_jnt",
            "faceLid_Open04_T_L_lctrLid_Pivot_jnt",
            "faceLid_Open03_T_L_lctrLid_Pivot_jnt",
            "faceLid_Open02_T_L_lctrLid_Pivot_jnt",
            "faceLid_Open01_T_L_lctrLid_Pivot_jnt",
            "faceLid_Closed05_L_lctrLid_Pivot_jnt",
            "faceLid_Closed04_L_lctrLid_Pivot_jnt",
            "faceLid_Closed03_L_lctrLid_Pivot_jnt",
            "faceLid_Closed02_L_lctrLid_Pivot_jnt",
            "faceLid_Closed01_L_lctrLid_Pivot_jnt")
        for each in lidPivot:
            cmds.parent(each, w=1)
        faceControllers=(
            "faceCheekBone_R_grp",
            "faceCheek_T_R_grp",
            "faceLip_T_R_grp",
            "faceNose_grp",
            "faceCheekBone_L_grp",
            "faceCheek_T_L_grp",
            "faceLip_Corner_L_grp",
            "faceCheek_R_grp",
            "faceLip_Corner_R_grp",
            "faceLip_T_grp",
            "faceNose_R_grp",
            "faceCheek_L_grp",
            "faceLip_T_L_grp",
            "faceNose_L_grp")
        for each in faceControllers:
            cmds.delete(each+"_parentConstraint1")
        getBrows=cmds.ls("faceBrow*_grp")
        for each in getBrows:
            cmds.parent(each, w=1)
        lowerLip=("faceLip_B_L_grp", "faceLip_B_grp", "faceLip_B_R_grp")
        for each in lowerLip:
            cmds.delete(each+"_parentConstraint1")
        cmds.parent("faceTongue_Master_grp", w=1)
        cmds.parent("Teeth_Handle_B_Ctrl_grp",w=1)
        cmds.parent("faceJaw_R_grp", w=1)
        cmds.parent("faceJaw_L_grp", w=1)
        ChildAttributes=(".tx", ".ty", ".tz" , ".rx", ".ry", ".rz")
#         getEachJaw=cmds.ls("Jaw_*_SDK")
        getEachJaw=["Jaw_R_SDK", "Jaw_L_SDK"]
        for each in getEachJaw:
            for attr in ChildAttributes:
                getJaw=cmds.ls(each+attr)
                getInf=cmds.listConnections(getJaw, s=1, p=1)
                cmds.disconnectAttr(getInf[0],each+attr)
        getTongue=cmds.ls("faceTongue*_TRN")
        for each in getTongue:
            cmds.parent(each,w=1)
        cmds.setAttr("Phonemes_CC.CheekLeftUp", cb=0, k=0)
        cmds.setAttr("Phonemes_CC.CheekRightUp", cb=0, k=0)
        cmds.setAttr("BigBox_CC.ShowSDKControls", 0)
        cmds.select( "*:BodyControllers" )
        cmds.pickWalk(d="Down")
        getBodyCtrls=[(each) for each in cmds.ls(sl=1) if "*:Eye*" not in each and "Waist" not in each and "Hand_L_Ctrl" not in each and "Hand_R_Ctrl" not in each]
        faceCtrl=cmds.ls("faceCheek*_grp")
        for each in faceCtrl:
            cmds.parent(each, w=1)    
        faceCtrl=cmds.ls("faceLip*_grp")
        for each in faceCtrl:
            cmds.parent(each, w=1)   
        faceCtrl=cmds.ls("faceNose*_grp")
        for each in faceCtrl:
            cmds.parent(each, w=1)
        print "disconnected face"

    def phonemeSDKKeys(self):
        '''this sets all the sdk keys for the mouth sdk controllers'''
        try:
            getObjects=("Phonemes_CC",
            "Lip_Corner_L_SDK",
            "Lip_T_L_SDK",
            "Lip_T_SDK",
            "Lip_T_R_SDK",
            "Nose_R_SDK",
            "Nose_L_SDK",
            "Jaw_R_SDK",
            "Jaw_L_SDK",
            "Lip_Corner_R_SDK",
            "Lip_B_R_SDK",
            "Lip_B_SDK",
            "Lip_B_L_SDK",
            "*:Chin_SDK", 
            "faceTongue05_SDK",
            )
        except:
            getObjects=("*:ControllerBox:Phonemes_CC",
            "*:Lip_Corner_L_SDK",
            "*:Lip_T_L_SDK",
            "*:Lip_T_SDK",
            "*:Lip_T_R_SDK",
            "*:Nose_R_SDK",
            "*:Nose_L_SDK",
            "*:Jaw_R_SDK",
            "*:Jaw_L_SDK",
            "*:Lip_Corner_R_SDK",
            "*:Lip_B_R_SDK",
            "*:Lip_B_SDK",
            "*:Lip_B_L_SDK",
            "*:Polly_Rig:Chin_SDK", 
            "*:faceTongue05_SDK",
            )
        '''this sets sdk keys for selected'''

        #getAttrBucket=[]
        getAttr=cmds.listAttr(getObjects[0], k=1, v=1)
        #global getObjects
        global colMenu
        winName = "SDK"
        winTitle = winName
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)

        window = cmds.window(winName, title=winTitle, tbm=1, w=200, h=100 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=150)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        
        cmds.rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(110, 20))
        colMenu=cmds.optionMenu( label='Attributes')
        for each in getAttr:
            cmds.menuItem( label=each)            
        cmds.button (label='setSDKkeys', p='listBuildButtonLayout', command = lambda *args:self.phonemeSDKKeysFunct(getObjects))
        cmds.showWindow(window)   
        
    def phonemeSDKKeysFunct(self, getObjects):  
        print getObjects[1:]
        queryAttr=cmds.optionMenu(colMenu, q=1, v=1)  
        ChildAttributes=(".tx", ".ty", ".tz" , ".rx", ".ry", ".rz")
        ControllerAttributesHz="."+str(queryAttr) 
        for Child in getObjects[1:]:
            print Child
            for attribute in ChildAttributes:
                cmds.setDrivenKeyframe(Child+attribute, cd=getObjects[0]+ControllerAttributesHz)
    def TR_SDKKeys(self):
        '''this sets sdk keys for selected'''
        selObj=cmds.ls(sl=1)
        Controller=selObj[0]
        #getAttrBucket=[]
        getAttr=cmds.listAttr(Controller, k=1, v=1)
        global colMenu
        winName = "SDK"
        winTitle = winName
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)

        window = cmds.window(winName, title=winTitle, tbm=1, w=200, h=100 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=150)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        
        cmds.rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(110, 20))
        colMenu=cmds.optionMenu( label='Attributes')
        for each in getAttr:
            cmds.menuItem( label=each)            
        cmds.button (label='setSDKkeys', p='listBuildButtonLayout', command = self.TR_SDKKeys_funct)
        cmds.showWindow(window)    
        
    def TR_SDKKeys_funct(self, arg=None):
        queryAttr=cmds.optionMenu(colMenu, q=1, v=1)    
        selObj=cmds.ls(sl=1)
        Controller=selObj[0]
        ChildAttributes=(".tx", ".ty", ".tz" , ".rx", ".ry", ".rz") 
        ControllerAttributesHz="."+str(queryAttr)    
        for Child in selObj[1:]:
            for attribute in ChildAttributes:
                cmds.setDrivenKeyframe(Child+attribute, cd=Controller+ControllerAttributesHz)
                
    def Reset(self):
        '''this resets selected'''
        selObj=cmds.ls(sl=1)
        Controller=selObj[0]
        ChildAttributes=(".tx", ".ty", ".tz" , ".rx", ".ry", ".rz")        
        for Child in selObj:
            for attribute in ChildAttributes:
                try:           
                    cmds.setAttr(Child+attribute, 0.0)
                except:
                    pass
                
    def mouthSDK_Reset(self):
        try:
            getSel=cmds.ls(sl=1)[0]
            pass
        except:
            print "select something"
        getParent=getSel.split(":")
        getAsset= ':'.join(getParent[:-1])+":"          
        '''this resets mouth'''
        try:
            getObjects=(
            "Lip_Corner_L_SDK",
            "Lip_T_L_SDK",
            "Lip_T_SDK",
            "Lip_T_R_SDK",
            "Nose_R_SDK",
            "Nose_L_SDK",
            "Jaw_R_SDK",
            "Jaw_L_SDK",
            "Lip_Corner_R_SDK",
            "Lip_B_R_SDK",
            "Lip_B_SDK",
            "Lip_B_L_SDK",
            "Polly_Rig:Chin_SDK", 
            "faceTongue05_SDK",
            )
        except:
            getObjects=(
            getAsset+"Lip_Corner_L_SDK",
            getAsset+"Lip_T_L_SDK",
            getAsset+"Lip_T_SDK",
            getAsset+"Lip_T_R_SDK",
            getAsset+"Nose_R_SDK",
            getAsset+"Nose_L_SDK",
            getAsset+"Jaw_R_SDK",
            getAsset+"Jaw_L_SDK",
            getAsset+"Lip_Corner_R_SDK",
            getAsset+"Lip_B_R_SDK",
            getAsset+"Lip_B_SDK",
            getAsset+"Lip_B_L_SDK",
            getAsset+"Polly_Rig:Chin_SDK", 
            getAsset+"faceTongue05_SDK",
            )        
        selObj=cmds.ls(sl=1)
        Controller=selObj[0]
        ChildAttributes=(".tx", ".ty", ".tz" , ".rx", ".ry", ".rz")        
        for Child in getObjects:
            for attribute in ChildAttributes:            
                cmds.setAttr(Child+attribute, 0.0)
    def mouth_Reset(self):
        try:
            getSel=cmds.ls(sl=1)[0]
            pass
        except:
            print "select something"
        getParent=getSel.split(":")
        getAsset= ':'.join(getParent[:1])+":"          
        '''this resets mouth'''
        try:
            getObjects=(
            getAsset+"Lip_Corner_L_Ctrl",
            getAsset+"Lip_T_L_Ctrl",
            getAsset+"Lip_T_Ctrl",
            getAsset+"Lip_T_R_Ctrl",
            getAsset+"Nose_R_Ctrl",
            getAsset+"Nose_L_Ctrl",
            getAsset+"Jaw_R_Ctrl",
            getAsset+"Jaw_L_Ctrl",
            getAsset+"Lip_Corner_R_Ctrl",
            getAsset+"Lip_B_R_Ctrl",
            getAsset+"Lip_B_Ctrl",
            getAsset+"Lip_B_L_Ctrl",
            getAsset+"Polly_Rig:Chin_Ctrl", 
            getAsset+"faceTongue05_Ctrl",
            )
        except:
            getObjects=(
            "Lip_Corner_L_Ctrl",
            "Lip_T_L_Ctrl",
            "Lip_T_Ctrl",
            "Lip_T_R_Ctrl",
            "Nose_R_Ctrl",
            "Nose_L_Ctrl",
            "Jaw_R_Ctrl",
            "Jaw_L_Ctrl",
            "Lip_Corner_R_Ctrl",
            "Lip_B_R_Ctrl",
            "Lip_B_Ctrl",
            "Lip_B_L_Ctrl",
            "Polly_Rig:Chin_Ctrl", 
            "faceTongue05_Ctrl",
            )        
        selObj=cmds.ls(sl=1)
        Controller=selObj[0]
        ChildAttributes=(".tx", ".ty", ".tz" , ".rx", ".ry", ".rz")        
        for Child in getObjects:
            for attribute in ChildAttributes:            
                cmds.setAttr(Child+attribute, 0.0)
    def selectMouth(self):
        try:
            getSel=cmds.ls(sl=1)[0]
            pass
        except:
            print "select something"
        getParent=getSel.split(":")
        getAsset= ':'.join(getParent[:1])+":"          
        '''this sets all the sdk keys for the mouth sdk controllers'''
        try:
            getObjects=(
            getAsset+"Lip_Corner_L_SDK",
            getAsset+"Lip_T_L_SDK",
            getAsset+"Lip_T_SDK",
            getAsset+"Lip_T_R_SDK",
            getAsset+"Lip_Corner_R_SDK",
            getAsset+"Lip_B_R_SDK",
            getAsset+"Lip_B_SDK",
            getAsset+"Lip_B_L_SDK",
            )
        except:
            getObjects=(
            "Lip_Corner_L_SDK",
            "Lip_T_L_SDK",
            "Lip_T_SDK",
            "Lip_T_R_SDK",
            "Lip_Corner_R_SDK",
            "Lip_B_R_SDK",
            "Lip_B_SDK",
            "Lip_B_L_SDK",
            )
        cmds.select(getObjects[0])
        for Child in getObjects[1:]:
            cmds.select(Child, add=1)
    def mirrorLashLR(self):
        '''this sets all the sdk keys for the mouth sdk controllers'''
        getObj=[
                "Lash_B_L_3_LSH",
                "Lash_B_R_3_LSH",
                "Lash_B_L_2_LSH",
                "Lash_B_R_2_LSH",
                "Lash_B_L_1_LSH",
                "Lash_B_R_1_LSH",
                "Lash_M_L_3_LSH",
                "Lash_M_R_3_LSH",
                "Lash_M_L_2_LSH",
                "Lash_M_R_2_LSH",
                "Lash_M_L_1_LSH",
                "Lash_M_R_1_LSH",
                "Lash_T_L_3_LSH",
                "Lash_T_R_3_LSH",
                "Lash_T_L_2_LSH",
                "Lash_T_R_2_LSH",
                "Lash_T_L_1_LSH",
                "Lash_T_R_1_LSH", 
                ]
#         cmds.select(getObj[0])
#         for Child in getObj[1:]:
#             cmds.select(Child, add=1)
#         selObj=cmds.ls(sl=1)
        for eachController, eachChild in map(None, getObj[::2], getObj[1::2]):
            translate, rot=getClass.forcedlocationXForm(eachController)
            translate=cmds.xform(eachController, q=1, t=1)
            cmds.xform(eachChild, t=[-translate[0], translate[1], translate[2]])
            cmds.rotate(rot[0], -rot[1], -rot[2],eachChild)            
    def mirrorLashRL(self):
        '''this sets all the sdk keys for the mouth sdk controllers'''
        getObj=[   
                "Lash_T_R_3_LSH",
                "Lash_T_L_3_LSH",
                "Lash_T_R_2_LSH",
                "Lash_T_L_2_LSH",
                "Lash_T_R_1_LSH",
                "Lash_T_L_1_LSH",
                "Lash_M_R_3_LSH",
                "Lash_M_L_3_LSH",
                "Lash_M_R_2_LSH",
                "Lash_M_L_2_LSH",
                "Lash_M_R_1_LSH",
                "Lash_M_L_1_LSH",
                "Lash_B_R_3_LSH",
                "Lash_B_L_3_LSH",
                "Lash_B_R_2_LSH",
                "Lash_B_L_2_LSH",
                "Lash_B_R_1_LSH",
                "Lash_B_L_1_LSH",
                ]
        for eachController, eachChild in map(None, getObj[::2], getObj[1::2]):
            translate, rot=getClass.forcedlocationXForm(eachController)
            translate=cmds.xform(eachController, q=1, t=1)
            cmds.xform(eachChild, t=[-translate[0], translate[1], translate[2]])
            cmds.rotate(rot[0], -rot[1], -rot[2],eachChild) 
            
    def selectFaceJoints(self):
        getFace=[(each) for each in cmds.ls("face*_jnt") if "Pivot" not in str(each) and "Teeth" not in each and "Chin" not in each and "Tongue" not in each]
        cmds.select(getFace[0])
        for each in getFace[1:]:
            cmds.select(each, add=1)
    def selectFaceControls(self):
        '''this collects all the controllers for the face'''        
        try:
            getSel=cmds.ls(sl=1)[0]
            pass
        except:
            print "select something"
        testSceneType=cmds.ls("Nose_R_Ctrl")
        if len(testSceneType)>0:
            getObjects=(
                "Nose_R_Ctrl",
                "Nose_L_Ctrl",
                "Lip_T_Ctrl",
                "Lip_T_R_Ctrl",
                "Lip_T_L_Ctrl",
                "Lip_Corner_R_Ctrl",
                "Lip_Corner_L_Ctrl",
                "Lip_B_Ctrl",
                "Lip_B_R_Ctrl",
                "Lip_B_L_Ctrl",
                "Cheek_T_R_Ctrl",
                "Cheek_T_L_Ctrl",
                "Cheek_R_Ctrl",
                "Cheek_L_Ctrl",
                "CheekBone_R_Ctrl",
                "CheekBone_L_Ctrl",
                "Teeth_Handle_T_Ctrl",
                "Teeth_T_Ctrl",
                "Lid_Open03_T_R_Ctrl",
                "Lid_Open05_B_R_Ctrl",
                "Lid_Open02_B_L_Ctrl",
                "Lid_Open03_B_L_Ctrl",
                "Lid_Open04_B_L_Ctrl",
                "Lid_Open05_B_L_Ctrl",
                "Lid_Open02_B_R_Ctrl",
                "Lid_Open03_B_R_Ctrl",
                "Lid_Open04_B_R_Ctrl",
                "Lid_Open02_T_L_Ctrl",
                "Lid_Open03_T_L_Ctrl",
                "Lid_Open04_T_L_Ctrl",
                "Lid_Open02_T_R_Ctrl",
                "Lid_Open04_T_R_Ctrl",
                "Brow05_R_Ctrl",
                "Brow05_L_Ctrl",
                "Brow04_R_Ctrl",
                "Brow04_L_Ctrl",
                "Brow03_R_Ctrl",
                "Brow03_L_Ctrl",
                "Brow02_R_Ctrl",
                "Brow02_L_Ctrl",
                "Brow01_R_Ctrl",
                "Brow01_L_Ctrl",
                "Jaw_L_Ctrl",
                "Jaw_R_Ctrl",
                "Teeth_Handle_B_Ctrl",
                "Teeth_B_Ctrl",
                "Tongue_Master_Ctrl",
                "Tongue01_Ctrl",
                "Tongue02_Ctrl",
                "Tongue03_Ctrl",
                "Tongue04_Ctrl",
                "Tongue05_Ctrl",
                "Nose_Ctrl",
                "*:Chin_Ctrl",
                )            
        else:
            getParent=getSel.split(":")
            getAsset= ':'.join(getParent[:1])+":"                 
            getObjects=(
                getAsset+"Nose_R_Ctrl",
                getAsset+"Nose_L_Ctrl",
                getAsset+"Lip_T_Ctrl",
                getAsset+"Lip_T_R_Ctrl",
                getAsset+"Lip_T_L_Ctrl",
                getAsset+"Lip_Corner_R_Ctrl",
                getAsset+"Lip_Corner_L_Ctrl",
                getAsset+"Lip_B_Ctrl",
                getAsset+"Lip_B_R_Ctrl",
                getAsset+"Lip_B_L_Ctrl",
                getAsset+"Cheek_T_R_Ctrl",
                getAsset+"Cheek_T_L_Ctrl",
                getAsset+"Cheek_R_Ctrl",
                getAsset+"Cheek_L_Ctrl",
                getAsset+"CheekBone_R_Ctrl",
                getAsset+"CheekBone_L_Ctrl",
                getAsset+"Teeth_Handle_T_Ctrl",
                getAsset+"Teeth_T_Ctrl",
                getAsset+"Lid_Open03_T_R_Ctrl",
                getAsset+"Lid_Open05_B_R_Ctrl",
                getAsset+"Lid_Open02_B_L_Ctrl",
                getAsset+"Lid_Open03_B_L_Ctrl",
                getAsset+"Lid_Open04_B_L_Ctrl",
                getAsset+"Lid_Open05_B_L_Ctrl",
                getAsset+"Lid_Open02_B_R_Ctrl",
                getAsset+"Lid_Open03_B_R_Ctrl",
                getAsset+"Lid_Open04_B_R_Ctrl",
                getAsset+"Lid_Open02_T_L_Ctrl",
                getAsset+"Lid_Open03_T_L_Ctrl",
                getAsset+"Lid_Open04_T_L_Ctrl",
                getAsset+"Lid_Open02_T_R_Ctrl",
                getAsset+"Lid_Open04_T_R_Ctrl",
                getAsset+"Brow05_R_Ctrl",
                getAsset+"Brow05_L_Ctrl",
                getAsset+"Brow04_R_Ctrl",
                getAsset+"Brow04_L_Ctrl",
                getAsset+"Brow03_R_Ctrl",
                getAsset+"Brow03_L_Ctrl",
                getAsset+"Brow02_R_Ctrl",
                getAsset+"Brow02_L_Ctrl",
                getAsset+"Brow01_R_Ctrl",
                getAsset+"Brow01_L_Ctrl",
                getAsset+"Jaw_L_Ctrl",
                getAsset+"Jaw_R_Ctrl",
                getAsset+"Teeth_Handle_B_Ctrl",
                getAsset+"Teeth_B_Ctrl",
                getAsset+"Tongue_Master_Ctrl",
                getAsset+"Tongue01_Ctrl",
                getAsset+"Tongue02_Ctrl",
                getAsset+"Tongue03_Ctrl",
                getAsset+"Tongue04_Ctrl",
                getAsset+"Tongue05_Ctrl",
                getAsset+"Nose_Ctrl",
                getAsset+"*:Chin_Ctrl",
                )

        cmds.select(getObjects[0])
        for Child in getObjects[1:]:
            cmds.select(Child, add=1)
    def selectPhonemeBoxControls(self):
        '''this collects all the controllers for the face'''          
        try:
            getSel=cmds.ls(sl=1)[0]
            pass
        except:
            print "select something"
        testSceneType=cmds.ls("Phonemes_CC")
        if len(testSceneType)>0:
            getObjects=(
                        "BigBox_CC",
                        "Emot_R_CC",
                        "Emot_L_CC",
                        "JawCtrl_CC",
                        "Brow_R_CC",
                        "Brow_L_CC",
                        "Phonemes_CC",
                        "Eyes_select"
                        )            
        else:
            getParent=getSel.split(":")
            getAsset= ':'.join(getParent[:1])+":"                 
            getObjects=(
                        getAsset+"BigBox_CC",
                        getAsset+"Emot_R_CC",
                        getAsset+"Emot_L_CC",
                        getAsset+"JawCtrl_CC",
                        getAsset+"Brow_R_CC",
                        getAsset+"Brow_L_CC",
                        getAsset+"Phonemes_CC",
                        getAsset+"Eyes_select"
                        )
        cmds.select(getObjects[0])
        for Child in getObjects[1:]:
            cmds.select(Child, add=1)
    def selectAnimMouth(self):
        '''this sets all the sdk keys for the mouth sdk controllers'''
        try:
            getSel=cmds.ls(sl=1)[0]
            pass
        except:
            print "select something"
        testSceneType=cmds.ls("Lip_Corner_L_Ctrl")
        if len(testSceneType)>0:
            getObjects=(
            "Lip_Corner_L_Ctrl",
            "Lip_T_L_Ctrl",
            "Lip_T_Ctrl",
            "Lip_T_R_Ctrl",
            "Lip_Corner_R_Ctrl",
            "Lip_B_R_Ctrl",
            "Lip_B_Ctrl",
            "Lip_B_L_Ctrl"
            )
        else:
            getParent=getSel.split(":")
            getAsset= ':'.join(getParent[:1])+":"               
            getObjects=(
                getAsset+"Lip_Corner_L_Ctrl",
                getAsset+"Lip_T_L_Ctrl",
                getAsset+"Lip_T_Ctrl",
                getAsset+"Lip_T_R_Ctrl",
                getAsset+"Lip_Corner_R_Ctrl",
                getAsset+"Lip_B_R_Ctrl",
                getAsset+"Lip_B_Ctrl",
                getAsset+"Lip_B_L_Ctrl",
                )
        cmds.select(getObjects[0])
        for Child in getObjects[1:]:
            cmds.select(Child, add=1)
    def select_R_Brow(self):
        '''this sets all the sdk keys for the mouth sdk controllers'''
        try:
            getSel=cmds.ls(sl=1)[0]
            pass
        except:
            print "select something"
        testSceneType=cmds.ls("Brow05_R_Ctrl")
        if len(testSceneType)>0:
            getObjects=(
            "Brow05_R_Ctrl",
            "Brow04_R_Ctrl",
            "Brow03_R_Ctrl",
            "Brow02_R_Ctrl",
            "Brow01_R_Ctrl",
            )
        else:
            getParent=getSel.split(":")
            getAsset= ':'.join(getParent[:1])+":"               
            getObjects=(
                getAsset+"Brow05_R_Ctrl",
                getAsset+"Brow04_R_Ctrl",
                getAsset+"Brow03_R_Ctrl",
                getAsset+"Brow02_R_Ctrl",
                getAsset+"Brow01_R_Ctrl",
                )
        cmds.select(getObjects[0])
        for Child in getObjects[1:]:
            cmds.select(Child, add=1)
    def select_L_Brow(self):
        '''this sets all the sdk keys for the mouth sdk controllers'''
        try:
            getSel=cmds.ls(sl=1)[0]
            pass
        except:
            print "select something"
        testSceneType=cmds.ls("Brow05_L_Ctrl")
        if len(testSceneType)>0:
            getObjects=(
            "Brow05_L_Ctrl",
            "Brow04_L_Ctrl",
            "Brow03_L_Ctrl",
            "Brow02_L_Ctrl",
            "Brow01_L_Ctrl",
            )
        else:
            getParent=getSel.split(":")
            getAsset= ':'.join(getParent[:1])+":"               
            getObjects=(
                getAsset+"Brow05_L_Ctrl",
                getAsset+"Brow04_L_Ctrl",
                getAsset+"Brow03_L_Ctrl",
                getAsset+"Brow02_L_Ctrl",
                getAsset+"Brow01_L_Ctrl",
                )
        cmds.select(getObjects[0])
        for Child in getObjects[1:]:
            cmds.select(Child, add=1)
    def select_R_Eye(self):
        '''this sets all the sdk keys for the mouth sdk controllers'''
        try:
            getSel=cmds.ls(sl=1)[0]
            pass
        except:
            print "select something"
        testSceneType=cmds.ls("Lid_Open02_B_R_Ctrl")
        if len(testSceneType)>0:
            getObjects=(
            "Lid_Open02_B_R_Ctrl",
            "Lid_Open03_B_R_Ctrl",
            "Lid_Open04_B_R_Ctrl",
            "Lid_Open05_B_R_Ctrl",
            "Lid_Open04_T_R_Ctrl",
            "Lid_Open03_T_R_Ctrl",
            "Lid_Open02_T_R_Ctrl")
        else:
            getParent=getSel.split(":")
            getAsset= ':'.join(getParent[:1])+":"               
            getObjects=(
                getAsset+"Lid_Open02_B_R_Ctrl",
                getAsset+"Lid_Open03_B_R_Ctrl",
                getAsset+"Lid_Open04_B_R_Ctrl",
                getAsset+"Lid_Open05_B_R_Ctrl",
                getAsset+"Lid_Open04_T_R_Ctrl",
                getAsset+"Lid_Open03_T_R_Ctrl",
                getAsset+"Lid_Open02_T_R_Ctrl",
                )
        cmds.select(getObjects[0])
        for Child in getObjects[1:]:
            cmds.select(Child, add=1)
    def select_L_Eye(self):
        '''this sets all the sdk keys for the mouth sdk controllers'''
        try:
            getSel=cmds.ls(sl=1)[0]
            pass
        except:
            print "select something"
        testSceneType=cmds.ls("Lid_Open02_B_L_Ctrl")
        if len(testSceneType)>0:
            getObjects=(
            "Lid_Open02_B_L_Ctrl",
            "Lid_Open03_B_L_Ctrl",
            "Lid_Open04_B_L_Ctrl",
            "Lid_Open05_B_L_Ctrl",
            "Lid_Open04_T_L_Ctrl",
            "Lid_Open03_T_L_Ctrl",
            "Lid_Open02_T_L_Ctrl")
        else:
            getParent=getSel.split(":")
            getAsset= ':'.join(getParent[:1])+":"               
            getObjects=(
                getAsset+"Lid_Open02_B_L_Ctrl",
                getAsset+"Lid_Open03_B_L_Ctrl",
                getAsset+"Lid_Open04_B_L_Ctrl",
                getAsset+"Lid_Open05_B_L_Ctrl",
                getAsset+"Lid_Open04_T_L_Ctrl",
                getAsset+"Lid_Open03_T_L_Ctrl",
                getAsset+"Lid_Open02_T_L_Ctrl",
                )
        cmds.select(getObjects[0])
        for Child in getObjects[1:]:
            cmds.select(Child, add=1)
            



        
    def skinning_face(self):
        try:
            selObj=cmds.ls(sl=1, fl=1)
        except:
            print "Must select a facemesh" 
            return   
        getFaceRigGrp=cmds.ls("FaceRigParts")[0]
        cmds.setAttr("*:EyeMask_Ctrl.Blink_Left", 1)
        cmds.duplicate(selObj[0],n="Blink_L_BS_Mesh")
        cmds.setAttr("Blink_L_BS_Mesh.visibility", 0)
        cmds.setAttr("*:EyeMask_Ctrl.Blink_Left", 0)
        cmds.setAttr("*:EyeMask_Ctrl.Blink_Right", 1)
        cmds.duplicate(selObj[0],n="Blink_R_BS_Mesh")
        cmds.setAttr("Blink_R_BS_Mesh.visibility", 0)
        cmds.setAttr("*:EyeMask_Ctrl.Blink_Right", 0)  
        cmds.group(n="BlendShapes") 
        cmds.parent("BlendShapes", getFaceRigGrp) 
        cmds.parent("Blink_R_BS_Mesh","BlendShapes") 
        topTeethmesh=cmds.ls("*:*_Teeth_T")    
        botTeethmesh=cmds.ls("*:*_Teeth_B")        
        cmds.blendShape("Blink_L_BS_Mesh", "Blink_R_BS_Mesh", selObj[0],  n="Blink_Blend", foc=1)
        cmds.connectAttr("*:EyeMask_Ctrl.Blink_Left", "Blink_Blend.Blink_L_BS_Mesh", f=1)
        cmds.connectAttr("*:EyeMask_Ctrl.Blink_Right", "Blink_Blend.Blink_R_BS_Mesh", f=1)
#         getFace=cmds.ls("face*_jnt")
        getFace=[(each) for each in cmds.ls("face*_jnt") if "Pivot" not in str(each) and "Teeth" not in each and "Chin" not in each]
        for each in selObj:
            try:
                getSkinCluster=cmds.skinCluster(each, q=1, dt=1)
                for item in getSkinCluster:
                    if "GroupId" in item:
                        skinID=[eachDefObj for eachDefObj in cmds.listConnections(item, s=1) if cmds.nodeType(eachDefObj)=="skinCluster"][0]
            except:
                print "no deformer found. Check that the mesh has had a skin applied ot it"        
            cmds.dagPose(name="ZooKeeper_Pose_DG", save=1, bp=1)
        for item in getFace:
            cmds.select(item)
            #cmds.dagPose(bp=1, sl=1, a=1, n=selObj[0]+"Pose_DG")
#             jointName=each.split("_guide",)[0]+"_jnt"
            cmds.skinCluster(skinID, e=1, ai=item, lw=1, wt=0)        
        getOldEyes=(cmds.ls("*:Eye_*_TBlink_jnt"), cmds.ls("*:Eye_*_BBlink_jnt"), cmds.ls("*:TopLid_*_jnt"), cmds.ls("*:BottomLid_*_jnt"), cmds.ls("faceTongue*_Clst_jnt"))
        for each in getOldEyes:
            for item in each:
                try:
                    cmds.skinCluster(str(skinID), e=1, ri=str(item))
                except:
                    pass
        newname, skinID=getClass.getSkinWeightsforXML(selObj[0])  
        cmds.select(selObj[0])
        cmds.skinPercent(skinID, normalize=1)                
        self.reskinFaceInternal()

    def reskinFaceInternal(self):
        Eye_L_Mesh=[cmds.ls("*:*Eye_L*")]
        if cmds.ls("*:*EyeSpecA_L"):
            getSpecA_L=cmds.ls("*:*EyeSpecA_L")[0]
            Eye_L_Mesh.append(getSpecA_L)
        elif cmds.ls("*:*Eyespeca_L"):
            getSpecA_L=cmds.ls("*:*Eyespeca_L")[0]
            Eye_L_Mesh.append(getSpecA_L)
        if cmds.ls("*:*EyeSpecB_L"):
            getSpecA_L=cmds.ls("*:*EyeSpecB_L")[0]
            Eye_L_Mesh.append(getSpecA_L)
        elif cmds.ls("*:*Eyespecb_L"):
            getSpecA_L=cmds.ls("*:*Eyespecb_L")[0]
            Eye_L_Mesh.append(getSpecA_L)
        Eye_R_Mesh=[cmds.ls("*:*Eye_R*")]
        if cmds.ls("*:*EyeSpecA_R"):
            getSpecA_R=cmds.ls("*:*EyeSpecA_R")[0]
            Eye_R_Mesh.append(getSpecA_R)
        elif cmds.ls("*:*Eyespeca_R"):
            getSpecA_R=cmds.ls("*:*Eyespeca_R")[0]
            Eye_R_Mesh.append(getSpecA_R)
        if cmds.ls("*:*EyeSpecB_R"):
            getSpecA_R=cmds.ls("*:*EyeSpecB_R")[0]
            Eye_R_Mesh.append(getSpecA_R)
        elif cmds.ls("*:*Eyespecb_R"):
            getSpecA_R=cmds.ls("*:*Eyespecb_R")[0]
            Eye_R_Mesh.append(getSpecA_R)
        Eye_L_joint=(cmds.ls("*:*Eye_L_jnt")[0])
        Eye_R_joint=(cmds.ls("*:*Eye_R_jnt")[0])
        for each in Eye_L_Mesh:
            try:
                cmds.select(Eye_L_joint, r=1)
                cmds.select(each, add=1)
                cmds.skinCluster(each,Eye_L_joint,tsb=1,sm=0 )
                keep=Eye_L_joint
                getClass.jointInfluenceHammer_callup(keep, each)
            except:
                pass
            try:
                cmds.skinCluster(each, e=1, ai=Eye_L_joint) 
                keep=Eye_L_joint
                getClass.jointInfluenceHammer_callup(keep, each)
                print "skinned left eye"
            except:
                pass
        for each in Eye_R_Mesh:
            try:
                cmds.select(Eye_L_joint, r=1)
                cmds.select(each, add=1)                
                cmds.skinCluster(each,Eye_R_joint,tsb=True, sm=0)
                keep=Eye_R_joint
                getClass.jointInfluenceHammer_callup(keep, each)                
            except:
                pass                
            try:
                cmds.skinCluster(each, e=1, ai=Eye_R_joint)
                keep=Eye_R_joint
                getClass.jointInfluenceHammer_callup(keep, each)                 
                print "skinned right eye"  
            except:
                pass                
        tongueJoints=cmds.ls("faceTongue*_Clst_jnt")
        #skinClustertongue=cmds.ls("*:*_TongueShapeDeformed")
        tonguemesh=cmds.ls("*:*Tongue")[0]
        try:
            cmds.skinCluster(tonguemesh, e=1, ub=1)
            print "unskinned tongue"
        except:
            pass
        cmds.skinCluster(tonguemesh,"faceTongue01_Clst_jnt")
        print "reskinned tongue"
        for each in tongueJoints[1:]:
            try:
                cmds.skinCluster(tonguemesh, e=1, ai=each)
                print "added joints to tongue"    
            except:
                pass        
        Sides=["L", "R"]
        for eachSide in Sides:
            BrowJoints=cmds.ls("faceBrow*_"+eachSide+"_Clst_"+eachSide+"_jnt")
            #skinClustertongue=cmds.ls("*:*_TongueShapeDeformed")
            if cmds.ls("*:*"+eachSide+"_Brow"):
                BrowMesh=cmds.ls("*:*"+eachSide+"_Brow")[0]
            elif cmds.ls("*:*Brow*"+eachSide):
                BrowMesh=cmds.ls("*:*Brow*"+eachSide)[0]
            try:
                cmds.skinCluster(BrowMesh, e=1, ub=1)
                print "unskinned "+eachSide+" brow"
            except:
                pass
            try:
                cmds.skinCluster(BrowMesh,"faceBrow01_"+eachSide+"_Clst_"+eachSide+"_jnt")
                print "reskinned "+eachSide+" brow"
                for each in BrowJoints[1:]:
                    try:
                        cmds.skinCluster(BrowMesh, e=1, ai=each)    
                        print "added joints to "+eachSide+" brow"
                    except:
                        pass
            except:
                pass
        if cmds.ls("*:*Teeth_T"):
            skinTeethtop=cmds.ls("*:*Teeth_T")[0] 
            try:
                cmds.skinCluster(skinTeethtop, e=1, ub=1)
                print "unskinned top teeth"
            except:
                pass
            try:
                cmds.skinCluster(topTeethmesh, "faceTeeth_T_jnt")
                print "skinned top teeth"
            except:
                cmds.skinCluster(skinTeethtop, "faceTeeth_T_jnt")  
                print "skinned top teeth"                                     
        if cmds.ls("*:*Teeth_B"):
            skinTeethbot=cmds.ls("*:*Teeth_B")[0]    
            try:
                cmds.skinCluster(skinTeethbot, e=1, ub=1)
                print "unskinned bottom teeth"
            except:
                pass
            try:
                cmds.skinCluster(botTeethmesh, "faceTeeth_B_jnt") 
                print "skinned bot teeth"             
            except:
                cmds.skinCluster(skinTeethbot, "faceTeeth_B_jnt")     
                print "skinned bot teeth"                                   
#         skinTeethtop=cmds.ls("*:*Teeth_T")[0]
#         print skinTeethtop
#         skinTeethbot=cmds.ls("*:*Teeth_B")[0]
#         print skinTeethbot
           
#         cmds.sets("FaceJoints", e=1, fe="faceTeeth_T_jnt")
        print "reskinned internal face"   
        
        
    def reskinFaceInternalV1(self):
        Eye_L_Mesh=[cmds.ls("*:*Eye_L*")]
        try:
            Eye_L_Mesh.append(cmds.ls("*:*EyeSpecA_L")[0])
            Eye_L_Mesh.append(cmds.ls("*:*EyeSpecB_L")[0])
        except:
            Eye_L_Mesh.append(cmds.ls("*:*Eyespeca_L")[0])
            Eye_L_Mesh.append(cmds.ls("*:*Eyespecb_L")[0])
        Eye_L_joint=(cmds.ls("*:*Eye_L_jnt")[0])        
        Eye_R_Mesh=[cmds.ls("*:*Eye_R*")]
        try:
            Eye_R_Mesh.append(cmds.ls("*:*EyeSpecA_R")[0])
            Eye_R_Mesh.append(cmds.ls("*:*EyeSpecB_R")[0])
        except:
            Eye_R_Mesh.append(cmds.ls("*:*Eyespeca_R")[0])
            Eye_R_Mesh.append(cmds.ls("*:*Eyespecb_R")[0])
        Eye_R_joint=(cmds.ls("*:*Eye_R_jnt")[0])
        for each in Eye_L_Mesh:
            try:
                cmds.skinCluster(each,Eye_L_joint)
            except:
                pass
            try:
                cmds.skinCluster(each, e=1, ai=Eye_L_joint)  
                print "skinned left eye"
            except:
                pass
        for each in Eye_R_Mesh:
            try:
                cmds.skinCluster(each,Eye_R_joint)
            except:
                pass                
            try:
                cmds.skinCluster(each, e=1, ai=Eye_R_joint)
                print "skinned right eye"  
            except:
                pass                
        tongueJoints=cmds.ls("faceTongue*_Clst_jnt")
        #skinClustertongue=cmds.ls("*:*_TongueShapeDeformed")
        tonguemesh=cmds.ls("*:*Tongue")[0]
        try:
            cmds.skinCluster(tonguemesh, e=1, ub=1)
            print "unskinned tongue"
        except:
            pass
        cmds.skinCluster(tonguemesh,"faceTongue01_Clst_jnt")
        print "reskinned tongue"
        for each in tongueJoints[1:]:
            try:
                cmds.skinCluster(tonguemesh, e=1, ai=each)
                print "added joints to tongue"    
            except:
                pass        
        Sides=["L", "R"]
        for eachSide in Sides:
            BrowJoints=cmds.ls("faceBrow*_"+eachSide+"_Clst_"+eachSide+"_jnt")
            #skinClustertongue=cmds.ls("*:*_TongueShapeDeformed")
            try:
                BrowMesh=cmds.ls("*:*"+eachSide+"_Brow")[0]
            except:
                BrowMesh=cmds.ls("*:*Brow*"+eachSide)[0]
            try:
                cmds.skinCluster(BrowMesh, e=1, ub=1)
                print "unskinned "+eachSide+" brow"
            except:
                pass
            cmds.skinCluster(BrowMesh,"faceBrow01_"+eachSide+"_Clst_"+eachSide+"_jnt")
            print "reskinned "+eachSide+" brow"
            for each in BrowJoints[1:]:
                try:
                    cmds.skinCluster(BrowMesh, e=1, ai=each)    
                    print "added joints to "+eachSide+" brow"
                except:
                    pass               
        skinTeethtop=cmds.ls("*:*Teeth_T")[0]
        print skinTeethtop
        skinTeethbot=cmds.ls("*:*Teeth_B")[0]
        print skinTeethbot
        try:
            cmds.skinCluster(skinTeethtop, e=1, ub=1)
            print "unskinned top teeth"
        except:
            pass
        try:
            cmds.skinCluster(topTeethmesh, "faceTeeth_T_jnt")
            print "skinned top teeth"
        except:
            cmds.skinCluster(skinTeethtop, "faceTeeth_T_jnt")  
            print "skinned top teeth"               
#         cmds.sets("FaceJoints", e=1, fe="faceTeeth_T_jnt")
        try:
            cmds.skinCluster(skinTeethbot, e=1, ub=1)
            print "unskinned bottom teeth"
        except:
            pass
        try:
            cmds.skinCluster(botTeethmesh, "faceTeeth_B_jnt") 
            print "skinned bot teeth"             
        except:
            cmds.skinCluster(skinTeethbot, "faceTeeth_B_jnt")     
            print "skinned bot teeth"                        
        print "reskinned internal face"   
        
    def blendShapeHighBlink(self):
        selObj=cmds.ls(sl=1, fl=1)
        if selObj:
            pass
        else:
            print "Must select a facemesh" 
            return           
        try:
            cmds.blendShape("BlinkHigh_L_BS_Mesh", "BlinkHigh_R_BS_Mesh", selObj[0],  n="Blink_High_Blend", foc=1)
        except:
            print "you need two targets : BlinkHigh_L_BS_Mesh and BlinkHigh_R_BS_Mesh"
            return
        try:
            cmds.addAttr(getEyeMask[0], ln="RightBlinkHeight",  min=0, max=1, at="double", k=1, nn="RightBlinkHeight")
        except:
            print "already added right blink high attr"
            pass
        try:
            cmds.addAttr(getEyeMask[0], ln="LeftBlinkHeight",  min=0, max=1, at="double", k=1, nn="LeftBlinkHeight")
        except:
            print "already added left blink high attr"
            pass
        try:
            cmds.connectAttr("*:EyeMask_Ctrl.RightBlinkHeight","Blink_High.BlinkHigh_R_BS_Mesh", f=1)
        except:
            print "can't find BlinkHigh_R_BS_Mesh connection"
            return
        try:
            cmds.connectAttr("*:EyeMask_Ctrl.LeftBlinkHeight","Blink_High.BlinkHigh_L_BS_Mesh", f=1)
        except:
            print "can't find BlinkHigh_L_BS_Mesh connection"
            return
        print "created high blink"
            
    def select_trn(self):
        getAllTRN=cmds.ls("*TRN_Ctrl")
        cmds.select(getAllTRN[0])
        for each in getAllTRN:
            cmds.select(each, add=1)
        
    def clean_face(self):
        getTongue=[(each) for each in cmds.ls("faceTongue*_grp") if "faceTongue05_SDK_grp" not in each]
        for each in getTongue:
            try:
                cmds.parent(each, "faceTongue_Master_Ctrl")
            except:
                pass
        cmds.parent("faceTongue05_SDK_grp", "faceTongue_Master_Ctrl")
        
        getTRN=[(each) for each in cmds.ls("*TRN") for item in cmds.listRelatives(each, c=1) if cmds.nodeType(item) != "nurbsCurve" if "Tongue" not in each]
        print getTRN
        for each in getTRN:
            getItem=cmds.listRelatives(each, c=1, typ="transform")
            cmds.parent(getItem[0], "FaceRig")
        getTRN=cmds.ls("*TRN")
        deleteList = []
        for tran in getTRN:
            children = [(each) for each in cmds.listRelatives(tran, ad=1) if cmds.nodeType(each) != "nurbsCurve"]
            if len(children) ==0:
                deleteList.append(tran)  
        cmds.delete(deleteList)
        allControllers=[(each) for each in cmds.ls("*_Ctrl") if "Teeth" not in each]
#         cmds.sets(allControllers, n="BodyControllers") 
        for each in allControllers:          
            cmds.setAttr(str(each)+".sx" , keyable=0, lock=1)
            cmds.setAttr(str(each)+".sy" , keyable=0, lock=1)
            cmds.setAttr(str(each)+".sz", keyable=0, lock=1)  
            try:
                newname=each.split("face")[1]
                cmds.rename(each, newname)
            except:
                pass
        for each in getJawNod:
            try:
                getShapes=[(each) for each in cmds.listRelatives(each, typ="shape") if "lctr" not in each]
                for shape in getShapes:
                        cmds.setAttr(shape+".visibility", 0)                
            except:
                pass

        print "Preformed cleanface "


 
    def reconnect_blinks(self):
        selObj=cmds.ls(sl=1, fl=1)
        cmds.connectAttr("*:EyeMask_Ctrl.Blink_Left", "Blink_Blend.Blink_L_BS_Mesh", f=1)
        cmds.connectAttr("*:EyeMask_Ctrl.Blink_Right", "Blink_Blend.Blink_R_BS_Mesh", f=1)
        try:
            cmds.connectAttr("*:EyeMask_Ctrl.RightBlinkHeight", "Blink_High_Blend.BlinkHigh_R_BS_Mesh", f=1)
            cmds.connectAttr("*:EyeMask_Ctrl.LeftBlinkHeight", "Blink_High_Blend.BlinkHigh_L_BS_Mesh", f=1)
        except:
            pass
        cmds.connectAttr("*:EyeMask_Ctrl.CheekLeftUp","Phonemes_CC.CheekLeftUp", f=1)
        cmds.connectAttr("*:EyeMask_Ctrl.CheekRightUp","Phonemes_CC.CheekRightUp", f=1)         
        
    def recreate_blinks(self):
        selObj=cmds.ls(sl=1, fl=1)
        try:
            cmds.delete("Blink_Blend")
            print "deleted current blink blend"
        except:
            pass
        try:
            cmds.blendShape("Blink_L_BS_Mesh", "Blink_R_BS_Mesh", selObj[0],  n="Blink_Blend", foc=1)
        except:
            print "you need 'Blink_L_BS_Mesh' and 'Blink_R_BS_Mesh' to continue"
            return
        cmds.connectAttr("*:EyeMask_Ctrl.Blink_Left", "Blink_Blend.Blink_L_BS_Mesh", f=1)
        cmds.connectAttr("*:EyeMask_Ctrl.Blink_Right", "Blink_Blend.Blink_R_BS_Mesh", f=1)
        if "BlinkHigh_R_BS_Mesh" and "BlinkHigh_L_BS_Mesh":
            try:
                cmds.delete("Blink_High_Blend")
                print "deleted current blink high blend"
            except:
                pass
            try:
                cmds.blendShape("BlinkHigh_L_BS_Mesh", "BlinkHigh_R_BS_Mesh", selObj[0],  n="Blink_High_Blend", foc=1)
            except:
                print "you need 'BlinkHigh_L_BS_Mesh' and 'BlinkHigh_R_BS_Mesh' to continue"
                return
            try:
                cmds.addAttr(getEyeMask[0], ln="RightBlinkHeight",  min=0, max=1, at="double", k=1, nn="RightBlinkHeight")
                cmds.addAttr(getEyeMask[0], ln="LeftBlinkHeight",  min=0, max=1, at="double", k=1, nn="LeftBlinkHeight")
                cmds.connectAttr("*:EyeMask_Ctrl.RightBlinkHeight", "Blink_High_Blend.BlinkHigh_R_BS_Mesh", f=1)
                cmds.connectAttr("*:EyeMask_Ctrl.LeftBlinkHeight", "Blink_High_Blend.BlinkHigh_L_BS_Mesh", f=1)                
            except:
                cmds.connectAttr("*:EyeMask_Ctrl.RightBlinkHeight", "Blink_High_Blend.BlinkHigh_R_BS_Mesh", f=1)
                cmds.connectAttr("*:EyeMask_Ctrl.LeftBlinkHeight", "Blink_High_Blend.BlinkHigh_L_BS_Mesh", f=1)
        else:
            pass
        try:
            cmds.connectAttr("*:EyeMask_Ctrl.CheekLeftUp","Phonemes_CC.CheekLeftUp", f=1)
        except:
            pass
        try:            
            cmds.connectAttr("*:EyeMask_Ctrl.CheekRightUp","Phonemes_CC.CheekRightUp", f=1) 
        except:
            pass
        self.Smooth_BS(selObj)        
        self.Blink_SDK()        
        
    def Smooth_BS(self, selObj):
        if cmds.ls("Smooth_BS_Mesh"):
            try:
                cmds.delete("Smooth")
                print "deleted current smooth blend"
            except:
                print "no smooth blend to delete"
                pass
            cmds.blendShape("Smooth_BS_Mesh",  selObj[0],  n="Smooth", foc=1, w=.5)
            cmds.polyAverageVertex("Smooth_BS_Mesh", i=10, ch=1)
        else:
            print "no 'Smooth_BS_Mesh'. skipping smooth blend."
            return        

        
    def connectBlendMouth(self):
        selObj=cmds.ls(sl=1, fl=1)
        getShapeBucket=[]
        if cmds.ls("Smile_R_BS_Mesh"):
            getSmile_R=cmds.ls("Smile_R_BS_Mesh")[0]
            getShapeBucket.append(getSmile_R)
        if cmds.ls("Smile_L_BS_Mesh"):
            getSmile_L=cmds.ls("Smile_L_BS_Mesh")[0]
            getShapeBucket.append(getSmile_L)
        if cmds.ls("Frown_R_BS_Mesh"):
            getFrown_R=cmds.ls("Frown_R_BS_Mesh")[0]
            getShapeBucket.append(getFrown_R)
        if cmds.ls("Frown_L_BS_Mesh"):
            getFrown_L=cmds.ls("Frown_L_BS_Mesh")[0]
            getShapeBucket.append(getFrown_L)
        if cmds.ls("Wide_R_BS_Mesh"):
            getWide_R=cmds.ls("Wide_R_BS_Mesh")[0]
            getShapeBucket.append(getWide_R)
        if cmds.ls("Wide_L_BS_Mesh"):
            getWide_L=cmds.ls("Wide_L_BS_Mesh")[0]
            getShapeBucket.append(getWide_L)
        if cmds.ls("Narrow_R_BS_Mesh"):
            getNarrow_R=cmds.ls("Narrow_R_BS_Mesh")[0]
            getShapeBucket.append(getNarrow_R)
        if cmds.ls("Narrow_L_BS_Mesh"):
            getNarrow_L=cmds.ls("Narrow_L_BS_Mesh")[0]
            getShapeBucket.append(getNarrow_L)        
        if cmds.ls("Up_BS_Mesh"):
            getUp=cmds.ls("Up_BS_Mesh")[0]
            getShapeBucket.append(getUp)
        if cmds.ls("Down_BS_Mesh"):
            getDown=cmds.ls("Down_BS_Mesh")[0]
            getShapeBucket.append(getDown)        
        if cmds.ls("CheekUp_R_BS_Mesh"):
            getCheekUp_R=cmds.ls("CheekUp_R_BS_Mesh")[0]
            getShapeBucket.append(getCheekUp_R)
        if cmds.ls("CheekUp_L_BS_Mesh"):
            getCheekUp_L=cmds.ls("CheekUp_L_BS_Mesh")[0]
            getShapeBucket.append(getCheekUp_L)        
        try:
            cmds.delete("Mouth")
            print "deleted current Mouth blend"
        except:
            pass
        try:
            cmds.blendShape(getShapeBucket,selObj[0], n="Mouth", foc=1)
        except:
            pass

        
        if cmds.ls("Smile_R_BS_Mesh"):
            Controller="Emot_R_CC.translateY"
            Child="Mouth.Smile_R_BS_Mesh"
            defaultSet=0
            ChildActivatedValue=1
            ChildDeactivatedValue=0
            ControllerOnValue=2
            ControllerOffValue=0
            getClass.controlSecondValueChildOn(Controller, Child, defaultSet, ChildActivatedValue, ChildDeactivatedValue, ControllerOnValue, ControllerOffValue)
#         if cmds.ls("Smile_R_BS_Mesh"):
#             cmds.setAttr("Mouth.Smile_R_BS_Mesh", lock=0)
#             cmds.setAttr("Emot_R_CC.translateY",2 )
#             cmds.setAttr("Mouth.Smile_R_BS_Mesh",1)          
#             cmds.setDrivenKeyframe("Mouth.Smile_R_BS_Mesh", cd="Emot_R_CC.translateY")
#             cmds.setAttr("Emot_R_CC.translateY",0)
#             cmds.setAttr("Mouth.Smile_R_BS_Mesh", 0)          
#             cmds.setDrivenKeyframe("Mouth.Smile_R_BS_Mesh", cd="Emot_R_CC.translateY")
#             cmds.setAttr("Emot_R_CC.translateY",0 )
#             cmds.setAttr("Mouth.Smile_R_BS_Mesh", lock=1)
        if cmds.ls("Smile_L_BS_Mesh"):
            Controller="Emot_L_CC.translateY"
            Child="Mouth.Smile_L_BS_Mesh"
            defaultSet=0
            ChildActivatedValue=1
            ChildDeactivatedValue=0
            ControllerOnValue=2
            ControllerOffValue=0
            getClass.controlSecondValueChildOn(Controller, Child, defaultSet, ChildActivatedValue, ChildDeactivatedValue, ControllerOnValue, ControllerOffValue)
#             cmds.setAttr("Mouth.Smile_L_BS_Mesh", lock=0)   
#             cmds.setAttr("Emot_L_CC.translateY",2 )
#             cmds.setAttr("Mouth.Smile_L_BS_Mesh",1)          
#             cmds.setDrivenKeyframe("Mouth.Smile_L_BS_Mesh", cd="Emot_L_CC.translateY")
#             cmds.setAttr("Emot_L_CC.translateY",0)
#             cmds.setAttr("Mouth.Smile_L_BS_Mesh", 0)          
#             cmds.setDrivenKeyframe("Mouth.Smile_L_BS_Mesh", cd="Emot_L_CC.translateY")
#             cmds.setAttr("Emot_L_CC.translateY",0 )
#             cmds.setAttr("Mouth.Smile_L_BS_Mesh", lock=1)
        if cmds.ls("Frown_R_BS_Mesh"):
            Controller="Emot_R_CC.translateY"
            Child="Mouth.Frown_R_BS_Mesh"
            defaultSet=0
            ChildActivatedValue=1
            ChildDeactivatedValue=0
            ControllerOnValue=-2
            ControllerOffValue=0
            getClass.controlSecondValueChildOn(Controller, Child, defaultSet, ChildActivatedValue, ChildDeactivatedValue, ControllerOnValue, ControllerOffValue)
#             cmds.setAttr("Mouth.Frown_R_BS_Mesh", lock=0)
#             cmds.setAttr("Emot_R_CC.translateY",-2 )
#             cmds.setAttr("Mouth.Frown_R_BS_Mesh",1)          
#             cmds.setDrivenKeyframe("Mouth.Frown_R_BS_Mesh", cd="Emot_R_CC.translateY")
#             cmds.setAttr("Emot_R_CC.translateY",0)
#             cmds.setAttr("Mouth.Frown_R_BS_Mesh", 0)          
#             cmds.setDrivenKeyframe("Mouth.Frown_R_BS_Mesh", cd="Emot_R_CC.translateY")
#             cmds.setAttr("Emot_R_CC.translateY",0 )
#             cmds.setAttr("Mouth.Frown_R_BS_Mesh", lock=1)
        if cmds.ls("Frown_L_BS_Mesh"):    
            Controller="Emot_L_CC.translateY"
            Child="Mouth.Frown_L_BS_Mesh"
            defaultSet=0
            ChildActivatedValue=1
            ChildDeactivatedValue=0
            ControllerOnValue=-2
            ControllerOffValue=0
            getClass.controlSecondValueChildOn(Controller, Child, defaultSet, ChildActivatedValue, ChildDeactivatedValue, ControllerOnValue, ControllerOffValue)
            
#             cmds.setAttr("Mouth.Frown_L_BS_Mesh", lock=0)
#             cmds.setAttr("Emot_L_CC.translateY",-2 )
#             cmds.setAttr("Mouth.Frown_L_BS_Mesh",1)          
#             cmds.setDrivenKeyframe("Mouth.Frown_L_BS_Mesh", cd="Emot_L_CC.translateY")
#             cmds.setAttr("Emot_L_CC.translateY",0)
#             cmds.setAttr("Mouth.Frown_L_BS_Mesh", 0)          
#             cmds.setDrivenKeyframe("Mouth.Frown_L_BS_Mesh", cd="Emot_L_CC.translateY")
#             cmds.setAttr("Emot_L_CC.translateY",0 )
#             cmds.setAttr("Mouth.Frown_L_BS_Mesh", lock=1)
        if cmds.ls("Up_BS_Mesh"):
            Controller="Phonemes_CC.MouthRaise"
            Child="Mouth.Up_BS_Mesh"
            defaultSet=0
            ChildActivatedValue=1
            ChildDeactivatedValue=0
            ControllerOnValue=1
            ControllerOffValue=0
            getClass.controlSecondValueChildOn(Controller, Child, defaultSet, ChildActivatedValue, ChildDeactivatedValue, ControllerOnValue, ControllerOffValue)
#             cmds.setAttr("Mouth.Up_BS_Mesh", lock=0) 
#             cmds.setAttr("Phonemes_CC.MouthRaise",1 )
#             cmds.setAttr("Mouth.Up_BS_Mesh", 1)          
#             cmds.setDrivenKeyframe("Mouth.Up_BS_Mesh", cd="Phonemes_CC.MouthRaise")
#             cmds.setAttr("Phonemes_CC.MouthRaise",0)
#             cmds.setAttr("Mouth.Up_BS_Mesh", 0)          
#             cmds.setDrivenKeyframe("Mouth.Up_BS_Mesh", cd="Phonemes_CC.MouthRaise")  
#             cmds.setAttr("Mouth.Up_BS_Mesh", lock=1) 
        if cmds.ls("Down_BS_Mesh"):
            Controller="Phonemes_CC.MouthRaise"
            Child="Mouth.Down_BS_Mesh"
            defaultSet=0
            ChildActivatedValue=1
            ChildDeactivatedValue=0
            ControllerOnValue=-1
            ControllerOffValue=0
            getClass.controlSecondValueChildOn(Controller, Child, defaultSet, ChildActivatedValue, ChildDeactivatedValue, ControllerOnValue, ControllerOffValue)
            
#             cmds.setAttr("Mouth.Down_BS_Mesh", lock=0) 
#             cmds.setAttr("Phonemes_CC.MouthRaise",-1 )
#             cmds.setAttr("Mouth.Down_BS_Mesh", 1)          
#             cmds.setDrivenKeyframe("Mouth.Down_BS_Mesh", cd="Phonemes_CC.MouthRaise")
#             cmds.setAttr("Phonemes_CC.MouthRaise",0)
#             cmds.setAttr("Mouth.Down_BS_Mesh", 0)          
#             cmds.setDrivenKeyframe("Mouth.Down_BS_Mesh", cd="Phonemes_CC.MouthRaise")   
#             cmds.setAttr("Phonemes_CC.MouthRaise",0 )
#             cmds.setAttr("Mouth.Down_BS_Mesh", lock=1) 
        if cmds.ls("Wide_L_BS_Mesh"):
            Controller="Phonemes_CC.MouthWidth"
            Child="Mouth.Wide_L_BS_Mesh"
            defaultSet=0
            ChildActivatedValue=1
            ChildDeactivatedValue=0
            ControllerOnValue=1
            ControllerOffValue=0
            getClass.controlSecondValueChildOn(Controller, Child, defaultSet, ChildActivatedValue, ChildDeactivatedValue, ControllerOnValue, ControllerOffValue)
        if cmds.ls("Wide_R_BS_Mesh"):
            Controller="Phonemes_CC.MouthWidth"
            Child="Mouth.Wide_R_BS_Mesh"
            defaultSet=0
            ChildActivatedValue=1
            ChildDeactivatedValue=0
            ControllerOnValue=1
            ControllerOffValue=0
            getClass.controlSecondValueChildOn(Controller, Child, defaultSet, ChildActivatedValue, ChildDeactivatedValue, ControllerOnValue, ControllerOffValue)
                    
#             cmds.setAttr("Mouth.Wide_L_BS_Mesh", lock=0) 
#             cmds.setAttr("Mouth.Wide_R_BS_Mesh", lock=0) 
#             cmds.setAttr("Phonemes_CC.MouthWidth",1 )
#             cmds.setAttr("Mouth.Wide_L_BS_Mesh", 1)          
#             cmds.setAttr("Mouth.Wide_R_BS_Mesh", 1)         
#             cmds.setDrivenKeyframe("Mouth.Wide_L_BS_Mesh", cd="Phonemes_CC.MouthWidth")         
#             cmds.setDrivenKeyframe("Mouth.Wide_R_BS_Mesh", cd="Phonemes_CC.MouthWidth")
#             cmds.setAttr("Phonemes_CC.MouthWidth",0)
#             cmds.setAttr("Mouth.Wide_L_BS_Mesh", 0)          
#             cmds.setAttr("Mouth.Wide_R_BS_Mesh", 0)         
#             cmds.setDrivenKeyframe("Mouth.Wide_L_BS_Mesh", cd="Phonemes_CC.MouthWidth")         
#             cmds.setDrivenKeyframe("Mouth.Wide_R_BS_Mesh", cd="Phonemes_CC.MouthWidth")
#             cmds.setAttr("Mouth.Wide_L_BS_Mesh", lock=1) 
#             cmds.setAttr("Mouth.Wide_R_BS_Mesh", lock=1) 
        if cmds.ls("Narrow_L_BS_Mesh"):
            Controller="Phonemes_CC.MouthWidth"
            Child="Mouth.Narrow_L_BS_Mesh"
            defaultSet=0
            ChildActivatedValue=1
            ChildDeactivatedValue=0
            ControllerOnValue=-1
            ControllerOffValue=0
            getClass.controlSecondValueChildOn(Controller, Child, defaultSet, ChildActivatedValue, ChildDeactivatedValue, ControllerOnValue, ControllerOffValue)
        if cmds.ls("Narrow_R_BS_Mesh"):
            Controller="Phonemes_CC.MouthWidth"
            Child="Mouth.Narrow_R_BS_Mesh"
            defaultSet=0
            ChildActivatedValue=1
            ChildDeactivatedValue=0
            ControllerOnValue=-1
            ControllerOffValue=0
            getClass.controlSecondValueChildOn(Controller, Child, defaultSet, ChildActivatedValue, ChildDeactivatedValue, ControllerOnValue, ControllerOffValue)
#             cmds.setAttr("Mouth.Narrow_L_BS_Mesh", lock=0) 
#             cmds.setAttr("Mouth.Narrow_R_BS_Mesh", lock=0)
#             cmds.setAttr("Phonemes_CC.MouthWidth",-1 )
#             cmds.setAttr("Mouth.Narrow_L_BS_Mesh", 1)          
#             cmds.setAttr("Mouth.Narrow_R_BS_Mesh", 1)         
#             cmds.setDrivenKeyframe("Mouth.Narrow_L_BS_Mesh", cd="Phonemes_CC.MouthWidth")         
#             cmds.setDrivenKeyframe("Mouth.Narrow_R_BS_Mesh", cd="Phonemes_CC.MouthWidth")
#             cmds.setAttr("Phonemes_CC.MouthWidth",0)
#             cmds.setAttr("Mouth.Narrow_L_BS_Mesh", 0)          
#             cmds.setAttr("Mouth.Narrow_R_BS_Mesh", 0)         
#             cmds.setDrivenKeyframe("Mouth.Narrow_L_BS_Mesh", cd="Phonemes_CC.MouthWidth")         
#             cmds.setDrivenKeyframe("Mouth.Narrow_R_BS_Mesh", cd="Phonemes_CC.MouthWidth")
#             cmds.setAttr("Mouth.Narrow_L_BS_Mesh", lock=1) 
#             cmds.setAttr("Mouth.Narrow_R_BS_Mesh", lock=1)             
        if cmds.ls("Wide_L_BS_Mesh"):
            Controller="Emot_L_CC.translateX"
            Child="Mouth.Wide_L_BS_Mesh"
            defaultSet=0
            ChildActivatedValue=1
            ChildDeactivatedValue=0
            ControllerOnValue=2
            ControllerOffValue=0
            getClass.controlSecondValueChildOn(Controller, Child, defaultSet, ChildActivatedValue, ChildDeactivatedValue, ControllerOnValue, ControllerOffValue)

#             cmds.setAttr("Mouth.Wide_L_BS_Mesh", lock=0)  
#             cmds.setAttr("Emot_L_CC.translateX",2 )
#             cmds.setAttr("Mouth.Wide_L_BS_Mesh",1)          
#             cmds.setDrivenKeyframe("Mouth.Wide_L_BS_Mesh", cd="Emot_L_CC.translateX")
#             cmds.setAttr("Emot_L_CC.translateX",0 )
#             cmds.setAttr("Mouth.Wide_L_BS_Mesh",0)          
#             cmds.setDrivenKeyframe("Mouth.Wide_L_BS_Mesh", cd="Emot_L_CC.translateX")
#             cmds.setAttr("Emot_L_CC.translateX",0 )
#             cmds.setAttr("Mouth.Wide_L_BS_Mesh", lock=1)                
        if cmds.ls("Wide_R_BS_Mesh"):
            Controller="Emot_R_CC.translateX"
            Child="Mouth.Wide_R_BS_Mesh"
            defaultSet=0
            ChildActivatedValue=1
            ChildDeactivatedValue=0
            ControllerOnValue=2
            ControllerOffValue=0
            getClass.controlSecondValueChildOn(Controller, Child, defaultSet, ChildActivatedValue, ChildDeactivatedValue, ControllerOnValue, ControllerOffValue)
#             cmds.setAttr("Mouth.Wide_R_BS_Mesh", lock=0)  
#             cmds.setAttr("Emot_R_CC.translateX",2 )
#             cmds.setAttr("Mouth.Wide_R_BS_Mesh",1)          
#             cmds.setDrivenKeyframe("Mouth.Wide_R_BS_Mesh", cd="Emot_R_CC.translateX")
#             cmds.setAttr("Emot_R_CC.translateX",0 )
#             cmds.setAttr("Mouth.Wide_R_BS_Mesh",0)          
#             cmds.setDrivenKeyframe("Mouth.Wide_R_BS_Mesh", cd="Emot_R_CC.translateX")
#             cmds.setAttr("Emot_R_CC.translateX",0 )
#             cmds.setAttr("Mouth.Wide_R_BS_Mesh", lock=1)  
        if cmds.ls("Narrow_R_BS_Mesh"):
            Controller="Emot_R_CC.translateX"
            Child="Mouth.Narrow_R_BS_Mesh"
            defaultSet=0
            ChildActivatedValue=1
            ChildDeactivatedValue=0
            ControllerOnValue=-2
            ControllerOffValue=0
            getClass.controlSecondValueChildOn(Controller, Child, defaultSet, ChildActivatedValue, ChildDeactivatedValue, ControllerOnValue, ControllerOffValue)
#             cmds.setAttr("Mouth.Narrow_R_BS_Mesh", lock=0) 
#             cmds.setAttr("Emot_R_CC.translateX",-2 )
#             cmds.setAttr("Mouth.Narrow_R_BS_Mesh",1)          
#             cmds.setDrivenKeyframe("Mouth.Narrow_R_BS_Mesh", cd="Emot_R_CC.translateX")
#             cmds.setAttr("Emot_R_CC.translateX",0 )
#             cmds.setAttr("Mouth.Narrow_R_BS_Mesh",0)          
#             cmds.setDrivenKeyframe("Mouth.Narrow_R_BS_Mesh", cd="Emot_R_CC.translateX")
#             cmds.setAttr("Emot_R_CC.translateX",0 )
#             cmds.setAttr("Mouth.Narrow_R_BS_Mesh", lock=1) 
        if cmds.ls("Narrow_L_BS_Mesh"):
            Controller="Emot_L_CC.translateX"
            Child="Mouth.Narrow_L_BS_Mesh"
            defaultSet=0
            ChildActivatedValue=1
            ChildDeactivatedValue=0
            ControllerOnValue=-2
            ControllerOffValue=0
            getClass.controlSecondValueChildOn(Controller, Child, defaultSet, ChildActivatedValue, ChildDeactivatedValue, ControllerOnValue, ControllerOffValue)
#             cmds.setAttr("Mouth.Narrow_L_BS_Mesh", lock=0)  
#             cmds.setAttr("Emot_L_CC.translateX",-2 )
#             cmds.setAttr("Mouth.Narrow_L_BS_Mesh",1)          
#             cmds.setDrivenKeyframe("Mouth.Narrow_L_BS_Mesh", cd="Emot_L_CC.translateX")
#             cmds.setAttr("Emot_L_CC.translateX",0 )
#             cmds.setAttr("Mouth.Narrow_L_BS_Mesh",0)          
#             cmds.setDrivenKeyframe("Mouth.Narrow_L_BS_Mesh", cd="Emot_L_CC.translateX")
#             cmds.setAttr("Emot_L_CC.translateX",0 )   
#             cmds.setAttr("Mouth.Narrow_L_BS_Mesh", lock=1)      
        if cmds.ls("CheekUp_L_BS_Mesh"):
            Controller="*:*EyeMask_Ctrl.CheekLeftUp"
            Child="Mouth.CheekUp_L_BS_Mesh"
            defaultSet=0
            ChildActivatedValue=1
            ChildDeactivatedValue=0
            ControllerOnValue=1
            ControllerOffValue=0
            getClass.controlSecondValueChildOn(Controller, Child, defaultSet, ChildActivatedValue, ChildDeactivatedValue, ControllerOnValue, ControllerOffValue)
#             cmds.setAttr("Mouth.CheekUp_L_BS_Mesh", lock=0) 
#             cmds.setAttr("*:*EyeMask_Ctrl.CheekLeftUp",1 )
#             cmds.setAttr("Mouth.CheekUp_L_BS_Mesh",1)          
#             cmds.setDrivenKeyframe("Mouth.CheekUp_L_BS_Mesh", cd="*:*EyeMask_Ctrl.CheekLeftUp")
#             cmds.setAttr("*:*EyeMask_Ctrl.CheekLeftUp",0 )
#             cmds.setAttr("Mouth.CheekUp_L_BS_Mesh",0)          
#             cmds.setDrivenKeyframe("Mouth.CheekUp_L_BS_Mesh", cd="*:*EyeMask_Ctrl.CheekLeftUp")
#             cmds.setAttr("*:*EyeMask_Ctrl.CheekLeftUp",0 )    
#             cmds.setAttr("Mouth.CheekUp_L_BS_Mesh", lock=1) 
        if cmds.ls("CheekUp_R_BS_Mesh"): 
            Controller="*:*EyeMask_Ctrl.CheekRightUp"
            Child="Mouth.CheekUp_R_BS_Mesh"
            defaultSet=0
            ChildActivatedValue=1
            ChildDeactivatedValue=0
            ControllerOnValue=1
            ControllerOffValue=0
            getClass.controlSecondValueChildOn(Controller, Child, defaultSet, ChildActivatedValue, ChildDeactivatedValue, ControllerOnValue, ControllerOffValue)
                                   
#             cmds.setAttr("Mouth.CheekUp_R_BS_Mesh", lock=0) 
#             cmds.setAttr("*:*EyeMask_Ctrl.CheekRightUp",1 )
#             cmds.setAttr("Mouth.CheekUp_R_BS_Mesh",1)          
#             cmds.setDrivenKeyframe("Mouth.CheekUp_R_BS_Mesh", cd="*:*EyeMask_Ctrl.CheekRightUp")
#             cmds.setAttr("*:*EyeMask_Ctrl.CheekRightUp",0 )
#             cmds.setAttr("Mouth.CheekUp_R_BS_Mesh",0)          
#             cmds.setDrivenKeyframe("Mouth.CheekUp_R_BS_Mesh", cd="*:*EyeMask_Ctrl.CheekRightUp")
#             cmds.setAttr("*:*EyeMask_Ctrl.CheekRightUp",0 )    
#             cmds.setAttr("Mouth.CheekUp_R_BS_Mesh", lock=1) 
        print "recreated mouth blends"
             
    def eyelash_rivet(self):
        selObj=cmds.ls(sl=1, fl=1)
        getLists=zip(selObj[::2], selObj[1::2])
        for each in getLists:
            cmds.select(each[0])
            cmds.select(each[1], add=1)
            maya.mel.eval( "rivet;" )
            getRiv=cmds.ls(sl=1)
            cmds.rename(getRiv[0], "lashRivet")
            getNewRiv=cmds.ls(sl=1)
            getClass.makeJoint()
            cmds.parent(getNewRiv[0]+"_jnt", getNewRiv[0])
    def lid_attrs(self):
        cmds.addAttr("EyeMask_Ctrl", ln="RightLidDown", min=0, max=1, at="double", k=1, nn="RightLidDown")
        cmds.addAttr("EyeMask_Ctrl", ln="LeftLidDown", min=0, max=1, at="double", k=1, nn="LeftLidDown")
        cmds.addAttr("EyeMask_Ctrl", ln="RightLidUp", min=0, max=1, at="double", k=1, nn="RightLidUp")
        cmds.addAttr("EyeMask_Ctrl", ln="LeftLidUp", min=0, max=1, at="double", k=1, nn="LeftLidUp")
    def lid_sdk(self):
        #topRight 04
        cmds.setAttr("*:EyeMask_Ctrl.RightLidDown", 0 )
        cmds.setAttr("Lid_Open04_T_R_SDK.translateX",0)        
        cmds.setAttr("Lid_Open04_T_R_SDK.translateY",0)        
        cmds.setAttr("Lid_Open04_T_R_SDK.translateZ",0)        
        cmds.setDrivenKeyframe("Lid_Open04_T_R_SDK.translateX", cd="*:EyeMask_Ctrl.RightLidDown")
        cmds.setDrivenKeyframe("Lid_Open04_T_R_SDK.translateY", cd="*:EyeMask_Ctrl.RightLidDown")
        cmds.setDrivenKeyframe("Lid_Open04_T_R_SDK.translateZ", cd="*:EyeMask_Ctrl.RightLidDown")
        cmds.setAttr("*:EyeMask_Ctrl.RightLidDown", 1 )
        cmds.setAttr("Lid_Open04_T_R_SDK.translateX",-0.449)        
        cmds.setAttr("Lid_Open04_T_R_SDK.translateY",-0.848)        
        cmds.setAttr("Lid_Open04_T_R_SDK.translateZ",-0.06)        
        cmds.setDrivenKeyframe("Lid_Open04_T_R_SDK.translateX", cd="*:EyeMask_Ctrl.RightLidDown")
        cmds.setDrivenKeyframe("Lid_Open04_T_R_SDK.translateY", cd="*:EyeMask_Ctrl.RightLidDown")
        cmds.setDrivenKeyframe("Lid_Open04_T_R_SDK.translateZ", cd="*:EyeMask_Ctrl.RightLidDown")
        #topRight 03
        cmds.setAttr("*:EyeMask_Ctrl.RightLidDown", 0 )
        cmds.setAttr("Lid_Open03_T_R_SDK.translateX",0)        
        cmds.setAttr("Lid_Open03_T_R_SDK.translateY",0)        
        cmds.setAttr("Lid_Open03_T_R_SDK.translateZ",0)        
        cmds.setDrivenKeyframe("Lid_Open03_T_R_SDK.translateX", cd="*:EyeMask_Ctrl.RightLidDown")
        cmds.setDrivenKeyframe("Lid_Open03_T_R_SDK.translateY", cd="*:EyeMask_Ctrl.RightLidDown")
        cmds.setDrivenKeyframe("Lid_Open03_T_R_SDK.translateZ", cd="*:EyeMask_Ctrl.RightLidDown")
        cmds.setAttr("*:EyeMask_Ctrl.RightLidDown", 1 )
        cmds.setAttr("Lid_Open03_T_R_SDK.translateX",-0.049)        
        cmds.setAttr("Lid_Open03_T_R_SDK.translateY",-2.271)        
        cmds.setAttr("Lid_Open03_T_R_SDK.translateZ",0.037)        
        cmds.setDrivenKeyframe("Lid_Open03_T_R_SDK.translateX", cd="*:EyeMask_Ctrl.RightLidDown")
        cmds.setDrivenKeyframe("Lid_Open03_T_R_SDK.translateY", cd="*:EyeMask_Ctrl.RightLidDown")
        cmds.setDrivenKeyframe("Lid_Open03_T_R_SDK.translateZ", cd="*:EyeMask_Ctrl.RightLidDown")
        #topRight 02
        cmds.setAttr("*:EyeMask_Ctrl.RightLidDown", 0 )
        cmds.setAttr("Lid_Open02_T_R_SDK.translateX",0)        
        cmds.setAttr("Lid_Open02_T_R_SDK.translateY",0)        
        cmds.setAttr("Lid_Open02_T_R_SDK.translateZ",0)        
        cmds.setDrivenKeyframe("Lid_Open02_T_R_SDK.translateX", cd="*:EyeMask_Ctrl.RightLidDown")
        cmds.setDrivenKeyframe("Lid_Open02_T_R_SDK.translateY", cd="*:EyeMask_Ctrl.RightLidDown")
        cmds.setDrivenKeyframe("Lid_Open02_T_R_SDK.translateZ", cd="*:EyeMask_Ctrl.RightLidDown")
        cmds.setAttr("*:EyeMask_Ctrl.RightLidDown", 1 )
        cmds.setAttr("Lid_Open02_T_R_SDK.translateX",0.285)        
        cmds.setAttr("Lid_Open02_T_R_SDK.translateY",-1.763)        
        cmds.setAttr("Lid_Open02_T_R_SDK.translateZ",-0.086)        
        cmds.setDrivenKeyframe("Lid_Open02_T_R_SDK.translateX", cd="*:EyeMask_Ctrl.RightLidDown")
        cmds.setDrivenKeyframe("Lid_Open02_T_R_SDK.translateY", cd="*:EyeMask_Ctrl.RightLidDown")
        cmds.setDrivenKeyframe("Lid_Open02_T_R_SDK.translateZ", cd="*:EyeMask_Ctrl.RightLidDown")
        cmds.setAttr("*:EyeMask_Ctrl.RightLidDown", 0 )
        ###########
        #topLeft 04
        cmds.setAttr("*:EyeMask_Ctrl.LeftLidDown", 0 )
        cmds.setAttr("Lid_Open04_T_L_SDK.translateX",0)        
        cmds.setAttr("Lid_Open04_T_L_SDK.translateY",0)        
        cmds.setAttr("Lid_Open04_T_L_SDK.translateZ",0)        
        cmds.setDrivenKeyframe("Lid_Open04_T_L_SDK.translateX", cd="*:EyeMask_Ctrl.LeftLidDown")
        cmds.setDrivenKeyframe("Lid_Open04_T_L_SDK.translateY", cd="*:EyeMask_Ctrl.LeftLidDown")
        cmds.setDrivenKeyframe("Lid_Open04_T_L_SDK.translateZ", cd="*:EyeMask_Ctrl.LeftLidDown")
        cmds.setAttr("*:EyeMask_Ctrl.LeftLidDown", 1 )
        cmds.setAttr("Lid_Open04_T_L_SDK.translateX",0.449)        
        cmds.setAttr("Lid_Open04_T_L_SDK.translateY",-0.848)        
        cmds.setAttr("Lid_Open04_T_L_SDK.translateZ",-0.06)        
        cmds.setDrivenKeyframe("Lid_Open04_T_L_SDK.translateX", cd="*:EyeMask_Ctrl.LeftLidDown")
        cmds.setDrivenKeyframe("Lid_Open04_T_L_SDK.translateY", cd="*:EyeMask_Ctrl.LeftLidDown")
        cmds.setDrivenKeyframe("Lid_Open04_T_L_SDK.translateZ", cd="*:EyeMask_Ctrl.LeftLidDown")
        #topLeft 03
        cmds.setAttr("*:EyeMask_Ctrl.LeftLidDown", 0 )
        cmds.setAttr("Lid_Open03_T_L_SDK.translateX",0)        
        cmds.setAttr("Lid_Open03_T_L_SDK.translateY",0)        
        cmds.setAttr("Lid_Open03_T_L_SDK.translateZ",0)        
        cmds.setDrivenKeyframe("Lid_Open03_T_L_SDK.translateX", cd="*:EyeMask_Ctrl.LeftLidDown")
        cmds.setDrivenKeyframe("Lid_Open03_T_L_SDK.translateY", cd="*:EyeMask_Ctrl.LeftLidDown")
        cmds.setDrivenKeyframe("Lid_Open03_T_L_SDK.translateZ", cd="*:EyeMask_Ctrl.LeftLidDown")
        cmds.setAttr("*:EyeMask_Ctrl.LeftLidDown", 1 )
        cmds.setAttr("Lid_Open03_T_L_SDK.translateX",0.049)        
        cmds.setAttr("Lid_Open03_T_L_SDK.translateY",-2.271)        
        cmds.setAttr("Lid_Open03_T_L_SDK.translateZ",0.037)        
        cmds.setDrivenKeyframe("Lid_Open03_T_L_SDK.translateX", cd="*:EyeMask_Ctrl.LeftLidDown")
        cmds.setDrivenKeyframe("Lid_Open03_T_L_SDK.translateY", cd="*:EyeMask_Ctrl.LeftLidDown")
        cmds.setDrivenKeyframe("Lid_Open03_T_L_SDK.translateZ", cd="*:EyeMask_Ctrl.LeftLidDown")
        #topLeft 02

        cmds.setAttr("*:EyeMask_Ctrl.RightLidDown", 0 )
        cmds.setAttr("Lid_Open02_T_L_SDK.translateX",0)        
        cmds.setAttr("Lid_Open02_T_L_SDK.translateY",0)        
        cmds.setAttr("Lid_Open02_T_L_SDK.translateZ",0)        
        cmds.setDrivenKeyframe("Lid_Open02_T_L_SDK.translateX", cd="*:EyeMask_Ctrl.LeftLidDown")
        cmds.setDrivenKeyframe("Lid_Open02_T_L_SDK.translateY", cd="*:EyeMask_Ctrl.LeftLidDown")
        cmds.setDrivenKeyframe("Lid_Open02_T_L_SDK.translateZ", cd="*:EyeMask_Ctrl.LeftLidDown")
        cmds.setAttr("*:EyeMask_Ctrl.LeftLidDown", 1 )
        cmds.setAttr("Lid_Open02_T_L_SDK.translateX",-0.285)        
        cmds.setAttr("Lid_Open02_T_L_SDK.translateY",-1.763)        
        cmds.setAttr("Lid_Open02_T_L_SDK.translateZ",-0.086)        
        cmds.setDrivenKeyframe("Lid_Open02_T_L_SDK.translateX", cd="*:EyeMask_Ctrl.LeftLidDown")
        cmds.setDrivenKeyframe("Lid_Open02_T_L_SDK.translateY", cd="*:EyeMask_Ctrl.LeftLidDown")
        cmds.setDrivenKeyframe("Lid_Open02_T_L_SDK.translateZ", cd="*:EyeMask_Ctrl.LeftLidDown")        
        cmds.setAttr("*:EyeMask_Ctrl.LeftLidDown", 0 )
        
        #bottomRight 05
        cmds.setAttr("*:EyeMask_Ctrl.RightLidUp", 0 )
        cmds.setAttr("Lid_Open05_B_R_SDK.translateX",0)        
        cmds.setAttr("Lid_Open05_B_R_SDK.translateY",0)        
        cmds.setAttr("Lid_Open05_B_R_SDK.translateZ",0)        
        cmds.setDrivenKeyframe("Lid_Open05_B_R_SDK.translateX", cd="*:EyeMask_Ctrl.RightLidUp")
        cmds.setDrivenKeyframe("Lid_Open05_B_R_SDK.translateY", cd="*:EyeMask_Ctrl.RightLidUp")
        cmds.setDrivenKeyframe("Lid_Open05_B_R_SDK.translateZ", cd="*:EyeMask_Ctrl.RightLidUp")
        cmds.setAttr("*:EyeMask_Ctrl.RightLidUp", 1 )
        cmds.setAttr("Lid_Open05_B_R_SDK.translateX",-0.067)        
        cmds.setAttr("Lid_Open05_B_R_SDK.translateY",1.662)        
        cmds.setAttr("Lid_Open05_B_R_SDK.translateZ",0.178)        
        cmds.setDrivenKeyframe("Lid_Open05_B_R_SDK.translateX", cd="*:EyeMask_Ctrl.RightLidUp")
        cmds.setDrivenKeyframe("Lid_Open05_B_R_SDK.translateY", cd="*:EyeMask_Ctrl.RightLidUp")
        cmds.setDrivenKeyframe("Lid_Open05_B_R_SDK.translateZ", cd="*:EyeMask_Ctrl.RightLidUp")        
        #bottomRight 03
        cmds.setAttr("*:EyeMask_Ctrl.RightLidUp", 0 )
        cmds.setAttr("Lid_Open03_B_R_SDK.translateX",0)        
        cmds.setAttr("Lid_Open03_B_R_SDK.translateY",0)        
        cmds.setAttr("Lid_Open03_B_R_SDK.translateZ",0)        
        cmds.setDrivenKeyframe("Lid_Open03_B_R_SDK.translateX", cd="*:EyeMask_Ctrl.RightLidUp")
        cmds.setDrivenKeyframe("Lid_Open03_B_R_SDK.translateY", cd="*:EyeMask_Ctrl.RightLidUp")
        cmds.setDrivenKeyframe("Lid_Open03_B_R_SDK.translateZ", cd="*:EyeMask_Ctrl.RightLidUp")
        cmds.setAttr("*:EyeMask_Ctrl.RightLidUp", 1 )
        cmds.setAttr("Lid_Open03_B_R_SDK.translateX",0.249)        
        cmds.setAttr("Lid_Open03_B_R_SDK.translateY",2.44)        
        cmds.setAttr("Lid_Open03_B_R_SDK.translateZ",0.287)        
        cmds.setDrivenKeyframe("Lid_Open03_B_R_SDK.translateX", cd="*:EyeMask_Ctrl.RightLidUp")
        cmds.setDrivenKeyframe("Lid_Open03_B_R_SDK.translateY", cd="*:EyeMask_Ctrl.RightLidUp")
        cmds.setDrivenKeyframe("Lid_Open03_B_R_SDK.translateZ", cd="*:EyeMask_Ctrl.RightLidUp")        
        #bottomRight 03
        cmds.setAttr("*:EyeMask_Ctrl.RightLidUp", 0 )
        cmds.setAttr("Lid_Open04_B_R_SDK.translateX",0)        
        cmds.setAttr("Lid_Open04_B_R_SDK.translateY",0)        
        cmds.setAttr("Lid_Open04_B_R_SDK.translateZ",0)        
        cmds.setDrivenKeyframe("Lid_Open04_B_R_SDK.translateX", cd="*:EyeMask_Ctrl.RightLidUp")
        cmds.setDrivenKeyframe("Lid_Open04_B_R_SDK.translateY", cd="*:EyeMask_Ctrl.RightLidUp")
        cmds.setDrivenKeyframe("Lid_Open04_B_R_SDK.translateZ", cd="*:EyeMask_Ctrl.RightLidUp")
        cmds.setAttr("*:EyeMask_Ctrl.RightLidUp", 1 )
        cmds.setAttr("Lid_Open04_B_R_SDK.translateX",-0.132)        
        cmds.setAttr("Lid_Open04_B_R_SDK.translateY",2.637)        
        cmds.setAttr("Lid_Open04_B_R_SDK.translateZ",-0.048)        
        cmds.setDrivenKeyframe("Lid_Open04_B_R_SDK.translateX", cd="*:EyeMask_Ctrl.RightLidUp")
        cmds.setDrivenKeyframe("Lid_Open04_B_R_SDK.translateY", cd="*:EyeMask_Ctrl.RightLidUp")
        cmds.setDrivenKeyframe("Lid_Open04_B_R_SDK.translateZ", cd="*:EyeMask_Ctrl.RightLidUp")        
        #bottomRight 03
        cmds.setAttr("*:EyeMask_Ctrl.RightLidUp", 0 )
        cmds.setAttr("Lid_Open02_B_R_SDK.translateX",0)        
        cmds.setAttr("Lid_Open02_B_R_SDK.translateY",0)        
        cmds.setAttr("Lid_Open02_B_R_SDK.translateZ",0)
        cmds.setAttr("Lid_Open02_B_R_SDK.rotateZ",0)         
        cmds.setDrivenKeyframe("Lid_Open02_B_R_SDK.translateX", cd="*:EyeMask_Ctrl.RightLidUp")
        cmds.setDrivenKeyframe("Lid_Open02_B_R_SDK.translateY", cd="*:EyeMask_Ctrl.RightLidUp")
        cmds.setDrivenKeyframe("Lid_Open02_B_R_SDK.translateZ", cd="*:EyeMask_Ctrl.RightLidUp")
        cmds.setDrivenKeyframe("Lid_Open02_B_R_SDK.rotateZ", cd="*:EyeMask_Ctrl.RightLidUp")
        cmds.setAttr("*:EyeMask_Ctrl.RightLidUp", 1 )
        cmds.setAttr("Lid_Open02_B_R_SDK.translateX",-0.035)        
        cmds.setAttr("Lid_Open02_B_R_SDK.translateY",1.046)        
        cmds.setAttr("Lid_Open02_B_R_SDK.translateZ",0.112)        
        cmds.setAttr("Lid_Open02_B_R_SDK.rotateZ",51.433)        
        cmds.setDrivenKeyframe("Lid_Open02_B_R_SDK.translateX", cd="*:EyeMask_Ctrl.RightLidUp")
        cmds.setDrivenKeyframe("Lid_Open02_B_R_SDK.translateY", cd="*:EyeMask_Ctrl.RightLidUp")
        cmds.setDrivenKeyframe("Lid_Open02_B_R_SDK.translateZ", cd="*:EyeMask_Ctrl.RightLidUp")        
        cmds.setDrivenKeyframe("Lid_Open02_B_R_SDK.rotateZ", cd="*:EyeMask_Ctrl.RightLidUp")
        #bottomLeft05
        cmds.setAttr("*:EyeMask_Ctrl.LeftLidUp", 0 )
        cmds.setAttr("Lid_Open05_B_L_SDK.translateX",0)        
        cmds.setAttr("Lid_Open05_B_L_SDK.translateY",0)        
        cmds.setAttr("Lid_Open05_B_L_SDK.translateZ",0)        
        cmds.setDrivenKeyframe("Lid_Open05_B_L_SDK.translateX", cd="*:EyeMask_Ctrl.LeftLidUp")
        cmds.setDrivenKeyframe("Lid_Open05_B_L_SDK.translateY", cd="*:EyeMask_Ctrl.LeftLidUp")
        cmds.setDrivenKeyframe("Lid_Open05_B_L_SDK.translateZ", cd="*:EyeMask_Ctrl.LeftLidUp")
        cmds.setAttr("*:EyeMask_Ctrl.LeftLidUp", 1 )
        cmds.setAttr("Lid_Open05_B_L_SDK.translateX",0.067)        
        cmds.setAttr("Lid_Open05_B_L_SDK.translateY",1.662)        
        cmds.setAttr("Lid_Open05_B_L_SDK.translateZ",0.178)        
        cmds.setDrivenKeyframe("Lid_Open05_B_L_SDK.translateX", cd="*:EyeMask_Ctrl.LeftLidUp")
        cmds.setDrivenKeyframe("Lid_Open05_B_L_SDK.translateY", cd="*:EyeMask_Ctrl.LeftLidUp")
        cmds.setDrivenKeyframe("Lid_Open05_B_L_SDK.translateZ", cd="*:EyeMask_Ctrl.LeftLidUp")   
        cmds.setAttr("*:EyeMask_Ctrl.RightLidUp", 0)             
        #bottomLeft 03
        cmds.setAttr("*:EyeMask_Ctrl.LeftLidUp", 0 )
        cmds.setAttr("Lid_Open03_B_L_SDK.translateX",0)        
        cmds.setAttr("Lid_Open03_B_L_SDK.translateY",0)        
        cmds.setAttr("Lid_Open03_B_L_SDK.translateZ",0)        
        cmds.setDrivenKeyframe("Lid_Open03_B_L_SDK.translateX", cd="*:EyeMask_Ctrl.LeftLidUp")
        cmds.setDrivenKeyframe("Lid_Open03_B_L_SDK.translateY", cd="*:EyeMask_Ctrl.LeftLidUp")
        cmds.setDrivenKeyframe("Lid_Open03_B_L_SDK.translateZ", cd="*:EyeMask_Ctrl.LeftLidUp")
        cmds.setAttr("*:EyeMask_Ctrl.LeftLidUp", 1 )
        cmds.setAttr("Lid_Open03_B_L_SDK.translateX",-0.249)        
        cmds.setAttr("Lid_Open03_B_L_SDK.translateY",2.44)        
        cmds.setAttr("Lid_Open03_B_L_SDK.translateZ",0.287)        
        cmds.setDrivenKeyframe("Lid_Open03_B_L_SDK.translateX", cd="*:EyeMask_Ctrl.LeftLidUp")
        cmds.setDrivenKeyframe("Lid_Open03_B_L_SDK.translateY", cd="*:EyeMask_Ctrl.LeftLidUp")
        cmds.setDrivenKeyframe("Lid_Open03_B_L_SDK.translateZ", cd="*:EyeMask_Ctrl.LeftLidUp")        
        #bottomLeft 03
        cmds.setAttr("*:EyeMask_Ctrl.LeftLidUp", 0 )
        cmds.setAttr("Lid_Open04_B_L_SDK.translateX",0)        
        cmds.setAttr("Lid_Open04_B_L_SDK.translateY",0)        
        cmds.setAttr("Lid_Open04_B_L_SDK.translateZ",0)        
        cmds.setDrivenKeyframe("Lid_Open04_B_L_SDK.translateX", cd="*:EyeMask_Ctrl.LeftLidUp")
        cmds.setDrivenKeyframe("Lid_Open04_B_L_SDK.translateY", cd="*:EyeMask_Ctrl.LeftLidUp")
        cmds.setDrivenKeyframe("Lid_Open04_B_L_SDK.translateZ", cd="*:EyeMask_Ctrl.LeftLidUp")
        cmds.setAttr("*:EyeMask_Ctrl.LeftLidUp", 1 )
        cmds.setAttr("Lid_Open04_B_L_SDK.translateX",0.132)        
        cmds.setAttr("Lid_Open04_B_L_SDK.translateY",2.637)        
        cmds.setAttr("Lid_Open04_B_L_SDK.translateZ",-0.048)        
        cmds.setDrivenKeyframe("Lid_Open04_B_L_SDK.translateX", cd="*:EyeMask_Ctrl.LeftLidUp")
        cmds.setDrivenKeyframe("Lid_Open04_B_L_SDK.translateY", cd="*:EyeMask_Ctrl.LeftLidUp")
        cmds.setDrivenKeyframe("Lid_Open04_B_L_SDK.translateZ", cd="*:EyeMask_Ctrl.LeftLidUp")        
        #bottomLeft 03
        cmds.setAttr("*:EyeMask_Ctrl.LeftLidUp", 0 )
        cmds.setAttr("Lid_Open02_B_L_SDK.translateX",0)        
        cmds.setAttr("Lid_Open02_B_L_SDK.translateY",0)        
        cmds.setAttr("Lid_Open02_B_L_SDK.translateZ",0)
        cmds.setAttr("Lid_Open02_B_L_SDK.rotateZ",0)         
        cmds.setDrivenKeyframe("Lid_Open02_B_L_SDK.translateX", cd="*:EyeMask_Ctrl.LeftLidUp")
        cmds.setDrivenKeyframe("Lid_Open02_B_L_SDK.translateY", cd="*:EyeMask_Ctrl.LeftLidUp")
        cmds.setDrivenKeyframe("Lid_Open02_B_L_SDK.translateZ", cd="*:EyeMask_Ctrl.LeftLidUp")
        cmds.setDrivenKeyframe("Lid_Open02_B_L_SDK.rotateZ", cd="*:EyeMask_Ctrl.LeftLidUp")
        cmds.setAttr("*:EyeMask_Ctrl.LeftLidUp", 1 )
        cmds.setAttr("Lid_Open02_B_L_SDK.translateX",0.035)        
        cmds.setAttr("Lid_Open02_B_L_SDK.translateY",1.046)        
        cmds.setAttr("Lid_Open02_B_L_SDK.translateZ",0.112)        
        cmds.setAttr("Lid_Open02_B_L_SDK.rotateZ",-51.433)        
        cmds.setDrivenKeyframe("Lid_Open02_B_L_SDK.translateX", cd="*:EyeMask_Ctrl.LeftLidUp")
        cmds.setDrivenKeyframe("Lid_Open02_B_L_SDK.translateY", cd="*:EyeMask_Ctrl.LeftLidUp")
        cmds.setDrivenKeyframe("Lid_Open02_B_L_SDK.translateZ", cd="*:EyeMask_Ctrl.LeftLidUp")        
        cmds.setDrivenKeyframe("Lid_Open02_B_L_SDK.rotateZ", cd="*:EyeMask_Ctrl.LeftLidUp")        
        cmds.setAttr("*:EyeMask_Ctrl.LeftLidUp", 0 )
    
    def scaleMouthCorners(self):
        cmds.setAttr("Lip_Corner_R_Ctrl.scaleX", cb=1, l=0)
        cmds.setAttr("Lip_Corner_R_Ctrl.scaleY", cb=1, l=0)
        cmds.setAttr("Lip_Corner_R_Ctrl.scaleZ", cb=1, l=0)
        cmds.setAttr("Lip_Corner_R_Ctrl.scaleX", k=True)
        cmds.setAttr("Lip_Corner_R_Ctrl.scaleY", k=True)
        cmds.setAttr("Lip_Corner_R_Ctrl.scaleZ", k=True)        
        cmds.setAttr("Lip_Corner_L_Ctrl.scaleX", cb=1, l=0)
        cmds.setAttr("Lip_Corner_L_Ctrl.scaleY", cb=1, l=0)
        cmds.setAttr("Lip_Corner_L_Ctrl.scaleZ", cb=1, l=0)
        cmds.setAttr("Lip_Corner_L_Ctrl.scaleX", k=True)
        cmds.setAttr("Lip_Corner_L_Ctrl.scaleY", k=True)
        cmds.setAttr("Lip_Corner_L_Ctrl.scaleZ", k=True)        
        cmds.setAttr("Lip_B_R_Ctrl.scaleX", cb=1, l=0)
        cmds.setAttr("Lip_B_R_Ctrl.scaleY", cb=1, l=0)
        cmds.setAttr("Lip_B_R_Ctrl.scaleZ", cb=1, l=0)
        cmds.setAttr("Lip_B_R_Ctrl.scaleX", k=True)
        cmds.setAttr("Lip_B_R_Ctrl.scaleY", k=True)
        cmds.setAttr("Lip_B_R_Ctrl.scaleZ", k=True)        
        cmds.setAttr("Lip_B_L_Ctrl.scaleX", cb=1, l=0)
        cmds.setAttr("Lip_B_L_Ctrl.scaleY", cb=1, l=0)
        cmds.setAttr("Lip_B_L_Ctrl.scaleZ", cb=1, l=0)
        cmds.setAttr("Lip_B_L_Ctrl.scaleX", k=True)
        cmds.setAttr("Lip_B_L_Ctrl.scaleY", k=True)
        cmds.setAttr("Lip_B_L_Ctrl.scaleZ", k=True)        
        cmds.setAttr("Lip_B_Ctrl.scaleX", cb=1, l=0)
        cmds.setAttr("Lip_B_Ctrl.scaleY", cb=1, l=0)
        cmds.setAttr("Lip_B_Ctrl.scaleZ", cb=1, l=0)
        cmds.setAttr("Lip_B_Ctrl.scaleX", k=True)
        cmds.setAttr("Lip_B_Ctrl.scaleY", k=True)
        cmds.setAttr("Lip_B_Ctrl.scaleZ", k=True)        
        cmds.setAttr("Lip_T_R_Ctrl.scaleX", cb=1, l=0)
        cmds.setAttr("Lip_T_R_Ctrl.scaleY", cb=1, l=0)
        cmds.setAttr("Lip_T_R_Ctrl.scaleZ", cb=1, l=0)
        cmds.setAttr("Lip_T_R_Ctrl.scaleX", k=True)
        cmds.setAttr("Lip_T_R_Ctrl.scaleY", k=True)
        cmds.setAttr("Lip_T_R_Ctrl.scaleZ", k=True)        
        cmds.setAttr("Lip_T_L_Ctrl.scaleX", cb=1, l=0)
        cmds.setAttr("Lip_T_L_Ctrl.scaleY", cb=1, l=0)
        cmds.setAttr("Lip_T_L_Ctrl.scaleZ", cb=1, l=0)
        cmds.setAttr("Lip_T_L_Ctrl.scaleX", k=True)
        cmds.setAttr("Lip_T_L_Ctrl.scaleY", k=True)
        cmds.setAttr("Lip_T_L_Ctrl.scaleZ", k=True)        
        cmds.setAttr("Lip_T_Ctrl.scaleX", cb=1, l=0)
        cmds.setAttr("Lip_T_Ctrl.scaleY", cb=1, l=0)
        cmds.setAttr("Lip_T_Ctrl.scaleZ", cb=1, l=0)
        cmds.setAttr("Lip_T_Ctrl.scaleX", k=True)
        cmds.setAttr("Lip_T_Ctrl.scaleY", k=True)
        cmds.setAttr("Lip_T_Ctrl.scaleZ", k=True)        
        cmds.scaleConstraint("Lip_Corner_R_Ctrl", "faceLip_Corner_R_jnt")
        cmds.scaleConstraint("Lip_Corner_L_Ctrl", "faceLip_Corner_L_jnt")
        cmds.scaleConstraint("Lip_B_L_Ctrl", "faceLip_B_L_jnt")
        cmds.scaleConstraint("Lip_B_R_Ctrl", "faceLip_B_R_jnt")
        cmds.scaleConstraint("Lip_B_Ctrl", "faceLip_B_jnt")
        cmds.scaleConstraint("Lip_T_L_Ctrl", "faceLip_T_L_jnt")
        cmds.scaleConstraint("Lip_T_R_Ctrl", "faceLip_T_R_jnt")
        cmds.scaleConstraint("Lip_T_Ctrl", "faceLip_T_jnt")
     
                
    def lidfix(self):
        getFaceSkin=cmds.ls(sl=1, fl=1)
        colour=22
        getTranslation, getRotation=getClass.locationXForm("faceLid_Open02_T_R_lctrLid_Pivot_jnt_ik")
        name="faceLid_Open02"
        grpname="faceLid_Open02_lctr_grp"
        getClass.buildLoc(name, grpname, getTranslation, getRotation, colour)
        getTranslation, getRotation=getClass.locationXForm("faceLid_Open03_T_R_lctrLid_Pivot_jnt_ik")
        name="faceLid_Open03"
        grpname="faceLid_Open03_lctr_grp"
        getClass.buildLoc(name, grpname, getTranslation, getRotation, colour)
        getTranslation, getRotation=getClass.locationXForm("faceLid_Open01_T_R_lctrLid_Pivot_jnt_ik")
        name="faceLid_Open01"
        grpname="faceLid_Open01_lctr_grp"
        getClass.buildLoc(name, grpname, getTranslation, getRotation, colour)
        getTranslation, getRotation=getClass.locationXForm("faceLid_Open04_T_R_lctrLid_Pivot_jnt_ik")
        name="faceLid_Open04"
        grpname="faceLid_Open04_lctr_grp"
        getClass.buildLoc(name, grpname, getTranslation, getRotation, colour)
        getTranslation, getRotation=getClass.locationXForm("faceLid_Closed01_R_lctrLid_Pivot_jnt_ik")
        name="faceLid_Closed01"
        grpname="faceLid_Closed01_lctr_grp"
        getClass.buildLoc(name, grpname, getTranslation, getRotation, colour)
        getTranslation, getRotation=getClass.locationXForm("faceLid_Closed02_R_lctrLid_Pivot_jnt_ik")
        name="faceLid_Closed02"
        grpname="faceLid_Closed02_lctr_grp"
        getClass.buildLoc(name, grpname, getTranslation, getRotation, colour)
        getTranslation, getRotation=getClass.locationXForm("faceLid_Closed03_R_lctrLid_Pivot_jnt_ik")
        name="faceLid_Closed03"
        grpname="faceLid_Closed03_lctr_grp"
        getClass.buildLoc(name, grpname, getTranslation, getRotation, colour)
        getTranslation, getRotation=getClass.locationXForm("faceLid_Closed04_R_lctrLid_Pivot_jnt_ik")
        name="faceLid_Closed04"
        grpname="faceLid_Closed04_lctr_grp"
        getClass.buildLoc(name, grpname, getTranslation, getRotation, colour)
        cmds.select("faceLid_Open01_lctr_grp")
        cmds.select("faceLid_Open02_lctr_grp", add=1)
        cmds.select("faceLid_Open03_lctr_grp", add=1)
        cmds.select("faceLid_Open04_lctr_grp", add=1)
        cmds.select("faceLid_Closed01_lctr_grp", add=1)
        cmds.select("faceLid_Closed02_lctr_grp", add=1)
        cmds.select("faceLid_Closed03_lctr_grp", add=1)
        cmds.select("faceLid_Closed04_lctr_grp", add=1)
        cmds.group(n="newGrp")
        cmds.CreateEmptyGroup()
        getObj=cmds.ls(sl=1)
        cmds.parent("newGrp", getObj[0])
        cmds.setAttr(getObj[0]+".scaleX", -1)
        cmds.MoveSkinJointsTool()     
        try:
            cmds.parent("faceLid_Open03_T_L_lctrLid_Pivot_jnt_ik", "Lid_Open03_T_L_Ctrl")
        except:
            pass
        try:
            cmds.parent("faceLid_Open03_T_R_lctrLid_Pivot_jnt_ik", "Lid_Open03_T_R_Ctrl")
        except:
            pass
        getClass.xformAutoMove("faceLid_Open04_T_L_lctrLid_Pivot_jnt_ik", "faceLid_Open04_lctr")
        getClass.xformAutoMove("faceLid_Open03_T_L_lctrLid_Pivot_jnt_ik", "faceLid_Open03_lctr")
        getClass.xformAutoMove("faceLid_Open02_T_L_lctrLid_Pivot_jnt_ik", "faceLid_Open02_lctr")
        getClass.xformAutoMove("faceLid_Open01_T_L_lctrLid_Pivot_jnt_ik", "faceLid_Open01_lctr")
        getClass.xformAutoMove("faceLid_Closed01_L_lctrLid_Pivot_jnt_ik", "faceLid_Closed01_lctr")
        getClass.xformAutoMove("faceLid_Closed02_L_lctrLid_Pivot_jnt_ik", "faceLid_Closed02_lctr")
        getClass.xformAutoMove("faceLid_Closed03_L_lctrLid_Pivot_jnt_ik", "faceLid_Closed03_lctr")
        getClass.xformAutoMove("faceLid_Closed04_L_lctrLid_Pivot_jnt_ik", "faceLid_Closed04_lctr")
        cmds.delete(getObj[0])
        maya.mel.eval( "moveJointsMode 0;" )
        
#         for each in getFaceSkin:
#             getSkinCluster=cmds.skinCluster(each, q=1, dt=1)
#             skinID, getInf=getClass.skinClust(getSkinCluster, each)  
#             cmds.copySkinWeights(ss=skinID, ds=skinID, mm="YZ", mi=0, sa="closestPoint", ia="oneToOne", nr=1)

#         getTranslation, getRotation=getClass.locationXForm("faceLid_Open02_lctr")    
#         cmds.select("faceLid_Open02_lctr")
#         cmds.select("faceLid_Open02_T_L_lctrLid_Pivot_jnt_ik", add=1)
#         getClass.xformtran()
#         getTranslation, getRotation=getClass.locationXForm("faceLid_Open03_lctr")           
#         cmds.select("faceLid_Open03_lctr")
#         cmds.select("faceLid_Open03_T_L_lctrLid_Pivot_jnt_ik", add=1)
#         getClass.xformtran()
#     def Chin_Attr(self):
#         cmds.addAttr("Chin_Ctrl", ln="Chin", min=0, max=1, at="double", k=1, nn="Chin")
#     def Chin_Blends(self):
#         selObj=cmds.ls(sl=1, fl=1)
#         cmds.blendShape("Chin_BS_Mesh", selObj[0],  n="Chin_Blend", foc=1)
#         cmds.blendShape("Chin_in_BS_Mesh", selObj[0],  n="Chin_in_Blend", foc=1)
#         cmds.setAttr("*:Chin_Ctrl.Chin",0)
#         cmds.setAttr("Chin_Blend.Chin_BS_Mesh", 0)          
#         cmds.setDrivenKeyframe("Chin_Blend.Chin_BS_Mesh", cd="*:Chin_Ctrl.Chin")
#         cmds.setAttr("*:Chin_Ctrl.Chin",1)
#         cmds.setAttr("Chin_Blend.Chin_BS_Mesh", 1)          
#         cmds.setDrivenKeyframe("Chin_Blend.Chin_BS_Mesh", cd="*:Chin_Ctrl.Chin")
#         cmds.setAttr("*:Chin_Ctrl.Chin",0)
#         cmds.setAttr("Chin_in_Blend.Chin_in_BS_Mesh", 0)          
#         cmds.setDrivenKeyframe("Chin_in_Blend.Chin_in_BS_Mesh", cd="*:Chin_Ctrl.Chin")
#         cmds.setAttr("*:Chin_Ctrl.Chin",-1)
#         cmds.setAttr("Chin_in_Blend.Chin_in_BS_Mesh", 1)          
#         cmds.setDrivenKeyframe("Chin_in_Blend.Chin_in_BS_Mesh", cd="*:Chin_Ctrl.Chin")
#         cmds.setAttr("*:Chin_Ctrl.Chin",0 )              
    def BottLip_Attr(self):
        cmds.addAttr("Chin_Ctrl", ln="FullBottLip", min=0, max=1, at="double", k=1, nn="FullBottLip")
    def BottLip_Blends(self):
        selObj=cmds.ls(sl=1, fl=1)
        cmds.blendShape("FatLip_BS_Mesh", selObj[0],  n="Bott_Fat_Lip_Blend", foc=1)        
        cmds.setAttr("*:Chin_Ctrl.FullBottLip",0)
        cmds.setAttr("Bott_Fat_Lip_Blend.FatLip_BS_Mesh", 0)
        cmds.setDrivenKeyframe("Bott_Fat_Lip_Blend.FatLip_BS_Mesh", cd="*:Chin_Ctrl.FullBottLip")
        cmds.setAttr("*:Chin_Ctrl.FullBottLip",1)
        cmds.setAttr("Bott_Fat_Lip_Blend.FatLip_BS_Mesh", 1)
        cmds.setDrivenKeyframe("Bott_Fat_Lip_Blend.FatLip_BS_Mesh", cd="*:Chin_Ctrl.FullBottLip")
        cmds.setAttr("*:Chin_Ctrl.FullBottLip",0)
        try:
            cmds.setAttr("Bott_Fat_Lip_Blend.FatLip_BS_Mesh",l=1)
        except:
            pass

    def Blink_SDK(self):
        try:
            cmds.setAttr("*:EyeMask_Ctrl.Blink_Left", 0 )
            cmds.setAttr("Eye_L_scpt.envelope",0)        
            cmds.setDrivenKeyframe("Eye_L_scpt.envelope", cd="*:EyeMask_Ctrl.Blink_Left")
            cmds.setAttr("*:EyeMask_Ctrl.Blink_Left", .2)
            cmds.setAttr("Eye_L_scpt.envelope",1)        
            cmds.setDrivenKeyframe("Eye_L_scpt.envelope", cd="*:EyeMask_Ctrl.Blink_Left")
            cmds.setAttr("*:EyeMask_Ctrl.Blink_Left", 0 )
            cmds.setAttr("*:EyeMask_Ctrl.Blink_Right", 0 )
            cmds.setAttr("Eye_R_scpt.envelope",0)        
            cmds.setDrivenKeyframe("Eye_R_scpt.envelope", cd="*:EyeMask_Ctrl.Blink_Right")
            cmds.setAttr("*:EyeMask_Ctrl.Blink_Right", .2)
            cmds.setAttr("Eye_R_scpt.envelope",1)        
            cmds.setDrivenKeyframe("Eye_R_scpt.envelope", cd="*:EyeMask_Ctrl.Blink_Right")
            cmds.setAttr("*:EyeMask_Ctrl.Blink_Right", 0 )
            cmds.setAttr("Eye_L_scpt.envelope",l=1) 
            cmds.setAttr("Eye_R_scpt.envelope",l=1) 
        except:
            pass
        try:
            cmds.setAttr("*:EyeMask_Ctrl.LeftBlinkHeight", 0 )
            cmds.setAttr("Eye_L_scpt.envelope",0)        
            cmds.setDrivenKeyframe("Eye_L_scpt.envelope", cd="*:EyeMask_Ctrl.LeftBlinkHeight")
            cmds.setAttr("*:EyeMask_Ctrl.LeftBlinkHeight", .6)
            cmds.setAttr("Eye_L_scpt.envelope",1)        
            cmds.setDrivenKeyframe("Eye_L_scpt.envelope", cd="*:EyeMask_Ctrl.LeftBlinkHeight")
            cmds.setAttr("*:EyeMask_Ctrl.LeftBlinkHeight", 0 )
            cmds.setAttr("*:EyeMask_Ctrl.RightBlinkHeight", 0 )
            cmds.setAttr("Eye_R_scpt.envelope",0)        
            cmds.setDrivenKeyframe("Eye_R_scpt.envelope", cd="*:EyeMask_Ctrl.RightBlinkHeight")
            cmds.setAttr("*:EyeMask_Ctrl.RightBlinkHeight", .6)
            cmds.setAttr("Eye_R_scpt.envelope",1)        
            cmds.setDrivenKeyframe("Eye_R_scpt.envelope", cd="*:EyeMask_Ctrl.RightBlinkHeight")
            cmds.setAttr("*:EyeMask_Ctrl.RightBlinkHeight", 0 )
            cmds.setAttr("Eye_L_scpt.envelope",l=1) 
            cmds.setAttr("Eye_R_scpt.envelope",l=1) 
        except:
            pass