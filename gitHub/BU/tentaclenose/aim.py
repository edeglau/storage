
from maya import cmds
import re
cmds.CreateEmptyGroup()
cmds.rename(cmds.ls(sl=1)[0], 'noseFingiesAIM_GRP')
cmds.parent('noseFingiesAIM_GRP', 'setup_GRP')
cmds.CreateEmptyGroup()
cmds.rename(cmds.ls(sl=1)[0], 'noseFingiesAIM_CTRLLOC_GRP')
cmds.parent('noseFingiesAIM_CTRLLOC_GRP', 'control_GRP')
cmds.CreateEmptyGroup()
cmds.rename(cmds.ls(sl=1)[0], 'noseFingiesAIM_SETUPLOC_GRP')
cmds.parent('noseFingiesAIM_SETUPLOC_GRP', 'setup_GRP')
lower_jaw = ['DEF']
C_LWR_FNG_JNT = cmds.duplicate('C_fingieMaskBot_JNT', n='C_lowerFingies_LCL_JNT')[0]
cmds.parent(C_LWR_FNG_JNT, 'setup_GRP')
C_NOSE_JNT = cmds.duplicate('C_fingieMaskTop_JNT', n='C_nose_LCL_JNT')[0]
cmds.parent(C_NOSE_JNT, 'setup_GRP')
nose_SRC = []
jaw_SRC = []

