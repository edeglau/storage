from maya import cmds
import re
cmds.CreateEmptyGroup()
cmds.rename(cmds.ls(sl=1)[0], 'noseFingiesFK_GRP')
cmds.parent('noseFingiesFK_GRP', 'setup_GRP')
lower_jaw = ['DEF']
for side in 'LR':
    for alpha in 'ABCDEFG':
        mn_curve_dvn = '{}_noseFingies_{}_mn_crv'.format(side, alpha)
        ############FK curves blend
        fk_curve_driver ='{}_fk_crv'.format(mn_curve_dvn.split('_mn')[0])
        fk_curve_skin ='{}_fk_skin_crv'.format(mn_curve_dvn.split('_mn')[0])
        cmds.duplicate(mn_curve_dvn, n=fk_curve_driver)
        cmds.duplicate(mn_curve_dvn, n=fk_curve_skin)
        cmds.rebuildCurve(fk_curve_driver, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=0, kt=0, s=4, d=2, tol=0.001)
        wrnm = '{}_wr'.format(fk_curve_skin)
        # cmds.wire(fk_curve_driver, w=fk_curve_skin, n=wrnm, gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)])
        def_name = '{}_FK_bsp'.format(mn_curve_dvn.split('_mn_')[0])
        cmds.blendShape(fk_curve_skin, mn_curve_dvn, origin = 'world',n=def_name, w=(0, 1.0))
        cmds.parent(fk_curve_driver, 'noseFingiesFK_GRP')
        cmds.parent(fk_curve_skin, 'noseFingiesFK_GRP')
        ######################
        ####NOW CREATE A JOINT AT EACH CV AT EACH PONT OF THE CURVE. CREATE SOME GROUPS FOR THE JOINT TO LIVE IN. ORGANIZE INTO SETUP
        #####################
        bone_collector = []
        grp_bn_coll = []
        boneik_collector = []
        grp_bn_ikcoll = []
        getfkCVs=cmds.ls(fk_curve_driver+".cv[*]", fl=1)
        orderlist = []
        grp = "{}_noseFingies_{}_1_JNT".format(side, alpha)
        getchildlist = [(eajnt) for eajnt in cmds.listRelatives(grp, ad=1, type="transform") if cmds.nodeType(eajnt) == "joint"]
        complista = getchildlist+[grp]
        getRot = cmds.xform(complista[0], q=True, ws=1, ro=True)
        complist = complista[:-1]
        getlngth = len(getchildlist)
        getdist = getlngth/5

        if len(getchildlist[::getdist])==6:
            for item in getchildlist[::getdist]:
                orderlist.append(item)
        elif len(getchildlist[::getdist])==7:
            for item in  getchildlist[::getdist][1:]:
                orderlist.append(item)
        for index, each in enumerate(orderlist[::-1]):
            gtnum= index
            clsnm = '{}_{}_{}_FK_JNT'.format(side, alpha, gtnum)
            getTranslation = cmds.xform(each, q=True, ws=1, t=True)
            # getRot = cmds.xform(each, q=True, ro=True)
            getCluster=cmds.joint(each, n= clsnm, p = getTranslation)
            crtOnt = cmds.orientConstraint(each, getCluster, mo=0)
            cmds.delete(crtOnt)
            getNewRot = cmds.xform(getCluster,  q=True, ws=1, ro=True)
            cmds.CreateEmptyGroup()
            cmds.rename(cmds.ls(sl=1)[0], getCluster+'_GRP')
            cmds.xform(getCluster+'_GRP', ws=1, t=getTranslation)
            cmds.xform(getCluster+'_GRP', ws=1, ro=getNewRot)
            cmds.parent(getCluster+'_GRP', 'noseFingiesFK_GRP')
            cmds.CreateEmptyGroup()
            cmds.rename(cmds.ls(sl=1)[0], getCluster+'ctl_GRP')
            cmds.xform(getCluster+'ctl_GRP', ws=1, t=getTranslation)
            cmds.xform(getCluster+'ctl_GRP', ws=1, ro=getNewRot)
            cmds.parent(getCluster+'ctl_GRP', getCluster+'_GRP')
            cmds.parent(getCluster, getCluster+'ctl_GRP')
            # bone_collector.append(getCluster)
            grp_bn_coll.append(getCluster+'_GRP')
        for index, each in enumerate(grp_bn_coll[:-1]):
            chld_item = each
            prnt_it = grp_bn_coll[(index + 1) % len(grp_bn_coll)]
            chld_it = chld_item.split('_GRP')[0]
            cmds.parent(prnt_it, chld_it)
        bone_sub_collector = []
        grp_bn_sub_coll = []
        for index, each in enumerate(orderlist[::-1]):
            gtnum= index
            clsnm = '{}_{}_{}_FKsub_JNT'.format(side, alpha, gtnum)
            getTranslation = cmds.xform(each, q=True, ws=1, t=True)
            # getRot = cmds.xform(each, q=True, ro=True)
            getSubCluster=cmds.joint(each, n= clsnm, p = getTranslation)
            crtOnt = cmds.orientConstraint(each, getSubCluster, mo=0)
            cmds.delete(crtOnt)
            getNewRot = cmds.xform(getSubCluster,  q=True, ws=1, ro=True)
            cmds.CreateEmptyGroup()
            cmds.rename(cmds.ls(sl=1)[0], getSubCluster+'_GRP')
            cmds.xform(getSubCluster+'_GRP', ws=1, t=getTranslation)
            cmds.xform(getSubCluster+'_GRP', ws=1, ro=getNewRot)
            cmds.parent(getSubCluster+'_GRP', 'noseFingiesFK_GRP')
            cmds.CreateEmptyGroup()
            cmds.rename(cmds.ls(sl=1)[0], getSubCluster+'ctl_GRP')
            cmds.xform(getSubCluster+'ctl_GRP', ws=1, t=getTranslation)
            cmds.xform(getSubCluster+'ctl_GRP', ws=1, ro=getNewRot)
            cmds.parent(getSubCluster+'ctl_GRP', getSubCluster+'_GRP')
            cmds.parent(getSubCluster, getSubCluster+'ctl_GRP')
            bone_sub_collector.append(getSubCluster)
            grp_bn_sub_coll.append(getSubCluster+'_GRP')
        for index, each in enumerate(grp_bn_sub_coll[:-1]):
            chld_item = each
            prnt_it = grp_bn_sub_coll[(index + 1) % len(grp_bn_sub_coll)]
            chld_it = chld_item.split('_GRP')[0]
            cmds.parent(prnt_it, chld_it)
        ######################
        #####NOW SKIN THE CURVE WITH THE DRIVER JOINTS
        #####################
        cmds.select(fk_curve_skin, bone_sub_collector)
        cmds.skinCluster(tsb=1, bm = 0)
        ##############################
        ######link the twists for control on top and bottom
        #########################
        strt_ik_jnt = '{}_{}_0_FK_JNT'.format(side, alpha)
        end_ik_jnt = '{}_{}_5_FK_JNT'.format(side, alpha)
        multdiv = cmds.createNode('multiplyDivide', n='{}_{}_fk_md'.format(side, alpha))
        pma = cmds.createNode('plusMinusAverage', n='{}_{}_fk_pma'.format(side, alpha))
        cmds.connectAttr('{}.rotateX'.format(strt_ik_jnt), '{}.input1X'.format(multdiv), f=1)
        cmds.connectAttr('{}.outputX'.format(multdiv), '{}.input1D[1]'.format(pma), f=1)
        revnode = cmds.createNode('reverse', n='{}_{}_1_fk_twst_rev'.format(side, alpha))
        cmds.connectAttr( '{}.output1D'.format(pma), '{}.inputX'.format(revnode), f=1)
        cmds.connectAttr('{}.rotateX'.format(end_ik_jnt), '{}.input1D[0]'.format(pma), f=1)
        cmds.setAttr('{}.input2X'.format(multdiv), -1)