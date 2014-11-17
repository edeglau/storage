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
class FootRig(object):
    
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
            controlSize=[10, 8, 12]
        elif queryType==2:
            controlSize=[7, 6, 8]
        elif queryType==3:
            controlSize=[4, 3, 5]
        self.createLimb(controlSize)
        
    def createLimb(self, controlSize):
        cmds.select(cl=1)
        Hooffront=("anklefrontRight_guide","toefrontRight_guide", "toeTipFrontRight_guide")    
        HoofIKfront=("heelfrontRight_guide", "toefrontRight_guide", "anklefrontRight_guide")  
        Hoofrear=("anklerearRight_guide","toerearRight_guide", "toeTipRearRight_guide")   
        HoofIKrear=("heelrearRight_guide", "toerearRight_guide", "anklerearRight_guide")
             
        for each in Hoofrear:
            jointSuffix=each.split("_guide")[0]+"_jnt"
            getTranslation=cmds.xform(each, q=1, t=1, ws=1)
            cmds.joint(n=jointSuffix, p=getTranslation)  
        cmds.select(cl=1) 
        for each in HoofIKrear:      
            jointSuffix=each.split("_guide")[0]+"IK_jnt"
            getTranslation=cmds.xform(each, q=1, t=1, ws=1)
            cmds.joint(n=jointSuffix, p=getTranslation)  
        cmds.select(cl=1)        
        for each in Hooffront:
            jointSuffix=each.split("_guide")[0]+"_jnt"
            getTranslation=cmds.xform(each, q=1, t=1, ws=1)
            cmds.joint(n=jointSuffix, p=getTranslation)  
        cmds.select(cl=1) 
        for each in HoofIKfront:      
            jointSuffix=each.split("_guide")[0]+"IK_jnt"
            getTranslation=cmds.xform(each, q=1, t=1, ws=1)
            cmds.joint(n=jointSuffix, p=getTranslation)  
        cmds.select(cl=1) 
        
        cmds.mirrorJoint("anklefrontRight_jnt", myz=1, sr=("Right", "Left"))
        cmds.mirrorJoint("heelfrontRightIK_jnt", myz=1, sr=("Right", "Left"))
        cmds.mirrorJoint("anklerearRight_jnt", myz=1, sr=("Right", "Left"))
        cmds.mirrorJoint("heelrearRightIK_jnt", myz=1, sr=("Right", "Left"))  
        

        
        #########################################################################
        #########################################################################
        #########################################################################
        #########################################################################
        
        Side=["Right", "Left"]
        DepthDimension=["front", "rear"]
        
        for eachSide in Side:
            for eachDim in DepthDimension:
        
                resetOrient=[
                             "ankle"+eachDim+eachSide+"_jnt",
                             "heel"+eachDim+eachSide+"IK_jnt", 
                            ]
                            
                for each in resetOrient:
                        cmds.joint( each, e=1, children=1, zso=1, oj='xyz', sao='ydown', spa=1) 
                           
                locsForCleanup=[]
                    #locators
                legRFL=( "heel"+eachDim+eachSide+"_guide", "toe"+eachDim+eachSide+"_jnt", "ankle"+eachDim+eachSide+"_jnt")
                for each in legRFL:
                    getName=each.split("_")[0]+'_lctr'
                    transformWorldMatrix, rotateWorldMatrix=getClass.locationXForm(each)
                    RFLitem=cmds.spaceLocator(n=getName, p=(transformWorldMatrix[0],0, transformWorldMatrix[2]))
                    locsForCleanup.append(RFLitem)
                    cmds.CenterPivot()
        
                        
                #ik hookup
                startLegJoint=["ankle"+eachDim+eachSide+"_jnt",
                            ]
                
                IKleglist=[
                        "toe"+eachDim+eachSide,
                        ]
                for each, item in map(None, IKleglist, startLegJoint):
                    cmds.ikHandle(n=each+"_ik", sj=item, ee=each+"_jnt", sol="ikSCsolver")
                    #cmds.setAttr(each+"_ik.visibility", 0)
                    cmds.parent(each+"_ik", each+"IK_jnt")
                    
                    
                    
                    
                jointGroup=[
                            "toe"+eachDim+eachSide, 
                            ]
                for eachjoint in jointGroup:
                    eachName=eachjoint+"_jnt"
                    getTranslation=cmds.xform(eachName, q=1, t=1, ws=1)
                    cmds.spaceLocator(n=str(eachName)+"Pole_lctr", p=(getTranslation))
                    cmds.CenterPivot()
                    cmds.setAttr(str(eachName)+"Pole_lctr.visibility", 0)
                
                #cmds.poleVectorConstraint("toe"+eachDim+eachSide+"_jntPole_lctr", "toe"+eachDim+eachSide+"_ik")   
    
                cmds.parent("toe"+eachDim+eachSide+"_ik", "heel"+eachDim+eachSide+"IK_jnt")
                
                
                #CONTROLLER
                name="heel"+eachDim+eachSide+"IK_ctrl"
                grpname="heel"+eachDim+eachSide+"IK_grp"
                numlen=controlSize[1]
                numwid=controlSize[0]
                colour=13
                transformWorldMatrix=cmds.xform("heel"+eachDim+eachSide+"_guide", q=1, t=1, ws=1)
                #pivtransformWorldMatrix, rotateWorldMatrix=getClass.locationXForm(each)ankleLeft_jnt
                rotateWorldMatrix=[0,0,0]
                getClass.rectI(name, grpname, numlen, numwid, transformWorldMatrix, rotateWorldMatrix, colour)  
                cmds.move(0, 0, controlSize[2], name ,r=1, rpr=1, )
                cmds.move(0, 0, -controlSize[2], name+".rotatePivot" ,r=1, rpr=1 )                 
                cmds.makeIdentity(name, a=True, t=1, s=1, r=1, n=0)
    
                
                cmds.parentConstraint("heel"+eachDim+eachSide+"IK_ctrl", "heel"+eachDim+eachSide+"IK_jnt", mo=1, w=1)
    
                
                #use only if controller is lacking these attributes
                cmds.addAttr("heel"+eachDim+eachSide+"IK_ctrl", ln="RaiseHeel", at="long", min=-90, max=90, dv=0, k=1, nn="RaiseHeel")  
                footAttributes=["TipToe",
                                "RaiseToe",
                                "PivotToe", 
                                "SwivelHeel"]
                for each in footAttributes:
                    cmds.addAttr("heel"+eachDim+eachSide+"IK_ctrl", ln=each, at="long", min=-90, max=90, dv=0, k=1, nn=each)    
    
                cmds.connectAttr ("heel"+eachDim+eachSide+"IK_ctrl.RaiseHeel", "toe"+eachDim+eachSide+"IK_jnt.rotateZ", f=1)
                cmds.connectAttr ("heel"+eachDim+eachSide+"IK_ctrl.PivotToe", "toe"+eachDim+eachSide+"IK_jnt.rotateY", f=1)
                cmds.connectAttr ("heel"+eachDim+eachSide+"IK_ctrl.SwivelHeel", "heel"+eachDim+eachSide+"IK_jnt.rotateY", f=1)
    
    
                    
                    
                cmds.orientConstraint("ankle"+eachDim+eachSide+"IK_jnt", "ankle"+eachDim+eachSide+"_jnt", mo=1, w=1)
                   
                    
                    
                cmds.pointConstraint("toe"+eachDim+eachSide+"IK_jnt", "toe"+eachDim+eachSide+"_ik", mo=1)
            
            
            
#             for each in locsForCleanup:
#                 cmds.delete(each)             