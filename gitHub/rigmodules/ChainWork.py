import sys, os
from pymel.core import *

filepath= os.getcwd()
sys.path.append(str(filepath))
import baseFunctions_maya
reload (baseFunctions_maya)
getClass=baseFunctions_maya.BaseClass()


import stretchIK
reload (stretchIK)
getIKClass=stretchIK.stretchIKClass()

# #name
# mainName="neck"
# #controllerdirection
# nrx=0
# nry=1
# nrz=0  

'''MG rigging modules'''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons License'
'http://creativecommons.org/licenses/by-sa/3.0/au/'
guide="_guide"
clstrctrl="_Clst_jnt_Ctrl"

import maya.cmds as cmds
import maya.mel
class ChainRig(object):
    def __init__(self, nrz, nry, nrx, mainName, ControllerSize):
        self.nrz = nrz 
        self.nry = nry
        self.nrx = nrx
        self.mainName =mainName
        self.ControllerSize=ControllerSize


        getGuide=cmds.ls("*_guide")
        mainChain=(cmds.ls(mainName+"*_guide"))
        neckTwist=(cmds.ls(mainName+"*_guide"))

        mainChainSection=len(mainChain)/3
        sudomainChain=mainChain[:1]+[mainChain[mainChainSection]]+mainChain[-mainChainSection-1::mainChainSection+1]+mainChain[-1:]
       
        print "build bones"
        
        cmds.select(cl=1)
        lastmainChainJoint=mainChain[-1:]
        for each in mainChain:
            jointSuffix='_jnt'
            getClass.rigJoints(each, jointSuffix)  
        cmds.select(cl=1)
        for each in mainChain:
            jointSuffix='FK_jnt'
            getClass.rigJoints(each, jointSuffix) 
        cmds.select(cl=1)        
        for each in mainChain:
            jointSuffix='IK_jnt'
            getClass.rigJoints(each, jointSuffix) 
        cmds.select(cl=1)
        for each in mainChain:            
            jointSuffix='_Clst_jnt'
            getClass.rigJoints(each, jointSuffix) 
 


        resetOrient=[
                    mainName+"01_jnt",
                    mainName+"01FK_jnt",
                    mainName+"01IK_jnt",
                    ]
        
        for each in resetOrient:
            cmds.joint( each, e=1, children=1, zso=1, oj='xyz', sao='yup', spa=1)  
        cmds.select(cl=1)
        
        ##################################
        ##################################
        ##################################
        ##################################
        ######################CONTROLLERS
        print 'build main controllers'
        
        translations=[".tx", ".ty", ".tz"] 
        rotation=[".rx", ".ry", ".rz"]
        
        FKmainChainJoints=[(each) for each in cmds.listRelatives(mainName+"01FK_jnt", ad=1, typ="joint")]
        FKmainChainJoints.append(mainName+"01FK_jnt")
        fkmainChain=sorted(FKmainChainJoints)
        bindmainChain=[(each) for each in cmds.listRelatives(mainName+"01_jnt", ad=1, typ="joint") if mainName in each]
        bindmainChain.append(mainName+"01_jnt")
        lastmainChainJoint=bindmainChain[-1:]
        lastmainChain=lastmainChainJoint[0].split("_")


        colour1=18
        colour2=colour1
        colour3=colour1
        transformWorldMatrix = cmds.xform(mainChain[-1:], q=True, wd=1, t=True)  
        rotateWorldMatrix = cmds.xform(mainChain[-1:], q=True, wd=1, ro=True) 
        getClass.guideBuild(each, transformWorldMatrix, rotateWorldMatrix, colour1, colour2, colour3 )
        getsel=cmds.ls(sl=1)
        cmds.setAttr(getsel[0]+".overrideColor", colour1)
        cmds.rename(getsel[0], mainName+"Parent_nod")
        getsel=cmds.ls(sl=1)
        getClass.buildGrp(getsel[0])

        clusterSpline=cmds.ls(mainName+"*Clst_jnt")
        CLSmainChain=cmds.listRelatives(clusterSpline[0], ad=1, typ="joint")
        
        mainChainFK_Ctrls=[]
        
        mainChain=cmds.ls(mainName+"*_guide")
    

        clstrCtrl=[]
        
        #create the Base"+mainChain+"
        transformWorldMatrix = cmds.xform(mainChain[:1], q=True, wd=1, t=True)  
        rotateWorldMatrix = cmds.xform(mainChain[:1], q=True, wd=1, ro=True) 
