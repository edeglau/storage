from maya import cmds
import re
'''This will create the attributes for the bending and connect them'''
cmds.CreateEmptyGroup()
cmds.rename(cmds.ls(sl=1)[0], 'noseFingies_GRP')
cmds.parent('noseFingies_GRP', 'setup_GRP')

cmds.CreateEmptyGroup()
cmds.rename(cmds.ls(sl=1)[0], 'skinJnts_GRP')
cmds.parent('skinJnts_GRP', 'noseFingies_GRP')

cmds.CreateEmptyGroup()
cmds.rename(cmds.ls(sl=1)[0], 'wrapDefs_GRP')
cmds.parent('wrapDefs_GRP', 'noseFingies_GRP')

cmds.CreateEmptyGroup()
cmds.rename(cmds.ls(sl=1)[0], 'build_Crvs')
cmds.parent('build_Crvs', 'noseFingies_GRP')

cmds.CreateEmptyGroup()
cmds.rename(cmds.ls(sl=1)[0], 'main_Crvs')
cmds.parent('main_Crvs', 'noseFingies_GRP')

cmds.CreateEmptyGroup()
cmds.rename(cmds.ls(sl=1)[0], 'offset_Crvs')
cmds.parent('offset_Crvs', 'noseFingies_GRP')

cmds.CreateEmptyGroup()
cmds.rename(cmds.ls(sl=1)[0], 'main_Locs')
cmds.parent('main_Locs', 'noseFingies_GRP')

cmds.CreateEmptyGroup()
cmds.rename(cmds.ls(sl=1)[0], 'ofs_Locs')
cmds.parent('ofs_Locs', 'noseFingies_GRP')

jntgrp = []
for side in 'LR':
    for alpha in 'ABCDEFG':
        fstjnt_o = '{}_noseFingies_{}_1_JNT'.format(side, alpha)
        fstjnt = cmds.duplicate(fstjnt_o, rc=1)
        # cmds.joint(fstjnt, e=1, children =1, zso=1, oj = 'yxz', sao='yup', spa=1)
        jntgrp.append(fstjnt[0])
        cmds.parent(fstjnt[0], 'skinJnts_GRP')
        ######################
        #CREATE THE SPLINE HERE
        #####################
        iknm = '{}{}_mn_IK'.format(side, alpha)
        fstjnt = '{}_noseFingies_{}_1_JNT1'.format(side, alpha)
        getall = cmds.ls('{}_noseFingies_{}_*_JNT1'.format(side, alpha))
        crvnm = '{}_noseFingies_{}_crv'.format(side, alpha)
        gettop = len(getall)
        length = gettop -1
        endjnt = '{}_noseFingies_{}_{}_JNT1'.format(side, alpha, gettop)
        getRot = cmds.xform(endjnt, q=True, ws=1, ro=True)
        cmds.select(fstjnt, hi=1)
        getchildObj=cmds.ls(sl=1, fl=1)
        hndl = cmds.ikHandle(n = iknm, sj = fstjnt, ee = endjnt,sol = 'ikSplineSolver', scv=0, ns=2, rtm=1, cra=1, pcv=0, tws = 'easIn')[0]
        getcrv = [(cmds.listRelatives(each, p=1, type = 'transform')[0])for each in cmds.listHistory(hndl) if cmds.nodeType(each) == "nurbsCurve" ][0]
        cmds.delete(hndl)
        cmds.rename(getcrv, crvnm)
        ###################################################
        ##wire constrin to the main curve to move it
        ##################################################
        getCVs=cmds.ls(crvnm+".cv[*]", fl=1)
        mn_curve_dvn ='{}_mn_crv'.format(crvnm.split('_crv')[0])
        cmds.duplicate(crvnm, n=mn_curve_dvn)
        cmds.rebuildCurve( mn_curve_dvn, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=0, kt=0, s=8, d=2, tol=0.001)
        wrnm = '{}_wr'.format(crvnm)
        for index, selObj in enumerate(getchildObj):
            pgetCVpos=cmds.xform(selObj, ws=1, q=1, t=1)
            npC = cmds.createNode("nearestPointOnCurve")
            cmds.setAttr(npC + ".inPosition", pgetCVpos[0], pgetCVpos[1], pgetCVpos[2], type="double3")
            get_hsp=cmds.listRelatives(mn_curve_dvn, ad=1, type="nurbsCurve")[0]
            cmds.connectAttr("{}.worldSpace".format(get_hsp), npC + ".inputCurve")
            getpoint = cmds.getAttr(npC + ".position")
            getParam = cmds.getAttr(npC + ".parameter")
            #################LOCAL
            loc = cmds.spaceLocator(n=selObj+'_loc')
            cmds.xform(loc, ws=1, t = pgetCVpos)
            cmds.select(loc, r=1)
            cmds.select(mn_curve_dvn, add=1)
            motionPath=cmds.pathAnimation(fractionMode=1, n='{}_{}_{}_mpth'.format(side, alpha, index), follow=1, followAxis="x", upAxis="y", worldUpType="object", bank=0)
            cmds.disconnectAttr(motionPath+"_uValue.output", motionPath+".uValue")
            getpth=str(motionPath)
            cmds.setAttr(motionPath+".fractionMode", False)
            cmds.setAttr(motionPath+".uValue", getParam)
            cmds.delete(npC)
            cmds.parentConstraint(loc, selObj, mo=1)
            cmds.parent(loc, 'main_Locs')
        ############set groups
        cmds.delete(crvnm)
        cmds.parent(mn_curve_dvn, 'main_Crvs')
