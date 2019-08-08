
'''Transfers selection to nearby verts of other objects'''
__author__="Elise Deglau"
import maya.cmds as mc
import os, sys
#import maya.mel
import numpy
from apiWrappers import getPoints
import mMesh
reload(mMesh)


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
    print "start"
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






