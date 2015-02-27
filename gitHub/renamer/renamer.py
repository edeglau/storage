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
import re, sys, os
from inspect import getsourcefile
from os.path import abspath
getfilePath=str(abspath(getsourcefile(lambda _: None)))
#getfilePath=str('__file__')
filepath= os.getcwd()

gtepiece=getfilePath.split("\\")
getguideFilepath='/'.join(gtepiece[:-2])+"/rigModules/"
sys.path.append(str(getguideFilepath))

import baseFunctions_maya
reload (baseFunctions_maya)
getClass=baseFunctions_maya.BaseClass()


badNameList=[
             "pSphere", 
             "curve", 
             "polySurface"
             ]

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
        cmds.columnLayout ('rColumn5', rs=3, cat = ('both', 0), parent = 'rMainRow', adjustableColumn=True, w=150)
      
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
        cmds.button (label='Guide names',bgc=[0.8, 0.75, 0.6], command = self.guide_name) 
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
        
        cmds.setParent ('rColumn3')
        cmds.text("Custom Prefix and Suffix")
        cmds.separator()
        global prefname
        prefname=cmds.textField()
        cmds.button (label='Add pref', command = self.preff)
        global sufname
        sufname=cmds.textField()
        cmds.button (label='Add suf', command = self.suff)


        cmds.setParent ('rColumn4')
        cmds.text("Shift")
        cmds.separator()
        self.breakName=cmds.textField(text="enter the partial name")
