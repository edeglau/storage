import sys
import os
filepath= os.getcwd()
sys.path.append(str(filepath))
import baseFunctions_maya
reload (baseFunctions_maya)
getClass=baseFunctions_maya.BaseClass()


__author__ = "Elise Deglau"
__version__ = 1.00

import maya.cmds as cmds
import maya.mel


class FootConn(object):
    def __init__(self):
        
        Side=["Right", "Left"]
        DepthDimension=["front", "rear"]
        
        for eachSide in Side:
            
            
            cmds.parent("anklefront"+eachSide+"_jnt", "armwrist"+eachSide+"_nod" )
            cmds.parent("anklerear"+eachSide+"_jnt", "foottalus"+eachSide+"_jnt" )

            #REAR
            cmds.setAttr("leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK", 1) 
            cmds.setAttr("toerear"+eachSide+"_ik.ikBlend", 1)
            cmds.setAttr("toerear"+eachSide+"_ik_pointConstraint1.toerear"+eachSide+"IK_jntW0", 1)
            cmds.setAttr("anklerear"+eachSide+"_jnt_orientConstraint1.anklerear"+eachSide+"IK_jntW0", 1)
            cmds.setDrivenKeyframe("anklerear"+eachSide+"_jnt_orientConstraint1", cd="leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK")
            cmds.setDrivenKeyframe("toerear"+eachSide+"_ik_pointConstraint1", cd="leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK")
            cmds.setDrivenKeyframe("toerear"+eachSide+"_ik", cd="leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK")
            cmds.setAttr("leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK", 0)
            cmds.setAttr("toerear"+eachSide+"_ik.ikBlend", 0)            
            cmds.setAttr("toerear"+eachSide+"_ik_pointConstraint1.toerear"+eachSide+"IK_jntW0", 0)
            cmds.setAttr("anklerear"+eachSide+"_jnt_orientConstraint1.anklerear"+eachSide+"IK_jntW0", 0)
            cmds.setDrivenKeyframe("anklerear"+eachSide+"_jnt_orientConstraint1", cd="leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK")
            cmds.setDrivenKeyframe("toerear"+eachSide+"_ik_pointConstraint1", cd="leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK")
            cmds.setDrivenKeyframe("toerear"+eachSide+"_ik", cd="leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK")
            cmds.setAttr("leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK", 1)            
            
            cmds.addAttr("heelrear"+eachSide+"IK_ctrl", ln="Stretch", at="enum",en="on:off:", k=1, nn="Stretch")



            ChildActivatedValue=2
            ChildDeactivatedValue=0
            ControllerSecondValue=1
            ControllerFirstValue=0
            Child="leg"+eachSide+"IK_jnt_cond.operation"
            Controller="heelrear"+eachSide+"IK_ctrl.Stretch"
            defaultSet=0
            getClass.controlFirstValueChildOn(Controller, 
                                              Child, 
                                              defaultSet, 
                                              ChildActivatedValue, 
                                              ChildDeactivatedValue, 
                                              ControllerSecondValue, 
                                              ControllerFirstValue)
            

                
