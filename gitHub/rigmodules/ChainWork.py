import sys, os, platform
from pymel.core import *
OSplatform=platform.platform()

# if "Windows" in OSplatform:
#     gtepiece=getfilePath.split("\\")
#     getRigModPath='/'.join(gtepiece[:-2])+"\rigModules"
#     scriptPath="D:\\code\\git\\myGit\\gitHub\\rigModules"
#     sys.path.append(str(scriptPath))
# 
#     getToolArrayPath=str(scriptPath)+"\Tools.py"
#     exec(open(getToolArrayPath))
#     toolClass=ToolFunctions()      
#     
# if "Linux" in OSplatform: 
#     scriptPath="//usr//people//elise-d//workspace//techAnimTools//personal//elise-d//rigModules"
#     sys.path.append(str(scriptPath))
# 
#     getToolArrayPath=str(scriptPath)+"/Tools.py"
#     exec(open(getToolArrayPath))
#     toolClass=ToolFunctions()
# 
#     gtepiece=getfilePath.split("/")  
#     getRigModPath='/'.join(gtepiece[:-2])+"/rigModules"


# from inspect import getsourcefile
# from os.path import abspath
# getfilePath=str(abspath(getsourcefile(lambda _: None)))
# print getfilePath
# if "Windows" in OSplatform:
#     gtepiece=getfilePath.split("\\")
# if "Linux" in OSplatform: 
#     gtepiece=getfilePath.split("/")  

# # getRigModPath='/'.join(gtepiece[:-2])+"/rigModules"
# getRigModPath="//usr//people//elise-d//workspace//techAnimTools//personal//elise-d//rigModules//"


# sys.path.append(str(getRigModPath))

# basepath=str(getRigModPath)+"/baseFunctions_maya.py"
# exec(open(basepath))
# getClass=BaseClass()

# stretchIKpath=str(getRigModPath)+"/stretchIK.py"
# exec(open(stretchIKpath))
# getIKClass=stretchIKClass()

# getToolArrayPath=str(getRigModPath)+"/Tools.py"
# exec(open(getToolArrayPath))
# toolClass=ToolFunctions()


import baseFunctions_maya
reload (baseFunctions_maya)
getClass=baseFunctions_maya.BaseClass()
sys.path.append(str(getClass))

import stretchIK
reload (stretchIK)
getIKClass=stretchIK.stretchIKClass()
sys.path.append(str(getIKClass))


import Tools
reload (Tools)
toolClass=Tools.ToolFunctions()
sys.path.append(str(toolClass))








# filepath= os.getcwd()
# sys.path.append(str(filepath))
# import baseFunctions_maya
# reload (baseFunctions_maya)
# getClass=baseFunctions_maya.BaseClass()


# import stretchIK
# reload (stretchIK)
# getIKClass=stretchIK.stretchIKClass()


# from inspect import getsourcefile
# from os.path import abspath
# getfilePath=str(abspath(getsourcefile(lambda _: None)))
# gtepiece=getfilePath.split("/")
# getRigModPath='/'.join(gtepiece[:-2])+"/rigModules"


# if "Windows" in OSplatform:
#     gtepiece=getRigModPath.split("\\")
# if "Linux" in OSplatform: 
#     gtepiece=getRigModPath.split("/")  
# #name
# mainName="neck"
# #controllerdirection
# nrx=0
# nry=1
# nrz=0  

'''MG rigging modules'''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons Attribution 4.0 International 4.0 (CC BY 4.0)'
'http://creativecommons.org/licenses/by/4.0/'
# 'This work is licensed under a Creative Commons Attribution-ShareAlike 3.0 Australia (CC BY-SA 3.0 AU)'
# 'http://creativecommons.org/licenses/by-sa/3.0/au/'


guide="_guide"
# clstrctrl="_Clst_jnt_Ctrl"




