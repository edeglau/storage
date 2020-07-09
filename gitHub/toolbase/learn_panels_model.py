from toolbase.cache_stuff import wk_strt_value
import os, sys, subprocess
import maya.cmds as mc
import maya.mel
from sys import argv
import collections

import PyQt4
from PyQt4 import QtCore, QtGui, Qt
from PyQt4.QtGui import QWidget, QRadioButton, QGridLayout, QLabel, \
    QTableWidget, QComboBox, QKeySequence, QToolButton, QPlainTextEdit, QPushButton,QBoxLayout, \
    QClipboard, QTableWidgetItem, QCheckBox, QVBoxLayout, QHBoxLayout, \
    QPixmap, QLineEdit, QListWidget, QTextEdit, QSizePolicy, QFrame, QPalette, QColor, \
    QFont, QAbstractItemView, QMenu, QMessageBox
from PyQt4.QtCore import SIGNAL
from Cython.Utility.MemoryView import item

class prvw_UI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(prvw_UI, self).__init__(parent = None)
 
        self.setWindowTitle("Preview setups")
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
        self.duplct_order_layout = QtWidgets.QHBoxLayout()
        self.myform.addRow(self.duplct_order_layout)
        self.dup_layout = QtWidgets.QVBoxLayout()
        self.duplct_order_layout.addLayout(self.dup_layout)
        self.duplct_slid_layout = QtWidgets.QVBoxLayout()
        self.duplct_order_layout.addLayout(self.duplct_slid_layout)  
        self.duplct_slider_layout = QtWidgets.QVBoxLayout()    
        self.duplct_slid_layout.addLayout(self.duplct_slider_layout)  
        
        self.lbl_substp = QtWidgets.QLabel("playback substep")
        self.dup_layout.addWidget(self.duplctlbl_substp_nm_obj_button)
        self.substp_amnt = QtWidgets.QLineEdit("1.0")
        self.dup_layout.addWidget(self.substp_amnt)
        
        self.duplct_nm_obj_button = QtWidgets.QPushButton("blast")
        self.connect(self.duplct_nm_obj_button, SIGNAL("clicked()"),
                    lambda: self.print_dups())
        self.dup_layout.addWidget(self.duplct_nm_obj_button)
        
        self.duplct_sl_obj_button = QtWidgets.QPushButton("Mem blast")
        self.connect(self.duplct_sl_obj_button, SIGNAL("clicked()"),
                    lambda: self.select_dups())
        self.dup_layout.addWidget(self.duplct_sl_obj_button) 
        
        self.duplct_rnm_button = QtWidgets.QPushButton("Mem Blast No Roll")
        self.connect(self.duplct_rnm_button, SIGNAL("clicked()"),
                    lambda: self.rename_dups())
        self.dup_layout.addWidget(self.duplct_rnm_button) 
        
    def lights_cam(self):
        if mc.objExists("*:camlight_loc"):
            print "cam lights already exist - won't import"
            pass
        else:
            try:
                getCameraGrp=mc.ls("*:*.cameraPreset")
                getNode=str(pm.PyNode(getCameraGrp[0]).node())
                getCam=[each for each in mc.listRelatives(getNode, ad=1) if mc.nodeType(each) =="camera"]
                gettransformCam=[each for each in mc.listRelatives(getCam[0], p=1) if mc.nodeType(each) =="transform"][0]
                getLocCam=mc.ls('cam_light_loc*:camlight_loc')[0]
                mc.select(gettransformCam, r=1)
                mc.select(getLocCam, add=1)
                print mc.ls(sl=1)
                self._transfer_anim_attr()
            except:
                pass
            getcamlightPath='/sw/dev/deglaue/cam_light_loc.mb'
            namer='cam_light_loc'
            mc.file(getcamlightPath, i=1, type="mayaBinary", ignoreVersion=1, ra=True, mergeNamespacesOnClash=False, namespace=n
                    
    def blast_def(self):
        fps_set = float(str(self.fps_fieldText.text()))
        mc.playbackOptions(fps = fps_set, e=1)
        strt_rng = mc.playbackOptions(q=1, min=1)
        end_rng = mc.playbackOptions(q=1, max=1)
        focPane = [(each) for each in mc.getPanel(vis=1) if "model" in each]
        for each in focPane:
            if mc.modelEditor(each, q=1, av=1) == True:
                mc.modelEditor(each, e=1, rnm = "base_OpenGL_Renderer")     
        folder_strt = '/'.join(mc.file(q=1, location=1).split('/')[:-5])
        scn_name=str(mc.file(q=1, location=1)).split('/')[-1].split(".")[0]
        gotten_name=str(mc.file(q=1, location=1)).split('/')[-1].split(".")[0]+"-playblast-half1712x903_vdf8"
        gotten_path = "{}/PRODUCTS/images/{}/{}/playblast-half1712x903_vdf8_jpg/{}".format(folder_strt, _dept_task, scn_name, gotten_name)
        sel_NumMn=mc.playbackOptions(q=1, min=1)
        sel_NumMn_reset=mc.playbackOptions(q=1, min=1)+1    
        mc.currentTime(sel_NumMn)
        mc.currentTime(sel_NumMn_reset)        
        mc.currentTime(sel_NumMn)
        mc.playblast(format="image", filename=gotten_path, sequenceTime=0, clearCache=1, viewer= 1,  showOrnaments=1, offScreen=1, fp=4, percent = 100, compression = "jpg",  quality = 100, widthHeight = (1712, 903))
        mc.playbackOptions(fps = 1.0, e=1)        
        mm.eval('setPolyCountVisibility(0);') 
                
    def mem_blast(self):
        fps_set = float(str(self.fps_fieldText.text()))
        mc.playbackOptions(fps = fps_set, e=1)
        focPane = [(each) for each in mc.getPanel(vis=1) if "model" in each]
        for each in focPane:
            if mc.modelEditor(each, q=1, av=1) == True:
                mm.eval('setRendererInModelPanel "vp2Renderer" {0}'.format(each))        
        mm.eval('setPolyCountVisibility(1);')
        folder_strt = '/'.join(mc.file(q=1, location=1).split('/')[:-5])
        scn_name=str(mc.file(q=1, location=1)).split('/')[-1].split(".")[0]
        gotten_name=str(mc.file(q=1, location=1)).split('/')[-1].split(".")[0]+"-playblast-half1712x903_vdf8"
        gotten_path = "{}/PRODUCTS/images/{}/{}/playblast-half1712x903_vdf8_jpg/{}".format(folder_strt, _dept_task, scn_name, gotten_name)
        sel_NumMn=mc.playbackOptions(q=1, min=1)
        sel_NumMn_reset=mc.playbackOptions(q=1, min=1)+1    
        mc.currentTime(sel_NumMn)
        mc.currentTime(sel_NumMn_reset)        
        mc.currentTime(sel_NumMn)
        mc.playblast(format="image", filename=gotten_path, sequenceTime=0, clearCache=1, viewer= 1,  showOrnaments=1, offScreen=1, fp=4, percent = 100, compression = "jpg",  quality = 100, widthHeight = (1712, 903))
        mc.playbackOptions(fps = 1.0, e=1)        
        mm.eval('setPolyCountVisibility(0);')
        for each in focPane:
            if mc.modelEditor(each, q=1, av=1) == True:
                mc.modelEditor(each, e=1, rnm="base_OpenGL_Renderer") 
                
    def mem_blast_no_roll(self):
        fps_set = float(str(self.fps_fieldText.text()))
        mc.playbackOptions(fps = fps_set, e=1)
        strt_rng = int(wk_strt_value)-1
        end_rng = mc.playbackOptions(q=1, max=1)
        focPane = [(each) for each in mc.getPanel(vis=1) if "model" in each]
        for each in focPane:
            if mc.modelEditor(each, q=1, av=1) == True:
                mm.eval('setRendererInModelPanel "vp2Renderer" {0}'.format(each))        
        mm.eval('setPolyCountVisibility(1);')
        folder_strt = '/'.join(mc.file(q=1, location=1).split('/')[:-5])
        scn_name=str(mc.file(q=1, location=1)).split('/')[-1].split(".")[0]
        gotten_name=str(mc.file(q=1, location=1)).split('/')[-1].split(".")[0]+"-playblast-half1712x903_vdf8"
        gotten_path = "{}/PRODUCTS/images/{}/{}/playblast-half1712x903_vdf8_jpg/{}".format(folder_strt, _dept_task, scn_name, gotten_name)
        sel_NumMn=mc.playbackOptions(q=1, min=1)
        sel_NumMn_reset=mc.playbackOptions(q=1, min=1)+1    
        mc.currentTime(sel_NumMn)
        mc.currentTime(sel_NumMn_reset)        
        mc.currentTime(sel_NumMn)
        mc.playblast(format="image", filename=gotten_path, sequenceTime=0, clearCache=1, viewer= 1,  showOrnaments=1, offScreen=1, fp=4, percent = 100, compression = "jpg",  quality = 100, widthHeight = (1712, 903))
        mc.playbackOptions(fps = 1.0, e=1)        
        mm.eval('setPolyCountVisibility(0);')
        for each in focPane:
            if mc.modelEditor(each, q=1, av=1) == True:
                mc.modelEditor(each, e=1, rnm="base_OpenGL_Renderer") 
        mc.playbackOptions(fps = 1.0, e=1) 

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
 
    def prim_mode(self):
        focPane = [(each) for each in mc.getPanel(vis=1) if "model" in each]
        for each in focPane:
            if mc.modelEditor(each, q=1, av=1) == True:
                mm.eval('setRendererInModelPanel "vp2Renderer" {0}'.format(each))
                mc.setAttr("hardwareRenderingGlobals.multiSampleEnable", 1)
                mc.setAttr("hardwareRenderingGlobals.lineAAEnable", 1)
                mc.setAttr("hardwareRenderingGlobals.multiSampleCount" ,16)
                mc.setAttr("hardwareRenderingGlobals.ssaoEnable", 1)
                mc.setAttr("hardwareRenderingGlobals.ssaoAmount", 1)
                mc.setAttr("hardwareRenderingGlobals.ssaoRadius", 7)
                mc.setAttr("hardwareRenderingGlobals.ssaoFilterRadius", 16)
                
    def blast_mode(self):
        focPane = [(each) for each in mc.getPanel(vis=1) if "model" in each]
        for each in focPane:
            if mc.modelEditor(each, q=1, av=1) == True:
                mc.modelEditor(each, e=1, rnm="base_OpenGL_Renderer")
                mc.setAttr("hardwareRenderingGlobals.multiSampleEnable", 0)
                mc.setAttr("hardwareRenderingGlobals.lineAAEnable", 0)
                mc.setAttr("hardwareRenderingGlobals.multiSampleCount" ,16)
                mc.setAttr("hardwareRenderingGlobals.ssaoEnable", 0)
                mc.setAttr("hardwareRenderingGlobals.ssaoAmount", 0)
                mc.setAttr("hardwareRenderingGlobals.ssaoRadius", 7)
                mc.setAttr("hardwareRenderingGlobals.ssaoFilterRadius", 16)
                
inst_do_win = prvw_UI()
inst_do_win.show()