import sys, os
filepath= os.getcwd()
sys.path.append(str(filepath))
import baseFunctions_maya
reload (baseFunctions_maya)
getClass=baseFunctions_maya.BaseClass()


import stretchIK
reload (stretchIK)
getIKClass=stretchIK.stretchIKClass()

import maya.cmds as cmds
import maya.mel

'''MG rigging modules'''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons License'
'http://creativecommons.org/licenses/by-sa/3.0/au/'

class LegRig(object):
    def __init__(self):
        #SKELETON
        getGuide=cmds.ls("*_guide")
        
        legRightFull=("legRight_guide",
                    "leghipRight_guide",             
                  "legkneeRight_guide", 
                  "foottalusRight_guide")
        legRight=("leghipRight_guide",             
                  "legkneeRight_guide", 
                  "foottalusRight_guide")
        
        getLimbs=( legRightFull) 
        
        cmds.select(cl=1)
        
        
        for item in getLimbs:
            jointSuffix='_jnt'
            getClass.rigJoints(item, jointSuffix)
        cmds.select(cl=1)
              
        for each in legRight:
            jointSuffix='FK_jnt'
            getClass.rigJoints(each, jointSuffix)          
        cmds.select(cl=1)   
              
        for each in legRight:
            jointSuffix='IK_jnt'
            getClass.rigJoints(each, jointSuffix)  
        cmds.select(cl=1)           
        
        
        cmds.mirrorJoint("legRight_jnt", myz=1, sr=("Right", "Left"))
        cmds.mirrorJoint("leghipRightIK_jnt", myz=1, sr=("Right", "Left"))
        cmds.mirrorJoint("leghipRightFK_jnt", myz=1, sr=("Right", "Left"))        
              
        resetOrient=["legLeft_jnt",
                    "legRight_jnt",
                    "leghipRightFK_jnt",
                    "leghipRightIK_jnt",
                    "leghipLeftIK_jnt",
                    "leghipLeftFK_jnt"
                    ]
        for each in resetOrient:
            cmds.joint( each, e=1, children=1, zso=1, oj='xyz', sao='yup', spa=1) 
 
        
        
        #########################################################################
        #########################################################################
        #########################################################################
        #########################################################################

        #controllers
        Side=["Right", "Left"]
        
        for eachSide in Side:
            translations=[".tx", ".ty", ".tz"] 
            rotation=[".rx", ".ry", ".rz"]
            
            jointGroup=[
                        "leghip"+eachSide,
                        "legknee"+eachSide,
                        "foottalus"+eachSide,
                        ]
                         
            cmds.group( em=True, name='IK_grp' )
            
            groupCtrls=[]             
            for eachjoint in jointGroup:
                scaleWorldMatrix = cmds.xform(eachjoint.split(eachSide)[0]+"Right_guide", q=True, r=1, s=True)
                scaleWorldMatrix=int(scaleWorldMatrix[0])                 
                eachPiece=eachjoint+"_jnt"
                name=eachjoint+"_ctrl"
                grpname=eachjoint+"_grp" 
                if "hip" in eachjoint:
                    size=12*scaleWorldMatrix
                    colour=6
                else:      
                    size=7*scaleWorldMatrix
                    colour=6  
                if "talus" in eachjoint:
                    nrx=0
                    nry=1
                    nrz=0     
                else:  
                    nrx=1
                    nry=0
                    nrz=0
                cmds.select(cl=1) 
                getTranslation, getRotation=getClass.locationXForm(eachPiece)
                getClass.buildCtrl(eachjoint, name, grpname, getTranslation, getRotation, size, colour, nrx, nry, nrz)
                colour1=18
                colour2=colour1
                colour3=colour1
                if "knee" in eachjoint:
                    pass
                else:
                    getClass.guideBuild(eachjoint, getTranslation, getRotation, colour1, colour2, colour3 )
                    getsel=cmds.ls(sl=1)
                    cmds.setAttr(getsel[0]+".overrideColor", colour1)
                    lognm=each.replace("grp", 'nod')   
                    cmds.rename(getsel[0], getsel[0]+'_nod')
                    getsel=cmds.ls(sl=1)
                    getClass.buildGrp(getsel[0])
                if "knee" in eachjoint:
                    cmds.setAttr(name+".sx" , keyable=0, lock=1)
                    cmds.setAttr(name+".sy" , keyable=0, lock=1)
                    cmds.setAttr(name+".sz", keyable=0, lock=1)                    
                    cmds.setAttr(name+".rx" , keyable=0, lock=1)
                    cmds.setAttr(name+".ry", keyable=0, lock=1)  
                    cmds.setAttr(name+".tx" , keyable=0, lock=1)
                    cmds.setAttr(name+".ty" , keyable=0, lock=1)
                    cmds.setAttr(name+".tz", keyable=0, lock=1)    
                if "hip" in eachjoint or "talus" in eachjoint:
                    cmds.setAttr(name+".sx" , keyable=0, lock=1)
                    cmds.setAttr(name+".sy" , keyable=0, lock=1)
                    cmds.setAttr(name+".sz", keyable=0, lock=1) 
                    cmds.setAttr(name+".tx" , keyable=0, lock=1)
                    cmds.setAttr(name+".ty" , keyable=0, lock=1)
                    cmds.setAttr(name+".tz", keyable=0, lock=1)                            
                
            jointGroup=[
                        "leghip"+eachSide+"",
                        "foottalus"+eachSide+"",
                        ]
            #ik
            IKHandlesLimbs=[
                            "legknee"+eachSide, 
                            "foottalus"+eachSide
                            ]

            for each in IKHandlesLimbs:
                name=each+"_jnt_ikPole_lctr"
                grpname=each+"_jnt_ikPole_lctr_grp"
                num=3*scaleWorldMatrix
                color=13                
                getTranslation=cmds.xform(each+"_jnt", q=1, t=1, ws=1)
                if "knee" in each:
                    getClass.JackI(name, grpname, num, getTranslation, (0.0,0.0,0.0), color)
                    cmds.move( 0.0, 0.0, +30.0,grpname,r=1, rpr=1)                    
                    #cmds.spaceLocator(n=each+"_jnt_ikPole_lctr", p=(getTranslation[0], getTranslation[1], getTranslation[2]+30))        
                elif "talus" in each and "Right" in each:
                    getClass.JackI(name, grpname, num, getTranslation, (0.0,0.0,0.0), color)
                    cmds.move( -40.0, 0.0, +30.0,grpname,r=1, rpr=1)                     
                    #cmds.spaceLocator(n=each+"_jnt_ikPole_lctr", p=(getTranslation[0]-40, getTranslation[1], getTranslation[2]))       
                elif "talus" in each and "Left" in each:
                    getClass.JackI(name, grpname, num, getTranslation, (0.0,0.0,0.0), color)
                    cmds.move( 40.0, 0.0, +30.0,grpname,r=1, rpr=1)                     
                    #cmds.spaceLocator(n=each+"_jnt_ikPole_lctr", p=(getTranslation[0]+40, getTranslation[1], getTranslation[2]))
                else:
                    getClass.JackI(name, grpname, num, getTranslation, (0.0,0.0,0.0), color)                   
                    #cmds.spaceLocator(n=each+"_jnt_ikPole_lctr", p=(getTranslation[0], getTranslation[1], getTranslation[2]))
