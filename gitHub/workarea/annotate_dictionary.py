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

        
class annot_range_win(QtWidgets.QMainWindow):
    def __init__(self):
        super(annot_range_win, self).__init__()
        self.initUI()

    def initUI(self):    
        """
        Main window setup
        """
        self.setWindowTitle("Annotate")

        self.central_widget=QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.master_layout=QtWidgets.QGridLayout(self.central_widget)
        self.master_layout.setAlignment(QtCore.Qt.AlignTop)
        file_menu = QtWidgets.QMenu('&Help', self)
        self.menuBar().addMenu(file_menu)
        file_menu.addAction('&Open help page...', self.help_page_launch, 'Ctrl+L')

        self.layout = QtWidgets.QVBoxLayout()
        self.btnlayout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.btnlayout)
        self.master_layout.addLayout(self.layout, 0,0,1,1)
        self.annot_sel_button =QtWidgets. QPushButton("Annotate Selected")
        self.annot_sel_button.setToolTip("Pipeline issues/data retrieval/IT")
        self.annot_sel_button.clicked.connect(lambda: self.annotations_list())
        self.auto_annot_button = QtWidgets.QPushButton("Auto Annotate")
        self.auto_annot_button.clicked.connect(lambda: self.dealers_choice())                  
        self.colour_annot_button = QtWidgets.QPushButton("Change Annot Colours")
        self.colour_annot_button.clicked.connect(lambda:self._change_anot_colors())  
        self.mrph_annot_button = QtWidgets.QPushButton("test morphs Annot")
        self.mrph_annot_button.clicked.connect(lambda: self.test_morph())       
        self.ctrl_annot_button = QtWidgets.QPushButton("test ctrls under selected")
        self.ctrl_annot_button.clicked.connect(lambda: self.ctrlr_annot())     
        self.set_annot_button = QtWidgets.QPushButton("test set")
        self.set_annot_button.clicked.connect(lambda: self.set_annot()        
        self.attr_annot_button = QtWidgets.QPushButton("attribute")
        self.attr_annot_button.clicked.connect(lambda: self.test_attr())      
        self.sel_annot_button = QtWidgets.QPushButton("selected")
        self.sel_annot_button.clicked.connect(lambda: self.test_sel())     
        self.recon_annot_button = QtWidgets.QPushButton("reconstrain title")
        self.recon_annot_button.clicked.connect(lambda: self.retape_to_selection())   
        self.mk_annot_button = QtWidgets.QPushButton("Make title")
        self.mk_annot_button.clicked.connect(lambda: self.make_arbitrary_title()) 
        self.btnlayout.addWidget(self.auto_annot_button)     
        self.btnlayout.addWidget(self.annot_sel_button)
        self.btnlayout.addWidget(self.colour_annot_button)
        self.btnlayout.addWidget(self.mrph_annot_button)
        self.btnlayout.addWidget(self.ctrl_annot_button)
        self.btnlayout.addWidget(self.set_annot_button)
        self.btnlayout.addWidget(self.attr_annot_button)
        self.btnlayout.addWidget(self.sel_annot_button)
        self.btnlayout.addWidget(self.recon_annot_button)
        self.btnlayout.addWidget(self.mk_annot_button)

        self.setLayout(self.layout)                                              
                                              
    def help_page_launch(self):
        """
        opens the helppage for tool in confluence
        """
        url=''
        subprocess.Popen('gio open %s' % url, stdout=subprocess.PIPE, shell=True) 
                                              
                                              
    def point_const(self, arg=None):
        getSel=mc.ls(sl=1, fl=1)
        self.point_const_callup(getSel)

    def point_const_callup(self, getSel):
        edgeBucket=[]
        if ".vtx[" in getSel[0]:
            pass
        else:
            print "You need to make some vertex selections for this tool to operate on."
        for each in getSel:
            print each
            if ":" in each:
                findName=each.split(":")[-1:][0]
            else:
                findName=each
            if ":" in getSel[0]:
                getObj=getSel[0].split(":")[-1:]
            else:
                getObj=getSel
            getObj=getObj[0].split('.')[0]
            getUVmap = mc.polyListComponentConversion(each, fv=1, tuv=1)
            getCoords=mc.polyEditUV(getUVmap, q=1)
            getNew=mc.spaceLocator(n=str(findName)+"ploc")
            mc.select(each, r=1)
            mc.select(getNew[0], add=1)
            buildConst=mc.pointOnPolyConstraint(each, getNew[0], mo=0, offset=(0.0, 0.0, 0.0))
            propShape = getObj.replace("Shape", "")
            getPropName = buildConst[0]
            mc.setAttr(getPropName+"."+propShape+"U0", getCoords[0])
            mc.setAttr(getPropName+"."+propShape+"V0", getCoords[1])   
                                              
    def dealers_choice(self):
        collectedVtx=[]
        if len(mc.ls(sl=1))<1:
            methodSpacerig = [(each) for each in mc.ls("*:animGeo") if mc.nodeType(each) == "transform" and mc.listRelatives(each, p=1) == None]
            nameSpacerig = [(each) for each in mc.ls("*:*") if mc.nodeType(each) == "transform" and mc.listRelatives(each, p=1) == None]
            normalrig = [(each) for each in mc.ls("*") if mc.nodeType(each) == "transform" and mc.listRelatives(each, p=1) == None]
            rigs = nameSpacerig+methodSpacerig+normalrig
            for item in rigs:
                if mc.listRelatives(item, ad=1, type="mesh"):
                    getparentObj=[(each) for each in mc.listRelatives(item, ad=1, type="mesh")][0]
                    # print getparentObj
                    getvert=getparentObj+".vtx[0]"
                    collectedVtx.append(getvert)
            mc.select(collectedVtx, r=1)
            self.annotations_list()                                  
    def dealers_choice(self):
        collectedVtx=[]
        if len(mc.ls(sl=1))<1:
            methodSpacerig = [(each) for each in mc.ls("*:animGeo") if mc.nodeType(each) == "transform" and mc.listRelatives(each, p=1) == None]
            nameSpacerig = [(each) for each in mc.ls("*:*") if mc.nodeType(each) == "transform" and mc.listRelatives(each, p=1) == None]
            normalrig = [(each) for each in mc.ls("*") if mc.nodeType(each) == "transform" and mc.listRelatives(each, p=1) == None]
            rigs = nameSpacerig+methodSpacerig+normalrig
            for item in rigs:
                if mc.listRelatives(item, ad=1, type="mesh"):
                    getparentObj=[(each) for each in mc.listRelatives(item, ad=1, type="mesh")][0]
                    # print getparentObj
                    getvert=getparentObj+".vtx[0]"
                    collectedVtx.append(getvert)
            mc.select(collectedVtx, r=1)
            self.annotations_list()                                                        

    def _change_anot_colors(self):
        getgrp = mc.ls(sl=1)
        if len(getgrp)==0:
            getgrp = mc.ls(type="annotationShape")
        elif mc.ls(sl=1)>0:
            getgrp=[(each) for item in getgrp for each in mc.listRelatives(item, ad=1, type="annotationShape")]
        else:
            print "annotations not present in scene"
            return
        for each in getgrp:
            random.shuffle(colorlist, random.random)
            offset = colorlist[0]
            mc.setAttr(each+".overrideEnabled", 1)
            mc.setAttr(each+".overrideColor", offset)                             
                                              
    def setTextVal(self, typeNode, textString):
        hexValues = []
        for character in textString:
            hexValues.append(character.encode('hex'))
        attrVal = ' '.join(hexValues)
        mc.setAttr(typeNode+'.textInput', attrVal, type = 'string')
                                              
    def type_list_preset(self, item, getTitle, get_loc):      
        transformWorldMatrix=mc.xform(get_loc, q=True, ws=1, t=True)
        plusnum=random.uniform(.2,3)
        newTransform = [transformWorldMatrix[0], transformWorldMatrix[1]+plusnum, transformWorldMatrix[2]]
        mm.eval('typeCreateText;')
        sel_typ = [(hist_type) for hist_type in mc.listHistory(mc.ls(sl=1)) if mc.nodeType(hist_type) == "type"][0]
        self.setTextVal(sel_typ, str(getTitle))
        selectMesh = [(each) for each in mc.listHistory(sel_typ) if mc.nodeType(each) == "transform"][0]
        mc.select(selectMesh, r=1)
        mc.CenterPivot()
        buildParent = mc.group(n=getTitle+"_grp")
        mc.parentConstraint(get_loc, buildParent, mo=0)
        mc.scaleConstraint(get_loc, buildParent, mo=0)
        return buildParent                              
                                              
    def annotations_list_preset(self, item, getTitle, getNew, get_color):
        getName=["namespace"]
        annot_title_grp=mc.ls("*ANNOTATE_GRP*")
        if len(annot_title_grp)<1:
            annot_title_grp=mc.CreateEmptyGroup()
            mc.rename(annot_title_grp, "ANNOTATE_GRP")
            annot_title_grp=mc.ls("*ANNOTATE_GRP*")
        else:
            annot_title_grp=mc.ls("*ANNOTATE_GRP*")             
        random.shuffle(colorlist, random.random)
        offset = colorlist[0]
        mc.select(item, r=1)
        transformWorldMatrix=mc.xform(getNew, q=True, ws=1, t=True)
        plusnum=random.uniform(.2,3)
        newTransform = [transformWorldMatrix[0], transformWorldMatrix[1]+plusnum, transformWorldMatrix[2]]
        getAnnot = mc.annotate(getNew, p=newTransform)
        buildParent = mc.group(n=getTitle+"_grp")
        mc.CenterPivot()
        mc.setAttr(getAnnot+".text", getTitle, type="string")
        mc.setAttr(getAnnot+".overrideEnabled", 1)
        mc.setAttr(getAnnot+".overrideColor", get_color)
        getparent = mc.listRelatives(getAnnot, p=1)[0]
        mc.pointConstraint(getNew, buildParent, mo=1)
        new_name_annot = getTitle+"_ant"
        mc.rename(getparent, getTitle+"_ant")
        # mc.rename(getNew, item)
        mc.parent(buildParent, annot_title_grp)
        return new_name_annot                                              

    def set_annot(self):
        # inst_win = get_sel_val_frm()
        inst_win = get_set_sel_val()
    

    def ctrlr_annot(self):
        # inst_win = get_ctrls_val_frm()
        inst_win = get_set_sel_val()        
                                              
    def ctrlr_set_annot(self, get_val, get_frames, drp_attr, attr_line_edit, use_cust):
        parentObj = mc.ls(sl=1)[0]
        if use_cust == False:
            drvn_attr = drp_attr
        else: 
            drvn_attr = attr_line_edit
        trgt_ctrlrs=[(each) for each in mc.listRelatives(parentObj, ad=1, type="transform") if "_ctrl" in each and "_grp" not in each]
        getrange = len(trgt_ctrlrs)
        getstrt = mc.currentTime(q=1)
        get_loc,create_shade_node, annot_title_grp  = self.build_the_cam_titles()
        for each in trgt_ctrlrs:
            # get_attrs_chn = [(the_item) for the_item in mc.listAttr (each, k=1) if 'visibility' not in the_item]
            get_cur = mc.currentTime(q=1)
            getstartval = get_cur
            gethalf = get_frames/2
            getactiveval = get_cur+gethalf
            getendval = get_cur+get_frames                                        
            try:
                # for item in get_attrs_chn:
                title_content = each+"."+drvn_attr
                new_name_annot = self.type_list_preset(mc.ls(sl=1)[0], title_content, get_loc)
                mc.select(new_name_annot, r=1)
                mc.hyperShade(assign=str(create_shade_node)) 
                mc.parent(new_name_annot, annot_title_grp)
                # mc.setAttr(new_name_annot+"Shape.displayArrow", 0)
                mc.setKeyframe(new_name_annot, at="visibility", v=0.0, time=(getstartval)) 
                mc.setKeyframe(each, at=drvn_attr, v=0.0, time=(getstartval))
                mc.setKeyframe(new_name_annot, at="visibility", v=1.0, time=(getstartval+1))
                mc.setKeyframe(each, at=drvn_attr, v=get_val, time=(getactiveval))
                mc.setKeyframe(new_name_annot, at="visibility", v=1.0, time=(getendval-1))
                mc.setKeyframe(each, at=drvn_attr, v=0.0, time=(getendval))
                mc.setKeyframe(new_name_annot, at="visibility", v=0.0, time=(getendval))    
                mc.currentTime(getendval)
            except:
                pass
        mm.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
        mc.setAttr( "{}.scaleZ".format(annot_title_grp[0]), 0.2)        
        mc.setAttr( "{}.scaleX".format(annot_title_grp[0]), 0.2)        
        mc.setAttr( "{}.scaleY".format(annot_title_grp[0]), 0.2)   
                                              
    def cam_constraint(self, tape_thing_to_cam):
        if mc.objExists("*:*.cameraPreset") == True:
            getCameraGrp=mc.ls("*:*.cameraPreset")[0]
            getNode=getCameraGrp.split(".")[0]
            selcnst = mc.parentConstraint(getNode, tape_thing_to_cam, mo=0)
            mc.rename(selcnst, 'annot_duct_tape_par')
        elif mc.objExists("shotcam*:camera") == True:
            getCameraGrp=mc.ls("shotcam*:camera")[0]
            getNode=getCameraGrp.split(".")[0]
            selcnst = mc.parentConstraint(getNode, tape_thing_to_cam, mo=0)
            mc.rename(selcnst, 'annot_duct_tape_par')
        else:
            getNode = [(mc.listRelatives(item, ap=1, type='transform')[0]) for item in mc.ls(type = 'camera') if 'persp' in item][0]
            try:
                selcnst = mc.parentConstraint(getNode, tape_thing_to_cam, mo=0)
                mc.rename(selcnst, 'annot_duct_tape_par')
            except:
                print "skipping {}".format(tape_thing_to_cam)
                pass


    def retape_to_selection(self):
        try:
            getNode = mc.ls(sl=1)[0]
            if mc.objExists("annot_loc_trn") == True:
                print "Label exists -  will skip creating it"
                print 'taping label to selected'
                try:
                    mc.delete('annot_duct_tape_par')
                except:
                    pass
                try:
                    selcnst = mc.parentConstraint(getNode, 'annot_loc_trn', mo=0)
                    mc.rename(selcnst, 'annot_duct_tape_par')
                except:
                    print "Nothing selected. skipping"
                    pass
            else:
                try:
                    get_loc=mc.ls("*_ploc")[0]
                except:
                    get_loc=mc.spaceLocator(n="annot_ploc")
                    get_loc=get_loc[0]  
                mc.select(get_loc, r=1)
                mc.group()
                mc.rename(mc.ls(sl=1)[0], 'annot_loc_trn')
                print 'taping label to selected'
                try:
                    selcnst = mc.parentConstraint(getNode, 'annot_loc_trn', mo=0)
                    mc.rename(selcnst, 'annot_duct_tape_par')
                except:
                    print "Nothing selected. skipping"
                    pass
        except:
            print "something needs to be selected for stuff to happen here"
            pass                                              
                                              
    def make_arbitrary_title(self):
        get_loc,create_shade_node, annot_title_grp  = self.build_the_cam_titles()
        label = "label"
        title_set = "label"
        new_name_annot = self.type_list_preset(mc.ls(sl=1)[0], title_set, get_loc)
        mc.select(new_name_annot, r=1)
        mc.hyperShade(assign=str(create_shade_node)) 
        mc.parent(new_name_annot, annot_title_grp)                                              
                                              
    def test_controllers(self):
        parentObj = mc.ls(sl=1)[0]
        try:
            get_loc=mc.ls("*_ploc")[0]
            # if len(get_loc)<1:
        except:
            get_loc=mc.spaceLocator(n="annot_ploc")
            get_loc=get_loc[0]  
        targetAttrs=[(each) for each in mc.listRelatives(parentObj, ad=1, type="transform") if "_ctrl" in each]
        getrange = len(targetAttrs)
        getstrt = mc.currentTime(q=1)
        get_loc,create_shade_node, annot_title_grp  = self.build_the_cam_titles()
        for each in targetAttrs:
            get_attrs_chn = [(the_item) for the_item in mc.listAttr (each, k=1) if 'visibility' not in the_item]
            get_cur = mc.currentTime(q=1)
            getstartval = get_cur
            getactiveval = get_cur+5
            getendval = get_cur+10.0                                              
            try:
                for item in get_attrs_chn:
                    title_content = each+"."+item
                    new_name_annot = self.type_list_preset(mc.ls(sl=1)[0], title_content, get_loc)
                    mc.select(new_name_annot, r=1)
                    mc.hyperShade(assign=str(create_shade_node)) 
                    mc.parent(new_name_annot, annot_title_grp)
                    # mc.setAttr(new_name_annot+"Shape.displayArrow", 0)
                    mc.setKeyframe(new_name_annot, at="visibility", v=0.0, time=(getstartval)) 
                    mc.setKeyframe(each, at=item, v=0.0, time=(getstartval))
                    mc.setKeyframe(new_name_annot, at="visibility", v=1.0, time=(getstartval+1))
                    mc.setKeyframe(each, at=item, v=1.0, time=(getactiveval))
                    mc.setKeyframe(new_name_annot, at="visibility", v=1.0, time=(getendval-1))
                    mc.setKeyframe(each, at=item, v=0.0, time=(getendval))
                    mc.currentTime(getendval)
            except:
                pass
        mm.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
        mc.setAttr( "{}.scaleZ".format(annot_title_grp[0]), 0.2)        
        mc.setAttr( "{}.scaleX".format(annot_title_grp[0]), 0.2)        
        mc.setAttr( "{}.scaleY".format(annot_title_grp[0]), 0.2)    
                                              
    def test_sel(self):
        # inst_win = get_sel_val_frm()
        inst_win = get_set_sel_val()
    
    def test_sel_callup(self, get_frames, cust_dict, fnd_dir):
        #set annotation
        targetAttrs = mc.ls(sl=1)
        getrange = len(targetAttrs)
        get_cur  = mc.currentTime(q=1)
        get_loc,create_shade_node, annot_title_grp  = self.build_the_cam_titles()
        #get the text ready   
        getName=["namespace"]                   
        for each in targetAttrs:
            # print each
            try:
                mc.sets(each, add=ctrl_set_name)
            except:
                pass
            try:
                for key, value in cust_dict.items():
                    if fnd_dir == "none":
                        # print key, value[0], value[1]
                        value_lo=value[0]
                        value_hi=value[1]
                        getstartval = get_cur
                        gethalf = get_frames/3
                        getactiveval_lo = get_cur+gethalf
                        getactiveval_hi = get_cur+gethalf+gethalf
                        getendval = get_cur+get_frames
                        title_set = each+"."+key
                        new_name_annot = self.type_list_preset(mc.ls(sl=1)[0], title_set, get_loc)
                        mc.select(new_name_annot, r=1)
                        mc.hyperShade(assign=str(create_shade_node)) 
                        mc.parent(new_name_annot, annot_title_grp)
                        # mc.setAttr(new_name_annot+"Shape.displayArrow", 0)
                        mc.setKeyframe(new_name_annot, at="visibility", v=0.0, time=(getstartval)) 
                        mc.setKeyframe(each, at=key, v=0.0, time=(getstartval))
                        mc.setKeyframe(new_name_annot, at="visibility", v=1.0, time=(getstartval+1))
                        mc.setKeyframe(each, at=key, v=value_lo, time=(getactiveval_lo))
                        mc.setKeyframe(each, at=key, v=value_hi, time=(getactiveval_hi))
                        mc.setKeyframe(new_name_annot, at="visibility", v=1.0, time=(getendval-1))
                        mc.setKeyframe(each, at=key, v=0.0, time=(getendval))
                        mc.setKeyframe(new_name_annot, at="visibility", v=0.0, time=(getendval))    
                        mc.currentTime(getendval)                    
                    if fnd_dir == "fig_eight":
                        size_area=value[0]*-1
                        if "rotateZ" or "translateZ" in key:
                            rotate_plane = "Z"
                        elif "rotateZ" or "translateZ" in key:
                            rotate_plane = "X"
                        getstartval = get_cur
                        get_portion = get_frames/20 
                        getendval = get_cur+get_frames
                        self.create_the_anim_loc(get_cur, get_portion, each, rotate_plane, size_area)
                        new_name_annot = self.type_list_preset(mc.ls(sl=1)[0], each, get_loc)
                        mc.select(new_name_annot, r=1)
                        mc.hyperShade(assign=str(create_shade_node))      
                        mc.parent(new_name_annot, annot_title_grp)
                        mc.setKeyframe(new_name_annot, at="visibility", v=0.0, time=(getstartval)) 
                        time_frame = get_cur+get_portion*2
                        mc.setKeyframe(new_name_annot, at="visibility", v=1.0, time=time_frame)
                        time_frame = get_cur+get_portion*19
                        mc.setKeyframe(new_name_annot, at="visibility", v=1.0, time=time_frame)
                        time_frame = get_cur+get_portion*20
                        mc.setKeyframe(new_name_annot, at="visibility", v=0.0, time=time_frame)    
                        mc.currentTime(getendval)                                              
                   if fnd_dir == "circle":
                        size_area=value[0]*-1
                        if "rotateZ" or "translateZ" in key:
                            rotate_plane = "Z"
                        elif "rotateZ" or "translateZ" in key:
                            rotate_plane = "X"
                        getstartval = get_cur
                        get_portion = get_frames/20 
                        getendval = get_cur+get_frames
                        self.create_circle_anim_loc(get_cur, get_portion, each, rotate_plane, size_area)
                        new_name_annot = self.type_list_preset(mc.ls(sl=1)[0], each, get_loc)
                        mc.select(new_name_annot, r=1)
                        mc.hyperShade(assign=str(create_shade_node)) 
                        mc.parent(new_name_annot, annot_title_grp)
                        mc.setKeyframe(new_name_annot, at="visibility", v=0.0, time=(getstartval)) 
                        time_frame = get_cur+get_portion*2
                        mc.setKeyframe(new_name_annot, at="visibility", v=1.0, time=time_frame)
                        time_frame = get_cur+get_portion*19
                        mc.setKeyframe(new_name_annot, at="visibility", v=1.0, time=time_frame)
                        time_frame = get_cur+get_portion*20
                        mc.setKeyframe(new_name_annot, at="visibility", v=0.0, time=time_frame)    
                        mc.currentTime(getendval)
                    if fnd_dir == "orbit":
                        size_area=value[0]*-1
                        if "rotateZ" or "translateZ" in key:
                            rotate_plane = "Z"
                        elif "rotateZ" or "translateZ" in key:
                            rotate_plane = "X"
                        getstartval = get_cur
                        get_portion = get_frames/20 
                        getendval = get_cur+get_frames
                        self.create_orbit_anim_loc(get_cur, get_portion, each, rotate_plane, size_area)
                        new_name_annot = self.type_list_preset(mc.ls(sl=1)[0], each, get_loc)
                        mc.select(new_name_annot, r=1)
                        mc.hyperShade(assign=str(create_shade_node)) 
                        mc.parent(new_name_annot, annot_title_grp)                                              
                        mc.setKeyframe(new_name_annot, at="visibility", v=0.0, time=(getstartval)) 
                        time_frame = get_cur+get_portion*2
                        mc.setKeyframe(new_name_annot, at="visibility", v=1.0, time=time_frame)
                        time_frame = get_cur+get_portion*19
                        mc.setKeyframe(new_name_annot, at="visibility", v=1.0, time=time_frame)
                        time_frame = get_cur+get_portion*20
                        mc.setKeyframe(new_name_annot, at="visibility", v=0.0, time=time_frame)    
                        mc.currentTime(getendval)                                
            except:
                pass
        mm.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
        mc.setAttr( "{}.scaleZ".format(annot_title_grp[0]), 0.2)        
        mc.setAttr( "{}.scaleX".format(annot_title_grp[0]), 0.2)        
        mc.setAttr( "{}.scaleY".format(annot_title_grp[0]), 0.2)        
                                              
    def create_the_anim_loc(self, get_cur, get_portion, get_obj, directional_plane, size_area):
        dictionary_saved = []
        anim_loc_name = "{}_anim_loc".format(get_obj)
        anim_loc_grp = "{}_anim_grp".format(get_obj)
        if mc.objExists(anim_loc_name) == True:
            anim_loc_grp = mc.ls(anim_loc_grp)[0]
            anim_loc = mc.ls(anim_loc_name)[0]
        else:
            anim_loc = mc.spaceLocator(n=anim_loc_name)
            mc.select(cl=1)
            mk_grp=mc.CreateEmptyGroup()
            mc.rename(mk_grp, anim_loc_grp)
            mc.parent(anim_loc, anim_loc_grp)                    
        val01 = [0.084, 0.0, 0.012,0.0, 0.0, 0.0]
        time_frame = get_cur
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val01, time_frame)
        val02 = [0.727, 0.0, .129, 0.0, -20, 0.0]
        time_frame = get_cur+get_portion*2
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val02, time_frame)
        val03 = [1.032, 0.0, .785,0.0, -30, 0.0]
        time_frame = get_cur+get_portion*3
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val03, time_frame)
        val04 = [0.985, 0.0, 1.406,0.0, 0.0, 0.0]
        time_frame = get_cur+get_portion*4
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val04, time_frame)
        val05 = [0.544, 0.0, 1.914,0.0, -40, 0.0]
        time_frame = get_cur+get_portion*5
        dictionary_saved.append(time_frame)         
        self.transform_anim(anim_loc, val05, time_frame)
        val06 = [-0.086, 0.0, 2.058,0.0, -90, 0.0]
        time_frame = get_cur+get_portion*6
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val06, time_frame)
        val07 = [-0.701, 0.0, 1.799,0.0, -40, 0.0]
        time_frame = get_cur+get_portion*7
        dictionary_saved.append(time_frame)
        self.transform_anim( anim_loc, val07, time_frame)
        val08 = [-1.026, 0.0, 1.257,0.0, 0.0, 0.0]
        time_frame = get_cur+get_portion*8
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val08, time_frame)
        val09 = [-1.011, 0.0, 0.565,0.0, 30, 0.0]              
        time_frame = get_cur+get_portion*9
        dictionary_saved.append(time_frame)
        self.transform_anim( anim_loc, val09, time_frame)
        val10 = [-0.496, 0.0, 0.035,0.0, 20, 0.0]
        time_frame = get_cur+get_portion*10
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val10, time_frame)               
        val12 = [0.717, 0.0, -.0142,0.0, -20, 0.0]
        time_frame = get_cur+get_portion*12
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val12, time_frame)
        val13 = [1.055, 0.0, -0.786,0.0, -30, 0.0]
        time_frame = get_cur+get_portion*13
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val13, time_frame)
        val14 = [0.964, 0.0, -1.441,0.0, 0.0, 0.0]
        time_frame = get_cur+get_portion*14
        dictionary_saved.append(time_frame)
        self.transform_anim( anim_loc, val14, time_frame)
        val15 = [0.529, 0.0, -1.926,0.0, 40.0, 0.0]
        time_frame = get_cur+get_portion*15
        dictionary_saved.append(time_frame)
        self.transform_anim( anim_loc, val15, time_frame)          
        val16 = [-0.121, 0.0, -2.049,0.0, 90.0, 0.0]
        time_frame = get_cur+get_portion*16
        dictionary_saved.append(time_frame)
        self.transform_anim( anim_loc, val16, time_frame)
        val17 = [-0.708, 0.0, -1.799, 0.0, -30.0, 0.0]
        time_frame = get_cur+get_portion*17
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val17, time_frame)
        val18 = [-1.054, 0.0, -1.195, 0.0, 0.0, 0.0]
        time_frame = get_cur+get_portion*18
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val18, time_frame)                         
        val19 = [-.96, 0.0, -0.605,0.0, 40.0, 0.0]
        time_frame = get_cur+get_portion*19
        dictionary_saved.append(time_frame)
        self.transform_anim( anim_loc, val19, time_frame)
        val20 = [-0.541, 0.0, -0.09,0.0, 20.0, 0.0]
        time_frame = get_cur+get_portion*20
        dictionary_saved.append(time_frame)
        self.transform_anim( anim_loc, val20, time_frame)
        mk_cnstrnt = mc.parentConstraint(get_obj, anim_loc_grp, mo=0)                                         
        mc.delete(mk_cnstrnt)
        if "X" in directional_plane:
            print "X"
            mc.setAttr("{}.rotateX".format(anim_loc_grp), -90)
            mc.setAttr("{}.rotateY".format(anim_loc_grp), 90)
        elif "Z" in directional_plane:
            print "Z"
            mc.setAttr("{}.rotateX".format(anim_loc_grp), -90)
        mc.setAttr("{}.scaleX".format(anim_loc_grp), size_area)
        mc.setAttr("{}.scaleY".format(anim_loc_grp), size_area)
        mc.setAttr("{}.scaleZ".format(anim_loc_grp), size_area)
        self.control_anim(dictionary_saved, get_obj, anim_loc[0])
        mc.delete(anim_loc_grp)                                              
                                              
    def create_circle_anim_loc(self, get_cur, get_portion, get_obj, directional_plane, size_area):
        dictionary_saved = []
        anim_loc_name = "{}_anim_loc".format(get_obj)
        anim_loc_grp = "{}_anim_grp".format(get_obj)
        if mc.objExists(anim_loc_name) == True:
            anim_loc_grp = mc.ls(anim_loc_grp)[0]
            anim_loc = mc.ls(anim_loc_name)[0]
        else:
            anim_loc = mc.spaceLocator(n=anim_loc_name)
            mc.select(cl=1)
            mk_grp=mc.CreateEmptyGroup()
            mc.rename(mk_grp, anim_loc_grp)
            mc.parent(anim_loc, anim_loc_grp)
        val01 = [0.0, 0.0, -1.083,0.0, 0.0, 0.0]
        time_frame = get_cur
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val01, time_frame)
        val02 = [-0.766, 0.0, -0.766, 0.0, -20, 0.0]
        time_frame = get_cur+get_portion*2
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val02, time_frame)
        val03 = [-1.083, 0.0, 0.0,0.0, -30, 0.0]
        time_frame = get_cur+get_portion*3
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val03, time_frame)
        val04 = [-0.766, 0.0, 0.766,0.0, 0.0, 0.0]
        time_frame = get_cur+get_portion*4
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val04, time_frame)
        val05 = [0.0, 0.0, 1.083,0.0, -40, 0.0]
        time_frame = get_cur+get_portion*5
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val05, time_frame)
        val06 = [0.766, 0.0, 0.766,0.0, -90, 0.0]
        time_frame = get_cur+get_portion*6
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val06, time_frame)
        val07 = [1.083, 0.0, 0.0,0.0, -40, 0.0]
        time_frame = get_cur+get_portion*7
        dictionary_saved.append(time_frame)
        self.transform_anim( anim_loc, val07, time_frame)
        val08 = [0.766, 0.0, -0.766,0.0, 0.0, 0.0]
        time_frame = get_cur+get_portion*8
        dictionary_saved.append(time_frame)                                          
        self.transform_anim(anim_loc, val08, time_frame)
        mk_cnstrnt = mc.parentConstraint(get_obj, anim_loc_grp, mo=0)
        mc.delete(mk_cnstrnt)
        if "X" in directional_plane:
            print "X"
            mc.setAttr("{}.rotateX".format(anim_loc_grp), -90)
            mc.setAttr("{}.rotateY".format(anim_loc_grp), 90)
        elif "Z" in directional_plane:
            print "Z"                                              
        mc.setAttr("{}.scaleX".format(anim_loc_grp), size_area)
        mc.setAttr("{}.scaleY".format(anim_loc_grp), size_area)
        mc.setAttr("{}.scaleZ".format(anim_loc_grp), size_area)
        self.control_anim(dictionary_saved, get_obj, anim_loc[0])
        mc.delete(anim_loc_grp)
                                              
    def create_orbit_anim_loc(self, get_cur, get_portion, get_obj, directional_plane, size_area):
        dictionary_saved = []
        anim_loc_name = "{}_anim_loc".format(get_obj)
        anim_loc_grp = "{}_anim_grp".format(get_obj)
        if mc.objExists(anim_loc_name) == True:
            anim_loc_grp = mc.ls(anim_loc_grp)[0]
            anim_loc = mc.ls(anim_loc_name)[0]
        else:
            anim_loc = mc.spaceLocator(n=anim_loc_name)
            mc.select(cl=1)
            mk_grp=mc.CreateEmptyGroup()
            mc.rename(mk_grp, anim_loc_grp)
            mc.parent(anim_loc, anim_loc_grp)       
        val01 = [0.0, 0.0, -1.083,0.0, 0.0, 0.0]
        time_frame = get_cur
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val01, time_frame)
        val02 = [-0.766, 0.0, -0.766, 0.0, 0, 0.0]
        time_frame = get_cur+get_portion*2
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val02, time_frame)
        val03 = [-1.083, 0.0, 0.0,0.0, 0, 0.0]
        time_frame = get_cur+get_portion*3
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val03, time_frame)
        val04 = [-0.766, 0.0, 0.766,0.0, 0.0, 0.0]
        time_frame = get_cur+get_portion*4
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val04, time_frame)
        val05 = [0.0, 0.0, 1.083,0.0, 0, 0.0]
        time_frame = get_cur+get_portion*5
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val05, time_frame)          
        val06 = [0.766, 0.0, 0.766,0.0, 0, 0.0]
        time_frame = get_cur+get_portion*6
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val06, time_frame)
        val07 = [1.083, 0.0, 0.0,0.0, 0, 0.0]
        time_frame = get_cur+get_portion*7
        dictionary_saved.append(time_frame)
        self.transform_anim( anim_loc, val07, time_frame)
        val08 = [0.766, 0.0, -0.766,0.0, 0.0, 0.0]
        time_frame = get_cur+get_portion*8
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val08, time_frame)
        val11 = [0.0, 0.766, -0.766,0.0, 0.0, 0.0]         
        time_frame = get_cur+get_portion*11
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val11, time_frame)
        val12 = [0.0, 1.083, 0.0,0.0, -20, 0.0]
        time_frame = get_cur+get_portion*12
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val12, time_frame)
        val13 = [0.0, 0.766, 0.786,0.0, 0.0, 0.0]
        time_frame = get_cur+get_portion*13
        dictionary_saved.append(time_frame)                  
        self.transform_anim(anim_loc, val13, time_frame)
        val14 = [0.0, 0.0, 1.083,0.0, 0.0, 0.0]
        time_frame = get_cur+get_portion*14
        dictionary_saved.append(time_frame)
        self.transform_anim( anim_loc, val14, time_frame)
        val15 = [0.0, -0.766, 0.766,0.0, 0.0, 0.0]
        time_frame = get_cur+get_portion*15
        dictionary_saved.append(time_frame)
        self.transform_anim( anim_loc, val15, time_frame)
        val16 =[0.0, -1.083, 0.0,0.0, 0.0, 0.0]
        time_frame = get_cur+get_portion*16
        dictionary_saved.append(time_frame)
        self.transform_anim( anim_loc, val16, time_frame)
        val17 = [0.0, -0.766, -0.766, 0.0, 0.0, 0.0]
        time_frame = get_cur+get_portion*17
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val17, time_frame)
        val18 = [0.0, 0.0, -1.083, 0.0, 0.0, 0.0]
        time_frame = get_cur+get_portion*18
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val18, time_frame)
        mk_cnstrnt = mc.parentConstraint(get_obj, anim_loc_grp, mo=0)
        mc.delete(mk_cnstrnt)
        mc.setAttr("{}.scaleX".format(anim_loc_grp), size_area)
        mc.setAttr("{}.scaleY".format(anim_loc_grp), size_area)
        mc.setAttr("{}.scaleZ".format(anim_loc_grp), size_area)
        self.control_anim(dictionary_saved, get_obj, anim_loc[0])
        mc.delete(anim_loc_grp)                                              
                                              
    def control_anim(self, dictionary_saved, get_obj, anim_loc):
        for time in dictionary_saved:
            mc.currentTime(time)
            matrix=mc.xform(anim_loc, q=True, ws=1, t=True)
            mc.xform(get_obj,  ws=1, t=matrix)
            mc.select(get_obj, r=1)
            mc.SetKey()

    def transform_anim(self, cur_obj, val_list, time_frame):
        trns = [".tx", ".ty", ".tz", ".rx", ".ry", ".rz"]
        for attr, val in map(None, trns, val_list):
            print attr, val
            mc.setKeyframe(cur_obj, at=attr, v=val, time=(time_frame))
                                              
    def test_attr(self):
        inst_win = get_val_frm()

    def build_the_cam_titles(self):
        #create the title group for camera lineup with text
        try:
            get_loc=mc.ls("*_ploc")[0]
        except:
            get_loc=mc.spaceLocator(n="annot_ploc")
            get_loc=get_loc[0]                                
        mc.select(get_loc, r=1)
        mc.group()
        mc.rename(mc.ls(sl=1)[0], 'annot_loc_trn')
        self.cam_constraint('annot_loc_trn')
        mc.setAttr('annot_ploc.ty', -.16)
        mc.setAttr('annot_ploc.tz', -.845)
        mc.setAttr('annot_ploc.sx', 0.002)
        mc.setAttr('annot_ploc.sy', 0.002)
        mc.setAttr('annot_ploc.sz', 0.002)
        annot_title_grp=mc.ls("*ANNOTATE_GRP*")                                        
        if len(annot_title_grp)<1:
            annot_title_grp=mc.CreateEmptyGroup()
            mc.rename(annot_title_grp, "ANNOTATE_GRP")
            annot_title_grp=mc.ls("*ANNOTATE_GRP*")
        else:
            annot_title_grp=mc.ls("*ANNOTATE_GRP*") 
        #create the shader for the text 
        create_shade_node=mc.ls("annotate_shd")
                                              
