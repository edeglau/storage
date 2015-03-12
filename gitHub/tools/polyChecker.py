##Author: Elise Deglau
import re

import maya.cmds as cmds
from functools import partial


class ui():
    def __init__(self, winName="checker"):
        self.winTitle = "PolyChecker"
        self.winName = winName

    def create(self):
        if cmds.window(self.winName, exists=True):
            cmds.deleteUI(self.winName)

        self.window = cmds.window(self.winName, title=self.winTitle, w=350, h=300 )

        cmds.rowLayout  (' MainRow ', numberOfColumns=2)
        cmds.columnLayout ('Column1', cat = ('both', 0), adjustableColumn = True , parent = 'MainRow')
        cmds.columnLayout ('Column2', cat = ('both', 0), parent = 'MainRow') 
        
        
        cmds.setParent ('Column1') 
        cmds.button (label='Check Ngons', command = "singleNgons()")
        cmds.button (label='Check Tris', command = "singleTris()")
        cmds.button (label='Check Poly', command = "singlePoly()")
        cmds.button (label='Check Poles', command = "poles()")

            
            

        
        cmds.showWindow(self.window)
inst = ui()
inst.create()


def singleNgons():
    pObjn=cmds.ls(sl=True)
    faceCount =  cmds.polyEvaluate( pObjn[0], f=True)
    newlist=range (faceCount)
    cmds.select(cl=True)

    if cmds.objExists("Ngons")==True:
        cmds.delete("Ngons")
    cmds.sets(n="Ngons", co=3)

    for i in range(len(newlist)):   
        face = pObjn[0]+ ".f[%d]"%i
        cmds.select (face)
        gross = cmds.polyInfo(face, fv=True)
        vertCount=gross[0].split("    ")
        if (len(vertCount))>=7:
            cmds.ConvertSelectionToVertices(face)
            cmds.sets( fe='Ngons')
            print "Ngon found"
            
    cmds.select('Ngons', r=True, ne=True)
    cmds.pickWalk(d='Up')
    acksel=cmds.ls(sl=True)
    if (len(acksel))==0:
        cmds.delete("Ngons")

def singleTris():
    pObjt=cmds.ls(sl=True)
    faceCount =  cmds.polyEvaluate( pObjt[0], f=True)
    newlist=range (faceCount)
    cmds.select(cl=True)

    if cmds.objExists("Tris")==True:
        cmds.delete("Tris")
    cmds.sets(n="Tris", co=6)

    for i in range(len(newlist)):   
        face = pObjt[0]+ ".f[%d]"%i
        cmds.select (face)
        gross = cmds.polyInfo(face, fv=True)
        vertCount=gross[0].split("    ")
        if (len(vertCount))==5:
            cmds.ConvertSelectionToVertices(face)
            cmds.sets( fe='Tris')
            cmds.select (face)
            cmds.sets( fe='Tris')
            print "Tri found"
    cmds.select('Tris', r=True, ne=True)
    cmds.pickWalk(d='Up')
    acksel=cmds.ls(sl=True)
    if (len(acksel))==0:
        cmds.delete("Tris")

def singlePoly():
    pObjp = cmds.ls (sl=True)
    cmds.select(cl=True)

    if cmds.objExists("PolyIssues")==True:
        cmds.delete("PolyIssues")
    cmds.sets(n="PolyIssues", co=5)

    cmds.select(pObjp)
    jack=cmds.polyInfo(pObjp, lf=True, nme=True, nmv=True )
    cmds.select (jack)
    cmds.ConvertSelectionToVertices('jack')
    if jack>0:
        print "Polygon error found"
        cmds.sets( fe='PolyIssues')

    cmds.select('PolyIssues', r=True, ne=True)
    cmds.pickWalk(d='Up')
    acksel=cmds.ls(sl=True)
    if (len(acksel))==0:
        cmds.delete("PolyIssues")

def poles():
    pObj=list()
    crap=list()
    pObjd = cmds.ls (sl=True)
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
    
    for h in range (len(pObjd)):
        f=pObjd[h].split('.')
        j=f[1].split('[')
        str= j[1][:-1]
        if ':' not in (str):
            ppo=int(str)
            jw=('%d' %ppo)
            jol=jim[0]+'.vtx['+jw+']'
            pObj.append(jol)
        elif ':' in (str):
            crap.append(str)
            for p in range (len(crap)):
                g=str.split(':')
                t=int(g[0])
                v=int(g[1])
                nmbr=range (t, v)
                for k in range(len(nmbr)):
                    jw=('%d' %nmbr[k])
                    kol=jim[0]+'.vtx['+jw+']'
                    pObj.append(kol)
    for y in range (len(pObj)):
        gross = cmds.polyInfo(pObj[y], ve=True)
        g=gross[0].split(':')
        edgeCount=g[1].split("   ")
        if (len(edgeCount))==4:
            cmds.sets(pObj[y], fe='Npoles')
        elif (len(edgeCount))==6:
            cmds.sets(pObj[y], fe='Epoles')
        elif (len(edgeCount))>=7:
            cmds.sets(pObj[y], fe='starpoles')
    
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