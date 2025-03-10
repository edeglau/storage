from pymel.core import *
getit=ls(sl=1, fl=1)
for each in getit:
    print each.getTranslation()

selected_polygons = [p for p in mesh.polygons if p.select]
selected_edges = [e for e in mesh.vertices if e.select]
selected_vertices = [v for v in mesh.vertices if v.select]


from pymel.core import *
getit=ls(sl=1, fl=1)
if nodeType(getit[0])=="transform":
    for each in getit:
        for item in each.cv[1]:
            delete(item)
elif nodeType(getit[0])=="nurbsCurve":
    for each in getit[1]:
        delete(each)




from pymel.core import *
selection=ls(sl=1)
for each in selection:
    print each.numCVs()
    print each.length(tolerance=0.001)
    for item in each.numCVs():
        makepoint= each.getCVs(item, space='preTransform')
    print makepoint
        print each.getParamAtPoint(item, space='preTransform')

    
    for eachNumber, eachItem in enumerate(each.cv):  
        print each.getDerivativesAtParm(eachNumber, space='preTransform')
    for eachNumber, eachItem in enumerate(each.cv):
        makepoint= each.getCV(eachNumber, space='preTransform')
        print makepoint
        
        
        
        print makepoint
        print each.getParamAtPoint(makepoint, space='preTransform')
        
from pymel.core import *
getit=ls(sl=1, fl=1)
for each in getit:
    delete(each.cv[1])
    
from pymel.core import *
getit=ls(sl=1, fl=1)
for each in getit:
    for item in each.cv[::2]
        delete(item)

from pymel.core import *
getit=ls(sl=1, fl=1)
if nodeType(each)=="transform":
    for each in getit:
        for item in each.cv[::2]:
            delete(item)
elif nodeType(each)=="nurbsCurve":
    for each in getit[::2]:
        delete(each)
        
        
cmds.undoInfo(state=1)


from pymel.core import *
sys.path.append(str('//usr//people//elise-d//workspace//sandBox//rigModules//'))
import baseFunctions_maya
reload (baseFunctions_maya)
getClass=baseFunctions_maya.BaseClass()
getSel=cmds.ls(sl=1, fl=1)
parentObj=getSel[0]
for each in getSel[1:]:
    getTranslation, getRotation=getClass.locationXForm(each)
    newObj=cmds.duplicate(parentObj)
    cmds.xform(newObj, ws=1, t=getTranslation)
    cmds.xform(newObj, ws=1, ro=getRotation)


nedit ~/config/env.csh

filepath="/usr/people/elise-d/workspace/techAnimTools/python/src/utils/"
sys.path.append(str(filepath))
import deformerControl
reload (deformerControl)
getClass=deformerControl.DeformerControl()    

exec(open('/usr/people/elise-d/workspace/techAnimTools/personal/elise-d/rigModules/RigToolKit.py'))
ToolKitUI()


secondpart=cmds.ls(sl=1)
BucketValue=[]
firstMinValue=.5
firstMaxValue=5.0
percentTop=firstMaxValue*100
print percentTop
getPercentile=percentTop/len(secondpart)            
for key, value in enumerate(secondpart):
    percValue= (key+1)*getPercentile*.01
    BucketValue.append(percValue)

for each in range(len(BucketValue)):
    getNewVal=BucketValue[each]
    print getNewVal
    
#        def frange(start, stop, step):
#            i = start
#            while i < stop:
#                yield i
#                i += step
#        for i in frange(firstMinValue, firstMaxValue, step):
#            print(i)  

selall=cmds.ls(sl=1)
for each in selall:
    cmds.setAttr(each+".selfCollide", 1)

selall=cmds.ls(sl=1)
for each in selall:
    cmds.setAttr(each+".maxIterations", 10000)

selall=cmds.ls(sl=1)
for each in selall:
    cmds.setAttr(each+".maxIterations", 3)

selall=cmds.ls(sl=1)
for each in selall:
    cmds.setAttr(each+".selfCollisionFlag", 2)


selall=cmds.ls(sl=1)
for each in selall:
    cmds.setAttr(each+".pointMass", 0.2)
    
#        for key, value in enumerate(getSeln):#reference the mid list length to append the incremented value to bucket
#            percValue= (key+1)*getPercentile*.01
#            BucketValue.append(percValue)


from statistics import median
getMesh=cmds.ls(sl=1)
for each in getMesh:
    transform=cmds.xform(getMesh[0], q=True, ws=1, t=True) 
    print len(transform)
    print transform[0::3]
    print transform[1::3]
    print median(transform[2::3])  
    for each in transform:
        print each
        
        
from pymel.core import *
getSel=ls(sl=1, fl=1)
for each in getSel:
    for item in each.vtx:
        print item.getPosition()
        
        
        
from pymel.core import *
getit=ls(sl=1, fl=1)
print getit[1:]
for each in getit[:-1]:
    for item in each.cv[0]:
        mypos=item.getPosition()
print mypos[0]
xform(getit[1:], ws=1, t=mypos)  



from pymel.core import *
getit=ls(sl=1, fl=1)
for eachctrl in xrange(len(getit) - 1):
    for each in getit:
        current_item, next_item, previous_item= getit[eachctrl], getit[eachctrl + 1], getit[eachctrl - 1]
        print current_item, next_item, previous_item
        select(current_item, r=1)
        if each!=current_item:
            select(each, add=1)
        else:
            pass
        cmds.CutCurve()      
        
        
from pymel.core import *
getit=ls(sl=1, fl=1)
for eachCurve in getit:
    for each in range(len(getit)):
        if getit[each]!=eachCurve:
            select(eachCurve, r=1)
            select(getit[each], add=1)
            cmds.CutCurve()
        else:
            print getit[each]+" matches and skipped"     
            
            
            
            
create a scriptNode:

myscriptNode=cmds.scriptNode(n="selectionScript", st=2, stp="python", bs=myScriptJobEvent)


put this in the expression:

def myScriptJobEvent():
    getObj=cmds.ls(sl=1)
    if getObj:
        if "pCone1" in getObj[0]:
            cmds.select("nurbsSphere1")
        else:
            return

getThisScript=cmds.scriptJob( e=["SelectionChanged", "myScriptJobEvent()"])



def myScriptJobEvent():
    from pymel.core import *
    getObj=ls("nParticleShape1")
    getValue=getattr(getObj[0],"lifespanPP").get()
    emitCount=30
    if getValue>10:
        emitCmd=emit("exploP", o="object")
        for each in range(emitCount):
            getPos=each.getPosition
            cmds.emit( object='particle1', pos=getPos, attribute=('lifespanPP'), floatValue=.5)

getThisScript=cmds.scriptJob( e=[myScriptJobEvent()])     


nurbsToPoly(newItem[0], mnd=1  ,ch=1 ,f=1 ,pt=1 ,pc=200 ,chr=0.9 ,ft=0.01 ,mel=0.001 ,d=0.1 ,ut=1 ,un=3 ,vt=1 ,vn=3 ,uch=0 ,ucr=0 ,cht=0.2 ,es=0 ,ntr=0 ,mrt=0 ,uss=1)


from pymel.core import *
def median_find(lst):
    even = (0 if len(lst) % 2 else 1) + 1
    half = (len(lst) - 1) / 2
    mysum= sum(sorted(lst)[half:half + even]) / float(even)
    print mysum    
getit=ls(sl=1, fl=1)
TheseFaces=getit[0].faces
posBucket=[]
for each in TheseFaces[0]:
    select(TheseFaces[0], r=1)
    getItems=cmds.polyListComponentConversion( ff=1, tv=1 )
    cmds.select(getItems)
    getItems=ls(sl=1, fl=1)
for each in getItems:
    transform=each.getPosition()
    posBucket.append(median_find(transform[0::3]))
    posBucket.append(median_find(transform[1::3]))
    posBucket.append(median_find(transform[2::3]))
    
    
from pymel.core import *
def median_find(lst):
    even = (0 if len(lst) % 2 else 1) + 1
    half = (len(lst) - 1) / 2
    mysum= sum(sorted(lst)[half:half + even]) / float(even)
    return mysum
getit=ls(sl=1, fl=1)
moveTool=ls(getit[1])
intersector=ls(getit[2])
TheseFaces=getit[0].faces
posBucket=[]
getFace=TheseFaces[2]
for each in getFace:
    select(getFace, r=1)
    getItems=cmds.polyListComponentConversion( ff=1, tv=1 )
    cmds.select(getItems)
    getItems=ls(sl=1, fl=1)
findTransformX=[]
findTransformY=[]
findTransformZ=[] 
for each in getItems:
    transform=xform(each, q=1, ws=1, t=1)
    print transform
    findTransformX.append(transform[0])
    findTransformY.append(transform[1])
    findTransformZ.append(transform[2])
getX=median_find(findTransformX)
getY=median_find(findTransformY)
getZ=median_find(findTransformZ)+1
newnumbers=[getX, getY, getZ]   
print newnumbers
cmds.xform(moveTool, ws=1, t=(newnumbers[0], newnumbers[1], newnumbers[2]))
print newnumbers
printget=getit[0].intersect(newnumbers, 2, tolerance=1e-10, space='object')
print printget





import sys
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

kPluginCmdName = "mayaPythonCornellBox"

