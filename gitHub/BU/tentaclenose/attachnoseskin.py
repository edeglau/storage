import maya.cmds as cmds
cmds.CreateEmptyGroup()
cmds.rename(cmds.ls(sl=1)[0], 'noseFingies_attach_GRP')
cmds.parent('noseFingies_attach_GRP', 'setup_GRP')

cmds.duplicate('techmesh_:lip_msh', n='lip_ctrl_msh')
cmds.duplicate('techmesh_:lip_crv', n='lip_ctrl_top_crv')
cmds.blendShape('techmesh_:lip_msh', 'lip_ctrl_msh', origin = 'local',n='lip_bsp', w=(0, 1.0))
cmds.blendShape('techmesh_:lip_crv', 'lip_ctrl_top_crv', origin = 'local',n='lip_crv_bsp', w=(0, 1.0))

hidegrp = [
        'lip_ctrl_msh',
        'lip_ctrl_top_crv',
        'techmesh_:lip_crv',
        'techmesh_:lip_msh',
        'setup_GRP'
        ]
for item in hidegrp:
    cmds.setAttr('{}.v'.format(item), 0)

microLeadCurve = 'techmesh_:lip_crv'
microLeadCurve_ctrl = 'techMesh_geometryStackFk_ctlFingiesWorldMesh_CRV'
cmds.parent(microLeadCurve_ctrl, 'noseFingies_attach_GRP')
cmds.blendShape(microLeadCurve, microLeadCurve_ctrl, o='local', n="fk_main_bsp", w=(0, 1.0))
cmds.parentConstraint('C_headWorld_JNT', 'techMesh_geometryStack_fk_ctl_GRP', mo=1)
cmds.scaleConstraint('C_headWorld_JNT', 'techMesh_geometryStack_fk_ctl_GRP', mo=1)

for side in 'LR':
    for alpha in 'DEF':
        selObj = "{}_noseFingies{}".format(side, alpha)
        jntalph = selObj[-1:]
        jntstrt = selObj[:-1]
        jnt = '{}_{}_1_JNT'.format(jntstrt, jntalph)
        try:
            pgetCVpos = cmds.xform(jnt, ws=1, q=1, t=1)
        except:
            pass
        npC = cmds.createNode("nearestPointOnCurve")
        pcI = cmds.createNode('pointOnCurveInfo')
        cmds.setAttr(npC + ".inPosition", pgetCVpos[0], pgetCVpos[1], pgetCVpos[2], type="double3")
        get_hsp = cmds.listRelatives(microLeadCurve, ad=1, type="nurbsCurve")[0]
        cmds.connectAttr("{}.worldSpace".format(get_hsp), npC + ".inputCurve")
        getpoint = cmds.getAttr(npC + ".position")
        getParam = cmds.getAttr(npC + ".parameter")
        cmds.delete(npC)
        cmds.connectAttr("{}.worldSpace".format(get_hsp), pcI + ".inputCurve")
        lc = cmds.spaceLocator(n=selObj + '_loc')[0]
        splc = cmds.spaceLocator(n=selObj + '_ctl_loc')[0]
        cmds.parent(splc, 'techMesh_geometryStack_fk_ctl_GRP')
        cmds.parent(lc, 'noseFingies_attach_GRP')
        cmds.connectAttr(pcI + ".position", "{}.t".format(lc))
        cmds.connectAttr(pcI + ".position", "{}.t".format(splc))
        cmds.setAttr(pcI + ".parameter", getParam)
        cmds.parentConstraint(lc, '{}_{}_0_FK_JNT_GRP'.format(side, alpha), mo=1)
        cmds.parentConstraint(lc, '{}_{}_0_FKsub_JNT_GRP'.format(side, alpha), mo=1)
        cmds.parentConstraint(lc, '{}_noseFingies{}LCLbase_JNTAIM_GRP'.format(side, alpha), mo=1)
        ####################################
        ####now connect the ctls
        ####################################        cmds.setAttr(pcI + ".parameter", getParam)
        cmds.parentConstraint(splc, '{}_noseFingies{}1Ctl_GRP'.format(side, alpha), mo=1)
        cmds.scaleConstraint('techMesh_geometryStack_fk_ctl_GRP', '{}_noseFingies{}1Ctl_GRP'.format(side, alpha), mo=1)
        cmds.parentConstraint(splc, '{}_noseFingies{}1subCtl_GRP'.format(side, alpha), mo=1)
        cmds.parentConstraint(splc, '{}_noseFingies{}_IKbaseCtl_GRP'.format(side, alpha), mo=1)

for side in 'LR':
    for alpha in 'ABCG':
        selObj = "{}_noseFingies{}".format(side, alpha)
        jntalph = selObj[-1:]
        jntstrt = selObj[:-1]
        jnt = '{}_{}_1_JNT'.format(jntstrt, jntalph)
        try:
            pgetCVpos = cmds.xform(jnt, ws=1, q=1, t=1)
        except:
            pass
        npC = cmds.createNode("nearestPointOnCurve")
        pcI = cmds.createNode('pointOnCurveInfo')
        cmds.setAttr(npC + ".inPosition", pgetCVpos[0], pgetCVpos[1], pgetCVpos[2], type="double3")
        get_hsp = cmds.listRelatives('lip_ctrl_top_crv', ad=1, type="nurbsCurve")[0]
        cmds.connectAttr("{}.worldSpace".format(get_hsp), npC + ".inputCurve")
        lc = cmds.spaceLocator(n=selObj + '_loc')[0]
        splc = cmds.spaceLocator(n=selObj + '_ctl_loc')[0]
        cmds.parent(splc, 'techMesh_geometryStack_fk_ctl_GRP')
        cmds.parent(lc, 'noseFingies_attach_GRP')
        cmds.connectAttr(pcI + ".position", "{}.t".format(lc))
        cmds.connectAttr(pcI + ".position", "{}.t".format(splc))
        cmds.setAttr(pcI + ".parameter", getParam)
        cmds.parentConstraint(lc, '{}_{}_0_FK_JNT_GRP'.format(side, alpha), mo=1)
        cmds.scaleConstraint(lc, '{}_{}_0_FK_JNT_GRP'.format(side, alpha), mo=1)
        cmds.parentConstraint(lc, '{}_{}_0_FKsub_JNT_GRP'.format(side, alpha), mo=1)
        cmds.scaleConstraint(lc, '{}_{}_0_FKsub_JNT_GRP'.format(side, alpha), mo=1)
        cmds.parentConstraint(lc, '{}_noseFingies{}LCLbase_JNTAIM_GRP'.format(side, alpha), mo=1)
        ####################################
        ####now connect the ctls
        ####################################
        cmds.setAttr(pcI + ".parameter", getParam)
        cmds.parentConstraint(splc, '{}_noseFingies{}1Ctl_GRP'.format(side, alpha), mo=1)
        cmds.parentConstraint(splc, '{}_noseFingies{}1subCtl_GRP'.format(side, alpha), mo=1)
        cmds.parentConstraint(splc, '{}_noseFingies{}_IKbaseCtl_GRP'.format(side, alpha), mo=1)

