from maya import cmds
import re
'''create the controller groups required for the bending functions'''
for side in 'LR':
    for alpha in 'ABCDEFG':
        ikeach ='{}_noseFingies{}1_IKCtl_GRP'.format(side, alpha)
        transform=cmds.xform(ikeach , q=True, ws=1, t=True)
        if transform==[0, 0, 0]:
            transformWorldMatrix = cmds.xform(ikeach, q=True, wd=1, sp=True)
            rotateWorldMatrix = cmds.xform(ikeach, q=True, wd=1, ra=True)
        else:
            transformWorldMatrix = cmds.xform(ikeach, q=True, ws=1, t=True)
            rotateWorldMatrix = cmds.xform(ikeach, q=True, ws=1, ro=True)
        ikname=ikeach.split("Ctl")[0]+"_SDWCH_Grp"
        ikselObjParentnxt=[(item) for item in cmds.listRelatives( ikeach, allParents=True ) if cmds.nodeType(item) == 'transform']
        ikset_prnt = ikselObjParentnxt[0]
        cmds.CreateEmptyGroup()
        cmds.rename(cmds.ls(sl=1)[0], ikname)
        cmds.xform(ikname, ws=1, t=transformWorldMatrix)
        cmds.xform(ikname, ws=1, ro=rotateWorldMatrix)
        cmds.parent(ikname, ikset_prnt)
        for x in xrange(1,7):
            try:
                each = '{}_noseFingies{}{}subCtl_GRP'.format(side, alpha, x)
                transformWorldMatrix=cmds.xform(each , q=True, ws=1, t=True)
                rotateWorldMatrix = cmds.xform(each, q=True, ws=1, ro=True)
                name=each.split("Ctl")[0]+"_SDWCH_Grp"
                selObjParentnxt=[(item) for item in cmds.listRelatives( each, allParents=True ) if cmds.nodeType(item) == 'transform']
                selObjchldnxt=[(item) for item in cmds.listRelatives( each, c=True ) if cmds.nodeType(item) == 'transform']
                set_prnt = selObjParentnxt[0]
                set_chld = selObjchldnxt[0]
                cmds.CreateEmptyGroup()
                cmds.rename(cmds.ls(sl=1)[0], name)
                cmds.xform(name, ws=1, t=transformWorldMatrix)
                cmds.xform(name, ws=1, ro=rotateWorldMatrix)
                cmds.parent(name, each)
                cmds.makeIdentity(name, apply=1, r=1, s=1, t=1, pn=1, n=0)
                if set_chld:
                    cmds.parent(set_chld, name)
            except:
                pass
            try:#now do the ik ctrls
                eachctl ='{}_noseFingies{}{}_IKCtl_GRP'.format(side, alpha, x)
                cmds.parent(eachctl, ikname)
            except:
                pass