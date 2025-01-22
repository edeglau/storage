import maya.cmds as cmds
from functools import partial

def makeX():
    cmds.CreateCluster(en=1, r=True)
    joe=cmds.ls(sl=True)
    jack=cmds.circle(c=(0, 0, 0), nr=(1, 0, 0), sw=360, r=1, d=3, s=8, n='Handle_CRV_00')
    cmds.select (joe)
    cmds.select(jack, add=True)
    clide=cmds.parentConstraint(mo=False, w=1)
    cmds.delete(clide)
    cmds.select(jack)
    cmds.makeIdentity (a=True, t=True, r=True, s=True) 
    cmds.delete(ch=True)
    cmds.select(joe, add=True)
    cmds.pointConstraint(mo=True, w=1)
    
def makeY():
    cmds.CreateCluster(en=1, r=True)
    joe=cmds.ls(sl=True)
    jack=cmds.circle(c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=1, d=3, s=8, n='Handle_CRV_00')
    cmds.select (joe)
    cmds.select(jack, add=True)
    clide=cmds.parentConstraint(mo=False, w=1)
    cmds.delete(clide)
    cmds.select(jack)
    cmds.makeIdentity (a=True, t=True, r=True, s=True) 
    cmds.delete(ch=True)
    cmds.select(joe, add=True)
    cmds.pointConstraint(mo=True, w=1)
    
def makeZ():
    cmds.CreateCluster(en=1, r=True)
    joe=cmds.ls(sl=True)
    jack=cmds.circle(c=(0, 0, 0), nr=(0, 0, 1), sw=360, r=1, d=3, s=8, n='Handle_CRV_00')
    cmds.select (joe)
    cmds.select(jack, add=True)
    clide=cmds.parentConstraint(mo=False, w=1)
    cmds.delete(clide)
    cmds.select(jack)
    cmds.makeIdentity (a=True, t=True, r=True, s=True) 
    cmds.delete(ch=True)
    cmds.select(joe, add=True)
    cmds.pointConstraint(mo=True, w=1)
    
def makeshape():
    cmds.CreateCluster(en=1, r=True)
    joe=cmds.ls(sl=True)

    jack=cmds.circle(c=(0, 0, 0), nr=(1, 0, 0), sw=360, r=1, d=3, s=8, n='Handle_CRV_00')
    jill=cmds.circle(c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=1, d=3, s=8, n='Handle_CRV_00')
    went=cmds.circle(c=(0, 0, 0), nr=(0, 0, 1), sw=360, r=1, d=3, s=8, n='Handle_CRV_00')
    cmds.select(jack)
    cmds.select(jill, add=True)
    cmds.delete(ch=True)
    cmds.makeIdentity (a=True, t=True, r=True, s=True, n=1) 
    transformNodeList=cmds.ls(sl=True)
    shapeNode=cmds.listRelatives(transformNodeList[0], s=True)
    choose=cmds.ls(sl=True)
    cmds.parent(shapeNode, transformNodeList, add=True, s=True) 
    cmds.select(choose)
    cmds.delete (transformNodeList[0])
    shark=cmds.ls(sl=True)
    cmds.select(went, add=True)
    cmds.delete(ch=True)
    cmds.makeIdentity (a=True, t=True, r=True, s=True, n=1) 
    transformNodeList=cmds.ls(sl=True)
    shapeNode=cmds.listRelatives(transformNodeList[0], s=True)
    choose=cmds.ls(sl=True)
    cmds.parent(shapeNode, transformNodeList, add=True, s=True)
    cmds.select(choose) 
    cmds.delete (transformNodeList[0])
    shark=cmds.ls(sl=True)
    cmds.select (joe)
    cmds.select(shark, add=True)
    clide=cmds.parentConstraint(mo=False, w=1)
    cmds.delete(clide)
    cmds.select(shark)
    cmds.makeIdentity (a=True, t=True, r=True, s=True) 
    cmds.delete(ch=True)
    cmds.select(joe, add=True)
    cmds.pointConstraint(mo=True, w=1)
    cmds.rename('HANDLE_CRV_')


class ui():
    def __init__(self, winName="winTheWindow"):
        self.winTitle = "The Window"
        self.winName = winName

    def create(self):
        if cmds.window(self.winName, exists=True):
            cmds.deleteUI(self.winName)

        cmds.window(self.winName, title=self.winTitle)
        self.mainCol = cmds.columnLayout( adjustableColumn=True )
        cmds.button (label='Xaligned', command = "makeX()")
        cmds.button (label='Zaligned', command = "makeZ()")
        cmds.button (label='Yaligned', command = "makeY()")
        cmds.button (label='sphere', command = "makeshape()")
        cmds.showWindow( self.winName )
        cmds.window(self.winName, edit=True, widthHeight=[250,100])

    def a(self, myarg=None, arg=None):
        print 'myarg: ', myarg

    def b(self, arg=None):
        print 'buttons require an argument'
        print 'the argument passed in will always be the last argument'

# create the window
inst = ui()
inst.create()
