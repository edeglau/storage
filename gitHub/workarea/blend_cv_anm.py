# from numpy import arange
# #from pymel.core import *
# import baseFunctions_maya
# import pymel.core as pm
# import sys, os, imp, inspect, getpass, re, platform, glob, time, operator
# getBaseClass=baseFunctions_maya.BaseClass()
# softwareID=os.getpid()
# OSplatform=platform.platform()

# blendShapes=[]
# getSel=cmds.ls(sl=1, fl=1)
# if len(getSel)<1:
#   print "select smething"
# else:
#   try:
#       getShape=[(grab) for item in getSel for grab in cmds.listRelatives(item, ad=1, typ="shape") if "Orig" not in grab]
#       getCurveTransforms=[(eachParentTransform) for eachShape in getShape for eachParentTransform in cmds.listRelatives(cmds.ls(eachShape)[0], p=1)]
#       for eachItem in getShape:
#           eachconnect=cmds.listConnections((cmds.ls(eachItem)[0]))
#           blendShapes=[(blended) for blended in eachconnect if cmds.nodeType(cmds.ls(blended)[0]) =="blendShape"]
#       blendShapes=list(set(blendShapes))
#   except:
#       print "Selected not right type"
from numpy import arange
#from pymel.core import *
import baseFunctions_maya
import pymel.core as pm
import sys, os, imp, inspect, getpass, re, platform, glob, time, operator
getBaseClass=baseFunctions_maya.BaseClass()
softwareID=os.getpid()
OSplatform=platform.platform()
eachCacheNode="blendShape"
blendShapes=[]
getSel=cmds.ls(sl=1, fl=1)


findThisType="blendShape"
collect=[]
for each in getSel:
    getShape=[(athing) for athing in cmds.listRelatives(each, ad=1, type="shape") if "Orig" not in athing]
    if getShape != None:
        for item in getShape:
            blendShapes=[(nodes) for nodes in cmds.listHistory(item) if cmds.nodeType(nodes) == findThisType]


