
import maya.cmds as cmds
import maya.mel


import sys, os
filepath= os.getcwd()
sys.path.append(str(filepath))
import baseFunctions_maya
reload (baseFunctions_maya)
getClass=baseFunctions_maya.BaseClass()

'''MG rigging modules'''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons License'
'http://creativecommons.org/licenses/by-sa/3.0/au/'

class BodConn(object):
    def __init__(self):
        Side=["Right", "Left"]
        for eachSide in Side:    
            try:
                cmds.parent("armhand"+eachSide+"IK_grp", "armcollar"+eachSide+"IK_ctrl")
            except:
                pass
            try:      
                cmds.parent("armhand"+eachSide+"IK_grp", "armcollar"+eachSide+"IK_ctrl")
            except:
                pass 
            #cmds.parent("armwrist"+eachSide+"_offset_grp", "Main_Ctrl")
            #cmds.addAttr("armwrist"+eachSide+"_offset_IK_ctrl", ln="HandUnlock", min=0, max=1, at="double", k=1, nn="HandUnlock")
            try:
                cmds.parentConstraint( "armhand"+eachSide+"IK_ctrl","armwrist"+eachSide+"_offset_IK_ctrl", mo=1)
            except:
                pass
#             cmds.setKeyframe("armwrist"+eachSide+"_offset_IK_ctrl", bd=0, hi="none", cp= 0, s=0)
#             cmds.connectAttr("armwrist"+eachSide+"_offset_IK_ctrl.HandUnlock","armwrist"+eachSide+"_offset_IK_ctrl.blendParent1", f=1)
#             cmds.connectAttr("armwrist"+eachSide+"_offset_IK_ctrl.HandUnlock","armwrist"+eachSide+"_offset_IK_ctrl_parentConstraint1.armhand"+eachSide+"IK_ctrlW0", f=1)
#             cmds.setAttr("armwrist"+eachSide+"_offset_IK_ctrl.HandUnlock", 1)
            
            
            #this causes fk arm to follow body - needs work
#             cmds.orientConstraint("UpperBody_Ctrl", "armshoulder"+eachSide+"_grp", mo=1)
#             bindSpine=[(each) for each in cmds.listRelatives("spine01_jnt", ad=1, typ="joint") if "spine" in each]
            cmds.orientConstraint("UpperBody_Ctrl", "armshoulder"+eachSide+"_grp", mo=1)
            try:
                cmds.parent("leghip"+eachSide+"_nod_grp","Hips_Ctrl")
            except:
                pass
            try:
                cmds.parent("leghip"+eachSide+"FK_jnt","Hips_Ctrl")
            except:
                pass
            try:        
                cmds.parent("leghip"+eachSide+"IK_jnt","Hips_Ctrl")
            except:
                pass

            try:
                cmds.parent("footheel"+eachSide+"IK_grp","Main_Ctrl")
            except:
                pass
            try:
                cmds.addAttr("Hips_Ctrl", ln="Leg"+eachSide+"FK_IK", min=0, max=1, at="double", en="FK:IK:", k=1, nn="Leg"+eachSide+"FK_IK")
            except:
                pass            
            try:
                cmds.connectAttr("Hips_Ctrl.Leg"+eachSide+"FK_IK", "leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK")
            except:
                pass
            try:
                cmds.setAttr("Hips_Ctrl.Leg"+eachSide+"FK_IK", 1)
            except:
                pass

            ChildActivatedValue=1
            ChildDeactivatedValue=0
            ControllerOnValue=1
            ControllerFirstValue=0
            Child="football"+eachSide+"_jnt_grp_orientConstraint1.football"+eachSide+"RFL_jntW0"
            Controller="Hips_Ctrl.Leg"+eachSide+"FK_IK"
            defaultSet=1
            getClass.controlSecondValueChildOn(Controller, 
                                               Child, 
                                               defaultSet, 
                                               ChildActivatedValue, 
                                               ChildDeactivatedValue, 
                                               ControllerOnValue, 
                                               ControllerFirstValue)             

        cmds.setAttr("spine01FK_jnt.visibility", 0)
        cmds.setAttr("spine01IK_jnt.visibility", 0)
        
        
        
        gethandles=cmds.select()
        try:
            cmds.setAttr("spineIK.visibility", 0)
        except:
            pass        
        
        getHandles=cmds.ls(typ="ikHandle")
        for each in getHandles:
            cmds.setAttr(each+'.visibility', 0)        