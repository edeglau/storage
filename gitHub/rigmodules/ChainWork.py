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
        for each in getGuide:
            cmds.setAttr(each+".visibility", 0)
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
#         for each in mainChain:            
#             jointSuffix='_Clst_jnt'
#             getClass.rigJoints(each, jointSuffix) 
 


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

#         clusterSpline=cmds.ls(mainName+"*Clst_jnt")
#         CLSmainChain=cmds.listRelatives(clusterSpline[0], ad=1, typ="joint")
        
        mainChainFK_Ctrls=[]
        
        mainChain=cmds.ls(mainName+"*_guide")
    

        clstrCtrl=[]        
        
        
        
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
        
#         '''--------------------------------------
#         #            set axis for scale
#         --------------------------------------'''
#         scaleAxis='X'
        
        lastmainChainJoint=mainNamTwistJnt[-1:]

        
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
        

        clusterBucket=[]
        getIKCurveCVs=cmds.ls(mainName+"IK_crv.cv[*]", fl=1)
        for eachCV in enumerate(getIKCurveCVs):
#             for enumerate in enumerate(getCurve.cv):
            getNum=eachCV[0]+1
            getCVobj=eachCV[1]                    
            cmds.select(getCVobj, r=1)
            aName=mainName+"IKcrv"+str(getNum)+"_clstr"
            cmds.cluster(n=aName)
            getClass.createGrpCtrl()
            getClustrGrp=cmds.ls(sl=1)
            newClstrs=getClustrGrp[0]+"_grp"
            print newClstrs
            clusterBucket.append(newClstrs)
        #=======================================================================
        # 
        #=======================================================================
        print "building controllers"
        #=======================================================================
        # 
        #=======================================================================


        num0, num1, num2, num3 = 1, .5, .7, .9
        colour=13
        for each in clusterBucket:
            print each
            name=each+"_Ctrl"
            grpname=name+"_grp"
#             cmds.parent(each, w=1)
            getTranslation, getRotation=getClass.locationXForm(each)
            getClass.CCCircle(name, grpname, num0, num1, num2, num3, getTranslation, getRotation, colour)
            cmds.parent(each, name)


        #disconnectAttr |tail06_Clst_jnt.worldMatrix[0] skinCluster1.matrix[5];
        cmds.addAttr(mainName+"Main_Ctrl", ln=mainName+"FK_IK", min=0, max=1, at="double",en="FK:IK:", k=1, nn=mainName+"FK_IK")
        cmds.setAttr(mainName+"Main_Ctrl."+mainName+"FK_IK", 1)
#         cmds.parent(clusterSpline[0], mainName+"Main_Ctrl")
        Controller=mainName+"Main_Ctrl."+mainName+"FK_IK"
        basemainChain=[(each.split("_")[0])for each in bindmainChain]
        #IK setup
        for each in basemainChain:
            getClass.blendColors(each, Controller) 

        num0, num1, num2, num3 = 1, .5, .7, .9
        colour=13


        fkmainChain=sorted(FKmainChainJoints)

        ChildActivatedValue=1
        ChildDeactivatedValue=0
        ControllerSecondValue=1
        ControllerFirstValue=0   
        Controller=mainName+"Main_Ctrl."+mainName+"FK_IK"
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

        
        #stretch
        
        getIKClass.stretchSpline(mainName+"01IK_jnt")
        
        
        cmds.addAttr(mainName+"Main_Ctrl", ln="Stretch"+mainName, at="enum",en="on:off:", k=1, nn="Stretch"+mainName)
        ChildActivatedValue=2
        ChildDeactivatedValue=0
        ControllerSecondValue=1
        ControllerFirstValue=0
        Child=mainName+"01IK_jnt_cond.operation"
        Controller=mainName+"Main_Ctrl.Stretch"+mainName
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
        Controller=mainName+"Main_Ctrl."+mainName+"FK_IK"
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
            
            cmds.setAttr(mainName+"Main_Ctrl."+mainName+"FK_IK", 1)  




        lastClstr=cmds.listRelatives(clstrCtrl, ap=1)  
        firstClstr=cmds.listRelatives(clstrCtrl, ap=1)             


         
