import maya.cmds as cmds
import maya.mel
from functools import partial
from string import *
import re
import sys

import os, subprocess, sys, platform
from os  import popen
from sys import stdin

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

class faceRig(object):
    def __init__(self):
        #create joints
        Face=[
                "TopLid_R_Ctrl_guide",
                "BottomLid_R_Ctrl_guide"]
        Eyes=["Eye_R_Ctrl_guide", 
                "EyeOrient_R_Ctrl_guide",
                ]
        Jaw=["Jaw_Ctrl_guide", "Chin_Ctrl_guide"]
        #Lids=["TopLid_R_jnt", "BottomLid_R_jnt"]   
        EyeLidTopRight=["Eye_R_Ctrl_guide", "TopLid_R_Ctrl_guide"]  
        EyeLidBottomRight=["Eye_R_Ctrl_guide", "BottomLid_R_Ctrl_guide"]            
        getLimbs=(Face, Eyes)
        cmds.select(cl=1)    
        for item in EyeLidTopRight:
            if "Eye" in item:
                jointnames=item.split("_Ctrl_guide")[0]+"_TBlink_jnt"
            else:
                jointnames=item.split("_Ctrl_guide")[0]+"_jnt"
            getTranslation=cmds.xform(item, q=1, t=1, ws=1)
            cmds.joint(n=jointnames, p=getTranslation)            
        cmds.select(cl=1)
        for item in EyeLidBottomRight:
            if "Eye" in item:            
                jointnames=item.split("_Ctrl_guide")[0]+"_BBlink_jnt"
            else:
                jointnames=item.split("_Ctrl_guide")[0]+"_jnt"            
            getTranslation=cmds.xform(item, q=1, t=1, ws=1)
            cmds.joint(n=jointnames, p=getTranslation)            
        cmds.select(cl=1)
        for each in Eyes:
            getTranslation=cmds.xform(each, q=1, t=1, ws=1)
            jointnames=each.split("_Ctrl_guide")[0]+"_jnt"
            cmds.joint(n=jointnames, p=getTranslation)  
        cmds.select(cl=1)
        for each in Jaw:
            getTranslation=cmds.xform(each, q=1, t=1, ws=1)
            jointnames=each.split("_Ctrl_guide")[0]+"_jnt"
            cmds.joint(n=jointnames, p=getTranslation)  
        cmds.select(cl=1)        
        Lids=["Eye_R_TBlink_jnt", "Eye_R_BBlink_jnt"]
        for each in Lids:
            cmds.mirrorJoint(each, myz=1, sr=("_R_", "_L_"))
        cmds.mirrorJoint("Eye_R_jnt", myz=1, sr=("_R_", "_L_"))
        cmds.joint( "Eye_R_jnt", e=1, children=1, zso=1, oj='xyz', sao='yup', spa=1) 
        cmds.joint( "Eye_L_jnt", e=1, children=1, zso=1, oj='xyz', sao='yup', spa=1)   
        LeftSide=("TopLid_L_jnt", "BottomLid_L_jnt")
        for each in LeftSide:
            cmds.joint(each, e=1, children=1, zso=1, oj='xyz', sao='yup', spa=1)  
            
        #create controllers   
        colour1=18
        colour2=colour1
        colour3=colour1        
        getTranslation, getRotation=getClass.locationXForm("Jaw_jnt") 
        getClass.guideBuild("Jaw_Ctrl_nod", getTranslation, getRotation, colour1, colour2, colour3 )
        getsel=cmds.ls(sl=1)
        cmds.setAttr(getsel[0]+".overrideColor", colour1)
        getClass.buildGrp(getsel[0])

        scaleWorldMatrix = cmds.xform("EyeOrient_R_Ctrl_guide", q=True, r=1, s=True)
        scaleWorldMatrix=int(scaleWorldMatrix[0])   
        eachPiece="EyeOrient_R_jnt"
        name="EyeMask_Ctrl"
        grpname="EyeMask_Ctrl_grp"               
        size=3*scaleWorldMatrix
        colour=17
        nrx=0
        nry=0
        nrz=1   
        getTranslation, getRotation=getClass.locationXForm(eachPiece)        
        getClass.buildCtrl(eachPiece, name, grpname, getTranslation, getRotation, size, colour, nrx, nry, nrz)
        cmds.move(0.0, getTranslation[1], getTranslation[2]+8, grpname) 
        name="EyeMask_Offset_Ctrl"
        grpname="EyeMask_Offset_grp"               
        size=4*scaleWorldMatrix
        colour=23
        nrx=0
        nry=0
        nrz=1   
        getTranslation, getRotation=getClass.locationXForm(eachPiece)        
        getClass.buildCtrl(eachPiece, name, grpname, getTranslation, getRotation, size, colour, nrx, nry, nrz)
        cmds.move(0.0, getTranslation[1], getTranslation[2]+8, grpname)        
