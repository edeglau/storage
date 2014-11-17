import maya.cmds as cmds
from functools import partial
from string import *
import re
import maya.mel
import os, subprocess, sys, platform
from os  import popen
from sys import stdin
import sys
filepath= os.getcwd()
sys.path.append(str(filepath))
import baseFunctions_maya
reload (baseFunctions_maya)
getClass=baseFunctions_maya.BaseClass()


import stretchIK
reload (stretchIK)
getIKClass=stretchIK.stretchIKClass()

'''MG rigging modules'''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons License'
'http://creativecommons.org/licenses/by-sa/3.0/au/'

class HandRig(object):
    def __init__(self):
        getGuide=cmds.ls("*_guide")
        
        ArmRightList=["armhandRight_guide"]
        pinkyFingerRight=("armpinkyFingerBaseKnuckleRight_guide", 
                          "armpinkyFingerMidKnuckleRight_guide", 
                          "armpinkyFingerEndKnuckleRight_guide", 
                          "armpinkyFingerTipRight_guide")
        ringFingerRight=("armringFingerBaseKnuckleRight_guide", 
                         "armringFingerMidKnuckleRight_guide", 
                         "armringFingerEndKnuckleRight_guide", 
                         "armringFingerTipRight_guide")
        midFingerRight=("armmidFingerBaseKnuckleRight_guide", 
                        "armmidFingerMidKnuckleRight_guide", 
                        "armmidFingerEndKnuckleRight_guide", 
                        "armmidFingerTipRight_guide" )
        indexFingerRight=("armindexFingerBaseKnuckleRight_guide", 
                          "armindexFingerMidKnuckleRight_guide",
                          "armindexFingerEndKnuckleRight_guide", 
                          "armindexFingerTipRight_guide")   
        thumbRight=("armthumbBaseKnuckleRight_guide", 
                    "armthumbMidKnuckleRight_guide", 
                    "armthumbEndKnuckleRight_guide", 
                    "armthumbTipRight_guide")
        cmds.select(cl=1)
        getLimbs=(ArmRightList, pinkyFingerRight, ringFingerRight, midFingerRight, indexFingerRight, thumbRight)                  
        for each in getLimbs:
            for item in each:
                getTranslation=cmds.xform(item, q=1, t=1)
                getName=item.split("_")
                jointnames=str(getName[0]+'_jnt')
                cmds.joint(n=jointnames, p=getTranslation)
            cmds.select(cl=1) 
        cmds.select(cl=1)
        Side="Right"
        otherSide="Left"
        for each in thumbRight:
            getClass.mirrorObject_callup(each, Side, otherSide)
          
        cmds.parent("armindexFingerBaseKnuckleRight_jnt", "armhandRight_jnt")
        cmds.parent("armmidFingerBaseKnuckleRight_jnt", "armhandRight_jnt")
        cmds.parent("armringFingerBaseKnuckleRight_jnt", "armhandRight_jnt")
        cmds.parent("armpinkyFingerBaseKnuckleRight_jnt", "armhandRight_jnt")
        cmds.parent("armthumbBaseKnuckleRight_jnt", "armhandRight_jnt")
        
        
        cmds.mirrorJoint("armhandRight_jnt", myz=1, sr=("Right", "Left"))
        
        
        resetOrient=[
                     "armhandRight_jnt",
                     "armhandLeft_jnt"
                    ]
        for each in resetOrient:
            cmds.joint( each, e=1, children=1, zso=1, oj='xyz', sao='yup', spa=1)   
        cmds.select(cl=1)
        

        #Controllers
        translations=[".tx", ".ty", ".tz"] 
        rotation=[".rx", ".ry", ".rz"]
        Side=["Right", "Left"]
        
        for eachSide in Side:
            jointGroup=[
                        "armthumbBaseKnuckle"+eachSide,              
                        "armthumbMidKnuckle"+eachSide,
                        "armhand"+eachSide, 
                        "armindexFingerBaseKnuckle"+eachSide, 
                        "armmidFingerBaseKnuckle"+eachSide, 
                        "armringFingerBaseKnuckle"+eachSide, 
                        "armpinkyFingerBaseKnuckle"+eachSide,          
                        ]
            
            
            cmds.group( em=True, name='IK_grp' )
            
            for eachjoint in jointGroup:
                scaleWorldMatrix = cmds.xform(eachjoint.split(eachSide)[0]+"Right_guide", q=True, r=1, s=True)
                scaleWorldMatrix=int(scaleWorldMatrix[0])                  
                eachPiece=eachjoint+"_jnt"
                eachPart=eachjoint+"_guide"
                name=eachjoint+"_ctrl"
                grpname=eachjoint+"_grp"
                getTranslation, getRotation=getClass.locationXForm(eachPiece)   
                getRotation=[0.0, 0.0, 0.0]                
                if "hand" in eachjoint:
                    size=5*scaleWorldMatrix
                    name=eachjoint+"_ctrl"
                    grpname=eachjoint+"_grp"
                    colour=6   
                    nrx=1
                    nry=0
                    nrz=0
                    cmds.select(cl=1) 
                    getClass.buildCtrl(each, name, grpname, getTranslation, getRotation, size, colour, nrx, nry, nrz)        
