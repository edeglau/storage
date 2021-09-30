#!/usr/bin/env python
# -*- coding: utf-8 -*- 

__author__="Elise Deglau"
__developer__="deglaue"

import maya.cmds as mc
import os, sys
import maya.mel as mm



import Qt_py
from Qt_py.Qt import QtCore, QtGui, QtWidgets

class mayaShrtTips(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(mayaShrtTips, self).__init__(parent = None)
        # self.setWindowTitle("Windowhm Command Tips")

        self.setWindowTitle("Windowhm Command Tips")
        self.left = 10
        self.top = 10
        self.width = 950
        self.height = 600
        self.setGeometry(self.left, self.top, self.width, self.height)
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

        # self.add_widgets()

        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(self.selection_widgetframe)
        scroll.setWidgetResizable(False)
        self.layout.addWidget(scroll, 1,0,1,1)
        self.setLayout(self.layout)

        # self.layout = QtWidgets.QVBoxLayout()
        self.btnlayout = QtWidgets.QHBoxLayout()
        # self.playlist_names = QtWidgets.QComboBox()
        # self.layout.addLayout(self.btnlayout)
        self.layout.addLayout(self.btnlayout, 1,0,1,1)
        self.label = QtWidgets.QPlainTextEdit("\
            \bCreate a list containing all nurbsCurve objects in a group]\
            \n=====================================================================>\
                \ngetit = [(mc.listRelatives(each, p=1, type='transform')[0]) for each in mc.listRelatives('Head_Coll_beardHairAddDesc_crv_grp', ad=1, type='nurbsCurve')]\
            \n=====================================================================>\
            \n                  Create a list containing all mesh objects in a group\
            \n=====================================================================>\
                \ngetit = [(mc.listRelatives(each, p=1, type='transform')[0]) for each in mc.listRelatives('Model_grp', ad=1, type='mesh')]\
            \n=====================================================================>\
            \n                  Execute a tool from python\
            \n=====================================================================>\
            \nimport sys\
                \nfilepath = ('//sw//dev//deglaue//sandbox//')\
                \nsys.path.append(str(filepath))\
                \nimport maya_shorthand\
                \nreload (maya_shorthand)\
            \n=====================================================================>\
            \n                  Get all the related mesh and joints they are constrained to(helpful in calamari rigs)\
            \n=====================================================================>\
            \nget_desttransform = [(mc.listRelatives(each, p=1, type = 'transform')[0])for each in mc.listRelatives('c_body_grp_mid', ad=1, type='mesh') if 'Orig' not in each]\
            \nmk_dict = {}\
            \nfor dest in get_desttransform:\
                \n    get_cnst = mc.listRelatives(dest, c=1, type= 'parentConstraint')[0]\
                \n    get_jnt = [(item) for item in mc.listConnections(get_cnst, s=1, c=1) if mc.nodeType(item) == 'joint'][0]\
                \n    new_item = {dest:get_jnt}\
                \n    mk_dict.update(new_item)\
            \nfor each, key in mk_dict.items():\
                \n    print '{}:{}'.format(each, key)\
            \n=====================================================================>\
            \n                  Select all curves within a group that fall below a specified length\
            \n=====================================================================>\
            \ndropoff = .85\
            \narclen_limit = 4\
            \ntargetSelection_crvs = [(mc.listRelatives(each, p = 1)[0]) for each in\
                                            \nmc.listRelatives(mc.ls(sl=1)[0], ad=1, type='nurbsCurve') if mc.arclen(each) < arclen_limit]\
            \nmc.select(targetSelection_crvs, r = 1)\
            \n=====================================================================>\
            \n                  Time items\
            \n=====================================================================>\           
            \nimport time\
            \nstart_time = time.time()\
            \n<inset python process here>\
            \nsetupSeconds = abs(start_time - time.time())\
            \nm, s = divmod(setupSeconds, 60)\
            \nh, m = divmod(m, 60)\
            \nprint '%02d hours %02d minutes %02d seconds Total' % (h, m, s) \
            ")            
        self.cls_button = QtWidgets.QPushButton("close")
        self.cls_button.clicked.connect(lambda: self.confirmButt())
        # self.connect(self.cls_button, SIGNAL("clicked()"),
        #             lambda: self.confirmButt())
        self.btnlayout.addWidget(self.label)
        self.btnlayout.addWidget(self.cls_button)
        self.setLayout(self.layout)

    def confirmButt(self):
        self.close()

inst_mppwin=mayaShrtTips()
inst_mppwin.show()
            
                
