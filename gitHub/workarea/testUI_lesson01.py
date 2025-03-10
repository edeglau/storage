
__author__="me"


import PyQt4
print "hi"
from PyQt4 import QtCore, QtGui, Qt
print "start"
from PyQt4.QtGui import QWidget, QRadioButton, QGridLayout, QLabel, \
	QTableWidget, QComboBox, QKeySequence, QToolButton, QPlainTextEdit, QPushButton,QBoxLayout, \
	QClipboard, QTableWidgetItem, QCheckBox, QVBoxLayout, QHBoxLayout, \
	QPixmap, QLineEdit, QListWidget, QTextEdit, QSizePolicy, QFrame, QPalette, QColor, \
	QFont, QAbstractItemView, QMenu, QMessageBox
from PyQt4.QtCore import SIGNAL
print "middle"

import os, sys, operator, re, glob, getpass, subprocess, shutil, string, random, ast, webbrowser, time, datetime
from subprocess import Popen, PIPE
from os import stat, listdir, walk
from pwd import getpwuid
import os.path
from os.path import isfile, join
from datetime import datetime
buttonGrp=[]
winTitle="title"
presetlist=["load"]
typesOfStuffInList=["firstPath", "secondPath"]
availableStyles=['darkorangefix']
styleSheetFile=availableStyles[0]
get_a_play_list=["load", "build"]
alist2=["arm","leg"]
col1, col2, col3= 240, 160, 500
pre=[]
regular=[(150,70,70), (150,150,70), (100, 100, 170)]
regularDict={"darkRed":(150,70,70), "yellow":(120,120,70), "green":(70, 150, 70), "blue":(50,100,200)}
buttonColoursDict=regularDict
developer=[__author__]
defaultText="defaultText"


workSpace='/jobs/vfx_okja/rdo/rdo00140/TASKS/techanim/'
M_USER = os.getenv("USER")
# workSpace=cmds.workspace(q=1, lfw=1)[-1]
PROJECT=workSpace.split('/')[2]
SCENE=workSpace.split('/')[3]
SHOT=workSpace.split('/')[4]
DEPT=workSpace.split('/')[6]



projectFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT
animFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/instances/'
abcFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/cache/alembic/'
pbFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/movies/'
rvFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/'+DEPT
projects='/jobs/'+PROJECT
prjFileName = os.listdir(projects)
prjFileName=sorted(prjFileName)
getUser=getpass.getuser()


audioVer="v0001"

audioName="/pcm_s16le_aif/ns0161_cut_main_v0001-pcm_s16le"

audioFormat=".aif"

audioFile='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/REFERENCE/editorial/cut/main/'+audioVer+'/'+audioName+audioFormat

comment="test"
startFR=998
endFR=1016

typeplay="playblast-hhd_vdf8"
foldertypeplay="playblast-hhd_vdf8_jpg"

formatEXT=".jpg"

print "making window..."

