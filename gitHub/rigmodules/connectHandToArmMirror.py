import maya.cmds as cmds
import maya.mel
import sys, os
filepath= os.getcwd()
sys.path.append(str(filepath))
import stretchIK
reload (stretchIK)
getIKClass=stretchIK.stretchIKClass()

import baseFunctions_maya
reload (baseFunctions_maya)
getClass=baseFunctions_maya.BaseClass()

'''MG rigging modules'''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons License'
'http://creativecommons.org/licenses/by-sa/3.0/au/'

class HandConn(object):
    def __init__(self):    
        Side=["Right", "Left"]
        for eachSide in Side:
            #cmds.parentConstraint("armhand"+eachSide+"_ctrl", "armhand"+eachSide+"_jnt", mo=1)
            

            handAttributes=["SpreadFingers", 
                                "CurlFingers"]
            hand=[
                    "armhand"+eachSide+"_fingers_ctrl"
                    ]             
            for item in hand:
                for each in handAttributes:
                    if "SpreadFingers" in each:
                        cmds.addAttr(item, ln=each, at="long", min=0, max=90, dv=0, k=1, nn=each)
                    else:
                        cmds.addAttr(item, ln=each, at="long", min=-90, max=0, dv=0, k=1, nn=each)
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
                            "armmidFingerEndKnuckle"+eachSide, ]
            for eachjoint in fingerJoints:
                cmds.connectAttr("armhand"+eachSide+"_fingers_ctrl.CurlFingers", eachjoint+"_minRot_ctrl.rotateZ", f=1)

            SDKfingers=("armindexFingerBaseKnuckle"+eachSide+"_maxRot_ctrl.rotateY",
                        "armmidFingerBaseKnuckle"+eachSide+"_maxRot_ctrl.rotateY",
                        "armringFingerBaseKnuckle"+eachSide+"_maxRot_ctrl.rotateY",
                        "armpinkyFingerBaseKnuckle"+eachSide+"_maxRot_ctrl.rotateY",
                        "armthumbMidKnuckle"+eachSide+"_maxRot_ctrl.rotateY",
                        "armthumbBaseKnuckle"+eachSide+"_maxRot_ctrl.rotateZ",
                        "armindexFingerBaseKnuckle"+eachSide+"_maxRot_ctrl.ry")
                         
            for each in SDKfingers:
                cmds.setDrivenKeyframe(each, cd="armhand"+eachSide+"_fingers_ctrl.SpreadFingers")
                 
            if "Left" in eachSide:
                cmds.setAttr("armhand"+eachSide+"_fingers_ctrl.SpreadFingers", 90)
                cmds.setAttr("armthumbBaseKnuckle"+eachSide+"_maxRot_ctrl.rotateZ", 30)
                cmds.setAttr("armthumbMidKnuckle"+eachSide+"_maxRot_ctrl.rotateY", -12)
                cmds.setAttr("armindexFingerBaseKnuckle"+eachSide+"_maxRot_ctrl.rotateY", -30)
                cmds.setAttr("armpinkyFingerBaseKnuckle"+eachSide+"_maxRot_ctrl.rotateY", +45)
                cmds.setAttr("armringFingerBaseKnuckle"+eachSide+"_maxRot_ctrl.rotateY", +18)
                cmds.setAttr("armmidFingerBaseKnuckle"+eachSide+"_maxRot_ctrl.rotateY", -12)
            else:
                cmds.setAttr("armhand"+eachSide+"_fingers_ctrl.SpreadFingers", 90)
                cmds.setAttr("armthumbBaseKnuckle"+eachSide+"_maxRot_ctrl.rotateZ", 30)
                cmds.setAttr("armthumbMidKnuckle"+eachSide+"_maxRot_ctrl.rotateY", 12)
                cmds.setAttr("armindexFingerBaseKnuckle"+eachSide+"_maxRot_ctrl.rotateY", 30)
                cmds.setAttr("armpinkyFingerBaseKnuckle"+eachSide+"_maxRot_ctrl.rotateY", -45)
                cmds.setAttr("armringFingerBaseKnuckle"+eachSide+"_maxRot_ctrl.rotateY", -18)
                cmds.setAttr("armmidFingerBaseKnuckle"+eachSide+"_maxRot_ctrl.rotateY", 12)
             
            for each in SDKfingers:
                cmds.setDrivenKeyframe(each, cd="armhand"+eachSide+"_fingers_ctrl.SpreadFingers")
                cmds.setAttr(each, lock=1)
                 
            cmds.setAttr("armhand"+eachSide+"_fingers_ctrl.SpreadFingers", 0)
            #cmds.parentConstraint("armhand"+eachSide+"_jnt", "armwrist"+eachSide+"_grp", mo=1)
            
            #Twist arm
            cmds.addAttr("armhand"+eachSide+"IK_ctrl", ln="TwistArm", at="long", min=-360, max=360, dv=0, k=1, nn="TwistArm")
             
            cmds.connectAttr ("armhand"+eachSide+"IK_ctrl.TwistArm", "armelbow"+eachSide+"_jnt.rotate.rotateX", f=1)
            cmds.connectAttr ("armhand"+eachSide+"IK_ctrl.TwistArm", "armshoulder"+eachSide+"_jnt.rotate.rotateX", f=1)   


            ChildActivatedValue=1
            ChildDeactivatedValue=0
            ControllerSecondValue=1
            ControllerFirstValue=0
            Child="armhand"+eachSide+"IK_ctrl.visibility"
            Controller="armcollar"+eachSide+"IK_ctrl."+eachSide+"ArmFK_IK"
            defaultSet=1
            getClass.controlSecondValueChildOn(Controller, 
                                               Child, 
                                               defaultSet, 
                                               ChildActivatedValue, 
                                               ChildDeactivatedValue, 
                                               ControllerSecondValue, 
                                               ControllerFirstValue)

            #set stretch

            cmds.addAttr("armhand"+eachSide+"IK_ctrl", ln="Stretch", at="enum",en="on:off:", k=1, nn="Stretch")

            

            
            cmds.connectAttr ("armhand"+eachSide+"IK_ctrl.TwistArm",  "armwrist"+eachSide+"IK_ctrl.TwistArm", f=1) 
            cmds.connectAttr ("armhand"+eachSide+"IK_ctrl.Stretch",  "armwrist"+eachSide+"IK_ctrl.Stretch", f=1)             
            cmds.setAttr("armhand"+eachSide+"_ctrl.tx", cb=0)
            cmds.setAttr("armhand"+eachSide+"_ctrl.ty", cb=0)
            cmds.setAttr("armhand"+eachSide+"_ctrl.tz", cb=0)
            cmds.setAttr("armhand"+eachSide+"_ctrl.rx", cb=0) 
            cmds.setAttr("armhand"+eachSide+"_ctrl.ry", cb=0) 
            cmds.setAttr("armhand"+eachSide+"_ctrl.rz", cb=0) 
            cmds.setAttr("armwrist"+eachSide+"_ctrl.rx")
            cmds.setAttr("armwrist"+eachSide+"_ctrl.ry")
            cmds.setAttr("armwrist"+eachSide+"_ctrl.rz")
            cmds.setAttr("armshoulder"+eachSide+"_ctrl.tx")
            cmds.setAttr("armshoulder"+eachSide+"_ctrl.ty")
            cmds.setAttr("armshoulder"+eachSide+"_ctrl.tz")

            cmds.pointConstraint( "armwrist"+eachSide+"_offset_IK_ctrl", "armwrist"+eachSide+"IK_ctrl", mo=1)
            
            cmds.orientConstraint("armwrist"+eachSide+"_offset_IK_ctrl", "armhand"+eachSide+"_ctrl", mo=1)
            cmds.orientConstraint("armwrist"+eachSide+"_ctrl", "armhand"+eachSide+"_ctrl", mo=1)
              
            cmds.setAttr("armcollar"+eachSide+"IK_ctrl."+eachSide+"ArmFK_IK", 1)     
            cmds.setAttr("armhand"+eachSide+"_ctrl_orientConstraint1.armwrist"+eachSide+"_offset_IK_ctrlW0", 1)
            cmds.setAttr("armhand"+eachSide+"_ctrl_orientConstraint1.armwrist"+eachSide+"_ctrlW1", 0)            
            cmds.setDrivenKeyframe("armhand"+eachSide+"_ctrl_orientConstraint1", cd="armcollar"+eachSide+"IK_ctrl."+eachSide+"ArmFK_IK")
            cmds.setAttr("armcollar"+eachSide+"IK_ctrl."+eachSide+"ArmFK_IK", 0)
            cmds.setAttr("armhand"+eachSide+"_ctrl_orientConstraint1.armwrist"+eachSide+"_offset_IK_ctrlW0", 0)
            cmds.setAttr("armhand"+eachSide+"_ctrl_orientConstraint1.armwrist"+eachSide+"_ctrlW1", 1)            
            cmds.setDrivenKeyframe("armhand"+eachSide+"_ctrl_orientConstraint1", cd="armcollar"+eachSide+"IK_ctrl."+eachSide+"ArmFK_IK")
            cmds.setAttr("armcollar"+eachSide+"IK_ctrl."+eachSide+"ArmFK_IK", 0)   
            
              
            cmds.parent("armhand"+eachSide+"_jnt", "armhand"+eachSide+"_ctrl")    
            cmds.parent("armhand"+eachSide+"_ctrl", "armwrist"+eachSide+"_nod")  
             
            cmds.parent("armhand"+eachSide+"offset_grp", "armhand"+eachSide+"_ctrl") 
            cmds.parent("armhand"+eachSide+"_fingers_grp", "armhand"+eachSide+"_ctrl")  

            cmds.parent("armwrist"+eachSide+"_nod_grp", "armwrist"+eachSide+"_jnt")  
                            