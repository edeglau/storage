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

filepath= os.getcwd()
sys.path.append(str(filepath))
import baseFunctions_maya
reload (baseFunctions_maya)
getClass=baseFunctions_maya.BaseClass()



class cln(object):
    def __init__(self):
        ########
        #Lock and hide scales
        ########           
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
#                 else:
#                     newCentric=self.renaming_centric(each, bodyPart) 
#                     cmds.rename(each, newCentric)
  
            if "foot" in each:
                bodyPart="foot"
                if "IK" in each:
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

                        
#             getJointsToHide=cmds.ls("*IK*", typ="joint")
#             for each in getJointsToHide:
#                 if "arm" not in each:
#                     cmds.setAttr(each+".visibility", 0)
#                 
#             getJointsToHide=cmds.ls("*FK*", typ="joint")
#             for each in getJointsToHide:
#                 cmds.setAttr(each+".visibility", 0)    
#             
#             getJointsToHide=cmds.ls(typ="ikHandle")
#             for each in getJointsToHide:
#                 cmds.setAttr(each+".visibility", 0) 
#                 
#             getJointsToHide=cmds.ls("*RFL*", typ="joint")
#             for each in getJointsToHide:
#                 cmds.setAttr(each+".visibility", 0)    
#                 
#             getJointsToHide=cmds.ls("*Clst*", typ="joint")
#             for each in getJointsToHide:
#                 cmds.setAttr(each+".visibility", 0) 
            

                
            try:
                cmds.delete("Guides_*_grp")
                cmds.delete("armcollarLeft_jnt")
                cmds.delete("armcollarRight_jnt")
                cmds.delete("heel*_lctr")
                cmds.delete("ankle*_lctr")
                cmds.delete("toe*_lctr")
                
            except:
                pass    

            
            getJointsToHide=cmds.ls("*dis*")
            for each in getJointsToHide:
                cmds.setAttr(each+".visibility", 0)
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
            
        #build Controller Groups

          

#         maya.mel.eval("cleanUpScene 1")
        
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

#old
#         bindSpine=[(each) for each in cmds.listRelatives("spine01_jnt", ad=1, typ="joint") if "IK" not in each and "FK" not in each]
        try: 
            tailbones=[(each) for each in cmds.listRelatives("tail01_jnt", ad=1, typ="joint") if "IK" not in each and "FK" not in each]
        except:
            pass
#         #bindSpine=cmds.ls("spine*_jnt")
        getfootBones=[
                      "anklefrontLeft_jnt", 
                      "anklefrontRight_jnt",
                      "anklerearLeft_jnt",
                      "anklerearRight_jnt"
                      ]
