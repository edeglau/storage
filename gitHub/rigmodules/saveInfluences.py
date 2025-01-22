import maya.cmds as cmds
from functools import partial
from string import *
import re, glob
import maya.mel
import os, subprocess, sys, platform
from os  import popen
from sys import stdin
#import win32clipboard
import operator

__author__ = "Elise Deglau"
__version__ = 1.00
  
# filepath=( 'G:\\_PIPELINE_MANAGEMENT\\Published\\maya\\AutoRig_MG\\rigmodules\\' )
# folderPath="C:\\temp\\influences\\"

getScenePath=cmds.file(q=1, location=1)
getPathSplit=getScenePath.split("/")
folderPath='\\'.join(getPathSplit[:-1])+"\\"
filepath= os.getcwd()
sys.path.append(str(filepath))
import baseFunctions_maya
reload (baseFunctions_maya)
getClass=baseFunctions_maya.BaseClass()

guideFolderPath=folderPath+"Guides\\"
infFolderPath=folderPath+"Influences\\"
xmlFolderPath=folderPath+"XMLskinWeights\\"

class savingInfluences(object):
    '''--------------------------------------------------------------------------------------------------------------------------------------
    Interface Layout
    --------------------------------------------------------------------------------------------------------------------------------------'''          
    def save_influences(self, arg=None):
        getSelected=cmds.ls(sl=1, fl=1)[0]
        winName = "Save guides filename"
        winTitle = winName
        global fileSaveName
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)

        window = cmds.window(winName, title=winTitle, tbm=1, w=600, h=100 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=600)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        
        cmds.rowLayout  (' rMainRow ', w=600, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=1, cellWidthHeight=(600, 20))      
        fileSaveName=cmds.textField(w=350, h=25, p='listBuildButtonLayout', text=infFolderPath)    
        cmds.button (label='Save', p='listBuildButtonLayout', command = lambda *args:self._save_influence_function())
        cmds.button (label='Open folder', p='listBuildButtonLayout', command = lambda *args:self._launch_exp(folderPath))
        cmds.showWindow(window)            
                
    def _launch_exp(self, folderPath):
        destImagePath=folderPath
        print destImagePath
        self.get_path(destImagePath)    
        
    def get_path(self, path):
        print path
        if '\\\\' in path:
            newpath=re.sub(r'\\\\',r'\\', path)
            os.startfile(r'\\'+newpath[1:])    
        else:
            os.startfile(path)
                     
    def _save_influence_function(self):
        filename=cmds.textField(fileSaveName, q=1, text=True)     
        if not os.path.exists(filename): os.makedirs(filename) 
        getSkinned=cmds.ls(sl=1)
        for each in getSkinned:
            self._save_influence_callup(filename, each)            
            
    def _save_influence_callup(self, filename, meshSkin):
        if not os.path.exists(filename): os.makedirs(filename)
        if ":" in meshSkin:
            getName=meshSkin.split(":")
            getName=getName[1:]
        else:
            getName=[meshSkin]
        printFolder=filename+getName[0]+".txt" 
        skinID, getInfluences=getClass.skinnedBones(meshSkin)
        for item in getInfluences:
            print item
        print str(meshSkin)+":"+str(getInfluences)
        inp=open(printFolder, 'w+')
        inp.write(str(meshSkin)+":"+str(getInfluences)+'\r\n')
        inp.close()  

                        
    def open_influence(self, arg=None):    
        getSelected=cmds.ls(sl=1, fl=1)[0]
        getPath=folderPath+"*.*"
        files=glob.glob(getPath)   
        makeBucket=[] 
        for each in files:
            getfileName=each.split("\\")
            getFile=getfileName[-1:][0]
            makeBucket.append(getFile)
        winName = "Open influences"
        winTitle = winName
        global fileOpenName
#         files=glob.glob(getPath)       
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)

        window = cmds.window(winName, title=winTitle, tbm=1, w=250, h=100 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=250)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        
        cmds.rowLayout  (' rMainRow ', w=200, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=1, cellWidthHeight=(200, 20))      