#             ChildActivatedValue=1
#             ChildDeactivatedValue=0
#             ControllerSecondValue=1
#             ControllerFirstValue=0
#             Child="anklerear"+eachSide+"_ctrl.visibility"
#             Controller="leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK"
#             defaultSet=1
#             getClass.controlFirstValueChildOn(Controller, 
#                                                Child, 
#                                                defaultSet, 
#                                                ChildActivatedValue, 
#                                                ChildDeactivatedValue, 
#                                                ControllerSecondValue, 
#                                                ControllerFirstValue)           


            ChildActivatedValue=1
            ChildDeactivatedValue=0
            ControllerSecondValue=1
            ControllerFirstValue=0
            Child="heelrear"+eachSide+"IK_ctrl.visibility"
            Controller="leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK"
            defaultSet=0
            getClass.controlSecondValueChildOn(Controller, 
                                              Child, 
                                              defaultSet, 
                                              ChildActivatedValue, 
                                              ChildDeactivatedValue, 
                                              ControllerSecondValue, 
                                              ControllerFirstValue)

            cmds.parent("foottalus"+eachSide+"_nod_grp", "heelrear"+eachSide+"IK_ctrl" )
            cmds.parent("foottalus"+eachSide+"_ik", "anklerear"+eachSide+"IK_jnt")
            cmds.parent("heelrear"+eachSide+"IK_jnt", "heelrear"+eachSide+"IK_ctrl" )
            #cmds.parent("anklerear"+eachSide+"_jnt","foottalus"+eachSide+"_jnt")
            cmds.setAttr("leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK", 1)
            
            
            
            
            
            
            
            
            
            
            
            
            #Front
            cmds.setAttr("armcollar"+eachSide+"IK_ctrl."+eachSide+"ArmFK_IK", 1) 
            cmds.setAttr("toefront"+eachSide+"_ik.ikBlend", 1)
            cmds.setAttr("toefront"+eachSide+"_ik_pointConstraint1.toefront"+eachSide+"IK_jntW0", 1)
            cmds.setAttr("anklefront"+eachSide+"_jnt_orientConstraint1.anklefront"+eachSide+"IK_jntW0", 1)
            cmds.setDrivenKeyframe("anklefront"+eachSide+"_jnt_orientConstraint1", cd="armcollar"+eachSide+"IK_ctrl."+eachSide+"ArmFK_IK")
            cmds.setDrivenKeyframe("toefront"+eachSide+"_ik_pointConstraint1", cd="armcollar"+eachSide+"IK_ctrl."+eachSide+"ArmFK_IK")
            cmds.setDrivenKeyframe("toefront"+eachSide+"_ik", cd="armcollar"+eachSide+"IK_ctrl."+eachSide+"ArmFK_IK")
            cmds.setAttr("armcollar"+eachSide+"IK_ctrl."+eachSide+"ArmFK_IK", 0)
            cmds.setAttr("toefront"+eachSide+"_ik.ikBlend", 0)            
            cmds.setAttr("toefront"+eachSide+"_ik_pointConstraint1.toefront"+eachSide+"IK_jntW0", 0)
            cmds.setAttr("anklefront"+eachSide+"_jnt_orientConstraint1.anklefront"+eachSide+"IK_jntW0", 0)
            cmds.setDrivenKeyframe("anklefront"+eachSide+"_jnt_orientConstraint1", cd="armcollar"+eachSide+"IK_ctrl."+eachSide+"ArmFK_IK")
            cmds.setDrivenKeyframe("toefront"+eachSide+"_ik_pointConstraint1", cd="armcollar"+eachSide+"IK_ctrl."+eachSide+"ArmFK_IK")
            cmds.setDrivenKeyframe("toefront"+eachSide+"_ik", cd="armcollar"+eachSide+"IK_ctrl."+eachSide+"ArmFK_IK")
            cmds.setAttr("armcollar"+eachSide+"IK_ctrl."+eachSide+"ArmFK_IK", 1)            
            

            cmds.addAttr("heelfront"+eachSide+"IK_ctrl", ln="Stretch", at="enum",en="on:off:", k=1, nn="Stretch")



            ChildActivatedValue=2
            ChildDeactivatedValue=0
            ControllerSecondValue=1
            ControllerFirstValue=0
            Child="armshoulder"+eachSide+"IK_jnt_cond.operation"
            Controller="heelfront"+eachSide+"IK_ctrl.Stretch"
            defaultSet=0
            getClass.controlFirstValueChildOn(Controller, 
                                              Child, 
                                              defaultSet, 
                                              ChildActivatedValue, 
                                              ChildDeactivatedValue, 
                                              ControllerSecondValue, 
                                              ControllerFirstValue)
            



            ChildActivatedValue=1
            ChildDeactivatedValue=0
            ControllerSecondValue=1
            ControllerFirstValue=0
            Child="heelfront"+eachSide+"IK_ctrl.visibility"
            Controller="armcollar"+eachSide+"IK_ctrl."+eachSide+"ArmFK_IK"
            defaultSet=0
            getClass.controlSecondValueChildOn(Controller, 
                                              Child, 
                                              defaultSet, 
                                              ChildActivatedValue, 
                                              ChildDeactivatedValue, 
                                              ControllerSecondValue, 
                                              ControllerFirstValue)

            cmds.parent("armwrist"+eachSide+"_nod_grp", "armwrist"+eachSide+"_jnt" )
            cmds.parent("armwrist"+eachSide+"_ik", "anklefront"+eachSide+"IK_jnt")
            cmds.parent("heelfront"+eachSide+"IK_jnt", "heelfront"+eachSide+"IK_ctrl" )
            cmds.setAttr("armcollar"+eachSide+"IK_ctrl."+eachSide+"ArmFK_IK", 1)
            cmds.parent("armelbow"+eachSide+"_jnt_ikPole_lctr_grp", "heelfront"+eachSide+"IK_ctrl")
            
            #cmds.aimConstraint("heelrear"+eachSide+"IK_ctrl","leghip"+eachSide+"IK_grp", mo=1)
            #cmds.aimConstraint("heelrear"+eachSide+"IK_ctrl","leg"+eachSide+"IK_grp", mo=1)
