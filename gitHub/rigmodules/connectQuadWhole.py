
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
        
        spine=cmds.ls("spine*_jnt")
        
        Side=["Right", "Left"]
        for eachSide in Side:    
  
            cmds.parent("armwrist"+eachSide+"_offset_IK_grp", "Main_Ctrl" )

            bindSpine=[(each) for each in cmds.listRelatives("spine01_jnt", ad=1, typ="joint") if "spine" in each]
            cmds.parent("armcollar"+eachSide+"_nod_grp", "spineArmParent_nod")
            cmds.parent("leg"+eachSide+"_nod_grp","Hips_Ctrl")
            cmds.parent("leg"+eachSide+"FK_jnt","Hips_Ctrl")
            cmds.parent("leg"+eachSide+"IK_jnt","Hips_Ctrl")

            cmds.parent("heelrear"+eachSide+"IK_grp","Main_Ctrl")
            cmds.parent("heelfront"+eachSide+"IK_grp","Main_Ctrl")
            cmds.addAttr("Hips_Ctrl", ln="Leg"+eachSide+"FK_IK", min=0, max=1, at="double", en="FK:IK:", k=1, nn="Leg"+eachSide+"FK_IK")
            cmds.connectAttr("Hips_Ctrl.Leg"+eachSide+"FK_IK", "leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK")
            cmds.setAttr("Hips_Ctrl.Leg"+eachSide+"FK_IK", 1)
            
            cmds.parent("armcollar"+eachSide+"_nod_grp", spine[-1:])

        try:
            cmds.parent("neckMain_grp", "spineArmParent_nod")
            cmds.pointConstraint(spine[-1:], "neckMain_grp", mo=1)
        except:
            print "no long neck-tail present - skipped spine//neck hookup"
            pass
        try:
            cmds.parent("tailMain_grp", spine[0])
        except:
            print "no tailMain grp present - skipped spine//tail hookup"
            pass
#         cmds.pointConstraint(spine[0], "tailMain_grp", mo=1)
        
        try:
            cmds.orientConstraint("Chest_FK_Ctrl", "neckMain_grp", mo=1)
            cmds.orientConstraint("Chest_IK_Ctrl", "neckMain_grp", mo=1)
            cmds.setAttr("Hips_Ctrl.spineFK_IK", 1)
            cmds.setAttr("neckMain_grp_orientConstraint1.Chest_FK_CtrlW0", 0)
            cmds.setAttr("neckMain_grp_orientConstraint1.Chest_IK_CtrlW1", 1)            
            cmds.setDrivenKeyframe("neckMain_grp_orientConstraint1", cd="Hips_Ctrl.spineFK_IK")
            cmds.setAttr("Hips_Ctrl.spineFK_IK", 0)   
            cmds.setAttr("neckMain_grp_orientConstraint1.Chest_FK_CtrlW0", 1)
            cmds.setAttr("neckMain_grp_orientConstraint1.Chest_IK_CtrlW1", 0)           
            cmds.setDrivenKeyframe("neckMain_grp_orientConstraint1", cd="Hips_Ctrl.spineFK_IK")
            cmds.setAttr("Hips_Ctrl.spineFK_IK", 1)            
        except:
            print "no long neck-tail present - skipped ik/fk switch hooked to spine top"
            pass
        cmds.setAttr("spine01FK_jnt.visibility", 1)
        cmds.setAttr("spine01IK_jnt.visibility", 1)
        
        try:
            cmds.parent("BaseTail_grp", spine[0])
        except:
            print "no tail present - skipped spine//tail hookup"
            pass
        
        gethandles=cmds.select()
        cmds.setAttr("spineIK.visibility", 1)
        
        getHandles=cmds.ls(typ="ikHandle")
        for each in getHandles:
            cmds.setAttr(each+'.visibility', 1)   
        spineChildBones=[(each) for each in cmds.listRelatives('spine01_jnt', ad=1, typ="joint") if "spine" in each]
        try:
            cmds.parent("neck01_jnt", spineChildBones[:1])
        except:
            print "no neck - skipped spine/neck hookup"
            pass
      
        try:
            cmds.addAttr("Hips_Ctrl", ln="tailFK_IK", min=0, max=1, at="double",en="FK:IK:", k=1, nn="tailFK_IK")
            cmds.connectAttr("LowerBody_Ctrl.tailFK_IK", "Basetail_Ctrl.tailFK_IK")
            cmds.addAttr("Hips_Ctrl", ln="Stretchtail", min=0, max=1, at="double",en="FK:IK:", k=1, nn="Stretchtail")
            cmds.connectAttr( "LowerBody_Ctrl.Stretchtail","Basetail_Ctrl.Stretchtail",)   
        except:
            print "no long tail present - skipped tail fk//ik switch"
            pass