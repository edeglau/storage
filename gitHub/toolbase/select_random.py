import os, sys, subprocess
import re, random
from datetime import datetime
from time import gmtime, strftime
 
import maya.cmds as mc
 
 
 
from maya import OpenMayaUI as omui
 
 
# checkHoudini = os.getenv("HOUDINI_VERSION")
 
# checkMaya = os.getenv("REZ_MAYA_VERSION")
 
 

import PyQt4
from PyQt4 import QtCore, QtGui, Qt
from PyQt4.QtGui import QWidget, QRadioButton, QGridLayout, QLabel, \
    QTableWidget, QComboBox, QKeySequence, QToolButton, QPlainTextEdit, QPushButton,QBoxLayout, \
    QClipboard, QTableWidgetItem, QCheckBox, QVBoxLayout, QHBoxLayout, \
    QPixmap, QLineEdit, QListWidget, QTextEdit, QSizePolicy, QFrame, QPalette, QColor, \
    QFont, QAbstractItemView, QMenu, QMessageBox
from PyQt4.QtCore import SIGNAL
 
# if checkHoudini != None:
#     import hutil
#     from hutil.Qt import QtCore, QtWidgets, QtWidgets
#     from hutil.Qt.QtCore import SIGNAL
 
 
 
 
# sel = mc.ls(selection=False)
class selection_win(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(selection_win, self).__init__(parent = None)
 
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
        self.prnt_verbose_button = QtWidgets.QPushButton("randomize")
        self.connect(self.prnt_verbose_button, SIGNAL("clicked()"),
                    lambda: self.select_randomize())
        self.sel_order_layout.addWidget(self.prnt_verbose_button) 
        self.prnt_verbose_button = QtWidgets.QPushButton("nth")
        self.connect(self.prnt_verbose_button, SIGNAL("clicked()"),
                    lambda: self.select_nth())
        self.sel_order_layout.addWidget(self.prnt_verbose_button)              
        self.textNum = QtWidgets.QLineEdit("50%")
        self.textNum.connect(self.textNum,QtCore.SIGNAL("returnPressed()"),self.set_slider)
        self.sel_order_layout.addWidget(self.textNum)
        self.selection_slider = QtWidgets.QSlider()
        self.selection_slider.setMinimum(1)
        self.selection_slider.setMaximum(100)
        self.selection_slider.setValue(50)       
        self.selection_slider.setTickInterval(5)
        self.selection_slider.setTickPosition(self.selection_slider.TicksBelow)
        self.selection_slider.Orientation = (2)
        self.selection_slider.valueChanged.connect(self.print_slider)
        self.sel_order_layout.addWidget(self.selection_slider)  
  
 
    def select_nth(self):
        getfulllist=mc.ls(sl=1, fl=1)
        get_select = self.find_n_number(getfulllist)
        mc.select(get_select, r=1)
        getfulllist=mc.ls(sl=1, fl=1)
 
    def select_randomize(self):
        getfulllist=mc.ls(sl=1, fl=1)
        get_select = self.find_number(getfulllist)
        mc.select(get_select, r=1)
        getfulllist=mc.ls(sl=1, fl=1)
 
 
    def find_n_number(self, getfulllist):
        nextList = []
        size = self.selection_slider.value()
        nsize = int(size)
        for each in getfulllist[::nsize]:
            nextList.append(each)
        return nextList
 
 
    def find_number(self, getfulllist):
        nextList = []
        size = self.selection_slider.value()
        random.shuffle(getfulllist)
        getlist=len(getfulllist)
        multiplyfulllist = float(size) *.01
        getNewlist = getlist*multiplyfulllist
        getNewlist = int(getNewlist)
        for index, part in enumerate(getfulllist):
            if index in range(getNewlist):
                nextList.append(part)
        return nextList
 
 
 
    def print_slider(self):
        size = self.selection_slider.value()
        self.textNum.setText(str(size)+"%")
 
    def set_slider(self):
        getText = self.textNum.text()
        getText = int(getText)
        self.selection_slider.setValue(getText)
 
 
inst_mkwin=selection_win()
inst_mkwin.show()
