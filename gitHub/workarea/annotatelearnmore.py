import maya.cmds as cmds
from functools import partial
from string import *
import maya.cmds as mc
import maya.mel
import os, subprocess, sys, platform, logging, signal, webbrowser, urllib, re, getpass, time, datetime, glob, random

from os  import popen
from sys import stdin
from random import randint
# from pymel.core import *
import pymel.core as pm
#import win32clipboard

import operator
from sys import argv
from datetime import datetime
from operator import itemgetter
from inspect import getsourcefile
from os.path import abspath

import baseMockFunctions_maya
reload (baseMockFunctions_maya)
# getBaseClass=baseMockFunctions_maya.BaseClass() 
# from mshotgun import mShotgun
import PyQt4
from PyQt4 import QtCore, QtGui, Qt
from PyQt4.QtGui import QWidget, QRadioButton, QGridLayout, QLabel, \
    QTableWidget, QComboBox, QKeySequence, QToolButton, QPlainTextEdit, QPushButton,QBoxLayout, \
    QClipboard, QTableWidgetItem, QCheckBox, QVBoxLayout, QHBoxLayout, \
    QPixmap, QLineEdit, QListWidget, QTextEdit, QSizePolicy, QFrame, QPalette, QColor, \
    QFont, QAbstractItemView, QMenu, QMessageBox
from PyQt4.QtCore import SIGNAL
import postDeformToolset as pdt
reload(pdt)
colorlist=[13, 6, 14, 17, 4, 8, 5, 7, 15, 5, 20, 24, 29, 31, 10, 16, 9, 30, 1, 2]

filepath=( '//sw/dev//deglaue//sandbox//rigModules//' ) 
if not filepath in sys.path: 
    sys.path.append(str(filepath)) 
import tools
reload (tools)
toolClass=tools.ToolFunctions()

import baseFunctions_maya
reload(baseFunctions_maya)
getBaseClass=baseFunctions_maya.BaseClass()
# filepath=( '//sw/dev//deglaue//sandbox//rigModules//' ) 
# if not filepath in sys.path: 
#     sys.path.append(str(filepath)) 
# import tools
# reload (tools)
# toolClass=tools.ToolFunctions()
# import baseFunctions_maya
# reload(baseFunctions_maya)
# getBaseClass=baseFunctions_maya.BaseClass() 

'''--------------------------Metal Golem(MG) rigging modules--------------------------'''

__author__ = "Elise Deglau"
__version__ = 1.00


'This work is licensed under a Creative Commons Attribution 4.0 International 4.0 (CC BY 4.0)'
'http://creativecommons.org/licenses/by/4.0/'


'''------------------------------------------------------------------------------'''



'''--------------------------Studio specific parameters--------------------------'''

getBaseClass=baseMockFunctions_maya.BaseClass() 
workSpace=cmds.workspace(q=1, lfw=1)[-1]
M_USER = os.getenv("USER")

spaceWork=workSpace


pathways={'open folder':spaceWork, "work":spaceWork, "project":projectFolder, "products":animFolder, "alembic":abcFolder, "blasts":rvFolder, "cache": cacheFolder}


proj_commonFolder='/dyn_att_presets/'





wk_strt_value = 0.0
wk_out_value = 0.0


'''------------------------------------------------------------------------------'''



class find_Path(QtGui.QWidget):
    def __init__(self):
        super(find_Path, self).__init__()
        self.initUI()

    def initUI(self):
        getPath='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/cache/nCloth/batch/'          
        getFiles=[os.path.join(getPath, o) for o in os.listdir(getPath) if os.path.isdir(os.path.join(getPath, o))]
        getFiles.sort(key=lambda x: os.path.getmtime(x))
        getFiles=[(each).split('/')[-1] for each in getFiles]
        # self._choser_group_window(getFiles)             
        self.setWindowTitle("path to caches")
        self.layout = QVBoxLayout()
        self.btnlayout = QBoxLayout(2)
        self.layout.addLayout(self.btnlayout)
        self.fieldText=QLineEdit(getPath)
        self.btnlayout.addWidget(self.fieldText)
        self.playlist = QComboBox()
        self.btnlayout.addWidget(self.playlist)
        self.playlist.addItems(getFiles)
        self.back_button = QPushButton("<<")
        self.set_button = QPushButton(">>")
        self.load_button = QPushButton("load cache")
        self.L_P_button = QPushButton("load and play")
        self.open_button = QPushButton("open folder")
        self.connect(self.set_button, SIGNAL('clicked()'), lambda *args:self.set_button_function(make_new_content = self.fieldText.text() ))
        self.connect(self.back_button, SIGNAL('clicked()'), lambda *args:self.back_button_function(make_new_content = self.fieldText.text() ))
        self.connect(self.load_button, SIGNAL('clicked()'), lambda *args:self.load_button_function(self.fieldText.text()))
        self.connect(self.L_P_button, SIGNAL('clicked()'), lambda *args:self.L_P_button_function(self.fieldText.text()))
        self.connect(self.open_button, SIGNAL('clicked()'), lambda *args:self.open_folder_button_function(self.fieldText.text()))
        self.btnlayout.addWidget(self.back_button)
        self.btnlayout.addWidget(self.set_button)
        self.btnlayout.addWidget(self.load_button)
        self.btnlayout.addWidget(self.L_P_button)
        self.btnlayout.addWidget(self.open_button)
        self.setLayout(self.layout)

    # def gotoAppend(self):
    #     self.close()

    def open_folder_button_function(self, content):
        access_main = mToolKit()
        content=str(content)
        access_main.opening_folder(content)

    def L_P_button_function(self, make_new_content):
        make_new_content = str(make_new_content)
        listed_extension = self.playlist
        listed_folder = listed_extension.currentText()    
        listed_folder= str(listed_folder)         
        access_main = mToolKit()
        access_main.load_and_play(make_new_content, listed_folder)

    def load_button_function(self, make_new_content):
        make_new_content = str(make_new_content)
        listed_extension = self.playlist
        listed_folder = listed_extension.currentText()    
        listed_folder= str(listed_folder)         
        access_main = mToolKit()
        access_main.load_cache(make_new_content, listed_folder)

    def set_button_function(self, make_new_content):
        make_new_content=str(make_new_content)
        listed_extension = self.playlist
        listed_folder = listed_extension.currentText()    
        listed_folder= str(listed_folder)      
        newgetpath = make_new_content+'/'+listed_folder
        self.fieldText.setText(newgetpath)     
        getFiles=[os.path.join(newgetpath, o) for o in os.listdir(newgetpath) if os.path.isdir(os.path.join(newgetpath, o)) and len(os.listdir(os.path.join(newgetpath, o)))>0]
        # getFiles=[os.path.join(newgetpath, o) for o in os.listdir(newgetpath) if os.path.isdir(os.path.join(newgetpath, o))]
        getFiles.sort(key=lambda x: os.path.getmtime(x))
        getFiles=[(each).split('/')[-1] for each in getFiles]        
        listed_extension.clear()
        listed_extension.addItems(getFiles)        

    def back_button_function(self, make_new_content):
        make_new_content=str(make_new_content)
        get_content_back = "/".join(make_new_content.split('/')[:-1])
        listed_extension = self.playlist
        listed_folder = listed_extension.currentText()    
        listed_folder= str(listed_folder)      
        self.fieldText.setText(get_content_back)     
        getFiles=[os.path.join(get_content_back, o) for o in os.listdir(get_content_back) if os.path.isdir(os.path.join(get_content_back, o))and len(os.listdir(os.path.join(get_content_back, o)))>0]
        getFiles.sort(key=lambda x: os.path.getmtime(x))
        getFiles=[(each).split('/')[-1] for each in getFiles]        
        self.playlist.clear()
        self.playlist.addItems(getFiles)   