def findMeshIntersection( meshName, raySource, rayDir):
    #       Create an empty selection list. 
    selectionList = OpenMaya.MSelectionList() 
    #       Put the mesh's name on the selection list. 
    selectionList.add(meshName) 
    #       Create an empty MDagPath object. 
    meshPath = OpenMaya.MDagPath()
    #       Get the first item on the selection list (which will be our mesh) 
    #       as an MDagPath. 
    selectionList.getDagPath(0, meshPath)
    #       Create an MFnMesh functionset to operate on the node pointed to by 
    #       the dag path. 
    meshFn = OpenMaya.MFnMesh(meshPath) 
    #       Convert the 'raySource' parameter into an MFloatPoint. 
    raySource = OpenMaya.MFloatPoint(raySource[0], raySource[1], raySource[2]) 
    #       Convert the 'rayDir' parameter into an MVector.` 
    rayDirection = OpenMaya.MFloatVector(rayDir[0], rayDir[1], rayDir[2]) 
    #       Create an empty MFloatPoint to receive the hit point from the call. 
    hitPoint = OpenMaya.MFloatPoint() 
    #       Set up a variable for each remaining parameter in the 
    #       MFnMesh::closestIntersection call. We could have supplied these as 
    #       literal values in the call, but this makes the example more readable. 
    sortIds = False 
    maxDist = 10.0 
    bothDirections = False 
    noFaceIds = None 
    noTriangleIds = None 
    noAccelerator = None
    noHitParam = None 
    noHitFace = None 
    noHitTriangle = None 
    noHitBary1 = None 
    noHitBary2 = None 
    #       Get the closest intersection. 
    gotHit = meshFn.closestIntersection( 
        raySource, rayDirection, 
        noFaceIds, noTriangleIds, 
        sortIds, OpenMaya.MSpace.kWorld, maxDist, bothDirections, 
        noAccelerator, 
        hitPoint, 
        noHitParam, noHitFace, noHitTriangle, noHitBary1, noHitBary2 
    ) 
    #       Return the intersection as a Pthon list. 
    if gotHit:
        print 'O'
        sys.stderr.write( "Intersection: (%f, %f, %f)\n" % (hitPoint.x, hitPoint.y, hitPoint.z))
        return [hitPoint.x, hitPoint.y, hitPoint.z] 
    else: 
        print 'X'
        return None 
    
import maya.OpenMaya as om
    selList = om.MSelection list;

    nodeObject = om.MObject();
    selList.getDependNode(0, nodeObject)

import maya.OpenMaya as om
meshName
raySource=None
rayDir=None
def findMeshIntersection(meshName, raySource, rayDir):
        #        Create an empty selection list.
        selectionList = om.MSelectionList()

        #        Put the mesh's name on the selection list.
        selectionList.add(meshName)

        #        Create an empty MDagPath object.
        meshPath = om.MDagPath()

        #        Get the first item on the selection list (which will be our mesh)
        #        as an MDagPath.
        selectionList.getDagPath(0, meshPath)

        #        Create an MFnMesh functionset to operate on the node pointed to by
        #        the dag path.
        meshFn = om.MFnMesh(meshPath)

        #        Convert the 'raySource' parameter into an MFloatPoint.
        raySource = om.MFloatPoint(raySource[0], raySource[1], raySource[2])

        #        Convert the 'rayDir' parameter into an MVector.`
        rayDirection = om.MFloatVector(rayDir[0], rayDir[1], rayDir[2])

        #        Create an empty MFloatPoint to receive the hit point from the call.
        hitPoint = om.MFloatPoint()

        #        Set up a variable for each remaining parameter in the
        #        MFnMesh::closestIntersection call. We could have supplied these as
        #        literal values in the call, but this makes the example more readable.
        sortIds = False
        maxDist = 10.0
        bothDirections = False
        noFaceIds = None
        noTriangleIds = None
        noAccelerator = None
        noHitParam = None
        noHitFace = None
        noHitTriangle = None
        noHitBary1 = None
        noHitBary2 = None

        #        Get the closest intersection.
        gotHit = meshFn.closestIntersection(
                raySource, rayDirection,
                noFaceIds, noTriangleIds,
                sortIds, om.MSpace.kWorld, maxDist, bothDirections,
                noAccelerator,
                hitPoint,
                noHitParam, noHitFace, noHitTriangle, noHitBary1, noHitBary2
        )

        #        Return the intersection as a Pthon list.
        if gotHit:
                return [hitPoint.x, hitPoint.y, hitPoint.z]
        else:
                return None
            
            
            
import maya.OpenMaya as om

from pymel.core import *


def findMeshIntersection(meshName, raySource, rayDir):
        #        Create an empty selection list.
        selectionList = om.MSelectionList()

        #        Put the mesh's name on the selection list.
        selectionList.add(meshName)

        #        Create an empty MDagPath object.
        meshPath = om.MDagPath()

        #        Get the first item on the selection list (which will be our mesh)
        #        as an MDagPath.
        selectionList.getDagPath(0, meshPath)

        #        Create an MFnMesh functionset to operate on the node pointed to by
        #        the dag path.
        meshFn = om.MFnMesh(meshPath)

        #        Convert the 'raySource' parameter into an MFloatPoint.
        raySource = om.MFloatPoint(raySource[0], raySource[1], raySource[2])

        #        Convert the 'rayDir' parameter into an MVector.`
        rayDirection = om.MFloatVector(rayDir[0], rayDir[1], rayDir[2])

        #        Create an empty MFloatPoint to receive the hit point from the call.
        hitPoint = om.MFloatPoint()

        #        Set up a variable for each remaining parameter in the
        #        MFnMesh::closestIntersection call. We could have supplied these as
        #        literal values in the call, but this makes the example more readable.
        sortIds = False
        maxDist = 10.0
        bothDirections = False
        noFaceIds = None
        noTriangleIds = None
        noAccelerator = None
        noHitParam = None
        noHitFace = None
        noHitTriangle = None
        noHitBary1 = None
        noHitBary2 = None

        #        Get the closest intersection.
        gotHit = meshFn.closestIntersection(
                raySource, rayDirection,
                noFaceIds, noTriangleIds,
                sortIds, om.MSpace.kWorld, maxDist, bothDirections,
                noAccelerator,
                hitPoint,
                noHitParam, noHitFace, noHitTriangle, noHitBary1, noHitBary2
        )

        #        Return the intersection as a Pthon list.
        if gotHit:
                return [hitPoint.x, hitPoint.y, hitPoint.z]
        else:
                return None
                
meshName=ls(sl=1, fl=1)
meshName=meshName[0]
raySource=[1, 1, 1]
rayDir=[1, 1, 1]
getsomething=findMeshIntersection(meshName, raySource, rayDir)
print getsomething     











import maya.OpenMaya as om

from pymel.core import *


def findMeshIntersection(meshName, raySource, rayDir):
        #        Create an empty selection list.
        selectionList = om.MSelectionList()

        #        Put the mesh's name on the selection list.
        selectionList.add(meshName)

        #        Create an empty MDagPath object.
        meshPath = om.MDagPath()

        #        Get the first item on the selection list (which will be our mesh)
        #        as an MDagPath.
        selectionList.getDagPath(0, meshPath)

        #        Create an MFnMesh functionset to operate on the node pointed to by
        #        the dag path.
        meshFn = om.MFnMesh(meshPath)

        #        Convert the 'raySource' parameter into an MFloatPoint.
        raySource = om.MFloatPoint( meshName+".translateX", meshName+".translateY", meshName+".translateZ" )

        #        Convert the 'rayDir' parameter into an MVector.`
        #rayDirection = om.MFloatVector()
        rayDirection = om.MVector()
        #        Create an empty MFloatPoint to receive the hit point from the call.
        hitPoint = om.MFloatPoint()

        #        Set up a variable for each remaining parameter in the
        #        MFnMesh::closestIntersection call. We could have supplied these as
        #        literal values in the call, but this makes the example more readable.
        sortIds = False
        maxDist = 10.0
        bothDirections = False
        noFaceIds = None
        noTriangleIds = None
        noAccelerator = None
        noHitParam = None
        noHitFace = None
        noHitTriangle = None
        noHitBary1 = None
        noHitBary2 = None

        #        Get the closest intersection.
        gotHit = meshFn.closestIntersection(
                raySource, rayDirection,
                noFaceIds, noTriangleIds,
                sortIds, om.MSpace.kWorld, maxDist, bothDirections,
                noAccelerator,
                hitPoint,
                noHitParam, noHitFace, noHitTriangle, noHitBary1, noHitBary2
        )

        #        Return the intersection as a Pthon list.
        if gotHit:
                return [hitPoint.x, hitPoint.y, hitPoint.z]
        else:
                return None
                
meshName=ls(sl=1, fl=1)
meshName=meshName[0]
#raySource=[1, 1, 1]
#rayDir=[1, 1, 1]
getsomething=findMeshIntersection(meshName, raySource, rayDir)
print getsomething                












import maya.OpenMaya as om

from pymel.core import *


