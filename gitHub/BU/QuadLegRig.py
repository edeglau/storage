import os
import sys
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
        winName = "Size set"
        global typeMenu
        winTitle = winName
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)

#         self.window = cmds.window(self.winName, title=self.winTitle, tbm=1, w=150, h=100 )
        window = cmds.window(winName, title=winTitle, tbm=1, w=250, h=100 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=250)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        
        cmds.rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(100, 20))
        typeMenu=cmds.optionMenu( label='ctrl size')
        cmds.menuItem( label="Large" )
        cmds.menuItem( label="Med" )
        cmds.menuItem( label="Small" )           
        cmds.button (label='Change Selection', p='listBuildButtonLayout', command = lambda *args:self.controllerSize())
        cmds.showWindow(window)    
    def controllerSize(self):
        queryType=cmds.optionMenu(typeMenu, q=1, sl=1)
        if queryType==1:
            controlSize=[20, 15, 3]
            controlDist=[30.0, 40.0]
        elif queryType==2:
            controlSize=[15, 10, 2]
            controlDist=[15.0, 20.0]
        elif queryType==3:
            controlSize=[4, 3, 1]
            controlDist=[5.0, 10.0]
        self.createLimb(controlSize, controlDist)
        
    def createLimb(self, controlSize, controlDist):
        #SKELETON
        getGuide=cmds.ls("*_guide")
        
        legRightFull=("legRight_guide",
                    "leghipRight_guide",             
                  "legkneeRight_guide", 
                  "foottalusRight_guide")
        
        legRight=("leghipRight_guide",             
                  "legkneeRight_guide", 
                  "foottalusRight_guide")
        
        
        cmds.select(cl=1)
        
        
        for each in legRightFull:
            jointSuffix='_jnt'
            getClass.rigJoints(each, jointSuffix)
        cmds.select(cl=1)
              
        for each in legRightFull:
            jointSuffix='FK_jnt'
            getClass.rigJoints(each, jointSuffix)          
        cmds.select(cl=1)   
              
        for each in legRightFull:
            jointSuffix='IK_jnt'
            getClass.rigJoints(each, jointSuffix)  
        cmds.select(cl=1)           
        
        
        cmds.mirrorJoint("legRight_jnt", myz=1, sr=("Right", "Left"))
        cmds.mirrorJoint("legRightIK_jnt", myz=1, sr=("Right", "Left"))
        cmds.mirrorJoint("legRightFK_jnt", myz=1, sr=("Right", "Left"))        
              
        resetOrient=["legLeft_jnt",
                    "legRight_jnt",
                    "legRightFK_jnt",
                    "legRightIK_jnt",
                    "legLeftIK_jnt",
                    "legLeftFK_jnt"
                    ]
        for each in resetOrient:
            cmds.joint( each, e=1, children=1, zso=1, oj='xyz', sao='yup', spa=1) 
 
        
        
        #########################################################################
        #########################################################################
        #########################################################################
        #########################################################################

        #CONTROLLER
        
        Side=["Right", "Left"]
        
        for eachSide in Side:
            translations=[".tx", ".ty", ".tz"] 
            rotation=[".rx", ".ry", ".rz"]
            
