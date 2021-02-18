import re, random, os
import subprocess, platform
import maya.cmds as mc
import maya.mel as mm
import ast
checkHoudini = os.getenv('HOUDINI_VERSION')

checkMaya = os.getenv('REZ_MAYA_VERSION')
OSplatform=platform.platform()

import Qt_py
from Qt_py.Qt import QtCore, QtGui, QtWidgets


import random
__author__="Elise Deglau"
colorlist=[13, 6, 14, 17, 4, 8, 5, 7, 15, 5, 20, 24, 29, 31, 10, 16, 9, 30, 1, 2]

class get_set_sel_val(QtWidgets.QWidget):
    def __init__(self, ):
        super(get_set_sel_val, self).__init__()
        self.initUI()


    def initUI(self):  
        sel_obj = mc.ls(sl=1)[0]
        if len(mc.ls(sl=1))>0:
            each_attr = [(the_item) for the_item in mc.listAttr (sel_obj, k=1) if 'visibility' not in the_item]
        else:
            each_attr = ["tx", "ty", "tz", "rx", "ry", "rz"]
        title = "Set Values for review titles"   
        self.setWindowTitle(title)
        self.layout = QtWidgets.QVBoxLayout()
        self.btnlayout = QtWidgets.QGridLayout()
        # self.playlist_names = QComboBox()
        self.frames_label = QtWidgets.QLabel("accross frames")
        self.frames = QtWidgets.QLineEdit("12")
        self.attr_label = QtWidgets.QLabel("Attr to animate")
        self.attrlist = QtWidgets.QComboBox()
        self.attrlist.addItems(each_attr)
        try:
            index1 = self.attrlist.findText("translateX", QtCore.Qt.MatchFixedString)
            if index1:
                self.attrlist.setCurrentIndex(index1)
        except:
            pass
        #if one
        self.attr_cust_label = QtWidgets.QLabel("Enter custom attr if preferred:")
        self.cust_checked = QtWidgets.QCheckBox()
        # self.attr_line_edit = QtWidgets.QLineEdit('translateY')
        self.value_label = QtWidgets.QLabel("Amount to animate")
        self.valueset_lo_one = QtWidgets.QLineEdit("-1")
        self.valueset_hi_one = QtWidgets.QLineEdit("1")
        #if two
        self.attrlist_two = QtWidgets.QComboBox()
        self.attrlist_two.addItems(each_attr)
        try:
            index2 = self.attrlist_two.findText("translateY", QtCore.Qt.MatchFixedString)
            if index2:
                self.attrlist_two.setCurrentIndex(index2)
        except:
            pass
        self.attr_cust_add_label = QtWidgets.QLabel("Enter additive custom attr if preferred:")
        self.cust_checked_two = QtWidgets.QCheckBox()
        # self.attr_two_line_edit = QtWidgets.QLineEdit('translateY')
        self.value_label = QtWidgets.QLabel("Amount to animate")
        self.valueset_lo_two = QtWidgets.QLineEdit("-1")
        self.valueset_hi_two = QtWidgets.QLineEdit("1")
        #if three
        self.attrlist_three = QtWidgets.QComboBox()
        self.attrlist_three.addItems(each_attr)
        try:
            index2 = self.attrlist_three.findText("translateZ", QtCore.Qt.MatchFixedString)
            if index2:
                self.attrlist_three.setCurrentIndex(index2)
        except:
            pass
        self.attr_cust_add_label = QtWidgets.QLabel("Enter additive custom attr if preferred:")
        self.cust_checked_three = QtWidgets.QCheckBox()
        # self.attr_three_line_edit = QtWidgets.QLineEdit('translateY')
        self.value_label = QtWidgets.QLabel("Amount to animate")
        self.valueset_lo_three = QtWidgets.QLineEdit("-1")
        self.valueset_hi_three = QtWidgets.QLineEdit("1")
        #if four
        self.attrlist_four = QtWidgets.QComboBox()
        self.attrlist_four.addItems(each_attr)       
        try:
            index2 = self.attrlist_four.findText("rotateX", QtCore.Qt.MatchFixedString)
            if index2:
                self.attrlist_four.setCurrentIndex(index2)
        except:
            pass
        self.attr_cust_add_label = QtWidgets.QLabel("Enter additive custom attr if preferred:")
        self.cust_checked_four = QtWidgets.QCheckBox()
        # self.attr_four_line_edit = QtWidgets.QLineEdit('translateY')
        self.value_label = QtWidgets.QLabel("Amount to animate")
        self.valueset_lo_four = QtWidgets.QLineEdit("-1")
        self.valueset_hi_four = QtWidgets.QLineEdit("1")
        #if five
        self.attrlist_five = QtWidgets.QComboBox()
        self.attrlist_five.addItems(each_attr)        
        try:
            index2 = self.attrlist_five.findText("rotateY", QtCore.Qt.MatchFixedString)
            if index2:
                self.attrlist_five.setCurrentIndex(index2)
        except:
            pass
        self.attr_cust_add_label = QtWidgets.QLabel("Enter additive custom attr if preferred:")
        self.cust_checked_five = QtWidgets.QCheckBox()
        # self.attr_five_line_edit = QtWidgets.QLineEdit('translateY')
        self.value_label = QtWidgets.QLabel("Amount to animate")
        self.valueset_lo_five = QtWidgets.QLineEdit("-1")
        self.valueset_hi_five = QtWidgets.QLineEdit("1")
        #if six
        self.attrlist_six = QtWidgets.QComboBox()
        self.attrlist_six.addItems(each_attr)   
        try:
            index2 = self.attrlist_six.findText("rotateZ", QtCore.Qt.MatchFixedString)
            if index2:
                self.attrlist_six.setCurrentIndex(index2)
        except:
            pass
        self.attr_cust_add_label = QtWidgets.QLabel("Enter additive custom attr if preferred:")
        self.cust_checked_six = QtWidgets.QCheckBox()
        # self.attr_six_line_edit = QtWidgets.QLineEdit('translateY')
        self.value_label = QtWidgets.QLabel("Amount to animate")
        self.valueset_lo_six = QtWidgets.QLineEdit("-1")
        self.valueset_hi_six = QtWidgets.QLineEdit("1")
        # self.playlist_names.addItems(detailMessge)
        # self.layout.addWidget(self.playlist_names)
        self.layout.addLayout(self.btnlayout)
        self.ctrl_button = QtWidgets.QPushButton("annot controllers")
        self.ctrl_button.clicked.connect(lambda: self.build_ctrl_annot_one())
        
        self.strLayout = QtWidgets.QGridLayout()
        self.strFrame = QtWidgets.QFrame()
        # self.strFrame.setStyleSheet("color: rgba(100,70,70,100);")
        self.strFrame.setLayout(self.strLayout)
        self.btnlayout.addWidget(self.strFrame)
        
        self.strLayout_two = QtWidgets.QGridLayout()
        self.strFrame_two = QtWidgets.QFrame()
        # self.strFrame_two.setStyleSheet("color: # rgba(70,100,70, 100);")
        self.strFrame_two.setLayout(self.strLayout_two)
        self.btnlayout.addWidget(self.strFrame_two)
        
        self.strLayout_three = QtWidgets.QGridLayout()
        self.strFrame_three = QtWidgets.QFrame()
        # self.strFrame_three.setStyleSheet("color: rgba(70,70,100, 100);")
        self.strFrame_three.setLayout(self.strLayout_three)
        self.btnlayout.addWidget(self.strFrame_three)        
        
        self.strLayout_four = QtWidgets.QGridLayout()
        self.strFrame_four = QtWidgets.QFrame()
        # self.strFrame_four.setStyleSheet("color: rgba(100,70,70,100);")
        self.strFrame_four.setLayout(self.strLayout_four)
        self.btnlayout.addWidget(self.strFrame_four)

        self.strLayout_five = QtWidgets.QGridLayout()
        self.strFrame_five = QtWidgets.QFrame()
        # self.strFrame_five.setStyleSheet("color:  rgba(70,100,70,100);")
        self.strFrame_five.setLayout(self.strLayout_five)
        self.btnlayout.addWidget(self.strFrame_five)        
        
        self.strLayout_six = QtWidgets.QGridLayout()
        self.strFrame_six = QtWidgets.QFrame()
        # self.strFrame_six.setStyleSheet("color: rgba(70,70,100, 100);")
        self.strFrame_six.setLayout(self.strLayout_six)
        self.btnlayout.addWidget(self.strFrame_six)        
        
        self.one_layout = QtWidgets.QHBoxLayout()
        self.strLayout.addLayout(self.one_layout, 0, 0, 1, 1)        
        self.one_layout.addWidget(self.cust_checked)
        self.one_layout.addWidget(self.attrlist)
        self.one_layout.addWidget(self.valueset_lo_one)
        self.one_layout.addWidget(self.valueset_hi_one)       

        self.two_layout = QtWidgets.QHBoxLayout()
        self.strLayout_two.addLayout(self.two_layout, 1, 0, 1, 1)        
        self.two_layout.addWidget(self.cust_checked_two)
        self.two_layout.addWidget(self.attrlist_two)
        self.two_layout.addWidget(self.valueset_lo_two)
        self.two_layout.addWidget(self.valueset_hi_two)        
        
        self.three_layout = QtWidgets.QHBoxLayout()
        self.strLayout_three.addLayout(self.three_layout, 2, 0, 1, 1)        
        self.three_layout.addWidget(self.cust_checked_three)
        self.three_layout.addWidget(self.attrlist_three)
        self.three_layout.addWidget(self.valueset_lo_three)
        self.three_layout.addWidget(self.valueset_hi_three)

        self.four_layout = QtWidgets.QHBoxLayout()
        self.strLayout_four.addLayout(self.four_layout, 3, 0, 1, 1)        
        self.four_layout.addWidget(self.cust_checked_four)
        self.four_layout.addWidget(self.attrlist_four)
        self.four_layout.addWidget(self.valueset_lo_four)
        self.four_layout.addWidget(self.valueset_hi_four)
        
        self.five_layout = QtWidgets.QHBoxLayout()
        self.strLayout_five.addLayout(self.five_layout, 4, 0, 1, 1)        
        self.five_layout.addWidget(self.cust_checked_five)
        self.five_layout.addWidget(self.attrlist_five)
        self.five_layout.addWidget(self.valueset_lo_five)
        self.five_layout.addWidget(self.valueset_hi_five)

        self.six_layout = QtWidgets.QHBoxLayout()
        self.strLayout_six.addLayout(self.six_layout, 5, 0, 1, 1)        
        self.six_layout.addWidget(self.cust_checked_six)
        self.six_layout.addWidget(self.attrlist_six)
        self.six_layout.addWidget(self.valueset_lo_six)
        self.six_layout.addWidget(self.valueset_hi_six)
        
        self.sev_layout = QtWidgets.QHBoxLayout()
        self.strLayout_six.addLayout(self.sev_layout, 6, 0, 1, 1)
        self.set_dir =["none", "circle", "orbit", "fig_eight"]
        # self.cust_sev_checked = QtWidgets.QCheckBox()
        # self.v_label = QtWidgets.QLabel("Amount to animate")
        self.dir_list = QtWidgets.QComboBox()
        self.dir_list.addItems(self.set_dir)   
        # self.sev_layout.addWidget(self.cust_sev_checked)
        self.sev_layout.addWidget(self.dir_list)
        # self.sev_layout.addWidget(self.sev_layout)


        self.btnlayout.addWidget(self.frames_label)
        self.btnlayout.addWidget(self.frames)
        self.btnlayout.addWidget(self.ctrl_button)
        self.setLayout(self.layout)
        self.show()

    def build_ctrl_annot_one(self):
        fnd_dir = str(self.dir_list.currentText())
        cust_dict = {}
        get_frames = float(self.frames.text())
        drp_attr = str(self.attrlist.currentText())
        get_val_one_1 = float(self.valueset_lo_one.text())
        get_val_one_2 = float(self.valueset_hi_one.text())
        set_val_1 = get_val_one_1, get_val_one_2
        # cust_attr_one = str(self.attr_line_edit.text())
        cust_check_qry = self.cust_checked
        if cust_check_qry.isChecked():
            make_dict_part = {drp_attr : set_val_1 }
            cust_dict.update(make_dict_part)
        drp_attr_two = str(self.attrlist_two.currentText())
        get_val_two_1 = float(self.valueset_lo_two.text())
        get_val_two_2 = float(self.valueset_hi_two.text())
        set_val_2= get_val_two_1, get_val_two_2
        cust_check_qry_two = self.cust_checked_two
        if cust_check_qry_two.isChecked():
            make_dict_part = {drp_attr_two : set_val_2}
            cust_dict.update(make_dict_part)
        drp_attr_three = str(self.attrlist_three.currentText())
        get_val_three_1 = float(self.valueset_lo_three.text())
        get_val_three_2 = float(self.valueset_hi_three.text())
        set_val_3 = get_val_three_1, get_val_three_2
        cust_check_qry_three = self.cust_checked_three
        if cust_check_qry_three.isChecked():
            make_dict_part = {drp_attr_three : set_val_3}
            cust_dict.update(make_dict_part)      
        drp_attr_four = str(self.attrlist_four.currentText())
        get_val_four_1 = float(self.valueset_lo_four.text())
        get_val_four_2 = float(self.valueset_hi_four.text())
        set_val_4 = get_val_four_1, get_val_four_2
        cust_check_qry_four = self.cust_checked_four
        if cust_check_qry_four.isChecked():
            make_dict_part = {drp_attr_four : set_val_4}
            cust_dict.update(make_dict_part)  
        drp_attr_five = str(self.attrlist_five.currentText())
        get_val_five_1 = float(self.valueset_lo_five.text())
        get_val_five_2 = float(self.valueset_hi_five.text())
        set_val_5 = get_val_five_1, get_val_five_2
        cust_check_qry_five = self.cust_checked_five
        if cust_check_qry_five.isChecked():
            make_dict_part = {drp_attr_five : set_val_5}
            cust_dict.update(make_dict_part) 
        drp_attr_six = str(self.attrlist_six.currentText())
        get_val_six_1 = float(self.valueset_lo_six.text())
        get_val_six_2 = float(self.valueset_hi_six.text())
        set_val_6 = get_val_six_1, get_val_six_2
        cust_check_qry_six = self.cust_checked_six
        if cust_check_qry_six.isChecked():
            make_dict_part = {drp_attr_six : set_val_6}
            cust_dict.update(make_dict_part)         
        access_main = annot_range_win()
        access_main.test_sel_callup( get_frames, cust_dict, fnd_dir)
        self.close()
        
