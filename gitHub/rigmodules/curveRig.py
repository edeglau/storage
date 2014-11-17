import sys, os
filepath= os.getcwd()
sys.path.append(str(filepath))
import baseFunctions_maya
reload (baseFunctions_maya)
getClass=baseFunctions_maya.BaseClass()


import stretchIK
reload (stretchIK)
getIKClass=stretchIK.stretchIKClass()

'''MG rigging modules'''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons License'
'http://creativecommons.org/licenses/by-sa/3.0/au/'

import maya.cmds as cmds
import maya.mel
class SpineRig(object):
    def __init__(self):
        getGuide=cmds.ls("*_guide")
        neck=(cmds.ls("neck*_guide"))
        head=(cmds.ls("head*_guide"))
        spine=(cmds.ls("spine*_guide"))
        
        spineTwist=(cmds.ls("spine*_guide"))
        
        spineSection=len(spine)/3
        neckTwist=[neck[0]]+["head01_guide"]
        
        sudoSpine=spine[:1]+[spine[spineSection]]+spine[-spineSection-1::spineSection+1]+spine[-1:]
        
        getLimbs=(neck, head, spine)         
        cmds.select(cl=1)
        lastSpineJoint=spine[-1:]
        for each in spine:
            jointSuffix='_jnt'
            getClass.rigJoints(each, jointSuffix)  
        cmds.select(cl=1)
        for each in spine:
            jointSuffix='FK_jnt'
            getClass.rigJoints(each, jointSuffix) 
        cmds.select(cl=1)   
        for each in spine:
            jointSuffix='IK_jnt'
            getClass.rigJoints(each, jointSuffix) 
        cmds.select(cl=1)
        for each in spine[::2]:
            jointSuffix='_Clst_jnt'
            getClass.rigJoints(each, jointSuffix) 
        getTranslation=cmds.xform("neck01_guide", q=1, t=1) 
        cmds.joint(p=getTranslation)  
        cmds.select(cl=1)
        for each in neck:
            jointSuffix='_jnt'
            getClass.rigJoints(each, jointSuffix)     
            cmds.select(cl=1)    
        cmds.select(cl=1)
        for each in head:
            jointSuffix='_jnt'
            getClass.rigJoints(each, jointSuffix)      
        cmds.select(cl=1)
        
        try:
            neckChildBones=cmds.listRelatives('neck01_jnt', ad=1, typ="joint")
            lastNeckJoint=neckChildBones[:1]
        except:
            lastNeckJoint='neck01_jnt'
        
        
        spineChildBones=cmds.listRelatives('spine01_jnt', ad=1, typ="joint")
        cmds.parent("neck01_jnt", spineChildBones[:1])
        cmds.parent("head01_jnt", lastNeckJoint)
        
        resetOrient=[
                    "spine01_jnt",
                    "spine01FK_jnt",
                    "spine01IK_jnt",
                    "head01_jnt"
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
        
        loResSpine=[(each) for each in cmds.listRelatives("spine01FK_jnt", ad=1, typ="joint")]
        loResSpine.append("spine01FK_jnt")
        bindSpine=[(each) for each in cmds.listRelatives("spine01_jnt", ad=1, typ="joint") if "spine" in each]
        bindSpine.append("spine01_jnt")
        lastSpineJoint=bindSpine[-1:]
        lastSpine=lastSpineJoint[0].split("_")

        colour1=18
        colour2=colour1
        colour3=colour1
        transformWorldMatrix = cmds.xform(spine[-1:], q=True, wd=1, t=True)  
        rotateWorldMatrix = cmds.xform(spine[-1:], q=True, wd=1, ro=True) 
        getClass.guideBuild(each, transformWorldMatrix, rotateWorldMatrix, colour1, colour2, colour3 )
        getsel=cmds.ls(sl=1)
        cmds.setAttr(getsel[0]+".overrideColor", colour1)
        cmds.rename(getsel[0], "spineArmParent_nod")
        getsel=cmds.ls(sl=1)
        getClass.buildGrp(getsel[0])
        
        CLSspine=cmds.listRelatives("spine01_Clst_jnt", ad=1, typ="joint")
        getCLSspine=[(each) for each in CLSspine if "spine" in each]
        getSpineClstParts=spine[1:-1]
        spineFK_Ctrls=[]
        spineIK_CLSTR=[]
        
        spine=cmds.ls("spine*_guide")
        clstrSplineCnt= spine[::2]
        clstrSplineCtrl=clstrSplineCnt[1:-1]
        clstrCtrl=[]
        FKCtrl=[]
        #create clusters for IK chain
        for each in clstrSplineCtrl:
            name=each+"_ctrl"
            grpname=each+"_grp"     
            size=12
            colour=13
            nrx=0
            nry=1
            nrz=0    
            transformWorldMatrix = cmds.xform(each, q=True, wd=1, t=True)  
            rotateWorldMatrix = cmds.xform(each, q=True, wd=1, ro=True) 
            getClass.buildCtrl(each, name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)
            getClass.buildGrp(name)
            clstrCtrl.append(name)
            name=each+"FK_ctrl"
            grpname=each+"FK_grp"   
            size=10
            colour=6
            nrx=0
            nry=1
            nrz=0    
            transformWorldMatrix = cmds.xform(each, q=True, wd=1, t=True)  
            rotateWorldMatrix = cmds.xform(each, q=True, wd=1, ro=True) 
            getClass.buildCtrl(each, name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)
            #getClass.buildGrp(name)        
#             cmds.setAttr(each+"FK_ctrl.tx", l=1, cb=0)
#             cmds.setAttr(each+"FK_ctrl.ty", l=1, cb=0)
#             cmds.setAttr(each+"FK_ctrl.tz", l=1, cb=0)
            FKCtrl.append(name)

        
        #create the hips
        transformWorldMatrix = cmds.xform(spine[:1], q=True, wd=1, t=True)  
        rotateWorldMatrix = cmds.xform(spine[:1], q=True, wd=1, ro=True) 
        name="Hips_ctrl"
        grpname="Hips_grp"    
        size=12
        colour=22
        nrx=0
        nry=1
        nrz=0      
        getClass.buildCtrl(spine[:1], name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)
        spineFK_Ctrls.append("Hips_ctrl")
        spineFK_Ctrls.append(FKCtrl)      
        #spineFK_Ctrls.append(clstrCtrl)
        
        name="UpperBody_ctrl"
        grpname="UpperBody_grp"    
        size=16
        colour=13
        nrx=0
        nry=1
        nrz=0      
        getClass.buildCtrl(spine[:1], name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)

        
        
        
        cmds.group( em=True, name='IK_grp' )
        
        #create the main controller
        
        cmds.circle(n="Master_ctrl", r=30, nrx=0, nry=1, nrz=0)
        cmds.setAttr("Master_ctrlShape.overrideEnabled", 1)
        cmds.setAttr("Master_ctrlShape.overrideColor", 13)
        getClass.buildGrp("Master_ctrl")        
        
        cmds.circle(n="Main_ctrl", r=25, nrx=0, nry=1, nrz=0)
        cmds.setAttr("Main_ctrlShape.overrideEnabled", 1)
        cmds.setAttr("Main_ctrlShape.overrideColor", 17)
        getClass.buildGrp("Main_ctrl")
        
        
        cmds.circle(n="Main_offset_ctrl", r=27, nrx=0, nry=1, nrz=0)
        cmds.setAttr("Main_offset_ctrlShape.overrideEnabled", 1)
        cmds.setAttr("Main_offset_ctrlShape.overrideColor", 23)
        getClass.buildGrp("Main_offset_ctrl")
        

        
        
        #create the IK controller

        name="Chest_ctrl"
        num=12
        colour=13
        transformWorldMatrix = cmds.xform(spine[-1:], q=True, wd=1, t=True)  
        rotateWorldMatrix = cmds.xform(spine[-1:], q=True, wd=1, ro=True) 
        getClass.squareI(name, num, transformWorldMatrix, rotateWorldMatrix, colour)
        cmds.move(0, -num/3, 0, "Chest_ctrl" ,r=1, rpr=1, )
        cmds.move(0, num/3, 0, "Chest_ctrl.rotatePivot" ,r=1, rpr=1 )
        cmds.makeIdentity("Chest_ctrl", a=True, t=1, s=1, r=1, n=0)

        
        name="Body_ctrl"
        num=9
        colour=6
        transformWorldMatrix = cmds.xform(spine[-1:], q=True, wd=1, t=True)  
        rotateWorldMatrix = cmds.xform(spine[-1:], q=True, wd=1, ro=True) 
        getClass.cubeI(name, num, transformWorldMatrix, rotateWorldMatrix, colour)
        cmds.move(0, -num, 0, "Body_ctrl" ,r=1, rpr=1, )
        cmds.move(0, num, 0, "Body_ctrl.rotatePivot" ,r=1, rpr=1 )
        cmds.makeIdentity("Body_ctrl", a=True, t=1, s=1, r=1, n=0)
        spineFK_Ctrls.append("Body_ctrl")
        
        #makehead
        
        OrigName= "head01"
        colour1=6
        colour2=colour1
        colour3=colour1
        size=15
        colour=13
        nrx=0
        nry=1
        nrz=0   
        eachPiece=OrigName+"_jnt"
        name=OrigName+"_ctrl"
        grpname=OrigName+"_grp" 
        getTranslation, getRotation=getClass.locationXForm(eachPiece)
        getClass.buildCtrl(each, name, grpname,getTranslation, getRotation, size, colour, nrx, nry, nrz)
        cmds.move(0, size, 0, "head01_ctrl" ,r=1, rpr=1, )
        cmds.move(0, -size, 0, "head01_ctrl.rotatePivot" ,r=1, rpr=1 )
        cmds.makeIdentity("head01_ctrl", a=True, t=1, s=1, r=1, n=0)
        
         
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
               # SPINE
        #--------------------------------------'''
        spineJoints=(cmds.ls("spine*_jnt"))
        lastJoint=spineJoints[-1:]
        spineTwistJnt=(cmds.ls("spine*IK_jnt"))
        spineLow=(cmds.ls("spine*FK_jnt"))
        spineCtrl=(cmds.ls("spine*_ctrl"))
        #spineCtrlGrp=cmds.pickWalk(spineCtrl, d="up")
        
        '''--------------------------------------
        #            set axis for scale
        --------------------------------------'''
        scaleAxis='X'
        
        lastSpineJoint=spineTwistJnt[-1:]
        
        allButLastspineJoints=spineJoints[:-1]
        '''--------------------------------------
        #            create spline IK
        --------------------------------------'''
        cmds.ikHandle(n="spineIK", sj="spine01IK_jnt", ee=str(lastSpineJoint[0]), sol="ikSplineSolver", scv=0, ns=3, rtm=1)
        '''--------------------------------------
        #        find the spline of the IK
        --------------------------------------'''
        list=cmds.listConnections('spineIK', t="shape")
        cmds.rename(list, "spineIK_crv")
        '''--------------------------------------
        #        get length of spline
        --------------------------------------'''
        curvInf=cmds.arclen("spineIK_crv", ch=1)
        
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
        spineCrvLength=cmds.getAttr(MDshader+".input1"+scaleAxis)
        cmds.setAttr(MDshader+".input2"+scaleAxis,spineCrvLength)
        
        '''--------------------------------------
        #        skinbind lowres spine to the spline
        --------------------------------------'''
        cmds.bindSkin("spine01_Clst_jnt","spineIK_crv")
        
        
        cmds.addAttr("Hips_ctrl", ln="spineFK_IK", at="enum",en="FK:IK:", k=1, nn="spineFK_IK")
        cmds.setAttr("Hips_ctrl.spineFK_IK", 1)
        
        
        baseSpine=[(each.split("_")[0])for each in bindSpine]
        #IK setup
        for each in baseSpine:
            getClass.blendColors(each) 
        
        
        for each in baseSpine:
            cmds.connectAttr("Hips_ctrl.spineFK_IK", each+"_blnd.blender", f=1)
            cmds.connectAttr("Hips_ctrl.spineFK_IK", each+"_sblnd.blender", f=1)
        
        for each in CLSspine:
            cmds.parent(each, w=1)
        
        
        #cmds.parentConstraint("Chest_ctrl", getCLSspine[0], mo=1)
        getSortedclusterSpline=cmds.ls("spine*_Clst_jnt")
        #spineIK_CLSTR=cmds.ls("spine*_clstr_ctrl")
        
        #connect IK to cluster spline
        cmds.parentConstraint("Hips_ctrl", "spine01_Clst_jnt ", mo=1)
        
        #cmds.parentConstraint("Chest_ctrl", getSortedclusterSpline[-1:], mo=1)
        cmds.parentConstraint("Chest_ctrl", getSortedclusterSpline[-1:], mo=1)
        
        for each, item in map(None, getSortedclusterSpline[1:-1], clstrCtrl):
            cmds.pointConstraint(item, each, mo=1)
           
        fkSpline=sorted(loResSpine)
        sortedSpline=fkSpline[::2]
        for each, item in map(None, fkSpline[::2], spineFK_Ctrls):            
            cmds.parentConstraint(item, each, mo=1)
        #constrain FK spin to controls
        
        
        #for each, item in map(None, sortedSpline[1:], spineFK_Ctrls):
         
            
#         for nextControl, eachControl in enumerate(spineFK_Ctrls[:-1]):
#             currentItem = eachControl
#             nextItem = spineFK_Ctrls[(nextControl+1)%len(spineFK_Ctrls)]
#             getParentgrp=cmds.listRelatives(nextItem, ap=1)
#             cmds.parent(getParentgrp, currentItem)    
            
        #cmds.parent(spineFK_Ctrls[0], "Hips_ctrl")
        cmds.pointConstraint("Hips_ctrl", "spine01_jnt", mo=1)
        
        cmds.orientConstraint("head01_ctrl", "head01_jnt", mo=1)
        
        bindneck=[(each) for each in cmds.listRelatives("neck01_jnt", ad=1, typ="joint") if "neck" in each]
        if len(bindneck)>1:
            cmds.parentConstraint(bindneck[:1], "head01_grp", mo=1)
        else:
            cmds.parentConstraint("neck01_jnt", "head01_grp", mo=1)
        #cmds.pointConstraint("Chest_ctrl", "head01_grp", mo=1)
        

        
        cmds.setAttr("Hips_ctrl.spineFK_IK", 1)
        cmds.setAttr("Chest_ctrl.visibility", 1)
        cmds.setDrivenKeyframe("Chest_ctrl.visibility", cd="Hips_ctrl.spineFK_IK")
        cmds.setAttr("Hips_ctrl.spineFK_IK", 0)
        cmds.setAttr("Chest_ctrl.visibility", 0)
        cmds.setDrivenKeyframe("Chest_ctrl.visibility", cd="Hips_ctrl.spineFK_IK")
        cmds.setAttr("Hips_ctrl.spineFK_IK", 1)

        
        #stretch
        
        getIKClass.stretchSpline("spine01IK_jnt")
        
        
        cmds.addAttr("Hips_ctrl", ln="StretchSpine", at="enum",en="on:off:", k=1, nn="StretchSpine")
        
        cmds.setAttr("spine01IK_jnt_cond.operation", 2)
        cmds.setDrivenKeyframe("spine01IK_jnt_cond.operation", cd="Hips_ctrl.StretchSpine")
        cmds.setAttr("Hips_ctrl.StretchSpine", 1)
        cmds.setAttr("spine01IK_jnt_cond.operation", 0)
        cmds.setDrivenKeyframe("spine01IK_jnt_cond.operation", cd="Hips_ctrl.StretchSpine")
        cmds.setAttr("Hips_ctrl.StretchSpine", 1)



        cmds.parent("Main_ctrl_grp", "Main_offset_ctrl")
        cmds.parent("Main_offset_ctrl_grp", "Master_ctrl")

        if len(clstrCtrl)>1:
            lastClstr=cmds.listRelatives(clstrCtrl[-1:], ap=1) 
            firstClstr=cmds.listRelatives(clstrCtrl[:1], ap=1) 
#             lastClstr=clstrCtrl[-1:]
#             firstClstr=clstrCtrl[:1]
        else:
            lastClstr=cmds.listRelatives(clstrCtrl, ap=1)  
            firstClstr=cmds.listRelatives(clstrCtrl, ap=1)             
            #lastClstr=clstrCtrl
            #firstClstr=clstrCtrl

        if len(FKCtrl)>1:
            lastFK=FKCtrl[-1:]  
            firstFK=FKCtrl[:1]           
            #lastFK=FKCtrl[-1:]
            #firstFK=FKCtrl[:1]
        else:
            lastFK=FKCtrl
            firstFK=FKCtrl            
            #lastFK=FKCtrl
            #firstFK=FKCtrl
        cmds.parent("Body_ctrl_grp", lastFK)
        cmds.parent(firstFK, "Hips_ctrl")
        cmds.parent("Hips_grp","UpperBody_ctrl")
        
        #cmds.orientConstraint("Body_ctrl", "Chest_ctrl", mo=1)
        #cmds.pointConstraint( "Chest_ctrl", "Body_ctrl")
        
        #cmds.parent("Body_ctrl_grp",lastFK)

        #cmds.parent(firstClstr, "Hips_ctrl")        
        #cmds.parent("Chest_ctrl_grp", "Body_ctrl")
        #cmds.parent("Chest_ctrl_grp", "Body_ctrl")

     
        #cmds.parent("UpperBody_grp","Body_ctrl")

        getMaster_IKCtrls=["Chest_ctrl", "Hips_ctrl"]
        getClstr_ctrls=clstrCtrl
        for item in getMaster_IKCtrls:
            for each in getClstr_ctrls:
                cmds.parentConstraint(item, each, mo=1, w=.5)
          