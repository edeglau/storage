from maya import cmds
import re


cmds.addAttr('visibilityControl_GRP', ln='noseFingiesVis', at="enum", en='off:on', k=1, nn='noseFingiesVis')
cmds.addAttr('visibilityControl_GRP', ln='noseFingiesIK2', at="enum", en='off:on', k=1, nn='noseFingiesIK2')
cmds.addAttr('visibilityControl_GRP', ln='noseFingiesFK2', at="enum", en='off:on', k=1, nn='noseFingiesFK2')
cmds.deleteAttr('C_fingieMaskTop_CTL', at = "stretch")
'''this will connect the controllers directly to the groups that control the joints that drive the curve'''
diction = {1:[0], 2:[1], 3:[2], 4:[3], 5:[4], 6:[5]}
attrs = ['rx', 'ry', 'rz', 'tx', 'ty', 'tz', 'sx', 'sy', 'sz']

t_to_hide = [ 'tx', 'ty', 'tz']
####################
#Delete etraneous attributes from the visibility group that will later be replaced with a single
###################
getNames = [(each+"."+item) for each in cmds.ls('visibilityControl_GRP')for item in cmds.listAttr(each, w=1,hd=1, s=1, m=0) if '_______' in item]
for each in getNames:
    cmds.setAttr(each, l=0)
    cmds.deleteAttr(each.split('.')[0], at = each.split('.')[-1])

nose_loc= 'C_nose_MAIN_loc'
# cmds.rename(cmds.ls(sl=1)[0], nose_loc)
getTranslation_nose = cmds.xform('C_nose_LCL_JNT', ws=1, q=1, t=1)
getEndRot_nose = cmds.xform('C_nose_LCL_JNT', ws=1, q=1, ro=1)
cmds.spaceLocator(n = nose_loc)
cmds.xform(nose_loc, ws=1, t=getTranslation_nose)
cmds.xform(nose_loc, ws=1, ro=getEndRot_nose)
cmds.parent(nose_loc, 'C_nose_CTL')

nose_HT_loc= 'C_nose_HITCH_loc'
# cmds.rename(cmds.ls(sl=1)[0], nose_loc)
getTranslation_nose = cmds.xform('C_nose_LCL_JNT', ws=1, q=1, t=1)
getEndRot_nose = cmds.xform('C_nose_LCL_JNT', ws=1, q=1, ro=1)
cmds.spaceLocator(n = nose_HT_loc)
cmds.xform(nose_HT_loc, ws=1, t=getTranslation_nose)
cmds.xform(nose_HT_loc, ws=1, ro=getEndRot_nose)
cmds.parent(nose_HT_loc, 'C_fingieTopHitch_CTL')

hitch_loc = 'C_hitchMAIN_loc'
# cmds.CreateEmptyGroup()
# cmds.rename(cmds.ls(sl=1)[0], hitch_loc)
getTranslation_low = cmds.xform('C_lowerFingies_LCL_JNT', ws=1, q=1, t=1)
getEndRot_low = cmds.xform('C_lowerFingies_LCL_JNT', ws=1, q=1, ro=1)
cmds.spaceLocator(n = hitch_loc)
cmds.xform(hitch_loc, ws=1, t=getTranslation_low)
cmds.xform(hitch_loc, ws=1, ro=getEndRot_low)
cmds.parent(hitch_loc,'C_fingieBotHitch_CTL')

low_loc = 'C_lowerMAIN_loc'
# cmds.CreateEmptyGroup()
# cmds.rename(cmds.ls(sl=1)[0], low_loc)
cmds.spaceLocator(n = low_loc)
cmds.xform(low_loc, ws=1, t=getTranslation_low)
cmds.xform(low_loc, ws=1, ro=getEndRot_low)
cmds.parent(low_loc, 'C_lowerFingies_CTL')
###constrain for low fingies to jaw
# #####cmds.rename('transform1', 'C_lowerFingies_SETUP_GRP')


