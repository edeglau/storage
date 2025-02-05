from maya import cmds

selfU = 12
selfV = 1
cmds.nurbsToPolygonsPref(un=selfU, vn=selfV)
# cmds.nurbsToPolygonsPref( pc=True, vn = 70 )
crcl = cmds.circle(c=(0,0,0), nr=(0, 1, 0), n='circle_ext_cv', sw=360, r=1.3, d=3, ut=0, tol=0.01, s=8, ch=1)[0]
cmds.parent('circle_ext_cv', "offset_Crvs")
cmds.setAttr("circle_ext_cv.visibility", 0)
for side in 'LR':
    for alpha in 'ABCDEFG':
        fstjnt = '{}_noseFingies_{}_1_JNT'.format(side, alpha)
        fstjnt_dup = '{}_noseFingies_{}_1_JNT1'.format(side, alpha)
        cmds.select(fstjnt, hi=1)
        getchildObj=cmds.ls(sl=1, fl=1)
        crvnm = '{}_noseFingies_{}_crv'.format(side, alpha)
        mn_curve_dvn = '{}_mn_crv'.format(crvnm.split('_crv')[0])
        #######################create offsetcurve for the main curve in order to keep the curve orientation
        locl_ofst_crv = '{}_ofst'.format(mn_curve_dvn)
        nmdup = '{}_forwrap'.format(mn_curve_dvn)
        cmds.select([crcl, mn_curve_dvn], r=1)
        ext = cmds.extrude(crcl, mn_curve_dvn, n='{}_{}_extd'.format(side, alpha), ch=1, rn=0, po=0, et=2, ucp=1, fpt=1, upn=1,
                           rsp=1, rotation=0, scale=1)[0]
        cmds.parent(ext, 'offset_Crvs')
        polycopy = cmds.nurbsToPoly(ext, n='{}_{}_poly'.format(side, alpha), pt=1, pc=100, ch=1, f=1, chr=0.9, ft=0.01, d=0.1, mel=0.001,
                                    ut=1, un=3, vt=1, mnd=1, uch=0, ucr=0, cht=0.2, es=0, ntr=0, mrt=0, uss=1)[0]
        ##############create offset curve
        cmds.select('{}_{}_poly.e[0]'.format(side, alpha))
        cmds.polySelectSp(loop=1)
        cmds.polyToCurve(form=2, degree=3)
        cmds.rename(cmds.ls(sl=1)[0], locl_ofst_crv)
        cmds.delete(locl_ofst_crv, ch=1)
        dup_fk  = cmds.duplicate(locl_ofst_crv, n='{}_fk'.format(locl_ofst_crv))[0]
        dup_ik  = cmds.duplicate(locl_ofst_crv, n='{}_ik'.format(locl_ofst_crv))[0]
        def_fk_name = '{}_fk_bsp'.format(locl_ofst_crv)
        def_ik_name = '{}_ik_bsp'.format(locl_ofst_crv)
        cmds.blendShape(dup_fk, locl_ofst_crv, origin='world', n=def_fk_name, w=(0, 1.0))
        cmds.blendShape(dup_ik, locl_ofst_crv, origin='world', n=def_ik_name, w=(0, 1.0))
        fk_jnts = '{}_{}_?_FKsub_JNT'.format(side, alpha)
        ik_jnts = '{}_noseFingies{}?_LCL_IK_JNT'.format(side, alpha)
        cmds.select(dup_fk, fk_jnts)
        cmds.skinCluster(tsb=1, bm = 0)
        cmds.select(dup_ik, ik_jnts)
        cmds.skinCluster(tsb=1, bm = 0)
        cmds.delete(polycopy)
        cmds.delete(ext)
        cmds.parent(dup_fk, 'offset_Crvs')
        cmds.parent(dup_ik, 'offset_Crvs')
        cmds.parent('{}_noseFingies_{}_mn_crv_ofst'.format(side, alpha), 'offset_Crvs')
        for index, selObj in enumerate(getchildObj):
            motionPath='{}_{}_{}_mpth'.format(side, alpha, index)
            pgetCVpos=cmds.xform(selObj, ws=1, q=1, t=1)
            ########################################
            ##################create orient
            #######################################
            npC_lcl_cv = cmds.createNode("nearestPointOnCurve")
            cmds.setAttr(npC_lcl_cv + ".inPosition", pgetCVpos[0], pgetCVpos[1], pgetCVpos[2], type="double3")
            get_hsp_off_ctl = cmds.listRelatives(locl_ofst_crv, ad=1, type="nurbsCurve")[0]
            cmds.connectAttr("{}.worldSpace".format(get_hsp_off_ctl), npC_lcl_cv + ".inputCurve", f=1)
            getpoint = cmds.getAttr(npC_lcl_cv + ".position")
            getParam = cmds.getAttr(npC_lcl_cv + ".parameter")
            lc_fol_jnt = cmds.spaceLocator(n=selObj + '_jnt_loc')[0]
            cmds.xform(lc_fol_jnt, ws=1, t=pgetCVpos)
            cmds.select(lc_fol_jnt, r=1)
            cmds.select(locl_ofst_crv, add=1)
            offset_lcl_motionPath = cmds.pathAnimation(fractionMode=1, follow=1, followAxis="x", upAxis="y", worldUpType="Vector",
                                                       bank=0)
            cmds.disconnectAttr(offset_lcl_motionPath + "_uValue.output", offset_lcl_motionPath + ".uValue")
            getpth = str(offset_lcl_motionPath)
            cmds.setAttr(offset_lcl_motionPath + ".fractionMode", False)
            cmds.setAttr(offset_lcl_motionPath + ".uValue", getParam)
            cmds.parent(lc_fol_jnt, 'ofs_Locs')
            cmds.connectAttr(lc_fol_jnt + '.worldMatrix[0]', motionPath + '.worldUpMatrix')
            cmds.delete(npC_lcl_cv)