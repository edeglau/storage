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
        #===============================================================================
        # 
        #===============================================================================
#        getMidClstr=cmds.ls(mainName+"*_Clst_jnt_grp")
#        firstpart, secondpart = getMidClstr[:len(getMidClstr)/2], getMidClstr[len(getMidClstr)/2:] 
#        minWeightValue=0.0 
#        maxWeightValue=1.0
#        BucketValue=getClass.Percentages(secondpart, minWeightValue, maxWeightValue)
#        for eachCluser, weighted in map(None,secondpart, BucketValue):
#            cmds.parentConstraint( "End"+mainName+"IK_Ctrl", eachCluser, mo=1, w=weighted)  
#        for eachCluser, weighted in map(None, reversed(secondpart), BucketValue):
#            cmds.parentConstraint( mainName+"Secondary_IK_Ctrl", eachCluser, mo=1, w=weighted) 
#        
#        
#        firstlist=(firstpart)
#        reversedBucket=[]
#        firstlist= reversed(firstlist)
#        for each in firstlist:
#            reversedBucket.append(each)
#        print reversedBucket
#        #beginning
#        minWeightValue=0.0 
#        maxWeightValue=1.0
#        BucketValue=getClass.Percentages(reversedBucket, minWeightValue, maxWeightValue)
#        for eachCluser, weighted in map(None, reversedBucket, BucketValue):
#            cmds.parentConstraint( "Base"+mainName+"_Ctrl", eachCluser, mo=1, w=weighted) 
#        for eachCluser, weighted in map(None, reversed(reversedBucket), BucketValue):
#            cmds.parentConstraint( mainName+"Secondary_IK_Ctrl", eachCluser, mo=1, w=weighted) 

        
        
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
        
        print "build mid controllers"
                    
        '''x5 controllers'''
        getSortedclusterSpline=cmds.ls(mainName+"*_Clst_jnt_grp")
        getSortedclusterCtrl=cmds.ls(mainName+"*_Clst_jnt_Ctrl")
        print getSortedclusterSpline
        if len(getSortedclusterSpline)>5:
            parentControllers=[]
            pairedParentControllers=[]  
            fiveclstrSplineCtrl=mainChain[4::5]
            getFirstOne=mainChain[:1]
            getlastOne=mainChain[-1:]
            makeEnds=[getFirstOne[0]]+[getlastOne[0]]
            #create clusters for IK chain
            for each in xrange(len(fiveclstrSplineCtrl) - 1):
                current_ctrl_item, next_ctrl_item = fiveclstrSplineCtrl[each], fiveclstrSplineCtrl[each + 1]  
                name=current_ctrl_item.split("_guide")[0]+"_mid_Ctrl"
                grpname=name+"_grp"    
                fivesize=ControllerSize/3
                colour=13
                transformWorldMatrix = cmds.xform(current_ctrl_item, q=True, wd=1, t=True)  
                rotateWorldMatrix = cmds.xform(current_ctrl_item, q=True, wd=1, ro=True) 
                getClass.buildCtrl(current_ctrl_item, name, grpname,transformWorldMatrix, rotateWorldMatrix, fivesize, colour, nrx, nry, nrz)
                parentControllers.append(name)
                cmds.setAttr(name+".sx" , keyable=0, lock=1)
                cmds.setAttr(name+".sy" , keyable=0, lock=1)
                cmds.setAttr(name+".sz", keyable=0, lock=1)
            for each in makeEnds:
                name=each.split("_guide")[0]+"_mid_Ctrl"
                grpname=name+"_grp"            
                transformWorldMatrix = cmds.xform(each, q=True, wd=1, t=True)  
                rotateWorldMatrix = cmds.xform(each, q=True, wd=1, ro=True) 
                getClass.buildCtrl(current_ctrl_item, name, grpname,transformWorldMatrix, rotateWorldMatrix, fivesize, colour, nrx, nry, nrz)
        getMidControllers=cmds.ls(mainName+"*_mid_Ctrl")
        firstCtrl=getMidControllers[:1]
        firstCtrlgrp=cmds.ls(mainName+"*_mid_Ctrl_grp")[:1]
        print firstCtrlgrp
