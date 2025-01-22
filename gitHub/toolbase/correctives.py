'''
Duplicates the selected mesh, cleans and names for corrective shapes using frame number. 
'''

__author__="Elise Deglau"


import maya.cmds as mc

#import custom
import mockTools_2018
reload (mockTools_2018) 
import baseMockFunctions_maya
reload (baseMockFunctions_maya) 


class corrective_bs():
	def __init__(self):
		#create geo set
		if mc.objExists("hiddenCorrectedGeo") == False:
			mc.sets(n="hiddenCorrectedGeo", co=3)		
		getParent = mc.ls(sl=1)
		dup_selected = mc.duplicate(rr=1)
		select_dups = []
		dup_shape_grp = mc.ls("*COR_BS_GRP*")
		#Setup the corrective shape group
		if len(dup_shape_grp)<1:
			dup_shape_grp = mc.CreateEmptyGroup()
			mc.rename(dup_shape_grp, "COR_BS_GRP")
			dup_shape_grp = mc.ls("*COR_BS_GRP*")
		else:
			dup_shape_grp = mc.ls("*COR_BS_GRP*")  
		#Name and clean the corrective shape
		for each_dup in dup_selected:
			currentFrameNum=mc.currentTime(q=1)
			currentFrameNum=int(currentFrameNum)
			i = 0
			new_dup_shape=each_dup+"_COR_BS_FR"+str(currentFrameNum)
			while mc.o
