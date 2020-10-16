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
class HeadRig(object):
    def __init__(self):
        head=(cmds.ls("head*_guide"))
       
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
        try:
            cmds.parent("head01_jnt", lastNeckJoint)
        except:
            print "no neck, neck connect skipped"
            pass


        resetOrient=[
                    "head01_jnt"
                    ]
        
        for each in resetOrient:
            cmds.joint( each, e=1, children=1, zso=1, oj='xyz', sao='yup', spa=1)  
        cmds.select(cl=1)

        
        ##################################
        ##################################
        ##################################
        ##################################
        ######################CONTROLLERS
        
        translations=[".tx", ".ty", ".tz"] 
        rotation=[".rx", ".ry", ".rz"]




        #makehead
        
        OrigName= "head01"
        size=30
        colour=13
        nrx=0
        nry=1
        nrz=0   
        eachPiece=OrigName+"_jnt"
        name="Head_Ctrl"
        grpname=OrigName+"_grp" 
        getTranslation, getRotation=getClass.locationXForm(eachPiece)
        getClass.buildCtrl(each, name, grpname,getTranslation, getRotation, size, colour, nrx, nry, nrz)
        cmds.move(0, size, 0 , "Head_Ctrl" ,r=1)
        cmds.move( 0, -size, 0, "Head_Ctrl.rotatePivot" ,  r=1)
        cmds.makeIdentity("Head_Ctrl", a=True, t=1, s=1, r=1, n=0)
        
        

        cmds.parentConstraint("Head_Ctrl", "head01_jnt", mo=1)
        try:
            neckjoints=[(each) for each in cmds.listRelatives("neck01_jnt", ad=1, typ="joint")]
        #cmds.parentConstraint("head01_grp", neckjoints[-1:], mo=1)
        #cmds.parent("head01_jnt", neckjoints[0])
        
            cmds.parent("head01_grp", "neckParent_nod")
        except:
            print "no neck present, skipped neck connect"
            pass

#         cmds.pointConstraint("neckParent_nod", "head01_grp", mo=1)
#         
#         cmds.orientConstraint("EndneckFK_Ctrl", "head01_grp", mo=1)
#         cmds.orientConstraint("EndneckIK_Ctrl", "head01_grp", mo=1)
#            
#         cmds.setAttr("Baseneck_Ctrl.neckFK_IK", 1)    
#         cmds.setAttr("head01_grp_orientConstraint1.EndneckFK_CtrlW0", 0)
#         cmds.setAttr("head01_grp_orientConstraint1.EndneckIK_CtrlW1", 1)            
#         cmds.setDrivenKeyframe("head01_grp_orientConstraint1", cd="Baseneck_Ctrl.neckFK_IK")
#         cmds.setAttr("Baseneck_Ctrl.neckFK_IK", 0)   
#         cmds.setAttr("head01_grp_orientConstraint1.EndneckFK_CtrlW0", 1)
#         cmds.setAttr("head01_grp_orientConstraint1.EndneckIK_CtrlW1", 0)           
#         cmds.setDrivenKeyframe("head01_grp_orientConstraint1", cd="Baseneck_Ctrl.neckFK_IK")
#         cmds.setAttr("Baseneck_Ctrl.neckFK_IK", 1)