#        self.breakPoint=cmds.textField(text="enter a breakpoint EG:'_")
        cmds.button (label='move to beginning', command = lambda *args:self._shift_beg(breakName=cmds.textField(self.breakName, q=1, text=1)))
        cmds.button (label='move to end', command = lambda *args:self._shift_end(breakName=cmds.textField(self.breakName, q=1, text=1)))   
        cmds.button (label='Shift >>', command = lambda *args:self._shift_right(breakName=cmds.textField(self.breakName, q=1, text=1)))
        cmds.button (label='<< Shift', command = lambda *args:self._shift_left(breakName=cmds.textField(self.breakName, q=1, text=1)))
        cmds.button (label='Number>>', command = lambda *args:self._insertNumberRight(breakName=cmds.textField(self.breakName, q=1, text=1)))
        cmds.button (label='<<Number', command = lambda *args:self._insertNumberLeft(breakName=cmds.textField(self.breakName, q=1, text=1)))

        
        cmds.setParent ('rColumn5')
        cmds.text( label='Numbers' )
        cmds.separator()
        cmds.gridLayout('listArrangmentButtonLayout', p='rColumn5', numberOfColumns=2, cellWidthHeight=(75, 20))
        self.padding=cmds.optionMenu(p="listArrangmentButtonLayout")
        self.startRange=cmds.textField(text="1")
        cmds.menuItem( label="padding")
        for each in range(6)[1:]:
            cmds.menuItem( label=each)
        cmds.gridLayout('listButtonLayout', p='rColumn5', numberOfColumns=1, cellWidthHeight=(150, 20))            
        cmds.button (label='Number Suffix', command = self.nmbrs, p="listButtonLayout")
        cmds.button (label='Remove numbers', command = self.rnmbrs, p='listButtonLayout')
        cmds.button (label='Remove non-tail numbers', command = self.rMid_nmbrs, p="listButtonLayout")
        cmds.button (label='Remove tail numbers', command = self.rEnd_nmbrs, p="listButtonLayout")
        cmds.button (label='Remove underscores', command = self.runders, p="listButtonLayout")
                
    
        cmds.window(self.window, e=1, w=430, h=103)
        cmds.showWindow(self.window)   

    def error_message_num(self):
        getError= "Cannot name. A number cannot be at the beginning of a name."     
        return getError

    def checkName(self, newName):
        findNumber=False
        try:
            getAnInt=int(newName[0])
            if getAnInt:
                findNumber=True
        except:
            pass  
        if newName[0]=="0":
            findNumber=True
        return findNumber
            
    def _shift_end(self, breakName):
        selObj=cmds.ls(sl = True, fl=1)
        for each in selObj:
            if breakName in each:
                ffile=re.sub(breakName, '', each)     
                newname=ffile+breakName
                findNumber=self.checkName(newname) 
                if findNumber==True:
                    print self.error_message_num()
                    return
                else:
                    aNewString=cmds.rename(each, newname) 

    def guide_name(self, arg=None):
        selectionCheck=cmds.ls(sl=1, fl=1)         
        guideName=getClass.fetchName()
        if selectionCheck:
            for indexNumber, eachSelObj in enumerate(xrange(len(selectionCheck) - 1)):
                newname=getClass.guide_names(indexNumber, guideName)
                print newname
                cmds.rename(selectionCheck[eachSelObj], newname)
                
    def _shift_beg(self, breakName):
        selObj=cmds.ls(sl = True, fl=1)
        for each in selObj:
            if breakName in each:            
                ffile=re.sub(breakName, '', each)     
                newname=breakName+ffile
                findNumber=self.checkName(newname)  
                if findNumber==True:
                    print self.error_message_num()
                else:
                    aNewString=cmds.rename(each, newname)  
      

    def _shift_left(self, breakName):
        selObj=cmds.ls(sl = True, fl=1)
        for each in selObj:
            if breakName in each:
                eachName=each.split(str(breakName))
                beginningPortion=eachName[0]
                endportion=eachName[1]
                newname=beginningPortion[:-1]+breakName+beginningPortion[-1:]+endportion
                findNumber=self.checkName(newname)  
                if findNumber==True:
                    print self.error_message_num()
                else:                
                    aNewString=cmds.rename(each, newname)

    def _shift_right(self, breakName):
        selObj=cmds.ls(sl = True, fl=1)
        for each in selObj:
            if breakName in each:
                eachName=each.split(str(breakName))
                beginningPortion=eachName[0]
                endportion=eachName[1]
                newname=beginningPortion+endportion[:1]+breakName+endportion[1:]
                findNumber=self.checkName(newname)  
                if findNumber==True:
                    print self.error_message_num()
                else:                
                    aNewString=cmds.rename(each, newname)                   
                    
                
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
        for item in selObj:
            aNewString=cmds.rename(item, item.replace( '%s'%old_String, '%s'%new_String))
            
    def _replace_all(self, arg=None):
        selObj=cmds.ls("*")
        old_String=cmds.textField(old, q=True, text=True)
        new_String=cmds.textField(new, q=True, text=True)     
        for item in selObj:
            aNewString=cmds.rename(item, item.replace( '%s'%old_String, '%s'%new_String))
            
    def rename(self, arg=None):
        selObj=cmds.ls(sl = True)  
        new_String=cmds.textField(self.relname, q=True, text=True)
        findNumber=self.checkName(new_String)  
        if findNumber==True:
            print self.error_message_num()
        else:
            for item in selObj:
                cmds.rename(item, new_String)
    
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
    
    def _insertNumberRight(self, breakName):
        getPadd=cmds.optionMenu(self.padding, q=1, v=1)
        getstartRange=cmds.textField(self.startRange, q=1, text=1)
        getstartRange=int(getstartRange)
        selObj=cmds.ls(sl=True)
        if getPadd=="padding":
            print "select a padding for your number" 
            return  
        else:
            pass         
        for index, each in enumerate(selObj):
            if breakName in each:  
                getRange=index+getstartRange
                getPadding=self.getpadd(getRange)                
                eachName=each.split(str(breakName))
                beginningPortion=eachName[0]
                endportion=eachName[1]                 
                nmbrname=beginningPortion+str(breakName)+str(getPadding)+endportion
                findNumber=self.checkName(nmbrname)  
                if findNumber==True:
                    print self.error_message_num()
                else:                                  
                    aNewString=cmds.rename(each, nmbrname) 
                
    def _insertNumberLeft(self, breakName):
        getPadd=cmds.optionMenu(self.padding, q=1, v=1)
        getstartRange=cmds.textField(self.startRange, q=1, text=1)
        getstartRange=int(getstartRange)
        selObj=cmds.ls(sl=True)
        if getPadd=="padding":
            print "select a padding for your number" 
            return  
        else:
            pass         
        for index, each in enumerate(selObj):
            if breakName in each:  
                getRange=index+getstartRange
                getPadding=self.getpadd(getRange)                
                eachName=each.split(str(breakName))
                beginningPortion=eachName[0]
                endportion=eachName[1]                 
                nmbrname=beginningPortion+str(getPadding)+str(breakName)+endportion
                findNumber=self.checkName(nmbrname)  
                if findNumber==True:
                    print self.error_message_num()
                else:                                  
                    aNewString=cmds.rename(each, nmbrname) 

    def nmbrs(self, arg=None):
        getstartRange=cmds.textField(self.startRange, q=1, text=1)
        getstartRange=int(getstartRange)
        getPadd=cmds.optionMenu(self.padding, q=1, v=1)
        fleName=cmds.ls(sl=True)
        if getPadd=="padding":
            print "select a padding for your number" 
            return  
        else:
            pass       
        for index, item in enumerate(fleName):
