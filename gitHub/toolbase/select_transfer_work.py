'''Transfers selection to nearby verts of other objects'''
__author__="Elise Deglau"
import maya.cmds as mc
import os, sys
#import maya.mel
import numpy
from apiWrappers import getPoints
import mMesh
reload(mMesh)
import maya.api.OpenMaya as OpenMaya
 
 
#Author: Elise Deglau
#https://atlas.bydeluxe.com/confluence/display/~lime/2018-8-23+Elise+D
 
#to add to shelf:
 
# import sys
# filepath=( '//sw/dev/deglaue/tools//' )
# if not filepath in sys.path:
#     sys.path.append(str(filepath))
# import select_transfer
# reload (select_transfer)
# evokeTool = select_transfer.map_select_transfer()
# evokeTool()
 
#icon
 
# /sw/dev/deglaue/icons/deglaue_toolset_seltransfr.png
 
def map_select_transfer():
    # print "start"
    # Transfers selection to nearby verts of other objects.
    NDIM = 3
    selObj=mc.ls(sl=1, fl=1)
    #query if selected
    if selObj:
        if len(selObj)<2:
            print "select a group of verts and an object or two objects near eachother."
            return
        else:
            pass        
        #get falloff amount
        result = mc.promptDialog(
            title="Confirm",
            message="Radius:",
            text=".001",
            button=["Swap","Add","Cancel"],
            cancelButton="Cancel",
            dismissString="Cancel" )
        if result == "Add":
            radius = mc.promptDialog(query=True, text=True)
            radius = float(radius)
            radius = radius * radius
            adding=True       
        elif result == "Swap":
            radius = mc.promptDialog(query=True, text=True)
            radius = float(radius)
            radius = radius * radius
            adding=False
        else:
            print "selection transfer cancelled" 
            return
    else:
        print "select a group of verts and an object or two objects near eachother."
        return
    # mc.select(selObj[0])
    #determine if the mapper is a vertex selection or object
    result = []
    if ".v" in selObj[0]:
        #collect the mapper verts
        getFirstGrp = selObj[0].split(".")[0]
        sourceName=[(each) for each in selObj if each.split(".")[0]==getFirstGrp]
        #determine the mapping selections
        targetName=[(each) for each in selObj if each.split(".")[0]!=getFirstGrp]
        # print sourceName, targetName
        if adding == False:
            mc.select(cl=1)
        for eachtarget in targetName:
            mc.select(eachtarget, d=1)
            mc.select(mMesh.get_closest_points(eachtarget, transform=0, mesh=0, mesh_vtx=sourceName, distance=radius), add=1)
    else:
        #transfer the mapper into verts
        sourceName = selObj[0]
        #determine the mapping selections
        targetName=[(each) for each in selObj if each != sourceName]
        #targetpoints into array
        if adding == False:
            mc.select(cl=1)   
        for eachtarget in targetName:
            mc.select(eachtarget, d=1)
            a = getPoints(mc.ls(eachtarget)[0], space='world')
            a.shape = a.size / NDIM, NDIM
            #sourcepoints into array
            srcPoints = getPoints(mc.ls(sourceName)[0], space = "world")
            #create empty set
            result = set()
            for point in srcPoints:
                d = ((a-point)**2).sum(axis = 1) #compute distance
                ndx = d.argsort()
                max_idx = next((i for i, v in enumerate(ndx) if d[v] >radius), None)
                if max_idx:
                    result.update(ndx[:max_idx])
        result = list(result)
        mc.select(['{}.vtx[{}]'.format(eachtarget, x) for x in result], add =1)
 
 
 
 
def UV_select_transfer():
    # NDIM = 3
    selObj=mc.ls(sl=1, fl=1)
    # selection_list = OpenMaya.MSelectionList()
    # for each in sourceSelection:
    #     selection_list.add(each)
    if selObj:
        if len(selObj)<2:
            print "select a group of verts and an object or two objects near eachother."
            return
        else:
            pass        
        #get falloff amount
        result = mc.promptDialog(
            title="Confirm",
            message="Radius:",
            text=".001",
            button=["Swap","Add","Cancel"],
            cancelButton="Cancel",
            dismissString="Cancel" )
        if result == "Add":
            radius = mc.promptDialog(query=True, text=True)
            radius = float(radius)
            radius = radius * radius
            adding=True       
        elif result == "Swap":
            radius = mc.promptDialog(query=True, text=True)
            radius = float(radius)
            radius = radius * radius
            adding=False
        else:
            print "selection transfer cancelled" 
            return
    else:
        print "select a group of verts and an object or two objects near eachother."
        return
    result = []
    bookit = []
    if adding == False:
        mc.select(cl=1)   
    sourceSelection = selObj[:-1]
    targetSelection = selObj[-1]       
    for each_src in sourceSelection:   
        # print eachtarget
        selection_source = OpenMaya.MSelectionList()
        selection_source.add(each_src)
        # print selection_source
        nodeDagPath = selection_source.getDagPath(0)
        mfnMesh_src = OpenMaya.MFnMesh(nodeDagPath)       
        # mc.select(clear=1) 
        # mc.select(eachtarget, r=1)
        a = mc.xform(each_src,q=True,ws=True, t=True)
        getmpoint = OpenMaya.MPoint(a[0], a[1], a[2])
        # createspaceorigin = mc.spaceLocator(p=(a[0], a[1], a[2]))
        uvSet = 'map1'
        placement = mfnMesh_src.getUVAtPoint(getmpoint, OpenMaya.MSpace.kWorld, uvSet)
        # print placement
        u = placement[0]
        v = placement[1]
        getlocators = newset(u, v, targetSelection)
        mc.select(clear = 1)
        returnselect = mMesh.get_closest_points(targetSelection, transform=getlocators, mesh=0, mesh_vtx=0, distance=2)
    if returnselect != None:
        print returnselect
        mc.select(returnselect, add=1)
        # if getselection != None:
            # for each in getselection:
            # print getselection
 
 
    #     if getselection != None:
    #         bookit.append(getselection)
    # print bookit
    # newset(u, v, targetSelection)
    # mc.select(bookit[0], add=1)
 
 
 