class get_ctrls_val_frm(QtWidgets.QWidget):
    def __init__(self, ):
        super(get_ctrls_val_frm, self).__init__()
        self.initUI()

    def initUI(self):  
        sel_obj = mc.ls(sl=1)[0]
        if len(mc.ls(sl=1))>0:
            each_attr = [(the_item) for the_item in mc.listAttr (sel_obj, k=1) if 'visibility' not in the_item]
        else:
            each_attr = ["tx", "ty", "tz", "rx", "ry", "rz"]
        title = "Set Values for review titles"   
        self.setWindowTitle(title)
        self.layout = QtWidgets.QVBoxLayout()
        self.btnlayout = QtWidgets.QGridLayout()
        # self.playlist_names = QComboBox()
        self.value_label = QtWidgets.QLabel("Amount to animate")
        self.valueset = QtWidgets.QLineEdit("1")
        self.frames_label = QtWidgets.QLabel("accross frames")
        self.frames = QtWidgets.QLineEdit("10")
        self.attr_label = QtWidgets.QLabel("Attr to animate")
        self.attrlist = QtWidgets.QComboBox()
        self.attr_cust_label = QtWidgets.QLabel("Enter custom attr if preferred:")
        self.cust_checked = QtWidgets.QCheckBox()
        self.attr_line_edit = QtWidgets.QLineEdit('translateY')
        self.attrlist.addItems(each_attr)
        self.layout.addLayout(self.btnlayout)
        self.ctrl_button = QtWidgets.QPushButton("annot controllers")
        self.ctrl_button.clicked.connect(lambda: self.build_ctrl_annot())
        self.btnlayout.addWidget(self.attr_label)
        self.btnlayout.addWidget(self.attrlist)
        self.btnlayout.addWidget(self.attr_cust_label)
        self.btnlayout.addWidget(self.cust_checked)
        self.btnlayout.addWidget(self.attr_line_edit)
        self.btnlayout.addWidget(self.value_label)
        self.btnlayout.addWidget(self.valueset)
        self.btnlayout.addWidget(self.frames_label)
        self.btnlayout.addWidget(self.frames)
        self.btnlayout.addWidget(self.ctrl_button)
        self.setLayout(self.layout)
        self.show()        
        
    def build_ctrl_annot(self):
        use_cust = False
        get_val = float(self.valueset.text())
        get_frames = float(self.frames.text())
        drp_attr = str(self.attrlist.currentText())
        attr_line_edit = str(self.frames.text())
        cust_check_qry = self.cust_checked
        if cust_check_qry.isChecked():
            use_cust = True
        else:
            use_cust = False
        access_main = annot_range_win()
        access_main.ctrlr_set_annot(get_val, get_frames, drp_attr, attr_line_edit, use_cust)
        self.close()        
        