#         
        getSingleJoints=Face
        getSingleJoints.append("TopLid_L_jnt")
        getSingleJoints.append("BottomLid_L_jnt" )
        for item in getSingleJoints:
            if "_L_" in item:
                eachPiece=item
                name=item.split("_jnt")[0]+"_Ctrl"
                grpname=item.split("_jnt")[0]+"_grp" 
            else:
                eachPiece=item.split("_Ctrl_guide")[0]+"_jnt"
                name=item.split("_guide")[0]
                grpname=item.split("_Ctrl_guide")[0]+"_grp"
            size=1*scaleWorldMatrix
            colour=13
            nrx=0
            nry=0
            nrz=1
            getTranslation, getRotation=getClass.locationXForm(item)
            getClass.buildCtrl(eachPiece, name, grpname, getTranslation, getRotation, size, colour, nrx, nry, nrz)
            cmds.move(getTranslation[0], getTranslation[1],getTranslation[2]+1, grpname)
            #cmds.parentConstraint(name, eachPiece, mo=1)
            cmds.parent(grpname, "Jaw_Ctrl_nod")
        
        eachPiece="Chin_jnt"
        name="Chin_Ctrl"
        grpname="Chin_grp"               
        size=3*scaleWorldMatrix
        colour=17
        nrx=0
        nry=0
        nrz=1   
        getTranslation, getRotation=getClass.locationXForm(eachPiece)        
        getClass.buildCtrl(eachPiece, name, grpname, getTranslation, getRotation, size, colour, nrx, nry, nrz)
        cmds.move(0.0, getTranslation[1], getTranslation[2]+2, grpname) 
        cmds.ikHandle(n="Chin_ik", sj="Jaw_jnt", ee="Chin_jnt", sol="ikRPsolver")
        cmds.setAttr("Chin_ik.visibility", 0)
        cmds.parent("Chin_ik", "Chin_Ctrl")
        
        
            
        getEyes=["EyeOrient_L_jnt", "EyeOrient_R_jnt"]
        for item in getEyes:
            name=item.split("_jnt")[0]+"_Ctrl"
            grpname=item.split("_jnt")[0]+"_grp"
            size=2*scaleWorldMatrix
            colour=14
            nrx=0
            nry=0
            nrz=1
            getTranslation, getRotation=getClass.locationXForm(item)
            getClass.buildCtrl(item, name, grpname, getTranslation, getRotation, size, colour, nrx, nry, nrz)
            cmds.move(getTranslation[0], getTranslation[1],getTranslation[2]+1, name)
            cmds.makeIdentity(name, a=True, t=1, r=1, s=1, n=0)

        
        getAllForParenting=["Eye_L_TBlink_jnt", "Eye_R_TBlink_jnt", "Eye_L_BBlink_jnt", "Eye_R_BBlink_jnt", "Eye_R_jnt", "Eye_L_jnt", "Jaw_jnt", "Chin_grp"]
        for each in getAllForParenting:
            cmds.parent(each, "Jaw_Ctrl_nod")
    
    
   
        cmds.addAttr("EyeMask_Ctrl", ln="Blink_Left",  min=0, max=1, at="double", dv=0, k=1, nn="Blink_Left")
        cmds.addAttr("EyeMask_Ctrl", ln="Blink_Right",  min=0, max=1, at="double", dv=0, k=1, nn="Blink_Right")


        #div by side for code ease
        Side=["R", "L"]
        
        #add ikhandle to eye targets
        for eachSide in Side:
            
            startEyeJoint=["Eye_"+eachSide+"_jnt"]
            
            IKEyelist=["EyeOrient_"+eachSide+"_jnt"]
            
            for each, item in map(None, IKEyelist, startEyeJoint):
                cmds.ikHandle(n=each+"_ik", sj=item, ee=each, sol="ikRPsolver")
                cmds.setAttr(each+"_ik.visibility", 0)
                cmds.parent(each+"_ik", "EyeOrient_"+eachSide+"_Ctrl")   