import maya.cmds as cmds
import maya.mel
class ChainRig(object):

    def build_chain(self, arg=None):
        axisList=["X", "Y", "Z"] 
        influenceList= ["curved", "straight"] 
        winName = "Create chain"
        winTitle = winName
        if cmds.window(winName, exists=True):
                deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=350, h=150 )
        cmds.menuBarLayout(h=30)
        stringField='''"ChainRig" - (launches window) FK and IK chain(use the tail guide layout) if you've chosen a 
    particular axis for your guides, use the same axis for your controls.(the spheres have a 
    colored shape to help guide the dimensions they are building in. (this is still in 
    development. use at own risk)'''
        self.fileMenu = cmds.menu( label='Help', hm=1, pmc=lambda *args:toolClass.helpWin(stringField))  
        rowColumnLayout  (' selectArrayRow ', nr=1, w=350)
        frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')      
        rowLayout  (' rMainRow ', w=350, numberOfColumns=6, p='selectArrayRow')
        columnLayout ('selectArrayColumn', parent = 'rMainRow')
        setParent ('selectArrayColumn')
        separator(h=10, p='selectArrayColumn')
        gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))
        direction=optionMenu( label='Axis')
        for each in axisList:
            menuItem( label=each)   
        curveInf=optionMenu( label='Curve Influence')
        for each in influenceList:
            menuItem( label=each)                     
        cmds.text(label="", w=80, h=25)            
        cmds.text(label="name", w=80, h=25)             
        self.namefield=cmds.textField(w=40, h=25, p='listBuildButtonLayout', text="name")
        cmds.text(label="size", w=80, h=25) 
        self.size=cmds.textField(w=40, h=25, p='listBuildButtonLayout', text="10") 
        gridLayout('BuildButtonLayout', p='selectArrayColumn', numberOfColumns=3, cellWidthHeight=(100, 20))             
        button (label='Tail guides',bgc=[0.8, 0.75, 0.6], p='BuildButtonLayout', command = lambda *args:self._tail_guides())
        button (label='Build guides',bgc=[0.8, 0.75, 0.6], p='BuildButtonLayout', command = lambda *args:self._build_guides())
        button (label='Build chain', p='BuildButtonLayout', command = lambda *args:self.create_Chain(ControllerSize=int(textField(self.size,q=1, text=1)), mainName=textField(self.namefield,q=1, text=1), getDir=optionMenu(direction, q=1, v=1), crvInf=optionMenu(curveInf, q=1, v=1)))
        showWindow(window)

    def _tail_guides(self, arg=None):
        getguideFilepath='/'.join(gtepiece[:-2])+"/guides/combinedGuides.py"
        exec(open(getguideFilepath))
        getguideClass=GuideUI()
        getguideClass.build_tail_guides()

    def _build_guides(self, arg=None):
        getguideFilepath='/'.join(gtepiece[:-2])+"/guides/combinedGuides.py"
        exec(open(getguideFilepath))
        getguideClass=GuideUI()
        getguideClass.build_helper_guides()

    def create_Chain(self, ControllerSize, mainName, getDir, crvInf):
        if getDir=="X":
            nrx=1
            nry=0
            nrz=0  
        if getDir=="Y":
            nrx=0
            nry=1
            nrz=0   
        if getDir=="Z":
            nrx=0
            nry=0
            nrz=1
        # self.mainName =mainName
        # self.ControllerSize=ControllerSize


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
            name=each.split("_guide")[0]+"_FK_Ctrl"  
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
        getGuide=cmds.ls("*_guide")
        valueBucket=[]
        for each in getGuide:
            each=ls(each)[0]
            pgetCVpos=each.getTranslation()
            valueBucket.append(pgetCVpos)
