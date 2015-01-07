'''
Created on Mar 3, 2011

@author: elise.deglau
'''

'''Renamer'''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons License'
'http://creativecommons.org/licenses/by-sa/3.0/au/'

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
        cmds.button (label='Getname', command = self.eyedropper)
        cmds.separator()
        global relname
        self.relname=cmds.textField()
        cmds.button (label='Rename', command = self.rename)
        cmds.separator()
        cmds.textField(self.relname, edit=True, enterCommand=('cmds.setFocus(\"' + self.relname + '\")'))
        cmds.separator()
        cmds.button (label='Check for bad names', command = self.badname) 

        cmds.setParent ('rColumn2')
        cmds.text("Replace name portion")
        cmds.separator()
        cmds.text("Old")
        global old
        old=cmds.textField()
        cmds.text("New")
        global new
        new=cmds.textField()
        cmds.button (label='Replace selected', command = self.replacr)    
        cmds.button (label='Replace all', command = self._replace_all)    
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
        cmds.button (label='Add pref', command = self.preff)
        global sufname
        sufname=cmds.textField()
        cmds.button (label='Add suf', command = self.suff)
        cmds.textField(prefname, edit=True, enterCommand=('cmds.setFocus(\"' + prefname + '\")'))
        cmds.textField(sufname, edit=True, enterCommand=('cmds.setFocus(\"' + sufname + '\")'))
        
                
        cmds.window(self.window, e=1, w=430, h=103)
        cmds.showWindow(self.window)   

        
    def eyedropper(self, arg=None):
        selectedObject=cmds.ls(sl=1)
        objListLength=len(selectedObject)
        if objListLength:
            if objListLength >= 1:
                cmds.textField(self.relname,e=1, text=selectedObject[0])  
        else:
            print "nothing selected"

    def replacr(self, arg=None):
        selObj=cmds.ls(sl = True)
        old_String=cmds.textField(old, q=True, text=True)
        new_String=cmds.textField(new, q=True, text=True)
        for item in range (len(selObj)):
            aNewString=cmds.rename(selObj[item], selObj[item].replace( '%s'%old_String, '%s'%new_String))
            
    def _replace_all(self, arg=None):
        selObj=cmds.ls("*")
        old_String=cmds.textField(old, q=True, text=True)
        new_String=cmds.textField(new, q=True, text=True)
        for item in range (len(selObj)):
            aNewString=cmds.rename(selObj[item], selObj[item].replace( '%s'%old_String, '%s'%new_String))
            
    def rename(self, arg=None):
        selObj=cmds.ls(sl = True)    
        new_String=cmds.textField(self.relname, q=True, text=True)
#         new_String=cmds.textField(relname, q=True, text=True)
        for item in range (len(selObj)):
            cmds.rename(selObj[item], new_String)
    
    def preff(self, arg=None):
        selObj=cmds.ls(sl = True)
        old_String = cmds.textField(prefname, q=True, tx=True)
        for item in range (len(selObj)):
           newpref=old_String+selObj[item]
           cmds.rename(selObj[item], newpref)
            
    def suff(self, arg=None):
        selObj=cmds.ls(sl = True)    
        new_String=cmds.textField(sufname, q=True, text=True)
        for item in range (len(selObj)):
            newpref=selObj[item]+new_String
            cmds.rename(selObj[item], newpref)
            
    def nmbrs(self, arg=None):
        fleName=cmds.ls(sl=True)
        for item in range (len(fleName)):
            ffile=re.sub(r'\d[1-9]*', '', fleName[item])
            nmbrname=ffile+'01'
            cmds.rename(fleName[item], nmbrname)
            
    def rnmbrs(self, arg=None):
        nodName=cmds.ls(sl=True)
        for item in range (len(nodName)):
            #===========================================================
            # remove numbers at end
            #===========================================================
#            sub_Name=re.sub("\d+$", "", lognm)         
            #===========================================================
            # remove numbers at beginning
            #===========================================================
#            s = re.sub(r"(^|\W)\d+", "", s)
            #===========================================================
            # remove all numbers
            #===========================================================
#            sub_Name=re.sub(r'\d[1-9]*', '', lognm)                
            sub_Name=re.sub(r'\d[1-9]*', '', nodName[item])
            cmds.rename(nodName[item] ,sub_Name)

    def rMid_nmbrs(self, arg=None):
        nodName=cmds.ls(sl=True)
        for item in range (len(nodName)):
            #===========================================================
            # remove numbers at end
            #===========================================================
#            sub_Name=re.sub("\d+$", "", lognm)         
            #===========================================================
            # remove numbers at beginning
            #===========================================================
#            s = re.sub(r"(^|\W)\d+", "", s)
            #===========================================================
            # remove all numbers
            #===========================================================
#            sub_Name=re.sub(r'\d[1-9]*', '', lognm)                
            sub_Name=re.sub(r'\d[1-9]*', '', nodName[item])
            cmds.rename(nodName[item] ,sub_Name)
    def rBeg_nmbrs(self, arg=None):
        nodName=cmds.ls(sl=True)
        for item in range (len(nodName)):
            #===========================================================
            # remove numbers at end
            #===========================================================
#            sub_Name=re.sub("\d+$", "", lognm)         
            #===========================================================
            # remove numbers at beginning
            #===========================================================
#            s = re.sub(r"(^|\W)\d+", "", s)
            #===========================================================
            # remove all numbers
            #===========================================================
#            sub_Name=re.sub(r'\d[1-9]*', '', lognm)                
            sub_Name=re.sub(r'\d[1-9]*', '', nodName[item])
            cmds.rename(nodName[item] ,sub_Name)
    def rEnd_nmbrs(self, arg=None):
        nodName=cmds.ls(sl=True)
        for item in range (len(nodName)):
            #===========================================================
            # remove numbers at end
            #===========================================================
            sub_Name=re.sub("\d+$", "", nodName[item])         
            cmds.rename(nodName[item] ,sub_Name)
    def runders(self, arg=None):
        undrsc=cmds.ls(sl=True)
        for item in range (len(undrsc)):
            sub_Name=undrsc[item].replace('_', '')
            cmds.rename(undrsc[item] ,sub_Name)
    
    def badname(self, arg=None):        
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
      