###group the upper fingies controller in local space to local jaw
localnosename = 'C_nose_SETUP_GRP'
cmds.CreateEmptyGroup()
cmds.rename(cmds.ls(sl=1)[0], localnosename)
getTranslation_nose = cmds.xform('C_nose_LCL_JNT', ws=1, q=1, t=1)
getEndRot_nose = cmds.xform('C_nose_LCL_JNT', ws=1, q=1, ro=1)
cmds.xform(localnosename, ws=1, t=getTranslation_nose)
cmds.xform(localnosename, ws=1, ro=getEndRot_nose)
cmds.parent('C_nose_LCL_JNT', localnosename)
# ######cmds.parent(localnosename, 'setup_GRP')
###group the upper fingies controller in local space to local jaw
mnnosename = 'C_nose_mn_SETUP_GRP'
cmds.CreateEmptyGroup()
cmds.rename(cmds.ls(sl=1)[0], mnnosename)
cmds.xform(mnnosename, ws=1, t=getTranslation_nose)
cmds.xform(mnnosename, ws=1, ro=getEndRot_nose)
cmds.parent(localnosename, mnnosename)
# ####cmds.parent(localnosename, 'setup_GRP')
spcnosename = 'C_nose_spc_SETUP_GRP'
cmds.CreateEmptyGroup()
cmds.rename(cmds.ls(sl=1)[0], spcnosename)
cmds.parent(mnnosename, spcnosename)
cmds.parent(spcnosename, 'setup_GRP')
###group the upper fingies controller in local space to local jaw
localnosename = 'C_lowerFingies_SETUP_GRP'
cmds.CreateEmptyGroup()
cmds.rename(cmds.ls(sl=1)[0], localnosename)
getTranslation_nose = cmds.xform('C_lowerFingies_LCL_JNT', ws=1, q=1, t=1)
getEndRot_nose = cmds.xform('C_lowerFingies_LCL_JNT', ws=1, q=1, ro=1)
cmds.xform(localnosename, ws=1, t=getTranslation_nose)
cmds.xform(localnosename, ws=1, ro=getEndRot_nose)
cmds.parent('C_lowerFingies_LCL_JNT', localnosename)
# cmds.parent(localnosename, 'setup_GRP')
###group the upper fingies controller in local space to local jaw
mnnosename = 'C_lowerFingies_mn_SETUP_GRP'
cmds.CreateEmptyGroup()
cmds.rename(cmds.ls(sl=1)[0], mnnosename)
cmds.xform(mnnosename, ws=1, t=getTranslation_nose)
cmds.xform(mnnosename, ws=1, ro=getEndRot_nose)
cmds.parent(localnosename, mnnosename)
spcnosename = 'C_lowerFingies_spc_SETUP_GRP'
cmds.CreateEmptyGroup()
cmds.rename(cmds.ls(sl=1)[0], spcnosename)
cmds.parent(mnnosename, spcnosename)
cmds.parent(spcnosename, 'setup_GRP')

# cmds.parent('lip_ctrl_msh','control_GRP')

for attr in attrs:
    # ######################
    # #this direct connects between the nose controls
    # ######################
    try:
        cmds.connectAttr('C_lowerMAIN_loc.{}'.format(attr), 'C_lowerFingies_LCL_JNT.{}'.format(attr), f=1)
        cmds.connectAttr('C_nose_MAIN_loc.{}'.format( attr), 'C_nose_LCL_JNT.{}'.format(attr), f=1)
    except:
        pass


######local constraints
cmds.parentConstraint('C_headLocal_JNT', 'C_nose_SETUP_GRP', mo=1)
cmds.parentConstraint('C_jawLocal_JNT', 'C_lowerFingies_SETUP_GRP', mo=1)