#         CurveMake = cmds.curve(n=mainName+"IK_crv", d=3, p=valueBucket) 
#         cmds.ikHandle(n=mainName+"IK", sj=mainName+"01IK_jnt", ee=str(lastmainChainJoint[0]), sol="ikSplineSolver", ccv=0, c=CurveMake, ns=4, rtm=1, tws="easeIn")
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

        print "building medium controllers"
        controllerType="_med_grp"
        childControllers=ls(mainName+"IKcrv*_clstrHandle_grp_Ctrl_grp")
        childCurve=mainName+"IK_crv"
        parentCurve=mainName+"_med_lead_crv"
        size, colour= 2, 22
        microLeadCurve=ls(childCurve)
        CVbucket=self.getCurveCVs(microLeadCurve)  
        medLeadCurveNum=len(CVbucket)/4
        medLeadCurve, getNum=self.dupCurve(childCurve, parentCurve, medLeadCurveNum)
        self.macroControls(medLeadCurve, mainName, controllerType, childControllers, microLeadCurve, childCurve, parentCurve, size, colour, nrx, nry, nrz, getNum, medLeadCurveNum)

        if crvInf == "curved":
            self.curvedLine(mainName, mainChain, ControllerSize, nrx, nry, nrz)
        elif crvInf=="straight":
            self.straightLine(mainName, nrx, nry, nrz)

        print "Tidying up"
        self.tidyUp(mainName)



    #getCVs
    def getCurveCVs(self, microLeadCurve):
        CVbucket=[]
        for eachCurve in microLeadCurve:
            getCurve=ls(eachCurve)[0]
            for eachCV in getCurve.cv:
                CVbucket.append(eachCV)
        return CVbucket
    
    #duplicating curve
    def dupCurve(self, childCurve, parentCurve, divNum):
        medLeadCurve=cmds.duplicate(childCurve, n=parentCurve)
        cmds.rebuildCurve(medLeadCurve, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=1, s=divNum, d=3, tol=1e-06)
        # cmds.rebuildCurve(medLeadCurve, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=divNum, d=3, tol=0)        
        CVbucket=self.getCurveCVs(medLeadCurve)       
        return medLeadCurve, CVbucket
    
    #building new controllers
    def macroControls(self, medLeadCurve, mainName,controllerType, childControllers,microLeadCurve, childCurve, parentCurve,size, colour, nrx, nry, nrz, getNum, medLeadCurveNum):
        CVbucketList=[]
        collectJack=[]
        for eachCurve in medLeadCurve:
            getCurve=ls(eachCurve)[0]
            for index, eachCV in enumerate(getCurve.cv):
                transformWorldMatrix=eachCV.getPosition()    
                rotateWorldMatrix=[0.0, 0.0, 0.0]                            
                tempname=mainName+str(index)+"none"
                tempgrpname=mainName+str(index)+"none_grp"
                tempsize, tempcolour= 6, 6
                getClass.JackI(tempname, tempgrpname, tempsize, transformWorldMatrix, rotateWorldMatrix, tempcolour)
                collectJack.append(tempname)
            for eachCV, eachJack in map(None, getCurve.cv, xrange(len(collectJack) - 1)):  
                # transformWorldMatrixNext=next_item.getPosition()
                try:
                    current_item, next_item =collectJack[eachJack], collectJack[eachJack + 1]
                except:
                    pass                
                getNum=re.sub("\D", "", str(eachCV))
                getNum=int(getNum)
                getNum="%02d" % (getNum,)
                aname=controllerType.split("_grp")[0]+"_Ctrl"
                name=mainName+str(getNum)+aname
                grpname= mainName+str(getNum)+controllerType
                CVbucketList.append(eachCV)
                transformWorldMatrix=eachCV.getPosition()
                rotateWorldMatrix=[0.0, 0.0, 0.0]            
                select(eachCV, r=1)
                getNewClust=cmds.cluster()
                getClass.buildCtrl(eachCV, name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)
                getNewCtrl=cmds.ls(sl=1, fl=1)
                try:
                    cmds.select(next_item, r=1)
                    cmds.select(grpname, add=1)
                    cmds.aimConstraint(offset=[0,0, 0], weight=1, aimVector=[1, 0, 0] , upVector=[0, 1, 0] ,worldUpType="vector" ,worldUpVector=[0, 1, 0])
                    cmds.delete(next_item+"_grp")
                except:
                    pass
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
        #attach controllers to new parent curve
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
        

    def straightLine(self, mainName,  nrx, nry, nrz):
        print "building major controllers"
        controllerType="_maj_grp"
        childControllers=ls(mainName+"*_med_grp")
        childCurve=mainName+"_med_lead_crv"
        parentCurve=mainName+"_maj_lead_crv"
        size, colour= 4, 29
        microLeadCurve=ls(childCurve) 
        CVbucket=self.getCurveCVs(microLeadCurve)  
        medLeadCurveNum=len(CVbucket)/5
        medLeadCurve, getNum=self.dupCurve(childCurve, parentCurve, medLeadCurveNum)
        self.macroControls(medLeadCurve, mainName, controllerType, childControllers, microLeadCurve, childCurve, parentCurve, size, colour, nrx, nry, nrz, getNum, medLeadCurveNum)
 
        print "building maximum controllers"
        controllerType="_max_grp"
        childControllers=ls(mainName+"*_maj_grp")
        childCurve=mainName+"_maj_lead_crv"
        parentCurve=mainName+"_max_lead_crv"
        size, colour= 6, 30
        microLeadCurve=ls(childCurve)  
        medLeadCurveNum=1
        medLeadCurve, getNum=self.dupCurve(childCurve, parentCurve, medLeadCurveNum)
        self.macroControls(medLeadCurve, mainName, controllerType, childControllers, microLeadCurve, childCurve, parentCurve, size, colour, nrx, nry, nrz, getNum, medLeadCurveNum)
        print "adding maximum controllers to rig"  
        getMaxCtrls=cmds.ls(mainName+"*_max_grp")
        for each in getMaxCtrls:
            cmds.parent(each, mainName+"Main_Ctrl")

    def curvedLine(self, mainName, mainChain, ControllerSize, nrx, nry, nrz):
        print "adding maximum controllers to rig" 
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
        cmds.setAttr(name+".sx" , keyable=0, lock=1)
        cmds.setAttr(name+".sy" , keyable=0, lock=1)
        cmds.setAttr(name+".sz", keyable=0, lock=1)

        #create the IK controller

        #create the Base"+mainChain+"
        transformWorldMatrix = cmds.xform(mainChain[:1], q=True, wd=1, t=True)  
        rotateWorldMatrix = cmds.xform(mainChain[:1], q=True, wd=1, ro=True) 
        name="Base"+mainName+"_Ctrl"
        grpname="Base"+mainName+"_grp"    
        size=ControllerSize
        colour=13   
        getClass.buildCtrl(mainChain[:1], name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)  


        name="End"+mainName+"IK_Ctrl"
        grpname="End"+mainName+"IK_grp"
        num=20
        colour=13

        transformWorldMatrix = cmds.xform(mainChain[-1:], q=True, wd=1, t=True)  
        rotateWorldMatrix = cmds.xform(mainChain[-1:], q=True, wd=1, ro=True) 
        getClass.buildCtrl(mainChain[-1:], name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)
        #getClass.squareI(name, grpname, num, transformWorldMatrix, rotateWorldMatrix, colour)  
        size=ControllerSize-2
        colour=6     
        cmds.makeIdentity("End"+mainName+"IK_Ctrl", a=True, t=1, s=1, r=1, n=0)        

        #===============================================================================
        # 
        #===============================================================================
        print "linking main controls for influence"
        #===============================================================================
        # 
        #===============================================================================
        getMidClstr=cmds.ls(mainName+"*_med_grp")
        firstpart, secondpart = getMidClstr[:len(getMidClstr)/2], getMidClstr[len(getMidClstr)/2:] 
        minWeightValue=0.0 
        maxWeightValue=1.0
        BucketValue=getClass.Percentages(secondpart, minWeightValue, maxWeightValue)
        for eachCluser, weighted in map(None,secondpart, BucketValue):
            cmds.parentConstraint( "End"+mainName+"IK_Ctrl", eachCluser, mo=1, w=weighted)  
        for eachCluser, weighted in map(None, reversed(secondpart), BucketValue):
            cmds.parentConstraint( mainName+"Secondary_IK_Ctrl", eachCluser, mo=1, w=weighted) 
        
        
        firstlist=(firstpart)
        reversedBucket=[]
        firstlist= reversed(firstlist)
        for each in firstlist:
            reversedBucket.append(each)
        print reversedBucket
        #beginning
        minWeightValue=0.0 
        maxWeightValue=1.0
        BucketValue=getClass.Percentages(reversedBucket, minWeightValue, maxWeightValue)
        for eachCluser, weighted in map(None, reversedBucket, BucketValue):
            cmds.parentConstraint( "Base"+mainName+"_Ctrl", eachCluser, mo=1, w=weighted) 
        for eachCluser, weighted in map(None, reversed(reversedBucket), BucketValue):
            cmds.parentConstraint( mainName+"Secondary_IK_Ctrl", eachCluser, mo=1, w=weighted) 

            
        cmds.parent("End"+mainName+"IK_grp",mainName+"Main_Ctrl")
        cmds.parent(mainName+"Secondary_IK_Ctrl",mainName+"Main_Ctrl")
        cmds.parent("Base"+mainName+"_Ctrl",mainName+"Main_Ctrl")        


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
        cmds.parent(mainName+"02_FK_grp", mainName+"Main_Ctrl")
        getClstrCtrlrs=cmds.ls(mainName+"IKcrv*_clstrHandle_grp_Ctrl_grp")
        for each in getClstrCtrlrs:
            cmds.parent(each, mainName+"_Rig")
        #create controller sets

        cmds.select(cl=1)
        getControllerSets=[(each) for each in cmds.ls(mainName+"Main_Ctrl") if cmds.nodeType(each)=="transform"]
        cmds.sets(n=mainName+"_Controllers")

        getControllerSets=[(each) for each in cmds.ls("*max_Ctrl") if cmds.nodeType(each)=="transform"]
        if len(getControllerSets)>0:
            cmds.sets(getControllerSets, n=mainName+"max_Controllers")
            cmds.sets(mainName+"max_Controllers", add=mainName+"_Controllers")

        getControllerSets=[(each) for each in cmds.ls("*maj_Ctrl") if cmds.nodeType(each)=="transform"]
        if len(getControllerSets)>0:        
            cmds.sets(getControllerSets, n=mainName+"maj_Controllers")
            cmds.sets(mainName+"maj_Controllers", add=mainName+"_Controllers")

        getControllerSets=[(each) for each in cmds.ls("*med_Ctrl") if cmds.nodeType(each)=="transform"]
        if len(getControllerSets)>0:
            cmds.sets(getControllerSets, n=mainName+"med_Controllers")
            cmds.sets(mainName+"med_Controllers", add=mainName+"_Controllers")

        getControllerSets=[(each) for each in cmds.ls("*_clstrHandle_grp_Ctrl") if cmds.nodeType(each)=="transform"]
        if len(getControllerSets)>0:
            cmds.sets(getControllerSets, n=mainName+"micro_Controllers")
            cmds.sets(mainName+"micro_Controllers", add=mainName+"_Controllers")

        getControllerSets=[(each) for each in cmds.ls("*FK_Ctrl") if cmds.nodeType(each)=="transform"]
        if len(getControllerSets)>0:
            cmds.sets(getControllerSets, n=mainName+"FK_Controllers")
            cmds.sets(mainName+"FK_Controllers", add=mainName+"_Controllers")

        #create skin joint set
        grpone=cmds.ls("*FK_jnt")
        grptwo=cmds.ls("*IK_jnt")
        removeFromControllers=grpone+grptwo
        getControllerSets=[(each) for each in cmds.ls(mainName+"*_jnt", type="joint") if each not in removeFromControllers]
        cmds.sets(getControllerSets, n=mainName+"skinjoints")       