#        scaleWorldMatrix = cmds.xform(mainChain[:1], q=True, r=1, s=True)
        name="Base"+mainName+"_Ctrl"
        grpname="Base"+mainName+"_grp"    
        size=ControllerSize
        colour=13   
        getClass.buildCtrl(mainChain[:1], name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)
        mainChainFK_Ctrls.append("Base"+mainName+"_Ctrl")    
        #"+mainChain+"FK_Ctrls.append(clstrCtrl)4
        
        '''middle main IK controller'''

        clstrSplineCtrl=mainChain[ len(mainChain) / 2 ]                 
        #create clusters for IK chain
        name=mainName+"Secondary_IK_Ctrl"
        grpname=mainName+"Secondary_IK_grp"    
        size=ControllerSize
        colour=13 
        transformWorldMatrix = cmds.xform(clstrSplineCtrl, q=True, wd=1, t=True)  
        rotateWorldMatrix = cmds.xform(clstrSplineCtrl, q=True, wd=1, ro=True) 
        getClass.buildCtrl(clstrSplineCtrl, name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)
        getClass.buildGrp(name)
        clstrCtrl.append(name)
        cmds.setAttr(name+".sx" , keyable=0, lock=1)
        cmds.setAttr(name+".sy" , keyable=0, lock=1)
        cmds.setAttr(name+".sz", keyable=0, lock=1)
        


        name="End"+mainName+"IK_Ctrl"
        grpname="End"+mainName+"IK_grp"
        num=20
        colour=13

        transformWorldMatrix = cmds.xform(mainChain[-1:], q=True, wd=1, t=True)  
        rotateWorldMatrix = cmds.xform(mainChain[-1:], q=True, wd=1, ro=True) 
        getClass.buildCtrl(each, name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)
        #getClass.squareI(name, grpname, num, transformWorldMatrix, rotateWorldMatrix, colour)  
        size=ControllerSize-2
        colour=6     
        cmds.makeIdentity("End"+mainName+"IK_Ctrl", a=True, t=1, s=1, r=1, n=0)
        
        
        
        
        FKCtrl=[]
        mainChainguides=cmds.ls(mainName+"*_guide")
        getOdd=mainChainguides[::2]
        for each in mainChainguides[1:-1]:
#         for each in getOdd[:-1]:
            fkmainChainSecondaryJoint=each.split("_guide")[0]+"FK_jnt"  
            name=each.split("_guide")[0]+"_FK_ctrl"  
            grpname=each.split("_guide")[0]+"_FK_grp"  
            size=ControllerSize
            colour=6  
            transformWorldMatrix = cmds.xform(each, q=True, wd=1, t=True)  
            rotateWorldMatrix = cmds.xform(each, q=True, wd=1, ro=True) 
            getClass.buildCtrl(each, name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)
            mainChainFK_Ctrls.append(name)
            FKCtrl.append(name)      
            cmds.parentConstraint(name, fkmainChainSecondaryJoint , mo=1)            
        
        

            
        name=mainName+"Main_Ctrl"
        grpname=mainName+"Main_grp"    
        size=ControllerSize+2
        colour=22   
        transformWorldMatrix = cmds.xform(mainChain[0], q=True, wd=1, t=True)  
        rotateWorldMatrix = cmds.xform(mainChain[0], q=True, wd=1, ro=True)          
        getClass.buildCtrl(mainChain[0], name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)

        cmds.group( em=True, name='IK_grp' )
        
        #create the main controller
        


        
        

       

        
        OrigName="End"+mainName+"FK"
        size=ControllerSize
        colour=6       
        eachPiece=OrigName+"_jnt"
        name=OrigName+"_Ctrl"
        grpname=OrigName+"_grp" 
        transformWorldMatrix = cmds.xform(mainChain[-1:], q=True, wd=1, t=True)  
        rotateWorldMatrix = cmds.xform(mainChain[-1:], q=True, wd=1, ro=True) 
        getClass.buildCtrl(each, name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)
        cmds.makeIdentity("End"+mainName+"FK_Ctrl", a=True, t=1, s=1, r=1, n=0)
        fkjoints=cmds.ls(mainName+"*FK_jnt")
        cmds.parentConstraint("End"+mainName+"FK_Ctrl", fkjoints[-1:] , mo=1)
        

        mainChainFK_Ctrls.append("End"+mainName+"FK_Ctrl")

   
         
        ##################################
        ##################################
        ##################################
        ##################################
        ##################################
        ##################################
        ##################################
        ##################################
        ##################################
        #IK
        
        
        #'''--------------------------------------
               # "+mainChain+"
        #--------------------------------------'''
        mainChainJoints=(cmds.ls(mainName+"*_jnt"))
        lastJoint=mainChainJoints[-1:]
        mainNamTwistJnt=(cmds.ls(mainName+"*IK_jnt"))
        mainChainLow=(cmds.ls(mainName+"*FK_jnt"))
        mainChainCtrl=(cmds.ls(mainName+"*_Ctrl"))
        #"+mainChain+"CtrlGrp=cmds.pickWalk("+mainChain+"Ctrl, d="up")
        
