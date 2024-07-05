getparentObj=cmds.listRelatives(cmds.ls(sl=1)[0], ad=1, type="transform")
getchildObj=cmds.listRelatives(cmds.ls(sl=1)[1], ad=1, type="transform") 
for each_child, each_parent in map(None, getchildObj, getparentObj):
    cmds.select(each_child, r=1)
    cmds.wire(w=each_parent,n=str(each_parent)+"_wr", gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )




import maya.cmds as mc
selObj=cmds.ls(sl=1, fl=1)
parentObj=selObj[0]
getparentObj=cmds.listRelatives(parentObj, ad=1, type="mesh")
cmds.select(getparentObj, r=1)






selObj=cmds.ls(sl=1, fl=1)
parentObj=selObj[0]
childrenObj=selObj[1]
getparentObj=cmds.listRelatives(parentObj, ad=1, type="mesh")
if getparentObj:
    pass
else:
    getparentObj=cmds.listRelatives(parentObj, ad=1, type="nurbsCurve")
getchildObj=cmds.listRelatives(childrenObj, ad=1, type="mesh")
if getchildObj:
    pass
else:
    getchildObj=cmds.listRelatives(childrenObj, ad=1, type="nurbsCurve")
for childItem  in getchildObj:
    for parentItem in getparentObj:
        if "Orig" not in str(childItem) and "Orig" not in str(parentItem):    
            grabNameChild=childItem
            grabNameParent=parentItem    
            if ":" in grabNameParent:
                grabNameParent=grabNameParent.split(":")[-1]
                grabNameParent=grabNameParent.split("skinRed_")[-1]
                grabNameParent=grabNameParent.split("_GEP")[0]
            grabNameChild=grabNameChild.split("Substrate_PLY")[0]
            grabNameParent=grabNameParent.split("Shape")[0]    
            grabNameParent=grabNameParent.split("Shape")[0]
            if grabNameParent in grabNameChild:
                print "blending: "+childItem+' to '+parentItem
                cmds.select(childItem, r=1)
                cmds.select(parentItem, add=1)
                cmds.CreateWrap()   


    
cmds.connectAttr("waiter1Tech:waite'r_hairSystemShape.startState", "waiter1Tech:waite'r_hai'r_ncl.inputActiveState[0]", f=1)
cmds.connectAttr("waiter1Tech:waite'r_hairSystemShape.currentState", "waiter1Tech:waite'r_hai'r_ncl.inputState[0]", f=1)
cmds.connectAttr("waiter1Tech:waite'r_hai'r_ncl.startFrame", "waiter1Tech:waite'r_hairSystemShape.startFrame", f=1)
cmds.connectAttr("waiter1Tech:waite'r_hai'r_ncl.outputObjects[0]", "waiter1Tech:waite'r_hairSystemShape.nextState", f=1)




#follicle for cfx


import sys
sys.path.append('/sw/dev/lime/src/mrig/maya/python/lib/')
import extraRigUtils
import maya.cmds as mc

ls = []g  = cmds.group(n='follicle_grp',empty=True)
for e in ls:            
    pos =cmds.pointPosition(e+'.cv[0]')
    lc =cmds.spaceLocator()[0]
    cmds.setAttr(lc+'.t',pos[0],pos[1],pos[2])
    flc = pointToFollicleOnMesh('c_skin_mid',lc, name=e.replace('_mid',''), mode=0)[0]
    cmds.parent(flc,g) 
    cmds.delete(lc)       
    
    
    
parentObj_techcurves = cmds.ls('*:tech_mid_geo_grp')[0]
print parentObj_techcurves
curves = [(each) for each in cmds.listRelatives(parentObj_techcurves, ad=1) if cmds.nodeType(cmds.listRelatives(each, ad=1)) == "nurbsCurve"]
for each in curves:
    simcrv = each.replace('tech_geo', 'input_crv')
    try:
        cmds.disconnectAttr(each+".worldSpace[0]", simcrv+".create")
        print "disconnecting "+each+".worldSpace[0]", simcrv+".create"
    except:
        pass

getchildObj=[(nodes) for nodes in cmds.listRelatives("headFu'r_postTech_crvs_grp", ad = 1) if cmds.nodeType(nodes) == "transform"]
getparentObj=[(nodes) for nodes in cmds.listRelatives("headLongFu'r_postTech_crvs_grp", ad = 1) if cmds.nodeType(nodes) == "transform"]
for childItem, parentItem in map(None, getchildObj, getparentObj):
    cmds.select([childItem, parentItem], r=1)
    wirename = str(childItem)+"_wr"
    cmds.wire(childItem, gw=0, en=1.000000, ce=0.000000, li=0.000000, w=parentItem, dds=[(0, 20)], n=wirename)

getchildObj=[(nodes) for nodes in cmds.listRelatives("bodyFu'r_postTech_crvs_grp", ad = 1) if cmds.nodeType(nodes) == "transform"]
getparentObj=[(nodes) for nodes in cmds.listRelatives("bodyLongFu'r_postTech_crvs_grp", ad = 1) if cmds.nodeType(nodes) == "transform"]
for childItem, parentItem in map(None, getchildObj, getparentObj):
    cmds.select([childItem, parentItem], r=1)
    wirename = str(childItem)+"_wr"
    cmds.wire(childItem, gw=0, en=1.000000, ce=0.000000, li=0.000000, w=parentItem, dds=[(0, 20)], n=wirename)


# reverse a list:
a = [1,2,3,4,5]
print a [::-1]



import sys 
filepath=( '//sw/dev/deglaue/tools//' ) 
if not filepath in sys.path: 
    sys.path.append(str(filepath)) 
import select_transfer
reload (select_transfer)
evokeTool = select_transfer.UV_select_transfer()


for each in cmds.ls(sl=1, fl=1):
    geteachnum= each.split(".vtx")[-1]
    find = cmds.getAttr("blendShape1.inputTarget[0].inputTargetGroup[0].targetWeights{}".format(geteachnum))
    print find


print cmds.currentCtx()

getop = cmds.currentCtx()
currOp = cmds.artAttrCtx(cmds.currentCtx(), q=1, selectedattroper=1)
print currOp

currValue = cmds.artAttrCtx(cmds.currentCtx(), q=1, value=1)
print currValue


currValue = cmds.artAttrCtx(cmds.currentCtx(), q=1, pna=1)
print currValue



currValue = cmds.artAttrCtx(cmds.currentCtx(), q=1, oaa=1)
print currValue


currValue = cmds.artAttrCtx(cmds.currentCtx(), q=1, asl=1)
print currValue

def selectionToVerts():
    # converts the selection to verticies and gets us into the paint skin weights tool
    mel.eval("ConvertSelectionToVertices;")
    if cmds.currentCtx() != "artAttrSkinContext":
        mel.eval("ArtPaintSkinWeightsTool;")



getobj = cmds.ls(sl=1, fl=1)[0]
verts = cmds.ls(getobj+'.vtx[*]', fl=True)
blendShapeNode = cmds.artAttrCtx(cmds.currentCtx(), q=1, asl=1)
blendShapeNode = blendShapeNode.split('.')[1]
for index, each_vert in enumerate(verts):
    #geteachnum= each_vert.split(".vtx[")[-1].split("]")[0]
    find = cmds.getAttr('{0}.inputTarget[0].baseWeights[{1}]'.format(blendShapeNode, index))
    print find


import maya.api.OpenMaya as OpenMaya
selObj= cmds.ls(sl=1, fl=1)
#targetSelection = selObj[:-1]
sourceSelection = selObj[-1]
nodeDagPath = sourceSelection.getDagPath(0)
mCurve = OpenMaya.MFnMesh(nodeDagPath)        
#placement = mfnMesh_src.getUVAtPoint(getmpoint, OpenMaya.MSpace.kWorld, uvSet)   
res=mCurve.closestPoint(sourceSelection+".cv[0]",tolerance = .5, space=om.MSpace.kWorld)
print res
import maya.api.OpenMaya as OpenMaya
selObj= cmds.ls(sl=1, fl=1)
#targetSelection = selObj[:-1]
sourceSelection = selObj[-1]
source_Selection = OpenMaya.MSelectionList()
source_Selection.add(sourceSelection)
#targetSelection = selObj[:-1]
nodeDagPath = source_Selection.getDagPath(0)
MFnCurve = OpenMaya.MFnNurbsCurve(nodeDagPath)        
#placement = mfnMesh_src.getUVAtPoint(getmpoint, OpenMaya.MSpace.kWorld, uvSet)   
res=MFnCurve.closestPoint(sourceSelection+".cv[0]",tolerance = .5, space=om.MSpace.kWorld)
print res


import maya.api.OpenMaya as OpenMaya
selObj= cmds.ls(sl=1, fl=1)
#targetSelection = selObj[:-1]
sourceSelection = selObj[-1]
sourcePoint = selObj[-1]+'.cv[0]'

source_Selection = OpenMaya.MSelectionList()
source_Selection.add(sourceSelection)
nodeDagPath = source_Selection.getDagPath(0)
MFnCurve = OpenMaya.MFnNurbsCurve(nodeDagPath) 

source_Selection_pt = OpenMaya.MSelectionList()
source_Selection_pt.add(sourcePoint)
nodeDagPath = source_Selection_pt.getDagPath(0)
MFnCurvept = OpenMaya.MPoint(nodeDagPath) 

#placement = mfnMesh_src.getUVAtPoint(getmpoint, OpenMaya.MSpace.kWorld, uvSet)   
res=MFnCurve.closestPoint(MFnCurvept,tolerance = .5, space=om.MSpace.kWorld)
print res

