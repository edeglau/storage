

#!/usr/bin/env python
__author__ = "Elise Deglau"
__ver__ = '1.5'


# standard
import os, sys, operator, re, glob, getpass, subprocess, shutil, string, random, ast, webbrowser, time, datetime
import ast
import os.path
import datetime
from subprocess import Popen, PIPE
from os import stat, listdir, walk
from pwd import getpwuid
from os.path import isfile, join
from functools import partial

# 3rd party
import PyQt4
from PyQt4 import QtCore, QtGui, Qt
from PyQt4.QtGui import QWidget, QRadioButton, QGridLayout, QLabel, \
	QTableWidget, QComboBox, QKeySequence, QToolButton, QPlainTextEdit, QPushButton,QBoxLayout, \
	QClipboard, QTableWidgetItem, QCheckBox, QVBoxLayout, QHBoxLayout, \
	QPixmap, QLineEdit, QListWidget, QTextEdit, QSizePolicy, QFrame, QPalette, QColor, \
	QFont, QAbstractItemView, QMenu, QMessageBox
from PyQt4.QtCore import SIGNAL



M_USER = os.getenv("USER")
get_custom_bookmarks = "/home/"+M_USER+'/'
bkmk_file = M_USER+"_bookmarks.txt"
full_cstmbkrmrk_path = os.path.join(get_custom_bookmarks, bkmk_file)



class createbookmarks(QtGui.QWidget):
	def __init__(self):
		super(createbookmarks, self).__init__()
		self.initUI()

	def initUI(self):
		self.setWindowTitle("Add bookmarks")
		self.layout = QVBoxLayout()
		self.btnlayout = QVBoxLayout()
		self.layout.addLayout(self.btnlayout)      
		self.labelWidget = QLabel("Enter name and URL of bookmark you wanna store")
		self.btnlayout.addWidget(self.labelWidget)
		self.verticalSpacer = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
		self.btnlayout.addItem(self.verticalSpacer)			
		self.listlayout = QHBoxLayout()
		self.btnlayout.addLayout(self.listlayout)      
		self.listnamelayout = QVBoxLayout()
		self.listlayout.addLayout(self.listnamelayout)      
		self.nameWidget = QLineEdit()
		self.listurllayout = QVBoxLayout()
		self.listlayout.addLayout(self.listurllayout)      
		self.urlWidget = QLineEdit()
		self.labelnameWidget = QLabel("Name")
		self.listnamelayout.addWidget(self.labelnameWidget)		
		self.listnamelayout.addWidget(self.nameWidget)
		self.labelURLWidget = QLabel("URL")
		self.listurllayout.addWidget(self.labelURLWidget)				
		self.listurllayout.addWidget(self.urlWidget)
		self.branching_button = QPushButton("Add")
		self.connect(self.branching_button, SIGNAL("clicked()"),
					lambda: self.create_list(self.nameWidget.text(), self.urlWidget.text()))                  
		self.btnlayout.addWidget(self.branching_button)
		self.setLayout(self.layout)
# 
	def openFile(self):
		subprocess.Popen('gio open "%s"' % full_cstmbkrmrk_path, stdout=subprocess.PIPE, shell=True) 

	def create_list(self, name, path):
		name, path = str(name), str(path)
		found_info = False
		try:
			with open(full_cstmbkrmrk_path, 'r') as f:
				s = f.read()
				whip = ast.literal_eval(s)
				if whip:
					found_info = True
		except:
			pass
		if found_info == True:
			inp = open(full_cstmbkrmrk_path, "w + ")
			dilist = "{"
			for key, value in whip.items():
				getstring = '"'+key+'":"'+value+'",\n'
				dilist = str(dilist)+str(getstring)
			getstring = '"'+name+'":"'+path+'",'
			dilist = str(dilist)+str(getstring)
			dilist = str(dilist)+"}"
			inp.write(str(dilist))	
			inp.close()
		else:
			inp = open(full_cstmbkrmrk_path, "w + ")
			dilist = "{"
			getstring = '"'+name+'":"'+path+'",\n'
			dilist = str(dilist)+str(getstring)
			dilist = str(dilist)+"}"
			inp.write(str(dilist))	
			inp.close()








# class openbookmarks(QtGui.QWidget):
class openbookmarks(QtGui.QMainWindow):
	def __init__(self, parent = None):
		super(openbookmarks, self).__init__(parent)
		self.initUI()

	def initUI(self):
		if os.path.isfile(full_cstmbkrmrk_path) == False:
			inp = open(full_cstmbkrmrk_path, 'w+')   
			inp.close()
			print "created " + full_cstmbkrmrk_path	
			nobui=createbookmarks()

			nobui.show()
		else:
			# self.setWindowTitle(winTitle)
			self.setWindowTitle("bookmarks")
			self.central_widget = QWidget(self)
			self.setCentralWidget(self.central_widget)
			self.masterLayout = QGridLayout(self.central_widget)
			self.masterLayout.setAlignment(QtCore.Qt.AlignTop)
		##VERTICAL LAYOUT
			self.vertical_order_layout = QtGui.QBoxLayout(2)
			self.vertical_order_layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignVCenter)
			self.masterLayout.addLayout(self.vertical_order_layout, 0,0,1,1)
						
			self.layout = QVBoxLayout()
			self.masterLayout.addLayout(self.layout, 0,0,1,1)
			self.btnlayout = QVBoxLayout()
			self.layout.addLayout(self.btnlayout)
			# self.setLayout(self.layout)
			self.addakey = QPushButton("Add")
			self.connect(self.addakey, SIGNAL("clicked()"),
						lambda: self.buildPage())			
			self.btnlayout.addWidget(self.addakey) 
			self.opentxt = QPushButton("Open")
			self.connect(self.opentxt, SIGNAL("clicked()"),
						lambda: self.openFile())			
			self.btnlayout.addWidget(self.opentxt) 
			self.verticalSpacer = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
			self.btnlayout.addItem(self.verticalSpacer)			
			self.buttongrp = []
			found_info = False
			try:
				with open(full_cstmbkrmrk_path, 'r') as f:
					s = f.read()
					whip = ast.literal_eval(s)
					found_info = True
			except:
				pass
			if found_info == True:
				for key, value in whip.items():
					self.buttongrp.append(QPushButton(key, self))
					self.buttongrp[-1].clicked.connect(partial(self._button_page, url = value))
					self.btnlayout.addWidget(self.buttongrp[-1])
			else:
				nobui=createbookmarks()
				# nobui.show()
		# self.show()

	def _button_page(self, url):
		subprocess.Popen('gio open "%s"' % url, stdout=subprocess.PIPE, shell=True) 

	def buildPage(self):
		nobui=createbookmarks()
		nobui.show()

	def openFile(self):
		subprocess.Popen('gio open "%s"' % full_cstmbkrmrk_path, stdout=subprocess.PIPE, shell=True) 



inst=openbookmarks()
# inst.show()


