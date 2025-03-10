import maya.cmds as cmds
from pymel.core import *
class myGrps():
    def ta_grps(self):
        getGroups=["INPUT_GRP", "OUTPUT_GRP", "DEFORMERS_GRP"]
        getSel=ls(sl=1, fl=1)
        getGrps=[]
        for each in getGroups:
            CreateEmptyGroup()
            newGrp=ls(sl=1, fl=1)
            rename(newGrp[0], each)
            getGrps.append(each)
            for item in getSel:
                newDupe=duplicate(item)
                parent(newDupe, each)
                rename(newDupe[0], item)
        if ls("DEFORMERS_GRP"):
            getMeshController=ls("DEFORMERS_GRP")[0]
            pass      
        else:
            print "'DEFORMERS_GRP' missing"
            return
        if ls("OUTPUT_GRP"):
            getMeshTarget=ls("OUTPUT_GRP")[0]
            pass
        else:
            print "'OUTPUT_GRP' group missing"
            return                 
        self.grps_defined(getMeshController, getMeshTarget)
        
    def grab_grp(self): 
        selObj=ls(sl=1, fl=1)
        getMeshController=selObj[1]
        getMeshTarget=selObj[0]
        self.grps_defined(getMeshController, getMeshTarget)
                    
    def grps_defined(self, getMeshController, getMeshTarget):
        getChildrenController=[(each) for each in getMeshController.getChildren() if getMeshController.name() == each.getParent() and each.type()=="transform" for item in each.getChildren() if item.type() =="mesh"]        
        if getChildrenController==None:
            getChildrenController=([getChildrenController])
        getChildrenTarget=[(each) for each in getMeshTarget.getChildren() if getMeshTarget.name() == each.getParent() and each.type()=="transform" for item in each.getChildren() if item.type() =="mesh"]     
        if getChildrenTarget==None:
            getChildrenTarget=([getChildrenTarget])
        self.create_wrap_callup(getChildrenController, getChildrenTarget)

    def create_wrap_callup(self, getChildrenController, getChildrenTarget):            
        for eachCtrl, eachTgt in map(None, getChildrenController, getChildrenTarget):
            if eachCtrl.nodeName()==eachTgt.nodeName():
                deformer(eachTgt, type="wrap")
                select(eachTgt, r=1)
                select(eachCtrl, add=1)
                cmds.AddWrapInfluence()
