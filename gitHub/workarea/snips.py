
####expressions


nucleus1_wind_CTRL.windSpeed = abs( noise( frame * .05) * 8)
turbulenceField1.magnitude=abs( noise( frame * .05) * 8)
vortexField1.magnitude=turbulenceField1.magnitude
locator1_WIND.localWind = (abs(noise(time * 1) * 12) -.5)
.O[0] = (abs(noise(time))/5) + .1


#sin wave
f(x) = A+sin(B+x*C)*D

#noise sin

$sine = sin(frame);

$formula = rand($sine);

$sine = sin(frame * .001);
locator1_WIND.localWind =  abs( noise($sine) *4);
locator1_WIND.localWind =  abs( noise(sin(frame* .001) *4);
locator1_WIND.localWind =  abs( noise(sin(frame* .001)*8)*2)


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




filepath="/usr/people/elise-d/workspace/techAnimTools/python/src/utils/"
sys.path.append(str(filepath))
import deformerControl
reload (deformerControl)
getClass=deformerControl.DeformerControl()    

exec(open('/usr/people/elise-d/workspace/techAnimTools/personal/elise-d/rigModules/RigToolKit.py'))
ToolKitUI()
exec(open('//usr//people//elise-d//workspace//sandBox//rigModules//RigToolKit.py'))
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








from pymel.core import *


getNames=ls(sl=1, fl=1)
getFirstGrp = getNames[0].split(".")[0]
getSecondGrp = getNames[-1:][0].split(".")[0]


firstList=[(each) for each in getNames if each.split(".")[0]==getFirstGrp]
secondList=[(each) for each in getNames if each.split(".")[0]==getSecondGrp]

cmds.select(firstList)
cmds.CreateCurveFromPoly()
getFirstCurve=cmds.ls(sl=1, fl=1)
getFirstCurveInfo=ls(sl=1, fl=1)
numberCV=getFirstCurveInfo[0].numCVs()
print numberCV

cmds.delete(getFirstCurve[0], ch=1)

cmds.select(secondList)
cmds.CreateCurveFromPoly()
getSecondCurve=cmds.ls(sl=1, fl=1)
getSecondCurveInfo=ls(sl=1, fl=1)
print getSecondCurveInfo[0].numCVs()
cmds.rebuildCurve(getSecondCurve[0], getFirstCurve[0], rt=2 )
getSecondCurve=cmds.ls(sl=1, fl=1)
getSecondCurveInfo=ls(sl=1, fl=1)
cmds.delete(getSecondCurve[0], ch=1)
#cmds.rebuildCurve(getSecondCurve[0], ch=0, rpo=1, rt=0, end=0, kr=2, kcp=0, kep=1, kt=1, s=numberCV, d=3, tol=1e-06)
print getSecondCurveInfo[0].numCVs()

#cmds.select(cmds.ls(getFirstGrp)[0], r=1)
cmds.select(getFirstCurve[0], r=1)
cmds.wire(cmds.ls(getFirstGrp)[0])
#cmds.CreateWrap()

#cmds.select(cmds.ls(getSecondGrp)[0], r=1)
cmds.select(getSecondCurve[0], r=1)
cmds.wire(cmds.ls(getSecondGrp)[0])
#cmds.CreateWrap()

cmds.blendShape(getSecondCurve[0], getFirstCurve[0],w=(0, 1.0)) 









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


medLeadCurve=cmds.duplicate("nameIK_crv", n="med_lead_crv")
getSel=ls("med_lead_crv")
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



        extractEdge=[int(s) for s in each.split() if s.isdigit()]   


selObj=cmds.ls(sl=1, fl=1)

for each in selObj:
    print str(each)
    getTrans=cmds.xform(each, q=1, ws=1, t=1)
    print getTrans
    getnum=re.sub(r"\D", "", each)
    print getnum
    getThing=cmds.annotate(each, tx=str(getnum), p=getTrans)
    cmds.setAttr(getThing+".overrideEnabled", 1)
    opbname=cmds.listRelatives(getThing, ad=1, typ="shape")
    



from pymel.core import *
getObj=cmds.ls(sl=1)
childControllers= getObj[:-1]
microLeadCurve=getObj[-1:]
CVbucketbuckList=[]
for each in microLeadCurve:
    each=ls(each)
    for eachCV, eachCtrlGro in map(None, each[0].cv, childControllers):
        CVbucketbuckList.append(eachCV)
for each in microLeadCurve:
    for eachItemCV, eachCtrlGro in map(None, CVbucketbuckList, childControllers):
        eachCtrlGro=ls(eachCtrlGro)
        pgetCVpos=eachCtrlGro[0].getTranslation()
        each=ls(each)
        getpoint=each[0].closestPoint(pgetCVpos, tolerance=0.001, space='preTransform')
        getParam=each[0].getParamAtPoint(getpoint, space='preTransform')
        select(eachCtrlGro, r=1)
        select(microLeadCurve[0], add=1)
        motionPath=cmds.pathAnimation(fractionMode=1, follow=1, followAxis="x", upAxis="y", worldUpType="vector", worldUpVector=[0, 1, 0], inverseUp=0, inverseFront=0, bank=0)        
        disconnectAttr(motionPath+"_uValue.output", motionPath+".uValue")
        getpth=str(motionPath)
        setAttr(motionPath+".fractionMode", False)
        setAttr(motionPath+".uValue", getParam) 



selObj=cmds.ls(sl=1, fl=1)

cmds.select(cl=1)

for each in selObj[::2]:
    print each
    cmds.select(each, add=1)



selObj=cmds.ls(sl=1, fl=1)
posBucketx=[]
posBuckety=[]
posBucketz=[]
transform=cmds.xform(selObj, q=1, t=1)
posBucket=[]
posBucketx.append(median_find(transform[0::3]))
posBuckety.append(median_find(transform[1::3]))
posBucketz.append(median_find(transform[2::3]))
print posBucketx, posBuckety, posBucketz

        
def median_find(lst):
    even = (0 if len(lst) % 2 else 1) + 1
    half = (len(lst) - 1) / 2
    mysum= sum(sorted(lst)[half:half + even]) / float(even)
    return mysum  


selObj=cmds.ls(sl=1, fl=1)
transform=cmds.xform(selObj, q=1, t=1)
even = (0 if len(transform[0::3]) % 2 else 1) + 1
half = (len(transform[0::3]) - 1) / 2
mysumx= sum(sorted(transform[0::3])[half:half + even]) / float(even)
print mysumx

even = (0 if len(transform[1::3]) % 2 else 1) + 1
half = (len(transform[1::3]) - 1) / 2
mysumy= sum(sorted(transform[1::3])[half:half + even]) / float(even)
print mysumy

even = (0 if len(transform[2::3]) % 2 else 1) + 1
half = (len(transform[2::3]) - 1) / 2
mysumz= sum(sorted(transform[2::3])[half:half + even]) / float(even)
print mysumz




def median_find(lst):
    even = (0 if len(lst) % 2 else 1) + 1
    half = (len(lst) - 1) / 2
    mysum= sum(sorted(lst)[half:half + even]) / float(even)
    return mysum
selObj=cmds.ls(sl=1, fl=1)
transform=cmds.xform(selObj, q=1, ws=1, t=1)
posBucketx=median_find(transform[0::3])
posBuckety=median_find(transform[1::3])
posBucketz=median_find(transform[2::3])
print posBucketx, posBuckety, posBucketz

getLoc=cmds.spaceLocator()
cmds.xform(getLoc[0], t=(posBucketx, posBuckety, posBucketz))



getSel=cmds.ls(sl=1, fl=1)

getBlendee=getSel[0]
getBlender=getSel[1]


getBlendeeChildren=[(each)for each in cmds.listRelatives(getBlendee, ad=1, typ="transform")]
getBlendeeParent=[(each)for each in cmds.listRelatives(getBlender, ad=1, typ="transform")]
for eachChild in getBlendeeChildren:
    for eachParent in getBlendeeParent:
        if str(eachChild) == str(eachParent):
            cmds.ls(eachChild)
            print eachChild, eachParent


getSel=cmds.ls(sl=1, fl=1)

getBlendee=getSel[0]
getBlender=getSel[1]


getBlendeeChildren=[(each)for each in cmds.listRelatives(getBlendee, ad=1, typ="transform")]
getBlendeeParent=[(each)for each in cmds.listRelatives(getBlender, ad=1, typ="transform")]
for eachChild in getBlendeeChildren:
    for eachParent in getBlendeeParent:
        if eachChild==eachParent:
            #print eachChild, eachChild 
            getParent=cmds.ls(eachParent)
            getChild=cmds.ls(eachChild)
            cmds.select(getParent[0], r=1)
            cmds.select(getChild[0], add=1)
            getNewBLend=cmds.blendShape(n="reflectBlend", w=(1, 1.0), en=1.0, foc=1)



int $currentTime=`currentTime -q`;
int $offset=10;
$offsetTime=$currentTime-$offset;
$getPos=`getAttr -t $offsetTime pSphere1.rotateY`;
pSphere4.rotateY=$getPos;

int $currentTime=`currentTime -q`;
int $offset=10;
$offsetTime=$currentTime-$offset;
$getPos=`getAttr -t $offsetTime l_lesserRow001UnderWingCoverts007_stickyDeformer_1_CTRL.rotateZ`;
defaultADeformSD_CTRL_Ctrl.rotateZ=$getPos;



defaultADeformSD_CTRL_Ctrl


l_lesserRow001UnderWingCoverts007_stickyDeformer_1_CTRL





getObj=cmds.ls(sl=1)
getParent=getObj[0]
print getParent
# cmds.nurbsToPolygonsPref(un=selfU, uv=selfV)
for each in getObj[1:]:
    print each
    cmds.connectAttr(getParent+".RotateRightRow01", each+".rotateY") 



int $currentTime=`currentTime -q`;
int $offset=-1;
$offsetTime=$currentTime-$offset;
$getPos=`getAttr -t $offsetTime defaultADeformSD_CTRL_Ctrl.rotateX`;
l_lesserRow001UnderWingCoverts007_stickyDeformer_1_CTRL.rotateZ=$getPos;
int $offset=1;
$offsetTime=$currentTime-$offset;
$getPos=`getAttr -t $offsetTime defaultADeformSD_CTRL_Ctrl.rotateX`;
l_lesserRow001UnderWingCoverts011_stickyDeformer_1_CTRL.rotateZ=$getPos;



from pymel.core import *

selObj=cmds.ls(sl=1, fl=1, sn=1)
for each in selObj:
    getChild=listRelatives(each, ad=1, f=1, typ="clusterHandle")
    cmds.select(getChild)


getObj=cmds.ls(sl=1)
getParent=getObj[0]
print getParent
# cmds.nurbsToPolygonsPref(un=selfU, uv=selfV)
for each in getObj[1:]:
    print each
    cmds.connectAttr(getParent+".rotate", each+".rotate") 




int $currentTime=`currentTime -q`;
int $offset=5;
$offsetTime=$currentTime-$offset;
$getPos=`getAttr -t $offsetTime L_ROW01_CTRL.rotateY`;
L_ROW02_CTRL.rotateY=$getPos;
int $offset=7;
$offsetTime=$currentTime-$offset;
$getPos=`getAttr -t $offsetTime L_ROW01_CTRL.rotateY`;
L_ROW03_CTRL.rotateY=$getPos;
int $offset=10;
$offsetTime=$currentTime-$offset;
$getPos=`getAttr -t $offsetTime L_ROW01_CTRL.rotateY`;
L_ROW04_CTRL.rotateY=$getPos/8;
int $offset=12;
$offsetTime=$currentTime-$offset;
$getPos=`getAttr -t $offsetTime L_ROW01_CTRL.rotateY`;
L_ROW05_CTRL.rotateY=$getPos/6;
int $offset=15;
$offsetTime=$currentTime-$offset;
$getPos=`getAttr -t $offsetTime R_ROW01_CTRL.rotateY`;
L_G_ROW01_CTRL.rotateY=$getPos/4;
int $offset=17;
$offsetTime=$currentTime-$offset;
$getPos=`getAttr -t $offsetTime R_ROW01_CTRL.rotateY`;
L_G_ROW02_CTRL.rotateY=$getPos/4;



int $currentTime=`currentTime -q`;
int $offset=5;
$offsetTime=$currentTime-$offset;
$getPos=`getAttr -t $offsetTime R_ROW01_CTRL.rotateY`;
R_ROW02_CTRL.rotateY=$getPos;
int $offset=7;
$offsetTime=$currentTime-$offset;
$getPos=`getAttr -t $offsetTime R_ROW01_CTRL.rotateY`;
R_ROW03_CTRL.rotateY=$getPos;
int $offset=10;
$offsetTime=$currentTime-$offset;
$getPos=`getAttr -t $offsetTime R_ROW01_CTRL.rotateY`;
R_ROW04_CTRL.rotateY=$getPos/8;
int $offset=12;
$offsetTime=$currentTime-$offset;
$getPos=`getAttr -t $offsetTime R_ROW01_CTRL.rotateY`;
R_ROW05_CTRL.rotateY=$getPos/6;
int $offset=15;
$offsetTime=$currentTime-$offset;
$getPos=`getAttr -t $offsetTime R_ROW01_CTRL.rotateY`;
R_G_ROW01_CTRL.rotateY=$getPos/4;
int $offset=17;
$offsetTime=$currentTime-$offset;
$getPos=`getAttr -t $offsetTime R_ROW01_CTRL.rotateY`;
R_G_ROW02_CTRL.rotateY=$getPos/4;




from pymel.core import *
selObj=cmds.ls(sl=1, fl=1)
for each in selObj:
    each=ls(each)[0]
    print each.mesh()



from pymel.core import *
selObj=cmds.ls(sl=1, fl=1)
getParentChild=cmds.listRelatives(selObj[0], p=1)
getParentParent=cmds.listRelatives(selObj[-1:], p=1)
for each in selObj:
    if cmds.listRelatives(each, p=1)==getParentChild:
        print "1"
    if cmds.listRelatives(each, p=1)==getParentParent:
        print "2"


from pymel.core import *
selObj=cmds.ls(sl=1, fl=1)
getParentChild=cmds.listRelatives(selObj[0], p=1)
getParentParent=cmds.listRelatives(selObj[-1:], p=1)
getChildCurveBuild=[(each) for each in selObj if cmds.listRelatives(each, p=1)==getParentChild]
getParentCurveBuild=[(each) for each in selObj if cmds.listRelatives(each, p=1)==getParentParent]
cmds.select(getChildCurveBuild)
createChildCurve=cmds.polyToCurve(n="childCurve", f=0, dg=3, addUnderTransform=1)
cmds.select(getParentCurveBuild)
createParentCurve=cmds.polyToCurve(n="parentCurve", f=0, dg=3, addUnderTransform=1)






selObj=cmds.ls(sl=1, fl=1)
getParent=selObj[-1:]
getChildren=selObj[1:]

for each in getChildren:
    cmds.connectAttr(getParent+".outputGeometry", each+".inMesh", f=1)





from pymel.core import *
selObj=cmds.ls(sl=1, fl=1)
getParent=selObj[-1:]
getChildren=selObj[:1]
getParent=ls(getParent)[0]
print getParent
print getChildren
for each in getChildren:
    cmds.connectAttr(getParent+".outputGeometry", each+".inMesh")


selObj=cmds.ls(sl=1)
for eachController, eachChild in map(None, selObj[::2], selObj[1::2]):
    cmds.select(eachController)
    cmds.select(eachChild, add=1)
    cmds.blendShape(n=parentItem+"_BShape", w=(0, 1.0))


selObj=cmds.ls(sl=1, fl=1)
parentObj=selObj[0]
childrenObj=selObj[1]
getparentObj=cmds.listRelatives(parentObj, c=1)
getchildObj=cmds.listRelatives(childrenObj, c=1)
for parentItem, childItem in map(None, getparentObj,getchildObj):
    cmds.select(parentItem)
    cmds.select(childItem, add=1)
    cmds.blendShape(n=parentItem+"_BShape", w=(0, 1.0))


#onionSkin
selObj=cmds.ls(sl=1, fl=1)       
if len(selObj)==1:
    pass
else:
    print "Select 1 object" 
getRange=cmds.playbackOptions(q=1, max=1)#get framerange of scene to set keys in iteration 
getRange=int(getRange)#change framerange to an integer. May have to change this to a float iterator on a half key blur(butterfly wings)
for each in range(getRange):
    for item in selObj:
        getloc=cmds.spaceLocator(n=item+"cnstr_lctr")
        cmds.normalConstraint(item, getloc[0])
        placeloc=cmds.spaceLocator(n=item+"_lctr")
        transform=cmds.xform(item, q=True, ws=1, t=True)
        cmds.xform(getloc[0], ws=1, t=transform)  
        cmds.SetKeyTranslate(getloc[0])
        cmds.xform(placeloc[0], ws=1, t=transform)
        cmds.SetKeyTranslate(placeloc[0])               
        rotate=cmds.xform(getloc[0], q=True, ws=1, ro=True)
        cmds.xform(placeloc[0], ws=1, ro=rotate)  
        cmds.SetKeyRotate(placeloc[0])
        maya.mel.eval( "playButtonStepForward;" )
        cmds.delete(getloc[0])


maya.mel.eval( 'artSetToolAndSelectAttr( "artAttrCtx", "ta_normalPush2.paintTargetWeights" );' )






#renaming files

fleName=""
folderPath="/jobs/pan/build/envNativeVillage/release/cache/geometryCache/NativeVillageTentB/backup"
oldNamePart=""
newNamePart=""
for fleName in glob.glob(os.path.join(folderPath, "*"+oldNamePart+"*")):
    os.rename(fleName, fleName.replace(oldNamePart, newNamePart))


getSel=cmds.ls(sl=1, fl=1)
for each in getSel:
    cmds.setAttr(each+'.sx', lock=0)
    cmds.setAttr(each+'.sx', cb=1)   
    cmds.setAttr(each+'.sx', k=1)
    cmds.setAttr(each+'.sy', lock=0)
    cmds.setAttr(each+'.sy', cb=1)   
    cmds.setAttr(each+'.sy', k=1)
    cmds.setAttr(each+'.sz', lock=0)
    cmds.setAttr(each+'.sz', cb=1)   
    cmds.setAttr(each+'.sz', k=1)

    
exec(open('/usr/people/elise-d/workspace/techAnimTools/personal/elise-d/Values//LimitValues.py'))
ValueClass()

exec(open('/usr/people/elise-d/workspace/techAnimTools/personal/elise-d/SSD//SSD.py'))
ui()



objSel=cmds.ls(sl=1, fl=1)
getparentObj=cmds.listRelatives(selObj, c=1)
for each in objSel:
    getShapes=cmds.listRelatives(each, c=1, typ="shape")
    print getShapes
    cmds.polySoftEdge(each, a=180, ch=1)
    cmds.makeIdentity(each, a=True, t=1, r=1, s=1, n=0)
    cmds.delete(each, ch=1)
    for item in getShapes:
        if "Orig" in item:
            cmds.delete(item)


nucleus1_wind_CTRL.windSpeed = abs( noise( frame * 0.05) *20)

getdef=[".sx", ".sy", ".sz", ".rx", ".ry", ".rz", ".tx", ".ty", ".tz", ".visibility"]
objSel=cmds.ls(sl=1, fl=1)
getparentObj=cmds.listRelatives(objSel, c=1)
for each in objSel:
    for eachAttr in getdef:
        cmds.setAttr(each+eachAttr, lock=0)
        cmds.setAttr(each+eachAttr, cb=1)   
        cmds.setAttr(each+eachAttr, k=1)  
        print each+eachAttr+" is now visible in channel box"
    if ":" in each:
        newName=each.split(":")[-1:]
        cmds.rename(each, newName)
        print "renamed "+each+" to "+newName
    getControllerListAttr=cmds.listAttr (objSel, ud=1)
    if getControllerListAttr:
        for eachAttr in getControllerListAttr:
            cmds.setAttr(each+"."+eachAttr, l=0)
            cmds.deleteAttr(each+"."+eachAttr)
            print "deleted "+each+"."+eachAttr
    cmds.polySoftEdge(each, a=180, ch=1)
    cmds.makeIdentity(each, a=True, t=1, r=1, s=1, n=0)
    print "zeroed out transforms for "+each
    cmds.delete(each, ch=1)
    print "deleted history on "+each
    getShapes=cmds.listRelatives(each, c=1, typ="shape")
    print getShapes
    for item in getShapes:
        if "Orig" in item:
            item=cmds.ls(item)
            cmds.delete(item[0])
            print "deleted "+item[0]
        if "output" in item:
            item=cmds.ls(item)
            cmds.rename(item[0], each+"Shape")
            print "renamed "+item[0]+" to "+each+"Shape"

getAll=cmds.ls()
for allthings in getAll:
    getFirstAttr=cmds.listAttr (allthings, w=1, a=1, s=1,u=1)
    for item in getFirstAttr:
        if "mult" in item:
            print allthings+" has "+item



AbcExport -j "-frameRange 1 120 -dataFormat ogawa -root |pCube1 -file /jobs/pan/070_PD/070_PD_0010/maya/cache/alembic/test.abc";

string $each[]=each
string $path[]=path
AbcExport -j "-frameRange 1 120 -dataFormat ogawa -root $each -file $path";






fileName="//usr//people//elise-d//"

selObj=cmds.ls(sl=1, fl=1)
for each in selObj:
    fileName=fileName+str(each)+'.txt'    
    if "Windows" in OSplatform:    
        # folderPath='/'.join(fileName.split('/')[:-1])+"/"
        # printFolder=re.sub(r'/',r'\\', folderPath)       
        if not os.path.exists(fileName): os.makedirs(fileName) 
    if "Linux" in OSplatform:
        open(fileName, 'w')
    inp=open(fileName, 'w+')
    selObj=cmds.ls(sl=1, fl=1)
    filterNode=["animCurve"]
    dirDict={}
    getStrtRange=cmds.playbackOptions(q=1, ast=1)#get framerange of scene to set keys in iteration 
    getEndRange=cmds.playbackOptions(q=1, aet=1)#get framerange of scene to set keys in iteration 
    try:
        ls_str=cmds.listConnections(each, d=0, s=1, p=1, sh=1)
        keepLS=[(eachConnected) for eachConnected in cmds.nodeType(ls_str[0].split(".")[0], i=1) for eachFilter in filterNode if eachConnected==eachFilter]
        if keepLS:
            for eachsource in ls_str:
                remove=each+"_"
                removeobj=eachsource.split(remove)[1]
                eachsource=removeobj.split(".")[0]
                getListedAttr=[(attrib) for attrib in listAttr (each) if attrib==eachsource]         
                attibute=getListedAttr[0]
                frames=cmds.keyframe(each, attribute=getListedAttr[0], time=(getStrtRange,getEndRange), query=True, timeChange=True)
                values=cmds.keyframe(each, attribute=getListedAttr[0], time=(getStrtRange,getEndRange), query=True, valueChange=True)
                print attibute
                inp.write(str(attibute)+";")
                for eachframe, valueitem in map(None, frames, values):
                    #inp.write(str(eachframe)+":"+str(valueitem)+'\n')
                    makeDict={eachframe:valueitem}
                    print str(makeDict)
                    dirDict.update(makeDict)
                    #print dirDict
                inp.write(str(dirDict)+'\n')
                print "saved as "+fileName
        inp.close()  
    except:
        pass





scriptPath="//usr//people//elise-d//workspace//techAnimTools//personal//elise-d//rigModules"
sys.path.append(str(scriptPath))

getToolArrayPath=str(scriptPath)+"/Tools.py"
exec(open(getToolArrayPath))
toolClass=ToolFunctions()


getBasePath=str(scriptPath)+"/baseFunctions_maya.py"
exec(open(getBasePath))
getBaseClass=BaseClass()

focusedThing=cmds.ls(sl=1, fl=1)
maya.mel.eval( "postModelEditorSelectCamera modelPanel4 modelPanel4 0;" )
getOldCam=cmds.ls(sl=1, fl=1)[0]
newcam=cmds.camera()
cmds.select(newcam[0], r=1)
cmds.select(getOldCam, add=1)
cmds.pickWalk(direction="down")
getBaseClass.massTransfer()
cmds.select(focusedThing[0])




selObj=cmds.ls(sl=1, fl=1)           
getOutPutConnection=cmds.listConnections(selObj[0], p=1, c=1, s=0, d=1)
for cord, socket in map(None, getOutPutConnection[::2], getOutPutConnection[1::2]):
    getPlug=selObj[1]+"."+cord.split(".")[1]  
    if "initialShadingGroup" not in socket or "dagSetMembers" not in socket:
        try:
            cmds.connectAttr(getPlug, eachChild, f=1)
            print "connected: "+str(getPlug)+">"+socket
        except:
            print "can't connect: "+str(getPlug)+">"+socket
            pass
getInputConnection=cmds.listConnections(selObj[0], p=1, c=1, s=1, d=0)
for cord, socket in map(None, getInputConnection[::2], getInputConnection[1::2]):
    getSocket=selObj[1]+"."+socket.split(".")[1]  
    try:
        cmds.connectAttr(cord, getSocket, f=1)
        print "connected: "+str(cord)+">"+str(getSocket)
    except:
        print "can't connect: "+str(cord)+">"+str(getSocket)
        pass


getAll=cmds.ls("*")
getName=["wind", "turbulence", "Wind", "noise", "Noise", "Turbulence"]
for each in getAll:
    Attrs=[(attrItem) for attrItem in cmds.listAttr (each, w=1, a=1, s=1,u=1) for thing in getName if thing in attrItem]
    if len(Attrs)>0:
        for item in Attrs:
            try:
                print each+"."+item
                print cmds.getAttr(each+"."+item)
                cmds.setAttr(each+"."+item, 0)
                print "set "+each+"."+item+" to 0"
            except:
                print "can't set "+each+"."+item
                pass



getSel=cmds.ls(sl=1)
getNEWTONOBJ=getSel[:-1]
getLAST=getSel[-1:]
for each in getNEWTONOBJ:
    cmds.select(getLAST, r=1)
    getNewton=cmds.newton(each)





#get type of files in path
path="/"
if [(os.path.join(dirpath, name)) for dirpath, dirnames, files in os.walk(path) for name in files if name.lower().endswith('.tif')]:
	format = '.tif'
	
#getList of frames
getList=[(file.split(format)[0]) for root, dirs, files in os.walk(latestFolder) for file in files if file.endswith(format)]
	
#findingNumbers
frameEndNum = "%04d"%(int(getFrameRange[1].split(".")[0]),)
endFrame=re.sub("\d+$", "", getList[-1]+frameEndNum+format


#if file is existing
fullEndPath=path+endFrame
if os.path.isfile(fullEndPath) ==False:
	print "not here"
	
	
	
#getDictionaries
getFrameRange=[str(shtime.get('aname'))]