#         fileName=cmds.textField(w=120, h=25, p='listBuildButtonLayout')    
        fileOpenName=cmds.textField(w=120, h=25, p='listBuildButtonLayout', text=folderPath)    
        cmds.button (label='Open', p='listBuildButtonLayout', command = lambda *args:self._open_influence_function())
        cmds.button (label='Open folder', p='listBuildButtonLayout', command = lambda *args:self._launch_exp(getPath))
        cmds.showWindow(window)                 
#     def open_influence(self, arg=None):    
#         getSelected=cmds.ls(sl=1, fl=1)[0]
#         getPath=folderPath+"*.*"
#         files=glob.glob(getPath)   
#         makeBucket=[] 
#         for each in files:
#             getfileName=each.split("\\")
#             getFile=getfileName[-1:][0]
#             makeBucket.append(getFile)
#         winName = "Open influences"
#         winTitle = winName
#         global fileName
# #         files=glob.glob(getPath)       
#         if cmds.window(winName, exists=True):
#                 cmds.deleteUI(winName)
# 
#         window = cmds.window(winName, title=winTitle, tbm=1, w=250, h=100 )
# 
#         cmds.menuBarLayout(h=30)
#         cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=250)
# 
#         cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
#         
#         cmds.rowLayout  (' rMainRow ', w=200, numberOfColumns=6, p='selectArrayRow')
#         cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
#         cmds.setParent ('selectArrayColumn')
#         cmds.separator(h=10, p='selectArrayColumn')
#         cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=1, cellWidthHeight=(200, 20))      
# #         fileName=cmds.textField(w=120, h=25, p='listBuildButtonLayout')    
#         fileName=cmds.optionMenu( label='files')
#         for each in makeBucket:
#             cmds.menuItem( label=each) 
# #         for (root, directories, files) in os.walk(getPath):            
# #             for filename in files: 
# #                 cmds.menuItem( label=filename)   
#         cmds.button (label='Open', p='listBuildButtonLayout', command = lambda *args:self._open_influence_function())
#         cmds.button (label='Open folder', p='listBuildButtonLayout', command = lambda *args:self._launch_exp(getPath))
#         cmds.showWindow(window)                 


    def _open_influence_function(self):  
        filename=cmds.textField(fileOpenName, q=1, text=True)   
        getSelected=cmds.ls(sl=1, fl=1)
        guideDict={}
        for item in getSelected:
            self.open_influence_callup(filename, item)
            
    def open_influence_callup(self, filename, item):
        if ":" in item:
            getName=item.split(":")
            getName=getName[1:]
        else:
            getName=[item]
        printFolder=filename+getName[0]+".txt"
        inp=open(printFolder, 'r')
        List = open(printFolder).readlines()            
        jointBucket=[]
        for each in List:
            getDictParts=each.split('[')
            for jointList in getDictParts[1:]:
                getEachJoint=jointList.split(',  ')
                for firstJoint in getEachJoint:
#                     print firstJoint
                    isolateFirstJoint=firstJoint.split("', u'")                                     
                    for unicodeJointString in isolateFirstJoint:
                        if "]" in unicodeJointString and "[" in unicodeJointString:
                            isolateJoint=unicodeJointString.split("']")[0]
                            isolateJoint=isolateJoint.split("['")[1]                       
                            jointBucket.append(isolateJoint)                        
                        elif "u'" in unicodeJointString and "]" in unicodeJointString:
                            isolateJoint=unicodeJointString.split("u'")[1]
                            isolateJoint=isolateJoint.split("']")[0]                            
                            jointBucket.append(isolateJoint)
                        elif "u'" in unicodeJointString:
                            isolateJoint=unicodeJointString.split("u'")[1]
                            jointBucket.append(isolateJoint)
                        elif "[" in unicodeJointString:
                            isolateJoint=unicodeJointString.split("['")[1]
                            jointBucket.append(isolateJoint)
                        else:
                            jointBucket.append(unicodeJointString)
#                     if "]" in firstJoint:
#                         print isolateJoint
# #                         isolateJoint=firstJoint.split("u'")[1]
#                         isolateJoint=isolateJoint.split("']")[0]   
#                         jointBucket.append(isolateJoint)                             
        cmds.select(item)
        cmds.select(jointBucket[0], add=1)
        cmds.skinCluster()