for side in 'LR':
    for alpha in 'ABCDEFG':
        fstjnt_SRC = '{}_noseFingies{}_IKbase_JNT'.format(side, alpha)
        if cmds.objExists('{}_noseFingies{}_IKendSub_JNT'.format(side, alpha)) == True:
            endjnt_SRC = '{}_noseFingies{}_IKendSub_JNT'.format(side, alpha)
            endjnt_SRC_prnt = '{}_noseFingies{}_IKend_JNT'.format(side, alpha)
        else:
            endjnt_SRC = '{}_noseFingies{}_IKend_JNT'.format(side, alpha)
        #################
        ###CREATE THE CURVE
        ################
        mn_curve_dvn = '{}_noseFingies_{}_mn_crv'.format(side, alpha)
        aim_curve_nm ='{}_aim_crv'.format(mn_curve_dvn.split('_mn')[0])
        aim_curve_driver = cmds.duplicate(mn_curve_dvn, n=aim_curve_nm)
        cmds.parent(aim_curve_driver, 'noseFingiesAIM_GRP')
        #################
        ###CREATE THE LOCAL BASE JOINT
        ################
        fstjnt_nm = fstjnt_SRC.split('_IK')[0]+'LCLbase_JNT'.format(alpha)
        fstjnt = cmds.duplicate(fstjnt_SRC, n=fstjnt_nm)[0]
        #################
        ###CREATE THE LOCAL END JOINT
        ################
        if cmds.objExists('{}_noseFingies{}_IKendSub_JNT'.format(side, alpha)) == True:
            endjntik_nm = endjnt_SRC.split('_IK')[0]+'LCLendSub_JNT'.format(alpha)
            endjntikprnt_nm = endjnt_SRC.split('_IK')[0] + 'LCLend_JNT'.format(alpha)
            endjntik = cmds.duplicate(endjnt_SRC, n=endjntik_nm)[0]
            endjntikprnt = cmds.duplicate(endjnt_SRC_prnt, n=endjntikprnt_nm)[0]
        else:
            endjntik_nm = endjnt_SRC.split('_IK')[0]+'LCLend_JNT'.format(alpha)
            endjntik = cmds.duplicate(endjnt_SRC, n=endjntik_nm)[0]
        #################
        ###CREATE THE LOCAL END JOINT
        ################
        getTranslation_strt = cmds.xform(fstjnt, q=True, ws=1, t=True)
        getTranslation_end = cmds.xform(endjntik, q=True, ws=1, t=True)
        getEndRot = cmds.xform(endjntik, q=True, ws=1, ro=True)
        #### this stays above the base joint!
        cmds.CreateEmptyGroup()
        cmds.rename(cmds.ls(sl=1)[0], fstjnt+'AIM_GRP')
        cmds.xform(fstjnt+'AIM_GRP', ws=1, t=getTranslation_strt)
        cmds.xform(fstjnt+'AIM_GRP', ws=1, ro=getEndRot)
        cmds.parent(fstjnt+'AIM_GRP', 'noseFingiesAIM_GRP')
        cmds.parent(fstjnt, fstjnt+'AIM_GRP')
        #this holds the tip - keep this at zero. gonna see if this helps world space - will have to constraint to jaw if it does
        grp_name_forset = '{}_noseFingies{}_IKendSubSetup_GRP'.format(side, alpha)
        cmds.CreateEmptyGroup()
        cmds.rename(cmds.ls(sl=1)[0], grp_name_forset)
        cmds.parent(grp_name_forset, 'noseFingiesAIM_GRP')
        ####collected group - this gets constrained to the skin or jaw or head!!!
        topname = '{}_{}_AIM_GRP'.format(side, alpha)
        cmds.CreateEmptyGroup()
        cmds.rename(cmds.ls(sl=1)[0], topname)
        cmds.xform(topname, ws=1, t=getTranslation_strt)
        cmds.xform(topname, ws=1, ro=getEndRot)
        cmds.parent(topname, 'noseFingiesAIM_GRP')
        cmds.parent(fstjnt+'AIM_GRP', topname)
        ####matrix group - this stays above the END joint
        mtxname = '{}_{}_MTX_GRP'.format(side, alpha)
        cmds.CreateEmptyGroup()
        cmds.rename(cmds.ls(sl=1)[0], mtxname)
        cmds.xform(mtxname, ws=1, t=getTranslation_end)
        cmds.xform(mtxname, ws=1, ro=getEndRot)
        cmds.parent(mtxname, grp_name_forset)
        # cmds.parent(endjntik, mtxname)
        spcname = '{}_{}_SPC_GRP'.format(side, alpha)
        cmds.CreateEmptyGroup()
        cmds.rename(cmds.ls(sl=1)[0], spcname)
        cmds.xform(spcname, ws=1, t=getTranslation_end)
        cmds.xform(spcname, ws=1, ro=getEndRot)
        cmds.parent(spcname, mtxname)
        if cmds.objExists('{}_noseFingies{}_IKendSub_JNT'.format(side, alpha)) == True:
            cmds.parent(endjntikprnt, spcname)
            cmds.parent(endjntik,endjntikprnt)
        else:
            cmds.parent(endjntik, spcname)
        #######################
        ######################
        ###DRIVE THE IK CONTROLS WITH THE AIM CURVE
        #####################
        objLst=cmds.ls('{}_noseFingies{}?_LCL_IK_JNT_IKGRP'.format(side, alpha))
        ctrlLst=cmds.ls('{}_noseFingies{}?_IKCtl_GRP'.format(side, alpha))
        for selObj, ctrl in map(None, objLst, ctrlLst):
            # getchld = [(each) for each in cmds.listRelatives(selObj, ad=1) if cmds.nodeType(each) == "joint"][0]
            pgetCVpos=cmds.xform(selObj, ws=1, q=1, t=1)
            npC = cmds.createNode("nearestPointOnCurve")
            cmds.setAttr(npC + ".inPosition", pgetCVpos[0], pgetCVpos[1], pgetCVpos[2], type="double3")
            get_hsp=cmds.listRelatives(aim_curve_driver, ad=1, type="nurbsCurve")[0]
            cmds.connectAttr("{}.worldSpace".format(get_hsp), npC + ".inputCurve")
            getpoint = cmds.getAttr(npC + ".position")
            getParam = cmds.getAttr(npC + ".parameter")
            #################LOCAL
            loc = cmds.spaceLocator(n=selObj+'_loc')
            cmds.xform(loc, ws=1, t = pgetCVpos)
            cmds.select(loc, r=1)
            cmds.select(aim_curve_driver, add=1)
            motionPath=cmds.pathAnimation(fractionMode=1, follow=1, followAxis="x", upAxis="y", worldUpType="vector", worldUpVector=[0, 1, 0], inverseUp=0, inverseFront=0, bank=0)
            cmds.disconnectAttr(motionPath+"_uValue.output", motionPath+".uValue")
            getpth=str(motionPath)
            cmds.setAttr(motionPath+".fractionMode", False)
            cmds.setAttr(motionPath+".uValue", getParam)
            cmds.parentConstraint(loc, selObj, mo=1)
            # cmds.parent(loc, 'noseFingiesAIM_GRP')
            cmds.parent(loc,'noseFingiesAIM_SETUPLOC_GRP')
            cmds.setAttr('noseFingiesAIM_SETUPLOC_GRP.v', 0)
            # #################CONTROLLER
            ctrl_loc = cmds.spaceLocator(n=ctrl+'_loc')
            cmds.select(ctrl_loc, r=1)
            cmds.select(aim_curve_driver, add=1)
            motionPath=cmds.pathAnimation(fractionMode=1, follow=1, followAxis="x", upAxis="y", worldUpType="vector", worldUpVector=[0, 1, 0], inverseUp=0, inverseFront=0, bank=0)
            cmds.disconnectAttr(motionPath+"_uValue.output", motionPath+".uValue")
            getpth=str(motionPath)
            cmds.setAttr(motionPath+".fractionMode", False)
            cmds.setAttr(motionPath+".uValue", getParam)
            cmds.parentConstraint(ctrl_loc, ctrl, mo=1)
            cmds.parent(ctrl_loc, 'noseFingiesAIM_CTRLLOC_GRP')
            cmds.setAttr('noseFingiesAIM_CTRLLOC_GRP.v', 0)
            cmds.delete(npC)
        ######################
        ###NOW SKIN THE CURVE WITH THE DRIVER AIM JOINTS
        #####################
        boneik_collector = []
        boneik_collector.append(fstjnt)
        boneik_collector.append(endjntik)
        cmds.select(aim_curve_driver, boneik_collector)
        cmds.skinCluster(tsb=1, bm = 0)