#                 cmds.aimConstraint("EyeOrient_"+eachSide+"_Ctrl", item, mo=1)
                cmds.parent("EyeOrient_"+eachSide+"_grp", "EyeMask_Ctrl")      #parent sep targets to main 
                cmds.addAttr("EyeOrient_"+eachSide+"_Ctrl", ln="Wink",  min=0, max=1, at="double", dv=0, k=1, nn="Wink")
            
            startEyeJoint=["Eye_"+eachSide+"_TBlink_jnt"]
            
            IKEyelist=["TopLid_"+eachSide+"_jnt"]
            
            for each, item in map(None, IKEyelist, startEyeJoint):
                cmds.ikHandle(n=each+"_ik", sj=item, ee=each, sol="ikRPsolver")
                cmds.setAttr(each+"_ik.visibility", 0)
                cmds.parent(each+"_ik", "TopLid_"+eachSide+"_Ctrl")       


            startEyeJoint=["Eye_"+eachSide+"_BBlink_jnt"]
            
            IKEyelist=["BottomLid_"+eachSide+"_jnt"]
            
            for each, item in map(None, IKEyelist, startEyeJoint):
                cmds.ikHandle(n=each+"_ik", sj=item, ee=each, sol="ikRPsolver")
                cmds.setAttr(each+"_ik.visibility", 0)
                cmds.parent(each+"_ik", "BottomLid_"+eachSide+"_Ctrl")
            
            # set SDK blinks
            cmds.setAttr("EyeOrient_"+eachSide+"_Ctrl.Wink", 0)     
            cmds.setAttr("TopLid_"+eachSide+"_Ctrl.translateY", 0) 
            cmds.setAttr("BottomLid_"+eachSide+"_Ctrl.translateY", 0)             
            cmds.setDrivenKeyframe("TopLid_"+eachSide+"_Ctrl.translateY", cd="EyeOrient_"+eachSide+"_Ctrl.Wink")
            cmds.setDrivenKeyframe("BottomLid_"+eachSide+"_Ctrl.translateY", cd="EyeOrient_"+eachSide+"_Ctrl.Wink")
            cmds.setAttr("EyeOrient_"+eachSide+"_Ctrl.Wink", 1)  
            cmds.setAttr("BottomLid_"+eachSide+"_Ctrl.translateY", .4)
            cmds.setAttr("TopLid_"+eachSide+"_Ctrl.translateY", -5) 
            cmds.setDrivenKeyframe("TopLid_"+eachSide+"_Ctrl.translateY", cd="EyeOrient_"+eachSide+"_Ctrl.Wink")
            cmds.setDrivenKeyframe("BottomLid_"+eachSide+"_Ctrl.translateY", cd="EyeOrient_"+eachSide+"_Ctrl.Wink")            
            cmds.setAttr("EyeOrient_"+eachSide+"_Ctrl.Wink", 0)        

        #connect winks to blinks on main controller  
        cmds.connectAttr("EyeMask_Ctrl.Blink_Left", "EyeOrient_L_Ctrl.Wink", f=1)
        cmds.connectAttr("EyeMask_Ctrl.Blink_Right", "EyeOrient_R_Ctrl.Wink", f=1)
        cmds.connectAttr("Chin_Ctrl.rotateY", "Chin_ik.translateX")
        cmds.addAttr("EyeMask_Ctrl", ln="CheekLeftUp", min=0, max=1, at="double", k=1, nn="CheekLeftUp")
        cmds.addAttr("EyeMask_Ctrl", ln="CheekRightUp", min=0, max=1, at="double", k=1, nn="CheekRightUp")          

        cmds.addAttr("EyeMask_Ctrl", ln="showLashCtrls", min=0, max=1, at="double", k=1, nn="showLashCtrls")
        cmds.addAttr("EyeMask_Ctrl", ln="RightLidDown", min=0, max=1, at="double", k=1, nn="RightLidDown")
        cmds.addAttr("EyeMask_Ctrl", ln="LeftLidDown", min=0, max=1, at="double", k=1, nn="LeftLidDown")
        cmds.addAttr("EyeMask_Ctrl", ln="RightLidUp", min=0, max=1, at="double", k=1, nn="RightLidUp")
        cmds.addAttr("EyeMask_Ctrl", ln="LeftLidUp", min=0, max=1, at="double", k=1, nn="LeftLidUp")