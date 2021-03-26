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

pub_cam = '/jobs/rnd_model/assets/cam.shotcam.AssetCam1HD/PRODUCTS/rigs/cam.shotcam.AssetCam1HD/rig/camera/approved/mb/cam.shotcam.AssetCam1HD_rig_camera.mb'

import random

colorlist=[13, 6, 14, 17, 4, 8, 5, 7, 15, 5, 20, 24, 29, 31, 10, 16, 9, 30, 1, 2]

class get_set_sel_val(QtWidgets.QWidget):
    def __init__(self, trgt_ctrlrs):
        super(get_set_sel_val, self).__init__()
        self.initUI(trgt_ctrlrs)


    def initUI(self, trgt_ctrlrs):  
        """
        sel_obj object popup window setup
        """        
        sel_obj = mc.ls(sl=1)[0]
        if len(mc.ls(sl=1))>0:
            each_attr = [(the_item) for the_item in mc.listAttr (sel_obj, k=1) if 'visibility' not in the_item]
        else:
            each_attr = ["tx", "ty", "tz", "rx", "ry", "rz"]
        title = "Set Values for review titles"   
        self.setWindowTitle(title)
        self.layout = QtWidgets.QVBoxLayout()
        self.btnlayout = QtWidgets.QGridLayout()
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
        self.value_label = QtWidgets.QLabel("Amount to Animate")
        self.valueset_lo_six = QtWidgets.QLineEdit("-1")
        self.valueset_hi_six = QtWidgets.QLineEdit("1")
        self.layout.addLayout(self.btnlayout)
        self.ctrl_button = QtWidgets.QPushButton("Animate Controllers")
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

        self.attr_lbl_layout = QtWidgets.QHBoxLayout()
        self.attr_label = QtWidgets.QLabel("Attributes")    
        self.attr_lbl_layout.addWidget(self.attr_label)
        self.strLayout.addLayout(self.attr_lbl_layout, 0, 0, 1, 1)  

        self.one_layout = QtWidgets.QHBoxLayout()
        self.strLayout.addLayout(self.one_layout, 1, 0, 1, 1)        
        self.one_layout.addWidget(self.cust_checked)
        self.one_layout.addWidget(self.attrlist)
        self.one_layout.addWidget(self.valueset_lo_one)
        self.one_layout.addWidget(self.valueset_hi_one)

        self.two_layout = QtWidgets.QHBoxLayout()
        self.strLayout_two.addLayout(self.two_layout, 2, 0, 1, 1)        
        self.two_layout.addWidget(self.cust_checked_two)
        self.two_layout.addWidget(self.attrlist_two)
        self.two_layout.addWidget(self.valueset_lo_two)
        self.two_layout.addWidget(self.valueset_hi_two)

        self.three_layout = QtWidgets.QHBoxLayout()
        self.strLayout_three.addLayout(self.three_layout, 3, 0, 1, 1)        
        self.three_layout.addWidget(self.cust_checked_three)
        self.three_layout.addWidget(self.attrlist_three)
        self.three_layout.addWidget(self.valueset_lo_three)
        self.three_layout.addWidget(self.valueset_hi_three)

        self.four_layout = QtWidgets.QHBoxLayout()
        self.strLayout_four.addLayout(self.four_layout, 4, 0, 1, 1)        
        self.four_layout.addWidget(self.cust_checked_four)
        self.four_layout.addWidget(self.attrlist_four)
        self.four_layout.addWidget(self.valueset_lo_four)
        self.four_layout.addWidget(self.valueset_hi_four)

        self.five_layout = QtWidgets.QHBoxLayout()
        self.strLayout_five.addLayout(self.five_layout, 5, 0, 1, 1)        
        self.five_layout.addWidget(self.cust_checked_five)
        self.five_layout.addWidget(self.attrlist_five)
        self.five_layout.addWidget(self.valueset_lo_five)
        self.five_layout.addWidget(self.valueset_hi_five)

        self.six_layout = QtWidgets.QHBoxLayout()
        self.strLayout_six.addLayout(self.six_layout, 6, 0, 1, 1)        
        self.six_layout.addWidget(self.cust_checked_six)
        self.six_layout.addWidget(self.attrlist_six)
        self.six_layout.addWidget(self.valueset_lo_six)
        self.six_layout.addWidget(self.valueset_hi_six)

        self.type_lbl_layout = QtWidgets.QHBoxLayout()
        self.typ_label = QtWidgets.QLabel("Type")    
        self.type_lbl_layout.addWidget(self.typ_label)
        self.strLayout_six.addLayout(self.type_lbl_layout, 7, 0, 1, 1)   
        
        self.sev_layout = QtWidgets.QHBoxLayout()
        self.strLayout_six.addLayout(self.sev_layout, 8, 0, 1, 1)
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
        """
        Gathers the attribute, min, max and range to animate
        """         
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
    def __init__(self, get_val_hi, def_val, trgt_obj, attr_channel):
        super(get_val_frm, self).__init__()
        self.initUI(get_val_hi, def_val, trgt_obj, attr_channel)

    def initUI(self, get_val_hi, def_val, trgt_obj, attr_channel):  
        """
        sel_obj value popup window setup
        """   
        get_val_hi = str(get_val_hi)
        title = "Set Values for review titles"   
        self.setWindowTitle(title)
        self.layout = QtWidgets.QVBoxLayout()
        self.btnlayout = QtWidgets.QGridLayout()
        self.value_label = QtWidgets.QLabel("Amount to animate")
        self.valueset = QtWidgets.QLineEdit(get_val_hi)
        self.frames_label = QtWidgets.QLabel("Accross Frames")
        self.frames = QtWidgets.QLineEdit("8")
        self.layout.addLayout(self.btnlayout)
        self.sel_button = QtWidgets.QPushButton("Animate Attribute")
        self.sel_button.clicked.connect(lambda: self.build_annot(def_val, trgt_obj, attr_channel))
        self.btnlayout.addWidget(self.value_label)
        self.btnlayout.addWidget(self.valueset)
        self.btnlayout.addWidget(self.frames_label)
        self.btnlayout.addWidget(self.frames)
        self.btnlayout.addWidget(self.sel_button)
        self.setLayout(self.layout)
        self.show()

    def build_annot(self, def_val, trgt_obj, attr_channel):
        """
        Gathers value amount and frame range to animate attribute
        """         
        get_val = self.valueset.text()
        get_val = float(get_val)
        get_frames = self.frames.text()
        get_frames = float(get_frames)
        access_main = annot_range_win()
        access_main.trigger_annot(get_val, def_val, get_frames, trgt_obj, attr_channel)
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

        self.annot_sel_button =QtWidgets. QPushButton("Annotate selected")
        self.annot_sel_button.setToolTip("Pipeline issues/data retrieval/IT")
        self.annot_sel_button.clicked.connect(lambda: self.sel_obj_vtx_annot())
        self.auto_annot_button = QtWidgets.QPushButton("Auto Annotate")
        self.auto_annot_button.clicked.connect(lambda: self.dealers_choice())                  
        self.colour_annot_button = QtWidgets.QPushButton("Change Annot Colours")
        self.colour_annot_button.clicked.connect(lambda:self._change_anot_colors())  
        self.mrph_annot_button = QtWidgets.QPushButton("Test Morph targets")
        self.mrph_annot_button.clicked.connect(lambda: self.test_morph())       
        self.ctrl_annot_button = QtWidgets.QPushButton("Test Controller heirarchy")
        self.ctrl_annot_button.clicked.connect(lambda: self.ctrlr_annot())     
        self.set_annot_button = QtWidgets.QPushButton("Test Set")
        self.set_annot_button.clicked.connect(lambda: self.set_annot())      
        self.attr_annot_button = QtWidgets.QPushButton("Selected Attribute")
        self.attr_annot_button.clicked.connect(lambda: self.test_attr())   
        self.all_attr_annot_button = QtWidgets.QPushButton("Attribute(s) on Selected")
        self.all_attr_annot_button.clicked.connect(lambda: self.test_attr_controllers())      
        self.sel_annot_button = QtWidgets.QPushButton("Test Selected")
        self.sel_annot_button.clicked.connect(lambda: self.test_sel())     
        self.recon_annot_button = QtWidgets.QPushButton("Reconstrain Title")
        self.recon_annot_button.clicked.connect(lambda: self.retape_to_selection())   
        self.mk_annot_button = QtWidgets.QPushButton("Make Title")
        self.mk_annot_button.clicked.connect(lambda: self.make_arbitrary_title())    
        self.mk_pubcam_button = QtWidgets.QPushButton("Make pub cam")
        self.mk_pubcam_button.clicked.connect(lambda: self.publishable_cam())    
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
        self.btnlayout.addWidget(self.mk_pubcam_button)         

        self.setLayout(self.layout)


    def publishable_cam(self):
        nm_space = 'shotcam1'
        mc.file(pub_cam, r=1, ns=nm_space)

    def help_page_launch(self):
        """
        opens the helppage for tool in confluence
        """
        url='https://atlas.bydeluxe.com/confluence/display/~deglaue/annotate+showtool+maya'
        subprocess.Popen('gio open %s' % url, stdout=subprocess.PIPE, shell=True) 

    def sel_obj_vtx_annot(self):
        """
        Creates annotation by sel_obj vertex(only component: vertex)
        Called up: Button: "Annotate sel_obj"
        """ 
        sel_obj = mc.ls(sl=1)
        if '.vtx' in mc.ls(sl=1)[0]:
            for sel_vert in sel_obj:
                self.create_annot_grp(sel_vert)
        else:
            print "select a vertice"
            pass        
        
    def dealers_choice(self):
        """
        If nothing sel_obj, interogates entire scene for objects to annotate. 
        Does also take selection(non component).
        Called up: Button: "Auto Annotate"
        """
        vert_collection=[]
        if len(mc.ls(sl=1))>0:
            for sel_item in mc.ls(sl=1):
                try:
                    mesh_obj=[(each_par) for each_par 
                    in mc.listRelatives(sel_item, ad=1, type="mesh")][0]
                    vert_obj=mesh_obj+".vtx[0]"
                    self.create_annot_grp(vert_obj)
                except:
                    self.create_annot_grp(sel_item)
        else:
            exclude= ["front", "side", "persp", "top", "ANNOTATE_GRP"]
            rigs = [(each) for each in mc.ls(type = "transform") 
            if mc.listRelatives(each, p=1) == None if each not in exclude]
            for sel_item in rigs:
                try:
                    mesh_obj=[(each_mesh) for each_mesh 
                    in mc.listRelatives(sel_item, ad=1, type="mesh")][0]
                    vert_obj=mesh_obj+".vtx[0]"
                    self.create_annot_grp(vert_obj)
                except:
                    print "found no mesh"
                    self.create_annot_grp(sel_item)

    def _change_anot_colors(self):
        """
        Changes the override index color to a randomized value
            randomized colorlist=[13, 6, 14, 17, 4, 8, 5, 7, 15, 5, 20, 24, 29, 31, 10, 16, 9, 30, 1, 2]
        """         
        getgrp = mc.ls(sl=1)
        if len(getgrp)==0:
            getgrp = mc.ls(type="annotationShape")
        elif mc.ls(sl=1)>0:
            getgrp=[(each) for item in getgrp for each 
            in mc.listRelatives(item, ad=1, type="annotationShape")]
        else:
            print "annotations not present in scene"
            return
        for each in getgrp:
            random.shuffle(colorlist, random.random)
            offset = colorlist[0]
            mc.setAttr(each+".overrideEnabled", 1)
            mc.setAttr(each+".overrideColor", offset)
            
    def setTextVal(self, typeNode, textString):
        """
        Changes the value of the textInput in hex code for maya type object
            Args:
                typeNode (str) : text object ("type1")
                textString (str) : new string ("pSphere.ry")
            Examples:
                for character in 'pSphere.xy':
                >>>>'p'.encode('hex')
                >>>>'S'.encode('hex')
                >>>>'h'.encode('hex')
                attrVal = ' '.join('p''S''h'...etc)
                >>>>mc.setAttr(type1.textInput, attrVal, type = 'string')
                >>>>type1.textInput = 'pSphere1.xy'
        """ 
        hexValues = []
        for character in textString:
            hexValues.append(character.encode('hex'))
        attrVal = ' '.join(hexValues)
        mc.setAttr(typeNode+'.textInput', attrVal, type = 'string')

    def type_list_preset(self, obj_name, get_loc):    
        """
        The common callup that creates the camera label
            Args:
                obj_name (str) : text string('pSphere.ry')
                get_loc (str) : the locator that controls transforms of the text('annot_ploc')
            Examples:
                object name: 'pShpere.ry'
                self.setTextVal('type1', 'pSphere.ry')
                >>>>type1.textInput = 'pSphere1.xy'
                parent and scale contrain new grouped text to locator
            Returns:
                text object group
                >>>>'pSphere1_ry_grp'
        """ 
        if mc.objExists(obj_name+"_grp") ==0:
            trnsfm_wrld_matrix=mc.xform(get_loc, q=True, ws=1, t=True)
            plusnum=random.uniform(.2,3)
            mm.eval('typeCreateText;')
            sel_typ = [(hist_type) for hist_type in mc.listHistory(mc.ls(sl=1)) 
            if mc.nodeType(hist_type) == "type"][0]
            self.setTextVal(sel_typ, str(obj_name))
            sel_mesh = [(each_trnsfm) for each_trnsfm in mc.listHistory(sel_typ) 
            if mc.nodeType(each_trnsfm) == "transform"][0]
            mc.select(sel_mesh, r=1)
            mc.CenterPivot()
            par_grp = mc.group(n=obj_name+"_grp")
            mc.parentConstraint(get_loc, par_grp, mo=0)
            mc.scaleConstraint(get_loc, par_grp, mo=0)
        else:
            par_grp = mc.ls(obj_name+"_grp")[0]
        return par_grp

    
    def create_annot_grp(self, sel_obj):
        """
        The common callup for creating the annotate group which contains all the text items
            Args:
                sel_obj (str) : sel_obj object('pSphere')
            Called up:
                annotation callups 
        """ 
        if 'Shape' in sel_obj:
            obj_name = sel_obj.split('Shape')[0]
        else:
            obj_name = sel_obj
        annot_grp=mc.ls("*ANNOTATE_GRP*")
        if len(annot_grp)<1:
            annot_grp=mc.CreateEmptyGroup()
            mc.rename(annot_grp, "ANNOTATE_GRP")
            annot_grp=mc.ls("*ANNOTATE_GRP*")
        else:
            annot_grp=mc.ls("*ANNOTATE_GRP*")    
        random.shuffle(colorlist, random.random)
        offset = colorlist[0]
        mc.select(sel_obj, r=1)
        if ".vtx" in sel_obj:
            self.point_const_callup(sel_obj)
        else:
            self.point_obj_const_callup(sel_obj)
        sel_obj = mc.ls(sl=1)
        if len(sel_obj)>1:
            sel_obj = sel_obj[-1]
        else:
            sel_obj = sel_obj[0]
        mc.parent(sel_obj, annot_grp)
        trnsfm_wrld_matrix=mc.xform(sel_obj, q=True, ws=1, t=True)
        new_trnsfm_wrld_mtx = [trnsfm_wrld_matrix[0], trnsfm_wrld_matrix[1]+offset, trnsfm_wrld_matrix[2]]
        crt_annot = mc.annotate(sel_obj, p=new_trnsfm_wrld_mtx)
        par_grp = mc.group(n=obj_name+"_grp")
        mc.CenterPivot()
        mc.setAttr(crt_annot+".text", obj_name, type="string")
        mc.setAttr(crt_annot+".overrideEnabled", 1)
        mc.setAttr(crt_annot+".overrideColor", offset)
        getparent = mc.listRelatives(crt_annot, p=1)[0]
        mc.pointConstraint(sel_obj, par_grp, mo=1)
        mc.rename(getparent, obj_name+"_ant")
        mc.rename(sel_obj, sel_obj)
        mc.parent(par_grp, annot_grp)
        
    def point_const_callup(self, sel_obj):
        """
        The common callup for creating creating a point-on-poly constraint 
        for annotations(mesh objects with verts and UV maps)
            Args:
                sel_obj (str) : sel_obj vertex ('pSphereShape.vtx[0]')
            Called up:
                create_annot_grp
        """ 
        if ":" in sel_obj:
            get_obj_name=sel_obj.split(":")[-1:]
        else:
            get_obj_name=sel_obj
        if '.' in get_obj_name:
            mesh_mod=get_obj_name.split('.')[0]
        else:
            mesh_mod=get_obj_name
        getUVmap = mc.polyListComponentConversion(sel_obj, fv=1, tuv=1)
        poly_coords=mc.polyEditUV(getUVmap, q=1)
        spc_loc=mc.spaceLocator(n=str(mesh_mod)+"ploc")
        mc.select(sel_obj, r=1)
        mc.select(spc_loc[0], add=1)
        pnt_poly_cnstrnt=mc.pointOnPolyConstraint(sel_obj, spc_loc[0], mo=0, offset=(0.0, 0.0, 0.0))
        try:
            mc.setAttr(pnt_poly_cnstrnt[0]+"."+mesh_mod+"U0", poly_coords[0])
            mc.setAttr(pnt_poly_cnstrnt[0]+"."+mesh_mod+"V0", poly_coords[1])    
        except:
            pass
        
    def point_obj_const_callup(self, sel_obj):
        """
        The common callup for creating creating a point constraint for annotation
            Args:
                sel_obj (str) : sel_obj  ('pSphere')
            Called up:
                create_annot_grp
        """ 
        if ":" in sel_obj:
            obj_name=sel_obj.split(":")[-1:][0]
        else:
            obj_name=sel_obj
        if ":" in sel_obj[0]:
            res_obj=sel_obj[0].split(":")[-1:]
        else:
            res_obj=sel_obj
        spc_loc=mc.spaceLocator(n=str(obj_name)+"ploc")
        #if object is rig, constrain to the root joint
        if "animGeo"in res_obj:
            rt_jnt = '{}:c_root_jnt'.format(sel_obj.split(":")[0])
            print rt_jnt
            mc.pointConstraint([rt_jnt, spc_loc[0]], n = '{}_{}_annot_cnst'.format(sel_obj, spc_loc[0]), mo=0) 
        else:
            mc.pointConstraint([sel_obj, spc_loc[0]], n = '{}_{}_annot_cnst'.format(sel_obj, spc_loc[0]), mo=0)  
            
            
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
        """
        Creates a default title that is constrained to camera
            Called up:
                Button "Make title"
        """ 
        get_loc,create_shade_node, annot_title_grp  = self.build_the_cam_titles()
        label = "label"
        title_set = "label"
        new_name_annot = self.type_list_preset(title_set, get_loc)
        mc.select(new_name_annot, r=1)
        mc.hyperShade(assign=str(create_shade_node)) 
        mc.parent(new_name_annot, annot_title_grp)

    def makeDialog(self, titleText, messageText, textText):
        '''make dialog box function
            Return:
                FrameRange
            Callup:
                test_attr_controllers
        '''
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
        '''make confirm box function'''
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
        '''Goes through each attribute on object to find 
        and animate max/min values within a defined frame range
            Return:
                
            Callup:
                Button: "Attribute(s) on Selected"
        '''
        max_items = 100
        trgt_attrs=mc.ls(sl=1)
        get_attrs_chn = [(the_item) for each_obj in trgt_attrs for the_item 
        in mc.listAttr (each_obj, k=1) if 'visibility' not in the_item]
        get_total = len(trgt_attrs + get_attrs_chn)
        get_blast_length = get_total * 8
        get_pass = self.checkDialog(
            "Function check", 
            "There are {} channels to parse\n"
            "which will potentially run a blast of {} frame length. \n"
            "Do you want to continue?".format(get_total, get_blast_length))
        if get_pass == True:
            pass
        else:
            print "cancelling function"
            return
        fnd_range = len(trgt_attrs)
        get_frames = int(self.makeDialog('FrameRange', 'Set frame span', '8'))
        fnd_dir="none"
        #USE FOR EACH ATTRIBUTE TEST
        for each_obj in trgt_attrs:
            get_attrs_chn = [(the_item) for the_item 
            in mc.listAttr (each_obj, k=1) if 'visibility' not in the_item]
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
        """
        Creates an animation based on selected set
            Called up:
                Button "Test Set"
            Calls up:
                get_set_sel_val window for picking an attribute to animate
        """ 
        get_set = mc.ls(sl=1)
        mc.select(get_set)
        trgt_ctrlrs = mc.ls(sl=1)
        inst_win = get_set_sel_val(trgt_ctrlrs)
    
    def ctrlr_annot(self):
        """
        Creates an animation based on selected controller heirarchy
            Called up:
                Button "Test Controller heirarchy"
            Calls up:
                get_set_sel_val window for picking an attribute to animate
        """ 
        parentObj = mc.ls(sl=1)
        trgt_ctrlrs=[(each) for each in mc.listRelatives(parentObj, ad=1, type="transform") 
        if "_ctrl" in each and "_grp" not in each]
        inst_win = get_set_sel_val(trgt_ctrlrs)

    def test_sel(self):
        """
        Creates an animation based on selected object
            Called up:
                Button "Selected"
            Calls up:
                get_set_sel_val window for picking an attribute to animate
        """ 
        trgt_ctrlrs = mc.ls(sl=1)
        inst_win = get_set_sel_val(trgt_ctrlrs)


    def animate_function(self, get_frames, cust_dict, fnd_dir, trgt_ctrlrs):
        """
        The animation callup. This sets the animation switches (min/max) for attributes 
        and the (on/off) visibility of the correlating camera title 
            Args:
                get_frames (str) : float(8.0) will be the span in which the animation per controller happens sequentially
                cust_dict (str) : If (find_dir = None) the dictionary containing the min/max of the attribute {'ty':'-1.0', '1.0'}
                fnd_dir (str) : The type of animation. (If None), will default to attribute selected in interface with min/max value
                    if other(circle, fig_eight, orbit) it will set a predetermined animation for that controller 
                    and will take Y direcction(if circle)
                    and will take Y min value as scale of the circle to sweep
                    based on transform
                trgt_ctrlrs (str) : the list of selected controllers
            Examples:
                get_frames (str) : 8.0
                cust_dict (str) : {'ty':'-1.0', '1.0'}
                fnd_dir (str) : None
                trgt_ctrlrs (str) : r_arm_wrist_ik_ctrl
            Result:
                animated r_arm_wrist_ik_ctrl.translateY -1.0/1.0 values spanning 8 frames
            Example 2 :
                get_frames (str) : 8.0
                cust_dict (str) : {'ty':'-5.0'}
                fnd_dir (str) : orbit
                trgt_ctrlrs (str) : r_arm_wrist_ik_ctrl
            Result:
                animated r_arm_wrist_ik_ctrl in a orbital arc with a width x5 sweep spanning 8 frames
            Callup:
                get_set_sel_val and: test_attr_controllers
        """ 
        if len(cust_dict)<1:
            print "need to pick a transform from the interface for scale and plane to animate in"
            return
        else:
            pass
        ctrl_set_name = 'titled_controllers' 
        if mc.objExists(ctrl_set_name):
            pass
        else:
            mc.sets(n=ctrl_set_name, co=3)
        mc.sets(trgt_ctrlrs, add=ctrl_set_name)
        fnd_range = len(trgt_ctrlrs)
        get_loc,create_shade_node, annot_title_grp  = self.build_the_cam_titles()
        print trgt_ctrlrs
        if fnd_dir == "none":
            for each in trgt_ctrlrs:
                print each
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
                    strt_tm_frm = get_cur
                    gethalf = get_frames/3
                    active_tm_frm_lo = get_cur+gethalf
                    active_tm_frm_hi = get_cur+gethalf+gethalf
                    end_tm_frm = get_cur+get_frames
                    #keyframe the object
                    mc.setKeyframe(each, at=key, v=find_def_val, time=(strt_tm_frm))
                    mc.setKeyframe(each, at=key, v=value_lo, time=(active_tm_frm_lo))
                    mc.setKeyframe(each, at=key, v=value_hi, time=(active_tm_frm_hi))
                    mc.setKeyframe(each, at=key, v=find_def_val, time=(end_tm_frm))
                    #create the title
                    title_set = each+"."+key
                    if mc.objExists(title_set+'_grp') == False:
                        new_name_annot = self.type_list_preset(title_set, get_loc)
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
                    mc.setKeyframe(new_name_annot, at="visibility", v=0.0, time=(strt_tm_frm)) 
                    mc.setKeyframe(new_name_annot, at="visibility", v=1.0, time=(strt_tm_frm+1))
                    mc.setKeyframe(new_name_annot, at="visibility", v=1.0, time=(end_tm_frm-1))
                    mc.setKeyframe(new_name_annot, at="visibility", v=0.0, time=(end_tm_frm))    
                    mc.currentTime(end_tm_frm)
            mc.select(trgt_ctrlrs, r=1)
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
                    strt_tm_frm = get_cur
                    get_portion = get_frames/20 
                    end_tm_frm = get_cur+get_frames
                    self.create_fig_eight_anim_loc(get_cur, get_portion, each, rotate_plane, size_area)
                    new_name_annot = self.type_list_preset(each, get_loc)
                    try:
                        mc.select(new_name_annot, r=1)
                        mc.hyperShade(assign=str(create_shade_node)) 
                    except:
                        pass
                    try:
                        mc.parent(new_name_annot, annot_title_grp)
                    except:
                        pass
                    mc.setKeyframe(new_name_annot, at="visibility", v=0.0, time=(strt_tm_frm)) 
                    time_frame = get_cur+get_portion*2
                    mc.setKeyframe(new_name_annot, at="visibility", v=1.0, time=time_frame)
                    time_frame = get_cur+get_portion*19
                    mc.setKeyframe(new_name_annot, at="visibility", v=1.0, time=time_frame)
                    time_frame = get_cur+get_portion*20
                    mc.setKeyframe(new_name_annot, at="visibility", v=0.0, time=time_frame)    
                    mc.currentTime(end_tm_frm)
            mc.select(trgt_ctrlrs, r=1)
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
                    strt_tm_frm = get_cur
                    get_portion = get_frames/8
                    end_tm_frm = get_cur+get_frames
                    self.create_circle_anim_loc(get_cur, get_portion, each, rotate_plane, size_area)
                    new_name_annot = self.type_list_preset(each, get_loc)
                    # mc.select(new_name_annot, r=1)
                    try:
                        mc.select(new_name_annot, r=1)
                        mc.hyperShade(assign=str(create_shade_node)) 
                    except:
                        pass
                    try:
                        mc.parent(new_name_annot, annot_title_grp)
                    except:
                        pass
                    mc.setKeyframe(new_name_annot, at="visibility", v=0.0, time=(strt_tm_frm)) 
                    time_frame = get_cur+get_portion*2
                    mc.setKeyframe(new_name_annot, at="visibility", v=1.0, time=time_frame)
                    time_frame = get_cur+get_portion*7
                    mc.setKeyframe(new_name_annot, at="visibility", v=1.0, time=time_frame)
                    time_frame = get_cur+get_portion*8
                    mc.setKeyframe(new_name_annot, at="visibility", v=0.0, time=time_frame)    
                    mc.currentTime(end_tm_frm)
            mc.select(trgt_ctrlrs, r=1)
        elif fnd_dir == "orbit":
            for each in trgt_ctrlrs:
                try:
                    mc.sets(each, add=ctrl_set_name)
                except:
                    pass
                for key, value in cust_dict.items():
                    get_cur = mc.currentTime(q=1)
                    size_area=value[0]*-1
                    rotate_plane = "X"
                    strt_tm_frm = get_cur
                    get_portion = get_frames/16 
                    end_tm_frm = get_cur+get_frames
                    self.create_orbit_anim_loc(get_cur, get_portion, each, size_area)
                    new_name_annot = self.type_list_preset(each, get_loc)
                    try:
                        mc.select(new_name_annot, r=1)
                        mc.hyperShade(assign=str(create_shade_node)) 
                    except:
                        pass
                    try:
                        mc.parent(new_name_annot, annot_title_grp)
                    except:
                        pass
                    mc.setKeyframe(new_name_annot, at="visibility", v=0.0, time=(strt_tm_frm)) 
                    time_frame = get_cur+get_portion*2
                    mc.setKeyframe(new_name_annot, at="visibility", v=1.0, time=time_frame)
                    time_frame = get_cur+get_portion*15
                    mc.setKeyframe(new_name_annot, at="visibility", v=1.0, time=time_frame)
                    time_frame = get_cur+get_portion*16
                    mc.setKeyframe(new_name_annot, at="visibility", v=0.0, time=time_frame)    
                    mc.currentTime(end_tm_frm)
            mc.select(trgt_ctrlrs, r=1)
        mm.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
        mc.setAttr( "{}.scaleZ".format(annot_title_grp[0]), 0.2)        
        mc.setAttr( "{}.scaleX".format(annot_title_grp[0]), 0.2)        
        mc.setAttr( "{}.scaleY".format(annot_title_grp[0]), 0.2)    


    def create_fig_eight_anim_loc(self, get_cur, get_portion, get_obj, directional_plane, size_area):
        """
        The figure eight animation curve applied to object
            Args:
                get_cur (int) : the current time frame on the timeline EG: 1024
                get_portion (float) : the division of the frame range that accomodates the span of keys required
                get_obj (str) : The object that is to be animated
                directional_plane (str) : The direction in which gets animated (XYZ)
                size_area (str) : The scale to which the animation takes place (EG:1, -1, 5)
            Examples:
                get_cur: 1000
                get_portion : (0.40) to cover span of 8 frames needing 20 keys at 0.4 frames.
                get_obj : pSphere
                directional_plane : Z
                size_area : 5
            Results: 
                Locator created and animated in a figure-8 pattern, keying each postion starting at 1000 
                incrementing at 0.40 to make up 8 frame range span with 20 keys, 
                rotated to face the Z axis, scaled to 5 unites. This will then be 
                transfered to the pSphere (control_anim function)
            Callup:
                animate_function
        """ 
        tm_frm_coll = []
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
        tm_frm_coll.append(time_frame)
        self.transform_anim(anim_loc, val00, time_frame)
        val01 = [0.084, 0.0, 0.012,0.0, 0.0, 0.0]
        time_frame = get_cur
        tm_frm_coll.append(time_frame)
        self.transform_anim(anim_loc, val01, time_frame)
        val02 = [0.727, 0.0, .129, 0.0, -20, 0.0]
        time_frame = get_cur+get_portion*2
        tm_frm_coll.append(time_frame)
        self.transform_anim(anim_loc, val02, time_frame)
        val03 = [1.032, 0.0, .785,0.0, -30, 0.0]
        time_frame = get_cur+get_portion*3
        tm_frm_coll.append(time_frame)
        self.transform_anim(anim_loc, val03, time_frame)
        val04 = [0.985, 0.0, 1.406,0.0, 0.0, 0.0]
        time_frame = get_cur+get_portion*4
        tm_frm_coll.append(time_frame)
        self.transform_anim(anim_loc, val04, time_frame)
        val05 = [0.544, 0.0, 1.914,0.0, -40, 0.0]
        time_frame = get_cur+get_portion*5
        tm_frm_coll.append(time_frame)
        self.transform_anim(anim_loc, val05, time_frame)
        val06 = [-0.086, 0.0, 2.058,0.0, -90, 0.0]
        time_frame = get_cur+get_portion*6
        tm_frm_coll.append(time_frame)
        self.transform_anim(anim_loc, val06, time_frame)
        val07 = [-0.701, 0.0, 1.799,0.0, -40, 0.0]
        time_frame = get_cur+get_portion*7
        tm_frm_coll.append(time_frame)
        self.transform_anim( anim_loc, val07, time_frame)
        val08 = [-1.026, 0.0, 1.257,0.0, 0.0, 0.0]
        time_frame = get_cur+get_portion*8
        tm_frm_coll.append(time_frame)
        self.transform_anim(anim_loc, val08, time_frame)
        val09 = [-1.011, 0.0, 0.565,0.0, 30, 0.0]
        time_frame = get_cur+get_portion*9
        tm_frm_coll.append(time_frame)
        self.transform_anim( anim_loc, val09, time_frame)
        val10 = [-0.496, 0.0, 0.035,0.0, 20, 0.0]
        time_frame = get_cur+get_portion*10
        tm_frm_coll.append(time_frame)
        self.transform_anim(anim_loc, val10, time_frame)
        val12 = [0.717, 0.0, -.0142,0.0, -20, 0.0]
        time_frame = get_cur+get_portion*12
        tm_frm_coll.append(time_frame)
        self.transform_anim(anim_loc, val12, time_frame)
        val13 = [1.055, 0.0, -0.786,0.0, -30, 0.0]
        time_frame = get_cur+get_portion*13
        tm_frm_coll.append(time_frame)
        self.transform_anim(anim_loc, val13, time_frame)
        val14 = [0.964, 0.0, -1.441,0.0, 0.0, 0.0]
        time_frame = get_cur+get_portion*14
        tm_frm_coll.append(time_frame)
        self.transform_anim( anim_loc, val14, time_frame)
        val15 = [0.529, 0.0, -1.926,0.0, 40.0, 0.0]
        time_frame = get_cur+get_portion*15
        tm_frm_coll.append(time_frame)
        self.transform_anim( anim_loc, val15, time_frame)
        val16 = [-0.121, 0.0, -2.049,0.0, 90.0, 0.0]
        time_frame = get_cur+get_portion*16
        tm_frm_coll.append(time_frame)
        self.transform_anim( anim_loc, val16, time_frame)
        val17 = [-0.708, 0.0, -1.799, 0.0, -30.0, 0.0]
        time_frame = get_cur+get_portion*17
        tm_frm_coll.append(time_frame)
        self.transform_anim(anim_loc, val17, time_frame)
        val18 = [-1.054, 0.0, -1.195, 0.0, 0.0, 0.0]
        time_frame = get_cur+get_portion*18
        tm_frm_coll.append(time_frame)
        self.transform_anim(anim_loc, val18, time_frame)
        val19 = [-.96, 0.0, -0.605,0.0, 40.0, 0.0]
        time_frame = get_cur+get_portion*19
        tm_frm_coll.append(time_frame)
        self.transform_anim( anim_loc, val19, time_frame)
        val20 = [-0.541, 0.0, -0.09,0.0, 20.0, 0.0]  
        time_frame = get_cur+get_portion*20
        tm_frm_coll.append(time_frame)
        self.transform_anim( anim_loc, val20, time_frame)
        time_frame = get_cur+get_portion*20+1
        tm_frm_coll.append(time_frame)
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
        self.control_anim(tm_frm_coll, get_obj, anim_loc[0])
        mc.delete(anim_loc_grp)        
        

    def create_circle_anim_loc(self, get_cur, get_portion, get_obj, directional_plane, size_area):
        """
        The circle animation curve applied to object
            Args:
                get_cur (int) : the current time frame on the timeline EG: 1024
                get_portion (float) : the division of the frame range that accomodates the span of keys required
                get_obj (str) : The object that is to be animated
                directional_plane (str) : The direction in which gets animated (XYZ)
                size_area (str) : The scale to which the animation takes place (EG:1, -1, 5)
            Examples:
                get_cur: 1000
                get_portion : portion of 1 frame each spaning 8 frames needing 8 keys at 1.0 frames.
                get_obj : pSphere
                directional_plane : Z
                size_area : 5
            Results: 
                Locator created and animated in a flat circle pattern, keying each postion starting at 1000 
                incrementing 8 frames at 1.0 frames to make up 8 frame range span, 
                rotated to face the Z axis, scaled to 5 unites.This will then be 
                transfered to the pSphere (control_anim function)
            Callup:
                animate_function
        """ 
        tm_frm_coll = []
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
        tm_frm_coll.append(time_frame)
        self.transform_anim(anim_loc, val00, time_frame)            
        val01 = [0.0, 0.0, -1.083,0.0, 0.0, 0.0]
        time_frame = get_cur
        tm_frm_coll.append(time_frame)
        self.transform_anim(anim_loc, val01, time_frame)
        val02 = [-0.766, 0.0, -0.766, 0.0, -20, 0.0]
        time_frame = get_cur+get_portion*2
        tm_frm_coll.append(time_frame)
        self.transform_anim(anim_loc, val02, time_frame)
        val03 = [-1.083, 0.0, 0.0,0.0, -30, 0.0]
        time_frame = get_cur+get_portion*3
        tm_frm_coll.append(time_frame)
        self.transform_anim(anim_loc, val03, time_frame)
        val04 = [-0.766, 0.0, 0.766,0.0, 0.0, 0.0]
        time_frame = get_cur+get_portion*4
        tm_frm_coll.append(time_frame)
        self.transform_anim(anim_loc, val04, time_frame)
        val05 = [0.0, 0.0, 1.083,0.0, -40, 0.0]
        time_frame = get_cur+get_portion*5  
        tm_frm_coll.append(time_frame)
        self.transform_anim(anim_loc, val05, time_frame)
        val06 = [0.766, 0.0, 0.766,0.0, -90, 0.0]
        time_frame = get_cur+get_portion*6
        tm_frm_coll.append(time_frame)
        self.transform_anim(anim_loc, val06, time_frame)
        val07 = [1.083, 0.0, 0.0,0.0, -40, 0.0]
        time_frame = get_cur+get_portion*7
        tm_frm_coll.append(time_frame)
        self.transform_anim( anim_loc, val07, time_frame)
        val08 = [0.766, 0.0, -0.766,0.0, 0.0, 0.0]
        time_frame = get_cur+get_portion*8
        tm_frm_coll.append(time_frame)
        self.transform_anim(anim_loc, val08, time_frame)
        time_frame = get_cur+get_portion*8+1
        tm_frm_coll.append(time_frame)
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
        self.control_anim(tm_frm_coll, get_obj, anim_loc[0])
        mc.delete(anim_loc_grp)            
