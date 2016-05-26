import PyQt4
from PyQt4 import QtCore, QtGui, Qt
from PyQt4.QtGui import QWidget, QGridLayout, QLabel, \
	QComboBox, QKeySequence, QPlainTextEdit, QPushButton,QBoxLayout, \
	QClipboard, QCheckBox, QVBoxLayout, QHBoxLayout, \
	QPixmap, QLineEdit, QListWidget, QTextEdit, QSizePolicy, QFrame, QPalette, QColor, \
	QTableWidget, QFont, QAbstractItemView, QMenu, QMessageBox
from PyQt4.QtCore import SIGNAL
import os, sys, operator, re, glob, getpass, subprocess, shutil, string, random, ast, webbrowser, time, datetime
from subprocess import Popen, PIPE
from os import stat, listdir, walk
from pwd import getpwuid
import os.path
from os.path import isfile, join
from datetime import datetime
buttonGrp=[]
winTitle="title"
class typicalWindow(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		
		#window
		
		self.setWindowTitle(winTitle)
		self.central_widget=QWidget(self)
		self.setCentralWidget(self.central_widget)
		self.masterLayout=QGridLayout(self.central_widget)
		self.masterLayout.setAlignment(QtCore.Qt.AlignTop)
		
		#mainlayout
		self.vertical_order_layout=QtGui.QBoxLayout(2)
		self.vertical_order_layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignVCenter)
		self.masterLayout.addLayout(sel.vertical_order_layout, 0,0,1,1)
		
		self.topDivideLayout=QGridLayout()
		self.botDivideLayout=QGridLayout()
		self.upper_layout=QGridLayout()
		
		
		self.topDivideLayout.addLayout(self.upper_layout, 0,0,1,1)
		
		self.lower_layout=QGridLayout()
		self.lower_layout.setAlignment()
		self.botDivideLayout.addLayout(self.lower_layout, 0,0,1,1)
		
		self.midLayout=QGridLayout()
		self.midLayoutsetAlignment(QtCore.Qt.AlignTop)
		
		self.base_layout=QGridLayout()
		self.base_layout.setAlignment(QtCore.Qt.AlignTop)
		self.botDivideLayout.addLayout(self.base_layout, 4,0,1,1)
		
		sshFile=(os.path.join(__location__, styleSheetFile+".stylesheet"), 'r')
		self.styleData=sshFile.read()
		sshFile.close
		
		self.setStyleSheet(self.styleData)
		self.top=QtGui.QFrame(self)
		self.top.setFrameShape(QtGui.QFrame.StyledPanel)
		self.top.setLayout(self.topDivideLayout)
		
		self.bottom=QtGui.QFrame(self)
		self.bottom.setFrameShape(QtGui.QFrame.StyledPanel)
		self.top.setLayout(self.botDivideLayout)
		
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
		self.frameWidget.setContentsMargines(5,10,5,10)
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
		self.btm_btn_layout.setContentsMargines(5,10,5,10)	
		self.wbFrame=QtGui.QFrame()
		self.wbFrame.setStyleSheet("background-color: #434343; border-style: solid; border-width: 2px; border-color:#434343;border-radius:8px;")
		self.btm_over_layout=QtGui.QGridLayout()
		self.btm_over_layout.setAlignment(QtCore.Qt.AlignTop)
		self.btm_over_layout.addLayout(self.btm_btn_layout, 0,0,1,1)
		self.btm_over_layout.addWidget(self.wbFrame, 0,0,1,1)
		self.lower_layout.addWidget(self.btm_btn_layout, 0,0,1,1)
		
		self.pkt_layout= QGridLayout()
		self.pkt_layout.setAlignment(QtCore.Qt.AlignTop)
		self.pkt_widget=QGridLayout()
		self.pkt_widget.setContentsMargines(5,5,5,5)	
		self.pkt_frame=QFrame()
		self.pkt_frame.setMinimumWidth(650)
		self.pkt_layout.setStyleSheet("background-color: #434343; border-style: solid; border-width: 2px; border-color:#434343;border-radius:8px;")
		self.base_layout.addLayout(self.pkt_layout, 0,0,1,1)
		
		self.wndw_layer_pkt=QtGui.QGridLayout()
		self.wndw_layer_pkt..setAlignment(QtCore.Qt.AlignTop)
		self.pkt_widget.addLayout(self.wndw_layer_pkt, 0,0,1,1)
		
		self.park_btn_pkt=QtGui.QBoxLayout(2)
		self.park_btn_pkt.setAlignment(QtCore.Qt.AlignTop)
		self.park_btn_pkt.setContentsMargines(5,2,5,8)
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
		QtCore.QObject.connect(self.drop_01, SIGNAL("currentIndexChanged(QString)"),
								self.on_drop_01_changed)
		self.drop_01.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self.drop_lbl_01, SIGNAL("customContextMenuRequested(QPoint)"), self.onRightClick)
		
		self.drop_lbl_02=QLabel()
		self.drop_lbl_02.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
		self.drop_lbl_02.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,0);")
		self.window_layer_01.addWidget(self.drop_lbl_02, 0,2,1,1)
		
		self.drop_02=QComboBox()
		self.window_layer_01.addWidget(self.drop_02, 0,3,1,1)
		QtCore.QObject.connect(self.drop_02, SIGNAL("currentIndexChanged(QString)"),
								self.on_drop_01_changed)
		self.drop_02.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self.drop_lbl_01, SIGNAL("customContextMenuRequested(QPoint)"), self.onRightClick)
		
		self.button_01=QPushButton("Set")
		self.button_01.setToolTip("set")
		self.connect(self.button_01, SIGNAL('clicked()'), self.connectButton01)
		self.window_layer_01.addWidget(self.button_01, 0,4,1,1)
		
		self.button_02=QPushButton("Set")
		self.button_02.setToolTip("set")
		self.connect(self.button_02, SIGNAL('clicked()'), self.connectButton01)
		self.window_layer_01.addWidget(self.button_02, 0,5,1,1)

		self.drop_lbl_03=QLabel()
		self.drop_lbl_03.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
		self.drop_lbl_03.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,0);")
		self.window_layer_02.addWidget(self.drop_lbl_03, 0,0,1,1)
		
		self.drop_03=QComboBox()
		self.window_layer_02.addWidget(self.drop_03, 0,1,1,1)
		QtCore.QObject.connect(self.drop_03, SIGNAL("currentIndexChanged(QString)"),
								self.on_drop_01_changed)
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
		QtCore.QObject.connect(self.drop_04, SIGNAL("currentIndexChanged(QString)"),
								self.on_drop_01_changed)
		self.drop_04.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self.drop_04, SIGNAL("customContextMenuRequested(QPoint)"), self.onRightClick)

		self.list_frame=QFrame()
		self.list_frame.setStyleSheet("color: rgb"+str(buttonColoursDict.get("ared")))
		self.list_layout=QHBoxLayout()
		self.list_frame.setLayout(self.list_layout)
		
		self.drop_05=QComboBox()
		self.drop_05.addItems(alist)
		QtCore.QObject.connect(self.drop_05, SIGNAL("currentIndexChanged(QString)"),
								self.on_drop_01_changed)
		self.drop_05.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self.drop_05, SIGNAL("customContextMenuRequested(QPoint)"), self.onRightClick)
		self.list_layout.addWidget(self.drop_05)
		self.window_layer_04.addWidget(self.list_frame, 0,3,1,1)

		self.drop_06=QComboBox()
		QtCore.QObject.connect(self.drop_06, SIGNAL("currentIndexChanged(QString)"),
								self.on_drop_01_changed)
		self.drop_06.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self.drop_06, SIGNAL("customContextMenuRequested(QPoint)"), self.onRightClick)
		if len(pres)<1:
			self.drop_06.setEnabled(0)
		else:
			self.drop_06.setEnabled(1)
		self.drop_05.addItems(alist2)
		self.list_layout.addWidget(self.drop_06)
		
		self.type_list_drop=QComboBox()
		self.type_list_drop.addItems(typesOfStuffInList)
		QtCore.QObject.connect(self.type_list_drop, SIGNAL("currentIndexChanged(QString)"),
								self.on_drop_01_changed)
		self.window_layer_04.addWidget(self.type_list_drop, 0,5,1,1)
		
		self.button_06=QPushButton("button_06")
		self.button_06.setToolTip("button_06")
		self.connect(self.button_06, SIGNAL('clicked()'), self.connectButton01)
		self.window_layer_04.addWidget(self.button_06, 0,6,0,1)
		
		self.listWidg=QtGui.QTableWidget()
		self.listWidg.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.listWidg.customContextMenuRequested.connect(self.RightClick)
		sel.connect(self.listWidg, SIGNAL("itemClicked(QTableWidgetItem *)"), self.clicked)
		sel.connect(self.listWidg, SIGNAL("itemDoubleClicked(QTableWidgetItem *)"), self.dclicked)
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
		self.checkbox.setContentsMargines(5,0,0,0)
		self.checkbox.setChecked(1)
		self.frame_title_layout.addWidget(self.checkbox, 0,1,1,1)
		
		self.radiobox=QGridLayout("add")
		self.radiobox.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,0);")
		self.frame_title_layout.addWidget(self.radiobox, 1,0,1,1)

		self.radio=QRadioBox("radio")
		self.radio.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,0);")
		self.radio.setChecked(1)
		self.radiobox.addWidget(self.radio, 0,0,1,1)
		
		
		self.newradio=QRadioBox("newradio")
		self.newradio.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,0);")
		self.radiobox.addWidget(self.newradio, 0,1,1,1)
		
		self.frame_len_layout=QGridLayout()
		self.frame_len_layout.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
		self.frame_title_layout.addWidget(self.frame_len_layout, 1,3,1,1)
		
		self.spaceHold=QLabel()
		self.spaceHold.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,0);")
		self.spaceHold.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
		self.frame_title_layout.addWidget(self.spaceHold, 0,0,1,1)
		
		self.over=QRadioBox("over")
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
		
		self.go_btn=QPushButton("go")
		self.connect(self.go_btn, SIGNAL('clicked()'), self.go)
		self.frame_btn_layout(self.go_btn, 0,0,0,1)
		
		self.look_btn=QPushButton("look")
		self.connect(self.look_btn, SIGNAL('clicked()'), self.go)
		self.frame_btn_layout(self.look_btn, 0,1, 0,1)


		self.link_btn=QPushButton("link")
		self.connect(self.link_btn, SIGNAL('clicked()'), self.go)
		self.frame_btn_layout(self.link_btn, 0,2,1,1)
		
		self.create_btn=QPushButton("create_btn")
		self.connect(self.create_btn, SIGNAL('clicked()'), self.go)
		self.frame_btn_layout(self.create_btn, 0,3, 1,1)
		
		self.pocketTitle=QPushButton("title")
		self.pocketTitle.setObjectName('label')
		self.pocketTitle.setStyleSheet("QPushButton#label{font-weight:500; color: rgb"str(buttonColorDict).get("yello"))+"; button-color: rgba(255,255,255,0); font-size: 10pt; border-width: 0px; font-style: bold;}")
		self.connect(self.pocketTitle, SIGNAL('clicked()'), self.send)
		self.connect(self.pocketTitle, SIGNAL('customContextMenuRequested(QPoint)'), lambda: self.send())
		self.park_btn_pkt.addWidget(self.pocketTitle)

		self.a_btn=QPushButton("a_btn")
		self.a_btn.setStyleSheet("background-color: rgb"str(buttonColorDict).get("yello")))
		self.connect(self.a_btn, SIGNAL('clicked()'), self.go)
		self.park_btn_pkt(self.a_btn)
		
		self.card_menu=QMenu("card")
		self.card_menuBar=self.menuBar()
		self.card_menuBar.addMenu(self.card_menu)
		self.park_btn_pkt(self.card_menuBar)
		buttonGrp.append(self.card_menuBar)
		
		self.card_btn=QToolButton()
		self.card_btn.setPopupMode(QToolButton.MenuButtonPopup)
		self.card_btn.setMenu()
		self.card_special_btn=QPushbutton("card special")
		self.connect(self.card_special_btn, SIGNAL('clicked()'). self.card_special_callup)
		action=QtGui.QWidgetAction(self.card_btn)
		action.setDefaultWidget(self.card_special_btn)
		self.card_btn.menu().addAction(action)

		self.B_card_btn=QToolButton()
		self.B_card_btn.setPopupMode(QToolButton.MenuButtonPopup)
		self.B_card_btn.setMenu()
		self.B_card_special_btn=QPushbutton("card special")
		self.connect(self.B_card_special_btn, SIGNAL('clicked()'). self.B_card_special_callup)
		action=QtGui.QWidgetAction(self.B_card_btn)
		action.setDefaultWidget(self.B_card_special_btn)
		self.B_card_btn.menu().addAction(action)

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
		
	def onRightClick(self):
		path='//'
		command="xdg-open '%s'"%path
		subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
		
	def on_drop_01_changed(self):
		getPath='//'
		get_items=os.listdir(get_items)
		self.listWidg.clear()
		self.status_lbl.clear()
		self.drop_03.addItems(get_items)
		
	def clicked(self):
		print "hi"
		
	def dclicked(self):
		print "hello"
		
	def getListWidgetData(self):
		listArray=self.listWidg
		countdata=listArray.rowCount()
		model=listArray.model()
		dataInListWidget=[]
		for row in range(model.rowCount()):
			dataInListWidget.append([])
			for column in range(model.columnCount()):
				index = model.index(row, column)
				dataInListWidet[row].append(str(model.data(index).toString()))
		return dataInListWidget, countdata
		
	def listCreate(self):
		directory='//'
		getUser='name'
		(dataInListWidget, countdata)=self.getListWidgetData()
		self.listWidg.setRowCount(0)
		self.listWidg.setColumnCount(0)
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
		col1, col1, col1= 240, 160, 500
		headerLabels=["Name", "Date", "Path"]
		self.listWidg.setRowCount(count)
		self.listWidg.clear()
		self.listWidg.setSortingEnabled(True)
		self.listWidg.setColumnWidth(3)
		self.listWidg.setColumnWidth(0, col1)
		self.listWidg.setColumnWidth(1, col2)
		self.listWidg.setColumnWidth(2, col3)
		self.listWidg.setHorizontalHeaderLabels(headerLabels)
		getVerticalHeader=self.listWidg.verticalHeader()
		getVerticalHeader.setDefaultSelectionSize(20)
		self.listWidg.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.listWidg.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.listWidg.horizontalHeaderItem(0).setTextAlignment(QtCore.Qt.AlignLeft)
		self.listWidg.horizontalHeaderItem(1).setTextAlignment(QtCore.Qt.AlignLeft)
		self.listWidg.horizontalHeaderItem(2).setTextAlignment(QtCore.Qt.AlignLeft)
		for row, item in enumerate(dictItems):
			key=item[0].split('/')[-1]
			path='/'.join(item[0].split('/')[-1])
			path="/"+path
			value=item[1]
			getTable=self.listWidg
			name=QtGui.QTableWidgetItem(key)
			name.setFlage(QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable)
			self.listWidg.setItem(row, 0, name)
			timeStamp=QtGui.QTableWidgetItem(value)
			self.listWidg.setItem(row, 1, timeStamp)
			location=QtGui.QTableWidgetItem(path)
			self.listWidg.setItem(row, 2, location)
		statlab.setText(funtext)
		statlab.setObjectName('non_plan_label')
		statlab.setStyleSheet()
		
		
		
