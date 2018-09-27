import maya.cmds as cmds
from functools import partial
from string import *
import maya.cmds as mc
import maya.mel
import os, subprocess, sys, platform, logging, signal, webbrowser, urllib, re, getpass, time, glob, shutil, re
from os  import popen
from sys import stdin
import random
import glob
 
import tech_utils
reload(tech_utils)
# import __main__ as m
# import pointGlue
import getpass
import pymel.core as pm
import inspect
from maya_groom_tools.hair_tools.xgen_tools.xg_fx import xg_animWire;reload(xg_animWire)
 
 
from random import shuffle
 
import promoteToTechUI
from random import randint
import pymel.core as pm
import operator
from sys import argv
import time
import datetime
from datetime import datetime
from operator import itemgetter
from inspect import getsourcefile
from os.path import abspath
import cape
import baseMockFunctions_maya
reload (baseMockFunctions_maya)
# getBaseClass=baseMockFunctions_maya.BaseClass()
import mWeights
 
# from mshotgun import mShotgun
import mrig_pyqt
from mrig_pyqt import QtCore, QtGui
from mrig_pyqt.QtGui import QWidget, QRadioButton, QGridLayout, QLabel, \
    QTableWidget, QComboBox, QKeySequence, QToolButton, QPlainTextEdit, QPushButton,QBoxLayout, \
    QClipboard, QTableWidgetItem, QCheckBox, QVBoxLayout, QHBoxLayout, \
    QPixmap, QLineEdit, QListWidget, QTextEdit, QSizePolicy, QFrame, QPalette, QColor, \
    QFont, QAbstractItemView, QMenu, QMessageBox
from mrig_pyqt.QtCore import SIGNAL
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
 
 
import ast
import tech_utils as tu
reload(tu)
# filepath=( '//home/deglaue/lotus/notes/data/workspace/sandbox/rigModules/' )
# if not filepath in sys.path:
#     sys.path.append(str(filepath))
# import baseFunctions_maya
# reload(baseFunctions_maya)
# getBaseClass=baseFunctions_maya.BaseClass()
# filepath=( '//sw/dev//deglaue//sandbox//rigModules//' )
# if not filepath in sys.path:
#     sys.path.append(str(filepath))
# import tools
# reload (tools)
# toolClass=tools.ToolFunctions()
# import baseFunctions_maya
# reload(baseFunctions_maya)
# getBaseClass=baseFunctions_maya.BaseClass()
import tech_hairUtils
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
PROJECT=os.getenv("M_JOB")
SCENE=os.getenv("SEQUENCE_SHOT_")
SHOT=os.getenv("M_LEVEL")
DEPT=os.getenv("M_TASK")
spaceWork=workSpace
projectFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/scenes/'
animFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/instances/'
abcFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/cache/alembic/'
pbFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/movies/'
rvFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/'+DEPT
cacheFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/cache/'
getcamlightPath='/jobs/'+PROJECT+'/COMMON/'+'/rigs/users/'+M_USER+'/cam_light_loc.mb'
pathways={'open folder':spaceWork, "work":spaceWork, "project":projectFolder, "products":animFolder, "alembic":abcFolder, "blasts":rvFolder, "cache": cacheFolder}
 
 
proj_commonFolder='/jobs/'+PROJECT+'/COMMON/rig/users/deglaue/dyn_att_presets/'
 
 
 
sgVarFilePath = '/jobs/%s/%s/%s/TECH/lib/shotgun/setshot.d/sgvars' % (PROJECT, SCENE, SHOT)
if os.path.isfile(sgVarFilePath):
    # get available in/out values
    franges = {'WORK_IN': None, 'CUT_IN': None,
               'WORK_OUT': None, 'CUT_OUT': None}
    for line in open(sgVarFilePath, 'r'):
        if "CUT_DURATION" in line:
            shot_len_value = line.split('=')[-1].strip()
            try:
                shot_len_value = int(shot_len_value)
            except:
                shot_len_value = 0.0
        if 'CUT_IN' in line:
            cut_in_value = line.split('=')[-1].strip()
            try:
                cut_in_value = int(cut_in_value)
            except:
                cut_in_value = 0.0
        if 'CUT_OUT' in line:
            cut_out_value = line.split('=')[-1].strip()
            try:
                cut_out_value = int(cut_out_value)
            except:
                cut_out_value = 0.0
        if 'WORK_IN' in line:
            wk_strt_value = line.split('=')[-1].strip()
            try:
                wk_strt_value = int(wk_strt_value)
            except:
                wk_strt_value = 0.0
        if 'WORK_OUT' in line:
            wk_out_value = line.split('=')[-1].strip()
            try:
                wk_out_value = int(wk_out_value)
            except:
                wk_out_value = 0.0
        if 'CUT_IN' in line:
            cut_shouldbe_in_value = line.split('=')[-1].strip()
            try:
                cut_shouldbe_in_value = int(cut_shouldbe_in_value)-8
            except:
                cut_shouldbe_in_value = 0.0
        if 'CUT_OUT' in line:
            cut_shouldbe_out_value = line.split('=')[-1].strip()
            try:
                cut_shouldbe_out_value = int(cut_shouldbe_out_value)+8
            except:
                cut_shouldbe_out_value = 0.0
 
else:
    wk_strt_value = 0.0
    wk_out_value = 0.0
 
 
