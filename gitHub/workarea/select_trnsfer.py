'''Transfers selection to nearby verts of other objects'''
__author__="Elise Deglau"
import maya.cmds as mc
import os, sys
#import maya.mel
import numpy
from apiWrappers import getPoints
import mMesh
reload(mMesh)
import maya.api.OpenMaya as OpenMaya
from scipy.spatial import ckdtree
import numpy as np
checkHoudini = os.getenv("HOUDINI_VERSION")
import re
checkMaya = os.getenv("REZ_MAYA_VERSION")
import PyQt4


if checkHoudini != None:
    import hutil
    from hutil.Qt import QtCore, QtWidgets, QtWidgets
    from hutil.Qt.QtCore import SIGNAL
    
class wgtmap_select_gui(QtWidgets.QMainWindow):
    def __init__(self):
        super(wgtmap_select_gui, self).__init__()
        self.initUI()

    def initUI(self):     
        self.setWindowTitle("Select based on weightmap")
        self.central_widget=QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.masterLayout=QtWidgets.QGridLayout(self.central_widget)
        self.masterLayout.setAlignment(QtCore.Qt.AlignTop)


        self.myform = QtWidgets.QFormLayout()
        self.wgt_layout = QtWidgets.QGridLayout()
        self.masterLayout.addLayout(self.wgt_layout, 0,0,1,1)

        self.SelectionSetupLayout = QtWidgets.QGridLayout()
        self.selection_widgetframe = QtWidgets.QFrame()
        self.selection_widgetframe.setLayout(self.SelectionSetupLayout)
        self.SelectionSetupLayout.addLayout(self.myform, 0,0,1,1)
        self.wgt_layout.addLayout(self.SelectionSetupLayout, 0,0,1,1)

        self.add_widgets()

        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(self.selection_widgetframe)
        scroll.setWidgetResizable(False)
        self.wgt_layout.addWidget(scroll, 1,0,1,1)
        self.setLayout(self.wgt_layout)
    def add_widgets(self):
        self.sel_order_layout = QtWidgets.QHBoxLayout()
        self.myform.addRow(self.sel_order_layout) 
        self.sel_button_layout = QtWidgets.QHBoxLayout()
        self.myform.addRow(self.sel_button_layout)         
        self.value_label = QtWidgets.QLabel("value")
        self.sel_order_layout.addWidget(self.value_label)  
        # self.textNum = QtWidgets.QLabel("10%")
        self.textNum = QtWidgets.QLineEdit("10%")
        self.textNum.connect(self.textNum,QtCore.SIGNAL("returnPressed()"),self.set_slider)
        self.sel_order_layout.addWidget(self.textNum)        
        self.selection_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal) 
        self.selection_slider.Orientation = (0) 
        self.selection_slider.setMinimum(1)
        self.selection_slider.setMaximum(100)
        self.selection_slider.setValue(10)        
        self.selection_slider.valueChanged.connect(self.print_slider)
        self.sel_order_layout.addWidget(self.selection_slider) 
        self.sel_order_layout.addWidget(self.drop_label)     
        self.droppoff = QtWidgets.QLineEdit(".5")
        self.sel_order_layout.addWidget(self.droppoff)           
        self.swap_button = QtWidgets.QPushButton("Swap")
        self.connect(self.swap_button, SIGNAL("clicked()"),
                    lambda: self.sel_wgt_function(radius = self.selection_slider.value(), adding = False, reverse = False))
        self.sel_button_layout.addWidget(self.swap_button)     
        self.add_button = QtWidgets.QPushButton("Add")
        self.connect(self.add_button, SIGNAL("clicked()"),
                    lambda: self.sel_wgt_function(radius = self.selection_slider.value(), adding = True, reverse = False))
        self.sel_button_layout.addWidget(self.add_button)   
        self.swap_rev_button = QtWidgets.QPushButton("SwapReverseValue")
        self.connect(self.swap_rev_button, SIGNAL("clicked()"),
                    lambda: self.sel_wgt_function(radius = self.selection_slider.value(), adding = False, reverse = True))
        self.sel_button_layout.addWidget(self.swap_rev_button)     
        self.add_rev_button = QtWidgets.QPushButton("AddReverseValue")
        self.connect(self.add_rev_button, SIGNAL("clicked()"),
                    lambda: self.sel_wgt_function(radius = self.selection_slider.value(), adding = True, reverse = True))
        self.sel_button_layout.addWidget(self.add_rev_button)                                     
        self.sel_errant_button = QtWidgets.QPushButton("Grab Errant")
        self.connect(self.sel_errant_button, SIGNAL("clicked()"),
                    lambda: self.sel_errant_weight(adding = False, reverse = False))
        self.sel_button_layout.addWidget(self.sel_errant_button)   
        self.sel_errant_button_pos = QtWidgets.QPushButton("Grab Errant Pos")
        self.connect(self.sel_errant_button_pos, SIGNAL("clicked()"),
                    lambda: self.sel_errant_weight_pos(adding = False, reverse = False))
        self.sel_button_layout.addWidget(self.sel_errant_button_pos)           
        self.pt_fol_button = QtWidgets.QPushButton("paint fol")
        self.connect(self.pt_fol_button, SIGNAL("clicked()"),
                    lambda: self.paint_fol_function(radius = self.selection_slider.value(), adding = True, reverse = False))
        self.sel_button_layout.addWidget(self.pt_fol_button)     
        self.pt_crv_button = QtWidgets.QPushButton("paint crv")
        self.connect(self.pt_crv_button, SIGNAL("clicked()"),
                    lambda: self.paint_crv_function(radius = self.selection_slider.value(), adding = True, reverse = False))
        self.sel_button_layout.addWidget(self.pt_crv_button)     
    def set_slider(self):
        getText = self.textNum.text()
        getText = int(getText)
        self.selection_slider.setValue(getText)


    def print_slider(self):
        size = self.selection_slider.value()
        self.textNum.setText(str(size)+"%")

    def sel_errant_weight(self, adding, reverse):
        getobj = mc.ls(sl=1, fl=1)[0]        
        collect = []
        if ".v" in getobj:
            getobj = getobj.split('.v')[0]
        verts = mc.ls(getobj+'.vtx[*]', fl=True)
        try:
            blendShapeNode = mc.artAttrCtx(mc.currentCtx(), q=1, asl=1)
        except:
            print "select a paint type map to apply(right click: paint)"
            return
        blendShapeNode = blendShapeNode.split('.')[1]
        for index, each_vert in enumerate(verts):
            find = mc.getAttr('{0}.inputTarget[0].baseWeights[{1}]'.format(blendShapeNode, index))
            if "e" in str(find):
                collect.append(each_vert)  
        mc.select(cl=1)                             
        
    def sel_errant_weight_pos(self, adding, reverse):
        getobj = mc.ls(sl=1, fl=1)[0]        
        collect = []
        if ".v" in getobj:
            getobj = getobj.split('.v')[0]
        verts = mc.ls(getobj+'.vtx[*]', fl=True)
        try:
            blendShapeNode = mc.artAttrCtx(mc.currentCtx(), q=1, asl=1)
        except:
            print "select a paint type map to apply(right click: paint)"
            return
        blendShapeNode = blendShapeNode.split('.')[1]
        for index, each_vert in enumerate(verts):
            find = mc.getAttr('{0}.inputTarget[0].baseWeights[{1}]'.format(blendShapeNode, index))
            if find>1:
                collect.append(each_vert)  
        mc.select(cl=1)                                          
        mc.select(collect, add=1) 


    def sel_wgt_function(self, radius, adding, reverse):
        getobj = mc.ls(sl=1, fl=1)[0]        
        radius = float(radius) *.01
        collect = []
        if ".v" in getobj:
            getobj = getobj.split('.v')[0]
        verts = mc.ls(getobj+'.vtx[*]', fl=True)
        try:
            blendShapeNode = mc.artAttrCtx(mc.currentCtx(), q=1, asl=1)
        except:
            print "select a paint type map to apply(right click: paint)"
            return
        blendShapeNode = blendShapeNode.split('.')[1]
        for index, each_vert in enumerate(verts):
            find = mc.getAttr('{0}.inputTarget[0].baseWeights[{1}]'.format(blendShapeNode, index))
            if "e" not in str(find):
                # find = str(find).split('e')[0]
                # find = float(find)
                if reverse == True:
                    if find < radius:
                        collect.append(each_vert)
                else:
                    if find > radius:
                        collect.append(each_vert)  
        if adding == False:
            mc.select(cl=1)                                          
        mc.select(collect, add=1) 
