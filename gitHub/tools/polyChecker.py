
import re
import maya.cmds as cmds
from functools import partial



'''MG rigging modules'''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons Attribution 4.0 International 4.0 (CC BY 4.0)'
# 'This work is licensed under a Creative Commons Attribution-ShareAlike 3.0 Australia (CC BY-SA 3.0 AU)'
'http://creativecommons.org/licenses/by-sa/3.0/au/'



class PolyUI():
    def __init__(self, winName="checker"):
        self.winTitle = "PolyChecker"
        self.winName = winName
    def create(self):
        if cmds.window(self.winName, exists=True):
            cmds.deleteUI(self.winName)
        self.window = cmds.window(self.winName, title=self.winTitle, w=250, h=150)
        cmds.rowLayout (' MainRow ', numberOfColumns=2)
        cmds.columnLayout ('Column1', cat = ('both', 0), adjustableColumn = True , parent = 'MainRow')
        cmds.columnLayout ('Column2', cat = ('both', 0), parent = 'MainRow')
        cmds.setParent ('Column1')
        cmds.button (label='Check (faces) Ngons', command = self.singleNgons)
        cmds.button (label='Check (Object) Poly', command = self.singlePoly)
        cmds.button (label='Check (Vertices) Poles', command = self.poles)
        cmds.showWindow(self.window)

    def selection_grab(self):
        '''--------------------------------------------------------------------------------------------------------------------------------------
        Common selection query
        --------------------------------------------------------------------------------------------------------------------------------------'''        
        getSel=cmds.ls(sl=1, fl=1)
        if getSel:
            pass
        else:
            print "You need to make a selection for this tool to operate on."
            return
        return getSel

    def singleNgons(self, arg=None):
        selObj=self.selection_grab()
        if selObj:
            pass
        else:
            print "select polygon faces"
            return      
        if ".f[" in selObj[0]:
            pass
        else:
            print "You need to make a selection of faces for this tool to interrogate."
            return               
        cmds.select(cl=True)
        if cmds.objExists("Ngons")==True:
            cmds.delete("Ngons")
        cmds.sets(n="Ngons", co=3)
        if cmds.objExists("Tris")==True:
            cmds.delete("Tris")
        cmds.sets(n="Tris", co=3)        
        for face in selObj:
            getComponent = cmds.polyInfo(face, fe=True)
            getVerts=getComponent[0].split(':')[1]
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
        errorFound=cmds.ls(sl=True)
        if (len(errorFound))==0:
            cmds.delete("Tris")
        cmds.select('Ngons', r=True, ne=True)
        cmds.pickWalk(d='Up')
        errorFound=cmds.ls(sl=True, fl=1)
        if (len(errorFound))==0:
            cmds.delete("Ngons")       


    def singlePoly(self, arg=None):
        selObj=self.selection_grab()
        if selObj:
            pass
        else:
            print "select a polygon object"
            return    
        if "." in selObj[0]:
            print "You need to select a polygon object to interogate.(check that you are not in component mode)"
            return     
        else:
            pass 
        cmds.select(cl=True)
        if cmds.objExists("PolyIssues")==True:
            cmds.delete("PolyIssues")
        cmds.sets(n="PolyIssues", co=5)
        cmds.select(selObj)
        errorFound=cmds.polyInfo(selObj, lf=True, nme=True, nmv=True )
        cmds.select (errorFound)
        cmds.ConvertSelectionToVertices(errorFound)
        if errorFound>0:
            print "Polygon error found"
            cmds.sets( fe='PolyIssues')
        cmds.select('PolyIssues', r=True, ne=True)
        cmds.pickWalk(d='Up')
        errorFound=cmds.ls(sl=True)
        if (len(errorFound))==0:
            cmds.delete("PolyIssues")



    def poles(self, arg=None):
        listOne=list()
        listTwo=list()
        selObj=self.selection_grab()
        if selObj:
            pass
        else:
            print "select polygon vertices"
            return        
        if ".vtx[" in selObj[0]:
            pass
        else:
            print "You need to make a selection of vertices for this tool to interrogate."
            return                  
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
        for each in selObj:
            getComponent = cmds.polyInfo(each, ve=True)
            getVerts=getComponent[0].split(':')[1]
            edgeCount=re.findall(r'\d+', getVerts)
            if (len(edgeCount))==3:
                cmds.sets(each, fe='Npoles')
            elif (len(edgeCount))==5:
                cmds.sets(each, fe='Epoles')
            elif (len(edgeCount))>5:
                cmds.sets(each, fe='starpoles')
        cmds.select('starpoles', r=True, ne=True)
        cmds.pickWalk(d='Up')
        errorFound=cmds.ls(sl=True)
        if (len(errorFound))==0:
            cmds.delete("starpoles")
        cmds.select('Npoles', r=True, ne=True)
        cmds.pickWalk(d='Up')
        errorFound=cmds.ls(sl=True)
        if (len(errorFound))==0:
            cmds.delete("Npoles")
        cmds.select('Epoles', r=True, ne=True)
        cmds.pickWalk(d='Up')
        errorFound=cmds.ls(sl=True)
        if (len(errorFound))==0:
            cmds.delete("Epoles")

inst = PolyUI()
inst.create()
