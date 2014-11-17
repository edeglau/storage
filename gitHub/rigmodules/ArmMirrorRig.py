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
import stretchIK
reload (stretchIK)
getIKClass=stretchIK.stretchIKClass()

import baseFunctions_maya
reload (baseFunctions_maya)
getClass=baseFunctions_maya.BaseClass()



class ArmRig(object):
    def __init__(self):
        getGuide=cmds.ls("*_guide")
        shoulderShrug=("armcollarRight_guide",
                        "armshoulderRight_guide", )
        ArmRightList=("armcollarRight_guide",
                        "armshoulderRight_guide", 
                        "armelbowRight_guide", 
                        "armwristRight_guide")
        sudoArm=("armshoulderRight_guide",
                "armelbowRight_guide",
                "armwristRight_guide")
        cmds.select(cl=1)        
        getLimbs=(ArmRightList)         
        for item in getLimbs:
            jointSuffix='_jnt'
            getClass.rigJoints(item, jointSuffix)
        cmds.select(cl=1)
        for item in sudoArm:
            jointSuffix='FK_jnt'
            getClass.rigJoints(item, jointSuffix)
        cmds.select(cl=1)  
        for item in sudoArm:
            jointSuffix='IK_jnt'
            getClass.rigJoints(item, jointSuffix)
        cmds.select(cl=1)
        for item in shoulderShrug:
            jointSuffix='SH_jnt'
            getClass.rigJoints(item, jointSuffix)
        cmds.select(cl=1)
        cmds.mirrorJoint("armcollarRightSH_jnt", myz=1, sr=("Right", "Left"))
        cmds.mirrorJoint("armcollarRight_jnt", myz=1, sr=("Right", "Left"))
        cmds.mirrorJoint("armshoulderRightFK_jnt", myz=1, sr=("Right", "Left"))
        cmds.mirrorJoint("armshoulderRightIK_jnt", myz=1, sr=("Right", "Left"))
        
        
        resetOrient=[
                    "armcollarRightSH_jnt",
                    "armcollarLeftSH_jnt",
                     "armcollarRight_jnt",
                     "armcollarLeft_jnt",
                    "armshoulderRightFK_jnt",
                    "armshoulderRightIK_jnt",
                    "armshoulderLeftFK_jnt",
                    "armshoulderLeftIK_jnt"
                    ]
        for each in resetOrient:
            if "Left" in each:
                cmds.joint( each, e=1, children=1, zso=1, oj='xyz', sao='ydown', spa=1) 
            elif "collar" in resetOrient and "Right" in resetOrient:
                cmds.joint( each, e=1, children=1, zso=1, oj='xyz', sao='zdown', spa=1)  
        cmds.select(cl=1)
        
        
        Side=["Right", "Left"]
        
        for eachSide in Side:
            #CONTROLS
            translations=[".tx", ".ty", ".tz"] 
            rotation=[".rx", ".ry", ".rz"]
            
            jointGroup=[
                        "armshoulder"+eachSide, 
                        "armelbow"+eachSide, 
                        "armwrist"+eachSide,          
                        ]
            
            controlGroup=["armwrist"+eachSide, 
                        "armcollar"+eachSide, 
                       
                        ]
            
            cmds.group( em=True, name='IK_grp' )
            
            groupCtrls=[]
            for eachjoint in jointGroup:
                scaleWorldMatrix = cmds.xform(eachjoint.split(eachSide)[0]+"Right_guide", q=True, r=1, s=True)
                scaleWorldMatrix=int(scaleWorldMatrix[0])
                eachPiece=eachjoint+"_jnt"
                name=eachjoint+"_ctrl"
                grpname=eachjoint+"_grp"  
                if "shoulder" in eachjoint:
                    size=9*scaleWorldMatrix
                    print size
                    colour=6
                else:
                    size=6*scaleWorldMatrix
                    colour=6
                nrx=1
                nry=0
                nrz=0
                getTranslation, getRotation=getClass.locationXForm(eachPiece)
                getClass.buildCtrl(eachjoint, name, grpname, getTranslation, getRotation, size, colour, nrx, nry, nrz)