#         else:
        lastFK=cmds.listRelatives(FKCtrl, ap=1) 
        firstFK=cmds.listRelatives(FKCtrl, ap=1)            
        lastFKCtrl=FKCtrl
        firstFKCtrl=FKCtrl
        
        bindmainChain=[(each) for each in cmds.listRelatives(mainName+"01_jnt", ad=1, typ="joint") if mainName in each]



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

        cmds.addAttr(mainName+"Main_Ctrl", ln="Roll", at="double",k=1, nn="Roll")
        cmds.connectAttr(mainName+"Main_Ctrl.Roll", mainName+"IK.roll")
        cmds.addAttr(mainName+"Main_Ctrl", ln="Twist", at="double",k=1, nn="Twist")
        cmds.connectAttr(mainName+"Main_Ctrl.Twist", mainName+"IK.twist")

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

        print "building medium controllers"
        controllerType="_med_grp"
        childControllers=ls(mainName+"IKcrv*_clstrHandle_grp_Ctrl_grp")
        childCurve=mainName+"IK_crv"
        parentCurve=mainName+"_med_lead_crv"
        size, colour= 2, 22
        microLeadCurve=ls(childCurve)
        divNum=6        
        medLeadCurve, medLeadCurveNum, getNum=self.macroControlsNumber(mainName, controllerType, childControllers, microLeadCurve, childCurve, parentCurve, divNum)
        self.macroControls(medLeadCurve, mainName, controllerType, childControllers, microLeadCurve, childCurve, parentCurve, size, colour, nrx, nry, nrz, getNum, medLeadCurveNum)
        
        print "building major controllers"
        controllerType="_maj_grp"
        childControllers=ls(mainName+"*_med_grp")
        childCurve=mainName+"_med_lead_crv"
        parentCurve=mainName+"_maj_lead_crv"
        size, colour= 3, 29
        microLeadCurve=ls(childCurve) 
        divNum=20
        medLeadCurve, medLeadCurveNum, getNum=self.macroControlsNumber(mainName, controllerType, childControllers, microLeadCurve, childCurve, parentCurve, divNum)
        self.macroControls(medLeadCurve, mainName, controllerType, childControllers, microLeadCurve, childCurve, parentCurve, size, colour, nrx, nry, nrz, getNum, medLeadCurveNum)

        print "building maximum controllers"
        controllerType="_max_grp"
        childControllers=ls(mainName+"*_maj_grp")
        childCurve=mainName+"_maj_lead_crv"
        parentCurve=mainName+"_max_lead_crv"
        size, colour= 5, 30
        microLeadCurve=ls(childCurve)  
        divNum=6      
        medLeadCurve, medLeadCurveNum, getNum=self.macroControlsNumber(mainName, controllerType, childControllers, microLeadCurve, childCurve, parentCurve, divNum)
        getNumNew=3
        self.macroControls(medLeadCurve, mainName, controllerType, childControllers, microLeadCurve, childCurve, parentCurve, size, colour, nrx, nry, nrz, getNumNew, medLeadCurveNum)

        print "Tidying up"
        self.tidyUp(mainName)

    def tidyUp(self, mainName):
        print "adding micro control visibility"
        cmds.addAttr(mainName+"Main_Ctrl", ln="microVisible", at="double",k=1, nn="microVisible")
        clstrCtrlrs=ls(mainName+"IKcrv*_clstrHandle_grp_Ctrl")
        for each in clstrCtrlrs:
            cmds.connectAttr(mainName+"Main_Ctrl.microVisible", each+".visibility", f=1)   
        getFirstClstrCtrl=cmds.ls(mainName+"IKcrv*_clstrHandle_grp_Ctrl")[0] 
        print "adding joints to beginning controller"
        cmds.parent(mainName+"01_jnt", getFirstClstrCtrl)
        cmds.parent(mainName+"01FK_jnt", getFirstClstrCtrl)
        cmds.parent(mainName+"01IK_jnt", getFirstClstrCtrl)      
        print "adding maximum controllers to rig"  
        getMaxCtrls=cmds.ls(mainName+"*_max_grp")
        for each in getMaxCtrls:
            cmds.parent(each, mainName+"Main_Ctrl")
        cmds.parent(mainName+"02_FK_grp", mainName+"Main_Ctrl")

    def macroControlsNumber(self, mainName,controllerType, childControllers,microLeadCurve, childCurve, parentCurve, divNum):
        microLeadCurve=ls(childCurve)
        medLeadCurve=cmds.duplicate(childCurve, n=parentCurve)
        CVbucket=[]
        for eachCurve in microLeadCurve:
            getCurve=ls(eachCurve)[0]
            for eachCV in getCurve.cv:
                CVbucket.append(eachCV)
        getNum=len(CVbucket)-2
        medLeadCurveNum=getNum/6
        return medLeadCurve, medLeadCurveNum, getNum

    def macroControls(self, medLeadCurve, mainName,controllerType, childControllers,microLeadCurve, childCurve, parentCurve,size, colour, nrx, nry, nrz, getNum, medLeadCurveNum):
        cmds.rebuildCurve(medLeadCurve, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=medLeadCurveNum, d=3, tol=0)
        CVbucketList=[]
        for eachCurve in medLeadCurve:
            getCurve=ls(eachCurve)[0]
            for eachCV in getCurve.cv:
                getNum=re.sub("\D", "", str(eachCV))
                getNum=int(getNum)
                getNum="%02d" % (getNum,)
                aname=controllerType.split("_grp")[0]+"_ctrl"
                name=mainName+str(getNum)+aname
                grpname= mainName+str(getNum)+controllerType
                CVbucketList.append(eachCV)
                transformWorldMatrix=eachCV.getPosition()
                rotateWorldMatrix=[0.0, 0.0, 0.0]
                select(eachCV, r=1)
                getNewClust=cmds.cluster()
                getClass.buildCtrl(eachCV, name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)
                cmds.parentConstraint(ls(name), getNewClust, mo=0, w=1)
                cmds.parent(grpname, mainName+"_Rig")
                cmds.parent(getNewClust, mainName+"_Rig")
        CVbucketbuckList=[]
        for each in microLeadCurve:
            for eachCV, eachCtrlGro in map(None, each.cv, childControllers):
                CVbucketbuckList.append(eachCV)
        CVbucketbuckList=CVbucketbuckList[:1]+CVbucketbuckList[2:]
        CVbucketbuckList=CVbucketbuckList[:-2]+CVbucketbuckList[-1:]
        medLeadCurve=ls(medLeadCurve)
        for each in medLeadCurve:
            for eachItemCV, eachCtrlGro in map(None, CVbucketbuckList, childControllers):
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