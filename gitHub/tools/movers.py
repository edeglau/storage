import maya.cmds as cmds
from functools import partial


class ui():
        def __init__(self, winName="moversWindow"):
                self.winTitle = "Movers"
                self.winName = winName

        def create(self):
                if cmds.window(self.winName, exists=True):
                        cmds.deleteUI(self.winName)

                self.window = cmds.window(self.winName, title=self.winTitle, w=350, h=300 )
                
                cmds.frameLayout( label='Transforms are based on last selected', borderStyle='in' )
                cmds.rowLayout  (' MainRow ', numberOfColumns=100, ebg=False, bgc=(.5, .5, .5),)
                cmds.columnLayout('Column1', parent = 'MainRow', adjustableColumn=True, w=150)
                cmds.columnLayout('Column2', parent = 'MainRow', adjustableColumn=True, w=150)
                cmds.columnLayout('Column3', parent = 'MainRow', adjustableColumn=True, w=150)
        
       
                cmds.setParent ('Column1')
                cmds.text( label='Basic Commands' )
                cmds.button (label='Reset Pivot', command = "ResetPivot()")
                cmds.button (label='Clean History', command = "CleanHistory()")
                cmds.button (label='Freeze Transforms', command = "FreezeTransforms()")
                cmds.button (label='Freeze Rot', command = "FreezeRotations()")
                cmds.button (label='Freeze Scale', command = "FreezeScales()")
                cmds.button (label='Freeze All', command = "FreezeAll()")
                cmds.button (label='Center Pivot', command = "CenterPiv()")
                cmds.button (label='Reorient Joint', command = "reorntJnt()")
                cmds.button (label='Locators', ann='creates locators at selected object', command = "Lctrs()")
                cmds.button (label='Heirarchy loc', ann='creates locators on a heirarchy', command = "Lctrshrchy()")
                cmds.button (label='Mirror X', command = "mirXx()")
                cmds.button (label='Mirror Y', command = "mirYy()")
                cmds.button (label='Mirror Z', command = "mirZz()")

                
                cmds.setParent ('Column2')
                cmds.text( label='Special moves' )
                cmds.button (label='Move/Rot/Sc objPiv2obj', ann="will not work on relocated vertices(will relocate to origin of object previously)", command = "MoveRotScobjPiv2obj()")
                cmds.button (label='Move obj2Piv', command = "moveObjtoPivot()")
                cmds.button (label='MovePiv2obj/RotPiv2piv', ann="will not work on relocated vertices(will relocate to origin of object previously)", command = "moveRotPivToObj()")
                cmds.button (label='Move/Rot Piv2piv', command = "moveRotPivToPiv()")
                cmds.button (label='Move Piv2obj', ann="will not work on relocated vertices(will relocate to origin of object previously)", command = "movePivToObj()")
                cmds.button (label='Move Piv2Piv', command = "movePivToPiv()")
                cmds.button (label='Rotate Piv2Piv', command = "rotPivot()")
                cmds.button (label='Move obj2obj', ann="will not work on relocated vertices(will relocate to origin of object previously)",command = "MoveObj2Obj()")
                cmds.button (label='Match objPiv2objPiv', ann="will not work on relocated vertices(will relocate to origin of object previously)", command = "MatchobjPiv2objPiv()")
                cmds.button (label='Match PivPlacement', command = "MatchpivotPlacement()")
                cmds.button (label='Piv2SelectVerts', command = "Pivot2Select()")

                cmds.setParent ('Column3')
                cmds.text( label='Mass Moves' )
                cmds.button (label='Mass move', command = "moveArray()")
                cmds.button (label='Mass Rotate', command = "rotArray()")
                cmds.button (label='Mass Scale',  command = "scaleArray()")
                cmds.button (label='Mass Move/Rot/Sc', command = "moveRotScArray()")
                cmds.button (label='Mass Match Pivots', command = "matchPivotArray()")          

                
                cmds.showWindow(self.window)
inst = ui()
inst.create()



def MoveObj2Obj():
        glog=cmds.ls(sl=True)
        moveFrogMiddle=cmds.xform(glog[0], q=True, t=True, ws=True)
        movefrog=cmds.xform(glog[1], q=True, t=True, ws=True)
        cmds.move(movefrog[0], movefrog[1], movefrog[2], glog[0], ws=True)
        plog=cmds.select(glog[0]+'.rotatePivot', r=True)
        cmds.move(moveFrogMiddle[0], moveFrogMiddle[1], moveFrogMiddle[2], plog, ws=True)

def rotPivot():
        glog=cmds.ls(sl=True)
        cmds.select(glog[0])
        cmds.makeIdentity (a=True, r=True)
        rotatefrog=cmds.xform(glog[1], q=True, ro=True, ws=True)
        flog=cmds.select(glog[0]+'.rotateAxis', r=True)
        clop=rotatefrog[0]*-1
        klop=rotatefrog[1]*-1
        qlop=rotatefrog[2]*-1
        cmds.rotate(clop, flog, x=True, r=True )
        cmds.rotate(klop, flog, y=True, r=True)
        cmds.rotate(qlop, flog, z=True, r=True)

