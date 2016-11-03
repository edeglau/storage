__author__="Elise Deglau"

# from mshotgun import mShotgun
import PyQt4
from PyQt4 import QtCore, QtGui, Qt
from PyQt4.QtGui import QWidget, QRadioButton, QGridLayout, QLabel, \
	QTableWidget, QComboBox, QKeySequence, QToolButton, QPlainTextEdit, QPushButton,QBoxLayout, \
	QClipboard, QTableWidgetItem, QCheckBox, QVBoxLayout, QHBoxLayout, \
	QPixmap, QLineEdit, QListWidget, QTextEdit, QSizePolicy, QFrame, QPalette, QColor, \
	QFont, QAbstractItemView, QMenu, QMessageBox
from PyQt4.QtCore import SIGNAL

import os, sys, operator, re, glob, getpass, subprocess, shutil, string, random, ast, webbrowser, time, datetime
from subprocess import Popen, PIPE
from os import stat, listdir, walk
from pwd import getpwuid
import os.path
from os.path import isfile, join
from datetime import datetime
buttonGrp=[]

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


projects='/jobs/'+PROJECT
prjFileName = os.listdir(projects)
prjFileName=sorted(prjFileName)
getUser=getpass.getuser()

audioVer="v0001"

audioName='/pcm_s16le_aif/'+SHOT+'_cut_main_v0001-pcm_s16le'

audioFormat=".aif"

audioFile='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/REFERENCE/editorial/cut/main/'+audioVer+'/'+audioName+audioFormat

formatEXT=".jpg"


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
	winTitle="mTools "+PROJECT+" : "+SHOT+" : (F"+str(shot_len_value)+") FRANGE:"+str(cut_in_value)+" - "+str(cut_out_value)
