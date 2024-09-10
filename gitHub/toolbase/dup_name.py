'''(This launches a GUI)Sets your viewport for review modes'''

import maya.cmds as mc
import os, sys
import maya.mel as mm
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets

import collections


class duplct_name_UI(QtWidgets.QMainWindow):
    def __init__(self):
        super(duplct_name_UI, self).__init__()

        self.setWindowTitle("Check for duplicate names")
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
        self.duplct_nm_order_layout = QtWidgets.QHBoxLayout()
        self.myform.addRow(self.duplct_nm_order_layout)
        self.duplct_nm_button_layout = QtWidgets.QVBoxLayout()
        self.duplct_nm_order_layout.addLayout(self.duplct_nm_button_layout)
        self.duplct_nm_slid_layout = QtWidgets.QVBoxLayout()
        self.duplct_nm_order_layout.addLayout(self.duplct_nm_slid_layout)  
        self.duplct_nm_slider_layout = QtWidgets.QVBoxLayout()    
        self.duplct_nm_slid_layout.addLayout(self.duplct_nm_slider_layout)


        self.duplct_nm_obj_button = QtWidgets.QPushButton("Print Duplicate names")
        self.duplct_nm_obj_button.setStyleSheet("color: #eeffaa; background-color: rgba(105,110,70,100);")
        self.duplct_nm_obj_button.clicked.connect(lambda: self.print_dups())
        # self.connect(self.duplct_nm_obj_button, SIGNAL("clicked()"),
        #             lambda: self.print_dups())
        self.duplct_nm_button_layout.addWidget(self.duplct_nm_obj_button)

        self.duplct_sl_obj_button = QtWidgets.QPushButton("Select Duplicate names")
        self.duplct_sl_obj_button.setStyleSheet("color: #eeffaa; background-color: rgba(105,110,70,100);")
        # self.connect(self.duplct_sl_obj_button, SIGNAL("clicked()"),
        #             lambda: self.select_dups())
        self.duplct_sl_obj_button.clicked.connect(lambda: self.select_dups())
        self.duplct_nm_button_layout.addWidget(self.duplct_sl_obj_button)

        self.duplct_rnm = QtWidgets.QPushButton("Rename Duplicates")
        self.duplct_rnm.setStyleSheet("color: #eeffaa; background-color: rgba(100,110,70,50);")
        # self.connect(self.duplct_rnm, SIGNAL("clicked()"),
        #             lambda: self.rename_dups())
        self.duplct_rnm.clicked.connect(lambda: self.rename_dups())
        self.duplct_nm_button_layout.addWidget(self.duplct_rnm)

    def print_dups(self):
        collect_dups = self.find_dups()
        if len(collect_dups)>0:
            collect_sel = []
            for index, each in enumerate(collect_dups):
                print each
                getgroup  = mc.ls(each[0], l=1)
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
                getgroup  = mc.ls(each[0], l=1)
                for item in getgroup:
                    print item
                    collect_sel.append(item)
            mc.select(collect_sel, r=1)
        else:
            print "no duplicate named objects present to select"

    # @commonUtil.undochunk
    def rename_dups(self):
        collect_dups = self.find_dups()
        if len(collect_dups)>0:
            for index, each in enumerate(collect_dups):
                for item in range(1, each[-1]):
                    try:
                        new_name = "{}_{}_{}".format(each[0], str(index), str(item))
                        mc.rename(mc.ls(each[0])[0], new_name)
                        print "Renamed {} to {} ".format(each[0], new_name)
                    except:
                        print "unable to rename {}".format(each[0])
                        pass
        else:
            print "no duplicate named objects present to rename"

    def find_dups(self):
        duplicates = [(f.split("|")[-1]) for f in mc.ls(dag=1) ]
        collect_dups = [(item, count) for item, count in collections.Counter(duplicates).items() if count >1]
        return collect_dups

inst_do_win=duplct_name_UI()
inst_do_win.show()