#         try:
#             Bones=bindSpine+getskinBones+tailbones
#         except:
#             Bones=bindSpine+getskinBones
#         cmds.sets(Bones, n="skinBones")       

        bindSpine=[(each) for each in cmds.listRelatives("spine01_jnt", ad=1, typ="joint") if "IK" not in each and "FK" not in each]
        #bindSpine=cmds.ls("spine*_jnt")
        getskinBones=["legLeft_jnt", "legRight_jnt", "armcollarLeftSH_jnt", "armcollarRightSH_jnt", "armshoulderLeft_jnt", "armshoulderRight_jnt"]
        bagOfChildrensBones=[]
        for each in getskinBones:
            getChildren=cmds.listRelatives(each, ad=1, typ="joint")
            for item in getChildren:
                bagOfChildrensBones.append(item)
        Bones=bindSpine+getskinBones+bagOfChildrensBones+tailbones
        cmds.sets(Bones, n="skinBones") 


        hideList=("Basetail_Ctrl", "Baseneck_Ctrl", "tailMain_Ctrl", "neckMain_Ctrl")
        for each in hideList:
            try:
                getShapes=[(each) for each in cmds.listRelatives(each, typ="shape")]
                cmds.setAttr(getShapes+".visibility", 0)
            except:
                pass                

        turnoffstretch=cmds.ls("*Ctrl")
        for each in turnoffstretch:
            try:
                cmds.setAttr(str(each)+".Strech*" , 0)
            except:
                pass
            
        try:
            lockOffAttributes=["neckMain_Ctrl"]
            for each in lockOffAttributes:
                cmds.setAttr(each+".tx" , k=0, cb=0)
                cmds.setAttr(each+".ty" , k=0, cb=0)
                cmds.setAttr(each+".tz", k=0, cb=0) 
                
            lockOffAttributes=["neckMain_Ctrl"]          
            for each in lockOffAttributes:
                cmds.setAttr(each+".rx" , k=0, cb=0)
                cmds.setAttr(each+".ry" , k=0, cb=0)
                cmds.setAttr(each+".rz", k=0, cb=0)             
        except:
            pass


            
        lockOffAttributes=[]
        getTail=cmds.ls("tail*Ctrl")
        for item in getTail:
            lockOffAttributes.append(item)
            cmds.setAttr(str(item)+".sx" , keyable=0, lock=1)
            cmds.setAttr(str(item)+".sy" , keyable=0, lock=1)
            cmds.setAttr(str(item)+".sz", keyable=0, lock=1)             
        lockOffAttributes=["Shoulder_R_Ctrl", "Wrist_R_Ctrl","Shoulder_L_Ctrl", "Wrist_L_Ctrl"]
        for each in lockOffAttributes:
            cmds.setAttr(each+".tx" , k=0, cb=0)
            cmds.setAttr(each+".ty" , k=0, cb=0)
            cmds.setAttr(each+".tz", k=0, cb=0) 

              
        cmds.setAttr("EyeMask_Offset_Ctrl.sx", keyable=0, cb=0)
        cmds.setAttr("EyeMask_Offset_Ctrl.sy", keyable=0, cb=0)
        cmds.setAttr("EyeMask_Offset_Ctrl.sz", keyable=0, cb=0)
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
            
        cmds.setAttr("Chest_IK_Ctrl.visibility" , lock=0)
        cmds.setAttr("Chest_IK_Ctrl.visibility" , lock=0)
        cmds.setAttr("Chest_FK_Ctrl.visibility" , lock=0)
        gethidelist=("Chest_IK_Ctrl", "Chest_FK_Ctrl" )
        for each in gethidelist:
            cmds.pickWalk(d="down")
            getshape=cmds.ls(sl=1)
            cmds.setAttr(getshape[0]+".visibility", 0)
        self.updates()
    def updates(self):
        if cmds.ls("Chin_SDK_Ctrl"):
            pass     
        else:
            getClass.sandwichAuto("Chin_Ctrl", "_SDK", 22, 1)        
            getObject=cmds.ls("Chin_SDK_Ctrl")[0]
            getChildShape=cmds.listRelatives(getObject, c=1, typ="shape")
            cmds.setAttr(getChildShape[0]+".visibility", 0)
            lognm=getObject.replace('_Ctrl', "")
            cmds.rename(getObject, lognm)          
        
        
        #steady head update  
        cmds.parent("head01_jnt", w=1)
        cmds.delete("head01_grp_parentConstraint1")
        cmds.orientConstraint("LowerBody_Ctrl", "head01_grp", mo=1)
        trans, rot=getClass.locationXForm("head01_jnt")
        #cmds.joint(n="neck02_jnt", p=trans)
        if cmds.ls("neck01_jnt"):
            getNeckFirstJoint=cmds.ls("neck01_jnt")[0]
            childBones=[(each) for each in cmds.listRelatives(getNeckFirstJoint, ad=1, typ="joint") if "neck" in each]#get all child bones
        getLastNeckBone=childBones[0]     
        try:     
            cmds.parent("neck02_jnt", "neck01_jnt")
        except:
            pass
        cmds.pointConstraint(getLastNeckBone, "head01_grp", mo=1)
        cmds.parent("head01_jnt", "Rig")
        
        #clean empty transforms
        transforms =  cmds.ls(type='transform')
        deleteList = []
        for tran in transforms:
            if cmds.nodeType(tran) == 'transform':
                children = cmds.listRelatives(tran, c=True) 
                if children == None:
                    deleteList.append(tran)  
        cmds.delete(deleteList)
        
        #turn off stretch
        getAllCtrl=cmds.ls("*_Ctrl")
        for each in getAllCtrl:
            try:
                cmds.setAttr(each+".Stretch", 1)
            except:
                pass
        cmds.setAttr("Hips_Ctrl.StretchSpine", 1)
        try:
            cmds.setAttr("Basetail_Ctrl.Stretchtail", 1)
        except:
            pass
        
        #rename pole ctrls
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
        
        #remove obsolete locators
        getemptylocs=cmds.ls("toe*_lctr")
        for each in getemptylocs:
            cmds.delete(each)
        getemptylocs=cmds.ls("heel*_lctr")
        for each in getemptylocs:
            cmds.delete(each)
        getemptylocs=cmds.ls("ankle*_lctr")
        for each in getemptylocs:
            cmds.delete(each)
        
        getemptylocs=cmds.ls("*dloc")
        for each in getemptylocs:
            cmds.setAttr(each+".visibility", 0)