#         print jointBucket[0]
        for eachItem in jointBucket[2:]:
            if "']" in eachItem:
                eachItem=eachItem.split("']")[0]  
#                 print "uhoh"
            print eachItem
            try:
                cmds.skinCluster(item, e=1, ai=eachItem)
                print eachItem+" is attached to "+item
            except:
                pass
            
    def open_influence_multi_callup(self, filename, item):
#         if ":" in item:
#             getName=item.split(":")
#             getName=getName[1:]
#         else:
#             getName=[item]      
        getName=[item]      
        printFolder=folderPath+getName[0]+".txt"
        print printFolder
        inp=open(printFolder, 'r')
        List = open(printFolder).readlines()            
        jointBucket=[]
        for each in List:
            getDictParts=each.split('[')
            for jointList in getDictParts[1:]:
                getEachJoint=jointList.split(',  ')
                for firstJoint in getEachJoint:
                    isolateFirstJoint=firstJoint.split("', u'")                                     
                    for unicodeJointString in isolateFirstJoint:
                        if "]" in unicodeJointString and "[" in unicodeJointString:
                            isolateJoint=unicodeJointString.split("']")[0]
                            isolateJoint=isolateJoint.split("['")[1]                       
                            jointBucket.append(isolateJoint)                        
                        elif "u'" in unicodeJointString and "]" in unicodeJointString:
                            isolateJoint=unicodeJointString.split("u'")[1]
                            isolateJoint=isolateJoint.split("']")[0]                            
                            jointBucket.append(isolateJoint)
                        elif "u'" in unicodeJointString:
                            isolateJoint=unicodeJointString.split("u'")[1]
                            jointBucket.append(isolateJoint)
                        elif "[" in unicodeJointString:
                            isolateJoint=unicodeJointString.split("['")[1]
                            jointBucket.append(isolateJoint)
                        else:
                            jointBucket.append(unicodeJointString)
        cmds.select(getName[0])
        cmds.select(jointBucket[0], add=1)
        cmds.skinCluster()
        print jointBucket[0]
        for eachItem in jointBucket[2:]:
            print eachItem
            try:
                cmds.skinCluster(item, e=1, ai=eachItem)
                print eachItem+" is attached to "+item
            except:
                pass
#     def _open_influence_function(self):  
#         filename=cmds.textField(fileOpenName, q=1, text=True)   
#         getSelected=cmds.ls(sl=1, fl=1)[0]
#         guideDict={}
#         filename=cmds.optionMenu(fileName, q=1, v=1)
#         printFolder=folderPath+filename
#         inp=open(printFolder, 'r')
#         List = open(printFolder).readlines()
#         newlocbucket=[]
#         for each in List:
#             getDictParts=each.split('[')
#             for item in getDictParts[1:]:
#                 getPiece=item.split(',  ')
#                 for anotherItem in getPiece:
#                     teit=anotherItem.split("', u'")                                     
#                     for chng in teit:
#                         if "u'" in chng:
#                             getridofit=chng.split("u'")[1]
#                             newlocbucket.append(getridofit)
#                         if "]" in chng:
#                             getridofit=chng.split("']")[0]
#                             newlocbucket.append(getridofit)
#                         else:
#                             newlocbucket.append(chng)
# #             for eachInf in getInfParts:
# #                 if "u" in eachInf:
# #                     print eachInf
# #                     getridofit=eachInf.split("u")[1]
# #                     newlocbucket.append(getridofit)
# #                 if "]" in eachInf:
# #                     print eachInf
# #                     getridofit=eachInf.split("]")[0]
# #                     newlocbucket.append(getridofit)
# #                 else:
# #                     newlocbucket.append(eachInf)
#         cmds.skinCluster(getSelected, newlocbucket[0])
#         print newlocbucket[0]
#         for eachItem in newlocbucket[2:]:
#             print eachItem
#             try:
#                 cmds.skinCluster(getSelected, e=1, ai=eachItem)
#                 print eachItem+" is attached to "+getSelected
#             except:
#                 pass

inst = savingInfluences()
