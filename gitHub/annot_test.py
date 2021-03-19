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

colorlist=[13, 6, 14, 17, 4, 8, 5, 7, 15, 5, 20, 24, 29, 31, 10, 16, 9, 30, 1, 2]

class get_set_sel_val(QtWidgets.QWidget):
    def __init__(self, trgt_ctrlrs):
        super(get_set_sel_val, self).__init__()
        self.initUI(trgt_ctrlrs)
    def initUI(self, trgt_ctrlrs):  
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
        self.value_label = QtWidgets.QLabel("Amount to animate")
        self.valueset_lo_six = QtWidgets.QLineEdit("-1")
        self.valueset_hi_six = QtWidgets.QLineEdit("1")
        self.layout.addLayout(self.btnlayout)
        self.ctrl_button = QtWidgets.QPushButton("annot controllers")
        self.ctrl_button.clicked.connect(lambda: self.build_ctrl_annot_one(trgt_ctrlrs))

        self.strLayout = QtWidgets.QGridLayout()
        self.strFrame = QtWidgets.QFrame()
        self.strFrame.setLayout(self.strLayout)
        self.btnlayout.addWidget(self.strFrame)
        
        self.strLayout_two = QtWidgets.QGridLayout()
        self.strFrame_two = QtWidgets.QFrame()
        self.strFrame_two.setLayout(self.strLayout_two)
        self.btnlayout.addWidget(self.strFrame_two)

        self.strLayout_three = QtWidgets.QGridLayout()
        self.strFrame_three = QtWidgets.QFrame()
        self.strFrame_three.setLayout(self.strLayout_three)
        self.btnlayout.addWidget(self.strFrame_three)


        self.strLayout_four = QtWidgets.QGridLayout()
        self.strFrame_four = QtWidgets.QFrame()
        self.strFrame_four.setLayout(self.strLayout_four)
        self.btnlayout.addWidget(self.strFrame_four)
        

        self.strLayout_five = QtWidgets.QGridLayout()
        self.strFrame_five = QtWidgets.QFrame()
        self.strFrame_five.setLayout(self.strLayout_five)
        self.btnlayout.addWidget(self.strFrame_five)

        self.strLayout_six = QtWidgets.QGridLayout()
        self.strFrame_six = QtWidgets.QFrame()
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
        self.dir_list = QtWidgets.QComboBox()
        self.dir_list.addItems(self.set_dir)   
        self.sev_layout.addWidget(self.dir_list)    
        
        self.btnlayout.addWidget(self.frames_label)
        self.btnlayout.addWidget(self.frames)
        self.btnlayout.addWidget(self.ctrl_button)
        self.setLayout(self.layout)
        self.show()     
        
    def build_ctrl_annot_one(self, trgt_ctrlrs):
        fnd_dir = str(self.dir_list.currentText())
        cust_dict = {}
        get_frames = float(self.frames.text())
        drp_attr = str(self.attrlist.currentText())
        get_val_one_1 = float(self.valueset_lo_one.text())
        get_val_one_2 = float(self.valueset_hi_one.text())
        set_val_1 = get_val_one_1, get_val_one_2
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
        access_main.animate_function( get_frames, cust_dict, fnd_dir, trgt_ctrlrs)
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
        self.value_label = QtWidgets.QLabel("Amount to animate")
        self.valueset = QtWidgets.QLineEdit("1")
        self.frames_label = QtWidgets.QLabel("accross frames")
        self.frames = QtWidgets.QLineEdit("8")
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
        self.annot_sel_button.clicked.connect(lambda: self.selected_vtx_annot())
        self.auto_annot_button = QtWidgets.QPushButton("Auto Annotate")
        self.auto_annot_button.clicked.connect(lambda: self.dealers_choice())                  
        self.colour_annot_button = QtWidgets.QPushButton("Change Annot Colours")
        self.colour_annot_button.clicked.connect(lambda:self._change_anot_colors())  
        self.mrph_annot_button = QtWidgets.QPushButton("Test morphs")
        self.mrph_annot_button.clicked.connect(lambda: self.test_morph())       
        self.ctrl_annot_button = QtWidgets.QPushButton("Test ctrlrs under hrchy")
        self.ctrl_annot_button.clicked.connect(lambda: self.ctrlr_annot())     
        self.set_annot_button = QtWidgets.QPushButton("Test set")
        self.set_annot_button.clicked.connect(lambda: self.set_annot())       
        self.attr_annot_button = QtWidgets.QPushButton("Selected Attribute")
        self.attr_annot_button.clicked.connect(lambda: self.test_attr())   
        self.all_attr_annot_button = QtWidgets.QPushButton("Attribute(s) on Selected")
        self.all_attr_annot_button.clicked.connect(lambda: self.test_attr_controllers())      
        self.sel_annot_button = QtWidgets.QPushButton("Selected")
        self.sel_annot_button.clicked.connect(lambda: self.test_sel())     
        self.recon_annot_button = QtWidgets.QPushButton("Reconstrain title")
        self.recon_annot_button.clicked.connect(lambda: self.retape_to_selection())   
        self.mk_annot_button = QtWidgets.QPushButton("Make title")
        self.mk_annot_button.clicked.connect(lambda: self.make_arbitrary_title())      
        self.btnlayout.addWidget(self.auto_annot_button)     
        self.btnlayout.addWidget(self.annot_sel_button)
        self.btnlayout.addWidget(self.colour_annot_button)
        self.btnlayout.addWidget(self.sel_annot_button)
        self.btnlayout.addWidget(self.attr_annot_button)
        self.btnlayout.addWidget(self.all_attr_annot_button)
        self.btnlayout.addWidget(self.ctrl_annot_button)
        self.btnlayout.addWidget(self.set_annot_button)
        self.btnlayout.addWidget(self.mrph_annot_button)
        self.btnlayout.addWidget(self.mk_annot_button)
        self.btnlayout.addWidget(self.recon_annot_button)

        self.setLayout(self.layout)

    def dealers_choice(self):
        collectedVtx=[]
        if len(mc.ls(sl=1))>0:
            for sel_item in mc.ls(sl=1):
                try:
                    getmeshObj=[(each) for each in mc.listRelatives(item, ad=1, type="mesh")][0]
                    getvert=getmeshObj+".vtx[0]"
                    self.annotations_list(getvert)
                except:
                    self.drop_annot(sel_item)
        else:
            exclude= ["front", "side", "persp", "top", "ANNOTATE_GRP"]
            rigs = [(each) for each in mc.ls(type = "transform") if mc.listRelatives(each, p=1) == None if each not in exclude]
            for sel_item in rigs:
                try:
                    getmeshObj=[(item) for item in mc.listRelatives(sel_item, ad=1, type="mesh")][0]
                    getvert=getmeshObj+".vtx[0]"
                    print "found mesh"
                    print getvert
                    self.annotations_list(getvert)
                except:
                    print "found no mesh"
  
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
        if mc.objExists(getTitle+"_grp") ==0:
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
        else:
            buildParent = mc.ls(getTitle+"_grp")[0]
        return buildParent        

    def point_obj_const_callup(self, getSel):
        edgeBucket=[]
        if ":" in getSel:
            findName=getSel.split(":")[-1:][0]
        else:
            findName=getSel
        if ":" in getSel[0]:
            getObj=getSel[0].split(":")[-1:]
        else:
            getObj=getSel
        getNew=mc.spaceLocator(n=str(findName)+"ploc")
        if "animGeo"in getObj:
            getroot = '{}:c_root_jnt'.format(getSel.split(":")[0])
            print getroot
            mc.pointConstraint([getroot, getNew[0]], n = '{}_{}_annot_cnst'.format(getSel, getNew[0]), mo=0) 
        else:
            mc.pointConstraint([getSel, getNew[0]], n = '{}_{}_annot_cnst'.format(getSel, getNew[0]), mo=0) 
            
    def selected_vtx_annot(self):
        getSel = mc.ls(sl=1)
        if '.vtx' in mc.ls(sl=1)[0]:
            for item in getSel:
                self.annotations_list(item)
        else:
            print "select a vertice"
            pass

    def annotations_list(self, selObj):
        print selObj
        # selObj = mc.ls(sl=1)
        getIt=mc.ls("*ANNOTATE_GRP*")
        if len(getIt)<1:
            getIt=mc.CreateEmptyGroup()
            mc.rename(getIt, "ANNOTATE_GRP")
            getIt=mc.ls("*ANNOTATE_GRP*")
        else:
            getIt=mc.ls("*ANNOTATE_GRP*")    
        getTitle = selObj.split('.vtx')[0]
        self.annot_function(selObj, getTitle, getIt)    
        
    def annot_function(self, item, getTitle, getIt):
        random.shuffle(colorlist, random.random)
        offset = colorlist[0]
        mc.select(item, r=1)
        if ".vtx" in item:
            self.point_const(item)
        else:
            self.point_obj_const_callup(item)
        selected = mc.ls(sl=1)
        if len(selected)>1:
            selected = selected[-1]
        else:
            selected = selected[0]
        mc.parent(selected, getIt)
        transformWorldMatrix=mc.xform(selected, q=True, ws=1, t=True)
        newTransform = [transformWorldMatrix[0], transformWorldMatrix[1]+offset, transformWorldMatrix[2]]
        getAnnot = mc.annotate(selected, p=newTransform)
        buildParent = mc.group(n=getTitle+"_grp")
        mc.CenterPivot()
        mc.setAttr(getAnnot+".text", getTitle, type="string")
        mc.setAttr(getAnnot+".overrideEnabled", 1)
        mc.setAttr(getAnnot+".overrideColor", offset)
        getparent = mc.listRelatives(getAnnot, p=1)[0]
        mc.pointConstraint(selected, buildParent, mo=1)
        mc.rename(getparent, getTitle+"_ant")
        mc.rename(selected, item)
        mc.parent(buildParent, getIt)
        

    def point_const(self, getSel):
        self.point_const_callup(getSel)


    def point_const_callup(self, getSel):
        if ":" in getSel:
            getObj=getSel.split(":")[-1:]
        else:
            getObj=getSel
        print getObj
        getMod=getObj[0].split('.')[0]
        getUVmap = mc.polyListComponentConversion(getSel, fv=1, tuv=1)
        getCoords=mc.polyEditUV(getUVmap, q=1)
        print str(getMod)+"ploc"
        getNew=mc.spaceLocator(n=str(getMod)+"ploc")
        mc.select(getSel, r=1)
        mc.select(getNew[0], add=1)
        buildConst=mc.pointOnPolyConstraint(getSel, getNew[0], mo=0, offset=(0.0, 0.0, 0.0))
        try:
            mc.setAttr(buildConst[0]+"."+getMod+"U0", getCoords[0])
            mc.setAttr(buildConst[0]+"."+getMod+"V0", getCoords[1])    
        except:
            pass        
        