#         '''--------------------------------------
#         #            set axis for scale
#         --------------------------------------'''
#         scaleAxis='X'
        
        lastmainChainJoint=mainNamTwistJnt[-1:]

        
#         allButlastmainChainJoints=mainChainJoints[:-1][0]
        '''--------------------------------------
        #            create spline IK
        --------------------------------------'''
        print 'create spline IK'
        
        cmds.ikHandle(n=mainName+"IK", sj=mainName+"01IK_jnt", ee=str(lastmainChainJoint[0]), sol="ikSplineSolver", scv=0, ns=4, rtm=1, tws="easeIn")
        #cmds.ikHandle(n=ikname, sj=getjoints[0], ee=lastjoint[0], sol="ikSplineSolver", ccv=0, ns=4, snc=1, tws="easeIn", rtm=1, c=curvename)
        '''--------------------------------------
        #        find the spline of the IK
        --------------------------------------'''
        print 'find the spline of the IK'
        list=cmds.listConnections(mainName+'IK', t="shape")
        cmds.rename(list, mainName+"IK_crv")

        
        '''--------------------------------------
        #        skinbind lowres "+mainChain+" to the spline
        --------------------------------------'''
        print "skinbind lowres "+str(mainChain)+" to the spline"
        
        getIKCurveCVs=cmds.ls(mainName+"IK_crv.cv[*]", fl=1)
        getfirstCVs=getIKCurveCVs[1::-1]
        getLastCVs= getIKCurveCVs[-2::1]
        getverylastCVs=getIKCurveCVs[-2:]
        getlastjoint=clusterSpline[-1:]
        for each, bone in map(None, getIKCurveCVs[2:-2], clusterSpline[1:-1]):  
            cmds.select(clear=1)
            cmds.select(bone)
            cmds.select(each, add=1)
            cmds.bindSkin(each, bone, tsb=1) 
        for each in getfirstCVs:  
            cmds.select(clear=1)
            cmds.select(clusterSpline[0])
            cmds.select(each, add=1)
            cmds.bindSkin(each, clusterSpline[0], tsb=1)
        for each in getverylastCVs:
            cmds.select(clear=1)
            cmds.select(each, add=1) 
            getNewClust=cmds.cluster(n="endChainCluster")
            cmds.select(getlastjoint)
            cmds.select(each, add=1)    
            cmds.SmoothBindSkin(each, getlastjoint, tsb=1, bcp=1)
            cmds.parent(getNewClust[1], getlastjoint)
        getconn=[(item) for item in cmds.listConnections(getlastjoint, d=1) if cmds.nodeType(item)=="skinCluster"]
        if getconn:
            for each in getconn:
                try:
                    cmds.delete(each)
                except:
                    pass        
        
        
        #=======================================================================
        # 
        #=======================================================================
        print "building controllers"
        #=======================================================================
        # 
        #=======================================================================
        
        #disconnectAttr |tail06_Clst_jnt.worldMatrix[0] skinCluster1.matrix[5];
        cmds.addAttr("Base"+mainName+"_Ctrl", ln=mainName+"FK_IK", min=0, max=1, at="double",en="FK:IK:", k=1, nn=mainName+"FK_IK")
        cmds.setAttr("Base"+mainName+"_Ctrl."+mainName+"FK_IK", 1)
        cmds.parent(clusterSpline[0], "Base"+mainName+"_Ctrl")
        Controller="Base"+mainName+"_Ctrl."+mainName+"FK_IK"
        basemainChain=[(each.split("_")[0])for each in bindmainChain]
        #IK setup
        for each in basemainChain:
            getClass.blendColors(each, Controller) 

        getSortedclusterSpline=cmds.ls(mainName+"*_Clst_jnt")
        clstrSplineCtrl=getSortedclusterSpline[ len(getSortedclusterSpline) / 2 ]          
        #cmds.pointConstraint(clstrCtrl, clstrSplineCtrl, mo=1)
        num0, num1, num2, num3 = 1, .5, .7, .9
        colour=13