#             #build IK controller for hip
#             IkControllers=("leg"+eachSide+"IK_jnt", 
#                            #"leghip"+eachSide+"IK_jnt"
#                            )
#             for eachjoint in IkControllers:
#                 name=eachjoint.split("_jnt")[0]+"_ctrl"
#                 grpname=eachjoint.split("_jnt")[0]+"_grp"
#                 size=20
#                 colour=13              
#                 nrx=1
#                 nry=0
#                 nrz=0               
#                 getTranslation, getRotation=getClass.locationXForm(eachjoint)
#                 getClass.buildCtrl(eachjoint, name, grpname, getTranslation, getRotation, size, colour, nrx, nry, nrz)
            
            jointGroup=["leg"+eachSide,
                        "leghip"+eachSide,
                        "legknee"+eachSide,
                        "foottalus"+eachSide,
                        ]
                         
            cmds.group( em=True, name='IK_grp' )
            
            #build FK controllers
            groupCtrls=[]
            for eachjoint in jointGroup:
                eachPiece=eachjoint+"_jnt"
                name=eachjoint+"_ctrl"
                grpname=eachjoint+"_grp" 
                if "hip" in eachjoint:
                    size=controlSize[1]
                    colour=6
                else:      
                    size=controlSize[0]
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
                if "knee" in eachjoint or "hip" in eachjoint:
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
                if "hip" in eachjoint or "talus" in eachjoint:
                    cmds.setAttr(name+".sx" , keyable=0, lock=1)
                    cmds.setAttr(name+".sy" , keyable=0, lock=1)
                    cmds.setAttr(name+".sz", keyable=0, lock=1) 

                
            jointGroup=[
                        "leghip"+eachSide,
                        "foottalus"+eachSide,
                        ]
            #IK POLE VECTORS
            IKHandlesLimbs=[
                            "legknee"+eachSide, 
                            "foottalus"+eachSide
                            ]

            for each in IKHandlesLimbs:
                name=each+"_jnt_ikPole_lctr"
                grpname=each+"_jnt_ikPole_lctr_grp"
                num=controlSize[2]
                color=13                
                getTranslation=cmds.xform(each+"_jnt", q=1, t=1, ws=1)
                if "knee" in each:
                    getClass.JackI(name, grpname, num, getTranslation, (0.0,0.0,0.0), color)
                    cmds.move( 0.0, 0.0, -controlDist[0],grpname,r=1, rpr=1)                    
                elif "talus" in each and "Right" in each:
                    getClass.JackI(name, grpname, num, getTranslation, (0.0,0.0,0.0), color)
                    cmds.move( -controlDist[1], 0.0, +controlDist[0],grpname,r=1, rpr=1)                     
                elif "talus" in each and "Left" in each:
                    getClass.JackI(name, grpname, num, getTranslation, (0.0,0.0,0.0), color)
                    cmds.move( controlDist[1], 0.0, controlDist[0],grpname,r=1, rpr=1)                     
                else:
                    getClass.JackI(name, grpname, num, getTranslation, (0.0,0.0,0.0), color)                   

                getTranslation=cmds.xform(each+"_jnt", q=1, t=1, ws=1)
                cmds.move(getTranslation[0], getTranslation[1], getTranslation[2],each+"_jnt_ikPole_lctr"+"_grp"+".rotatePivot", ws=1, rpr=1 )
                if 'talus' in each:
                     cmds.setAttr(each+"_jnt_ikPole_lctr.visibility", 0)
                name=each+"FK_target"
                grpname=each+"FK_target"+"_grp"
                num=3
                color=22    
                getTranslation=cmds.xform(each+"_jnt", q=1, t=1, ws=1)
                if "knee" in each:
                    getClass.JackI(name, grpname, num, getTranslation, (0.0,0.0,0.0), color)
                    cmds.move( 0.0, 0.0, -controlDist[0],grpname,r=1, rpr=1)          
                    cmds.parent(grpname,each+"FK_jnt")
                    cmds.setAttr(name+".visibility", 0)
                    cmds.makeIdentity(name, a=True, t=1, s=1, r=1, n=0)  

            cmds.ikHandle(n="foottalus"+eachSide+"_ik", sj="leg"+eachSide+"IK_jnt", ee="foottalus"+eachSide+"IK_jnt", sol="ikRPsolver")
            cmds.setAttr("foottalus"+eachSide+"_ik.visibility", 0)


            
            cmds.connectAttr("legknee"+eachSide+"_jnt_ikPole_lctr.translateX", "foottalus"+eachSide+"_jnt_ikPole_lctr_grp.rotateY", f=1)

            
            cmds.poleVectorConstraint("legknee"+eachSide+"_jnt_ikPole_lctr", "foottalus"+eachSide+"_ik")  


            ########
            #connect
            ########
            
            cmds.addAttr("leghip"+eachSide+"_ctrl", ln=eachSide+"LegFK_IK",  min=0, max=1, at="double", en="FK:IK:", k=1, nn=eachSide+"LegFK_IK")
            cmds.setAttr("leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK", 1)
            
            Controller="leghip"+eachSide+"_ctrl."+eachSide+"LegFK_IK"
            
            bodyskel=["leg"+eachSide,
                      "leghip"+eachSide,
                        "legknee"+eachSide,
                        "foottalus"+eachSide
                        ]
            for each in bodyskel:
                getClass.blendColors(each, Controller)
#                 getClass.blendColorsTranslate(each, Controller)


            ########
            #HIP HINGE
            ########
            
            #cmds.ikHandle(n="hip"+eachSide+"_ik", sj="leg"+eachSide+"IK_jnt", ee="leghip"+eachSide+"IK_jnt", sol="ikRPsolver")
            
            
            
            
            ########
            #Parenting controllers
            ######## 
            
            cmds.parent("leghip"+eachSide+"_grp", "leg"+eachSide+"_ctrl")
            cmds.parent("legknee"+eachSide+"_grp ", "leghip"+eachSide+"_ctrl")
            cmds.parent("foottalus"+eachSide+"_grp", "legknee"+eachSide+"_ctrl")
            
            
            ########LEGS
            #Connect Blender Controls for IK/FK switch
            ########
            cmds.connectAttr ("leg"+eachSide+"_ctrl.rotate","leg"+eachSide+"FK_jnt.rotate", f=1)
            cmds.connectAttr ("leghip"+eachSide+"_ctrl.rotate","leghip"+eachSide+"FK_jnt.rotate", f=1)
            cmds.connectAttr ("legknee"+eachSide+"_ctrl.rotate","legknee"+eachSide+"FK_jnt.rotate", f=1)
            cmds.connectAttr ("foottalus"+eachSide+"_ctrl.rotate","foottalus"+eachSide+"FK_jnt.rotate", f=1)

           # cmds.parentConstraint ("leg"+eachSide+"_ctrl","leg"+eachSide+"FK_jnt", mo=1)
#             cmds.parentConstraint ("leghip"+eachSide+"_ctrl","leghip"+eachSide+"FK_jnt", mo=1)
#             cmds.parentConstraint ("legknee"+eachSide+"_ctrl","legknee"+eachSide+"FK_jnt", mo=1)
#             cmds.parentConstraint ("foottalus"+eachSide+"_ctrl","foottalus"+eachSide+"FK_jnt", mo=1)
#               

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
            #cmds.parentConstraint("leg"+eachSide+"_nod", "leg"+eachSide+"_jnt", mo=1)
            cmds.parent("leg"+eachSide+"_jnt", "leg"+eachSide+"_nod")
            #cmds.parent("leghip"+eachSide+"IK_grp", "leg"+eachSide+"IK_ctrl")
#             cmds.parent("leg"+eachSide+"IK_grp", "leg"+eachSide+"_nod")
            cmds.parent("leg"+eachSide+"_grp", "leg"+eachSide+"_nod")

            getIKClass.stretch("leg"+eachSide+"IK_jnt")

