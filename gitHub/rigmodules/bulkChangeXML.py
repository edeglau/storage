import maya.cmds as cmds
from functools import partial
from string import *
import re
import sys, os, glob

import maya.mel

'''MG rigging modules'''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons License'
'http://creativecommons.org/licenses/by-sa/3.0/au/'

getScenePath=cmds.file(q=1, location=1)
getPathSplit=getScenePath.split("/")
folderPath='\\'.join(getPathSplit[:-1])+"\\"
guideFolderPath=folderPath+"Guides\\"
infFolderPath=folderPath+"Influences\\"
xmlFolderPath=folderPath+"XMLskinWeights\\"
class changeXML(object):
    '''--------------------------------------------------------------------------------------------------------------------------------------
    Interface Layout
    --------------------------------------------------------------------------------------------------------------------------------------'''          
    def __init__(self, winName="change XML skins"):
        self.winTitle = "change XML skins or influences"
        self.winName = winName

    def xml_transformUI(self, winName="change XML skins"):
        if cmds.window(self.winName, exists=True):
                cmds.deleteUI(self.winName)

        self.window = cmds.window(self.winName, title=self.winTitle, tbm=1, w=800, h=300 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=800)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        
        cmds.rowLayout  (' rMainRow ', w=800, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.text( label='Full file path(set as specific file path + file name for single edit or file path + "*.*" to change files in bulk)' )
        self.pathText=cmds.textField(w=800, h=25, p='selectArrayColumn', tx=xmlFolderPath+"*.*" )
        cmds.text( label='old string' )
        self.oldJointText=cmds.textField(w=300, h=25, p='selectArrayColumn', tx="LA0095_MaleIncidental4_Rig"    )
        cmds.text( label='new string' )
        self.newJointText=cmds.textField(w=300, h=25, p='selectArrayColumn', tx="LA0095_ZookeeperAdam_Rig"     )              
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(100, 20)) 
        cmds.button (label='Change XMLs', p='listBuildButtonLayout', command = self._change_xml)
        cmds.showWindow(self.window)

    def _change_xml(self, arg=None):
        pathText=cmds.textField(self.pathText,q=True, text=True)
        oldJointText=cmds.textField(self.oldJointText,q=True, text=True)
        newJointText=cmds.textField(self.newJointText,q=True, text=True)
        print pathText
        files=glob.glob(pathText)
        for each in files: 
            dataFromTextFile=open(each).read()
            dataFromTextFile=dataFromTextFile.replace(oldJointText, newJointText)
            replacedDataTextFile=open(each, 'w')
            replacedDataTextFile.write(dataFromTextFile)
            print dataFromTextFile
            replacedDataTextFile.close()          
        '''----------------------------------------------------------------------------------
        Common add to list function
        ----------------------------------------------------------------------------------'''  

inst = changeXML()
inst.xml_transformUI()

      