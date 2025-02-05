
from maya import cmds
import re
microLeadCurve = 'techmesh_:lip_crv'
cmds.CreateEmptyGroup()
cmds.rename(cmds.ls(sl=1)[0], 'beardFingiesFK_GRP')
cmds.parent('beardFingiesFK_GRP', 'setup_GRP')
attrs = ['rx', 'ry', 'rz', 'tx', 'ty', 'tz', 'sx', 'sy', 'sz']
for side in 'LR':
    for alpha in 'ABC':
        for gtnum in xrange(1,4):
            each = '{}_beardFingies{}{}_JNT'.format(side, alpha, gtnum)
            clsnm = '{}_beardFingies{}{}_LCL_JNT'.format(side, alpha, gtnum)
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
            if '2_LCL_JNT' in getCluster:
                cmds.parent(getCluster+'_GRP', '{}_beardFingies{}1_LCL_JNT'.format(side, alpha))
            elif '3_LCL_JNT' in getCluster:
                cmds.parent(getCluster+'_GRP', '{}_beardFingies{}2_LCL_JNT'.format(side, alpha))
            else:
                cmds.parent(getCluster+'_GRP', 'beardFingiesFK_GRP')
            cmds.CreateEmptyGroup()
            cmds.rename(cmds.ls(sl=1)[0], getCluster+'ctl_GRP')
            cmds.xform(getCluster+'ctl_GRP', ws=1, t=getTranslation)
            cmds.xform(getCluster+'ctl_GRP', ws=1, ro=getNewRot)
            cmds.parent(getCluster+'ctl_GRP', getCluster+'_GRP')
            cmds.parent(getCluster, getCluster+'ctl_GRP')
            for attr in attrs:
                cmds.connectAttr('{}_beardFingies{}{}_CTL.{}'.format(side, alpha, gtnum, attr),
                                 '{}_beardFingies{}{}_LCL_JNT.{}'.format(side, alpha, gtnum, attr), f=1)
        ########joint
        selObj = '{}_beardFingies{}1_LCL_JNT'.format(side, alpha)
        pgetCVpos = cmds.xform(selObj, ws=1, q=1, t=1)
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
        #####attach
        cmds.scaleConstraint(lc, '{}_beardFingies{}1_LCL_JNT_GRP'.format(side, alpha), mo=1)
        cmds.parentConstraint(lc,'{}_beardFingies{}1_LCL_JNT_GRP'.format(side, alpha), mo=1)
        cmds.parentConstraint(splc,'{}_beardFingies{}1Ctl_GRP'.format(side, alpha), mo=1)
        cmds.scaleConstraint('techMesh_geometryStack_fk_ctl_GRP', '{}_beardFingies{}1Ctl_GRP'.format(side, alpha), mo=1)
        #######################visibility
        cmds.connectAttr("visibilityControl_GRP.lipTweaker_sculptlipBeard", "{}_beardFingies{}1Ctl_GRP.v".format(side, alpha), f=1)



getNames = [(each+"."+item) for each in cmds.ls('visibilityControl_GRP')for item in cmds.listAttr(each, w=1,hd=1, s=1, m=0) if 'beard' in item]
for each in getNames:
    cmds.setAttr(each, l=0)
    cmds.deleteAttr(each.split('.')[0], at = each.split('.')[-1])

