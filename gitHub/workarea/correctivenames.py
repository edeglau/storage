import maya.cmds as cmds

class corrective_bs():
	def __init__(self):
		getParent=cmds.ls(sl=1)
		selected=cmds.duplicate(rr=1)
		getIt=cmds.ls("*COR_BS_GRP*")
		if len(getIt)<1:
		    getIt=cmds.CreateEmptyGroup()
		    cmds.rename(getIt, "COR_BS_GRP")
		    getIt=cmds.ls("*COR_BS_GRP*")
		else:
		    getIt=cmds.ls("*COR_BS_GRP*")  
		for each in selected:
		    currentFrameNum=cmds.currentTime(q=1)
		    currentFrameNum=int(currentFrameNum)
		    frname=each+"_COR_BS_FR"+str(currentFrameNum)
		    cmds.rename(each, frname)
		    cmds.parent(frname, getIt)
		for item in getParent:
		    cmds.setAttr(item+".visibility", 0)   