except:
	winTitle="mTools "+PROJECT+" : "+SHOT
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
		
		#mainlayout
		self.vertical_order_layout=QtGui.QBoxLayout(2)
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
		
		self.park_btn_pkt=QtGui.QBoxLayout(2)
		self.park_btn_pkt.setAlignment(QtCore.Qt.AlignTop)
		self.park_btn_pkt.setContentsMargins(5,2,5,8)
		self.wndw_layer_pkt.addLayout(self.park_btn_pkt, 0,0,1,1)
		self.park_frame=QtGui.QFrame()
		self.park_frame.setStyleSheet("background-color: #434343; border-style: solid; border-width: 2px; border-color:#434343;border-radius:8px;")
		
		self.blend_button=QPushButton("BlendGrps")
		self.blend_button.setToolTip("Select driving group, select driver group. press this button")
		self.connect(self.blend_button, SIGNAL('clicked()'), self.BlendGrps_butt)
		self.window_layer_01.addWidget(self.blend_button, 0,0,1,1)

		self.init_range_button=QPushButton("Initialize")
		self.init_range_button.setToolTip("reset to current shot")
		self.connect(self.init_range_button, SIGNAL('clicked()'), self.init_from_range_butt)
		self.window_layer_01.addWidget(self.init_range_button, 0,1,1,1)

		
		self.init_nuc_button=QPushButton("Init_to_nuc")
		self.init_nuc_button.setToolTip("reset to current shot")
		self.connect(self.init_nuc_button, SIGNAL('clicked()'), self.init_from_nuc_butt)
		self.window_layer_01.addWidget(self.init_nuc_button, 0,5,1,1)


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




		self.msgBox=QGridLayout()

		self.status_lbl=QLabel("Comment: ")
		self.status_lbl.setStyleSheet('background-color:transparent')
		self.status_lbl.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
		self.msgBox.addWidget(self.status_lbl, 0,0,1,1)

		self.fieldBox=QLineEdit()
		self.fieldBox.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
		self.fieldBox.setVisible(1)
		self.fieldBox.setText(defaultText)
		self.fieldBox.setFixedWidth(600)
		self.msgBox.addWidget(self.fieldBox, 0,1,1,1)


		self.radiobox=QGridLayout()
		self.frame_title_layout.addLayout(self.radiobox, 1,0,1,1)

		self.sel_nuc_button=QPushButton("grab nucleus")
		self.sel_nuc_button.setToolTip("reset to current shot")
		self.sel_nuc_button.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
		self.connect(self.sel_nuc_button, SIGNAL('clicked()'), self._grab_nucleus)
		self.radiobox.addWidget(self.sel_nuc_button, 0,0,1,1)
		# self.window_layer_01.addWidget(self.sel_nuc_button, 0,5,1,1)
		
		self.head_lbl=QLabel("start")
		self.head_lbl.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,0);")
		self.radiobox.addWidget(self.head_lbl, 1, 0,1,1)
		
		self.head_field=QTextEdit("")
		self.head_field.setFixedHeight(35)
		self.head_field.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,0);")
		self.radiobox.addWidget(self.head_field, 1, 1,1,1)
		
		self.toe_lbl=QLabel("end")
		self.toe_lbl.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,0);")
		self.radiobox.addWidget(self.toe_lbl, 1, 2,1,1)
		
		self.toe_field=QTextEdit("")
		self.toe_field.setFixedHeight(35)
		self.toe_field.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,0);")
		self.radiobox.addWidget(self.toe_field, 1, 3,1,1)
		
		
		self.play_in_rv_button=QPushButton("play in RV")
		# self.connect(self.play_in_rv_button, SIGNAL('clicked()'), self.play_in_rv)
		self.frame_btn_layout.addWidget(self.play_in_rv_button, 0,0,0,1)
		
		self.look_btn=QPushButton("compare")
		# self.connect(self.look_btn, SIGNAL('clicked()'), self.compare_in_rv)
		self.frame_btn_layout.addWidget(self.look_btn, 0,1, 0,1)


		# self.link_btn=QPushButton("link")
		# self.connect(self.link_btn, SIGNAL('clicked()'), self.play_in_rv)
		# self.frame_btn_layout.addWidget(self.link_btn, 0,2,1,1)
		
		self.create_btn=QPushButton("Submit To Shotgun")
		# self.connect(self.create_btn, SIGNAL('clicked()'), self.pub_to_shotgun)
		# self.connect(self.create_btn, SIGNAL('clicked()'), self.pub_to_shotgun)
		self.frame_btn_layout.addWidget(self.create_btn, 0,3, 1,1)
		
		self.pocketTitle=QPushButton("title")
		self.pocketTitle.setObjectName('label')
		#self.pocketTitle.setStyleSheet("QPushButton#label{font-weight:500; color: rgb"str(buttonColorDict).get("yello"))+"; button-color: rgba(255,255,255,0); font-size: 10pt; border-width: 0px; font-style: bold;}")
		# self.connect(self.pocketTitle, SIGNAL('clicked()'), self.send)
		self.connect(self.pocketTitle, SIGNAL('customContextMenuRequested(QPoint)'), lambda: self.send())
		self.park_btn_pkt.addWidget(self.pocketTitle)

		self.a_btn=QPushButton("a_btn")
		#self.a_btn.setStyleSheet("background-color: rgb"str(buttonColorDict).get("yello")))
		# self.connect(self.a_btn, SIGNAL('clicked()'), self.play_in_rv)
		self.park_btn_pkt.addWidget(self.a_btn)
		
		self.card_menu=QMenu("card")
		self.card_menuBar=self.menuBar()
		self.card_menuBar.addMenu(self.card_menu)
		self.park_btn_pkt.addWidget(self.card_menuBar)
		buttonGrp.append(self.card_menuBar)
		
		self.card_btn=QToolButton()
		self.card_btn.setPopupMode(QToolButton.MenuButtonPopup)
		self.card_btn.setMenu(self.card_menu)
		self.card_special_btn=QPushButton("card special")
		# self.connect(self.card_special_btn, SIGNAL('clicked()'), self.card_special_callup)
		action=QtGui.QWidgetAction(self.card_btn)
		action.setDefaultWidget(self.card_special_btn)
		self.card_btn.menu().addAction(action)

		self.B_card_btn=QToolButton()
		self.B_card_btn.setPopupMode(QToolButton.MenuButtonPopup)
		self.B_card_btn.setMenu(self.card_menu)
		self.B_card_special_btn=QPushButton("card special")
		# self.connect(self.B_card_special_btn, SIGNAL('clicked()'),self.B_card_special_callup)
		action=QtGui.QWidgetAction(self.B_card_btn)
		action.setDefaultWidget(self.B_card_special_btn)
		self.B_card_btn.menu().addAction(action)

		# self.start_window()




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



	def _grab_nucleus(self):
		get_baseTools=mockTools.mToolKit() 
		get_baseTools.grab_nucleus()




# app=QtGui.QApplication(sys.argv)
inst=typicalWindow()
inst.show()
# sys.exit(app.exec_())