def findMeshIntersection(meshName, raySource, rayDir):
        #        Create an empty selection list.
        selectionList = om.MSelectionList()

        #        Put the mesh's name on the selection list.
        selectionList.add(meshName)

        #        Create an empty MDagPath object.
        meshPath = om.MDagPath()

        #        Get the first item on the selection list (which will be our mesh)
        #        as an MDagPath.
        selectionList.getDagPath(0, meshPath)

        #        Create an MFnMesh functionset to operate on the node pointed to by
        #        the dag path.
        meshFn = om.MFnMesh(meshPath)

        #        Convert the 'raySource' parameter into an MFloatPoint.
        raySource = om.MFloatPoint()

        #        Convert the 'rayDir' parameter into an MVector.`
        rayDirection = om.MFloatVector()
        #rayDirection = om.MVector()
        #        Create an empty MFloatPoint to receive the hit point from the call.
        hitPoint = om.MFloatPoint()

        #        Set up a variable for each remaining parameter in the
        #        MFnMesh::closestIntersection call. We could have supplied these as
        #        literal values in the call, but this makes the example more readable.
        sortIds = False
        maxDist = 10.0
        bothDirections = False
        noFaceIds = None
        noTriangleIds = None
        noAccelerator = None
        noHitParam = None
        noHitFace = None
        noHitTriangle = None
        noHitBary1 = None
        noHitBary2 = None

        #        Get the closest intersection.
        gotHit = meshFn.closestIntersection(
                raySource, rayDirection,
                noFaceIds, noTriangleIds,
                sortIds, om.MSpace.kWorld, maxDist, bothDirections,
                noAccelerator,
                hitPoint,
                noHitParam, noHitFace, noHitTriangle, noHitBary1, noHitBary2
        )

        #        Return the intersection as a Pthon list.
        if gotHit:
                return [hitPoint.x, hitPoint.y, hitPoint.z]
        else:
                return None
                
meshName=ls(sl=1, fl=1)
getValueX= xform(meshName[0], q=1, ws=1, t=1)
print getValueX
raySource=getValueX
#rayDir=[1, 1, 1]
getsomething=findMeshIntersection(meshName[0], raySource, rayDir)
print getsomething                           



meshName=ls(sl=1, fl=1)
for each in meshName:
    for item in each.face:
        newobject=ls(item)
        gotNormals=newobject[0].getNormal(space='preTransform')
        print gotNormals
        
        
        
import maya.OpenMaya as om

from pymel.core import *


def findMeshIntersection(meshName, raySource, rayDir):
        #        Create an empty selection list.
        selectionList = om.MSelectionList()

        #        Put the mesh's name on the selection list.
        selectionList.add(meshName)

        #        Create an empty MDagPath object.
        meshPath = om.MDagPath()

        #        Get the first item on the selection list (which will be our mesh)
        #        as an MDagPath.
        selectionList.getDagPath(0, meshPath)

        #        Create an MFnMesh functionset to operate on the node pointed to by
        #        the dag path.
        meshFn = om.MFnMesh(meshPath)

        #        Convert the 'raySource' parameter into an MFloatPoint.
        raySource = om.MFloatPoint()

        #        Convert the 'rayDir' parameter into an MVector.`
        rayDirection = om.MFloatVector()
        #rayDirection = om.MVector()
        #        Create an empty MFloatPoint to receive the hit point from the call.
        hitPoint = om.MFloatPoint()

        #        Set up a variable for each remaining parameter in the
        #        MFnMesh::closestIntersection call. We could have supplied these as
        #        literal values in the call, but this makes the example more readable.
        sortIds = False
        maxDist = 10.0
        bothDirections = False
        noFaceIds = None
        noTriangleIds = None
        noAccelerator = None
        noHitParam = None
        noHitFace = None
        noHitTriangle = None
        noHitBary1 = None
        noHitBary2 = None

        #        Get the closest intersection.
        gotHit = meshFn.closestIntersection(
                raySource, rayDirection,
                noFaceIds, noTriangleIds,
                sortIds, om.MSpace.kWorld, maxDist, bothDirections,
                noAccelerator,
                hitPoint,
                noHitParam, noHitFace, noHitTriangle, noHitBary1, noHitBary2
        )

        #        Return the intersection as a Pthon list.
        if gotHit:
                return [hitPoint.x, hitPoint.y, hitPoint.z]
        else:
                return None
                
meshName=ls(sl=1, fl=1)
for each in meshName:
    for item in each.vtx:
        gotNormals=item.getNormal(space='preTransform')
        getValueX= xform(meshName[0], q=1, ws=1, t=1)
        print gotNormals
        print getValueX
        raySource=getValueX
        rayDirection=gotNormals
        getsomething=findMeshIntersection(meshName[0], raySource, rayDirection)
        print getsomething       
        
        
        
        
        
        
        
        
        
meshName=ls(sl=1, fl=1)
moveTool=ls(getit[1])
for each in meshName:
    for eachFace in each.faces:
        select(ls(eachFace), r=1)
        getItems=cmds.polyListComponentConversion( ff=1, tv=1 )
        cmds.select(getItems)
        getItems=ls(sl=1, fl=1)
    findTransformX=[]
    findTransformY=[]
    findTransformZ=[] 
    for each in getItems:
        transform=xform(each, q=1, ws=1, t=1)
        findTransformX.append(transform[0])
        findTransformY.append(transform[1])
        findTransformZ.append(transform[2])
    getX=median_find(findTransformX)
    getY=median_find(findTransformY)
    getZ=median_find(findTransformZ)
    newnumbers=[getX, getY, getZ]   
    cmds.xform(moveTool, ws=1, t=(newnumbers[0], newnumbers[1], newnumbers[2]))



import maya.OpenMaya as om

from pymel.core import *


def findMeshIntersection(meshName, raySource, rayDir):
        #        Create an empty selection list.
        selectionList = om.MSelectionList()

        #        Put the mesh's name on the selection list.
        selectionList.add(meshName)

        #        Create an empty MDagPath object.
        meshPath = om.MDagPath()

        #        Get the first item on the selection list (which will be our mesh)
        #        as an MDagPath.
        selectionList.getDagPath(0, meshPath)

        #        Create an MFnMesh functionset to operate on the node pointed to by
        #        the dag path.
        meshFn = om.MFnMesh(meshPath)

        #        Convert the 'raySource' parameter into an MFloatPoint.
        raySource = om.MFloatPoint()

        #        Convert the 'rayDir' parameter into an MVector.`
        rayDirection = om.MFloatVector()
        #rayDirection = om.MVector()
        #        Create an empty MFloatPoint to receive the hit point from the call.
        hitPoint = om.MFloatPoint()

        #        Set up a variable for each remaining parameter in the
        #        MFnMesh::closestIntersection call. We could have supplied these as
        #        literal values in the call, but this makes the example more readable.
        sortIds = False
        maxDist = 50.0
        bothDirections = 1
        noFaceIds = None
        noTriangleIds = None
        noAccelerator = None
        noHitParam = None
        noHitFace = None
        noHitTriangle = None
        noHitBary1 = None
        noHitBary2 = None

        #        Get the closest intersection.
        gotHit = meshFn.closestIntersection(
                raySource, rayDirection,
                noFaceIds, noTriangleIds,
                sortIds, om.MSpace.kWorld, maxDist, bothDirections,
                noAccelerator,
                hitPoint,
                noHitParam, noHitFace, noHitTriangle, noHitBary1, noHitBary2
        )

        #        Return the intersection as a Pthon list.
        if gotHit:
                return [hitPoint.x, hitPoint.y, hitPoint.z]
        else:
                return None


def median_find(lst):
    even = (0 if len(lst) % 2 else 1) + 1
    half = (len(lst) - 1) / 2
    mysum= sum(sorted(lst)[half:half + even]) / float(even)
    return mysum

              
meshName=ls(sl=1, fl=1)
moveTool=ls(getit[1])
for each in meshName:
    for eachFace in each.faces:
        select(ls(eachFace), r=1)
        getItems=cmds.polyListComponentConversion( ff=1, tv=1 )
        cmds.select(getItems)
        getItems=ls(sl=1, fl=1)
    findTransformX=[]
    findTransformY=[]
    findTransformZ=[] 
    for each in getItems:
        transform=xform(each, q=1, ws=1, t=1)
        findTransformX.append(transform[0])
        findTransformY.append(transform[1])
        findTransformZ.append(transform[2])
    getX=median_find(findTransformX)
    getY=median_find(findTransformY)
    getZ=median_find(findTransformZ)
    newnumbers=[getX, getY, getZ]   
    cmds.xform(moveTool, ws=1, t=(newnumbers[0], newnumbers[1], newnumbers[2]))

          

for each in meshName:
    select(getFace, r=1)
    getItems=cmds.polyListComponentConversion( ff=1, tv=1 )
    cmds.select(getItems)
    getItems=ls(sl=1, fl=1)
findTransformX=[]
findTransformY=[]
findTransformZ=[] 
for each in getItems:
    transform=xform(each, q=1, ws=1, t=1)
    print transform
    findTransformX.append(transform[0])
    findTransformY.append(transform[1])
    findTransformZ.append(transform[2])
getX=median_find(findTransformX)
getY=median_find(findTransformY)
getZ=median_find(findTransformZ)+1
newnumbers=[getX, getY, getZ]   
print newnumbers
cmds.xform(moveTool, ws=1, t=(newnumbers[0], newnumbers[1], newnumbers[2]))
print newnumbers
printget=getit[0].intersect(newnumbers, 2, tolerance=1e-10, space='object')
print printget
        
        
    for item in each.vtx:
        gotNormals=item.getNormal(space='preTransform')
        getValueX=xform(meshName[0], q=1, ws=1, t=1)
        raySource=getValueX
        rayDirection=gotNormals
        getsomething=findMeshIntersection(meshName[0], raySource, getDirection)