#placement = mfnMesh_src.getUVAtPoint(getmpoint, OpenMaya.MSpace.kWorld, uvSet)   
res=MFnCurve.closestPoint(MFnCurvept,tolerance = .5, space=om.MSpace.kWorld)
print res
for each in targetSelection:
    cmds.select(clear=1)
    cmds.select([each], r=1) 
    #cmds.select([sourceSelection], add=1)  
    #cmds.pickWalk(d="up"
    cmds.wire(w=sourceSelection,n=str(each)+"_wr", gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
    cmds.percent(str(each)+"_wr", str(each)+".cv[0]", v=0)
    cmds.percent(str(each)+"_wr", str(each)+".cv[1]", v=.25)
    cmds.percent(str(each)+"_wr", str(each)+".cv[2]", v=.5)
    cmds.percent(str(each)+"_wr", str(each)+".cv[3]", v=.75)



import maya.api.OpenMaya as OpenMaya
selObj= cmds.ls(sl=1, fl=1)
#targetSelection = selObj[:-1]
sourceSelection = selObj[-1]
sourcePoint = selObj[-1]+'.cv[0]'
pos = [0, 0, 0]
source_Selection = OpenMaya.MSelectionList()
source_Selection.add(sourceSelection)
nodeDagPath = source_Selection.getDagPath(0)
MFnCurve = OpenMaya.MFnNurbsCurve(nodeDagPath) 

source_Selection_pt = OpenMaya.MSelectionList()
source_Selection_pt.add(sourcePoint)
nodeDagPath = source_Selection_pt.getDagPath(0)
#MFnCurvecv = OpenMaya.MPoint(nodeDagPath) 

#placement = mfnMesh_src.getUVAtPoint(getmpoint, OpenMaya.MSpace.kWorld, uvSet)   
res=MFnCurve.closestPoint(OpenMaya.MPoint(OpenMaya.MVector(pos)),tolerance = .5, space=om.MSpace.kWorld)
print res



import maya.api.OpenMaya as OpenMaya
selObj= cmds.ls(sl=1, fl=1)
#targetSelection = selObj[:-1]
sourceSelection = selObj

sourcePoint = selObj[0]+'.cv[0]'

pos = [0, 0, 0]
source_Selection = OpenMaya.MSelectionList()
for each in selObj:
    source_Selection.add(each)
nodeDagPath = source_Selection.getDagPath(0)
MFnCurve = OpenMaya.MFnNurbsCurve(nodeDagPath) 

source_Selection_pt = OpenMaya.MSelectionList()
source_Selection_pt.add(sourcePoint)
nodeDagPath = source_Selection_pt.getDagPath(0)
#MFnCurvecv = OpenMaya.MPoint(nodeDagPath) 

#placement = mfnMesh_src.getUVAtPoint(getmpoint, OpenMaya.MSpace.kWorld, uvSet)   
res=MFnCurve.closestPoint(OpenMaya.MPoint(OpenMaya.MVector(pos)),tolerance = .5, space=om.MSpace.kWorld)
print res[0]
objplace = (res[0][0], res[0][1] , res[0][2])
print objplace
createtargetspace = cmds.spaceLocator(n="newplace")
cmds.xform(createtargetspace[0], ws=1, t=objplace)

import maya.api.OpenMaya as OpenMaya
selObj= cmds.ls(sl=1, fl=1)
targetSelection = selObj[:-1]
source_get_Selection_cv = selObj[-1]

sourcePoint = source_get_Selection_cv+'.cv[0]'

pos = cmds.pointPosition(sourcePoint )
print pos
for each in targetSelection:
    target_Selection = OpenMaya.MSelectionList()
    target_Selection.add(each)
    nodeDagPath = source_Selection.getDagPath(0)
    MFnCurve = OpenMaya.MFnNurbsCurve(nodeDagPath) 
    #source_Selection_pt = OpenMaya.MSelectionList()
    #source_Selection_pt.add(sourcePoint)
    #nodeDagPath = source_Selection_pt.getDagPath(0)
    #MFnCurvecv = OpenMaya.MPoint(nodeDagPath) 
    #placement = mfnMesh_src.getUVAtPoint(getmpoint, OpenMaya.MSpace.kWorld, uvSet)   
    res=MFnCurve.closestPoint(OpenMaya.MPoint(OpenMaya.MVector(pos)),tolerance = .5, space=om.MSpace.kWorld)
    print res[0]
    objplace = (res[0][0], res[0][1] , res[0][2])
    print objplace
    createtargetspace = cmds.spaceLocator(n="newplace")
    cmds.xform(createtargetspace[0], ws=1, t=objplace)
import maya.api.OpenMaya as OpenMaya
selObj= cmds.ls(sl=1, fl=1)
targetSelection = selObj[:-1]
source_get_Selection_cv = selObj[-1]
sourcePoint = source_get_Selection_cv+'.cv[0]'
pos = cmds.pointPosition(sourcePoint )
print pos
for each in targetSelection:
    target_Selection = OpenMaya.MSelectionList()
    target_Selection.add(each)
    nodeDagPath = target_Selection.getDagPath(0)
    MFnCurve = OpenMaya.MFnNurbsCurve(nodeDagPath)   
    res=MFnCurve.closestPoint(OpenMaya.MPoint(OpenMaya.MVector(pos)),tolerance = .001, space=om.MSpace.kWorld)
    objplace = (res[0][0], res[0][1] , res[0][2])
    createtargetspace = cmds.spaceLocator(n="newplace")
    cmds.xform(createtargetspace[0], ws=1, t=objplace)


point=om.MVector(res[0])
for each in targetSelection:
    cmds.select(clear=1)
    cmds.select([each], r=1) 
    #cmds.select([sourceSelection], add=1)  
    #cmds.pickWalk(d="up"
    cmds.wire(w=sourceSelection,n=str(each)+"_wr", gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
    cmds.percent(str(each)+"_wr", str(each)+".cv[0]", v=0)
    cmds.percent(str(each)+"_wr", str(each)+".cv[1]", v=.25)
    cmds.percent(str(each)+"_wr", str(each)+".cv[2]", v=.5)
    cmds.percent(str(each)+"_wr", str(each)+".cv[3]", v=.75)

import maya.api.OpenMaya as OpenMaya
selObj= cmds.ls(sl=1, fl=1)
targetSelection = selObj[:-1]
source_get_Selection_cv = selObj[-1]
sourcePoint = source_get_Selection_cv+'.cv[0]'
pos = cmds.pointPosition(sourcePoint )
dropoff = 0.003
for each in targetSelection:
    target_Selection = OpenMaya.MSelectionList()
    target_Selection.add(each)
    nodeDagPath = target_Selection.getDagPath(0)
    MFnCurve = OpenMaya.MFnNurbsCurve(nodeDagPath)   
    res=MFnCurve.closestPoint(OpenMaya.MPoint(OpenMaya.MVector(pos)), space=om.MSpace.kWorld)
    objplace = (res[0][0], res[0][1] , res[0][2])
    if not objplace[0] < pos[0]-dropoff:
        if not objplace[0] > pos[0]+dropoff:
            createtargetspace = cmds.spaceLocator(n="newplace")
            cmds.xform(createtargetspace[0], ws=1, t=objplace)

import maya.api.OpenMaya as OpenMaya
selObj= cmds.ls(sl=1, fl=1)
targetSelection = selObj[:-1]
source_get_Selection_cv = selObj[-1]
sourcePoint = source_get_Selection_cv+'.cv[0]'
pos = cmds.pointPosition(sourcePoint )
dropoff = 0.003
collectmycurve=[]
for each in targetSelection:
    target_Selection = OpenMaya.MSelectionList()
    target_Selection.add(each)
    nodeDagPath = target_Selection.getDagPath(0)
    MFnCurve = OpenMaya.MFnNurbsCurve(nodeDagPath)   
    res=MFnCurve.closestPoint(OpenMaya.MPoint(OpenMaya.MVector(pos)), space=om.MSpace.kWorld)
    objplace = (res[0][0], res[0][1] , res[0][2])
    if not objplace[0] < pos[0]-dropoff:
        if not objplace[0] > pos[0]+dropoff:
            collectmycurve.append(each)
            createtargetspace = cmds.spaceLocator(n="newplace")
            cmds.xform(createtargetspace[0], ws=1, t=objplace)
cmds.select(collectmycurve, add=1)
for each in collectmycurve:
    cmds.select(clear=1)
    cmds.select([each], r=1) 
    #cmds.select([sourceSelection], add=1)  
    #cmds.pickWalk(d="up"
    cmds.wire(w=source_get_Selection_cv,n=str(each)+"_wr", gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
    cmds.percent(str(each)+"_wr", str(each)+".cv[0]", v=0)
    cmds.percent(str(each)+"_wr", str(each)+".cv[1]", v=.25)
    cmds.percent(str(each)+"_wr", str(each)+".cv[2]", v=.5)
    cmds.percent(str(each)+"_wr", str(each)+".cv[3]", v=.75)

import maya.api.OpenMaya as OpenMaya
targetSelection_crvs=cmds.listRelatives(cmds.ls(sl=1)[1], ad=1, type="nurbsCurve")
cmds.select(targetSelection, r=1)
cmds.pickWalk(d="up")
targetSelection_crvs= cmds.ls(sl=1, fl=1)
dropoff = 0.003
getsrcObj=cmds.listRelatives(cmds.ls(sl=1)[0], ad=1, type="nurbsCurve")
for each_src in getsrcObj:
    cmds.select(each_src, r=1)
    cmds.pickWalk(d="up")
    source_get_Selection_cv = cmds.ls(sl=1, fl=1)[0]
    sourcePoint = source_get_Selection_cv+'.cv[0]'
    pos = cmds.pointPosition(sourcePoint )
    collectmycurve=[]
    for each in targetSelection:
        target_Selection = OpenMaya.MSelectionList()
        target_Selection.add(each)
        nodeDagPath = target_Selection.getDagPath(0)
        MFnCurve = OpenMaya.MFnNurbsCurve(nodeDagPath)   
        res=MFnCurve.closestPoint(OpenMaya.MPoint(OpenMaya.MVector(pos)), space=om.MSpace.kWorld)
        objplace = (res[0][0], res[0][1] , res[0][2])
        if not objplace[0] < pos[0]-dropoff:
            if not objplace[0] > pos[0]+dropoff:
                collectmycurve.append(each)
                #createtargetspace = cmds.spaceLocator(n="newplace")
                #cmds.xform(createtargetspace[0], ws=1, t=objplace)
    # print collectmycurve
    # cmds.select(collectmycurve, r=1)
    for each_tgt in collectmycurve:
        shapetgt=cmds.listRelatives(each_tgt, ad=1, type="nurbsCurve")[0]
        cmds.select(clear=1)
        cmds.select([each_tgt], r=1) 
        #cmds.select([sourceSelection], add=1)  
        #cmds.pickWalk(d="up"
        shapetgt=cmds.listConnections(shapetgt, s=1, type="wire")[0]
        if len(shapetgt)<1:
            cmds.wire(w=each_src,n=str(each_tgt)+"_wr", gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[0]", v=0)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[1]", v=.25)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[2]", v=.5)                 cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[3]", v=.75)




import maya.api.OpenMaya as OpenMaya
getsrcObj=cmds.listRelatives(cmds.ls(sl=1)[0], ad=1, type="nurbsCurve")
targetSelection_cr=cmds.listRelatives(cmds.ls(sl=1)[1], ad=1, type="nurbsCurve")
cmds.select(targetSelection_cr, r=1)
cmds.pickWalk(d="up")
targetSelection_crvs= cmds.ls(sl=1, fl=1)
dropoff = 0.003
for each_src, each_tgt_crv in map(None, getsrcObj, targetSelection_crvs):
    cmds.select(each_src, r=1)
    cmds.pickWalk(d="up")
    source_get_Selection_cv = cmds.ls(sl=1, fl=1)[0]
    sourcePoint = source_get_Selection_cv+'.cv[0]'
    pos = cmds.pointPosition(sourcePoint )
    collectmycurve=[]
    target_Selection = OpenMaya.MSelectionList()
    target_Selection.add(each_tgt_crv)
    nodeDagPath = target_Selection.getDagPath(0)
    MFnCurve = OpenMaya.MFnNurbsCurve(nodeDagPath)  
    try:
        res=MFnCurve.closestPoint(OpenMaya.MPoint(OpenMaya.MVector(pos)), space=om.MSpace.kWorld)
        objplace = (res[0][0], res[0][1] , res[0][2])
        if not objplace[0] < pos[0]-dropoff:
            if not objplace[0] > pos[0]+dropoff:
                collectmycurve.append(each_tgt_crv)
    except:
        pass
    if collectmycurve:
        print collectmycurve
            for each_tgt in collectmycurve:
                shapetgt=cmds.listRelatives(each_tgt, ad=1, type="nurbsCurve")[0]
                cmds.select(clear=1)
                cmds.select([each_tgt], r=1) 
                #cmds.select([sourceSelection], add=1)  
                #cmds.pickWalk(d="up"
                try:
                    shapetgt=cmds.listConnections(shapetgt, s=1, type="wire")[0]
                except:
                    pass
                if len(shapetgt)<1:
                    cmds.wire(w=each_src,n=str(each_tgt)+"_wr", gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
                    cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[0]", v=0)
                    cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[1]", v=.25)
                    cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[2]", v=.5)
                    cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[3]", v=.75)




import maya.api.OpenMaya as OpenMaya
getsrcObj=cmds.listRelatives(cmds.ls(sl=1)[0], ad=1, type="transform")
targetSelection_crvs=cmds.listRelatives(cmds.ls(sl=1)[1], ad=1, type="transform")
dropoff = 0.003
collectmycurve = []
collectmycurve_ct={}
for each_tgt_crv  in targetSelection_crvs:
    target_Selection = OpenMaya.MSelectionList()
    target_Selection.add(each_tgt_crv)
    nodeDagPath = target_Selection.getDagPath(0)
    MFnCurve = OpenMaya.MFnNurbsCurve(nodeDagPath)  
    for each_src in getsrcObj:
        sourcePoint = each_src+'.cv[0]'
        pos = cmds.pointPosition(sourcePoint)   
    try:
        res=MFnCurve.closestPoint(OpenMaya.MPoint(OpenMaya.MVector(pos)), space=om.MSpace.kWorld)
        objplace = (res[0][0], res[0][1] , res[0][2])
        if not objplace[0] < pos[0]-dropoff:
            if not objplace[0] > pos[0]+dropoff:
                collectmycurve.append(each_tgt_crv)
    except:
        pass
    if collectmycurve:
        newdict = {each_src:collectmycurve}
        collectmycurve_ct.update(newdict)
print collectmycurve
            for each_tgt in collectmycurve:
                shapetgt=cmds.listRelatives(each_tgt, ad=1, type="nurbsCurve")[0]
                cmds.select(clear=1)
                cmds.select([each_tgt], r=1) 
                #cmds.select([sourceSelection], add=1)  
                #cmds.pickWalk(d="up"
                try:
                    shapetgt=cmds.listConnections(shapetgt, s=1, type="wire")[0]
                except:
                    pass
                if len(shapetgt)<1:
                    cmds.wire(w=each_src,n=str(each_tgt)+"_wr", gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
                    cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[0]", v=0)
                    cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[1]", v=.25)
                    cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[2]", v=.5)
                    cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[3]", v=.75)


import maya.api.OpenMaya as OpenMaya
getsrcObj=cmds.listRelatives(cmds.ls(sl=1)[0], ad=1, type="transform")
targetSelection_crvs=cmds.listRelatives(cmds.ls(sl=1)[1], ad=1, type="transform")
dropoff = 0.003
collectmycurve = []
collectmycurve_ct={}
for each_tgt_crv  in targetSelection_crvs:
    target_Selection = OpenMaya.MSelectionList()
    target_Selection.add(each_tgt_crv)
    nodeDagPath = target_Selection.getDagPath(0)
    MFnCurve = OpenMaya.MFnNurbsCurve(nodeDagPath)  
    for each_src in getsrcObj:
        sourcePoint = each_src+'.cv[0]'
        pos = cmds.pointPosition(sourcePoint)
        try:
            res=MFnCurve.closestPoint(OpenMaya.MPoint(OpenMaya.MVector(pos)), space=om.MSpace.kWorld)
            objplace = (res[0][0], res[0][1] , res[0][2])
            if not objplace[0] < pos[0]-dropoff:
                if not objplace[0] > pos[0]+dropoff:
                    collectmycurve.append(each_tgt_crv)
        except:
            pass
        if collectmycurve:
            newdict = {each_src:collectmycurve}
            collectmycurve_ct.update(newdict)
print collectmycurve_ct
import maya.api.OpenMaya as OpenMaya
getsrcObj=cmds.listRelatives(cmds.ls(sl=1)[0], ad=1, type="transform")
targetSelection_crvs=cmds.listRelatives(cmds.ls(sl=1)[1], ad=1, type="transform")
dropoff = 0.003
collectmycurve = []
collectmycurve_ct={}
for each_tgt_crv  in targetSelection_crvs:
    target_Selection = OpenMaya.MSelectionList()
    target_Selection.add(each_tgt_crv)
    nodeDagPath = target_Selection.getDagPath(0)
    MFnCurve = OpenMaya.MFnNurbsCurve(nodeDagPath)  
for each_src in getsrcObj:
    sourcePoint = each_src+'.cv[0]'
    pos = cmds.pointPosition(sourcePoint)
    try:
        res=MFnCurve.closestPoint(OpenMaya.MPoint(OpenMaya.MVector(pos)), space=om.MSpace.kWorld)
        objplace = (res[0][0], res[0][1] , res[0][2])
        if not objplace[0] < pos[0]-dropoff:
            if not objplace[0] > pos[0]+dropoff:
                collectmycurve.append(each_tgt_crv)
    except:
        pass
    if collectmycurve:

    print collectmycurve_ct


import maya.api.OpenMaya as OpenMaya
getsrcObj=cmds.listRelatives(cmds.ls(sl=1)[0], ad=1, type="transform")
targetSelection_crvs=cmds.listRelatives(cmds.ls(sl=1)[1], ad=1, type="transform")
dropoff = 0.003
collectmycurve_ct={}
for each_src in getsrcObj:
    sourcePoint = each_src+'.cv[0]'
    pos = cmds.pointPosition(sourcePoint)
    collectmycurve = []
    for each_tgt_crv  in targetSelection_crvs:
        target_Selection = OpenMaya.MSelectionList()
        target_Selection.add(each_tgt_crv)
        nodeDagPath = target_Selection.getDagPath(0)
        MFnCurve = OpenMaya.MFnNurbsCurve(nodeDagPath)  
        res=MFnCurve.closestPoint(OpenMaya.MPoint(OpenMaya.MVector(pos)), space=om.MSpace.kWorld)
        objplace = (res[0][0], res[0][1] , res[0][2])
        if not objplace[0] < pos[0]-dropoff:
            if not objplace[0] > pos[0]+dropoff:
                collectmycurve.append(each_tgt_crv)
    newdict = {each_src:collectmycurve}
    collectmycurve_ct.update(newdict) 
print collectmycurve_ct

import maya.api.OpenMaya as OpenMaya
getsrcObj=cmds.listRelatives(cmds.ls(sl=1)[0], ad=1, type="transform")
targetSelection_crvs=cmds.listRelatives(cmds.ls(sl=1)[1], ad=1, type="transform")
dropoff = 0.001
collectmycurve_ct={}
for each_src in getsrcObj:
    print each_src
    collectmycurve = []
    sourcePoint = each_src+'.cv[0]'
    pos = cmds.pointPosition(sourcePoint)
    for each_tgt_crv  in targetSelection_crvs:
        set_dict = {}
        target_Selection = OpenMaya.MSelectionList()
        target_Selection.add(each_tgt_crv)
        nodeDagPath = target_Selection.getDagPath(0)
        MFnCurve = OpenMaya.MFnNurbsCurve(nodeDagPath)  
        res=MFnCurve.closestPoint(OpenMaya.MPoint(OpenMaya.MVector(pos)), space=om.MSpace.kWorld)
        objplace = (res[0][0], res[0][1] , res[0][2])
        if not objplace[0] < pos[0]-dropoff:
            if not objplace[0] > pos[0]+dropoff:
                print each_tgt_crv
import maya.api.OpenMaya as OpenMaya
getsrcObj=cmds.listRelatives(cmds.ls(sl=1)[0], ad=1, type="transform")
targetSelection_crvs=cmds.listRelatives(cmds.ls(sl=1)[1], ad=1, type="transform")
dropoff = 0.0006
collectmycurve_ct={}
for each_src in getsrcObj:
    collectmycurve = []
    sourcePoint = each_src+'.cv[0]'
    pos = cmds.pointPosition(sourcePoint, w=1)
    for each_tgt_crv  in targetSelection_crvs:
        set_dict = {}
        target_Selection = OpenMaya.MSelectionList()
        target_Selection.add(each_tgt_crv)
        nodeDagPath = target_Selection.getDagPath(0)
        MFnCurve = OpenMaya.MFnNurbsCurve(nodeDagPath)  
        res=MFnCurve.closestPoint(OpenMaya.MPoint(OpenMaya.MVector(pos)), space=om.MSpace.kWorld)
        objplace = (res[0][0], res[0][1] , res[0][2])
        if not objplace[0] < pos[0]-dropoff:
            if not objplace[0] > pos[0]+dropoff:
                collectmycurve.append(each_tgt_crv)
    newdict = {each_src:collectmycurve}
    collectmycurve_ct.update(newdict) 
for key, value in collectmycurve_ct.items():
    for each_tgt in value:
        shapetgt=cmds.listRelatives(each_tgt, ad=1, type="nurbsCurve")[0]
        cmds.select(clear=1)
        cmds.select([each_tgt], r=1) 
        try:
            fnd=cmds.listConnections(shapetgt, s=1, type="wire")[0]
        except:     
            grabWire = cmds.wire(w=key,n=str(each_tgt)+"_wr", gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
            cmds.setAttr(grabWire[0]+".rotation", 0)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[0]", v=0)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[1]", v=.25)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[2]", v=.5)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[3]", v=.75)import maya.api.OpenMaya as OpenMaya



getsrcObj=cmds.listRelatives(cmds.ls(sl=1)[0], ad=1, type="transform")
targetSelection_crvs=cmds.listRelatives(cmds.ls(sl=1)[1], ad=1, type="transform")
dropoff = 0.0006
collectmycurve_ct={}
for each_src in getsrcObj:
    collectmycurve = []
    sourcePoint = each_src+'.cv[0]'
    pos = cmds.pointPosition(sourcePoint, w=1)
    for each_tgt_crv  in targetSelection_crvs:
        sourcePoint = each_tgt_crv+'.cv[0]'
        tgt_pos = cmds.pointPosition(sourcePoint, w=1)
        if not tgt_pos[0] < pos[0]-dropoff:
            if not tgt_pos[0] > pos[0]+dropoff:
                if not tgt_pos[1] < pos[1]-dropoff:
                    if not tgt_pos[1] > pos[1]+dropoff:
                        if not tgt_pos[2] < pos[2]-dropoff:
                            if not tgt_pos[2] > pos[2]+dropoff:
                                collectmycurve.append(each_tgt_crv)
    newdict = {each_src:collectmycurve}
    collectmycurve_ct.update(newdict) 
for key, value in collectmycurve_ct.items():
    for each_tgt in value:
        shapetgt=cmds.listRelatives(each_tgt, ad=1, type="nurbsCurve")[0]
        cmds.select(clear=1)
        cmds.select([each_tgt], r=1) 
        try:
            fnd=cmds.listConnections(shapetgt, s=1, type="wire")[0]
        except:     
            grabWire = cmds.wire(w=key,n=str(each_tgt)+"_wr", gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
            cmds.setAttr(grabWire[0]+".rotation", 0)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[0]", v=0)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[1]", v=.25)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[2]", v=.5)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[3]", v=.75)
getsrcObj=cmds.listRelatives(cmds.ls(sl=1)[0], ad=1, type="transform")
targetSelection_crvs=cmds.listRelatives(cmds.ls(sl=1)[1], ad=1, type="transform")
dropoff = 0.1
collectmycurve_ct={}
for each_src in getsrcObj:
    collectmycurve = []
    sourcePoint = each_src+'.cv[0]'
    pos = cmds.pointPosition(sourcePoint, w=1)
    for each_tgt_crv  in targetSelection_crvs:
        collectmycurve = []
        sourcePoint = each_tgt_crv+'.cv[0]'
        tgt_pos = cmds.pointPosition(sourcePoint, w=1)
        if not tgt_pos[0] < pos[0]-dropoff:
            if not tgt_pos[0] > pos[0]+dropoff:
                if not tgt_pos[1] < pos[1]-dropoff:
                    if not tgt_pos[1] > pos[1]+dropoff:
                        if not tgt_pos[2] < pos[2]-dropoff:
                            if not tgt_pos[2] > pos[2]+dropoff:
                                collectmycurve.append(each_tgt_crv)
    newdict = {each_src:collectmycurve}
    collectmycurve_ct.update(newdict) 
print collectmycurve_ct
for key, value in collectmycurve_ct.items():
    for each_tgt in value:
        shapetgt=cmds.listRelatives(each_tgt, ad=1, type="nurbsCurve")[0]
        cmds.select(clear=1)
        cmds.select([each_tgt], r=1) 
        try:
            fnd=cmds.listConnections(shapetgt, s=1, type="wire")[0]
        except:     
            grabWire = cmds.wire(w=key,n=str(each_tgt)+"_wr", gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
            cmds.setAttr(grabWire[0]+".rotation", 0)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[0]", v=0)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[1]", v=.25)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[2]", v=.5)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[3]", v=.75)
getsrcObj=cmds.listRelatives(cmds.ls(sl=1)[0], ad=1, type="transform")
targetSelection_crvs=cmds.listRelatives(cmds.ls(sl=1)[1], ad=1, type="transform")
dropoff = .5
collectmycurve_ct={}
for each_src in getsrcObj:
    collectmycurve = []
    sourcePoint = each_src+'.cv[0]'
    pos = cmds.pointPosition(sourcePoint, w=1)
    for each_tgt_crv  in targetSelection_crvs:
        collectmycurve = []
        sourcePoint = each_tgt_crv+'.cv[0]'
        tgt_pos = cmds.pointPosition(sourcePoint, w=1)
        x_pos_min = pos[0]-dropoff
        x_pos_max = pos[0]+dropoff
        y_pos_min = pos[1]-dropoff
        y_pos_max = pos[1]+dropoff
        z_pos_min = pos[2]-dropoff
        z_pos_max = pos[2]+dropoff 
        if not tgt_pos[0] < x_pos_min and not tgt_pos[0] > x_pos_max and not tgt_pos[1] < y_pos_min and not tgt_pos[1] > y_pos_max and not tgt_pos[2] < z_pos_min and not tgt_pos[2] > z_pos_max:
            collectmycurve.append(each_tgt_crv)
    newdict = {each_src:collectmycurve}
    collectmycurve_ct.update(newdict) 
print collectmycurve_ct
for key, value in collectmycurve_ct.items():
    for each_tgt in value:
        shapetgt=cmds.listRelatives(each_tgt, ad=1, type="nurbsCurve")[0]
        cmds.select(clear=1)
        cmds.select([each_tgt], r=1) 
        try:
            fnd=cmds.listConnections(shapetgt, s=1, type="wire")[0]
        except:     
            grabWire = cmds.wire(w=key,n=str(each_tgt)+"_wr", gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
            cmds.setAttr(grabWire[0]+".rotation", 0)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[0]", v=0)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[1]", v=.25)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[2]", v=.5)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[3]", v=.75)
