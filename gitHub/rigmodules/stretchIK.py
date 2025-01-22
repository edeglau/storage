import os, sys
import maya.cmds as cmds

'''MG rigging modules'''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons License'
'http://creativecommons.org/licenses/by-sa/3.0/au/'

scaleAxis="X"
getfilePath=str(__file__)
filepath= os.getcwd()

sys.path.append(str(filepath))
import baseFunctions_maya
reload (baseFunctions_maya)
getClass=baseFunctions_maya.BaseClass()
class stretchIKClass():
    
    def getSel(self):
        getbones=cmds.ls(sl=1)[0]#get selection
        self.stretch(getbones)
        
    def stretch(self, getbones):
        childBones=cmds.listRelatives(getbones, ad=1, typ="joint")#get all child bones
        alljoints=childBones
        alljoints.append(getbones)#make full list of bones
        self.create_ik_stretch(alljoints, getbones)
        
    def create_ik_stretch(self, alljoints, getbones):
        getDistances=[]
        for nextControl, eachControl in enumerate(alljoints[:-1]):
            current_item = eachControl
            next_item = alljoints[(nextControl+1)%len(alljoints)]
            curTran = cmds.xform(current_item, q=True, ws=1, t=True)
            nextTran = cmds.xform(next_item, q=True, ws=1, t=True)
            selDistance=cmds.distanceDimension(sp=(curTran[0], curTran[1], curTran[2]), ep=(nextTran[0], nextTran[1], nextTran[2]))#create distance measure 
            getlocs=cmds.listConnections(selDistance)
            cmds.pointConstraint(current_item,getlocs[0],mo=0, w=1 )#DO NOT PARENT CONSTRAIN. it will create cycle loop.
            cmds.pointConstraint(next_item,getlocs[1],mo=0, w=1 )    
            getDist=cmds.getAttr(selDistance+".distance")#get the distance
            getDistances.append(getDist)
            cmds.delete(getlocs)
        fullDistance=sum(getDistances)
        getIKEffector=cmds.listRelatives(getbones, ad=1, typ="ikEffector")#find effector 
        getIKHandle=cmds.listConnections(getIKEffector[0], d=1, t="ikHandle")#now i can find ikhandle
        selDistance=cmds.distanceDimension(sp=(0, 0 ,0), ep=(1, 1 ,1))#create distance measure 
        getIKLocators=cmds.listConnections(selDistance)#get the distance locators to point constrain
        cmds.pointConstraint(getbones,getIKLocators[0],mo=0, w=1 )#DO NOT PARENT CONSTRAIN. it will create cycle loop.
        cmds.pointConstraint(getIKHandle[0],getIKLocators[1],mo=0, w=1 )
        getDistance=cmds.getAttr(selDistance+".distance")#get the distance
        MultDivNode=cmds.shadingNode( "multiplyDivide", au=1, n=getbones+'_md')
        ConditionNode=cmds.shadingNode( "condition", au=1, n=getbones+"_cond")
        cmds.setAttr(str(MultDivNode)+".operation", 2)#change to divide
        cmds.setAttr(str(ConditionNode)+".operation", 2)#change to greater than
        cmds.connectAttr(selDistance+".distance", MultDivNode+".input1.input1"+scaleAxis, f=1)#set default length on input of divide
        cmds.connectAttr(selDistance+".distance", ConditionNode+".firstTerm", f=1)#set default on first term when greater than
        cmds.connectAttr(MultDivNode+".output.output"+scaleAxis, ConditionNode+".colorIfTrue.colorIfTrueR", f=1)#divide outputscaleX to color is greater than
        cmds.setAttr(ConditionNode+".secondTerm", fullDistance)#set default length on second term of greaterThan
        cmds.setAttr(MultDivNode+".input2"+scaleAxis, fullDistance)#set default length on second input of divide
        cmds.rename(getIKLocators[0], getbones+'_bdloc')
        cmds.rename(getIKLocators[1], getbones+'_edloc')
        getpartransform=cmds.listRelatives(selDistance, ap=1, typ="transform")
        cmds.rename(getpartransform[0], getbones+'_dis')
        for each in alljoints[1:]:
            cmds.connectAttr(ConditionNode+".outColor.outColorR",each+".scale.scale"+scaleAxis, f=1)#set divide on scale X of each bone except for last bone
        conditionNode=str(ConditionNode)+".operation"
        return conditionNode

    def stretchSpline(self, getbones):
        childBones=cmds.listRelatives(getbones, ad=1, typ="joint")
        alljoints=childBones
        alljoints.append(getbones)#make full list of bones
        getIKEffector=cmds.listRelatives(getbones, ad=1, typ="ikEffector")#find effector 
        getIKHandle=cmds.listConnections(getIKEffector[0], d=1, t="ikHandle")#now i can find ikhandle
        getCurve=cmds.listConnections(getIKHandle[0], d=1, t="nurbsCurve")#now i can find curve
        getShape=cmds.listRelatives(getCurve[0], ad=1, typ="nurbsCurve")#now i can find shape
        curvInf=cmds.arclen(getShape[0], ch=1)#get shape length
        getDistance=cmds.getAttr(curvInf+".arcLength")
        MultDivNode=cmds.shadingNode( "multiplyDivide", au=1, n=getbones+'_md')
        ConditionNode=cmds.shadingNode( "condition", au=1, n=getbones+"_cond")
        cmds.setAttr(str(MultDivNode)+".operation", 2)#change to divide
        cmds.setAttr(str(ConditionNode)+".operation", 2)#change to greater than
        cmds.connectAttr(curvInf+".arcLength", MultDivNode+".input1.input1"+scaleAxis, f=1)#set default length on input of divide
        cmds.connectAttr(curvInf+".arcLength", ConditionNode+".firstTerm", f=1)#set default on first term when greater than
        cmds.connectAttr(MultDivNode+".output.output"+scaleAxis, ConditionNode+".colorIfTrue.colorIfTrueR", f=1)#divide outputscaleX to color is greater than
        cmds.setAttr(ConditionNode+".secondTerm", getDistance)#set default length on second term of greaterThan
        cmds.setAttr(MultDivNode+".input2"+scaleAxis, getDistance)#set default length on second input of divide
        for each in alljoints[1:]:
            cmds.connectAttr(ConditionNode+".outColor.outColorR",each+".scale.scale"+scaleAxis, f=1)#set divide on scale X of each bone except for last bone
        
    def get_ik_chain(self, Controller, ikHandle):
        boneBag=[]
        getbones=ikHandle
        try:
            getEndJnt=[cmds.connectionInfo(getbones+".endEffector", sfd=1)]
            pass
        except:
            print "select a controller to add an attribute and an ikHandle" 
            return
        getfirstJnt=[cmds.connectionInfo(getbones+".startJoint", sfd=1)]
        getEndJntName=[cmds.connectionInfo(getEndJnt[0].split(".")[0]+".translateX", sfd=1)]
        firstJoint=getfirstJnt[0].split(".")[0]
        cmds.joint( firstJoint, e=1, children=1, zso=1, oj='xyz', sao='yup', spa=1)
#         boneBag.append(firstJoint)
        endJoint=getEndJntName[0].split(".")[0]
        getTree=cmds.listRelatives(endJoint, p=1, f=1)
        getEach=getTree[0].split("|")
        boneBag.append(endJoint)
        for each in reversed(getEach[1:]):
            boneBag.append(each)
        print boneBag
        Child=self.create_ik_stretch(boneBag, firstJoint)
        cmds.addAttr(Controller, ln="Stretch", at="enum",en="on:off:", k=1, nn="Stretch")
        ChildActivatedValue=2
        ChildDeactivatedValue=0
        ControllerSecondValue=1
        ControllerFirstValue=0
        Controller=Controller+".Stretch"
        defaultSet=0
        getClass.controlFirstValueChildOn(Controller, 
                                           Child, 
                                           defaultSet, 
                                           ChildActivatedValue, 
                                           ChildDeactivatedValue, 
                                           ControllerSecondValue,
                                           ControllerFirstValue)
        
#         childBones=cmds.listRelatives(firstJoint, ad=1, typ="joint")#get all child bones
#         alljoints=childBones
#         alljoints.append(firstJoint)#make full list of bones
#         self.create_ik_stretch(alljoints, getbones)   


     
