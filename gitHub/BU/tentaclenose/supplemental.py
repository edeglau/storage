import maya.cmds as cmds
attrs = ['rx', 'ry', 'rz', 'tx', 'ty', 'tz', 'sx', 'sy', 'sz']
cmds.parentConstraint('C_nose_HITCH_loc', 'C_nose_MAIN_loc', mo=1)
cmds.parentConstraint('C_fingieMaskTop_CTL', 'C_nose_HITCH_loc', mo=1)

cmds.parentConstraint('C_hitchMAIN_loc', 'C_lowerMAIN_loc', mo=1)

cmds.parentConstraint('C_fingieMaskBot_CTL', 'C_hitchMAIN_loc', mo=1)

cmds.setAttr('visibilityControl_GRP.C_lowerFingies1', 0)
cmds.setAttr('visibilityControl_GRP.C_fingieBotHitch1', 0)
cmds.setAttr('visibilityControl_GRP.C_nose1', 0)
cmds.setAttr('visibilityControl_GRP.C_fingieTopHitch1', 0)


getsrcObj_p =  [(each) for each in cmds.listRelatives("setup_GRP", c=1, type = "transform") if "noseFingies" in each]
for each in getsrcObj_p:cmds.setAttr('{}.v'.format(each), 0)