def newset(u, v, targetSelection):
    mc.select(targetSelection, r=1)
    selection_last = OpenMaya.MSelectionList()
    selection_last.add(targetSelection)   
    nodeDagPath = selection_last.getDagPath(0)
    mfnMesh_tgt = OpenMaya.MFnMesh(nodeDagPath)   
    uvSet = 'map1'
    try:
        targetPoints = mfnMesh_tgt.getPointsAtUV(u, v, OpenMaya.MSpace.kWorld, uvSet, tolerance=1e-5)
        # print targetPoints
        objplace = (targetPoints[1][0][0], targetPoints[1][0][1] , targetPoints[1][0][2])
        transforms = []
        for each in objplace:
            if "e" in str(each):
                newnum = str(each).split('e')[0]
                transforms.append(float(newnum))
            else:
                newnum = each
                transforms.append(float(newnum))
        # print transforms
        # createtargetspace = mc.spaceLocator(p=transforms, n="newplace")[0]
        createtargetspace = mc.spaceLocator(n="newplace")[0]
        mc.move(createtargetspace, )
        # print createtargetspace
        # getselection = mc.ls(sl = createtargetspace)
        # print getselection
        # mc.select(mMesh.get_closest_points(target_geo=targetSelection, transform=createtargetspace, mesh=0, mesh_vtx=0, distance=5), add=1)
        # returnselect = mMesh.get_closest_points(targetSelection, transform=getselection, mesh=0, mesh_vtx=0, distance=3)
        # print returnselect
        return createtargetspace
        # mc.select(mMesh.get_closest_points(targetSelection, transform=createtargetspace, mesh=0, mesh_vtx=0, distance=2), add=1)
        # print findpoint
        # return findpoint
    except:
        pass
    # findpoint = mMesh.get_closest_point(geo=targetSelection, transform=createtargetspace, vertex=1, face=0, facet_vtx=0)
    # print findpoint
 
 
 
# def get_dag_path(node):
#     """Get the MDagPath of the given node.
 
#     :param node: Node name
#     :return: Node MDagPath
#     """
#     selection_list = OpenMaya.MSelectionList()
#     print selection_list
#     selection_list.add(node)
#     path = OpenMaya.MDagPath()
#     selection_list.getDagPath(0)
#     return path
 
 
# def getPosition(point):
#     print point
#     '''
#     Return the position of any point or transform
#     @param point: Point to return position for
#     @type point: str or list or tuple
#     '''
#     # Initialize point value
#     pos = []
#     if (type(point) == list) or (type(point) == tuple):
#         if len(point) < 3:
#             raise Exception('Invalid point value supplied! Not enough list/tuple elements!')
#         pos = point[0:3]
#     elif (type(point) == str) or (type(point) == unicode):
#         # Check Transform
#         mObject = getMObject(point)
#         if mObject.hasFn(OpenMaya.MFn.kTransform):
#             try:
#                 pos = mc.xform(point,q=True,ws=True,rp=True)
#                 print pos
#             except:
#                 pass
          
#         # pointPosition query
#         if not pos:
#             try:
#                 pos = mc.pointPosition(point)
#                 print pos
#             except:
#                 pass
#         # xform - rotate pivot query
#         if not pos:
#             try:
#                 pos = mc.xform(point,q=True,ws=True,rp=True)
#                 print pos
#             except:
#                 pass
#     #     # Unknown type
#     #     if not pos:
#     #         raise Exception('Invalid point value supplied! Unable to determine type of point "'+str(point)+'"!')
#     # else:
#     #     raise Exception('Invalid point value supplied! Invalid argument type!')
          
#     # # Return result
#     return pos
