from maya import cmds
import re

attrs = ['rx', 'ry', 'rz', 'tx', 'ty', 'tz', 'sx', 'sy', 'sz']

name_of = 'C_noseTip'
local_grp = 'noseTip'
faceSkin = 'render_head_default_topology_decomposed_:skinPurple_C_head_GED'#this is the shapenetwork mesh(topo)
tech_grp = 'techMesh_geometryStack_fk_ctl_GRP'

#create setup local group for the new localized joint
cmds.CreateEmptyGroup()
cmds.rename(cmds.ls(sl=1)[0], '{}FK_GRP'.format(local_grp))
cmds.parent('{}FK_GRP'.format(local_grp), 'setup_GRP')

#######make the rivet
centerFace = '2748'
leftFace = '2762'
rightFace = '25666'
prnt_node_rvt = '{}_rvt'.format(name_of)

facelink = '{}.f[{}]'.format(faceSkin, centerFace)
cmds.select(facelink, r=1)
cmds.Rivet()
cmds.rename('pinOutput', prnt_node_rvt)
cmds.parent(prnt_node_rvt, '{}FK_GRP'.format(local_grp))
# cmds.parent('C_noseTip_ctl_rvt', 'noseTipFK_GRP')
getTrns_strt = cmds.xform(prnt_node_rvt, q=True, ws=1, t=True)
getRot_strt = cmds.xform(prnt_node_rvt, q=True, ws=1, ro=True)
cmds.CreateEmptyGroup()
cmds.rename(cmds.ls(sl=1)[0], '{}CTL_rvt'.format(name_of))
splc = cmds.ls(sl=1)
cmds.xform(splc, ws=1, t=getTrns_strt)
cmds.xform(splc, ws=1, ro=getRot_strt)
cmds.CreateEmptyGroup()
cmds.rename(cmds.ls(sl=1)[0], '{}LCL_rvt'.format(name_of))
lc = cmds.ls(sl=1)
cmds.xform(lc, ws=1, t=getTrns_strt)
cmds.xform(lc, ws=1, ro=getRot_strt)
cmds.CreateEmptyGroup()
cmds.rename(cmds.ls(sl=1)[0], '{}_grp'.format(name_of))
lcgrp = cmds.ls(sl=1)
cmds.xform(lcgrp, ws=1, t=getTrns_strt)
cmds.xform(lcgrp, ws=1, ro=getRot_strt)
cmds.parent(lcgrp, tech_grp)

#make the local joint and constrain it. The world space joint already exists by this point via ride common FK task.

link_loc = cmds.duplicate('{}_rvt'.format(name_of), n='{}_loc'.format(name_of))
cmds.xform(link_loc, ws=1, t=getTrns_strt)
cmds.xform(link_loc, ws=1, ro=getRot_strt)
cmds.parentConstraint(lcgrp[0], '{}Ctl_GRP'.format(name_of), mo=1)
cmds.parent(lc, '{}FK_GRP'.format(local_grp))
try:
    cmds.parent('{}_loc'.format(name_of), '{}FK_GRP'.format(local_grp))
except:
    pass
cmds.parent(splc, tech_grp)
cmds.parentConstraint(prnt_node_rvt, lc, mo=1)
cmds.parentConstraint(prnt_node_rvt, splc, mo=1)
each_cnosetip = '{}_JNT'.format(name_of)
clsnm = '{}_LCL_JNT'.format(name_of)
getTranslation = cmds.xform(each_cnosetip, q=True, ws=1, t=True)
getCluster = cmds.joint(each_cnosetip, n=clsnm, p=getTranslation)
crtOnt = cmds.orientConstraint(each_cnosetip, getCluster, mo=0)
cmds.delete(crtOnt)
getNewRot = cmds.xform(getCluster, q=True, ws=1, ro=True)
cmds.CreateEmptyGroup()
cmds.rename(cmds.ls(sl=1)[0], getCluster + '_GRP')
cmds.xform(getCluster + '_GRP', ws=1, t=getTranslation)
cmds.xform(getCluster + '_GRP', ws=1, ro=getNewRot)
cmds.parent(clsnm, getCluster + '_GRP')
cmds.parent(getCluster + '_GRP', '{}FK_GRP'.format(local_grp))
for attr in attrs:
    cmds.connectAttr('{}.{}'.format(lc[0], attr),
                     '{}.{}'.format(lcgrp[0], attr), f=1)
cmds.parentConstraint('{}_rvt'.format(name_of), '{}_LCL_JNT'.format(name_of))