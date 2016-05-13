from numpy import arange
from pymel.core import *
import baseFunctions_maya
getBaseClass=baseFunctions_maya.BaseClass()


blendShapes=[]
getSel=cmds.ls(sl=1, fl=1)
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


class blendShapeCurveWEights():
	def __init__(self, winName=blends):
		self.winTitle="blends"
		self.winName=winName
	def createBlendWin(self):
		if cmds.window(self.winName, exists=True):
			cmds.deleteUI(self.winName)
		self.window=cmds.window(self.winName, title=self.winTitle, tbm=1, w=380, h=300)
		cmds.rowColumnLayout('selectArrWin' , nr=1, w=300, h=300)
		cmds.frameLayout("lrow", label="", lv=0, nch=1, borderStyle='out', bv=1,, p='selectArrWin')
		self.blendShape_node=cmds.optionMenu(label="blendshape", w=150)
		for each in blendsShapes:
			cmds.menuItem(label=each)
		cmds.columnLayout()
		self.curveGUI=cmds.gradientControlNoAttr("falloffCurve", h=90)
		
		cmds.button(label"set", command=lambda *args:self.execute_go())
		cmds.showWindow()

def exectute_go(self):
    getSel=cmds.ls(sl=1, fl=1)
    getShape, getTransform=self.getTransformsAndShapes(getSel)
    getBlendShape=self.getBlendShapeNodeSelected()
    blendShapeInputCurves=self.makeBlendShapeAttrDictionary(getBlendShape)
    weightList, getCVrange=self.buildWeigthBucket(getTransforms)
    self.blendWeigthExecutionCallup(getCVrange, weightList, blendShapeInputCurves, getTRansforms)


def getBlendShapeNodeSelected(self)
    blendName=cmds.optionMenu(self.blendShape_Node, q=1, sl=1)
    getBlendShape=cmds.optionMenu(self.blendShape_Node, q=1, value=1)
    return getBlendShape
    
def blendWeigthExecutionCallup(self, CVrange, weightList, blendShapeInputCurves, getSel)
    setAttrDict={}
    for eachCVInCaptureRange, targetWeightValue in map(None, getCVrange, weightList):
        for blendConnection, eachCurve in blendShapeInputCurves.items():
            next_item=pm.ls(eachCurve)[0]
            if next_item in getSel:
                for eachcv in pm.PyNode(next_item).cv:
                	findName=eachcv.split('.cv')[1]
                	builtAttribute=blendConnection+findName
                	if eachCV.index == eachCVInCaptureRange:
	                    makeDict={builtAttribute:targetWeightValue}
	                    setAttrDict.update(makeDict)
    for key, value in setAttrDict.index():
        cmds.setAttr(key, value)

def buildWeigthBucket(self, getSel)
    getCurveForFindingCV=ls(getSel)[0]
    endCV=len(getCurveForFindingCV.cv)
    getCVrange=arange(endCV, 1)
    minWeightValue, maxWeightValue=0.0, 1.0
    weightList=[]
    lengthList=getBaseClass.Percentages(getCVrange, 0.0, 1.0)
    for each in lengthList:
        getInfo=cmds.gradientControlNoAttr(self.curveGUI, q=1, valueAtPoint=each)
        weightList.append(getInfo)
    return weightList, getCVrange
    
def getTranformsAndShapes(self, getSel):
    getShape=[(grab) for item in getSel for grab in cmds.listRelatives(item, ad=1, typ="shape", f=1) if "Orig" not in grab]
    getcurveTransforms=[(eachParentTransform) for eachShape in getShape for eachPArentTRansform in cmds.listRelatives(cmds.ls(eachShape), p=1, f=1)]
    return getShape, getcurveTransforms