#             cmds.aimConstraint("heelfront"+eachSide+"IK_ctrl","armcollar"+eachSide+"IK_grp", mo=1)
            #cmds.parent("hip"+eachSide+"_ik", "leghip"+eachSide+"IK_ctrl" )
            #cmds.parent("hip"+eachSide+"_ik", "leghip"+eachSide+"IK_ctrl")
#             cmds.setAttr("toerear"+eachSide+"IK_jnt.rotateX", lock=1)  
#             cmds.setAttr("anklerear"+eachSide+"_jnt.rotateX", lock=1)
#             cmds.setAttr("toefront"+eachSide+"IK_jnt.rotateX", lock=1)  
#             cmds.setAttr("anklefront"+eachSide+"_jnt.rotateX", lock=1)   
#             cmds.setAttr("heelfront"+eachSide+"IK_jnt.rotateX", lock=1) 
# 
#             cmds.setAttr("foottalus"+eachSide+"_jnt.rotateX", lock=1)  
#             cmds.setAttr("armwrist"+eachSide+"_jnt.rotateX", lock=1)  

#             for eachDim in DepthDimension:
#         
#                 resetOrient=[
#                              "ankle"+eachDim+eachSide+"_jnt",
#                              "heel"+eachDim+eachSide+"IK_jnt", 
#                             ]
#                             
#                 for each in resetOrient:
#                     getChildren=cmds.listRelatives(each, ad=1, typ="joint")
#                     for each in getChildren:
#                         cmds.setAttr(each+".rotateX", lock=1) 
#                         cmds.setAttr(each+".jo", lock=1)
#                     cmds.setAttr(each+".rotateX", lock=1) 
#                     cmds.setAttr(each+".jo", lock=1)

#             resetOrient=[
#                         "armcollar"+eachSide+"SH_jnt",
#                         "armcollar"+eachSide+"_jnt",
#                         "armshoulder"+eachSide+"_jnt",
#                         "armshoulder"+eachSide+"FK_jnt",
#                         "armshoulder"+eachSide+"IK_jnt"
#                         ]
#             for each in resetOrient:
#                  #cmds.joint( each, e=1, children=1, zso=1, oj='xyz', sao='yup', spa=1)        
#                  cmds.setAttr(each+".jo", lock=1)    
#                  cmds.setAttr(each+".rotateX", lock=1) 