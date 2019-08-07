
__author__="Elise Deglau"

# import soupUtils
import sys, os
import maya.cmds as mc
try:
    mc.pluginInfo("/sw/packages/internal.td/mrigplugins/1.11.5/maya/2016.5/linux_x86_64_CentOS-7/plugins/3rdparty/SOuP.so", edit = 1, autoload=1)
except:
    pass

'''
Creates a blendCurves node and connects selected groups

step 1: enter first group of curves(usually input curves)
step 2: enter second group of curves(usually sim curves)
step 3: enter third group of curves(output curves)
step 4: Click "Go" will connect first two into the third group of curves.

'''


# import mrig_pyqt
# from mrig_pyqt import QtCore, QtGui
# from mrig_pyqt.QtGui import QWidget, QRadioButton, QGridLayout, QLabel, \
#     QTableWidget, QComboBox, QKeySequence, QToolButton, QPlainTextEdit, QPushButton,QBoxLayout, \
#     QClipboard, QTableWidgetItem, QCheckBox, QVBoxLayout, QHBoxLayout, \
#     QPixmap, QLineEdit, QListWidget, QTextEdit, QSizePolicy, QFrame, QPalette, QColor, \
#     QFont, QAbstractItemView, QMenu, QMessageBox
# from mrig_pyqt.QtCore import SIGNAL

import mrig_pyqt
from mrig_pyqt import QtCore, QtGui, QtWidgets
from mrig_pyqt.QtCore import SIGNAL

import pymel.core as pm
import maya.app.general.nodeEditor as __mod  

class blendCurve_connect(QtWidgets.QWidget):
    def __init__(self):
        super(blendCurve_connect, self).__init__()
        self.initUI()

    def initUI(self):
        # self._choser_group_window(getFiles)             
        self.setWindowTitle("blendCurves Build")
        self.layout = QtWidgets.QVBoxLayout()
        self.btnlayout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.btnlayout)

        self.Hlayout_one = QtWidgets.QHBoxLayout()
        self.btnlayout.addLayout(self.Hlayout_one)
        self.label_one_Text = QtWidgets.QLabel()
        self.label_one_Text.setText("input1")
        self.Hlayout_one.addWidget(self.label_one_Text)
        self.field_one_Text = QtWidgets.QLineEdit()
        self.Hlayout_one.addWidget(self.field_one_Text)
        self.set_one_button = QtWidgets.QPushButton("<<")
        self.connect(self.set_one_button, SIGNAL('clicked()'), lambda *args:self.set_button_one_function())
        self.Hlayout_one.addWidget(self.set_one_button)
        
        self.Hlayout_two = QtWidgets.QHBoxLayout()
        self.btnlayout.addLayout(self.Hlayout_two)
        self.label_two_Text = QtWidgets.QLabel()
        self.label_two_Text.setText("input2")
        self.Hlayout_two.addWidget(self.label_two_Text)
        self.field_two_Text = QtWidgets.QLineEdit()
        self.Hlayout_two.addWidget(self.field_two_Text)
        self.set_two_button = QtWidgets.QPushButton("<<")
        self.connect(self.set_two_button, SIGNAL('clicked()'), lambda *args:self.set_button_two_function())
        self.Hlayout_two.addWidget(self.set_two_button)

        self.Hlayout_three = QtWidgets.QHBoxLayout()
        self.btnlayout.addLayout(self.Hlayout_three)
        self.label_three_Text = QtWidgets.QLabel()
        self.label_three_Text.setText("output")
        self.Hlayout_three.addWidget(self.label_three_Text)
        self.field_three_Text = QtWidgets.QLineEdit()
        self.Hlayout_three.addWidget(self.field_three_Text)
        self.set_three_button = QtWidgets.QPushButton("<<")
        self.connect(self.set_three_button, SIGNAL('clicked()'), lambda *args:self.set_button_three_function())
        self.Hlayout_three.addWidget(self.set_three_button)

        self.set_all_button = QtWidgets.QPushButton("fill all")
        self.set_all_button.setToolTip("select 3 groups in order will fill all fields")
        self.btnlayout.addWidget(self.set_all_button)
        self.connect(self.set_all_button, SIGNAL('clicked()'), lambda *args:self.set_all_button_function())

        self.go_button = QtWidgets.QPushButton("Go")
        self.go_button.setToolTip("will create a blendCurve node and connect first two groups of curves into the third group of curves")
        self.btnlayout.addWidget(self.go_button)
        self.connect(self.go_button, SIGNAL('clicked()'), lambda *args:self.activate())

        self.setLayout(self.layout)
        
    def set_button_one_function(self):
        getItemOne = mc.ls(sl=1)[0]
        self.field_one_Text.setText(getItemOne)

    def set_button_two_function(self):
        getItemTwo = mc.ls(sl=1)[0]
        self.field_two_Text.setText(getItemTwo)

    def set_button_three_function(self):
        getItemThree = mc.ls(sl=1)[0]
        self.field_three_Text.setText(getItemThree)

    def set_all_button_function(self):
        if len(mc.ls(sl=1)) == 3:
            pass
        else:
            print "need to select three groups of curves"
            return
        getItems = mc.ls(sl=1)
        self.field_one_Text.setText(getItems[0])
        self.field_two_Text.setText(getItems[1])
        self.field_three_Text.setText(getItems[2])


    # def activate(self):
    #     inputsA = self.field_one_Text.text()
    #     inputsB = self.field_two_Text.text()
    #     outPutS = self.field_three_Text.text()
    #     if outPutS == None:
    #         copc = True
    #     else:
    #         copc = False
    #     bc = soupUtils.createBlendCurves(name=inputsA+"_bc")
    #     # inputsA = ['curve1'] # list as many curves 
    #     # inputsB = ['curve2'] # list as many curves to blend
    #     soupUtils.connectBlendCurves(bc, inputCurves1=inputsA, inputCurves2=inputsB, outputCurves=outPutS, createOutputCurves=copc)

    def activate(self):     
        get_one = self.field_one_Text.text()
        get_two = self.field_two_Text.text()
        get_three = self.field_three_Text.text()
        crvObj_one=mc.listRelatives(mc.ls(get_one)[0], ad=1, type="nurbsCurve")
        crvObj_two=mc.listRelatives(mc.ls(get_two)[0], ad=1, type="nurbsCurve")
        crvObj_three=mc.listRelatives(mc.ls(get_three)[0], ad=1, type="nurbsCurve")
        mc.createNode("blendCurves")
        # bc = soupUtils.createBlendCurves(name= get_three+"_bc")
        bc_node = mc.rename(mc.ls(sl=1)[0], get_three+"_bc") 
        # bc_node = mc.shadingNode('blendCurves', n=get_three+"_bc")
        for index, each_one in enumerate(crvObj_one):
            mc.connectAttr(each_one+".worldSpace[0]", bc_node+".inCurves[{}]".format(index), f=1)
        for index, each_two in enumerate(crvObj_two):
            mc.connectAttr(each_two+".worldSpace[0]", bc_node+".inCurves2[{}]".format(index), f=1)
        for index, each_three in enumerate(crvObj_three):
            mc.connectAttr(bc_node+".outCurves[{}]".format(index), each_three+".create", f=1)


inst=blendCurve_connect()
inst.show()                    