def makeBlendshapeAttrDictionary(self, getBlendShape):
    setInputList=[]
    outPutCurve=[]
    for each in xrange(len(getSource)-1):
        current_item, next_item=getSource[each], getSource[each+1]
        if "inputTarget" in current_item:
            findAttribute=current_item.split("inputTargetItem")[0]+"targetWeights"
            setInputList.append(findAttribute)
    for each in xrange(len(getDest)-1):
        current_item, next_item=getDest[each], getDest[each+1]
        if "outputGeometry" in current_item:
        outPutCurve.append(next_item)
    for each, item in map(None, setInputList, outPutCurve):
        createDict={each:item}
        blendShapeInputs.update(createDict)
    return blendShapeInputCurves















#BlendShapeNode="blendShape12"
#rangeObjsWithBlends=arange(0, 168, 1)
#getCVrange=arange(0, 25, 1)



collectNewNumbers=[]

getBlendShape=cmds.ls(sl=1, fl=1)


minWeightValue=0.0#input
maxWeightValue=1.0#input



getSource=cmds.listConnections(getBlendShape[0], s=1)
blendShapeInputs={}
getDest=cmds.listConnections(getBlendShape[0], d=1)
setInputList=[]
outPutCurve=[]

for each in xrange(len(getSource)-1):
  current_item, next_item=getSource[each], getSource[each+1]
  if "inputTarget" in current_item:
    findAttribute=current_item.split("inputTargetItem")[0]+"targetWeights"
    setInputList.append(findAttribute)
for each in xrange(len(getDest)-1):
  current_item, next_item=getDest[each], getDest[each+1]
  if "outputGeometry" in current_item:
    outPutCurve.append(next_item)
for each, item in map(None, setInputList, outPutCurve):
    createDict={each:item}
    blendShapeInputs.update(createDict)


    
    
getCurve=blendShapeInputs.items()[0][1]
defaultCVrange=arange(0, len(ls(getCurve)[0].cv), 1)
getCVrange=defaultCVrange#input
rangeObjsWithBlends=arange(len(blendShapeInputs), 1)


BlendShapeNode=getBlendShape

'''add first value to bucket'''
collectNewNumbers.append(minWeightValue)  #store min value in bucket
'''find incremental percentile to add to bucket'''
getSeln=getCVrange[1:-1]#isolate midrange selection(as this will be what the  non end values)
RangeSel=getCVrange[:-1]#isolate all but the last (full 100%) list item
findRangeSpace=maxWeightValue-minWeightValue#find difference of range            
percentTop=findRangeSpace*100#find the 100% value that could be added to the minimum range to reach the maximum cap amount
getPercentile=percentTop/len(RangeSel)#divide the cap by the ranged list length to find  what would be the incremented value of 100% value
BucketValue=[(key+1)*getPercentile*.01 for key in range(len(getSeln))]#reference the mid list length to append the incremented value to bucket
for each in BucketValue:#Add each value to the minimum number to get true value to add to bucket if in case minimum is not 0.0
    getNum=minWeightValue+each
    collectNewNumbers.append(getNum)#add all midrange values to bucket
setAttrDict={}
for each, targetWeightValue in map(None, getCVrange, collectNewNumbers):
    for blendConnection, eachCurve in map(None, getCVrange, collectNewNumbers):
        next_item=ls(eachCurve)[0]
            findName=eachCV.name()
            builtAttribute=blendConnection+findName.split('.cv')[0]
            if eachCV.index == each:
                makeDict={builtAttribute:targetWeightValue}
                setAttrDict.update(makeDict)
for key, value in setAttrDict.index():
     cmds.setAttr(key, value)
print "blends are done"




for blendConnection, eachCurve in blendShapeInputs.items()::
  next_item=ls(value)[0]
  for eachcv, targetWeightValue in map(None, next_item.cv, collectNewNumbers):
    findName=eachcv.name()
    buildAttribute=key+findName.split('v')[2]
    cmds.setAttr(buildAttribute, targetWeightValue)







##############################################
'''add last value to bucket'''
collectNewNumbers.append(maxWeightValue)#now add the max value to bucket
for eachCurve in rangeObjsWithBlends:
    for cvNum, targetWeightValue in map(None, getCVrange, collectNewNumbers):


    
for key, value in blendShapeInputs.items():
  next_item=ls(value)[0]
  for eachcv in next_item.cv:
