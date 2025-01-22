# import maya.cmds as mc
import os, sys, subprocess
from datetime import datetime
 
# import xgenm as xg
# import xgenm.xgGlobal as xgg
# import xgenm.XgExternalAPI as xge
 
import re
 
# from mshotgun import mShotgun
import mrig_pyqt
from mrig_pyqt import QtCore, QtGui
from mrig_pyqt.QtGui import QWidget, QRadioButton, QGridLayout, QLabel, QScrollArea, \
    QTableWidget, QComboBox, QKeySequence, QToolButton, QPlainTextEdit, QPushButton,QBoxLayout, \
    QClipboard, QTableWidgetItem, QCheckBox, QVBoxLayout, QHBoxLayout, \
    QPixmap, QLineEdit, QListWidget, QTextEdit, QSizePolicy, QFrame, QPalette, QColor, \
    QFont, QAbstractItemView, QMenu, QMessageBox
from mrig_pyqt.QtCore import SIGNAL
 
from time import gmtime, strftime
         
_project = os.getenv("M_JOB")
_scene = os.getenv("M_SEQUENCE")
_shot = os.getenv("M_LEVEL")
_dept_task = os.getenv("M_TASK")
_get_partial_folder='/jobs/' + _project + '/' + _scene + '/' + _shot + '/PRODUCTS/instances/'
path_build='/jobs/'+_project+'/'+_scene+'/'+_shot+'/TASKS/'+_dept_task+'/maya/scenes/pub_MSG/'
_get_cfx_folder = [(dirpath) for dirpath, dirnames, files in os.walk(_get_partial_folder) if "techanim" in dirpath and "groom" not in dirpath]
collect_assets=[]
for item in _get_cfx_folder:
    find = re.search(r"\d+$", item)
    if find != None:
        ab_seq=item.split("/techanim")[0]
        b_seq=ab_seq.split("instances/")[-1]
        collect_assets.append(b_seq)
get_assets =  set(collect_assets)
 
 
title = str(_shot)+" cfx versions"
 
if len(get_assets) <1:
    _get_cfx_folder = [(dirpath) for dirpath, dirnames, files in os.walk(_get_partial_folder) if "techanim" in dirpath]
    collect_assets=[]
    for item in _get_cfx_folder:
        find = re.search(r"\d+$", item)
        if find != None:
            ab_seq=item.split("/techanim")[0]
            b_seq=ab_seq.split("instances/")[-1]
            collect_assets.append(b_seq)
    get_assets =  set(collect_assets)
    print get_assets
 
class set_pubAssets_win(QtGui.QWidget):
    # def __init__(self):
    def __init__(self):
        super(set_pubAssets_win, self).__init__()
        self.initUI()
 
    def initUI(self):   
        print "This might take a moment. This tool accesses folders on the network and mas. If there are network issues, tools like this will be affected." 
        self.setWindowTitle(title)
 
        self.myform = QtGui.QFormLayout()
        self.layout=QtGui.QGridLayout()
 
 
        self.color_layout=QGridLayout()
        self.color_layout.setAlignment(QtCore.Qt.AlignTop)
         
         
        self.colorSetupLayout=QtGui.QGridLayout()
        self.colorOverride=QtGui.QFrame()
        # self.colorOverride.setFixedHeight(400)
        self.colorOverride.setLayout(self.colorSetupLayout)
        self.colorSetupLayout.addLayout(self.myform, 0,0,1,1)
        self.layout.addLayout(self.colorSetupLayout, 0,0,1,1)
 
        self.btnlayout = QVBoxLayout()
                   
        self.add_widgets()
 
        scroll = QtGui.QScrollArea()
        scroll.setWidget(self.colorOverride)
        scroll.setWidgetResizable(False)
        # scroll.setFixedHeight(400)
        self.layout.addWidget(scroll, 1,0,1,1)
 
 
        self.layout.addLayout(self.btnlayout, 0,0,1,1)   
        self.sel_button = QPushButton("Print")
        self.connect(self.sel_button, SIGNAL("clicked()"),
                    lambda: self.buildVers(self.store_vars))
        self.btnlayout.addWidget(self.sel_button)
        self.save_button = QPushButton("Save")
        self.connect(self.save_button, SIGNAL("clicked()"),
                    lambda: self.saveVers(self.store_vars))
        self.btnlayout.addWidget(self.save_button)
        self.open_folder_button = QPushButton("Open folder")
        self.connect(self.open_folder_button, SIGNAL("clicked()"),
                    lambda: self.open_defined_path())
        self.btnlayout.addWidget(self.open_folder_button)
        self.open_letter_button = QPushButton("Open last msg")
        self.connect(self.open_letter_button, SIGNAL("clicked()"),
                    lambda: self.open_asset_info())
        self.btnlayout.addWidget(self.open_letter_button)   
        self.prnt_letter_button = QPushButton("Print last msg")
        self.connect(self.prnt_letter_button, SIGNAL("clicked()"),
                    lambda: self.print_saved_asset_info())
        self.btnlayout.addWidget(self.prnt_letter_button)    
        self.prnt_verbose_button = QPushButton("Print sources")
        self.connect(self.prnt_verbose_button, SIGNAL("clicked()"),
                    lambda: self.print_verbose(self.store_vars))
        self.btnlayout.addWidget(self.prnt_verbose_button)     
        self.btnlayout_lower = QVBoxLayout()
        self.check_all_button = QPushButton("Check all")
        self.connect(self.check_all_button, SIGNAL("clicked()"),
                    lambda: self.check_butts(self.store_vars))
        self.btnlayout_lower.addWidget(self.check_all_button)     
        self.uncheck_all_button = QPushButton("Uncheck all")
        self.connect(self.uncheck_all_button, SIGNAL("clicked()"),
                    lambda: self.uncheck_butts(self.store_vars))
        self.btnlayout_lower.addWidget(self.uncheck_all_button)   
        self.layout.addLayout(self.btnlayout_lower, 3,0,1,1)                    
        self.setLayout(self.layout)
        self.show()
 
    def add_widgets(self):
        self.asset_dict = {}
        self.store_vars = []
        for each in get_assets:
            gr_container={}
            vr_container = {}
            _get_formal_cfx_folder = [(dirpath) for dirpath, dirnames, files in os.walk(_get_partial_folder) if "techanim" in dirpath and "groom" not in dirpath and each in dirpath]
            _get_grm_folder = [(dirpath) for dirpath, dirnames, files in os.walk(_get_partial_folder) if "techanim" in dirpath and "groom" in dirpath and each in dirpath and "backupFxModule" not in dirpath and "Clumping" not in dirpath and "paintmaps" not in dirpath and "xgenData" not in dirpath ]
            if len(_get_grm_folder)>0:
                # _get_grm_folder = sorted(_get_grm_folder)
                for item in _get_grm_folder:
                    find = re.search(r"\d+$", item)
                    if find != None:
                        a_seq=item.split("techanim/")[-1]
                        ab_seq=item.split("/techanim")[0]
                        b_seq=ab_seq.split("instances/")[-1]
                        container_item={item:a_seq}
                        gr_container.update(container_item)
            # _get_formal_cfx_folder = sorted(_get_formal_cfx_folder)
            for item in _get_formal_cfx_folder:
                find = re.search(r"\d+$", item)
                if find != None:
                    a_seq=item.split("techanim/")[-1]
                    ab_seq=item.split("/techanim")[0]
                    b_seq=ab_seq.split("instances/")[-1]
                    collect_assets.append(b_seq)
                    container_item={item:a_seq}
                    vr_container.update(container_item)
            get_geo_list = sorted(vr_container.values())
            get_gr_list = sorted(gr_container.values())
            get_geo_list = get_geo_list[::-1]
            get_gr_list = get_gr_list[::-1]
            self.cust_path_label = QCheckBox(each)
            self.cust_path_label.setCheckState(mrig_pyqt.QtCore.Qt.Checked)
            self.vertical_order_layout = QtGui.QHBoxLayout()
            # self.cust_path_label = QLabel(each)
            self.ttop_line = QtGui.QFrame()
            self.ttop_line.setFrameShape(QFrame.HLine)
            self.ttop_line.setFrameShadow(QFrame.Sunken)
            self.cust_techanim = QLabel("techanim")
            self.vertical_order_layout_ta = QtGui.QHBoxLayout()
            self.techanim_geo_asset = QComboBox()
            self.techanim_geo_asset.addItems(get_geo_list)   
            self.cust_grm = QLabel("groom")
            self.vertical_order_layout_grm = QtGui.QHBoxLayout()
            self.techanim_gr_asset = QComboBox()
            self.techanim_gr_asset.addItems(get_gr_list)
            # self.myform.addRow(self.cust_path_label)
            self.myform.addRow(self.vertical_order_layout)
            self.myform.addRow(self.vertical_order_layout_ta)
            self.myform.addRow(self.vertical_order_layout_grm)
            self.myform.addRow(self.ttop_line)         
            buildlist= (self.techanim_geo_asset, self.techanim_gr_asset)
            self.vertical_order_layout.addWidget(self.cust_path_label)           
            self.vertical_order_layout_ta.addWidget(self.cust_techanim)      
            self.vertical_order_layout_grm.addWidget(self.cust_grm)      
            self.vertical_order_layout_grm.addWidget(self.techanim_gr_asset)
            self.vertical_order_layout_ta.addWidget(self.techanim_geo_asset)
            create_dict=(self.cust_path_label, buildlist)
            self.store_vars.append(create_dict)
 
    def uncheck_butts(self,asset_dict):
        for each in asset_dict:         
            each[0].setCheckState(mrig_pyqt.QtCore.Qt.Unchecked)
 
    def check_butts(self,asset_dict):
        for each in asset_dict:         
            each[0].setCheckState(mrig_pyqt.QtCore.Qt.Checked)       
        # self.cust_path_label.setCheckState(mrig_pyqt.QtCore.Qt.Checked)