meshName=ls(sl=1, fl=1)
moveTool=ls(meshName[1])
mainMesh=ls(meshName[0])
for each in mainMesh:
    for indexFace, faceItem in enumerate(each.face):
        gotNormals=each.getPolygonNormal(indexFace, space='preTransform')
        print gotNormals    
    for eachFace in each.faces:
        select(ls(eachFace), r=1)
        getItems=cmds.polyListComponentConversion( ff=1, tv=1 )
        cmds.select(getItems)
        getItems=ls(sl=1, fl=1)
    findTransformX=[]
    findTransformY=[]
    findTransformZ=[] 
    for each in getItems:
        transform=xform(each, q=1, ws=1, t=1)
        findTransformX.append(transform[0])
        findTransformY.append(transform[1])
        findTransformZ.append(transform[2])
    getX=median_find(findTransformX)
    getY=median_find(findTransformY)
    getZ=median_find(findTransformZ)
    newnumbers=[getX, getY, getZ]   
    cmds.xform(moveTool, ws=1, t=(newnumbers[0], newnumbers[1], newnumbers[2])








from pymel.core import *
import maya.OpenMaya as om


def median_find(lst):
    even = (0 if len(lst) % 2 else 1) + 1
    half = (len(lst) - 1) / 2
    mysum= sum(sorted(lst)[half:half + even]) / float(even)
    return mysum

def findMeshIntersection(meshName, raySource, rayDir):
        #        Create an empty selection list.
        selectionList = om.MSelectionList()

        #        Put the mesh's name on the selection list.
        selectionList.add(meshName)

        #        Create an empty MDagPath object.
        meshPath = om.MDagPath()

        #        Get the first item on the selection list (which will be our mesh)
        #        as an MDagPath.
        selectionList.getDagPath(0, meshPath)

        #        Create an MFnMesh functionset to operate on the node pointed to by
        #        the dag path.
        meshFn = om.MFnMesh(meshPath)

        #        Convert the 'raySource' parameter into an MFloatPoint.
        raySource = om.MFloatPoint()

        #        Convert the 'rayDir' parameter into an MVector.`
        rayDirection = om.MFloatVector()
        #rayDirection = om.MVector()
        #        Create an empty MFloatPoint to receive the hit point from the call.
        hitPoint = om.MFloatPoint()

        #        Set up a variable for each remaining parameter in the
        #        MFnMesh::closestIntersection call. We could have supplied these as
        #        literal values in the call, but this makes the example more readable.
        sortIds = False
        maxDist = 50.0
        bothDirections = 1
        noFaceIds = None
        noTriangleIds = None
        noAccelerator = None
        noHitParam = None
        noHitFace = None
        noHitTriangle = None
        noHitBary1 = None
        noHitBary2 = None

        #        Get the closest intersection.
        gotHit = meshFn.closestIntersection(
                raySource, rayDirection,
                noFaceIds, noTriangleIds,
                sortIds, om.MSpace.kWorld, maxDist, bothDirections,
                noAccelerator,
                hitPoint,
                noHitParam, noHitFace, noHitTriangle, noHitBary1, noHitBary2
        )

        #        Return the intersection as a Pthon list.
        if gotHit:
                return [hitPoint.x, hitPoint.y, hitPoint.z]
        else:
                return None


meshName=ls(sl=1, fl=1)

mainMesh=ls(meshName[0])
for each in mainMesh:
    for indexFace, faceItem in enumerate(each.face):
        gotNormals=each.getPolygonNormal(indexFace, space='preTransform')
        print gotNormals    
    for eachFace in each.faces:
        select(ls(eachFace), r=1)
        getItems=cmds.polyListComponentConversion( ff=1, tv=1 )
        cmds.select(getItems)
        getItems=ls(sl=1, fl=1)
    findTransformX=[]
    findTransformY=[]
    findTransformZ=[] 
    for each in getItems:
        transform=xform(each, q=1, ws=1, t=1)
        findTransformX.append(transform[0])
        findTransformY.append(transform[1])
        findTransformZ.append(transform[2])
    getX=median_find(findTransformX)
    getY=median_find(findTransformY)
    getZ=median_find(findTransformZ)
    newnumbers=[getX, getY, getZ] 
    
    

    raySource=newnumbers
    rayDirection=gotNormals
    getsomething=findMeshIntersection(meshName[0], raySource, rayDirection)
    print getsomething       
    
    
    
    
    
from pymel.core import *
import maya.OpenMaya as om


def median_find(lst):
    even = (0 if len(lst) % 2 else 1) + 1
    half = (len(lst) - 1) / 2
    mysum= sum(sorted(lst)[half:half + even]) / float(even)
    return mysum

def findMeshIntersection(meshName, raySource, rayDir):
        #        Create an empty selection list.
        selectionList = om.MSelectionList()

        #        Put the mesh's name on the selection list.
        selectionList.add(meshName)

        #        Create an empty MDagPath object.
        meshPath = om.MDagPath()

        #        Get the first item on the selection list (which will be our mesh)
        #        as an MDagPath.
        selectionList.getDagPath(0, meshPath)

        #        Create an MFnMesh functionset to operate on the node pointed to by
        #        the dag path.
        meshFn = om.MFnMesh(meshPath)

        #        Convert the 'raySource' parameter into an MFloatPoint.
        raySource = om.MFloatPoint()

        #        Convert the 'rayDir' parameter into an MVector.`
        rayDirection = om.MFloatVector()
        #rayDirection = om.MVector()
        #        Create an empty MFloatPoint to receive the hit point from the call.
        hitPoint = om.MFloatPoint()

        #        Set up a variable for each remaining parameter in the
        #        MFnMesh::closestIntersection call. We could have supplied these as
        #        literal values in the call, but this makes the example more readable.
        sortIds = False
        maxDist = 50.0
        bothDirections = 1
        noFaceIds = None
        noTriangleIds = None
        noAccelerator = None
        noHitParam = None
        noHitFace = None
        noHitTriangle = None
        noHitBary1 = None
        noHitBary2 = None

        #        Get the closest intersection.
        gotHit = meshFn.closestIntersection(
                raySource, rayDirection,
                noFaceIds, noTriangleIds,
                sortIds, om.MSpace.kWorld, maxDist, bothDirections,
                noAccelerator,
                hitPoint,
                noHitParam, noHitFace, noHitTriangle, noHitBary1, noHitBary2
        )

        #        Return the intersection as a Pthon list.
        if gotHit:
                return [hitPoint.x, hitPoint.y, hitPoint.z]
        else:
                return None



def getfaceNormals(indexFace, each):
    gotNormals=each.getPolygonNormal(indexFace, space='preTransform')
    return gotNormals

def getlocation(eachFace):
    select(ls(eachFace), r=1)
    getItems=cmds.polyListComponentConversion( ff=1, tv=1 )
    cmds.select(getItems)
    getItems=ls(sl=1, fl=1)
    findTransformX=[]
    findTransformY=[]
    findTransformZ=[] 
    for item in getItems:
        transform=xform(item, q=1, ws=1, t=1)
        findTransformX.append(transform[0])
        findTransformY.append(transform[1])
        findTransformZ.append(transform[2])
    getX=median_find(findTransformX)
    getY=median_find(findTransformY)
    getZ=median_find(findTransformZ)
    newnumbers=[getX, getY, getZ] 
    return newnumbers


meshName=ls(sl=1, fl=1)
mainMesh=ls(meshName[0])
for each in mainMesh: 
    for indexFace, faceItem in enumerate(each.face):
        gotNormals=each.getPolygonNormal(indexFace, space='preTransform')  
        rayDirection=gotNormals
    for eachFace in each.faces:
        getMyStartpoint=getlocation(eachFace)
        raySource=getMyStartpoint
        getsomething=findMeshIntersection(meshName[0], raySource, rayDirection)
        print getsomething       
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
from pymel.core import *
import maya.OpenMaya as om


def median_find(lst):
    even = (0 if len(lst) % 2 else 1) + 1
    half = (len(lst) - 1) / 2
    mysum= sum(sorted(lst)[half:half + even]) / float(even)
    return mysum

def findMeshIntersection(meshName, raySource, rayDir):
        #        Create an empty selection list.
        selectionList = om.MSelectionList()

        #        Put the mesh's name on the selection list.
        selectionList.add(meshName)

        #        Create an empty MDagPath object.
        meshPath = om.MDagPath()

        #        Get the first item on the selection list (which will be our mesh)
        #        as an MDagPath.
        selectionList.getDagPath(0, meshPath)

        #        Create an MFnMesh functionset to operate on the node pointed to by
        #        the dag path.
        meshFn = om.MFnMesh(meshPath)

        #        Convert the 'raySource' parameter into an MFloatPoint.
        raySource = om.MFloatPoint()

        #        Convert the 'rayDir' parameter into an MVector.`
        rayDirection = om.MFloatVector()
        #rayDirection = om.MVector()
        #        Create an empty MFloatPoint to receive the hit point from the call.
        hitPoint = om.MFloatPoint()

        #        Set up a variable for each remaining parameter in the
        #        MFnMesh::closestIntersection call. We could have supplied these as
        #        literal values in the call, but this makes the example more readable.
        sortIds = False
        maxDist = 50.0
        bothDirections = 1
        noFaceIds = None
        noTriangleIds = None
        noAccelerator = None
        hitPoint = None
        noHitParam = None
        noHitFace = None
        noHitTriangle = None
        noHitBary1 = None
        noHitBary2 = None
        atolerance = 1e-6
        ReturnStatus = False

        #        Get the closest intersection.
        gotHit = meshFn.allIntersections(
                raySource, rayDirection,
                noFaceIds, noTriangleIds,
                sortIds, om.MSpace.kWorld, maxDist, bothDirections,
                noAccelerator,
                hitPoint,
                noHitParam, noHitFace, noHitTriangle, noHitBary1, noHitBary2, atolerance, ReturnStatus
        )

        #        Return the intersection as a Pthon list.
        if gotHit:
                return [hitPoint.x, hitPoint.y, hitPoint.z]
        else:
                return None



def getfaceNormals(indexFace, each):
    gotNormals=each.getPolygonNormal(indexFace, space='preTransform')
    return gotNormals

def getlocation(eachFace):
    select(ls(eachFace), r=1)
    getItems=cmds.polyListComponentConversion( ff=1, tv=1 )
    cmds.select(getItems)
    getItems=ls(sl=1, fl=1)
    findTransformX=[]
    findTransformY=[]
    findTransformZ=[] 
    for item in getItems:
        transform=xform(item, q=1, ws=1, t=1)
        findTransformX.append(transform[0])
        findTransformY.append(transform[1])
        findTransformZ.append(transform[2])
    getX=median_find(findTransformX)
    getY=median_find(findTransformY)
    getZ=median_find(findTransformZ)
    newnumbers=[getX, getY, getZ] 
    return newnumbers


meshName=ls(sl=1, fl=1)
mainMesh=ls(meshName[0])
for each in mainMesh: 
    for indexFace, faceItem in enumerate(each.face):
        gotNormals=each.getPolygonNormal(indexFace, space='preTransform')  
        rayDirection=gotNormals
    for eachFace in each.faces:
        getMyStartpoint=getlocation(eachFace)
        raySource=getMyStartpoint
        getsomething=findMeshIntersection(meshName[0], raySource, rayDirection)
        print getsomething       
        
        
AOShader=cmds.shadingNode( "lambert", au=1, n="AO_testLambert")
AO=cmds.shadingNode( "mib_amb_occlusion", au=1, n="AO_shader")
cmds.createRenderLayer(n="AO_renderLayer", num=1, nr=1)
hookShaderOverride("defaultRenderLayer", "", "lambert3");


getParent.xValue.connect(getChild.TranslateX)










from pymel.core import *
getIKCurveCVs=cmds.ls("nameIK_crv", fl=1)
CVbucket=[]
microLeadCurve=cmds.duplicate("nameIK_crv", n="micro_lead_crv")
for eachCurve in microLeadCurve:
    getCurve=ls(eachCurve)[0]
    for eachCV in getCurve.cv:
        CVbucket.append(eachCV)
getNum=len(CVbucket)-2
#CVbucket= CVbucket[:1] + CVbucket[1+1 :]
CVbucket=CVbucket[:1]+CVbucket[2:]
#CVbucket=CVbucket[:getNum] + CVbucket[getNum+1 :]
CVbucket=CVbucket[:-2]+CVbucket[-1:]
getObjects=cmds.ls("name*_Clst_jnt_grp", fl=1)
for eachLeadCV, eachControllerObj in map(None,CVbucket, getObjects):
    print eachLeadCV+".xValue"
    print eachControllerObj+".translateX"
    connectAttr(eachLeadCV+".xValue", eachControllerObj+".translateX")
    connectAttr(eachLeadCV+".yValue", eachControllerObj+".translateY")
    connectAttr(eachLeadCV+".zValue", eachControllerObj+".translateZ")

from pymel.core import *
getObj=ls(sl=1)
getParent=getObj[0]
getChild=getObj[1]
getFirstPoint=getParent.getPosition()
getSecondPoint=getChild.getTranslation()

connectAttr(getParent+".xValue", getChild+".translateX")



from pymel.core import *
getIKCurveCVs=cmds.ls("nameIK_crv", fl=1)
CVbucket=[]
microLeadCurve=cmds.duplicate("nameIK_crv", n="micro_lead_crv")
for eachCurve in microLeadCurve:
    getCurve=ls(eachCurve)[0]
    for eachCV in getCurve.cv:
        CVbucket.append(eachCV)
getNum=len(CVbucket)-2
CVbucket= CVbucket[:1] + CVbucket[1+1 :]
CVbucket=CVbucket[:getNum] + a[getNum+1 :]
getObjects=cmds.ls("name*_Clst_jnt_grp", fl=1)
for eachLeadCV, eachControllerObj in map(None,CVbucket, getObjects):
    print eachLeadCV+".xValue"
    print eachControllerObj+".translateX"
    connectAttr(eachLeadCV+".xValue", eachControllerObj+".translateX")
    connectAttr(eachLeadCV+".yValue", eachControllerObj+".translateY")
    connectAttr(eachLeadCV+".zValue", eachControllerObj+".translateZ")




from pymel.core import *
getIKCurveCVs=cmds.ls("nameIK_crv", fl=1)
CVbucket=[]
microLeadCurve=cmds.duplicate("nameIK_crv", n="micro_lead_crv")
for eachCurve in microLeadCurve:
    getCurve=ls(eachCurve)[0]
    for eachCV in getCurve.cv:
        CVbucket.append(eachCV)
getNum=len(CVbucket)-2
CVbucket= CVbucket[:1] + CVbucket[1+1 :]
CVbucket=CVbucket[:getNum] + a[getNum+1 :]
getObjects=cmds.ls("name*_Clst_jnt_grp", fl=1)
for eachControllerObj, eachLeadCV in map(None,CVbucket, getObjects):
    print eachControllerObj, eachLeadCV 

    
    
    
    
    
from pymel.core import *
getIKCurveCVs=cmds.ls("nameIK_crv", fl=1)
CVbucket=[]
microLeadCurve=cmds.duplicate("nameIK_crv", n="micro_lead_crv")
for eachCurve in microLeadCurve:
    getCurve=ls(eachCurve)[0]
    for eachCV in getCurve.cv:
        CVbucket.append(eachCV)
getNum=len(CVbucket)-2
medLeadCurveNum=getNum/2
print medLeadCurveNum
#CVbucket= CVbucket[:1] + CVbucket[1+1 :]
CVbucket=CVbucket[:1]+CVbucket[2:]
#CVbucket=CVbucket[:getNum] + CVbucket[getNum+1 :]
CVbucket=CVbucket[:-2]+CVbucket[-1:]
getObjects=cmds.ls("name*_Clst_jnt_grp", fl=1)
for eachLeadCV, eachControllerObj in map(None,CVbucket, getObjects):

    connectAttr(eachLeadCV+".xValue", eachControllerObj+".translateX")
    connectAttr(eachLeadCV+".yValue", eachControllerObj+".translateY")
    connectAttr(eachLeadCV+".zValue", eachControllerObj+".translateZ")
medLeadCurve=cmds.duplicate("micro_lead_crv", n="med_lead_crv")
cmds.rebuildCurve(medLeadCurve, ch=1, rpo=1, rt=0, end=1, kr 0, kcp=0, kep=1, kt=0 s=medLeadCurveNum, d=3, tol=0)



















from pymel.core import *
filepath="D:\\code\\git\\myGit\\gitHub\\rigmodules\\"
sys.path.append(str(filepath))
import baseFunctions_maya
reload (baseFunctions_maya)
getClass=baseFunctions_maya.BaseClass()
getIKCurveCVs=cmds.ls("nameIK_crv", fl=1)
CVbucket=[]
microLeadCurve=cmds.duplicate("nameIK_crv", n="micro_lead_crv")
for eachCurve in microLeadCurve:
    getCurve=ls(eachCurve)[0]
    for eachCV in getCurve.cv:
        CVbucket.append(eachCV)
getNum=len(CVbucket)-2
medLeadCurveNum=getNum/3
print medLeadCurveNum
#CVbucket= CVbucket[:1] + CVbucket[1+1 :]
CVbucket=CVbucket[:1]+CVbucket[2:]
#CVbucket=CVbucket[:getNum] + CVbucket[getNum+1 :]
getObjects=cmds.ls("name*_Clst_jnt_grp", fl=1)
for eachLeadCV, eachControllerObj in map(None,CVbucket, getObjects):
    connectAttr(eachLeadCV+".xValue", eachControllerObj+".translateX")
    connectAttr(eachLeadCV+".yValue", eachControllerObj+".translateY")
    connectAttr(eachLeadCV+".zValue", eachControllerObj+".translateZ")
medLeadCurve=cmds.duplicate("micro_lead_crv", n="med_lead_crv")
cmds.rebuildCurve(medLeadCurve, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=medLeadCurveNum, d=3, tol=0)
name, grpname, size, colour, nrx, nry, nrz="name_mid_Ctrl", "name_mid_grp", 2, 25, 0, 1, 0 
for eachCurve in medLeadCurve:
    getCurve=ls(eachCurve)[0]
    for eachCV in getCurve.cv:
        transformWorldMatrix=getParent.getPosition()
        rotateWorldMatrix=[0.0, 0.0, 0.0]
        getClass.buildCtrl(eachCV, name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)






filepath="D:\\code\\git\\myGit\\gitHub\\rigmodules\\"
sys.path.append(str(filepath))
import baseFunctions_maya
reload (baseFunctions_maya)
getClass=baseFunctions_maya.BaseClass()
from pymel.core import *
getIKCurveCVs=cmds.ls("nameIK_crv", fl=1)
CVbucket=[]
microLeadCurve=cmds.duplicate("nameIK_crv", n="micro_lead_crv")
for eachCurve in microLeadCurve:
    getCurve=ls(eachCurve)[0]
    for eachCV in getCurve.cv:
        CVbucket.append(eachCV)
getNum=len(CVbucket)-2
medLeadCurveNum=getNum/3
CVbucket=CVbucket[:1]+CVbucket[2:]
CVbucket=CVbucket[:-2]+CVbucket[-1:]
getObjects=cmds.ls("name*_Clst_jnt_grp", fl=1)
for eachLeadCV, eachControllerObj in map(None,CVbucket, getObjects):
    connectAttr(eachLeadCV+".xValue", eachControllerObj+".translateX")
    connectAttr(eachLeadCV+".yValue", eachControllerObj+".translateY")
    connectAttr(eachLeadCV+".zValue", eachControllerObj+".translateZ")
medLeadCurve=cmds.duplicate("micro_lead_crv", n="med_lead_crv")
cmds.rebuildCurve(medLeadCurve, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=medLeadCurveNum, d=3, tol=0)
name, grpname, size, colour, nrx, nry, nrz="name_mid_Ctrl", "name_mid_grp", 2, 22, 0, 1, 0 
for eachCurve in medLeadCurve:
    getCurve=ls(eachCurve)[0]
    for eachCV in getCurve.cv:
        transformWorldMatrix=eachCV.getPosition()
        rotateWorldMatrix=[0.0, 0.0, 0.0]
        getClass.buildCtrl(eachCV, name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)






filepath="D:\\code\\git\\myGit\\gitHub\\rigmodules\\"
sys.path.append(str(filepath))
import baseFunctions_maya
reload (baseFunctions_maya)
getClass=baseFunctions_maya.BaseClass()
from pymel.core import *
getIKCurveCVs=cmds.ls("nameIK_crv", fl=1)
CVbucket=[]
microLeadCurve=cmds.duplicate("nameIK_crv", n="micro_lead_crv")
for eachCurve in microLeadCurve:
    getCurve=ls(eachCurve)[0]
    for eachCV in getCurve.cv:
        CVbucket.append(eachCV)
getNum=len(CVbucket)-2
medLeadCurveNum=getNum/3
CVbucket=CVbucket[:1]+CVbucket[2:]
CVbucket=CVbucket[:-2]+CVbucket[-1:]
getObjects=cmds.ls("name*_Clst_jnt_grp", fl=1)
for eachLeadCV, eachControllerObj in map(None,CVbucket, getObjects):
    connectAttr(eachLeadCV+".xValue", eachControllerObj+".translateX")
    connectAttr(eachLeadCV+".yValue", eachControllerObj+".translateY")
    connectAttr(eachLeadCV+".zValue", eachControllerObj+".translateZ")
medLeadCurve=cmds.duplicate("micro_lead_crv", n="med_lead_crv")
cmds.rebuildCurve(medLeadCurve, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=medLeadCurveNum, d=3, tol=0)
name, grpname, size, colour, nrx, nry, nrz="name_mid_Ctrl", "name_mid_grp", 2, 22, 0, 1, 0 
for eachCurve in medLeadCurve:
    getCurve=ls(eachCurve)[0]
    for eachCV in getCurve.cv:
        CVbucket.append(eachCV)
        transformWorldMatrix=eachCV.getPosition()
        rotateWorldMatrix=[0.0, 0.0, 0.0]
        getNewClust=cmds.cluster(n=)
        getClass.buildCtrl(eachCV, name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)
        cmds.parentConstraint(name, getNewClust[0], mo=1, w=1)
        
        
        
filepath="D:\\code\\git\\myGit\\gitHub\\rigmodules\\"
sys.path.append(str(filepath))
import baseFunctions_maya
import re
reload (baseFunctions_maya)
getClass=baseFunctions_maya.BaseClass()
from pymel.core import *
getIKCurveCVs=cmds.ls("nameIK_crv", fl=1)
CVbucket=[]
microLeadCurve=cmds.duplicate("nameIK_crv", n="micro_lead_crv")
for eachCurve in microLeadCurve:
    getCurve=ls(eachCurve)[0]
    for eachCV in getCurve.cv:
        CVbucket.append(eachCV)
getNum=len(CVbucket)-2
medLeadCurveNum=getNum/3
CVbucket=CVbucket[:1]+CVbucket[2:]
CVbucket=CVbucket[:-2]+CVbucket[-1:]
getObjects=cmds.ls("name*_Clst_jnt_grp", fl=1)
for eachLeadCV, eachControllerObj in map(None,CVbucket, getObjects):
    connectAttr(eachLeadCV+".xValue", eachControllerObj+".translateX")
    connectAttr(eachLeadCV+".yValue", eachControllerObj+".translateY")
    connectAttr(eachLeadCV+".zValue", eachControllerObj+".translateZ")
medLeadCurve=cmds.duplicate("micro_lead_crv", n="med_lead_crv")
cmds.rebuildCurve(medLeadCurve, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=medLeadCurveNum, d=3, tol=0)
size, colour, nrx, nry, nrz= 2, 22, 0, 1, 0 
for eachCurve in medLeadCurve:
    getCurve=ls(eachCurve)[0]
    for eachCV in getCurve.cv:
        getNum=re.sub("\D", "", str(eachCV))
        getNum=int(getNum)
        getNum="%02d" % (getNum,)
        name, grpname="name"+str(getNum)+"_med_Ctrl", "name"+str(getNum)+"_med_grp"
        CVbucket.append(eachCV)
        transformWorldMatrix=eachCV.getPosition()
        rotateWorldMatrix=[0.0, 0.0, 0.0]
        select(eachCV, r=1)
        getNewClust=cmds.cluster()
        print getNewClust[0]
        getClass.buildCtrl(eachCV, name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)
        print ls(name)
        cmds.parentConstraint(ls(name), getNewClust, mo=0, w=1)

        
        
        
        
        
        
        
filepath="D:\\code\\git\\myGit\\gitHub\\rigmodules\\"
sys.path.append(str(filepath))
import baseFunctions_maya
import re
reload (baseFunctions_maya)
getClass=baseFunctions_maya.BaseClass()
from pymel.core import *
getIKCurveCVs=cmds.ls("nameIK_crv", fl=1)
CVbucket=[]
microLeadCurve=cmds.duplicate("nameIK_crv", n="micro_lead_crv")
for eachCurve in microLeadCurve:
    getCurve=ls(eachCurve)[0]
    for eachCV in getCurve.cv:
        CVbucket.append(eachCV)
getNum=len(CVbucket)-2
medLeadCurveNum=getNum/3
CVbucket=CVbucket[:1]+CVbucket[2:]
CVbucket=CVbucket[:-2]+CVbucket[-1:]
getObjects=cmds.ls("name*_Clst_jnt_grp", fl=1)
for eachLeadCV, eachControllerObj in map(None,CVbucket, getObjects):
    connectAttr(eachLeadCV+".xValue", eachControllerObj+".translateX")
    connectAttr(eachLeadCV+".yValue", eachControllerObj+".translateY")
    connectAttr(eachLeadCV+".zValue", eachControllerObj+".translateZ")
medLeadCurve=cmds.duplicate("micro_lead_crv", n="med_lead_crv")
cmds.rebuildCurve(medLeadCurve, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=medLeadCurveNum, d=3, tol=0)
size, colour, nrx, nry, nrz= 2, 22, 0, 1, 0 
for eachCurve in medLeadCurve:
    getCurve=ls(eachCurve)[0]
    for eachCV in getCurve.cv:
        getNum=re.sub("\D", "", str(eachCV))
        getNum=int(getNum)
        getNum="%02d" % (getNum,)
        name, grpname="name"+str(getNum)+"_med_Ctrl", "name"+str(getNum)+"_med_grp"
        CVbucket.append(eachCV)
        transformWorldMatrix=eachCV.getPosition()
        rotateWorldMatrix=[0.0, 0.0, 0.0]
        select(eachCV, r=1)
        getNewClust=cmds.cluster()
        print getNewClust[0]
        getClass.buildCtrl(eachCV, name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)
        print ls(name)
        cmds.parentConstraint(ls(name), getNewClust, mo=0, w=1)
select("micro_lead_crv", r=1)
wire(w="med_lead_crv", n="wire_def", gw=0, en=1.000000, ce=0.000000, li=1.000000, dds=[(0, 500)] )









getSel=ls(sl=1)
for each in getSel:
    for item in each.cv:
        pgetCVpos=item.getPosition(space='preTransform')
        getpoint=each.closestPoint(pgetCVpos, tolerance=0.001, space='preTransform')
        getParam=each.getParamAtPoint(getpoint, space='preTransform')
        pathAnimation(fractionMode=1, follow=1, followAxis x, upAxis=y, worldUpType= "vector", worldUpVector=[0, 1, 0], inverseUp=0, inverseFront=0, bank=0)
        setAttr "motionPath1.uValue" getParam;
        disconnectAttr motionPath1_uValue.output motionPath1.uValue;

        
        
getSel=ls(sl=1)
stuff=ls("name*_Clst_jnt_grp")


for each in getSel:
    for eachCV, eachCtrlGro in map(None, each.cv, stuff):
        pgetCVpos=eachCV.getPosition(space='preTransform')
        getpoint=each.closestPoint(pgetCVpos, tolerance=0.001, space='preTransform')
        getParam=each.getParamAtPoint(getpoint, space='preTransform')
        select(eachCtrlGro, r=1)
        select(each, add=1)
        try:
	        pathAnimation(fractionMode=1, follow=1, followAxis="x", upAxis="y", worldUpType="vector", worldUpVector=[0, 1, 0], inverseUp=0, inverseFront=0, bank=0)
	        disconnectAttr("motionPath1_uValue.output", "motionPath1.uValue")
	        setAttr("motionPath1.uValue", getParam)
	    except:
	    	pass




getSel=ls(sl=1)
curvestuff=getSel[0]
stuff=ls("name*_Clst_jnt_grp")
for each in getSel:
for eachCV, eachCtrlGro in map(None, each.cv, stuff):
    pgetCVpos=eachCV.getPosition(space='preTransform')
    getpoint=each.closestPoint(pgetCVpos, tolerance=0.001, space='preTransform')
    getParam=each.getParamAtPoint(getpoint, space='preTransform')
    select(eachCtrlGro, r=1)
    select(getSel[0], add=1)
    motionPath=cmds.pathAnimation(fractionMode=1, follow=1, followAxis="x", upAxis="y", worldUpType="vector", worldUpVector=[0, 1, 0], inverseUp=0, inverseFront=0, bank=0)
    setAttr(motionPath[0]+".uValue", getParam)        
    disconnectAttr(motionPath[0]+"_uValue.output", "motionPath1.uValue")
    
    
getSel=ls(sl=1)
curvestuff=getSel[0]
stuff=ls("name*_Clst_jnt_grp")
for each in getSel:
    for eachCV, eachCtrlGro in map(None, each.cv[:-1], stuff[:-1]):
        pgetCVpos=eachCV.getPosition(space='preTransform')
        getpoint=each.closestPoint(pgetCVpos, tolerance=0.001, space='preTransform')
        getParam=each.getParamAtPoint(getpoint, space='preTransform')
        select(eachCtrlGro, r=1)
        select(getSel[0], add=1)
        try:
            motionPath=cmds.pathAnimation(fractionMode=1, follow=1, followAxis="x", upAxis="y", worldUpType="vector", worldUpVector=[0, 1, 0], inverseUp=0, inverseFront=0, bank=0)
            setAttr(motionPath+".uValue", getParam)        
            disconnectAttr(motionPath+"_uValue.output", "motionPath1.uValue")
        except:
            pass
            
            
            
            
            
            
            
getSel=ls(sl=1)
curvestuff=getSel[0]
stuff=ls("name*_Clst_jnt_grp")
CVbucket=[]
for each in getSel:
    for eachCV, eachCtrlGro in map(None, each.cv, stuff):
        CVbucket.append(eachCV)
CVbucket=CVbucket[:1]+CVbucket[2:]
CVbucket=CVbucket[:-2]+CVbucket[-1:]
for each in getSel:
    for eachCV, eachCtrlGro in map(None, CVbucket, stuff):
        print eachCV
        print eachCtrlGro
        pgetCVpos=eachCV.getPosition(space='preTransform')
        getpoint=each.closestPoint(pgetCVpos, tolerance=0.001, space='preTransform')
        getParam=each.getParamAtPoint(getpoint, space='preTransform')
        select(eachCtrlGro, r=1)
        select(getSel[0], add=1)
        motionPath=cmds.pathAnimation(fractionMode=1, follow=1, followAxis="x", upAxis="y", worldUpType="vector", worldUpVector=[0, 1, 0], inverseUp=0, inverseFront=0, bank=0)        
        disconnectAttr(motionPath+"_uValue.output", motionPath+".uValue")
        getpth=str(motionPath)
        setAttr(motionPath+".fractionMode", False)
        setAttr(motionPath+".uValue", getParam)            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
filepath="D:\\code\\git\\myGit\\gitHub\\rigmodules\\"
sys.path.append(str(filepath))
import baseFunctions_maya
import re
reload (baseFunctions_maya)
getClass=baseFunctions_maya.BaseClass()
from pymel.core import *
getIKCurveCVs=cmds.ls("nameIK_crv", fl=1)
CVbucket=[]
microLeadCurve=cmds.duplicate("nameIK_crv", n="micro_lead_crv")
for eachCurve in microLeadCurve:
    getCurve=ls(eachCurve)[0]
    for eachCV in getCurve.cv:
        CVbucket.append(eachCV)
getNum=len(CVbucket)-2
medLeadCurveNum=getNum/3
CVbucket=CVbucket[:1]+CVbucket[2:]
CVbucket=CVbucket[:-2]+CVbucket[-1:]
getObjects=cmds.ls("name*_Clst_jnt_grp", fl=1)
medLeadCurve=cmds.duplicate("micro_lead_crv", n="med_lead_crv")
cmds.rebuildCurve(medLeadCurve, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=medLeadCurveNum, d=3, tol=0)
size, colour, nrx, nry, nrz= 2, 22, 0, 1, 0 
for eachCurve in medLeadCurve:
    getCurve=ls(eachCurve)[0]
    for eachCV in getCurve.cv:
        getNum=re.sub("\D", "", str(eachCV))
        getNum=int(getNum)
        getNum="%02d" % (getNum,)
        name, grpname="name"+str(getNum)+"_med_Ctrl", "name"+str(getNum)+"_med_grp"
        CVbucket.append(eachCV)
        transformWorldMatrix=eachCV.getPosition()
        rotateWorldMatrix=[0.0, 0.0, 0.0]
        select(eachCV, r=1)
        getNewClust=cmds.cluster()
        getClass.buildCtrl(eachCV, name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)
        cmds.parentConstraint(ls(name), getNewClust, mo=0, w=1)
select("micro_lead_crv", r=1)
wire(w="med_lead_crv", n="wire_def", gw=0, en=1.000000, ce=0.000000, li=1.000000, dds=[(0, 500)] )


getSel=ls(sl=1)
curvestuff=getSel[0]
stuff=ls("name*_Clst_jnt_grp")
CVbucket=[]
for each in getSel:
    for eachCV, eachCtrlGro in map(None, each.cv, stuff):
        CVbucket.append(eachCV)
CVbucket=CVbucket[:1]+CVbucket[2:]
CVbucket=CVbucket[:-2]+CVbucket[-1:]
for each in getSel:
    for eachCV, eachCtrlGro in map(None, CVbucket, stuff):
        print eachCV
        print eachCtrlGro
        pgetCVpos=eachCV.getPosition(space='preTransform')
        getpoint=each.closestPoint(pgetCVpos, tolerance=0.001, space='preTransform')
        getParam=each.getParamAtPoint(getpoint, space='preTransform')
        select(eachCtrlGro, r=1)
        select(getSel[0], add=1)
        motionPath=cmds.pathAnimation(fractionMode=1, follow=1, followAxis="x", upAxis="y", worldUpType="vector", worldUpVector=[0, 1, 0], inverseUp=0, inverseFront=0, bank=0)        
        disconnectAttr(motionPath+"_uValue.output", motionPath+".uValue")
        getpth=str(motionPath)
        setAttr(motionPath+".fractionMode", False)
        setAttr(motionPath+".uValue", getParam) 
        
        
        
        
        
        
medLeadCurve=cmds.duplicate("nameIK_crv", n="med_lead_crv")
cmds.rebuildCurve(medLeadCurve, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=medLeadCurveNum, d=3, tol=0)
curvestuff=getSel[0]
stuff=ls("name*_Clst_jnt_grp")
CVbucket=[]
for each in getSel:
    for eachCV, eachCtrlGro in map(None, each.cv, stuff):
        CVbucket.append(eachCV)
CVbucket=CVbucket[:1]+CVbucket[2:]
CVbucket=CVbucket[:-2]+CVbucket[-1:]
for each in getSel:
    for eachCV, eachCtrlGro in map(None, CVbucket, stuff):
        print eachCV
        print eachCtrlGro
        pgetCVpos=eachCtrlGro.getTranslation()
        getpoint=each.closestPoint(pgetCVpos, tolerance=0.001, space='preTransform')
        getParam=each.getParamAtPoint(getpoint, space='preTransform')
        select(eachCtrlGro, r=1)
        select(getSel[0], add=1)
        motionPath=cmds.pathAnimation(fractionMode=1, follow=1, followAxis="x", upAxis="y", worldUpType="vector", worldUpVector=[0, 1, 0], inverseUp=0, inverseFront=0, bank=0)        
        disconnectAttr(motionPath+"_uValue.output", motionPath+".uValue")
        getpth=str(motionPath)
        setAttr(motionPath+".fractionMode", False)
        setAttr(motionPath+".uValue", getParam) 





filepath="D:\\code\\git\\myGit\\gitHub\\rigmodules\\"
sys.path.append(str(filepath))
import baseFunctions_maya
import re
reload (baseFunctions_maya)
getClass=baseFunctions_maya.BaseClass()
from pymel.core import *


CVbucket=[]
microLeadCurve=ls("nameIK_crv")
medLeadCurve=cmds.duplicate("nameIK_crv", n="med_lead_crv")
stuff=ls("name*_Clst_jnt_grp")
CVbucket=[]
for eachCurve in microLeadCurve:
    getCurve=ls(eachCurve)[0]
    for eachCV in getCurve.cv:
        CVbucket.append(eachCV)
getNum=len(CVbucket)-2
medLeadCurveNum=getNum/6
cmds.rebuildCurve(medLeadCurve, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=medLeadCurveNum, d=3, tol=0)
size, colour, nrx, nry, nrz= 2, 22, 0, 1, 0 
CVbucket=[]
for eachCurve in medLeadCurve:
    getCurve=ls(eachCurve)[0]
    for eachCV in getCurve.cv:
        getNum=re.sub("\D", "", str(eachCV))
        getNum=int(getNum)
        getNum="%02d" % (getNum,)
        name, grpname="name"+str(getNum)+"_med_Ctrl", "name"+str(getNum)+"_med_grp"
        CVbucket.append(eachCV)
        transformWorldMatrix=eachCV.getPosition()
        rotateWorldMatrix=[0.0, 0.0, 0.0]
        select(eachCV, r=1)
        getNewClust=cmds.cluster()
        getClass.buildCtrl(eachCV, name, grpname,transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)
        cmds.parentConstraint(ls(name), getNewClust, mo=0, w=1)
for each in microLeadCurve:
    for eachCV, eachCtrlGro in map(None, each.cv, stuff):
        CVbucket.append(eachCV)
CVbucket=CVbucket[:1]+CVbucket[2:]
CVbucket=CVbucket[:-2]+CVbucket[-1:]
getSel=ls(medLeadCurve)
for each in getSel:
    for eachCV, eachCtrlGro in map(None, CVbucket, stuff):
        print eachCV
        print eachCtrlGro
        pgetCVpos=eachCtrlGro.getTranslation()
        getpoint=each.closestPoint(pgetCVpos, tolerance=0.001, space='preTransform')
        getParam=each.getParamAtPoint(getpoint, space='preTransform')
        select(eachCtrlGro, r=1)
        select(getSel[0], add=1)
        motionPath=cmds.pathAnimation(fractionMode=1, follow=1, followAxis="x", upAxis="y", worldUpType="vector", worldUpVector=[0, 1, 0], inverseUp=0, inverseFront=0, bank=0)        
        disconnectAttr(motionPath+"_uValue.output", motionPath+".uValue")
        getpth=str(motionPath)
        setAttr(motionPath+".fractionMode", False)
        setAttr(motionPath+".uValue", getParam) 





pObj=list()
crap=list()
import re
pObjd = cmds.ls (sl=True)
cmds.selectMode(object=True)
jim=cmds.ls (sl=True)
cmds.select(cl=True)
if cmds.objExists("Npoles")==True:
        cmds.delete("Npoles")
cmds.sets(n="Npoles", co=2)

if cmds.objExists("Epoles")==True:
        cmds.delete("Epoles")
cmds.sets(n="Epoles", co=2)

if cmds.objExists("starpoles")==True:
        cmds.delete("starpoles")
cmds.sets(n="starpoles", co=2)


for h in range (len(pObjd)):
    if ':' not in (pObjd[h]):
        pObj.append(pObjd[h])
for r in range (len(pObjd)):
        if ':' in (pObjd[r]):
                crap.append(pObjd[r])
                for p in range (len(crap)):
                        f=crap[p].split('.')
                        t=re.sub(r'\A[a-zA-Z]*','',f[1])
                        edd= t[1:]
                        str= edd[:-1]
                        g=str.split(':')
                        t=int(g[0])
                        v=int(g[1])
                        nmbr=range (t, v)
                        for k in range(len(nmbr)):
                            jw=('%d' %nmbr[k])
                            kol=jim[0]+'.vtx['+jw+']'
                            pObj.append(kol)
cmds.select(crap)
for y in range (len(pObj)):
        gross = cmds.polyInfo(pObj[y], ve=True)
        g=gross[0].split(':')
        edgeCount=g[1].split("   ")
        edges=edgeCount[1:]
        if (len(edges))==3:
                cmds.sets(pObj[y], fe='Npoles')
        elif (len(edges))==5:
                cmds.sets(pObj[y], fe='Epoles')
        elif (len(edges))>5:
                cmds.sets(pObj[y], fe='starpoles')


cmds.select('starpoles', r=True, ne=True)
cmds.pickWalk(d='Up')
acksel=cmds.ls(sl=True)
if (len(acksel))==0:
        cmds.delete("starpoles")


cmds.select('Npoles', r=True, ne=True)
cmds.pickWalk(d='Up')
acksel=cmds.ls(sl=True)
if (len(acksel))==0:
        cmds.delete("Npoles")

cmds.select('Epoles', r=True, ne=True)
cmds.pickWalk(d='Up')
acksel=cmds.ls(sl=True)
if (len(acksel))==0:
        cmds.delete("Epoles")
        










    def DropOffControls(self, 
                        span, 
                        colour, 
                        size,  
                        ControllerSize, 
                        nrx, nry, nrz, 
                        influencedCtrl, 
                        controlSuff, 
                        buildNameFrom):
        print influencedCtrl
        if len(influencedCtrl)>span:
            parentControllers=[]
            pairedParentControllers=[] 
            lastInf=influencedCtrl[-1:] 
            firstInf=influencedCtrl[:1]
            #create clusters for IK chain
            for each in influencedCtrl[1::2]:
                name=each.split(buildNameFrom)[0]+controlSuff
                grpname=name+"_grp"    
                fivesize=ControllerSize/size
                colour=colour
                transformWorldMatrix = cmds.xform(each, q=True, wd=1, t=True)  
                rotateWorldMatrix = cmds.xform(each, q=True, wd=1, ro=True) 
                getClass.buildCtrl(each, name, grpname,transformWorldMatrix, rotateWorldMatrix, fivesize, colour, nrx, nry, nrz)
                parentControllers.append(name)
                cmds.setAttr(name+".sx" , keyable=0, lock=1)
                cmds.setAttr(name+".sy" , keyable=0, lock=1)
                cmds.setAttr(name+".sz", keyable=0, lock=1)
            controllerInfDropOffBucket=[]
            for each in xrange(len(influencedCtrl) - 1):
                try:
                    current_ctrl_item=influencedCtrl[1:][::2][each]
                    prev_item=influencedCtrl[::2][each]
                    next_ctrl_item=influencedCtrl[::2][each+1]                 
                except:
                    pass
                if prev_item!=influencedCtrl[-1:][0]:
                    controllerInfDropOffBucket.append([prev_item, current_ctrl_item, next_ctrl_item])                   
            for eachPContrl, item in map(None, parentControllers, controllerInfDropOffBucket):
                try:
                    FIRST=item[:1][0]
                    SECOND=item[1:2][0]
                    THIRD=item[-1:][0]
                    if str(FIRST) != firstInf[0]:
                        cmds.parentConstraint(eachPContrl, FIRST, mo=1, w=.5)
                    cmds.parentConstraint(eachPContrl, SECOND, mo=1, w=1.0)
                    if str(THIRD) != lastInf[0]:
                        cmds.parentConstraint(eachPContrl, THIRD, mo=1, w=.5)
                except:
                    pass            


    def leading_curve(self):
        getIKCurveCVs=cmds.ls("nameIK_crv", fl=1)
        CVbucket=[]
        microLeadCurve=cmds.duplicate("nameIK_crv", n="micro_lead_crv")
        for eachCurve in microLeadCurve:
            getCurve=ls(eachCurve)[0]
            for eachCV in getCurve.cv:
                CVbucket.append(eachCV)
        getNum=len(CVbucket)-2
        #CVbucket= CVbucket[:1] + CVbucket[1+1 :]
        CVbucket=CVbucket[:1]+CVbucket[2:]
        #CVbucket=CVbucket[:getNum] + CVbucket[getNum+1 :]
        CVbucket=CVbucket[:-2]+CVbucket[-1:]
        getObjects=cmds.ls("name*_Clst_jnt_grp", fl=1)
        for eachLeadCV, eachControllerObj in map(None,CVbucket, getObjects):
            connectAttr(eachLeadCV+".xValue", eachControllerObj+".translateX")
            connectAttr(eachLeadCV+".yValue", eachControllerObj+".translateY")
            connectAttr(eachLeadCV+".zValue", eachControllerObj+".translateZ")



        if cmds.ls(mainName+"*_max_Ctrl"):
           maxinfluencedCtrl=cmds.ls(mainName+"*_max_Ctrl")
        if cmds.ls(mainName+"*_maj_Ctrl"):
           majinfluencedCtrl=cmds.ls(mainName+"*_maj_Ctrl")
        if cmds.ls(mainName+"*_mid_Ctrl"):
           medinfluencedCtrl=cmds.ls(mainName+"*_mid_Ctrl")
        if cmds.ls(mainName+"*_sml_Ctrl"):
           smlinfluencedCtrl=cmds.ls(mainName+"*_sml_Ctrl")

        if maxinfluencedCtrl:
            print "THERE ARE MAX CONTROLLERS PRESENT"
            getControllerBucket=maxinfluencedCtrl                      
#            cmds.parentConstraint("Secondary"+mainName+"_Ctrl", mo=1, w=.5)
        elif majinfluencedCtrl:
            print "THERE ARE MAJOR CONTROLLERS PRESENT"
            getControllerBucket=majinfluencedCtrl
        elif medinfluencedCtrl:
            print "THERE ARE MEDIUM CONTROLLERS PRESENT"  
            getControllerBucket=medinfluencedCtrl
        elif smlinfluencedCtrl:
            print "THERE ARE SMALL CONTROLLERS PRESENT"    
            getControllerBucket=smlinfluencedCtrl              
 
        print getControllerBucket
    
    
    
    
    
import sys
sys.path.append("C:/Users/edegl/git/storage/gitHub/rigmodules/")

import RigToolKit
go=RigToolKit.ToolKitUI()
go.create()
