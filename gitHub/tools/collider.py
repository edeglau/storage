'''
Created on Mar 28, 2011

Instructions: swap character to output rig and switch to high model.
Select top node and run this script. this will create the cf group. It will name the new group,
tagging the cf name as a suffix and connects the attributes to follow the rig.

@author: elise.deglau
'''
import maya.cmds as cmds
import re
import maya.mel

###PREP FILE#####################################################################################

nmgrp=cmds.ls(sl=True) #nmgrp
cmds.select(hi=True)
flooo=cmds.ls(sl=True, tr=1)
Orgbody=list()
initModgrp=list()
for i in flooo:
    if 'deform:high:C_geo_body' in i:
        Orgbody.append(i) #Orgbody
cmds.select(Orgbody, r=1)
cmds.pickWalk(d='up')
initModgrp=cmds.ls(sl=1) #initModgrp
cmds.select(Orgbody, r=True)
cmds.pickWalk(d='down')
OrgbdyShp=cmds.ls(sl=True)#OrgbdyShp

cmds.select(Orgbody, r=1)
transform=cmds.ls(sl=True, l=True)[0]
inmesh=cmds.listConnections((transform+'.inMesh'), s=True, d=False, p=True)

cfgrp='_cf'

#duplicate group and group it under a named node
cmds.select(initModgrp)
cmds.duplicate(rr=True)
grpmod=cmds.ls(sl=1)
mgnm=nmgrp[0]+'_model'+cfgrp
cmds.rename(grpmod[0], mgnm)
newModgrp=cmds.ls(sl=True)#newModgrp

#remove other geometry from copied group
cmds.select(newModgrp, r=1)
cmds.select(hi=True)
cmds.select(newModgrp, d=1)
fyo=cmds.ls(sl=True, tr=1)
delLst=list()
for i in fyo:
    if 'C_geo_body' not in i:
        delLst.append(i)
cmds.delete(delLst)
cmds.select(newModgrp, r=1)

#group it under a named node
jlaw=cmds.group()
ilnm=nmgrp[0]+cfgrp
cmds.rename(jlaw, ilnm)
chargrp=cmds.ls(sl=True)


#unparent the new model group from main
cmds.select(chargrp)
cmds.parent(w=True)
cmds.select(chargrp)
cmds.pickWalk(d='down')
newModgrp=cmds.ls(sl=True) #chargrp

#ID the new body
cmds.select(newModgrp, hi=True)
flooo=cmds.ls(sl=True, tr=1)
newBod=list()
for i in flooo:
    if 'body' in i:
                newBod.append(i)  #newBod
cmds.select(newBod, r=1)
nodName=cmds.ls(sl=True)
for i in range (len(nodName)):
    lognm=re.sub(r'\d[1-9]*', '', nodName[i])
    cmds.rename(nodName[i], lognm)
    ffile=lognm.strip('_')
    rognm=cmds.rename(lognm, ffile)
    blKl=nmgrp[0]+'_'+rognm+'+1'+cfgrp
    newBod=cmds.rename(ffile, blKl)
newBod=cmds.ls(sl=1)

#assign new body to lambert shader
cmds.sets (e=1, forceElement='initialShadingGroup')



#ID the new body shape
cmds.select(newBod)
cmds.pickWalk(d='down')
nwShp=cmds.ls(sl=True) #nwShp


cmds.setAttr(nwShp[0]+".overrideEnabled", 0 )


#turn off render options
cmds.setAttr (nwShp[0]+".castsShadows", 0),
cmds.setAttr (nwShp[0]+".receiveShadows", 0)
cmds.setAttr (nwShp[0]+".motionBlur", 0)
cmds.setAttr (nwShp[0]+".primaryVisibility", 0)
cmds.setAttr (nwShp[0]+".smoothShading", 0)
cmds.setAttr (nwShp[0]+".visibleInReflections", 0)
cmds.setAttr (nwShp[0]+".visibleInRefractions", 0)
cmds.setAttr (nwShp[0]+".doubleSided", 0)


##connect duplicated group to rig
cmds.connectAttr((inmesh[0]), (nwShp[0]+'.inMesh'))
cmds.connectAttr((initModgrp[0]+'.translate'), (newModgrp[0]+'.translate'))
cmds.connectAttr((initModgrp[0]+'.rotate'), (newModgrp[0]+'.rotate'))
cmds.connectAttr((initModgrp[0]+'.scale'), (newModgrp[0]+'.scale'))



#add to personal container

cmds.select(chargrp, hi=1)
cntgrp=cmds.ls(sl=1)
ncntnr=cmds.container(n=ilnm, includeShapes=1, includeTransform=1, force=1, an=cntgrp)
cmds.select(newModgrp, r=1)
cmds.select(ncntnr, add=1)
maya.mel.eval('doPublishAttribute 1 { "1", "0", ""  } ;')


