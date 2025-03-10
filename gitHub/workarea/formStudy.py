
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
# import datetime
import os, sys, operator, re, glob, getpass, subprocess, shutil, string, random, ast, webbrowser, time, datetime
from subprocess import Popen, PIPE
from os import stat, listdir, walk
from pwd import getpwuid
import os.path
from os.path import isfile, join
import datetime
from datetime import datetime
buttonGrp=[]

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
get_a_play_list=["createlist", "build", "append"]
alist2=['playlist']
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

project_path_pbMovs='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+"/TASKS/"+DEPT+"/maya/movies"
user_path_pbmovs='/home/'+getUser

formatEXT=".jpg"
playlistpath='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+"/maya/"

sgVarFilePath = '/jobs/%s/%s/%s/TECH/lib/shotgun/setshot.d/sgvars' % (PROJECT, SCENE, SHOT)

by_detail=["folder", "file"]


class dropMenu(QtGui.QWidget):
	def __init__(self, detailMessge, title, makeNewContent):
		super(dropMenu, self).__init__()
		self.initUI(detailMessge, title, makeNewContent)

	def initUI(self, detailMessge, title, makeNewContent):
		self.setWindowTitle(title)
		
		self.layout = QVBoxLayout()
		self.btnlayout=QBoxLayout(1)
		
		self.playlist_names=QComboBox()
		self.playlist_names.addItems(detailMessge)
		self.layout.addWidget(self.playlist_names)

		self.layout.addLayout(self.btnlayout)


		self.sel_button=QPushButton("append")
		self.connect(self.sel_button, SIGNAL("clicked()"),
					lambda: self.gotoAppend(makeNewContent))
		self.btnlayout.addWidget(self.sel_button)
		self.setLayout(self.layout)

	def gotoAppend(self, makeNewContent):
		getplayList=self.playlist_names
		getplayList=getplayList.currentText()
		goToMain=typicalWindow()
		goToMain.appender(getplayList, makeNewContent)

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
class typicalWindow(QtGui.QMainWindow):
	def __init__(self, parent=None):
		super(typicalWindow, self).__init__(parent)
		new_sgVarFilePath, projectFolder, animFolder, abcFolder, pbFolder, rvFolder, getDeptRVFolder, get_mm_ver, get_track_ver, get_roto_ver, get_an_ver,get_ta_ver, get_fx_ver, get_light_ver, get_comp_ver, get_mm_date, get_track_date, get_roto_date, get_an_date,get_ta_date, get_fx_date, get_light_date, get_comp_date, get_an_pub_date, get_ta_pub_date, get_an_pub_ver, get_ta_pub_ver=self.getSetup(PROJECT, SCENE, SHOT)
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
		self.midLayout.addLayout(self.window_layer_05,5,0,1,1)
		
		self.window_layer_06=QGridLayout()
		self.upper_layout.addLayout(self.window_layer_06, 6,0,1,1)


		self.window_layer_07=QGridLayout()
		self.upper_layout.addLayout(self.window_layer_07, 7,0,1,1)

	
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
		
		
		#widgets
		self.launch_shotgun_btn=QPushButton("launch shotgun")
		# self.launch_shotgun_btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		# self.launch_shotgun_btn.customContextMenuRequested.connect(self.onRightClick_techanim)
		self.launch_shotgun_btn.setStyleSheet("color: #b1b1b1; background-color: rgba(200,200,200,100);")
		# self.launch_shotgun_btn.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")		
		self.connect(self.launch_shotgun_btn, SIGNAL('clicked()'), self.launch_shotgun)
		# self.lowerButtSetupLayout.addWidget(self.launch_shotgun_btn,2,7,1,1)
		self.window_layer_01.addWidget(self.launch_shotgun_btn, 0,0,1,1)



		self.launch_shotgun_btn=QPushButton("open workfolder")
		self.connect(self.launch_shotgun_btn, SIGNAL('clicked()'), self._workFolder)
		self.window_layer_01.addWidget(self.launch_shotgun_btn, 0,1,1,1)
		


		# self.drop_lbl_01=QLabel()
		# self.drop_lbl_01.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
		# self.drop_lbl_01.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,0);")
		# self.window_layer_01.addWidget(self.drop_lbl_01, 0,1,1,1)
		
		self.drop_01=QComboBox()
		self.window_layer_01.addWidget(self.drop_01, 0,2,1,1)
		self.drop_01.addItems(prjFileName)
		self.drop_01.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.drop_01.customContextMenuRequested.connect(self.onRightClick)

		# self.drop_01.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		# self.connect(self.drop_lbl_01, SIGNAL("customContextMenuRequested(QPoint)"), self.onRightClick)
		
		# self.drop_lbl_02=QLabel()
		# self.drop_lbl_02.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
		# self.drop_lbl_02.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,0);")
		# self.window_layer_01.addWidget(self.drop_lbl_02, 0,2,1,1)
		
		self.drop_02=QComboBox()
		self.window_layer_01.addWidget(self.drop_02, 0,3,1,1)
		# QtCore.QObject.connect(self.drop_02, SIGNAL("currentIndexChanged(QString)"),
		# 						self.on_drop_01_changed)
		self.drop_02.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self.drop_02, SIGNAL("customContextMenuRequested(QPoint)"), self.onRightClick_shot)
		
		QtCore.QObject.connect(self.drop_01, SIGNAL("currentIndexChanged(QString)"),
								self.on_drop_01_changed)


		self.button_02=QPushButton("Reset")
		self.button_02.setToolTip("reset to current shot")
		self.connect(self.button_02, SIGNAL('clicked()'), self.reset_window)
		self.window_layer_01.addWidget(self.button_02, 0,5,1,1)



		self.drop_04=QComboBox()
		# QtCore.QObject.connect(self.drop_04, SIGNAL("currentIndexChanged(QString)"),
		# 						self.on_drop_01_changed)
		self.drop_04.addItems(getDepts)
		self.drop_04.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self.drop_04, SIGNAL("customContextMenuRequested(QPoint)"), self.onRightClick_dept)
		# QtCore.QObject.connect(self.drop_04, SIGNAL("currentIndexChanged(QString)"),
		# 						self.drop_04_changed)
		deptindex = self.drop_04.findText(DEPT, QtCore.Qt.MatchFixedString)
		self.drop_04.setCurrentIndex(deptindex)
		self.window_layer_04.addWidget(self.drop_04, 0,2,1,1)

		self.list_frame=QFrame()
		self.list_frame.setStyleSheet("color: rgb"+str(buttonColoursDict.get("red")))
		self.list_layout=QHBoxLayout()
		self.list_frame.setLayout(self.list_layout)
		



		self.type_list_drop=QComboBox()
		self.type_list_drop.addItems(typesOfReview)
		self.window_layer_04.addWidget(self.type_list_drop, 0,3,1,1)



		self.drop_list_builder_05=QComboBox()
		self.drop_list_builder_05.addItems(get_a_play_list)
		self.drop_list_builder_05.setStyleSheet("color: #b1b1b1; background-color: rgba(175,70,70,50);")
		QtCore.QObject.connect(self.drop_list_builder_05, SIGNAL("currentIndexChanged(QString)"),
								self.build)
		self.drop_list_builder_05.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self.drop_list_builder_05, SIGNAL("customContextMenuRequested(QPoint)"), self.onRightClick)
		self.list_layout.addWidget(self.drop_list_builder_05)
		self.window_layer_04.addWidget(self.drop_list_builder_05, 0,4,1,1)


		self.drop_list_06=QComboBox()
		self.drop_list_06.setStyleSheet("color: #b1b1b1; background-color: rgba(175,70,70,50);")
		preset=self.find_playlists(playlistpath)
		preset=[(each.split("/")[-1]) for each in preset]
		playListNames=[(each.split("_storedText.txt")[0]) for each in preset]
		QtCore.QObject.connect(self.drop_list_06, SIGNAL("currentIndexChanged(QString)"),self.load)
		self.drop_list_06.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self.drop_list_06, SIGNAL("customContextMenuRequested(QPoint)"), self.onRightClick_preset)
		# #if len(pres)<1:
			#self.drop_list_06.setEnabled(0)
		#else:
			#self.drop_list_06.setEnabled(1)
		self.drop_list_06.addItems(alist2)
		self.drop_list_06.addItems(playListNames)
		self.window_layer_04.addWidget(self.drop_list_06, 0,5,1,1)
		

		
		self.button_06=QPushButton("Refresh")
		self.button_06.setToolTip("refresh")
		self.connect(self.button_06, SIGNAL('clicked()'), self.refresh_window)	
		self.window_layer_04.addWidget(self.button_06, 0,6,0,1)

		self.listWidg = QTableWidget(1, 4)
		# self.listWidg.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		# self.listWidg.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
		# self.listWidg.cellPressed.connect(self.clicked)
		
		# self.listWidg=QTableWidget(0, 3)
		self.listWidg.setHorizontalHeaderLabels(headers)
		# tableWidget=self.listWidg
		self.listWidg.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)		
		col1, col2, col3, col4= 240, 160, 500, 50
		self.listWidg.setColumnWidth(0, col1)
		self.listWidg.setColumnWidth(1, col2)
		self.listWidg.setColumnWidth(2, col3)
		self.listWidg.setColumnWidth(3, col4)
		self.listWidg.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.listWidg.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.listWidg.customContextMenuRequested.connect(self.RightClick)
		self.listWidg.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
		# self.listWidg.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)		
		self.connect(self.listWidg, SIGNAL("itemClicked(QTableWidgetItem *)"), self.clicked)
		self.connect(self.listWidg, SIGNAL("itemDoubleClicked(QTableWidgetItem *)"), self.dclicked)
		self.window_layer_05.addWidget(self.listWidg, 0,0,1,1)


		self.customLayout=QtGui.QGridLayout()
		self.customLayout.setContentsMargins(5,10,5,10)
		self.customFrame=QtGui.QFrame()
		self.customFrame.setStyleSheet("background-color: #454545; border-style: solid; border-width: 2px; border-color:#565656;border-radius:8px;")
		self.customFrame.setFixedHeight(80)
		self.customFrame.setLayout(self.customLayout)
		# self.frame_layout.addLayout(self.frameSetupLayout, 0,0,1,1)
		self.window_layer_06.addWidget(self.customFrame, 0,0,1,1)



		self.custom_pathfile=QLabel("Custom path: ")
		self.custom_pathfile.setStyleSheet('background-color:transparent')
		self.custom_pathfile.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
		self.customLayout.addWidget(self.custom_pathfile, 0,0,1,1)


		self.custompath=QLineEdit()
		self.custompath.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
		self.custompath.setVisible(1)
		self.custompath.setText("//")
		self.custompath.setFixedWidth(600)
		self.customLayout.addWidget(self.custompath, 0,1,1,1)




		self.drop_list_det=QComboBox()
		self.drop_list_det.addItems(by_detail)
		self.drop_list_det.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.list_layout.addWidget(self.drop_list_det)
		self.customLayout.addWidget(self.list_frame, 0,2,1,1)

		self.button_05=QPushButton("Set to project default")
		self.button_05.setToolTip("set list to load from custom path")
		self.connect(self.button_05, SIGNAL('clicked()'), self.set_to_project)
		self.customLayout.addWidget(self.button_05, 2,0,1,1)

		self.button_05=QPushButton("Load from user folder")
		self.button_05.setToolTip("set list to load from custom path")
		self.connect(self.button_05, SIGNAL('clicked()'), self.set_to_user)
		self.customLayout.addWidget(self.button_05, 2,1,1,1)

		self.button_05=QPushButton("Set")
		self.button_05.setToolTip("set list to load from custom path")
		self.connect(self.button_05, SIGNAL('clicked()'), self.set_toCustom)
		self.customLayout.addWidget(self.button_05, 2,2,1,1)

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
		self.frame_title_layout.addLayout(self.msgBox, 0,0,1,1)

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
		self.connect(self.play_in_rv_button, SIGNAL('clicked()'), self.play_in_rv)
		self.frame_btn_layout.addWidget(self.play_in_rv_button, 0,0,0,1)
		
		self.look_btn=QPushButton("compare")
		self.connect(self.look_btn, SIGNAL('clicked()'), self.compare_in_rv)
		self.frame_btn_layout.addWidget(self.look_btn, 0,1, 0,1)



		self.create_btn=QPushButton("Submit To Shotgun")
		# self.connect(self.create_btn, SIGNAL('clicked()'), self.pub_to_shotgun)
		self.connect(self.create_btn, SIGNAL('clicked()'), self.pub_to_shotgun)
		self.frame_btn_layout.addWidget(self.create_btn, 0,3, 1,1)
		
		self.pocketTitle=QPushButton("title")
		self.pocketTitle.setObjectName('label')
		#self.pocketTitle.setStyleSheet("QPushButton#label{font-weight:500; color: rgb"str(buttonColorDict).get("yello"))+"; button-color: rgba(255,255,255,0); font-size: 10pt; border-width: 0px; font-style: bold;}")
		self.connect(self.pocketTitle, SIGNAL('clicked()'), self.send)
		self.connect(self.pocketTitle, SIGNAL('customContextMenuRequested(QPoint)'), lambda: self.send())
		self.park_btn_pkt.addWidget(self.pocketTitle)

		self.a_btn=QPushButton("a_btn")
		#self.a_btn.setStyleSheet("background-color: rgb"str(buttonColorDict).get("yello")))
		self.connect(self.a_btn, SIGNAL('clicked()'), self.play_in_rv)
		self.park_btn_pkt.addWidget(self.a_btn)

		self.lowerButtSetupLayout=QtGui.QGridLayout()
		self.lowerButtSetupLayout.setContentsMargins(5,10,5,10)
		self.lower_but_frame=QtGui.QFrame()
		# self.lower_but_frame.setStyleSheet("background-color: #434343; border-style: solid; border-width: 2px; border-color:#434343;border-radius:8px;")
		self.lower_but_frame.setFixedHeight(80)
		self.lower_but_frame.setLayout(self.lowerButtSetupLayout)
		# self.frame_layout.addLayout(self.frameSetupLayout, 0,0,1,1)
		self.lower_layout.addWidget(self.lower_but_frame, 1,0,1,1)

		# self.lower_layout.addWidget(self.lower_but_frame,1,0,1,1)

		self.play_anim_btn=QPushButton("anim "+get_an_ver)
		self.play_anim_btn.setToolTip(get_an_date)	
		# self.play_anim_btn.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,0);")
		self.play_anim_btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.play_anim_btn.customContextMenuRequested.connect(self.onRightClick_anim)
		self.connect(self.play_anim_btn, SIGNAL('clicked()'), self.play_latest_anim)
		self.lowerButtSetupLayout.addWidget(self.play_anim_btn,1,3,1,1)

		self.play_anim_pub_btn=QPushButton("pubanim "+get_an_pub_ver)
		self.play_anim_pub_btn.setToolTip(get_an_pub_date)		
		self.play_anim_pub_btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.play_anim_pub_btn.customContextMenuRequested.connect(self.onRightClick_anim)
		self.connect(self.play_anim_pub_btn, SIGNAL('clicked()'), self.play_latest_anim_pub)
		self.lowerButtSetupLayout.addWidget(self.play_anim_pub_btn,2,3,1,1)
		
		self.play_light_btn=QPushButton("light "+get_light_ver)
		self.play_light_btn.setToolTip(get_light_date)		
		self.play_light_btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.play_light_btn.customContextMenuRequested.connect(self.onRightClick_light)
		self.connect(self.play_light_btn, SIGNAL('clicked()'), self.play_latest_light)
		self.lowerButtSetupLayout.addWidget(self.play_light_btn,1,6,1,1)
		
		self.play_comp_btn=QPushButton("comp "+get_comp_ver)
		self.play_comp_btn.setToolTip(get_comp_date)			
		self.play_comp_btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.play_comp_btn.customContextMenuRequested.connect(self.onRightClick_comp)
		self.connect(self.play_comp_btn, SIGNAL('clicked()'), self.play_latest_comp)
		self.lowerButtSetupLayout.addWidget(self.play_comp_btn,1,7,1,1)
		
		self.play_track_btn=QPushButton("track "+get_track_ver)
		self.play_track_btn.setToolTip(get_track_date)			
		self.play_track_btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.play_track_btn.customContextMenuRequested.connect(self.onRightClick_tracking)
		self.connect(self.play_track_btn, SIGNAL('clicked()'), self.play_latest_tracking)
		self.lowerButtSetupLayout.addWidget(self.play_track_btn,1,0,1,1)
		
		self.play_fx_btn=QPushButton("fx "+get_fx_ver)
		self.play_fx_btn.setToolTip(get_fx_date)			
		self.play_fx_btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.play_fx_btn.customContextMenuRequested.connect(self.onRightClick_fx)
		self.connect(self.play_fx_btn, SIGNAL('clicked()'), self.play_latest_fx)
		self.lowerButtSetupLayout.addWidget(self.play_fx_btn,1,5,1,1)

		self.play_mm_btn=QPushButton("match "+get_mm_ver)
		self.play_mm_btn.setToolTip(get_mm_date)		
		self.play_mm_btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.play_mm_btn.customContextMenuRequested.connect(self.onRightClick_matchmove)
		self.connect(self.play_mm_btn, SIGNAL('clicked()'), self.play_latest_matchmove)
		self.lowerButtSetupLayout.addWidget(self.play_mm_btn,1,1,1,1)

		self.play_roto_btn=QPushButton("roto "+get_roto_ver)
		self.play_roto_btn.setToolTip(get_roto_date)		
		self.play_roto_btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.play_roto_btn.customContextMenuRequested.connect(self.onRightClick_roto)
		self.connect(self.play_roto_btn, SIGNAL('clicked()'), self.play_latest_roto)
		self.lowerButtSetupLayout.addWidget(self.play_roto_btn,1,2,1,1)
		
		self.play_ta_btn=QPushButton("techanim "+get_ta_ver)
		self.play_ta_btn.setToolTip(get_ta_date)				
		self.play_ta_btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.play_ta_btn.customContextMenuRequested.connect(self.onRightClick_techanim)
		self.connect(self.play_ta_btn, SIGNAL('clicked()'), self.play_latest_techanim)
		self.lowerButtSetupLayout.addWidget(self.play_ta_btn,1,4,1,1)

		self.play_ta_pub_btn=QPushButton("pubtechanim "+get_ta_pub_ver)
		self.play_ta_pub_btn.setToolTip(get_ta_pub_date)				
		self.play_ta_pub_btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.play_ta_pub_btn.customContextMenuRequested.connect(self.onRightClick_techanim)
		self.connect(self.play_ta_pub_btn, SIGNAL('clicked()'), self.play_latest_techanim_pub)
		self.lowerButtSetupLayout.addWidget(self.play_ta_pub_btn,2,4,1,1)





		self.start_window()




	def launch_shotgun(self):
		url="http://sg.methodstudios.com"
		subprocess.Popen('firefox "%s"' % url, stdout=subprocess.PIPE, shell=True) 
            

	def start_window(self):
		# self.connectButton01
		index = self.drop_01.findText(SCENE, QtCore.Qt.MatchFixedString)
		self.drop_01.setCurrentIndex(index)
		self.get_scene()
		index2 = self.drop_02.findText(SHOT, QtCore.Qt.MatchFixedString)
		self.drop_02.setCurrentIndex(index2)
		index6 = self.type_list_drop.findText(setDefaultType[0], QtCore.Qt.MatchFixedString)
		self.type_list_drop.setCurrentIndex(index6)
		try:
			self.head_field.setText(str(float(cut_in_value)))
			self.toe_field.setText(str(float(cut_out_value)))
		except:
			self.head_field.setText("0")
			self.toe_field.setText("0")
		self.listCreate()

	def refresh_window(self):
		self.listCreate()
		self.refresh_playlist()



	def refresh_playlist(self):
		preset=self.find_playlists(playlistpath)
		preset=[(each.split("/")[-1]) for each in preset]
		playListNames=[(each.split("_storedText.txt")[0]) for each in preset]
		self.drop_list_06.clear()
		self.drop_list_06.addItems(alist2)
		self.drop_list_06.addItems(playListNames)		


	def reset_window(self):
		deptindex = self.drop_04.findText(DEPT, QtCore.Qt.MatchFixedString)
		self.drop_04.setCurrentIndex(deptindex)
		self.start_window()

	def buttonToggle(self):
		get_a_layout=self.park_btn_pkt
		get_size=get_a_layout.getContentsMargine()
		if get_size==(0,0,0,0):
			self.setvisible()
		else:
			self.setinvisible()
			
	def setinvisible(self):
		for each in buttonGrp:
			each.setVisible(0)
		self.park_btn_pkt.setContentsMargine(0,0,0,0)
		
	def setvisible(self):
		for each in buttonGrp:
			each.setVisible(1)
		self.park_btn_pkt.setContentsMargine(5,8,5,8)

	def deselected(self):
		print "hi"

	def get_scene(self):
		scene=self.drop_01
		scene=scene.currentText()		
		getPath='/jobs/'+PROJECT+'/'+scene
		get_items=os.listdir(getPath)
		get_items=sorted(get_items)
		# get_items=set(get_items)
		# get_items=sorted(get_items)
		self.get_shot(get_items)

	def get_shot(self, get_items):
		getDropScene=self.drop_02
		getDropScene.clear()
		getDropScene.addItems(get_items)		

	def onRightClick(self):
		scene=self.drop_01
		scene=scene.currentText()		
		path='/jobs/'+PROJECT+'/'+scene+"/"
		self.launch_folder(path)


	def onRightClick_shot(self):
		scene=self.drop_01
		scene=scene.currentText()		
		path='/jobs/'+PROJECT+'/'+scene+"/"+SHOT
		self.launch_folder(path)

	def onRightClick_dept(self):
		scene=self.drop_01
		scene=scene.currentText()		
		path='/jobs/'+PROJECT+'/'+scene+"/"+SHOT+'/PRODUCTS/images/'+DEPT
		self.launch_folder(path)


	def _workFolder(self):
		scene=self.drop_01
		scene=scene.currentText()		
		path='/jobs/'+PROJECT+'/'+scene+"/"+SHOT+'/TASKS/'+DEPT+"/maya/scenes/"
		self.launch_folder(path)


	def launch_folder(self, path):
		# command="xdg-open '%s'"%path
		command="dolphin '%s'"%path
		subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
		
	def on_drop_01_changed(self):
		self.get_scene()
		newcol1=self.listWidg.columnWidth(0)
		newcol2=self.listWidg.columnWidth(1)
		newcol3=self.listWidg.columnWidth(2)
		newcol4=self.listWidg.columnWidth(3)
		if newcol1==0:
			col1, col2, col3, col4= 240, 160, 500, 50
		else:
			col1, col2, col3, col4= newcol1, newcol2, newcol3, newcol4
		# findproject=self.drop_01
		self.listWidg.clear()
		# self.status_lbl.clear()
		# self.listCreate()
		# self.makeList(listpath, newUser, self.listWidg, model, stat_lab, listtype)
		# self.drop_03.addItems(get_items)
		# model, countdata, listArray	=self.get_listset_directory()	
		# if self.on_drop_01=="item1":
		# 	buildListPath=pathList.get("listpathtype").replace(getUser, newUser)
		# 	self.makeList(listpath, newUser, self.listWidg, model, stat_lab, listtype)
		# elif self.on_drop_01=="item2":
		# 	buildListPath=pathList.get("listpathtype2").replace(getUser, newUser)
		# 	self.makeList(listpath, newUser, self.listWidg, model, stat_lab, listtype)
			
	def clicked(self):
		selected_in_list=self.is_listWid_item_selected()
		getPath=selected_in_list[0]+'/'
		get_items=os.listdir(getPath)
		try:
			getFolderForJpgs=[(each) for each in get_items if "jpg" in each]
			getPlayFolder=selected_in_list[0]+'/'+getFolderForJpgs[0]+'/'
		except:
			getFolderForJpgs=[(each) for each in get_items if "mov" in each]
			getPlayFolder=selected_in_list[0]+'/'
		try:
			getList=os.listdir(getPlayFolder)
		except:
			getList=os.listdir(selected_in_list[0]+'/')
		getList=[(each) for each in getList if not each.startswith('.')]
		try:
			getImageName=getList[0].split('.')[0]
		except:
			pass
		try:
			getFrameLengthExist=[os.path.join(getPlayFolder, o) for o in os.listdir(getPlayFolder)]
		except:
			getFrameLengthExist=[os.path.join(selected_in_list[0], o) for o in os.listdir(selected_in_list[0])]
		getFrameLengthExist.sort(key=lambda x: os.path.getmtime(x))	
		try:
			getTrueFirst=int(getFrameLengthExist[0].split('.')[-2:-1][0])		
			getTrueLast=int(getFrameLengthExist[-3].split('.')[-2:-1][0])		
		except:
			getTrueFirst=int(0)		
			getTrueLast=int(0)
		try:
			self.head_field.setText(str(float(getTrueFirst)))
			self.toe_field.setText(str(float(getTrueLast)))
		except:
			self.head_field.setText("0")
			self.toe_field.setText("0")		

		
	def get_listset_directory(self):
		listArray=self.listWidg
		countdata=listArray.rowCount()
		model=listArray.model()
		return model, countdata, listArray
		
	def getListWidgetData(self):
		model, countdata, listArray	=self.get_listset_directory()	
		dataInListWidget=[]
		for row in range(model.rowCount()):
			dataInListWidget.append([])
			for column in range(model.columnCount()):
				index = model.index(row, column)
				dataInListWidget[row].append(str(model.data(index).toString()))
		return dataInListWidget, countdata


	def getSetup(self, PROJECT, SCENE, SHOT):
		new_sgVarFilePath = '/jobs/%s/%s/%s/TECH/lib/shotgun/setshot.d/sgvars' % (PROJECT, SCENE, SHOT)
		projectFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT
		animFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/instances/'
		abcFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/cache/alembic/'
		pbFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/movies/'
		rvFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/'+DEPT
		getDeptRVFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/'	
		getfoldertypes=["matchmove", "roto", "trackcomp", "anim", "techanim", "lightcomp", "comp", "fxflip"]
		#getmatchmovefolder
		playFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/matchmove'
		fileDict=self.rv_latest_mov(playFolder)
		if fileDict:
			get_play=fileDict[-1][0]
			getitem=get_play.split('/')[-2]
			get_mm_ver=getitem.split('_')[-1]
			get_mm_date=fileDict[-1][1]	
		else:
			get_mm_ver='no ver'
			get_mm_date='no date'
		#gettrackfolder
		playFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/trackcomp'
		fileDict=self.rv_latest_mov(playFolder)
		if fileDict:
			get_play=fileDict[-1][0]
			getitem=get_play.split('/')[-2]
			get_track_ver=getitem.split('_')[-1]
			get_track_date=fileDict[-1][1]	
		else:
			get_track_ver='no ver'
			get_track_date='no date'
		#getrotofolder	
		playFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/roto'
		fileDict=self.rv_latest_mov(playFolder)
		if fileDict:
			get_play=fileDict[-1][0]
			getitem=get_play.split('/')[-2]
			get_roto_ver=getitem.split('_')[-1]
			get_roto_date=fileDict[-1][1]
		else:
			get_roto_ver='no ver'
			get_roto_date='no date'	
		#getanimfolder
		playFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/anim'
		fileDict=self.rv_latest_mov_nopub(playFolder)
		if fileDict:
			get_play=fileDict[-1][0]
			getitem=get_play.split('/')[-2]
			get_an_ver=getitem.split('_')[-1]
			get_an_date=fileDict[-1][1]
		else:
			get_an_ver='no ver'
			get_an_date='no date'
		#getanimpubfolder
		playFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/anim'
		fileDict=self.rv_latest_mov_pubonly(playFolder)
		if fileDict:
			get_play=fileDict[-1][0]
			getitem=get_play.split('/')[-2]
			get_an_pub_ver=getitem.split('_')[-1]
			get_an_pub_date=fileDict[-1][1]
		else:
			get_an_pub_ver='no ver'
			get_an_pub_date='no date'	
		#gettechanimfolder
		playFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/techanim'
		fileDict=self.rv_latest_mov_nopub(playFolder)
		if fileDict:
			get_play=fileDict[-1][0]
			getitem=get_play.split('/')[-2]
			get_ta_ver=getitem.split('_')[-1]
			get_ta_date=fileDict[-1][1]
		else:
			get_ta_ver='no ver'
			get_ta_date='no date'	
		#gettechanimpubfolder
		playFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/techanim'
		fileDict=self.rv_latest_mov_pubonly(playFolder)
		if fileDict:
			get_play=fileDict[-1][0]
			getitem=get_play.split('/')[-2]
			get_ta_pub_ver=getitem.split('_')[-1]
			get_ta_pub_date=fileDict[-1][1]
		else:
			get_ta_pub_ver='no ver'
			get_ta_pub_date='no date'	
		#getfxfolder
		playFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/fxflip'
		fileDict=self.rv_latest_mov(playFolder)
		if fileDict:
			get_play=fileDict[-1][0]
			getitem=get_play.split('/')[-2]
			get_fx_ver=getitem.split('_')[-1]			
			get_fx_date=fileDict[-1][1]
		else:
			get_fx_ver='no ver'
			get_fx_date='no date'		
		#getlightcompfolder
		playFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/lightcomp'
		fileDict=self.rv_latest_mov(playFolder)
		if fileDict:
			get_play=fileDict[-1][0]
			getitem=get_play.split('/')[-2]
			get_light_ver=getitem.split('_')[-1]		
			get_light_date=fileDict[-1][1]
		else:
			get_light_ver='no ver'
			get_light_date='no date'	
		#getcompfolder
		playFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/comp'
		fileDict=self.rv_latest_mov(playFolder)
		if fileDict:
			get_play=fileDict[-1][0]
			getitem=get_play.split('/')[-2]
			get_comp_ver=getitem.split('_')[-1]		
			get_comp_date=fileDict[-1][1]
		else:
			get_comp_ver='no ver'
			get_comp_date='no date'	
		return new_sgVarFilePath, projectFolder, animFolder, abcFolder, pbFolder, rvFolder, getDeptRVFolder\
		 ,get_mm_ver, get_track_ver, get_roto_ver, get_an_ver,get_ta_ver, get_fx_ver, get_light_ver, get_comp_ver\
		 ,get_mm_date, get_track_date, get_roto_date, get_an_date,get_ta_date, get_fx_date, get_light_date, get_comp_date\
		 ,get_an_pub_date, get_ta_pub_date, get_an_pub_ver, get_ta_pub_ver



	def dclicked(self):
		selected_in_list=self.is_listWid_item_selected()
		self.relistCreate(selected_in_list[0])
		# self.set_folder_items(selected_in_list[0])
		# getPath=selected_in_list[0]+'/'
		# get_items=os.listdir(getPath)	
		# print get_items
		# print type(get_items[0])


	def relistCreate(self, directory):
		self.listWidg.setColumnCount(4)
		fileDict, count=self.set_folder_items(directory)		
		self.listWidg.setRowCount(count)
		self.listWidg.setHorizontalHeaderLabels(headers)
		sub='no'
		for row, item in enumerate(fileDict):
			key=item[0].split('/')[-1]
			path=item[0]
			value=item[1].split('>')[0]
			# sub=item[1].split('>')[1]
			self.listWidg.setItem(row, 0, QTableWidgetItem(key))
			self.listWidg.setItem(row, 1, QTableWidgetItem(value))
			self.listWidg.setItem(row, 2, QTableWidgetItem(path))
			self.listWidg.setItem(row, 3, QTableWidgetItem(sub))


	def set_folder_items(self, directory):
		try:
			getFiles=[os.path.join(directory, o) for o in os.listdir(directory) if os.path.isdir(os.path.join(directory, o))]
			pass
		except:
			# print "nothing found"
			return	
		getFiles.sort(key=lambda x: os.path.getmtime(x))
		# print getFiles[0].split(".")[-2:-1]
		fileDict=[]
		for each in getFiles:
			import datetime
			statbuf=os.stat(each)			
			# timeFormat=time.strftime('%m/%d/%Y', time.gmtime(os.path.getctime(each)))
			getAccTime=time.ctime(os.path.getmtime(each))
			timeFormat=datetime.datetime.fromtimestamp(statbuf.st_mtime).strftime('%c')
			timeFormat=timeFormat.split(" ")[:4]
			timeFormat=" ".join(timeFormat)
			if "  " in str(getAccTime):
				getAccTime=getAccTime.split("  ")
				getAccTime=getAccTime[1].split(" ")[1]
			else:
				getAccTime=getAccTime.split(" ")[3]
			# timeFormat=timeFormat+"  "+findSomeTime+'>'+sub
			timeFormat=timeFormat+"  "+getAccTime
			makeDict=(each, timeFormat)
			fileDict.append(makeDict)
		count=len(fileDict)
		fileDict=reversed(fileDict)
		return fileDict, count
		
	def grab_folder_items(self):
		getscene=self.drop_01.currentText()
		SCENE=str(getscene)
		getshot=self.drop_02.currentText()
		SHOT=str(getshot)
		new_sgVarFilePath, projectFolder, animFolder, abcFolder, pbFolder, rvFolder, getDeptRVFolder, get_mm_ver, get_track_ver, get_roto_ver, get_an_ver,get_ta_ver, get_fx_ver, get_light_ver, get_comp_ver, get_mm_date, get_track_date, get_roto_date, get_an_date,get_ta_date, get_fx_date, get_light_date, get_comp_date, get_an_pub_date, get_ta_pub_date, get_an_pub_ver, get_ta_pub_ver=self.getSetup(PROJECT, SCENE, SHOT)
		getDepts = os.listdir(getDeptRVFolder)		
		if os.path.isfile(new_sgVarFilePath):
		    franges = {'WORK_IN': None, 'CUT_IN': None,
		               'WORK_OUT': None, 'CUT_OUT': None}
		    for line in open(new_sgVarFilePath, 'r'):
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
		try:
			self.head_field.setText(str(float(cut_in_value)))
			self.toe_field.setText(str(float(cut_out_value)))
		except:
			self.head_field.setText("0")
			self.toe_field.setText("0")
		deptload=self.drop_04
		deptType=deptload.currentText()
		deptType=str(deptType)
		rvFolder=getDeptRVFolder+deptType
		directory=rvFolder
		try:
			getFiles=[os.path.join(directory, o) for o in os.listdir(directory) if os.path.isdir(os.path.join(directory, o))]
			pass
		except:
			# print "nothing found"
			return
		# getFile=[(each) for each in getFiles if getpwuid(stat(each).st_uid).pw_name==getUser]
		getFiles.sort(key=lambda x: os.path.getmtime(x))
		fileDict=[]
		for each in getFiles:
			getFolders=[(folderItem) for folderItem in os.listdir(each) if "mov" in folderItem]
			if getFolders:
				sub="yes"
			else:
				sub="no"
			statbuf=os.stat(each)
			import datetime
			# timeFormat=time.strftime('%m/%d/%Y', time.gmtime(os.path.getctime(each)))
			getAccTime=time.ctime(os.path.getmtime(each))
			timeFormat=datetime.datetime.fromtimestamp(statbuf.st_mtime).strftime('%c')
			timeFormat=timeFormat.split(" ")[:4]
			timeFormat=" ".join(timeFormat)
			if "  " in str(getAccTime):
				getAccTime=getAccTime.split("  ")
				getAccTime=getAccTime[1].split(" ")[1]
			else:
				getAccTime=getAccTime.split(" ")[3]
			# timeFormat=timeFormat+"  "+findSomeTime+'>'+sub
			timeFormat=timeFormat+"  "+getAccTime+'>'+sub
			makeDict=(each, timeFormat)
			fileDict.append(makeDict)
		count=len(fileDict)
		fileDict=reversed(fileDict)
		dictItems=fileDict
		return fileDict, count


	def listCreate(self):
		self.listWidg.setColumnCount(4)
		fileDict, count=self.grab_folder_items()		
		self.listWidg.setRowCount(count)
		self.listWidg.setHorizontalHeaderLabels(headers)
		for row, item in enumerate(fileDict):
			key=item[0].split('/')[-1]
			path=item[0]
			value=item[1].split('>')[0]
			sub=item[1].split('>')[1]
			self.listWidg.setItem(row, 0, QTableWidgetItem(key))
			self.listWidg.setItem(row, 1, QTableWidgetItem(value))
			self.listWidg.setItem(row, 2, QTableWidgetItem(path))
			self.listWidg.setItem(row, 3, QTableWidgetItem(sub))



	def is_listWid_item_selected(self):
		listW=self.listWidg
		(dataInListWidget, countdata)=self.getListWidgetData()
		get_string_id=[]
		for index in xrange(countdata):
			get=listW.item(index, 0).isSelected()
			if get==True:
				getObj=listW.item(index, 2).text()
				getObj=str(getObj)
				get_string_id.append(getObj)
			else:
				get=listW.item(index, 1).isSelected()
				if get==True:
					getObj=listW.item(index, 2).text()
					getObj=str(getObj)
					get_string_id.append(getObj)
				else:
					get=listW.item(index, 2).isSelected()
					if get==True:
						getObj=listW.item(index, 2).text()
						getObj=str(getObj)
						get_string_id.append(getObj)
					else:
						get=listW.item(index, 3).isSelected()
						if get==True:
							getObj=listW.item(index, 3).text()
							getObj=str(getObj)
							get_string_id.append(getObj)						
		return get_string_id
		
	def build(self):
		selected_in_list=self.is_listWid_item_selected()
		list_build=self.drop_list_builder_05
		list_build_function=list_build.currentText()
		if list_build_function==get_a_play_list[0]:
			return
		elif list_build_function==get_a_play_list[1]:
			if len(selected_in_list)<1:
				print "need to select something"
				return
			else:
				pass			
			allthePaths=[playlistpath]
			compareBucket=[]
			getitems=[(each.split("/")[-1]) for each in selected_in_list]
			name_to_save=' '.join(getitems)
			prompt="name of list:"
			getComment=self.makeBody(prompt)
			print getComment
			if getComment==None:
				print "needs name"
				return
			else:
				pass
			getComment=getComment.replace(' ', '_')
			shotList=getComment+"_storedText.txt"
			fileBuild=playlistpath+shotList
			copyfilemessage="creating "+fileBuild
			reply = QtGui.QMessageBox.question(None, 'Message' ,copyfilemessage, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
			if reply == QtGui.QMessageBox.Yes:
				if os.path.isfile(fileBuild)==True:
					cmessage="create over "+fileBuild
					replay = QtGui.QMessageBox.question(None, 'Message' ,cmessage, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
					if reply == QtGui.QMessageBox.Yes:
						inp=open(fileBuild, "w+")
						print selected_in_list
						inp.write(str(selected_in_list))
						inp.close()
						print "created "+fileBuild
					else:
						print "cancelled"
						return
				else:
					inp=open(fileBuild, "w+")
					print selected_in_list
					inp.write(str(selected_in_list))
					inp.close()
					print "created "+fileBuild
			else:
				print "cancelled"
				return
			self.refresh_playlist()
		elif list_build_function==get_a_play_list[2]:
			if len(selected_in_list)<1:
				print "need to select something"
				return
			else:
				pass				
			getpreset=[os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(playlistpath) for name in files if "_storedText.txt" in name]
			# getpreset=[os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(playlistpath) for name in files if playlist_name+"_storedText.txt"==name]
			# preset=self.find_playlists(playlistpath)
			if len(getpreset)<1:
				print "there are no lists available to append to"
				return
			else:
				pass
			makeContent=self.obtain_presets([getpreset[0]])	
			print makeContent
			makeNewContent=list(set(makeContent+selected_in_list))
			print makeNewContent
			title="new"
			inst_win=dropMenu(getpreset, title, makeNewContent)
			inst_win.show()

	def appender(self, getplayList, makeNewContent):
		inp=open(getplayList, "w+")
		inp.write(str(makeNewContent))
		inp.close()
		print "appended "+str(makeNewContent)+" into "+getplayList


	def find_playlists(self, prodding_directory):
		import ast
		preset=False
		format=".txt"
		getpreset=[os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(prodding_directory) for name in files if name.lower().endswith(format)]
		preset=[(each) for each in getpreset if "storedText" in each]	
		return preset	

	def obtain_presets(self, prodding_file):
		# getlistnames={}
		for each in prodding_file:
			List = open(each).readlines()
			for aline in List:
				makeContent=ast.literal_eval(aline)
				return makeContent
		

	def messageBox_callup(self, note):
		QtGui.QMessageBox.question(None, 'Message' , note)

		
	def makeBody(self, prompt):
		text, ok=QtGui.QInputDialog.getText(None, 'Intput Dialog', prompt)
		if ok:
			project=(str(text))
		else:
			return
		return project
		
	def makeBodyFilled(self, prompt, message):
		text, ok=QtGui.QInputDialog.getText(None, 'Intput Dialog', prompt, QtGui.QLineEdit.Normal, message)
		if ok and text:
			project=(str(text))
		else:
			return
		return project

	def makedialog(self, prompt):
		QtGui.QWidget(None, 'Intput Dialog', prompt, QtGui.QLineEdit.Normal, message)



	def onRightClick_preset(self):
		path=playlistpath
		self.launch_folder(path)


	def load(self):
		playlist_load=self.drop_list_06
		playlist_name=playlist_load.currentText()
		if playlist_name==get_a_play_list[0]:
			pass
		else:
			getpreset=[os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(playlistpath) for name in files if playlist_name+"_storedText.txt"==name]
			fileDict=[]
			makeContent=self.obtain_presets(getpreset)
			if makeContent:
				pass
			else:
				return
			for each in makeContent:
				import datetime
				getFolders=[(folderItem) for folderItem in os.listdir(each) if "mov" in folderItem]
				if getFolders:
					sub="yes"
				else:
					sub="no"				
				getAccTime=time.ctime(os.path.getmtime(each))
				statbuf=os.stat(each)	
				timeFormat=datetime.datetime.fromtimestamp(statbuf.st_mtime).strftime('%c')
				timeFormat=timeFormat.split(" ")[:4]
				timeFormat=" ".join(timeFormat)
				if "  " in str(getAccTime):
					getAccTime=getAccTime.split("  ")
					getAccTime=getAccTime[1].split(" ")[1]
				else:
					getAccTime=getAccTime.split(" ")[3]
				timeFormat=timeFormat+"  "+getAccTime+'>'+sub
				makeDict=(each, timeFormat)
				fileDict.append(makeDict)
			count=len(fileDict)
			fileDict=reversed(fileDict)		
			count=len(makeContent)
			self.listWidg.setColumnCount(4)
			self.listWidg.setRowCount(count)
			self.listWidg.setHorizontalHeaderLabels(headers)
			for row, item in enumerate(fileDict):
				key=item[0].split('/')[-1]
				path=item[0]
				value=item[1].split('>')[0]
				sub=item[1].split('>')[1]
				self.listWidg.setItem(row, 0, QTableWidgetItem(key))
				self.listWidg.setItem(row, 1, QTableWidgetItem(value))
				self.listWidg.setItem(row, 2, QTableWidgetItem(path))
				self.listWidg.setItem(row, 3, QTableWidgetItem(sub))




	def directory_for_taking(self, getUser, directory):
		model, countdata, listArray	=self.get_listset_directory()
		# self.status_lbl

	def connectButton01(self):
		self.listCreate()

	def set_to_project(self):
		type_list=self.drop_list_det
		list_type=type_list.currentText()		
		get_the_path_slot=self.custompath
		get_the_path_slot.setText(project_path_pbMovs)
		self.cust_listCreate(project_path_pbMovs, list_type)

	def set_to_user(self):
		type_list=self.drop_list_det
		list_type=type_list.currentText()	
		get_the_path_slot=self.custompath
		get_the_path_slot.setText(user_path_pbmovs)
		self.cust_listCreate(user_path_pbmovs, list_type)

	def set_toCustom(self):
		type_list=self.drop_list_det
		list_type=type_list.currentText()			
		get_the_path_slot=self.custompath
		user_path=get_the_path_slot.text()
		self.cust_listCreate(user_path,list_type)

	def cust_listCreate(self, pathFound, list_type):
		self.listWidg.setColumnCount(4)
		try:
			if list_type=="file":
				getFiles=[os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(playlistpath) for name in files]
			elif list_type=="folder":
				getFiles=[os.path.join(pathFound, o) for o in os.listdir(pathFound) if os.path.isdir(os.path.join(pathFound, o))]
			pass
		except:
			print "nothing found"
			return
		# getFile=[(each) for each in getFiles if getpwuid(stat(each).st_uid).pw_name==getUser]
		getFiles.sort(key=lambda x: os.path.getmtime(x))
		fileDict=[]
		sub="no"
		for each in getFiles:
			statbuf=os.stat(each)
			import datetime
			# timeFormat=time.strftime('%m/%d/%Y', time.gmtime(os.path.getctime(each)))
			getAccTime=time.ctime(os.path.getmtime(each))
			timeFormat=datetime.datetime.fromtimestamp(statbuf.st_mtime).strftime('%c')
			timeFormat=timeFormat.split(" ")[:4]
			timeFormat=" ".join(timeFormat)
			if "  " in str(getAccTime):
				getAccTime=getAccTime.split("  ")
				getAccTime=getAccTime[1].split(" ")[1]
			else:
				getAccTime=getAccTime.split(" ")[3]
			# timeFormat=timeFormat+"  "+findSomeTime+'>'+sub
			timeFormat=timeFormat+"  "+getAccTime+'>'+sub
			makeDict=(each, timeFormat)
			fileDict.append(makeDict)
		count=len(fileDict)
		fileDict=reversed(fileDict)
		dictItems=fileDict
		self.listWidg.setRowCount(count)
		self.listWidg.setHorizontalHeaderLabels(headers)
		for row, item in enumerate(fileDict):
			key=item[0].split('/')[-1]
			path=item[0]
			value=item[1].split('>')[0]
			sub=item[1].split('>')[1]
			self.listWidg.setItem(row, 0, QTableWidgetItem(key))
			self.listWidg.setItem(row, 1, QTableWidgetItem(value))
			self.listWidg.setItem(row, 2, QTableWidgetItem(path))
			self.listWidg.setItem(row, 3, QTableWidgetItem(sub))

	def RightClick(self):
		selected_in_list=self.is_listWid_item_selected()
		path=str(selected_in_list[0])+"/"
		# command="xdg-open '%s'"%path
		self.launch_folder(path)


	def play_in_rv(self):
		selected_in_list=self.is_listWid_item_selected()
		command="rv "+str(selected_in_list[0])+"/*"
		print "you are running command: "+command
		subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)



	def play_latest_anim(self):
		playFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/anim'		
		fileDict=self.rv_latest_mov_nopub(playFolder)
		get_play=fileDict[-1][0]
		self.direct_play_rv(get_play)

	def play_latest_anim_pub(self):
		playFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/anim'		
		fileDict=self.rv_latest_mov_pubonly(playFolder)
		get_play=fileDict[-1][0]
		self.direct_play_rv(get_play)

	def onRightClick_anim(self):		
		path='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/anim'
		self.launch_folder(path)


	def play_latest_light(self):
		playFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/lightcomp'		
		fileDict=self.rv_latest_mov(playFolder)
		get_play=fileDict[-1][0]
		self.direct_play_rv(get_play)


	def onRightClick_light(self):		
		path='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/lightcomp'
		self.launch_folder(path)

	def play_latest_comp(self):
		playFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/comp'		
		fileDict=self.rv_latest_mov(playFolder)
		get_play=fileDict[-1][0]
		self.direct_play_rv(get_play)


	def onRightClick_comp(self):		
		path='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/comp'
		self.launch_folder(path)


	def play_latest_fx(self):
		playFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/fxflip'		
		fileDict=self.rv_latest_mov(playFolder)
		get_play=fileDict[-1][0]
		self.direct_play_rv(get_play)


	def onRightClick_fx(self):		
		path='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/fxflip'
		self.launch_folder(path)


	def play_latest_tracking(self):
		playFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/trackcomp'		
		fileDict=self.rv_latest_mov(playFolder)
		get_play=fileDict[-1][0]
		self.direct_play_rv(get_play)



	def onRightClick_tracking(self):		
		path='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/trackcomp'
		self.launch_folder(path)



	def play_latest_matchmove(self):
		playFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/matchmove'		
		fileDict=self.rv_latest_mov(playFolder)
		get_play=fileDict[-1][0]
		self.direct_play_rv(get_play)



	def onRightClick_matchmove(self):		
		path='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/matchmove'
		self.launch_folder(path)




	def play_latest_roto(self):
		playFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/roto'		
		fileDict=self.rv_latest_mov(playFolder)
		get_play=fileDict[-1][0]
		self.direct_play_rv(get_play)



	def onRightClick_roto(self):		
		path='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/roto'
		self.launch_folder(path)



	def play_latest_techanim(self):
		playFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/techanim'		
		fileDict=self.rv_latest_mov_nopub(playFolder)
		get_play=fileDict[-1][0]
		self.direct_play_rv(get_play)



	def onRightClick_techanim(self):		
		path='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/techanim'
		self.launch_folder(path)


	def play_latest_techanim_pub(self):
		playFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/techanim'		
		fileDict=self.rv_latest_mov_pubonly(playFolder)
		get_play=fileDict[-1][0]
		self.direct_play_rv(get_play)


	def rv_latest_raw(self, playFolder):
		try:
			getFiles=[os.path.join(playFolder, o) for o in os.listdir(playFolder) if os.path.isdir(os.path.join(playFolder, o))]
			pass
		except:
			print "nothing found"
			return
		# getFile=[(each) for each in getFiles if getpwuid(stat(each).st_uid).pw_name==getUser]
		getFiles.sort(key=lambda x: os.path.getmtime(x))
		fileDict=[]
		for each in getFiles:
			statbuf=os.stat(each)
			import datetime
			# timeFormat=time.strftime('%m/%d/%Y', time.gmtime(os.path.getctime(each)))
			getAccTime=time.ctime(os.path.getmtime(each))
			timeFormat=datetime.datetime.fromtimestamp(statbuf.st_mtime).strftime('%c')
			timeFormat=timeFormat.split(" ")[:4]
			timeFormat=" ".join(timeFormat)
			if "  " in str(getAccTime):
				getAccTime=getAccTime.split("  ")
				getAccTime=getAccTime[1].split(" ")[1]
			else:
				getAccTime=getAccTime.split(" ")[3]
			# timeFormat=timeFormat+"  "+findSomeTime+'>'+sub
			timeFormat=timeFormat+"  "+getAccTime
			makeDict=(each, timeFormat)
			fileDict.append(makeDict)
		command="rv "+str(fileDict[-1][0])+"/*"
		print "you are running command: "+command
		subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)	

	def rv_latest_mov(self, playFolder):
		try:
			getFiles=[os.path.join(playFolder, o) for o in os.listdir(playFolder) if os.path.isdir(os.path.join(playFolder, o))]
			pass
		except:
			# print "nothing found"
			return
		# getFile=[(each) for each in getFiles if getpwuid(stat(each).st_uid).pw_name==getUser]
		getFiles.sort(key=lambda x: os.path.getmtime(x))
		fileDict=[]
		for each in getFiles:
			getTheMovFolders=[(folderItem) for folderItem in os.listdir(each) if "mov" in folderItem]
			if getTheMovFolders:
				statbuf=os.stat(each)
				import datetime
				# timeFormat=time.strftime('%m/%d/%Y', time.gmtime(os.path.getctime(each)))
				getAccTime=time.ctime(os.path.getmtime(each))
				getMovie=each+'/'+getTheMovFolders[0]
				timeFormat=datetime.datetime.fromtimestamp(statbuf.st_mtime).strftime('%c')
				timeFormat=timeFormat.split(" ")[:4]
				timeFormat=" ".join(timeFormat)
				if "  " in str(getAccTime):
					getAccTime=getAccTime.split("  ")
					getAccTime=getAccTime[1].split(" ")[1]
				else:
					getAccTime=getAccTime.split(" ")[3]
				# timeFormat=timeFormat+"  "+findSomeTime+'>'+sub
				timeFormat=timeFormat+"  "+getAccTime
				makeDict=(getMovie, timeFormat)
				fileDict.append(makeDict)
		return fileDict

	def rv_latest_mov_nopub(self, playFolder):
		try:
			getFiles=[os.path.join(playFolder, o) for o in os.listdir(playFolder) if os.path.isdir(os.path.join(playFolder, o))]
			pass
		except:
			# print "nothing found"
			return
		# getFile=[(each) for each in getFiles if getpwuid(stat(each).st_uid).pw_name==getUser]
		getFiles.sort(key=lambda x: os.path.getmtime(x))
		fileDict=[]
		for each in getFiles:
			getTheMovFolders=[(folderItem) for folderItem in os.listdir(each) if "mov" in folderItem and "pubRender" not in folderItem]
			if getTheMovFolders:
				statbuf=os.stat(each)
				import datetime
				# timeFormat=time.strftime('%m/%d/%Y', time.gmtime(os.path.getctime(each)))
				getAccTime=time.ctime(os.path.getmtime(each))
				getMovie=each+'/'+getTheMovFolders[0]
				timeFormat=datetime.datetime.fromtimestamp(statbuf.st_mtime).strftime('%c')
				timeFormat=timeFormat.split(" ")[:4]
				timeFormat=" ".join(timeFormat)
				if "  " in str(getAccTime):
					getAccTime=getAccTime.split("  ")
					getAccTime=getAccTime[1].split(" ")[1]
				else:
					getAccTime=getAccTime.split(" ")[3]
				# timeFormat=timeFormat+"  "+findSomeTime+'>'+sub
				timeFormat=timeFormat+"  "+getAccTime
				makeDict=(getMovie, timeFormat)
				fileDict.append(makeDict)
		return fileDict


	def rv_latest_mov_pubonly(self, playFolder):
		try:
			getFiles=[os.path.join(playFolder, o) for o in os.listdir(playFolder) if os.path.isdir(os.path.join(playFolder, o))]
			pass
		except:
			# print "nothing found"
			return
		# getFile=[(each) for each in getFiles if getpwuid(stat(each).st_uid).pw_name==getUser]
		getFiles.sort(key=lambda x: os.path.getmtime(x))
		fileDict=[]
		for each in getFiles:
			getTheMovFolders=[(folderItem) for folderItem in os.listdir(each) if "mov" in folderItem and "pubRender" in folderItem]
			if getTheMovFolders:
				statbuf=os.stat(each)
				import datetime
				# timeFormat=time.strftime('%m/%d/%Y', time.gmtime(os.path.getctime(each)))
				getAccTime=time.ctime(os.path.getmtime(each))
				getMovie=each+'/'+getTheMovFolders[0]
				timeFormat=datetime.datetime.fromtimestamp(statbuf.st_mtime).strftime('%c')
				timeFormat=timeFormat.split(" ")[:4]
				timeFormat=" ".join(timeFormat)
				if "  " in str(getAccTime):
					getAccTime=getAccTime.split("  ")
					getAccTime=getAccTime[1].split(" ")[1]
				else:
					getAccTime=getAccTime.split(" ")[3]
				# timeFormat=timeFormat+"  "+findSomeTime+'>'+sub
				timeFormat=timeFormat+"  "+getAccTime
				makeDict=(getMovie, timeFormat)
				fileDict.append(makeDict)
		return fileDict

	def direct_play_rv(self, item):
		selected_in_list=self.is_listWid_item_selected()
		if selected_in_list:
			command="rv -wipe "+str(item)+"/* "+' '.join(selected_in_list)
			print "you are running command: "+command
			subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)		
		else:
			command="rv "+str(item)+"/*"
			print "you are running command: "+command
			subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)		

	def compare_in_rv(self):
		selected_in_list=self.is_listWid_item_selected()
		if len(selected_in_list)<2:
			print "must select more than one object in list"
		else:
			command="rv -wipe "+str(selected_in_list[0])+"/* "+str(selected_in_list[1])+"/*"
			print "you are running command: "+command
			subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)


	def pub_to_shotgun(self):
		selected_in_list=self.is_listWid_item_selected()
		if len(selected_in_list)>0:
			pass
		else:
			selWarningText= "Must select something in list"
			self.messageBox_callup(selWarningText)
			print selWarningText
			return
		checkForMov=[(each) for each in os.listdir(selected_in_list[0]) if "_mov" in each]
		if len(checkForMov)>0:
			warningText="This version has already been submitted to shotgun. Unable to submit again."
			print warningText
			self.messageBox_callup(warningText)
			return
		else:
			pass
		getFirst=self.head_field
		getFirstFrame=getFirst.toPlainText()
		getFirstFrame=getFirstFrame.split('.')[0]
		getFirstFrame=str(getFirstFrame)
		getCommentBox=self.fieldBox
		comment=getCommentBox.text()
		comment=str(comment)
		getType=self.type_list_drop
		getTheType=getType.currentText()
		getTheType=str(getTheType)
		for each in failedComments:
			if comment == each:
				commentWarning= "Please provide a meaningful comment for submit"
				comment=self.makeBody(commentWarning)
				print commentWarning
			else:
				pass
		# if comment == "defaultText":
		# 	commentWarning= "Please provide a meaningful comment for submit"
		# 	comment=self.makeBody(commentWarning)
		# 	print commentWarning
		# elif comment == "":
		# 	commentWarning= "Please provide a meaningful comment for submit"
		# 	comment=self.makeBody(commentWarning)
		# 	print commentWarning
		# else:
		# 	pass
		getPath=selected_in_list[0]+'/'
		get_items=os.listdir(getPath)
		getFolderForJpgs=[(each) for each in get_items if "jpg" in each]
		# sys.exit(app.exec_())
		getPlayFolder=selected_in_list[0]+'/'+getFolderForJpgs[0]+'/'
		getList=os.listdir(getPlayFolder)
		getList=[(each) for each in getList if not each.startswith('.')]
		getImageName=getList[0].split('.')[0]
		# getFrameLengthExist=len(os.listdir(getPlayFolder)[0].split('.'))-2
		# print getFrameLengthExist
		getFrameLengthExist=[os.path.join(getPlayFolder, o) for o in os.listdir(getPlayFolder)]
		getFrameLengthExist.sort(key=lambda x: os.path.getmtime(x))	
		getTrueLast=int(getFrameLengthExist[-3].split('.')[-2:-1][0])
		# plate=getPlayFolder+getImageName+'.'+str(int(getFirstFrame))+'-'+str(int(getLastFrame))+formatEXT
		# plate=str(getPlayFolder)+str(getImageName)+'.f.%d-f.%d' % (int(getFirstFrame), int(getLastFrame))
		getLast=self.toe_field	
		getLastFrame=getLast.toPlainText()	
		getLastFrame=getLastFrame.split('.')[0]
		getLastFrame=str(getLastFrame)
		if getTrueLast<int(getLastFrame):
			getLastFrame=getTrueLast
		else:
			getLastFrame=getLastFrame
		# plate=getPlayFolder+getImageName+'.%04d['+str(getFirstFrame)+'-'+str(getLastFrame)+']'+formatEXT
		plate=getPlayFolder+getImageName+'.%04d'+formatEXT
		command='msubmitCmd -p '+plate+' -s '+str(getFirstFrame)+' -e '+str(getLastFrame)+' -n "'+comment+'" -t '+getTheType+' --task '+DEPT
		print "you are running command: "+command
		subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
		print "submitted"


	def pub_mov_to_shotgun(self):
		selected_in_list=self.is_listWid_item_selected()
		if len(selected_in_list)>0:
			pass
		else:
			selWarningText= "Must select something in list"
			self.messageBox_callup(selWarningText)
			print selWarningText
			return
		checkForMov=[(each) for each in os.listdir(selected_in_list[0]) if "_mov" in each]
		getCommentBox=self.fieldBox
		comment=getCommentBox.text()
		comment=str(comment)
		getType=self.type_list_drop
		getTheType=getType.currentText()
		getTheType=str(getTheType)
		for each in failedComments:
			if comment == each:
				commentWarning= "Please provide a meaningful comment for submit"
				comment=self.makeBody(commentWarning)
				print commentWarning
			else:
				pass
		getPath=selected_in_list[0]+'/'
		get_items=os.listdir(getPath)
		getFolderForJpgs=[(each) for each in get_items if "mov" in each]
		getCompletePath=selected_in_list[0]+'/'+getFolderForJpgs[0]
		getmov=[(each) for each in os.listdir(getCompletePath) if "mov" in each][0]
		plate= getCompletePath+'/'+getmov
		print plate
		command='msubmitCmd -p ' +plate+' -n "'+comment+'" -t '+getTheType+' --task '+DEPT
		print "you are running command: "+command
		subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
		print "submitted"

	def send(self):
		print "end"

	def card_special_callup(self):
		print "card_special_callup"
		
	def Bcard_special_callup(self):
		print "B_card_special_callup"
		
		
	def B_card_special_callup(self):
		print "B_card_special_callup"
		
# if __name__=="__main__":
app=QtGui.QApplication(sys.argv)
inst=typicalWindow()
inst.show()
sys.exit(app.exec_())

