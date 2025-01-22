import sys, os
filepath= os.getcwd()
sys.path.append(str(filepath))
import baseFunctions_maya
reload (baseFunctions_maya)
getClass=baseFunctions_maya.BaseClass()


import stretchIK
reload (stretchIK)
getIKClass=stretchIK.stretchIKClass()

mainName="neck"


__author__ = "Elise Deglau"
__version__ = 1.00

import maya.cmds as cmds
import maya.mel
class ChainRig(object):
    def __init__(self):
        getGuide=cmds.ls("*_guide")
        neck=(cmds.ls("neck*_guide"))
        neckTwist=(cmds.ls("neck*_guide"))
        
        neckSection=len(neck)/3
        sudoneck=neck[:1]+[neck[neckSection]]+neck[-neckSection-1::neckSection+1]+neck[-1:]
       
        cmds.select(cl=1)
        lastneckJoint=neck[-1:]
        for each in neck:
            jointSuffix='_jnt'
            getClass.rigJoints(each, jointSuffix)  
        cmds.select(cl=1)
        for each in neck:
            jointSuffix='FK_jnt'
            getClass.rigJoints(each, jointSuffix) 
        cmds.select(cl=1)        
        for each in neck:
            jointSuffix='IK_jnt'
            getClass.rigJoints(each, jointSuffix) 
        cmds.select(cl=1)
        #for each in neck[::2]:
        for each in neck:            
            jointSuffix='_Clst_jnt'
            getClass.rigJoints(each, jointSuffix) 


        resetOrient=[
                    "neck01_jnt",
                    "neck01FK_jnt",
                    "neck01IK_jnt",
                    ]
        
        for each in resetOrient:
            cmds.joint( each, e=1, children=1, zso=1, oj='xyz', sao='yup', spa=1)  
        cmds.select(cl=1)
        
        ##################################
        ##################################
        ##################################
        ##################################
        ######################CONTROLLERS
        
        translations=[".tx", ".ty", ".tz"] 
        rotation=[".rx", ".ry", ".rz"]
        
        FKneckJoints=[(each) for each in cmds.listRelatives("neck01FK_jnt", ad=1, typ="joint")]
        FKneckJoints.append("neck01FK_jnt")
        fkneck=sorted(FKneckJoints)
        bindneck=[(each) for each in cmds.listRelatives("neck01_jnt", ad=1, typ="joint") if "neck" in each]
        bindneck.append("neck01_jnt")
        lastneckJoint=bindneck[-1:]
        lastneck=lastneckJoint[0].split("_")


        colour1=18
        colour2=colour1
        colour3=colour1
        transformWorldMatrix = cmds.xform(neck[-1:], q=True, wd=1, t=True)  
        rotateWorldMatrix = cmds.xform(neck[-1:], q=True, wd=1, ro=True) 
        getClass.guideBuild(each, transformWorldMatrix, rotateWorldMatrix, colour1, colour2, colour3 )
        getsel=cmds.ls(sl=1)
        cmds.setAttr(getsel[0]+".overrideColor", colour1)
        cmds.rename(getsel[0], "neckArmParent_nod")
        getsel=cmds.ls(sl=1)
        getClass.buildGrp(getsel[0])

        clusterSpline=cmds.ls("neck*Clst_jnt")
        CLSneck=cmds.listRelatives(clusterSpline[0], ad=1, typ="joint")
        neckFK_Ctrls=[]
        neckIK_CLSTR=[]
        
        neck=cmds.ls("neck*_guide")

        if neck[ len(neck) / 2 - 1] < neck[ len(neck) / 2 ]: 
            clstrSplineCtrl=neck[ len(neck) / 2 - 1] 
        else: 
            clstrSplineCtrl=neck[ len(neck) / 2 ]         
