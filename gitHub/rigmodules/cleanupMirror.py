import maya.cmds as cmds
import maya.mel
from functools import partial
from string import *
import re
import sys

import os, subprocess, sys, platform
from os  import popen
from sys import stdin
import unicodedata

'''MG rigging modules'''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons License'
'http://creativecommons.org/licenses/by-sa/3.0/au/'

trans=[".tx", ".ty", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz"]  

import baseFunctions_maya
reload (baseFunctions_maya)
getClass=baseFunctions_maya.BaseClass()


class cln(object):
    def __init__(self):
        ########
        #Lock and hide scales
        ########           
        getGuidesToDelete=cmds.ls("*_guide")
        for each in getGuidesToDelete:
            cmds.delete(each)
        allLoc=cmds.ls("*_lctr")   
        for eachlctr in allLoc:
            if "knee" in eachlctr:
                lognm=eachlctr.replace("_jnt_ikPole_lctr", '_Ctrl')   
                nlognm=lognm.replace("leg", '') 
                splitCentric= re.split(r'([A-Z][a-z]*)', nlognm)
                splitCentric[0]=str.capitalize(str(splitCentric[0]))
                splitCentric[0]=splitCentric[0]+"_PoleVector"
                if '' in splitCentric:
                    splitCentric.remove('')
                    splitCentric.remove('_')                     
                newCentric='_'.join(splitCentric) 
                cmds.rename(eachlctr, newCentric)                       
        allControllers=cmds.ls("*_ctrl")
        for each in allControllers:
            #cmds.setAttr(str(each)+".visibility" , keyable=0, cb=0)            
            cmds.setAttr(str(each)+".sx" , keyable=0, lock=1)
            cmds.setAttr(str(each)+".sy" , keyable=0, lock=1)
            cmds.setAttr(str(each)+".sz", keyable=0, lock=1)           
            #cmds.setAttr(str(each)+".visiblity", keyable=0, lock=1)
            if "head01" in each:
                lognm=each.replace("head01", 'Head') 
                cmds.rename(each, lognm)
            if "arm" in each and "hand" not in each and "Knuckle" not in each:
                bodyPart="arm"
                if "IK" in each:
                    Kinetic="IK"  
                    if "offset" in each:
                        newCentric=self.renaming_centric_kenetic(each, bodyPart, Kinetic)
                        bucket=newCentric.split("_")
                        for spot in bucket:
                            if spot=="":
                                bucket.remove(spot)                        
                        bucket[-4:-3], bucket[-3:-2] = bucket[-3:-2], bucket[-4:-3]
                        bucket[-3:-2], bucket[-2:-1] = bucket[-2:-1],bucket[-3:-2]
                        newName='_'.join(bucket)
                        cmds.rename(each, newName)  
                    else:                             
                        newCentric=self.renaming_centric_swap(each, bodyPart, Kinetic) 
                        cmds.rename(each, newCentric)
                else:                
                    newCentric=self.renaming_centric(each, bodyPart) 
                    cmds.rename(each, newCentric)                 
#             if "arm" in each and "hand" in each and "Knuckle" not in each and "IK" in each:
#                 bodyPart="arm"
#                 Kinetic="IK" 
#                 newCentric=self.renaming_centric_swap(each, bodyPart, Kinetic) 
#                 bucket=newCentric.split("_")
#                 #bucket[-3:-2], bucket[-2:-1] = bucket[-2:-1],bucket[-3:-2]
#                 newName='_'.join(bucket)
#                 print newName
#                 print each
#                 cmds.rename(each, newName)
            if "armthumbMidKnuckle" in each:                                    
                cmds.setAttr(each+".rx" , keyable=0, lock=1)
                cmds.setAttr(each+".rz", keyable=0, lock=1)  
                cmds.setAttr(each+".tx" , keyable=0, lock=1)
                cmds.setAttr(each+".ty" , keyable=0, lock=1)
                cmds.setAttr(each+".tz", keyable=0, lock=1)                                              
            if "hand" in each:
                lognm=each.replace("hand", "Hand_" )   
                nlognm=lognm.replace("arm", '')     
                unicodedata.normalize('NFKD', nlognm).encode('ascii','ignore')
                getpiece=nlognm.split('_')
                bucket=[]
                mybucket=[]
                if "IK" in each:                
                    bodyPart="Hand"
                    Kinetic="IK"          
                    newCentric=self.renaming_centric_kenetic(each, bodyPart, Kinetic)
                    bucket=newCentric.split("_") 
                    bucket[-3:-2], bucket[-2:-1] = bucket[-2:-1],bucket[-3:-2]
                    newName='_'.join(bucket)
                    cmds.rename(each, newName)
                elif "offset" in each:
                    for part in getpiece:
                        capitalString=str.capitalize(str(part))
                        bucket.append(capitalString)
                    for eachPart in bucket:
                        if "Left" in eachPart or "Right" in eachPart:
                            getTruename= "Offset_"+eachPart[0]
                            mybucket.append(getTruename)
                        else:
                            getTruename= "Offset_"+eachPart
                            mybucket.append(eachPart)                     
                    ##bucket=self.swapCentricSuf(bucket)                      
                    newName='_'.join(mybucket)
                    cmds.rename(each, newName)                      
                elif "offset" not in each:                       
                    for part in getpiece:
                        capitalString=str.capitalize(str(part))
                        bucket.append(capitalString)
                    for eachPart in bucket:
                        if "Left" in eachPart or "Right" in eachPart:
                            mybucket.append(eachPart[0])
                        else:
                            mybucket.append(eachPart)                     
                    ##bucket=self.swapCentricSuf(bucket)                      
                    newName='_'.join(mybucket)
                    cmds.rename(each, newName)  
            if "thumb" in each:
                lognm=each.replace("Knuckle", '_')   
                nlognm=lognm.replace("arm", '')     
                alognm=nlognm.replace("Finger", '_Finger')  
                unicodedata.normalize('NFKD', alognm).encode('ascii','ignore')
                getpiece=alognm.split('_')
                bucket=[]
                for part in getpiece:
                    capitalString=str.capitalize(str(part))
                    bucket.append(capitalString)
                getSide= str(bucket[-2:-1])
                bucket[-2:-1]=getSide[2]
                #bucket=self.swapCentricSuf(bucket)                   
                newName='_'.join(bucket)
                cmds.rename(each, newName)
            if "Finger" in each:                
                cmds.setAttr(each+".tx" , keyable=0, lock=1)
                cmds.setAttr(each+".ty" , keyable=0, lock=1)
                cmds.setAttr(each+".tz", keyable=0, lock=1)
                lognm=each.replace("BaseKnuckle", '_')   
                nlognm=lognm.replace("arm", '')     
                alognm=nlognm.replace("Finger", '_Finger')  
                unicodedata.normalize('NFKD', alognm).encode('ascii','ignore')
                getpiece=alognm.split('_')
                bucket=[]
                for part in getpiece:
                    capitalString=str.capitalize(str(part))
                    bucket.append(capitalString)
                getSide= str(bucket[-2:-1])
                bucket[-2:-1]=getSide[2]                    
                #bucket=self.swapCentricSuf(bucket)                     
                newName='_'.join(bucket)
                cmds.rename(each, newName)                    
            if "leg" in each:
                bodyPart="leg"
                if "IK" in each:
                    Kinetic="IK"          
                    newCentric=self.renaming_centric_kenetic(each, bodyPart, Kinetic) 
                    cmds.rename(each, newCentric)  
                if "FK" in each:
                    Kinetic="FK"
                    newCentric=self.renaming_centric_kenetic(each, bodyPart, Kinetic)  
                    cmds.rename(each, newCentric)                                      
                else:
                    newCentric=self.renaming_centric(each, bodyPart) 
                    cmds.rename(each, newCentric)
  
            if "foot" in each:
                bodyPart="foot"
                if "IK" in each:
                    Kinetic="IK"          
                    newCentric=self.renaming_centric_kenetic(each, bodyPart, Kinetic) 
                    bucket=newCentric.split("_")
                    bucket[-3:-2], bucket[-2:-1] = bucket[-2:-1],bucket[-3:-2]
                    newName='_'.join(bucket)
                    cmds.rename(each, newName)  
                if "FK" in each:
                    Kinetic="FK"
                    newCentric=self.renaming_centric_kenetic(each, bodyPart, Kinetic)  
                    cmds.rename(each, newCentric)                   
                try:   
                    newCentric=self.renaming_centric(each, bodyPart) 
                    cmds.rename(each, newCentric)
                except:
                    pass

                        
            getJointsToHide=cmds.ls("*IK*", typ="joint")
            for each in getJointsToHide:
                if "arm" not in each:
                    cmds.setAttr(each+".visibility", 0)
                
            getJointsToHide=cmds.ls("*FK*", typ="joint")
            for each in getJointsToHide:
                cmds.setAttr(each+".visibility", 0)    
            
            getJointsToHide=cmds.ls(typ="ikHandle")
            for each in getJointsToHide:
                cmds.setAttr(each+".visibility", 0) 
                
            getJointsToHide=cmds.ls("*RFL*", typ="joint")
            for each in getJointsToHide:
                cmds.setAttr(each+".visibility", 0)    
                
            getJointsToHide=cmds.ls("*Clst*", typ="joint")
            for each in getJointsToHide:
                cmds.setAttr(each+".visibility", 0) 
            

        
            try:
                cmds.delete("Guides_*_grp")
                cmds.delete("armcollarLeft_jnt")
                cmds.delete("armcollarRight_jnt")
            except:
                pass    

            
            getJointsToHide=cmds.ls("*dis*")
            for each in getJointsToHide:
                cmds.setAttr(each+".visibility", 0)
        cmds.rename("Armwrist_IK_L_Ctrl", "Armwrist_IK_L_OPR")
        cmds.setAttr("Armwrist_IK_L_OPRShape.visibility", 0)
        cmds.rename("Armwrist_IK_R_Ctrl", "Armwrist_IK_R_OPR")
        cmds.setAttr("Armwrist_IK_R_OPRShape.visibility", 0)        
        allControllers=cmds.ls("*_Ctrl")
        for each in allControllers:
            if "spine" in each:     
                if "FK" in each:
                    clnName=each.replace("guide", '')
                    splitCentric=clnName.split("_") 
                    splitCentric[0]=str.capitalize(str(splitCentric[0]))
                    splitNum= re.split(r'(\d+)',splitCentric[0])
                    if '' in splitNum:
                        splitNum.remove('')
                    for part in splitCentric[1:]:
                        capPart=str.capitalize(str(part))
                        splitNum.append(capPart)                             
                else:       
                    lnName=each.replace("clst", 'IK')        
                    splitCentric=lnName.split("_")
                    splitCentric[0]=str.capitalize(str(splitCentric[0]))
                    splitNum= re.split(r'(\d+)',splitCentric[0])
                    Kinetic=', '.join(splitCentric[1:2])
                    splitNum.append(Kinetic)                         
                    if '' in splitNum:
                        splitNum.remove('')
                    for part in splitCentric[-1:]:
                        capPart=str.capitalize(str(part))
                        splitNum.append(capPart)
                newCentric='_'.join(splitNum )                      
                cmds.rename(each, newCentric)                 
#         getik=["foottoeRight_ik", "foottoeLeft_ik"]
#         for each in getik:
#             cmds.delete(each)
#             
        #build Controller Groups
        cmds.delete("foottoeLeft_ik_poleVectorConstraint1")
        cmds.delete("foottoeRight_ik_poleVectorConstraint1")
        

        #maya.mel.eval("cleanUpScene 1")
        
        cams=["persp", "top", "front", "side"]
        collectForGroup=["transform","joint", "ikHandle" ]
        groupItems=[(each) for each in cmds.ls("*") for item in collectForGroup for cam in cams if cmds.listRelatives(each, ap=1) == None and cmds.nodeType(each)== item and each not in cams]
        cmds.select(groupItems)
        cmds.group(n="Rig")
        
        cullControllers=["EyeMask_Offset_Ctrl","Armwrist_L_IK_Ctrl", "Armwrist_R_IK_Ctrl", "Chin_Ctrl", "EyeMask_Ctrl", "EyeOrient_L_Ctrl", "EyeOrient_R_Ctrl", "BottomLid_R_Ctrl", "BottomLid_L_Ctrl", "TopLid_R_Ctrl", "TopLid_L_Ctrl"]
        removeFromControllers=("knuckle")
        getControllerSets=[(each) for each in cmds.ls("*_Ctrl") for item in removeFromControllers if cmds.nodeType(each)=="transform" and item not in each and each not in cullControllers ]
        cmds.sets(getControllerSets, n="BodyControllers")   
        
        getFaceControllerSets=["EyeMask_Offset_Ctrl", "Chin_Ctrl", "EyeMask_Ctrl", "EyeOrient_L_Ctrl", "EyeOrient_R_Ctrl", "BottomLid_R_Ctrl", "BottomLid_L_Ctrl", "TopLid_R_Ctrl", "TopLid_L_Ctrl"]
        cmds.sets(getFaceControllerSets, n="FaceControllers")   

        bindSpine=[(each) for each in cmds.listRelatives("spine01_jnt", ad=1, typ="joint") if "IK" not in each and "FK" not in each]
        #bindSpine=cmds.ls("spine*_jnt")
        getskinBones=["legLeft_jnt", "legRight_jnt", "armcollarLeftSH_jnt", "armcollarRightSH_jnt", "armshoulderLeft_jnt", "armshoulderRight_jnt", "armhandLeft_jnt", "armhandRight_jnt"]
        bagOfChildrensBones=[]
        for each in getskinBones:
            try:
                getChildren=cmds.listRelatives(each, ad=1, typ="joint")
                for item in getChildren:
                    bagOfChildrensBones.append(item)
            except:
                pass
        Bones=bindSpine+getskinBones+bagOfChildrensBones
        cmds.sets(Bones, n="skinBones")       
        
        getHideCurves=cmds.ls("*_crv")
        for each in getHideCurves:
            cmds.setAttr(each+".visibility", 0)
            
        hideList=("tailMain_Ctrl", "neckMain_Ctrl", "foottalusRight_nod", "foottalusLeft_nod")
        for each in hideList:
            try:
                getShapes=[(each) for each in cmds.listRelatives(each, typ="shape") if "lctr" not in each]
                for shape in getShapes:
                        cmds.setAttr(shape+".visibility", 0)                
            except:
                pass                



        lockOffAttributes=[]
        getTail=cmds.ls("tail*Ctrl")
        for item in getTail:
            lockOffAttributes.append(item)
            cmds.setAttr(str(item)+".sx" , keyable=0, lock=1)
            cmds.setAttr(str(item)+".sy" , keyable=0, lock=1)
            cmds.setAttr(str(item)+".sz", keyable=0, lock=1)             
        lockOffAttributes=["Shoulder_R_Ctrl", "Wrist_R_Ctrl","Ball_R_Ctrl", "Shoulder_L_Ctrl", "Wrist_L_Ctrl","Ball_L_Ctrl","Hand_L_Ctrl", "Hand_R_Ctrl", "Neck_Ctrl"]
        for each in lockOffAttributes:
            cmds.setAttr(each+".tx" , k=0, cb=0)
            cmds.setAttr(each+".ty" , k=0, cb=0)
            cmds.setAttr(each+".tz", k=0, cb=0) 
            
        lockOffAttributes=["Hand_L_Ctrl", "Hand_R_Ctrl"]          
        for each in lockOffAttributes:
            cmds.setAttr(each+".rx" , k=0, cb=0)
            cmds.setAttr(each+".ry" , k=0, cb=0)
            cmds.setAttr(each+".rz", k=0, cb=0) 

   
        cmds.setAttr("EyeMask_Offset_Ctrl.sx"  , k=0, cb=0)
        cmds.setAttr("EyeMask_Offset_Ctrl.sy" , k=0, cb=0)
        cmds.setAttr("EyeMask_Offset_Ctrl.sz" , k=0, cb=0)
        allControllers=cmds.ls("*_Ctrl")
        for each in allControllers:
            #cmds.setAttr(str(each)+".visibility" , keyable=0, cb=0)            
            cmds.setAttr(str(each)+".sx" , keyable=0, lock=1)
            cmds.setAttr(str(each)+".sy" , keyable=0, lock=1)
            cmds.setAttr(str(each)+".sz", keyable=0, lock=1)            
            
        getnods=[(each) for each in cmds.ls("*nod") if "grp" not in each]
        for each in getnods:
            try:
                getClass.buildGrp(each)
            except:
                pass    
        self.updates()

    def updates(self):
        getClass.sandwichAuto("Chin_Ctrl", "_SDK", 22, 1)
        getObject="Chin_SDK_Ctrl"
        getChildShape=cmds.listRelatives(getObject, c=1, typ="shape")
        cmds.setAttr(getChildShape[0]+".visibility", 0)
        lognm=getObject.replace('_Ctrl', "")
        cmds.rename(getObject, lognm)          
        
        
        #current requests and fixes to the rig
        cmds.parent("head01_jnt", w=1)
        cmds.delete("head01_grp_parentConstraint1")
        cmds.orientConstraint("UpperBody_Ctrl", "head01_grp", mo=1)
        trans, rot=getClass.locationXForm("head01_jnt")
        cmds.joint(n="neck02_jnt", p=trans)
        cmds.parent("neck02_jnt", "neck01_jnt")
        cmds.pointConstraint("neck02_jnt", "head01_grp", mo=1)
        cmds.parent("head01_jnt", "Rig")

        getAllCtrl=cmds.ls("*_Ctrl")
        for each in getAllCtrl:
            try:
                cmds.setAttr(each+".Stretch", 1)
            except:
                pass
        cmds.setAttr("Hips_Ctrl.StretchSpine", 1)
        
        footSides=("Left", "Right")
        for each in footSides:
            item="football"+each+"_jnt"
            trans, rot=getClass.locationXForm(item)
            cmds.parent(item, w=1)
            cmds.select(cl=1)
            jntName=item.split("_jnt")[0]+"RT_jnt"
            getClass.rigJointnames(item, jntName)
            cmds.parent(item, jntName)
            cmds.parent(jntName, "footankle"+each+"_jnt")
            if "Left" in each:    
                cmds.disconnectAttr("Footheel_IK_L_Ctrl.RaiseToe","footballLeft_jnt.rotateZ")
                cmds.connectAttr("Footheel_IK_L_Ctrl.RaiseToe","footballLeftRT_jnt.rotateX", f=1)
            if "Right" in each:
                cmds.disconnectAttr("Footheel_IK_R_Ctrl.RaiseToe","footballRight_jnt.rotateZ")
                cmds.connectAttr("Footheel_IK_R_Ctrl.RaiseToe","footballRightRT_jnt.rotateX", f=1)   
                
        hideObjects=("BottomLid_L_Ctrl", "BottomLid_R_Ctrl", "TopLid_R_Ctrl", "TopLid_L_Ctrl", "armshoulderLeftIK_jnt_edloc", "armshoulderLeftIK_jnt_bdloc", "armshoulderRightIK_jnt_bdloc", "armshoulderRightIK_jnt_edloc", "spineIK_crv", )
        for each in hideObjects:
            cmds.setAttr(each+".visibility", 0)
        try:
            cmds.setAttr("tailIK_crv.visibility", 0)
        except:
            pass          
        lockHideObjects=('armshoulderLeftIK_jnt_bdloc','armshoulderRightIK_jnt_bdloc','leghipLeftIK_jnt_bdloc','leghipRightIK_jnt_bdloc','armshoulderLeftIK_jnt_edloc','armshoulderRightIK_jnt_edloc','leghipLeftIK_jnt_edloc','leghipRightIK_jnt_edloc')
        for each in lockHideObjects:
            cmds.setAttr(each+".tx" , k=0, cb=0)
            cmds.setAttr(each+".ty" , k=0, cb=0)
            cmds.setAttr(each+".tz", k=0, cb=0)  
            cmds.setAttr(each+".rx" , k=0, cb=0)
            cmds.setAttr(each+".ry" , k=0, cb=0)
            cmds.setAttr(each+".rz", k=0, cb=0)  
            cmds.setAttr(each+".sx" , k=0, cb=0)
            cmds.setAttr(each+".sy" , k=0, cb=0)
            cmds.setAttr(each+".sz", k=0, cb=0)


        cmds.showHidden("armwristRight_jnt_ikPole_lctr", a=1)
        cmds.showHidden("armwristLeft_jnt_ikPole_lctr", a=1)
        
        hideList=("Armwrist_IK_L_Ctrl", "Armwrist_IK_R_Ctrl")
        for each in hideList:
            try:
                getShapes=[(each) for each in cmds.listRelatives(each, typ="shape") if "lctr" not in each]
                for shape in getShapes:
                        cmds.setAttr(shape+".visibility", 0)                
            except:
                pass  
        cmds.addAttr("Armhand_IK_R_Ctrl", ln="ExtraPoleControl", at="enum",en="off:on:", k=1, nn="ExtraPoleControl")
        cmds.addAttr("Armhand_IK_L_Ctrl", ln="ExtraPoleControl", at="enum",en="off:on:", k=1, nn="ExtraPoleControl")
        
        cmds.connectAttr("Armhand_IK_L_Ctrl.ExtraPoleControl", "armwristLeft_jnt_ikPole_lctr.visibility")
        cmds.connectAttr("Armhand_IK_R_Ctrl.ExtraPoleControl", "armwristRight_jnt_ikPole_lctr.visibility")
        cmds.setAttr("armwristRight_jnt_ikPole_lctr.ty", k=0, cb=0)
        cmds.setAttr("armwristRight_jnt_ikPole_lctr.rx", k=0, cb=0)
        cmds.setAttr("armwristRight_jnt_ikPole_lctr.ry", k=0, cb=0)
        cmds.setAttr("armwristRight_jnt_ikPole_lctr.rz", k=0, cb=0)
        cmds.setAttr("armwristRight_jnt_ikPole_lctr.sx", k=0, cb=0)
        cmds.setAttr("armwristRight_jnt_ikPole_lctr.sy", k=0, cb=0)
        cmds.setAttr("armwristRight_jnt_ikPole_lctr.sz", k=0, cb=0)
        cmds.setAttr("armwristRight_jnt_ikPole_lctr.visibility", lock=1)
        
        cmds.setAttr("armwristLeft_jnt_ikPole_lctr.ty", k=0, cb=0)
        cmds.setAttr("armwristLeft_jnt_ikPole_lctr.rx", k=0, cb=0)
        cmds.setAttr("armwristLeft_jnt_ikPole_lctr.ry", k=0, cb=0)
        cmds.setAttr("armwristLeft_jnt_ikPole_lctr.rz", k=0, cb=0)
        cmds.setAttr("armwristLeft_jnt_ikPole_lctr.sx", k=0, cb=0)
        cmds.setAttr("armwristLeft_jnt_ikPole_lctr.sy", k=0, cb=0)
        cmds.setAttr("armwristLeft_jnt_ikPole_lctr.sz", k=0, cb=0)
        cmds.setAttr("armwristLeft_jnt_ikPole_lctr.visibility", lock=1) 
        
        #new arm IK layout
        try:
            cmds.delete("armwristLeft_offset_IK_ctrl_parentConstraint1")
        except:
            pass
        try:
            cmds.delete("armwristRight_offset_IK_ctrl_parentConstraint1")
        except:
            pass
        cmds.parentConstraint("Armhand_IK_R_Ctrl", "armwristRight_offset_IK_grp", mo=1)
        cmds.parentConstraint("Armhand_IK_L_Ctrl", "armwristLeft_offset_IK_grp", mo=1)
         
        cmds.parent("armwristLeftIK_grp", "Armcollar_IK_L_Ctrl")
        cmds.parent("armwristRightIK_grp", "Armcollar_IK_R_Ctrl")
        cmds.delete("EyeMask_Offset_Ctrl_parentConstraint1")
        cmds.parentConstraint("Head_Ctrl", "EyeMask_Offset_grp", mo=1)        

        transforms =  cmds.ls(type='transform')
        deleteList = []
        for tran in transforms:
            if cmds.nodeType(tran) == 'transform':
                children = cmds.listRelatives(tran, c=True) 
                if children == None:
                    deleteList.append(tran)  
        cmds.delete(deleteList)

        getSel=("armwristLeft_jnt_ikPole_lctr",
        "armelbowLeft_jnt_ikPole_lctr",
        "armelbowRight_jnt_ikPole_lctr",
        "armwristRight_jnt_ikPole_lctr")
        for each in getSel:
            cmds.sets(each, include="BodyControllers")
            lognm=each.replace("_lctr", '_Ctrl')
            getnewname=lognm.replace("_jnt", "")
            getcleanname=getnewname.replace("ikPole", "PoleVector")
            getFullName=getcleanname.replace("arm", "")
            #capitalString=getFullName.capitalize()
            if "Right" in each:
                getPartname=getFullName.replace("Right", "_R")
            else:
                getPartname=getFullName.replace("Left", "_L")
            print getPartname
            cmds.rename(each, getPartname)      

        thumbGrp=cmds.ls("*thumb*_guide")
        cmds.delete(thumbGrp)


        Sides=["_L_", "_R_"]
        fullSides=["Left", "Right"]
        for eachside, eachFullside in map(None, Sides, fullSides):
            cmds.parent("armhand"+eachFullside+"IK_grp", w=1)
            cmds.parentConstraint("Armcollar_IK"+eachside+"Ctrl", "armhand"+eachFullside+"IK_grp", mo=1)
            cmds.parentConstraint("Main_Ctrl", "armhand"+eachFullside+"IK_grp", mo=1)
            #cmds.addAttr("Armhand_IK"+eachside+"Ctrl", ln="ArmFollow", min=0, max=1, at="double", k=1, nn="ArmFollow")
            cmds.addAttr("Armhand_IK"+eachside+"Ctrl", ln="ArmFollow", at="enum", en="on:World:Main:", k=1, nn="ArmFollow")
            cmds.setAttr("Armhand_IK"+eachside+"Ctrl.ArmFollow", 0)
            cmds.setAttr("armhand"+eachFullside+"IK_grp_parentConstraint1.Armcollar_IK"+eachside+"CtrlW0", 1)
            cmds.setAttr("armhand"+eachFullside+"IK_grp_parentConstraint1.Main_CtrlW1", 0)
            cmds.setDrivenKeyframe("armhand"+eachFullside+"IK_grp_parentConstraint1", cd="Armhand_IK"+eachside+"Ctrl.ArmFollow")
            cmds.setAttr("Armhand_IK"+eachside+"Ctrl.ArmFollow", 1)
            cmds.setAttr("armhand"+eachFullside+"IK_grp_parentConstraint1.Armcollar_IK"+eachside+"CtrlW0", 0)
            cmds.setAttr("armhand"+eachFullside+"IK_grp_parentConstraint1.Main_CtrlW1", 0)
            cmds.setDrivenKeyframe("armhand"+eachFullside+"IK_grp_parentConstraint1", cd="Armhand_IK"+eachside+"Ctrl.ArmFollow")  
            cmds.setAttr("Armhand_IK"+eachside+"Ctrl.ArmFollow", 2)
            cmds.setAttr("armhand"+eachFullside+"IK_grp_parentConstraint1.Armcollar_IK"+eachside+"CtrlW0", 0)
            cmds.setAttr("armhand"+eachFullside+"IK_grp_parentConstraint1.Main_CtrlW1", 1)
            cmds.setDrivenKeyframe("armhand"+eachFullside+"IK_grp_parentConstraint1", cd="Armhand_IK"+eachside+"Ctrl.ArmFollow")  
            cmds.setAttr("Armhand_IK"+eachside+"Ctrl.ArmFollow", 0)    
        cmds.parent("armhandLeftIK_grp","Rig")
        cmds.parent("armhandRightIK_grp","Rig")
            
            
        cmds.addAttr("Main_Ctrl", ln="WaistFollow", min=0, max=1, at="double", k=1, nn="WaistFollow")
        cmds.connectAttr("Main_Ctrl.WaistFollow","WaistFollow_CtrlShape.visibility")
        cmds.connectAttr("Main_Ctrl.WaistFollow","WaistFollow_offset_CtrlShape.visibility")      

#         Sides=["_L_", "_R_"]
#         fullSides=["Left", "Right"]
#         for eachside, eachFullside in map(None, Sides, fullSides):
#             cmds.parent("armhand"+eachFullside+"IK_grp", w=1)
#             cmds.parentConstraint("Armcollar_IK"+eachside+"Ctrl", "armhand"+eachFullside+"IK_grp", mo=1)
#             cmds.addAttr("Armhand_IK"+eachside+"Ctrl", ln="ArmFollow", min=0, max=1, at="double", k=1, nn="ArmFollow")
#             cmds.setAttr("Armhand_IK"+eachside+"Ctrl.ArmFollow", 1)
#             cmds.setAttr("armhand"+eachFullside+"IK_grp_parentConstraint1.Armcollar_IK"+eachside+"CtrlW0", 1)
#             cmds.setDrivenKeyframe("armhand"+eachFullside+"IK_grp_parentConstraint1", cd="Armhand_IK"+eachside+"Ctrl.ArmFollow")
#             cmds.setAttr("Armhand_IK"+eachside+"Ctrl.ArmFollow", 0)
#             cmds.setAttr("armhand"+eachFullside+"IK_grp_parentConstraint1.Armcollar_IK"+eachside+"CtrlW0", 0)
#             cmds.setDrivenKeyframe("armhand"+eachFullside+"IK_grp_parentConstraint1", cd="Armhand_IK"+eachside+"Ctrl.ArmFollow")
#             cmds.setAttr("Armhand_IK"+eachside+"Ctrl.ArmFollow", 1)
#             cmds.setAttr("armhand"+eachFullside+"IK_grp_parentConstraint1.Armcollar_IK"+eachside+"CtrlW0", lock=1)   
#             cmds.setAttr("Armwrist_offset_IK"+eachside+"CtrlShape.visibility", 0) 
#             
#     cmds.setAttr("Armhand_IK"+eachside+"Ctrl.ArmFollow", 2)
#             
#             
#         cmds.addAttr("EyeMask_Ctrl", ln="HeadFollow", min=0, max=1, at="double", k=1, nn="HeadFollow")
#         cmds.setAttr("EyeMask_Ctrl.HeadFollow", 1)
#         cmds.setAttr("EyeMask_Offset_grp_parentConstraint1.Head_CtrlW0", 1)
#         cmds.setDrivenKeyframe("EyeMask_Offset_grp_parentConstraint1", cd="EyeMask_Ctrl.HeadFollow")
#         cmds.setAttr("EyeMask_Ctrl.HeadFollow", 0)
#         cmds.setAttr("EyeMask_Offset_grp_parentConstraint1.Head_CtrlW0", 0)
#         cmds.setDrivenKeyframe("EyeMask_Offset_grp_parentConstraint1", cd="EyeMask_Ctrl.HeadFollow")
#         cmds.setAttr("EyeMask_Ctrl.HeadFollow", 1)
#         cmds.setAttr("EyeMask_Offset_grp_parentConstraint1.Head_CtrlW0", lock=1)       

        Side=["R", "L"]
        for eachSide in Side:
            startEyeJoint=["Eye_"+eachSide+"_jnt"]
            IKEyelist=["EyeOrient_"+eachSide+"_jnt"]
            for each, item in map(None, IKEyelist, startEyeJoint):
                try:
                    cmds.delete("Eye_"+eachSide+"_jnt_aimConstraint1")
                    cmds.ikHandle(n=each+"_ik", sj=item, ee=each, sol="ikRPsolver")
                    cmds.setAttr(each+"_ik.visibility", 0)
                    cmds.parent(each+"_ik", "EyeOrient_"+eachSide+"_Ctrl")   
                except:
                    pass
        Side=["Right", "Left"]
        for eachSide in Side: 
            getLimb=["legknee"+eachSide]
            IKHandlesLimbsarms=["armelbow"+eachSide,
                                "armwrist"+eachSide]
            for each in IKHandlesLimbsarms:
                getTranslation=cmds.xform(each+"_jnt", q=1, t=1, ws=1)
                name=each+"FK_target"
                grpname=each+"FK_target"+"_grp"
                print grpname
                num=3
                color=22
                if "elbow" in each:
                    getClass.JackI(name, grpname, num, getTranslation, (0.0,0.0,0.0), color)
                    cmds.move( 0.0, 0.0, -10.0,grpname,r=1, rpr=1)     
                    cmds.parent(grpname,each+"FK_jnt")
                    cmds.setAttr(name+".visibility", 0)
                    cmds.makeIdentity(name, a=True, t=1, s=1, r=1, n=0)  
                if "wrist" in each:
                    getClass.JackI(name, grpname, num, getTranslation, (0.0,0.0,0.0), color)
                    cmds.move(0.0, -5.0, 0.0,grpname,r=1, rpr=1)   
                    cmds.parent(grpname,each+"FK_jnt")
                    cmds.setAttr(name+".visibility", 0)
                    cmds.makeIdentity(name, a=True, t=1, s=1, r=1, n=0) 
            for each in getLimb:
                getTranslation=cmds.xform(each+"_jnt", q=1, t=1, ws=1)
                name=each+"FK_target"
                grpname=each+"FK_target"+"_grp"
                print grpname
                num=3
                color=22    
                getTranslation=cmds.xform(each+"_jnt", q=1, t=1, ws=1)
                if "knee" in each:
                    getClass.JackI(name, grpname, num, getTranslation, (0.0,0.0,0.0), color)
                    cmds.move( 0.0, 0.0, +30.0,grpname,r=1, rpr=1)          
                    cmds.parent(grpname,each+"FK_jnt")
                    cmds.setAttr(name+".visibility", 0)
                    cmds.makeIdentity(name, a=True, t=1, s=1, r=1, n=0)                    
        try:
            cmds.addAttr("EyeMask_Ctrl", ln="CheekLeftUp", min=0, max=1, at="double", k=1, nn="CheekLeftUp")
            cmds.addAttr("EyeMask_Ctrl", ln="CheekRightUp", min=0, max=1, at="double", k=1, nn="CheekRightUp")
        except:
            pass    
        cmds.setAttr("Hips_Ctrl.spineFK_IK", 0) 
        selObj=cmds.ls("*Elbow_*_Ctrl")
        for each in selObj:
            cmds.setAttr(each+".rx", cb=1)
            cmds.setAttr(each+".rx", k=1)
            cmds.setAttr(each+".rx", l=0)       
            cmds.setAttr(each+".rotateOrder", 3)
        selObj=cmds.ls("Hand_*_Fingers_Ctrl")
        for each in selObj:
            cmds.addAttr(each+".SpreadFingers", e=1, min=-0, max=90)
            cmds.addAttr(each+".CurlFingers", e=1, min=-160, max=0)            
        selObj=cmds.ls("*_Finger_*_Ctrl")
        for each in selObj:
            if "|" not in each:
                cmds.addAttr(each+".MiddleJoint", e=1, min=-160, max=0)
                cmds.addAttr(each+".LastJoint", e=1, min=-160, max=0)
                cmds.addAttr(each+".FingerFullCurl", e=1, min=-160, max=0)        
        getSel=cmds.ls("leghip*IK_jnt_*loc")  
        for item in getSel:
            for each in trans:
                cmds.setAttr(item+each, k=0)
                cmds.setAttr(item+".visibility", 0)   
                
    def renaming_centric_kenetic(self, each, bodyPart, Kinetic):
        cullKinetic=each.split(Kinetic)
        cullCentric=cullKinetic[0].replace(bodyPart, '')  
        ctrllr_nm=cullKinetic[1].split("_")
        splitCentric= re.split(r'([A-Z][a-z]*)', cullKinetic[0])
        splitCentric[0]=str.capitalize(str(splitCentric[0]))
        ctrllr_nm[1]=str.capitalize(str(ctrllr_nm[1]))
        splitCentric.append(Kinetic)
        splitCentric.append(ctrllr_nm[1])
        myBucket=[]                      
        if '' in splitCentric:
            splitCentric.remove('')
        for each in splitCentric:
            if "Left" in each or "Right" in each:
                myBucket.append(each[0])
            else:
                myBucket.append(each)   
        newCentric='_'.join(myBucket)
        return newCentric    
    def renaming_centric_swap(self, each, bodyPart, Kinetic):
        cullKinetic=each.split(Kinetic)
        cullCentric=cullKinetic[0].replace(bodyPart, '')  
        ctrllr_nm=cullKinetic[1].split("_")
        splitCentric= re.split(r'([A-Z][a-z]*)', cullKinetic[0])
        splitCentric[0]=str.capitalize(str(splitCentric[0]))
        ctrllr_nm[1]=str.capitalize(str(ctrllr_nm[1]))
        splitCentric.append(Kinetic)
        splitCentric.append(ctrllr_nm[1])
        myBucket=[]                      
        if '' in splitCentric:
            splitCentric.remove('')
        for each in splitCentric:
            if "Left" in each or "Right" in each:
                myBucket.append(each[0])
            else:
                myBucket.append(each) 
        myBucket[-3:-2], myBucket[-2:-1] = myBucket[-2:-1],myBucket[-3:-2]  
        newCentric='_'.join(myBucket)
        return newCentric
    def renaming_centric(self, each, bodyPart):
        cullCentric=each.replace(bodyPart, '')  
        ctrllr_nm=cullCentric.split("_")
        splitCentric= re.split(r'([A-Z][a-z]*)', ctrllr_nm[0]) 
        splitCentric[0]=str.capitalize(str(splitCentric[0]))
        ctrllr_nm[1]=str.capitalize(str(ctrllr_nm[1]))
        splitCentric.append(ctrllr_nm[1]) 
        myBucket=[]           
        if '' in splitCentric:
            splitCentric.remove('')
        for each in splitCentric:
            if "Left" in each or "Right" in each:
                myBucket.append(each[0])
            else:
                myBucket.append(each)      
        newCentric='_'.join(myBucket)
        return newCentric
    
    def renaming_centric_finger(self, each, bodyPart):
        lognm=each.replace("BaseKnuckle", '_')   
        nlognm=lognm.replace("arm", '')     
        alognm=nlognm.replace("Finger", '_Finger')  
        unicodedata.normalize('NFKD', alognm).encode('ascii','ignore')
        getpiece=alognm.split('_')
        bucket=[]
        for part in getpiece:
            capitalString=str.capitalize(str(part))
            bucket.append(capitalString)
        bucket=self.swapCentricSuf(bucket)
        newName='_'.join(bucket)
        return newName

    def swapCentricSuf(self,splitCentric):
        splitCentric[-1:], splitCentric[-2:-1] = splitCentric[-2:-1], splitCentric[-1:]
        splitCentric[-1:]=str(splitCentric[-1:])[2] 
        return splitCentric
    
    
    
