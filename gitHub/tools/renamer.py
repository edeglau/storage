'''
Created on Mar 3, 2011

@author: elise.deglau
'''

import maya.cmds as cmds
from functools import partial
from string import *
import re

class myUI:
    

    def __init__(self, winName="namereplace"):
        self.winTitle = "Bulk Custom Renamer"
        self.winName = winName

        if cmds.window(self.winName, exists=True):
            cmds.deleteUI(self.winName)

        self.window = cmds.window(self.winName, title=self.winTitle, w=100, h=50 )
        cmds.rowLayout  (' rMainRow ', numberOfColumns=5)
        cmds.columnLayout ('rColumn1', rs=3, cat = ('both', 0), parent = 'rMainRow', adjustableColumn=True, w=150)
        cmds.columnLayout ('rColumn2', rs=3, cat = ('both', 0), parent = 'rMainRow', adjustableColumn=True, w=150)
        cmds.columnLayout ('rColumn3', rs=3, cat = ('both', 0), parent = 'rMainRow', adjustableColumn=True, w=150)
        cmds.columnLayout ('rColumn4', rs=3, cat = ('both', 0), parent = 'rMainRow', adjustableColumn=True, w=150)
      
        cmds.setParent ('rColumn1')
        cmds.text( label='Naming' )
        cmds.separator()
        global dropname
        cmds.button (label='getname', command = self.eyedropper)
        cmds.separator()
        global relname
        relname=cmds.textField()
        cmds.button (label='rename', command = "renam()")
        cmds.separator()
        cmds.textField(relname, edit=True, enterCommand=('cmds.setFocus(\"' + relname + '\")'))
        cmds.separator()
        cmds.button (label='Check for bad names', command = "badname()") 

        cmds.setParent ('rColumn2')
        cmds.text("Replace name portion")
        cmds.separator()
        cmds.text("old")
        global old
        old=cmds.textField()
        cmds.text("new")
        global new
        new=cmds.textField()
        cmds.button (label='replace', command = "replacr()")    
        cmds.textField(old, edit=True, enterCommand=('cmds.setFocus(\"' + new + '\")') )
        cmds.textField(new, edit=True, enterCommand=('cmds.setFocus(\"' + old + '\")'))        
        
        
        cmds.setParent ('rColumn4')
        cmds.text( label='Numbers' )
        cmds.separator()
        cmds.button (label='Number Suffix', command = self.nmbrs)
        cmds.button (label='Remove numbers', command = self.rnmbrs)
        cmds.button (label='Remove underscores', command = self.runders)
        
        
        cmds.setParent ('rColumn3')
        cmds.text("Custom Prefix and Suffix")
        cmds.separator()
        global prefname
        prefname=cmds.textField()
        cmds.button (label='add pref', command = self.preff)
        global sufname
        sufname=cmds.textField()
        cmds.button (label='add suf', command = self.suff)
        cmds.textField(prefname, edit=True, enterCommand=('cmds.setFocus(\"' + prefname + '\")'))
        cmds.textField(sufname, edit=True, enterCommand=('cmds.setFocus(\"' + sufname + '\")'))
        
                
        cmds.window(self.window, e=1, w=430, h=103)
        cmds.showWindow(self.window)   

        
    def eyedropper(self):
        selObj=cmds.ls(sl = True)
        bug=cmds.textField(old, q=True, text=True)
        who=cmds.textField(new, q=True, text=True)
        for i in range (len(clasp)):
            aNewString=cmds.rename(clasp[i], clasp[i].replace( '%s'%bug, '%s'%who))
            
    def replacr(self):
        clasp=cmds.ls(sl = True)
        bug=cmds.textField(old, q=True, text=True)
        who=cmds.textField(new, q=True, text=True)
        for i in range (len(clasp)):
            aNewString=cmds.rename(clasp[i], clasp[i].replace( '%s'%bug, '%s'%who))
            
    def renam(self):
        clasp=cmds.ls(sl = True)    
        who=cmds.textField(relname, q=True, text=True)
        for i in range (len(clasp)):
            cmds.rename(clasp[i], who)
    
    def preff(self):
        clasp=cmds.ls(sl = True)
        bug = cmds.textField(prefname, q=True, tx=True)
        for i in range (len(clasp)):
           newpref=bug+clasp[i]
           cmds.rename(clasp[i], newpref)
            
    def suff(self):
        clasp=cmds.ls(sl = True)    
        who=cmds.textField(sufname, q=True, text=True)
        for i in range (len(clasp)):
            newpref=clasp[i]+who
            cmds.rename(clasp[i], newpref)
            
    def nmbrs(self):
        fleName=cmds.ls(sl=True)
        for i in range (len(fleName)):
            ffile=re.sub(r'\d[1-9]*', '', fleName[i])
            nmbrname=ffile+'0001'
            cmds.rename(fleName[i], nmbrname)
            
    def rnmbrs(self):
        nodName=cmds.ls(sl=True)
        for i in range (len(nodName)):
            rognm=re.sub(r'\d[1-9]*', '', nodName[i])
            cmds.rename(nodName[i] ,rognm)
            
    def runders(self):
        undrsc=cmds.ls(sl=True)
        for i in range (len(undrsc)):
            lognm=undrsc[i].replace('_', '')
            cmds.rename(undrsc[i] ,lognm)
    
    def badname(self):        
        cmds.select(d=True)
        if cmds.objExists("badNames")==True:
            cmds.delete("badNames")
        cmds.sets(n="badNames", co=5)
        
        
        if cmds.objExists('pSphere*'):
            cmds.select ('pSphere*', hierarchy=False, add=True)    
            cmds.sets( fe="badNames")
            
        if cmds.objExists('curve*'):
            cmds.select ('curve*', hierarchy=False, add=True)
            cmds.sets( fe="badNames")
        
            
        if cmds.objExists('polySurface*'):
            cmds.select ('polySurface*', hierarchy=False, add=True)
            cmds.sets( fe="badNames")
        
    
        if cmds.objExists('badNames'):
            cmds.select('badNames', r=True, ne=True)
            shoo=cmds.ls(sl=True)
            cmds.pickWalk (d='up')
            pete=cmds.ls(sl=True)  
            if (len(pete))>0:
                print("you must give the selected object(s) descriptive names.")
            else:
                cmds.select(cl=True)
                print(" no bad names exists.")
            cmds.delete(shoo)

inst=myUI()
      