#         clstrSplineCnt= neck[::2]
#         #clstrSplineCnt= neck       
#         clstrSplineCtrl=clstrSplineCnt[1:-1]
        clstrCtrl=[]
        
        #create the BaseNeck
        transformWorldMatrix = cmds.xform(neck[:1], q=True, wd=1, t=True)  
        rotateWorldMatrix = cmds.xform(neck[:1], q=True, wd=1, ro=True) 
        name="BaseNeck_Ctrl"
        grpname="BaseNeck_grp"    
        size=30
        colour=13
        nrx=0
        nry=1
        nrz=0      
        getClass.buildCtrl(neck[:1], name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)
        neckFK_Ctrls.append("BaseNeck_Ctrl")    
        #neckFK_Ctrls.append(clstrCtrl)4
        
                
        #create clusters for IK chain
        lognm=clstrSplineCtrl.replace("guide", "clst")             
        name="NeckSecondary_IK_Ctrl"
        grpname="NeckSecondary_IK_grp"    
        size=25
        colour=13
        nrx=0
        nry=1
        nrz=0    
        transformWorldMatrix = cmds.xform(clstrSplineCtrl, q=True, wd=1, t=True)  
        rotateWorldMatrix = cmds.xform(clstrSplineCtrl, q=True, wd=1, ro=True) 
        getClass.buildCtrl(clstrSplineCtrl, name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)
        getClass.buildGrp(name)
        clstrCtrl.append(name)
        cmds.setAttr(name+".sx" , keyable=0, lock=1)
        cmds.setAttr(name+".sy" , keyable=0, lock=1)
        cmds.setAttr(name+".sz", keyable=0, lock=1)       
        
        FKCtrl=[]
        neckguides=cmds.ls("neck*_guide")
        for each in neckguides[::2]:
            FKNeckSecondaryJoint=each.split("_guide")[0]+"FK_jnt"  
            name=each.split("_guide")[0]+"_FK_ctrl"  
            grpname=each.split("_guide")[0]+"_FK_grp"  
            size=25
            colour=6
            nrx=0
            nry=1
            nrz=0    
            transformWorldMatrix = cmds.xform(each, q=True, wd=1, t=True)  
            rotateWorldMatrix = cmds.xform(each, q=True, wd=1, ro=True) 
            getClass.buildCtrl(each, name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)
            neckFK_Ctrls.append(name)
            FKCtrl.append(name)      
            cmds.parentConstraint(name, FKNeckSecondaryJoint , mo=1)            
           
        

        cmds.group( em=True, name='IK_grp' )
        
        #create the main controller
        


        
        
        #create the IK controller

        name="EndNeckIK_Ctrl"
        grpname="EndNeckIK_grp"
        num=25
        colour=13
        nrx=0
        nry=1
        nrz=0        
        transformWorldMatrix = cmds.xform(neck[-1:], q=True, wd=1, t=True)  
        rotateWorldMatrix = cmds.xform(neck[-1:], q=True, wd=1, ro=True) 
        getClass.buildCtrl(each, name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)
        #getClass.squareI(name, grpname, num, transformWorldMatrix, rotateWorldMatrix, colour)  
        size=18
        colour=6
        nrx=0
        nry=1
        nrz=0      
        cmds.makeIdentity("EndNeckIK_Ctrl", a=True, t=1, s=1, r=1, n=0)
       

        
        OrigName="EndNeckFK"
        num=25
        colour=6
        nrx=0
        nry=1
        nrz=0          
        eachPiece=OrigName+"_jnt"
        name=OrigName+"_Ctrl"
        grpname=OrigName+"_grp" 
        transformWorldMatrix = cmds.xform(neck[-1:], q=True, wd=1, t=True)  
        rotateWorldMatrix = cmds.xform(neck[-1:], q=True, wd=1, ro=True) 
        getClass.buildCtrl(each, name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)
        cmds.makeIdentity("EndNeckFK_Ctrl", a=True, t=1, s=1, r=1, n=0)
        

        neckFK_Ctrls.append("EndNeckFK_Ctrl")

   
         
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
               # neck
        #--------------------------------------'''
        neckJoints=(cmds.ls("neck*_jnt"))
        lastJoint=neckJoints[-1:]
        neckTwistJnt=(cmds.ls("neck*IK_jnt"))
        neckLow=(cmds.ls("neck*FK_jnt"))
        neckCtrl=(cmds.ls("neck*_Ctrl"))
        #neckCtrlGrp=cmds.pickWalk(neckCtrl, d="up")
        
        '''--------------------------------------
        #            set axis for scale
        --------------------------------------'''
        scaleAxis='X'
        
        lastneckJoint=neckTwistJnt[-1:]
        
        allButLastneckJoints=neckJoints[:-1]
        '''--------------------------------------
        #            create spline IK
        --------------------------------------'''
        cmds.ikHandle(n="neckIK", sj="neck01IK_jnt", ee=str(lastneckJoint[0]), sol="ikSplineSolver", scv=0, ns=4, rtm=1)
        '''--------------------------------------
        #        find the spline of the IK
        --------------------------------------'''
        list=cmds.listConnections('neckIK', t="shape")
        cmds.rename(list, "neckIK_crv")
        '''--------------------------------------
        #        get length of spline
        --------------------------------------'''
        curvInf=cmds.arclen("neckIK_crv", ch=1)
        
        '''--------------------------------------
        #        connect the length to a multiplyDivide
        --------------------------------------'''
        MDshader=cmds.shadingNode( "multiplyDivide", au=1)
        '''--------------------------------------
        #        set multiplyDivide to Divide
        --------------------------------------'''
        cmds.setAttr(str(MDshader)+".operation", 2)
        '''--------------------------------------
        #        connect length of spline to MD node
        --------------------------------------'''
        cmds.connectAttr(curvInf+".arcLength", MDshader+".input1"+scaleAxis, f=1)
        '''--------------------------------------
        #        input the length into the second input
        --------------------------------------'''
        neckCrvLength=cmds.getAttr(MDshader+".input1"+scaleAxis)
        cmds.setAttr(MDshader+".input2"+scaleAxis,neckCrvLength)
        
        '''--------------------------------------
        #        skinbind lowres neck to the spline
        --------------------------------------'''
        for each in clusterSpline:
            cmds.bindSkin(each,"neckIK_crv")
        #cmds.bindSkin(clusterSpline[0],"neckIK_crv")
        
        
        cmds.addAttr("BaseNeck_Ctrl", ln="neckFK_IK", min=0, max=1, at="double",en="FK:IK:", k=1, nn="neckFK_IK")
        cmds.setAttr("BaseNeck_Ctrl.neckFK_IK", 1)
        
        Controller="BaseNeck_Ctrl.neckFK_IK"
        baseneck=[(each.split("_")[0])for each in bindneck]
        #IK setup
        for each in baseneck:
            getClass.blendColors(each, Controller) 

        getSortedclusterSpline=cmds.ls("neck*_Clst_jnt")
        if getSortedclusterSpline[ len(getSortedclusterSpline) / 2 - 1] < getSortedclusterSpline[ len(getSortedclusterSpline) / 2 ]: 
            clstrSplineCtrl=getSortedclusterSpline[ len(getSortedclusterSpline) / 2 - 1] 
        else: 
            clstrSplineCtrl=getSortedclusterSpline[ len(getSortedclusterSpline) / 2 ]          
        cmds.pointConstraint(clstrCtrl, clstrSplineCtrl, mo=1)
        num0, num1, num2, num3 = 1, .5, .7, .9
        colour=13
        for each in getSortedclusterSpline[1:]:
            name=each+"_Ctrl"
            grpname=each+"_grp"
            cmds.parent(each, w=1)
            getTranslation, getRotation=getClass.locationXForm(each)
            getClass.CCCircle(name, grpname, num0, num1, num2, num3, getTranslation, getRotation, colour)
            cmds.parentConstraint(name, each)



        fkneck=sorted(FKneckJoints)

        ChildActivatedValue=1
        ChildDeactivatedValue=0
        ControllerSecondValue=1
        ControllerFirstValue=0   
        Controller="BaseNeck_Ctrl.neckFK_IK"
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

            
        #cmds.parent(neckFK_Ctrls[0], "BaseNeck_Ctrl")
        cmds.pointConstraint("BaseNeck_Ctrl", "neck01_jnt", mo=1)
        cmds.orientConstraint("EndNeckFK_Ctrl", fkneck[-1], mo=1)


        ChildActivatedValue=1
        ChildDeactivatedValue=0
        ControllerSecondValue=1
        ControllerFirstValue=0
        Child="EndNeckIK_Ctrl.visibility"
        Controller="BaseNeck_Ctrl.neckFK_IK"
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
        Child="EndNeckFK_Ctrl.visibility"
        Controller="BaseNeck_Ctrl.neckFK_IK"
        defaultSet=1
        getClass.controlFirstValueChildOn(Controller, 
                                           Child, 
                                           defaultSet, 
                                           ChildActivatedValue, 
                                           ChildDeactivatedValue, 
                                           ControllerSecondValue,
                                           ControllerFirstValue)
        
        #stretch
        
        getIKClass.stretchSpline("neck01IK_jnt")
        
        
        cmds.addAttr("BaseNeck_Ctrl", ln="Stretchneck", at="enum",en="on:off:", k=1, nn="Stretchneck")
        ChildActivatedValue=2
        ChildDeactivatedValue=0
        ControllerSecondValue=1
        ControllerFirstValue=0
        Child="neck01IK_jnt_cond.operation"
        Controller="BaseNeck_Ctrl.Stretchneck"
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
        Controller="BaseNeck_Ctrl.neckFK_IK"
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
            
            cmds.setAttr("BaseNeck_Ctrl.neckFK_IK", 1)  




        lastClstr=cmds.listRelatives(clstrCtrl, ap=1)  
        firstClstr=cmds.listRelatives(clstrCtrl, ap=1)             


         
