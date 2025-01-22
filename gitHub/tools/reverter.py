##Created on Mar 3, 2011
##@author: elise.deglau


import maya.cmds as cmds
from functools import partial


class RevertUI():
    def __init__(self, winName="revwin"):
        self.winTitle = "Reverter"
        self.winName = winName

    def create(self):
        if cmds.window(self.winName, exists=True):
                cmds.deleteUI(self.winName)

        self.window = cmds.window(self.winName, title=self.winTitle, w=250, h=100 )
        cmds.frameLayout( label='Are you sure you want to revert?', borderStyle='in' )
        cmds.rowLayout  (' Mn_Row ', numberOfColumns=100)
        cmds.columnLayout('showl', parent = 'Mn_Row', adjustableColumn=True, w=150)
        cmds.columnLayout('shwl', parent = 'Mn_Row', adjustableColumn=True, w=150)
        cmds.columnLayout('howlb', parent = 'Mn_Row', adjustableColumn=True, w=150)
        cmds.setParent ('showl')
        cmds.button (label='Yes!', command = self.revertingb)
        cmds.setParent ('shwl')
        cmds.button (label='No!', command = self.NWin)
        cmds.showWindow(self.window)

    def revertingb(self, arg=None):
        path=str(cmds.file(q=1,exn=1))
        cmds.file(path, o=True, f=True)
        if cmds.window("revwin", exists=True):
                cmds.deleteUI("revwin")
    
    def NWin(self, arg=None):
        if cmds.window("revwin", exists=True):
                cmds.deleteUI("revwin")
inst = RevertUI()
inst.create()                    