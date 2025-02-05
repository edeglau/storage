import maya.cmds as cmds
import ridemaya.lib.attr as ltra
ltra.insertUnder("visibilityControl_GRP", "LeaveAlone", "LeaveAlone")
get = cmds.listAttr("visibilityControl_GRP", ud=1)
newget = [u'_', u'joint',
u'__', u'membrane_fk1',
u'___', u'C_jaw1',
 u'C_jaw2', u'____', u'C_tongueFk1',
 u'C_tongueIk1', u'C_tongueSubs', u'C_face1', u'C_face2', u'C_face3', u'_____',
 u'C_fingieMaskTop1', u'C_fingieMaskBot1', u'______', u'noseFingiesVis', u'noseFingiesFK2', u'noseFingiesIK2',  'lipTweaker_sculptlipBeard', u'_______', u'C_nose1', u'C_fingieTopHitch1',
  u'C_lowerFingies1', u'C_fingieBotHitch1']
cmds.deleteAttr('visibilityControl_GRP', at = "LeaveAlone")
ltra.reorder("visibilityControl_GRP", newget)