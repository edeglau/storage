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

class duplct_name_UI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(duplct_name_UI, self).__init__(parent = None)
 
        self.setWindowTitle("Check for Duplicate names")
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
 
        self.duplct_nm_obj_button = QtWidgets.QPushButton("Print Duplicate names")
        self.connect(self.duplct_nm_obj_button, SIGNAL("clicked()"),
                    lambda: self.print_dups())
        self.dup_layout.addWidget(self.duplct_nm_obj_button)
        
        self.duplct_sl_obj_button = QtWidgets.QPushButton("Select Duplicate names")
        self.connect(self.duplct_sl_obj_button, SIGNAL("clicked()"),
                    lambda: self.select_dups())
        self.dup_layout.addWidget(self.duplct_sl_obj_button) 
        
        self.duplct_rnm_button = QtWidgets.QPushButton("Rename Duplicates")
        self.connect(self.duplct_rnm_button, SIGNAL("clicked()"),
                    lambda: self.rename_dups())
        self.dup_layout.addWidget(self.duplct_rnm_button) 


    def find_dups(self):
        duplicates = [(f.split("|")[-1]) for f in mc.ls(dag=1) ]
        collect_dups = [(item, count) for item, count in collections.Counter(duplicates).items() if count >1]
        return collect_dups
    
    def print_dups(self):
        collect_dups = self.find_dups()
        if len(collect_dups)>0:
            collect_sel = []
            for index, each in enumerate(collect_dups):
                print each
                getgroup = mc.ls(each[0], l=1)
                for item in getgroup:
                    print item
        else:
            print "no duplicate named objects present to print"    
                
    def select_dups(self):
        collect_dups = self.find_dups()
        if len(collect_dups)>0:
            collect_sel = []
            for index, each in enumerate(collect_dups):
                print each
                getgroup = mc.ls(each[0], l=1)
                for item in getgroup:
                    print item
                    collect_sel.append(item)
            mc.select(collect_sel, r=1)
        else:
            print "no duplicate named objects present to print"   

    def rename_dups(self):
        collect_dups = self.find_dups()
        if len(collect_dups)>0:
            collect_sel = []
            for index, each in enumerate(collect_dups):
                for item in range(1, each[-1]):
                    try:
                        new_name = "{}_{}_{}".format(each[0], str(index), str(item))
                        mc.rename(mc.ls(each[0])[0], new_name)
                    except:
                        print "unable to rename {}".format(each[0])
                        pass
        else:
            print "no duplicate named objects present to rename"   


inst_do_win = duplct_name_UI()
inst_do_win.show()
