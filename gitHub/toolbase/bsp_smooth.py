import PyQt4
from PyQt4 import QtCore, QtGui, Qt
from PyQt4.QtGui import QWidget, QRadioButton, QGridLayout, QLabel, \
    QTableWidget, QComboBox, QKeySequence, QToolButton, QPlainTextEdit, QPushButton,QBoxLayout, \
    QClipboard, QTableWidgetItem, QCheckBox, QVBoxLayout, QHBoxLayout, \
    QPixmap, QLineEdit, QListWidget, QTextEdit, QSizePolicy, QFrame, QPalette, QColor, \
    QFont, QAbstractItemView, QMenu, QMessageBox
from PyQt4.QtCore import SIGNAL


import maya.cmds as mc
import os, sys

import maya.mel as mm


class smth_win(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(smth_win, self).__init__(parent = None)

        self.setWindowTitle("SmoothFlooder")
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
        self.sel_button_layout = QtWidgets.QHBoxLayout()
        self.myform.addRow(self.sel_button_layout)         
        self.drop_label = QtWidgets.QLabel("Amount")
        self.sel_order_layout.addWidget(self.drop_label)     
        self.droppoff = QtWidgets.QLineEdit("10")
        self.sel_order_layout.addWidget(self.droppoff)           
        self.swap_button = QtWidgets.QPushButton("Go")
        self.connect(self.swap_button, SIGNAL("clicked()"),
                    lambda: self.smoothPaint(amt = int(self.droppoff.text())))
        self.sel_button_layout.addWidget(self.swap_button)     
        self.help_button = QtWidgets.QPushButton("Help")
        self.connect(self.help_button, SIGNAL("clicked()"),
                    lambda: self.help())
        self.sel_button_layout.addWidget(self.help_button) 

    @undo      
    def smoothPaint ( self, amt):
        getState=mc.artAttrCtx(mc.currentCtx(), q=1, sao=1)
        mc.artAttrCtx(mc.currentCtx(), e=1, sao="smooth")
        for each in range (0, amt):
            mc.artAttrCtx(mc.currentCtx(), e=1, clr=1)
        mc.artAttrCtx(mc.currentCtx(), e=1, sao=getState)

    def help ( self):
        url="https://atlas.bydeluxe.com/confluence/display/~deglaue/Blend+Groups"
        subprocess.Popen('xdg-open "%s"' % url, stdout=subprocess.PIPE, shell=True)


inst_win = smth_win()
inst_win.show()