smth_ctrl ='C_fingieMaskBot_CTL'
for side in 'LR':
    for alpha in 'ABCDEFG':
        try:
            if alpha != 'G':
                cmds.addAttr(smth_ctrl, ln='{}{}_smth_bsp'.format(side, alpha), min=0.0, max = 1.0, at="float", k=1, nn='{}{}_smth_bsp'.format(side, alpha), dv=0.0)
                cmds.connectAttr('{}.{}{}_smth_bsp'.format(smth_ctrl, side, alpha), '{}{}_blendShape_render_primary_default_default_cHeadPolyDelete_BLS.envelope'.format(side, alpha), f=1)
                cmds.connectAttr('{}.{}{}_smth_bsp'.format(smth_ctrl, side, alpha), '{}{}_blendShape_render_primary_default_topology_cHeadPolyDelete_BLS.envelope'.format(side, alpha), f=1)
        except:
            pass
        #cmds.connectAttr('C_fingieMaskTop_CTL.{}{}_smth_bsp'.format(side, alpha), '{}{}_blendShape_render_primary_default_default_cHeadPolyDelete_BLS.envelope'.format(side, alpha), f=1)
        revnode = cmds.createNode('reverse', n='{}_{}_1_bsp_rev'.format(side, alpha))
        cmds.setAttr('{}_noseFingies{}_IKbase_JNT.visibility'.format(side, alpha), 0)
        # for tra in t_to_hide:
        #     cmds.setAttr('{}_noseFingies{}1_CTL.{}'.format(side, alpha, tra), k=0, cb=0, l=1)
        try:
            ##############################
            #This connects the  aim for the length of the ik chains
            ################################
            cmds.aimConstraint('{}_noseFingies{}_IKend_CTL'.format(side, alpha), '{}_noseFingies{}1_IK_SDWCH_Grp'.format(side, alpha), mo=1)
            cmds.aimConstraint('{}_{}_IK_AIM_JNT'.format(side, alpha), '{}_{}_IKCtl_GRP'.format(side, alpha), mo=1)
        except:
            pass
        cmds.addAttr('C_fingieMaskTop_CTL', ln='{}{}_FKactive'.format(side, alpha), min=-0, max=1, at="float", k=1, nn='{}{}_FKactive'.format(side, alpha), dv=1)
        try:
            ########################
            #This connects the blend from ik to fk joint chains on the fingies to the mask controller
            ####################################
            cmds.connectAttr("C_fingieMaskTop_CTL.{}{}_FKactive".format(side, alpha), '{}_noseFingies_{}_FK_bsp.envelope'.format(side, alpha))
            cmds.connectAttr("C_fingieMaskTop_CTL.{}{}_FKactive".format(side, alpha), '{}.inputX'.format(revnode), f=1)
            cmds.connectAttr('{}.outputX'.format(revnode), '{}_noseFingies_{}_IK_bsp.envelope'.format(side, alpha), f=1)
            cmds.connectAttr('{}.outputX'.format(revnode),'{}_noseFingies{}_IKend_CTL_CRVShape.visibility'.format(side, alpha), f=1)
            cmds.connectAttr('{}.outputX'.format(revnode),'{}_noseFingies{}_IKendSub_CTL_CRVShape.visibility'.format(side, alpha), f=1)
        except:
            pass
        try:
            ########################
            #This connects the offset curve to take on the orientation of the active controls
            ####################################
            cmds.connectAttr("C_fingieMaskTop_CTL.{}{}_FKactive".format(side, alpha), '{}_noseFingies_{}_mn_crv_ofst_fk_bsp.envelope'.format(side, alpha))
            cmds.connectAttr('{}.outputX'.format(revnode),
                             '{}_noseFingies_{}_mn_crv_ofst_ik_bsp.envelope'.format(side, alpha))
        except:
            pass
        try:
            cmds.setAttr('{}_noseFingies{}_IKendSub2_CTL.visibility'.format(side, alpha), l=0)
            cmds.connectAttr('visibilityControl_GRP.noseFingiesIK2', '{}_noseFingies{}_IKendSub2_CTL.visibility'.format(side, alpha), f=1)
        except:
            pass
        for x in xrange(1,7):
            #############################3
            #this switches the visibility template for both sets of the fk ik chain controllers
            ######################################
            cmds.connectAttr('{}.outputX'.format(revnode),'{}_noseFingies{}{}_IK_CTL_CRVShape.visibility'.format(side, alpha, x), f=1)
            try:
                cmds.connectAttr("C_fingieMaskTop_CTL.{}{}_FKactive".format(side, alpha), '{}_noseFingies{}{}Ctl_GRP.visibility'.format(side, alpha, x), f=1)
            except:
                pass
            try:
                cmds.setAttr('{}_noseFingies{}{}_IK2_CTL.visibility'.format(side, alpha, x), l=0)
                cmds.setAttr('{}_noseFingies{}{}sub_CTL.visibility'.format(side, alpha, x), l=0)
            except:
                pass
            cmds.connectAttr('visibilityControl_GRP.noseFingiesIK2', '{}_noseFingies{}{}_IK2_CTL.visibility'.format(side, alpha, x), f=1)
            cmds.connectAttr('visibilityControl_GRP.noseFingiesVis', '{}_noseFingies{}{}_CTL_CRVShape.visibility'.format(side, alpha, x), f=1)
            cmds.connectAttr('visibilityControl_GRP.noseFingiesFK2', '{}_noseFingies{}{}sub_CTL_CRVShape.visibility'.format(side, alpha, x), f=1)
        #############################
        # #####DIRECT CONNECT HERE!!!!!
        ########################
        for attr in attrs:
            ###################
            #DIRECT CONNECT CTRLR TO FK JOINTS
            ################
            for x in xrange(0, 6):
                ctl_x = x+1
                cmds.connectAttr('{}_noseFingies{}{}_CTL.{}'.format(side, alpha, ctl_x, attr), '{}_{}_{}_FKsub_JNTctl_GRP.{}'.format(side, alpha, x, attr), f=1)
            for x in xrange(1, 7):
                cmds.connectAttr('{}_noseFingies{}{}_CTL.{}'.format(side, alpha, x, attr), '{}_{}_{}_FK_JNT.{}'.format(side, alpha, str(x-1), attr), f=1)
                cmds.connectAttr('{}_noseFingies{}{}sub_CTL.{}'.format(side, alpha, x, attr),  '{}_{}_{}_FKsub_JNT.{}'.format(side, alpha, str(x - 1), attr), f=1)
            for key, value in diction.items():
                for val in value:
                    try:
                        cmds.connectAttr('{}_noseFingies{}{}_CTL.{}'.format(side, alpha, str(val), attr), '{}_noseFingies{}{}sub_SDWCH_Grp.{}'.format(side, alpha, str(val), attr), f=1)
                    except:
                        pass
            ###################
            #DIRECT CONNECT CTRLR TO IK JOINTS
            ################
            for key, value in diction.items():
                for val in value:
                    try:
                        ####drive the IK curve driver joints with controllers
                        #cmds.parent('{}_{}_{}_JNT'.format(side, alpha, str(val)), '{}_noseFingies{}{}_CTL'.format(side, alpha, str(key)))
                        cmds.connectAttr('{}_noseFingies{}{}_IK_CTL.{}'.format(side, alpha, str(key), attr), '{}_noseFingies{}{}_LCL_IK_JNT.{}'.format(side, alpha, str(key), attr), f=1)
                    except:
                        pass
            # ######################
            # #this direct connects between the aim controller to the local joint
            # ######################
            try:
                if cmds.objExists('{}_noseFingies{}_IKendSub_CTL'.format(side, alpha) )== True:
                    cmds.connectAttr('{}_noseFingies{}_IKendSub_CTL.{}'.format(side, alpha,  attr), '{}_noseFingies{}LCLendSub_JNT.{}'.format(side, alpha,  attr), f=1)
                    cmds.connectAttr('{}_noseFingies{}_IKend_CTL.{}'.format(side, alpha,  attr), '{}_noseFingies{}LCLend_JNT.{}'.format(side, alpha,  attr), f=1)
                else:
                    cmds.connectAttr('{}_noseFingies{}_IKend_CTL.{}'.format(side, alpha,  attr), '{}_noseFingies{}LCLend_JNT.{}'.format(side, alpha,  attr), f=1)
                    cmds.connectAttr('{}_noseFingies{}_IKbase_CTL.{}'.format(side, alpha,  attr), '{}_noseFingies{}LCLbase_JNT.{}'.format(side, alpha,  attr), f=1)
            except:
                pass
        ###################
        ######Set the all nose fingie visibilities to only 1 attribute on the face
        ######################
        cmds.setAttr("visibilityControl_GRP.{}_noseFingies{}1".format(side, alpha), 1)
        cmds.deleteAttr('visibilityControl_GRP', at = "{}_noseFingies{}1".format(side, alpha))
        cmds.deleteAttr('visibilityControl_GRP', at = "{}_noseFingies{}_IK1".format(side, alpha))
        # cmds.deleteAttr('visibilityControl_GRP', at = "{}_noseFingies{}1".format(side, alpha))
        # cmds.deleteAttr('visibilityControl_GRP', at = "{}_noseFingies{}x2".format(side, alpha))
        cmds.deleteAttr('visibilityControl_GRP', at = "{}_noseFingies{}_IKend1".format(side, alpha))
        cmds.deleteAttr('visibilityControl_GRP', at = "{}_noseFingies{}_IKend2".format(side, alpha))
        cmds.deleteAttr('visibilityControl_GRP', at = "{}_noseFingies{}_IK2".format(side, alpha))
        # for x in xrange(1, 7):
        #     cmds.connectAttr('visibilityControl_GRP.noseFingiesVis', '{}_noseFingies{}{}_CTL_CRVShape.v'.format(side, alpha, x))
        cmds.connectAttr('visibilityControl_GRP.noseFingiesVis', '{}_noseFingies{}_IKControl_GRP.v'.format(side, alpha))
        cmds.connectAttr('visibilityControl_GRP.noseFingiesVis', '{}_noseFingies{}_IKendControl_GRP.v'.format(side, alpha))
        ####

        ######################
        #CONNECT FK TO JAW - remove this when you do a proximity attach
        #####################
        getgrp = cmds.ls('?_?_0_FK_JNT_GRP')
        getctlgrp = cmds.ls('?_noseFingies?Control_GRP')
        for each_part in getgrp:
            if '_D_' in each_part or '_E_' in each_part or '_F_' in each_part:
                cmds.parentConstraint('C_jawLocal_JNT',each_part, mo=1)
        for each_part in getctlgrp:
            if 'noseFingiesDControl' in each_part or 'noseFingiesEControl' in each_part or 'noseFingiesFControl' in each_part:
                cmds.parentConstraint('C_jawWorld_JNT',each_part, mo=1)

        ######################
        #CONNECT IK TO JAW - remove this when you do a proximity attach
        #####################
        getgrp = cmds.ls('?_?_0_JNT_GRP')
        getikctlgrp = cmds.ls('?_noseFingies?_IKControl_GRP')
        for each_part in getikctlgrp:
            if 'noseFingiesD_IKControl' in each_part or 'noseFingiesE_IKControl' in each_part or 'noseFingiesF_IKControl' in each_part:
                cmds.parentConstraint('C_jawWorld_JNT',each_part, mo=1)



        #####
        ##This changes when linked to skin
        ####
        getgrp = cmds.ls('?_?_AIM_GRP')
        for index, each_part in enumerate(getgrp):
            if '_D_' in each_part or '_E_' in each_part or '_F_' in each_part:
                cmds.parentConstraint('C_jawLocal_JNT',each_part, mo=1)


        #######
        ####This is for the space switch on single fingies.
        #######
        getgrp = cmds.ls('?_?_MTX_GRP')
        for index, each_part in enumerate(getgrp):
            if '_D_' in each_part or '_E_' in each_part or '_F_' in each_part:
                cmds.parentConstraint('C_lowerFingies_LCL_JNT',each_part, mo=1)
                # cmds.parentConstraint('C_jawLocal_JNT',each_part, mo=1)####this is for the space switch on individuals
            else:
                cmds.parentConstraint('C_nose_LCL_JNT',each_part, mo=1)
                # cmds.parentConstraint('C_headLocal_JNT',each_part, mo=1)####this is for the space switch on individuals

        ns_selection = [
            'C_nose_HITCH_loc',
            'L_noseFingiesA_IKendCtl_GRP',
            'L_noseFingiesB_IKendCtl_GRP',
            'L_noseFingiesC_IKendCtl_GRP',
            'L_noseFingiesG_IKendCtl_GRP',
            'R_noseFingiesA_IKendCtl_GRP',
            'R_noseFingiesB_IKendCtl_GRP',
            'R_noseFingiesC_IKendCtl_GRP',
            'R_noseFingiesG_IKendCtl_GRP',
        ]
        for each in ns_selection[1:]:
            cmds.parentConstraint(ns_selection[0], each, mo=1)
        jw_selection = [
            'C_hitchMAIN_loc',
            'L_noseFingiesD_IKendCtl_GRP',
            'L_noseFingiesE_IKendCtl_GRP',
            'L_noseFingiesF_IKendCtl_GRP',
            'R_noseFingiesD_IKendCtl_GRP',
            'R_noseFingiesE_IKendCtl_GRP',
            'R_noseFingiesF_IKendCtl_GRP',
        ]
        for each in jw_selection[1:]:
            cmds.parentConstraint(jw_selection[0], each, mo=1)

