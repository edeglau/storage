from maya import cmds
import re
microLeadCurve = 'techmesh_:lip_crv'
cmds.CreateEmptyGroup()
cmds.rename(cmds.ls(sl=1)[0], 'noseTipFK_GRP')
cmds.parent('noseTipFK_GRP', 'setup_GRP')
attrs = ['rx', 'ry', 'rz', 'tx', 'ty', 'tz', 'sx', 'sy', 'sz']
centerFace = '2748'
leftFace = '2762'
rightFace = '25666'
prnt_node_rvt = 'C_noseTip_rvt'


#######make the rivet
facelink = 'render_head_default_topology_decomposed_:skinPurple_C_head_GED.f[{}]'.format(centerFace)
cmds.select(facelink, r=1)
cmds.Rivet()
cmds.rename('pinOutput', prnt_node_rvt)
cmds.parent(prnt_node_rvt, 'noseTipFK_GRP')
# cmds.parent('C_noseTip_ctl_rvt', 'noseTipFK_GRP')
getTrns_strt = cmds.xform(prnt_node_rvt, q=True, ws=1, t=True)
getRot_strt = cmds.xform(prnt_node_rvt, q=True, ws=1, ro=True)
cmds.CreateEmptyGroup()
cmds.rename(cmds.ls(sl=1)[0], 'C_noseTipCTL_rvt')
splc = cmds.ls(sl=1)
cmds.xform(splc, ws=1, t=getTrns_strt)
cmds.xform(splc, ws=1, ro=getRot_strt)
cmds.CreateEmptyGroup()
cmds.rename(cmds.ls(sl=1)[0], 'C_noseTipLCL_rvt')
lc = cmds.ls(sl=1)
cmds.xform(lc, ws=1, t=getTrns_strt)
cmds.xform(lc, ws=1, ro=getRot_strt)
cmds.CreateEmptyGroup()
cmds.rename(cmds.ls(sl=1)[0], 'C_noseTip_grp')
lcgrp = cmds.ls(sl=1)
cmds.xform(lcgrp, ws=1, t=getTrns_strt)
cmds.xform(lcgrp, ws=1, ro=getRot_strt)
cmds.parent(lcgrp, 'techMesh_geometryStack_fk_ctl_GRP')

link_loc = cmds.duplicate('C_noseTip_rvt', n='C_noseTip_loc')
cmds.xform(link_loc, ws=1, t=getTrns_strt)
cmds.xform(link_loc, ws=1, ro=getRot_strt)
cmds.parentConstraint(lcgrp[0], 'C_noseTipCtl_GRP', mo=1)
cmds.parent(lc, 'noseTipFK_GRP')
try:
    cmds.parent('C_noseTip_loc', 'noseTipFK_GRP')
except:
    pass
cmds.parent(splc, 'techMesh_geometryStack_fk_ctl_GRP')
cmds.parentConstraint(prnt_node_rvt, lc, mo=1)
cmds.parentConstraint(prnt_node_rvt, splc, mo=1)
each_cnosetip = 'C_noseTip_JNT'
clsnm = 'C_noseTip_LCL_JNT'
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
cmds.parent(getCluster + '_GRP', 'noseTipFK_GRP')
for attr in attrs:
    cmds.connectAttr('{}.{}'.format(lc[0], attr),
                     '{}.{}'.format(lcgrp[0], attr), f=1)
cmds.parentConstraint('C_noseTip_rvt', 'C_noseTip_LCL_JNT')
for side in 'LR':
    for gtnum in xrange(1,4):
        each = '{}_noseTip0{}_JNT'.format(side, gtnum)
        clsnm = '{}_noseTip{}_LCL_JNT'.format(side, gtnum)
        getTranslation = cmds.xform(each, q=True, ws=1, t=True)
        getCluster=cmds.joint(each, n= clsnm, p = getTranslation)
        crtOnt = cmds.orientConstraint(each, getCluster, mo=0)
        cmds.delete(crtOnt)
        getNewRot = cmds.xform(getCluster,  q=True, ws=1, ro=True)
        cmds.CreateEmptyGroup()
        cmds.rename(cmds.ls(sl=1)[0], getCluster+'_GRP')
        cmds.xform(getCluster+'_GRP', ws=1, t=getTranslation)
        cmds.xform(getCluster+'_GRP', ws=1, ro=getNewRot)
        if '2_LCL_JNT' in getCluster:
            cmds.parent(getCluster+'_GRP', '{}_noseTip1_LCL_JNT'.format(side))
        elif '3_LCL_JNT' in getCluster:
            cmds.parent(getCluster+'_GRP', '{}_noseTip2_LCL_JNT'.format(side))
        else:
            cmds.parent(getCluster+'_GRP', 'C_noseTip_LCL_JNT')
        cmds.CreateEmptyGroup()
        cmds.rename(cmds.ls(sl=1)[0], getCluster+'ctl_GRP')
        cmds.xform(getCluster+'ctl_GRP', ws=1, t=getTranslation)
        cmds.xform(getCluster+'ctl_GRP', ws=1, ro=getNewRot)
        cmds.parent(getCluster+'ctl_GRP', getCluster+'_GRP')
        cmds.parent(getCluster, getCluster+'ctl_GRP')
        for attr in attrs:
            cmds.connectAttr('{}_noseTip0{}_CTL.{}'.format(side, gtnum, attr),
                             '{}_noseTip{}_LCL_JNT.{}'.format(side, gtnum, attr), f=1)
        cmds.parentConstraint(lc, '{}_noseTip1_LCL_JNT_GRP'.format(side), mo=1)