#        lastCtrl=getMidControllers[-1:]
#        lastChild=getSortedclusterSpline[-1:]
#        cmds.parentConstraint(lastCtrl, lastChild, mo=1, w=1.0)
        for eachCntrl in xrange(len(getMidControllers[:-1]) - 1):
            current_ctrl_item, next_ctrl_item = getMidControllers[eachCntrl], getMidControllers[eachCntrl + 1] 
            getCurNumber=int(re.sub("\D", "", current_ctrl_item))
            getNextNumber=int(re.sub("\D", "", next_ctrl_item)) 
            getChildren=[] 
            for item in range(getCurNumber, getNextNumber):
                getNum="%02d" % (item,)
                theController=mainName+str(getNum)+clstrctrl
                thegrp=theController.split("_Ctrl")[0]+"_grp"
                getChildren.append(thegrp)
            BucketValue=getClass.Percentages(getChildren, 1.0, 0.0)                
            for child, weighted in map(None, getChildren, BucketValue):         
                cmds.parentConstraint(current_ctrl_item, child, mo=1, w=weighted)
            reversedBucketValue=reversed(BucketValue)
            for child, weighted in map(None, getChildren, reversedBucketValue):
                cmds.parentConstraint(next_ctrl_item, child, mo=1, w=weighted)
        print firstCtrlgrp
        cmds.parent(firstCtrlgrp, "Base"+mainName+"_Ctrl")
        cmds.parent(getSortedclusterSpline, getMidControllers[0])
        cmds.parent(mainName+"01_jnt",getSortedclusterCtrl[0])
        cmds.parent(mainName+"01FK_jnt",getSortedclusterCtrl[0])
        cmds.parent(mainName+"01IK_jnt",getSortedclusterCtrl[0]) 
#        cmds.parent(firstFK, mainName)                       
#        getChildString=cmds.ls(mainName+"*_Clst_jnt_grp")
#        getLastChildren=getChildString[-6:]
#        getFirstChildren=getChildString[:5]        
#        cmds.parentConstraint(getMidControllers[-1:], getLastChildren[0], mo=1, w=1.0)
#        BucketValue=getClass.Percentages(getFirstChildren, 0.0, 1.0)
#        for eachChild, eachBucketItem in map(None, getFirstChildren, BucketValue):
#            cmds.parentConstraint(firstCtrl[0], eachChild, mo=1, w=eachBucketItem)
#        BucketValue=getClass.Percentages(getFirstChildren, 1.0, 0.0)
#        getBaseControl=cmds.ls("Basename_Ctrl")
#        for eachChild, eachBucketItem in map(None, getFirstChildren, BucketValue):
#            cmds.parentConstraint(getBaseControl[0], eachChild, mo=1, w=eachBucketItem)  
#        endBucketValue=getClass.Percentages(getLastChildren, 0.0, 1.0)
#        getEndControl=cmds.ls("EndnameIK_Ctrl")
#        for eachChild, eachBucketItem in map(None, getLastChildren, endBucketValue):
#            cmds.parentConstraint(getEndControl[0], eachChild, mo=1, w=eachBucketItem)      
#        secondEndBucketValue=getClass.Percentages(getLastChildren, 1.0, 0.0)
#        for eachChild, eachBucketItem in map(None, getLastChildren, secondEndBucketValue):
#            cmds.parentConstraint(getMidControllers[-1:], eachChild, mo=1, w=eachBucketItem)  

        print "build max controllers"
        '''x10 controllers'''
        influencedCtrl=cmds.ls(mainName+"*_mid_Ctrl_grp")
        controlSuff="_max_Ctrl"
        print mainName+"this is mainname"
        self.DropOffControls(1, 2, 3, 31, 2, getSortedclusterSpline, ControllerSize, mainChain, mainName, nrx, nry, nrz, influencedCtrl, controlSuff)
        
    def DropOffControls(self, lowspan, span, highspan, colour, size, getSortedclusterSpline, ControllerSize, mainChain, mainName, nrx, nry, nrz, influencedCtrl, controlSuff):
        if len(influencedCtrl)>span:
            parentControllers=[]
            pairedParentControllers=[]  
            fiveclstrSplineCtrl=influencedCtrl[lowspan::span]
            #create clusters for IK chain
            for each in influencedCtrl[1::2]:
                name=each.split("_mid_Ctrl")[0]+controlSuff
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
#             getNewControls=cmds.ls(mainName+"*_max_Ctrl_grp")
            bag=[]
            for each in xrange(len(influencedCtrl) - 1):
                prev_item, current_ctrl_item, next_ctrl_item =  influencedCtrl[each - 1], influencedCtrl[each], influencedCtrl[each + 1] 
                if prev_item!=influencedCtrl[-1:][0]:
                    bag.append([prev_item, current_ctrl_item, next_ctrl_item])
            for eachPContrl, item in map(None, parentControllers, bag):
                FIRST=item[:1][0]
                SECOND=item[1:2][0]
                THIRD=item[-1:][0]
                print eachPContrl, FIRST, SECOND, THIRD
                cmds.parentConstraint(eachPContrl, FIRST, mo=1, w=.5)
                cmds.parentConstraint(eachPContrl, SECOND, mo=1, w=1.0)
                cmds.parentConstraint(eachPContrl, THIRD, mo=1, w=.5)