'''------------------------------------------------------------------------------'''
 
 
class strand_Behaviour_Win(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setWindowTitle("dynamic strands")
        self.layout = QVBoxLayout()
        self.btnlayout = QBoxLayout(1)
        self.layout.addLayout(self.btnlayout)
        self.sttc_strnd = QPushButton("Static strand")
        self.connect(self.sttc_strnd, SIGNAL("clicked()"),
                    lambda: self.static_curves())
        self.btnlayout.addWidget(self.sttc_strnd)
        self.dyn_strnd = QPushButton("Dynamic strand")
        self.connect(self.dyn_strnd, SIGNAL("clicked()"),
                    lambda: self.dynamic_curves())       
        self.btnlayout.addWidget(self.dyn_strnd)
        self.setLayout(self.layout)
        self.show()
 
    def static_curves(self):
        tech_hairUtils.mkPostTechCurvesStatic()
 
    def dynamic_curves(self):
        for each in mc.ls(sl=1):
            hairSys = mc.listRelatives(mc.getAttr(each+".hairSystem"), p=1, type="transform")[0]
            tech_hairUtils.mkPostTechCurvesDynamicAgain(postTechCurves=each,  hairSystem=hairSys)
            print "attempting to added "+each+" to "+hairSys
 
class find_Path(QtGui.QWidget):
    def __init__(self):
        super(find_Path, self).__init__()
        self.initUI()
 
    def initUI(self):
        # getPath='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/cache/nCloth/batch/'   
        getPath='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/cache/'   
        if os.path.exists(getPath):
            pass    
        else:
            print "no caches exist"
            return
        getFiles=[os.path.join(getPath, o) for o in os.listdir(getPath) if os.path.isdir(os.path.join(getPath, o))]
        getFiles.sort(key=lambda x: os.path.getmtime(x))
        getFiles=[(each).split('/')[-1] for each in getFiles]
        # self._choser_group_window(getFiles)            
        self.setWindowTitle("path to caches")
        self.layout = QVBoxLayout()
        self.btnlayout = QVBoxLayout()
        self.layout.addLayout(self.btnlayout)
        self.fieldText=QLineEdit(getPath)
        self.btnlayout.addWidget(self.fieldText)
        self.playlist = QComboBox()
        self.btnlayout.addWidget(self.playlist)
        self.playlist.addItems(getFiles)
        self.back_button = QPushButton("<<")
        self.set_button = QPushButton(">>")
        self.load_button = QPushButton("load cache")
        self.load_hair_button = QPushButton("load hair cache")
        self.load_cloth_button = QPushButton("load cloth cache")
        self.L_P_button = QPushButton("load and play")
        self.open_button = QPushButton("open folder")
        self.connect(self.set_button, SIGNAL('clicked()'), lambda *args:self.set_button_function(make_new_content = self.fieldText.text() ))
        self.connect(self.back_button, SIGNAL('clicked()'), lambda *args:self.back_button_function(make_new_content = self.fieldText.text() ))
        self.connect(self.load_button, SIGNAL('clicked()'), lambda *args:self.load_button_function(self.fieldText.text()))
        self.connect(self.load_hair_button, SIGNAL('clicked()'), lambda *args:self.load_hair_function(self.fieldText.text()))
        self.connect(self.load_cloth_button, SIGNAL('clicked()'), lambda *args:self.load_cloth_function(self.fieldText.text()))
        self.connect(self.L_P_button, SIGNAL('clicked()'), lambda *args:self.L_P_button_function(self.fieldText.text()))
        self.connect(self.open_button, SIGNAL('clicked()'), lambda *args:self.open_folder_button_function(self.fieldText.text()))
        self.btnlayout.addWidget(self.back_button)
        self.btnlayout.addWidget(self.set_button)
        self.btnlayout.addWidget(self.load_button)
        self.btnlayout.addWidget(self.load_hair_button)
        self.btnlayout.addWidget(self.load_cloth_button)
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
        listed_folder = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(listed_folder) for name in files if name.lower().endswith(".xml")]        
        access_main = mToolKit()
        access_main.load_and_play(make_new_content, listed_folder)
 
    def load_button_function(self, make_new_content):
        make_new_content = str(make_new_content)
        print make_new_content
        # listed_extension = self.playlist
        # listed_folder = listed_extension.currentText()   
        # listed_folder= str(listed_folder)        
        # print listed_folder
        # xmlfiles = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(listed_folder+'/') for name in files if name.lower().endswith(".xml")]  
        # get_folder_for_jpgs = [(each_file) for each_file in os.walk(get_selected_path) if "xml" in str(each_file)]    
        # print get_folder_for_jpgs  
        # print xmlfiles     
        access_main = mToolKit()
        access_main.load_cache(make_new_content)
 
    def load_hair_function(self, make_new_content):
        make_new_content = str(make_new_content)
        listed_extension = self.playlist
        listed_folder = listed_extension.currentText()   
        access_main = mToolKit()
        access_main.load_hair_cache(make_new_content, listed_folder)
 
    def load_cloth_function(self, make_new_content):
        make_new_content = str(make_new_content)
        listed_extension = self.playlist
        listed_folder = listed_extension.currentText()   
        access_main = mToolKit()
        access_main.load_cloth_cache(make_new_content, listed_folder)
 
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
        print check_dict.get("dyn_cnstrnt_exc")
        if check_dict.get("dyn_cnstrnt_exc") == 1:
            for each in cmds.ls(type="dynamicConstraint"):
                print each, cmds.getAttr(each+".excludeCollisions")
                if cmds.getAttr(each+".excludeCollisions") == 0:       
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
        if cmds.ls(sl=1) >0:
           for each in cmds.ls(sl=1):
                cmds.pointConstraint(cmds.ls("*:*root_jnt")[0], each, mo=0) 
        else:
            cmds.pointConstraint(cmds.ls("*:*root_jnt")[0], cmds.ls(type="nucleus")[0], mo=0)
 
 
    def nuc_pconstrnt_neck(self):
        if cmds.ls(sl=1) >0:
           for each in cmds.ls(sl=1):
                cmds.pointConstraint(cmds.ls("*:*head*jnt")[0], each, mo=0)        
        else:
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
 
    def fix_camV1(self):
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
    # def selectNclothMesh(self):
        typeN="nCloth"
        getSel=cmds.ls(sl=1)
        if len(getSel)<1:
            getSel=cmds.ls(type=typeN) 
            cmds.select(getSel, r=1)
            return
        else:
            getNode=[(item) for each in cmds.ls(sl=1) for item in cmds.listHistory(each, f=1) if cmds.nodeType(item) == typeN]
        if getNode != None:
            cmds.select(getNode, r=1)
 
        # findThisType="nCloth"
        # getSel=cmds.ls(sl=1)
        # if len(getSel)==0:
        #     getSel=cmds.ls(type=findThisType) 
        #     cmds.select(getSel, r=1)
        #     return   
        # else:
        #     pass
        # cmds.select(cl=1)
        # collect=[]
        # for each in getSel:
        #     getShape=cmds.listRelatives(each, ad=1, type="shape")
        #     if getShape != None:
        #         for item in getShape:
        #             getNode=[(nodes) for nodes in cmds.listHistory(item) if cmds.nodeType(nodes) == findThisType]
        #             # getNode=cmds.listConnections(item, scn=1, et=1, sh=1, type=findThisType)
        #             if getNode != None:
        #                 print getNode
        #                 collect.append(getNode)
        #                 cmds.select(getNode, add=1)
 
    def selectNhair(self):
        findThisType="hairSystem"
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
            getShape=cmds.listRelatives(each, ad=1, type="nurbsCurve")
            if getShape != None:
                for item in getShape:
                    getNode=[(nodes) for nodes in cmds.listHistory(item) if cmds.nodeType(nodes) == findThisType]
                    # getNode=cmds.listConnections(item, scn=1, et=1, sh=1, type=findThisType)
                    if getNode != None:
                        print getNode
                        collect.append(getNode)
                        cmds.select(getNode, add=1)
                         
    def selectNconstraint(self):
        findThisType="dynamicConstraint"
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
            getShape=cmds.listRelatives(each, ad=1, type="nurbsCurve")
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
 
    # def first_loading_xgen(self):
 
    # def saving_xgen(self):
 
    # def publish_xgen(self):
 
    def fix_hairfx_xgen_methpipe_scene(self):
        getSel=cmds.ls(type="xgmPalette")
        cmds.select(getSel, r=1)
        grabbed_the_thing=cmds.ls(sl=1)
        if len(grabbed_the_thing)>0:
            try:
                cmds.parent(w=1)
            except:
                print "groom already child of world"
                pass
        else:
            print "try again, I might have missed a node"
        print "setting your frames so as to not corrupt this file on save - do this often"
        self.initialize_strt_based_on_wkrange()
        getLowRange=cmds.playbackOptions(min=1, ast=1, q=1)
        getSel=cmds.ls(type="hrSimulatorShape")
        cmds.select(getSel, r=1)
        grabbed_the_thing=cmds.ls(sl=1)
        if len(grabbed_the_thing)>0:
            for each in grabbed_the_thing:
                cmds.setAttr(each+".startTime", getLowRange)
                cmds.currentTime(getLowRange)
        # self.reinit_hairfx()
        typeN="mesh"
        getSel=cmds.ls(type="xgmSubdPatch")[0]
        getNode=[(nodes) for nodes in cmds.listHistory(getSel) if cmds.nodeType(nodes) == typeN]
        print "makin pretty: hiding build mesh from preview"
        for each in getNode:
            cmds.setAttr(each+".visibility", 0)
 
    def reinit_hairfx(self):
        print "reinitializing your hair"
        maya.mel.eval( "hrReinitializeSolver;" )
        maya.mel.eval( "hrClearCache;" )
 
 
    def hair_set(self):
        print "selecting curves and attaching them"
        get_hair_simulator=cmds.ls(type="hrSimulatorShape")[0]
        getNode=[(nodes) for nodes in cmds.listHistory(get_hair_simulator, f=1) if cmds.nodeType(nodes) == 'nurbsCurve']
        cmds.select(getNode, r=1)           
        maya.mel.eval( 'xgmFindAttachment -description "Hair" -module "SplinePrimitive";' )
        print "creating temp cache path"
        get_work_cache_path = str(pathways.get("cache")) + '/hairTemp/'
        filename=str(cmds.file(q=1, location=1)).split('/')[-1]
        newfoldername=filename.split('.')[0]
        cache_path=get_work_cache_path+newfoldername+'/'           
        self.makeFolder(cache_path)
        # get_hair_simulator=cmds.ls(type="hrSimulatorShape")[0]
        cmds.setAttr(get_hair_simulator+".usePerFrameCache", 1)
        cmds.setAttr(get_hair_simulator+".perFrameCacheName", str(newfoldername), type="string")
        cmds.setAttr(get_hair_simulator+".cacheFolder", str(cache_path), type="string")
 
 
    def selectNclothMesh(self):
        typeN="mesh"
        getSel=cmds.ls(sl=1)
        if len(getSel)<1:
            getNode=[(item) for each in cmds.ls(type=typeN) for item in cmds.listRelatives(each, c=1, type="transform") if "Orig" not in str(each)]
        else:
            getNode=[(item) for each in cmds.ls(sl=1) for item in cmds.listHistory(each, f=1) if cmds.nodeType(item) == "mesh"]
        if getNode != None:
            cmds.select(getNode, r=1)
 
 
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
 
    # def importneck(self):
    #     if cmds.objExists("*:NECK_SMOOTHING_setup"):
    #         print "already exist - won't import"
    #         pass
    #     else:
    #         getcamlightPath='/jobs/vfx_cr/egf/egf1150/TASKS/techanim/maya/scenes/tmp/NECK_SMOOTHING_setup.mb'
    #         namer='NECK_SMOOTHING_setup'
    #         cmds.file(getcamlightPath, i=1, type="mayaBinary", ignoreVersion=1, ra=True, mergeNamespacesOnClash=False, namespace=namer, options="v=0;", pr=1)
    #         # getLocCam=cmds.ls(sl=1)[0]
    #         print "imported NECK_SMOOTHING_setup"
 
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
            getcamlightPath='/sw/dev/deglaue/cam_light_loc.mb'
            # getcamlightPath='/jobs/'+PROJECT+'/COMMON/'+DEPT+'/template/cam_light_loc.mb'
            namer='cam_light_loc'
            cmds.file(getcamlightPath, i=1, type="mayaBinary", ignoreVersion=1, ra=True, mergeNamespacesOnClash=False, namespace=namer, options="v=0;", pr=1)
            # getLocCam=cmds.ls(sl=1)[0]
            print "imported cam lights"
        # if cmds.objExists("techanim_playblast_shd"):
        #     FVfirst=cmds.ls("techanim_playblast_shd")[0]
        #     print "shader already exists. Won't create"
        #     print cmds.getAttr("techanim_playblast_shd.color")
        #     if cmds.getAttr("techanim_playblast_shd.color")==[(1.0, 1.0, 1.0)]:
        #         print "default grey blast"
        #         self.makeDefaultsetup(FVfirst)
        #     else:
        #         print "occ blast"
        #         self.makeOccsetup(FVfirst)
        # else:              
        #     FVfirst = cmds.shadingNode('blinn', asShader=True, n="techanim_playblast_shd")
        #     self.makeOccsetup(FVfirst)
 
    def makeDefaultsetup(self, FVfirst):
        maya.mel.eval( "setRendererInModelPanel base_OpenGL_Renderer modelPanel3;" )
        cmds.modelEditor('modelPanel4', e=1, dl="default")
        cmds.modelEditor( 'modelPanel4', e=1, twoSidedLighting=False) # Query for non-UI names for any render overrides
        cmds.modelEditor( 'modelPanel4', e=1, shadows=False) # Query for non-UI names for any render overrides
        cmds.modelEditor( 'modelPanel4', e=1, twoSidedLighting=False) # Query for non-UI names for any render overrides
        # cmds.setAttr("piggo_okja*:animGeo.res", 4)           
        '''---------------------------------
        assign shader
        ---------------------------------'''
        getType=["*:noTransform", "*:c_okja_001_mid", "*:c_okja_001_hi","*:c_okja_001_xhi", "c_okja_001_hi", "c_okja_001_mid", "c_okja_001_xhi"]
        collectItem=[(item) for each in getType for item in cmds.ls(each) ] 
        setName="sash"
        # getSel=cmds.listRelatives(cmds.ls('postTech'), ad=1, type="mesh")       
        cmds.setAttr("techanim_playblast_shd.color", 0.5, 0.5, 0.5, type="double3")
        cmds.setAttr("techanim_playblast_shd.eccentricity", 0.0)
        cmds.setAttr("techanim_playblast_shd.specularRollOff", 0.0)
        cmds.setAttr("techanim_playblast_shd.specularColor", .0, .0, .0, type="double3")
        cmds.setAttr("techanim_playblast_shd.reflectivity", 0.0)
        if cmds.objExists(setName):
            pass
        else:
            cmds.sets(n=setName, co=3)
        for selected in collectItem:
            cmds.sets(selected, add=setName)
            cmds.select(selected)
            cmds.hyperShade(assign=str(FVfirst))
            cmds.select( cl=True )
        print "set for default"
 
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
        # cmds.setAttr("piggo_okja*:animGeo.res", 4)           
        '''---------------------------------
        assign shader
        ---------------------------------'''
        getType=["*:noTransform", "*:c_okja_001_mid", "*:c_okja_001_hi","*:c_okja_001_xhi", "c_okja_001_hi", "c_okja_001_mid", "c_okja_001_xhi"]
        collectItem=[(item) for each in getType for item in cmds.ls(each) ] 
        setName="sash"
        # getSel=cmds.listRelatives(cmds.ls('postTech'), ad=1, type="mesh")       
        cmds.setAttr("techanim_playblast_shd.color", 1.0, 1.0, 1.0, type="double3")
        cmds.setAttr("techanim_playblast_shd.eccentricity", 0.453)
        cmds.setAttr("techanim_playblast_shd.specularRollOff", 0.222)
        cmds.setAttr("techanim_playblast_shd.specularColor", .470, .470, .470, type="double3")
        cmds.setAttr("techanim_playblast_shd.reflectivity", 0.0)
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
        # cmds.setAttr("piggo_okja*:animGeo.res", 4)           
        '''---------------------------------
        assign shader
        ---------------------------------'''
        getType=["*:noTransform", "*:c_okja_001_mid", "*:c_okja_001_hi","*:c_okja_001_xhi", "c_okja_001_hi", "c_okja_001_mid", "c_okja_001_xhi"]
        collectItem=[(item) for each in getType for item in cmds.ls(each) ] 
        setName="sash"
        # getSel=cmds.listRelatives(cmds.ls('postTech'), ad=1, type="mesh")       
        FVfirst = cmds.shadingNode('blinn', asShader=True, n="techanim_playblast_shd")
        getFVfirst=[FVfirst]
        cmds.setAttr("techanim_playblast_shd.color", 1.0, 1.0, 1.0, type="double3")
        cmds.setAttr("techanim_playblast_shd.eccentricity", 0.453)
        cmds.setAttr("techanim_playblast_shd.specularRollOff", 0.222)
        cmds.setAttr("techanim_playblast_shd.specularColor", .470, .470, .470, type="double3")
        cmds.setAttr("techanim_playblast_shd.reflectivity", 0.0)
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
                            BlendShapeName=cmds.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", o="world", w=(0, 1.0))
                        except:
                            pass
                    elif grabNameChild in grabNameParent:
                        print "blending: "+childItem+' to '+parentItem
                        try:
                            BlendShapeName=cmds.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", o="world", w=(0, 1.0))
                        except:
                            pass
                    elif grabNameChild==grabNameParent:
                        print "blending: "+childItem+' to '+parentItem
                        try:
                            BlendShapeName=cmds.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", o="world", w=(0, 1.0))
                        except:
                            pass
 
    def blendSearchGroups_alias_morph(self):
        #only prefix
        # mc.select("rocket1Tech:c_bodySuit_simCage_hi_restShape_geo")
        # mc.deformer(typ="morph", foc=False,name='preWrinklesMorph')
        # mc.setAttr("preWrinklesMorph.preWrinkles",0.5)   
        selObj=cmds.ls(sl=1, fl=1)
        if selObj:
            pass
        else:
            print "must select a driver group and a driven group(same shortnames)"
            return
        parentObj=selObj[0]
        childrenObj=selObj[1]
        if ":" in childrenObj:
            name_blend=childrenObj.split(":")[-1]+"_BSPS"
        else:
            name_blend = childrenObj+"_BSPS"
        print name_blend
        cmds.addAttr(parentObj, ln=name_blend, min=0, max=1, at="double", k=1, nn=name_blend)
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
                        try:
                            cmds.select(childItem, r=1)
                            truchild = mc.ls(childItem.split("Shape")[0])[0]
                            truparent = mc.ls(parentItem.split("Shape")[0])[0]
                            getpartial = parentItem.split("Shape")[0]
                            truparentmph = getpartial+"_mph"
                            print "morphing: "+truchild+' to '+truparent
                            mc.deformer(typ="morph", foc=False,name=truparentmph)
                            #Morph().add(truparentmph, truchild, truparent)
                            Morph().add(truparentmph, truchild, truparent, threshold=-1.0, neutral=False, force=True, transform=None, surface=False, connect=False, additive=False, inbetweens=False, combinations=False, alternativeName=None, safe=False)
                            mc.connectAttr(parentObj+"."+name_blend, truparentmph+".envelope", f=1)
                            mc.setAttr(truparentmph+"."+truparent, 1)
                        except:
                            pass
            # Morph().add(str(truparent)+"_mph", truchild, truparent, threshold=0.001, neutral=False, force=True, transform=None, surface=False, connect=False, additive=False, inbetweens=False, combinations=False, alternativeName=None, safe=True)
        # cmds.setAttr(parentObj+"."+name_blend, 1.0)
 
 
        # import pymel.core as pm
        # selObj=cmds.ls(sl=1, fl=1)
        # parentObj=selObj[0]
        # childrenObj=selObj[1]
        # if ":" in childrenObj:
        #     name_blend=childrenObj.split(":")[-1]+"_BSPS"
        # else:
        #     name_blend = childrenObj+"_BSPS"
        # print name_blend
        # cmds.addAttr(parentObj, ln=name_blend, min=0, max=1, at="double", k=1, nn=name_blend)
        # getparentObj=cmds.listRelatives(parentObj, ad=1, type="mesh")
        # getchildObj=cmds.listRelatives(childrenObj, ad=1, type="mesh")
        # for childItem  in getchildObj:
        #     for parentItem in getparentObj:
        #         if "Orig" not in str(childItem) and "Orig" not in str(parentItem):   
        #             grabNameChild=str(pm.PyNode(childItem).nodeName())
        #             grabNameParent=str(pm.PyNode(parentItem).nodeName())    
        #             if ":" in grabNameChild:
        #                 grabNameChild=grabNameChild.split(":")[-1]
        #             if ":" in grabNameParent:
        #                 grabNameParent=grabNameParent.split(":")[-1]
        #             grabNameChild=grabNameChild.split("Shape")[0]   
        #             grabNameParent=grabNameParent.split("Shape")[0]
        #             if grabNameParent in grabNameChild:
        #                 cmds.select(childItem, r=1)
        #                 truchild = mc.ls(childItem.split("Shape")[0])[0]
        #                 truparent = mc.ls(parentItem.split("Shape")[0])[0]
        #                 getpartial = parentItem.split("Shape")[0]
        #                 truparentmph = getpartial+"_mph"
        #                 print "morphing: "+truchild+' to '+truparent
        #                 print truparentmph
        #                 print truchild
        #                 print truparent
        #                 mc.deformer(typ="morph", foc=False,name=truparentmph)
        #                 Morph().add(truparentmph, truchild, truparent, threshold=0.001, neutral=False, force=True, transform=None, surface=False, connect=False, additive=False, inbetweens=False, combinations=False, alternativeName=None, safe=True)
        #                 mc.setAttr(truparentmph+"."+truparent, 1)
 
 
    def inputSearchGroups(self):
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
                            BlendShapeName=cmds.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", o="world", w=(0, 1.0))
                        except:
                            pass
                    elif grabNameChild in grabNameParent:
                        print "blending: "+childItem+' to '+parentItem
                        try:
                            BlendShapeName=cmds.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", o="world", w=(0, 1.0))
                        except:
                            pass
                    elif grabNameChild==grabNameParent:
                        print "blending: "+childItem+' to '+parentItem
                        try:
                            BlendShapeName=cmds.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", o="world", w=(0, 1.0))
                        except:
                            pass
 
    def blendSearchGroups_alias(self):
        #only prefix
        selObj=cmds.ls(sl=1, fl=1)
        if selObj:
            pass
        else:
            print "must select a driver group and a driven group(same shortnames)"
            return
        parentObj=selObj[0]
        childrenObj=selObj[1]
        name_blend=childrenObj.split(":")[-1]
        name_blend = name_blend+"_BSPS"
        cmds.addAttr(parentObj, ln=name_blend, min=0, max=1, at="double", k=1, nn=name_blend)
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
                            cmds.connectAttr(parentObj+"."+name_blend, grabNameParent+"_bs."+grabNameParent+"Shape",  f=1)
                        except:
                            pass
                    elif grabNameChild in grabNameParent:
                        print "blending: "+childItem+' to '+parentItem
                        try:
                            BlendShapeName=cmds.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", w=(0, 1.0))
                            cmds.connectAttr(parentObj+"."+name_blend, grabNameParent+"_bs."+grabNameParent+"Shape",  f=1)
                        except:
                            pass
                    elif grabNameChild==grabNameParent:
                        print "blending: "+childItem+' to '+parentItem
                        try:
                            BlendShapeName=cmds.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", w=(0, 1.0))
                            cmds.connectAttr(parentObj+"."+name_blend, grabNameParent+"_bs."+grabNameParent+"Shape",  f=1)
                        except:
                            pass
        cmds.setAttr(parentObj+"."+name_blend, 1.0)
 
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
        cmds.loadPlugin('pointGlue', qt=1)
        result = mc.promptDialog(
            title='Confirm',
            message='Falloff:',
            text='.001',
            button=['Continue','Cancel'],
            defaultButton='Continue',
            cancelButton='Cancel',
            dismissString='Cancel' )
        if result == 'Continue':
            falloff_amt = mc.promptDialog(query=True, text=True)
            falloff_amt = float(falloff_amt)
        else:
            print "selection transfer cancelled"
            return           
        # maya.mel.eval( "catch(`loadPlugin '/sw/packages/internal.td/mrigplugins/1.1.6/maya/2016.5/linux_ub12_x86-64/plugins/build/pointGlue.so'`);")
        # maya.mel.eval( "pluginInfo -edit -autoload true '/sw/packages/internal.td/mrigplugins/1.1.6/maya/2016.5/linux_ub12_x86-64/plugins/build/pointGlue.so';")       
        blenderShape=cmds.ls(sl=1)[0]
        for each in cmds.ls(sl=1)[1:]:
            command='pointGlue -s "%s" -t "%s" -max %f' % (str(blenderShape), each, falloff_amt)
            maya.mel.eval( command )
 
    def pointGlue_one_to_mass(self):
        cmds.loadPlugin('pointGlue', qt=1)
        result = mc.promptDialog(
            title='Confirm',
            message='Falloff:',
            text='.001',
            button=['Continue','Cancel'],
            defaultButton='Continue',
            cancelButton='Cancel',
            dismissString='Cancel' )
        if result == 'Continue':
            falloff_amt = mc.promptDialog(query=True, text=True)
            falloff_amt = float(falloff_amt)
        else:
            print "selection transfer cancelled"
            return                   
        # maya.mel.eval( "catch(`loadPlugin '/sw/packages/internal.td/mrigplugins/1.1.6/maya/2016.5/linux_ub12_x86-64/plugins/build/pointGlue.so'`);")
        # maya.mel.eval( "pluginInfo -edit -autoload true '/sw/packages/internal.td/mrigplugins/1.1.6/maya/2016.5/linux_ub12_x86-64/plugins/build/pointGlue.so';")       
        blenderShape=cmds.ls(sl=1)[0]
        for each in cmds.ls(sl=1)[1:]:
            command='pointGlue -s "%s" -t "%s" -max %f' % (each, str(blenderShape), falloff_amt)
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
 
    def hookupOkja(self):
        subDept="anim"
        hiresTechAsset=SHOT+'_piggo_okja1_'+DEPT+'_charPiggoOkjaModelHi.mb'
        hiresAnimAsset=SHOT+'_piggo_okja1_'+subDept+'_charPiggoOkjaModelHi.mb'
        getTechPath='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/instances/piggo_okja1/'+DEPT+'/highest/hi/abcmb/'+hiresTechAsset
        getAnimPath='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/instances/piggo_okja1/'+subDept+'/highest/hi/abcmb/'+hiresAnimAsset
        if os.path.isfile(getTechPath):
            cmds.file(getTechPath, i=1, type="mayaBinary", ignoreVersion=1, ra=True, mergeNamespacesOnClash=False, namespace=hiresTechAsset, options="v=0;", pr=1)
            print "Loaded techanim hires alembic"
            aNewString=hiresTechAsset.replace( '.mb', '_mb')
            cmds.blendShape(aNewString+':c_okja_001_hi', 'harness_truck1Tech:c_okja_001_hi_preTech_geo', w=(0, 1.0))
        else:
            if os.path.isfile(getAnimPath):
                cmds.file(getAnimPath, i=1, type="mayaBinary", ignoreVersion=1, ra=True, mergeNamespacesOnClash=False, namespace=hiresAnimAsset, options="v=0;", pr=1)
                print "Could not find techanim hires alembic. Loading anim high alembic"
                self.animWarning()
                aNewString=hiresAnimAsset.replace( '.mb', '_mb')
                cmds.blendShape(aNewString+':c_okja_001_hi', 'harness_truck1Tech:c_okja_001_hi_preTech_geo', w=(0, 1.0))
        # cmds.select([aNewString+':char_piggo_okja__model__hi', 'piggo_okja1:char_piggo_okja__model__hi'], r=1)
        # self.blendSearchGroups()
        # cmds.blendShape()
        defName="harness_blend"
        if cmds.objExists('piggo_okja1:c_okja_001_hi'):
            cmds.blendShape('harness_truck1Tech:c_okja_001_hi_postTech_geo', 'piggo_okja1:c_okja_001_hi', n=defName, w=(0, 1.0))
        else:
            print "unable to access piggo_okja1 - please check name"
        cmds.setAttr("piggo_okja1:animGeo.res", 4)
        # cmds.select('*charPiggoOkjaModelHi:c_blackbox_001_grp_hi', r=1)            
        # cmds.select('*piggo_okja1_techanim_charPiggoOkjaModel*:c_blackbox_001_grp_hi', r=1)
        # cmds.select('piggo_okja1:c_blackbox_001_grp_hi', add=1)
        # self.blendSearchGroups()
        # self.initialize_strt_based_on_wkrange()
 
 
    def hookupsash(self):
        subDept="anim"
        hiresTechAsset=SHOT+'_piggo_okja1_'+DEPT+'_charPiggoOkjaModelMid.mb'
        hiresAnimAsset=SHOT+'_piggo_okja1_'+subDept+'_charPiggoOkjaModelMid.mb'
        getTechPath='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/instances/piggo_okja1/'+DEPT+'/highest/mid/abcmb/'+hiresTechAsset
        getAnimPath='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/instances/piggo_okja1/'+subDept+'/highest/mid/abcmb/'+hiresAnimAsset
        if os.path.isfile(getTechPath):
            cmds.file(getTechPath, i=1, type="mayaBinary", ignoreVersion=1, ra=True, mergeNamespacesOnClash=False, namespace=hiresTechAsset, options="v=0;", pr=1)
            print "Loaded techanim hires alembic"
            aNewString=hiresTechAsset.replace( '.mb', '_mb')
            # cmds.blendShape(aNewString+':c_okja_001_mid', 'okja_sash1Tech:c_okja_001_collider', w=(0, 1.0))
        else:
            if os.path.isfile(getAnimPath):
                cmds.file(getAnimPath, i=1, type="mayaBinary", ignoreVersion=1, ra=True, mergeNamespacesOnClash=False, namespace=hiresAnimAsset, options="v=0;", pr=1)
                print "Could not find techanim hires alembic. Loading anim high alembic"
                self.animWarning()
                aNewString=hiresAnimAsset.replace( '.mb', '_mb')
                cmds.blendShape(aNewString+':c_okja_001_mid', 'okja_sash1Tech:c_okja_001_collider', w=(0, 1.0))
        # defName="sash_blend"
        # if cmds.objExists('piggo_okja1:c_okja_001_mid'):
            # cmds.blendShape('piggo_okja1:c_okja_001_mid', 'okja_sash1Tech:c_okja_001_mid', n=defName, w=(0, 1.0))
        # cmds.setAttr("piggo_okja1:animGeo.res", 3)
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
 
    def hookupOkja_simple(self):
        getAlembic=cmds.ls(sl=1)[0]
        cmds.blendShape(getAlembic, 'harness_truck1Tech:c_okja_001_hi_preTech_geo', w=(0, 1.0))
        defName="harness_blend"
        cmds.blendShape('harness_truck1Tech:c_okja_001_hi_postTech_geo', 'piggo_okja1:c_okja_001_hi', n=defName, w=(0, 1.0))
        cmds.setAttr("piggo_okja1:animGeo.res", 4)
        cmds.select('*charPiggoOkjaModelHi:c_blackbox_001_grp_hi', r=1)
        cmds.select('piggo_okja1:c_blackbox_001_grp_hi', add=1)
        self.blendSearchGroups()
        self.initialize_strt_based_on_wkrange()
 
 
    def fix_rainbow(self):
        getAlembic=cmds.ls(sl=1)
        if len(getAlembic) == 0:
            for each in cmds.ls("*:*.displayColors"):
                cmds.setAttr(each, 0)           
            for each in cmds.ls("*.displayColors"):
                cmds.setAttr(each, 0)     
        else:
            for each in getAlembic:
                cmds.setAttr(each+".displayColors", 0)                 
 
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
 
    def load_cache(self, listed_folder):
        if len(cmds.ls(sl=1))<1:
            getSel = [(each) for each in cmds.ls(type = "nCloth") if "Orig" not in each]
        else:
            getSel = cmds.ls(sl=1)
        # filepath = make_new_content+"/"+listed_folder
        # filexml = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(filepath) for name in files if name.lower().endswith(".xml")][0]
        # getSel=cmds.ls(sl=1) 
              
        # if len(getSel)>0:
        for each in getSel:
            getMesh=[(item) for clothitem in cmds.ls(getSel) for item in cmds.listHistory(clothitem) if cmds.nodeType(item) == "mesh" if "Orig" not in item][0]
            # cmds.select(each)
            findName = each.replace(":", "_")
            newName=findName+'.xml'
            filexml = listed_folder+'/'+newName
            pm.mel.doImportCacheFile(filexml, '', each, getMesh)
 
    def checkCacheFile(self, interrogateName):
        cachefolderStart=getCachePath
        number=0000
        getScene=cmds.file(q=1, sn=1, shn=1)
        getFilename =  getScene.split(".")[:-1]
        getFilename='_'.join(getFilename)+"_"+str(getUser)+"_nCache"
        getnewcachefolder=getFilename+"_"+str("%04d" % (number,))
        makecachefolder = cachefolderStart+"/"+getnewcachefolder
        if os.path.exists(makecachefolder):
            get_vr_folders=[(dirnames) for dirpath, dirnames, files in os.walk(cachefolderStart)][0]
            get_vr_folders=[(each) for each in get_vr_folders if each.split("_")[-1].isdigit()]
            get_top = max(get_vr_folders)
            number = get_top.split("_")[-1]
            if "v" not in number:
                number = int(number)
            else:
                number = re.sub("\D", "", number)
            number = int(number)
            number +=1
            getnewcachefolder=getFilename+"_"+str("%04d" % (number,))
            makecachefolder = cachefolderStart+"/"+getnewcachefolder
            os.makedirs(makecachefolder)
            print "created "+makecachefolder
        if not os.path.exists(makecachefolder):
            os.makedirs(makecachefolder)
            print "created "+makecachefolder
        print getFilename, makecachefolder
        return getFilename, makecachefolder
 
    def load_cloth_cache(self, make_new_content, listed_folder):
        filepath = make_new_content+"/"+listed_folder+"/"
        grabsystem=cmds.ls(type="nCloth")
        cmds.select(grabsystem, r=1)      
        getLowRange=cmds.playbackOptions(q=1, ast=1)
        getHiRange=cmds.playbackOptions(q=1, aet=1)
        if len(cmds.ls(sl=1))<1:
            getHairSel = [(each) for each in cmds.ls(type = "nCloth") if "Orig" not in each]
        else:
            getHairSel = cmds.ls(sl=1)       
        createdict = [(name) for dirpath, dirnames, files in os.walk(str(filepath)) for name in files if name.lower().endswith(".mcx")]
        filecloth = [(name) for dirpath, dirnames, files in os.walk(str(filepath)) for name.split(".")[-1] in files]
        getSel=cmds.ls(sl=1)
        if len(getHairSel)>0:
            for value in createdict:
                for hairbit in getHairSel:   
                    grab_filename_match = hairbit.replace(':', '_')  
                    presetName = value.split(".")[0]
                    filexml=str(filepath)+value
                    if grab_filename_match == presetName:
                        getCache=[(nodes) for nodes in mc.listHistory(hairbit) if mc.nodeType(nodes) == "cacheBlend"]
                        if len(getCache)>0:
                            mc.delete(getCache)
                        getCache=[(nodes) for nodes in mc.listHistory(hairbit) if mc.nodeType(nodes) == "cacheFile"]
                        if len(getCache)>0:
                            mc.delete(getCache)  
                        presetName = value.split(".")[0]
                        cache_path = filepath.replace('//', '/')
                        cache_name = presetName
                        shape = hairbit             
                        createdCacheFileNode = mc.createNode("cacheFile", n=presetName+"Cache1")
                        mc.setAttr(createdCacheFileNode+".cachePath", filepath, type = "string")
                        mc.setAttr(createdCacheFileNode+".cacheName", presetName, type = "string")
                        mc.setAttr(createdCacheFileNode+".startFrame", getLowRange)
                        mc.setAttr(createdCacheFileNode+".originalStart", getLowRange)
                        mc.setAttr(createdCacheFileNode+".sourceStart", getLowRange)
                        mc.setAttr(createdCacheFileNode+".originalEnd", getHiRange)
                        mc.setAttr(createdCacheFileNode+".sourceEnd", getHiRange)
                        mc.setAttr(createdCacheFileNode+".inRange", 1)
                        mc.connectAttr(createdCacheFileNode+".inRange", hairbit+".playFromCache", f=1)
                        mc.connectAttr(createdCacheFileNode+".outCacheData[0]", hairbit+".positions", f=1)          
                        mc.connectAttr("time1.outTime", createdCacheFileNode+".time", f=1)              
 
 
    def load_hair_cache(self, make_new_content, listed_folder):
        getLowRange=cmds.playbackOptions(q=1, ast=1)
        print getLowRange
        getHiRange=cmds.playbackOptions(q=1, aet=1)
        print getHiRange
        if len(cmds.ls(sl=1))<1:
            getHairSel = [(each) for each in cmds.ls(type = "hairSystem") if "Orig" not in each]
        else:
            getHairSel = cmds.ls(sl=1)       
        filepath = make_new_content+"/"+listed_folder+"/"
        createdict = [(name) for dirpath, dirnames, files in os.walk(str(filepath)) for name in files if name.lower().endswith(".mcx")]
        filecloth = [(name) for dirpath, dirnames, files in os.walk(str(filepath)) for name.split(".")[-1] in files]
        getSel=cmds.ls(sl=1)
        if len(getHairSel)>0:
            for value in createdict:
                for hairbit in getHairSel:              
                    filexml=str(filepath)+value
                    grabName = hairbit.split(":")[-1]
                    if grabName in value:
                        getCache=[(nodes) for nodes in cmds.listHistory(hairbit) if cmds.nodeType(nodes) == "cacheBlend"]
                        if len(getCache)>0:
                            cmds.delete(getCache)
                        getCache=[(nodes) for nodes in cmds.listHistory(hairbit) if cmds.nodeType(nodes) == "cacheFile"]
                        if len(getCache)>0:
                            cmds.delete(getCache)  
                        presetName = value.split(".")[0]
                        cache_path = filepath
                        cache_name = presetName
                        shape = hairbit
                        createdCacheFileNode = cmds.createNode("cacheFile", n=presetName+"Cache1")
                        cmds.setAttr(createdCacheFileNode+".cachePath", filepath, type = "string")
                        cmds.setAttr(createdCacheFileNode+".cacheName", presetName, type = "string")
                        cmds.setAttr(createdCacheFileNode+".startFrame", getLowRange)
                        cmds.setAttr(createdCacheFileNode+".originalStart", getLowRange)
                        cmds.setAttr(createdCacheFileNode+".sourceStart", getLowRange)
                        cmds.setAttr(createdCacheFileNode+".originalEnd", getHiRange)
                        cmds.setAttr(createdCacheFileNode+".sourceEnd", getHiRange)
                        cmds.setAttr(createdCacheFileNode+".inRange", 1)
                        cmds.connectAttr(createdCacheFileNode+".inRange", hairbit+".playFromCache", f=1)
                        cmds.connectAttr(createdCacheFileNode+".outCacheData[0]", hairbit+".hairCounts", f=1)
                        cmds.connectAttr(createdCacheFileNode+".outCacheData[1]", hairbit+".vertexCounts", f=1)
                        cmds.connectAttr(createdCacheFileNode+".outCacheData[2]", hairbit+".positions", f=1)          
                        # cmds.connectAttr(createdCacheFileNode+".outCacheData[0]", createdCacheBlendNode+".vectorArray[1]", f=1)            
        else:
            for value in createdict:
                for hairbit in getHairSel:
                    filexml=str(filepath)+value
                    grabName = hairbit.split(":")[-1]
                    if grabName in value:
                        getCache=[(nodes) for nodes in cmds.listHistory(hairbit) if cmds.nodeType(nodes) == "cacheBlend"]
                        if len(getCache)>0:
                            cmds.delete(getCache)
                        getCache=[(nodes) for nodes in cmds.listHistory(hairbit) if cmds.nodeType(nodes) == "cacheFile"]
                        if len(getCache)>0:
                            cmds.delete(getCache)  
                        presetName = value.split(".")[0]
                        cache_path = filepath
                        cache_name = presetName
                        shape = hairbit
                        createdCacheFileNode = cmds.createNode("cacheFile", n=presetName+"Cache1")
                        cmds.setAttr(createdCacheFileNode+".cachePath", filepath, type = "string")
                        cmds.setAttr(createdCacheFileNode+".cacheName", presetName, type = "string")
                        cmds.setAttr(createdCacheFileNode+".startFrame", getLowRange)
                        cmds.setAttr(createdCacheFileNode+".originalStart", getLowRange)
                        cmds.setAttr(createdCacheFileNode+".sourceStart", getLowRange)
                        cmds.setAttr(createdCacheFileNode+".originalEnd", getHiRange)
                        cmds.setAttr(createdCacheFileNode+".sourceEnd", getHiRange)
                        cmds.connectAttr(createdCacheFileNode+".inRange", hairbit+".playFromCache", f=1)
                        cmds.connectAttr(createdCacheFileNode+".outCacheData[0]", hairbit+".hairCounts", f=1)
                        cmds.connectAttr(createdCacheFileNode+".outCacheData[1]", hairbit+".vertexCounts", f=1)
                        cmds.connectAttr(createdCacheFileNode+".outCacheData[2]", hairbit+".positions", f=1)
                        # pm.mel.doImportCacheFile(filexml, '', hairbit, presetName) 
                        # getCommand='createHistorySwitch("%s",false)' %hairbit
                        # switch = maya.mel.eval(getCommand)
                        # cacheNode = cmds.cacheFile(f=filexml, ia='%s.inp[0]' % switch ,attachFile=True)
                        # cmds.setAttr( '%s.playFromCache' % switch, 1 )
                        # cmds.select(hairbit, r=1)
                        # newBlend = cmds.cacheFileCombine()
                        # print newBlend
                        # cmds.cacheFileCombine(newBlend[0], e=1, cc = createdCacheFileNode)
                        # outCacheData[0], hairCounts
                        # channel_name = maya.mel.eval('cacheFile -dir "{cache_path}" -fileName "{cache_name}.xml" -q -channelName'.format(cache_path=cache_path, cache_name=cache_name))
                        # hs_node = pm.PyNode(maya.mel.eval('createHistorySwitch("'+shape.name()+'",false)'))
                        # getCommand='createHistorySwitch("%s",false)' %hairbit
                        # hs_node = pm.PyNode(maya.mel.eval(getCommand))
                        # cf_node = pm.PyNode(pm.cacheFile(dir=cache_path, fileName=cache_name, channelName=channel_name, ia=hs_node.inp[0], attachFile=True))
                        # cf_node = pm.PyNode(pm.cacheFile(dir=cache_path, fileName=cache_name, channelName=channel_name, attachFile=True))
                        # pm.connectAttr(cf_node.inRange, hs_node.pfc)
                        # doAttachCacheArgList(0,{});
                        # cmds.select(hairbit, r=1)
                        # getCommand='doAttachCacheArgList(0,{"%s" "%s" "%s"});' %(cache_path, presetName, hairbit)
                        # maya.mel.eval(getCommand)
 
    def load_hair_cacheV1(self, listed_folder):
        if len(cmds.ls(sl=1))<1:
            getSel = [(each) for each in cmds.ls(type = "hairSystem") if "Orig" not in each]
        else:
            getSel = cmds.ls(sl=1)
        # filepath = make_new_content+"/"+listed_folder
        # filexml = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(filepath) for name in files if name.lower().endswith(".xml")][0]
        # getSel=cmds.ls(sl=1) 
        # if len(getSel)>0:
        for each in getSel:
            getCache=[(nodes) for nodes in cmds.listHistory(each) if cmds.nodeType(nodes) == "cacheBlend"]
            if len(getCache)>0:
                cmds.delete(getCache)
            getCache=[(nodes) for nodes in cmds.listHistory(each) if cmds.nodeType(nodes) == "cacheFile"]
            if len(getCache)>0:
                cmds.delete(getCache)          
            # cmds.select(each)
            findName = each.replace(":", "_")
            newName=findName+'.xml'
            print newName
            filexml = listed_folder+'/'+newName
            print filexml
            # pm.mel.doImportCacheFile(filexml, '', getSel, each)
            pm.mel.doImportCacheFile(filexml, '', findName, each)
 
 
                # getHistorySwitch=[(nodes) for nodes in cmds.listHistory(each) if cmds.nodeType(nodes) == "historySwitch"]
                # getCache=[(nodes) for nodes in cmds.listHistory(each) if cmds.nodeType(nodes) == "cacheFile"]
                # try:
                #     cmds.delete(getHistorySwitch)
                # except:
                #     pass
                # try:
                #     cmds.delete(getCache)
                # except:
                #     pass  
                #getShape=cmds.listRelatives(each, ad=1, type="historySwitch")
                # if len(getCache)>0:
                #     try:
                #         maya.mel.eval('deleteCacheFile 2 { "keep", "" } ;')
                #     except:
                #         pass
                #     cmds.delete(getHistorySwitch)
                #     getCommand='createHistorySwitch("%s",false)' %each
                #     switch = maya.mel.eval(getCommand)
                #     cacheNode = cmds.cacheFile(f=filexml, ia='%s.inp[0]' % switch ,attachFile=True)
                #     cmds.setAttr( '%s.playFromCache' % switch, 1 )                          
                # if len(getHistorySwitch)>0:
                #     try:
                #         maya.mel.eval('deleteCacheFile 2 { "keep", "" } ;')
                #     except:
                #         pass
                #     getCommand='createHistorySwitch("%s",false)' %each
                #     switch = maya.mel.eval(getCommand)
                #     cacheNode = cmds.cacheFile(f=filexml, ia='%s.inp[0]' % switch ,attachFile=True)
                #     cmds.setAttr( '%s.playFromCache' % switch, 1 )  
                # else:
                # print each
                # getCommand='createHistorySwitch("%s",false)' %each
                # switch = maya.mel.eval(getCommand)
                # cacheNode = cmds.cacheFile(f=filexml)
                # cmds.connectAttr(cacheNode+".outCacheData[0]",each+".positions")
                # import pymel.core as pm
                # pm.mel.doImportCacheFile(filexml, 'mcx', each)
                # cmds.setAttr( '%s.playFromCache' % switch, 1 )                    
                    # if len(getHistorySwitch)>0:
                    #     getCommand='createHistorySwitch("%s",false)' %each
                    #     switch = maya.mel.eval(getCommand)
                    #     cacheNode = cmds.cacheFile(f=filexml, ia='%s.inp[0]' % switch ,attachFile=True)
                    #     cmds.setAttr( '%s.playFromCache' % switch, 1 )
                    # else:
                    #     getCommand='createHistorySwitch("%s",true)' %each
                    #     switch = maya.mel.eval(getCommand)
                    #     cacheNode = cmds.cacheFile(f=filexml, ia='%s.inp[0]' % switch ,attachFile=True)
                    #     cmds.setAttr( '%s.playFromCache' % switch, 1 )                       
                # else:
                #     cacheNode = cmds.cacheFile(f=filexml, ia='%s.inp[0]' % switch ,attachFile=True)
                #     cmds.setAttr( '%s.playFromCache' % switch, 1 )
        # else:
        #     print "can't find cache in scene"
 
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
        # selobj = cmds.ls(sl=1)
        # if len(selobj)>0:
        #     mainRig = selobj[0]
        # else:
        mainRig=[(each) for each in cmds.ls("*:*animGeo") if cmds.nodeType(each)=="transform" and cmds.listRelatives(each, p=1)==None][0]
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
        # for each in mainRig:
        cmds.setAttr(mainRig+".selectableGeo", 1)
        cmds.setAttr(mainRig+".ctrlVis", 1)
 
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
    # def load_cache(self, make_new_content, listed_folder):
    #     filepath = make_new_content+"/"+listed_folder
    #     filexml = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(filepath) for name in files if name.lower().endswith(".xml")][0]
    #     getSel=cmds.ls(sl=1)
    #     if len(getSel)>0:
    #         for each in getSel:
    #             getShape=[(nodes) for nodes in cmds.listHistory(each) if cmds.nodeType(nodes) == "historySwitch"]
    #             #getShape=cmds.listRelatives(each, ad=1, type="historySwitch")
    #             if len(getShape)>0:
    #                 maya.mel.eval('deleteCacheFile 2 { "keep", "" } ;')
    #             getCommand='createHistorySwitch("%s",false)' %each
    #             switch = maya.mel.eval(getCommand)
    #             cacheNode = cmds.cacheFile(f=filexml, ia='%s.inp[0]' % switch ,attachFile=True)
    #             cmds.setAttr( '%s.playFromCache' % switch, 1 )
    #     else:
    #         print "select something"           
 
 
    def collision_fix(self):
        projectFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT
        animFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/instances/'
        abcFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/cache/alembic/'
        pbFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/movies/'
        rvFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/'+DEPT
        spaceWork='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/scenes'
        pathways={'open folder':spaceWork, "work":spaceWork, "project":projectFolder, "products":animFolder, "alembic":abcFolder, "blasts":rvFolder}
        # print str(pathways.keys())
        sgVarFilePath = '/jobs/%s/%s/%s/TECH/lib/shotgun/setshot.d/sgvars' % (PROJECT, SCENE, SHOT)
        if os.path.isfile(sgVarFilePath):
            # get available in/out values
            franges = {'WORK_IN': None, 'CUT_IN': None,
                       'WORK_OUT': None, 'CUT_OUT': None}
            for line in open(sgVarFilePath, 'r'):
                if "CUT_DURATION" in line:
                    shot_len_value = line.split('=')[-1].strip()
                    try:
                        shot_len_value = int(shot_len_value)
                    except:
                        shot_len_value = None
                if 'CUT_IN' in line:
                    cut_in_value = line.split('=')[-1].strip()
                    try:
                        cut_in_value = int(cut_in_value)
                    except:
                        cut_in_value = None
                if 'CUT_OUT' in line:
                    cut_out_value = line.split('=')[-1].strip()
                    try:
                        cut_out_value = int(cut_out_value)
                    except:
                        cut_out_value = None
                if 'WORK_IN' in line:
                    wk_strt_value = line.split('=')[-1].strip()
                    try:
                        wk_strt_value = int(wk_strt_value)
                    except:
                        wk_strt_value = None
                if 'WORK_OUT' in line:
                    wk_out_value = line.split('=')[-1].strip()
                    try:
                        wk_out_value = int(wk_out_value)
                    except:
                        wk_out_value = None
        bodyCollideMesh = '*:c_body*coll_geo'          
        print bodyCollideMesh 
        getStrtRangefloat=cmds.playbackOptions(q=1, ast=1)#get framerange of scene to set keys in iteration
        getStrtRange = str(getStrtRangefloat).split('.')[0]
        cmds.currentTime(getStrtRange)
        cmds.duplicate(bodyCollideMesh, n='c_body_001_pl_geo_'+str(getStrtRange))
        cmds.setAttr('c_body_001_pl_geo_'+str(getStrtRange)+'.visibility', 0)
        cmds.currentTime(wk_strt_value)
        cmds.duplicate(bodyCollideMesh, n='c_body_001_pl_geo_'+str(wk_strt_value))
        cmds.setAttr('c_body_001_pl_geo_'+str(wk_strt_value)+'.visibility', 0)
        childItemls='c_body_001_pl_geo_'+str(getStrtRange)
        parentItemls='c_body_001_pl_geo_'+str(wk_strt_value)
        defName='c_body_001_pl_geo_BS'
        BlendShapeName=cmds.blendShape(childItemls, parentItemls, n=defName)
        cmds.setKeyframe(BlendShapeName[0], t=wk_strt_value, at="c_body_001_pl_geo_"+getStrtRange, v=1.0 )
        cmds.setKeyframe(BlendShapeName[0], t=getStrtRangefloat, at="c_body_001_pl_geo_"+getStrtRange, v=0.0 )
        pdt.PostDeformToolset().createPeakDeformer([bodyCollideMesh], defName = 'c_body_001_lo_tech_geo_peak', distance = 0.000000, )
        cmds.setKeyframe('c_body_001_lo_tech_geo_peak', t=wk_strt_value, at='distance', v=0.12 )
        cmds.setKeyframe('c_body_001_lo_tech_geo_peak', t=getStrtRangefloat, at='distance', v=-0.12 )
        child='c_body_001_pl_geo_'+str(wk_strt_value)
        parentname=bodyCollideMesh
        defName='strt_c_body_001_pl_geo_BS'
        BlendShapeName=cmds.blendShape(child, parentname, n=defName)
        cmds.setKeyframe(BlendShapeName[0], t=wk_strt_value, at="c_body_001_pl_geo_1018", v=0.0 )
        cmds.setKeyframe(BlendShapeName[0], t=wk_strt_value-1, at="c_body_001_pl_geo_1018", v=1.0 )
        # userScriptDir = os.path.join(os.path.dirname("/jobs/vfx_motherland/COMMON/rig/peak"), 'peak')
        # bs = mc.ls(mc.listHistory(bodyCollideMesh), type='peak')
        # for each in bs:
        #     mWeights.load(each, filePath=os.path.join(userScriptDir, '%s.wts' % each))
 
    def eguard_skirt(self):
        self.nuc_pconstrnt_hip()
        cmds.setAttr("*:animGeo.capeVisibility", 1)
        cmds.blendShape( '*:c_leatherSkirt_1_simCage_mid_preTech_geo', '*:c_leatherSkirt_1_simCage_mid_sim_geo',n='c_leatherSkirt_1_simCage_mid_preTech_geo_BShape', w=(0, 1.0))
        cmds.blendShape('*:l_fishChainSkirt_1_simCage_mid_preTech_geo','*:l_fishChainSkirt_1_simCage_mid_sim_geo',  n='l_fishChainSkirt_1_simCage_mid_preTech_geo_BShape', w=(0, 1.0))
        cmds.blendShape('*:r_fishChainSkirt_1_simCage_mid_preTech_geo', '*:r_fishChainSkirt_1_simCage_mid_sim_geo', n='r_fishChainSkirt_1_simCage_mid_preTech_geo_BShape', w=(0, 1.0))
        cmds.select(['c_leatherSkirt_1_simCage_mid_preTech_geo_BShape', 'l_fishChainSkirt_1_simCage_mid_preTech_geo_BShape', 'r_fishChainSkirt_1_simCage_mid_preTech_geo_BShape'], r =1 )
        userScriptDir = os.path.join(os.path.dirname("/jobs/vfx_cr/COMMON/rig/"), 'blendShape')
        for each in cmds.ls(sl=1):
            mWeights.load('r_fishChainSkirt_1_simCage_mid_preTech_geo_BShape', filePath=os.path.join(userScriptDir, '%s.wts' % 'r_fishChainSkirt_1_simCage_mid_preTech_geo_BShape_bs'))
            mWeights.load('l_fishChainSkirt_1_simCage_mid_preTech_geo_BShape', filePath=os.path.join(userScriptDir, '%s.wts' % 'l_fishChainSkirt_1_simCage_mid_preTech_geo_BShape_bs'))
            mWeights.load('c_leatherSkirt_1_simCage_mid_preTech_geo_BShape', filePath=os.path.join(userScriptDir, '%s.wts' % 'c_leatherSkirt_1_simCage_mid_preTech_geo_BShape_bs'))
        cmds.setAttr("*:animGeo.res", 3)
        maya.mel.eval( 'CBdeleteConnection "%s:c_capeCloth_1_mid.v";' % '*')
        cmds.setAttr("*:c_capeCloth_1_mid.visibility",1)
        cmds.file('/jobs/vfx_cr/egf/egf2160/TASKS/techanim/maya/data/grnd.obj', i=1, iv=1, mnc=0, gr=1, gn="groundplane", op=1, rpr="grnd")
        cmds.select('pPlane1')
        cmds.CenterPivot()
        cmds.select(['*:c_leatherSkirt_1_simCage_mid_sim_nClothShape',
            "*:l_fishChainSkirt_1_simCage_mid_sim_nClothShape",
            "*:r_fishChainSkirt_1_simCage_mid_sim_nClothShape",
            "*:c_capeLeather_1_simCage_mid_sim_nClothShape", "pPlane1"],r=1)
        cmds.nClothMakeCollide()
         
 
    def cape_to_pauldrons(self):
        if cmds.objExists(cmds.ls('c_cape_fix_geo')[0]):
            try:
                cmds.ls('cape_fix_BShape')[0]
                print "this blendShape fix has already been applied"
                cmds.select('cape_fix_BShape', r=1)
                return
            except:
                defName='cape_fix_BShape'
                parentItemls = 'hela_greyBlack1Tech:c_cape_001_simCage_mid_sim_geo'
                childItemls = 'c_cape_fix_geo'
                self.load_cape_shoulder_map(parentItemls, childItemls, defName)
        else:
            dupname = 'c_cape_fix_geo'
            getclothgeo = 'hela_greyBlack1Tech:c_cape_001_simCage_mid_sim_geo'
            # defName='cape_fix_BShape'
            bodyCollideMesh = 'hela_greyBlack1Tech:c_cape_001_simCage_mid_tech_geo' 
            grouper = 'hela_greyBlack1Tech:tech_mid_geo_grp'
            cmds.select('hela_greyBlack1Tech:c_body_001_lo_tech_geo.vtx[2889]', r =1)
            waistedvert = cmds.ls(sl =1)[0]
            toolClass.point_const()
            startname = waistedvert.split(":")[1]
            getname = startname.split('.vtx')[0]
            getnum = re.findall('\d+', waistedvert)[-1]
            name = getname+"_vtx_"+str(getnum)
            transformWorldMatrix, rotateWorldMatrix=getBaseClass.selection_location_type(waistedvert)
            # maintransformWorldMatrix, mainrotateWorldMatrix=self.locationXForm(selection) 
            # rotateWorldMatrix = [0.0,0.0,0.0]
            # transformWorldVertex=pm.PyNode(waistedvert).getPosition()
            getBaseClass.buildJoint(name, transformWorldVertex, rotateWorldMatrix)
            jntname = getname+"_vtx_"+str(getnum)+"_jnt"
            plcname = getname+"_vtx_"+str(getnum)+"_ploc"
            cmds.parent(jntname, plcname)
            cmds.parent(plcname, grouper)
            cmds.duplicate(bodyCollideMesh, n=dupname) 
            transforms = [".tx", ".ty", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz"]
            for each in transforms:
                cmds.setAttr(dupname+each, l=0)
            parentItemls=getclothgeo
            childItemls=dupname
            defName='cape_fix_BShape'
            # BlendShapeName=cmds.blendShape(childItemls, parentItemls, n=defName, w=(0, 1.0))   
            cmds.setAttr(dupname+'.visibility', 0)
            selectgroups = {'hela_greyBlack1Tech:c_cape_001_simCage_mid_tech_geo.vtx[6234]': 'hela_greyBlack1Tech:r_shoulderPanel_1_mid_tech_geo.vtx[813]',
            'hela_greyBlack1Tech:c_cape_001_simCage_mid_tech_geo.vtx[390]':'hela_greyBlack1Tech:r_shoulderPanel_1_mid_tech_geo.vtx[800]',
            'hela_greyBlack1Tech:c_cape_001_simCage_mid_tech_geo.vtx[2644]':'hela_greyBlack1Tech:r_shoulderPanel_1_mid_tech_geo.vtx[765]',
            'hela_greyBlack1Tech:c_cape_001_simCage_mid_tech_geo.vtx[5418]':'hela_greyBlack1Tech:r_shoulderPanel_1_mid_tech_geo.vtx[779]',
            'hela_greyBlack1Tech:c_cape_001_simCage_mid_tech_geo.vtx[2088]':'hela_greyBlack1Tech:l_shoulderPanel_1_mid_tech_geo.vtx[684]',
            'hela_greyBlack1Tech:c_cape_001_simCage_mid_tech_geo.vtx[5370]':'hela_greyBlack1Tech:l_shoulderPanel_1_mid_tech_geo.vtx[798]',
            'hela_greyBlack1Tech:c_cape_001_simCage_mid_tech_geo.vtx[7647]':'hela_greyBlack1Tech:l_shoulderPanel_1_mid_tech_geo.vtx[809]',
            'hela_greyBlack1Tech:c_cape_001_simCage_mid_tech_geo.vtx[372]':'hela_greyBlack1Tech:l_shoulderPanel_1_mid_tech_geo.vtx[762]',
            'hela_greyBlack1Tech:c_cape_001_simCage_mid_tech_geo.vtx[7777]':'hela_greyBlack1Tech:l_shoulderPanel_1_mid_tech_geo.vtx[776]',
            'hela_greyBlack1Tech:c_cape_001_simCage_mid_tech_geo.vtx[6265]':'hela_greyBlack1Tech:l_shoulderPanel_1_mid_tech_geo.vtx[769]',
            'hela_greyBlack1Tech:c_cape_001_simCage_mid_tech_geo.vtx[5370]':'hela_greyBlack1Tech:l_shoulderPanel_1_mid_tech_geo.vtx[1692]',
            'hela_greyBlack1Tech:c_cape_001_simCage_mid_tech_geo.vtx[741]':'hela_greyBlack1Tech:l_shoulderPanel_1_mid_tech_geo.vtx[798]',
            'hela_greyBlack1Tech:c_cape_001_simCage_mid_tech_geo.vtx[9721]':'hela_greyBlack1Tech:r_shoulderPanel_1_mid_tech_geo.vtx[1683]',
            'hela_greyBlack1Tech:c_cape_001_simCage_mid_tech_geo.vtx[5606]':'hela_greyBlack1Tech:r_shoulderPanel_1_mid_tech_geo.vtx[769]'}
            for cape, shoulder in selectgroups.items():
                startname = cape.split(":")[1]
                getname = startname.split('.vtx')[0]
                getnum = re.findall('\d+', cape)[-1]
                name = getname+"_"+str(getnum)   
                cmds.select(shoulder)
                toolClass.point_const()
                plocthing = cmds.ls(sl=1)[0]
                transformWorldMatrix, rotateWorldMatrix=getBaseClass.selection_location_type(cape)
                # rotateWorldMatrix = [0.0,0.0,0.0]
                # transformWorldVertex=pm.PyNode(cape).getPosition()           
                getBaseClass.buildJoint(name, transformWorldMatrix, rotateWorldMatrix)
                jointname = name+"_jnt"
                startname = shoulder.split(":")[1]
                getname = startname.split('.vtx')[0]
                getnum = re.findall('\d+', shoulder)[-1]
                plcname = getname+"_vtx_"+str(getnum)+"_ploc"      
                cmds.parent(jointname, plcname)
                cmds.parent(plcname, grouper)
            childrenObj=cmds.ls(grouper)[0]
            getparentObj=cmds.listRelatives(childrenObj, ad=1, type="joint")
            cmds.select(getparentObj, r =1)
            cmds.select("c_cape_fix_geo", add =1)
            cmds.skinCluster()
            self.load_cape_shoulder_map(parentItemls, childItemls, defName)
 
    def load_cape_shoulder_map(self, parentItemls, childItemls, defName):
        BlendShapeName=cmds.blendShape(childItemls, parentItemls, n=defName, w=(0, 1.0)) 
        userScriptDir = os.path.join(os.path.dirname("/jobs/vfx_cr/COMMON/rig/blendShape"), 'blendShape')
        mWeights.load(defName, filePath=os.path.join(userScriptDir, '%s.wts' % defName))
 
 
    def drag_whisker_fix(self):
        selected = [
        'rewireWhiskers_geo.e[7420:7421]',
        'rewireWhiskers_geo.e[7470]',
        'rewireWhiskers_geo.e[7528:7529]',
        'rewireWhiskers_geo.e[7596:7597]',
        'rewireWhiskers_geo.e[7621]',
        'rewireWhiskers_geo.e[7642]',
        'rewireWhiskers_geo.e[7704:7705]',
        'rewireWhiskers_geo.e[7777:7778]',
        'rewireWhiskers_geo.e[7857:7858]',
        'rewireWhiskers_geo.e[7921]',
        'rewireWhiskers_geo.e[7968]',
        'rewireWhiskers_geo.e[8016]',
        'rewireWhiskers_geo.e[8064]',
        'rewireWhiskers_geo.e[8112]',
        'rewireWhiskers_geo.e[8148]',
        'rewireWhiskers_geo.e[8165]',
        'rewireWhiskers_geo.e[8181]',
        'rewireWhiskers_geo.e[8196]',
        'rewireWhiskers_geo.e[8212]',
        'rewireWhiskers_geo.e[8228]',
        'rewireWhiskers_geo.e[8245]',
        'rewireWhiskers_geo.e[8268]']
        cmds.select(selected, r=1)
        cmds.polyToCurve(form=2, degree=3)
        cmds.rename(cmds.ls(sl=1)[0], "R_whisker_crv")
        cmds.rebuildCurve("R_whisker_crv", ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=0, kt=0, s=26, d=2, tol=0.001)
        cmds.delete('R_whisker_crv', ch=1)
        cmds.select(cmds.ls('rewireWhiskers_geo')[0], r=1)
        cmds.wire(w='R_whisker_crv', n = 'R_wire', gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
        #load wire blend maps
        userScriptDir = os.path.join(os.path.dirname("/jobs/vfx_cr/slm/slm4700/TASKS/techanim/maya/scenes/wire"), 'wire')
        bs = mc.ls(mc.listHistory('rewireWhiskers_geo'), type='wire')
        for each in bs:
            mWeights.load(each, filePath=os.path.join(userScriptDir, '%s.wts' % each))
        #override the mesh to see the new whiskers
        cmds.blendShape('rewireWhiskers_geo', 'dragon1Tech:c_body_tentacle_001_simCage_mid_postTech_geo', n='wire_correction_BSP', before = 1, w=(0, 1.0), o = "world")
        #override the whiskers with the dynamic ones
        cmds.blendShape('rt_Tentacle_HSM_DynCRV', 'R_whisker_crv', n='R_wire_correction_BSP', before = 1, w=(0, 1.0), o = "world")
        cmds.blendShape('lf_Tentacle_HSM_DynCRV', 'L_whisker_crv', n='L_wire_correction_BSP', before = 1, w=(0, 1.0), o = "world")
        #hide the new tentacle geo
        cmds.setAttr("rewireWhiskers_geo.visibility", 0)
        #load the blendmap for the tentacle geo
        userScriptDir = os.path.join(os.path.dirname("/jobs/vfx_cr/slm/slm4700/TASKS/techanim/maya/scenes/blendShape"), 'blendShape')
        bs = mc.ls(mc.listHistory('dragon1Tech:c_body_tentacle_001_simCage_mid_postTech_geo'), type='blendShape')
        for each in bs:
            if each =="wire_correction_BSP":
                mWeights.load(each, filePath=os.path.join(userScriptDir, '%s.wts' % each))
        #new rigid name and settings
        cmds.setAttr("hairCollider_rgdShape.pointMass", 20)
        cmds.setAttr("hairCollider_rgdShape.collisionLayer", 3)
        cmds.setAttr("rt_Tentacle_HSMShape.collisionLayer", 3)
        cmds.setAttr("lf_Tentacle_HSMShape.collisionLayer", 3)
        cmds.setAttr("lf_Tentacle_HSM_DynCRVShape.overrideDisplayType", 0)
        cmds.setAttr("rt_Tentacle_HSM_DynCRVShape.overrideDisplayType", 0)
        cmds.setAttr("lf_Tentacle_HSM_DynCRVShape.overrideColor", 17)
        cmds.setAttr("rt_Tentacle_HSM_DynCRVShape.overrideColor", 14)
        import maya.cmds as cmds
        from functools import partial
        from string import *
        import re
        import maya.mel
        import os, subprocess, sys, platform, logging, signal, webbrowser, urllib, re, getpass, datetime
        from os  import popen
        from sys import stdin
        import subprocess
        import os
        import random
        import glob
        from random import randint
        import operator
        from sys import argv
        from datetime import datetime
        from operator import itemgetter
        from inspect import getsourcefile
        from os.path import abspath
        OSplatform=platform.platform()
        import ast
        from numpy import arange
        selected = [
        'rt_Tentacle_HSMShape.txt',
        'lf_Tentacle_HSMShape.txt',
        'nahirTentacle_NCL.txt']
        folderType='/jobs/vfx_cr/COMMON/rig/dyn_att_presets/dragon_whiskers_loopy/'
        notAttr=["isHierarchicalConnection", "solverDisplay", "isHierarchicalNode", "publishedNodeInfo", "fieldScale_Position", "fieldScale", "fieldScale.fieldScale_Position"]
        for selItem in selected:
            each = selItem.split('.')[0]
            print each
            getfolder = folderType+selItem
            print getfolder
            List = open(getfolder).readlines()
            for aline in List:
                print aline
                attribute_container=[]
                getListedAttr=[(attrib) for attrib in cmds.listAttr(each, k=1, s=1, iu=1, u=1, lf=1, m=0) for item in notAttr if item not in attrib]
                if ">>" in aline:
                    getObj=aline.split('>>')[0]
                    getExistantInfo=aline.split('>>')[1]
                    if getExistantInfo!="\n":
                        findAtt=getExistantInfo.split("<")
                        for eachInfo in findAtt:
                            getAnimDicts=eachInfo.split(";")
                            for eachctrl in xrange(len(getAnimDicts) - 1):
                                current_item, next_item = getAnimDicts[eachctrl], getAnimDicts[eachctrl + 1]
                                gethis=ast.literal_eval(next_item)
                                print "changing: "+str(each)+"."+str(eachInfo)+" at "+str(gethis)
                                gethis=ast.literal_eval(next_item)
                                try:
                                    if len(gethis)<2:
                                        for key, value in gethis.items():
                                            for listeditem in getListedAttr:
                                                if current_item==listeditem:
                                                    cmds.setAttr(each+'.'+current_item, value)                                                
                                    else:
                                         for key, value in gethis.items():
                                            for listeditem in getListedAttr:
                                                if current_item==listeditem:
                                                    cmds.setKeyframe( each, t=key, at=current_item, v=value ) 
                                except:
                                    pass                                             
                    else:
                        pass
        getLowRange=cmds.playbackOptions(q=1, min=1)
        getNode=cmds.ls(type="nucleus")
        for each in getNode:
            cmds.setAttr(each+".startFrame", getLowRange)                       
 
 
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
            else:
                getTitle = getparentObj
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
            plusnum=random.uniform(0,20)
            newTransform = [transformWorldMatrix[0], transformWorldMatrix[1]+plusnum, transformWorldMatrix[2]]
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
            nameSpacerig = [(each) for each in cmds.ls("*:*") if cmds.nodeType(each) == "transform" and cmds.listRelatives(each, p=1) == None]
            normalrig = [(each) for each in cmds.ls("*") if cmds.nodeType(each) == "transform" and cmds.listRelatives(each, p=1) == None]
            rigs = nameSpacerig +normalrig
            for item in rigs:
                if cmds.listRelatives(item, ad=1, type="mesh"):
                    getparentObj=[(each) for each in cmds.listRelatives(item, ad=1, type="mesh")][0]
                    getvert=getparentObj+".vtx[0]"
                    collectedVtx.append(getvert)
            cmds.select(collectedVtx, r=1)
            self.annotations_list()             
        elif cmds.nodeType(cmds.ls(sl=1)[0]) == "transform":
            rigs = cmds.ls(sl=1)
            for item in rigs:
                if cmds.listRelatives(item, ad=1, type="mesh"):
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
 
    def rocket_fix(self):
        cmds.select("rocket1_c_body_hi_driverGeo", r=1)
        cmds.polyNormalPerVertex(ufn=1)
 
    def static_curves(self):
        inst_win = strand_Behaviour_Win()
        inst_win.show()       
        # import tech_hairUtils
        # tech_hairUtils.mkPostTechCurvesStatic()
 
 
    def rockets_face_fur_auto(self):
        selected = self.find_static_face_curves()
        cmds.select(selected, r=1)
        tech_hairUtils.mkPostTechCurvesStatic()
 
 
    def setup_preview_fur(self):
        getAnimGeo=cmds.ls("*animGeo")
        for item in getAnimGeo:
            cmds.setAttr(".ctrlVis", 0)
            cmds.setAttr(".res" , 4)
            cmds.setAttr(".jntVis", 0)
        getPalettes=cmds.ls(type='xgmPalette')
        if len(getPalettes) > 0:
            for eachItem in getPalettes:
                cmds.setAttr(eachItem+".visibility", 1)
                command='relationshipEditorBreakRelationship relationshipPanel1 displayLayers {"%s"};' % (eachItem)
                maya.mel.eval( command )   
                if cmds.listRelatives(eachItem, p=1) != None:
                    cmds.parent(eachItem, w=1)
        # self.break_connections()
        getAdditionals=[(each) for each in cmds.ls("*:*rocketChair*") if cmds.listRelatives(each, p=1) == None and cmds.nodeType(each) == "transform"]
        getAdditionals_more=[(each) for each in cmds.ls("*:*chairRocket*") if cmds.listRelatives(each, p=1) == None and cmds.nodeType(each) == "transform"]
        getAdditionals_more_seat=[(each) for each in cmds.ls("*:*seatbelt*") if cmds.listRelatives(each, p=1) == None and cmds.nodeType(each) == "transform"]
        cmds.setAttr("rocket1:c_slidersOffset_ctrl.lodVisibility", 0)
        cmds.setAttr("rocket1:c_mouthPatch_DNT_grp.lodVisibility", 0)
        try:
            cmds.setAttr("rocket1:c_face_controls_DNT_GRP.lodVisibility", 0)
        except:
            pass
        cmds.select(getAnimGeo, r=1)       
        selected = [
        'rocket1:animGeo',
        'shotcam1:camera']
        if len(getPalettes)>0:
            selected = selected + getPalettes        
        if len(getAdditionals)>0:
            selected = selected + getAdditionals
        if len(getAdditionals_more)>0:
            selected = selected + getAdditionals_more         
        if len(getAdditionals_more_seat)>0:
            selected = selected + getAdditionals_more_seat                    
        if cmds.objExists('rocket1Tech:simCurves_postTech_grp',):
            selected.append('rocket1Tech:simCurves_postTech_grp')
        for eachItem in selected:
            cmds.setAttr(eachItem+".visibility", 1)
        cmds.select(selected, r=1)
        focPane = [(each) for each in cmds.getPanel(vis=1) if "model" in each]
        for each in focPane:
            if cmds.modelEditor(each, q=1, av=1) == True:
                cmds.modelEditor(each, e=1, alo=0, nurbsCurves = 1, polymeshes = 1, imagePlane = 1, pluginShapes = 1)
        #         cmds.isolateSelect(focPane[0], state=1)
        # cmds.select(cl=1)
 
 
    def setup_collide_fur(self):
        bodyCollideMesh = 'rocket1Tech:c_bodySuit_simCage_hi_sim_geo'            
        cmds.duplicate(bodyCollideMesh, n='c_bodySuit_collide_hair_geo')
        cmds.select(['c_bodySuit_collide_hair_geo', 'rocket1_XPDarm_hairSysShape', 'rocket1_XPDhead_hairSysShape'], r=1)
        maya.mel.eval( "makeCollideNCloth;" )
        cmds.pickWalk(d='up')
        cmds.rename(cmds.ls(sl=1)[0], "hair_suit_collider_rgd")
        deformName='hair_body_collider_follow_BS'
        BlendShapeName=cmds.blendShape('rocket1Tech:c_bodySuit_simCage_hi_sim_geo', 'c_bodySuit_collide_hair_geo', n=deformName, w=(0, 1.0))      
 
 
    def Jesus_wrinkle_script(self):
        mc.select("rocket1Tech:c_bodySuit_simCage_hi_restShape_geo")
        mc.deformer(typ="morph", foc=False,name='preWrinklesMorph')
        Morph().load("preWrinklesMorph", '/jobs/vfx_marylou/abt/abt3080/TASKS/techanim/maya/scenes/morph/Wrinkles_C.morph')
        mc.setAttr("preWrinklesMorph.preWrinkles",0.5)       
 
    def find_static_face_curves(self):
        print "nothing here"
        return None
 
 
    def add_hairs_back_in(self):
        import tech_hairUtils
        for each in cmds.ls(sl=1):
            grabName=each.split(":")[-1]
            grabPart=grabName.split("_")[0]
            if grabPart == "whiskers":
                grabPart = "whisker"
            hairSys=[item for item in cmds.ls(type="hairSystem") if grabPart in item][0].split('Shape')[0]
            tech_hairUtils.mkPostTechCurvesDynamicAgain(postTechCurves=each,  hairSystem=hairSys)
            print "attempting to added "+getnew+" to "+hairSys       
 
 
    def hair_wires(self):
        dictionary_wires={"rocket1Tech:tail_simCurves_postTech_grp":31,
        "rocket1Tech:whiskers_simCurves_postTech_grp":4,
        "rocket1Tech:leg_simCurves_postTech_grp":30,
        "rocket1Tech:head_simCurves_postTech_grp":25,
        "rocket1Tech:arm_simCurves_postTech_grp": 23}
        for value, key in dictionary_wires.items():
            cmds.setAttr(value+".overrideEnabled", 1)
            cmds.setAttr(value+".overrideColor", key)         
 
    def motion_mult_item(self):
        import setup_MM_UI
        reload(setup_MM_UI)
        setup_MM_UI.origin_offset()
 
 
 
    def origin_multiplier_input(self, parent_root, Obj):
        cmds.select(Obj)
        buildCluster = cmds.cluster()
        cmds.rename(cmds.ls(sl=1)[0], parent_root+'_'+Obj+"_MM")
        createdCluster=cmds.ls(sl=1)[0]
        translate_MD_name=getSelected+'_'+Obj+'_trans_md'
        rotate_MD_name=getSelected+'_'+Obj+'_rot_md'
        get_md_trans_Node = cmds.shadingNode('multiplyDivide', n=translate_MD_name, asUtility=True)
        get_md_rot_Node = cmds.shadingNode('multiplyDivide', n=rotate_MD_name, asUtility=True)
        cmds.connectAttr(parent_root+".rotate", get_md_rot_Node+".input1")
        cmds.connectAttr(get_md_rot_Node+".output", createdCluster+".rotate")
        cmds.connectAttr(parent_root+".translate", get_md_trans_Node+".input1")
        cmds.connectAttr(get_md_trans_Node+".output", createdCluster+".translate")
        attrs = [".input2X", ".input2Y", ".input2Z"]
        for each in attrs:
            cmds.setAttr(get_md_trans_Node+each, -1)
            cmds.setAttr(rotate_MD_name+each, -1)
 
 
 
    def findGroom(self):    
        import xgenm as xg
        import xgenm.xgGlobal as xgg
        import xgenm.XgExternalAPI as xge
        palettes = xg.palettes()
        for palette in palettes:
            descriptions = xg.descriptions(palette)
            for description in descriptions:
                objects = xg.objects(palette, description, True)
                for object in objects:
                    attrs = xg.allAttrs(palette, description, object)
                    for attr in attrs:
                        if "custom_color_uvMap" in attr:
                            getVer = xg.getAttr(attr, palette, description, object)
                            #print " Attribute:" + attr + ", Value:" + xg.getAttr(attr, palette, description, object)
        if len(getVer)>0:           
            getFirst = getVer.split("Main/v")[1]
            findVerGroom = getFirst.split("/")[0]
        else:
            findVerGroom = "Anim's groom"
        return findVerGroom
 
    def print_pub_message(self):
        #mainRig=[(each) for each in mc.ls("*:*animGeo") if mc.listRelatives(each, p=1) ==None]
        # mainRig = [(each) for each in cmds.ls(type = "reference") if "cam" not in str(each)][0]
        mainRig=[(each) for each in mc.ls("*:*animGeo") if mc.listRelatives(each, p=1) ==None]
        for item in mainRig:
            comment = self.find_comment_for_asset(item)
            print comment
 
 
    def print_anim_message(self):
        comment = self.build_comment()
        print comment
 
    def build_comment(self):
        mainRig=[(each) for each in cmds.ls("*:*animGeo") if cmds.nodeType(each)=="transform" and cmds.listRelatives(each, p=1)==None and "rocket" in each][0]
        getRigVer= cmds.getAttr(mainRig+".version")
        getRef = [(each) for each in cmds.ls(type = "reference") if "rocket" in str(each)][0]
        getfileRef=cmds.referenceQuery( getRef, filename=True)
        cullpath=getfileRef.split("_")[-1]
        getAnimVer=cullpath.split(".mb")[0]    
        grabPathpart=getfileRef.split('lodagnostic')[0]
        get_preset = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(grabPathpart) for name in files if name.lower().endswith(".yaml")][0]
        List = open(get_preset).readlines()
        for aline in List:
            if "comment" in aline:
                animCmnt= aline.split("comment:")[-1]
                animCmntline= animCmnt.split('\n')[0]
        comment = "Techanim Export using Anim:'"+animCmntline+"' version "+ getAnimVer +", animRig version "+getRigVer          
        return comment
 
    def select_mesh_heirarchy(self):
        grabMesh = [(each) for each in mc.listRelatives(mc.ls(sl=1), ad=1, type="mesh") if "Orig" and "Deformed" not in each]
        mc.select(grabMesh, r=1)
 
    def blendSearch(self):
        selObj=cmds.ls(sl=1, fl=1)
        if len(selObj) == 2:
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
                                BlendShapeName=cmds.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", w=(0, 1.0), o = "world")
                            except:
                                pass
                        elif grabNameChild in grabNameParent:
                            print "blending: "+childItem+' to '+parentItem
                            try:
                                BlendShapeName=cmds.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", w=(0, 1.0), o = "world")
                            except:
                                pass
                        elif grabNameChild==grabNameParent:
                            print "blending: "+childItem+' to '+parentItem
                            try:
                                BlendShapeName=cmds.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", w=(0, 1.0),  o = "world")
                            except:
                                pass
        else:
            print "need to select two groups"
 
    def reconnSearch(self):
        selObj=cmds.ls(sl=1, fl=1)
        if len(selObj) == 2:       
            if selObj:
                pass
            else:
                print "must select a driver group and a driven group(same shortnames)"
                return
            selObj=cmds.ls(sl=1, fl=1)
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
                            print "connecting: "+childItem+' to '+parentItem
                            try:
                                cmds.connectAttr(parentItem+".outMesh", childItem+".inMesh", f=1)
                            except:
                                pass
                        elif grabNameChild in grabNameParent:
                            print "connecting: "+childItem+' to '+parentItem
                            try:
                                cmds.connectAttr(parentItem+".outMesh", childItem+".inMesh", f=1)
                            except:
                                pass
                        elif grabNameChild==grabNameParent:
                            print "connecting: "+childItem+' to '+parentItem
                            try:
                                cmds.connectAttr(parentItem+".outMesh", childItem+".inMesh", f=1)
                            except:
                                pass
        else:
            print "need to select two groups"
 
    def connSearch(self):
        selObj=cmds.ls(sl=1, fl=1)
        if len(selObj) == 2:       
            if selObj:
                pass
            else:
                print "must select a driver group and a driven group(same shortnames)"
                return
            selObj=cmds.ls(sl=1, fl=1)
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
                            print "connecting: "+childItem+' to '+parentItem
                            try:
                                cmds.connectAttr(parentItem+".outMesh", childItem+".inMesh", f=1)
                            except:
                                pass
                        elif grabNameChild in grabNameParent:
                            print "connecting: "+childItem+' to '+parentItem
                            try:
                                cmds.connectAttr(parentItem+".outMesh", childItem+".inMesh", f=1)
                            except:
                                pass
                        elif grabNameChild==grabNameParent:
                            print "connecting: "+childItem+' to '+parentItem
                            try:
                                cmds.connectAttr(parentItem+".outMesh", childItem+".inMesh", f=1)
                            except:
                                pass
        else:
            print "need to select two groups"
 
    def blendGroupToGroup(self):
        selObj=cmds.ls(sl=1, fl=1)
        if len(selObj) == 2:
            parentObj=selObj[0]
            childrenObj=selObj[1]
            getparentObj=cmds.listRelatives(parentObj, c=1)
            getchildObj=cmds.listRelatives(childrenObj, c=1)
            for parentItem, childItem in map(None, getparentObj,getchildObj):
                parentItemls=cmds.ls(parentItem)
                childItemls=cmds.ls(childItem)
                cmds.select(parentItemls)
                cmds.select(childItemls, add=1)
                defName=str(parentItem)+"_BShape"
                print defName
                cmds.blendShape(n=defName, w=(0, 1.0), o="world", af=1)
        else:
            print "need to select two groups"
 
    def blendMass(self):
        selObj=cmds.ls(sl=1, fl=1)
        if len(selObj) >1:
            for eachController, eachChild in map(None, selObj[::2], selObj[1::2]):
                parentItem=cmds.ls(eachController)
                childItem=cmds.ls(eachChild)
                cmds.select(parentItem)
                cmds.select(childItem, add=1)
                cmds.blendShape(n=str(parentItem[0])+"_BShape", w=(0, 1.0), o="world", af=1)
        else:
            print "need to select more than one thing"               
 
 
 
    def preroll(self):
        if mc.ls(sl=1):
            ns = mc.ls(sl=1)[0].split(':')[0]
            if ns[-4:] is 'Tech':
                ns = ns[:-4]
            tech_utils.setPreroll(ns, preroll=25, animFrame=mc.playbackOptions(q=1, min=1), velocity=True)
        else:
            print 'NOTHING SELECTED'
         
 
    def precision_setup(self):
        print "Setting the translate and mute on model_hi"
        translate = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz']
        for each in translate:
            cmds.setAttr("rocket1:char_rocket__model__hi"+each, 0)
            cmds.mute("rocket1:char_rocket__model__hi"+each)
        #set preroll
        print "Setting the preroll and rest pose"
        mainRig=[(each) for each in cmds.ls("*:*animGeo") if cmds.nodeType(each)=="transform" and cmds.listRelatives(each, p=1)==None][0]
        cmds.select(mainRig, r=1)
        cmds.playbackOptions(e=1, ast=wk_strt_value, min=wk_strt_value)
        cmds.currentTime(wk_strt_value)
        ns = mc.ls(sl=1)[0].split(':')[0]
        if ns[-4:] is 'Tech':
            ns = ns[:-4]
        tech_utils.setPreroll(ns, preroll=25, animFrame=mc.playbackOptions(q=1, min=1), velocity=True)
        #make tail into techgeo
        print "adding tail into techrig for pose"
        cmds.select("rocket1:c_tail_hi", r=1)
        getwin=promoteToTechUI.PromoteToTechUI()
        getwin.generateTechGeos(sim=False)
        #import ref pose
        print "Importing body at ref pose and blending"
        cmds.file(('/jobs/vfx_marylou/COMMON/rig/users/deglaue/orig_whole_exp.mb'), mnp=1, i=1)
        #blend the bind pose model into the pretech GEO for hair setup
        newBS = mc.blendShape('hairBind_body1', 'rocket1Tech:c_body_hi_preTech_geo', n= 'hairBind_PoseBS', w=(0, 1.0), o="world")
        #key the blend shape off after ref frame and set timeline on ref frame to prepare for hair sim build
        getTopRange=cmds.playbackOptions(q=1, min=1)+1
        getLowRange=cmds.playbackOptions(q=1, min=1)
        cmds.setKeyframe( 'hairBind_PoseBS', t=getLowRange, at='envelope', v=1.0 )
        cmds.setKeyframe( 'hairBind_PoseBS', t=getTopRange, at='envelope', v=0.0 )
        cmds.setAttr('hairBind_body1.visibility', 0)
        #import ref tail pose
        print "Importing tail at ref pose and blending"
        cmds.file(('/jobs/vfx_marylou/COMMON/rig/users/deglaue/tail_exp.mb'), mnp=1, i=1)
        #blend the bind pose model into the pretech GEO for hair setup
        newBS = mc.blendShape('hairBind_tail1', 'rocket1Tech:c_tail_hi_preTech_geo', n= 'hairBind_TailPoseBS', w=(0, 1.0), o="world")
        #key the blend shape off after ref frame and set timeline on ref frame to prepare for hair sim build
        cmds.setKeyframe( 'hairBind_TailPoseBS', t=getLowRange, at='envelope', v=1.0 )
        cmds.setKeyframe( 'hairBind_TailPoseBS', t=getTopRange, at='envelope', v=0.0 )
        cmds.setAttr('hairBind_tail1.visibility', 0)       
        print "Switching on Multiplier."
        cmds.setAttr ("rocket1Tech:techRig.main_motionMult_envelope", 1)
        cmds.setAttr ("rocket1Tech:techRig.main_motionMult_X", 1)
        cmds.setAttr ("rocket1Tech:techRig.main_motionMult_Y", 1)
        cmds.setAttr ("rocket1Tech:techRig.main_motionMult_Z", 1)
        cmds.currentTime(getLowRange)
        print "Done precision pre-setup for hair. Check the xgen start frame in the UI before hair setup to make sure it matches this new preroll setting"
 
 
 
    def abc_curves(self):
        currentShot=cmds.workspace(q=1, openWorkspace=1)
        currentdir=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        scriptPath=currentdir
        sys.path.insert(0, scriptPath)
        getScenePathWorkPath=cmds.file(q=1, location=1)
        filename_string=getScenePathWorkPath.split("scene")[0]
        cachefolderStart=filename_string+"cache/alembic"
        number=0000
        getScene=cmds.file(q=1, sn=1, shn=1)
        getFilename =  getScene.split(".")[:-1]
        getFilename='_'.join(getFilename)+"_"+str(M_USER)+"_abc_curves"
        getnewcachefolder=getFilename+"_"+str("%04d" % (number,))
        makecachefolder = cachefolderStart+"/"+getnewcachefolder
        if os.path.exists(makecachefolder):
            get_vr_folders = [(dirnames) for dirnames in os.walk(cachefolderStart)][0][1]
            get_top = max(get_vr_folders)
            number = get_top.split("_")[-1]
            number = int(number)
            number +=1
            getnewcachefolder=getFilename+"_"+str("%04d" % (number,))
            makecachefolder = cachefolderStart+"/"+getnewcachefolder
            os.makedirs(makecachefolder)
            print "created "+makecachefolder
        if not os.path.exists(makecachefolder):
            os.makedirs(makecachefolder)
            print "created "+makecachefolder
        xgenFx_animWire= xg_animWire.xgenAnimWire()
        getTopRange=cmds.playbackOptions(q=1, max=1)
        getLowRange=cmds.playbackOptions(q=1, min=1)
        actionList= [["rocket1_XPDarmPrimary","rocket1_XPDarmPrimary_sim_animWire"], ["rocket1_XPDwhisker","rocket1_XPDwhisker_sim_animWire"], ["rocket1_XPDheadPrimary","rocket1_XPDheadPrimary_sim_animWire"]]
        frameRange= [getLowRange,getTopRange]
        outDir = makecachefolder
        for each in actionList:
            description = each[0]
            fxName= each[1]
            outAbcPath= "%s/%s_%s.abc"%(outDir,description,fxName)
            xgenFx_animWire.cacheFxModule(description=description,fxName=fxName,frameRange= frameRange,abcFilePath=outAbcPath,exportAbc=True)
 
 
 
    def viewport(self):
        import maya.mel
        focPane = [(each) for each in mc.getPanel(vis=1) if "model" in each]
        for each in focPane:
            if mc.modelEditor(each, q=1, av=1) == True:
                maya.mel.eval('setRendererInModelPanel "vp2Renderer" {0}'.format(each))
 
    def set_end_frame_blur_fix(self):
        # M_USER = os.getenv("USER")
        # PROJECT=os.getenv("M_JOB")
        # SCENE=os.getenv("SEQUENCE_SHOT_")
        # SHOT=os.getenv("M_LEVEL")
        # sgVarFilePath = '/jobs/%s/%s/%s/TECH/lib/shotgun/setshot.d/sgvars' % (PROJECT, SCENE, SHOT)
        # if os.path.isfile(sgVarFilePath):
        #     # get available out values
        #     franges = {'WORK_IN': None, 'CUT_IN': None,
        #                'WORK_OUT': None, 'CUT_OUT': None}
        #     for line in open(sgVarFilePath, 'r'):
        #         if 'WORK_OUT' in line:
        #             wk_out_value = line.split('=')[-1].strip()
        #             try:
        #                 wk_out_value = int(wk_out_value)
        #             except:
        #                 wk_out_value = 0.0
        #                 cut_shouldbe_in_value = 0.0
        # else:
        #     wk_out_value = 0.0
        blurFix_endValue = wk_out_value+1
        mc.playbackOptions(aet=blurFix_endValue, max=blurFix_endValue)
 
 
    def post_shape_crv(self):
        parentItem=cmds.ls(sl=1)[0]
        childItem=cmds.ls(sl=1)[1]
        getStrtRange=cmds.playbackOptions(q=1, ast=1)
        getEndRange = getStrtRange+10
        off=0.0
        on=1.0
        BlendShapeName=cmds.blendShape(parentItem, childItem, n=str(parentItem)+"_bs", w=(0, 0.0))
        cmds.setKeyframe(str(parentItem)+"_bs", t=getStrtRange, at=parentItem, v=off ) 
        cmds.setKeyframe(str(parentItem)+"_bs", t=getEndRange, at=parentItem, v=on )        
 
 
    def clearCache(self):
        grabsystem = []
        if len(cmds.ls(sl=1)) <1:
            grabsystem=cmds.ls(type="hairSystem")
            print grabsystem
            if len(grabsystem) >0:
                pass
            else:
                grabsystem=cmds.ls(type="nCloth")
                print grabsystem
            if len(grabsystem) >0:
                pass
            else:
                grabsystem=cmds.ls(type="cacheFile")
                print grabsystem
        else:
            grabsystem = cmds.ls(sl=1)
            print grabsystem
        cmds.select(grabsystem, r=1)
        for each in grabsystem:
            getCache=[(nodes) for nodes in cmds.listHistory(each) if cmds.nodeType(nodes) == "cacheBlend"]
            if len(getCache)>0:
                cmds.delete(getCache)
                print "deleted cacheBlend on "+each
            getCache=[(nodes) for nodes in cmds.listHistory(each) if cmds.nodeType(nodes) == "cacheFile"]
            if len(getCache)>0:
                cmds.delete(getCache)
                print "deleted cacheFile on "+each        
 
    def check_groomVer(self):
        for p in sys.path:
            if 'maya_groom_tools' in p:
               version = re.findall('[0-9]+\.[0-9]+\.[0-9]+', p)
               if version:
                   print 'maya_groom_tools-{}'.format(version[0])       
 
 
    def fix_methpipe(self):
        os.environ['MANIM_DISABLE_PKG_MGR'] = '1'
        print "disabled pkg mgr"
 
    def blur_bookends(self):
        PROJECT=os.getenv("M_JOB")
        SCENE=os.getenv("SEQUENCE_SHOT_")
        SHOT=os.getenv("M_LEVEL")
        DEPT=os.getenv("M_TASK")
        sgVarFilePath = '/jobs/%s/%s/%s/TECH/lib/shotgun/setshot.d/sgvars' % (PROJECT, SCENE, SHOT)
        if os.path.isfile(sgVarFilePath):
            # get available in/out values
            franges = {'WORK_IN': None, 'CUT_IN': None,
                       'WORK_OUT': None, 'CUT_OUT': None}
            for line in open(sgVarFilePath, 'r'):
                if 'WORK_IN' in line:
                    wk_strt_value = line.split('=')[-1].strip()
                    try:
                        wk_strt_value = int(wk_strt_value)
                    except:
                        wk_strt_value = None
                if 'WORK_OUT' in line:
                    wk_out_value = line.split('=')[-1].strip()
                    try:
                        wk_out_value = int(wk_out_value)
                    except:
                        wk_out_value = None
        getSel = cmds.ls(sl=1)
        collect_mesh=[]
        if len(getSel)>0:
            getSel = [(each) for each in getSel if "postTech_hi_geo_grp" in each]
            if len(getSel)<1:
                print "no tech rigs selected"
                return
        else:
            getSel=[(each) for each in mc.ls("*:postTech_hi_geo_grp")]
            if len(getSel)<1:
                print "no rigs present"
                return
        strt_bsp = "StrtBlurExtend_"+str(wk_strt_value)+"BSP"
        strt_grp = "StrtBlurExtend_"+str(wk_strt_value)+"GRP"
        end_bsp = "EndBlurExtend_"+str(wk_out_value)+"BSP"
        end_grp = "EndBlurExtend_"+str(wk_out_value)+"GRP"
        childItemls = getSel
        cmds.currentTime(wk_out_value)
        checkstrt_exists = cmds.ls(strt_bsp)
        if len(checkstrt_exists)>0:
            cmds.delete(checkstrt_exists)
        checkend_exists = cmds.ls(end_bsp)
        if len(checkend_exists)>0:
            cmds.delete(checkend_exists)
        modelend_exists = cmds.ls(end_grp)
        if len(modelend_exists)>0:
            cmds.delete(modelend_exists)
        modelstrt_exists = cmds.ls(strt_grp)
        if len(modelstrt_exists)>0:
            cmds.delete(modelstrt_exists)
        parentItemls = cmds.duplicate(getSel, n=end_grp) 
        defName = end_bsp
        BlendShapeName=cmds.blendShape(parentItemls[0], childItemls, n=defName, w=(0, 1.0))
        cmds.setKeyframe(defName, t=wk_out_value, at=parentItemls[0], v=0.0 )
        cmds.setKeyframe(defName, t=wk_out_value+1, at=parentItemls[0], v=1.0 )
        cmds.setAttr(parentItemls[0]+".visibility", 0)
        cmds.currentTime(wk_strt_value)
        parentItemls = cmds.duplicate(getSel, n=strt_grp) 
        defName = strt_bsp
        BlendShapeName=cmds.blendShape(parentItemls[0], childItemls, n=defName, w=(0, 1.0))
        cmds.setKeyframe(defName, t=wk_strt_value, at=parentItemls[0], v=0.0 )
        cmds.setKeyframe(defName, t=wk_strt_value-1, at=parentItemls[0], v=1.0 )
        cmds.setKeyframe(defName, t=wk_strt_value-10, at=parentItemls[0], v=0.0 )
        cmds.setAttr(parentItemls[0]+".visibility", 0)
 
 
    def shrinkWrap_meshcut(self):
        shrinkWrap_for_meshcut = {".caching":False,
                                ".isHistoricallyInteresting":2,
                                ".nodeState":0,
                                ".frozen":False,
                                ".envelope":1.0,
                                ".fchild1": 0,
                                ".fchild2":0,
                                ".fchild3":0,
                                ".targetSmoothLevel":1,
                                ".innerGeom":None,
                                ".innerGroupId":0,
                                ".projection":4,
                                ".closestIfNoIntersection":True,
                                ".reverse":True,
                                ".bidirectional":True,
                                ".boundingBoxCenter":True,
                                ".axisReference":0,
                                ".alongX":False,
                                ".alongY":False,
                                ".alongZ":False,
                                ".offset":0.0,
                                ".targetInflation":0.02,
                                ".falloff":1.0,
                                ".falloffIterations":20,
                                ".shapePreservationEnable":True,
                                ".shapePreservationSteps":1,
                                ".shapePreservationIterations":7,
                                ".shapePreservationReprojection":0,
                                ".shapePreservationMethod":1}
        if len(cmds.ls(sl=1))==0:
            print "select one or two surfaces to either apply or change values of a shrinkwrap"
        elif len(cmds.ls(sl=1))==1:
            get_mesh = [(each_mesh) for each_mesh in cmds.listRelatives(cmds.ls(sl=1)[0], ad=1, type= "mesh") if "Orig" not in each_mesh]
            for each in get_mesh:
                getNode=[(nodes) for nodes in cmds.listHistory(each) if cmds.nodeType(nodes) == "shrinkWrap"]
        elif len(cmds.ls(sl=1))==2:
            get_mesh=[(each) for each in cmds.ls(sl=1) if cmds.nodeType(each) == "transform" and cmds.listRelatives(each, ad=1, type= "mesh")]  
            if len(get_mesh) == 2:
                getNode=cmds.deformer(cmds.ls(sl=1)[0], type="shrinkWrap")
                cmds.connectAttr(cmds.ls(sl=1)[1]+".worldMesh[0]", getNode[0]+".targetGeom", f=1)
            get_shape=[(each) for each in cmds.ls(sl=1) if cmds.nodeType(each) == "mesh"]
            if len(get_shape) == 2:
                getshapenode_one=cmds.listRelatives(cmds.ls(sl=1)[0], ap=1, type= "transform")
                getshapenode_two=cmds.listRelatives(cmds.ls(sl=1)[1], ap=1, type= "transform")
                getNode=cmds.deformer(getshapenode_one[0], type="shrinkWrap")
                cmds.connectAttr(getshapenode_two[0]+".worldMesh[0]", getNode[0]+".targetGeom", f=1)
            else:
                print "both transforms must be meshes or transforms of meshes"
        for key, value in shrinkWrap_for_meshcut.items():
            for getNode_item in getNode:
                try:
                    mc.setAttr(getNode_item+key, value)
                except:
                    print "cannot set: " + str(key) + " to "+ str(value)
 
    def fix_cam(self, arg=None):
        if len(cmds.ls(sl=1))==0:
            print "select something to focus cam on"
        elif len(cmds.ls(sl=1))>=1:
            focusedThing=cmds.ls(sl=1, fl=1)[0]
            focPane = [(each) for each in cmds.getPanel(vis=1) if "model" in each][0]
            command='postModelEditorSelectCamera "%s" "%s" 0' % (focPane, focPane)
            maya.mel.eval( command )  
            getOldCam=cmds.ls(sl=1, fl=1)[0]
            newcam=cmds.camera()
            cmds.select(newcam[0], r=1)
            cmds.select(getOldCam, add=1)
            getBaseClass.massTransfer()
            cmds.select(focusedThing, r=1)
            cmds.viewFit()
            cmds.delete(newcam[0])
 
    def wit_cam(self, arg=None):
        focusedThing=cmds.ls(sl=1, fl=1)[0]
        if cmds.nodeType(focusedThing)=="transform":
            focPane = [(each) for each in cmds.getPanel(vis=1) if "model" in each][0]
            command='postModelEditorSelectCamera "%s" "%s" 0' % (focPane, focPane)
            maya.mel.eval( command )  
            getOldCam=cmds.ls(sl=1, fl=1)[0]
            newcam=cmds.duplicate(getOldCam, n=focusedThing+"wit_cam")[0]
            command='lookThroughModelPanel "%s" "%s"' % (newcam, focPane)
            maya.mel.eval( command )       
        elif cmds.nodeType(focusedThing)=="mesh":
            command='rivet;'
            maya.mel.eval( command )
            locatorObj=cmds.ls(sl=1, fl=1)[0]
            focPane = [(each) for each in cmds.getPanel(vis=1) if "model" in each][0]
            command='postModelEditorSelectCamera "%s" "%s" 0' % (focPane, focPane)
            maya.mel.eval( command )  
            getOldCam=cmds.ls(sl=1, fl=1)[0]
            newcam=cmds.duplicate(getOldCam, n=focusedThing+"wit_cam")[0]
            cmds.parentConstraint(locatorObj,newcam, mo=1)
            command='lookThroughModelPanel "%s" "%s"' % (newcam, focPane)
            maya.mel.eval( command )
            cmds.setAttr(locatorObj+".visibility", 0)
 
    def turn_on_undo(self, arg=None):
        cmds.undoInfo(state=1)
 
 
    def optimize(self):
        command = ('unloadPlugin( "/sw/install/global/linux_x86_64_CentOS-7/autodesk/maya/2016.5.3276/payload/usr/autodesk/maya2016.5/plug-ins/bifrost/plug-ins/bifrostshellnode.so" );')
        maya.mel.eval(command)
        command = ('pluginInfo -edit -autoload false "/sw/install/global/linux_x86_64_CentOS-7/autodesk/maya/2016.5.3276/payload/usr/autodesk/maya2016.5/plug-ins/bifrost/plug-ins/bifrostvisplugin.so";')
        maya.mel.eval(command)
        command = ('pluginInfo -edit -autoload false "/sw/install/global/linux_x86_64_CentOS-7/autodesk/maya/2016.5.3276/payload/usr/autodesk/maya2016.5/plug-ins/bifrost/plug-ins/bifrostshellnode.so";')
        maya.mel.eval(command)
        print "disabled bifrost"    
        command = ('optionVar -iv enableSwatchRendering false;')
        maya.mel.eval(command)
        print "disabled swatches"
        command = ('pluginInfo -edit -autoload false "/sw/install/global/linux_x86_64_CentOS-7/autodesk/maya/2016.5.3276/payload/usr/autodesk/maya2016.5/plug-ins/MASH/plug-ins/MASH.so";')
        maya.mel.eval(command)  
        command = ('unloadPlugin( "/sw/install/global/linux_x86_64_CentOS-7/autodesk/maya/2016.5.3276/payload/usr/autodesk/maya2016.5/plug-ins/MASH/plug-ins/MASH.so" );')
        maya.mel.eval(command)
        print "diasabled MASH" 
        # command = ('optionVar -iv "interfaceScalingMode" 0;')
        # maya.mel.eval(command)
        # print "set swatches to 512"          
        # command = ('optionVar -iv prefSetSwatchMaxSize 512;')
        # maya.mel.eval(command)  
        # print "set swatches to 512"     
 
    def buildTemp_techanim(self):
        import promoteToTechUI
        pmt = promoteToTechUI.PromoteToTechUI()
        # CHANGE the name space to your instance NS + 'Tech'
        mainRig=[(each) for each in cmds.ls("*:*") if cmds.nodeType(each)=="transform" and cmds.listRelatives(each, p=1)==None and "cam" not in each][0]    
        pmt.techNamespace= mainRig.split(":")[0]+"Tech"
        pmt.createTechHi( ['preTech', 'tech', 'postTech', 'sim'], True)
 
    def locktorivet(self, arg=None):
        nuc=mc.ls(type="nucleus")[0]
        command='rivet;'
        maya.mel.eval( command )
        edges=mc.ls(sl=1, fl=1)
        fst_pc = mc.pointConstraint(edges, nuc, mo=0)
        loc=mc.spaceLocator(n="lcl_nuc_rvt")
        xcnd_pc = mc.pointConstraint(loc[0], nuc, mo=0)
        mc.setAttr(xcnd_pc[0]+"."+loc[0]+"W1", 0)
 
 
    def select_half(self):
        getfulllist=mc.ls(sl=1)
        random.shuffle(getfulllist)
        gethalflist=len(getfulllist)/2
        # print gethalflist
        nextList=[]
        for index, part in enumerate(getfulllist):
            if index in range(gethalflist):
                nextList.append(part)
        # print len(nextList)
        mc.select(nextList, r=1)
 
    def cln_curves(self):
        import maya.cmds as mc
        from maya_groom_tools.hair_tools.xgen_tools.xg_groom import xg_guide
        #xg_guide.Hair().fixFlipedCurves(boundGeo='',selection=None,**kw )
        #ags: lift : with True will pull curve out side otherwise only select and print information
        outCurves= xg_guide.Hair().fixFlipedCurves(boundGeo='c_body_mid',selection=mc.ls(sl=1),lift=True )
        mc.select(outCurves)       
 
    def kelpdragon_prosthetics(self):
        # import nSettings
        jobPath = os.environ['M_JOB_PATH']
        # nSettings path
        pathBase = '/jobs/vfx_volt/COMMON/rig/users/deglaue/nh0290/'
        nSettingsList = ['nucleus','nCloth','dynamicConstraint']
        # import sets
        pathFolder = ('/jobs/vfx_volt/COMMON/rig/users/deglaue/')
        #declare char
        animRigNS=[(each) for each in mc.ls("*:*animGeo") if mc.listRelatives(each, p=1) ==None][0]
        techRigNS = animRigNS.split(":")[0] + 'Tech'
        #set animal parts
        prosthetics = ["top", "bot", "tail"]
        #interrogate for existing pieces
        if cmds.objExists("c_fins_simCage_lo_sim_"+prosthetics[0]+"_geo"):
            print "this already exists"
        else:
            for each_piece in prosthetics:
                print "creating pieces for new cloth"
                mc.select(cl=1)
                get_fin=mc.ls("*:c_fins_simCage_lo_sim_geo")[0]
                mc.duplicate(get_fin, rr=1, n="c_fins_simCage_lo_sim_"+each_piece+"_geo")
                mc.select("c_fins_simCage_lo_sim_"+each_piece+"_geo", r=1)
                self.justCleanit()
                mc.select("c_fins_simCage_lo_sim_"+each_piece+"_geo")
                maya.mel.eval( 'nClothCreate;' )
                getCloth=mc.listRelatives(mc.ls(sl=1), p=1, type="transform")[0]
                mc.rename(getCloth, "c_fins_simCage_lo_sim_"+each_piece+"_nCloth")
                maya.mel.eval( 'assignNSolver "";')
                getnuc=[(each) for each in mc.listHistory("c_fins_simCage_lo_sim_"+each_piece+"_nClothShape", ac=1) if mc.nodeType(each) == "nucleus"][0]
                cmds.rename(getnuc, "c_fins_simCage_lo_sim_"+each_piece+"_ncl")
                mc.select("c_fins_simCage_lo_sim_"+each_piece+"_geo", r=1)    
                print "plugging in input mesh"       
                maya.mel.eval( 'displayNClothMesh "input";' )
                getinputHistory = [(each) for each in mc.listRelatives ("c_fins_simCage_lo_sim_"+each_piece+"_geo", ad=1, s=1) if "output" not in each]
                mc.select(mc.ls("*:c_fins_simCage_lo_preTech_geo")[0], r=1)              
                mc.select("c_fins_simCage_lo_sim_"+each_piece+"_geo", add=1)
                defName = "c_fins_simCage_lo_sim_"+each_piece+"_bsp" 
                mc.blendShape(n=defName, w=(0, 1.0))
                mc.select("c_fins_simCage_lo_sim_"+each_piece+"_geo", r=1)              
                maya.mel.eval( 'displayNClothMesh "current";' )
                print "init blendShape made for "+each_piece+" fins"
                bs_name="c_fin_"+each_piece+"_bsp"
                childItemls = mc.ls("c_fins_simCage_lo_sim_"+each_piece+"_geo")[0]
                parentItemls = mc.ls("*:c_fins_simCage_lo_postTech_geo")[0]
                BlendShapeName=mc.blendShape(childItemls, parentItemls, n=bs_name, w=(0, 1.0))
                print "output blendShape made for "+each_piece+" fins"
                userScriptDir = os.path.join(os.path.dirname("/jobs/vfx_volt/COMMON/rig/users/deglaue/nh0290/blendShape"), 'blendShape')
                bs="c_fin_"+each_piece+"_bsp"
                mWeights.load(bs, filePath=os.path.join(userScriptDir, '%s.wts' % bs))
                mc.parent("c_fins_simCage_lo_sim_"+each_piece+"_ncl", mc.ls('*:c_motionMul_out_grp')[0])
                mc.connectAttr("kelpie1Tech:techRig.startFrame","c_fins_simCage_lo_sim_"+each_piece+"_ncl.startFrame", f=1)
                mc.parent("c_fins_simCage_lo_sim_"+each_piece+"_nCloth", mc.ls('*:cloth_nNodes')[0])
                mc.setAttr("c_fins_simCage_lo_sim_"+each_piece+"_ncl.translateX",0)
                mc.setAttr("c_fins_simCage_lo_sim_"+each_piece+"_ncl.translateY",0)
                mc.setAttr("c_fins_simCage_lo_sim_"+each_piece+"_ncl.translateZ",0)
                mc.select(cl=1)
                get_coll=mc.ls("*:c_body_collTech_lo_coll_geo")[0]
                getnewcoll=mc.duplicate(get_coll, rr=1, n="c_body_collTech_lo_coll_"+each_piece+"_geo")
                bs_name="c_fin_"+each_piece+"_coll_bsp"
                childItemls = getnewcoll[0]
                parentItemls = get_coll
                mc.select(cl=1)
                get_coll=mc.ls("*:c_body_collTech_lo_coll_geo")[0]
                getnewcoll=mc.duplicate(get_coll, rr=1, n="c_body_collTech_lo_coll_"+each_piece+"_geo")
                mc.select(cl=1)      
                grabFileName="c_fins_simCage_lo_sim_"+each_piece+"_geo.vtx[0:1]_select.txt"
                printFolder=pathFolder+grabFileName   
                getBucket=[]
                List = open(printFolder).readlines()
                for aline in List:
                    if "," in aline:
                        getObj=aline.split(',')
                    else:
                        getObj=aline
                for item in getObj:
                    if item != "":
                        getBucket.append(item)
                mc.select(cl=1)
                mc.select(getBucket, r=1) 
                mc.select(getnewcoll, add=1)
                maya.mel.eval( 'createNConstraint pointToSurface 0;' )
                getdyn = mc.pickWalk(d="up")
                print getdyn
                #getdyn=mc.listRelatives(mc.ls(sl=1), p=1, type="transform")[0]
                mc.select(cl=1)
                cmds.rename(getdyn, "c_fins_simCage_lo_sim_"+each_piece+"_dnc")   
                getconstr="c_fins_simCage_lo_sim_"+each_piece+"_dnc"
                bs_name="c_fin_"+each_piece+"_coll_bsp"
                parentItemls = getnewcoll[0]
                childItemls = get_coll    
                BlendShapeName=mc.blendShape(childItemls, parentItemls, n=bs_name, w=(0, 1.0))
                mc.select(cl=1)
                mc.parent(getconstr,mc.ls('*:cloth_nNodes')[0])
                print "finished loading the constraints"
        bs="fingers_bsp"
        childItemls = mc.ls("*:c_fins_simCage_lo_sim_geo")[0]
        parentItemls = mc.ls("*:c_fins_simCage_lo_postTech_geo")[0]       
        BlendShapeName=mc.blendShape(childItemls, parentItemls, n=bs, w=(0, 1.0))
        mWeights.load(bs, filePath=os.path.join(userScriptDir, '%s.wts' % bs))               
        print "loading settings"
        for nSettings in nSettingsList:
            nObjectList = [f for f in os.listdir(pathBase+nSettings) if os.path.isfile(os.path.join(pathBase+nSettings, f))]
            # techRigNS = 'babyNifflersWalkTech'
            for nObject in nObjectList:
                obName = nObject.split('.')[0]
                if mc.objExists(techRigNS+':'+obName):
                    importFilePaths = pathBase + nSettings +'/' + nObject
                    if os.path.isfile(importFilePaths):
                        print 'importing: ' + importFilePaths
                        if nSettings == 'dynamicConstraint':
                            tu.import_nConstraint(importFilePaths, nameSpace=techRigNS)
                        else:
                            tu.import_nObjSettings(importFilePaths, nameSpace=techRigNS)
                    else:
                        mc.warning('file does not exist: ' + importFilePaths)
                else:
                    mc.warning(techRigNS+':'+obName + ' does not exist in your scene')
        print "set nucleus"
        # get_baseTools.initialize_strt_based_on_first()
        volAxis = cmds.volumeAxis(pos=[0, 0, 0], m=80, att=0, ia=0, afc=1, afx=1, arx=1, alx=2, drs=8, dx=0, dy=1, dz=0, trb=1, trs=1, tfx=.2, tfy=.2, tfz=.2, tox=0, toy=0, toz=0, dtr=0, mxd=190, vsh="cylinder", vof=[0, 0, 0], vsw=360, tsr=0.5)
        getGrav = cmds.gravity(pos=[0, 0, 0], m=20, att=0, dx=-1, dy=0, dz=0, mxd=1, vsh='none', vex=0, vof=[0, 0, 0], vsw=360, tsr=0.5)
        cmds.setKeyframe(volAxis[0], t="1021", at="trb", v=0)
        cmds.setKeyframe(volAxis[0], t="1039", at="trb", v=1)
        cmds.setKeyframe(volAxis[0], t="1104", at="drs", v=5)
        cmds.setKeyframe(volAxis[0], t="1111", at="drs", v=8)
        cmds.setKeyframe(getGrav[0], t="1026", at="magnitude", v=20 )
        cmds.setKeyframe(getGrav[0], t="1056", at="magnitude", v=0 )
        getClthGrp = cmds.ls(type="nCloth")
        cmds.select(getClthGrp, r=1)
        cmds.select("volumeAxisField1", add=1)
        maya.mel.eval("performDynamicsConnect 1;")
        print "created volumeAxis"
        print "finished"       
 
 
    def justCleanit(self):
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
            cmds.delete(each, ch=1)
            print "deleted history on "+each
            try:
                getShapes=cmds.listRelatives(each, c=1, typ="shape")
                for item in getShapes:
                    if "Orig" in item:
                        item=cmds.ls(item)
                        cmds.delete(item[0])
                        print "deleted "+item[0]
                    if "output" in item:
                        item=cmds.ls(item)
                        cmds.rename(item[0], each+"Shape")
                        print "renamed "+item[0]+" to "+each+"Shape"
                    if "_outputClothShape" in item:
                        item=cmds.ls(item)
                        cmds.delete(item[0])
                        print "deleted "+item[0] 
                    if "_geoShape1" in item:
                        item=cmds.ls(item)
                        cmds.delete(item[0])
                        print "deleted "+item[0]                       
            except:
                print "Object has no shapes. Passing on cleaning shapes."               
 
 
    def save_gamut(self, arg=None):
        self.saveSelection()
 
    def saveSelection(self, arg=None):
        getScenePath=cmds.file(q=1, location=1)
        getPathSplit=getScenePath.split("/")
        folderPath='\\'.join(getPathSplit[:-1])+"\\"
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
        objNameFile=str(newfolderPath)
        filebucket = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(objNameFile) for name in files if name.lower().endswith(".txt")]
        self.fileDropName=cmds.optionMenu( label='files')
        for each in filebucket:
            cmds.menuItem( label=each)       
        cmds.rowLayout  (' listBuildButtonLayout ', w=600, numberOfColumns=6, cw6=[350, 40, 40, 40, 40, 1], ct6=[ 'both', 'both', 'both',  'both', 'both', 'both'], p='bottomFrame')
        self.getName=cmds.textField(h=25, p='listBuildButtonLayout', text=objNameFile)
        cmds.button (label='Save', w=90, p='listBuildButtonLayout', command = lambda *args:self._save_select(fileName=cmds.textField(self.getName, q=1, text=1)))           
        cmds.button (label='Load', p='listBuildButtonLayout', command = lambda *args:self._load_selection(printFolder=cmds.textField(self.getName, q=1, text=1), grabFileName=cmds.optionMenu(self.fileDropName, q=1, v=1)))
        cmds.showWindow(window)
 
    def _save_select(self, fileName):  
        getgrp=cmds.ls(sl=1, fl=1)  
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        fileName=fileName+'_color.txt'
        print fileName
        inp=open(fileName, 'w+')
        # inp.write(str("colorDictionary = {"))
        cmds.hyperShade (getgrp[0], smn=1)
        for each in cmds.ls(sl = 1):
            print str(each)
            getval = cmds.getAttr(each+".color")
            # cmds.setAttr(each+".color", newval[0], newval[1], newval[2], type="double3")
            print str(getval)
            inp.write(str(each)+"|"+str(getval)+" , ")
        # inp.write(str("}"))
        inp.close()  
        print "saved as "+fileName
 
    def _load_selection(self, printFolder, grabFileName):
        import ast
        printFolder=grabFileName 
        if os.path.exists(printFolder):
            pass
        else:
            print printFolder+"does not exist"
            return
        getBucket=[]
        attribute_container=[]
        List = open(printFolder).readlines()
        create_dict = {}
        for aline in List:
            a_list = list(aline)
            a_list = aline.split(" , ")
        if len(a_list)>0:
            for each in a_list:
                listp1=each.split("|")
                if len(listp1)>1:
                    s = eval(str(listp1[1]))
            #         newdict = {dict[0]:dict[1]}
            #         create_dict.update(newdict)
            # print create_dict
            #     getObj=aline.split(':')[0]
            #     print getObj
            #     getColor=aline.split(':')[1]
            #     print getColor
                    cmds.setAttr(listp1[0]+".color", s[0][0],s[0][1], s[0][2], type="double3")
        else:
            print "can't parse"
 
 
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
 
    def _apply_wire_color(self):
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
 
    def create_rgb_window(self, winName="Colors"):
        winTitle = winName
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)
 
        self.window = cmds.window(winName, title=winTitle, tbm=1, w=300, h=100 )
 
        cmds.menuBarLayout(h=30)
        stringField=''''''
        self.fileMenu = cmds.menu( label='Help', hm=1, pmc=lambda *args:toolClass.helpWin(stringField))       
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=150)
 
        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        cmds.rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))
        self.colourmenu = cmds.optionMenu( label='Colors', w=150)
        cmds.menuItem( label='Apply' )#1
        cmds.menuItem( label='Grey' )#2
        cmds.menuItem( label='Red' )#3
        cmds.menuItem( label='Green' )#4
        cmds.menuItem( label='Blue' )#5
        cmds.menuItem( label='Teal' ) #6
        cmds.menuItem( label='Yellow' ) #7
        cmds.menuItem( label='Purple' ) #8
        cmds.menuItem( label='Random' ) #9
        cmds.menuItem( label='Dark' ) #9
        cmds.menuItem( label='Light' ) #9
        cmds.menuItem( label='slight grey' ) #9
        cmds.menuItem( label='save gamut' ) #9
        # command = lambda *args:self._save_select(fileName=cmds.textField(self.getName, q=1, text=1))) 
        cmds.button (label='Go', w=150, p='listBuildButtonLayout', command = lambda *args:self._change_colour()) 
        # cmds.button (label='Go', w=150, p='listBuildButtonLayout', command = self._change_colour)
        cmds.showWindow(self.window)
 
 
 
    def _change_colour(self):
        '''----------------------------------------------------------------------------------
        Common add to list function
        ----------------------------------------------------------------------------------''' 
        queryColor=cmds.optionMenu(self.colourmenu, q=1, sl=1)
        getSel=cmds.ls(sl=1)
        if queryColor==1:
            self._apply_colors()
        elif queryColor==2:
            self._change_primary_gry()
        elif queryColor==3:
            self._change_primary_red()
        elif queryColor==4:
            self._change_primary_grn()
        elif queryColor==5:
            self._change_primary_blue()
        elif queryColor==6:
            self._change_primary_teal()
        elif queryColor==7:
            self._change_primary_orange()
        elif queryColor==8:
            self._change_primary_prpl()
        elif queryColor==9:
            self._change_colors()
        elif queryColor==10:
            self._change_darker()
        elif queryColor==11:
            self._change_lighter()
        elif queryColor==12:
            self._slight_to_gry()           
        elif queryColor==13:
            self.save_gamut()           
        # for each in getSel:
        #     cmds.setAttr(each+".overrideEnabled", 1)
        #     cmds.setAttr(each+".overrideColor", color)   
 
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
 
    def _apply_grey_colors(self):
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
            getval = random.uniform(0.0,1.0)
            cmds.setAttr(name+".color", getval, getval, getval, type="double3")
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
 
    def _change_primary_gry(self):
        getgrp = cmds.ls(sl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        cmds.hyperShade (getgrp[0], smn=1)
        for each in cmds.ls(sl = 1):
            getval = random.uniform(0.0,1.0)
            cmds.setAttr(each+".color", getval, getval, getval, type="double3")
        cmds.select(getgrp, r=1)   
 
    def _slight_to_gry(self):
        getgrp = cmds.ls(sl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        cmds.hyperShade (getgrp[0], smn=1)
        for each in cmds.ls(sl = 1):
            getval = cmds.getAttr(each+".color")
            getvallow = random.uniform(getval[0][0],getval[0][2])
            cmds.setAttr(each+".color", getvallow, getvallow, getvallow, type="double3")
        cmds.select(getgrp, r=1)
 
 
    def _change_primary_grn(self):
        getgrp = cmds.ls(sl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        cmds.hyperShade (getgrp[0], smn=1)
        for each in cmds.ls(sl = 1):
            getval = random.uniform(0.0,1.0)
            getvallow = random.uniform(0.0,0.25)
            cmds.setAttr(each+".color", getvallow, getval, getvallow, type="double3")
        cmds.select(getgrp, r=1)    
 
 
    def _change_primary_red(self):
        getgrp = cmds.ls(sl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        cmds.hyperShade (getgrp[0], smn=1)
        for each in cmds.ls(sl = 1):
            getvallow = random.uniform(0.0,0.25)
            getval = random.uniform(0.0,1.0)
            cmds.setAttr(each+".color", getval, getvallow, getvallow, type="double3")
        cmds.select(getgrp, r=1)    
 
 
    def _change_primary_blue(self):
        getgrp = cmds.ls(sl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        cmds.hyperShade (getgrp[0], smn=1)
        for each in cmds.ls(sl = 1):
            getvallow = random.uniform(0.0,0.25)
            getval = random.uniform(0.0,1.0)
            cmds.setAttr(each+".color", getvallow, getvallow, getval, type="double3")
        cmds.select(getgrp, r=1)    
 
    def _change_primary_teal(self):
        getgrp = cmds.ls(sl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        cmds.hyperShade (getgrp[0], smn=1)
        for each in cmds.ls(sl = 1):
            getvallow = random.uniform(0.0,0.25)
            getval = random.uniform(0.0,1.0)
            cmds.setAttr(each+".color", getvallow, getval, getval, type="double3")
        cmds.select(getgrp, r=1)
 
    def _change_primary_orange(self):
        getgrp = cmds.ls(sl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        cmds.hyperShade (getgrp[0], smn=1)
        for each in cmds.ls(sl = 1):
            getvallow = random.uniform(0.0,0.25)
            getval = random.uniform(0.0,1.0)
            cmds.setAttr(each+".color", getval, getval, getvallow, type="double3")
        cmds.select(getgrp, r=1)
 
    def _change_primary_prpl(self):
        getgrp = cmds.ls(sl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        cmds.hyperShade (getgrp[0], smn=1)
        for each in cmds.ls(sl = 1):
            getvallow = random.uniform(0.0,0.25)
            getval = random.uniform(0.0,1.0)
            cmds.setAttr(each+".color", getval, getvallow, getval, type="double3")
        cmds.select(getgrp, r=1)
 
    def _change_darker(self):
        getgrp = cmds.ls(sl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        cmds.hyperShade (getgrp[0], smn=1)
        for each in cmds.ls(sl = 1):
            getval = cmds.getAttr(each+".color")
            getvallow = random.uniform(0.0,0.25)
            newval = getval[0][0]-getvallow, getval[0][1]-getvallow, getval[0][2]-getvallow
            cmds.setAttr(each+".color", newval[0], newval[1], newval[2], type="double3")
        cmds.select(getgrp, r=1)
 
    def _change_lighter(self):
        getgrp = cmds.ls(sl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        cmds.hyperShade (getgrp[0], smn=1)
        for each in cmds.ls(sl = 1):
            getval = cmds.getAttr(each+".color")
            getvallow = random.uniform(0.0,0.25)
            newval = getval[0][0]+getvallow, getval[0][1]+getvallow, getval[0][2]+getvallow
            cmds.setAttr(each+".color", newval[0], newval[1], newval[2], type="double3")
        cmds.select(getgrp, r=1)
 
    def _change_grey(self):
        getgrp = cmds.ls(sl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        cmds.hyperShade (getgrp[0], smn=1)
        for each in cmds.ls(sl = 1):
            getval = random.uniform(0.0,1.0)
            cmds.setAttr(each+".color", getval, getval, getval, type="double3")
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
 
 
    def build_a_curve(self):
        # getTopOpenGuides=cmds.ls(sl=1, fl=1)
        if len(cmds.ls(sl=1))<1:
            print "need to select some verts"
            return
        getSelectPref = cmds.selectPref(q=1, tso=1)
        if getSelectPref == False:
            cmds.selectPref(tso=1)
            getTopOpenGuides = cmds.ls(os=1, fl=1)
        else:
            getTopOpenGuides = cmds.ls(os=1, fl=1)       
        if len(getTopOpenGuides)>3:
            get_crv = self.build_a_curve_callup(getTopOpenGuides)
        else:
            get_crv = self.build_a_curve_short_callup(getTopOpenGuides)
        cmds.select(get_crv, r=1)
 
 
    def build_a_curve_callup(self, selectedObjects):
        values=[]
        for each in selectedObjects:#get point values to build curve
            # transformWorldMatrix = cmds.xform(each, q=True, wd=1, t=True)
            transformWorldMatrix=pm.PyNode(each).getPosition()
            values.append(transformWorldMatrix)
        get_crv = cmds.curve(n=selectedObjects[0]+"_crv", d=3, p=values)      
        return get_crv
 
 
    def build_a_curve_short_callup(self, selectedObjects):
        values=[]
        for each in selectedObjects:#get point values to build curve
            # transformWorldMatrix = cmds.xform(each, q=True, wd=1, t=True)
            transformWorldMatrix=pm.PyNode(each).getPosition()
            values.append(transformWorldMatrix)
        values.append(transformWorldMatrix)
        values.append(transformWorldMatrix)
        get_crv = cmds.curve(n=selectedObjects[0]+"_crv", d=3, p=values)
        cmds.rebuildCurve(get_crv, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=7, d=3, tol=0.01)
        cmds.rebuildCurve(get_crv, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=7, d=3, tol=0.01)
        return get_crv
 
 
 
    def wirewrap(self):
        # getshapenode_one=[(each) for each in cmds.ls(sl=1) if cmds.nodeType(cmds.listRelatives(each, ad=1)) == "mesh"]
        getshapenode_one=[(each) for each in cmds.ls(sl=1) if cmds.listRelatives(each, c=1, s=1)]
        # getshapenode_two=[(each) for each in cmds.ls(sl=1) if cmds.nodeType(cmds.listRelatives(each, c=1)) == "nurbsCurve"]
        getshapenode_two=[(each) for each in cmds.ls(sl=1) if cmds.listRelatives(each, c=1, type = "nurbsCurve")]
        # getNode=cmds.deformer(getshapenode_one[0], type="wire")
        cmds.wire(getshapenode_one[0], gw=0, en=1.000000, ce=0.000000, li=0.000000, w=getshapenode_two[0], dds=[(0, 20)])
        # cmds.connectAttr(getshapenode_two[0]+".worldSpace[0]", getNode[0]+".deformedWire[0]", f=1)
        # cmds.setAttr(getNode[0]+".dropoffDistance[0]", 50)
        cmds.pickWalk(getshapenode_one, d="up")
        cmds.pickWalk(getshapenode_one, d="up")
        cmds.pickWalk(getshapenode_one, d="up")
        cmds.setAttr(cmds.ls(sl=1)[0]+".visibility", 0)
 
    def fastwire(self):
        if len(cmds.ls(sl=1))<1:
            print "need to select some verts"
            return
        getObj = cmds.ls(sl=1)[0].split(".")[0]
        self.build_a_curve()
        getCrv = cmds.ls(sl=1)[0]
        cmds.select([getObj, getCrv])
        self.wirewrap()
                 
    def build_a_cloth_short_callup(self):
        if len(cmds.ls(sl=1))<1:
            print "need to select some verts"
            return
        getObj = cmds.ls(sl=1)[0].split(".")[0]
        self.build_a_curve()
        getCrv=cmds.ls(sl=1)
        cmds.select([getObj, getCrv[0]], r =1)
        getshapenode_one=[(each) for each in cmds.ls(sl=1) if cmds.listRelatives(each, c=1, s=1)]
        getshapenode_two=[(each) for each in cmds.ls(sl=1) if cmds.listRelatives(each, c=1, type = "nurbsCurve")]  
        selfU=cmds.textField(text="12")
        selfV=cmds.textField(text="1")
        cmds.nurbsToPolygonsPref(un=selfU, vn=selfV)
        getIt=cmds.ls("extCurve")
        if len(getIt)<1:
            name = "extCurve"
            xCubeMake=cmds.curve(n=name, d=1, p =[(-1.0, 0.0, 0.0), (-.5, 0.0, 0.0),(0.0, 0.0, 0.0), (.5, 0.0, 0.0), (1.0, 0.0, 0.0)])
        else:
            name=cmds.ls("extCurve")[0] 
        cmds.extrude(xCubeMake, getshapenode_two, ch=1, rn=0, po=1, et=1, ucp=1, fpt=1, upn=1, rotation=0, scale=1, rsp=1)
        getStrip = cmds.ls(sl=1)
        cmds.select(getObj, r=1)
        cmds.select(getStrip[0], add=1)
        cmds.CreateWrap()
 
    def map_select_transfer(self):
        #select surrounding object verts
        # from numpy import arange     
        selObj=cmds.ls(sl=1, fl=1)
        if selObj:
            if len(selObj)<2:
                print "select a group of verts and an object or two objects near eachother."
                return
            else:
                pass         
            result = cmds.promptDialog(
                title='Confirm',
                message='Falloff:',
                button=['Continue','Cancel'],
                defaultButton='Continue',
                cancelButton='Cancel',
                dismissString='Cancel' )
            if result == 'Continue':
                falloff_amt = cmds.promptDialog(query=True, text=True)
                falloff_amt = float(falloff_amt)
            else:
                print "selection transfer cancelled"
                return   
        else:
            print "select a group of verts and an object or two objects near eachother."
            return
        cmds.select(selObj[0])
        if ".v" in selObj[0]:
            getFirstGrp = selObj[0].split(".")[0]
            getobjOneVerts=[(each) for each in selObj if each.split(".")[0]==getFirstGrp]
            getSecondGrp=[(each) for each in selObj if each.split(".")[0]!=getFirstGrp]
        else:
            getFirstGrp = selObj[0]
            cmds.ConvertSelectionToVertices()
            getobjOneVerts=cmds.ls(sl=1, fl=1)
            getSecondGrp=[(each) for each in selObj if each != getFirstGrp]
        cmds.select(getSecondGrp)
        cmds.ConvertSelectionToVertices()
        getobjTwoVerts=cmds.ls(sl=1, fl=1)
        cmds.select(cl=1)
        getvert=[]
        for eachone in getobjOneVerts:
            objpos = cmds.xform(eachone, q=1, ws=1, t=1)
            buildCube = cmds.polyCube(d=falloff_amt, h=falloff_amt, w=falloff_amt)
            cmds.move(objpos[0],objpos[1], objpos[2], buildCube[0])
            bb = mc.xform(buildCube[0], q=True, bb=True)
            for eachtwo in getobjTwoVerts:
                objpos2 = cmds.xform(eachtwo, q=1, ws=1, t=1)
                getit = (objpos2[0] > bb[0] and objpos2[0] < bb[3] and objpos2[1] > bb[1] and objpos2[1] < bb[4] and objpos2[2] > bb[2] and objpos2[2] < bb[5])
                if getit == True:
                    getvert.append(eachtwo)
            cmds.delete(buildCube[0])
        cmds.select(getvert, r=1)
 
    def sim_vis(self):
        getall_postT = mc.ls("*:*sim")
        if len(getall_postT)>0:
            for each in getall_postT:
                try:
                    get_val_active = mc.getAttr(each+".visibility")
                    if get_val_active == 1:
                        print each+ " is already visibile. skipping."
                        pass
                    else:
                        mc.setAttr(each+".visibility", 1)
                        print each + " is now visibile"
                except:
                    pass
        getall_preT = mc.ls("*:*preTech")
        if len(getall_preT)>0:
            for each in getall_preT:
                try:
                    get_val_active = mc.getAttr(each+".visibility")
                    if get_val_active == 0:
                        print each+ " is already invisibile. skipping."
                        pass
                    else:
                        mc.setAttr(each+".visibility", 0)
                        print each + " is now invisibile"
                except:
                    pass
        getall_rig = mc.ls("*:*postTech")
        if len(getall_rig)>0:
            for each in getall_rig:
                try:
                    get_val_active = mc.getAttr(each+".visibility")
                    if get_val_active == 0:
                        print each+ " is already invisibile. skipping."
                        pass
                    else:
                        mc.setAttr(each+".visibility", 0)
                        print each + " is now invisibile"
                except:
                    pass                    
        getall_rig = mc.ls("*:animGeo")
        if len(getall_rig)>0:
            for each in getall_rig:
                try:
                    get_val_active = mc.getAttr(each+".visibility")
                    if get_val_active == 0:
                        print each+ " is already invisibile. skipping."
                        pass
                    else:
                        mc.setAttr(each+".visibility", 0)
                        print each + " is now invisibile"
                except:
                    pass       
 
    def anim_vis(self):
        getall_postT = mc.ls("*:animGeo")
        if len(getall_postT)>0:
            for each in getall_postT:
                try:
                    get_val_active = mc.getAttr(each+".visibility")
                    if get_val_active == 1:
                        print each+ " is already visibile. skipping."
                        pass
                    else:
                        mc.setAttr(each+".visibility", 1)
                        print each + " is now visibile"
                except:
                    pass
        getall_preT = mc.ls("*:*preTech")
        if len(getall_preT)>0:
            for each in getall_preT:
                try:
                    get_val_active = mc.getAttr(each+".visibility")
                    if get_val_active == 0:
                        print each+ " is already invisibile. skipping."
                        pass
                    else:
                        mc.setAttr(each+".visibility", 0)
                        print each + " is now invisibile"
                except:
                    pass
        getall_rig = mc.ls("*:*postTech")
        if len(getall_rig)>0:
            for each in getall_rig:
                try:
                    get_val_active = mc.getAttr(each+".visibility")
                    if get_val_active == 0:
                        print each+ " is already invisibile. skipping."
                        pass
                    else:
                        mc.setAttr(each+".visibility", 0)
                        print each + " is now invisibile"
                except:
                    pass                    
        getall_rig = mc.ls("*:*sim")
        if len(getall_rig)>0:
            for each in getall_rig:
                try:
                    get_val_active = mc.getAttr(each+".visibility")
                    if get_val_active == 0:
                        print each+ " is already invisibile. skipping."
                        pass
                    else:
                        mc.setAttr(each+".visibility", 0)
                        print each + " is now invisibile"
                except:
                    pass                    
 
 
    def postTech_vis(self):
        getall_postT = mc.ls("*:*postTech")
        if len(getall_postT)>0:
            for each in getall_postT:
                try:
                    get_val_active = mc.getAttr(each+".visibility")
                    if get_val_active == 1:
                        print each+ " is already visibile. skipping."
                        pass
                    else:
                        mc.setAttr(each+".visibility", 1)
                        print each + " is now visibile"
                except:
                    pass
        getall_preT = mc.ls("*:*preTech")
        if len(getall_preT)>0:
            for each in getall_preT:
                try:
                    get_val_active = mc.getAttr(each+".visibility")
                    if get_val_active == 0:
                        print each+ " is already invisibile. skipping."
                        pass
                    else:
                        mc.setAttr(each+".visibility", 0)
                        print each + " is now invisibile"
                except:
                    pass
        getall_rig = mc.ls("*:*animGeo")
        if len(getall_rig)>0:
            for each in getall_rig:
                try:
                    get_val_active = mc.getAttr(each+".visibility")
                    if get_val_active == 0:
                        print each+ " is already invisibile. skipping."
                        pass
                    else:
                        mc.setAttr(each+".visibility", 0)
                        print each + " is now invisibile"
                except:
                    pass                    
        getall_rig = mc.ls("*:*sim")
        if len(getall_rig)>0:
            for each in getall_rig:
                try:
                    get_val_active = mc.getAttr(each+".visibility")
                    if get_val_active == 0:
                        print each+ " is already invisibile. skipping."
                        pass
                    else:
                        mc.setAttr(each+".visibility", 0)
                        print each + " is now invisibile"
                except:
                    pass      
 
    def turn_on_nuc(self):
        getall_technuc = mc.ls("*:techRig")
        if len(getall_technuc)>0:
            for each in getall_technuc:
                try:
                    get_val_active = mc.getAttr(each+".Nucleus")
                    if get_val_active == 1:
                        print each+ ".Nucleus is already active. skipping."
                        pass
                    else:
                        mc.setAttr(each+".Nucleus", 1)
                        print each + " is now active"
                except:
                    pass
        getall_nuc = mc.ls(type = "nucleus")
        if len(getall_nuc)>0:
            for each in getall_nuc:
                get_val_active = mc.getAttr(each+".enable")
                if get_val_active == 1:
                    print each+ ".enable is already active. skipping."
                    pass
                else:
                    mc.setAttr(each+".enable", 1)
                    print each + " is now active"      
 
    def fixcam_attr(self):            
        print "attempting to set cam" 
        try:
            cmds.disconnectAttr ("*:camera_plate_2_depth.output", "*:camera.plate_2_depth")
        except:
            pass
        try:
            cmds.disconnectAttr ("*:camera_plate_1_depth.output", "*:camera.plate_1_depth")
        except:
            pass
        cmds.setAttr( "*:camera.plate_1_depth",  1000)
        cmds.setAttr( "*:camera.plate_2_depth",  10)
        try:
            cmds.disconnectAttr('*:camera_plateSelection.output', '*:camera.plateSelection')
        except:
            pass
        cmds.setAttr( "*:camera.plateSelection", 3)    
        try: 
            cmds.setAttr( "*:camera.platePath_2_lo", "/jobs/vfx_1224/hol/hol1650/PRODUCTS/images/elements/hol1650_comp_cgfg_v0002/2kaxp_acescg_png/hol1650_comp_cgfg_v0002-2kaxp_acescg.%04d.png", type = "string")
        except:
            print "may have to manually enter plate into foreground"
        print "set cam done"
 
    def percentage_preview(self):
        import xgenm as xg
        import xgenm.xgGlobal as xgg
        import xgenm.XgExternalAPI as xge
        if xgg.Maya:
            #palette is collection, use palettes to get collections first.
            palettes = xg.palettes()
            for palette in palettes: 
                #Use descriptions to get description of each collection
                descriptions = xg.descriptions(palette)
                for description in descriptions:
                    objects = xg.objects(palette, description, True)
                    #Get active objects,e.g. SplinePrimtives
                    for object in objects:
                        attrs = xg.allAttrs(palette, description, object)
                        for attr in attrs:
                            if "percent" in attr:      
                                createStr =  str(" Attribute:" + attr + ", Value:" + xg.getAttr(attr, palette, description, object))
                                xg.setAttr('percent', '100', palette, description, object)
                            if "inCameraOnly" in attr:     
                                xg.setAttr('inCameraOnly', 'false', palette, description, object)                               
 
    def setframerange(self):
        #set framerange for extra frame blur
        PROJECT=os.getenv("M_JOB")
        SCENE=os.getenv("SEQUENCE_SHOT_")
        SHOT=os.getenv("M_LEVEL")
        try:
            sgVarFilePath = '/jobs/%s/%s/%s/TECH/lib/shotgun/setshot.d/sgvars' % (PROJECT, SCENE, SHOT)
            if os.path.isfile(sgVarFilePath):
                # get available in/out values
                franges = {'WORK_IN': None, 'CUT_IN': None,
                           'WORK_OUT': None, 'CUT_OUT': None}
                for line in open(sgVarFilePath, 'r'):
                    if 'WORK_OUT' in line:
                        wk_out_value = line.split('=')[-1].strip()
                        try:
                            wk_out_value = int(wk_out_value)
                        except:
                            wk_out_value = None
            getHiRange=cmds.playbackOptions(max=wk_out_value+1)  
            print "set frame range end"
        except:
            print "can't find SG range"
