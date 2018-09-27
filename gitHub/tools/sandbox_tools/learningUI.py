__author__="Elise Deglau"
import maya.cmds as cmds
# from mshotgun import mShotgun
 
 
import mrig_pyqt
from mrig_pyqt import QtCore, QtGui
from mrig_pyqt.QtGui import QWidget, QRadioButton, QGridLayout, QLabel, \
    QTableWidget, QComboBox, QKeySequence, QToolButton, QPlainTextEdit, QPushButton,QBoxLayout, \
    QClipboard, QTableWidgetItem, QCheckBox, QVBoxLayout, QHBoxLayout, \
    QPixmap, QLineEdit, QListWidget, QTextEdit, QSizePolicy, QFrame, QPalette, QColor, \
    QFont, QAbstractItemView, QMenu, QMessageBox
from mrig_pyqt.QtCore import SIGNAL
 
#QI:12407 is the smallest uninteresting integer
 
 
import shutil
import os, sys, operator, re, glob, getpass, subprocess, shutil, string, random, ast, webbrowser, time, datetime
from subprocess import Popen, PIPE
from os import stat, listdir, walk
from pwd import getpwuid
import os.path
from os.path import isfile, join
from datetime import datetime
buttonGrp=[]
import mTools
reload (mTools)
import mockTools
reload (mockTools)
failedComments=[
                "defaultText",
                "",
                "-",
                "_",
                "asdf",
                "asd",
                ".",
                "oo",
                "0",
                "00",
                " ",
                "qwer",
                "qwerty"
                ]
 
presetlist=["load"]
typesOfReview=['review', 'review_anim', 'delivery']
__location__=os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
 
availableStyles=['darkOrange']
styleSheetFile=availableStyles[0]
 
headers = ('Name', 'Date', 'Path', 'Sub')
get_a_play_list=["load", "build"]
alist2=['listone', 'listtwo']
setDefaultType=['review']
col1, col2, col3, col4= 240, 160, 500, 50
pre=[]
regular=[(150,70,70), (150,150,70), (100, 100, 170)]
regularDict={"darkRed":(150,70,70), "yellow":(120,120,70), "green":(70, 150, 70), "blue":(50,100,200)}
buttonColoursDict=regularDict
developer=[__author__]
defaultText="defaultText"
 
M_USER = os.getenv("USER")
 
 
PROJECT=os.getenv("M_JOB")
SCENE=os.getenv("SEQUENCE_SHOT_")
SHOT=os.getenv("M_LEVEL")
DEPT=os.getenv("M_TASK")
 
# spaceWork=cmds.workspace(q=1, lfw=1)[-1]
 
projectFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT
animFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/instances/'
abcFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/cache/alembic/'
pbFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/movies/'
rvFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/'+DEPT
spaceWork='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/scenes'
 
pathways={'open folder':spaceWork, "work":spaceWork, "project":projectFolder, "products":animFolder, "alembic":abcFolder, "blasts":rvFolder}
 
 
 
blendoptions=['blendType', 'Grp_to_Grp', "Mass_blnd", "Grp_search_blend", "Grp_search_conn", "Grp_search_blend_alias", "Grp_morph_alias"]
 
 
 
sgVarFilePath = '/jobs/%s/%s/%s/TECH/lib/shotgun/setshot.d/sgvars' % (PROJECT, SCENE, SHOT)
if os.path.isfile(sgVarFilePath):
    # get available in/out values
    franges = {'WORK_IN': None, 'CUT_IN': None,
               'WORK_OUT': None, 'CUT_OUT': None}
    for line in open(sgVarFilePath, 'r'):
        if "CUT_DURATION" in line:
            shot_len_value = line.split('=')[-1].strip()
            try:
                shot_len_value = int(shot_len_value)
            except:
                shot_len_value = None
        if 'CUT_IN' in line:
            cut_in_value = line.split('=')[-1].strip()
            try:
                cut_in_value = int(cut_in_value)
            except:
                cut_in_value = None
        if 'CUT_OUT' in line:
            cut_out_value = line.split('=')[-1].strip()
            try:
                cut_out_value = int(cut_out_value)
            except:
                cut_out_value = None
        if 'WORK_IN' in line:
            wk_strt_value = line.split('=')[-1].strip()
            try:
                wk_strt_value = int(wk_strt_value)
            except:
                wk_strt_value = None
        if 'WORK_OUT' in line:
            wk_out_value = line.split('=')[-1].strip()
            try:
                wk_out_value = int(wk_out_value)
            except:
                wk_out_value = None
        if 'CUT_IN' in line:
            cut_shouldbe_in_value = line.split('=')[-1].strip()
            try:
                cut_shouldbe_in_value = int(cut_shouldbe_in_value)-8
            except:
                cut_shouldbe_in_value = None
        if 'CUT_OUT' in line:
            cut_shouldbe_out_value = line.split('=')[-1].strip()
            try:
                cut_shouldbe_out_value = int(cut_shouldbe_out_value)+8
            except:
                cut_shouldbe_out_value = None
 
print "launching window..."
try:
    winTitle=PROJECT+" : "+SHOT+" : (F"+str(shot_len_value)+")   :   ( "+str(wk_strt_value-1)+"  |[ "+str(wk_strt_value)+" <<<["+str(cut_in_value)+"-"+str(cut_out_value)+"]>>> "+str(wk_out_value)+" ]|  "+str(wk_out_value+1)+" )"
except:
    winTitle=PROJECT+" : "+SHOT
 
 
class Expression_Examples(QtGui.QWidget):
    def __init__(self):
        super(Expression_Examples, self).__init__()
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle("Expressions")
        self.layout = QVBoxLayout()
        self.btnlayout = QHBoxLayout()
        self.playlist_names = QComboBox()
        self.layout.addLayout(self.btnlayout)
        self.label = QTextEdit()
        self.label.setText("nucleus1_wind_CTRL.windSpeed = abs( noise( frame * .05) * 8);\
            \n\n#connect:\
            \nlocator1_WIND.localWind =  abs( noise(sin(frame* .001)*8)*2)\
            \n\n#connect:\
            \nvortexField1.magnitude=turbulenceField1.magnitude;\
            \n\n#sine:\
            \npSphere1.translateY = sin(time);\
            \n\n#bounce:\
            \n$sine = sin(frame * .001);\
            \npSphere1.translateY =  abs( noise($sine) *4);\
            \n\n#bounce random:\
            \npSphere1.translateY =  abs( noise(sin(frame* .01) *2));\
            \n\n#offset:\
            \nint $currentTime=`currentTime -q`;\
            \nint $offset=5;\
            \n$offsetTime=$currentTime-$offset;\
            \n$getPos=`getAttr -t $offsetTime pSphere1.rotateY`;\
            \npSphere1.rotateY=$getPos;\
            \nint $offset=7;\
            \n$offsetTime=$currentTime-$offset;\
            \n$getPos=`getAttr -t $offsetTime pSphere1.rotateY`;\
            \npSphere2.rotateY=$getPos;\
            ")
        self.sel_button = QPushButton(" close")
        self.connect(self.sel_button, SIGNAL("clicked()"),lambda: self.gotoAppend())
        self.btnlayout.addWidget(self.label)
        self.btnlayout.addWidget(self.sel_button)
        self.setLayout(self.layout)
 
    def gotoAppend(self):
        self.close()
 
 