getsrcObj=cmds.listRelatives(cmds.ls(sl=1)[0], ad=1, type="transform")
targetSelection_crvs=cmds.listRelatives(cmds.ls(sl=1)[1], ad=1, type="transform")
dropoff = .02
collectmycurve_ct={}
for each_src in getsrcObj[:-698]:
    collectmycurve = []
    sourcePoint = each_src+'.cv[0]'
    pos = cmds.pointPosition(sourcePoint, w=1)
    x_pos_min = pos[0]-dropoff
    lc =cmds.spaceLocator()[0]
    cmds.setAttr(lc+'.t',x_pos_min,pos[1],pos[2])    
    x_pos_max = pos[0]+dropoff
    lc =cmds.spaceLocator()[0]
    cmds.setAttr(lc+'.t',x_pos_max,pos[1],pos[2])        
    y_pos_min = pos[1]-dropoff
    lc =cmds.spaceLocator()[0]
    cmds.setAttr(lc+'.t',pos[0],y_pos_min,pos[2])       
    y_pos_max = pos[1]+dropoff
    lc =cmds.spaceLocator()[0]
    cmds.setAttr(lc+'.t',pos[0],y_pos_max,pos[2])       
    z_pos_min = pos[2]-dropoff
    lc =cmds.spaceLocator()[0]
    cmds.setAttr(lc+'.t',pos[0],pos[1],z_pos_min)
    z_pos_max = pos[2]+dropoff 
    lc =cmds.spaceLocator()[0]
    cmds.setAttr(lc+'.t',pos[0],pos[1],z_pos_max)      
    for each_tgt_crv  in targetSelection_crvs:
        collectmycurve = []
        tgt_sourcePoint = each_tgt_crv+'.cv[0]'
        tgt_pos = cmds.pointPosition(tgt_sourcePoint, w=1) 
        if not tgt_pos[0] < x_pos_min and not tgt_pos[0] > x_pos_max and not tgt_pos[1] < y_pos_min and not tgt_pos[1] > y_pos_max and not tgt_pos[2] < z_pos_min and not tgt_pos[2] > z_pos_max:
            collectmycurve.append(each_tgt_crv)
    newdict = {each_src:collectmycurve}
    collectmycurve_ct.update(newdict) 