#         else:
        lastFK=cmds.listRelatives(FKCtrl, ap=1) 
        firstFK=cmds.listRelatives(FKCtrl, ap=1)            
        lastFKCtrl=FKCtrl
        firstFKCtrl=FKCtrl
        
        bindneck=[(each) for each in cmds.listRelatives("neck01_jnt", ad=1, typ="joint") if "neck" in each]

        cmds.parent(firstFK, "BaseNeck_Ctrl")        
        cmds.parent("neck01_jnt","BaseNeck_Ctrl")
        cmds.parent("neck01FK_jnt","BaseNeck_Ctrl")
        cmds.parent("neck01IK_jnt","BaseNeck_Ctrl") 
        cmds.connectAttr("EndNeckIK_Ctrl.rotate.rotateY", "neckIK.twist")

 
        

        neckChildBones=[(each) for each in cmds.listRelatives('neck01_jnt', ad=1, typ="joint") if "neck" in each]
        cmds.parent("neckIK","EndNeckIK_Ctrl")
        cmds.parent("neckArmParent_nod_grp", neckChildBones[0])
             
 
        seq=cmds.ls("neck*Clst_jnt")
        size=3
        getClusterChunk=[]
        getMiddleClusters=[]
        splitsize = 1.0/size*len(seq)
        for i in range(size):
            getClusterChunk.append(seq[int(round(i*splitsize)):int(round((i+1)*splitsize))])