#                     if "Right" in eachjoint:                                  
#                         cmds.rotate(180, 180, 180, grpname, ws=1)       
                    getShapes=cmds.listRelatives(name, typ="shape")
                    cmds.setAttr(getShapes[0]+".visibility", 0)
                    size=5*scaleWorldMatrix
                    name=eachjoint+"_fingers_ctrl"
                    grpname=eachjoint+"_fingers_grp"
                    colour=22
                    cmds.select(cl=1) 
                    getClass.TriI(name, grpname, size, getTranslation, getRotation, colour)
                    if "Left" in eachjoint:
                        cmds.move(4, -1, 0, grpname, r=1, rpr=1, )
                        cmds.rotate(0, 0,-90, grpname, ws=1)
                    else:
                        cmds.move(-4, -1, 0, grpname, r=1, rpr=1, )
                        cmds.rotate(0, 0,90, grpname, ws=1)
                    #cmds.makeIdentity(name, a=True, t=1, s=1, r=1, n=0)                       
                    size=2*scaleWorldMatrix
                    name=eachjoint+"offset_ctrl"
                    grpname=eachjoint+"offset_grp"
                    colour=23
                    nrx=1
                    nry=0
                    nrz=0                    
                    cmds.select(cl=1) 
                    getClass.buildCtrl(each, name, grpname, getTranslation, getRotation, size, colour, nrx, nry, nrz)
                    if "Left" in eachjoint:
                        cmds.move(5, -1, 0, grpname, r=1, rpr=1, )
                    else:
                        cmds.move(-5, -1, 0, grpname, r=1, rpr=1, )
                    cmds.rotate(0, 0,-90, grpname, ws=1)
                    cmds.makeIdentity(name, a=True, t=1, s=1, r=1, n=0)                      
                    size=5
                    name=eachjoint+"IK_ctrl"
                    grpname=eachjoint+"IK_grp"                    
                    colour=13  
                    nrx=1
                    nry=0
                    nrz=0
                    cmds.select(cl=1) 
                    getClass.buildCtrl(each, name, grpname, getTranslation, getRotation, size, colour, nrx, nry, nrz)
                if "Finger" in eachjoint:
                    if "pinky" in eachjoint:
                        size=2.0*scaleWorldMatrix
                        colour=17
                    if "index" in eachjoint:
                        size=2.5*scaleWorldMatrix
                        colour=17
                    if "mid" in eachjoint:
                        size=3.0*scaleWorldMatrix
                        colour=17
                    if "ring" in eachjoint:
                        size=2.7*scaleWorldMatrix                  
                        colour=17
                    cmds.select(cl=1) 
                    getClass.TriI(name, grpname, size, getTranslation, getRotation, colour)       
                    if "Left" in eachjoint:
                            cmds.rotate(0, 180, 0, grpname)                                     
                elif "thumb" in eachjoint:
                    getTranslation, getRotation=getClass.locationXForm(eachPart) 
                    size=3*scaleWorldMatrix
                    colour=17
                    nrx=1
                    nry=0
                    nrz=0
                    getClass.buildCtrl(each, name, grpname, getTranslation, getRotation, size, colour, nrx, nry, nrz)