class blendShapeCurveWeights():
    def __init__(self):
        self.winTitle='blends'
    def createBlendWin(self):
        if cmds.window(self.winTitle, exists=True):
            cmds.deleteUI(self.winTitle)
            
        self.window=cmds.window(self.winTitle, title=self.winTitle, tbm=1, w=380, h=300)
        
        cmds.rowColumnLayout('selectArrWin' , nr=1, w=300, h=300)
        cmds.frameLayout("lrow", label="", lv=0, nch=1, borderStyle='out', bv=1, p='selectArrWin')
        
        self.blendShape_Node=cmds.optionMenu(label="blendshape", w=150)
        for each in blendShapes:
            cmds.menuItem(label=each, p=self.blendShape_Node)
        cmds.columnLayout()
        self.curveGUI=cmds.gradientControlNoAttr("falloffCurve", h=90)
        
        cmds.button(label="set", command=lambda *args:self.execute_go())
        cmds.button(label="anim", command=lambda *args:self.execute_go_anim())
        #cmds.button(label="anim", command=lambda *args:self.execute_go_anim2())
        cmds.button(label="reset", command=lambda *args:self.reset_weight())
        cmds.button(label="print", command=lambda *args:self.execute_go_anim3())
        cmds.showWindow()

    def execute_go(self):
        getSel=cmds.ls(sl=1, fl=1)
        getShape, getTransform=self.getTransformsAndShapes(getSel)
        getBlendShape=self.getBlendShapeNodeSelected()
        blendShapeInputCurves=self.makeBlendShapeAttrDictionary(getBlendShape, getSel)
        weightList, getCVrange=self.buildWeightBucket(getTransform)
        self.blendWeightExecutionCallup(getCVrange, weightList, blendShapeInputCurves, getTransform)



    def execute_go_anim(self):
        getSel=cmds.ls(sl=1, fl=1)
        getShape, getTransform=self.getTransformsAndShapes(getSel)
        getBlendShape=self.getBlendShapeNodeSelected()
        blendShapeInputCurves=self.makeBlendShapeAttrDictionary(getBlendShape, getSel)
        weightList, getCVrange=self.buildWeightBucket(getTransform)
        self.blendWeightExecutionCallup_anim(getCVrange, weightList, blendShapeInputCurves, getTransform)

    def execute_go_anim2(self):
        getSel=cmds.ls(sl=1, fl=1)
        getShape, getTransform=self.getTransformsAndShapes(getSel)
        getBlendShape=self.getBlendShapeNodeSelected()
        blendShapeInputCurves=self.makeBlendShapeAttrDictionary(getBlendShape, getSel)
        weightList, getCVrange=self.buildWeightBucket(getTransform)
        self.blendWeightExecutionCallup_animV2(getCVrange, weightList, blendShapeInputCurves, getTransform)
        
    def execute_go_anim3(self):
        getSel=cmds.ls(sl=1, fl=1)
        getShape, getTransform=self.getTransformsAndShapes(getSel)
        getBlendShape=self.getBlendShapeNodeSelected()
        blendShapeInputCurves=self.makeBlendShapeAttrDictionary(getBlendShape, getSel)
        weightList, getCVrange=self.buildWeightBucket(getTransform)
        self.print_out(getCVrange, weightList, blendShapeInputCurves, getTransform)
        
    def refresh(self):
        blendShapes=[]
        getSel=cmds.ls(sl=1, fl=1)
        menuItems=cmds.optionMenu(self.blendShape_Node, q=1, ill=1)
        if menuItems:
            cmds.deleteUI(menuItems)
        if len(getSel)<1:
            print "select smething"
        else:
            try:
                getShape=[(grab) for item in getSel for grab in cmds.listRelatives(item, ad=1, typ="shape") if "Orig" not in grab]
                getCurveTransforms=[(eachParentTransform) for eachShape in getShape for eachParentTransform in cmds.listRelatives(cmds.ls(eachShape)[0], p=1)]
                for eachItem in getShape:
                    eachconnect=cmds.listConnections((cmds.ls(eachItem)[0]))
                    blendShapes=[(blended) for blended in eachconnect if cmds.nodeType(cmds.ls(blended)[0]) =="blendShape"]
                blendShapes=list(set(blendShapes))
            except:
                print "Selected not right type"
            blendShapeDrop=cmds.optionMenu(self.blendShape_Node, e=1)
            for each in blendShapes:
                cmds.menuItem(label=each, p=self.blendShape_Node)   
        self.blendWeightExecutionCallup(getCVrange, weightList, blendShapeInputCurves, getTRansforms)
    
    
    def getBlendShapeNodeSelected(self):
        blendName=cmds.optionMenu(self.blendShape_Node, q=1, sl=1)
        getBlendShape=cmds.optionMenu(self.blendShape_Node, q=1, value=1)
        return getBlendShape
        
    def blendWeightExecutionCallupV2(self, getCVrange, weightList, blendShapeInputCurves, getSel):
        '''>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..
        cv weight name in blendshape template: cmds.select('blendShape1.inputTarget[1].inputTargetGroup[0].targetWeights[4]')
        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'''
        setAttrDict={}
        print weightList      
        for eachCVInCaptureRange, targetWeightValue in map(None, getCVrange, weightList):
            print str(eachCVInCaptureRange)+"each cv"
            print str(targetWeightValue)+"target weight value"            
            for blendConnection, eachCurve in blendShapeInputCurves.items():
                next_item=pm.ls(eachCurve)[0]
                if next_item in getSel:
                    for eachCV in pm.PyNode(next_item).cv:
                        findName=eachCV.split('.cv')[1]
                        builtAttribute=blendConnection+findName
                        if eachCV.index() == eachCVInCaptureRange:
                            makeDict={builtAttribute:targetWeightValue}
                            setAttrDict.update(makeDict)
        for key, value in setAttrDict.items():
            print key, value
            cmds.setAttr(key, value)


    def blendWeightExecutionCallup(self, getCVrange, weightList, blendShapeInputCurves, getSel):
        '''>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..
        cv weight name in blendshape template: cmds.select('blendShape1.inputTarget[1].inputTargetGroup[0].targetWeights[4]')
        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'''
        setAttrDict={}
        print blendShapeInputCurves
        print weightList
        for eachCVInCaptureRange, targetWeightValue in map(None, getCVrange, weightList):
            for blendConnection, eachCurve in blendShapeInputCurves.items():
                # print "continue"
                # if '|' in eachCurve:
                #     next_item = eachCurve.split('|')[1]
                # else:
                next_item=pm.ls(eachCurve, an=1)[0] 
                for eachCV in pm.PyNode(next_item).cv:
                    findName=eachCV.split('.cv')[1]
                    builtAttribute=blendConnection+findName
                    if eachCV.index() == eachCVInCaptureRange:
                        makeDict={builtAttribute:targetWeightValue}
                        setAttrDict.update(makeDict)
            for key, value in setAttrDict.items():
                # print key+" setting at "+ str(value)
                cmds.setAttr(key, value)



    def blendWeightExecutionCallup_anim(self, getCVrange, weightList, blendShapeInputuCrves, getSel):
        '''>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..
        cv weight name in blendshape template: cmds.select('blendShape1.inputTarget[1].inputTargetGroup[0].targetWeights[4]')
        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'''
        if len(blendShapeInputuCrves)>1:
            self.add_anim(getCVrange, weightList, blendShapeInputuCrves, getSel)
        else:
            self.first_anim(getCVrange, weightList, blendShapeInputuCrves, getSel)
        
    def add_anim(self, getCVrange, weightList, blendShapeInputCurves, getSel):
        grab_branch=[]
        for each in blendShapeInputCurves:
            if "_targetWeights" in each:
                grab_branch.append(each)
        component=sorted(grab_branch)
        getcurrent=cmds.currentTime(q=1)
        for key, value in map(None, component, weightList):
            complete=key.split('targetWeights')[:-1]
            key='targetWeights'.join(complete)            
            cmds.setKeyframe( key, t=getcurrent, v=value )  

    def first_anim(self, getCVrange, weightList, blendShapeInputCurves, getSel):
        '''>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..
        cv weight name in blendshape template: cmds.select('blendShape1.inputTarget[1].inputTargetGroup[0].targetWeights[4]')
        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'''
        setAttrDict={}
        for eachCVInCaptureRange, targetWeightValue in map(None, getCVrange, weightList):
            for blendConnection, eachCurve in blendShapeInputCurves.items():
                next_item=pm.ls(eachCurve)[0]
                if next_item in getSel:
                    for eachCV in pm.PyNode(next_item).cv:
                        findName=eachCV.split('.cv')[1]
                        builtAttribute=blendConnection+findName
                        if eachCV.index() == eachCVInCaptureRange:
                            makeDict={builtAttribute:targetWeightValue}
                            setAttrDict.update(makeDict)
        getcurrent=cmds.currentTime(q=1)
        for key, value in setAttrDict.items():
            cmds.setAttr(key, value)
            cmds.setKeyframe( key, t=getcurrent, at=key, v=value ) 
            
            
    def print_out(self, getCVrange, weightList, blendShapeInputCurves, getSel):
        print len(blendShapeInputCurves)
        '''>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..
        cv weight name in blendshape template: cmds.select('blendShape1.inputTarget[1].inputTargetGroup[0].targetWeights[4]')
        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'''
        for each in blendShapeInputCurves:
            print each
            
    def reset_weight(self):
        getSel=[]
        getSel=cmds.ls(sl=1, fl=1)
        weightValue=0.0
        getcurveForFindingCV=pm.ls(getSel[0])[0]
        endCV=len(pm.PyNode(getCurveForFindingCV).cv)
        getCVrange=arange(0, endCV, 1)
        getBlendShape=self.getBlendShapeNodeSelected()
        blendShapeInputs=self.makeBlendShapeAttrDictionary(getBlendShape, getSel)
        weightList=[]
        for each in range(len(getCVrange)):
            weightList.append(weightValue)
        setAttrDict={}
        for eachCVInCaptureRange, targetWeightValue in map(None, getCVrange, weightList):
            for blendConnection, eachCurve in blendShapeInputs.items():
                next_item=pm.ls(eachCurve)[0]
                if next_item in getSel:
                    for eachCV in pm.PyNode(next_item).cv:
                        findName=eachCV.split('.cv')[1]
                        builtAttribute=blendConnection+findName
                        if eachCV.index() == eachCVInCaptureRange:
                            makeDict={builtAttribute:targetWeightValue}
                            setAttrDict.update(makeDict)
        for key, value in setAttrDict.items():
            cmds.setAttr(key, value)
        
        
        
    def buildWeightBucket(self, getSel):
        getCurveForFindingCV=pm.ls(getSel)[0]
        endCV=len(pm.PyNode(getCurveForFindingCV).cv)
        getCVrange=arange(0, endCV, 1)
        minWeightValue, maxWeightValue=0.0, 1.0
        weightList=[]
        lengthList=getBaseClass.Percentages(getCVrange, 0.0, 1.0)
        for each in lengthList:
            getInfo=cmds.gradientControlNoAttr(self.curveGUI, q=1, valueAtPoint=each)
            weightList.append(getInfo)
        return weightList, getCVrange
        
    def getTransformsAndShapes(self, getSel):
        print getSel
        getShape=[(grab) for item in getSel for grab in cmds.listRelatives(item, ad=1, typ="shape", f=1) if "Orig" not in grab]
        getcurveTransforms=[(eachParentTransform) for eachShape in getShape for eachParentTransform in cmds.listRelatives(cmds.ls(eachShape), p=1, f=1)]
        return getShape, getcurveTransforms
    def makeBlendShapeAttrDictionary(self, getBlendShape, getSel):
        setInputList=[]
        outPutCurve=[]
        blendShapeInputCurves={}
        getSource=cmds.listConnections(getBlendShape, c=1, s=1)
        getDest=cmds.listConnections(getBlendShape, c=1, d=1)
        for each in xrange(len(getSource)-1):
            current_item, next_item=getSource[each], getSource[each+1]
            if "inputTarget" in current_item:
                findAttribute=current_item.split("inputTargetItem")[0]+"targetWeights"
                setInputList.append(findAttribute)
        for eachout in xrange(len(getDest)-1):
            current_item, next_item=getDest[eachout], getDest[eachout+1]
            if "outputGeometry" in current_item:
                outPutCurve.append(next_item)
        for eachInput, curveitem in map(None, setInputList, outPutCurve):
            createDict={eachInput:curveitem}
            blendShapeInputCurves.update(createDict)
        return blendShapeInputCurves
    
    
inst=blendShapeCurveWeights()
inst.createBlendWin()