#         getTheNewControllers=cmds.ls(str(mainName)+"*"+str(controlSuff))
#         firstCtrl=getTheNewControllers[:1]
#         BucketValue=getClass.Percentages(influencedCtrl, 1.0, 0.0)    
#         for each in xrange(len(getTheNewControllers) - 1):
#             current_ctrl_item, next_ctrl_item = getTheNewControllers[each], getTheNewControllers[each + 1]                      
#         for child, weighted in map(None, influencedCtrl, BucketValue):  
#             try:      
#                 cmds.parentConstraint(current_ctrl_item, child, mo=1, w=weighted)
#             except:
#                 pass
#         reversedBucketValue=reversed(BucketValue)
#         for child, weighted in map(None, influencedCtrl, reversedBucketValue):
#             try:      
#                 cmds.parentConstraint(next_ctrl_item, child, mo=1, w=weighted)
#             except:
#                 pass
#         getLastChildren=influencedCtrl[-highspan:]
#         getFirstChildren=influencedCtrl[:span]    
#         print firstCtrl[0], getFirstChildren
#         self.bucketConstraint(firstCtrl[0], getFirstChildren, 0.0, 1.0)
#         getBaseControl=cmds.ls("Basename_Ctrl")
#         self.bucketConstraint(getBaseControl[0], getFirstChildren, 1.0, 0.0)  
#         getEndControl=cmds.ls("EndnameIK_Ctrl")
#         self.bucketConstraint(getEndControl, getLastChildren, 0.0, 1.0)   
#         self.bucketConstraint(getTheNewControllers[-1:], getLastChildren, 1.0, 0.0)   
        
        
    def bucketConstraint(self, controller, children, valone, valtwo):
        BucketValue=getClass.Percentages(children, valone, valtwo)
        for eachChild, eachBucketItem in map(None, children, BucketValue):
            try:
                cmds.parentConstraint(controller, eachChild, mo=1, w=eachBucketItem)
            except:
                pass 
            
            

#        if len(clstrSplineCtrl)>10:
#            tenclstrSplineCtrl=mainChain[9::10]     
#            #create clusters for IK chain
#            for each in tenclstrSplineCtrl:
#                name=each.split("_guide")[0]+"_max_Ctrl"
#                grpname=name+"_grp"     
#                tensize=ControllerSize/2
#                colour=31
#                transformWorldMatrix = cmds.xform(each, q=True, wd=1, t=True)  
#                rotateWorldMatrix = cmds.xform(each, q=True, wd=1, ro=True) 
#                getClass.buildCtrl(each, name, grpname,transformWorldMatrix, rotateWorldMatrix, tensize, colour, nrx, nry, nrz)
#                clstrCtrl.append(name)
#                cmds.setAttr(name+".sx" , keyable=0, lock=1)
#                cmds.setAttr(name+".sy" , keyable=0, lock=1)
#                cmds.setAttr(name+".sz", keyable=0, lock=1)
#                
                
#            for eachctrl in xrange(len(tenclstrSplineCtrl) - 1):
#                current_item, next_item = tenclstrSplineCtrl[eachctrl], tenclstrSplineCtrl[eachctrl + 1]   
#                getCurNumber=int(re.sub("\D", "", current_item))
#                getNextNumber=int(re.sub("\D", "", next_item))
#                for each in range(getCurNumber, getNextNumber):
#                    getNum="%02d" % (each,)
#                    print mainName+str(getNum)+clstrctrl+" middle10"
#            for each in range(1, 10):
#                getNum="%02d" % (each,)
#                print mainName+str(getNum)+clstrctrl+" first10"

        #create the IK controller       