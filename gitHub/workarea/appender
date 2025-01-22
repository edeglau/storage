import PyQt4
from PyQt4 import QtCore, QtGui, Qt
from PyQt4.QtGui import QWidget, QGridLayout, QLabel, \
	QComboBox, QKeySequence, QPlainTextEdit, QPushButton,QBoxLayout, \
	QClipboard, QCheckBox, QVBoxLayout, QHBoxLayout, \
	QPixmap, QLineEdit, QListWidget, QTextEdit, QSizePolicy, QFrame, QPalette, QColor, \
	QTableWidget, QFont, QAbstractItemView, QMenu, QMessageBox
import os, sys, operator, re, glob, getpass, subprocess, shutil, string, random, ast, webbrowser, time, datetime
from subprocess import Popen, PIPE
from os import stat, listdir, walk
from pwd import getpwuid
import os.path
from os.path import isfile, join
from datetime import datetime




class pllstapp(QGui.QWidget):
	def __init__(self, List, selection):
    	super(pllstapp,self).__init__()
    	self.initUI(List, selection)
    def initUI(self, List, selection):
    	self.layout=QVBoxLayout()
    	self.DirectionsLabel=QLabel('which one do you want?')
    	self.layout.addWidget(self.DirectionsLabel)
    	self.buttonslayout=QBoxLayout(1)
    	self.buttonslayout2=QBoxLayout(0)
    	self.framesingle=QFrame()
    	self.framesingle.setStyleSheet("border-width: 2px; border-color:#ffffff;")
    	self.framesingle.setLayout(self.buttonslayout2)
    	
    	self.a_spinner=QComboBox()
    	self.a_spinner.addItems(List.keys())
    	self.buttonslayout2.addWidget(self.a_spinner)
    	
    	self.singlebtn=QPushButton("<append")
    	self.connect(self.singlebtn, SIGNAL("clicked()"),
    		lambda:self.appendTo(List, selection))
    	self.buttonslayout2.addWidget(self.singlebtn)
    	
    	self.layout.addWidget(self.framesingle)
    	self.layout.addLayout(self.buttonslayout)
    	self.setLayout(self.layout)
    	
    def appendToV1(self, List, selection):
    	getName=self.a_spinner
    	theName=getName.currentText()
    	getPth=str(List.get(str(theName)))
    	mainFunct=ManagerMain()
    	mainFunct.addToFile(getPth, selection)
    	
    def appendTo(self, List, selection):
    	getName=self.a_spinner
    	theName=getName.currentText()
    	getPth=str(List.get(str(theName)))
    	self.addToFile(getPth, selection)
    	
    def addToFile(getPth, selection):
    	message="adding "+getPth+". continue?"
    	reply=QtGui.QMessageBox.question(None, "Message", message, QtGui.QMessageBox.Yes,
    									QtGui.QMessageBox.No)
    	if reply == QtGui.QMessageBox.Yes:
    		inp=open(FileBuild, 'a')
    		inp.write('  ')
    		for selecteditem in fileNamesToSave:
    			inp.write(selecteditem)
    			inp.write('  ')
    		inp.close()
    		print "created"+str(getPth)
    	if reply ==QtGui.MessageBox.No:
    		print "cancelled"
    		return
	