print collectmycurve_ct
for key, value in collectmycurve_ct.items():
    for each_tgt in value:
        shapetgt=cmds.listRelatives(each_tgt, ad=1, type="nurbsCurve")[0]
        cmds.select(clear=1)
        cmds.select([each_tgt], r=1) 
        try:
            fnd=cmds.listConnections(shapetgt, s=1, type="wire")[0]        except:     
            grabWire = cmds.wire(w=key,n=str(each_tgt)+"_wr", gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
            cmds.setAttr(grabWire[0]+".rotation", 0)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[0]", v=0)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[1]", v=.25)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[2]", v=.5)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[3]", v=.75)

getsrcObj=cmds.listRelatives(cmds.ls(sl=1)[0], ad=1, type="transform")
targetSelection_crvs=cmds.listRelatives(cmds.ls(sl=1)[1], ad=1, type="transform")
dropoff = .02
collectmycurve_ct={}
for each_src in getsrcObj[:-698]:
    collectmycurve = []
    sourcePoint = each_src+'.cv[0]'
    pos = cmds.pointPosition(sourcePoint, w=1)
    x_pos_min, x_pos_max, y_pos_min, y_pos_max, z_pos_min, z_pos_max = pos[0]-dropoff, pos[0]+dropoff, pos[1]-dropoff, pos[1]+dropoff, pos[2]-dropoff, pos[2]+dropoff 
    for each_tgt_crv  in targetSelection_crvs:
        collectmycurve = []
        tgt_sourcePoint = each_tgt_crv+'.cv[0]'
        tgt_pos = cmds.pointPosition(tgt_sourcePoint, w=1) 
        if not tgt_pos[0] < x_pos_min and not tgt_pos[0] > x_pos_max and not tgt_pos[1] < y_pos_min and not tgt_pos[1] > y_pos_max and not tgt_pos[2] < z_pos_min and not tgt_pos[2] > z_pos_max:
            collectmycurve.append(each_tgt_crv)
    newdict = {each_src:collectmycurve}
    collectmycurve_ct.update(newdict) 
print collectmycurve_ct
for key, value in collectmycurve_ct.items():
    for each_tgt in value:
        shapetgt=cmds.listRelatives(each_tgt, ad=1, type="nurbsCurve")[0]
        cmds.select(clear=1)
        cmds.select([each_tgt], r=1) 
        try:
            fnd=cmds.listConnections(shapetgt, s=1, type="wire")[0]
        except:     
            grabWire = cmds.wire(w=key,n=str(each_tgt)+"_wr", gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
            cmds.setAttr(grabWire[0]+".rotation", 0)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[0]", v=0)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[1]", v=.25)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[2]", v=.5)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[3]", v=.75)
            
#must do wire then follicle constraint

getsrcObj=cmds.listRelatives(cmds.ls(sl=1)[0], ad=1, type="transform")
targetSelection_crvs=cmds.listRelatives(cmds.ls(sl=1)[1], ad=1, type="transform")
dropoff = .03
collectmycurve_ct={}
for each_src in getsrcObj:
    collectmycurve = []
    sourcePoint = each_src+'.cv[0]'
    pos = cmds.pointPosition(sourcePoint, w=1)
    x_pos_min, x_pos_max, y_pos_min, y_pos_max, z_pos_min, z_pos_max = pos[0]-dropoff, pos[0]+dropoff, pos[1]-dropoff, pos[1]+dropoff, pos[2]-dropoff, pos[2]+dropoff 
    for each_tgt_crv  in targetSelection_crvs:
        tgt_sourcePoint = each_tgt_crv+'.cv[0]'
        tgt_pos = cmds.pointPosition(tgt_sourcePoint, w=1) 
        if tgt_pos[0] >= x_pos_min and tgt_pos[0] <= x_pos_max and tgt_pos[1] >= y_pos_min and tgt_pos[1] <= y_pos_max and tgt_pos[2] >= z_pos_min and tgt_pos[2] <= z_pos_max:
            collectmycurve.append(each_tgt_crv)
    newdict = {each_src:collectmycurve}
    collectmycurve_ct.update(newdict) 
for key, value in collectmycurve_ct.items():
    for each_tgt in value:
        shapetgt=cmds.listRelatives(each_tgt, ad=1, type="nurbsCurve")[0]
        cmds.select(clear=1)
        cmds.select([each_tgt], r=1) 
        try:
            fnd=cmds.listConnections(shapetgt, s=1, type="wire")[0]
        except:     
            grabWire = cmds.wire(w=key,n=str(each_tgt)+"_wr", gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
            cmds.setAttr(grabWire[0]+".rotation", 0)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[0]", v=0)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[1]", v=.25)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[2]", v=.5)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[3]", v=.75)


import re
baseShapeSelection_crvs=cmds.listRelatives(cmds.ls(sl=1)[0], ad=1, type="nurbsCurve")
for eachbase in baseShapeSelection_crvs:
    fnd=[(each.split('.')[0]) for each in cmds.listConnections(eachbase, p=1) if "baseWire" in each]
    get_trsnlt = [(eachtrns) for eachtrns in cmds.listRelatives(eachbase, p=1, type= "transform")][0]
    for each_item in fnd:
        gert = re.findall(r'\d+', each_item)[0]
        extract = each_item.split(gert)[0]+"Shape"+gert+"Orig"
        get_foll_static = [(fol) for fol in cmds.listConnections(extract, p=1, sh=1) if cmds.nodeType(fol) =="follicle"][0]
        get_foll = [(trnshr) for trnshr in cmds.listRelatives(get_foll_static.split('.')[0], p=1, type= "transform")][0]
        cmds.parent(get_trsnlt, get_foll)


getsrcObj=cmds.listRelatives(cmds.ls(sl=1)[0], ad=1, type="transform")
targetSelection_crvs=cmds.listRelatives(cmds.ls(sl=1)[1], ad=1, type="transform")
dropoff = .03
collectmycurve_ct={}
for each_src in getsrcObj:
    collectmycurve = []
    sourcePoint = each_src+'.cv[0]'
    pos = cmds.pointPosition(sourcePoint, w=1)
    x_pos_min, x_pos_max, y_pos_min, y_pos_max, z_pos_min, z_pos_max = pos[0]-dropoff, pos[0]+dropoff, pos[1]-dropoff, pos[1]+dropoff, pos[2]-dropoff, pos[2]+dropoff 
    for each_tgt_crv  in targetSelection_crvs:
        tgt_sourcePoint = each_tgt_crv+'.cv[0]'
        tgt_pos = cmds.pointPosition(tgt_sourcePoint, w=1) 
        if tgt_pos[0] >= x_pos_min and tgt_pos[0] <= x_pos_max and tgt_pos[1] >= y_pos_min and tgt_pos[1] <= y_pos_max and tgt_pos[2] >= z_pos_min and tgt_pos[2] <= z_pos_max:
            collectmycurve.append(each_tgt_crv)
    newdict = {each_src:collectmycurve}
    collectmycurve_ct.update(newdict) 

import re


tgtdict = {}
import esCurveDeformer
get_tgt_geo=sorted([(each) for each in cmds.listRelatives(cmds.ls("c_featherSystem_mid_postTech_geo_separated")[0], ad=1, type="mesh") if "Orig" not in each])
for each in get_tgt_geo:
    get_num = re.findall(r'\d+', each)
    c'r_dict = {get_num:each}
    tgtdict.update(tgtdict)
