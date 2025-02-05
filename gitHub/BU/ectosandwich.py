import maya.cmds as mc


fk_ctrls ={
'C_spineFK1Ctl_GRP':"C_spine1_JNT",
'C_spineFK2Ctl_GRP':"C_spine2_JNT",
'C_spineFK3Ctl_GRP':"C_spine3_JNT",
'C_spineFK4Ctl_GRP':"C_spine4_JNT",
'C_spineFK5Ctl_GRP':"C_spine5_JNT",
'C_spineFK6Ctl_GRP':"C_spine6_JNT",
'C_spineFK7Ctl_GRP':"C_spine5_JNT",
'C_spineHCtl_GRP':"C_chest_JNT",
}

for each , value in fk_ctrls.items():
    transform=mc.xform(each , q=True, ws=1, t=True)
    if transform==[0, 0, 0]:
        transformWorldMatrix = mc.xform(each, q=True, wd=1, sp=True)
        rotateWorldMatrix = mc.xform(each, q=True, wd=1, ra=True)
    else:
        transformWorldMatrix = mc.xform(each, q=True, ws=1, t=True)
        rotateWorldMatrix = mc.xform(each, q=True, ws=1, ro=True)
    name=each.split("Ctl")[0]+"_SDWCH_Grp"
    selObjParentnxt=[(item) for item in mc.listRelatives( each, allParents=True ) if mc.nodeType(item) == 'transform']
    set_prnt = selObjParentnxt[0]
    mc.CreateEmptyGroup()
    mc.rename(mc.ls(sl=1)[0], name)
    mc.xform(name, ws=1, t=transformWorldMatrix)
    getornt = mc.orientConstraint (value, name, mo=0)
    mc.delete(getornt)
    #mc.xform(name, ws=1, ro=rotateWorldMatrix)
    if set_prnt:
        mc.parent(name, set_prnt)
    mc.parent(each, name)

fk_ctrls =[
'C_spineFK1_SDWCH_Grp',
'C_spineFK2_SDWCH_Grp',
'C_spineFK3_SDWCH_Grp',
'C_spineFK4_SDWCH_Grp',
'C_spineFK5_SDWCH_Grp',
'C_spineFK6_SDWCH_Grp',
'C_spineFK7_SDWCH_Grp',
'C_spineH_SDWCH_Grp'
]
for each in fk_ctrls:
    transform=mc.xform(each , q=True, ws=1, t=True)
    if transform==[0, 0, 0]:
        transformWorldMatrix = mc.xform(each, q=True, wd=1, sp=True)
        rotateWorldMatrix = mc.xform(each, q=True, wd=1, ra=True)
    else:
        transformWorldMatrix = mc.xform(each, q=True, ws=1, t=True)
        rotateWorldMatrix = mc.xform(each, q=True, ws=1, ro=True)
    name=each.split("Ctl")[0]+"_SDWCH_Grp"
    selObjParentnxt=[(item) for item in mc.listRelatives( each, allParents=True ) if mc.nodeType(item) == 'transform']
    set_prnt = selObjParentnxt[0]
    mc.CreateEmptyGroup()
    mc.rename(mc.ls(sl=1)[0], name)
    mc.xform(name, ws=1, t=transformWorldMatrix)
    mc.xform(name, ws=1, ro=rotateWorldMatrix)
    if set_prnt:
        mc.parent(name, set_prnt)
    mc.parent(each, name)

for indexNumber, eachPoint in enumerate(xrange(1,8)):
   #f mc.orientConstraint(['C_spine{}_JNT'.format(eachPoint), 'C_spineFK{}_SDWCH_Grp'.format(eachPoint)], mo=1)
    mc.connectAttr('C_spine{}_JNT.rotate'.format(eachPoint), 'C_spineFK{}_SDWCH_Grp.rotate'.format(eachPoint), f=1)
mc.connectAttr('C_chest_JNT.rotate', 'C_spineH_SDWCH_Grp.rotate', f=1)
mc.parent('C_spineH_SDWCH_Grp_SDWCH_Grp', 'C_spineFK7_CTL')