class clothCheck_UI(QtGui.QWidget):
    def __init__(self):
        super(clothCheck_UI, self).__init__()
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle("Check cloth scene health")
        self.checklayout = QVBoxLayout()
        self.checkLayout = QVBoxLayout()
        self.playlist_names = QComboBox()
        self.checklayout.addLayout(self.checkLayout)
        self.check_all = QPushButton("check all")
        self.connect(self.check_all, SIGNAL("clicked()"),lambda: self._check_all())
        self.checkLayout.addWidget(self.check_all)
        self.check_none = QPushButton("check none")
        self.connect(self.check_none, SIGNAL("clicked()"),lambda: self._check_none())
        self.checkLayout.addWidget(self.check_none)
        self.checkRange = QCheckBox("Framerange")
        self.checkRange.setCheckState(mrig_pyqt.QtCore.Qt.Unchecked)
        self.checkLayout.addWidget(self.checkRange)
        self.nuc_category = QLabel("Nucleus")
        self.nuc_enable = QCheckBox("nuc enabled")
        self.nuc_enable.setCheckState(mrig_pyqt.QtCore.Qt.Checked)
        self.checkLayout.addWidget(self.nuc_enable)
        self.checkLayout.addWidget(self.nuc_category)
        self.nuc_strt = QCheckBox("Nucleus startframe")
        self.nuc_strt.setCheckState(mrig_pyqt.QtCore.Qt.Checked)
        self.checkLayout.addWidget(self.nuc_strt)
        self.space_scale = QCheckBox("space scale")
        self.space_scale.setCheckState(mrig_pyqt.QtCore.Qt.Checked)
        self.checkLayout.addWidget(self.space_scale)
        self.nuc_subs = QCheckBox("substeps")
        self.nuc_subs.setCheckState(mrig_pyqt.QtCore.Qt.Checked)
        self.checkLayout.addWidget(self.nuc_subs)
        self.coll_iter = QCheckBox("collision iterations")
        self.coll_iter.setCheckState(mrig_pyqt.QtCore.Qt.Checked)
        self.checkLayout.addWidget(self.coll_iter)
        self.rgd_category = QLabel("Rigids")
        self.checkLayout.addWidget(self.rgd_category)
        self.rgd_pnt_mass = QCheckBox("rgd point mass")
        self.rgd_pnt_mass.setCheckState(mrig_pyqt.QtCore.Qt.Checked)
        self.checkLayout.addWidget(self.rgd_pnt_mass)
        self.clth_category = QLabel("Cloth")
        self.checkLayout.addWidget(self.clth_category)
        self.scale_rel = QCheckBox("scale relations")
        self.scale_rel.setCheckState(mrig_pyqt.QtCore.Qt.Checked)
        self.checkLayout.addWidget(self.scale_rel)
 
        self.trap_check = QCheckBox("trapped check")
        self.trap_check.setCheckState(mrig_pyqt.QtCore.Qt.Checked)
        self.checkLayout.addWidget(self.trap_check)
 
 
        self.clth_enable = QCheckBox("enabled")
        self.clth_enable.setCheckState(mrig_pyqt.QtCore.Qt.Checked)
        self.checkLayout.addWidget(self.clth_enable)
 
        self.dyn_cnstrnt_category = QLabel("Dynamic Constraints")
        self.checkLayout.addWidget(self.dyn_cnstrnt_category)
 
        self.dyncnstrnt_exc = QCheckBox("dconstrnt exclusions")
        self.dyncnstrnt_exc.setCheckState(mrig_pyqt.QtCore.Qt.Checked)
        self.checkLayout.addWidget(self.dyncnstrnt_exc)
 
 
        self.dyncnstrnt_cmp = QCheckBox("dconstrnt component")
        self.dyncnstrnt_cmp.setCheckState(mrig_pyqt.QtCore.Qt.Checked)
        self.checkLayout.addWidget(self.dyncnstrnt_cmp)
 
 
        self.dry_button = QPushButton("dry run")
        self.connect(self.dry_button, SIGNAL("clicked()"),lambda: self.dry_run())
        self.checkLayout.addWidget(self.dry_button)
        self.doit_button = QPushButton("check cloth scene")
        self.connect(self.doit_button, SIGNAL("clicked()"),lambda: self.checkit())
        self.checkLayout.addWidget(self.doit_button)
        self.close_button = QPushButton("close")
        self.connect(self.close_button, SIGNAL("clicked()"),lambda: self.gotoAppend())
        # self.checkLayout.addWidget(self.label)
        self.checkLayout.addWidget(self.close_button)
        self.setLayout(self.checklayout)
 
    def gotoAppend(self):
        self.close()
 
    def dry_run(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.troubleshoot_clth()
 
    def checkit(self):
        check_dict={}
        getrange={"range":self.checkRange.checkState()}
        check_dict.update(getrange)
        getnucstart={"nucstart":self.nuc_strt.checkState()}
        check_dict.update(getnucstart)
        getnucenable={"nucenable":self.nuc_enable.checkState()}
        check_dict.update(getnucenable)
        getspcscl={"nuc_spc_scl":self.space_scale.checkState()}
        check_dict.update(getspcscl)
        getnucsubstp={"nuc_sub_stp":self.nuc_subs.checkState()}
        check_dict.update(getnucsubstp)
        getnuccoliter={"nuc_col_itr":self.coll_iter.checkState()}
        check_dict.update(getnuccoliter)
        getrdgmss={"rgd_mass":self.rgd_pnt_mass.checkState()}
        check_dict.update(getrdgmss)
        getsclerel={"scl_rel":self.scale_rel.checkState()}
        check_dict.update(getsclerel)
        getdyncnstrntexcl={"dyn_cnstrnt_exc":self.dyncnstrnt_exc.checkState()}
        check_dict.update(getdyncnstrntexcl)
        getdyncnstrntcmpl={"dyn_cnstrnt_cmp":self.dyncnstrnt_cmp.checkState()}
        check_dict.update(getdyncnstrntcmpl)
        getclthenble={"clthenable":self.clth_enable.checkState()}
        check_dict.update(getclthenble)
        getclthtrpchk={"clth_trp_chk":self.trap_check.checkState()}
        check_dict.update(getclthtrpchk)
        get_baseTools=mockTools.mToolKit()
        get_baseTools.set_troubleshoot(check_dict)
 
    def _check_all(self):
        self.checkRange.setCheckState(mrig_pyqt.QtCore.Qt.Checked)
        self.nuc_strt.setCheckState(mrig_pyqt.QtCore.Qt.Checked)
        self.clth_enable.setCheckState(mrig_pyqt.QtCore.Qt.Checked)
        self.nuc_enable.setCheckState(mrig_pyqt.QtCore.Qt.Checked)
        self.space_scale.setCheckState(mrig_pyqt.QtCore.Qt.Checked)
        self.nuc_subs.setCheckState(mrig_pyqt.QtCore.Qt.Checked)
        self.coll_iter.setCheckState(mrig_pyqt.QtCore.Qt.Checked)
        self.rgd_pnt_mass.setCheckState(mrig_pyqt.QtCore.Qt.Checked)
        self.scale_rel.setCheckState(mrig_pyqt.QtCore.Qt.Checked)
        self.dyncnstrnt_exc.setCheckState(mrig_pyqt.QtCore.Qt.Checked)
        self.dyncnstrnt_cmp.setCheckState(mrig_pyqt.QtCore.Qt.Checked)
        self.clth_enable.setCheckState(mrig_pyqt.QtCore.Qt.Checked)
 
    def _check_none(self):
        self.checkRange.setCheckState(mrig_pyqt.QtCore.Qt.Unchecked)
        self.nuc_strt.setCheckState(mrig_pyqt.QtCore.Qt.Unchecked)
        self.clth_enable.setCheckState(mrig_pyqt.QtCore.Qt.Unchecked)
        self.nuc_enable.setCheckState(mrig_pyqt.QtCore.Qt.Unchecked)
        self.space_scale.setCheckState(mrig_pyqt.QtCore.Qt.Unchecked)
        self.nuc_subs.setCheckState(mrig_pyqt.QtCore.Qt.Unchecked)
        self.coll_iter.setCheckState(mrig_pyqt.QtCore.Qt.Unchecked)
        self.rgd_pnt_mass.setCheckState(mrig_pyqt.QtCore.Qt.Unchecked)
        self.scale_rel.setCheckState(mrig_pyqt.QtCore.Qt.Unchecked)
        self.dyncnstrnt_exc.setCheckState(mrig_pyqt.QtCore.Qt.Unchecked)
        self.dyncnstrnt_cmp.setCheckState(mrig_pyqt.QtCore.Qt.Unchecked)
        self.trap_check.setCheckState(mrig_pyqt.QtCore.Qt.Unchecked)
 
class typicalWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(typicalWindow, self).__init__(parent)
        new_sgVarFilePath, projectFolder, animFolder, abcFolder, pbFolder, rvFolder, getDeptRVFolder=self.getSetup(PROJECT, SCENE, SHOT)
        getDepts = os.listdir(getDeptRVFolder)
        # QtGui.QMainWindow.__init__(self)
        #window
        self.setWindowTitle(winTitle)
        self.central_widget=QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.masterLayout=QGridLayout(self.central_widget)
        self.masterLayout.setAlignment(QtCore.Qt.AlignTop)
 
        fileMenu = QtGui.QMenu("&Tips", self)
        self.menuBar().addMenu(fileMenu)
 
        fileMenu.addAction("&Expressions...", self.extractAction, "Ctrl+N")
 
 
        #mainlayout
        self.vertical_order_layout=QtGui.QHBoxLayout()
        self.vertical_order_layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignVCenter)
        self.masterLayout.addLayout(self.vertical_order_layout, 0,0,1,1)
         
        self.topDivideLayout=QGridLayout()
        self.botDivideLayout=QGridLayout()
        self.upper_layout=QGridLayout()
         
         
        self.topDivideLayout.addLayout(self.upper_layout, 0,0,1,1)
         
        self.lower_layout=QGridLayout()
        self.lower_layout.setAlignment(QtCore.Qt.AlignTop)
        self.botDivideLayout.addLayout(self.lower_layout, 0,0,1,1)
         
        self.midLayout=QGridLayout()
        self.midLayout.setAlignment(QtCore.Qt.AlignTop)
        self.topDivideLayout.addLayout(self.midLayout, 2,0,1,1)
         
        self.base_layout=QGridLayout()
        self.base_layout.setAlignment(QtCore.Qt.AlignTop)
        self.botDivideLayout.addLayout(self.base_layout, 2,0,1,1)
         
        sshFile=open(os.path.join(__location__, styleSheetFile+".stylesheet"), 'r')
        self.styleData=sshFile.read()
        sshFile.close
         
        self.setStyleSheet(self.styleData)
        self.top=QtGui.QFrame(self)
        self.top.setFrameShape(QtGui.QFrame.StyledPanel)
        self.top.setLayout(self.topDivideLayout)
         
        self.bottom=QtGui.QFrame(self)
        self.bottom.setFrameShape(QtGui.QFrame.StyledPanel)
        self.bottom.setLayout(self.botDivideLayout)
         
        self.splitPlane=QtGui.QSplitter(QtCore.Qt.Vertical)
        self.splitPlane.addWidget(self.top)
        self.splitPlane.addWidget(self.bottom)
        self.splitPlane.setSizes([650, 650])
        self.vertical_order_layout.addWidget(self.splitPlane)
         
        #layouts
        self.window_layer_00=QGridLayout()
        self.upper_layout.addLayout(self.window_layer_00, 0,0,1,1)
         
        self.window_layer_01=QGridLayout()
        self.upper_layout.addLayout(self.window_layer_01,1,0,1,1)
         
        self.window_layer_02=QGridLayout()
        self.upper_layout.addLayout(self.window_layer_02, 2,0,1,1)
         
        self.window_layer_03=QGridLayout()
        self.upper_layout.addLayout(self.window_layer_03,3,0,1,1)
         
        self.window_layer_04=QGridLayout()
        self.upper_layout.addLayout(self.window_layer_04, 4,0,1,1)
         
        self.window_layer_05=QGridLayout()
        self.upper_layout.addLayout(self.window_layer_05,5,0,1,1)
         
        self.window_layer_06=QGridLayout()
        self.midLayout.addLayout(self.window_layer_06, 6,0,1,1)
         
 
     
        self.btm_btn_layout=QtGui.QGridLayout()
        self.btm_btn_layout.setAlignment(QtCore.Qt.AlignTop)
        self.btm_btn_layout.setContentsMargins(5,10,5,10)  
        self.wbFrame=QtGui.QFrame()
        self.wbFrame.setStyleSheet("background-color: #434343; border-style: solid; border-width: 2px; border-color:#434343;border-radius:8px;")
        self.btm_over_layout=QtGui.QGridLayout()
        self.btm_over_layout.setAlignment(QtCore.Qt.AlignTop)
        self.btm_over_layout.addLayout(self.btm_btn_layout, 0,0,1,1)
        self.btm_over_layout.addWidget(self.wbFrame, 0,0,1,1)
         
        self.pkt_layout= QGridLayout()
        self.pkt_layout.setAlignment(QtCore.Qt.AlignTop)
        self.pkt_widget=QGridLayout()
        self.pkt_widget.setContentsMargins(5,5,5,5)
        self.pkt_frame=QFrame()
        self.pkt_frame.setMinimumWidth(650)
        self.pkt_frame.setStyleSheet("background-color: #434343; border-style: solid; border-width: 2px; border-color:#434343;border-radius:8px;")
        self.base_layout.addLayout(self.pkt_layout, 0,0,1,1)
         
        self.wndw_layer_pkt=QtGui.QGridLayout()
        self.wndw_layer_pkt.setAlignment(QtCore.Qt.AlignTop)
        self.pkt_widget.addLayout(self.wndw_layer_pkt, 0,0,1,1)
         
        self.park_btn_pkt=QtGui.QHBoxLayout()
        self.park_btn_pkt.setAlignment(QtCore.Qt.AlignTop)
        self.park_btn_pkt.setContentsMargins(5,2,5,8)
        self.wndw_layer_pkt.addLayout(self.park_btn_pkt, 0,0,1,1)
        self.park_frame=QtGui.QFrame()
        self.park_frame.setStyleSheet("background-color: #434343; border-style: solid; border-width: 2px; border-color:#434343;border-radius:8px;")
         
 
        # self.blend_button=QPushButton("BlendGrps")
        # self.blend_button.setToolTip("Select driving group, select driver group. press this button")
        # self.connect(self.blend_button, SIGNAL('clicked()'), self.BlendGrps_butt)
        # self.window_layer_01.addWidget(self.blend_button, 0,3,1,1)
 
 
 
        self.lit_cam_button=QPushButton("lit cam")
        self.lit_cam_button.setToolTip("lit with occ")
        self.lit_cam_button.setStyleSheet("color: #b1b1b1; background-color: rgba(200,200,70,100);")
        self.connect(self.lit_cam_button, SIGNAL('clicked()'), self._lit_cam)
        self.window_layer_01.addWidget(self.lit_cam_button, 1,4, 1,1)
 
 
 
        self.load_attr_button=QPushButton("load attr UI")
        self.load_attr_button.setToolTip("reset to current shot")
        self.load_attr_button.setStyleSheet("color: #b1b1b1; background-color: rgba(130,175,175,100);")
        self.connect(self.load_attr_button, SIGNAL('clicked()'), self.save_import_attrs)
        self.window_layer_01.addWidget(self.load_attr_button, 1,0,1,1)
 
        self.sel_arry_btton=QPushButton("Select Array")
        self.sel_arry_btton.setToolTip("select palette")
        self.sel_arry_btton.setStyleSheet("color: #b1b1b1; background-color: rgba(130,175,175,100);")
        self.connect(self.sel_arry_btton, SIGNAL('clicked()'), self._select_array)
        self.window_layer_01.addWidget(self.sel_arry_btton, 1,1,1,1)
 
        self.renamer_button=QPushButton("Renamer")
        self.renamer_button.setToolTip("point glue many meshes to one(select parent first)")
        self.renamer_button.setStyleSheet("color: #b1b1b1; background-color: rgba(130,175,175,100);")
        self.connect(self.renamer_button, SIGNAL('clicked()'), self._renamer)
        self.window_layer_01.addWidget(self.renamer_button, 1,2,1,1)
 
        self.ftchwin_button=QPushButton("fetch attr")
        self.ftchwin_button.setToolTip("point glue many meshes to one(select parent first)")
        self.ftchwin_button.setStyleSheet("color: #b1b1b1; background-color: rgba(130,175,175,100);")
        self.connect(self.ftchwin_button, SIGNAL('clicked()'), self._fetchAttr_win)
        self.window_layer_01.addWidget(self.ftchwin_button, 1,3,1,1)
 
        self.groom_tool_button=QPushButton("groom tools?")
        self.groom_tool_button.setToolTip("point glue many meshes to one(select parent first)")
        # self.groom_tool_button.setStyleSheet("color: #b1b1b1; background-color: rgba(130,175,175,100);")
        self.connect(self.groom_tool_button, SIGNAL('clicked()'), self._check_grmtools)
        self.window_layer_01.addWidget(self.groom_tool_button, 2,4,1,1)
 
        self.anim_export_button=QPushButton("anim export")
        self.anim_export_button.setToolTip("opens the anim export menu if shelf busts")
        self.connect(self.anim_export_button, SIGNAL('clicked()'), self._anim_export)
        self.window_layer_01.addWidget(self.anim_export_button, 2,0,1,1)
 
        self.auto_anot_button=QPushButton("auto annot")
        self.auto_anot_button.setToolTip("annotate all in scene")
        self.connect(self.auto_anot_button, SIGNAL('clicked()'), self._autoAnnot)
        self.window_layer_01.addWidget(self.auto_anot_button, 3,0,1,1)
 
 
        self.select_half_rand=QPushButton("select random half")
        self.select_half_rand.setToolTip("reduces the selection to half and to a random shuffle")
        self.connect(self.select_half_rand, SIGNAL('clicked()'), self.select_half)
        self.window_layer_01.addWidget(self.select_half_rand, 4,2,1,1)
 
        self.cln_crv_mesh=QPushButton("cleancurves")
        self.cln_crv_mesh.setToolTip("uses eugene hair tools for cleaning the inside curves in the mesh")
        self.connect(self.cln_crv_mesh, SIGNAL('clicked()'), self._clean_mesh_curves)
        self.window_layer_01.addWidget(self.cln_crv_mesh, 4,3,1,1)
 
        self.cln_button=QPushButton("clean model")
        self.cln_button.setToolTip("clean a model's history")
        self.cln_button.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        self.connect(self.cln_button, SIGNAL('clicked()'), self.cleanModels)
        self.window_layer_01.addWidget(self.cln_button, 4,4,1,1)
 
        self.annotate_button=QPushButton("annotate")
        self.annotate_button.setToolTip("annotate selected verts")
        self.connect(self.annotate_button, SIGNAL('clicked()'), self._annots)
        self.window_layer_01.addWidget(self.annotate_button, 3,1,1,1)
 
        self.annotate_button=QPushButton("wit cam")
        self.annotate_button.setToolTip("select two edges and create witness camera")
        self.connect(self.annotate_button, SIGNAL('clicked()'), self._wit_cam)
        self.window_layer_01.addWidget(self.annotate_button, 3,2,1,1)
 
        # self.hookup_button=QPushButton("prep hair file for save")
        # self.hookup_button.setToolTip("sets the known fixes before saving")
        # self.connect(self.hookup_button, SIGNAL('clicked()'), self._fix_hairfx_scene)
        # self.window_layer_01.addWidget(self.hookup_button, 2,0,1,1)
 
        # self.hookup_button=QPushButton("reinit hair")
        # self.hookup_button.setToolTip("sets the known fixes before saving")
        # self.connect(self.hookup_button, SIGNAL('clicked()'), self._reinit_hair)
        # self.window_layer_01.addWidget(self.hookup_button, 2,1,1,1)
 
        self.hookup_button=QPushButton("bsp_tools")
        self.hookup_button.setStyleSheet("color: #b1b1b1; background-color: rgba(130,175,175,100);")
        self.hookup_button.setToolTip("")
        self.connect(self.hookup_button, SIGNAL('clicked()'), self._bsptools)
        self.window_layer_01.addWidget(self.hookup_button, 2,2,1,1)
 
        self.hookup_button=QPushButton("techgrp")
        self.hookup_button.setToolTip("")
        self.connect(self.hookup_button, SIGNAL('clicked()'), self._techgrp)
        self.window_layer_01.addWidget(self.hookup_button, 2,3,1,1)
 
        self.chk_clth_button=QPushButton("check cloth")
        self.chk_clth_button.setToolTip("")
        self.connect(self.chk_clth_button, SIGNAL('clicked()'), self._check_clth)
        self.window_layer_01.addWidget(self.chk_clth_button, 3,3,1,1)
 
        # self.chk_clth_button=QPushButton("cachePlay")
        # self.chk_clth_button.setToolTip("")
        # self.connect(self.chk_clth_button, SIGNAL('clicked()'), self._cache_play)
        # self.window_layer_01.addWidget(self.chk_clth_button, 6,3,1,1)
 
        self.tbl_clth_button=QPushButton("troubleshoot cloth")
        self.tbl_clth_button.setStyleSheet("color: #b1b1b1; background-color: rgba(130,175,175,100);")
        self.tbl_clth_button.setToolTip("")
        # self.connect(self.tbl_clth_button, SIGNAL('clicked()'), self._tbl_clth)
        self.connect(self.tbl_clth_button, SIGNAL('clicked()'), self.cloth_TS_UI)
        self.window_layer_01.addWidget(self.tbl_clth_button, 3,4,1,1)
 
 
 
        self.frame_layout=QGridLayout()
        self.frame_layout.setAlignment(QtCore.Qt.AlignTop)
        self.lower_layout.addLayout(self.frame_layout, 0,0,1,1)
         
         
        self.frameSetupLayout=QtGui.QGridLayout()
        self.frameSetupLayout.setContentsMargins(5,10,5,10)
        self.frameOverride=QtGui.QFrame()
        self.frameOverride.setStyleSheet("background-color: #434343; border-style: solid; border-width: 2px; border-color:#434343;border-radius:8px;")
        self.frameOverride.setFixedHeight(100)
        self.frameOverride.setLayout(self.frameSetupLayout)
        # self.frame_layout.addLayout(self.frameSetupLayout, 0,0,1,1)
        self.frame_layout.addWidget(self.frameOverride, 0,0,1,1)
         
         
        self.frame_title_layout=QGridLayout()
        self.frameSetupLayout.addLayout(self.frame_title_layout, 0,0,1,1)
        self.frame_radio_layout=QGridLayout()
        self.frameSetupLayout.addLayout(self.frame_radio_layout, 1,0,1,1)
        self.frame_btn_layout=QGridLayout()
        self.frame_layout.addLayout(self.frame_btn_layout, 2,0,1,1)
 
 
 
 
 
        self.radiobox=QGridLayout()
        self.frame_title_layout.addLayout(self.radiobox, 1,0,1,1)
 
        self.labelradiobox = QLabel()
        self.labelradiobox.setText("Select dependant")
        self.radiobox.addWidget(self.labelradiobox, 0,0,1,1)
 
        self.sel_nuc_button=QPushButton("grab nucleus")
        self.sel_nuc_button.setToolTip("grab dynamic nucleus connected with selection")
        self.sel_nuc_button.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        self.connect(self.sel_nuc_button, SIGNAL('clicked()'), self._grab_nucleus)
        self.radiobox.addWidget(self.sel_nuc_button, 1,0,1,1)
 
        self.sel_msh_h_button=QPushButton("grab mesh heirarchy")
        self.sel_msh_h_button.setToolTip("grab dynamic nucleus connected with selection")
        self.sel_msh_h_button.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        self.connect(self.sel_msh_h_button, SIGNAL('clicked()'), self._grab_msh_heir)
        self.radiobox.addWidget(self.sel_msh_h_button, 2,1,1,1)
 
        self.sel_nuc_button=QPushButton("grab mesh")
        self.sel_nuc_button.setToolTip("grab the mesh of the selected cloth")
        self.sel_nuc_button.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        self.connect(self.sel_nuc_button, SIGNAL('clicked()'), self._grab_mesh)
        self.radiobox.addWidget(self.sel_nuc_button, 0,1,1,1)
 
        self.sel_nuc_button=QPushButton("grab ncloth")
        self.sel_nuc_button.setStyleSheet("color: #b1b1b1; background-color: rgba(175,70,70,50);")
        self.sel_nuc_button.setToolTip("grab the cloth of the selected mesh")
        self.connect(self.sel_nuc_button, SIGNAL('clicked()'), self._grab_ncloth)
        self.radiobox.addWidget(self.sel_nuc_button, 0,2,1,1)
 
        self.sel_nuc_button=QPushButton("grab nhair")
        self.sel_nuc_button.setStyleSheet("color: #b1b1b1; background-color: rgba(175,70,70,50);")
        self.sel_nuc_button.setToolTip("grab the cloth of the selected mesh")
        self.connect(self.sel_nuc_button, SIGNAL('clicked()'), self._grab_nhair)
        self.radiobox.addWidget(self.sel_nuc_button, 1,2,1,1)
 
        self.sel_nuc_button=QPushButton("grab cache")
        self.sel_nuc_button.setToolTip("grab the cache file of the selected object")
        self.sel_nuc_button.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        self.connect(self.sel_nuc_button, SIGNAL('clicked()'), self._grab_cache)
        self.radiobox.addWidget(self.sel_nuc_button, 0,3,1,1)
 
        self.sel_nuc_button=QPushButton("grab blend shape")
        self.sel_nuc_button.setToolTip("grab the blend file of the selected object")
        self.sel_nuc_button.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        self.connect(self.sel_nuc_button, SIGNAL('clicked()'), self._grab_bs)
        self.radiobox.addWidget(self.sel_nuc_button, 1,1,1,1)
 
 
        self.sel_nuc_button=QPushButton("grab nConstraint")
        self.sel_nuc_button.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        self.sel_nuc_button.setToolTip("grab the nconstraints")
        self.connect(self.sel_nuc_button, SIGNAL('clicked()'), self._grab_nconstraints)
        self.radiobox.addWidget(self.sel_nuc_button, 1,3,1,1)
 
        self.sel_trnsfr_button=QPushButton("transfer selected")
        self.sel_trnsfr_button.setToolTip("select an object or verts, select a nearby object to tranfer the selection to the other object")
        self.sel_trnsfr_button.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        self.connect(self.sel_trnsfr_button, SIGNAL('clicked()'), self._grab_transfer)
        self.radiobox.addWidget(self.sel_trnsfr_button, 2,0,1,1)
 
 
        # self.sel_hrp_button=QPushButton("grab hair property")
        # self.sel_hrp_button.setToolTip("grab the cache file of the selected object")
        # self.sel_hrp_button.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        # self.connect(self.sel_hrp_button, SIGNAL('clicked()'), self._grab_hrprop)
        # self.radiobox.addWidget(self.sel_hrp_button, 1,1,1,1)
 
        # self.sel_hrs_button=QPushButton("grab hair simulator")
        # self.sel_hrs_button.setToolTip("grab the blend file of the selected object")
        # self.sel_hrs_button.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        # self.connect(self.sel_hrs_button, SIGNAL('clicked()'), self._grab_hrsim)
        # self.radiobox.addWidget(self.sel_hrs_button, 1,2,1,1)
 
 
        self.nucleus_layout=QGridLayout()
        self.nucleus_layout.setAlignment(QtCore.Qt.AlignTop)
        self.lower_layout.addLayout(self.nucleus_layout, 3,0,1,1)
         
        self.nucleusSetupLayout=QtGui.QGridLayout()
        self.nucleusOverride=QtGui.QFrame()
        self.nucleusOverride.setStyleSheet("background-color: #434343; border-style: solid; border-width: 2px; border-color:#434343;border-radius:8px;")
        # self.nucleusOverride.setFixedHeight(100)
        self.nucleusOverride.setLayout(self.nucleusSetupLayout)
        self.nucleus_layout.addWidget(self.nucleusOverride, 0,0,1,1)
         
         
        self.nucleus_title_layout=QGridLayout()
        self.nucleusSetupLayout.addLayout(self.nucleus_title_layout, 0,0,1,1)
        self.nucleus_radio_layout=QGridLayout()
        self.nucleusSetupLayout.addLayout(self.nucleus_radio_layout, 1,0,1,1)
        self.nucleus_btn_layout=QGridLayout()
        self.nucleus_layout.addLayout(self.nucleus_btn_layout, 2,0,1,1)
 
        self.nucleusbox=QGridLayout()
        self.nucleus_title_layout.addLayout(self.nucleusbox, 2,0,1,1)
 
 
        self.labelradiobox = QLabel()
        self.labelradiobox.setText("Nucleus")
        self.nucleusbox.addWidget(self.labelradiobox, 0,0,1,1)
 
        self.init_range_button=QPushButton("Initialize")
        self.init_range_button.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        self.init_range_button.setToolTip("reset to current shot")
        self.connect(self.init_range_button, SIGNAL('clicked()'), self.init_from_range_butt)
        self.nucleusbox.addWidget(self.init_range_button, 1,0,1,1)
         
        self.init_nuc_button=QPushButton("Init_to_nuc")
        self.init_nuc_button.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        self.init_nuc_button.setToolTip("reset to current shot")
        self.connect(self.init_nuc_button, SIGNAL('clicked()'), self.init_from_nuc_butt)
        self.nucleusbox.addWidget(self.init_nuc_button, 1,1,1,1)
         
        self.init_frm_button=QPushButton("nuc_to_fframe")
        self.init_frm_button.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        self.init_frm_button.setToolTip("reset to current shot")
        self.connect(self.init_frm_button, SIGNAL('clicked()'), self.nuc_to_first)
        self.nucleusbox.addWidget(self.init_frm_button, 1,2,1,1)
 
        self.nuc_rvt_buttn=QPushButton("parent nucleus rivet")
        self.nuc_rvt_buttn.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        self.nuc_rvt_buttn.setToolTip("point constraint nucleus to rivet created by two selected edges")
        self.connect(self.nuc_rvt_buttn, SIGNAL('clicked()'), self._nuc_rvt)
        self.nucleusbox.addWidget(self.nuc_rvt_buttn, 0,2,1,1)
 
        self.nuc_root_buttn=QPushButton("parent nucleus root")
        self.nuc_root_buttn.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        self.nuc_root_buttn.setToolTip("point constraint nucleus to root joint in techanim setup shot")
        self.connect(self.nuc_root_buttn, SIGNAL('clicked()'), self._nuc_root)
        self.nucleusbox.addWidget(self.nuc_root_buttn, 0,3,1,1)
 
        self.nuc_neck_buttn=QPushButton("parent nucleus neck")
        self.nuc_neck_buttn.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        self.nuc_neck_buttn.setToolTip("point constraint nucleus to neck joint in techanim setup shot")
        self.connect(self.nuc_neck_buttn, SIGNAL('clicked()'), self._nuc_neck)
        self.nucleusbox.addWidget(self.nuc_neck_buttn, 1,3,1,1)
 
 
        self.color_layout=QGridLayout()
        self.color_layout.setAlignment(QtCore.Qt.AlignTop)
        self.lower_layout.addLayout(self.color_layout, 5,0,1,1)
         
         
        self.colorSetupLayout=QtGui.QGridLayout()
        self.colorOverride=QtGui.QFrame()
        self.colorOverride.setStyleSheet("background-color: #434343; border-style: solid; border-width: 2px; border-color:#434343;border-radius:8px;")
        # self.colorOverride.setFixedHeight(100)
        self.colorOverride.setLayout(self.colorSetupLayout)
        self.color_layout.addWidget(self.colorOverride, 0,0,1,1)
         
         
        self.color_title_layout=QGridLayout()
        self.colorSetupLayout.addLayout(self.color_title_layout, 0,0,1,1)
        self.color_radio_layout=QGridLayout()
        self.colorSetupLayout.addLayout(self.color_radio_layout, 1,0,1,1)
        self.color_btn_layout=QGridLayout()
        self.color_layout.addLayout(self.color_btn_layout, 2,0,1,1)
 
 
        self.colorbox=QGridLayout()
        self.color_title_layout.addLayout(self.colorbox, 2,0,1,1)
 
        self.labelradiobox = QLabel()
        self.labelradiobox.setText("Display")
        self.colorbox.addWidget(self.labelradiobox, 2,0,1,1)
 
        self.tch_col_buttn=QPushButton("tech rgb")
        self.tch_col_buttn.setToolTip("rgb tech geos")
        self.tch_col_buttn.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        self.connect(self.tch_col_buttn, SIGNAL('clicked()'), self._get_geo_techanim)
        self.colorbox.addWidget(self.tch_col_buttn, 3,2,1,1)
 
        self.tch_col_buttn=QPushButton("change primary color")
        self.tch_col_buttn.setToolTip("rgb tech geos")
        self.tch_col_buttn.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        self.connect(self.tch_col_buttn, SIGNAL('clicked()'), self._change_primary_grn)
        self.colorbox.addWidget(self.tch_col_buttn, 4,2,1,1)
 
        self.apply_col_buttn=QPushButton("apply rgb")
        self.apply_col_buttn.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        self.apply_col_buttn.setToolTip("change rgb values on shader")
        self.connect(self.apply_col_buttn, SIGNAL('clicked()'), self.apply_colors)
        self.colorbox.addWidget(self.apply_col_buttn, 3,3,1,1)
 
        self.change_gry_buttn=QPushButton("change greyrgb")
        self.change_gry_buttn.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        self.change_gry_buttn.setToolTip("change rgb values on shader")
        self.connect(self.change_gry_buttn, SIGNAL('clicked()'), self.change_grey)
        self.colorbox.addWidget(self.change_gry_buttn, 2,1,1,1)
 
        self.apply_gry_buttn=QPushButton("apply greyrgb")
        self.apply_gry_buttn.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        self.apply_gry_buttn.setToolTip("change rgb values on shader")
        self.connect(self.apply_gry_buttn, SIGNAL('clicked()'), self.apply_grey_colors)
        self.colorbox.addWidget(self.apply_gry_buttn, 3,1,1,1)
 
        self.chng_col_buttn=QPushButton("change rgb")
        self.chng_col_buttn.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        self.chng_col_buttn.setToolTip("change rgb values on shader")
        self.connect(self.chng_col_buttn, SIGNAL('clicked()'), self.change_colors)
        self.colorbox.addWidget(self.chng_col_buttn, 2,2,1,1)
 
        self.chng_amb_buttn=QPushButton("change amb")
        self.chng_amb_buttn.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        self.chng_amb_buttn.setToolTip("change ambient values on shader")
        self.connect(self.chng_amb_buttn, SIGNAL('clicked()'), self.change_ambient)
        self.colorbox.addWidget(self.chng_amb_buttn, 2,3,1,1)
 
        self.fix_rb_buttn=QPushButton("fix the rainbow")
        self.fix_rb_buttn.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        self.fix_rb_buttn.setToolTip("turns off the display color override")
        self.connect(self.fix_rb_buttn, SIGNAL('clicked()'), self._fix_RB)
        self.colorbox.addWidget(self.fix_rb_buttn, 3,0,1,1)
 
        self.hair_prev_buttn=QPushButton("preview modes")
        self.hair_prev_buttn.setToolTip("UI for changing viewport into different modes for working with xgen/setting model preferences(turns selectable geo on)")
        self.hair_prev_buttn.setStyleSheet("color: #b1b1b1; background-color: rgba(130,175,175,100);")
        self.connect(self.hair_prev_buttn, SIGNAL('clicked()'), self._rocket_fur_preview)
        self.colorbox.addWidget(self.hair_prev_buttn, 4,1,1,1)
 
 
 
        self.cache_layout=QGridLayout()
        self.cache_layout.setAlignment(QtCore.Qt.AlignTop)
        self.lower_layout.addLayout(self.cache_layout, 4,0,1,1)
         
        self.cacheSetupLayout=QtGui.QGridLayout()
        self.cacheOverride=QtGui.QFrame()
        self.cacheOverride.setStyleSheet("background-color: #434343; border-style: solid; border-width: 2px; border-color:#434343;border-radius:8px;")
        # self.cacheOverride.setFixedHeight(100)
        self.cacheOverride.setLayout(self.cacheSetupLayout)
        self.cache_layout.addWidget(self.cacheOverride, 0,0,1,1)
         
         
        self.cache_title_layout=QGridLayout()
        self.cacheSetupLayout.addLayout(self.cache_title_layout, 0,0,1,1)
        self.cache_radio_layout=QGridLayout()
        self.cacheSetupLayout.addLayout(self.cache_radio_layout, 1,0,1,1)
        self.cache_btn_layout=QGridLayout()
        self.cache_layout.addLayout(self.cache_btn_layout, 2,0,1,1)
 
 
        self.cachebox=QGridLayout()
        self.cache_title_layout.addLayout(self.cachebox, 2,0,1,1)
 
        self.labelradiobox = QLabel()
        self.labelradiobox.setText("Caches")
        self.cachebox.addWidget(self.labelradiobox, 0,0,1,1)
 
        self.dyn_names_button=QPushButton("clean caches")
        self.dyn_names_button.setToolTip("removes cachefiles and blends on selected (or all hair caches if nothing selected)")
        self.dyn_names_button.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        self.connect(self.dyn_names_button, SIGNAL('clicked()'), self._clear_cache)
        self.cachebox.addWidget(self.dyn_names_button, 2,0,1,1)
 
        self.chk_clth_button=QPushButton("cachePlay")
        self.chk_clth_button.setToolTip("")
        self.chk_clth_button.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        self.connect(self.chk_clth_button, SIGNAL('clicked()'), self._cache_play)
        self.cachebox.addWidget(self.chk_clth_button, 2,1,1,1)
 
        self.offset_cache_buttn=QPushButton("abc_curves")
        self.offset_cache_buttn.setToolTip("GUI abc animwire/nhair caching: options to set live, cache, set a cache on either abc or nhair")
        self.offset_cache_buttn.setStyleSheet("color: #b1b1b1; background-color: rgba(130,175,175,100);")
        self.connect(self.offset_cache_buttn, SIGNAL('clicked()'), self._abc_xgen)
        self.cachebox.addWidget(self.offset_cache_buttn, 2,2,1,1)
 
 
        self.find_cache_buttn=QPushButton("cache find")
        self.find_cache_buttn.setToolTip("GUI: enter the path to where a large amount of caches live. this will help load and playblast them")
        self.find_cache_buttn.setStyleSheet("color: #b1b1b1; background-color: rgba(130,175,175,100);")
        self.connect(self.find_cache_buttn, SIGNAL('clicked()'), self._cache_window)
        self.cachebox.addWidget(self.find_cache_buttn, 2,3,1,1)
             
 
 
        self.fix_layout=QGridLayout()
        self.fix_layout.setAlignment(QtCore.Qt.AlignTop)
        self.upper_layout.addLayout(self.fix_layout, 4,0,1,1)
         
        self.fixSetupLayout=QtGui.QGridLayout()
        self.fixOverride=QtGui.QFrame()
        self.fixOverride.setStyleSheet("background-color: #434343; border-style: solid; border-width: 2px; border-color:#434343;border-radius:8px;")
        # self.fixOverride.setFixedHeight(100)
        self.fixOverride.setLayout(self.fixSetupLayout)
        self.fix_layout.addWidget(self.fixOverride, 0,0,1,1)
         
        self.fix_title_layout=QGridLayout()
        self.fixSetupLayout.addLayout(self.fix_title_layout, 0,0,1,1)
        self.fix_radio_layout=QGridLayout()
        self.fixSetupLayout.addLayout(self.fix_radio_layout, 1,0,1,1)
        self.fix_btn_layout=QGridLayout()
        self.fix_layout.addLayout(self.fix_btn_layout, 2,0,1,1)
 
        self.fixbox=QGridLayout()
        self.fix_title_layout.addLayout(self.fixbox, 2,0,1,1)
 
        self.labelradiobox = QLabel()
        self.labelradiobox.setText("Fixes")
        self.fixbox.addWidget(self.labelradiobox, 0,0,1,1)
 
        self.blur_button=QPushButton("fix blur frames")
        self.blur_button.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        # self.blur_button.setToolTip("blends and keys output curves for fixes")
        self.connect(self.blur_button, SIGNAL('clicked()'), self._blur_frames)
        self.fixbox.addWidget(self.blur_button, 1,2,1,1)
 
        self.mp_fix_button=QPushButton("fix methpipe")
        self.mp_fix_button.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        # self.mp_fix_button.setToolTip("blends and keys output curves for fixes")
        self.connect(self.mp_fix_button, SIGNAL('clicked()'), self._fix_methpipe)
        self.fixbox.addWidget(self.mp_fix_button, 0,1,1,1)
 
        self.cam_fix_button=QPushButton("fix cam")
        self.cam_fix_button.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        # self.cam_fix_button.setToolTip("blends and keys output curves for fixes")
        self.connect(self.cam_fix_button, SIGNAL('clicked()'), self._fix_cam)
        self.fixbox.addWidget(self.cam_fix_button, 0,2,1,1)
 
        self.fix_undo_button=QPushButton("fix undo")
        self.fix_undo_button.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        # self.fix_undo_button.setToolTip("blends and keys output curves for fixes")
        self.connect(self.fix_undo_button, SIGNAL('clicked()'), self._fix_undo)
        self.fixbox.addWidget(self.fix_undo_button, 0,3,1,1)
 
        self.opt_maya_butt=QPushButton("optimize")
        self.opt_maya_butt.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        self.opt_maya_butt.setToolTip("shuts off unneeded plugins and high rez swatches")
        self.connect(self.opt_maya_butt, SIGNAL('clicked()'), self._opt_maya)
        self.fixbox.addWidget(self.opt_maya_butt, 1,0, 1,1)
 
 
        self.fix_frm_button=QPushButton("fix playblast frames")
        self.fix_frm_button.setToolTip("removes roll frames and maintains only the work range in folder for submit")
        self.fix_frm_button.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        self.connect(self.fix_frm_button, SIGNAL('clicked()'), self._fix_frames)
        self.fixbox.addWidget(self.fix_frm_button, 1,1,1,1)
 
 
        self.cor_shape=QPushButton("corshape")
        self.cor_shape.setStyleSheet("color: #b1b1b1; background-color: rgba(175,70,70,50);")
        self.cor_shape.setToolTip("create a shape from current frame")
        self.connect(self.cor_shape, SIGNAL('clicked()'), self.corrective_shape)
        self.frame_btn_layout.addWidget(self.cor_shape, 0,0, 1,1)
 
 
        self.cor_shape=QPushButton("edge to edge")
        self.cor_shape.setToolTip("select edge of one polyObj and edge of another, this will follow like a quill on a feather")
        self.connect(self.cor_shape, SIGNAL('clicked()'), self._edge_to_edge)
        self.frame_btn_layout.addWidget(self.cor_shape, 0,1, 1,1)
 
 
        self.cor_shape=QPushButton("shape to shape")
        self.cor_shape.setToolTip("select edge of one polyObj and edge of another, this will match a shape to follow another")
        self.connect(self.cor_shape, SIGNAL('clicked()'), self._shape_to_shape)
        self.frame_btn_layout.addWidget(self.cor_shape, 0,2, 1,1)
 
 
        self.curve_xgen_button=QPushButton("xgen curve shapes")
        self.curve_xgen_button.setToolTip("blends and keys output curves for fixes")
        self.connect(self.curve_xgen_button, SIGNAL('clicked()'), self._postTech_crv_shapes)
        self.frame_btn_layout.addWidget(self.curve_xgen_button, 0,3,1,1)
 
 
        self.pointGlu_button=QPushButton("pointGlue all to 1")
        self.pointGlu_button.setToolTip("point glue many meshes to one(select parent first)")
        self.pointGlu_button.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        self.connect(self.pointGlu_button, SIGNAL('clicked()'), self._pointGlue_mass_to_one)
        self.frame_btn_layout.addWidget(self.pointGlu_button, 1, 0,1,1)
 
 
        self.pointGlu_button=QPushButton("pointGlue 1 to all")
        self.pointGlu_button.setToolTip("point glue many meshes to one(select parent first)")
        self.pointGlu_button.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        self.connect(self.pointGlu_button, SIGNAL('clicked()'), self._pointGlue_one_to_mass)
        self.frame_btn_layout.addWidget(self.pointGlu_button, 2, 0,1,1)
 
        self.cape_button=QPushButton("cape")
        self.cape_button.setToolTip("cape")
        self.cape_button.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        self.connect(self.cape_button, SIGNAL('clicked()'), self._cape_callup)
        self.frame_btn_layout.addWidget(self.cape_button, 1, 1,1,1)
 
        self.xform_button=QPushButton("Match Xform")
        self.xform_button.setToolTip("point glue many meshes to one(select parent first)")
        self.xform_button.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        self.connect(self.xform_button, SIGNAL('clicked()'), self._match_xform)
        self.frame_btn_layout.addWidget(self.xform_button, 1,2,1,1)
 
        self.copy_att_button=QPushButton("Copy attributes")
        self.copy_att_button.setToolTip("point glue many meshes to one(select parent first)")
        self.copy_att_button.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        self.connect(self.copy_att_button, SIGNAL('clicked()'), self._copy_attr)
        self.frame_btn_layout.addWidget(self.copy_att_button, 1,3,1,1)
 
        self.hela_col_button=QPushButton("fix collide")
        self.connect(self.hela_col_button, SIGNAL('clicked()'), self._fix_hela_collide)
        # self.hela_col_button.setStyleSheet("color: #b1b1b1; background-color: rgba(255,200,150,100);")
        self.frame_btn_layout.addWidget(self.hela_col_button, 2,3,1,1)
 
 
        self.dyn_names_button=QPushButton("scissor fix")
        self.dyn_names_button.setToolTip("launch the scissor fix window")
        self.dyn_names_button.setStyleSheet("color: #b1b1b1; background-color: rgba(130,175,175,100);")
        self.connect(self.dyn_names_button, SIGNAL('clicked()'), self._scissor_win)
        self.frame_btn_layout.addWidget(self.dyn_names_button, 4,1,1,1)
 
 
        self.build_crv_button=QPushButton("wire wrap")
        self.build_crv_button.setToolTip("select two or more verts to generate a curve from a surface and wire wrap")
        self.connect(self.build_crv_button, SIGNAL('clicked()'), self._wire_wrap)
        self.frame_btn_layout.addWidget(self.build_crv_button, 4,2,1,1)
 
        self.build_crv_button=QPushButton("cloth strips")
        self.build_crv_button.setToolTip("select two or more verts to generate a cloth strip and wrap")
        self.connect(self.build_crv_button, SIGNAL('clicked()'), self._cloth_strips)
        self.frame_btn_layout.addWidget(self.build_crv_button, 4,3,1,1)
 
 
        self.print_asset_button=QPushButton("shot asset info")
        self.print_asset_button.setStyleSheet("color: #b1b1b1; background-color: rgba(70,70,170,50);")
        self.print_asset_button.setToolTip("saves the print info into a local working shot folder")
        self.connect(self.print_asset_button, SIGNAL('clicked()'), self._save_asset_info_cfx)
        self.frame_btn_layout.addWidget(self.print_asset_button, 7,0,1,1)
 
 
        self.print_asset_button=QPushButton("anim asset info")
        self.print_asset_button.setStyleSheet("color: #b1b1b1; background-color: rgba(70,70,170,50);")
        self.print_asset_button.setToolTip("saves the print info into a local working shot folder")
        self.connect(self.print_asset_button, SIGNAL('clicked()'), self._save_asset_info_anim)
        self.frame_btn_layout.addWidget(self.print_asset_button, 8,0,1,1)
 
 
        self.mm_button=QPushButton("MM item")
        self.mm_button.setToolTip("for item: cache or abc item. import, select item, select rig which you want to set the relatoin offset and click button")
        self.connect(self.mm_button, SIGNAL('clicked()'), self._mm_item)
        self.frame_btn_layout.addWidget(self.mm_button, 2,2,1,1)
 
        self.build_crv_button=QPushButton("build curve")
        self.build_crv_button.setToolTip("select two or more verts to generate a curve from a surface")
        self.connect(self.build_crv_button, SIGNAL('clicked()'), self._build_curve)
        self.frame_btn_layout.addWidget(self.build_crv_button, 7,2,1,1)
 
        self.wire_button=QPushButton("wire")
        self.wire_button.setToolTip("creates a wire deformer with selected mesh and wire")
        self.connect(self.wire_button, SIGNAL('clicked()'), self._wirewrap)
        self.frame_btn_layout.addWidget(self.wire_button, 7,3,1,1)     
 
        # self.print_asset_button=QPushButton("MM techrig")
        # self.print_asset_button.setToolTip("Select techrig and run")
        # self.connect(self.print_asset_button, SIGNAL('clicked()'), self._mm_techrig)
        # self.frame_btn_layout.addWidget(self.print_asset_button, 8,0,1,1)
 
 
        self.print_asset_button=QPushButton("print asset")
        self.print_asset_button.setStyleSheet("color: #b1b1b1; background-color: rgba(70,70,170,50);")
        self.print_asset_button.setToolTip("print asset information (to copy and paste to comments)")
        self.connect(self.print_asset_button, SIGNAL('clicked()'), self._print_asset)
        self.frame_btn_layout.addWidget(self.print_asset_button, 7,1,1,1)
 
 
        self.offset_cache_buttn=QPushButton("Offset cache")
        self.offset_cache_buttn.setToolTip("displace the cache to another cache position")
        self.connect(self.offset_cache_buttn, SIGNAL('clicked()'), self._offset_cache)
        self.frame_btn_layout.addWidget(self.offset_cache_buttn, 2,1,1,1)
 
 
        # self.break_con_button=QPushButton("break connections")
        # self.break_con_button.setToolTip("breaks typical connections on the main controller")
        # self.connect(self.break_con_button, SIGNAL('clicked()'), self._break_con)
        # self.frame_btn_layout.addWidget(self.break_con_button, 4,2,1,1)
 
        self.swrp_mshct_button=QPushButton("shrinkwrap meshcut")
        self.swrp_mshct_button.setToolTip("sets a shrink wrap to ideal meshcut settings")
        self.connect(self.swrp_mshct_button, SIGNAL('clicked()'), self._shrinkwrap_meshcut)
        self.frame_btn_layout.addWidget(self.swrp_mshct_button, 4,0,1,1)
 
 
        self.dyn_names_button=QPushButton("dynamic names")
        self.dyn_names_button.setToolTip("rename dynamic constraints")
        self.connect(self.dyn_names_button, SIGNAL('clicked()'), self._dyn_names)
        self.frame_btn_layout.addWidget(self.dyn_names_button, 8,1,1,1)
 
        self.dyn_names_button=QPushButton("100 percent prims")
        self.dyn_names_button.setToolTip("set all primitives to 100 % preview for blasts")
        self.connect(self.dyn_names_button, SIGNAL('clicked()'), self._perc_preview)
        self.frame_btn_layout.addWidget(self.dyn_names_button, 8,3,1,1)
 
 
        if "vfx_1224" in PROJECT:
            self.fixcam_attr=QPushButton("fix cam hol1650")
            self.fixcam_attr.setStyleSheet("color: #b1b1b1; background-color: rgba(255,200,150,100);")
            self.fixcam_attr.setToolTip("breaks fins into separate pieces (originally for nh0290)")
            self.connect(self.fixcam_attr, SIGNAL('clicked()'), self._fixcam_attr)
            self.frame_btn_layout.addWidget(self.fixcam_attr, 10,0,1,1)
 
        if "vfx_volt" in PROJECT:
            self.kelpie_button=QPushButton("kelpie prosthetics")
            self.kelpie_button.setStyleSheet("color: #b1b1b1; background-color: rgba(255,200,150,100);")
            self.kelpie_button.setToolTip("breaks fins into separate pieces (originally for nh0290)")
            self.connect(self.kelpie_button, SIGNAL('clicked()'), self._kelpie_prost)
            self.frame_btn_layout.addWidget(self.kelpie_button, 10,0,1,1)      
        #   # self.ffur_buttn=QPushButton("fix fur normals")
        #   # self.ffur_buttn.setStyleSheet("color: #b1b1b1; background-colo          r: rgba(255,200,150,100);")
        #   # self.ffur_buttn.setToolTip("unlock rocket's normals(fixes scattered curves on body)")
        #   # self.connect(self.ffur_buttn, SIGNAL('clicked()'), self._fixfur)
        #   # self.frame_btn_layout.addWidget(self.ffur_buttn, 5,1,1,1)
        #   self.sthair_buttn=QPushButton("Strands Dyn Static")
        #   self.sthair_buttn.setStyleSheet("color: #b1b1b1; background-color: rgba(255,200,150,100);")
        #   self.sthair_buttn.setToolTip("makes the selected sim curves static(works on postTech)")
        #   self.connect(self.sthair_buttn, SIGNAL('clicked()'), self._statichair)
        #   self.frame_btn_layout.addWidget(self.sthair_buttn, 7,3,1,1)
        #   # self.strockethair_buttn=QPushButton("static face hair")
        #   # self.strockethair_buttn.setStyleSheet("color: #b1b1b1; background-color: rgba(255,200,150,100);")
        #   # self.connect(self.strockethair_buttn, SIGNAL('clicked()'), self._rocketfacehairstatic)
        #   # self.frame_btn_layout.addWidget(self.strockethair_buttn, 6,2,1,1)
 
        #   self.hair_colsuit_buttn=QPushButton("collide hair2suit")
        #   self.hair_colsuit_buttn.setStyleSheet("color: #b1b1b1; background-color: rgba(255,200,150,100);")
        #   self.connect(self.hair_colsuit_buttn, SIGNAL('clicked()'), self._setup_collide_fur)
        #   self.frame_btn_layout.addWidget(self.hair_colsuit_buttn, 6,1,1,1)
        #   self.pubVersions_button=QPushButton("print anim version yaml")
        #   self.pubVersions_button.setStyleSheet("color: #b1b1b1; background-color: rgba(255,200,150,100);")
        #   self.connect(self.pubVersions_button, SIGNAL('clicked()'), self._print_pub_message)
        #   self.frame_btn_layout.addWidget(self.pubVersions_button, 6,3,1,1)
        #   self.wrinkle_button=QPushButton("Jesus wrinkle script")
        #   self.connect(self.wrinkle_button, SIGNAL('clicked()'), self._addWrinkle)
        #   self.wrinkle_button.setStyleSheet("color: #b1b1b1; background-color: rgba(255,200   ,150,100);")
        #   self.frame_btn_layout.addWidget(self.wrinkle_button, 7,1,1,1)
        #   self.w_colr_button=QPushButton("wire colour")
        #   self.connect(self.w_colr_button, SIGNAL('clicked()'), self._hair_wires)
        #   self.w_colr_button.setStyleSheet("color: #b1b1b1; background-color: rgba(255,200,150,100);")
        #   self.frame_btn_layout.addWidget(self.w_colr_button, 7,2,1,1)           
        # # if "vfx_cr" in PROJECT:
        #   self.cape_shoulder_buttn=QPushButton("fix hela cape shoulders")
        #   self.cape_shoulder_buttn.setStyleSheet("color: #b1b1b1; background-color: rgba(255,200,150,100);")
        #   self.connect(self.cape_shoulder_buttn, SIGNAL('clicked()'), self._fix_hela_cape)
        #   self.frame_btn_layout.addWidget(self.cape_shoulder_buttn, 5,2,1,1)
        #   self.drag_whisk_buttn=QPushButton("fix whiskers")
        #   self.drag_whisk_buttn.setStyleSheet("color: #b1b1b1; background-color: rgba(255,200,150,100);")
        #   self.connect(self.drag_whisk_buttn, SIGNAL('clicked()'), self._fix_whiskers)
        #   self.frame_btn_layout.addWidget(self.drag_whisk_buttn, 6,0,1,1)
        #   self.importneck_buttn=QPushButton("import neck")
        #   self.connect(self.importneck_buttn, SIGNAL('clicked()'), self._neck_import)
        #   self.importneck_buttn.setStyleSheet("color: #b1b1b1; background-color: rgba(255,200,150,100);")
        #   self.frame_btn_layout.addWidget(self.importneck_buttn, 6,1,1,1)
        #   self.eguard_buttn=QPushButton("fix_eguard_clth")
        #   self.connect(self.eguard_buttn, SIGNAL('clicked()'), self.eguard_clth)
        #   self.eguard_buttn.setStyleSheet("color: #b1b1b1; background-color: rgba(255,200,150,100);")
        #   self.frame_btn_layout.addWidget(self.eguard_buttn, 6,2,1,1)
 
        # self.w_colr_button=QPushButton("preroll")
        # self.connect(self.w_colr_button, SIGNAL('clicked()'), self._preroll)
        # self.frame_btn_layout.addWidget(self.w_colr_button, 2,3,1,1)     
 
        self.pathway_names=QComboBox()
        self.pathway_names.addItems(pathways.keys())
        self.frame_btn_layout.addWidget(self.pathway_names)
        QtCore.QObject.connect(self.pathway_names, SIGNAL("currentIndexChanged(QString)"),self._open_path_drop)
 
        self.blend_types=QComboBox()
        self.blend_types.addItems(blendoptions)
        self.frame_btn_layout.addWidget(self.blend_types)
        QtCore.QObject.connect(self.blend_types, SIGNAL("currentIndexChanged(QString)"),self._blend_options)
 
        # self.start_window()
 
    def cloth_TS_UI(self):
        ext_win = clothCheck_UI()
        ext_win.show()
 
    def extractAction(self):
        ext_win = Expression_Examples()
        ext_win.show()
 
    def _fix_frames(self):
        # getToolbase=mTools.mToolKit()
        # getToolbase.remove_preroll_and_postroll_for_mSubmit()
        getFile= cmds.file(q=1, sn=1).split('/')[-1]
        getFilename=getFile.split('.mb')[0]
        getDepts = os.listdir(rvFolder)
        for each in getDepts:
            if getFilename ==each:
                getFolderFiles=rvFolder+'/'+each
                moreFile=projectFolder+'/'+getFilename+'tmp'
                if not os.path.exists(moreFile):
                    os.makedirs(moreFile)              
                # getList = os.listdir(getFolderFiles)
                getpreset=[os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(getFolderFiles) for name in files if name.lower().endswith(".jpg")]
                for item in getpreset:
                    getpart=item.split(".")[-2]
                    try:
                        if int(getpart) < wk_strt_value:
                            getit=item.split("/")[-1]
                            shutil.move(item, moreFile+'/'+getit)
                    except:
                        pass
                    try:
                        if int(getpart) > wk_out_value:
                            shutil.move(item, moreFile+'/'+getit)
                    except:
                        pass
 
    def getSetup(self, PROJECT, SCENE, SHOT):
        new_sgVarFilePath = '/jobs/%s/%s/%s/TECH/lib/shotgun/setshot.d/sgvars' % (PROJECT, SCENE, SHOT)
        projectFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT
        animFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/instances/'
        abcFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/cache/alembic/'
        pbFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/movies/'
        rvFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/'+DEPT
        getDeptRVFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/'    
        return new_sgVarFilePath, projectFolder, animFolder, abcFolder, pbFolder, rvFolder, getDeptRVFolder
 
 
 
    def BlendGrps_butt(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.blendSearchGroups()
 
 
 
    def init_from_range_butt(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.initialize_strt_based_on_wkrange()
 
 
 
    def init_from_nuc_butt(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.initialize_strt_based_on_nucleus()
 
 
    def nuc_to_first(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.initialize_strt_based_on_first()
 
 
 
    def _grab_nucleus(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.grab_nucleus()
 
 
 
    def _grab_msh_heir(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.select_mesh_heirarchy()
 
 
 
    def _grab_transfer(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.map_select_transfer()
 
    def _dyn_names(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.dynnames()
 
    def _rgdnames(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.rgdnames()
 
 
    def _grab_bs(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.grab_blend()
 
    def _grab_hrprop(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.grab_hrproperty()
 
    def _grab_hrsim(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.grab_hairfxshape()
 
    def _fix_hairfx_scene(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.fix_hairfx_xgen_methpipe_scene()
 
    def _reinit_hair(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.reinit_hairfx()
 
    def _bsptools(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.bsptools()
 
    def _techgrp(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.buildTemp_techanim()
 
    def cleanModels(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.cleanModels()
 
    def _grab_mesh(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.selectNclothMesh()
 
    def _fixcam_attr(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.fixcam_attr()
 
    def _grab_ncloth(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.selectNclothcloth()
 
    def _grab_nhair(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.selectNhair()
 
    def _grab_nconstraints(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.selectNconstraint()
 
    def _grab_cache(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.selectNclothCache()
 
    def _fix_RB(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.fix_rainbow()
 
 
    def _select_array(self):
        import selectArray
        reload (selectArray)
        selectArray.SelectionPalettUI()
 
 
    def _lit_cam(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.grabCameraLights()
 
    def _neck_import(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.importneck()
 
    def eguard_clth(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.eguard_skirt()
 
    def save_import_attrs(self):
        import loadAttrs
        reload (loadAttrs)
        get_attrTools=loadAttrs.attributeSwapper()
        get_attrTools.saveAttributesWindow()
 
    def corrective_shape(self):
        import cor_bs
        reload (cor_bs)
        cor_bs.corrective_bs()
 
    def _opening_folder(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.opening_folder(spaceWork)
 
    def apply_colors(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools._apply_colors()
 
    def _change_primary_grn(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.create_rgb_window()
 
    def apply_grey_colors(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools._apply_grey_colors()
 
    def _get_geo_techanim(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.get_geo_techanim()
 
    def change_colors(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools._change_colors()
 
    def change_grey(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools._change_grey()
 
    def change_ambient(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools._change_ambient()
 
 
    def _match_xform(self):
        import baseMockFunctions_maya
        reload (baseMockFunctions_maya)
        get_baseTools=baseMockFunctions_maya.BaseClass()
        get_baseTools.xformmove()
 
 
    def _load_web_hair(self):
        gethairweb=mockTools.mToolKit()
        gethairweb._load_web_hair()
 
 
    def _copy_attr(self):
        import baseMockFunctions_maya
        reload (baseMockFunctions_maya)
        get_baseTools=baseMockFunctions_maya.BaseClass()
        get_baseTools._transfer_anim_attr()
 
    def _edge_to_edge(self):
        getCurveWrap=mockTools.mToolKit()
        getCurveWrap.matchCurveShapes()
 
    def _shape_to_shape(self):
        getCurveWrap=mockTools.mToolKit()
        getCurveWrap.matchFullShape()
 
    def _connect_to_curve(self):
        getCurveWrap=mockTools.mToolKit()
        getCurveWrap.matchFullShape()
 
    def _hu_okja(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.hookupOkja()
 
    def _nuc_root(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.nuc_pconstrnt_hip()
 
    def _nuc_rvt(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.locktorivet()
 
    def _nuc_neck(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.nuc_pconstrnt_neck()
 
    def _check_clth(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.troubleshoot_clth()
 
    def _break_con(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.break_connections()
 
    def _cache_window(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.cache_find_window()
 
    def _annots(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.annotations_list()
 
    def _autoAnnot(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.dealers_choice()
 
    def change_anot_colors(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools._change_anot_colors()
 
    def _tbl_clth(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.set_troubleshoot()
 
    def _print_saved_asset_info(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.print_asset_info()
 
    def _open_saved_asset_info(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.open_asset_info()
 
    def _save_asset_info_cfx(self):
        # get_baseTools=mockTools.mToolKit()
        # get_baseTools.save_asset_info()
        import asset_info2
        reload (asset_info2)
        asset_info2.set_pubAssets_win()
        # asset_info._shot_asset_identification_Win()
 
    def _save_asset_info_anim(self):
        # get_baseTools=mockTools.mToolKit()
        # get_baseTools.save_asset_info()
        import asset_info_anim
        reload (asset_info_anim)
        asset_info_anim.set_anim_pubAssets_win()
        # asset_info._shot_asset_identification_Win()
 
    def _print_asset(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.print_asset()
 
    def _pointGlue_mass_to_one(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.pointGlue_mass_to_one()
 
    def _pointGlue_one_to_mass(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.pointGlue_one_to_mass()
 
    def _cape_callup(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.cape_callup()
 
    def _print_pub_message(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.print_anim_message()
 
    def _open_path_drop(self):
        print str(pathways.keys()[0])
        pathlist_load=self.pathway_names
        playlist_name=pathlist_load.currentText()
        get_baseTools=mockTools.mToolKit()
        if playlist_name==pathways.keys()[0]:
            pass       
        if playlist_name==pathways.keys()[1]:
            get_baseTools.opening_folder(pathways.get("work")) 
        if playlist_name==pathways.keys()[2]:
            get_baseTools.opening_folder(pathways.get("project"))  
        if playlist_name==pathways.keys()[3]:
            get_baseTools.opening_folder(pathways.get("products")) 
        if playlist_name==pathways.keys()[4]:
            get_baseTools.opening_folder(pathways.get("alembic"))  
        if playlist_name==pathways.keys()[5]:
            get_baseTools.opening_folder(pathways.get("blasts"))   
 
    def _blend_options(self):
        blend_load=self.blend_types
        blend_name=blend_load.currentText()
        get_baseTools=mockTools.mToolKit()
        if blend_name==blendoptions[0]:
            pass       
        if blend_name==blendoptions[1]:
            get_baseTools.blendGroupToGroup()  
        if blend_name==blendoptions[2]:
            get_baseTools.blendMass()  
        if blend_name==blendoptions[3]:
            get_baseTools.blendSearch()
        if blend_name==blendoptions[4]:
            get_baseTools.connSearch() 
        if blend_name==blendoptions[5]:
            get_baseTools.blendSearchGroups_alias()
        if blend_name==blendoptions[6]:
            get_baseTools.blendSearchGroups_alias_morph()  
 
    def _abc_xgen(self, arg=None): 
        import abc_cache_versioning
        reload (abc_cache_versioning)
        # getFetchClass=bake_abc_curves.fetchAttrs()
        # getFetchClass._findAttr_window()
 
    def _fetchAttr_win(self, arg=None): 
        import fetchAttrs_win
        reload (fetchAttrs_win)
        getFetchClass=fetchAttrs_win.fetchAttrs()
        # getFetchClass._findAttr_window()
 
    def _renamer(self):
        import renamer
        reload (renamer)
        renamer.myUI()   
                 
    def _offset_cache(self):
        import baseMockFunctions_maya
        reload (baseMockFunctions_maya)
        get_baseTools=baseMockFunctions_maya.BaseClass()
        get_baseTools.offset_cache()
                 
    def _offset_rotate_cache(self):
        import baseMockFunctions_maya
        reload (baseMockFunctions_maya)
        get_baseTools=baseMockFunctions_maya.BaseClass()
        get_baseTools.rotate_to_point()
                 
    def _cache_play(self):
        import cache_stuff
        reload (cache_stuff)
 
    # creature report only
    def _fix_whiskers(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.drag_whisker_fix()
    def _fix_hela_cape(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.cape_to_pauldrons()
 
    def _fix_hela_collide(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.collision_fix()
 
    def _setup_collide_fur(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.setup_collide_fur()
 
    def _addWrinkle(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.Jesus_wrinkle_script()
 
    def _hair_wires(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.hair_wires()
 
    def _fixfur(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.rocket_fix()
 
    def _statichair(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.static_curves()
 
    def _rocketfacehairstatic(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.rockets_face_fur_auto()
 
    def _rocket_fur_preview(self):
        import previews
        reload(previews)
        get_baseTools=previews.preview_ports()
        # get_baseTools.setup_preview_fur()
 
    def _scissor_win(self):
        import scissor_win
        reload (scissor_win)
        scissor_win.scissor_UI()       
    def _preroll(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.preroll()
 
    def _precision_set(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.precision_setup()
 
 
    def _mm_item(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.motion_mult_item()
 
 
    def _wirewrap(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.wirewrap()
 
    def _postTech_crv_shapes(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.post_shape_crv()
 
    def _clear_cache(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.clearCache()
 
    def _check_grmtools(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.check_groomVer()
 
    def _blur_frames(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.blur_bookends()
 
    def _fix_methpipe(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.fix_methpipe()
 
    def _fix_cam(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.fix_cam()
 
    def _wit_cam(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.wit_cam()
 
    def _fix_undo(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.turn_on_undo()
 
    def _opt_maya(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.optimize()
 
    def _shrinkwrap_meshcut(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.shrinkWrap_meshcut()
 
    def select_half(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.select_half()
         
    def _clean_mesh_curves(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.cln_curves()
 
    def _kelpie_prost(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.kelpdragon_prosthetics()
 
    def _build_curve(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.build_a_curve()
 
 
    def _wire_wrap(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.fastwire()
 
    def _cloth_strips(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.build_a_cloth_short_callup()
 
    def _perc_preview(self):
        get_baseTools=mockTools.mToolKit()
        get_baseTools.percentage_preview()
 
 
    def _anim_export(self):
        from maya_animexport import ui
        ui.launch()
 
    # def _mm_techrig(self):
    #   get_baseTools=mockTools.mToolKit()
    #   get_baseTools.motion_mult_techRig()
 
# app=QtGui.QApplication(sys.argv)
inst_mckwin=typicalWindow()
inst_mckwin.show()
# sys.exit(app.exec_())
