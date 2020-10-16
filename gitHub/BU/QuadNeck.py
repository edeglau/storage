import sys, os
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

import maya.cmds as cmds
import maya.mel
class QuadNoNeckRig(object):
    def __init__(self):
        getGuide=cmds.ls("*_guide")
        neck=(cmds.ls("neck*_guide"))
        head=(cmds.ls("head*_guide"))

        getLimbs=(neck, head)         
        cmds.select(cl=1)
        cmds.select(cl=1)   
        for each in neck:
            jointSuffix='FK_jnt'
            getClass.rigJoints(each, jointSuffix)     
            cmds.select(cl=1)    
        cmds.select(cl=1)
        for each in head:
            jointSuffix='FK_jnt'
            getClass.rigJoints(each, jointSuffix)      

        for each in neck:
            jointSuffix='_jnt'
            getClass.rigJoints(each, jointSuffix)     
            cmds.select(cl=1)    
        cmds.select(cl=1)
        for each in head:
            jointSuffix='_jnt'
            getClass.rigJoints(each, jointSuffix)      
        cmds.select(cl=1)
        
        
        try:
            neckChildBones=cmds.listRelatives('neck01_jnt', ad=1, typ="joint")
            lastNeckJoint=neckChildBones[:1]
        except:
            lastNeckJoint='neck01_jnt'
        spineChildBones=cmds.listRelatives('spine01_jnt', ad=1, typ="joint")
        cmds.parent("neck01_jnt", spineChildBones[:1])
        cmds.parent("head01_jnt", lastNeckJoint)

        try:
            neckFKChildBones=cmds.listRelatives('neck01FK_jnt', ad=1, typ="joint")
            lastFKNeckJoint=neckChildBones[:1]
        except:
            lastFKNeckJoint='neck01FK_jnt'
        spineFKChildBones=cmds.listRelatives('spine01FK_jnt', ad=1, typ="joint")
        cmds.parent("neck01FK_jnt", spineFKChildBones[:1])
        cmds.parent("head01FK_jnt", lastFKNeckJoint)

        resetOrient=[
                    "head01_jnt"
                    ]
        
        for each in resetOrient:
            cmds.joint( each, e=1, children=1, zso=1, oj='xyz', sao='yup', spa=1)  
        cmds.select(cl=1)
        cmds.delete('neck01FK_jnt')
        
        ##################################
        ##################################
        ##################################
        ##################################
        ######################CONTROLLERS
        
        translations=[".tx", ".ty", ".tz"] 
        rotation=[".rx", ".ry", ".rz"]
        
        
        #makehead
        
        OrigName= "head01"
        size=15
        colour=13
        nrx=0
        nry=1
        nrz=0   
        eachPiece=OrigName+"_jnt"
        name="Head_Ctrl"
        grpname=OrigName+"_grp" 
        getTranslation, getRotation=getClass.locationXForm(eachPiece)
        getClass.buildCtrl(each, name, grpname,getTranslation, getRotation, size, colour, nrx, nry, nrz)
        cmds.move(0, size, 0, "Head_Ctrl" ,r=1, rpr=1, )
        cmds.move(0, -size, 0, "Head_Ctrl.rotatePivot" ,r=1, rpr=1 )
        cmds.makeIdentity("Head_Ctrl", a=True, t=1, s=1, r=1, n=0) 
        
        
        OrigName= "Neck"
        colour1=6
        colour2=colour1
        colour3=colour1
        size=7
        nrx=0
        nry=1
        nrz=0   
        eachPiece="neck01_jnt"
        name=OrigName+"_Ctrl"
        grpname=OrigName+"_grp" 
        getTranslation, getRotation=getClass.locationXForm(eachPiece)
        getClass.buildCtrl(each, name, grpname,getTranslation, getRotation, size, colour, nrx, nry, nrz)
        cmds.makeIdentity("Neck_Ctrl", a=True, t=1, s=1, r=1, n=0)
        
        
        
        colour=22
        size=5
        name="God_Node_Ctrl"
        grpname="God_Node_grp"
        getTranslation=[0.0,0.0,0.0]
        getRotation=[0.0,0.0,0.0]
        getClass.PrimI(name, grpname, size, getTranslation, getRotation, colour)
        getTranslation, getRotation=getClass.locationXForm("head02_jnt")
        cmds.move(0, getTranslation[1]+5, 0, grpname,r=1, rpr=1, )
        cmds.makeIdentity(name, a=True, t=1, s=1, r=1, n=0)             
        #constrain FK spin to controls
        cmds.parent("Master_Ctrl_grp", "God_Node_Ctrl")
            
        #cmds.parent(spineFK_Ctrls[0], "Hips_Ctrl")
        cmds.parentConstraint("Neck_Ctrl", "neck01_jnt", mo=1)     
        cmds.parentConstraint("Head_Ctrl", "head01_jnt", mo=1)

        bindneck=[(each) for each in cmds.listRelatives("neck01_jnt", ad=1, typ="joint") if "neck" in each]
        if len(bindneck)>1:
            cmds.parentConstraint(bindneck[:1], "head01_grp", mo=1)
        else:
            cmds.parentConstraint("neck01_jnt", "head01_grp", mo=1)


        spineChildBones=[(each) for each in cmds.listRelatives('spine01_jnt', ad=1, typ="joint") if "spine" in each]
        #cmds.parent(spineChildBones[0], "spineArmParent_nod")
        #cmds.parent("spineIK","Chest_IK_Ctrl")
        cmds.parent("Neck_grp", "spineArmParent_nod")
        cmds.parent("neck01_jnt", "spineArmParent_nod")
        #cmds.parent("spineArmParent_nod_grp", spineChildBones[0])
