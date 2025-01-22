from maya import cmds
import re
'''This will create the attributes for the bending and connect them'''
cmds.CreateEmptyGroup()
cmds.rename(cmds.ls(sl=1)[0], 'noseFingies_GRP')
cmds.parent('noseFingies_GRP', 'setup_GRP')
cmds.CreateEmptyGroup()
cmds.rename(cmds.ls(sl=1)[0], 'skinJnts_GRP')
cmds.parent('skinJnts_GRP', 'noseFingies_GRP')
pxmty_msh_lcl = 'techmesh_:lip_msh'
pxmty_msh_wld = 'lip_ctrl_msh'
jntgrp = []
lower_jaw = ['DEF']
for side in 'LR':
    for alpha in 'ABCDEFG':
        fstjnt_o = '{}_noseFingies_{}_1_JNT'.format(side, alpha)
        fstjnt = cmds.duplicate(fstjnt_o, rc=1)
        cmds.joint(fstjnt, e=1, children =1, zso=1, oj = 'yxz', sao='yup', spa=1)
        jntgrp.append(fstjnt[0])
        cmds.parent(fstjnt[0], 'setup_GRP')
        ######################
        #CREATE THE SPLINE HERE
        #####################
        iknm = '{}{}_IK'.format(side, alpha)
        fstjnt = '{}_noseFingies_{}_1_JNT1'.format(side, alpha)
        getall = cmds.ls('{}_noseFingies_{}_*_JNT1'.format(side, alpha))
        crvnm = '{}_noseFingies_{}_IK_crv'.format(side, alpha)
        gettop = len(getall)
        length = gettop -1
        endjnt = '{}_noseFingies_{}_{}_JNT1'.format(side, alpha, gettop)
        getRot = cmds.xform(endjnt, q=True, ws=1, ro=True) 
        cmds.select(fstjnt, hi=1)
        getchildObj=cmds.ls(sl=1, fl=1)
        hndl = cmds.ikHandle(n = iknm, sj = fstjnt, ee = endjnt,sol = 'ikSplineSolver', scv=0, ns=2, rtm=1, tws = 'easIn')[0]
        getcrv = [(cmds.listRelatives(each, p=1, type = 'transform')[0])for each in cmds.listHistory(hndl) if cmds.nodeType(each) == "nurbsCurve" ][0]
        cmds.delete(hndl)
        cmds.rename(getcrv, crvnm)
        cmds.rebuildCurve( crvnm, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=0, kt=0, s=length, d=1, tol=0.001)
        ######################
        #AIM CURVE
        #####################
        aimcurv_nm = '{}_aim'.format(crvnm)
        cmds.duplicate(crvnm, n=aimcurv_nm)
        cmds.select('{}_aim.cv[*]'.format(crvnm))
        cmds.move(0,0,-.1, r=1, wd =1)
        ##
        getCVs=cmds.ls(crvnm+".cv[*]", fl=1)
        ######################
        #DETERMINE THE PARAMETERS YOU NEED FOR JOINT CONNECTION TO CURVE
        #####################
        for pgetCVpos, each_jnt in map(None, getCVs, getchildObj):
            cmds.parent(each_jnt, 'skinJnts_GRP')
            npC = cmds.createNode("nearestPointOnCurve")
            pcI = cmds.createNode('pointOnCurveInfo')
            transformWorldMatrix = cmds.xform(pgetCVpos, q=True, wd=1, t=True)
            cmds.setAttr(npC + ".inPosition", transformWorldMatrix[0], transformWorldMatrix[1], transformWorldMatrix[2], type="double3") 
            get_hsp=cmds.listRelatives(crvnm, ad=1, type="nurbsCurve")[0]
            cmds.connectAttr("{}.worldSpace".format(get_hsp), npC + ".inputCurve")
            getpoint = cmds.getAttr(npC + ".position")
            getParam = cmds.getAttr(npC + ".parameter")
            cmds.delete(npC)
            ######################
            #DECIDE WHICH TYPE OF CONNECTION TO CURVE HERE YOU WOULD LIKE
            #####################
            # cmds.connectAttr("{}.worldSpace".format(get_hsp), pcI + ".inputCurve")
            # cmds.connectAttr( pcI + ".position", "{}.t".format(each_jnt))
            # cmds.setAttr(pcI + ".parameter", getParam)
            cmds.select(each_jnt, r=1)
            cmds.select(crvnm, add=1)            
            if 'R_' in each_jnt:
                print "reverse it"
                motionPath=cmds.pathAnimation(n='{}_mp'.format(each_jnt) , fractionMode=1, follow=1, followAxis="x", upAxis="y", worldUpType="1", worldUpVector=[0, -1, 0], inverseUp=1, inverseFront=1, bank=0)        
                #cmds.connectAttr('{}_mp'.format(each_jnt) , '{}_aim.worldUpMatrix'.format(crvnm))
            else:
                motionPath=cmds.pathAnimation(n='{}_mp'.format(each_jnt) , fractionMode=1, follow=1, followAxis="x", upAxis="y", worldUpType="1", worldUpVector=[0, 1, 0], inverseUp=0, inverseFront=0, bank=0)        
            cmds.disconnectAttr(motionPath+"_uValue.output", motionPath+".uValue")
            getpth=str(motionPath)
            cmds.setAttr(motionPath+".fractionMode", True)
            cmds.setAttr(motionPath+".uValue", getParam) 
        mn_curve_dvn ='{}_mn_crv'.format(crvnm)
        cmds.duplicate(crvnm, n=mn_curve_dvn)
        cmds.rebuildCurve( mn_curve_dvn, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=0, kt=0, s=6, d=2, tol=0.001)
        wrnm = '{}_wr'.format(crvnm)
        cmds.wire(aimcurv_nm, w=mn_curve_dvn,n=wrnm, gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
        cmds.wire(crvnm, w=mn_curve_dvn,n=wrnm, gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
        fk_curve_driver ='{}_fk_crv'.format(crvnm)
        cmds.duplicate(mn_curve_dvn, n=fk_curve_driver)
        def_name = '{}_fk_bsp'.format(crvnm)
        cmds.blendShape(fk_curve_driver, mn_curve_dvn, origin = 'world',n=def_name, w=(0, 1.0))
        cmds.parent(fk_curve_driver, 'noseFingies_GRP')
        cmds.parent(mn_curve_dvn, 'noseFingies_GRP')
        cmds.parent(crvnm, 'noseFingies_GRP')
        cmds.parent(aimcurv_nm, 'noseFingies_GRP')
        ######################
        #NOW CREATE A JOINT AT EACH CV AT EACH PONT OF THE CURVE. CREATE SOME GROUPS FOR THE JOINT TO LIVE IN. ORGANIZE INTO SETUP
        #####################
        bone_collector = []
        grp_bn_coll = []
        getfkCVs=cmds.ls(fk_curve_driver+".cv[*]", fl=1)
        for each in getfkCVs:
            getnumprt1 = each.split('.cv[')[-1]
            gtnum= getnumprt1.split(']')[0]
            clsnm = '{}_{}_{}_JNT'.format(side, alpha, gtnum)
            getTranslation = cmds.xform(each, q=True, ws=1, t=True)  
            getCluster=cmds.joint(each, n= clsnm, p = getTranslation, o=getRot)
            cmds.CreateEmptyGroup()
            cmds.rename(cmds.ls(sl=1)[0], getCluster+'_GRP')
            cmds.xform(getCluster+'_GRP', ws=1, t=getTranslation)
            cmds.xform(getCluster+'_GRP', ws=1, ro=getRot)
            cmds.parent(getCluster+'ctl_GRP', getCluster+'_GRP')
            cmds.parent(getCluster, getCluster+'ctl_GRP')
            bone_collector.append(getCluster)
            grp_bn_coll.append(getCluster+'_GRP')
        for index, each in enumerate(grp_bn_coll[:-1]):
            chld_item = each
            prnt_it = grp_bn_coll[(index + 1) % len(grp_bn_coll)]
            chld_it = chld_item.split('_GRP')[0]
            cmds.parent(prnt_it, chld_it)
        ######################
        #NOW SKIN THE CURVE WITH THE DRIVER JOINTS
        #####################
        cmds.select(fk_curve_driver, bone_collector)
        cmds.skinCluster(tsb=1, bm = 0)        getgrp = cmds.ls('?_?_0_JNT_GRP') 
        getctlgrp = cmds.ls('?_noseFingies?Control_GRP') 
        for each_part in getgrp:
            if '_D_' in each_part or '_E_' in each_part or '_F_' in each_part:
                cmds.parentConstraint('C_jawLocal_JNT',each_part, mo=1)
        getgrp = cmds.ls('?_?_0_JNT_GRP') 
        for each_part in getctlgrp:
            if 'noseFingiesDControl' in each_part or 'noseFingiesEControl' in each_part or 'noseFingiesFControl' in each_part:
                cmds.parentConstraint('C_jawWorld_JNT',each_part, mo=1)