#                     if "Right" in eachjoint:
#                             cmds.rotate(0, 0, -180, grpname,a=1)                       
                elif "wrist" in eachjoint:
                    colour1=18
                    colour2=colour1
                    colour3=colour1
                    getClass.guideBuild(eachjoint, getTranslation, getRotation, colour1, colour2, colour3 )
                    getsel=cmds.ls(sl=1)
                    cmds.setAttr(getsel[0]+".overrideColor", colour1)
                    lognm=each.replace("grp", 'nod')   
                    cmds.rename(getsel[0], getsel[0]+'_nod')
                    getsel=cmds.ls(sl=1)
                    getClass.buildGrp(getsel[0])

            
            #make finger control rotations
            fingerJoints=[
                          "armindexFingerBaseKnuckle"+eachSide,
                            "armindexFingerMidKnuckle"+eachSide,
                            "armindexFingerEndKnuckle"+eachSide,
                            "armmidFingerBaseKnuckle"+eachSide,
                            "armmidFingerMidKnuckle"+eachSide,
                            "armmidFingerEndKnuckle"+eachSide,
                            "armringFingerBaseKnuckle"+eachSide,
                            "armringFingerMidKnuckle"+eachSide,
                            "armringFingerEndKnuckle"+eachSide,
                            "armpinkyFingerBaseKnuckle"+eachSide,
                            "armpinkyFingerMidKnuckle"+eachSide,
                            "armpinkyFingerEndKnuckle"+eachSide,            
                            ]
            translations=[".tx", ".ty", ".tz"] 
            rotation=[".rx", ".ry", ".rz"]
            creatTranDict={}
            creatRotDict={}
            fingerMaxCtrls=()
            for eachjoint in fingerJoints:
                makeCirc=cmds.circle(n=eachjoint+"_minRot_ctrl", r=.2, nrx=1, nry=0, nrz=0)
                cmds.setAttr(makeCirc[0]+"Shape.visibility", 0)
                cmds.group(n=eachjoint+"_minRot_ctrl_grp")
                makeCirc=cmds.circle(n=eachjoint+"_medRot_ctrl", r=.3, nrx=1, nry=0, nrz=0)
                cmds.setAttr(makeCirc[0]+"Shape.visibility", 0)
                cmds.group(n=eachjoint+"_medRot_ctrl_grp")
                makeCirc=cmds.circle(n=eachjoint+"_maxRot_ctrl", r=.4, nrx=1, nry=0, nrz=0)
                cmds.setAttr(makeCirc[0]+"Shape.visibility", 0)
                cmds.group(n=eachjoint+"_maxRot_ctrl_grp")
                cmds.parent(eachjoint+"_minRot_ctrl_grp", eachjoint+"_medRot_ctrl")
                cmds.parent(eachjoint+"_medRot_ctrl_grp", eachjoint+"_maxRot_ctrl")
                getTranslation=cmds.xform(eachjoint+"_jnt", q=1, t=1, ws=1)
                getRotation=cmds.xform(eachjoint+"_jnt", q=1, ro=1,ws=1)       
                for each, item in map(None, getTranslation, translations):
                    dictmake={item:each}
                    creatTranDict.update(dictmake)
                for each, item in map(None, getRotation, rotation):
                    dictmake={item:each}
                    creatRotDict.update(dictmake)
                for key, value in creatTranDict.items():
                    cmds.setAttr(eachjoint+"_maxRot_ctrl_grp"+str(key), value)
                for key, value in creatRotDict.items():
                    cmds.setAttr(eachjoint+"_maxRot_ctrl_grp"+str(key), value)
            fingerJoints=[
                            "armthumbBaseKnuckle"+eachSide,
                            "armthumbMidKnuckle"+eachSide,
                            "armthumbEndKnuckle"+eachSide,             
                            ]
            translations=[".tx", ".ty", ".tz"] 
            rotation=[".rx", ".ry", ".rz"]
            creatTranDict={}
            creatRotDict={}
            fingerMaxCtrls=()
            for eachjoint in fingerJoints:
                makeCirc=cmds.circle(n=eachjoint+"_minRot_ctrl", r=.2, nrx=1, nry=0, nrz=0)
                cmds.setAttr(makeCirc[0]+"Shape.visibility", 0)
                cmds.group(n=eachjoint+"_minRot_ctrl_grp")
                makeCirc=cmds.circle(n=eachjoint+"_medRot_ctrl", r=.3, nrx=1, nry=0, nrz=0)
                cmds.setAttr(makeCirc[0]+"Shape.visibility", 0)
                cmds.group(n=eachjoint+"_medRot_ctrl_grp")
                makeCirc=cmds.circle(n=eachjoint+"_maxRot_ctrl", r=.4, nrx=1, nry=0, nrz=0)
                cmds.setAttr(makeCirc[0]+"Shape.visibility", 0)
                cmds.group(n=eachjoint+"_maxRot_ctrl_grp")
                cmds.parent(eachjoint+"_minRot_ctrl_grp", eachjoint+"_medRot_ctrl")
                cmds.parent(eachjoint+"_medRot_ctrl_grp", eachjoint+"_maxRot_ctrl")
                getTranslation=cmds.xform(eachjoint+"_jnt", q=1, t=1, ws=1)
                getRotation=cmds.xform(eachjoint+"_guide", q=1, ro=1,ws=1)       
                for each, item in map(None, getTranslation, translations):
                    dictmake={item:each}
                    creatTranDict.update(dictmake)
                for each, item in map(None, getRotation, rotation):
                    dictmake={item:each}
                    creatRotDict.update(dictmake)
                for key, value in creatTranDict.items():
                    cmds.setAttr(eachjoint+"_maxRot_ctrl_grp"+str(key), value)
                for key, value in creatRotDict.items():
                    cmds.setAttr(eachjoint+"_maxRot_ctrl_grp"+str(key), value)
                    
            #add finger attributes
            fingerAttributes=["MiddleJoint", 
                                "LastJoint",
                                "FingerFullCurl"]
            fingers=["armpinkyFingerBaseKnuckle"+eachSide,
                    "armringFingerBaseKnuckle"+eachSide, 
                    "armmidFingerBaseKnuckle"+eachSide, 
                    "armindexFingerBaseKnuckle"+eachSide,  
                    ]
            for item in fingers:
                for each in fingerAttributes:
                    cmds.addAttr(item+"_ctrl", ln=each, at="long", min=-160, max=0, dv=0, k=1, nn=each)
                    cmds.setAttr(item+"_ctrl.visibility", 1)

            fingerAttributes=[
                                "LastJoint",
                                "FingerFullCurl"]
            fingers=[
                    "armthumbMidKnuckle"+eachSide,
                    ]
            for item in fingers:
                for each in fingerAttributes:
                    cmds.addAttr(item+"_ctrl", ln=each, at="long", min=-160, max=45, dv=0, k=1, nn=each)
                    cmds.setAttr(item+"_ctrl.visibility",1)


            #hook up base rotation to controllers
            digitBase=["armindexFingerBaseKnuckle"+eachSide,
                    "armmidFingerBaseKnuckle"+eachSide,
                    "armringFingerBaseKnuckle"+eachSide,
                    "armpinkyFingerBaseKnuckle"+eachSide,
                    "armthumbBaseKnuckle"+eachSide,
                    "armthumbMidKnuckle"+eachSide
                    ]
            for each in digitBase:
                cmds.parentConstraint(each+"_ctrl", each+"_minRot_ctrl_grp", mo=1)  

            cmds.parent("armindexFingerEndKnuckle"+eachSide+"_maxRot_ctrl_grp", "armindexFingerMidKnuckle"+eachSide+"_minRot_ctrl")
            cmds.parent("armindexFingerMidKnuckle"+eachSide+"_maxRot_ctrl_grp", "armindexFingerBaseKnuckle"+eachSide+"_minRot_ctrl")
            cmds.parent("armmidFingerEndKnuckle"+eachSide+"_maxRot_ctrl_grp", "armmidFingerMidKnuckle"+eachSide+"_minRot_ctrl")
            cmds.parent("armmidFingerMidKnuckle"+eachSide+"_maxRot_ctrl_grp", "armmidFingerBaseKnuckle"+eachSide+"_minRot_ctrl")
            cmds.parent("armringFingerEndKnuckle"+eachSide+"_maxRot_ctrl_grp", "armringFingerMidKnuckle"+eachSide+"_minRot_ctrl")
            cmds.parent("armringFingerMidKnuckle"+eachSide+"_maxRot_ctrl_grp", "armringFingerBaseKnuckle"+eachSide+"_minRot_ctrl")
            cmds.parent("armpinkyFingerEndKnuckle"+eachSide+"_maxRot_ctrl_grp", "armpinkyFingerMidKnuckle"+eachSide+"_minRot_ctrl")
            cmds.parent("armpinkyFingerMidKnuckle"+eachSide+"_maxRot_ctrl_grp", "armpinkyFingerBaseKnuckle"+eachSide+"_minRot_ctrl")
            cmds.parent("armthumbEndKnuckle"+eachSide+"_maxRot_ctrl_grp", "armthumbMidKnuckle"+eachSide+"_minRot_ctrl")
            
            
            fingerJoints=["armindexFingerBaseKnuckle"+eachSide,
                            "armindexFingerMidKnuckle"+eachSide,
                            "armindexFingerEndKnuckle"+eachSide,
                            "armpinkyFingerBaseKnuckle"+eachSide,
                            "armpinkyFingerMidKnuckle"+eachSide,
                            "armpinkyFingerEndKnuckle"+eachSide,
                            "armringFingerBaseKnuckle"+eachSide,
                            "armringFingerMidKnuckle"+eachSide,
                            "armringFingerEndKnuckle"+eachSide,
                            "armmidFingerBaseKnuckle"+eachSide,
                            "armmidFingerMidKnuckle"+eachSide,
                            "armmidFingerEndKnuckle"+eachSide,
                            ]
            for eachjoint in fingerJoints:
                cmds.parentConstraint(eachjoint+"_minRot_ctrl", eachjoint+"_jnt", sr=["x"], st=["x", "y", "z"])
            
            cmds.parentConstraint("armthumbBaseKnuckle"+eachSide+"_minRot_ctrl", "armthumbBaseKnuckle"+eachSide+"_jnt") 
            cmds.parentConstraint("armthumbMidKnuckle"+eachSide+"_minRot_ctrl", "armthumbMidKnuckle"+eachSide+"_jnt")    
            cmds.parentConstraint("armthumbEndKnuckle"+eachSide+"_minRot_ctrl", "armthumbEndKnuckle"+eachSide+"_jnt")  
            
            ##CONNECT
            ########
            #Lock and hide scales
            ########           
            allControllers=cmds.ls("*_ctrl")
            for each in allControllers:
                cmds.setAttr(str(each)+".sx" , keyable=0, lock=1)
                cmds.setAttr(str(each)+".sy" , keyable=0, lock=1)
                cmds.setAttr(str(each)+".sz", keyable=0, lock=1)
            
            ########
            #Parenting controllers
            ########
            Handchildren=[
                          "armindexFingerBaseKnuckle"+eachSide, 
                            "armmidFingerBaseKnuckle"+eachSide,
                            "armringFingerBaseKnuckle"+eachSide,
                            "armpinkyFingerBaseKnuckle"+eachSide,
                            "armthumbBaseKnuckle"+eachSide
                            ]
            
            for each in Handchildren:
                cmds.parent(each+"_grp", each+"_maxRot_ctrl")
                
                
            Handchildren=[
                          "armindexFingerBaseKnuckle"+eachSide, 
                            "armmidFingerBaseKnuckle"+eachSide,
                            "armringFingerBaseKnuckle"+eachSide,
                            "armpinkyFingerBaseKnuckle"+eachSide,
                            "armthumbBaseKnuckle"+eachSide
                            ]
             
            for each in Handchildren:
                cmds.parent(each+"_maxRot_ctrl_grp", "armhand"+eachSide+"_jnt")
                
            cmds.parent("armthumbMidKnuckle"+eachSide+"_grp", "armthumbBaseKnuckle"+eachSide+"_ctrl")
            
            ########
            #HANDS
            ########
            

            #attach finger curl to the medRotate on each joint
            cmds.connectAttr("armindexFingerBaseKnuckle"+eachSide+"_ctrl.FingerFullCurl", "armindexFingerBaseKnuckle"+eachSide+"_medRot_ctrl.rotateZ", f=1)
            cmds.connectAttr("armindexFingerBaseKnuckle"+eachSide+"_ctrl.FingerFullCurl", "armindexFingerMidKnuckle"+eachSide+"_medRot_ctrl.rotateZ", f=1)
            cmds.connectAttr("armindexFingerBaseKnuckle"+eachSide+"_ctrl.FingerFullCurl", "armindexFingerEndKnuckle"+eachSide+"_medRot_ctrl.rotateZ", f=1)
            cmds.connectAttr("armindexFingerBaseKnuckle"+eachSide+"_ctrl.MiddleJoint", "armindexFingerMidKnuckle"+eachSide+"_maxRot_ctrl.rotateZ", f=1)
            cmds.connectAttr("armindexFingerBaseKnuckle"+eachSide+"_ctrl.LastJoint", "armindexFingerEndKnuckle"+eachSide+"_maxRot_ctrl.rotateZ", f=1)
            
            cmds.connectAttr("armpinkyFingerBaseKnuckle"+eachSide+"_ctrl.FingerFullCurl", "armpinkyFingerBaseKnuckle"+eachSide+"_medRot_ctrl.rotateZ", f=1)
            cmds.connectAttr("armpinkyFingerBaseKnuckle"+eachSide+"_ctrl.FingerFullCurl", "armpinkyFingerMidKnuckle"+eachSide+"_medRot_ctrl.rotateZ", f=1)
            cmds.connectAttr("armpinkyFingerBaseKnuckle"+eachSide+"_ctrl.FingerFullCurl", "armpinkyFingerEndKnuckle"+eachSide+"_medRot_ctrl.rotateZ", f=1)
            cmds.connectAttr("armpinkyFingerBaseKnuckle"+eachSide+"_ctrl.MiddleJoint", "armpinkyFingerMidKnuckle"+eachSide+"_maxRot_ctrl.rotateZ", f=1)
            cmds.connectAttr("armpinkyFingerBaseKnuckle"+eachSide+"_ctrl.LastJoint", "armpinkyFingerEndKnuckle"+eachSide+"_maxRot_ctrl.rotateZ", f=1)
            
            cmds.connectAttr("armringFingerBaseKnuckle"+eachSide+"_ctrl.FingerFullCurl", "armringFingerMidKnuckle"+eachSide+"_medRot_ctrl.rotateZ", f=1)
            cmds.connectAttr("armringFingerBaseKnuckle"+eachSide+"_ctrl.FingerFullCurl", "armringFingerBaseKnuckle"+eachSide+"_medRot_ctrl.rotateZ", f=1)
            cmds.connectAttr("armringFingerBaseKnuckle"+eachSide+"_ctrl.FingerFullCurl", "armringFingerEndKnuckle"+eachSide+"_medRot_ctrl.rotateZ", f=1)
            cmds.connectAttr("armringFingerBaseKnuckle"+eachSide+"_ctrl.MiddleJoint", "armringFingerMidKnuckle"+eachSide+"_maxRot_ctrl.rotateZ", f=1)
            cmds.connectAttr("armringFingerBaseKnuckle"+eachSide+"_ctrl.LastJoint", "armringFingerEndKnuckle"+eachSide+"_maxRot_ctrl.rotateZ", f=1)
            
            cmds.connectAttr("armmidFingerBaseKnuckle"+eachSide+"_ctrl.FingerFullCurl", "armmidFingerBaseKnuckle"+eachSide+"_medRot_ctrl.rotateZ", f=1)
            cmds.connectAttr("armmidFingerBaseKnuckle"+eachSide+"_ctrl.FingerFullCurl", "armmidFingerMidKnuckle"+eachSide+"_medRot_ctrl.rotateZ", f=1)
            cmds.connectAttr("armmidFingerBaseKnuckle"+eachSide+"_ctrl.FingerFullCurl", "armmidFingerEndKnuckle"+eachSide+"_medRot_ctrl.rotateZ", f=1)
            cmds.connectAttr("armmidFingerBaseKnuckle"+eachSide+"_ctrl.MiddleJoint", "armmidFingerMidKnuckle"+eachSide+"_maxRot_ctrl.rotateZ", f=1)
            cmds.connectAttr("armmidFingerBaseKnuckle"+eachSide+"_ctrl.LastJoint", "armmidFingerEndKnuckle"+eachSide+"_maxRot_ctrl.rotateZ", f=1)
            
            
            cmds.connectAttr("armthumbMidKnuckle"+eachSide+"_ctrl.LastJoint", "armthumbEndKnuckle"+eachSide+"_maxRot_ctrl.rotateY", f=1)
            #cmds.orientConstraint("armhand"+eachSide+"_ctrl", "armhand"+eachSide+"_jnt", mo=1)
            cmds.setAttr("armthumbMidKnuckle"+eachSide+"_ctrl.FingerFullCurl", keyable=0, lock=1)     
            