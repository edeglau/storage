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

#JOINTS
class ToeAddition(object):
    def __init__(self):

        getToes=cmds.ls("toeTipFrontRight_jnt", "toeTipFrontLeft_jnt", "toeTipRearRight_jnt", "toeTipRearLeft_jnt")
        
        createNewIK =["toefrontRight_jnt", "toefrontLeft_jnt", "toerearRight_jnt", "toerearLeft_jnt"]    
        for each, item in map(None, createNewIK, getToes) :
            cmds.ikHandle(n=each.split("_jnt")[0]+"_Tip_ik", sj=each, ee=item, sol="ikRPsolver")
        
        colour=6
        selection=["toefrontRight_Tip_ik", "toefrontLeft_Tip_ik", "toerearRight_Tip_ik", "toerearLeft_Tip_ik"]
        getClass.getLoc(selection, colour)
        newParent=cmds.ls(sl=1)
        cmds.delete("heelfrontRightIK_jnt_parentConstraint1")
        cmds.parentConstraint("toefrontRight_Tip_ik_loc_lctr", "heelfrontRightIK_jnt", mo=1)
        #cmds.parent("armelbowRight_jnt_ikPole_lctr_grp", "toefrontRight_Tip_ik_loc_lctr")
        cmds.parent("toefrontRight_Tip_ik", "toefrontRight_Tip_ik_loc_lctr")
        cmds.parent("toefrontRight_Tip_ik_loc_lctr_grp", "Armwrist_offset_IK_R_Ctrl")
        #cmds.parent("armwristRight_offset_IK_grp", "Wrist_R_Ctrl") 
        cmds.connectAttr("heelfrontRightIK_ctrl.TipToe", "toefrontRightIK_jnt.rotateZ", f=1)
        cmds.connectAttr("heelfrontRightIK_ctrl.RaiseHeel", "toefrontRight_Tip_ik_loc_lctr.rotateX", f=1)
        cmds.connectAttr("heelfrontRightIK_ctrl.PivotToe", "toefrontRight_Tip_ik_loc_lctr.rotateY", f=1)
        cmds.addAttr("heelfrontRightIK_ctrl", ln="SwivelToe", at="long", min=-90, max=90, dv=0, k=1, nn="SwivelToe") 
        cmds.connectAttr("heelfrontRightIK_ctrl.SwivelToe", "toefrontRight_Tip_ik_loc_lctr.rotateZ", f=1)             
        cmds.setAttr("heelfrontRightIK_ctrl.SwivelHeel", cb=0, k=0)
        #cmds.addAttr("heelfrontRightIK_ctrl", ln="RaiseToe", at="long", min=-90, max=90, dv=0, k=1, nn="RaiseToe") 
        cmds.connectAttr("heelfrontRightIK_ctrl.RaiseToe", "toefrontRight_Tip_ik.translateY", f=1)    
        
        cmds.delete("heelfrontLeftIK_jnt_parentConstraint1")        
        cmds.parentConstraint("toefrontLeft_Tip_ik_loc_lctr", "heelfrontLeftIK_jnt", mo=1)
        #cmds.parent("armelbowLeft_jnt_ikPole_lctr_grp", "toefrontLeft_Tip_ik_loc_lctr")
        cmds.parent("toefrontLeft_Tip_ik", "toefrontLeft_Tip_ik_loc_lctr")
        cmds.parent("toefrontLeft_Tip_ik_loc_lctr_grp", "Armwrist_offset_IK_L_Ctrl") 
        #cmds.parent("armwristLeft_offset_IK_grp", "Wrist_L_Ctrl") 
        cmds.connectAttr("heelfrontLeftIK_ctrl.TipToe", "toefrontLeftIK_jnt.rotateZ", f=1)
        cmds.connectAttr("heelfrontLeftIK_ctrl.RaiseHeel", "toefrontLeft_Tip_ik_loc_lctr.rotateX", f=1)
        cmds.connectAttr("heelfrontLeftIK_ctrl.PivotToe", "toefrontLeft_Tip_ik_loc_lctr.rotateY", f=1)
        cmds.addAttr("heelfrontLeftIK_ctrl", ln="SwivelToe", at="long", min=-90, max=90, dv=0, k=1, nn="SwivelToe") 
        cmds.connectAttr("heelfrontLeftIK_ctrl.SwivelToe", "toefrontLeft_Tip_ik_loc_lctr.rotateZ", f=1)        
        cmds.setAttr("heelfrontLeftIK_ctrl.SwivelHeel", cb=0, k=0)
        #cmds.addAttr("heelfrontLeftIK_ctrl", ln="RaiseToe", at="long", min=-90, max=90, dv=0, k=1, nn="RaiseToe") 
        cmds.connectAttr("heelfrontLeftIK_ctrl.RaiseToe", "toefrontLeft_Tip_ik.translateY", f=1)    
        
        
        cmds.delete("heelrearRightIK_jnt_parentConstraint1")
        cmds.parentConstraint("toerearRight_Tip_ik_loc_lctr", "heelrearRightIK_jnt", mo=1)
        cmds.parent("toerearRight_Tip_ik_loc_lctr_grp", "foottalusRight_nod") 
        cmds.parent("foottalusRight_nod_grp", "Main_Ctrl") 
        #cmds.parent("foottalusRight_nod_grp", "toerearRight_Tip_ik_loc_lctr")
        cmds.parent("legkneeRight_jnt_ikPole_lctr_grp", "heelrearRightIK_ctrl")
        cmds.parent("heelrearRightIK_jnt", "toerearRight_Tip_ik_loc_lctr")
        #cmds.parent("toerearRight_Tip_ik_loc_lctr", "heelrearRightIK_ctrl")
        cmds.parent("toerearRight_Tip_ik", "toerearRight_Tip_ik_loc_lctr")
        #cmds.parent("toerearRight_Tip_ik_loc_lctr", "foottalusRight_nod")
        #cmds.parent("foottalusRight_nod_grp", "Talus_R_Ctrl")
        cmds.connectAttr("heelrearRightIK_ctrl.TipToe", "toerearRightIK_jnt.rotateZ", f=1)
        cmds.connectAttr("heelrearRightIK_ctrl.RaiseHeel", "toerearRight_Tip_ik_loc_lctr.rotateX", f=1)
        cmds.connectAttr("heelrearRightIK_ctrl.PivotToe", "toerearRight_Tip_ik_loc_lctr.rotateY", f=1)
        cmds.addAttr("heelrearRightIK_ctrl", ln="SwivelToe", at="long", min=-90, max=90, dv=0, k=1, nn="SwivelToe") 
        cmds.connectAttr("heelrearRightIK_ctrl.SwivelToe", "toerearRight_Tip_ik_loc_lctr.rotateZ", f=1)
        cmds.setAttr("heelrearRightIK_ctrl.SwivelHeel", cb=0, k=0)
        #cmds.addAttr("heelrearRightIK_ctrl", ln="RaiseToe", at="long", min=-90, max=90, dv=0, k=1, nn="RaiseToe") 
        cmds.connectAttr("heelrearRightIK_ctrl.RaiseToe", "toerearRight_Tip_ik.translateY", f=1)
         
        cmds.delete("heelrearLeftIK_jnt_parentConstraint1")
        cmds.parentConstraint("toerearLeft_Tip_ik_loc_lctr", "heelrearLeftIK_jnt", mo=1)
        cmds.parent("toerearLeft_Tip_ik_loc_lctr_grp", "foottalusLeft_nod") 
        cmds.parent("foottalusLeft_nod_grp", "Main_Ctrl") 
        #cmds.parent("foottalusLeft_nod_grp", "toerearLeft_Tip_ik_loc_lctr")
        cmds.parent("legkneeLeft_jnt_ikPole_lctr_grp", "heelrearLeftIK_ctrl")
        cmds.parent("heelrearLeftIK_jnt", "toerearLeft_Tip_ik_loc_lctr")
        #cmds.parent("toerearLeft_Tip_ik_loc_lctr", "heelrearLeftIK_ctrl")
        cmds.parent("toerearLeft_Tip_ik", "toerearLeft_Tip_ik_loc_lctr")
        #cmds.parent("toerearLeft_Tip_ik_loc_lctr", "foottalusLeft_nod")
        #cmds.parent("foottalusLeft_nod_grp", "Talus_L_Ctrl")
        cmds.connectAttr("heelrearLeftIK_ctrl.TipToe", "toerearLeftIK_jnt.rotateZ", f=1)
        cmds.connectAttr("heelrearLeftIK_ctrl.RaiseHeel", "toerearLeft_Tip_ik_loc_lctr.rotateX", f=1)
        cmds.connectAttr("heelrearLeftIK_ctrl.PivotToe", "toerearLeft_Tip_ik_loc_lctr.rotateY", f=1)
        cmds.addAttr("heelrearLeftIK_ctrl", ln="SwivelToe", at="long", min=-90, max=90, dv=0, k=1, nn="SwivelToe") 
        cmds.connectAttr("heelrearLeftIK_ctrl.SwivelToe", "toerearLeft_Tip_ik_loc_lctr.rotateZ", f=1)
        #cmds.setAttr("heelrearLeftIK_ctrl.SwivelHeel", cb=0, k=0)
        #cmds.addAttr("heelrearLeftIK_ctrl", ln="RaiseToe", at="long", min=-90, max=90, dv=0, k=1, nn="RaiseToe") 
        cmds.connectAttr("heelrearLeftIK_ctrl.RaiseToe", "toerearLeft_Tip_ik.translateY", f=1)
        
        selection=["heelfrontRightIK_ctrl",
        #"heelrearRightIK_ctrl",
        #"heelrearLeftIK_ctrl",
        "heelfrontLeftIK_ctrl"
        ]
        for each in selection:
                size=2
                colour=22
                nrx=0
                nry=1
                nrz=0      
                name=each.split("_ctrl")[0]+"_pvt"     
                grpname=each.split("_ctrl")[0]+"_pvt_grp"  
                transformWorldMatrix, rotateWorldMatrix=getClass.locationXForm(each)
                getClass.buildCtrl(each, name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)    
                cmds.parent(grpname, each)
        
        
        
        
        
        cmds.delete("heelfrontLeftIK_jnt_parentConstraint1")
        
        cmds.parentConstraint("heelfrontLeftIK_ctrl", "armwristLeft_offset_IK_grp", mo=1)
        cmds.parentConstraint("Wrist_L_Ctrl", "armwristLeft_offset_IK_grp", mo=1)
        
        cmds.setAttr("Armcollar_IK_L_Ctrl.LeftArmFK_IK", 1)     
        cmds.setAttr("armwristLeft_offset_IK_grp_parentConstraint1.heelfrontLeftIK_ctrlW0", 1)
        cmds.setAttr("armwristLeft_offset_IK_grp_parentConstraint1.Wrist_L_CtrlW1", 0)
        cmds.setDrivenKeyframe("armwristLeft_offset_IK_grp_parentConstraint1", cd="Armcollar_IK_L_Ctrl.LeftArmFK_IK")
        cmds.setAttr("Armcollar_IK_L_Ctrl.LeftArmFK_IK", 0)     
        cmds.setAttr("armwristLeft_offset_IK_grp_parentConstraint1.heelfrontLeftIK_ctrlW0", 0)
        cmds.setAttr("armwristLeft_offset_IK_grp_parentConstraint1.Wrist_L_CtrlW1", 1)
        cmds.setDrivenKeyframe("armwristLeft_offset_IK_grp_parentConstraint1", cd="Armcollar_IK_L_Ctrl.LeftArmFK_IK")
        cmds.setAttr("Armcollar_IK_L_Ctrl.LeftArmFK_IK", 1)
        getTranslate=cmds.xform("toefrontLeft_Tip_ik_loc_lctr_grp", q=1, r=1, t=1)
        cmds.move(getTranslate[0], 0, getTranslate[2], "heelfrontLeftIK_pvt.rotatePivot" ,r=1, rpr=1 )
        cmds.parent("heelfrontLeftIK_jnt", "heelfrontLeftIK_pvt")
        
        
        cmds.connectAttr("heelfrontLeftIK_ctrl.RaiseHeel", "heelfrontLeftIK_pvt.rotateX", f=1)
        cmds.connectAttr("heelfrontLeftIK_ctrl.PivotToe", "heelfrontLeftIK_pvt.rotateY", f=1)
        cmds.setAttr("heelfrontLeftIK_ctrl.SwivelToe", cb=0, k=0)
        cmds.setAttr("heelfrontLeftIK_ctrl.RaiseToe", cb=0, k=0)
        
        
        getShapes=[(each) for each in cmds.listRelatives("heelfrontLeftIK_pvt", typ="shape")]
        cmds.setAttr(getShapes[0]+".visibility", 0)
        
        
        cmds.delete("heelfrontRightIK_jnt_parentConstraint1")
        
        cmds.parentConstraint("heelfrontRightIK_ctrl", "armwristRight_offset_IK_grp", mo=1)
        cmds.parentConstraint("Wrist_R_Ctrl", "armwristRight_offset_IK_grp", mo=1)
        
        cmds.setAttr("Armcollar_IK_R_Ctrl.RightArmFK_IK", 1)     
        cmds.setAttr("armwristRight_offset_IK_grp_parentConstraint1.heelfrontRightIK_ctrlW0", 1)
        cmds.setAttr("armwristRight_offset_IK_grp_parentConstraint1.Wrist_R_CtrlW1", 0)
        cmds.setDrivenKeyframe("armwristRight_offset_IK_grp_parentConstraint1", cd="Armcollar_IK_R_Ctrl.RightArmFK_IK")
        cmds.setAttr("Armcollar_IK_R_Ctrl.RightArmFK_IK", 0)     
        cmds.setAttr("armwristRight_offset_IK_grp_parentConstraint1.heelfrontRightIK_ctrlW0", 0)
        cmds.setAttr("armwristRight_offset_IK_grp_parentConstraint1.Wrist_R_CtrlW1", 1)
        cmds.setDrivenKeyframe("armwristRight_offset_IK_grp_parentConstraint1", cd="Armcollar_IK_R_Ctrl.RightArmFK_IK")
        cmds.setAttr("Armcollar_IK_R_Ctrl.RightArmFK_IK", 1)
        
        getTranslate=cmds.xform("toefrontRight_Tip_ik_loc_lctr_grp", q=1, r=1, t=1)
        cmds.move(getTranslate[0], 0, getTranslate[2], "heelfrontRightIK_pvt.rotatePivot" ,r=1, rpr=1 )
        cmds.parent("heelfrontRightIK_jnt", "heelfrontRightIK_pvt")
        
        cmds.connectAttr("heelfrontRightIK_ctrl.RaiseHeel", "heelfrontRightIK_pvt.rotateX", f=1)
        cmds.connectAttr("heelfrontRightIK_ctrl.PivotToe", "heelfrontRightIK_pvt.rotateY", f=1)
        cmds.setAttr("heelfrontRightIK_ctrl.SwivelToe", cb=0, k=0)
        cmds.setAttr("heelfrontRightIK_ctrl.RaiseToe", cb=0, k=0)
        
        
        getShapes=[(each) for each in cmds.listRelatives("heelfrontRightIK_pvt", typ="shape")]
        cmds.setAttr(getShapes[0]+".visibility", 0)
        

        cmds.parentConstraint("heelrearLeftIK_ctrl", "foottalusLeft_nod_grp", mo=1)
        cmds.parentConstraint("Talus_L_Ctrl", "foottalusLeft_nod_grp", mo=1)
        
        cmds.setAttr("Hips_Ctrl.LegLeftFK_IK", 1)     
        cmds.setAttr("foottalusLeft_nod_grp_parentConstraint1.heelrearLeftIK_ctrlW0", 1)
        cmds.setAttr("foottalusLeft_nod_grp_parentConstraint1.Talus_L_CtrlW1", 0)
        cmds.setDrivenKeyframe("foottalusLeft_nod_grp_parentConstraint1", cd="Hips_Ctrl.LegLeftFK_IK")
        cmds.setAttr("Hips_Ctrl.LegLeftFK_IK", 0)     
        cmds.setAttr("foottalusLeft_nod_grp_parentConstraint1.heelrearLeftIK_ctrlW0", 0)
        cmds.setAttr("foottalusLeft_nod_grp_parentConstraint1.Talus_L_CtrlW1", 1)
        cmds.setDrivenKeyframe("foottalusLeft_nod_grp_parentConstraint1", cd="Hips_Ctrl.LegLeftFK_IK")
        cmds.setAttr("Hips_Ctrl.LegLeftFK_IK", 1) 
        
        cmds.setAttr("heelrearLeftIK_ctrl.SwivelToe", cb=0, k=0)
        cmds.setAttr("heelrearLeftIK_ctrl.RaiseToe", cb=0, k=0)

        
        cmds.parentConstraint("heelrearRightIK_ctrl", "foottalusRight_nod_grp", mo=1)
        cmds.parentConstraint("Talus_R_Ctrl", "foottalusRight_nod_grp", mo=1)
        
        cmds.setAttr("Hips_Ctrl.LegRightFK_IK", 1)     
        cmds.setAttr("foottalusRight_nod_grp_parentConstraint1.heelrearRightIK_ctrlW0", 1)
        cmds.setAttr("foottalusRight_nod_grp_parentConstraint1.Talus_R_CtrlW1", 0)
        cmds.setDrivenKeyframe("foottalusRight_nod_grp_parentConstraint1", cd="Hips_Ctrl.LegRightFK_IK")
        cmds.setAttr("Hips_Ctrl.LegRightFK_IK", 0)     
        cmds.setAttr("foottalusRight_nod_grp_parentConstraint1.heelrearRightIK_ctrlW0", 0)
        cmds.setAttr("foottalusRight_nod_grp_parentConstraint1.Talus_R_CtrlW1", 1)
        cmds.setDrivenKeyframe("foottalusRight_nod_grp_parentConstraint1", cd="Hips_Ctrl.LegRightFK_IK")
        cmds.setAttr("Hips_Ctrl.LegRightFK_IK", 1) 
        
        cmds.setAttr("heelrearRightIK_ctrl.SwivelToe", cb=0, k=0)
        #cmds.setAttr("heelrearRightIK_ctrl.RaiseToe", cb=0, k=0)
        
        
        getCollection=[
                    "Armwrist_offset_IK_L_Ctrl",
                    "Armwrist_offset_IK_R_Ctrl",
                    "toefrontLeft_Tip_ik_loc_lctr",
                    "toefrontRight_Tip_ik_loc_lctr",
                    "toerearRight_Tip_ik_loc_lctr",
                    "toerearLeft_Tip_ik_loc_lctr",
                    "foottalusLeft_nod",
                    "foottalusRight_nod",
                    "armwristLeft_nod",
                    "armwristRight_nod"]
        for each in getCollection:
            getChildForIK=cmds.listRelatives(each, ad=1, typ="shape")
            for item in getChildForIK:
                cmds.setAttr(item+".visibility", 0)

#         getSel=("heelfrontLeftIK_ctrl",
#         "heelfrontRightIK_ctrl",
#         "heelrearRightIK_ctrl",
#         "heelrearLeftIK_ctrl")
#         for each in getSel:
#             cmds.sets(each, include="BodyControllers")
#             lognm=each.replace("_ctrl", '_Ctrl')
#             getnewname=lognm.replace("_jnt", "")
#             getcleanname=getnewname.replace("ikPole", "PoleVector")
#             getFullName=getcleanname.replace("heel", "Heel_")
#             #capitalString=getFullName.capitalize()
#             if "Right" in each:
#                 getPartname=getFullName.replace("Right", "_R_")
#             else:
#                 getPartname=getFullName.replace("Left", "_L_")
#             print getPartname
#             cmds.rename(each, getPartname)                 