class typicalWindow(QtGui.QMainWindow):
	def __init__(self, parent=None):
		super(typicalWindow, self).__init__(parent)
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
		
		self.base_layout=QGridLayout()
		self.base_layout.setAlignment(QtCore.Qt.AlignTop)
		self.botDivideLayout.addLayout(self.base_layout, 4,0,1,1)
		
		#sshFile=open(os.path.join(__location__, styleSheetFile+".stylesheet"), 'r')
		#self.styleData=sshFile.read()
		#sshFile.close
		
		#self.setStyleSheet(self.styleData)
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
		
		self.frame_layout=QGridLayout()
		self.frame_layout.setAlignment(QtCore.Qt.AlignTop)
		self.lower_layout.addLayout(self.frame_layout, 0,0,1,1)
		
		
		self.frameWidget=QtGui.QGridLayout()
		self.frameWidget.setContentsMargins(5,10,5,10)
		self.frameOverride=QtGui.QFrame()
		self.frameOverride.setStyleSheet("background-color: #434343; border-style: solid; border-width: 2px; border-color:#434343;border-radius:8px;")
		self.frameOverride.setFixedHeight(100)
		self.frame_layout.addLayout(self.frameWidget, 0,0,1,1)
		self.frame_layout.addWidget(self.frameOverride, 0,0,1,1)
		
		
		self.frame_title_layout=QGridLayout()
		self.frameWidget.addLayout(self.frame_title_layout, 0,0,1,1)
		self.frame_radio_layout=QGridLayout()
		self.frameWidget.addLayout(self.frame_radio_layout, 1,0,1,1)
		self.frame_btn_layout=QGridLayout()
		self.frameWidget.addLayout(self.frame_btn_layout, 2,0,1,1)
	
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
		self.drop_lbl_01=QLabel()
		self.drop_lbl_01.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
		self.drop_lbl_01.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,0);")
		self.window_layer_01.addWidget(self.drop_lbl_01, 0,0,1,1)
		
		self.drop_01=QComboBox()
		self.window_layer_01.addWidget(self.drop_01, 0,1,1,1)
		self.drop_01.addItems(prjFileName)
		self.drop_01.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.drop_01.customContextMenuRequested.connect(self.onRightClick)

		# self.drop_01.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		# self.connect(self.drop_lbl_01, SIGNAL("customContextMenuRequested(QPoint)"), self.onRightClick)
		
		self.drop_lbl_02=QLabel()
		self.drop_lbl_02.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
		self.drop_lbl_02.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,0);")
		self.window_layer_01.addWidget(self.drop_lbl_02, 0,2,1,1)
		
		self.drop_02=QComboBox()
		self.window_layer_01.addWidget(self.drop_02, 0,3,1,1)
		# QtCore.QObject.connect(self.drop_02, SIGNAL("currentIndexChanged(QString)"),
		# 						self.on_drop_01_changed)
		self.drop_02.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self.drop_lbl_01, SIGNAL("customContextMenuRequested(QPoint)"), self.onRightClick)
		
		QtCore.QObject.connect(self.drop_01, SIGNAL("currentIndexChanged(QString)"),
								self.on_drop_01_changed)

		self.button_01=QPushButton("Set")
		self.button_01.setToolTip("set")
		self.connect(self.button_01, SIGNAL('clicked()'), self.listCreate)
		self.window_layer_01.addWidget(self.button_01, 0,4,1,1)
		
		self.button_02=QPushButton("Set2")
		self.button_02.setToolTip("set2")
		self.connect(self.button_02, SIGNAL('clicked()'), self.connectButton01)
		self.window_layer_01.addWidget(self.button_02, 0,5,1,1)

		self.drop_lbl_03=QLabel()
		self.drop_lbl_03.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
		self.drop_lbl_03.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,0);")
		self.window_layer_02.addWidget(self.drop_lbl_03, 0,0,1,1)
		
		self.drop_03=QComboBox()
		self.window_layer_02.addWidget(self.drop_03, 0,1,1,1)
		# QtCore.QObject.connect(self.drop_03, SIGNAL("currentIndexChanged(QString)"),
		# 						self.on_drop_01_changed)
		self.drop_03.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self.drop_03, SIGNAL("customContextMenuRequested(QPoint)"), self.onRightClick)

		self.button_03=QPushButton("button_03")
		self.button_03.setToolTip("button_03")
		self.connect(self.button_03, SIGNAL('clicked()'), self.connectButton01)
		self.window_layer_02.addWidget(self.button_03, 0,2,1,1)
		
		self.button_04=QPushButton("button_04")
		self.button_04.setToolTip("button_04")
		self.connect(self.button_04, SIGNAL('clicked()'), self.connectButton01)
		self.window_layer_02.addWidget(self.button_04, 0,3,1,1)
		
		self.button_05=QPushButton("button_05")
		self.button_05.setToolTip("button_05")
		self.connect(self.button_05, SIGNAL('clicked()'), self.connectButton01)
		self.window_layer_02.addWidget(self.button_05, 0,4,1,1)

		self.drop_04=QComboBox()
		self.window_layer_04.addWidget(self.drop_04, 0,2,1,1)
		# QtCore.QObject.connect(self.drop_04, SIGNAL("currentIndexChanged(QString)"),
		# 						self.on_drop_01_changed)
		self.drop_04.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self.drop_04, SIGNAL("customContextMenuRequested(QPoint)"), self.onRightClick)

		self.list_frame=QFrame()
		self.list_frame.setStyleSheet("color: rgb"+str(buttonColoursDict.get("red")))
		self.list_layout=QHBoxLayout()
		self.list_frame.setLayout(self.list_layout)
		
		self.drop_list_builder_05=QComboBox()
		self.drop_list_builder_05.addItems(get_a_play_list)
		QtCore.QObject.connect(self.drop_list_builder_05, SIGNAL("currentIndexChanged(QString)"),
								self.build)
		self.drop_list_builder_05.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self.drop_list_builder_05, SIGNAL("customContextMenuRequested(QPoint)"), self.onRightClick)
		self.list_layout.addWidget(self.drop_list_builder_05)
		self.window_layer_04.addWidget(self.list_frame, 0,3,1,1)

		self.drop_list_06=QComboBox()
		# QtCore.QObject.connect(self.drop_list_06, SIGNAL("currentIndexChanged(QString)"),self.load)
		self.drop_list_06.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self.drop_list_06, SIGNAL("customContextMenuRequested(QPoint)"), self.onRightClick)
		#if len(pres)<1:
			#self.drop_list_06.setEnabled(0)
		#else:
			#self.drop_list_06.setEnabled(1)
		self.drop_list_06.addItems(alist2)
		self.list_layout.addWidget(self.drop_list_06)
		
		self.type_list_drop=QComboBox()
		self.type_list_drop.addItems(typesOfStuffInList)
		QtCore.QObject.connect(self.type_list_drop, SIGNAL("currentIndexChanged(QString)"),
								self.on_drop_01_changed)
		self.window_layer_04.addWidget(self.type_list_drop, 0,5,1,1)
		
		self.button_06=QPushButton("button_06")
		self.button_06.setToolTip("button_06")
		self.connect(self.button_06, SIGNAL('clicked()'), self.connectButton01)	
		self.window_layer_04.addWidget(self.button_06, 0,6,0,1)



		headers = ('Name', 'Date', 'Path')

		self.listWidg = QTableWidget(1, 3)
		# self.listWidg.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		# self.listWidg.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
		# self.listWidg.cellPressed.connect(self.clicked)
		
		# self.listWidg=QTableWidget(0, 3)
		self.listWidg.setHorizontalHeaderLabels(headers)
		# tableWidget=self.listWidg
		self.listWidg.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)		
		col1, col2, col3= 240, 160, 500
		self.listWidg.setColumnWidth(0, col1)
		self.listWidg.setColumnWidth(1, col2)
		self.listWidg.setColumnWidth(2, col3)
		self.listWidg.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.listWidg.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.listWidg.customContextMenuRequested.connect(self.RightClick)
		# self.listWidg.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)		
		self.connect(self.listWidg, SIGNAL("itemClicked(QTableWidgetItem *)"), self.clicked)
		self.connect(self.listWidg, SIGNAL("itemDoubleClicked(QTableWidgetItem *)"), self.dclicked)
		self.window_layer_05.addWidget(self.listWidg, 0,2,1,1)


		self.status_lbl=QLabel()
		self.status_lbl.setStyleSheet('background-color:transparent')
		self.status_lbl.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
		self.frame_title_layout.addWidget(self.status_lbl, 0,2,1,1)

		self.spaceHold=QLabel()
		self.spaceHold.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,0);")
		self.spaceHold.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
		self.frame_title_layout.addWidget(self.spaceHold, 0,0,1,1)


		self.checkbox=QCheckBox("add")
		self.checkbox.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,0);")
		# self.checkbox.setContentsMargins(5,0,0,0)
		self.checkbox.setChecked(1)
		self.frame_title_layout.addWidget(self.checkbox, 0,1,1,1)
		
		self.radiobox=QGridLayout()

		self.radio=QRadioButton("radio")
		self.radio.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,0);")
		self.radio.setChecked(1)
		self.radiobox.addWidget(self.radio, 0,0,1,1)
		
		
		self.newradio=QRadioButton("newradio")
		self.newradio.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,0);")
		self.radiobox.addWidget(self.newradio, 0,2,1,1)
		
		self.frame_len_layout=QGridLayout()
		self.frame_len_layout.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
		#self.frame_title_layout.addWidget(self.frame_len_layout, 1,3,1,1)
		
		self.spaceHold=QLabel()
		self.spaceHold.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,0);")
		self.spaceHold.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
		self.frame_title_layout.addWidget(self.spaceHold, 0,3,1,1)
		
		self.over=QRadioButton("over")
		self.over.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,0);")
		self.radiobox.addWidget(self.over, 1,1,1,1)
		
		self.head_lbl=QLabel("from")
		self.head_lbl.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,0);")
		self.radiobox.addWidget(self.head_lbl, 1, 4,1,1)
		
		self.head_field=QTextEdit("")
		self.head_field.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,0);")
		self.radiobox.addWidget(self.head_field, 1, 5,1,1)
		
		self.toe_lbl=QLabel("til")
		self.toe_lbl.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,0);")
		self.radiobox.addWidget(self.toe_lbl, 1, 6,1,1)
		
		self.toe_field=QTextEdit("")
		self.toe_field.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,0);")
		self.radiobox.addWidget(self.toe_field, 1, 7,1,1)
		
		self.fieldBox=QLineEdit()
		self.fieldBox.setVisible(0)
		self.fieldBox.setText(defaultText)
		
		self.play_in_rv_button=QPushButton("play in RV")
		self.connect(self.play_in_rv_button, SIGNAL('clicked()'), self.play_in_rv)
		self.frame_btn_layout.addWidget(self.play_in_rv_button, 0,0,0,1)
		
		self.look_btn=QPushButton("compare")
		self.connect(self.look_btn, SIGNAL('clicked()'), self.compare_in_rv)
		self.frame_btn_layout.addWidget(self.look_btn, 0,1, 0,1)


		# self.link_btn=QPushButton("link")
		# self.connect(self.link_btn, SIGNAL('clicked()'), self.play_in_rv)
		# self.frame_btn_layout.addWidget(self.link_btn, 0,2,1,1)
		
		self.create_btn=QPushButton("Publish")
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
		
		self.card_menu=QMenu("card")
		self.card_menuBar=self.menuBar()
		self.card_menuBar.addMenu(self.card_menu)
		self.park_btn_pkt.addWidget(self.card_menuBar)
		buttonGrp.append(self.card_menuBar)
		
		self.card_btn=QToolButton()
		self.card_btn.setPopupMode(QToolButton.MenuButtonPopup)
		self.card_btn.setMenu(self.card_menu)
		self.card_special_btn=QPushButton("card special")
		self.connect(self.card_special_btn, SIGNAL('clicked()'), self.card_special_callup)
		action=QtGui.QWidgetAction(self.card_btn)
		action.setDefaultWidget(self.card_special_btn)
		self.card_btn.menu().addAction(action)

		self.B_card_btn=QToolButton()
		self.B_card_btn.setPopupMode(QToolButton.MenuButtonPopup)
		self.B_card_btn.setMenu(self.card_menu)
		self.B_card_special_btn=QPushButton("card special")
		self.connect(self.B_card_special_btn, SIGNAL('clicked()'),self.B_card_special_callup)
		action=QtGui.QWidgetAction(self.B_card_btn)
		action.setDefaultWidget(self.B_card_special_btn)
		self.B_card_btn.menu().addAction(action)

		self.start_window()

	def start_window(self):
		# self.connectButton01
		print PROJECT		
		print SCENE
		print SHOT
		index = self.drop_01.findText(SCENE, QtCore.Qt.MatchFixedString)
		self.drop_01.setCurrentIndex(index)
		self.get_scene()
		index2 = self.drop_02.findText(SHOT, QtCore.Qt.MatchFixedString)
		self.drop_02.setCurrentIndex(index2)		
		self.listCreate()

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


	def launch_folder(self, path):
		# command="xdg-open '%s'"%path
		command="dolphin '%s'"%path
		subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
		
	def on_drop_01_changed(self):
		self.get_scene()
		newcol1=self.listWidg.columnWidth(0)
		newcol2=self.listWidg.columnWidth(1)
		newcol3=self.listWidg.columnWidth(2)
		if newcol1==0:
			col1, col2, col3= 240, 160, 500
		else:
			col1, col2, col3= newcol1, newcol2, newcol3
		# findproject=self.drop_01
		self.listWidg.clear()
		self.status_lbl.clear()
		# self.listCreate()
		# self.makeList(listpath, newUser, self.listWidg, model, stat_lab, listtype)
		# self.drop_03.addItems(get_items)
		# model, countdata, listArray	=self.get_listStuff()	
		# if self.on_drop_01=="item1":
		# 	buildListPath=pathList.get("listpathtype").replace(getUser, newUser)
		# 	self.makeList(listpath, newUser, self.listWidg, model, stat_lab, listtype)
		# elif self.on_drop_01=="item2":
		# 	buildListPath=pathList.get("listpathtype2").replace(getUser, newUser)
		# 	self.makeList(listpath, newUser, self.listWidg, model, stat_lab, listtype)
			
	def clicked(self):
		print "hi"
		
	def dclicked(self):
		print "hello"
		
	def get_listStuff(self):
		listArray=self.listWidg
		countdata=listArray.rowCount()
		model=listArray.model()
		return model, countdata, listArray
		
	def getListWidgetData(self):
		model, countdata, listArray	=self.get_listStuff()	
		dataInListWidget=[]
		for row in range(model.rowCount()):
			dataInListWidget.append([])
			for column in range(model.columnCount()):
				index = model.index(row, column)
				dataInListWidget[row].append(str(model.data(index).toString()))
		return dataInListWidget, countdata
		
	def grab_folder_items(self):
		directory=rvFolder
		getstuff=os.listdir(directory)
		getUser=M_USER
		(dataInListWidget, countdata)=self.getListWidgetData()
		# self.listWidg.setRowCount(0)
		# self.listWidg.setColumnCount(0)
		try:
			getFiles=[os.path.join(directory, o) for o in os.listdir(directory) if os.path.isdir(os.path.join(directory, o))]
			pass
		except:
			print "nothing found"
			return
		getFile=[(each) for each in getFiles if getpwuid(stat(each).st_uid).pw_name==getUser]
		getFiles.sort(key=lambda x: os.path.getmtime(x))
		fileDict=[]
		for each in getFiles:
			statbuf=os.stat(each)
			timeFormat=time.strftime('%m/%d/%Y', time.gmtime(os.path.getctime(each)))
			getAccTime=time.ctime(os.path.getmtime(each))
			if "  " in str(getAccTime):
				getAccTime=getAccTime.split("  ")
				getAccTime=getAccTime[1].split(" ")[1]
			else:
				getAccTime=getAccTime.split("  ")[3]
			timeFormat=timeFormat+"  "+getAccTime
			makeDict=(each, timeFormat)
			fileDict.append(makeDict)
		count=len(fileDict)
		fileDict=reversed(fileDict)
		dictItems=fileDict
		return fileDict, count


	def listCreate(self):
		self.listWidg.setColumnCount(3)
		fileDict, count=self.grab_folder_items()		
		self.listWidg.setRowCount(count)
		for row, item in enumerate(fileDict):
			key=item[0].split('/')[-1]
			path=item[0]
			value=item[1]
			self.listWidg.setItem(row, 0, QTableWidgetItem(key))
			self.listWidg.setItem(row, 1, QTableWidgetItem(value))
			self.listWidg.setItem(row, 2, QTableWidgetItem(path))



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
		return get_string_id
		
	def build(self):
		list_build=self.drop_list_builder_05
		list_build_function=list_build.currentText()
		selected_in_list=self.is_listWid_item_selected()
		allthePaths=('//', '//')
		allthePathsDic={"firstPath":'//', "secondPath":'//'}
		#drop_list_builder_05
		getlisttype=self.type_list_drop
		listtype=getlisttype.currentText()
		if selected_in_list>1:
			getItems=[(each) for each in selected_in_list]
			nameToSave=' '.join(getItems)
			if listtype=="firstPath":
				suffixAppend="first"
				path=allthePathsDic.get("firstPath")
			if listtype=="secondPath":
				suffixAppend="second"
				path=allthePathsDic.get("secondPath")
		compareBucket=[]
		getitems=[(suffixAppend+":"+each.split("/")[-1]) for each in selected_in_list]
		name_to_save=' '.join(getitems)
		if list_build_function==get_a_play_list[1]:
			prompt="name of list:"
			getcomment=self.makeBody(prompt)
			if getComment==None:
				print "needs name"
				return
			else:
				pass
			getComment=getComment.replace(' ', '_')
			#shotList=suffixAppend+"_"+getComment+"storedText.txt"
			fileBuild=path+shotList
			copyfilemessage="creating in "+fileBuild
			replay = QtGui.QMessageBox.question(None, 'Message' ,copyfilemessage, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
			if reply == QtGui.QMessageBox.Yes:
				if os.path.isfile(fileBuild)==True:
					cmessage="create over "+fileBuild
					replay = QtGui.QMessageBox.question(None, 'Message' ,cmessage, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
					if reply == QtGui.QMessageBox.Yes:
						inp=open(fileBuild, "w+")
						inp.write(name_to_save)
						inp.close()
						print "created "+fileBuild
					else:
						print "cancelled"
						return
				else:
					inp=open(fileBuild, "w+")
					inp.write(name_to_save)
					inp.close()
					print "created "+fileBuild
			else:
				print "cancelled"
				return
		elif list_build_function==get_a_play_list[2]:
			fileDict, list=self.getAllLists(allthePaths)
					
	def getAllLists(self, stuff):
		fileDict={}
		for each in stuff:
			getList, getnamesdic=self.obtain_presets(each)
			getnames=getnamesdic.keys()
			for eachp in eachn in map(None, getList, getnames):
				dictlist={eachn:eachp}
				fileDict.update(dictlist)
		return fileDict, getList
			
	def obtain_presets(self, morestuff):
		preset=False
		format=".txt"
		getpreset=[os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(morestuff) for name in files if name.lower().endswith(format)]
		preset=[(each) for each in getpreset if "storedText" in each]
		getlistnames={}
		for each in preset:
			getName=each.split("/")[-1]
			nam=getName.split("_")
			getpletename='_'.join(nam[:-1])
			diction={getpletename:nam[0]}
			getlistnames.update(diction)
		return preset, getlistnames
		
		
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

	def load(self):
		list_load=self.drop_list_06
		list_load_function=list_load.currentText()
		allthePaths=('//', '//')
		allthePathsDic={"firstPath":'//', "secondPath":'//'}
		if list_load_function==presetlist[0]:
			prompt="name of list:"
			getcomment=self.makeBody(prompt)
			if getComment==None:
				print "needs name"
				return
			else:
				pass
			getComment=getComment.replace(' ', '_')
			shotList=suffixAppend+"_"+getComment+"storedText.txt"
			fileBuild=path+shotList
			copyfilemessage="creating in "+fileBuild
			replay = QtGui.QMessageBox.question(None, 'Message', copyfilemessage, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
			if reply == QtGui.QMessageBox.Yes:
				if os.path.isfile(fileBuild)==True:
					cmessage="create over "+fileBuild
					replay = QtGui.QMessageBox.question(None, 'Message' ,cmessage, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
					if reply == QtGui.QMessageBox.Yes:
						inp=open(fileBuild, "w+")
						inp.write(name_to_save)
						inp.close()
						print "created "+fileBuild
					else:
						print "cancelled"
						return
				else:
					inp=open(fileBuild, "w+")
					inp.write(name_to_save)
					inp.close()
					print "created "+fileBuild
			else:
				print "cancelled"
				return
		elif list_build_function==list_build[2]:
			fileDict, list=self.getAllLists(allthePaths)
			
	def reset_callup(self):
		allthePaths=('//', '//')
		allthePathsDic={"firstPath":'//', "secondPath":'//'}
		getlisttype=self.type_list_drop
		listtype=getlisttype.currentText()
		if listtype=="firstPath":
			directory=allthePathsDic.get("firstPath")
		getUser=getUser
		self.directory_for_taking(getUser, directory)
		
	def directory_for_taking(self, getUser, directory):
		model, countdata, listArray	=self.get_listStuff()
		# self.status_lbl

	def connectButton01(self):
		print "hi"
		self.listCreate()


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
		getPath=selected_in_list[0]+'/'+foldertypeplay+"/"
		get_items=os.listdir(getPath)
		getFileName=get_items[0].split(".")[0]
		print getFileName
		# getFileName=str(getFileName)+"-"+str(typeplay)
		# print getFileName
		format="_jpg"
		# command='msubmitCmd -p "'+str(selected_in_list[0])+getFileName+'.%04d'+formatEXT+'"'+' -s '+str(startFR)+' -e '+str(endFR)+' -t review -n='+comment+' --task techanim -audio '+audioFile+' -audioOffset 0'
		command='msubmitCmd -p "'+str(selected_in_list[0])+'/'+typeplay+format+'/'+getFileName+'.%04d'+formatEXT+'"'+' -s '+str(startFR)+' -e '+str(endFR)+' -t review -n="'+comment+'" --task '+DEPT
		# command="rv "+str(selected_in_list[0])+"/*"
		print "you are running command: "+command
		subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)


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
