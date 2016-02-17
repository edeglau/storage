
  from numpy import arange
  BlendShapeNode="blendShape12"
  rangeObjsWithBlends=arange(0, 168, 1)
  getCVrange=arange(0, 25, 1))
  collectNewNumber=[]
  minWeightValue=0.0
  maxWeightValue=1.0
  '''add first value to bucket'''
  collectNewNumbers.append(minWeightValue)  
  '''find incremental percentile to add to bucket'''
  getSeln=getCVrange[1:-1]#isolate midrange selection
  RangeSel=getCVrange[:-1]#isolate all but the last (full 100%) list item
  findRangeSpace=maxWeightValue-minWeightValue#find difference of range            
  percentTop=findRangeSpace*100#find the 100% value that could be added to the minimum range to reach the maximum cap amount
  getPercentile=percentTop/len(RangeSel)#divide the cap by the ranged list length to find the incremented value
  BucketValue=[(key+1)*getPercentile*.01 for key in range(len(getSeln))]#reference the mid list length to append the incremented value to bucket
  for each in BucketValue:#Add each value to the minimum number to get true value to add to bucket
      getNum=minWeightValue+each
      collectNewNumbers.append(getNum)
  '''add last value to bucket'''
  collectNewNumbers.append(maxWeightValue)
  for eachCurve in rangeObjsWithBlends:
    for cvNum, targetWeightValue in map(None, getCVrange, collectNewNumbers):
      cmds.setAttr(BlendShapeNode+".inputTarget["+str(eachCurve)+"].inputTargetGroup[0].targetWeights]""+str(cvNum)+]", targetWeightValue)
