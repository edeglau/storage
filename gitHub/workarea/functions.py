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

presetlist=["load"]
typesOfStuffInList=["firstPath", "secondPath"]


messagelist=("hi", "hello", "how's it going?", "bonjour", "g'day")
grab=[(index) for index, each in enumerate(messagelist)]
random.shuffle(grab)
grabText=messagelist[grab[0]]

class classFunctions():

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
		newcol1=self.listWidg.columnWidth(0)
		newcol2=self.listWidg.columnWidth(1)
		newcol3=self.listWidg.columnWidth(2)
		if newcol1==0:
			col1, col1, col1= 240, 160, 500
		else:
			col1, col1, col1= newcol1, newcol2, newcol3
		getPath='//'
		get_items=os.listdir(get_items)
		self.listWidg.clear()
		self.status_lbl.clear()
		self.drop_03.addItems(get_items)
		model, countdata, listArray	=self.get_listStuff()	
		if self.on_drop_01=="item1":
			buildListPath=pathList.get("listpathtype").replace(getUser, newUser)
			self.makeList(listpath, newUser, self.listWidg, model, stat_lab, listtype)
		elif self.on_drop_01=="item2":
			buildListPath=pathList.get("listpathtype2").replace(getUser, newUser)
			self.makeList(listpath, newUser, self.listWidg, model, stat_lab, listtype)
			
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
		self.status_lbl.setText(grabText)
		self.status_lbl.setObjectName('non_plan_label')
		self.status_lbl.setStyleSheet('QLabel#non_plan_label{font-weight: 500; color: orange; background-color: rgba(255,255,255,0);font-size: 9pt}')
	
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
		if list_build_function==list_build[1]:
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
		elif list_build_function==list_build[2]:
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
		
	# def obtain_files(self, stuff):
	# 	preset_name=[]
	# 	if presetis!=False:
	# 		for each in presetis:
	# 			pathsplit=each.split("/")[-1]
	# 			namefind=pathsplit.split("_")[0]
	# 			preset_name.append(namefind)
	# 	else:
	# 		preset_name=False
	# 	return preset_name
		
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
		list_load_function=list_build.currentText()
		allthePaths=('//', '//')
		allthePathsDic={"firstPath":'//', "secondPath":'//'}
		# getlisttype=self.type_list_drop
		# listtype=getlisttype.currentText()
		# if selected_in_list>1:
		# 	getItems=[(each) for each in selected_in_list]
		# 	nameToSave=' '.join(getItems)
		# 	if listtype=="firstPath"
		# 		suffixAppend="first"
		# 		path=allthePathsDic.get("firstPath")
		# 	if listtype=="secondPath"
		# 		suffixAppend="second"
		# 		path=allthePathsDic.get("secondPath")
		# compareBucket=[]
		# getitems=[(suffixAppend+":"+each.split("/")[-1]) for each in selected_in_list]
		# name_to_save=' '.join(getitems)
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
