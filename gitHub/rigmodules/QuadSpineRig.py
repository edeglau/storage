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
        getArm=cmds.ls(sl=1)
        colour=6
        if queryType==1:
            controlSize=[30, 25, 18]
        elif queryType==2:
            controlSize=[15, 12, 10]
        elif queryType==3:
            controlSize=[8, 5, 4]
        self.createLimb(controlSize)
        
    def createLimb(self, controlSize):
        getGuide=cmds.ls("*_guide")
        spine=(cmds.ls("spine*_guide"))
        spineTwist=(cmds.ls("spine*_guide"))
        
        spineSection=len(spine)/3
        sudoSpine=spine[:1]+[spine[spineSection]]+spine[-spineSection-1::spineSection+1]+spine[-1:]
       
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
        #for each in spine[::2]:
        for each in spine:            
            jointSuffix='_Clst_jnt'
            getClass.rigJoints(each, jointSuffix) 


        resetOrient=[
                    "spine01_jnt",
                    "spine01FK_jnt",
                    "spine01IK_jnt",
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
        
        FKSpineJoints=[(each) for each in cmds.listRelatives("spine01FK_jnt", ad=1, typ="joint")]
        FKSpineJoints.append("spine01FK_jnt")
        fkSpine=sorted(FKSpineJoints)
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

        clusterSpline=cmds.ls("spine*Clst_jnt")
        CLSspine=cmds.listRelatives(clusterSpline[0], ad=1, typ="joint")
        spineFK_Ctrls=[]
        spineIK_CLSTR=[]
        
        spine=cmds.ls("spine*_guide")

        if spine[ len(spine) / 2 - 1] < spine[ len(spine) / 2 ]: 
            clstrSplineCtrl=spine[ len(spine) / 2 - 1] 
        else: 
            clstrSplineCtrl=spine[ len(spine) / 2 ]         
#         clstrSplineCnt= spine[::2]
#         #clstrSplineCnt= spine       
#         clstrSplineCtrl=clstrSplineCnt[1:-1]
        clstrCtrl=[]
        
        #create the hips
        transformWorldMatrix = cmds.xform(spine[:1], q=True, wd=1, t=True)  
        rotateWorldMatrix = cmds.xform(spine[:1], q=True, wd=1, ro=True) 
        name="Hips_Ctrl"
        grpname="Hips_grp"    
        size=controlSize[0]
        colour=13
        nrx=0
        nry=1
        nrz=0      
        getClass.buildCtrl(spine[:1], name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)
        spineFK_Ctrls.append("Hips_Ctrl")    
        #spineFK_Ctrls.append(clstrCtrl)4
        
                
        #create clusters for IK chain
        lognm=clstrSplineCtrl.replace("guide", "clst")             
        name="Torso_IK_Ctrl"
        grpname="Torso_IK_grp"    
        size=controlSize[1]
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
        spineguides=cmds.ls("spine*_guide")
        for each in spineguides[::2]:
            FKTorsoJoint=each.split("_guide")[0]+"FK_jnt"  
            name=each.split("_guide")[0]+"_FK_ctrl"  
            grpname=each.split("_guide")[0]+"_FK_grp"  
            size=controlSize[1]
            colour=6
            nrx=0
            nry=1
            nrz=0    
            transformWorldMatrix = cmds.xform(each, q=True, wd=1, t=True)  
            rotateWorldMatrix = cmds.xform(each, q=True, wd=1, ro=True) 
            getClass.buildCtrl(each, name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)
            spineFK_Ctrls.append(name)
            FKCtrl.append(name)      
            cmds.parentConstraint(name, FKTorsoJoint , mo=1)            
           
        
        name="LowerBody_Ctrl"
        grpname="LowerBody_grp"    
        size=controlSize[0]
        colour=22
        nrx=0
        nry=1
        nrz=0    
        transformWorldMatrix = cmds.xform(spine[1:2], q=True, wd=1, t=True)  
        rotateWorldMatrix = cmds.xform(spine[1:2], q=True, wd=1, ro=True)          
        getClass.buildCtrl(spine[:1], name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)
        
        name="WaistFollow_Ctrl"
        grpname="WaistFollow_grp"    
        size=35
        colour=22
        nrx=0
        nry=1
        nrz=0     
        transformWorldMatrix = cmds.xform(spine[:1], q=True, wd=1, t=True)  
        rotateWorldMatrix = cmds.xform(spine[:1], q=True, wd=1, ro=True)                
        getClass.buildCtrl(spine[:1], name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)
        
        
        name="WaistFollow_offset_Ctrl"
        grpname="WaistFollow_offset_grp"    
        size=controlSize[0]
        colour=23
        nrx=0
        nry=1
        nrz=0      
        getClass.buildCtrl(spine[:1], name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)
        
        cmds.group( em=True, name='IK_grp' )
        
        #create the main controller
        
        cmds.circle(n="Master_Ctrl", r=30, nrx=0, nry=1, nrz=0)
        cmds.setAttr("Master_CtrlShape.overrideEnabled", 1)
        cmds.setAttr("Master_CtrlShape.overrideColor", 13)
        getClass.buildGrp("Master_Ctrl")        
        
        cmds.circle(n="Main_Ctrl", r=25, nrx=0, nry=1, nrz=0)
        cmds.setAttr("Main_CtrlShape.overrideEnabled", 1)
        cmds.setAttr("Main_CtrlShape.overrideColor", 17)
        getClass.buildGrp("Main_Ctrl")
        
        
        cmds.circle(n="Main_offset_Ctrl", r=27, nrx=0, nry=1, nrz=0)
        cmds.setAttr("Main_offset_CtrlShape.overrideEnabled", 1)
        cmds.setAttr("Main_offset_CtrlShape.overrideColor", 23)
        getClass.buildGrp("Main_offset_Ctrl")
        

        
        
        #create the IK controller

        name="Chest_IK_Ctrl"
        grpname="ChestIK_grp"
        num=controlSize[1]
        colour=13
        nrx=0
        nry=1
        nrz=0        
        transformWorldMatrix = cmds.xform(spine[-2:-1], q=True, wd=1, t=True)  
        rotateWorldMatrix = cmds.xform(spine[-2:-1], q=True, wd=1, ro=True) 
#         transformWorldMatrix = cmds.xform(spine[-1:], q=True, wd=1, t=True)  
#         rotateWorldMatrix = cmds.xform(spine[-1:], q=True, wd=1, ro=True) 
        getClass.buildCtrl(each, name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)
        #getClass.squareI(name, grpname, num, transformWorldMatrix, rotateWorldMatrix, colour)  
        cmds.makeIdentity("Chest_IK_Ctrl", a=True, t=1, s=1, r=1, n=0)
       

        
        OrigName="Chest_FK"
        num=controlSize[1]
        colour=6
        nrx=0
        nry=1
        nrz=0          
        eachPiece=OrigName+"_jnt"
        name=OrigName+"_Ctrl"
        grpname=OrigName+"_grp" 
        transformWorldMatrix = cmds.xform(spine[-1:], q=True, wd=1, t=True)  
        rotateWorldMatrix = cmds.xform(spine[-1:], q=True, wd=1, ro=True) 
        getClass.buildCtrl(each, name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)
        cmds.makeIdentity("Chest_FK_Ctrl", a=True, t=1, s=1, r=1, n=0)
        

        spineFK_Ctrls.append("Chest_FK_Ctrl")
 

        #IK
        
        
        #'''--------------------------------------
               # SPINE
        #--------------------------------------'''
        spineJoints=(cmds.ls("spine*_jnt"))
        lastJoint=spineJoints[-1:]
        spineTwistJnt=(cmds.ls("spine*IK_jnt"))
        spineLow=(cmds.ls("spine*FK_jnt"))
        spineCtrl=(cmds.ls("spine*_Ctrl"))
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
        cmds.ikHandle(n="spineIK", sj="spine01IK_jnt", ee=str(lastSpineJoint[0]), sol="ikSplineSolver", scv=0, ns=4, rtm=1)
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
        for each in CLSspine:
            cmds.bindSkin(each,"spineIK_crv")
        #cmds.bindSkin(clusterSpline[0],"spineIK_crv")
        
        
        cmds.addAttr("Hips_Ctrl", ln="spineFK_IK", min=0, max=1, at="double",en="FK:IK:", k=1, nn="spineFK_IK")
        cmds.setAttr("Hips_Ctrl.spineFK_IK", 1)
        
        Controller="Hips_Ctrl.spineFK_IK"
        baseSpine=[(each.split("_")[0])for each in bindSpine]
        #IK setup
        for each in baseSpine:
            getClass.blendColors(each, Controller) 

        getSortedclusterSpline=cmds.ls("spine*_Clst_jnt")
        if getSortedclusterSpline[ len(getSortedclusterSpline) / 2 - 1] < getSortedclusterSpline[ len(getSortedclusterSpline) / 2 ]: 
            clstrSplineCtrl=getSortedclusterSpline[ len(getSortedclusterSpline) / 2 - 1] 
        else: 
            clstrSplineCtrl=getSortedclusterSpline[ len(getSortedclusterSpline) / 2 ]          
        cmds.pointConstraint(clstrCtrl, clstrSplineCtrl, mo=1)
        num0, num1, num2, num3 = 1, .5, .7, .9
        colour=13
        for each in getSortedclusterSpline[1:-1]:
            name=each+"_Ctrl"
            grpname=each+"_grp"
            cmds.parent(each, w=1)
            getTranslation, getRotation=getClass.locationXForm(each)
            getClass.CCCircle(name, grpname, num0, num1, num2, num3,getTranslation, getRotation, colour)
            cmds.parentConstraint(name, each)



        fkSpine=sorted(FKSpineJoints)

        ChildActivatedValue=1
        ChildDeactivatedValue=0
        ControllerSecondValue=1
        ControllerFirstValue=0   
        Controller="Hips_Ctrl.spineFK_IK"
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

            
        #cmds.parent(spineFK_Ctrls[0], "Hips_Ctrl")
        cmds.pointConstraint("Hips_Ctrl", "spine01_jnt", mo=1)
        cmds.orientConstraint("Chest_FK_Ctrl", fkSpine[-1], mo=1)


        ChildActivatedValue=1
        ChildDeactivatedValue=0
        ControllerSecondValue=1
        ControllerFirstValue=0
        Child="Chest_IK_Ctrl.visibility"
        Controller="Hips_Ctrl.spineFK_IK"
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
        Child="Chest_FK_Ctrl.visibility"
        Controller="Hips_Ctrl.spineFK_IK"
        defaultSet=1
        getClass.controlFirstValueChildOn(Controller, 
                                           Child, 
                                           defaultSet, 
                                           ChildActivatedValue, 
                                           ChildDeactivatedValue, 
                                           ControllerSecondValue,
                                           ControllerFirstValue)
        
        #stretch
        
        getIKClass.stretchSpline("spine01IK_jnt")
        
        
        cmds.addAttr("Hips_Ctrl", ln="StretchSpine", at="enum",en="on:off:", k=1, nn="StretchSpine")
        ChildActivatedValue=2
        ChildDeactivatedValue=0
        ControllerSecondValue=1
        ControllerFirstValue=0
        Child="spine01IK_jnt_cond.operation"
        Controller="Hips_Ctrl.StretchSpine"
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
        Controller="Hips_Ctrl.spineFK_IK"
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
            
            cmds.setAttr("Hips_Ctrl.spineFK_IK", 1)  


        cmds.parent("Main_Ctrl_grp", "Main_offset_Ctrl")
        cmds.parent("Main_offset_Ctrl_grp", "Master_Ctrl")


        lastClstr=cmds.listRelatives(clstrCtrl, ap=1)  
        firstClstr=cmds.listRelatives(clstrCtrl, ap=1)             


         
#         else:
        lastFK=cmds.listRelatives(FKCtrl, ap=1) 
        firstFK=cmds.listRelatives(FKCtrl, ap=1)            
        lastFKCtrl=FKCtrl
        firstFKCtrl=FKCtrl
        
        bindSpine=[(each) for each in cmds.listRelatives("spine01_jnt", ad=1, typ="joint") if "spine" in each]

        cmds.parent(firstFK, "Hips_Ctrl")        
        cmds.parent("Hips_grp","LowerBody_Ctrl")
        cmds.parent("ChestIK_grp","LowerBody_Ctrl")
        cmds.parent("LowerBody_grp","Main_Ctrl")
        cmds.parent("spine01_jnt","Hips_Ctrl")
        cmds.parent("spine01FK_jnt","Hips_Ctrl")
        cmds.parent("spine01IK_jnt","Hips_Ctrl") 
        cmds.connectAttr("Chest_IK_Ctrl.rotate.rotateY", "spineIK.twist")
        
        cmds.parent("Main_offset_Ctrl_grp", "WaistFollow_Ctrl")
        cmds.parent("WaistFollow_grp", "WaistFollow_offset_Ctrl")
        cmds.parent("WaistFollow_offset_grp", "Master_Ctrl")
 
        
        cmds.setAttr("WaistFollow_CtrlShape.visibility" , 0)  
        cmds.setAttr("WaistFollow_offset_CtrlShape.visibility" , 0) 
        spineChildBones=[(each) for each in cmds.listRelatives('spine01_jnt', ad=1, typ="joint") if "spine" in each]
        cmds.parent("spineIK","Chest_IK_Ctrl")
        cmds.parent("spineArmParent_nod_grp", spineChildBones[0])
             
 
        seq=cmds.ls("spine*Clst_jnt")
        size=3
        getClusterChunk=[]
        getMiddleClusters=[]
        splitsize = 1.0/size*len(seq)
        for i in range(size):
            getClusterChunk.append(seq[int(round(i*splitsize)):int(round((i+1)*splitsize))])
#             getClusterChunk=[seq[i:i+size] for i  in range(0, len(seq), size)]
        for each in getClusterChunk[0]:
            cmds.parent(each, "Hips_Ctrl")
        if len(getClusterChunk[0])>1:                  
            cmds.parent(getClusterChunk[0][-1:],"Torso_IK_Ctrl")
        else:
            pass
        for each in getClusterChunk[1]:
            cmds.parent(each,"Torso_IK_Ctrl")
        for each in getClusterChunk[2]:
            cmds.parent(each, "Chest_IK_Ctrl") 
        if len(getClusterChunk[2])>1:                  
            cmds.parent(getClusterChunk[2][0],"Torso_IK_Ctrl")
        else:
            pass            
        poleAxis=("X", "Y", "Z")
        for each in poleAxis:
            cmds.connectAttr("Chest_IK_Ctrl.rotate.rotate"+each, "spineIK.poleVector.poleVector"+each)
            
            
            
            
        getMidClstr=cmds.ls("spine*_Clst_jnt_grp")
        num = float(len(getMidClstr))/size
        getMiddleClusters = [ getMidClstr [i:i + int(num)] for i in range(0, (size-1)*int(num), int(num))]
        getMiddleClusters.append(getMidClstr[(size-1)*int(num):])
        if len(getMiddleClusters[0])>1:
            cmds.parentConstraint("Hips_Ctrl", getMiddleClusters[0][0], mo=1,  w=.8)
            cmds.parentConstraint("Torso_IK_Ctrl", getMiddleClusters[0][0],  mo=1, w=.2)
            cmds.parentConstraint("Hips_Ctrl", getMiddleClusters[0][1], mo=1,  w=.4)
            cmds.parentConstraint("Torso_IK_Ctrl", getMiddleClusters[0][1],  mo=1, w=.6)            
        else:
            cmds.parentConstraint("Hips_Ctrl", getMiddleClusters[0], mo=1,  w=1.0)
        if len(getMiddleClusters[1])>1:
            cmds.parentConstraint("Hips_Ctrl", getMiddleClusters[1][0], mo=1,  w=.3)
            cmds.parentConstraint("Torso_IK_Ctrl", getMiddleClusters[1][0],  mo=1, w=.7)
            cmds.parentConstraint("Chest_IK_Ctrl", getMiddleClusters[1][1], mo=1,  w=.3)
            cmds.parentConstraint("Torso_IK_Ctrl", getMiddleClusters[1][1],  mo=1, w=.7)
        else:
            cmds.parentConstraint("Torso_IK_Ctrl", getMiddleClusters[1],  mo=1, w=1.0)
        if len(getMiddleClusters[2])>1:
            cmds.parentConstraint("Chest_IK_Ctrl", getMiddleClusters[2][0], mo=1,  w=.4)
            cmds.parentConstraint("Torso_IK_Ctrl", getMiddleClusters[2][0],  mo=1, w=.6)
            cmds.parentConstraint("Chest_IK_Ctrl", getMiddleClusters[2][1], mo=1,  w=.8)
            cmds.parentConstraint("Torso_IK_Ctrl", getMiddleClusters[2][1],  mo=1, w=.2)
        else:
            cmds.parentConstraint("Chest_IK_Ctrl", getMiddleClusters[2], mo=1,  w=1.0) 



         
        cmds.parentConstraint( "Hips_Ctrl", "Torso_IK_grp",mo=1, w=.50)  
        cmds.parentConstraint( "Chest_IK_Ctrl", "Torso_IK_grp",mo=1, w=.50)          

        #lock off head 
        cmds.parentConstraint("spineIK","spineArmParent_nod_grp", mo=1)
        ChildActivatedValue=1
        ChildDeactivatedValue=0
        ControllerSecondValue=1
        ControllerFirstValue=0
        Child="spineArmParent_nod_grp_parentConstraint1.spineIKW0"
        Controller="Hips_Ctrl.spineFK_IK"
        defaultSet=1
        getClass.controlSecondValueChildOn(Controller, 
                                           Child, 
                                           defaultSet, 
                                           ChildActivatedValue, 
                                           ChildDeactivatedValue, 
                                           ControllerSecondValue, 
                                           ControllerFirstValue)
            
            
            
            
        #create control on the ends of the IK spline
        #cmds.disconnectAttr("spine01IK_jnt_cond.outColorR", "spine06IK_jnt.scale.scaleX")
        cmds.disconnectAttr("spine01IK_jnt_cond.outColorR", "spine07IK_jnt.scale.scaleX")
        cmds.disconnectAttr("spine01IK_jnt_cond.outColorR", "spine01IK_jnt.scale.scaleX")
        
        #lock off IK spline
        Vector="X"
        YUpswitch=0
        cmds.setAttr("spineIK.dTwistControlEnable", 0)
        
        cmds.setAttr("spineIK.dWorldUpType", 4)
        cmds.setAttr("spineIK.dWorldUpAxis", 1)

        cmds.connectAttr("Hips_Ctrl.xformMatrix", "spineIK.dWorldUpMatrix", f=1)
        cmds.connectAttr("Chest_IK_Ctrl.xformMatrix", "spineIK.dWorldUpMatrixEnd", f=1)
        
        cmds.setAttr("spineIK.dWorldUpVector"+Vector, 1)
        cmds.setAttr("spineIK.dWorldUpVectorEnd"+Vector, 1)
        if YUpswitch==0:
            cmds.setAttr("spineIK.dWorldUpVectorY", YUpswitch)
            cmds.setAttr("spineIK.dWorldUpVectorEndY", YUpswitch)     
        else:
            pass        
        cmds.setAttr("spineIK.ikFkManipulation",  1)
        
        if len(FKCtrl)>1:
            lastFK=cmds.listRelatives(FKCtrl[-1:], ap=1)   
            firstFK=cmds.listRelatives(FKCtrl[:1], ap=1)          
            lastFKCtrl=FKCtrl[-1:]
            firstFKCtrl=FKCtrl[:1]
            for eachctrl in xrange(len(FKCtrl) - 1):
                current_item, next_item = FKCtrl[eachctrl], FKCtrl[eachctrl + 1]
                getParentgrp=cmds.listRelatives(next_item, ap=1)
                cmds.parent(getParentgrp[0], current_item) 
            cmds.parent("Chest_FK_grp", FKCtrl[-1:])    
        else:
            cmds.parent("Chest_FK_grp", FKCtrl[0])