#             getClusterChunk=[seq[i:i+size] for i  in range(0, len(seq), size)]
        for each in getClusterChunk[0]:
            cmds.parent(each, "BaseNeck_Ctrl")
        if len(getClusterChunk[0])>1:                  
            cmds.parent(getClusterChunk[0][-1:],"NeckSecondary_IK_Ctrl")
        else:
            pass
        for each in getClusterChunk[1]:
            cmds.parent(each,"NeckSecondary_IK_Ctrl")
        for each in getClusterChunk[2]:
            cmds.parent(each, "EndNeckIK_Ctrl") 
        if len(getClusterChunk[2])>1:                  
            cmds.parent(getClusterChunk[2][0],"NeckSecondary_IK_Ctrl")
        else:
            pass            
        poleAxis=("X", "Y", "Z")
        for each in poleAxis:
            cmds.connectAttr("EndNeckIK_Ctrl.rotate.rotate"+each, "neckIK.poleVector.poleVector"+each)
            
            
            
            
        getMidClstr=cmds.ls("neck*_Clst_jnt_grp")
        num = float(len(getMidClstr))/size
        getMiddleClusters = [ getMidClstr [i:i + int(num)] for i in range(0, (size-1)*int(num), int(num))]
        getMiddleClusters.append(getMidClstr[(size-1)*int(num):])
        if len(getMiddleClusters[0])>1:
            cmds.parentConstraint("BaseNeck_Ctrl", getMiddleClusters[0][0], mo=1,  w=.8)
            cmds.parentConstraint("NeckSecondary_IK_Ctrl", getMiddleClusters[0][0],  mo=1, w=.2)
            cmds.parentConstraint("BaseNeck_Ctrl", getMiddleClusters[0][1], mo=1,  w=.4)
            cmds.parentConstraint("NeckSecondary_IK_Ctrl", getMiddleClusters[0][1],  mo=1, w=.6)            
        else:
            cmds.parentConstraint("BaseNeck_Ctrl", getMiddleClusters[0], mo=1,  w=1.0)
        if len(getMiddleClusters[1])>1:
            cmds.parentConstraint("BaseNeck_Ctrl", getMiddleClusters[1][0], mo=1,  w=.3)
            cmds.parentConstraint("NeckSecondary_IK_Ctrl", getMiddleClusters[1][0],  mo=1, w=.7)
            cmds.parentConstraint("EndNeckIK_Ctrl", getMiddleClusters[1][1], mo=1,  w=.3)
            cmds.parentConstraint("NeckSecondary_IK_Ctrl", getMiddleClusters[1][1],  mo=1, w=.7)
        else:
            cmds.parentConstraint("NeckSecondary_IK_Ctrl", getMiddleClusters[1],  mo=1, w=1.0)
        if len(getMiddleClusters[2])>1:
            cmds.parentConstraint("EndNeckIK_Ctrl", getMiddleClusters[2][0], mo=1,  w=.4)
            cmds.parentConstraint("NeckSecondary_IK_Ctrl", getMiddleClusters[2][0],  mo=1, w=.6)
            cmds.parentConstraint("EndNeckIK_Ctrl", getMiddleClusters[2][1], mo=1,  w=.8)
            cmds.parentConstraint("NeckSecondary_IK_Ctrl", getMiddleClusters[2][1],  mo=1, w=.2)
        else:
            cmds.parentConstraint("EndNeckIK_Ctrl", getMiddleClusters[2], mo=1,  w=1.0) 



         
        cmds.parentConstraint( "BaseNeck_Ctrl", "NeckSecondary_IK_grp",mo=1, w=.50)  
        cmds.parentConstraint( "EndNeckIK_Ctrl", "NeckSecondary_IK_grp",mo=1, w=.50)          

        #lock off head 
        cmds.parentConstraint("neckIK","neckArmParent_nod_grp", mo=1)
        ChildActivatedValue=1
        ChildDeactivatedValue=0
        ControllerSecondValue=1
        ControllerFirstValue=0
        Child="neckArmParent_nod_grp_parentConstraint1.neckIKW0"
        Controller="BaseNeck_Ctrl.neckFK_IK"
        defaultSet=1
        getClass.controlSecondValueChildOn(Controller, 
                                           Child, 
                                           defaultSet, 
                                           ChildActivatedValue, 
                                           ChildDeactivatedValue, 
                                           ControllerSecondValue, 
                                           ControllerFirstValue)
            
            
            
            
        #create control on the ends of the IK spline
        #cmds.disconnectAttr("neck01IK_jnt_cond.outColorR", "neck06IK_jnt.scale.scaleX")
#         cmds.disconnectAttr("neck01IK_jnt_cond.outColorR", "neck07IK_jnt.scale.scaleX")
#         cmds.disconnectAttr("neck01IK_jnt_cond.outColorR", "neck01IK_jnt.scale.scaleX")
        
        
        if len(FKCtrl)>1:
            lastFK=cmds.listRelatives(FKCtrl[-1:], ap=1)   
            firstFK=cmds.listRelatives(FKCtrl[:1], ap=1)          
            lastFKCtrl=FKCtrl[-1:]
            firstFKCtrl=FKCtrl[:1]
            for eachctrl in xrange(len(FKCtrl) - 1):
                current_item, next_item = FKCtrl[eachctrl], FKCtrl[eachctrl + 1]
                getParentgrp=cmds.listRelatives(next_item, ap=1)
                cmds.parent(getParentgrp[0], current_item) 
            cmds.parent("EndNeckFK_grp", FKCtrl[-1:])    
        else:
            cmds.parent("EndNeckFK_grp", FKCtrl[0])
            
        cmds.bindSkin("neck04_Clst_jnt","neckIK_crv.cv[4]")