##add blendshape to connect to original mesh
#
#cmds.select(OrgbdyShp, r=1)
#cmds.select(nwShp, add=1)
#nmr=nmgrp[0]+"_cf_deform"
#cmds.blendShape(n=nmr, bf=1)
#cmds.setAttr(nmr+'.weight[0]', 1)





###SETTING UP COLLIDERS################################################################################


##create ground solver deformer
newDef=cmds.deformer('C_geo_body_0_cf', type='groundSolver')


cmds.select(newDef)
cmds.rename(newDef, nmgrp[0]+'_'+newDef[0]+'_cf')
grnDef=cmds.ls(sl=True)
#import collider rig
cmds.file('/drd/jobs/hf2/wip/depts/rig/users/nikhil.anand/ForTransfer/To_Elise/groundPlane.mb', i=True)


##Skin the plane to the collider rig#################################################

mds.select("C_geo_collisionPlane_0", r=True)
cmds.select("*2sk*", add=True)
cmds.SmoothBindSkin ()

## Turn on controls
cmds.setAttr('C_ctl_collisionPlane_0.subCtrlsVis', 1)

##MOVING THE COLLIDER IN PLACE##########################################################
########Select a vertex (or group of verts) on the ground beneath character#############################################

vertgrp=cmds.ls(sl=True)
vectorshome=cmds.xform(vertgrp, q=True, t=True, ws=True)
glep=vectorshome[::3]
vecXsum=max(glep)+min(glep)
vecXmid=vecXsum/2
flep=vectorshome[1::3]
vecYsum=max(flep)+min(flep)
vecYmid=vecYsum/2
slep=vectorshome[2::3]
vecZsum=max(slep)+min(slep)
vecZmid=vecZsum/2
cmds.selectMode(object=True)
cmds.spaceLocator()
plog=cmds.ls(sl=True)
cmds.move(vecXmid, vecYmid, vecZmid, plog, ws=True)
cmds.select(plog, r=True)
cmds.select('C_ctl_collisionPlane_0 ', add=True)
newgrpmv=cmds.ls(sl=True)
movefrog=cmds.xform(newgrpmv[0], q=True, t=True, ws=True)
cmds.move(movefrog[0], movefrog[1], movefrog[2], newgrpmv[1], ws=True)
cmds.delete(newgrpmv[0])

#################################################################################################

##Connecting collision plane mesh to the ground solver deformer as target

cmds.connectAttr('C_geo_collisionPlane_0.worldMatrix[0]', (grnDef[0]+'.colliderWorldMatrix'), f=True)
cmds.connectAttr('C_geo_collisionPlane_Shape0.outMesh', (grnDef[0]+'.collisionMesh'), f=True)


##creating the rig collider deformer
coldr=cmds.deformer(newBody, type='rigCollider')
cmds.select(coldr)
cmds.rename(coldr, nmgrp[0]+'_'+coldr[0]+'_cf')
newcoll=cmds.ls(sl=True)

##connecting rig colider to collision plane
cmds.connectAttr('C_geo_collisionPlane_Shape0.worldMesh[0]', (newcoll[0]+'.collisionMesh'), f=True)

##Connecting the body to the ground solver
cmds.connectAttr((newBody[0]+'.worldInverseMatrix[0]'), (grnDef[0]+'.meshInvWorldMatrix'), f=True)


#===============================================================================
#for a bloated look like Ramon on end shot 04_040
# ground solver settings:
# envelope 1
# num iterations 1
# volume factor.015
# ground factor .1
# max volume 70
# uv space distance 0.2
#===============================================================================



'''
Created on Mar 31, 2011

@author: elise.deglau
'''
####SmoothMeshDeformer

##############################################

from maya import cmds
from Functions import shapeFunctions

##Check plugins to load smoothMeshDeformer.


transform=cmds.ls(sl=True)[0]
transform, shape = shapeFunctions.filterShpAndTransform(transform)
origShape   =   shapeFunctions.getShapeOrig(shape)


print transform
print shape
print origShape


cmds.select (origShape)

deformer='C_smoothMesh_0'
cmds.createNode('smoothMesh', name=deformer)
cmds.select (deformer)

inmesh=cmds.listConnections((shape+'.inMesh'), p=True, s=True)[0]

cmds.select(deformer)
cmds.select(origShape)

cmds.connectAttr((origShape+'.outMesh'), (deformer+'.targetMesh'), f=True)
cmds.connectAttr((inmesh), (deformer+'.inputMesh'), f=True)
cmds.connectAttr((deformer+'.outputMesh'), (shape+'.inMesh'), f=True)


#===============================================================================
# overall smooth if used
# pre smooth iterations if used
# pre smooth strength if used
# relax iterations 8
# relax compress strength 5
# relax expand strength 2
# relax multiplier .1
# relax smooth iterations 3
#
# min/max offset str 0/.5
# min/max expand str 0/1
# min/max compress str 0/1
#===============================================================================



#######################################
##Reconnecting Smooth and Collider output>input

# connect rbd>groundsolver1Grp>collider>smooth>shape