class get_val_frm(QtWidgets.QWidget):
    def __init__(self, ):
        super(get_val_frm, self).__init__()
        self.initUI()

    def initUI(self):  
        title = "Set Values for review titles"   
        self.setWindowTitle(title)
        self.layout = QtWidgets.QVBoxLayout()
        self.btnlayout = QtWidgets.QGridLayout()
        # self.playlist_names = QComboBox()
        self.value_label = QtWidgets.QLabel("Amount to animate")
        self.valueset = QtWidgets.QLineEdit("1")
        self.frames_label = QtWidgets.QLabel("accross frames")
        self.frames = QtWidgets.QLineEdit("8")
        # self.playlist_names.addItems(detailMessge)
        # self.layout.addWidget(self.playlist_names)
        self.layout.addLayout(self.btnlayout)
        self.sel_button = QtWidgets.QPushButton("annot attr")
        self.sel_button.clicked.connect(lambda: self.build_annot())
        self.btnlayout.addWidget(self.value_label)
        self.btnlayout.addWidget(self.valueset)
        self.btnlayout.addWidget(self.frames_label)
        self.btnlayout.addWidget(self.frames)
        self.btnlayout.addWidget(self.sel_button)
        self.setLayout(self.layout)
        self.show()
        
    def build_annot(self):
        get_val = self.valueset.text()
        get_val = float(get_val)
        get_frames = self.frames.text()
        get_frames = float(get_frames)
        access_main = annot_range_win()
        access_main.trigger_annot(get_val, get_frames)
        self.close()