srcdict = {}
get_src_crvs=[(each) for each in cmds.listRelatives(cmds.ls("feathers_sim")[0], ad=1, type="nurbsCurve") if "Orig" not in each]
for each in get_tgt_geo:
    get_num = re.findall(r'\d+', each)
    c'r_dict = {get_num:each}
    srcdict.update(c'r_dict)

    
def wire_wrap(srcdict, tgtdict):
    for key, driven in tgtdict:
        try:
            driven = srcdict.get(key)
        except:
            pass
        esCurveDeformer.bindWithUpObject(driven, driver, upObj='', name='', upType=1, upAxis='x', refMeshes=None, refCrv=None, refUpObj=None)
        #cmds.wire(driven, w=driver,n="{}_wr".format(driven), ex=1, ce=0.000000, li=0.000000, dds=[(0, 5)] )
        
wire_wrap(srcdict, tgtdict)


for key, value in collectmycurve_ct.items():
    for each_tgt in value:
        shapetgt=cmds.listRelatives(each_tgt, ad=1, type="nurbsCurve")[0]
        cmds.select(clear=1)
        cmds.select([each_tgt], r=1) 
        try:
            fnd=cmds.listConnections(shapetgt, s=1, type="wire")[0]
            if len(fnd)>0:
                fnd_crv=[(curve_item.split("Base")[0]) for curve_item in cmds.listConnections(fnd, p=1) if 'Base' in curve_item][0]
                fnd_point = fnd_crv+'.cv[0]'
                fnd_pos = cmds.pointPosition(fnd_point, w=1)
                sourcePoint = key+'.cv[0]'
                src_pos = cmds.pointPosition(sourcePoint, w=1)
                tgt_point = each_tgt+'.cv[0]'
                tgt_pos = cmds.pointPosition(tgt_point, w=1)                
                x_fnd_pos, y_fnd_pos, z_fnd_pos = tgt_pos[0]-fnd_pos[0], tgt_pos[1]-fnd_pos[1], tgt_pos[2]-fnd_pos[2]
                x_src_pos, y_src_pos, z_src_pos = tgt_pos[0]-src_pos[0], tgt_pos[1]-src_pos[1], tgt_pos[2]-src_pos[2]
                if x_fnd_pos > x_src_pos and y_fnd_pos > y_src_pos and z_fnd_pos>z_src_pos:
                    grabWire = cmds.wire(w=key,n=str(each_tgt)+"_wr", gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
                    cmds.setAttr(grabWire[0]+".rotation", 0)
                    cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[0]", v=0)
                    cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[1]", v=.25)
                    cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[2]", v=.5)
                    cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[3]", v=.75)          
        except:     
            grabWire = cmds.wire(w=key,n=str(each_tgt)+"_wr", gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
            cmds.setAttr(grabWire[0]+".rotation", 0)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[0]", v=0)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[1]", v=.25)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[2]", v=.5)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[3]", v=.75)getsrcObj=cmds.listRelatives(cmds.ls(sl=1)[0], ad=1, type="transform")
targetSelection_crvs=cmds.listRelatives(cmds.ls(sl=1)[1], ad=1, type="transform")
dropoff = .006
collectmycurve_ct={}
for each_src in getsrcObj:
    collectmycurve = []
    sourcePoint = each_src+'.cv[0]'
    pos = cmds.pointPosition(sourcePoint, w=1)
    x_pos_min, x_pos_max, y_pos_min, y_pos_max, z_pos_min, z_pos_max = pos[0]-dropoff, pos[0]+dropoff, pos[1]-dropoff, pos[1]+dropoff, pos[2]-dropoff, pos[2]+dropoff 
    for each_tgt_crv  in targetSelection_crvs:
        tgt_sourcePoint = each_tgt_crv+'.cv[0]'
        tgt_pos = cmds.pointPosition(tgt_sourcePoint, w=1) 
        if tgt_pos[0] >= x_pos_min and tgt_pos[0] <= x_pos_max and tgt_pos[1] >= y_pos_min and tgt_pos[1] <= y_pos_max and tgt_pos[2] >= z_pos_min and tgt_pos[2] <= z_pos_max:
            collectmycurve.append(each_tgt_crv)
    newdict = {each_src:collectmycurve}
    collectmycurve_ct.update(newdict) 
for key, value in collectmycurve_ct.items():
    for each_tgt in value:
        shapetgt=cmds.listRelatives(each_tgt, ad=1, type="nurbsCurve")[0]
        cmds.select(clear=1)
        cmds.select([each_tgt], r=1) 
        try:
            fnd=cmds.listConnections(shapetgt, s=1, type="wire")[0]
            if len(fnd)>0:
                fnd_crv=[(curve_item.split("Base")[0]) for curve_item in cmds.listConnections(fnd, p=1) if 'Base' in curve_item][0]
                fnd_point = fnd_crv+'.cv[0]'
                fnd_pos = cmds.pointPosition(fnd_point, w=1)
                sourcePoint = key+'.cv[0]'
                src_pos = cmds.pointPosition(sourcePoint, w=1)
                tgt_point = each_tgt+'.cv[0]'
                tgt_pos = cmds.pointPosition(tgt_point, w=1)                
                x_fnd_pos, y_fnd_pos, z_fnd_pos = abs(tgt_pos[0]-fnd_pos[0]), abs(tgt_pos[1]-fnd_pos[1]), abs(tgt_pos[2]-fnd_pos[2])
                x_src_pos, y_src_pos, z_src_pos = abs(tgt_pos[0]-src_pos[0]), abs(tgt_pos[1]-src_pos[1]), abs(tgt_pos[2]-src_pos[2])
                if x_fnd_pos > x_src_pos and y_fnd_pos > y_src_pos and z_fnd_pos>z_src_pos:
                    cmds.delete(fnd)
                    grabWire = cmds.wire(w=key,n=str(each_tgt)+"_wr", gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
                    cmds.setAttr(grabWire[0]+".rotation", 0)
                    cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[0]", v=0)
                    cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[1]", v=.25)
                    cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[2]", v=.5)
                    cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[3]", v=.75)                    
        except:     
            grabWire = cmds.wire(w=key,n=str(each_tgt)+"_wr", gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
            cmds.setAttr(grabWire[0]+".rotation", 0)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[0]", v=0)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[1]", v=.25)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[2]", v=.5)
            cmds.percent(str(each_tgt)+"_wr", str(each_tgt)+".cv[3]", v=.75)
get_src_crvs=[(each) for each in cmds.listRelatives(cmds.ls(sl=1)[0], ad=1, type="nurbsCurve") if cmds.arclen(each) > .008]
cmds.select (get_src_crvs, r=1)


@P *= (1-@opinput1_blendPaint * ch(&quot;intensity&quot;));
@P += (@opinput1_P * @opinput1_blendPaint * ch("intensity"));



@P *= (1-@opinput1_blendPaint * ch("intensity"));
@P += (@opinput1_P * @opinput1_blendPaint * ch("intensity"));


for collide_mesh in cmds.ls(sl=1):
    pdt.PostDeformToolset().createPeakDeformer([collide_mesh], defName = collide_mesh, distance = 0.000000, )
    cmds.setAttr(collide_mesh+'_peak.distance', -.011 )



sel_NumMn=cmds.playbackOptions(q=1, min=1)
sel_NumMn_reset=cmds.playbackOptions(q=1, min=1)+1
cmds.currentTime(sel_NumMn)
cmds.currentTime(sel_NumMn_reset)
cmds.currentTime(sel_NumMn)



arclen_limit = .008
getsrcObj = [(each) for each in cmds.listRelatives(cmds.ls(sl=1)[0], ad=1, type="nurbsCurve")  if cmds.arclen(each) < arclen_limit]
cmds.select(getsrcObj, r=1)
        #glue the collider culled mesh to the body
        command='pointGlue -s "%s" -t "%s" -max %f' % ("c_body_mid_tech_geo", "c_body_collide'r_pg_tech_geo", .001)
        mm.eval(command)
        pgnode = [(item) for item in cmds.listHistory("c_body_collide'r_pg_tech_geoShape", f=0, ac=1) if cmds.nodeType(item) == "pointGlue"][0]
        cmds.rename(pgnode, "c_body_mid_tech_geo_pg")
        self.wrapDeformer("c_body_collide'r_wrp_tech_geo", "c_body_mid_tech_geo")
        select_objects = ('c_body_collide'r_mid_coll_geo','c_body_collide'r_wrp_tech_geo','c_body_collide'r_pg_tech_geo')
        self.pointGlue_one_to_mass(select_objects)
        #drive the snake's body collider with dress body collider(crossover nucleus trick)
        cmds.connectAttr("c_body_collide'r_mid_coll_geoShape.outMesh", "c_body_snk_collide'r_mid_coll_geoShape.inMesh", f=1)

        #plug the snake anim to drive the driver in tech layer
        self.wrapDeformer("c_btm_mesh_simCage_geo_tech_geo", "c_btm_mesh_mid_tech_geo")
        self.wrapDeformer("c_metalBody_simCage_geo_tech_geo", "c_metalBody_mid_tech_geo")
        self.wrapDeformer("c_snakeHead_simCage_geo_tech_geo", "c_snakeHead_mid_tech_geo")
        self.wrapDeformer("c_tp_mesh_simCage_geo_tech_geo", "c_tp_mesh_mid_tech_geo")
        self.wrapDeformer("c_btm_tailMesh_simCage_geo_tech_geo", "c_btm_tailMesh_mid_tech_geo")

        #pointglueing the driver whole to the pieces to pick up the animation
        select_objects = ('c_snake_simCage_drive'r_tech_geo',
            'c_btm_mesh_simCage_geo_tech_geo',
            'c_metalBody_simCage_geo_tech_geo',
            'c_snakeHead_simCage_geo_tech_geo',
            'c_tp_mesh_simCage_geo_tech_geo',
            'c_btm_tailMesh_simCage_geo_tech_geo')
        self.pointGlue_one_to_mass(select_objects)

        #wrap the snake tetmesh onto anim input driver (for input attract) 
        self.wrapDeformer("c_snake_tetgen_tech_geo", "c_snake_simCage_drive'r_tech_geo")


        #glue the collider culled mesh to the body
        command='pointGlue -s "%s" -t "%s" -max %f' % ("c_body_mid_preTech_geo", "c_body_collide'r_pg_preTech_geo", .001)
        mm.eval(command)
        pgnode = [(item) for item in cmds.listHistory("c_body_collide'r_pg_preTech_geoShape", f=0, ac=1) if cmds.nodeType(item) == "pointGlue"][0]
        cmds.rename(pgnode, "c_body_mid_preTech_geo_pg")
        self.wrapDeformer("c_body_collide'r_wrp_preTech_geo", "c_body_mid_preTech_geo")
        select_objects = ('c_body_collide'r_mid_coll_geo','c_body_collide'r_wrp_preTech_geo','c_body_collide'r_pg_preTech_geo')
        self.pointGlue_one_to_mass(select_objects)
        #drive the snake's body collider with dress body collider(crossover nucleus trick)
        cmds.connectAttr("c_body_collide'r_mid_coll_geoShape.outMesh", "c_body_snk_collide'r_mid_coll_geoShape.inMesh", f=1)

        #plug the snake anim to drive the driver in tech layer
        self.wrapDeformer("c_btm_mesh_simCage_geo_preTech_geo", "c_btm_mesh_mid_preTech_geo")
        self.wrapDeformer("c_metalBody_simCage_geo_preTech_geo", "c_metalBody_mid_preTech_geo")
        self.wrapDeformer("c_snakeHead_simCage_geo_preTech_geo", "c_snakeHead_mid_preTech_geo")
        self.wrapDeformer("c_tp_mesh_simCage_geo_preTech_geo", "c_tp_mesh_mid_preTech_geo")
        self.wrapDeformer("c_btm_tailMesh_simCage_geo_preTech_geo", "c_btm_tailMesh_mid_preTech_geo")

        #pointglueing the driver whole to the pieces to pick up the animation
        select_objects = ('c_snake_simCage_drive'r_preTech_geo',
            'c_btm_mesh_simCage_geo_preTech_geo',
            'c_metalBody_simCage_geo_preTech_geo',
            'c_snakeHead_simCage_geo_preTech_geo',
            'c_tp_mesh_simCage_geo_preTech_geo',
            'c_btm_tailMesh_simCage_geo_preTech_geo')
        self.pointGlue_one_to_mass(select_objects)

        #wrap the snake tetmesh onto anim input driver (for input attract) 
        self.wrapDeformer("c_snake_tetgen_preTech_geo", "c_snake_simCage_drive'r_preTech_geo")cmds.cluster(n="scalp_scale")

cmds.cluster('preTech', )

cmds.setAttr("scalp_scaleHandle.sx", .05)
cmds.setAttr("scalp_scaleHandle.sy", .05)
cmds.setAttr("scalp_scaleHandle.sz", .05)

import xgenm as xg
import xgenm.xgGlobal as xgg
from maya_groom_tools.hai'r_tools.xgen_tools.xg_fx import xg_guideAnim
incl = ["head", "body"]
if xgg.Maya:
    #palette is collection, use palettes to get collections first.
    palettes = xg.palettes()
    for palette in palettes: 
        sel_instance = palette.split(":")[0]
        sel_palette = palette.split(":")[-1]
        #Use descriptions to get description of each collection
        descriptions = [(each) for each in xg.descriptions(palette) for item in incl if item in each if "short" not in each]
        for description in descriptions: 
            sel_description = description.split(':')[-1]
            guideAnim = xg_guideAnim.xgenGuideAnim(palette, description)
            guideAnim.wires = guideAnim.getWireNames()
            print 'attached wires: ', guideAnim.wires
            guideAnim.wireGrp = '{}_mid_Main1:{}_{}_mid_postTech_grp'.format(sel_instance, sel_palette, sel_description)
            guideAnim.attachWireGrp()
            print 'attached wires: ', guideAnim.wires
from maya_groom_tools.hai'r_tools.xgen_tools.xg_fx import xg_guideAnim
incl = ["head", "body"]

if xgg.Maya:
    #palette is collection, use palettes to get collections first.
    palettes = xg.palettes()
    for palette in palettes: 
        #Use descriptions to get description of each collection
        descriptions = [(each) for each in xg.descriptions(palette) for item in incl if item in each]
        for description in descriptions:
            print description
            guideAnim = xg_guideAnim.xgenGuideAnim(palette, description)
            guideAnim.wires = guideAnim.getWireNames()
            print 'attached wires: ', guideAnim.wires
            guideAnim.wireGrp = '{}_mid_Main1:{}_{}_mid_postTech_grp'.format(palette.split(":")[0], (palette.split(":")[-1], description)
            guideAnim.attachWireGrp()
            print 'attached wires: ', guideAnim.wires

guideAnim = xg_guideAnim.xgenGuideAnim('practicalMouse1:BodyColl', 'practicalMouse1:bodyFur')
guideAnim.wires = guideAnim.getWireNames()
print 'attached wires: ', guideAnim.wires
guideAnim.wireGrp = 'practicalMouse1_mid_Main1:BodyColl_bodyFu'r_mid_postTech_grp'
guideAnim.attachWireGrp()
print 'attached wires: ', guideAnim.wires
import xgenm as xg
import xgenm.xgGlobal as xgg
from maya_groom_tools.hai'r_tools.xgen_tools.xg_fx import xg_guideAnim
incl = ["head", "body"]
if xgg.Maya:
    #palette is collection, use palettes to get collections first.
    palettes = xg.palettes()
    for palette in palettes: 
        sel_instance = palette.split(":")[0]
        sel_palette = palette.split(":")[-1]
        #Use descriptions to get description of each collection
        descriptions = [(each) for each in xg.descriptions(palette) for item in incl if item in each if "short" not in each]
        for description in descriptions: 
            objects = xg.objects(palette, description, True)
            #Get active objects,e.g. SplinePrimtives
            for object in objects:
                attrs = xg.allAttrs(palette, description, object)
                print attrs

liveMode
            sel_description = description.split(':')[-1]
            guideAnim = xg_guideAnim.xgenGuideAnim(palette, description)
            guideAnim.wires = guideAnim.getWireNames()
            print 'attached wires: ', guideAnim.wires
            guideAnim.wireGrp = '{}_mid_Main1:{}_{}_mid_postTech_grp'.format(sel_instance, sel_palette, sel_description)
            guideAnim.attachWireGrp()
            print 'attached wires: ', guideAnim.wires
import xgenm as xg
import xgenm.xgGlobal as xgg
from maya_groom_tools.hai'r_tools.xgen_tools.xg_fx import xg_guideAnim
incl = ["head", "body"]
if xgg.Maya:
    #palette is collection, use palettes to get collections first.
    palettes = xg.palettes()
    for palette in palettes: 
        sel_instance = palette.split(":")[0]
        sel_palette = palette.split(":")[-1]
        #Use descriptions to get description of each collection
        descriptions = [(each) for each in xg.descriptions(palette) for item in incl if item in each if "short" not in each]
        for description in descriptions: 
            objects = xg.objects(palette, description, True)
            #Get active objects,e.g. SplinePrimtives
            for object in objects:
                attrs = xg.allAttrs(palette, description, object)
                for attributes in attrs:
                    if "useCache" == attributes:
                        print xg.getAttr(attributes, palette, description, object)

import xgenm as xg
import xgenm.xgGlobal as xgg
from maya_groom_tools.hai'r_tools.xgen_tools.xg_fx import xg_guideAnim
incl = ["head", "body"]
if xgg.Maya:
    #palette is collection, use palettes to get collections first.
    palettes = xg.palettes()
    for palette in palettes: 
        sel_instance = palette.split(":")[0]
        sel_palette = palette.split(":")[-1]
        #Use descriptions to get description of each collection
        descriptions = [(each) for each in xg.descriptions(palette) for item in incl if item in each if "short" not in each]
        for description in descriptions: 
            objects = xg.objects(palette, description, True)
            #Get active objects,e.g. SplinePrimtives
            for object in objects:
                attrs = xg.allAttrs(palette, description, object)
                for attributes in attrs:
                    if "useCache" == attributes:
                        if xg.getAttr(attributes, palette, description, object) == False:
                            sel_description = description.split(':')[-1]
                            guideAnim = xg_guideAnim.xgenGuideAnim(palette, description)
                            guideAnim.wires = guideAnim.getWireNames()
                            print 'attached wires: ', guideAnim.wires
                            guideAnim.wireGrp = '{}_mid_Main1:{}_{}_mid_postTech_grp'.format(sel_instance, sel_palette, sel_description)
                            guideAnim.attachWireGrp()
                            print 'attached wires: ', guideAnim.wires
                    if "liveMode" == attributes:                            
                        if xg.getAttr(attributes, palette, description, object) == False:
                            sel_description = description.split(':')[-1]
                            guideAnim = xg_guideAnim.xgenGuideAnim(palette, description)
                            guideAnim.wires = guideAnim.getWireNames()
                            print 'attached wires: ', guideAnim.wires

                    if "liveMode" == attributes:
                        print xg.setAttr(attributes, False, palette, description, object)                        

import xgenm as xg
import xgenm.xgGlobal as xgg
from maya_groom_tools.hai'r_tools.xgen_tools.xg_fx import xg_guideAnim
incl = ["head", "body"]
if xgg.Maya:
    #palette is collection, use palettes to get collections first.
    palettes = xg.palettes()
    for palette in palettes: 
        sel_instance = palette.split(":")[0]
        sel_palette = palette.split(":")[-1]
        #Use descriptions to get description of each collection
        descriptions = [(each) for each in xg.descriptions(palette) for item in incl if item in each if "short" not in each]
        for description in descriptions: 
            objects = xg.objects(palette, description, True)
            #Get active objects,e.g. SplinePrimtives
            for object in objects:
                attrs = xg.allAttrs(palette, description, object)
                for attributes in attrs:
                    if "useCache" == attributes:
                        print xg.getAttr(attributes, palette, description, object)
                        if xg.getAttr(attributes, palette, description, object) == False:
                            print "yo"
                            sel_description = description.split(':')[-1]
                            guideAnim = xg_guideAnim.xgenGuideAnim(palette, description)
                            guideAnim.wires = guideAnim.getWireNames()
                            print 'attached wires: ', guideAnim.wires
                            guideAnim.wireGrp = '{}_mid_Main1:{}_{}_mid_postTech_grp'.format(sel_instance, sel_palette, sel_description)
                            guideAnim.attachWireGrp()
                            print 'attached wires: ', guideAnim.wires
                    if "liveMode" == attributes:                            
                        if xg.getAttr(attributes, palette, description, object) == False:
                            sel_description = description.split(':')[-1]
                            guideAnim = xg_guideAnim.xgenGuideAnim(palette, description)
                            guideAnim.wires = guideAnim.getWireNames()
                            print 'attached wires: ', guideAnim.wires
                            guideAnim.wireGrp = '{}_mid_Main1:{}_{}_mid_postTech_grp'.format(sel_instance, sel_palette, sel_description)
                            guideAnim.attachWireGrp()
                            print 'attached wires: ', guideAnim.wires                        

nextList = []
nsize = 50
for each in getfulllist[::nsize]:
    nextList.append(each)



import maya.cmds as mc
getAnimGeo=cmds.ls("*:scalpMidBody")[0]
animRigNS=getAnimGeo.split(":")[0]
if cmds.objExists('{}*:techRig.follicle_scale'.format(animRigNS)) == False:
    cmds.addAttr('{}*:techRig'.format(animRigNS),ln ="follicle_scale",  at = 'float', dv = 1.0 )
    cmds.setAttr("{}*:techRig.follicle_scale".format(animRigNS), edit =True, channelBox = True)

sel_sim_foll_trsnfrm = [(each) for each in cmds.listRelatives(cmds.ls("{}*:*_input_grp".format(animRigNS)), c=1, type="transform")]

for each in sel_sim_foll_trsnfrm:
    cmds.connectAttr("{}*:techRig.follicle_scale".format(animRigNS), "{}.scaleX".format(each), f=1)
    cmds.connectAttr("{}*:techRig.follicle_scale".format(animRigNS), "{}.scaleY".format(each), f=1)
    cmds.connectAttr("{}*:techRig.follicle_scale".format(animRigNS), "{}.scaleZ".format(each), f=1)

sel_stc_foll_trsnfrm = [(each) for each in cmds.listRelatives(cmds.ls("{}*:*_static_tech_fol_grp".format(animRigNS)), c=1, type="transform")]

for each in sel_stc_foll_trsnfrm:
    cmds.connectAttr("{}*:techRig.follicle_scale".format(animRigNS), "{}.scaleX".format(each), f=1)
    cmds.connectAttr("{}*:techRig.follicle_scale".format(animRigNS), "{}.scaleY".format(each), f=1)
    cmds.connectAttr("{}*:techRig.follicle_scale".format(animRigNS), "{}.scaleZ".format(each), f=1)
gettime = cmds.getAttr(cmds.ls(type = 'time')[0]+'.outTime')
if gettime:
    try:
        cmds.setAttr(inst+'Tech:techRig.startFrame', gettime)
    except:
        pass
cmds.connectAttr("{}:scalpMidBody.scale".format(animRigNS), "{}_mid_Main:scalpMidBody_tech_geo.scale".format(animRigNS), f=1)
cmds.connectAttr("{}:scalpMidBody.scale".format(animRigNS), "{}_mid_Main:scalpMidBody_preTech_geo.scale".format(animRigNS), f=1)
cmds.connectAttr("{}:scalpMidBody.scale".format(animRigNS), "{}_mid_Main:scalpMidBody_scalp_geo.scale".format(animRigNS), f=1)
cmds.connectAttr("{}:scalpMidBody.scale".format(animRigNS), "{}_mid_Main:scalpMidBody_coll_geo.scale".format(animRigNS), f=1)
cmds.connectAttr("{}:scalpMidBody.scale".format(animRigNS), "{}_mid_Main:scalpMidBody_postTech_geo.scale".format(animRigNS), f=1) 

import os
import xgenm as xg
import xgenm.xgGlobal as xgg


#XGEN collection name
collection = "practicalMouse1:BodyColl"#xgen Collection name with name space will be furballTest1:headColl
  

gExpAttrType = "float"
gExpAttr     = gExpAttrType+"inheritsTransform"

xgExp = "$a=0.0600;#-1.0,1.0/n$a"
    
xg.setAttr(gExpAttr,str(xgExp),collection)
xgg.DescriptionEditor.refresh("Full")

import os
import xgenm as xg
import xgenm.xgGlobal as xgg


#this is example to create string can paste to xgen globalExpression attribute
import os
import xgenm as xg
import xgenm.xgGlobal as xgg
  

#=
#XGEN collection name
collection = "practicalMouse1:BodyColl"#xgen Collection name with name space will be furballTest1:headColl
  
#==
#create expression 
   
#you need to have prefix attribute type  custom_float_ and attribute name
gExpAttrType = "float_"
gExpAttr     = gExpAttrType+"gGroomScale"
#gExpAttr     = gExpAttrType+"cfx_growing"

    
xgExp= "$a=0.0500;#-1.0,1.0\\n"
xgExp += "$a"

    
xg.setAttr(gExpAttr,str(xgExp),collection)
xgg.DescriptionEditor.refresh("Full")
import xgenm as xg
import xgenm.xgGlobal as xgg
from maya_groom_tools.hai'r_tools.xgen_tools.xg_fx import xg_guideAnim
incl = ["head", "body"]

if xgg.Maya:
    #palette is collection, use palettes to get collections first.
    palettes = xg.palettes()
    for palette in palettes: 
        sel_instance = palette.split(":")[0]
        sel_palette = palette.split(":")[-1]
        #Use descriptions to get description of each collection
        descriptions = [(each) for each in xg.descriptions(palette) for item in incl if item in each if "short" not in each]
        for description in descriptions: 
            objects = xg.objects(palette, description, True)
            #Get active objects,e.g. SplinePrimtives
            for object in objects:
                attrs = xg.allAttrs(palette, description, object)
                for attributes in attrs:
                    if "liveMode" in attributes:
                        find_state = xg.getAttr(attributes, palette, description, object)   
                        if find_state == "false":
                            sel_description = description.split(':')[-1]
                            guideAnim = xg_guideAnim.xgenGuideAnim(palette, description)
                            guideAnim.wires = guideAnim.getWireNames()
                            print 'attached wires: ', guideAnim.wires
                            guideAnim.wireGrp = '{}_mid_Main1:{}_{}_mid_postTech_grp'.format(sel_instance, sel_palette, sel_description)
                            guideAnim.attachWireGrp()
                            print 'attached wires: ', guideAnim.wires
import xgenm as xg
import xgenm.xgGlobal as xgg
from maya_groom_tools.hai'r_tools.xgen_tools.xg_fx import xg_guideAnim
incl = ["head", "body"]
if xgg.Maya:
    #palette is collection, use palettes to get collections first.
    palettes = xg.palettes()
    for palette in palettes: 
        sel_instance = palette.split(":")[0]
        sel_palette = palette.split(":")[-1]
        #Use descriptions to get description of each collection
        descriptions = [(each) for each in xg.descriptions(palette) for item in incl if item in each if "short" not in each]
        for description in descriptions: 
            objects = xg.objects(palette, description, True)
            #Get active objects,e.g. SplinePrimtives
            for object in objects:
                attrs = xg.allAttrs(palette, description, object)
                for attributes in attrs:
                    print attributes, xg.getAttr(attributes, palette, description, object)

import xgenm as xg
import xgenm.xgGlobal as xgg
from maya_groom_tools.hai'r_tools.xgen_tools.xg_fx import xg_guideAnim
glob = {}
if xgg.Maya:
    #palette is collection, use palettes to get collections first.
    palettes = xg.palettes()
    for palette in palettes: 
        sel_instance = palette.split(":")[0]
        sel_palette = palette.split(":")[-1]
        #Use descriptions to get description of each collection
        descriptions = [(each) for each in xg.descriptions(palette)]
        for description in descriptions: 
            objects = xg.objects(palette, description, True)
            #Get active objects,e.g. SplinePrimtives
            for object in objects:
                attrs = xg.allAttrs(palette, description, object)
                for attributes in attrs:
                    newdict ={attributes: xg.getAttr(attributes, palette, description, object)}
                    glob.update(newdict)
for key in sorted(glob.keys()):
    if "$a" in glob.get(key):
        print key, glob.get(key)
#this is example to create string can paste to xgen globalExpression attribute
import os
import xgenm as xg
import xgenm.xgGlobal as xgg
  
#set XGEN_XGD global path env
#this is your local or published xgen delta file instance partent folder.
#for example I am using my local,
 
 
#=
#XGEN collection name
collection = "mouseBruno1:BodyColl"#xgen Collection name with name space will be furballTest1:headColl
  
#==
#create expression 
mapDir     = "/jobs/vfx_mice/dev/dev1010/TASKS/cfx/maya/images/checkergrowth/"
mapName    = "checker1_map_fo'r_grwth"
mapPath    = mapDir+mapName
   
#you need to have prefix attribute type  custom_float_ and attribute name
gExpAttrType = "float_"
gExpAttr     = gExpAttrType+"gGroomScale"

xgExp += "$a= 0.0800;#-1.0,1.0\\n"
xgExp += "$a"

xg.setAttr(gExpAttr,str(xgExp),collection)
xgg.DescriptionEditor.refresh("Full")


selfU=12
selfV=1     
cmds.group(n='whiske'r_rende'r_tubes',empty=True)
getParent = cmds.circle(c=(0, 0, 0), nr=(0, 1, 0), n="whiske'r_root_nrbs", sw=360, r=0.0015, d=3, ut=0, tol=0.01, s=8, ch=1)[0]
cmds.parent(getParent, "whiske'r_rende'r_tubes")
cmds.setAttr("whiske'r_root_nrbs.visibility", 0)
cmds.nurbsToPolygonsPref(un=selfU, vn=selfV)
profile_obj=cmds.ls('?_whisker?_????_mid')
gettgtObj = [(each) for each in cmds.listRelatives(profile_obj, ad=1, type="nurbsCurve")]
for each in gettgtObj: 
    cmds.extrude(getParent, each, n=each+"_renderTube_geo",  ch=1, rn=0, po=1, et=2, ucp=1, fpt=1, upn=1, rsp=1, rotation=0, scale=1)
    cmds.parent(each+"_renderTube_geo", "whiske'r_rende'r_tubes")
res = [int(i) for i in test_string.split() if i.isdigit()]




import esCurveDeformer
get_tgt_geo=sorted([(each) for each in cmds.listRelatives(cmds.ls("c_featherSystem_mid_postTech_geo_separated")[0], ad=1, type="mesh") if "Orig" not in each])
get_src_crvs=[(each) for each in cmds.listRelatives(cmds.ls("feathers_sim")[0], ad=1, type="nurbsCurve") if "Orig" not in each]

def wire_wrap(get_src_crvs, get_tgt_geo):
    for driven in get_tgt_geo:
        for driver in get_src_crvs:
            if driven != None:
                if driver in driven:
                    esCurveDeformer.bindWithUpObject(driven, driver, upObj='', name='', upType=1, upAxis='x', refMeshes=None, refCrv=None, refUpObj=None)
                    #cmds.wire(driven, w=driver,n="{}_wr".format(driven), ex=1, ce=0.000000, li=0.000000, dds=[(0, 5)] )
        
wire_wrap(get_src_crvs, get_tgt_geo)



import esCurveDeformer
get_tgt_geo=sorted([(each) for each in cmds.listRelatives(cmds.ls("c_featherSystem_mid_postTech_geo_separated")[0], ad=1, type="mesh") if "Orig" not in each])
get_src_crvs=[(each) for each in cmds.listRelatives(cmds.ls("feathers_sim")[0], ad=1, type="nurbsCurve") if "Orig" not in each]



def wire_wrap(get_src_crvs, get_tgt_geo):
    for driven in get_tgt_geo:
        for driver in get_src_crvs:
            if driven != None:
                if driver in driven:
                    esCurveDeformer.bindWithUpObject(driven, driver, upObj='', name='', upType=1, upAxis='x', refMeshes=None, refCrv=None, refUpObj=None)
                    #cmds.wire(driven, w=driver,n="{}_wr".format(driven), ex=1, ce=0.000000, li=0.000000, dds=[(0, 5)] )
        
wire_wrap(get_src_crvs, get_tgt_geo)

if len(cmds.ls(sl = 1))<1:
    get_hr = cmds.ls('*Tech:whiskersHairSysShape')[0]
    get_techrig = cmds.ls("*:techRig")[0]
else:
    get_select = [(each) for each in cmds.ls(sl=1) if 'Tech' in each]
    get_hr = "{}:whiskersHairSysShape".format(get_select[0].split(':')[0])
    get_techrig = "{}:techRig".format(get_select[0].split(':')[0])
print get_hr, get_techrig

stiffer = {
"{}.stiffness".format(get_hr):5,
"{}.extraBendLinks".format(get_hr): 2,
"{}.bendResistance".format(get_hr): 50,
"{}.startCurveAttract".format(get_hr): 1,
"{}.damp".format(get_hr): 1,
"{}.whskrs_bc_strt_pos".format(get_techrig): 0.1,
"{}.whskrs_bc_strt_val".format(get_techrig): 0.0,
"{}.whskrs_bc_end_pos".format(get_techrig): 0.35,
"{}.whskrs_bc_end_val".format(get_techrig): 1.0}
for key, value in stiffer.items():
    pre_val = cmds.getAttr(key)
    print 'setting {} {} to {}'.format(key, pre_val, str(value))
    cmds.setAttr(key, value)

jobNums = [127, 128, 129, 130, 131, 134]
for job_item in jobNums:
    try:
        cmds.scriptJob(kill=job_item, force=True)
    except:
        pass
import maya.cmds as mc
for editor in cmds.lsUI(editors=True):
    if not cmds.outlinerEditor(editor, query=True, exists=True):
        continue
    sel_cmd = cmds.outlinerEditor(editor, query=True, selectCommand=True)
    if not sel_cmd or not sel_cmd.startswith('<function selCom at '):
        continue
    cmds.outlinerEditor(editor, edit=True, selectCommand='print("")')





import maya.cmds as mc

import showUtils
reload(showUtils)
groomType = 'rman_xgen'
variant = 'Main'
lod = 'mid'
job = 'vfx_mice'
sequence = 'assets'
shot = 'char.practicalMouse'
task = 'model'
showUtils.importLatestGroomGuides(job, sequence, shot, lod, task, variant, groomType)
import maya.cmds as mc
import assetLib
import mWeights
lods = ['mid']
assetFiles = assetLib.getModel(show='vfx_mice',
                               assetType='char',
                               asset='practicalMouse',
                               lods=lods,
                               versionType='mb',
                               context='PRODUCTS',
                               mode="import",
                               namespace=None,
                               assignShaders=True,
                               resetPivots=False,
                               verbose=True)
cmds.select(['c_body_mid.e[34585]', 'c_body_mid.e[34225]'], r=1)
maya.mel.eval("ConvertSelectionToVertices;")
def median_find(lst):
    even = (0 if len(lst) % 2 else 1) + 1
    half = (len(lst) - 1) / 2
    mysum= sum(sorted(lst)[half:half + even]) / float(even)
    return mysum
selObj=cmds.ls(sl=1, fl=1)
transform=cmds.xform(selObj, q=1, bb=1)
posBucketx=median_find(transform[0::3])
posBuckety=median_find(transform[1::3])
posBucketz=median_find(transform[2::3])
getLoc=cmds.spaceLocator()
cmds.xform(getLoc[0], t=(posBucketx, posBuckety, posBucketz))
cmds.duplicate(getLoc[0], n="internal_rot")
cmds.parent("internal_rot", getLoc[0])
cmds.parent('c_body_mid', "internal_rot")
cmds.select(['practicalMouse1Tech:c_body_mid_postTech_geo.e[34585]', 'practicalMouse1Tech:c_body_mid_postTech_geo.e[34225]'], r=1)
maya.mel.eval("rivet;")
getPa'r_Loc = cmds.ls(sl=1)[0]'
cmds.parentConstraint(getPa'r_Loc, getLoc[0], mo=0)'
# cmds.xform("internal_rot", os=1, ro=[70,0,180] )
cmds.blendShape('c_body_mid', 'practicalMouse1Tech:c_body_mid_postTech_geo', n = "tail_blend_bsp", w=(0, 1.0))
userScriptDir = os.path.join(os.path.dirname("//jobs/vfx_mice/COMMON/rig/users/deglaue/maps/blendShapes"), 'blendShape')
bs="tail_blend_bsp"
mWeights.load(bs, filePath=os.path.join(userScriptDir, '%s.wts' % bs))

import maya.cmds as mc
import assetLib
import mWeights
if "practical" in cmds.ls(sl=1)[0]:
    lods = ['mid']
    assetFiles = assetLib.getModel(show='vfx_mice',
                                   assetType='char',
                                   asset='practicalMouse',
                                   lods=lods,
                                   versionType='mb',
                                   context='PRODUCTS',
                                   mode="import",
                                   namespace=None,
                                   assignShaders=True,
                                   resetPivots=False,
                                   verbose=True)
    cmds.select(['c_body_mid.e[34585]', 'c_body_mid.e[34225]'], r=1)
    maya.mel.eval("ConvertSelectionToVertices;")
    def median_find(lst):
        even = (0 if len(lst) % 2 else 1) + 1
        half = (len(lst) - 1) / 2
        mysum= sum(sorted(lst)[half:half + even]) / float(even)
        return mysum
    selObj=cmds.ls(sl=1, fl=1)
    transform=cmds.xform(selObj, q=1, bb=1)
    posBucketx=median_find(transform[0::3])
    posBuckety=median_find(transform[1::3])
    posBucketz=median_find(transform[2::3])
    getLoc=cmds.spaceLocator()
    cmds.xform(getLoc[0], t=(posBucketx, posBuckety, posBucketz))
    cmds.duplicate(getLoc[0], n="internal_rot")
    cmds.parent("internal_rot", getLoc[0])
    cmds.parent('c_body_mid', "internal_rot")
    #cmds.select(['practicalMouse1Tech:c_body_mid_postTech_geo.e[34585]', 'practicalMouse1Tech:c_body_mid_postTech_geo.e[34225]'], r=1)
    #maya.mel.eval("rivet;")
    #cmds.select(['practicalMouse1Tech:c_skeleton_tech_mid_preTech_geo.e[3177]', 'practicalMouse1Tech:c_skeleton_tech_mid_preTech_geo.e[3131]'], r=1)
    #maya.mel.eval("rivet;")
    getPa'r_Loc = cmds.ls("practicalMouse1:c_spine_pelvis_out_srt")[0]'
    cmds.parentConstraint(getPa'r_Loc, getLoc[0], mo=0)'
    # cmds.xform("internal_rot", os=1, ro=[70,0,180] )
    cmds.blendShape('c_body_mid', 'practicalMouse1Tech:c_body_mid_preTech_geo', o = "world",  n = "tail_blend_bsp", w=(0, 1.0))
    userScriptDir = os.path.join(os.path.dirname("//jobs/vfx_mice/COMMON/rig/users/deglaue/maps/blendShapes"), 'blendShape')
    bs="tail_blend_bsp"
    mWeights.load(bs, filePath=os.path.join(userScriptDir, '%s.wts' % bs))
    cmds.setAttr("{}."format(getLoc[0]), 0)
import maya.cmds as mc
import assetLib
import mWeights
if "practical" in cmds.ls(sl=1)[0]:
    cmds.file(('/jobs/vfx_mice/COMMON/rig/users/deglaue/data/standing_051_010.mb'), mnp=1, i=1)
    cmds.select(['c_body_mid_fix_bipedal_tail_geo.e[34585]', 'c_body_mid_fix_bipedal_tail_geo.e[34225]'], r=1)
    maya.mel.eval("ConvertSelectionToVertices;")
    def median_find(lst):
        even = (0 if len(lst) % 2 else 1) + 1
        half = (len(lst) - 1) / 2
        mysum= sum(sorted(lst)[half:half + even]) / float(even)
        return mysum
    selObj=cmds.ls(sl=1, fl=1)
    transform=cmds.xform(selObj, q=1, bb=1)
    posBucketx=median_find(transform[0::3])
    posBuckety=median_find(transform[1::3])
    posBucketz=median_find(transform[2::3])
    getLoc=cmds.spaceLocator()
    cmds.xform(getLoc[0], t=(posBucketx, posBuckety, posBucketz))
    cmds.duplicate(getLoc[0], n="internal_rot")
    cmds.parent("internal_rot", getLoc[0])
    cmds.parent('c_body_mid_fix_bipedal_tail_geo', "internal_rot")
    getPa'r_Loc = cmds.ls("practicalMouse1:c_spine_pelvis_out_srt")[0]'
    cmds.parentConstraint(getPa'r_Loc, getLoc[0], mo=0)'
    cmds.blendShape('c_body_mid_fix_bipedal_tail_geo', 'practicalMouse1Tech:c_body_mid_preTech_geo', o = "world",  n = "tail_blend_bsp", w=(0, 1.0))
    userScriptDir = os.path.join(os.path.dirname("//jobs/vfx_mice/COMMON/rig/users/deglaue/maps/blendShapes"), 'blendShape')
    bs="tail_blend_bsp"
    mWeights.load(bs, filePath=os.path.join(userScriptDir, '%s.wts' % bs))
    cmds.setAttr("{}.visibility".format(getLoc[0]), 0)
import maya.cmds as mc
import assetLib
import mWeights
if "practical" in cmds.ls(sl=1)[0]:
    cmds.file(('/jobs/vfx_mice/COMMON/rig/users/deglaue/data/standing_051_010.mb'), mnp=1, i=1)
    cmds.select(['c_body_mid_fix_bipedal_tail_geo.e[34585]', 'c_body_mid_fix_bipedal_tail_geo.e[34225]'], r=1)
    maya.mel.eval("ConvertSelectionToVertices;")
    def median_find(lst):
        even = (0 if len(lst) % 2 else 1) + 1
        half = (len(lst) - 1) / 2
        mysum= sum(sorted(lst)[half:half + even]) / float(even)
        return mysum
    selObj=cmds.ls(sl=1, fl=1)
    transform=cmds.xform(selObj, q=1, bb=1)
    posBucketx=median_find(transform[0::3])
    posBuckety=median_find(transform[1::3])
    posBucketz=median_find(transform[2::3])
    getLoc=cmds.spaceLocator()
    cmds.xform(getLoc[0], t=(posBucketx, posBuckety, posBucketz))
    cmds.duplicate(getLoc[0], n="internal_rot")
    cmds.parent("internal_rot", getLoc[0])
    cmds.parent('c_body_mid_fix_bipedal_tail_geo', "internal_rot")
    getPa'r_Loc = cmds.ls("practicalMouse1:c_spine_pelvis_out_srt")[0]'
    cmds.parentConstraint(getPa'r_Loc, getLoc[0], mo=0)'
    cmds.xform("internal_rot", os=1, ro=[83.057,31.535,80.116] )
    cmds.blendShape('c_body_mid_fix_bipedal_tail_geo', 'practicalMouse1Tech:c_body_mid_preTech_geo', o = "world",  n = "tail_blend_biped_bsp", w=(0, 1.0))
    userScriptDir = os.path.join(os.path.dirname("//jobs/vfx_mice/COMMON/rig/users/deglaue/maps/blendShapes"), 'blendShape')
    bs="tail_blend_biped_bsp"
    mWeights.load(bs, filePath=os.path.join(userScriptDir, '%s.wts' % bs))
    cmds.setAttr("{}.visibility".format(getLoc[0]), 0)
import maya.cmds as mc
import assetLib
import mWeights
if "practical" in cmds.ls(sl=1)[0]:
    mouseName = "practicalMouse"
if "boy" in cmds.ls(sl=1)[0]:
    mouseName = "mouseBoy"
cmds.file(('/jobs/vfx_mice/COMMON/rig/users/deglaue/data/standing_051_010.mb'), mnp=1, i=1)
cmds.select(['c_body_mid_fix_bipedal_tail_geo.e[34585]', 'c_body_mid_fix_bipedal_tail_geo.e[34225]'], r=1)
maya.mel.eval("ConvertSelectionToVertices;")
def median_find(lst):
    even = (0 if len(lst) % 2 else 1) + 1
    half = (len(lst) - 1) / 2
    mysum= sum(sorted(lst)[half:half + even]) / float(even)
    return mysum
selObj=cmds.ls(sl=1, fl=1)
transform=cmds.xform(selObj, q=1, bb=1)
posBucketx=median_find(transform[0::3])
posBuckety=median_find(transform[1::3])
posBucketz=median_find(transform[2::3])
getLoc=cmds.spaceLocator()
cmds.xform(getLoc[0], t=(posBucketx, posBuckety, posBucketz))
cmds.duplicate(getLoc[0], n="internal_rot")
cmds.parent("internal_rot", getLoc[0])
cmds.parent('c_body_mid_fix_bipedal_tail_geo', "internal_rot")
getPa'r_Loc = cmds.ls("{}1:c_spine_pelvis_out_srt".format(mouseName))[0]'
cmds.parentConstraint(getPa'r_Loc, getLoc[0], mo=0)'
cmds.xform("internal_rot", os=1, ro=[83.057,31.535,80.116] )
cmds.blendShape('c_body_mid_fix_bipedal_tail_geo', '{}1Tech:c_body_mid_preTech_geo'.format(mouseName), o = "world",  n = "tail_blend_biped_bsp", w=(0, 1.0))
userScriptDir = os.path.join(os.path.dirname("//jobs/vfx_mice/COMMON/rig/users/deglaue/maps/blendShapes"), 'blendShape')
bs="tail_blend_biped_bsp"
mWeights.load(bs, filePath=os.path.join(userScriptDir, '%s.wts' % bs))
cmds.setAttr("{}.visibility".format(getLoc[0]), 0)

for each in cmds.ls("zelda_diningRoom1_48fpsTech:featherHairSystem_to_postTech_*_BC.blend[0]"):
    cmds.setAttr("{}.blend_FloatValue".format(each), 0)


for each in cmds.ls("zelda_diningRoom1_48fpsTech:featherHairSystem_to_sim_*_BC.blend[0]"):
    cmds.setAttr("{}.blend_FloatValue".format(each), 1)
for each in cmds.ls("zelda_diningRoom1_48fpsTech:featherHairSystem_to_sim_*_BC.blend[1]"):
    cmds.setAttr("{}.blend_FloatValue".format(each),1)



for each in cmds.ls("zelda_diningRoom1_48fpsTech:featherHairSystem_to_sim_*_BC.blend[0]"):
    cmds.setAttr("{}.blend_FloatValue".format(each), 0)
for each in cmds.ls("zelda_diningRoom1_48fpsTech:featherHairSystem_to_sim_*_BC.blend[1]"):
    cmds.setAttr("{}.blend_FloatValue".format(each),0)

remove all blends from input

for each in cmds.ls(sl=1):
    cmds.setAttr("{}.simulationMethod".format(each), 1)



arclen_limit = .0067
getsrcObj = [(cmds.listRelatives(each, p=1, type="transform")[0]) for each in cmds.listRelatives(cmds.ls(sl=1)[0], ad=1, type="nurbsCurve")  if cmds.arclen(each) > arclen_limit]
cmds.select(getsrcObj, r=1)

getsrcObj = [(each) for each in cmds.listRelatives(cmds.ls(sl=1)[0], ad=1, type="follicle")]
cmds.select(getsrcObj, r=1)



muzzleFu'r_simCurves_input_grp'

getsrcObj_p = [(cmds.listRelatives(each, p=1, type="transform")[0]) for each in cmds.listRelatives(cmds.ls(sl=1)[0], ad=1, type="nurbsCurve")]
print getsrcObj_p
getsrcObj_c = [(cmds.listRelatives(each, p=1, type="transform")[0]) for each in cmds.listRelatives(cmds.ls(sl=1)[1], ad=1, type="nurbsCurve")]
print getsrcObj_c
for parent_item, child_item in map(None, getsrcObj_p, getsrcObj_c):
    try:
        cmds.blendShape(parent_item, child_item, n = "{}_bsp".format(child_item),o="world", w=(0, 1.0))
    except:
        pass

getdrvObj = [(cmds.listRelatives(each, p=1, type="transform")[0]) for each in cmds.listRelatives(cmds.ls(sl=1)[0], ad=1, type="nurbsCurve")]
getsrcObj = [(cmds.listRelatives(each, p=1, type="transform")[0]) for each in cmds.listRelatives(cmds.ls(sl=1)[0], ad=1, type="nurbsCurve")]
for parent_item, child_item in map(None, getdrvObj, getsrcObj):
    try:
        cmds.blendShape(parent_item, child_item, n = "{}_bsp".format(child_item),o="world", w=(0, 1.0))
    except:
        pass


output =[[a, b] for a in getdrvObj for b in getsrcObj if b in a]

getdrvObj = [(cmds.listRelatives(each, p=1, type="transform")[0]) for each in cmds.listRelatives(cmds.ls(sl=1)[1], ad=1, type="nurbsCurve")]
getsrcObj = [(cmds.listRelatives(each, p=1, type="transform")[0]) for each in cmds.listRelatives(cmds.ls(sl=1)[0], ad=1, type="nurbsCurve")]
output =[[parent_item, child_item] for parent_item in getdrvObj for child_item in getsrcObj if child_item.split("_mid")[0] in parent_item.split(":")[-1]]
for each in output:
    print each

getdrvObj = [(cmds.listRelatives(each, p=1, type="transform")[0]) for each in cmds.listRelatives(cmds.ls(sl=1)[1], ad=1, type="nurbsCurve")]
getsrcObj = [(cmds.listRelatives(each, p=1, type="transform")[0]) for each in cmds.listRelatives(cmds.ls(sl=1)[0], ad=1, type="nurbsCurve")]
output =[(parent_item, child_item) for parent_item in set(getdrvObj )for child_item in set(getsrcObj) if child_item.split("_mid")[0] in parent_item.split(":")[-1]]for each in output:
    try:
        cmds.blendShape(each[1], each[0], n = "{}_bsp".format(each[1]),o="world", w=(0, 1.0))
    except:
        pass

2059








