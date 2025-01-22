import maya.cmds as cmds
from functools import partial


class moversUI():
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
         cmds.button (label='Reset Pivot', command = self.ResetPivot)
         cmds.button (label='Clean History', command = self.CleanHistory)
         cmds.button (label='Freeze Transforms', command = self.FreezeTransforms)
         cmds.button (label='Freeze Rot', command = self.FreezeRotations)
         cmds.button (label='Freeze Scale', command = self.FreezeScales)
         cmds.button (label='Freeze All', command = self.FreezeAll)
         cmds.button (label='Center Pivot', command = self.CenterPiv)
         cmds.button (label='Reorient Joint', command = self.reorntJnt)
         cmds.button (label='Locators', ann='creates locators at selected object', command = self.Lctrs)
         cmds.button (label='Heirarchy loc', ann='creates locators on a heirarchy', command = self.Lctrshrchy)
         cmds.button (label='Mirror X', command = self.mirXx)
         cmds.button (label='Mirror Y', command = self.mirYy)
         cmds.button (label='Mirror Z', command = self.mirZz)

         
         cmds.setParent ('Column2')
         cmds.text( label='Special moves' )
         cmds.button (label='Move/Rot/Sc objPiv2obj', ann="will not work on relocated vertices(will relocate to origin of object previously)", command = self.MoveRotScobjPiv2obj)
         cmds.button (label='Move obj2Piv', command = self.moveObjtoPivot)
         cmds.button (label='MovePiv2obj/RotPiv2piv', ann="will not work on relocated vertices(will relocate to origin of object previously)", command = self.moveRotPivToObj)
         cmds.button (label='Move/Rot Piv2piv', command = self.moveRotPivToPiv)
         cmds.button (label='Move Piv2obj', ann="will not work on relocated vertices(will relocate to origin of object previously)", command = self.movePivToObj)
         cmds.button (label='Move Piv2Piv', command = self.movePivToPiv)
         cmds.button (label='Rotate Piv2Piv', command = self.rotPivot)
         cmds.button (label='Move obj2obj', ann="will not work on relocated vertices(will relocate to origin of object previously)",command = self.MoveObj2Obj)
         cmds.button (label='Match objPiv2objPiv', ann="will not work on relocated vertices(will relocate to origin of object previously)", command = self.MatchobjPiv2objPiv)
         cmds.button (label='Match PivPlacement', command = self.MatchpivotPlacement)
         cmds.button (label='Piv2SelectVerts', command = self.Pivot2Select)

         cmds.setParent ('Column3')
         cmds.text( label='Mass Moves' )
         cmds.button (label='Mass move', command = self.moveArray)
         cmds.button (label='Mass Rotate', command = self.rotArray)
         cmds.button (label='Mass Scale',  command = self.scaleArray)
         cmds.button (label='Mass Move/Rot/Sc', command = self.moveRotScArray)
         cmds.button (label='Mass Match Pivots', command = self.matchPivotArray)          

         cmds.showWindow(self.window)


    def MoveObj2Obj(self, arg=None):
        selObj=cmds.ls(sl=True, fl=1)
        movefransformMiddle=cmds.xform(selObj[0], q=True, t=True, ws=True)
        movefransform=cmds.xform(selObj[1], q=True, t=True, ws=True)
        cmds.move(movefransform[0], movefransform[1], movefransform[2], selObj[0], ws=True)
        pivSelect=cmds.select(selObj[0]+'.rotatePivot', r=True)
        cmds.move(movefransformMiddle[0], movefransformMiddle[1], movefransformMiddle[2], pivSelect, ws=True)

    def rotPivot(self, arg=None):
        selObj=cmds.ls(sl=True, fl=1)
        cmds.select(selObj[0])
        cmds.makeIdentity (a=True, r=True)
        rotatefransform=cmds.xform(selObj[1], q=True, ro=True, ws=True)
        pivotTransform=cmds.select(selObj[0]+'.rotateAxis', r=True)
        xTrans=rotatefransform[0]*-1
        yTrans=rotatefransform[1]*-1
        zTrans=rotatefransform[2]*-1
        cmds.rotate(xTrans, pivotTransform, x=True, r=True )
        cmds.rotate(yTrans, pivotTransform, y=True, r=True)
        cmds.rotate(zTrans, pivotTransform, z=True, r=True)
    
    def movePivToObj(self, arg=None):
        selObj=cmds.ls(sl=True, fl=1)
        cmds.select(selObj[0])
        movefransform=cmds.xform(selObj[1], q=True, t=True, ws=True)
        cmds.select(selObj[0]+'.rotatePivot', r=True)
        cmds.move(movefransform[0], movefransform[1], movefransform[2], ws=True)



    def ResetPivot(self, arg=None):
            selObj=cmds.ls(sl=True, fl=1)
            home=cmds.xform(selObj, q=True, ws=True, rp=True)
            xTrans=home[0]*-1
            yTrans=home[1]*-1
            zTrans=home[2]*-1
            cmds.move(xTrans, yTrans, zTrans, r=True)
            cmds.makeIdentity (a=True, t=True)
            cmds.move(home[0], home[1], home[2], ws=True)
    
    def FreezeTransforms(self, arg=None):
            cmds.makeIdentity (a=True, t=True)
    
    def FreezeRotations(self, arg=None):
            cmds.makeIdentity (a=True, r=True)
    
    def FreezeScales(self, arg=None):
            cmds.makeIdentity (a=True, s=True)
    
    def FreezeAll(self, arg=None):
            cmds.makeIdentity (a=True, t=True, r=True, s=True)
    
    
    def CleanHistory(self, arg=None):
            cmds.delete (ch=True)
    
    def CenterPiv(self, arg=None):
            cmds.xform(cp=1)
    
    def MoveRotScobjPiv2obj(self, arg=None):
        selObj=cmds.ls(sl=True, fl=1)
        scalefransform=cmds.xform(selObj[1], q=True, s=True, r=True)
        movefransform=cmds.xform(selObj[1], q=True, t=True, ws=True)
        rotatefransform=cmds.xform(selObj[1], q=True, ro=True, ws=True)
        cmds.rotate(rotatefransform[0], rotatefransform[1], rotatefransform[2], selObj[0], ws=True)
        cmds.move(movefransform[0], movefransform[1], movefransform[2], selObj[0], ws=True)
        cmds.scale(scalefransform[0], scalefransform[1], scalefransform[2], selObj[0], r=True)
        cmds.select(selObj[0])
        cmds.makeIdentity (a=True, r=True)
        rotatefransform=cmds.xform(selObj[1], q=True, ro=True, ws=True)
        movefransform=cmds.xform(selObj[1], q=True, t=True, ws=True)
        pivSelect=cmds.select(selObj[0]+'.rotatePivot', r=True)
        cmds.move(movefransform[0], movefransform[1], movefransform[2], pivSelect, ws=True)
        pivotTransform=cmds.select(selObj[0]+'.rotateAxis', r=True)
        xTrans=rotatefransform[0]*-1
        yTrans=rotatefransform[1]*-1
        zTrans=rotatefransform[2]*-1
        cmds.rotate(xTrans, pivotTransform, x=True, r=True )
        cmds.rotate(yTrans, pivotTransform, y=True, r=True)
        cmds.rotate(zTrans, pivotTransform, z=True, r=True)
    
    def moveObjtoPivot(self, arg=None):
        glog=cmds.ls(sl=True, fl=1)
        cmds.select(glog[1]+'.rotatePivot', r=True)
        movefransform=cmds.xform(q=True, t=True, ws=True)
        cmds.move(movefransform[0], movefransform[1], movefransform[2], glog[0], ws=True)
    
    def moveRotPivToObj(self, arg=None):
        glog=cmds.ls(sl=True, fl=1)
        cmds.select(glog[0])
        cmds.makeIdentity (a=True, r=True)
        rotatefransform=cmds.xform(glog[1], q=True, ro=True, ws=True)
        movefransform=cmds.xform(glog[1], q=True, t=True, ws=True)
        pivSelect=cmds.select(glog[0]+'.rotatePivot', r=True)
        cmds.move(movefransform[0], movefransform[1], movefransform[2], pivSelect, ws=True)
        pivotTransform=cmds.select(glog[0]+'.rotateAxis', r=True)
        xTrans=rotatefransform[0]*-1
        yTrans=rotatefransform[1]*-1
        zTrans=rotatefransform[2]*-1
        cmds.rotate(xTrans, pivotTransform, x=True, r=True )
        cmds.rotate(yTrans, pivotTransform, y=True, r=True)
        cmds.rotate(zTrans, pivotTransform, z=True, r=True)
    
    def moveRotPivToPiv(self, arg=None):
        glog=cmds.ls(sl=True, fl=1)
        cmds.select(glog[0])
        cmds.makeIdentity (a=True, r=True)
        cmds.select(glog[1]+'.rotatePivot', r=True)
        movefransform=cmds.xform(q=True, t=True, ws=True)
        pivSelect=cmds.select(glog[0]+'.rotatePivot', r=True)
        cmds.move(movefransform[0], movefransform[1], movefransform[2], pivSelect,ws=True)
        rotatefransform=cmds.xform(glog[1], q=True, ro=True, ws=True)
        pivotTransform=cmds.select(glog[0]+'.rotateAxis', r=True)
        xTrans=rotatefransform[0]*-1
        yTrans=rotatefransform[1]*-1
        zTrans=rotatefransform[2]*-1
        cmds.rotate(xTrans, pivotTransform, x=True, r=True )
        cmds.rotate(yTrans, pivotTransform, y=True, r=True)
        cmds.rotate(zTrans, pivotTransform, z=True, r=True)

    
    
    def movePivToPiv(self, arg=None):
        glog=cmds.ls(sl=True, fl=1)
        cmds.select(glog[1]+'.rotatePivot', r=True)
        movefransform=cmds.xform(q=True, t=True, ws=True)
        cmds.select(glog[0]+'.rotatePivot', r=True)
        cmds.move(movefransform[0], movefransform[1], movefransform[2], ws=True)
        
inst = moversUI()
inst.create()