#                 cmds.setAttr(each+"_jnt_ikPole_lctr"+"Shape.overrideEnabled", 1)
#                 cmds.setAttr(each+"_jnt_ikPole_lctr"+"Shape.overrideColor", 13)
#                 cmds.setAttr(each+"_jnt_ikPole_lctr"+"Shape.localScaleX", 3)
#                 cmds.setAttr(each+"_jnt_ikPole_lctr"+"Shape.localScaleY", 3) 
#                 cmds.setAttr(each+"_jnt_ikPole_lctr"+"Shape.localScaleZ", 3) 
#                 cmds.CenterPivot()
#                 cmds.group(n=each+"_jnt_ikPole_lctr"+"_grp")
                getTranslation=cmds.xform(each+"_jnt", q=1, t=1, ws=1)
                cmds.move(getTranslation[0], getTranslation[1], getTranslation[2],each+"_jnt_ikPole_lctr"+"_grp"+".rotatePivot", ws=1, rpr=1 )
                if 'talus' in each:
                     cmds.setAttr(each+"_jnt_ikPole_lctr.visibility", 0)

            cmds.ikHandle(n="foottalus"+eachSide+"_ik", sj="leghip"+eachSide+"IK_jnt", ee="foottalus"+eachSide+"IK_jnt", sol="ikRPsolver")
            cmds.setAttr("foottalus"+eachSide+"_ik.visibility", 0)

            #connect
            
            cmds.addAttr("leghip"+eachSide+"_ctrl", ln=eachSide+"LegFK_IK",  min=0, max=1, at="double", en="FK:IK:", k=1, nn=eachSide+"LegFK_IK")
            cmds.setAttr("leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK", 1)
            
            Controller="leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK"
            bodyskel=[
                      "leghip"+eachSide,
                        "legknee"+eachSide,
                        "foottalus"+eachSide
                        ]
            for each in bodyskel:
                getClass.blendColors(each, Controller)  

            
            
            ########
            #Parenting controllers
            ######## 
            
            cmds.parent("legknee"+eachSide+"_grp ", "leghip"+eachSide+"_ctrl")
            
            cmds.parent("foottalus"+eachSide+"_grp", "legknee"+eachSide+"_ctrl")
            
            
            ########LEGS
            #Connect Blender Controls for IK/FK switch
            ########
            
            #cmds.parent("leghip"+eachSide+"FK_jnt", "leghip"+eachSide+"_ctrl")
            cmds.connectAttr ("leghip"+eachSide+"_ctrl.rotate","leghip"+eachSide+"FK_jnt.rotate", f=1)
            cmds.connectAttr ("legknee"+eachSide+"_ctrl.rotate","legknee"+eachSide+"FK_jnt.rotate", f=1)
            cmds.connectAttr ("foottalus"+eachSide+"_ctrl.rotate","foottalus"+eachSide+"FK_jnt.rotate", f=1)
            
            cmds.connectAttr("legknee"+eachSide+"_jnt_ikPole_lctr.translateX", "foottalus"+eachSide+"_jnt_ikPole_lctr_grp.rotateY", f=1)

            
            cmds.poleVectorConstraint("legknee"+eachSide+"_jnt_ikPole_lctr", "foottalus"+eachSide+"_ik")  

            #set visibility
            ChildActivatedValue=1
            ChildDeactivatedValue=0
            ControllerSecondValue=1
            ControllerFirstValue=0
            Children=["legknee"+eachSide+"_ctrl.visibility", 
                      "foottalus"+eachSide+"_ctrl.visibility", 
                      "leghip"+eachSide+"_ctrl.visibility"]
            Controller="leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK"
            defaultSet=0
            for eachChild in Children:
                getClass.controlFirstValueChildOn(Controller, 
                                                  eachChild, 
                                                  defaultSet, 
                                                  ChildActivatedValue, 
                                                  ChildDeactivatedValue, 
                                                  ControllerSecondValue, 
                                                  ControllerFirstValue)


            ChildActivatedValue=1
            ChildDeactivatedValue=0
            ControllerSecondValue=1
            ControllerFirstValue=0
            Child="legknee"+eachSide+"_jnt_ikPole_lctr.visibility"
            Controller="leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK"
            defaultSet=1
            getClass.controlSecondValueChildOn(Controller, 
                                               Child, 
                                               defaultSet, 
                                               ChildActivatedValue, 
                                               ChildDeactivatedValue, 
                                               ControllerSecondValue, 
                                               ControllerFirstValue)
           

            cmds.parent("foottalus"+eachSide+"_ik", "foottalus"+eachSide+"_nod")
            cmds.parent("legknee"+eachSide+"_jnt_ikPole_lctr_grp", "foottalus"+eachSide+"_nod")

            cmds.parent("leg"+eachSide+"_jnt", "leghip"+eachSide+"_nod")
            cmds.parent("leghip"+eachSide+"_ctrl", "leghip"+eachSide+"_nod")
            #cmds.parent("leghip"+eachSide+"IK_jnt", "leghip"+eachSide+"_nod")
            #cmds.parent("leghip"+eachSide+"_jnt", "leghip"+eachSide+"_nod")
            cmds.parent("leghip"+eachSide+"_grp", "leghip"+eachSide+"_nod")
            #cmds.pointConstraint("leghip"+eachSide+"FK_jnt", "leghip"+eachSide+"_ctrl")

            getIKClass.stretch("leghip"+eachSide+"IK_jnt")

