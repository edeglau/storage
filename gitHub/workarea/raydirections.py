import pymel.core as pm
import maya.cmds as cmds

meshName=cmds.ls(sl=1, fl=1)

for each in meshName: 
    getNode = pm.PyNode(each).node()
    print getNode
    getSpan = cmds.polyEvaluate(each, f=1)
    for number in range(getSpan):
        getfc= getNode+".f["+str(number)+"]"
        getNodeFace=cmds.ls(getfc)[0]
        getMyStartpoint=getlocation(getNodeFace)
        print getMyStartpoint
    for indexFace, faceItem in enumerate(pm.PyNode(each).face):
        rayDirection=pm.PyNode(each).getPolygonNormal(indexFace, space='preTransform')
        print rayDirection
