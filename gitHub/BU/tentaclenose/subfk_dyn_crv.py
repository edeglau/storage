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
        cmds.scaleConstraint(lc, '{}_{}_0_FK_JNT_GRP'.format(side, alpha), mo=1)