#         getemptylocs=cmds.ls("*FK_jnt")
#         for each in getemptylocs:
#             cmds.setAttr(each+".visibility", 0)
        getemptylocs=cmds.ls("*IK_jnt")
        for each in getemptylocs:
            cmds.setAttr(each+".visibility", 0)
        getemptylocs=cmds.ls("*_crv")
        for each in getemptylocs:
            cmds.setAttr(each+".visibility", 0)            
        getemptylocs=cmds.ls(type="ikHandle")
        for each in getemptylocs:
            cmds.setAttr(each+".visibility", 0)    
        try:
            getTailmain= cmds.ls("tailMain_Ctrl")
            getShape=cmds.listRelatives(getTailmain[0], typ="shape")
            cmds.setAttr(getShape[0]+".visibility", 0)       
        except:
            pass
        hideObjects=("BottomLid_L_Ctrl", "BottomLid_R_Ctrl", "TopLid_R_Ctrl", "TopLid_L_Ctrl")
        for each in hideObjects:
            getShape=cmds.listRelatives(each, typ="shape")
            cmds.setAttr(getShape[0]+".visibility", 0)          
#         cmds.parent("heelfrontRightIK_grp", "toefrontRight_Tip_ik_loc_lctr")
#         cmds.parent("heelfrontLeftIK_grp", "toefrontLeft_Tip_ik_loc_lctr")
#         cmds.parent("heelrearRightIK_grp", "toerearRight_Tip_ik_loc_lctr")
#         cmds.parent("heelrearLeftIK_grp", "toerearLeft_Tip_ik_loc_lctr")
#         getToeGrp=["toefrontRight_Tip_ik_loc_lctr", "toefrontLeft_Tip_ik_loc_lctr", "toerearRight_Tip_ik_loc_lctr", "toerearLeft_Tip_ik_loc_lctr"]
#         for each in getToeGrp:
#             cmds.parent(each+"_grp", "Main_Ctrl")
#         Side=["Right", "Left"]
#         DepthDimension=["front", "rear"]
#         for eachSide in Side:
#             for eachDim in DepthDimension:
#                 cmds.connectAttr ("heel"+eachDim+eachSide+"IK_ctrl.RaiseHeel", "toe"+eachDim+eachSide+"_Tip_ik_loc_lctr.rotateX", f=1)
#                 cmds.connectAttr ("heel"+eachDim+eachSide+"IK_ctrl.TipToe", "toe"+eachDim+eachSide+"IK_jnt.rotateZ", f=1)

        #centralize controls
        try:
            cmds.connectAttr("Hips_Ctrl.tailFK_IK", "Basetail_Ctrl.tailFK_IK", f=1)
            cmds.addAttr("Hips_Ctrl", ln="StretchTail", at="enum",en="on:off:", k=1, nn="StretchTail")
            cmds.connectAttr("Hips_Ctrl.StretchTail", "Basetail_Ctrl.Stretchtail", f=1)
            cmds.setAttr("Hips_Ctrl.StretchTail", 1)
            cmds.setAttr("Hips_Ctrl.tailFK_IK", 1)
            cmds.setAttr("Basetail_Ctrl.tailFK_IK", l=0, k=0)
            cmds.setAttr("Basetail_Ctrl.Stretchtail", l=0, k=0)
        except:
            print "no tail present, skipping FK/IK hookup to spine"
            pass
 
        getSel=("heelfrontLeftIK_ctrl",
        "heelfrontRightIK_ctrl",
        "heelrearRightIK_ctrl",
        "heelrearLeftIK_ctrl")
        for each in getSel:
            cmds.sets(each, include="BodyControllers")
            lognm=each.replace("_ctrl", '_Ctrl')
            getnewname=lognm.replace("_jnt", "")
            getcleanname=getnewname.replace("ikPole", "PoleVector")
            getFullName=getcleanname.replace("heel", "Heel_")
            #capitalString=getFullName.capitalize()
            if "Right" in each:
                getPartname=getFullName.replace("Right", "_R_")
            else:
                getPartname=getFullName.replace("Left", "_L_")
            print getPartname
            cmds.rename(each, getPartname)    
    
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
    
    def alternate_head_leveller(self):
            cmds.parent("head01_jnt", w=1)
            cmds.orientConstraint("LowerBody_Ctrl", "head01_grp", mo=1)
            trans, rot=getClass.locationXForm("head01_jnt")
            #cmds.joint(n="neck02_jnt", p=trans)
            if cmds.ls("neck01_jnt"):
                getNeckFirstJoint=cmds.ls("neck01_jnt")[0]
                childBones=[(each) for each in cmds.listRelatives(getNeckFirstJoint, ad=1, typ="joint") if "neck" in each]#get all child bones
            getLastNeckBone=childBones[0]     
            try:     
                cmds.parent("neck02_jnt", "neck01_jnt")
            except:
                pass
            cmds.pointConstraint(getLastNeckBone, "head01_grp", mo=1)
            cmds.parent("head01_jnt", "Rig")    
