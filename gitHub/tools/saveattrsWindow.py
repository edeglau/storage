import maya.cmds as cmds
from functools import partial
from string import *
import re
import maya.mel
import os, subprocess, sys, platform, glob
from os  import popen
from sys import stdin
import sys
#import win32clipboard
import operator
import glob


import random
import maya.cmds as cmds

import maya.mel
import platform
import numpy
OSplatform=platform.platform()
from numpy import arange
import re

getdef=[".sx", ".sy", ".sz", ".rx", ".ry", ".rz", ".tx", ".ty", ".tz", ".visibility"]
getScenePath=cmds.file(q=1, location=1)

'''MG rigging modules'''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons Attribution 4.0 International 4.0 (CC BY 4.0)'
# 'This work is licensed under a Creative Commons Attribution-ShareAlike 3.0 Australia (CC BY-SA 3.0 AU)'
'http://creativecommons.org/licenses/by-sa/3.0/au/'


getScenePath=cmds.file(q=1, location=1)
getPathSplit=getScenePath.split("/")
folderPath='\\'.join(getPathSplit[:-1])+"\\"
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets

class selectionchs_win(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(selectionchs_win, self).__init__(parent = None)

        self.setWindowTitle("Selections")
        self.central_widget=QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.masterLayout=QtWidgets.QGridLayout(self.central_widget)
        self.masterLayout.setAlignment(QtCore.Qt.AlignTop)


        self.myform = QtWidgets.QFormLayout()
        self.layout = QtWidgets.QGridLayout()
        self.masterLayout.addLayout(self.layout, 0,0,1,1)

        self.SelectionSetupLayout = QtWidgets.QGridLayout()
        self.selection_widgetframe = QtWidgets.QFrame()
        self.selection_widgetframe.setLayout(self.SelectionSetupLayout)
        self.SelectionSetupLayout.addLayout(self.myform, 0,0,1,1)
        self.layout.addLayout(self.SelectionSetupLayout, 0,0,1,1)
        self.add_widgets()

        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(self.selection_widgetframe)
        scroll.setWidgetResizable(False)
        self.layout.addWidget(scroll, 1,0,1,1)
        self.setLayout(self.layout)

    def add_widgets(self):
        self.sel_order_layout = QtWidgets.QHBoxLayout()
        self.myform.addRow(self.sel_order_layout) 
        self.prnt_verbose_button = QtWidgets.QPushButton("save")
        self.prnt_verbose_button.clicked.connect(lambda: self.saveSelection())
        self.sel_order_layout.addWidget(self.prnt_verbose_button)  
        self.prnt_verbose_button = QtWidgets.QPushButton("load")
        self.prnt_verbose_button.clicked.connect(lambda: self.openSelection())
        self.sel_order_layout.addWidget(self.prnt_verbose_button)    


    def _make_set_from_selection_list(self, message, selObj):
        '''----------------------------------------------------------------------------------
        prompt to see if user wants to continue with multiple selected
        ----------------------------------------------------------------------------------'''          
        result = cmds.promptDialog(
            title='Confirm',
            message=message,
            button=['Continue','Cancel'],
            defaultButton='Continue',
            cancelButton='Cancel',
            dismissString='Cancel' )
        if result == 'Continue':
            text = self.saveWindow(selObj)
        else:
            print ("cancelled")
            return

    def saveSelection(self):
        selObj=cmds.ls(sl=1, fl=1, sn=1)
        if len(selObj)==1:
            text = self.saveWindow(selObj)
        elif len(selObj)<1:
            print ("select something")
            return
        else:
            message = "You have more than one selected. Are you sure you want to proceed?"
            self._make_set_from_selection_list(message, selObj)
            return

    def saveWindow(self, selObj):
        getScenePath=cmds.file(q=1, location=1)
        getPathSplit=getScenePath.split("/")
        folderPath='\\'.join(getPathSplit[:-1])+"\\"        
        if "Windows" in OSplatform:
            newfolderPath=re.sub(r'/',r'\\', folderPath)
        if "Linux" in OSplatform:
            newfolderPath=re.sub(r'\\',r'/', folderPath)
        folderBucket=[]
        winName = "Save attribute"
        winTitle = winName
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=1280, h=100 )
        cmds.menuBarLayout(h=30)
        stringField='''"Save Anim/Attr" (launches window)a home made scripted save anim keys and attribute values
    into external file(s)(works on a heirarchy). Put full file path with preferred name of
    object in text field("/usr/people/<user>/joint4"). save button saves out file. Can add
    more to save from add selected at top. Will save out a file
    EG:"/usr/people/<user>/joint4.txt"

        * Step 1: select object
        * Step 2: pressing save will create .txt files that will contain the animation
            and attriute values for heirarchy(if applicable) within the path indicated
            and name of file indicated in field

         "ADD SELECTION" - button
            Adds a slot for new object (each parent is added seperately)
        "SAVE" - button
            Will change the value on the attribute that is currently
                visible in the drop down menu
        "OPEN FOLDER" - button
            opens the folder window for path indicated
        "ATTR DICT" - button
            prints out an attriubute dictionary for personal use(see script editor)
            useful for writing a "setAttr" script on custom setups'''
        self.fileMenu = cmds.menu( label='Help', pmc=lambda *args:self.helpWin(stringField))        
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=1270)
        cmds.frameLayout('bottomFrame', label='', lv=0, nch=1, borderStyle='in', bv=1, p='selectArrayRow')     
        cmds.gridLayout('topGrid', p='bottomFrame', numberOfColumns=1, cellWidthHeight=(1270, 20))   
        cmds.text("Objects to save attributes from:")
        cmds.button (label='Add selected(one at a time)', p='topGrid', command = lambda *args:self._add_function())
        cmds.gridLayout('listBuildButtonLayout', p='bottomFrame', numberOfColumns=1, cellWidthHeight=(1250, 20))
        cmds.text(label="") 
        objNameFile=newfolderPath+str(selObj[0])       
        fieldBucket=[]
        cmds.rowLayout  (' listBuildButtonLayout ', w=600, numberOfColumns=6, cw6=[1000, 40, 40, 40, 40, 1], ct6=[ 'both', 'both', 'both',  'both', 'both', 'both'], p='bottomFrame')
        self.getName=cmds.textField(h=25, p='listBuildButtonLayout', text=objNameFile)
        cmds.button (label='Save', w=90, p='listBuildButtonLayout', command = lambda *args:self._save_anim_heirarchy(selObj, fileName=cmds.textField(self.getName, q=1, text=1)))            
        cmds.button (label='Save_constrained', w=90, p='listBuildButtonLayout', command = lambda *args:self._save_constrained(selObj, fileName=cmds.textField(self.getName, q=1, text=1)))            
        cmds.button (label='Open folder', w=60, p='listBuildButtonLayout', command = lambda *args:self._open_defined_path(destImagePath=cmds.textField(self.getName, q=1, text=1)))
        cmds.button (label='Attr dict', w=60, ann=" prints a dictionary with attributes(for dev)", p='listBuildButtonLayout', command = lambda *args:self._printAttributes())
        cmds.showWindow(window)        

    def _save_anim_heirarchy(self, selObj, fileName):       
        print (fileName)
        foldername=fileName+selObj[0]+'.txt'
        inp=open(foldername, 'w+')
        for each in selObj:
            filterNode=["animCurve"]
            dirDict={}
            getStrtRange=cmds.playbackOptions(q=1, ast=1)#get framerange of scene to set keys in iteration
            getEndRange=cmds.playbackOptions(q=1, aet=1)#get framerange of scene to set keys in iteration
            allChildren=cmds.listRelatives(each, ad=1)
            getChildren=allChildren
            try:
                getChildren=[each]+getChildren
            except:
                getChildren=[each]
            for eachChildTree in getChildren:
                inp.write('\n'+str(eachChildTree)+">>")
                getListedAttr=[(attrib) for attrib in cmds.listAttr (eachChildTree, w=1, a=1, s=1,u=1) if "solverDisplay" not in attrib]
                for eachAttribute in getListedAttr:
                    try:
                        findFact=cmds.listConnections( eachChildTree+'.'+eachAttribute, d=False, s=True )
                        # findFact=[(eachConnected) for eachConnected in cmds.nodeType(ls_str[0].split(".")[0], i=1) for eachFilter in filterNode if eachConnected==eachFilter]
                        if findFact==None:                            try:
                                attrVal=cmds.getAttr(eachChildTree+"."+eachAttribute)
                                inp.write("<"+str(eachAttribute+";"))
                                makeDict={0.0:attrVal}
                                inp.write(str(makeDict))
                            except:
                                pass
                        else:
                            try:
                                dirDict={}
                                frames=cmds.keyframe(eachChildTree, attribute=eachAttribute, time=(getStrtRange,getEndRange), query=True, timeChange=True)
                                values=cmds.keyframe(eachChildTree, attribute=eachAttribute, time=(getStrtRange,getEndRange), query=True, valueChange=True)
                                for eachFrame, valueitem in map(None, frames, values):
                                    makeDict={eachFrame:valueitem}
                                    dirDict.update(makeDict)
                                inp.write("<"+str(eachAttribute+";"))                                    
                                inp.write(str(dirDict))
                            except:
                                pass
                    except:
                        pass
            inp.close()   
            print ("saved as "+foldername)
    def _save_constrained(self, each, fileName):   
        getBaseClass.store_obj_matrix_pt(each, fileName)

    def store_obj_matrix_pt(self, objectSel, fileName):
        '''plots transforms off of an object with constraint to a text file'''
        objectSel=cmds.ls(sl=1)
        if len(objectSel)>0:
            pass
        else:
            print ("Select 1 object" )
            return     
        fileName=fileName+'.txt'
        print (fileName)
        if "Windows" in OSplatform:
            if not os.path.exists(fileName): os.makedirs(fileName)
        if "Linux" in OSplatform:
            inp=open(fileName, 'w+')
        getTopRange=cmds.playbackOptions(q=1, max=1)+1#get framerange of scene to set keys in iteration 
        getLowRange=cmds.playbackOptions(q=1, min=1)-1#get framerange of scene to set keys in iteration 
        getRange=arange(getLowRange,getTopRange, 1 )
        collection_of_valueTX={}
        collection_of_valueTY={}
        collection_of_valueTZ={}
        collection_of_valueRX={}
        collection_of_valueRY={}
        collection_of_valueRZ={}        for each_obj in objectSel:            
            inp.write('\n'+str(each_obj)+">>")        
            for each_frame in getRange:
                cmds.currentTime(each_frame)            
                transform=cmds.xform(each_obj, q=True, ws=1, t=True)
                rotation=cmds.xform(each_obj, q=True, ws=1, ro=True)
                if len(transform)<4:
                    pass
                else:
                    posBucket=[]
                    posBucket.append(self.median_find(transform[0::3]))
                    posBucket.append(self.median_find(transform[1::3]))
                    posBucket.append(self.median_find(transform[2::3]))
                    transform=posBucket
                # print str(each_frame)+":"+str(transform[0])
                makeDictTX = {each_frame:transform[0]}
                collection_of_valueTX.update(makeDictTX)
                makeDictTY = {each_frame:transform[1]}
                collection_of_valueTY.update(makeDictTY)
                makeDictTZ = {each_frame:transform[2]}
                collection_of_valueTZ.update(makeDictTZ)
                makeDictRX = {each_frame:rotation[0]}
                collection_of_valueRX.update(makeDictRX)
                makeDictRY = {each_frame:rotation[1]}
                collection_of_valueRY.update(makeDictRY)
                makeDictRZ = {each_frame:rotation[2]}
                collection_of_valueRZ.update(makeDictRZ)
                cmds.currentTime(each_frame)
            inp.write("<translateX;")
            inp.write(str(collection_of_valueTX))
            inp.write("<translateY;")
            inp.write(str(collection_of_valueTY))
            inp.write("<translateZ;")
            inp.write(str(collection_of_valueTZ))
            inp.write("<rotateX;")
            inp.write(str(collection_of_valueRX))
            inp.write("<rotateY;")
            inp.write(str(collection_of_valueRY))
            inp.write("<rotateZ;")
            inp.write(str(collection_of_valueRZ))
        inp.close()
    def _open_defined_path(self, destImagePath):
        folderPath='\\'.join(destImagePath.split("/")[:-1])+"\\"        
        self.opening_folder(folderPath)

    def _load_defined_path(self, newfolderPath, grabFileName):
        printFolder=newfolderPath+grabFileName     
        self.load_attributes(printFolder)

    def getWorkPath(self, getScenePath):
        filebucket=[]
        getPathSplit=getScenePath.split("/")
        folderPath='\\'.join(getPathSplit[:-1])+"\\"        
        if "Windows" in OSplatform:
            newfolderPath=re.sub(r'/',r'\\', folderPath)
        if "Linux" in OSplatform:
            newfolderPath=re.sub(r'\\',r'/', folderPath)
        getPath=newfolderPath+"*.txt"
        files=glob.glob(getPath)
        for each in files:
            if "Windows" in OSplatform:
                getfileName=each.split("\\")
            if "Linux" in OSplatform:
                getfileName=each.split("/")         
            getFile=getfileName[-1:][0]
            filebucket.append(getFile)         
        return files, getPath, newfolderPath, filebucket
    def _printAttributes(self):
        selObj=cmds.ls(sl=1, fl=1)
        for each in selObj:       
            newDict={}     
            getListedAttr=[(attrib) for attrib in cmds.listAttr (each, w=1, a=1, s=1,u=1) if "solverDisplay" not in attrib]
            getListedAttr_sort =sorted(getListedAttr)
            for eachAttribute in getListedAttr_sort:
                print (eachAttribute)
                try:
                    attrVal=cmds.getAttr(each+"."+eachAttribute)
                    makeDict={eachAttribute:attrVal}
                    newDict.update(makeDict)
                except:
                    pass
            print ("{")
            for key, value in newDict.items():
                print ("'"+str(key)+"':"+str(value)+",")
            print ("}")
    def openSelection(self, arg=None):
        getScenePath=cmds.file(q=1, location=1)
        files, getPath, newfolderPath, filebucket=self.getWorkPath(getScenePath)    
        winName = "Open attributes"
        winTitle = winName
        getPathSplit=getScenePath.split("/")
        folderPath='\\'.join(getPathSplit[:-1])+"\\"          
        openFolderPath=folderPath+"\\"   
        selObj=cmds.ls(sl=1, fl=1)
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=1280, h=280 )
        cmds.menuBarLayout(h=30)
        stringField='''"Load Anim/Attr" (launches window)Opens anim keys and attribute values from external file(s)
    (works on a heirarchy). Put full path with no of object in the text field("/usr/people/
    <user>/"). Press refresh and it will repopulate the drop down for available .txt files;
    stick to the name of your object to reload anim

        * Step 1: select object - needs to have a matching name
        * Step 2: fill in path(without name EG: "/usr/people/<user>/")
        * Step 3: press "refresh folder"
        * Step 4: if text file available, it should populate in the
            drop down menu. Check path name and if animation is saved first
            if drop down remains empty
        * Step 5: press "Load" button will load animation onto selection

         "REFRESH FOLDER" - button
            Adds a slot for new object (each parent is added seperately)
        "WORKPATH" - button
            Will change the value on the attribute that is currently
                visible in the drop down menu
        "LOAD" - button
            loads animation
        "OPEN FOLDER" - button
            opens the folder window for path indicated '''        self.fileMenu = cmds.menu( label='Help', pmc=lambda *args:self.helpWin(stringField))         
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=1270)
        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        cmds.rowLayout  (' rMainRow ', w=600, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=1, cellWidthHeight=(480, 20))
        cmds.button (label='refresh folder', p='listBuildButtonLayout', command = lambda *args:self.refresh_text())
        cmds.button (label='workpath', p='listBuildButtonLayout', command = lambda *args:self.refresh_work_text())      
        self.fileDropName=cmds.optionMenu( label='files')
        for each in filebucket:
            cmds.menuItem( label=each)
        self.pathFile=cmds.textField(h=25, p='listBuildButtonLayout', text=newfolderPath+selObj[0])
        cmds.button (label='Load', p='listBuildButtonLayout', command = lambda *args:self._load_anim_heirarchy(printFolder=cmds.textField(self.pathFile, q=1, text=1), grabFileName=cmds.optionMenu(self.fileDropName, q=1, v=1)))
        cmds.button (label='Open folder', p='listBuildButtonLayout', command = lambda *args:self._open_defined_path(destImagePath=cmds.textField(self.pathFile, q=1, text=1)))         
        cmds.showWindow(window)    def refresh_text(self, arg=None):
        menuItems = cmds.optionMenu(self.fileDropName, q=True, ill=True)
        if menuItems:
            cmds.deleteUI(menuItems)
        getPathSplit=cmds.textField(self.pathFile, q=1, text=1)
        files, getPath, newfolderPath, filebucket=self.getWorkPath(getPathSplit)      
        cmds.optionMenu(self.fileDropName, e=1)
        for each in filebucket:
            cmds.menuItem(label=each, parent=self.fileDropName)    def _load_anim_heirarchy(self, printFolder, grabFileName):
        import ast
        notAttr=["isHierarchicalConnection", "solverDisplay", "isHierarchicalNode", "publishedNodeInfo", "fieldScale_Position", "fieldScale", "fieldScale.fieldScale_Position"]         
        printFolder=printFolder+grabFileName    
        selObj=cmds.ls(sl=1, fl=1)
        if os.path.exists(printFolder):
            pass
        else:
            print (printFolder+"does not exist")
            return
        for each in selObj:
            attribute_container=[]
            getListedAttr=[(attrib) for attrib in cmds.listAttr(each, k=1, s=1, iu=1, u=1, lf=1, m=0) for item in notAttr if item not in attrib]             
            List = open(printFolder).readlines()
            for aline in List:
                if ">>" in aline:
                    getObj=aline.split('>>')[0]
                    getExistantInfo=aline.split('>>')[1]
                    if getExistantInfo!="\n":
                        findAtt=getExistantInfo.split("<")
                        for eachInfo in findAtt:
                            getAnimDicts=eachInfo.split(";")
                            for eachctrl in range(len(getAnimDicts) - 1):
                                current_item, next_item = getAnimDicts[eachctrl], getAnimDicts[eachctrl + 1]
                                # cmds.setAttr(cmds.ls(getObj)[0]+'.'+current_item, value)
                                gethis=ast.literal_eval(next_item)
                                try:
                                    if len(gethis)<2:
                                        for key, value in gethis.items():
                                            for listeditem in getListedAttr:
                                                if current_item==listeditem:
                                                    cmds.setKeyframe( cmds.ls(getObj)[0], t=key, at=current_item, v=value )  
                                except:
                                    pass                                              
                    else:
                        pass
    def helpWin(self, stringField):
        '''--------------------------------------------------------------------------------------------------------------------------------------
        Interface Layout
        --------------------------------------------------------------------------------------------------------------------------------------'''
        # def helpPage(self, arg=None):
        winName = "Description"
        winTitle = winName
        if cmds.window(winName, exists=True):
                deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=700, h=400 )
        menuBarLayout(h=30)
        rowColumnLayout  (' selectArrayRow ', nr=1, w=700)
        frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        rowLayout  (' rMainRow ', w=700, numberOfColumns=6, p='selectArrayRow')
        columnLayout ('selectArrayColumn', parent = 'rMainRow')
        setParent ('selectArrayColumn')
        cmds.gridLayout('txvaluemeter', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(700, 400))
        self.list=cmds.scrollField( editable=False, wordWrap=True, ebg=1,bgc=[0.11, 0.15, 0.15], w=700, text=str(stringField))
        showWindow(window)    def median_find(self, lst):
        even = (0 if len(lst) % 2 else 1) + 1
        half = (len(lst) - 1) / 2
        mysum= sum(sorted(lst)[half:half + even]) / float(even)
        return mysum



inst_mkwin=selectionchs_win()
inst_mkwin.show()       

