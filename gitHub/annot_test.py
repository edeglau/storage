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
        
    def drop_annot(self, obj_item):
        getIt=mc.ls("*ANNOTATE_GRP*")
        if len(getIt)<1:
            getIt=mc.CreateEmptyGroup()
            mc.rename(getIt, "ANNOTATE_GRP")
            getIt=mc.ls("*ANNOTATE_GRP*")
        else:
            getIt=mc.ls("*ANNOTATE_GRP*")         
        self.annot_function(obj_item, obj_item, getIt)

    def selected_verts(self, selObj):
        for item in selObj:
            self.annotations_list(item)
            
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
        # try:
        getNode = mc.ls(sl=1)[0]
        print getNode
        if mc.objExists("annot_loc_trn") == True:
            print "Label exists -  will skip creating it"
            print 'taping label to selected'
            try:
                mc.delete('annot_duct_tape_par')
            except:
                pass
            if len(getNode)>0:
                selcnst = mc.parentConstraint(getNode, 'annot_loc_trn', mo=0)
                mc.rename(selcnst, 'annot_duct_tape_par')
            else:
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
            if len(getNode)>0:
                selcnst = mc.parentConstraint(getNode, 'annot_loc_trn', mo=0)
                mc.rename(selcnst, 'annot_duct_tape_par')
            else:
                print "Nothing selected. skipping"
                pass
            

    def make_arbitrary_title(self):
        get_loc,create_shade_node, annot_title_grp  = self.build_the_cam_titles()
        label = "label"
        title_set = "label"
        new_name_annot = self.type_list_preset(mc.ls(sl=1)[0], title_set, get_loc)
        mc.select(new_name_annot, r=1)
        mc.hyperShade(assign=str(create_shade_node)) 
        mc.parent(new_name_annot, annot_title_grp)

    def makeDialog(self, titleText, messageText, textText):
        '''make dialog box function'''
        result = mc.promptDialog( 
            title=str(titleText), 
            message=str(messageText), 
            text=str(textText),
            button=['Continue','Cancel'],
            defaultButton='Continue', 
            cancelButton='Cancel', 
            dismissString='Cancel' )
        if result == 'Continue':            
            mainName=mc.promptDialog(q=1)
            return mainName
        else:
            print "nothing collected"    
            
    def checkDialog(self, titleText, messageText):
        result = mc.confirmDialog ( 
            title=str(titleText),
            message=str(messageText), 
            button=['Continue','Cancel'],
            defaultButton='Continue', 
            cancelButton='Cancel', 
            dismissString='Cancel' )
        if result == 'Continue':
            hall_pass = True
            return hall_pass
        else:
            print "nothing collected"         


    def test_attr_controllers(self):
        max_items = 100
        targetAttrs=mc.ls(sl=1)
        get_attrs_chn = [(the_item) for each_obj in targetAttrs for the_item in mc.listAttr (each_obj, k=1) if 'visibility' not in the_item]
        get_total = len(targetAttrs + get_attrs_chn)
        get_blast_length = get_total * 8
        get_pass = self.checkDialog("Function check", 'There are {} channels to parse which will potentially run a blast of {} frame length. Do you want to continue?'.format(get_total, get_blast_length))
        if get_pass == True:
            pass
        else:
            print "cancelling function"
            return
        getrange = len(targetAttrs)
        get_frames = int(self.makeDialog('FrameRange', 'Set frame span', '8'))
        fnd_dir="none"
    #     #   USE FOR EACH ATTRIBUTE TEST
        for each_obj in targetAttrs:
            get_attrs_chn = [(the_item) for the_item in mc.listAttr (each_obj, k=1) if 'visibility' not in the_item]
            for item in get_attrs_chn:
                if "translate" in item:
                    print "translation check"
                    get_val_1 = -3
                    get_val_2 = 3
                    set_val= get_val_1, get_val_2
                    make_dict_part = {item : set_val}
                    self.animate_function(get_frames, make_dict_part, fnd_dir, [each_obj])
                elif "rotate" in item:
                    print "rotation check"
                    get_val_1 = -25
                    get_val_2 = 25
                    set_val= get_val_1, get_val_2
                    make_dict_part = {item : set_val}
                    self.animate_function(get_frames, make_dict_part, fnd_dir, [each_obj])
                elif "scale" in item:
                    print "scale check"
                    get_val_1 =0.001
                    get_val_2 = 3
                    set_val= get_val_1, get_val_2
                    make_dict_part = {item : set_val}
                    self.animate_function(get_frames, make_dict_part, fnd_dir, [each_obj])
                else:
                    print "other check"
                    try:
                        get_val_1 = mc.attributeQuery(item, node=each_obj, min=1)
                    except:
                        get_val_1 =0
                    try:
                        get_val_2 = mc.attributeQuery(item, node=each_obj, max=1)
                    except:
                        get_val_2 =1
                    set_val= get_val_1, get_val_2
                    make_dict_part = {item : set_val}
                    self.animate_function(get_frames, make_dict_part, fnd_dir, [each_obj])


    def set_annot(self):
        get_set = mc.ls(sl=1)
        mc.select(get_set)
        trgt_ctrlrs = mc.ls(sl=1)
        inst_win = get_set_sel_val(trgt_ctrlrs)
        
    def ctrlr_annot(self):
        parentObj = mc.ls(sl=1)
        trgt_ctrlrs=[(each) for each in mc.listRelatives(parentObj, ad=1, type="transform") if "_ctrl" in each and "_grp" not in each]
        inst_win = get_set_sel_val(trgt_ctrlrs)

    def test_sel(self):
        trgt_ctrlrs = mc.ls(sl=1)
        inst_win = get_set_sel_val(trgt_ctrlrs)        
        
    def animate_function(self, get_frames, cust_dict, fnd_dir, trgt_ctrlrs):
        getRange = len(trgt_ctrlrs)
        get_loc,create_shade_node, annot_title_grp  = self.build_the_cam_titles()
        if fnd_dir == "none":
            for each in trgt_ctrlrs:
                try:
                    mc.sets(each, add=ctrl_set_name)
                except:
                    pass
                for key, value in cust_dict.items():
                    #set key points
                    find_def_val = mc.getAttr(each+"."+key)
                    value_lo=value[0]
                    if type(value_lo) == list:
                        value_lo = value_lo[0]
                    value_hi=value[1]
                    if type(value_hi) == list:
                        value_hi = value_hi[0]
                    get_cur = mc.currentTime(q=1)
                    getstartval = get_cur
                    gethalf = get_frames/3
                    getactiveval_lo = get_cur+gethalf
                    getactiveval_hi = get_cur+gethalf+gethalf
                    getendval = get_cur+get_frames
                    #keyframe the object
                    mc.setKeyframe(each, at=key, v=find_def_val, time=(getstartval))
                    mc.setKeyframe(each, at=key, v=value_lo, time=(getactiveval_lo))
                    mc.setKeyframe(each, at=key, v=value_hi, time=(getactiveval_hi))
                    mc.setKeyframe(each, at=key, v=find_def_val, time=(getendval))
                    #create the title
                    title_set = each+"."+key
                    if mc.objExists(title_set+'_grp') == False:
                        new_name_annot = self.type_list_preset(each, title_set, get_loc)
                    else:
                        new_name_annot = mc.ls(title_set+'_grp')[0]
                    # print new_name_annot
                    try:
                        mc.select(new_name_annot, r=1)
                        mc.hyperShade(assign=str(create_shade_node)) 
                    except:
                        pass
                    try:
                        mc.parent(new_name_annot, annot_title_grp)
                    except:
                        pass
                    #key the title
                    mc.setKeyframe(new_name_annot, at="visibility", v=0.0, time=(getstartval)) 
                    mc.setKeyframe(new_name_annot, at="visibility", v=1.0, time=(getstartval+1))
                    mc.setKeyframe(new_name_annot, at="visibility", v=1.0, time=(getendval-1))
                    mc.setKeyframe(new_name_annot, at="visibility", v=0.0, time=(getendval))  
        elif fnd_dir == "fig_eight":
            for each in trgt_ctrlrs:
                try:
                    mc.sets(each, add=ctrl_set_name)
                except:
                    pass
                for key, value in cust_dict.items():
                    get_cur = mc.currentTime(q=1)
                    size_area=value[0]*-1
                    if "rotateZ" or "translateZ" in key:
                        rotate_plane = "Z"
                    elif "rotateZ" or "translateZ" in key:
                        rotate_plane = "X"
                    getstartval = get_cur
                    get_portion = get_frames/20 
                    getendval = get_cur+get_frames
                    self.create_the_anim_loc(get_cur, get_portion, each, rotate_plane, size_area)
                    new_name_annot = self.type_list_preset(each, each, get_loc)         
                    try:
                        mc.select(new_name_annot, r=1)
                        mc.hyperShade(assign=str(create_shade_node)) 
                    except:
                        pass
                    try:
                        mc.parent(new_name_annot, annot_title_grp)
                    except:
                        pass
                    mc.setKeyframe(new_name_annot, at="visibility", v=0.0, time=(getstartval)) 
                    time_frame = get_cur+get_portion*2
                    mc.setKeyframe(new_name_annot, at="visibility", v=1.0, time=time_frame)
                    time_frame = get_cur+get_portion*19
                    mc.setKeyframe(new_name_annot, at="visibility", v=1.0, time=time_frame)
                    time_frame = get_cur+get_portion*20
                    mc.setKeyframe(new_name_annot, at="visibility", v=0.0, time=time_frame)    
                    mc.currentTime(getendval)                    
        elif fnd_dir == "circle":
            for each in trgt_ctrlrs:
                try:
                    mc.sets(each, add=ctrl_set_name)
                except:
                    pass
                for key, value in cust_dict.items():
                    get_cur = mc.currentTime(q=1)
                    size_area=value[0]*-1
                    if "rotateZ" or "translateZ" in key:
                        rotate_plane = "Z"
                    elif "rotateZ" or "translateZ" in key:
                        rotate_plane = "X"
                    getstartval = get_cur
                    get_portion = get_frames/8
                    getendval = get_cur+get_frames
                    self.create_circle_anim_loc(get_cur, get_portion, each, rotate_plane, size_area)
                    new_name_annot = self.type_list_preset(each, each, get_loc)        
                    try:
                        mc.select(new_name_annot, r=1)
                        mc.hyperShade(assign=str(create_shade_node)) 
                    except:
                        pass
                    try:
                        mc.parent(new_name_annot, annot_title_grp)
                    except:
                        pass
                    mc.setKeyframe(new_name_annot, at="visibility", v=0.0, time=(getstartval)) 
                    time_frame = get_cur+get_portion*2
                    mc.setKeyframe(new_name_annot, at="visibility", v=1.0, time=time_frame)
                    time_frame = get_cur+get_portion*7
                    mc.setKeyframe(new_name_annot, at="visibility", v=1.0, time=time_frame)
                    time_frame = get_cur+get_portion*8
                    mc.setKeyframe(new_name_annot, at="visibility", v=0.0, time=time_frame)    
                    mc.currentTime(getendval)                    
        elif fnd_dir == "orbit":
            for each in trgt_ctrlrs:
                try:
                    mc.sets(each, add=ctrl_set_name)
                except:
                    pass
                for key, value in cust_dict.items():
                    get_cur = mc.currentTime(q=1)
                    size_area=value[0]*-1
                    if "rotateZ" or "translateZ" in key:
                        rotate_plane = "Z"
                    elif "rotateZ" or "translateZ" in key:
                        rotate_plane = "X"
                    getstartval = get_cur
                    get_portion = get_frames/16 
                    getendval = get_cur+get_frames
                    self.create_orbit_anim_loc(get_cur, get_portion, each, rotate_plane, size_area)
                    new_name_annot = self.type_list_preset(each, each, get_loc)   
                    try:
                        mc.select(new_name_annot, r=1)
                        mc.hyperShade(assign=str(create_shade_node)) 
                    except:
                        pass
                    try:
                        mc.parent(new_name_annot, annot_title_grp)
                    except:
                        pass
                    mc.setKeyframe(new_name_annot, at="visibility", v=0.0, time=(getstartval)) 
                    time_frame = get_cur+get_portion*2
                    mc.setKeyframe(new_name_annot, at="visibility", v=1.0, time=time_frame)
                    time_frame = get_cur+get_portion*15
                    mc.setKeyframe(new_name_annot, at="visibility", v=1.0, time=time_frame)
                    time_frame = get_cur+get_portion*16
                    mc.setKeyframe(new_name_annot, at="visibility", v=0.0, time=time_frame)    
                    mc.currentTime(getendval)              
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
        val00 = [0.0, 0.0, 0.0,0.0, 0.0, 0.0]
        time_frame = get_cur-1
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val00, time_frame)
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
        time_frame = get_cur+get_portion*20+1
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val00, time_frame)
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
        val00 = [0.0, 0.0, 0.0,0.0, 0.0, 0.0]
        time_frame = get_cur-1
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val00, time_frame)            
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
        time_frame = get_cur+get_portion*8+1
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val00, time_frame)        
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
        val00 = [0.0, 0.0, 0.0,0.0, 0.0, 0.0]
        time_frame = get_cur-1
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val00, time_frame)                
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
        time_frame = get_cur+get_portion*18+1        
        dictionary_saved.append(time_frame)
        self.transform_anim(anim_loc, val00, time_frame)          
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

        
    def test_morph(self):
        try:
            get_morph_obj = mc.ls(sl=1)[0]
            if mc.nodeType(get_morph_obj) != "morph":
                get_Shape = [(each) for each in mc.listRelatives(get_morph_obj, ad=1, typ="shape")][0]
                get_morph = mc.ls(mc.listHistory(get_Shape), typ='morph')[0]
            else:
                get_morph = get_morph_obj
            targetAttrs = mc.listAttr("{}.controlWeight".format(get_morph), m=True) or []
            if len(targetAttrs)<1:
                print "cannot find morph targets"
                return
            else:
                getstrt = mc.currentTime(q=1)
                get_loc,create_shade_node, annot_title_grp  = self.build_the_cam_titles()
                for each in targetAttrs:
                    if "_" not in each:
                        get_cur = mc.currentTime(q=1)
                        getstartval = get_cur
                        getactiveval = get_cur+5
                        getendval = get_cur+10.0
                        try:
                            self.build_anim_singles(get_morph, get_morph_obj, each, get_loc, get_cur, getstartval, getactiveval, getendval, annot_title_grp)
                        except:
                            pass
                mm.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
                mc.setAttr( "{}.scaleZ".format(annot_title_grp[0]), 0.2)        
                mc.setAttr( "{}.scaleX".format(annot_title_grp[0]), 0.2)        
                mc.setAttr( "{}.scaleY".format(annot_title_grp[0]), 0.2)                 
        except:
            print "cannot find morph target weights"
            return



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
        if len(create_shade_node)<1:
            create_shade_node = mc.shadingNode('lambert', asShader=True, n="annotate_shd")
        else:
            create_shade_node=mc.ls(create_shade_node)[0]            
        lst_sg_node = [create_shade_node]
        #add the texture to a set
        set_name = 'techanim_textures'         
        if mc.objExists(set_name):
            pass
        else:
            mc.sets(n=set_name, co=3)
        mc.sets(lst_sg_node, add=set_name)  
        #change shader color to be more visible in grey viewport
        mc.setAttr("annotate_shd.color", 1, 0.5, 0, type = 'double3')
        return get_loc, create_shade_node, annot_title_grp
    
    def trigger_annot(self, get_val, get_frames):
        targetAttrs = mc.ls(sl=1)[0]
        #get selected attribute in channelbox
        getChannels =mm.eval('global string $gChannelBoxName; $temp=$gChannelBoxName;')
        try:
            attr_channel = mc.channelBox(getChannels, q=1, sma=1) [0]   
            pass
        except:
            print "select attribute on slected object"
            return
        title_content = targetAttrs+"."+attr_channel
        #add the attributes to a set
        ctrl_set_name = 'titled_controllers' 
        if mc.objExists(ctrl_set_name):
            pass
        else:
            mc.sets(n=ctrl_set_name, co=3)
        mc.sets(targetAttrs, add=ctrl_set_name)
        #create the title group for camera lineup with text
        get_loc,create_shade_node, annot_title_grp  = self.build_the_cam_titles()
        #calculate length and time to key on/off functions
        getstrt = mc.currentTime(q=1)
        getName=["namespace"]
        # for each in targetAttrs: 
        mc.select(targetAttrs, r=1)
        get_cur = mc.currentTime(q=1)
        getstartval = get_cur
        div_two = get_frames/2
        getactiveval = get_cur+div_two
        getendval = get_cur+get_frames
        print title_content
        try:
            self.build_anim_singles(targetAttrs, targetAttrs, attr_channel, get_loc, get_cur, getstartval, getactiveval, getendval, annot_title_grp)
        except:
            pass
        mm.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
        mc.setAttr( "{}.scaleZ".format(annot_title_grp[0]), 0.2)        
        mc.setAttr( "{}.scaleX".format(annot_title_grp[0]), 0.2)        
        mc.setAttr( "{}.scaleY".format(annot_title_grp[0]), 0.2)      
        
    def build_anim_singles(self, obj_item, sel_obj, anim_attr, get_loc, get_cur, getstartval, getactiveval, getendval, annot_title_grp):
        '''
        obj_item = the object the attribute belongs to(EG:sphere1)
        sel_obj = the selected object the attribute belongs to(EG:morph node)
        anim_attr = the attribute to be keyed at(EG:1.0)
        get_loc = the object in which the resulting title will be contrained to(annot_loc_trn)
        getstartval = the relative frame that the animation of that attribute starts(EG:1000)
        getactiveval = the "on" time frame for the attribute to be tested at(EG:1008)
        getendval = the relative frame that the animation of that attribute ends(EG:1012)
        '''
        if mc.objExists(anim_attr+'_grp') == False:
            title_label = sel_obj+'.'+anim_attr
            new_name_annot = self.type_list_preset(sel_obj, title_label, get_loc)
        else:
            new_name_annot = mc.ls(anim_attr+'_grp')[0]
        # print new_name_annot
        try:
            mc.select(new_name_annot, r=1)
            mc.hyperShade(assign=str(create_shade_node)) 
        except:
            pass
        try:
            mc.parent(new_name_annot, annot_title_grp)
        except:
            pass
        #key morphs
        mc.setKeyframe(obj_item, at=anim_attr, v=0.0, time=(getstartval))   
        mc.setKeyframe(obj_item, at=anim_attr, v=1.0, time=(getactiveval))
        mc.setKeyframe(obj_item, at=anim_attr, v=0.0, time=(getendval))
        #key the title
        mc.setKeyframe(new_name_annot, at="visibility", v=0.0, time=(getstartval)) 
        mc.setKeyframe(new_name_annot, at="visibility", v=1.0, time=(getstartval+1))
        mc.setKeyframe(new_name_annot, at="visibility", v=1.0, time=(getendval-1))
        mc.setKeyframe(new_name_annot, at="visibility", v=0.0, time=(getendval))    
        mc.currentTime(getendval)

    
inst_win = annot_range_win()
inst_win.show()    

   