#                 cmds.scale(scaleWorldMatrix[0], scaleWorldMatrix[0], scaleWorldMatrix[0],grpname )
                if "Right" in eachjoint:
                    cmds.rotate(0, 0, 0, grpname, ws=1)             
                    if "wrist" in eachjoint:
                            cmds.rotate(0, 180, 180, grpname)             
#                 if "elbow" in eachjoint:                  
#                     cmds.setAttr(name+".rx" , keyable=0, lock=1)
#                     cmds.setAttr(name+".rz", keyable=0, lock=1)  
#                     cmds.setAttr(name+".tx" , keyable=0, lock=1)
#                     cmds.setAttr(name+".ty" , keyable=0, lock=1)
#                     cmds.setAttr(name+".tz", keyable=0, lock=1)    

                                     
            
            for eachjoint in controlGroup:
                scaleWorldMatrix = cmds.xform(eachjoint.split(eachSide)[0]+"Right_guide", q=True, r=1, s=True)
                scaleWorldMatrix=int(scaleWorldMatrix[0])                
                eachPiece=eachjoint+"_jnt"
                name=eachjoint+"IK_ctrl"
                grpname=eachjoint+"IK_grp" 
                if "collar" in eachjoint:
                    size=12*scaleWorldMatrix
                else:
                    size=5*scaleWorldMatrix
                colour=13
                nrx=1
                nry=0
                nrz=0
                getTranslation, getRotation=getClass.locationXForm(eachPiece)
                getClass.buildCtrl(eachjoint, name, grpname, getTranslation, getRotation, size, colour, nrx, nry, nrz)
#                 if "Right" in eachjoint:
#                     cmds.rotate(180, 0, 0,grpname, ws=1)  
# #                     cmds.rotate(180, 180-19.489, 180-8.064, grpname)
#                 else:
                cmds.rotate(0, 0, 0,grpname, ws=1)
                if "Right" in eachjoint:
                    cmds.rotate(180, 0, 0,grpname, ws=1)                  
#                     if "wrist" in eachjoint:
#                             cmds.rotate(0, 180, 180, grpname)                                         
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

            scaleWorldMatrix = cmds.xform("armwristRight_guide", q=True, r=1, s=True)
            scaleWorldMatrix=int(scaleWorldMatrix[0])     
            eachPiece="armwrist"+eachSide+"_jnt"              
            getTranslation, getRotation=getClass.locationXForm(eachPiece)
            size=4*scaleWorldMatrix
            name="armwrist"+eachSide+"_offset_IK_ctrl"
            grpname="armwrist"+eachSide+"_offset_IK_grp"
            colour=23
            nrx=1
            nry=0
            nrz=0
            cmds.select(cl=1)     
            getClass.buildCtrl("armwrist"+eachSide, name, grpname, getTranslation, getRotation, size, colour, nrx, nry, nrz)
#             if "Right" in eachjoint:            
#                 cmds.rotate(180, 180, 180, grpname)                 
#                 if "wrist" in eachjoint:
#                         cmds.rotate(180, 0, 0, grpname)     
            #create ik pole constraint controllers
            
            
            IKHandlesLimbsarms=["armelbow"+eachSide,
                                "armwrist"+eachSide]
            for each in IKHandlesLimbsarms:
                scaleWorldMatrix = cmds.xform(eachjoint.split(eachSide)[0]+"Right_guide", q=True, r=1, s=True)
                scaleWorldMatrix=int(scaleWorldMatrix[0])     
                getTranslation=cmds.xform(each+"_jnt", q=1, t=1, ws=1)
                name=each+"_jnt_ikPole_lctr"
                grpname=each+"_jnt_ikPole_lctr"+"_grp"
                num=3
                color=13
                if "elbow" in each:
