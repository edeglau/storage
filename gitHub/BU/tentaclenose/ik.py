from maya import cmds
import re
cmds.CreateEmptyGroup()
cmds.rename(cmds.ls(sl=1)[0], 'noseFingiesIK_GRP')
cmds.parent('noseFingiesIK_GRP', 'setup_GRP')
pxmty_msh_lcl = 'techmesh_:lip_msh'
pxmty_msh_wld = 'lip_ctrl_msh'
jntgrp = []
lower_jaw = ['DEF']
cmds.addAttr('C_fingieMaskTop_CTL', ln='stretch', min=-0, max=0.2, at="float", k=1, nn='stretch', dv=0.1)
for side in 'LR':
    for alpha in 'ABCDEFG':
        mn_curve_dvn = '{}_noseFingies_{}_mn_crv'.format(side, alpha)
        ik_curve_driver ='{}_ik_drv_crv'.format(mn_curve_dvn.split('_mn')[0])
        cmds.duplicate(mn_curve_dvn, n=ik_curve_driver)
        cmds.parent(ik_curve_driver, 'noseFingiesIK_GRP')
        ####################IKhandle for less flip
        fstjnt_o = '{}_noseFingies_{}_1_JNT1'.format(side, alpha)
        cmds.duplicate(fstjnt_o, rc=1)
        fstjnt2 = '{}_noseFingies_{}_1_JNT2'.format(side, alpha)
        getall = cmds.ls('{}_noseFingies_{}_*_JNT2'.format(side, alpha))
        crvnm = '{}_noseFingies_{}_crv'.format(side, alpha)
        gettop = len(getall)
        length = gettop -1
        endjnt2 = '{}_noseFingies_{}_{}_JNT2'.format(side, alpha, gettop)
        iknm = '{}{}_mn_IK'.format(side, alpha)
        newhndl = cmds.ikHandle(n = iknm, sj = fstjnt2, ee = endjnt2,sol = 'ikSplineSolver', c = ik_curve_driver, ccv=0, roc=0, snc = 0, pcv =0,  rtm=1, cra = 1, tws = 'easIn')[0]
        cmds.parent(newhndl, 'noseFingies_GRP')
        tsfm_nm ='{}_{}_curve_trsfrm'.format(side, alpha)
        cmds.rename('transform1', tsfm_nm)
        cmds.parent(tsfm_nm, 'noseFingiesIK_GRP')
        cmds.select(tsfm_nm, r=1)
        cmds.select(ik_curve_driver, add=1)
        motionPath=cmds.pathAnimation(fractionMode=1, follow=1, followAxis="x", upAxis="y", worldUpType="object", bank=0, wuo= tsfm_nm)
        cmds.setAttr(motionPath+".fractionMode", False)
        cmds.setAttr(motionPath+".uValue", 0)
        offset_cv = 'offset_{}'.format(ik_curve_driver)
        cmds.offsetCurve (ik_curve_driver, ch=1, rn=0, cb=2, st =1, cl= 1, cr=0, d= 1.0, tol =0.01, sd=5, ugn=0)
        cmds.rename('offsetNurbsCurve1', offset_cv)
        cmds.parent(offset_cv, 'noseFingiesIK_GRP')
        cmds.setAttr('{}.v'.format(offset_cv), 0)
        ############IK curve blend
        defik_name = '{}_IK_bsp'.format(mn_curve_dvn.split('_mn')[0])
        cmds.blendShape(ik_curve_driver, mn_curve_dvn, origin = 'world',n=defik_name, w=(0, 1.0))
        ######################
        #NOW CREATE A JOINT AT EACH CV AT EACH PONT OF THE CURVE. CREATE SOME GROUPS FOR THE JOINT TO LIVE IN. ORGANIZE INTO SETUP
        #####################
        boneik_collector = []
        #########################
        #CREATE THE BASE GROUP(you'll need this for the aim control later)
        #################################
        orig_jnt = '{}_noseFingies{}1_IK_JNT'.format(side, alpha)
        getTranslation_strt = cmds.xform(orig_jnt, q=True, ws=1, t=True)
        getRot_strt = cmds.xform(orig_jnt, q=True, ws=1, ro=True)
        cmds.CreateEmptyGroup()
        iknameprntname ='{}_{}_IKPrntCtl_GRP'.format(side, alpha)
        cmds.rename(cmds.ls(sl=1)[0], iknameprntname)
        cmds.xform(iknameprntname, ws=1, t=getTranslation_strt)
        cmds.xform(iknameprntname, ws=1, ro=getRot_strt)
        cmds.parent(iknameprntname, 'noseFingiesIK_GRP')
        cmds.CreateEmptyGroup()
        iknamebasename ='{}_{}_IKBASECtl_GRP'.format(side, alpha)
        cmds.rename(cmds.ls(sl=1)[0], iknamebasename)
        cmds.xform(iknamebasename, ws=1, t=getTranslation_strt)
        cmds.xform(iknamebasename, ws=1, ro=getRot_strt)
        cmds.parent(iknamebasename, iknameprntname)
        for gtnum in xrange(1,7):
            ####################BUILD IK JOINTS
            orig_jnt = '{}_noseFingies{}{}_IK_JNT'.format(side, alpha, gtnum)
            getTranslation = cmds.xform(orig_jnt, q=True, ws=1, t=True)
            getRot = cmds.xform(orig_jnt, q=True, ws=1, ro=True)
            clsnmik = orig_jnt.split('_IK_')[0]+'_LCL_IK_JNT'
            getCluster=cmds.duplicate(orig_jnt, n= clsnmik)[0]
            # crtOnt = cmds.orientConstraint(each, getCluster, mo=0)
            # cmds.delete(crtOnt)
            cmds.CreateEmptyGroup()
            cmds.rename(cmds.ls(sl=1)[0], getCluster+'_IKGRP')
            cmds.xform(getCluster+'_IKGRP', ws=1, t=getTranslation)
            cmds.xform(getCluster+'_IKGRP', ws=1, ro=getRot)
            cmds.parent(getCluster+'_IKGRP', iknamebasename)
            cmds.CreateEmptyGroup()
            cmds.rename(cmds.ls(sl=1)[0], getCluster+'ikctl_GRP')
            cmds.xform(getCluster+'ikctl_GRP', ws=1, t=getTranslation)
            cmds.xform(getCluster+'ikctl_GRP', ws=1, ro=getRot)
            cmds.parent(getCluster+'ikctl_GRP', getCluster+'_IKGRP')
            cmds.parent(getCluster, getCluster+'ikctl_GRP')
            boneik_collector.append(getCluster)
        ######################
        #NOW SKIN THE CURVE WITH THE DRIVER JOINTS
        #####################
        cmds.select(ik_curve_driver, boneik_collector)
        cmds.skinCluster(tsb=1, bm = 0)
        # # ##############################
        # # #stretchIK
        # # #########################
        scaleAxis="X"
        getbones = '{}_noseFingies_{}_1_JNT2'.format(side, alpha)
        childBones=cmds.listRelatives(getbones, ad=1, typ="joint")
        alljoints=childBones
        alljoints.append(getbones)#make full list of bones
        curvInf=cmds.arclen(mn_curve_dvn, ch=1)#get shape length
        getDistance=cmds.getAttr(curvInf+".arcLength")
        MultDivNode=cmds.shadingNode( "multiplyDivide", au=1, n=getbones+'_md')
        cmds.connectAttr("{}.arcLength".format(curvInf), "{}.input1.input1{}".format(MultDivNode, scaleAxis), f=1)#
        cmds.setAttr(str(MultDivNode)+".operation", 2)#change to divide
        ConditionNode=cmds.shadingNode( "condition", au=1, n=getbones+"_cond")
        cmds.connectAttr("{}.outputX".format(MultDivNode), "{}.firstTerm".format(ConditionNode), f=1)#
        cmds.connectAttr("{}.firstTerm".format(ConditionNode), "{}.colorIfTrueR".format(ConditionNode), f=1)#
        cmds.setAttr("{}.colorIfFalseR".format(ConditionNode), 1, l=1)#
        cmds.setAttr("{}.operation".format(ConditionNode), 2)#change to greater than
        blnd_clr=cmds.shadingNode( "blendColors", asShader=1, n=getbones+'_bc')
        cmds.connectAttr("C_fingieMaskTop_CTL.stretch".format(side, alpha), '.blender'.format(blnd_clr))
        cmds.connectAttr("{}.outColorR".format(ConditionNode), "{}.color1R".format(blnd_clr), f=1)#
        cmds.setAttr("{}.color2R".format(blnd_clr), 1, l=1)#change to greater than
        cmds.setAttr("{}.input2{}".format(MultDivNode,scaleAxis), getDistance)#set default length on second input of divide
        for each in alljoints[1:-1]:
            md_inv=cmds.shadingNode( "multiplyDivide", au=1, n=each+'_inv_md')
            cmds.connectAttr("{}.scaleX".format(each), ".input2X ".format(md_inv), f=1)
            md_sqr=cmds.shadingNode( "multiplyDivide", au=1, n=each+'_sqr_md')
            cmds.connectAttr("{}.outputX".format(md_inv), ".input1X ".format(md_sqr), f=1)
            cmds.setAttr("{}.operation".format(md_inv), 2)#change to divide
            cmds.setAttr("{}.input1X".format(md_inv), 1, l=1)
            cmds.setAttr("{}.input2X".format(md_sqr), .5, l=1)
            cmds.setAttr("{}.operation".format(md_sqr), 3)#change to divide
            cmds.addAttr(each, ln='stretch_jnt', min=0.1, at="float", k=1, nn='stretch_jnt', dv=1)
            cmds.connectAttr("{}.outputX".format(md_sqr), "{}.scaleY".format(each), f=1)
            cmds.connectAttr("{}.outputX".format(md_sqr), "{}.scaleZ".format(each), f=1)
            cmds.connectAttr("{}.stretch_jnt".format(each), "{}.scaleX".format(each), f=1)
            cmds.connectAttr("{}.outputR".format(blnd_clr), "{}.stretch_jnt".format(each))