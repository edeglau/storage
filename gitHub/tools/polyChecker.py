

##Author: Elise Deglau
import re
import maya.cmds as cmds
from functools import partial

class PolyUI():
    def __init__(self, winName="checker"):
        self.winTitle = "PolyChecker"
        self.winName = winName
    def create(self):
        if cmds.window(self.winName, exists=True):
            cmds.deleteUI(self.winName)
        self.window = cmds.window(self.winName, title=self.winTitle, w=350, h=300 )
        cmds.rowLayout (' MainRow ', numberOfColumns=2)
        cmds.columnLayout ('Column1', cat = ('both', 0), adjustableColumn = True , parent = 'MainRow')
        cmds.columnLayout ('Column2', cat = ('both', 0), parent = 'MainRow')
        cmds.setParent ('Column1')
        cmds.button (label='Check Ngons', command = self.singleNgons)
        cmds.button (label='Check Poly', command = self.singlePoly)
        cmds.button (label='Check Poles', command = self.poles)
        cmds.showWindow(self.window)

    def singleNgons(self, arg=None):
        pObjn=cmds.ls(sl=True, fl=1)
        cmds.select(cl=True)
        if cmds.objExists("Ngons")==True:
            cmds.delete("Ngons")
        cmds.sets(n="Ngons", co=3)
        if cmds.objExists("Tris")==True:
            cmds.delete("Tris")
        cmds.sets(n="Tris", co=3)        
        for face in pObjn:
            gross = cmds.polyInfo(face, fe=True)
            getVerts=gross[0].split(':')[1]
            edgeCount=re.findall(r'\d+', getVerts) 
            if (len(edgeCount))>=5:
                cmds.ConvertSelectionToVertices(face)
                cmds.select (face)
                cmds.sets( fe='Ngons')                
                print "Ngon found"
            if (len(edgeCount))==3:
                cmds.ConvertSelectionToVertices(face)
                cmds.select (face)
                cmds.sets( fe='Tris')
                print "Tri found"           
        cmds.select('Tris', r=True, ne=True)
        cmds.pickWalk(d='Up')
        acksel=cmds.ls(sl=True)
        if (len(acksel))==0:
            cmds.delete("Tris")
        cmds.select('Ngons', r=True, ne=True)
        cmds.pickWalk(d='Up')
        acksel=cmds.ls(sl=True, fl=1)
        if (len(acksel))==0:
            cmds.delete("Ngons")             
    def singlePoly(self, arg=None):
        pObjp = cmds.ls (sl=True, fl=1)
        cmds.select(cl=True)
        if cmds.objExists("PolyIssues")==True:
            cmds.delete("PolyIssues")
        cmds.sets(n="PolyIssues", co=5)
        cmds.select(pObjp)
        jack=cmds.polyInfo(pObjp, lf=True, nme=True, nmv=True )
        cmds.select (jack)
        cmds.ConvertSelectionToVertices(jack)
        if jack>0:
            print "Polygon error found"
            cmds.sets( fe='PolyIssues')
        cmds.select('PolyIssues', r=True, ne=True)
        cmds.pickWalk(d='Up')
        acksel=cmds.ls(sl=True)
        if (len(acksel))==0:
            cmds.delete("PolyIssues")
    def poles(self, arg=None):
        pObj=list()
        crap=list()
        pObjd = cmds.ls (sl=True, fl=1)
        cmds.selectMode(object=True)
        jim=cmds.ls (sl=True)
        cmds.select(cl=True)
        if cmds.objExists("Npoles")==True:
            cmds.delete("Npoles")
        cmds.sets(n="Npoles", co=1)
        if cmds.objExists("Epoles")==True:
            cmds.delete("Epoles")
        cmds.sets(n="Epoles", co=4)
        if cmds.objExists("starpoles")==True:
            cmds.delete("starpoles")
        cmds.sets(n="starpoles", co=7)
        for each in pObjd:
            gross = cmds.polyInfo(each, ve=True)
            getVerts=gross[0].split(':')[1]
            edgeCount=re.findall(r'\d+', getVerts)
            if (len(edgeCount))==3:
                cmds.sets(each, fe='Npoles')
            elif (len(edgeCount))==5:
                cmds.sets(each, fe='Epoles')
            elif (len(edgeCount))>5:
                cmds.sets(each, fe='starpoles')
        cmds.select('starpoles', r=True, ne=True)
        cmds.pickWalk(d='Up')
        acksel=cmds.ls(sl=True)
        if (len(acksel))==0:
            cmds.delete("starpoles")
        cmds.select('Npoles', r=True, ne=True)
        cmds.pickWalk(d='Up')
        acksel=cmds.ls(sl=True)
        if (len(acksel))==0:
            cmds.delete("Npoles")
        cmds.select('Epoles', r=True, ne=True)
        cmds.pickWalk(d='Up')
        acksel=cmds.ls(sl=True)
        if (len(acksel))==0:
            cmds.delete("Epoles")

inst = PolyUI()
inst.create()