class mToolKit(object):

    def set_troubleshoot(self, check_dict):
        if check_dict.get("range") == 1:        
            getNumStrt=cmds.playbackOptions(q=1, ast=1)
            getNumMn=cmds.playbackOptions(q=1, min=1)
            getNumMx=cmds.playbackOptions(q=1, max=1)
            getNumEnd=cmds.playbackOptions(q=1, aet=1)
            if getNumStrt <> wk_strt_value - 15:
                print "CHANGING>>>> "+str(getNumStrt)+" to "+str(wk_strt_value - 15)
                self.initialize_strt_based_on_wkrange()
            elif getNumMn <> wk_strt_value - 15:
                print "CHANGING>>>> "+str(getNumMn)+" to "+str(wk_strt_value - 15)
                self.initialize_strt_based_on_wkrange()        
            else:
                pass       
            if getNumEnd <> wk_out_value:
                print "CHANGING>>>> "+str(getNumEnd)+" to "+str(wk_out_value)
                cmds.playbackOptions(aet=wk_out_value)  
            elif getNumMx <> wk_out_value:
                print "CHANGING>>>> "+str(getNumMx)+" to "+str(wk_out_value)
                cmds.playbackOptions(max=wk_out_value)
            else:
                pass 
        else:
            print "Skipping range check"
        if check_dict.get("dyn_cnstrnt_exc") == 1: 
            for each in cmds.ls(type="dynamicConstraint"):
                print each, cmds.getAttr(each+".excludeCollisions")
                if cmds.getAttr(each+".excludeCollisions") != 1:        
                    cmds.setAttr(each+".excludeCollisions", 1)
                    print "CHANGED>>>> "+each, cmds.getAttr(each+".excludeCollisions")
                else:
                    print each+"excludeCollisions is already on - leaving as is"
        if check_dict.get("dyn_cnstrnt_cmp") == 1: 
            for each in cmds.ls(type='nCloth'):
                for item in  cmds.listConnections(each, s=1, type="nComponent"):
                    if cmds.getAttr(item+".componentType", asString=1) != "Point":
                        cmds.setAttr(item+".componentType",2)
                        print "CHANGED>>>> "+item+".componentType", cmds.getAttr(item+".componentType", asString=1)
                    else:
                        print item+" componentType check is healthy - leaving as is"               
            for each in cmds.ls(type='dynamicConstraint'):
                for item in  cmds.listConnections(each, s=1, type="nComponent"):
                    if cmds.getAttr(item+".componentType", asString=1) == "Point":
                        if cmds.getAttr(item+".elements", asString=1) != "From Indice List":
                            cmds.setAttr(item+".elements", 0)
                            print "CHANGED>>>> "+item+".elements", cmds.getAttr(item+".elements", asString=1)
                    else:
                        print item+" elements check is healthy - leaving as is"
        else:
            print "Skipping dynamic constraint collide exclusion check"
        for each in cmds.ls(type="nucleus"):
            if check_dict.get("nuc_spc_scl") == 1:     
                print each+".spaceScale", cmds.getAttr(each+".spaceScale")
                if cmds.getAttr(each+".spaceScale") ==1.0:
                    cmds.setAttr(each+".spaceScale", 0.1)
                    print "CHANGED>>>> "+each+".spaceScale", cmds.getAttr(each+".spaceScale")
                else:
                    print "spaceScale check is healthy - leaving as is"
            else:
                print "Skipping space scale check"     
            if check_dict.get("nuc_sub_stp") == 1:                          
                print each+".subSteps", cmds.getAttr(each+".subSteps")
                if cmds.getAttr(each+".subSteps") >3:
                    print "subSteps check is healthy - leaving as is"
                else:
                    cmds.setAttr(each+".subSteps", 30)
                    print "CHANGED>>>> "+each+".subSteps", cmds.getAttr(each+".subSteps")        
            else:
                print "Skipping substep check"
            if check_dict.get("nuc_col_itr") == 1:       
                print each+".maxCollisionIterations", cmds.getAttr(each+".maxCollisionIterations")
                if cmds.getAttr(each+".maxCollisionIterations") >4:
                    print "maxCollisionIterations check is healthy - leaving as is"
                else:
                    cmds.setAttr(each+".maxCollisionIterations", 20)
                    print "CHANGED>>>> "+each+".maxCollisionIterations", cmds.getAttr(each+".maxCollisionIterations")
            else:
                print "Skipping max collision iteration check"     
            if check_dict.get("nucstart") == 1:     
                print each+".startFrame", cmds.getAttr(each+".startFrame")
                print str(int(wk_strt_value) - 15)
                if cmds.getAttr(each+".startFrame") != wk_strt_value - 15:
                    cmds.setAttr(each+".startFrame", int(wk_strt_value - 15))
                    print "CHANGED>>>> "+each+".startFrame", cmds.getAttr(each+".startFrame")
                else:
                    print "startFrame check is healthy - leaving as is"
            else:
                print "Skipping nucleus start frame check"
            if check_dict.get("nucenable") == 1: 
                print each+".enable", cmds.getAttr(each+".enable")
                if cmds.getAttr(each+".enable")!=1:
                    cmds.setAttr(each+".enable", 1)
                    print "CHANGED>>>> "+each+".enable", cmds.getAttr(each+".enable")           
                else:
                    print "enabled check is good - leaving as is"
            else:
                print "Skipping enabled nucleus check"
        for each in cmds.ls(type="nRigid"):
            if check_dict.get("rgd_mass") == 1: 
                print each+".pointMass", cmds.getAttr(each+".pointMass")
                if cmds.getAttr(each+".pointMass")<20:
                    cmds.setAttr(each+".pointMass", 20)
                    print "CHANGED>>>> "+each+".pointMass", cmds.getAttr(each+".pointMass")                    
                else:
                    print "pointMass check is good - leaving as is"
            else:
                print "Skipping rigid point mass check"
        for each in cmds.ls(type="nCloth"):
            if check_dict.get("scl_rel") == 1: 
                print each+".scalingRelation", cmds.getAttr(each+".scalingRelation")
                if cmds.getAttr(each+".scalingRelation")==2:
                    cmds.setAttr(each+".scalingRelation", 1)
                    print "CHANGED>>>> "+each+".scalingRelation", cmds.getAttr(each+".scalingRelation")                  
                else:
                    print "scalingRelation check is good but check resolution. hires is good on 'object(1)' where as lores may be better on 'link(0)'"
            else:
                print "Skipping scale relation check"
            if check_dict.get("clth_trp_chk") == 1: 
                print each+".trappedCheck", cmds.getAttr(each+".trappedCheck")
                if each+".trappedCheck"==1:
                    cmds.setAttr(each+".trappedCheck", 0)
                    print "CHANGED>>>> "+each+".trappedCheck", cmds.getAttr(each+".trappedCheck")                        
                else:
                    print "trappedCheck check is good"
            else:
                print "Skipping cloth trap check"
            if check_dict.get("clthenable") == 1: 
                print each+".isDynamic", cmds.getAttr(each+".isDynamic")
                if each+".isDynamic"==1:
                    cmds.setAttr(each+".isDynamic", 0)
                    print "CHANGED>>>> "+each+".isDynamic", cmds.getAttr(each+".isDynamic")                        
                else:
                    print "isDynamic check is good"
            else:
                print "Skipping cloth enabled check"


    def nuc_pconstrnt_hip(self):
        cmds.pointConstraint(cmds.ls("*:*root_jnt")[0], cmds.ls(type="nucleus")[0], mo=0) 


    def nuc_pconstrnt_neck(self):
        cmds.pointConstraint(cmds.ls("*:*head*jnt")[0], cmds.ls(type="nucleus")[0], mo=0) 

    def troubleshoot_clth(self):
        getNumStrt=cmds.playbackOptions(q=1, ast=1)
        getNumEnd=cmds.playbackOptions(q=1, aet=1)
        if getNumStrt == wk_strt_value:
            print "SUGGESTED CHANGE>>>>>>> Maybe you want some preroll?"  
        else:
            pass        
        if getNumEnd == wk_out_value:
            "SUGGESTED CHANGE>>>>>>> Maybe you want to set the frame end to the work end range?"  
        else:
            pass               
        for each in cmds.ls("*:*.excludeCollisions"):
            if each != 1:
                print "SUGGESTED CHANGE>>>>>>> Maybe you want "+each+" on?"     
            else:
                print "exclusions passed"
        for each in cmds.ls(type='dynamicConstraint'):
            for item in  cmds.listConnections(each, s=1, type="nComponent"):
                if cmds.getAttr(item+".componentType", asString=1) != "Point":
                    print "SUGGESTED CHANGE>>>>>>>  "+item+".componentType 'POINTS' should be set on cloth items. Is currently set to: "+str(cmds.getAttr(item+".componentType", asString=1))
                else:
                    print item+" componentType check is healthy - leaving as is"   
        for each in cmds.ls(type='dynamicConstraint'):
            for item in  cmds.listConnections(each, s=1, type="nComponent"):
                if cmds.getAttr(item+".componentType", asString=1) == "Point":
                    if cmds.getAttr(item+".elements", asString=1) != "From Indice List":
                        print "SUGGESTED CHANGE>>>>>>>  "+item+".elements 'POINTS' - elements should be set to indices. Is currently set to: "+str(cmds.getAttr(item+".elements", asString=1))
                else:
                    print item+" elements check is healthy - leaving as is"                
        for each in cmds.ls(type="nucleus"):
            print each, cmds.getAttr(each+".spaceScale")
            if cmds.getAttr(each+".spaceScale") ==1.0:
                print "SUGGESTED CHANGE>>>>>>> Maybe you want "+each+" spaceScale lower?" 
            else:
                print "spaceScale check is healthy"
            print each, cmds.getAttr(each+".subSteps")
            if cmds.getAttr(each+".subSteps") >3:
                print "subSteps check is healthy"
            else:
                print "SUGGESTED CHANGE>>>>>>> Maybe you want "+each+" subSteps higher?"                 
            print each, cmds.getAttr(each+".maxCollisionIterations")
            if cmds.getAttr(each+".maxCollisionIterations") >4:
                print "maxCollisionIterations check is healthy"
            else:
                print "SUGGESTED CHANGE>>>>>>> Maybe you want "+each+" maxCollisionIterations higher?"            
            print each, cmds.getAttr(each+".startFrame")
            if cmds.getAttr(each+".startFrame") ==getNumStrt:
                print "startFrame is good"
            else:
                print "you might want to check this startFrame attribute"
            print each, cmds.getAttr(each+".enable")
            if cmds.getAttr(each+".enable")!=1:
                print "SUGGESTED CHANGE>>>>>>> Maybe you want "+each+" enabled?"            
            else:
                print "enabled check is good"
        for each in cmds.ls(type="nRigid"):
            print each+".pointMass", cmds.getAttr(each+".pointMass")
            if each+".pointMass"<20:
                print "you might want to check this pointMass attribute"                   
            else:
                print "pointMass check is good"
        for each in cmds.ls(type="nCloth"):
            print each+".scalingRelation", cmds.getAttr(each+".scalingRelation")
            if each+".scalingRelation"==2:
                print "you might want to check this scalingRelation attribute - setting to 'world(2)' is varying results"                   
            else:
                print "scalingRelation check is good but check resolution. hires is good on 'object(1)' where as lores may be better on 'link(0)'"
            print each+".trappedCheck", cmds.getAttr(each+".trappedCheck")
            if each+".trappedCheck"==1:
                print "you might want to check this trappedCheck attribute...off may have better results"                  
            else:
                print "trappedCheck check is good"

    def fix_cam(self):
        getSelectedStuff=cmds.ls(sl=1)
        print len(getSelectedStuff)
        if len(getSelectedStuff)==2:
                pass
        else:
                print "you need to select a camera and an object to frame to"
                return
        focusedThing=cmds.ls(sl=1, fl=1)[1]
        getOldCam=cmds.ls(sl=1, fl=1)[0]
        newcam=cmds.camera()
        cmds.select(newcam[0], r=1)
        cmds.select(getOldCam, add=1)
        getBaseClass.massTransfer()
        cmds.select(focusedThing, r=1)
        cmds.viewFit()
        cmds.delete(newcam[0])


    def grab_blend(self):
        findThisType="blendShape"
        getSel=cmds.ls(sl=1)
        if len(getSel)==0:
            getSel=cmds.ls(type=findThisType)  
            cmds.select(getSel, r=1)
            return    
        else:
            pass
        cmds.select(cl=1)
        collect=[]
        for each in getSel:
            getShape=cmds.listRelatives(each, ad=1, type="shape")
            if getShape != None:
                for item in getShape:
                    getNode=[(nodes) for nodes in cmds.listHistory(item) if cmds.nodeType(nodes) == findThisType]
                    # getNode=cmds.findType(item, type=findThisType)
                    if getNode != None:
                        print getNode
                        collect.append(getNode)
                        cmds.select(getNode, add=1)


    def selectNclothCache(self):
        findThisType=["cacheFile", "AlembicNode"]
        getSel=cmds.ls(sl=1)
        if len(getSel)==0:
            getSel=cmds.ls(type=findThisType)  
            cmds.select(getSel, r=1)
            return    
        else:
            pass
        cmds.select(cl=1)
        collect=[]
        for each in getSel:
            getShape=cmds.listRelatives(each, ad=1, type="shape")
            if getShape != None:
                for item in getShape:
                    for eachCacheNode in findThisType:
                        getNode=[(nodes) for nodes in cmds.listHistory(item) if cmds.nodeType(nodes) == eachCacheNode]
                        if getNode != None:
                            print getNode
                            collect.append(getNode)
                            cmds.select(getNode, add=1)

    def bsptools(self):
        filepath=( '//sw//dev//deglaue//tools//' )
        if not filepath in sys.path:
            sys.path.append(str(filepath))
        import BSPToolsUI
        reload (BSPToolsUI)
        BSPToolsUI.BSPUI() 
        blendShape_tools_UI()



    def selectNclothcloth(self):
        findThisType="nCloth"
        getSel=cmds.ls(sl=1)
        if len(getSel)==0:
            getSel=cmds.ls(type=findThisType)  
            cmds.select(getSel, r=1)
            return    
        else:
            pass
        cmds.select(cl=1)
        collect=[]
        for each in getSel:
            getShape=cmds.listRelatives(each, ad=1, type="shape")
            if getShape != None:
                for item in getShape:
                    getNode=[(nodes) for nodes in cmds.listHistory(item) if cmds.nodeType(nodes) == findThisType]
                    # getNode=cmds.listConnections(item, scn=1, et=1, sh=1, type=findThisType)
                    if getNode != None:
                        print getNode
                        collect.append(getNode)
                        cmds.select(getNode, add=1)


    def grab_nucleus(self):
        findThisType="nucleus"
        getSel=cmds.ls(sl=1)
        if len(getSel)==0:
            getSel=cmds.ls(type=findThisType)  
            cmds.select(getSel, r=1)
            return    
        else:
            pass       
        cmds.select(cl=1)
        collect=[]
        for each in getSel:
            getShape=cmds.listRelatives(each, ad=1, type="shape")
            if getShape != None:
                for item in getShape:
                    getNode=[(nodes) for nodes in cmds.listHistory(item) if cmds.nodeType(nodes) == findThisType]
                    # getNode=cmds.findType(item, type=findThisType)
                    if getNode != None:
                        print getNode
                        collect.append(getNode)
                        cmds.select(getNode, add=1)

    def grab_hairfxshape(self):
        findThisType="hrSimulatorShape"
        getSel=cmds.ls(sl=1)
        if len(getSel)==0:
            getSel=cmds.ls(type=findThisType)  
            cmds.select(getSel, r=1)
            return    
        else:
            pass
        cmds.select(cl=1)
        collect=[]
        for each in getSel:
            getShape=cmds.listRelatives(each, ad=1, type="shape")
            if getShape != None:
                for item in getShape:
                    getNode=[(nodes) for nodes in cmds.listHistory(item) if cmds.nodeType(nodes) == findThisType]
                    # getNode=cmds.findType(item, type=findThisType)
                    if getNode != None:
                        print getNode
                        collect.append(getNode)
                        cmds.select(getNode, add=1)

    def grab_hrproperty(self):
        findThisType="hrProperty"
        getSel=cmds.ls(sl=1)
        if len(getSel)==0:
            getSel=cmds.ls(type=findThisType)  
            cmds.select(getSel, r=1)
            return    
        else:
            pass
        cmds.select(cl=1)
        collect=[]
        for each in getSel:
            getShape=cmds.listRelatives(each, ad=1, type="shape")
            if getShape != None:
                for item in getShape:
                    getNode=[(nodes) for nodes in cmds.listHistory(item) if cmds.nodeType(nodes) == findThisType]
                    # getNode=cmds.findType(item, type=findThisType)
                    if getNode != None:
                        print getNode
                        collect.append(getNode)
                        cmds.select(getNode, add=1)

    

    

    

    


    def selectNclothMesh(self):
        typeN="mesh"
        getSel=cmds.ls(sl=1)
        if len(getSel)<1:
            getSel=[(item) for each in cmds.ls(type=typeN) for item in cmds.listRelatives(each, c=1, type="transform") if "Orig" not in str(each)]
        else:
            pass                 
        cmds.select(cl=1)
        collect=[]
        for each in getSel:
            getShape=cmds.listRelatives(each, ad=1, type="shape")
            if getShape != None:
                for item in getShape:
                    getNode=[(nodes) for nodes in cmds.listHistory(item) if cmds.nodeType(nodes) == typeN]
                    # getNode=cmds.listConnections(item, s=1, d=1, type=typeN)
                    if getNode != None:
                        print getNode
                        collect.append(getNode)
                        cmds.select(getNode, add=1)

    def streamSelector(self):
        getSel=cmds.ls(sl=1)
        if len(getSel)<1:
            print "select something"
            return
        else:
            pass
        cmds.select(cl=1)
        collect=[]
        for each in getSel:
            if cmds.nodeType(each) == "mesh":
                getShape=each
                pass
            elif cmds.nodeType(each) == "transform":
                getNode=[(nodes) for nodes in cmds.listHistory(each) if cmds.nodeType(nodes) == "shape"]
                # getShape=cmds.listRelatives(each, type="shape")
                pass
            else:
                print "need to select a transform mesh or shape"
                return
            for item in getShape:
                getNode=[(nodes) for nodes in cmds.listHistory(item) if cmds.nodeType(nodes) == nType]
                # getNode=cmds.findType(item, type=nType)
                if getNode != None:
                    print getNode
                    collect.append(getNode)
                    pass
                else:
                    print "no nucleus in scene found connected to this object"
                    return
        cmds.select(collect, r=1)


    def streamSelectorV1(self, typeN):
        getSel=cmds.ls(sl=1)
        cmds.select(cl=1)
        collect=[]
        for each in getSel:
            getShape=cmds.listRelatives(each, ad=1, type="shape")
            if getShape != None:
                for item in getShape:
                    getNode=cmds.listConnections(item, s=1, d=1, type=typeN)
                    if getNode != None:
                        collect.append(getNode)
                        cmds.select(getNode, add=1)                



    def initialize_strt_based_on_nucleus(self):
        getNode=cmds.ls(type="nucleus")
        getStartValue=cmds.getAttr(getNode[0]+".startFrame")
        getLowRange=cmds.playbackOptions(min=getStartValue)


    def initialize_strt_based_on_first(self):
        getLowRange=cmds.playbackOptions(q=1, min=1)
        print getLowRange
        getNode=cmds.ls(type="nucleus")
        for each in getNode:
            cmds.setAttr(each+".startFrame", getLowRange)

    def initialize_strt(self):
        '''COPY OF THE ABOVE : initialize_strt_based_on_nucleus - FOR LEGACY ONLY'''
        getNode=cmds.ls(type="nucleus")
        getStartValue=cmds.getAttr(getNode[0]+".startFrame")
        getLowRange=cmds.playbackOptions(min=getStartValue)


    def initialize_strt_based_on_wkrange(self):
        getNode=[(each) for each in cmds.ls(".startFrame") if cmds.nodeType(each) == "nucleus"]
        getNameNode=[(each) for each in cmds.ls("*:*.startFrame") if cmds.nodeType(each) == "nucleus"]
        for each in getNameNode:
            getNode.append(each)
        getPrerollRange=wk_strt_value-15
        print str(wk_strt_value)+" = old start range"
        getLowRange=cmds.playbackOptions(min=getPrerollRange, ast=getPrerollRange)
        print str(getPrerollRange)+" = new start cache range"
        postRollRange=wk_out_value+1
        print str(wk_out_value)+" = old end range"
        cmds.playbackOptions(max=postRollRange, aet=postRollRange)
        print str(postRollRange)+" = new end cache range"
        for each in getNode:
            try:
                cmds.setAttr(each, getLowRange)
                print "setting "+each+" to "+str(getLowRange)
            except:
                pass


    def reset_wraps(self):
        getit=cmds.ls(type="cape")
        cmds.select(getit)
        for each in getit:
            cmds.setAttr(each+".envelope", 0)
            cmds.setAttr(each+".envelope", 1)    
            cmds.setAttr(each+".interpolation", 1)      
            cmds.setAttr(each+".interpolation", 0)
        getit=cmds.ls(type="wrap")
        cmds.select(getit)
        for each in getit:
            cmds.setAttr(each+".envelope", 0)
            cmds.setAttr(each+".envelope", 1)    
            cmds.setAttr(each+".exclusiveBind", 0)
            cmds.setAttr(each+".exclusiveBind", 1)       


    def grabCameraLights(self):
        if cmds.objExists("*:camlight_loc"):
            print "cam lights already exist - won't import"
            pass
        else:
            try:
                getCameraGrp=cmds.ls("*:*.cameraPreset")
                getNode=str(pm.PyNode(getCameraGrp[0]).node())
                getCam=[each for each in cmds.listRelatives(getNode, ad=1) if cmds.nodeType(each) =="camera"]
                gettransformCam=[each for each in cmds.listRelatives(getCam[0], p=1) if cmds.nodeType(each) =="transform"][0]
                getLocCam=cmds.ls('cam_light_loc*:camlight_loc')[0]
                cmds.select(gettransformCam, r=1)
                cmds.select(getLocCam, add=1)
                print cmds.ls(sl=1)
                self._transfer_anim_attr()
            except:
                pass
            getcamlightPath='/jobs/'+PROJECT+'/COMMON/rig/template/cam_light_loc.mb'
            namer='cam_light_loc'
            cmds.file(getcamlightPath, i=1, type="mayaBinary", ignoreVersion=1, ra=True, mergeNamespacesOnClash=False, namespace=namer, options="v=0;", pr=1)
            # getLocCam=cmds.ls(sl=1)[0]
            print "imported cam lights"
        if cmds.objExists("o_techanim_playblast_shd"):
            FVfirst=cmds.ls("o_techanim_playblast_shd")[0]
            print "shader already exists. Won't create"
            print cmds.getAttr("o_techanim_playblast_shd.color")
            if cmds.getAttr("o_techanim_playblast_shd.color")==[(1.0, 1.0, 1.0)]:
                print "default grey blast"
                self.makeDefaultsetup(FVfirst)
            else:
                print "occ blast"
                self.makeOccsetup(FVfirst)
        else:               
            FVfirst = cmds.shadingNode('blinn', asShader=True, n="o_techanim_playblast_shd")
            self.makeOccsetup(FVfirst)

   
    def makeOccsetup(self, FVfirst):
        cmds.setAttr("hardwareRenderingGlobals.ssaoEnable", 1)
        cmds.setAttr("hardwareRenderingGlobals.ssaoAmount", 2.26)
        cmds.setAttr("hardwareRenderingGlobals.ssaoRadius", 1)
        cmds.setAttr("hardwareRenderingGlobals.ssaoFilterRadius", 4)
        cmds.setAttr("hardwareRenderingGlobals.ssaoSamples", 32)
        maya.mel.eval( "ActivateViewport20;" )
        maya.mel.eval( "DisplayLight;" )
        cmds.modelEditor( 'modelPanel4', e=1, twoSidedLighting=True) # Query for non-UI names for any render overrides
        cmds.modelEditor( 'modelPanel4', e=1, shadows=True) # Query for non-UI names for any render overrides
        # cmds.setAttr("piggo_o*:animGeo.res", 4)            
        '''---------------------------------
        assign shader
        ---------------------------------'''
        getType=["*:noTransform", "*:c_o_001_mid", "*:c_o_001_hi","*:c_o_001_xhi", "c_o_001_hi", "c_o_001_mid", "c_o_001_xhi"]
        collectItem=[(item) for each in getType for item in cmds.ls(each) ]  
        setName="sash" 
        # getSel=cmds.listRelatives(cmds.ls('postTech'), ad=1, type="mesh")        
        cmds.setAttr("o_techanim_playblast_shd.color", 1.0, 1.0, 1.0, type="double3")
        cmds.setAttr("o_techanim_playblast_shd.eccentricity", 0.453)
        cmds.setAttr("o_techanim_playblast_shd.specularRollOff", 0.222)
        cmds.setAttr("o_techanim_playblast_shd.specularColor", .470, .470, .470, type="double3")
        cmds.setAttr("o_techanim_playblast_shd.reflectivity", 0.0)
        if cmds.objExists(setName):
            pass
        else:
            cmds.sets(n=setName, co=3)
        for selected in collectItem:
            cmds.sets(selected, add=setName)
            cmds.select(selected)
            cmds.hyperShade(assign=str(FVfirst))
            cmds.select( cl=True )
        print "set for occlusion"

    def grabCameraLightsV1(self):
        getCameraGrp=cmds.ls("*:*.cameraPreset")
        getNode=str(pm.PyNode(getCameraGrp[0]).node())
        getCam=[each for each in cmds.listRelatives(getNode, ad=1) if cmds.nodeType(each) =="camera"]
        gettransformCam=[each for each in cmds.listRelatives(getCam[0], p=1) if cmds.nodeType(each) =="transform"][0]
        getcamlightPath='/jobs/'+PROJECT+'/COMMON/rig/template/cam_light_loc.mb'
        namer='cam_light_loc'
        # cmds.file(getcamlightPath, i=1, type="mayaAscii", ignoreVersion=1, ra=True, mergeNamespacesOnClash=False, namespace=namer, options="v=0;", pr=1)
        cmds.file(getcamlightPath, i=1, type="mayaBinary", ignoreVersion=1, ra=True, mergeNamespacesOnClash=False, namespace=namer, options="v=0;", pr=1)
        getLocCam=cmds.ls('cam_light_loc*:camlight_loc')[0]
        cmds.select(gettransformCam, r=1)
        cmds.select(getLocCam, add=1)
        self._transfer_anim_attr()
        cmds.setAttr("hardwareRenderingGlobals.ssaoEnable", 1)
        cmds.setAttr("hardwareRenderingGlobals.ssaoAmount", 2.26)
        cmds.setAttr("hardwareRenderingGlobals.ssaoRadius", 1)
        cmds.setAttr("hardwareRenderingGlobals.ssaoFilterRadius", 4)
        cmds.setAttr("hardwareRenderingGlobals.ssaoSamples", 32)
        maya.mel.eval( "ActivateViewport20;" )
        maya.mel.eval( "DisplayLight;" )
        cmds.modelEditor( 'modelPanel4', e=1, twoSidedLighting=True) # Query for non-UI names for any render overrides
        cmds.modelEditor( 'modelPanel4', e=1, shadows=True) # Query for non-UI names for any render overrides
        # cmds.setAttr("piggo_o*:animGeo.res", 4)            
        '''---------------------------------
        assign shader
        ---------------------------------'''
        getType=["*:noTransform", "*:c_o_001_mid", "*:c_o_001_hi","*:c_o_001_xhi", "c_o_001_hi", "c_o_001_mid", "c_o_001_xhi"]
        collectItem=[(item) for each in getType for item in cmds.ls(each) ]  
        setName="sash" 
        # getSel=cmds.listRelatives(cmds.ls('postTech'), ad=1, type="mesh")        
        FVfirst = cmds.shadingNode('blinn', asShader=True, n="o_techanim_playblast_shd")
        getFVfirst=[FVfirst]
        cmds.setAttr("o_techanim_playblast_shd.color", 1.0, 1.0, 1.0, type="double3")
        cmds.setAttr("o_techanim_playblast_shd.eccentricity", 0.453)
        cmds.setAttr("o_techanim_playblast_shd.specularRollOff", 0.222)
        cmds.setAttr("o_techanim_playblast_shd.specularColor", .470, .470, .470, type="double3")
        cmds.setAttr("o_techanim_playblast_shd.reflectivity", 0.0)
        if cmds.objExists(setName):
            pass
        else:
            cmds.sets(n=setName, co=3)
        for selected in collectItem:
            cmds.sets(selected, add=setName)
            cmds.select(selected)
            cmds.hyperShade(assign=str(FVfirst))
            cmds.select( cl=True )


    def _transfer_anim_attrV1(self, arg=None):
        '''This copies values and animcurve nodes of a first selection to all secondary selections'''
        getSel=cmds.ls(sl=1)
        getChildren=getSel[1:]
        getParent=getSel[:1]
        print "transfering values from: "+str(getParent)+" to "+str(getChildren)
        for each in getChildren:
            getFirstattr=cmds.listAttr (getParent[0], w=1, a=1, s=1, u=1, m=0)
            for item in getFirstattr:
                if "." not in item:
                    if "direction" not in item:
                        get=cmds.keyframe(getParent[0]+'.'+item, q=1, kc=1)
                        if get!=0:
                            try:
                                getSource=connectionInfo(getParent[0]+'.'+item, sfd=1)
                                newAnimSrce=duplicate(getSource)
                                lognm=newAnimSrce[0].replace(str(getParent[0]), str(each))
                                #===========================================================
                                # remove numbers at end
                                #===========================================================
                                newname=re.sub("\d+$", "", lognm)
                                cmds.rename(newAnimSrce, newname)
                                getChangeAttr=each+'.'+item                        
                                connectAttr(newname+'.output', getChangeAttr, f=1)                             
                                print "transferred animated attribute"
                            except:
                                pass
                        else:
                            try:
                                getValue=getattr(getParent[0],item).get()
                                getChangeAttr=getattr(each,item)
                                getChangeAttr.set(getValue)
                                print "transferred attribute set"
                            except:
                                pass


    def _transfer_anim_attr(self, arg=None):
        '''This copies values and animcurve nodes of a first selection to all secondary selections'''
        getSel=cmds.ls(sl=1)
        getChildren=getSel[1:]
        getParent=getSel[:1]
        for each in getChildren:
            getFirstattr=cmds.listAttr (getParent[0], w=1, a=1, s=1, u=1, m=0)
            for item in getFirstattr:
                if "." not in item:
                    if "direction" not in item:
                        get=cmds.keyframe(getParent[0]+'.'+item, q=1, kc=1)
                        if get!=0:
                            try:
                                getSource=connectionInfo(getParent[0]+'.'+item, sfd=1)
                                newAnimSrce=duplicate(getSource)
                                lognm=newAnimSrce[0].replace(str(getParent[0]), str(each))
                                newname=re.sub("\d+$", "", lognm)
                                cmds.rename(newAnimSrce, newname)
                                getChangeAttr=each+'.'+item                        
                                connectAttr(newname+'.output', getChangeAttr, f=1)                             
                            except:
                                pass
                        else:
                            try:
                                getValue=getattr(getParent[0],item).get()
                                getChangeAttr=getattr(each,item)
                                getChangeAttr.set(getValue)
                            except:
                                pass

    def saveSelection(self, arg=None):
        selObj=cmds.ls(sl=1, sn=1)
        getScenePath=cmds.file(q=1, location=1)
        getPathSplit=getScenePath.split("/")
        newfolderPath=re.sub(r'\\',r'/', folderPath)
        folderBucket=[]
        winName = "Save selected externally"
        winTitle = winName
        if cmds.window(winName, exists=True):
                deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=620, h=100 )
        cmds.menuBarLayout(h=30)
        stringField='''"Save selected" (launches window)a home made scripted save selection externally.
    Put full file path with preferred name of
    object in text field("/usr/people/<user>/joint4"). save button saves out file. Can add
    more to save from add selected at top. Will save out a file
    EG:"/usr/people/<user>/joint4.txt"

        * Step 1: select object or components
        * Step 2: pressing save will create .txt files that will contain the component names within the
            path indicated and name of file indicated in field

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
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=620)
        cmds.frameLayout('bottomFrame', label='', lv=0, nch=1, borderStyle='in', bv=1, p='selectArrayRow')      
        cmds.gridLayout('listBuildButtonLayout', p='bottomFrame', numberOfColumns=1, cellWidthHeight=(600, 20))         
        fieldBucket=[]
        objNameFile=str(newfolderPath)+str(selObj[0])
        cmds.rowLayout  (' listBuildButtonLayout ', w=600, numberOfColumns=6, cw6=[350, 40, 40, 40, 40, 1], ct6=[ 'both', 'both', 'both',  'both', 'both', 'both'], p='bottomFrame')
        self.getName=cmds.textField(h=25, p='listBuildButtonLayout', text=objNameFile)
        cmds.button (label='Save', w=90, p='listBuildButtonLayout', command = lambda *args:self._save_select(fileName=cmds.textField(self.getName, q=1, text=1)))            
        cmds.button (label='Open folder', w=60, p='listBuildButtonLayout', command = lambda *args:self._open_defined_path(destImagePath=cmds.textField(self.getName, q=1, text=1)))
        cmds.showWindow(window)

    def _open_defined_path(self, destImagePath):
        folderPath='\\'.join(destImagePath.split("/")[:-1])+"\\"        
        self.opening_folder(folderPath)

    def _save_select(self, fileName):   
        selObj=cmds.ls(sl=1, fl=1)        
        fileName=fileName+'_select.txt'
        print fileName
        inp=open(fileName, 'w+')
        for each in selObj:
            try:
                inp.write(str(each+","))
            except:
                pass
        inp.close()   
        print "saved as "+fileName

    def openSelection(self, arg=None):
        getScenePath=cmds.file(q=1, location=1)
        files, getPath, newfolderPath, filebucket=self.getWorkPath(getScenePath)    
        winName = "Open external selection"
        winTitle = winName
        openFolderPath=newfolderPath+"\\"   
        selObj=cmds.ls(sl=1, fl=1)
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=600, h=280 )
        cmds.menuBarLayout(h=30)
        stringField='''"Load selection" (launches window) Opens a selection. Put full path with no
    of object in the text field("/usr/people/<user>/").
    Press refresh and it will repopulate the drop down for available .txt files;
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
            opens the folder window for path indicated '''
        self.fileMenu = cmds.menu( label='Help', pmc=lambda *args:self.helpWin(stringField))         
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=600)
        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        cmds.rowLayout  (' rMainRow ', w=600, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=1, cellWidthHeight=(480, 20))
        cmds.button (label='refresh folder', p='listBuildButtonLayout', command = lambda *args:self.refresh_text())
        cmds.button (label='workpath', p='listBuildButtonLayout', command = lambda *args:self.refresh_work_text())      
        self.fileDropName=cmds.optionMenu( label='files')
        for each in filebucket:
            cmds.menuItem( label=each)
        self.pathFile=cmds.textField(h=25, p='listBuildButtonLayout', text=newfolderPath)
        cmds.button (label='Load', p='listBuildButtonLayout', command = lambda *args:self._load_selection(printFolder=cmds.textField(self.pathFile, q=1, text=1), grabFileName=cmds.optionMenu(self.fileDropName, q=1, v=1)))
        cmds.button (label='Open folder', p='listBuildButtonLayout', command = lambda *args:self._open_defined_path(destImagePath=cmds.textField(self.pathFile, q=1, text=1)))         
        cmds.showWindow(window)





    def _load_selection(self, printFolder, grabFileName):
        import ast
        notAttr=["isHierarchicalConnection", "solverDisplay", "isHierarchicalNode", "publishedNodeInfo", "fieldScale_Position", "fieldScale", "fieldScale.fieldScale_Position"]         
        printFolder=printFolder+grabFileName    
        if os.path.exists(printFolder):
            pass
        else:
            print printFolder+"does not exist"
            return
        getBucket=[]
        attribute_container=[]
        List = open(printFolder).readlines()
        for aline in List:
            if "," in aline:
                getObj=aline.split(',')
            else:
                getObj=aline
        for item in getObj:
            if item != "":
                getBucket.append(item)
        cmds.select(getBucket)                

    def saveConnection(self, arg=None):
        selObj=ls(sl=1, fl=1, sn=1)
        getScenePath=cmds.file(q=1, location=1)
        getPathSplit=getScenePath.split("/")
        folderPath='\\'.join(getPathSplit[:-1])+"\\"        
        if "Windows" in OSplatform:
            newfolderPath=re.sub(r'/',r'\\', folderPath)
        if "Linux" in OSplatform:
            newfolderPath=re.sub(r'\\',r'/', folderPath)
        folderBucket=[]
        winName = "Save connections"
        winTitle = winName
        if cmds.window(winName, exists=True):
                deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=620, h=100 )
        cmds.menuBarLayout(h=30)
        stringField='''"Save selected" (launches window)a home made scripted save selection externally.
    Put full file path with preferred name of
    object in text field("/usr/people/<user>/joint4"). save button saves out file. Can add
    more to save from add selected at top. Will save out a file
    EG:"/usr/people/<user>/joint4.txt"

        * Step 1: select object or components
        * Step 2: pressing save will create .txt files that will contain the component names within the
            path indicated and name of file indicated in field

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
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=620)
        cmds.frameLayout('bottomFrame', label='', lv=0, nch=1, borderStyle='in', bv=1, p='selectArrayRow')      
        cmds.gridLayout('listBuildButtonLayout', p='bottomFrame', numberOfColumns=1, cellWidthHeight=(600, 20))         
        fieldBucket=[]
        objNameFile=newfolderPath+str(selObj[0])
        cmds.rowLayout  (' listBuildButtonLayout ', w=600, numberOfColumns=6, cw6=[350, 40, 40, 40, 40, 1], ct6=[ 'both', 'both', 'both',  'both', 'both', 'both'], p='bottomFrame')
        self.getName=cmds.textField(h=25, p='listBuildButtonLayout', text=objNameFile)
        cmds.button (label='Save', w=90, p='listBuildButtonLayout', command = lambda *args:self._save_connection(fileName=cmds.textField(self.getName, q=1, text=1)))
        cmds.button (label='Open folder', w=60, p='listBuildButtonLayout', command = lambda *args:self._open_defined_path(destImagePath=cmds.textField(self.getName, q=1, text=1)))
        cmds.showWindow(window)

    def _save_connection(self, fileName):   
        selObj=cmds.ls(sl=1, fl=1)        
        fileName=fileName+'_connect.txt'
        if "Windows" in OSplatform:    
            # folderPath='/'.join(fileName.split('/')[:-1])+"/"
            # printFolder=re.sub(r'/',r'\\', folderPath)       
            if not os.path.exists(fileName): os.makedirs(fileName)
        if "Linux" in OSplatform:
            inp=open(fileName, 'w+')
        dirDict={}
        getStrtRange=cmds.playbackOptions(q=1, ast=1)#get framerange of scene to set keys in iteration
        getEndRange=cmds.playbackOptions(q=1, aet=1)#get framerange of scene to set keys in iteration
        sourceOutBucket=[]
        sourceInBucket=[]        
        for each in selObj:
            getOutPutConnection=cmds.listConnections(each, p=1, c=1, s=0, d=1)
            for eachController, eachChild in map(None, getOutPutConnection[::2], getOutPutConnection[1::2]):
                getPlug="MainOBJ."+eachController.split(".")[1]  
                getoutConnection=getPlug+">"+eachChild
                if "initialShadingGroup" not in eachChild or "dagSetMembers" not in eachChild:
                    sourceOutBucket.append(getoutConnection)
            getInputConnection=cmds.listConnections(each, p=1, c=1, s=1, d=0)
            for eachController, eachChild in map(None, getInputConnection[::2], getInputConnection[1::2]):
                getPlug="MainOBJ."+eachController.split(".")[1]  
                getinConnection=eachChild+">"+getPlug
                if "instObjGroups" not in getPlug:
                    sourceInBucket.append(getinConnection)
        inp.write("output$")
        for each in sourceOutBucket:
            inp.write(str(each)+",")
        inp.write("input$")         
        for each in sourceInBucket:           
            inp.write(str(each)+",")
        inp.close()   
        print "saved as "+fileName


    def openConnection(self, arg=None):
        getScenePath=cmds.file(q=1, location=1)
        files, getPath, newfolderPath, filebucket=self.getWorkPath(getScenePath)    
        winName = "Open external selection"
        winTitle = winName
        openFolderPath=folderPath+"\\"   
        selObj=cmds.ls(sl=1, fl=1)
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=600, h=280 )
        cmds.menuBarLayout(h=30)
        stringField='''"Load selection" (launches window) Opens a selection. Put full path with no
    of object in the text field("/usr/people/<user>/").
    Press refresh and it will repopulate the drop down for available .txt files;
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
            opens the folder window for path indicated '''
        self.fileMenu = cmds.menu( label='Help', pmc=lambda *args:self.helpWin(stringField))         
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=600)
        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        cmds.rowLayout  (' rMainRow ', w=600, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=1, cellWidthHeight=(480, 20))
        cmds.button (label='refresh folder', p='listBuildButtonLayout', command = lambda *args:self.refresh_text())
        cmds.button (label='workpath', p='listBuildButtonLayout', command = lambda *args:self.refresh_work_text())      
        self.fileDropName=cmds.optionMenu( label='files')
        for each in filebucket:
            cmds.menuItem( label=each)
        self.pathFile=cmds.textField(h=25, p='listBuildButtonLayout', text=newfolderPath)
        cmds.button (label='Load in', p='listBuildButtonLayout', command = lambda *args:self._load_connection_in(printFolder=cmds.textField(self.pathFile, q=1, text=1), grabFileName=cmds.optionMenu(self.fileDropName, q=1, v=1)))
        cmds.button (label='Load out', p='listBuildButtonLayout', command = lambda *args:self._load_connection_out(printFolder=cmds.textField(self.pathFile, q=1, text=1), grabFileName=cmds.optionMenu(self.fileDropName, q=1, v=1)))
        cmds.button (label='Load both', p='listBuildButtonLayout', command = lambda *args:self._load_connection_both(printFolder=cmds.textField(self.pathFile, q=1, text=1), grabFileName=cmds.optionMenu(self.fileDropName, q=1, v=1)))
        cmds.button (label='Open folder', p='listBuildButtonLayout', command = lambda *args:self._open_defined_path(destImagePath=cmds.textField(self.pathFile, q=1, text=1)))         
        cmds.showWindow(window)

    def makeFolder(self, folderType):
        if os.path.exists(folderType):
            pass
        else:
            os.makedirs(folderType)

    def _load_connection_both(self, printFolder, grabFileName):
        self._load_connection_in(printFolder, grabFileName)
        self._load_connection_out(printFolder, grabFileName)


    def _load_web_hair(self):
        url="https://atlas.bydeluxe.com/confluence/pages/viewpage.action?spaceKey=MRIG&title=Techanim+XGen+hair+walkthrough"
        subprocess.Popen('firefox "%s"' % url, stdout=subprocess.PIPE, shell=True) 
        
    def _load_connection_in(self, printFolder, grabFileName):
        import ast
        selObj=cmds.ls(sl=1, fl=1)
        printFolder=printFolder+grabFileName
        if os.path.exists(printFolder):
            pass
        else:
            print printFolder+"does not exist"
            return
        getBucket=[]
        attribute_container=[]
        List = open(printFolder).readlines()
        for aline in List:
            if "input$" in aline:
                getInput=aline.split("input$")[1]
        getObj=getInput.split(',')
        for item in getObj:
            if len(item)>0:
                getOutSourcePlug=item.split(">")[0]
                getSocket=item.split(">")[1]
                socket=getSocket.replace("MainOBJ", selObj[0])
                print "connecting: "+str(getOutSourcePlug)+">"+socket
                try:
                    cmds.connectAttr(getOutSourcePlug, socket, f=1)
                    print "connected: "+str(getOutSourcePlug)+">"+socket
                except:
                    print "can't connect: "+str(getOutSourcePlug)+">"+socket
                    pass


    def _load_connection_out(self, printFolder, grabFileName):
        selObj=cmds.ls(sl=1, fl=1)
        printFolder=printFolder+grabFileName
        if os.path.exists(printFolder):
            pass
        else:
            print printFolder+"does not exist"
            return
        getBucket=[]
        attribute_container=[]
        List = open(printFolder).readlines()
        for aline in List:
            if "output$" in aline:
                getOutput=aline.split("output$")[1]
                getInput=getOutput.split("input$")[0]
        getObj=getInput.split(',')
        for item in getObj:
            if len(item)>0:         
                getOutSourcePlug=item.split(">")[0]
                sourcePlug=getOutSourcePlug.replace("MainOBJ", selObj[0])
                getSocket=item.split(">")[1]
                print "connecting: "+str(sourcePlug)+">"+getSocket
                try:
                    cmds.connectAttr(sourcePlug, getSocket, f=1)
                    print "connected: "+str(sourcePlug)+">"+getSocket
                except:
                    print "can't connect: "+str(sourcePlug)+">"+getSocket
                    pass


    def blendSearchGroups(self):
        #only prefix
        selObj=cmds.ls(sl=1, fl=1)
        if selObj:
            pass
        else:
            print "must select a driver group and a driven group(same shortnames)"
            return
        parentObj=selObj[0]
        childrenObj=selObj[1]
        getparentObj=cmds.listRelatives(parentObj, ad=1, type="mesh")
        getchildObj=cmds.listRelatives(childrenObj, ad=1, type="mesh")
        for childItem  in getchildObj:
            for parentItem in getparentObj:
                if "Orig" not in str(childItem) and "Orig" not in str(parentItem):    
                    grabNameChild=str(pm.PyNode(childItem).nodeName())
                    grabNameParent=str(pm.PyNode(parentItem).nodeName())     
                    if ":" in grabNameChild:
                        grabNameChild=grabNameChild.split(":")[-1]
                    if ":" in grabNameParent:
                        grabNameParent=grabNameParent.split(":")[-1]
                    grabNameChild=grabNameChild.split("Shape")[0]    
                    grabNameParent=grabNameParent.split("Shape")[0]
                    if grabNameParent in grabNameChild:
                        print "blending: "+childItem+' to '+parentItem
                        try:
                            BlendShapeName=cmds.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", w=(0, 1.0))
                        except:
                            pass
                    elif grabNameChild in grabNameParent:
                        print "blending: "+childItem+' to '+parentItem
                        try:
                            BlendShapeName=cmds.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", w=(0, 1.0))
                        except:
                            pass
                    elif grabNameChild==grabNameParent:
                        print "blending: "+childItem+' to '+parentItem
                        try:
                            BlendShapeName=cmds.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", w=(0, 1.0))
                        except:
                            pass


    # def blendSearchGroups(self):
    #     #only prefix
    #     selObj=cmds.ls(sl=1, fl=1)
    #     if selObj:
    #         pass
    #     else:
    #         print "must select a driver group and a driven group(same shortnames)"
    #         return
    #     parentObj=selObj[0]
    #     childrenObj=selObj[1]
    #     getparentObj=cmds.listRelatives(parentObj, ad=1, type="mesh")
    #     getchildObj=cmds.listRelatives(childrenObj, ad=1, type="mesh")
    #     for childItem  in getchildObj:
    #         for parentItem in getparentObj:
    #             if "Orig" not in str(childItem) and "Orig" not in str(parentItem):    
    #                 grabNameChild=str(pm.PyNode(childItem).nodeName())
    #                 grabNameParent=str(pm.PyNode(parentItem).nodeName())     
    #                 if ":" in grabNameChild:
    #                     grabNameChild=grabNameChild.split(":")[-1]
    #                 if ":" in grabNameParent:
    #                     grabNameParent=grabNameParent.split(":")[-1]
    #                 grabNameChild=grabNameChild.split("Shape")[0]    
    #                 grabNameParent=grabNameParent.split("Shape")[0]
    #                 if grabNameParent in grabNameChild:
    #                 # if grabNameChild==grabNameParent:
    #                     print "blending: "+childItem+' to '+parentItem
    #                     try:
    #                         BlendShapeName=cmds.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", w=(0, 1.0))
    #                     except:
    #                         pass
    #                 elif grabNameChild in grabNameParent:
    #                 # if grabNameChild==grabNameParent:
    #                     print "blending: "+childItem+' to '+parentItem
    #                     try:
    #                         BlendShapeName=cmds.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", w=(0, 1.0))
    #                     except:
    #                         pass


    def testBlend(self):
        #only prefix
        selObj=cmds.ls(sl=1, fl=1)
        parentObj=selObj[0]
        childrenObj=selObj[1]
        getparentObj=cmds.listRelatives(parentObj, ad=1, type="mesh")
        getchildObj=cmds.listRelatives(childrenObj, ad=1, type="mesh")
        for childItem in getchildObj:
            grabNameChild=str(pm.PyNode(childItem).nodeName())
            grabNameChild=grabNameChild.split(":")[-1]
            grabNameChild=grabNameChild.split("Shape")[0]
            for parentItem in getparentObj:
                grabNameParent=str(pm.PyNode(parentItem).nodeName())
                grabNameParent=grabNameParent.split(":")[-1]
                grabNameParent=grabNameParent.split("Shape")[0]
            if grabNameChild==grabNameParent:
                print "blending: "+childItem+' to '+parentItem
                try:
                    BlendShapeName=cmds.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", w=(0, 1.0))
                except:
                    pass


    def connect_to_curve(self):
        selObj=cmds.ls(sl=1)
        microLeadCurve=[selObj[0]]
        CVbucketbuckList=[]
        childControllers=selObj[1:]
        for each in microLeadCurve:
            each=cmds.ls(each)[0]
            for eachCV, eachCtrlGro in map(None, pm.PyNode(each).cv, childControllers):
            # for eachCV, eachCtrlGro in map(None, each.cv, childControllers):
                CVbucketbuckList.append(eachCV)
        microLeadCurve=ls(microLeadCurve)[0]        
        for eachCtrlGro in childControllers:
            try:
                pgetCVpos=cmds.xform(eachCtrlGro, ws=1, q=1, t=1)
            except:
                pass
            getpoint=microLeadCurve.closestPoint(pgetCVpos, tolerance=0.001, space='preTransform')
            getParam=microLeadCurve.getParamAtPoint(getpoint, space='preTransform')
            select(eachCtrlGro, r=1)
            select(microLeadCurve, add=1)
            motionPath=cmds.pathAnimation(fractionMode=1, follow=1, followAxis="x", upAxis="y", worldUpType="vector", worldUpVector=[0, 1, 0], inverseUp=0, inverseFront=0, bank=0)        
            disconnectAttr(motionPath+"_uValue.output", motionPath+".uValue")
            getpth=str(motionPath)
            setAttr(motionPath+".fractionMode", False)
            setAttr(motionPath+".uValue", getParam)        

    def matchCurveShapes(self):
        self.CurveShapes()

    def matchFullShape(self):
        getFirstGrp, getSecondGrp=self.CurveShapes()
        self.matchCurveShapes_andShrinkWrap(getFirstGrp, getSecondGrp)


    def CurveShapes(self):
        getSel=cmds.ls(sl=1, fl=1)
        if getSel:
            pass
        else:
            print "need to select something"
            return
        getNames=cmds.ls(sl=1, fl=1)
        if ".e[" not in str(getNames[0]):
            print "selection needs to be continuous edges of two seperate polygon objects: first select one, then continuous edge and then the continuous edge on a seperate poly object that you want to deform it along"
            return
        else:
            pass
        getFirstGrp = getNames[0].split(".")[0]
        getSecondGrp = getNames[-1:][0].split(".")[0]
        if getFirstGrp == getSecondGrp:
            print "Only one poly object has been detected. Select one object and it's continuous edge and then select another object and select it's continuous edge for the first object to align to."
            return
        else:
            pass
        firstList=[(each) for each in getNames if each.split(".")[0]==getFirstGrp]
        secondList=[(each) for each in getNames if each.split(".")[0]==getSecondGrp]
        '''create childfirst curve'''
        cmds.select(firstList)
        cmds.CreateCurveFromPoly()
        getFirstCurve=cmds.ls(sl=1, fl=1)
        '''get cv total of curve'''
        getFirstCurveInfo=cmds.ls(sl=1, fl=1)
        numberCV=pm.PyNode(getFirstCurveInfo[0]).numCVs()
        cmds.delete(getFirstCurve[0], ch=1)
        '''wrap child mesh to curve'''
        cmds.select(cmds.ls(getFirstGrp)[0], r=1)
        cmds.wire(w=getFirstCurve[0], gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
        '''create parent curve'''
        cmds.select(secondList)
        cmds.CreateCurveFromPoly()
        getSecondCurve=cmds.ls(sl=1, fl=1)
        getSecondCurveInfo=cmds.ls(sl=1, fl=1)
        '''rebuilt curve to match first curve built'''
        cmds.rebuildCurve(getSecondCurve[0], getFirstCurve[0], rt=2 )
        getSecondCurve=cmds.ls(sl=1, fl=1)
        getSecondCurveInfo=cmds.ls(sl=1, fl=1)
        cmds.delete(getSecondCurve[0], ch=1)
        '''wrap parent curve to parent mesh'''
        cmds.select(getSecondCurve[0], r=1)
        cmds.select(cmds.ls(getSecondGrp)[0], add=1)
        cmds.CreateWrap()
        '''blend child curve to parent curve'''
        cmds.blendShape(getSecondCurve[0], getFirstCurve[0],w=(0, 1.0))
        return getFirstGrp, getSecondGrp


    def _apply_colors(self):
        getgrp = cmds.ls(sl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        for each in getgrp:
            name = each+"_shd"
            FVfirst = cmds.shadingNode('lambert', asShader=True, n=name)
            getFVfirst=[FVfirst]
            setName="techanim_textures" 
            if cmds.objExists(setName):
                pass
            else:
                cmds.sets(n=setName, co=3)
            cmds.sets(getFVfirst, add=setName)
            cmds.select(each)
            cmds.hyperShade(assign=str(FVfirst))
            cmds.setAttr(name+".color", random.uniform(0.0,1.0), random.uniform(0.0,1.0), random.uniform(0.0,1.0), type="double3")
        cmds.select(getgrp, r=1)        

    def get_geo_techanim(self):
        get_tech=cmds.ls("*:*_tech_geo")
        get_tech_two=cmds.ls("*_tech_geo")
        get_posttech=cmds.ls("*:*_postTech_geo")
        get_posttech_two=cmds.ls("*_postTech_geo")
        get_geo=get_tech+get_tech_two+get_posttech+get_posttech_two
        cmds.select(get_geo, r=1)
        self._apply_colors()

    def _change_colors(self):
        getgrp = cmds.ls(sl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        cmds.hyperShade (getgrp[0], smn=1)
        for each in cmds.ls(sl = 1):
            cmds.setAttr(each+".color", random.uniform(0.0,1.0), random.uniform(0.0,1.0), random.uniform(0.0,1.0), type="double3")
        cmds.select(getgrp, r=1)        


    def _change_ambient(self):
        getgrp = cmds.ls(sl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        cmds.hyperShade (getgrp[0], smn=1)
        for each in cmds.ls(sl = 1):
            get_float = random.uniform(0.0,1.0)
            cmds.setAttr(each+".incandescence", get_float, get_float, get_float, type="double3")
        cmds.select(getgrp, r=1)        


    def matchCurveShapes_andShrinkWrap(self, getFirstGrp, getSecondGrp):
        myDict={
                ".shapePreservationEnable":1,
                ".shapePreservationSteps":72,
                ".shapePreservationReprojection":1,
                ".shapePreservationIterations":1,
                ".shapePreservationMethod":0,
                ".envelope":1,
                ".targetSmoothLevel":1,
                ".continuity":1,
                ".keepBorder":0,
                ".boundaryRule":1,
                ".keepHardEdge":0,
                ".propagateEdgeHardness":0,
                ".keepMapBorders":1,
                ".projection":4,
                ".closestIfNoIntersection":0,
                ".closestIfNoIntersection":0 ,
                ".reverse":0,
                ".bidirectional":0,
                ".boundingBoxCenter":1,
                ".axisReference":0 ,
                ".alongX":1,
                ".alongY":1,
                ".alongZ":1,
                ".offset":0,
                ".targetInflation":0,
                ".falloff":0.3021390379,
                ".falloffIterations": 1
                }        
        cmds.delete(getFirstGrp, ch=1)
        getShrink=cmds.deformer(getFirstGrp, type="shrinkWrap")
        cmds.connectAttr(getSecondGrp+".worldMesh[0]", getShrink[0]+".targetGeom", f=1)
        for key, value in myDict.items():
            cmds.setAttr(getShrink[0]+key, value)
        # cmds.delete(getFirstGrp, ch=1)
        # cmds.select(getFirstGrp, r=1)
        # cmds.select(cmds.ls(getSecondGrp)[0], add=1)
        # cmds.CreateWrap()


    def cleaningFunctionCallup(self, winName):
        '''this deletes history, smooths and unlocks normals, removes user defined attributes, unused shapes and freezes out transformes'''
        objSel=cmds.ls(sl=1, fl=1)
        if len(objSel)>1:
            if "." in objSel[1]:
                objSel=cmds.ls(objSel[1].split(".")[0])
            else:
                objSel=objSel        
            print objSel
        # getparentObj=cmds.listRelatives(objSel, c=1)
        for each in objSel:
            getControllerListAttr=cmds.listAttr (each, ud=1)
            if getControllerListAttr:
                for eachAttr in getControllerListAttr:
                    try:
                        cmds.setAttr(each+"."+eachAttr, l=0)
                        print "unlocked "+each+"."+eachAttr 
                    except:
                        pass  
                    try:                      
                        cmds.deleteAttr(each+"."+eachAttr)
                        print "deleted "+each+"."+eachAttr                    
                    except:
                        pass
            try:
                cmds.makeIdentity(each, a=True, t=1, r=1, s=1, n=0)
                print "zeroed out transforms for "+each
            except:
                print "Object isn't a transform or has already had it's transform zeroed. Passing on zeroing out transforms"
            try:
                if ":" in each:
                    newName=each.split(":")[-1:]
                    cmds.rename(each, newName)
                    print "renamed "+str(each)+" to "+str(newName)  
            except:
                print "Object has clean name space"
                pass
            try:
                self.freeTheAttrs(each)                
            except:
                pass
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName) 

    def cleanModels(self, arg=None):       
        winName = "Clean object"
        winTitle = winName
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=500, h=100 )
        cmds.menuBarLayout(h=30)
        stringField='''"Clean model" (script)wipes history, resets transforms and averages normals on a
    model(modelling)

        "CLEAN+HISTORY" - button
            * Step 1: Select object
            * Step 2: pressing this button cleans history, zeros out object and
                cleans shape name, removes custom attr, averages normals(hard edges)
        "CLEAN" - button
            * Step 1: Select object
            * Step 2: pressing this button zeros out object and
                cleans shape name, removes custom attr, averages normals(hard edges)'''
        self.fileMenu = cmds.menu( label='Help', hm=1, pmc=lambda *args:toolClass.helpWin(stringField))           
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=500)
        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        cmds.rowLayout  (' rMainRow ', w=500, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(240, 20))
        cmds.button (label='clean+history', p='listBuildButtonLayout', command = lambda *args:getBaseClass.cleanObjHist(winName))
        cmds.button (label='clean', p='listBuildButtonLayout', command = lambda *args:getBaseClass.cleanObj(winName))  
        cmds.showWindow(window)

    def freeTheAttrs(self, each):
        getdef=[".sx", ".sy", ".sz", ".rx", ".ry", ".rz", ".tx", ".ty", ".tz", ".visibility"]
        for eachAttr in getdef:
            cmds.setAttr(each+eachAttr, lock=0)
            cmds.setAttr(each+eachAttr, cb=1)   
            cmds.setAttr(each+eachAttr, k=1) 
        print each+eachAttr+" is now visible in channel box"


    def pointGlue_mass_to_one(self):
        # maya.mel.eval( "catch(`loadPlugin '/sw/packages/internal.td/mrigplugins/1.1.6/maya/2016.5/linux_ub12_x86-64/plugins/build/pointGlue.so'`);")
        # maya.mel.eval( "pluginInfo -edit -autoload true '/sw/packages/internal.td/mrigplugins/1.1.6/maya/2016.5/linux_ub12_x86-64/plugins/build/pointGlue.so';")        
        blenderShape=cmds.ls(sl=1)[0]
        for each in cmds.ls(sl=1)[1:]:
            command='pointGlue -s "%s" -t "%s" -max 1' % (str(blenderShape), each)
            maya.mel.eval( command )

    def cape_callup(self):
        cmds.loadPlugin('cape', qt=1)
        cape.cape().create()

    def _fix_frames(self):
        getFile= cmds.file(q=1, sn=1).split('/')[-1]
        print getFile
        getFilename=getFile.split('.mb')[0]
        getDepts = os.listdir(rvFolder)
        for each in getDepts:
            if getFilename ==each:
                getFolderFiles=rvFolder+'/'+each
                moreFile=projectFolder+'/'+getFilename+'tmp'
                if not os.path.exists(moreFile):
                    os.makedirs(moreFile)               
                getpreset=[os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(getFolderFiles) for name in files if name.lower().endswith(".jpg")]
                for item in getpreset:
                    getpart=item.split(".")[-2]
                    try:
                        if int(getpart) < wk_strt_value:
                            getit=item.split("/")[-1]
                            print "moving "+getit+" to "+moreFile+'/'+getit
                            shutil.move(item, moreFile+'/'+getit)
                    except:
                        pass
                    try:
                        if int(getpart) > wk_out_value:
                            print "moving "+getit+" to "+moreFile+'/'+getit
                            shutil.move(item, moreFile+'/'+getit)
                    except:
                        pass

    def opening_folder(self, folderPath):
        # newfolderPath=re.sub(r'\\',r'/', folderPath)
        os.system('xdg-open "%s"' % folderPath)

    '''--------------------------Studio specific tools--------------------------'''

    def print_asset(self):
        getName=["abcmb", "shot"]
        import datetime
        getAll=[(each) for each in cmds.ls("*:*") if cmds.nodeType(each) == "transform"]
        collectAttr=[]
        for each in getAll:
            Attrs=[(attrItem) for attrItem in cmds.listAttr (each) for attrName in getName if attrName in attrItem]
            if len(Attrs)>0:        
                for item in Attrs:
                    newItem=each+"."+item
                    findShot=cmds.getAttr(newItem)
                    print findShot            
                    if '/' in str(findShot):
                        timeFormat=os.stat(findShot)   
                        print "finished publish at: "+datetime.datetime.fromtimestamp(timeFormat.st_mtime).strftime('%c')   

    def hookupo(self):
        subDept="anim"
        hiresTechAsset=SHOT+'_piggo_o1_'+DEPT+'_charPiggooModelHi.mb'
        hiresAnimAsset=SHOT+'_piggo_o1_'+subDept+'_charPiggooModelHi.mb'
        getTechPath='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/instances/piggo_o1/'+DEPT+'/highest/hi/abcmb/'+hiresTechAsset
        getAnimPath='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/instances/piggo_o1/'+subDept+'/highest/hi/abcmb/'+hiresAnimAsset
        if os.path.isfile(getTechPath):
            cmds.file(getTechPath, i=1, type="mayaBinary", ignoreVersion=1, ra=True, mergeNamespacesOnClash=False, namespace=hiresTechAsset, options="v=0;", pr=1)
            print "Loaded techanim hires alembic"
            aNewString=hiresTechAsset.replace( '.mb', '_mb')
            cmds.blendShape(aNewString+':c_o_001_hi', 'harness_truck1Tech:c_o_001_hi_preTech_geo', w=(0, 1.0))
        else:
            if os.path.isfile(getAnimPath):
                cmds.file(getAnimPath, i=1, type="mayaBinary", ignoreVersion=1, ra=True, mergeNamespacesOnClash=False, namespace=hiresAnimAsset, options="v=0;", pr=1)
                print "Could not find techanim hires alembic. Loading anim high alembic"
                self.animWarning()
                aNewString=hiresAnimAsset.replace( '.mb', '_mb')
                cmds.blendShape(aNewString+':c_o_001_hi', 'harness_truck1Tech:c_o_001_hi_preTech_geo', w=(0, 1.0))
        # cmds.select([aNewString+':char_piggo_o__model__hi', 'piggo_o1:char_piggo_o__model__hi'], r=1)
        # self.blendSearchGroups()
        # cmds.blendShape()
        defName="harness_blend"
        if cmds.objExists('piggo_o1:c_o_001_hi'):
            cmds.blendShape('harness_truck1Tech:c_o_001_hi_postTech_geo', 'piggo_o1:c_o_001_hi', n=defName, w=(0, 1.0))
        else:
            print "unable to access piggo_o1 - please check name"
        cmds.setAttr("piggo_o1:animGeo.res", 4)
        # cmds.select('*charPiggooModelHi:c_blackbox_001_grp_hi', r=1)             
        # cmds.select('*piggo_o1_techanim_charPiggooModel*:c_blackbox_001_grp_hi', r=1) 
        # cmds.select('piggo_o1:c_blackbox_001_grp_hi', add=1)
        # self.blendSearchGroups()
        # self.initialize_strt_based_on_wkrange()


    def hookupsash(self):
        subDept="anim"
        hiresTechAsset=SHOT+'_piggo_o1_'+DEPT+'_charPiggooModelMid.mb'
        hiresAnimAsset=SHOT+'_piggo_o1_'+subDept+'_charPiggooModelMid.mb'
        getTechPath='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/instances/piggo_o1/'+DEPT+'/highest/mid/abcmb/'+hiresTechAsset
        getAnimPath='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/instances/piggo_o1/'+subDept+'/highest/mid/abcmb/'+hiresAnimAsset
        if os.path.isfile(getTechPath):
            cmds.file(getTechPath, i=1, type="mayaBinary", ignoreVersion=1, ra=True, mergeNamespacesOnClash=False, namespace=hiresTechAsset, options="v=0;", pr=1)
            print "Loaded techanim hires alembic"
            aNewString=hiresTechAsset.replace( '.mb', '_mb')
            # cmds.blendShape(aNewString+':c_o_001_mid', 'o_sash1Tech:c_o_001_collider', w=(0, 1.0))
        else:
            if os.path.isfile(getAnimPath):
                cmds.file(getAnimPath, i=1, type="mayaBinary", ignoreVersion=1, ra=True, mergeNamespacesOnClash=False, namespace=hiresAnimAsset, options="v=0;", pr=1)
                print "Could not find techanim hires alembic. Loading anim high alembic"
                self.animWarning()
                aNewString=hiresAnimAsset.replace( '.mb', '_mb')
                cmds.blendShape(aNewString+':c_o_001_mid', 'o_sash1Tech:c_o_001_collider', w=(0, 1.0))
        # defName="sash_blend"
        # if cmds.objExists('piggo_o1:c_o_001_mid'):
            # cmds.blendShape('piggo_o1:c_o_001_mid', 'o_sash1Tech:c_o_001_mid', n=defName, w=(0, 1.0))
        # cmds.setAttr("piggo_o1:animGeo.res", 3)
        # self.initialize_strt_based_on_wkrange()

    def animWarning(self):
        result = cmds.confirmDialog ( 
            title='Clean object', 
            message="Warning: The anim cache loaded! This means a techanim abc is not available. Check your assets!", 
            button=['Continue','Cancel'],
            defaultButton='Continue', 
            cancelButton='Cancel', 
            dismissString='Cancel' )
        if result == 'Continue':
            print "anim collected"   
            pass
        else:
            pass

    def techWarning(self):
        result = cmds.confirmDialog ( 
            title='Clean object', 
            message="Tech hi v: " +"collected. this was created: ", 
            button=['Continue','Cancel'],
            defaultButton='Continue', 
            cancelButton='Cancel', 
            dismissString='Cancel' )
        if result == 'Continue':
            print "anim collected"   
            pass
        else:
            pass

    def hookupo_simple(self):
        getAlembic=cmds.ls(sl=1)[0]
        cmds.blendShape(getAlembic, 'harness_truck1Tech:c_o_001_hi_preTech_geo', w=(0, 1.0))
        defName="harness_blend"
        cmds.blendShape('harness_truck1Tech:c_o_001_hi_postTech_geo', 'piggo_o1:c_o_001_hi', n=defName, w=(0, 1.0))
        cmds.setAttr("piggo_o1:animGeo.res", 4)
        cmds.select('*charPiggooModelHi:c_blackbox_001_grp_hi', r=1) 
        cmds.select('piggo_o1:c_blackbox_001_grp_hi', add=1)
        self.blendSearchGroups()
        self.initialize_strt_based_on_wkrange()


    def fix_rainbow(self):
        for each in cmds.ls("*:*.displayColors"):
            cmds.setAttr(each, 0)            


    # def _choser_gen_group_window(self, getFiles, getPath):
    #     choose_gen_grp_win = "Pick from text files"
    #     if cmds.window(choose_gen_grp_win, exists=True):
    #         cmds.deleteUI(choose_gen_grp_win)
    #     chooser_gen_window = cmds.window(choose_gen_grp_win, title=choose_gen_grp_win, tbm=1, w=800, h=150)
    #     cmds.menuBarLayout(h=30)
    #     cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=800)
    #     cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
    #     cmds.rowLayout  (' rMainRow ', w=800, numberOfColumns=1, p='selectArrayRow')
    #     cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
    #     cmds.setParent ('selectArrayColumn')
    #     cmds.separator(h=10, p='selectArrayColumn')
    #     cmds.frameLayout('title1', bgc=[0.15, 0.15, 0.15], cll=1, label='Select version', lv=1, nch=1, borderStyle='out', bv=1, w=800, fn="tinyBoldLabelFont", p='selectArrayColumn')
    #     cmds.gridLayout('valuebuttonlayout', p='title1', numberOfColumns=2, cellWidthHeight=(800, 20))  
    #     self.attributepath=cmds.optionMenu( label='Find')
    #     for each in getFiles:
    #         cmds.menuItem( label=each)
    #     cmds.gridLayout('listBuildButtonLayout', p='title1', numberOfColumns=3, cellWidthHeight=(148, 20))
    #     cmds.button (label='Ok', p='listBuildButtonLayout', w=150, command = lambda *args:self.forceAtt(getPath, getPathfile=cmds.optionMenu(self.attributepath, q=1, v=1)))
    #     cmds.button (label='open folder', p='listBuildButtonLayout', w=150, command = lambda *args:self._open_defined_path(cmds.optionMenu(self.attributepath, q=1, v=1)))
    #     cmds.showWindow(chooser_gen_window) 

    # def openAttributesWindow(self, getPathCustom, optionPath):
    #     # getPath=proj_commonFolder
    #     # print optionPath
    #     if optionPath=="custom":   
    #         getPath=getPathCustom
    #     else:
    #         getPath=optionPath             
    #     getFiles=[os.path.join(getPath, o) for o in os.listdir(getPath) if os.path.isdir(os.path.join(getPath, o))]
    #     getFiles.sort(key=lambda x: os.path.getmtime(x))
    #     self._choser_group_window(getFiles)     



    def cache_find_window(self):
        inst_win = find_Path()
        inst_win.show()

    def load_cache(self, make_new_content, listed_folder):
        filepath = make_new_content+"/"+listed_folder
        filexml = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(filepath) for name in files if name.lower().endswith(".xml")][0]
        getSel=cmds.ls(sl=1)        
        if len(getSel)>0:
            for each in getSel:
                getShape=[(nodes) for nodes in cmds.listHistory(each) if cmds.nodeType(nodes) == "historySwitch"]
                #getShape=cmds.listRelatives(each, ad=1, type="historySwitch")
                if len(getShape)>0:
                    try:
                        maya.mel.eval('deleteCacheFile 2 { "keep", "" } ;')
                    except:
                        pass
                getCommand='createHistorySwitch("%s",false)' %each
                switch = maya.mel.eval(getCommand)
                cacheNode = cmds.cacheFile(f=filexml, ia='%s.inp[0]' % switch ,attachFile=True)
                cmds.setAttr( '%s.playFromCache' % switch, 1 )
        else:
            print "select something"
    def load_cacheV1(self, make_new_content, listed_folder):
        filepath = make_new_content+"/"+listed_folder
        createdict = [{os.path.join(dirpath, name): name} for dirpath, dirnames, files in os.walk(filepath) for name in files if name.lower().endswith(".xml")]
        filecloth = [(name) for dirpath, dirnames, files in os.walk(filepath) for name in files if name.lower().endswith(".nCloth")]
        # filexml, filename = [(os.path.join(dirpath, name), name) for dirpath, dirnames, files in os.walk(filepath) for name in files if name.lower().endswith(".xml")][0]
        # filename=[(each.split('/')[-1]) for each in filexml]
        print createdict
        print filecloth
        # if len(filexml)<2:
        #     filexml = [(filexml)]
        # else:
        #     filexml = filexml
        # if len(filename)<2:
        #     filename = [(filename)]
        # else:
        #     filename = filename
        # print filexml, filename            
        # createdict={}
        # for each, item in map(None, filexml, filename):
        #     # print ea             ch, item
        #     make_dict = {each:item}
        #     createdict.update(make_dict)
        # filename_only=[(each.split('.')[0]) for each in filename]
        # print filename_only         
        getSel=cmds.ls(sl=1)
        if len(getSel)>0:
            for selobj in getSel:
                for key, value in createdict.items():
                    getobjname=value[0].split('.')[0]
                    # print getobjname
                    if getobjname == str(selobj):
                        getShape=[(nodes) for nodes in cmds.listHistory(selobj) if cmds.nodeType(nodes) == "historySwitch"]
                        if len(getShape)>0:
                            maya.mel.eval('deleteCacheFile 2 { "keep", "" } ;')
                        getCommand='createHistorySwitch("%s",false)' %selobj
                        switch = maya.mel.eval(getCommand)
                        cacheNode = cmds.cacheFile(f=key, ia='%s.inp[0]' % switch ,attachFile=True)
                        cmds.setAttr( '%s.playFromCache' % switch, 1 )                
        else:
            for key, value in createdict.items():
                # print key, value
                # getobjname=value.split('.')[0]
                # print getobjname
                if filecloth in value:
                # filecloth = [(name.split('.')[0]) for dirpath, dirnames, files in os.walk(filepath) for name in files if name.lower().endswith(".nCloth") and if name.split('.')[0] in value][0]
                    getObj = cmds.ls(filecloth)[0]
                    getShape=[(nodes) for nodes in cmds.listHistory(getObj) if cmds.nodeType(nodes) == "historySwitch"]
                    if len(getShape)>0:
                        maya.mel.eval('deleteCacheFile 2 { "keep", "" } ;')
                    getCommand='createHistorySwitch("%s",false)' %getObj
                    switch = maya.mel.eval(getCommand)
                    cacheNode = cmds.cacheFile(f=filexml, ia='%s.inp[0]' % switch ,attachFile=True)
                    cmds.setAttr( '%s.playFromCache' % switch, 1 )
        # else:
        #     print "select something"                 
            
    def load_and_play(self, make_new_content, listed_folder):
        filepath = make_new_content+"/"+listed_folder
        filexml = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(filepath) for name in files if name.lower().endswith(".xml")][0]
        getSel=cmds.ls(sl=1)
        if len(getSel)>0:
            for each in getSel:
                getShape=[(nodes) for nodes in cmds.listHistory(each) if cmds.nodeType(nodes) == "historySwitch"]
                #getShape=cmds.listRelatives(each, ad=1, type="historySwitch")
                if len(getShape)>0:
                    maya.mel.eval('deleteCacheFile 2 { "keep", "" } ;')
                getCommand='createHistorySwitch("%s",false)' %each
                switch = maya.mel.eval(getCommand)
                cacheNode = cmds.cacheFile(f=filexml, ia='%s.inp[0]' % switch ,attachFile=True)
                cmds.setAttr( '%s.playFromCache' % switch, 1 )
            cmds.select(clear=1)
            filepath="_".join(filepath.split("."))
            filename=filepath.split('/')[-1]
            filepathname=filepath+'/'+filename
            print filepathname
            if not os.path.exists(filepath): os.makedirs(filepath)
            cmds.playblast(clearCache=1, endTime=cmds.playbackOptions(max=1, aet=1, q=1), filename=filepathname, format="image", offScreen=1, percent=100, quality=100, sequenceTime=0, showOrnaments=1, startTime=cmds.playbackOptions(min=1, ast=1, q=1), viewer=0, widthHeight=[2156, 1212])
            time.sleep(1.3)
            command = "rv "+ filepath
            subprocess.Popen(command, stdout = subprocess.PIPE, shell = True)
        else:
            print "select something"

    def break_connections(self):
        getAttrsToBreak=[".selectableJnt", ".selectableGeo", ".res", ".ctrlVis", ".jntVis", ".visibility"]
        selobj = cmds.ls(sl=1)
        if len(selobj)>0:
            mainRig = selobj[0]
        else:
            mainRig=[(each) for each in cmds.ls("*:*animGeo") if cmds.nodeType(each)=="transform" and cmds.listRelatives(each, p=1)==None and "piggo_o" in each][0]
        print mainRig
        for each in getAttrsToBreak:
            GetCtrlConnection=mainRig+each
            print GetCtrlConnection
            ToBreak=cmds.connectionInfo(GetCtrlConnection, sfd=1)
            print "breaking "+ToBreak+" to "+GetCtrlConnection
            try:
                cmds.disconnectAttr(ToBreak, GetCtrlConnection)
                print "broke "+ToBreak+" to "+GetCtrlConnection
            except:
                "Cannot break "+ToBreak+" to "+GetCtrlConnection
                pass
        for each in selobj:
            cmds.setAttr(each+".selectableGeo", 1)
            cmds.setAttr(each+".ctrlVis", 1)

    def dynnames(self):
        for each in cmds.ls(sl=1):
            if ":" in each:
                getParent=cmds.listRelatives(cmds.ls(sl=1)[0], p=1, type="transform")[0]    
                getConnecType='To'.join(reversed([(cmds.getAttr(item+".componentType", asString=1)) for item in  cmds.listConnections(cmds.ls(sl=1)[0], s=1, type="nComponent")]))+"_"
                cmds.select(cmds.ls(sl=1)[0], r=1)
                maya.mel.eval( 'dynamicConstraintMembership "select";' )
                getitems=[(item.split(".")[0]) for item in cmds.ls(sl=1)]
                getitems=[(item.split(":")[1]) for item in getitems]
                newlist=getConnecType+'_to_'.join(set(getitems))+'_dnc'
                cmds.rename(getParent, newlist)
            else:
                getParent=cmds.listRelatives(each, p=1, type="transform")[0]        
                getConnecType='To'.join(reversed([(cmds.getAttr(item+".componentType", asString=1)) for item in  cmds.listConnections(each, s=1, type="nComponent")]))+"_"
                cmds.select(each, r=1)
                maya.mel.eval( 'dynamicConstraintMembership "select";' )
                getitems=cmds.ls(sl=1)
                newlist=getConnecType+'_to_'.join(set([(each.split('.')[0]) for each in cmds.ls(sl=1)]))+'_dnc'
                cmds.rename(getParent, newlist)

    def rgdnames(self):
        for each in cmds.ls(sl=1):
            getSource=cmds.listConnections(each+".inputMesh", s=1)[0]
            getParent=cmds.listRelatives(each, p=1, type="transform")[0] 
            newlist = getSource.split(":")[1]+"_coll_nRigid_rgd"    
            cmds.rename(getParent, newlist)
    
        #cmds.nClothMakeCollide()
        

    

    


                           


    def annotate(self):
        getName = cmds.ls(sl=1)[0].split(":")[0]



    def annotations_list(self):
        getName=["namespace"]
        selObj = cmds.ls(sl=1)
        getIt=cmds.ls("*ANNOTATE_GRP*")
        if len(getIt)<1:
            getIt=cmds.CreateEmptyGroup()
            cmds.rename(getIt, "ANNOTATE_GRP")
            getIt=cmds.ls("*ANNOTATE_GRP*")
        else:
            getIt=cmds.ls("*ANNOTATE_GRP*")         
        for item in selObj:
            getparentObj=[(each.split("|")[1]) for each in cmds.listRelatives(item, f=1, ap=1)][0]
            Attrs=[(attrItem) for attrItem in cmds.listAttr (getparentObj) for attrName in getName if attrName in attrItem] 
            if len(Attrs)>0:        
                for attributeitem in Attrs:
                    newItem=getparentObj+"."+attributeitem
                    getTitle=cmds.getAttr(newItem)
            random.shuffle(colorlist, random.random)
            offset = colorlist[0]
            cmds.select(item, r=1)
            toolClass.point_const()
            selected = cmds.ls(sl=1)
            if len(selected)>1:
                selected = selected[-1]
            else:
                selected = selected[0]
            cmds.parent(selected, getIt)
            transformWorldMatrix=cmds.xform(selected, q=True, ws=1, t=True)
            newTransform = [transformWorldMatrix[0], transformWorldMatrix[1]+offset, transformWorldMatrix[2]]
            getAnnot = mc.annotate(selected, p=newTransform)
            buildParent = cmds.group(n=getTitle+"_grp")
            cmds.CenterPivot()
            cmds.setAttr(getAnnot+".text", getTitle, type="string")
            cmds.setAttr(getAnnot+".overrideEnabled", 1)
            cmds.setAttr(getAnnot+".overrideColor", offset)
            getparent = cmds.listRelatives(getAnnot, p=1)[0]
            cmds.pointConstraint(selected, buildParent, mo=1)
            cmds.rename(getparent, getTitle+"_ant")
            cmds.rename(selected, item)
            cmds.parent(buildParent, getIt)
            


    def dealers_choice(self):
        collectedVtx=[]
        if len(cmds.ls(sl=1))<1:
            rigs = [(each) for each in cmds.ls("*:*") if cmds.nodeType(each) == "transform" and cmds.listRelatives(each, p=1) == None]
            for item in rigs:
                getparentObj=[(each) for each in cmds.listRelatives(item, ad=1, type="mesh")][0]
                getvert=getparentObj+".vtx[0]"
                collectedVtx.append(getvert)
            cmds.select(collectedVtx, r=1)
            self.annotations_list()              
        elif cmds.nodeType(cmds.ls(sl=1)[0]) == "transform":
            rigs = cmds.ls(sl=1)
            for item in rigs:
                getparentObj=[(each) for each in cmds.listRelatives(item, ad=1, type="mesh")][0]
                getvert=getparentObj+".vtx[0]"
                collectedVtx.append(getvert)
            cmds.select(collectedVtx, r=1)
            self.annotations_list()            
        elif cmds.nodeType(cmds.ls(sl=1)[0]) == "mesh":
            self.annotations_list()

    def _change_anot_colors(self):
        getgrp = cmds.ls(type="annotationShape")
        if len(getgrp)>0:
            pass
        else:
            print "annotations not present in scene"
            return
        for each in getgrp:
            random.shuffle(colorlist, random.random)
            offset = colorlist[0]
            cmds.setAttr(each+".overrideEnabled", 1)
            cmds.setAttr(each+".overrideColor", offset)


