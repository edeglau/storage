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

pub_cam = ''

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
        self.layout.addLayout(self.btnlayout)


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
        self.cust_checked = QtWidgets.QCheckBox()
        self.value_label = QtWidgets.QLabel("Amount to animate")
        self.lo_label = QtWidgets.QLabel("low")
        self.valueset_lo_one = QtWidgets.QLineEdit("-1")
        self.hi_label = QtWidgets.QLabel("high")
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
        self.cust_checked_six = QtWidgets.QCheckBox()
        self.value_label = QtWidgets.QLabel("Amount to Animate")
     self.valueset_lo_six = QtWidgets.QLineEdit("-1")
        self.valueset_hi_six = QtWidgets.QLineEdit("1")


        self.strLayout = QtWidgets.QGridLayout()
        self.strFrame = QtWidgets.QFrame()
        self.strFrame.setLayout(self.strLayout)
        self.btnlayout.addWidget(self.strFrame)


        self.typeLayout = QtWidgets.QGridLayout()
        self.driftFrame = QtWidgets.QFrame()
        self.driftFrame.setLayout(self.typeLayout)

        self.typ_label = QtWidgets.QLabel("Type")    
        self.typeLayout.addWidget(self.typ_label)

        self.set_dir =["none", "circle", "orbit", "fig_eight"]
        self.dir_list = QtWidgets.QComboBox()
        self.dir_list.addItems(self.set_dir)   
        self.typeLayout.addWidget(self.dir_list)
        self.strLayout.addWidget(self.driftFrame)

        self.attr_all_layout = QtWidgets.QGridLayout()
        self.attr_frame = QtWidgets.QFrame()
        self.attr_frame.setLayout(self.attr_all_layout)
        self.strLayout.addWidget(self.attr_frame)

        self.attr_lbl_layout = QtWidgets.QHBoxLayout()
        self.attr_label = QtWidgets.QLabel("Attributes")    
        self.attr_lbl_layout.addWidget(self.attr_label)
        self.attr_lbl_layout.addWidget(self.lo_label)
        self.attr_lbl_layout.addWidget(self.hi_label)
        self.attr_all_layout.addLayout(self.attr_lbl_layout, 0, 0, 1, 1)  
        
        self.one_layout = QtWidgets.QHBoxLayout()
        self.attr_all_layout.addLayout(self.one_layout, 1, 0, 1, 1)
        self.one_layout.addWidget(self.cust_checked)
        self.one_layout.addWidget(self.attrlist)
        self.one_layout.addWidget(self.valueset_lo_one)
        self.one_layout.addWidget(self.valueset_hi_one)

        self.two_layout = QtWidgets.QHBoxLayout()
        self.attr_all_layout.addLayout(self.two_layout, 2, 0, 1, 1)        
        self.two_layout.addWidget(self.cust_checked_two)
        self.two_layout.addWidget(self.attrlist_two)
        self.two_layout.addWidget(self.valueset_lo_two)
        self.two_layout.addWidget(self.valueset_hi_two)

        self.three_layout = QtWidgets.QHBoxLayout()
        self.attr_all_layout.addLayout(self.three_layout, 3, 0, 1, 1)        
        self.three_layout.addWidget(self.cust_checked_three)
        self.three_layout.addWidget(self.attrlist_three)
        self.three_layout.addWidget(self.valueset_lo_three)
        self.three_layout.addWidget(self.valueset_hi_three)



        self.attr_rot_layout = QtWidgets.QGridLayout()
        self.attr_rot_frame = QtWidgets.QFrame()
        self.attr_rot_frame.setLayout(self.attr_rot_layout)
        self.strLayout.addWidget(self.attr_rot_frame)


        self.four_layout = QtWidgets.QHBoxLayout()
        self.attr_rot_layout.addLayout(self.four_layout, 0, 0, 1, 1)        
        self.four_layout.addWidget(self.cust_checked_four)
        self.four_layout.addWidget(self.attrlist_four)
        self.four_layout.addWidget(self.valueset_lo_four)
        self.four_layout.addWidget(self.valueset_hi_four)

        self.five_layout = QtWidgets.QHBoxLayout()
        self.attr_rot_layout.addLayout(self.five_layout, 1, 0, 1, 1)        
        self.five_layout.addWidget(self.cust_checked_five)
        self.five_layout.addWidget(self.attrlist_five)
        self.five_layout.addWidget(self.valueset_lo_five)
        self.five_layout.addWidget(self.valueset_hi_five)
        

        self.six_layout = QtWidgets.QHBoxLayout()
        self.attr_rot_layout.addLayout(self.six_layout, 2, 0, 1, 1)        
        self.six_layout.addWidget(self.cust_checked_six)
        self.six_layout.addWidget(self.attrlist_six)
        self.six_layout.addWidget(self.valueset_lo_six)
        self.six_layout.addWidget(self.valueset_hi_six)


        self.fr_rng_layout = QtWidgets.QGridLayout()
        self.fr_rng_frame = QtWidgets.QFrame()
        self.fr_rng_frame.setLayout(self.fr_rng_layout)
        self.strLayout.addWidget(self.fr_rng_frame)


        self.frames_label = QtWidgets.QLabel("Across frames")
        self.frames = QtWidgets.QLineEdit("12")


        self.fr_rng_layout.addWidget(self.frames_label)
        self.fr_rng_layout.addWidget(self.frames)

        self.ctrl_button = QtWidgets.QPushButton("Animate Controllers")
        self.ctrl_button.clicked.connect(lambda: self.build_ctrl_annot_one(trgt_ctrlrs))

        self.fr_rng_layout.addWidget(self.ctrl_button)

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
        self.frames_label = QtWidgets.QLabel("Across Frames")
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
        

        self.annt_label = QtWidgets.QLabel("Annotate")
        self.anm_label = QtWidgets.QLabel("Animate")
        self.edt_label = QtWidgets.QLabel("Editing")
        self.annot_sel_button =QtWidgets. QPushButton("Annotate selected")
        self.annot_sel_button.setToolTip("Pipeline issues/data retrieval/IT")
        self.annot_sel_button.clicked.connect(lambda: self.sel_obj_vtx_annot())
        self.auto_annot_button = QtWidgets.QPushButton("Auto Annotate")
        self.auto_annot_button.clicked.connect(lambda: self.dealers_choice())                  
        self.colour_annot_button = QtWidgets.QPushButton("Change Annot Colours")
        self.colour_annot_button.clicked.connect(lambda:self._change_anot_colors())  
        self.mrph_annot_button = QtWidgets.QPushButton("Test Morph targets")
        self.mrph_annot_button.clicked.connect(lambda: self.test_morph()) 
        self.bsp_annot_button = QtWidgets.QPushButton("Test Blendshape weights")
        self.bsp_annot_button.clicked.connect(lambda: self.test_blendShape())       
        self.ctrl_annot_button = QtWidgets.QPushButton("Test Controller heirarchy")
        self.ctrl_annot_button.clicked.connect(lambda: self.ctrlr_annot())     
        self.set_annot_button = QtWidgets.QPushButton("Test Set")
        self.set_annot_button.clicked.connect(lambda: self.set_annot())      
        self.attr_annot_button = QtWidgets.QPushButton("Selected Attribute")
        self.attr_annot_button.clicked.connect(lambda: self.test_attr())   
        self.all_attr_annot_button = QtWidgets.QPushButton("All attribute(s) on Selected")
        self.all_attr_annot_button.clicked.connect(lambda: self.test_attr_controllers())      
        self.sel_annot_button = QtWidgets.QPushButton("Test Selected")
        self.sel_annot_button.clicked.connect(lambda: self.test_sel())     
        self.recon_annot_button = QtWidgets.QPushButton("Reconstrain Title")
        self.recon_annot_button.clicked.connect(lambda: self.retape_to_selection())   
        self.mk_annot_button = QtWidgets.QPushButton("Make Title")
        self.mk_annot_button.clicked.connect(lambda: self.make_arbitrary_title())    
        self.mk_pubcam_button = QtWidgets.QPushButton("Make pub cam")
        self.mk_pubcam_button.clicked.connect(lambda: self.publishable_cam())    



        self.annot_layout = QtWidgets.QGridLayout()
        self.annot_frame = QtWidgets.QFrame()
        self.annot_frame.setLayout(self.annot_layout)
        self.btnlayout.addWidget(self.annot_frame)


        self.anim_layout = QtWidgets.QGridLayout()
        self.anim_frame = QtWidgets.QFrame()
        self.anim_frame.setLayout(self.anim_layout)
        self.btnlayout.addWidget(self.anim_frame)

        self.edt_layout = QtWidgets.QGridLayout()
        self.edt_frame = QtWidgets.QFrame()
        self.edt_frame.setLayout(self.edt_layout)
        self.btnlayout.addWidget(self.edt_frame)
        
        self.annot_layout.addWidget(self.annt_label)     
        self.annot_layout.addWidget(self.auto_annot_button)     
        self.annot_layout.addWidget(self.annot_sel_button)
        self.annot_layout.addWidget(self.colour_annot_button)
        self.anim_layout.addWidget(self.anm_label)
        self.anim_layout.addWidget(self.sel_annot_button)
        self.anim_layout.addWidget(self.attr_annot_button)
        self.anim_layout.addWidget(self.all_attr_annot_button)
        self.anim_layout.addWidget(self.ctrl_annot_button)
        self.anim_layout.addWidget(self.set_annot_button)
        self.anim_layout.addWidget(self.bsp_annot_button)
        self.anim_layout.addWidget(self.mrph_annot_button)
        self.edt_layout.addWidget(self.edt_label)
        self.edt_layout.addWidget(self.mk_annot_button)
        self.edt_layout.addWidget(self.recon_annot_button)
        self.edt_layout.addWidget(self.mk_pubcam_button)

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
            # new_trnsfm_wrld_mtx = [trnsfm_wrld_matrix[0], trnsfm_wrld_matrix[1]+plusnum, trnsfm_wrld_matrix[2]]
            mm.eval('typeCreateText;')            sel_typ = [(hist_type) for hist_type in mc.listHistory(mc.ls(sl=1)) 
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
        if mc.nodeType(mc.ls(sl=1)[0]) == "objectSet":
            get_set = mc.ls(sl=1)
            mc.select(get_set)
            trgt_ctrlrs = mc.ls(sl=1)
            inst_win = get_set_sel_val(trgt_ctrlrs)
        else:
            print "current selection isn't a set"
            return
        
    def ctrlr_annot(self):
        """
        Creates an animation based on selected controller heirarchy
            Called up:
                Button "Test Controller heirarchy"
            Calls up:
                get_set_sel_val window for picking an attribute to animate
        """ 
        parentObj = mc.ls(sl=1)
        try:
            trgt_ctrlrs=[(each) for each in mc.listRelatives(parentObj, ad=1, type="transform") 
            if "_ctrl" in each and "_grp" not in each]
            inst_win = get_set_sel_val(trgt_ctrlrs)
        except:
            print "No heirarchy found from selected"
            pass
        

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
        if fnd_dir == "none":
            for each in trgt_ctrlrs:
                # print each
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
 
    def transform_anim(self, cur_obj, val_list, time_frame):
        """
        This passes the animation from the animated locator (created on the creat anim function) onto the group of controller(s)
            Args:
                cur_obj (str) : The locator object that is to be animated
                val_list (list) : Tranformation list of values
                time_frame (float) : The frame to key 
            Examples:
                cur_obj: pSphere_anim_loc
                val_list : [-0.766, 0.0, 0.766,0.0, 0.0, 0.0]
                anim_loc :  1001.4
            Results: 
                locator will be animated
            Callup:
                create_orbit_anim_loc, create_circle_anim_loc, create_fig_eight_anim_loc
        """ 
        trns = [".tx", ".ty", ".tz", ".rx", ".ry", ".rz"]
        for attr, val in map(None, trns, val_list):
            mc.setKeyframe(cur_obj, at=attr, v=val, time=(time_frame))
            
    def control_anim(self, tm_frm_coll, get_obj, anim_loc):
        """
        This passes the animation from the animated locator (created on the creat anim function) onto the group of controller(s)
            Args:
                tm_frm_coll (list) : The dictionary of animated frames
                get_obj (str) : The object that is to be animated
                anim_loc (str) : The locator that holds the animation
            Examples:
                tm_frm_coll: [1000, 1000.40, 1000.80, 1001.20, 1001.60, ....]
                get_portion : 'pSphere'
                anim_loc : 'pSphere_anim_loc'
            Results: 
                sphere will be animated to the controller
            Callup:
                create_orbit_anim_loc, create_circle_anim_loc, create_fig_eight_anim_loc
        """ 
        for time in tm_frm_coll:
            mc.currentTime(time)
            matrix=mc.xform(anim_loc, q=True, ws=1, t=True)
            mc.xform(get_obj,  ws=1, t=matrix)
            mc.select(get_obj, r=1)
            mc.SetKey()

    def test_attr(self):
        trgt_obj = mc.ls(sl=1)[0]
        #get sel_obj attribute in channelbox
        getChannels =mm.eval('global string $gChannelBoxName; $temp=$gChannelBoxName;')
        try:
            attr_channel = mc.channelBox(getChannels, q=1, sma=1) [0]   
            pass
        except:
            print "select attribute on slected object"
            return
        if mc.attributeQuery(attr_channel, node=trgt_obj, maxExists=1) == True:
            get_val_hi = mc.attributeQuery(attr_channel, node=trgt_obj, max=1)[0]
        else:
            get_val_hi = 1
        def_val = mc.getAttr("{}.{}".format(trgt_obj, attr_channel))
        inst_win = get_val_frm(get_val_hi, def_val, trgt_obj, attr_channel)
    def test_blendShape(self):
        """
        Triggers and animates all the controlWeights on blendshapes node as a sequence 
            Callup:
                "Test Blendshape targets"
        """ 
        try:
            get_bsp_obj = mc.ls(sl=1)
            if mc.nodeType(get_bsp_obj[0]) != "blendShape":
                get_Shapes = [(each) for item in get_bsp_obj for each in mc.listRelatives(item, ad=1, typ="shape")]
                get_bsp = [(items) for shapes in get_Shapes for items in mc.ls(mc.listHistory(shapes), typ='blendShape')]
            else:
                get_bsp = get_bsp_obj
            # trgt_attrs = mc.listAttr("{}.controlWeight".format(get_bsp), m=True) or []
            for blend_item in get_bsp:
                trgt_attrs = mc.listAttr("{}.weight".format(blend_item), m=True) or []
                if len(trgt_attrs)<1:
                    print "cannot find bsp targets"
                    return
                else:
                    getstrt = mc.currentTime(q=1)
                    get_loc,create_shade_node, annot_title_grp  = self.build_the_cam_titles()
                    for each in trgt_attrs:
                        label_object = '{}.{}'.format(get_bsp_obj[0], blend_item)
                        get_cur = mc.currentTime(q=1)
                        strt_tm_frm = get_cur
                        active_tm_frm = get_cur+5
                        end_tm_frm = get_cur+10.0
                        get_val = 1.0
                        def_val = 0.0
                        def_type = 'blendShape'
                        try:
                            self.build_anim_singles(get_val, 
                                                    def_val, 
                                                    blend_item, 
                                                    label_object, 
                                                    each, 
                                                    get_loc, 
                                                    get_cur, 
                                                    strt_tm_frm, 
                                                    active_tm_frm, 
                                                    end_tm_frm, 
                                                    annot_title_grp, 
                                                    def_type, 
                                                    create_shade_node
                                                    )
                            # self.build_anim_singles(get_val, def_val, blend_item, get_bsp_obj[0], each, get_loc, get_cur, strt_tm_frm, active_tm_frm, end_tm_frm, annot_title_grp)
                        except:
                            pass
                mm.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
                mc.setAttr( "{}.scaleZ".format(annot_title_grp[0]), 0.2)        
                mc.setAttr( "{}.scaleX".format(annot_title_grp[0]), 0.2)        
                mc.setAttr( "{}.scaleY".format(annot_title_grp[0]), 0.2)   
        except:
            print "cannot find bsp target weights"
            return


    def test_morph(self):
        """
        Triggers and animates all the controlWeights on a morph node as a sequence 
            Callup:
                "Test Morph targets"
        """ 
        try:
            get_morph_obj = mc.ls(sl=1)[0]
            if mc.nodeType(get_morph_obj) != "morph":
                get_Shape = [(each) for each in mc.listRelatives(get_morph_obj, ad=1, typ="shape")][0]
                get_morph = mc.ls(mc.listHistory(get_Shape), typ='morph')[0]
            else:
                get_morph = get_morph_obj
            trgt_attrs = mc.listAttr("{}.controlWeight".format(get_morph), m=True) or []
            if len(trgt_attrs)<1:
                print "cannot find morph targets" 
                return
            else:
                getstrt = mc.currentTime(q=1)
                get_loc,create_shade_node, annot_title_grp  = self.build_the_cam_titles()
                for each in trgt_attrs:
                    if "_" not in each:
                        get_cur = mc.currentTime(q=1)
                        strt_tm_frm = get_cur
                        active_tm_frm = get_cur+5
                        end_tm_frm = get_cur+10.0
                        get_val = 1.0
                        def_val = 0.0
                        def_type = 'morph'
                        try:
                            self.build_anim_singles(
                                get_val, 
                                def_val, 
                                get_morph, 
                                get_morph_obj, 
                                each, 
                                get_loc, 
                                get_cur, 
                                strt_tm_frm, 
                                active_tm_frm, 
                                end_tm_frm, 
                                annot_title_grp, 
                                def_type,
                                create_shade_node
                                )
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
        """
        Creates the title group for camera lineup with text
        """ 
        try:
            get_loc=mc.ls("*_ploc")[0]
        except:
            get_loc=mc.spaceLocator(n="annot_ploc")
            get_loc=get_loc[0]  
            mc.select(get_loc, r=1)
            mc.group()
            mc.rename(mc.ls(sl=1)[0], 'annot_trn')
            mc.group()
            mc.rename(mc.ls(sl=1)[0], 'annot_loc_trn')
            self.cam_constraint('annot_loc_trn')
            mc.setAttr('annot_trn.ty', -.16)
            mc.setAttr('annot_trn.tz', -.845)
            mc.setAttr('annot_trn.sx', 0.002)
            mc.setAttr('annot_trn.sy', 0.002)
            mc.setAttr('annot_trn.sz', 0.002)
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
    

    def trigger_annot(self, get_val, def_val, get_frames, trgt_obj, attr_channel):
        """
        The function for animating the current selected attribute
            Callup:
                "Selected Attribute"
                get_val_frm
        """
        title_content = trgt_obj+"."+attr_channel
        #add the attributes to a set
        ctrl_set_name = 'titled_controllers' 
        if mc.objExists(ctrl_set_name):
            pass
        else:
            mc.sets(n=ctrl_set_name, co=3)
        mc.sets(trgt_obj, add=ctrl_set_name)
        #create the title group for camera lineup with text
        get_loc,create_shade_node, annot_title_grp  = self.build_the_cam_titles()
        #calculate length and time to key on/off functions
        getstrt = mc.currentTime(q=1)
        getName=["namespace"]
        # for each in trgt_attrs: 
        mc.select(trgt_obj, r=1)
        get_cur = mc.currentTime(q=1)
        strt_tm_frm = get_cur
        div_two = get_frames/2
        active_tm_frm = get_cur+div_two
        # active_tm_frm = trgt_obj
        end_tm_frm = get_cur+get_frames
        def_type = 'None'
        try:
            self.build_anim_singles(get_val, 
                def_val, 
                trgt_obj, 
                trgt_obj, 
                attr_channel, 
                get_loc, 
                get_cur, 
                strt_tm_frm, 
                active_tm_frm, 
                end_tm_frm, 
                annot_title_grp, 
                def_type,
                create_shade_node
                )
        except:
            pass
        mm.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
        mc.setAttr( "{}.scaleZ".format(annot_title_grp[0]), 0.2)        
        mc.setAttr( "{}.scaleX".format(annot_title_grp[0]), 0.2)        
        mc.setAttr( "{}.scaleY".format(annot_title_grp[0]), 0.2)    
        
    def build_anim_singles(self,get_val, 
                            def_val, 
                            obj_item, 
                            sel_obj, 
                            anim_attr, 
                            get_loc, 
                            get_cur, 
                            strt_tm_frm, 
                            active_tm_frm, 
                            end_tm_frm, 
                            annot_title_grp, 
                            def_type,
                            create_shade_node,
                            ):
        print obj_item, sel_obj, anim_attr        
        '''
        This passes the animation from the animated locator (created on the creat anim function) onto the group of controller(s)
            Args:
                get_val(float) : the maximum active value to animate the attribute
                obj_item(str) : the object the attribute belongs to(EG:sphere1)
                sel_obj(str) : the sel_obj object the attribute belongs to(EG:morph node)
                anim_attr(str) : the attribute to key
                get_loc(str) : the object in which the resulting title will be contrained to(annot_loc_trn)
                strt_tm_frm(float) : the relative frame that the animation of that attribute starts(EG:1000)
                active_tm_frm(float) : the "on" time frame for the attribute to be tested at(EG:1008)
                end_tm_frm(float) : the relative frame that the animation of that attribute ends(EG:1012)
            Examples:
                get_val(float) : 90.0
                obj_item(str) : pSphere)
                sel_obj(str) : morph1(if using morph)
                anim_attr(str) : translateX
                get_loc(str) : annot_loc_trn
                strt_tm_frm(float) : 1000
                active_tm_frm(float) : 1008
                end_tm_frm(float) : 1012
            Results: 
                pSphere.pivot will be animated on by a value of 90
            Callup:
                test_morph, trigger_annot

        '''
        ctrl_set_name = 'titled_controllers' 
        if mc.objExists(ctrl_set_name):
            pass
        else:
            mc.sets(n=ctrl_set_name, co=3)
        try:
            mc.sets(sel_obj, add=ctrl_set_name)
        except:
            print "cannot add {} to set".format(sel_obj)
            pass
        print def_type
        if def_type == 'blendShape': 
            if '.' in sel_obj:
                sel_obj = sel_obj.replace('.', '_')
            if mc.objExists('{}_{}_grp'.format(sel_obj, anim_attr)) == False:
                    title_label = sel_obj+'.'+anim_attr
                    new_name_annot = self.type_list_preset(title_label, get_loc)
            else:
                new_name_annot = mc.ls('{}_{}_grp'.format(sel_obj, anim_attr))[0]
        elif def_type == 'morph':
            if mc.objExists('{}_{}_grp'.format(obj_item, anim_attr)) == False:
                title_label = obj_item+'.'+anim_attr
                new_name_annot = self.type_list_preset(title_label, get_loc)
            else:
                new_name_annot = mc.ls('{}_{}_grp'.format(obj_item, anim_attr))[0]
        else:
            if mc.objExists('{}_{}_grp'.format(sel_obj, anim_attr)) == False:
                title_label = sel_obj+'.'+anim_attr
                new_name_annot = self.type_list_preset(title_label, get_loc)
            else:
                new_name_annot = mc.ls('{}_{}_grp'.format(sel_obj, anim_attr))[0]
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
        mc.setKeyframe(obj_item, at=anim_attr, v=def_val, time=(strt_tm_frm))   
        mc.setKeyframe(obj_item, at=anim_attr, v=get_val, time=(active_tm_frm))
        mc.setKeyframe(obj_item, at=anim_attr, v=def_val, time=(end_tm_frm))
        #key the title
        mc.setKeyframe(new_name_annot, at="visibility", v=0.0, time=(strt_tm_frm)) 
        mc.setKeyframe(new_name_annot, at="visibility", v=1.0, time=(strt_tm_frm+1))
        mc.setKeyframe(new_name_annot, at="visibility", v=1.0, time=(end_tm_frm-1))       
        mc.setKeyframe(new_name_annot, at="visibility", v=0.0, time=(end_tm_frm))    
        mc.currentTime(end_tm_frm)

    
inst_win = annot_range_win()
inst_win.show()    