#            ffile=re.sub(r'\d[1-9]*', '', fleName[item]) 
            getRange=getstartRange+index      
            getPadding=self.getpadd(getRange)
            nmbrname=item+str(getPadding)
            cmds.rename(item, nmbrname)
            
    def getpadd(self, index):
        getPadd=cmds.optionMenu(self.padding, q=1, v=1)
        if getPadd=="1":
            getNum="%01d" % (index,)
        elif getPadd=="2":
            getNum="%02d" % (index,)
        elif getPadd=="3":
            getNum="%03d" % (index,)
        elif getPadd=="4":
            getNum="%04d" % (index,)
        elif getPadd=="5":
            getNum="%05d" % (index,)
        else:
            getNum=index
        return getNum
            
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
        for item in nodName:   
            getPortions=re.split(r'(\d+)', item)
            if len(getPortions[-1:][0])<1:
                each=''.join(getPortions[:-2])
                sub_Name=re.sub(r'\d[1-9]*', '', each)
                getEndNumbs=''.join(getPortions[-2:])
                newSub_Name=sub_Name+getEndNumbs
            else:
                sub_Name=re.sub(r'\d[1-9]*', '', item)
            cmds.rename(item ,newSub_Name)
            
    def rBeg_nmbrs(self, arg=None):
        nodName=cmds.ls(sl=True)
        for item in range (len(nodName)):             
            sub_Name=re.sub(r"(^|\W)\d+", "", nodName[item])
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
        for each in badNameList:
            if cmds.objExists(each+'*'):
                cmds.select (each+'*', hierarchy=False, add=True)    
                cmds.sets( fe="badNames")
                              
#        if cmds.objExists('pSphere*'):
#            cmds.select ('pSphere*', hierarchy=False, add=True)    
#            cmds.sets( fe="badNames")
#            
#        if cmds.objExists('curve*'):
#            cmds.select ('curve*', hierarchy=False, add=True)
#            cmds.sets( fe="badNames")
#        
#            
#        if cmds.objExists('polySurface*'):
#            cmds.select ('polySurface*', hierarchy=False, add=True)
#            cmds.sets( fe="badNames")
        
        if cmds.objExists('badNames'):
            cmds.select('badNames', r=True, ne=True)
            shoo=cmds.ls(sl=True)
            cmds.pickWalk (d='up')
            pete=cmds.ls(sl=True)  
            if (len(pete))>0:
                print("The selected object(s) don't have very descriptive names.")
            else:
                cmds.select(cl=True)
                print(" no bad names exists.")
            cmds.delete(shoo)

inst=myUI()
      