def movePivToObj():
        glog=cmds.ls(sl=True)
        cmds.select(glog[0])
        movefrog=cmds.xform(glog[1], q=True, t=True, ws=True)
        plog=cmds.select(glog[0]+'.rotatePivot', r=True)
        cmds.move(movefrog[0], movefrog[1], movefrog[2], ws=True)



def ResetPivot():
        chalk=cmds.ls(sl=True)
        home=cmds.xform(chalk, q=True, ws=True, rp=True)
        clop=home[0]*-1
        klop=home[1]*-1
        qlop=home[2]*-1
        cmds.move(clop, klop, qlop, r=True)
        cmds.makeIdentity (a=True, t=True)
        cmds.move(home[0], home[1], home[2], ws=True)

def FreezeTransforms():
        cmds.makeIdentity (a=True, t=True)

def FreezeRotations():
        cmds.makeIdentity (a=True, r=True)

def FreezeScales():
        cmds.makeIdentity (a=True, s=True)

def FreezeAll():
        cmds.makeIdentity (a=True, t=True, r=True, s=True)


def CleanHistory():
        cmds.delete (ch=True)

def CenterPiv():
        cmds.xform(cp=1)



def MoveRotScobjPiv2obj():
        glog=cmds.ls(sl=True)
        scalefrog=cmds.xform(glog[1], q=True, s=True, r=True)
        movefrog=cmds.xform(glog[1], q=True, t=True, ws=True)
        rotatefrog=cmds.xform(glog[1], q=True, ro=True, ws=True)
        cmds.rotate(rotatefrog[0], rotatefrog[1], rotatefrog[2], glog[0], ws=True)
        cmds.move(movefrog[0], movefrog[1], movefrog[2], glog[0], ws=True)
        cmds.scale(scalefrog[0], scalefrog[1], scalefrog[2], glog[0], r=True)
        cmds.select(glog[0])
        cmds.makeIdentity (a=True, r=True)
        rotatefrog=cmds.xform(glog[1], q=True, ro=True, ws=True)
        movefrog=cmds.xform(glog[1], q=True, t=True, ws=True)
        plog=cmds.select(glog[0]+'.rotatePivot', r=True)
        cmds.move(movefrog[0], movefrog[1], movefrog[2], plog, ws=True)
        flog=cmds.select(glog[0]+'.rotateAxis', r=True)
        clop=rotatefrog[0]*-1
        klop=rotatefrog[1]*-1
        qlop=rotatefrog[2]*-1
        cmds.rotate(clop, flog, x=True, r=True )
        cmds.rotate(klop, flog, y=True, r=True)
        cmds.rotate(qlop, flog, z=True, r=True)

def moveObjtoPivot():
        glog=cmds.ls(sl=True)
        cmds.select(glog[1]+'.rotatePivot', r=True)
        movefrog=cmds.xform(q=True, t=True, ws=True)
        cmds.move(movefrog[0], movefrog[1], movefrog[2], glog[0], ws=True)

def moveRotPivToObj():
        glog=cmds.ls(sl=True)
        cmds.select(glog[0])
        cmds.makeIdentity (a=True, r=True)
        rotatefrog=cmds.xform(glog[1], q=True, ro=True, ws=True)
        movefrog=cmds.xform(glog[1], q=True, t=True, ws=True)
        plog=cmds.select(glog[0]+'.rotatePivot', r=True)
        cmds.move(movefrog[0], movefrog[1], movefrog[2], plog, ws=True)
        flog=cmds.select(glog[0]+'.rotateAxis', r=True)
        clop=rotatefrog[0]*-1
        klop=rotatefrog[1]*-1
        qlop=rotatefrog[2]*-1
        cmds.rotate(clop, flog, x=True, r=True )
        cmds.rotate(klop, flog, y=True, r=True)
        cmds.rotate(qlop, flog, z=True, r=True)

def moveRotPivToPiv():
        glog=cmds.ls(sl=True)
        cmds.select(glog[0])
        cmds.makeIdentity (a=True, r=True)
        cmds.select(glog[1]+'.rotatePivot', r=True)
        movefrog=cmds.xform(q=True, t=True, ws=True)
        plog=cmds.select(glog[0]+'.rotatePivot', r=True)
        cmds.move(movefrog[0], movefrog[1], movefrog[2], plog,ws=True)
        rotatefrog=cmds.xform(glog[1], q=True, ro=True, ws=True)
        flog=cmds.select(glog[0]+'.rotateAxis', r=True)
        clop=rotatefrog[0]*-1
        klop=rotatefrog[1]*-1
        qlop=rotatefrog[2]*-1
        cmds.rotate(clop, flog, x=True, r=True )
        cmds.rotate(klop, flog, y=True, r=True)
        cmds.rotate(qlop, flog, z=True, r=True)



def movePivToPiv():
        glog=cmds.ls(sl=True)
        cmds.select(glog[1]+'.rotatePivot', r=True)
        movefrog=cmds.xform(q=True, t=True, ws=True)
        cmds.select(glog[0]+'.rotatePivot', r=True)
        cmds.move(movefrog[0], movefrog[1], movefrog[2], ws=True)