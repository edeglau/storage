from numpy import arange
from pymel.core import *


getBlendShape=cmds.ls(sl=1, fl=1)
getSource=cmds.listConnections(getBlendShape[0], s=1)
blendShapeInputs={}
for each in xrange(len(getSource)-1):
  current_item, next_item=getSource[each], getSource[each+1]
  if "inputTarget" in current_item:
    print current_item, next_item
    findAttribute=current_item.split("inputTargetItem")[0]+"targetWeights"
    createDict={findAttributeName:next_item}
    blendShapeInputs.update(createDict)
for key, value in blendShapeInputs.items():
  next_item=ls(value)[0]
  for eachcv in next_item.cv:
    findName=eachcv.name()
    buildAttribute=key+findName.split('v')[2]
    
        
    
  
  
BlendShapeNode="blendShape12"
rangeObjsWithBlends=arange(0, 168, 1)
getCVrange=arange(0, 25, 1)
collectNewNumbers=[]
minWeightValue=0.0
maxWeightValue=1.0
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
'''add last value to bucket'''
collectNewNumbers.append(maxWeightValue)#now add the max value to bucket
for eachCurve in rangeObjsWithBlends:
    for cvNum, targetWeightValue in map(None, getCVrange, collectNewNumbers):
        cmds.setAttr(BlendShapeNode+".inputTarget["+str(eachCurve)+"].inputTargetGroup[0].targetWeights]""+str(cvNum)+]", targetWeightValue)
