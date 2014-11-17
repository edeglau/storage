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

import maya.cmds as cmds
import maya.mel


class FootConn(object):
    def __init__(self):
        
        Side=["Right", "Left"]
        
        for eachSide in Side:
            
            
            cmds.parent("footankle"+eachSide+"IK_jnt", "foottalus"+eachSide+"IK_jnt" )
            cmds.parent("footankle"+eachSide+"FK_jnt", "foottalus"+eachSide+"FK_jnt" )
        
            cmds.setAttr("leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK", 1)     
            cmds.setAttr("footankle"+eachSide+"_jnt_orientConstraint1.footankle"+eachSide+"IK_jntW0", 1)
            cmds.setAttr("footankle"+eachSide+"_jnt_orientConstraint1.footankle"+eachSide+"FK_jntW1", 0)
            cmds.setDrivenKeyframe("footankle"+eachSide+"_jnt_orientConstraint1", cd="leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK")
            cmds.setAttr("leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK", 0)
            cmds.setAttr("footankle"+eachSide+"_jnt_orientConstraint1.footankle"+eachSide+"IK_jntW0", 0)
            cmds.setAttr("footankle"+eachSide+"_jnt_orientConstraint1.footankle"+eachSide+"FK_jntW1", 1)
            cmds.setDrivenKeyframe("footankle"+eachSide+"_jnt_orientConstraint1", cd="leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK")
            cmds.setAttr("leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK", 1)            
            
            cmds.addAttr("footheel"+eachSide+"IK_ctrl", ln="Stretch", at="enum",en="on:off:", k=1, nn="Stretch")
            
            
            cmds.setAttr("football"+eachSide+"IK_jnt.rotateX", lock=1)  
            cmds.setAttr("football"+eachSide+"FK_jnt.rotateX", lock=1)
            cmds.setAttr("football"+eachSide+"_jnt.rotateX", lock=1)
#             children=("football"+eachSide+"_jnt.rotateX",
# #                     "footheel"+eachSide+"_jnt.jointOrientX", 
# #                     "footheel"+eachSide+"_jnt.jointOrientY", 
# #                     "footheel"+eachSide+"_jnt.jointOrientZ",
# #                     "footankle"+eachSide+"_jnt.jointOrientX", 
# #                     "footankle"+eachSide+"_jnt.jointOrientY", 
# #                     "footankle"+eachSide+"_jnt.jointOrientZ",                    
# #                     "football"+eachSide+"_jnt.jointOrientX", 
# #                     "football"+eachSide+"_jnt.jointOrientY", 
# #                     "football"+eachSide+"_jnt.jointOrientZ",
# #                       "foottoe"+eachSide+"_jnt.jointOrientX", 
# #                       "foottoe"+eachSide+"_jnt.jointOrientY", 
# #                       "foottoe"+eachSide+"_jnt.jointOrientZ"
#                       )
#             ChildActivatedValue=0
#             ChildDeactivatedValue=0
#             ControllerSecondValue=1
#             ControllerFirstValue=0
#             Controller="leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK"
#             defaultSet=0
#             for Child in children:
#                 getClass.controlFirstValueChildOn(Controller, 
#                                                   Child, 
#                                                   defaultSet, 
#                                                   ChildActivatedValue, 
#                                                   ChildDeactivatedValue, 
#                                                   ControllerSecondValue, 
#                                                   ControllerFirstValue)


            ChildActivatedValue=2
            ChildDeactivatedValue=0
            ControllerSecondValue=1
            ControllerFirstValue=0
            Child="leghip"+eachSide+"IK_jnt_cond.operation"
            Controller="footheel"+eachSide+"IK_ctrl.Stretch"
            defaultSet=0
            getClass.controlFirstValueChildOn(Controller, 
                                              Child, 
                                              defaultSet, 
                                              ChildActivatedValue, 
                                              ChildDeactivatedValue, 
                                              ControllerSecondValue, 
                                              ControllerFirstValue)
            



            Controller="leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK"
            bodyskel=["footankle"+eachSide,
                        "football"+eachSide,
                        "foottoe"+eachSide,
                        "footheel"+eachSide,
                        ]
            for each in bodyskel:
                getClass.blendColors(each, Controller)

                
            ChildActivatedValue=1
            ChildDeactivatedValue=0
            ControllerSecondValue=1
            ControllerFirstValue=0
            Child="football"+eachSide+"_ctrl.visibility"
            Controller="leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK"
            defaultSet=1
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
            Child="footheel"+eachSide+"IK_ctrl.visibility"
            Controller="leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK"
            defaultSet=0
            getClass.controlSecondValueChildOn(Controller, 
                                              Child, 
                                              defaultSet, 
                                              ChildActivatedValue, 
                                              ChildDeactivatedValue, 
                                              ControllerSecondValue, 
                                              ControllerFirstValue)

#             cmds.setAttr("football"+eachSide+"_ctrl.visibility", 0)
#             cmds.setDrivenKeyframe("football"+eachSide+"_ctrl.visibility", cd="leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK")
#             cmds.setAttr("leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK", 0)
#             cmds.setAttr("football"+eachSide+"_ctrl.visibility", 1)
#             cmds.setDrivenKeyframe("football"+eachSide+"_ctrl.visibility", cd="leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK")
#             cmds.setAttr("leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK", 1)
        
#             
#             cmds.setAttr("footheel"+eachSide+"IK_ctrl.visibility", 1)
#             cmds.setDrivenKeyframe("footheel"+eachSide+"IK_ctrl.visibility", cd="leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK")
#             cmds.setAttr("leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK", 0)
#             cmds.setAttr("footheel"+eachSide+"IK_ctrl.visibility", 0)
#             cmds.setDrivenKeyframe("footheel"+eachSide+"IK_ctrl.visibility", cd="leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK")
#             cmds.setAttr("leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK", 1)
            
            #cmds.parent("foottalus"+eachSide+"_nod", "foottalus"+eachSide+"_jnt") 
            cmds.parent("foottalus"+eachSide+"_nod_grp", "footheel"+eachSide+"IK_ctrl" )
            cmds.parent("footankle"+eachSide+"IK_jnt", "footankle"+eachSide+"RFL_jnt")
            cmds.parentConstraint("foottalus"+eachSide+"_ctrl", "footankle"+eachSide+"FK_jnt", mo=1, w=1)
            cmds.parent("foottalus"+eachSide+"_ik", "footankle"+eachSide+"RFL_jnt")
            cmds.parent(" foot"+eachSide+"RFL_jnt", "footheel"+eachSide+"IK_ctrl" )
            cmds.parent("footankle"+eachSide+"_jnt","foottalus"+eachSide+"_jnt")
            cmds.parent("football"+eachSide+"_grp", "foottalus"+eachSide+"_ctrl" )
            cmds.setAttr("leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK", 1)