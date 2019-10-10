


import maya.cmds as mc
import os, sys

import mrig_pyqt
from mrig_pyqt import QtCore, QtGui, QtWidgets
from mrig_pyqt.QtCore import SIGNAL


class createSDK_alias_window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(createSDK_alias_window, self).__init__(parent = None)

        getSel=mc.ls(sl=1, fl=1)  
        if len(getSel)>1:
            pass
        else:
            print "need to select 2 or more items"
            return     
        self.getFirstAttr=mc.listAttr(getSel, w=1, a=1, s=1,u=1)   

        self.setWindowTitle("fast SKD key")
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
        self.sdk_order_layout = QtWidgets.QHBoxLayout()
        self.myform.addRow(self.sdk_order_layout) 
        self.sdkper_button_layout = QtWidgets.QVBoxLayout()
        self.sdk_order_layout.addLayout(self.sdkper_button_layout)
        self.sdk_slid_layout = QtWidgets.QVBoxLayout()
        self.sdk_order_layout.addLayout(self.sdk_slid_layout)   
        self.sdk_slider_layout = QtWidgets.QVBoxLayout()     
        self.sdk_slid_layout.addLayout(self.sdk_slider_layout)
        self.sdk_drop = QtWidgets.QComboBox()
        self.sdk_drop.addItems(self.getFirstAttr)
        self.sdk_slid_layout.addWidget(self.sdk_drop)
        self.att_label = QtWidgets.QLineEdit("attribute name")
        self.sdk_slid_layout.addWidget(self.att_label) 

        # self.textNum.connect(self.textNum,QtCore.SIGNAL("returnPressed()"),self.set_slider)

        self.fstminmax_label = QtWidgets.QLabel("1st min/max")
        self.sdk_slid_layout.addWidget(self.fstminmax_label) 
        self.minval = QtWidgets.QLineEdit("0")
        self.sdk_slid_layout.addWidget(self.minval)
        self.maxval = QtWidgets.QLineEdit("1")
        self.sdk_slid_layout.addWidget(self.maxval)


        self.scndminmax_label = QtWidgets.QLabel("2nd min/max")
        self.sdk_slid_layout.addWidget(self.scndminmax_label) 
        self.scndminval = QtWidgets.QLineEdit("0")
        self.sdk_slid_layout.addWidget(self.scndminval)
        self.scndmaxval = QtWidgets.QLineEdit("1")
        self.sdk_slid_layout.addWidget(self.scndmaxval)

        self.sdkper_fx_button=QtWidgets.QPushButton("Go")
        self.connect(self.sdkper_fx_button, SIGNAL('clicked()'),lambda:  self._create_SDK_alias(
            float(self.minval.text()),
            float(self.maxval.text()),
            float(self.scndminval.text()),
            float(self.scndmaxval.text()), 
            str(self.sdk_drop.currentText()), 
            str(self.att_label.text())))

        self.sdk_slid_layout.addWidget(self.sdkper_fx_button) 

          
    def _create_SDK_alias(self, firstMinValue, firstMaxValue, secondMinValue, secondMaxValue, getFirstattr, floater):
        print firstMinValue, firstMaxValue, secondMinValue, secondMaxValue, getFirstattr, floater
        getSel=mc.ls(sl=1)
        getFirst=getSel[:-1]
        getSecond=getSel[-1]
        anAttr=mc.addAttr([getSecond], ln=floater, at="double", k=1, nn=floater)
        Controller=getSecond+"."+floater
        for each in getFirst:
            Child=each+"."+getFirstattr
            mc.setAttr(Child, lock=0)
            mc.setAttr(Controller, secondMinValue)
            mc.setAttr(Child,firstMinValue)
            mc.setDrivenKeyframe(Child, cd=Controller)
            mc.setAttr(Controller, secondMaxValue)
            mc.setAttr(Child, firstMaxValue)
            mc.setDrivenKeyframe(Child, cd=Controller)
            mc.setAttr(Controller, secondMinValue)
            mc.setAttr(Child, lock=1)        

inst_win = createSDK_alias_window()
inst_win.show()        