#         /for each in getSortedclusterSpline[1:-1]:
#        for each in getSortedclusterSpline[1:]:
        for each in getSortedclusterSpline:
            name=each+"_Ctrl"
            grpname=each+"_grp"
            cmds.parent(each, w=1)
            getTranslation, getRotation=getClass.locationXForm(each)
            getClass.CCCircle(name, grpname, num0, num1, num2, num3, getTranslation, getRotation, colour)
            cmds.parentConstraint(name, each)



        fkmainChain=sorted(FKmainChainJoints)

        ChildActivatedValue=1
        ChildDeactivatedValue=0
        ControllerSecondValue=1
        ControllerFirstValue=0   
        Controller="Base"+mainName+"_Ctrl."+mainName+"FK_IK"
        defaultSet=1           
        for each in clstrCtrl:
            Child=each+".visibility"
            getClass.controlSecondValueChildOn(Controller, 
                                               Child, 
                                               defaultSet, 
                                               ChildActivatedValue, 
                                               ChildDeactivatedValue, 
                                               ControllerSecondValue, 
                                               ControllerFirstValue)          
        #constrain FK spin to controls

            
        #cmds.parent("+mainChain+"FK_Ctrls[0], "Base"+mainChain+"_Ctrl")
#         cmds.pointConstraint("Base"+mainName+"_Ctrl", mainName+"01_jnt", mo=1)
        #cmds.orientConstraint("End"+mainName+"FK_Ctrl", fkmainChain[-1], mo=1)


        ChildActivatedValue=1
        ChildDeactivatedValue=0
        ControllerSecondValue=1
        ControllerFirstValue=0
        Child="End"+mainName+"IK_Ctrl.visibility"
        Controller="Base"+mainName+"_Ctrl."+mainName+"FK_IK"
        defaultSet=1
        getClass.controlSecondValueChildOn(Controller, 
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
        Child="End"+mainName+"FK_Ctrl.visibility"
        Controller="Base"+mainName+"_Ctrl."+mainName+"FK_IK"
        defaultSet=1
        getClass.controlFirstValueChildOn(Controller, 
                                           Child, 
                                           defaultSet, 
                                           ChildActivatedValue, 
                                           ChildDeactivatedValue, 
                                           ControllerSecondValue,
                                           ControllerFirstValue)
        
        #stretch
        
        getIKClass.stretchSpline(mainName+"01IK_jnt")
        
        
        cmds.addAttr("Base"+mainName+"_Ctrl", ln="Stretch"+mainName, at="enum",en="on:off:", k=1, nn="Stretch"+mainName)
        ChildActivatedValue=2
        ChildDeactivatedValue=0
        ControllerSecondValue=1
        ControllerFirstValue=0
        Child=mainName+"01IK_jnt_cond.operation"
        Controller="Base"+mainName+"_Ctrl.Stretch"+mainName
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
        Controller="Base"+mainName+"_Ctrl."+mainName+"FK_IK"
        defaultSet=1
        for each in FKCtrl:
            Child=each+".visibility"
            getClass.controlFirstValueChildOn(Controller, 
                                               Child, 
                                               defaultSet, 
                                               ChildActivatedValue, 
                                               ChildDeactivatedValue, 
                                               ControllerSecondValue,
                                               ControllerFirstValue)
            
            cmds.setAttr("Base"+mainName+"_Ctrl."+mainName+"FK_IK", 1)  




        lastClstr=cmds.listRelatives(clstrCtrl, ap=1)  
        firstClstr=cmds.listRelatives(clstrCtrl, ap=1)             


         
#         else:
        lastFK=cmds.listRelatives(FKCtrl, ap=1) 
        firstFK=cmds.listRelatives(FKCtrl, ap=1)            
        lastFKCtrl=FKCtrl
        firstFKCtrl=FKCtrl
        
        bindmainChain=[(each) for each in cmds.listRelatives(mainName+"01_jnt", ad=1, typ="joint") if mainName in each]


        #cmds.connectAttr("End"+mainName+"IK_Ctrl.rotate.rotateY", mainName+"IK.twist")

 
        

        #cmds.parent(mainName+"IK","End"+mainName+"IK_Ctrl")
        cmds.parent(mainName+"Parent_nod_grp", bindmainChain[0])
        #===============================================================================
        # 
        #===============================================================================
        print "linking main controls for influence"

        
        
        if len(FKCtrl)>1:
            lastFK=cmds.listRelatives(FKCtrl[-1:], ap=1)   
            firstFK=cmds.listRelatives(FKCtrl[:1], ap=1)          
            lastFKCtrl=FKCtrl[-1:]
            firstFKCtrl=FKCtrl[:1]
            for eachctrl in xrange(len(FKCtrl) - 1):
                current_item, next_item = FKCtrl[eachctrl], FKCtrl[eachctrl + 1]
                getParentgrp=cmds.listRelatives(next_item, ap=1)
                cmds.parent(getParentgrp[0], current_item) 
            cmds.parent("End"+mainName+"FK_grp", FKCtrl[-1:])    
        else:
            cmds.parent("End"+mainName+"FK_grp", FKCtrl[0])
            
        cmds.parent("End"+mainName+"IK_grp",mainName+"Main_Ctrl")
        cmds.parent("Base"+mainName+"_grp",mainName+"Main_Ctrl")
        

        getNames=cmds.ls(mainName+"*_guideFK_Ctrl")
        for each in getNames:
            newname=str.capitalize(str(each))
            lognm=newname.replace("guide", "")
            getname=lognm.replace("fk_ctrl", "FK_Ctrl")
            cmds.rename(each, getname)
        getNames=cmds.ls(mainName+"*_IK_Ctrl")
        for each in getNames:
            newname=str.capitalize(str(each))
            getname=newname.replace("ik_ctrl", "IK_Ctrl")
            cmds.rename(each, getname)        
#             
        cmds.parent(mainName+"Secondary_IK_grp", mainName+"Main_Ctrl")

        cmds.addAttr("Base"+mainName+"_Ctrl", ln="Roll", at="double",k=1, nn="Roll")
        cmds.connectAttr("Base"+mainName+"_Ctrl.Roll", mainName+"IK.roll")
        cmds.addAttr("Base"+mainName+"_Ctrl", ln="Twist", at="double",k=1, nn="Twist")
        cmds.connectAttr("Base"+mainName+"_Ctrl.Twist", mainName+"IK.twist")

        getRigGrp=cmds.group( em=True, name=mainName+'_Rig' )
        cmds.parent(mainName+"IK", getRigGrp)
        cmds.parent(mainName+"IK_crv", getRigGrp)
        getFreeStuff=[(each) for each in cmds.ls(mainName+"*_Clst_jnt*") if cmds.listRelatives(each, ap=1)==None and cmds.nodeType(each)=="joint"]
        for each in getFreeStuff:
            cmds.parent(each, getRigGrp)
        getFreeStuff=[(each) for each in cmds.ls(mainName+"*_Clst_jnt*") if cmds.listRelatives(each, ap=1)==None and cmds.nodeType(each)=="transform"]
        for each in getFreeStuff:
            cmds.parent(each, getRigGrp)
        cmds.parent("IK_grp", getRigGrp)
        
        getSortedclusterSpline=cmds.ls(mainName+"*_Clst_jnt_grp")
        getSortedclusterCtrl=cmds.ls(mainName+"*_Clst_jnt_Ctrl")

        
#         print "build midrange controllers - 5"
#                     
#         '''x5 controllers'''
#         getSortedclusterSpline=cmds.ls(mainName+"*_Clst_jnt_grp")
#         getSortedclusterCtrl=cmds.ls(mainName+"*_Clst_jnt_Ctrl")
#         if len(getSortedclusterSpline)>5:
#             parentControllers=[]
#             pairedParentControllers=[]  
#             fiveclstrSplineCtrl=mainChain[4::5]
#             getFirstOne=mainChain[:1]
#             getlastOne=mainChain[-1:]
#             makeEnds=[getFirstOne[0]]+[getlastOne[0]]
#             #create clusters for IK chain
#             for each in xrange(len(fiveclstrSplineCtrl) - 1):
#                 current_ctrl_item, next_ctrl_item = fiveclstrSplineCtrl[each], fiveclstrSplineCtrl[each + 1]  
#                 name=current_ctrl_item.split("_guide")[0]+"_sml_Ctrl"
#                 grpname=name+"_grp"    
#                 fivesize=ControllerSize/4.5
#                 colour=22
#                 transformWorldMatrix = cmds.xform(current_ctrl_item, q=True, wd=1, t=True)  
#                 rotateWorldMatrix = cmds.xform(current_ctrl_item, q=True, wd=1, ro=True) 
#                 getClass.buildCtrl(current_ctrl_item, name, grpname,transformWorldMatrix, rotateWorldMatrix, fivesize, colour, nrx, nry, nrz)
#                 parentControllers.append(name)
#                 cmds.setAttr(name+".sx" , keyable=0, lock=1)
#                 cmds.setAttr(name+".sy" , keyable=0, lock=1)
#                 cmds.setAttr(name+".sz", keyable=0, lock=1)
#             for each in makeEnds:
#                 name=each.split("_guide")[0]+"_sml_Ctrl"
#                 grpname=name+"_grp"            
#                 transformWorldMatrix = cmds.xform(each, q=True, wd=1, t=True)  
#                 rotateWorldMatrix = cmds.xform(each, q=True, wd=1, ro=True) 
#                 getClass.buildCtrl(current_ctrl_item, name, grpname,transformWorldMatrix, rotateWorldMatrix, fivesize, colour, nrx, nry, nrz)
#         getMidControllers=cmds.ls(mainName+"*_sml_Ctrl")
#         firstCtrl=getMidControllers[:1]
#         firstCtrlgrp=cmds.ls(mainName+"*_sml_Ctrl_grp")[:1]
# #        lastCtrl=getMidControllers[-1:]
# #        lastChild=getSortedclusterSpline[-1:]
# #        cmds.parentConstraint(lastCtrl, lastChild, mo=1, w=1.0)
#         for eachCntrl in xrange(len(getMidControllers[:-1]) - 1):
#             current_ctrl_item, next_ctrl_item = getMidControllers[eachCntrl], getMidControllers[eachCntrl + 1] 
#             getCurNumber=int(re.sub("\D", "", current_ctrl_item))
#             getNextNumber=int(re.sub("\D", "", next_ctrl_item)) 
#             getChildren=[] 
#             for item in range(getCurNumber, getNextNumber):
#                 getNum="%02d" % (item,)
#                 theController=mainName+str(getNum)+clstrctrl
#                 thegrp=theController.split("_Ctrl")[0]+"_grp"
#                 getChildren.append(thegrp)
#             BucketValue=getClass.Percentages(getChildren, 1.0, 0.0)                
#             for child, weighted in map(None, getChildren, BucketValue):         
#                 cmds.parentConstraint(current_ctrl_item, child, mo=1, w=weighted)
#             reversedBucketValue=reversed(BucketValue)
#             for child, weighted in map(None, getChildren, reversedBucketValue):
#                 cmds.parentConstraint(next_ctrl_item, child, mo=1, w=weighted)
#         print firstCtrlgrp
#         cmds.parent(firstCtrlgrp, "Base"+mainName+"_Ctrl")
#         cmds.parent(getSortedclusterSpline, getMidControllers[0])
#         cmds.parent(mainName+"01_jnt",getSortedclusterCtrl[0])
#         cmds.parent(mainName+"01FK_jnt",getSortedclusterCtrl[0])
#         cmds.parent(mainName+"01IK_jnt",getSortedclusterCtrl[0]) 
#         getChildString=cmds.ls(mainName+"*_Clst_jnt_grp")
#         getLastChildren=getChildString[-6:]
#         getFirstChildren=getChildString[:5]        
#         secondEndBucketValue=getClass.Percentages(getLastChildren, 1.0, 0.0)
#         for eachChild, eachBucketItem in map(None, getLastChildren, secondEndBucketValue):
#             cmds.parentConstraint(getMidControllers[-2:-1], eachChild, mo=1, w=eachBucketItem)      
#         secondEndBucketValue=getClass.Percentages(getLastChildren, 0.0, 1.0)
#         for eachChild, eachBucketItem in map(None, getLastChildren, secondEndBucketValue):
#             cmds.parentConstraint(getMidControllers[-1:], eachChild, mo=1, w=eachBucketItem)  

        print "build major range controllers -10"
        '''x10 controllers'''
        influencedCtrl=cmds.ls(mainName+"*_sml_Ctrl_grp")
        controlSuff="_mid_Ctrl"
        buildNameFrom="_sml_Ctrl"
        #self.DropOffControls(2, 31, 3, ControllerSize, nrx, nry, nrz, influencedCtrl, controlSuff, buildNameFrom)

        print "build maj range controllers - 20"
        '''x20 controllers'''
        majinfluencedCtrl=cmds.ls(mainName+"*_mid_Ctrl_grp")
        maxcontrolSuff="_maj_Ctrl"
        maxbuildNameFrom="_mid_Ctrl"
        #self.DropOffControls(2, 30, 2, ControllerSize, nrx, nry, nrz, majinfluencedCtrl, maxcontrolSuff, maxbuildNameFrom)

        print "build max range controllers -30"
        '''x30 controllers'''
        majinfluencedCtrl=cmds.ls(mainName+"*_maj_Ctrl_grp")
        maxcontrolSuff="_max_Ctrl"
        maxbuildNameFrom="_maj_Ctrl"
        #self.DropOffControls(2, 25, 1, ControllerSize, nrx, nry, nrz, majinfluencedCtrl, maxcontrolSuff, maxbuildNameFrom)

        cmds.parentConstraint("Base"+mainName+"_Ctrl", mainName+"Secondary_IK_grp", mo=1, w=.5)
        cmds.parentConstraint("End"+mainName+"IK_Ctrl", mainName+"Secondary_IK_grp", mo=1, w=.5)
        maxinfluencedCtrl=cmds.ls(mainName+"*_max_Ctrl")


        controllerType="_med_grp"
        microLeadCurve=ls(mainName+"IK_crv")
        childControllers=ls(mainName+"*_Clst_jnt_grp")
        childCurve=mainName+"IK_crv"
        parentCurve=mainName+"_med_lead_crv"
        size, colour, nrx, nry, nrz= 2, 22, 0, 1, 0
        if len(getSortedclusterSpline)>10:
            self.macroControls(mainName, controllerType, childControllers, microLeadCurve, childCurve, parentCurve, size, colour, nrx, nry, nrz)
        
        controllerType="_med_grp"
        microLeadCurve=ls(mainName+"IK_crv")
        childControllers=ls(mainName+"*_Clst_jnt_grp")
        childCurve=mainName+"IK_crv"
        parentCurve=mainName+"_med_lead_crv"
        size, colour, nrx, nry, nrz= 2, 22, 0, 1, 0
        self.macroControls(mainName, controllerType, childControllers, microLeadCurve, childCurve, parentCurve, size, colour, nrx, nry, nrz)

        if cmds.ls(mainName+"*_max_Ctrl"):
           maxinfluencedCtrl=cmds.ls(mainName+"*_max_Ctrl")
        if cmds.ls(mainName+"*_maj_Ctrl"):
           majinfluencedCtrl=cmds.ls(mainName+"*_maj_Ctrl")
        if cmds.ls(mainName+"*_mid_Ctrl"):
           medinfluencedCtrl=cmds.ls(mainName+"*_mid_Ctrl")
        if cmds.ls(mainName+"*_sml_Ctrl"):
           smlinfluencedCtrl=cmds.ls(mainName+"*_sml_Ctrl")

        if maxinfluencedCtrl:
            print "THERE ARE MAX CONTROLLERS PRESENT"
            getControllerBucket=maxinfluencedCtrl                      
#            cmds.parentConstraint("Secondary"+mainName+"_Ctrl", mo=1, w=.5)
        elif majinfluencedCtrl:
            print "THERE ARE MAJOR CONTROLLERS PRESENT"
            getControllerBucket=majinfluencedCtrl
        elif medinfluencedCtrl:
            print "THERE ARE MEDIUM CONTROLLERS PRESENT"  
            getControllerBucket=medinfluencedCtrl
        elif smlinfluencedCtrl:
            print "THERE ARE SMALL CONTROLLERS PRESENT"    
            getControllerBucket=smlinfluencedCtrl              
 
        print getControllerBucket
    def macroControls(self, mainName,controllerType, childControllers,microLeadCurve, childCurve, parentCurve,size, colour, nrx, nry, nrz ):
        microLeadCurve=ls(childCurve)
        medLeadCurve=cmds.duplicate(childCurve, n=parentCurve)
        CVbucket=[]
        for eachCurve in microLeadCurve:
            getCurve=ls(eachCurve)[0]
            for eachCV in getCurve.cv:
                CVbucket.append(eachCV)
        getNum=len(CVbucket)-2
        medLeadCurveNum=getNum/6
        cmds.rebuildCurve(medLeadCurve, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=medLeadCurveNum, d=3, tol=0)
        CVbucket=[]
        for eachCurve in medLeadCurve:
            getCurve=ls(eachCurve)[0]
            for eachCV in getCurve.cv:
                getNum=re.sub("\D", "", str(eachCV))
                getNum=int(getNum)
                getNum="%02d" % (getNum,)
                name, grpname=mainName+str(getNum)+controllerType, mainName+str(getNum)+controllerType
                CVbucket.append(eachCV)
                transformWorldMatrix=eachCV.getPosition()
                rotateWorldMatrix=[0.0, 0.0, 0.0]
                select(eachCV, r=1)
                getNewClust=cmds.cluster()
                getClass.buildCtrl(eachCV, name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)
                cmds.parentConstraint(ls(name), getNewClust, mo=0, w=1)
        for each in microLeadCurve:
            for eachCV, eachCtrlGro in map(None, each.cv, childControllers):
                CVbucket.append(eachCV)
        CVbucket=CVbucket[:1]+CVbucket[2:]
        CVbucket=CVbucket[:-2]+CVbucket[-1:]
        medLeadCurve=ls(medLeadCurve)
        for each in medLeadCurve:
            for eachCV, eachCtrlGro in map(None, CVbucket, childControllers):
                pgetCVpos=eachCtrlGro.getTranslation()
                getpoint=each.closestPoint(pgetCVpos, tolerance=0.001, space='preTransform')
                getParam=each.getParamAtPoint(getpoint, space='preTransform')
                select(eachCtrlGro, r=1)
                select(medLeadCurve[0], add=1)
                motionPath=cmds.pathAnimation(fractionMode=1, follow=1, followAxis="x", upAxis="y", worldUpType="vector", worldUpVector=[0, 1, 0], inverseUp=0, inverseFront=0, bank=0)        
                disconnectAttr(motionPath+"_uValue.output", motionPath+".uValue")
                getpth=str(motionPath)
                setAttr(motionPath+".fractionMode", False)
                setAttr(motionPath+".uValue", getParam) 



    def DropOffControls(self, 
                        span, 
                        colour, 
                        size,  
                        ControllerSize, 
                        nrx, nry, nrz, 
                        influencedCtrl, 
                        controlSuff, 
                        buildNameFrom):
        print influencedCtrl
        if len(influencedCtrl)>span:
            parentControllers=[]
            pairedParentControllers=[] 
            lastInf=influencedCtrl[-1:] 
            firstInf=influencedCtrl[:1]
            #create clusters for IK chain
            for each in influencedCtrl[1::2]:
                name=each.split(buildNameFrom)[0]+controlSuff
                grpname=name+"_grp"    
                fivesize=ControllerSize/size
                colour=colour
                transformWorldMatrix = cmds.xform(each, q=True, wd=1, t=True)  
                rotateWorldMatrix = cmds.xform(each, q=True, wd=1, ro=True) 
                getClass.buildCtrl(each, name, grpname,transformWorldMatrix, rotateWorldMatrix, fivesize, colour, nrx, nry, nrz)
                parentControllers.append(name)
                cmds.setAttr(name+".sx" , keyable=0, lock=1)
                cmds.setAttr(name+".sy" , keyable=0, lock=1)
                cmds.setAttr(name+".sz", keyable=0, lock=1)
            controllerInfDropOffBucket=[]
            for each in xrange(len(influencedCtrl) - 1):
                try:
                    current_ctrl_item=influencedCtrl[1:][::2][each]
                    prev_item=influencedCtrl[::2][each]
                    next_ctrl_item=influencedCtrl[::2][each+1]                 
                except:
                    pass
                if prev_item!=influencedCtrl[-1:][0]:
                    controllerInfDropOffBucket.append([prev_item, current_ctrl_item, next_ctrl_item])                   
            for eachPContrl, item in map(None, parentControllers, controllerInfDropOffBucket):
                try:
                    FIRST=item[:1][0]
                    SECOND=item[1:2][0]
                    THIRD=item[-1:][0]
                    if str(FIRST) != firstInf[0]:
                        cmds.parentConstraint(eachPContrl, FIRST, mo=1, w=.5)
                    cmds.parentConstraint(eachPContrl, SECOND, mo=1, w=1.0)
                    if str(THIRD) != lastInf[0]:
                        cmds.parentConstraint(eachPContrl, THIRD, mo=1, w=.5)
                except:
                    pass            


    def leading_curve(self):
        getIKCurveCVs=cmds.ls("nameIK_crv", fl=1)
        CVbucket=[]
        microLeadCurve=cmds.duplicate("nameIK_crv", n="micro_lead_crv")
        for eachCurve in microLeadCurve:
            getCurve=ls(eachCurve)[0]
            for eachCV in getCurve.cv:
                CVbucket.append(eachCV)
        getNum=len(CVbucket)-2
        #CVbucket= CVbucket[:1] + CVbucket[1+1 :]
        CVbucket=CVbucket[:1]+CVbucket[2:]
        #CVbucket=CVbucket[:getNum] + CVbucket[getNum+1 :]
        CVbucket=CVbucket[:-2]+CVbucket[-1:]
        getObjects=cmds.ls("name*_Clst_jnt_grp", fl=1)
        for eachLeadCV, eachControllerObj in map(None,CVbucket, getObjects):
            connectAttr(eachLeadCV+".xValue", eachControllerObj+".translateX")
            connectAttr(eachLeadCV+".yValue", eachControllerObj+".translateY")
            connectAttr(eachLeadCV+".zValue", eachControllerObj+".translateZ")
