#select surrounding object verts
import pymel.core as pm
from numpy import arange
selObj=cmds.ls(sl=1, fl=1)
cmds.select(selObj[0])
if ".v" in selObj[0]:
    getFirstGrp = selObj[0].split(".")[0]
    getobjOneVerts=[(each) for each in selObj if each.split(".")[0]==getFirstGrp]
    getSecondGrp=[(each) for each in selObj if each.split(".")[0]!=getFirstGrp]
else:
    cmds.ConvertSelectionToVertices()
    getobjOneVerts=cmds.ls(sl=1, fl=1)
    getSecondGrp=[(each) for each in selObj if each != getFirstGrp]
cmds.select(getSecondGrp)
cmds.ConvertSelectionToVertices()
getobjTwoVerts=cmds.ls(sl=1, fl=1)
cmds.select(cl=1)
getvert=[]
for eachone in getobjOneVerts:
    objpos = cmds.xform(eachone, q=1, ws=1, t=1)
    buildCube = cmds.polyCube(d=.2, h=.2, w=.2)
    cmds.move(objpos[0],objpos[1], objpos[2], buildCube[0])
    bb = mc.xform(buildCube[0], q=True, bb=True)
    for eachtwo in getobjTwoVerts:
        objpos2 = cmds.xform(eachtwo, q=1, ws=1, t=1)
        getit = (objpos2[0] > bb[0] and objpos2[0] < bb[3] and objpos2[1] > bb[1] and objpos2[1] < bb[4] and objpos2[2] > bb[2] and objpos2[2] < bb[5])
        if getit == True:
            getvert.append(eachtwo)
    cmds.delete(buildCube[0])
cmds.select(getvert, r=1)
 
 
 
 
#wrapgroup
import pymel.core as pm
selObj=cmds.ls(sl=1, fl=1)
parentObj=selObj[0]
childrenObj=selObj[1]
if ":" in childrenObj:
    name_blend=childrenObj.split(":")[-1]+"_BSPS"
else:
    name_blend = childrenObj+"_BSPS"
print name_blend
cmds.addAttr(parentObj, ln=name_blend, min=0, max=1, at="double", k=1, nn=name_blend)
mc.setAttr(parentObj+"."+name_blend, 1)
getparentObj=cmds.listRelatives(parentObj, ad=1, type="mesh")
getchildObj=cmds.listRelatives(childrenObj, ad=1, type="mesh")
for childItem  in getchildObj:
    for parentItem in getparentObj:
        if "Orig" not in str(childItem) and "Orig" not in str(parentItem):   
            grabNameChild=str(pm.PyNode(childItem).nodeName())
            grabNameParent=str(pm.PyNode(parentItem).nodeName())    
            if ":" in grabNameChild:
                grabNameChild=grabNameChild.split(":")[-1]
            if ":" in grabNameParent:
                grabNameParent=grabNameParent.split(":")[-1]
            grabNameChild=grabNameChild.split("lo")[0]   
            grabNameChild= grabNameChild.split('simCage_')[0]+grabNameChild.split('simCage_')[1]
            grabNameParent=grabNameParent.split("lo")[0]
            if grabNameParent in grabNameChild:
                cmds.select(childItem, r=1)
                cmds.select(parentItem, add=1)
                cmds.CreateWrap()
                #getwrp=cmds.listHistory(parentItem, type="wrap")
                getwrp = mc.ls(mc.listHistory(childItem), type='wrap')[0]
                print getwrp
                print "blending: "+childItem+' to '+parentItem
                mc.connectAttr(parentObj+"."+name_blend,getwrp+".envelope", f=1)
                mc.setAttr(parentObj+"."+name_blend, 1)