#                     if "Right" in each:
#                         getClass.JackI(name, grpname, num, getTranslation, (0.0,0.0,0.0), color)
#                         cmds.move( 0.0, -10.0, 0.0,grpname,r=1, rpr=1)
#                     else:
                    getClass.JackI(name, grpname, num, getTranslation, (0.0,0.0,0.0), color)
                    cmds.move( 0.0, +10.0, 0.0,grpname,r=1, rpr=1)
                    #cmds.spaceLocator(n=each+"_jnt_ikPole_lctr", p=(getTranslation[0], getTranslation[1]+10, getTranslation[2]))           
                if "wrist" in each:
                    if "Right" in each:
                        getClass.JackI(name, grpname, num, getTranslation, (0.0,0.0,0.0), color)
                        cmds.move(0.0, +5.0, 0.0,grpname,r=1, rpr=1)             
                    else:                 
                        getClass.JackI(name, grpname, num, getTranslation, (0.0,0.0,0.0), color)
                        cmds.move(0.0, -5.0, 0.0,grpname,r=1, rpr=1)                    
                    #cmds.spaceLocator(n=each+"_jnt_ikPole_lctr", p=(getTranslation[0], getTranslation[1]-5, getTranslation[2])) 
                getTranslation=cmds.xform(each+"_jnt", q=1, t=1, ws=1)
                cmds.move(getTranslation[0], getTranslation[1], getTranslation[2],each+"_jnt_ikPole_lctr"+"_grp"+".rotatePivot", ws=1, rpr=1 )
                if 'wrist' in each:
                     cmds.setAttr(each+"_jnt_ikPole_lctr.visibility", 0)
                    
                
            getTranslation=cmds.xform("armshoulder"+eachSide+"_jnt", q=1, t=1, ws=1)
            cmds.move(getTranslation[0], getTranslation[1], getTranslation[2],"armelbow"+eachSide+"_jnt_ikPole_lctr_grp.rotatePivot", ws=1, rpr=1 )
            
            #create IK
            
            startArmJoint=["armshoulder"+eachSide+"IK_jnt",
                            ]
            
            IKArmlist=["armwrist"+eachSide,
                        ]
            
            for each, item in map(None, IKArmlist, startArmJoint):
                cmds.ikHandle(n=each+"_ik", sj=item, ee=each+"IK_jnt", sol="ikRPsolver")
                cmds.setAttr(each+"_ik.visibility", 0)
                cmds.parent(each+"_ik", each+"IK_ctrl")
            
            armIKs=["armwrist"+eachSide]
            for eachjoint in armIKs:
                eachName=eachjoint+"IK_jnt"
                getTranslation=cmds.xform(eachName, q=1, t=1, ws=1)
                cmds.spaceLocator(n=str(eachjoint)+"Pole_lctr", p=(getTranslation))
                cmds.CenterPivot()
                cmds.setAttr(str(eachjoint)+"Pole_lctr.visibility", 0)
            
            #IKpole twist
            if "Left" in eachSide:
                cmds.setAttr("armwrist"+eachSide+"_ik.twist", 90)
            else:
                cmds.setAttr("armwrist"+eachSide+"_ik.twist", -90)
            
            #poleVector Constraints
            cmds.parent("armwrist"+eachSide+"_jnt_ikPole_lctr_grp", "armwrist"+eachSide+"IK_ctrl" )
            cmds.parent("armelbow"+eachSide+"_jnt_ikPole_lctr_grp", "armshoulder"+eachSide+"IK_jnt")
            cmds.poleVectorConstraint("armwrist"+eachSide+"_jnt_ikPole_lctr", "armwrist"+eachSide+"_ik")  
            
            cmds.connectAttr("armelbow"+eachSide+"_jnt_ikPole_lctr.translateZ", "armwrist"+eachSide+"_jnt_ikPole_lctr_grp.rotateX", f=1)               


            ########ARMS
            #Connect Blender Controls for IK/FK switch
            ########
            cmds.addAttr("armcollar"+eachSide+"IK_ctrl", ln=eachSide+"ArmFK_IK", min=0, max=1, at="double", k=1, nn=""+eachSide+"ArmFK_IK")
            #cmds.addAttr("armcollar"+eachSide+"IK_ctrl", ln=eachSide+"ArmFK_IK", at="enum",en="FK:IK:", k=1, nn=""+eachSide+"ArmFK_IK")
            cmds.parent("armshoulder"+eachSide+"_jnt", w=1)
            
            Controller="armcollar"+eachSide+"IK_ctrl."+eachSide+"ArmFK_IK"
            armskel=[
                    "armshoulder"+eachSide,
                    "armelbow"+eachSide,
                    "armwrist"+eachSide
                        ]
            for each in armskel:
                getClass.blendColors(each, Controller)
                getClass.blendColorsTranslate(each, Controller)#this creates a FK stretch. Use parentConstraint on the joint to control to work


            #Twist arm
            cmds.addAttr("armwrist"+eachSide+"IK_ctrl", ln="TwistArm", at="long", min=-360, max=360, dv=0, k=1, nn="TwistArm")
            
            cmds.connectAttr ("armwrist"+eachSide+"IK_ctrl.TwistArm", "armelbow"+eachSide+"_jnt.rotate.rotateX", f=1)
            cmds.connectAttr ("armwrist"+eachSide+"IK_ctrl.TwistArm", "armshoulder"+eachSide+"_jnt.rotate.rotateX", f=1)
                
            IKArmlist=[
                     "armshoulder"+eachSide+"SH"
                            ]
            
            startArmJoint=[
                        "armcollar"+eachSide+"SH_jnt"
                        ]
            
            for each, item in map(None, IKArmlist, startArmJoint):
                cmds.ikHandle(n=each+"_ik", sj=item, ee=each+"_jnt", sol="ikRPsolver")
                cmds.setAttr(each+"_ik.visibility", 0)

            #connect FK controllers to FK skel
            
            cmds.connectAttr ("armshoulder"+eachSide+"_ctrl.rotate", "armshoulder"+eachSide+"FK_jnt.rotate", f=1)
            
            #cmds.connectAttr ("armelbow"+eachSide+"_ctrl.rotate", "armelbow"+eachSide+"FK_jnt.rotate", f=1)
            
            cmds.parentConstraint ("armelbow"+eachSide+"_ctrl", "armelbow"+eachSide+"FK_jnt", mo=1)     
            cmds.parentConstraint ("armwrist"+eachSide+"_ctrl", "armwrist"+eachSide+"FK_jnt", mo=1)       
            #cmds.connectAttr ("armelbow"+eachSide+"_ctrl.translate", "armelbow"+eachSide+"FK_jnt.translate", f=1)
            #cmds.orientConstraint("armwrist"+eachSide+"_ctrl", "armwrist"+eachSide+"FK_jnt", mo=1)


            #FK controls parents
            cmds.parent("armwrist"+eachSide+"_grp","armelbow"+eachSide+"_ctrl")
            cmds.parent("armelbow"+eachSide+"_grp","armshoulder"+eachSide+"_ctrl")               

            #set visibility
            ChildActivatedValue=1
            ChildDeactivatedValue=0
            ControllerSecondValue=1
            ControllerFirstValue=0
            Children=["armelbow"+eachSide+"_ctrl.visibility", 
                      "armwrist"+eachSide+"_ctrl.visibility", 
                      "armshoulder"+eachSide+"_ctrl.visibility"]
            Controller="armcollar"+eachSide+"IK_ctrl."+eachSide+"ArmFK_IK"
            defaultSet=0
            for eachChild in Children:
                getClass.controlFirstValueChildOn(Controller, 
                                                  eachChild, 
                                                  defaultSet, 
                                                  ChildActivatedValue, 
                                                  ChildDeactivatedValue, 
                                                  ControllerSecondValue, 
                                                  ControllerFirstValue)

            Children=["armelbow"+eachSide+"_jnt_ikPole_lctr.visibility", "armwrist"+eachSide+"_offset_IK_ctrl.visibility"]
            ChildActivatedValue=1
            ChildDeactivatedValue=0
            ControllerSecondValue=1
            ControllerFirstValue=0
            Controller="armcollar"+eachSide+"IK_ctrl."+eachSide+"ArmFK_IK"
            defaultSet=1
            for Child in Children:
                getClass.controlSecondValueChildOn(Controller, 
                                                   Child, 
                                                   defaultSet, 
                                                   ChildActivatedValue, 
                                                   ChildDeactivatedValue, 
                                                   ControllerSecondValue, 
                                                   ControllerFirstValue)


                        
            #cmds.connectAttr ("armhand"+eachSide+"IK_ctrl.translate", "armhand"+eachSide+"_ctrl.translate" , f=1)
            
            #set stretch
            
            getIKClass.stretch("armshoulder"+eachSide+"IK_jnt")
            
            cmds.addAttr("armwrist"+eachSide+"IK_ctrl", ln="Stretch", at="enum",en="on:off:", k=1, nn="Stretch")
            
            
            
            ChildActivatedValue=2
            ChildDeactivatedValue=0
            ControllerSecondValue=1
            ControllerFirstValue=0
            Child="armshoulder"+eachSide+"IK_jnt_cond.operation"
            Controller="armwrist"+eachSide+"IK_ctrl.Stretch"
            defaultSet=0
            getClass.controlFirstValueChildOn(Controller, 
                                               Child, 
                                               defaultSet, 
                                               ChildActivatedValue, 
                                               ChildDeactivatedValue, 
                                               ControllerSecondValue,
                                               ControllerFirstValue)
            

            #hooking up the nods

 

            #parent ik controls
            cmds.parent("armshoulder"+eachSide+"SH_ik", "armcollar"+eachSide+"IK_ctrl") #shoulder shrug ik to the collar control
            cmds.parent("armcollar"+eachSide+"IK_grp", "armcollar"+eachSide+"_nod")
            cmds.parent("armcollar"+eachSide+"SH_jnt", "armcollar"+eachSide+"_nod")

            #connect wrist orientation to FK wrist control
            #cmds.orientConstraint("armwrist"+eachSide+"IK_ctrl", "armwrist"+eachSide+"IK_jnt", mo=1)#aim wrist to ik control
            

            cmds.pointConstraint("armshoulder"+eachSide+"_ctrl", "armshoulder"+eachSide+"IK_jnt")#follow the IK chain to the shoulder control
            cmds.pointConstraint("armshoulder"+eachSide+"_ctrl", "armshoulder"+eachSide+"FK_jnt")#follow the FK chain to the shoulder control
            cmds.pointConstraint("armshoulder"+eachSide+"_ctrl", "armshoulder"+eachSide+"_jnt")#follow the skeleton to the shoulder control
            cmds.pointConstraint("armshoulder"+eachSide+"SH_ik", "armshoulder"+eachSide+"_ctrl")#follow the shoulder control to the ik handle of the shrug
            

            cmds.parent("armshoulder"+eachSide+"_jnt", "armcollar"+eachSide+"_nod")                          
            cmds.parent("armshoulder"+eachSide+"_grp", "armcollar"+eachSide+"_nod")
            cmds.parent("armshoulder"+eachSide+"FK_jnt", "armcollar"+eachSide+"_nod") 

            #cmds.parentConstraint("armcollar"+eachSide+"_nod", "armshoulder"+eachSide+"IK_jnt", mo=1)  
            cmds.parent("armshoulder"+eachSide+"IK_jnt", "armcollar"+eachSide+"_nod")  #attach the IK chain to parent nod 
            cmds.setAttr("armwrist"+eachSide+"IK_ctrl.visibility", 0)
            cmds.rotate(180, 0, 0, "armwristRight_offset_IK_grp")   