
__author__="Elise Deglau"

import sys, os




import PyQt4
from PyQt4 import QtCore, QtGui, Qt
from PyQt4.QtGui import QWidget, QRadioButton, QGridLayout, QLabel, \
    QTableWidget, QComboBox, QKeySequence, QToolButton, QPlainTextEdit, QPushButton,QBoxLayout, \
    QClipboard, QTableWidgetItem, QCheckBox, QVBoxLayout, QHBoxLayout, \
    QPixmap, QLineEdit, QListWidget, QTextEdit, QSizePolicy, QFrame, QPalette, QColor, \
    QFont, QAbstractItemView, QMenu, QMessageBox
from PyQt4.QtCore import SIGNAL

import maya.cmds as mc
import pymel.core as pm

workSpace=mc.workspace(q=1, lfw=1)[-1]
M_USER = os.getenv("USER")
PROJECT=os.getenv("M_JOB")
SCENE=os.getenv("SEQUENCE_SHOT_")
SHOT=os.getenv("M_LEVEL")
DEPT=os.getenv("M_TASK")

class find_Path(QtWidgets.QWidget):
    def __init__(self):
        super(find_Path, self).__init__()
        self.initUI()

    def initUI(self):
        # getPath='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/cache/nCloth/batch/'    
        getPath='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/cache/'    
        if os.path.exists(getPath): 
            pass     
        else:
            print "no caches exist"
            return
        getFiles = [os.path.join(getPath, o) for o in os.listdir(getPath) if os.path.isdir(os.path.join(getPath, o))]
        getFiles.sort(key=lambda x: os.path.getmtime(x))
        getFiles = [(each).split('/')[-1] for each in getFiles]
        # self._choser_group_window(getFiles)             
        self.setWindowTitle("path to caches")
        self.layout = QtWidgets.QVBoxLayout()
        self.btnlayout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.btnlayout)
        self.fieldText = QtWidgets.QLineEdit(getPath)
        self.btnlayout.addWidget(self.fieldText)
        self.playlist = QtWidgets.QComboBox()
        self.btnlayout.addWidget(self.playlist)
        self.playlist.addItems(getFiles)
        self.back_button = QtWidgets.QPushButton("<<")
        self.set_button = QtWidgets.QPushButton(">>")
        self.load_button = QtWidgets.QPushButton("load cache")
        self.load_hair_button = QtWidgets.QPushButton("load hair cache")
        self.load_hair_single_button = QtWidgets.QPushButton("load hair single cache")
        self.load_cloth_button = QtWidgets.QPushButton("load cloth cache")
        self.L_P_button = QtWidgets.QPushButton("load and play")
        self.open_button = QtWidgets.QPushButton("open folder")
        self.connect(self.set_button, SIGNAL('clicked()'), lambda *args:self.set_button_function(make_new_content = self.fieldText.text() ))
        self.connect(self.back_button, SIGNAL('clicked()'), lambda *args:self.back_button_function(make_new_content = self.fieldText.text() ))
        self.connect(self.load_button, SIGNAL('clicked()'), lambda *args:self.load_button_function(self.fieldText.text()))
        self.connect(self.load_hair_button, SIGNAL('clicked()'), lambda *args:self.load_hair_function(self.fieldText.text()))
        self.connect(self.load_hair_single_button, SIGNAL('clicked()'), lambda *args:self.load_hair_single_function(self.fieldText.text()))
        self.connect(self.load_cloth_button, SIGNAL('clicked()'), lambda *args:self.load_cloth_function(self.fieldText.text()))
        self.connect(self.L_P_button, SIGNAL('clicked()'), lambda *args:self.L_P_button_function(self.fieldText.text()))
        self.connect(self.open_button, SIGNAL('clicked()'), lambda *args:self.open_folder_button_function(self.fieldText.text()))
        self.btnlayout.addWidget(self.back_button)
        self.btnlayout.addWidget(self.set_button)
        self.btnlayout.addWidget(self.load_button)
        self.btnlayout.addWidget(self.load_hair_button)
        self.btnlayout.addWidget(self.load_hair_single_button)
        self.btnlayout.addWidget(self.load_cloth_button)
        self.btnlayout.addWidget(self.L_P_button)
        self.btnlayout.addWidget(self.open_button)
        self.setLayout(self.layout)

# class find_Path(QtGui.QWidget):
#     def __init__(self):
#         super(find_Path, self).__init__()
#         self.initUI()

#     def initUI(self):
#         # getPath='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/cache/nCloth/batch/'    
#         getPath='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/cache/'    
#         if os.path.exists(getPath): 
#             pass     
#         else:
#             print "no caches exist"
#             return
#         getFiles = [os.path.join(getPath, o) for o in os.listdir(getPath) if os.path.isdir(os.path.join(getPath, o))]
#         getFiles.sort(key=lambda x: os.path.getmtime(x))
#         getFiles = [(each).split('/')[-1] for each in getFiles]
#         # self._choser_group_window(getFiles)             
#         self.setWindowTitle("path to caches")
#         self.layout = QVBoxLayout()
#         self.btnlayout = QVBoxLayout()
#         self.layout.addLayout(self.btnlayout)
#         self.fieldText=QLineEdit(getPath)
#         self.btnlayout.addWidget(self.fieldText)
#         self.playlist = QComboBox()
#         self.btnlayout.addWidget(self.playlist)
#         self.playlist.addItems(getFiles)
#         self.back_button = QPushButton("<<")
#         self.set_button = QPushButton(">>")
#         self.load_button = QPushButton("load cache")
#         self.load_hair_button = QPushButton("load hair cache")
#         self.load_hair_single_button = QPushButton("load hair single cache")
#         self.load_cloth_button = QPushButton("load cloth cache")
#         self.L_P_button = QPushButton("load and play")
#         self.open_button = QPushButton("open folder")
#         self.connect(self.set_button, SIGNAL('clicked()'), lambda *args:self.set_button_function(make_new_content = self.fieldText.text() ))
#         self.connect(self.back_button, SIGNAL('clicked()'), lambda *args:self.back_button_function(make_new_content = self.fieldText.text() ))
#         self.connect(self.load_button, SIGNAL('clicked()'), lambda *args:self.load_button_function(self.fieldText.text()))
#         self.connect(self.load_hair_button, SIGNAL('clicked()'), lambda *args:self.load_hair_function(self.fieldText.text()))
#         self.connect(self.load_hair_single_button, SIGNAL('clicked()'), lambda *args:self.load_hair_single_function(self.fieldText.text()))
#         self.connect(self.load_cloth_button, SIGNAL('clicked()'), lambda *args:self.load_cloth_function(self.fieldText.text()))
#         self.connect(self.L_P_button, SIGNAL('clicked()'), lambda *args:self.L_P_button_function(self.fieldText.text()))
#         self.connect(self.open_button, SIGNAL('clicked()'), lambda *args:self.open_folder_button_function(self.fieldText.text()))
#         self.btnlayout.addWidget(self.back_button)
#         self.btnlayout.addWidget(self.set_button)
#         self.btnlayout.addWidget(self.load_button)
#         self.btnlayout.addWidget(self.load_hair_button)
#         self.btnlayout.addWidget(self.load_hair_single_button)
#         self.btnlayout.addWidget(self.load_cloth_button)
#         self.btnlayout.addWidget(self.L_P_button)
#         self.btnlayout.addWidget(self.open_button)
#         self.setLayout(self.layout)

    # def gotoAppend(self):
    #     self.close()


    def open_folder_button_function(self, content):
        access_main = cache_functions()
        content=str(content)
        access_main.opening_folder(content)

    def L_P_button_function(self, make_new_content):
        make_new_content = str(make_new_content)
        listed_extension = self.playlist
        listed_folder = listed_extension.currentText()    
        listed_folder = str(listed_folder)
        listed_folder = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(listed_folder) for name in files if name.lower().endswith(".xml")]         
        access_main = cache_functions()
        access_main.load_and_play(make_new_content, listed_folder)

    def load_button_function(self, make_new_content):
        make_new_content = str(make_new_content)
        print make_new_content
        # listed_extension = self.playlist
        # listed_folder = listed_extension.currentText()    
        # listed_folder= str(listed_folder)         
        # print listed_folder
        # xmlfiles = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(listed_folder+'/') for name in files if name.lower().endswith(".xml")]   
        # get_folder_for_jpgs = [(each_file) for each_file in os.walk(get_selected_path) if "xml" in str(each_file)]     
        # print get_folder_for_jpgs   
        # print xmlfiles      
        access_main = cache_functions()
        access_main.load_cache(make_new_content)

    def load_hair_function(self, make_new_content):
        make_new_content = str(make_new_content)
        listed_extension = self.playlist
        listed_folder = listed_extension.currentText()    
        access_main = cache_functions()
        access_main.load_hair_cache(make_new_content, listed_folder)

    def load_hair_single_function(self, make_new_content):
        make_new_content = str(make_new_content)
        listed_extension = self.playlist
        listed_folder = listed_extension.currentText()    
        access_main = cache_functions()
        access_main.load_hair_cache_single(make_new_content, listed_folder)

    def load_cloth_function(self, make_new_content):
        make_new_content = str(make_new_content)
        listed_extension = self.playlist
        listed_folder = listed_extension.currentText()    
        access_main = cache_functions()
        access_main.load_cloth_cache(make_new_content, listed_folder)

    def set_button_function(self, make_new_content):
        make_new_content=str(make_new_content)
        listed_extension = self.playlist
        listed_folder = listed_extension.currentText()    
        listed_folder= str(listed_folder)      
        newgetpath = make_new_content+'/'+listed_folder
        self.fieldText.setText(newgetpath)     
        getFiles = [os.path.join(newgetpath, o) for o in os.listdir(newgetpath) if os.path.isdir(os.path.join(newgetpath, o)) and len(os.listdir(os.path.join(newgetpath, o)))>0]
        # getFiles = [os.path.join(newgetpath, o) for o in os.listdir(newgetpath) if os.path.isdir(os.path.join(newgetpath, o))]
        getFiles.sort(key=lambda x: os.path.getmtime(x))
        getFiles = [(each).split('/')[-1] for each in getFiles]        
        listed_extension.clear()
        listed_extension.addItems(getFiles)        

    def back_button_function(self, make_new_content):
        make_new_content=str(make_new_content)
        get_content_back = "/".join(make_new_content.split('/')[:-1])
        listed_extension = self.playlist
        listed_folder = listed_extension.currentText()    
        listed_folder= str(listed_folder)      
        self.fieldText.setText(get_content_back)     
        getFiles = [os.path.join(get_content_back, o) for o in os.listdir(get_content_back) if os.path.isdir(os.path.join(get_content_back, o))and len(os.listdir(os.path.join(get_content_back, o)))>0]
        getFiles.sort(key=lambda x: os.path.getmtime(x))
        getFiles = [(each).split('/')[-1] for each in getFiles]        
        self.playlist.clear()
        self.playlist.addItems(getFiles)  


class cache_functions(object):

    def opening_folder(self, folderPath):
        # newfolderPath=re.sub(r'\\',r'/', folderPath)
        os.system('xdg-open "%s"' % folderPath)

    def load_cache(self, listed_folder):
        if len(mc.ls(sl=1))<1:
            getSel = [(each) for each in mc.ls(type = "nCloth") if "Orig" not in each]
        else:
            getSel = mc.ls(sl=1)
        # filepath = make_new_content+"/"+listed_folder
        # filexml = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(filepath) for name in files if name.lower().endswith(".xml")][0]
        # getSel=mc.ls(sl=1)  
             
        # if len(getSel)>0:
        for each in getSel:
            getMesh = [(item) for clothitem in mc.ls(getSel) for item in mc.listHistory(clothitem) if mc.nodeType(item) == "mesh" if "Orig" not in item][0]
            # mc.select(each)
            findName = each.replace(":", "_")
            newName = findName+'.xml'
            filexml = listed_folder+'/'+newName
            pm.mel.doImportCacheFile(filexml, '', each, getMesh) 

    def checkCacheFile(self, interrogateName):
        cachefolderStart=getCachePath
        number = 0000
        getScene = mc.file(q=1, sn=1, shn=1)
        getFilename =  getScene.split(".")[:-1]
        getFilename ='_'.join(getFilename)+"_"+str(getUser)+"_nCache"
        getnewcachefolder = getFilename+"_"+str("%04d" % (number,))
        makecachefolder = cachefolderStart+"/"+getnewcachefolder
        if os.path.exists(makecachefolder): 
            get_vr_folders = [(dirnames) for dirpath, dirnames, files in os.walk(cachefolderStart)][0]
            get_vr_folders = [(each) for each in get_vr_folders if each.split("_")[-1].isdigit()]
            get_top = max(get_vr_folders)
            number = get_top.split("_")[-1]
            if "v" not in number:
                number = int(number)
            else:
                number = re.sub("\D", "", number)
            number = int(number)
            number +=1
            getnewcachefolder=getFilename+"_"+str("%04d" % (number,))
            makecachefolder = cachefolderStart+"/"+getnewcachefolder
            os.makedirs(makecachefolder)
            print "created "+makecachefolder
        if not os.path.exists(makecachefolder): 
            os.makedirs(makecachefolder) 
            print "created "+makecachefolder
        print getFilename, makecachefolder
        return getFilename, makecachefolder

    def load_cloth_cache(self, make_new_content, listed_folder):
        filepath = make_new_content+"/"+listed_folder+"/"
        grabsystem=mc.ls(type="nCloth")
        mc.select(grabsystem, r=1)       
        getLowRange=mc.playbackOptions(q=1, ast=1)
        getHiRange=mc.playbackOptions(q=1, aet=1)
        if len(mc.ls(sl=1))<1:
            getHairSel = [(each) for each in mc.ls(type = "nCloth") if "Orig" not in each]
        else:
            getHairSel = mc.ls(sl=1)        
        createdict = [(name) for dirpath, dirnames, files in os.walk(str(filepath)) for name in files if name.lower().endswith(".xml")]
        # createdict = [(name) for dirpath, dirnames, files in os.walk(str(filepath)) for name in files if name.lower().endswith(".mcx")]
        filecloth = [(name) for dirpath, dirnames, files in os.walk(str(filepath)) for name.split(".")[-1] in files]
        getSel=mc.ls(sl=1)
        if len(getHairSel)>0:
            for value in createdict:
                for hairbit in getHairSel:   
                    grab_filename_match = hairbit.replace(':', '_')   
                    if "Frame" in value:
                        presetName = value.split("Frame")[0]
                    else:
                        presetName = value.split(".")[0]
                    filexml=str(filepath)+value
                    if grab_filename_match == presetName:
                        getCache=[(nodes) for nodes in mc.listHistory(hairbit) if mc.nodeType(nodes) == "cacheBlend"]
                        if len(getCache)>0:
                            mc.delete(getCache)
                            print "deleted: " + str(getCache)
                        getCache=[(nodes) for nodes in mc.listHistory(hairbit) if mc.nodeType(nodes) == "cacheFile"]
                        if len(getCache)>0:
                            mc.delete(getCache)   
                            print "deleted: " + str(getCache)
                        presetName = value.split(".")[0]
                        cache_path = filepath.replace('//', '/')
                        cache_name = presetName
                        shape = hairbit      
                        createdCacheFileNode = mc.createNode("cacheFile", n=presetName+"Cache1")
                        print "created cachefile "+presetName+"Cache1"
                        mc.setAttr(createdCacheFileNode+".cachePath", filepath, type = "string")
                        print "set attr: "+createdCacheFileNode+".cachePath to "+filepath
                        mc.setAttr(createdCacheFileNode+".cacheName", presetName, type = "string")
                        print "set attr: "+createdCacheFileNode+".cacheName to "+presetName
                        mc.setAttr(createdCacheFileNode+".startFrame", getLowRange)
                        print "set attr: "+createdCacheFileNode+".startFrame to "+str(getLowRange)
                        mc.setAttr(createdCacheFileNode+".originalStart", getLowRange)
                        print "set attr: "+createdCacheFileNode+".originalStart to "+str(getLowRange)
                        mc.setAttr(createdCacheFileNode+".sourceStart", getLowRange)
                        print "set attr: "+createdCacheFileNode+".sourceStart to "+str(getLowRange)
                        mc.setAttr(createdCacheFileNode+".originalEnd", getHiRange)
                        print "set attr: "+createdCacheFileNode+".originalEnd to "+str(getHiRange)
                        mc.setAttr(createdCacheFileNode+".sourceEnd", getHiRange)
                        print "set attr: "+createdCacheFileNode+".sourceEnd to "+str(getHiRange)
                        mc.setAttr(createdCacheFileNode+".inRange", 1)
                        print "set attr: "+createdCacheFileNode+".inRange to 1"
                        mc.connectAttr(createdCacheFileNode+".inRange", hairbit+".playFromCache", f=1)
                        print "connected attr: "+createdCacheFileNode+".inRange to "+hairbit+".playFromCache"
                        mc.connectAttr(createdCacheFileNode+".outCacheData[0]", hairbit+".positions", f=1)           
                        print "connected attr: "+createdCacheFileNode+".outCacheData[0] to "+hairbit+".positions"
                        mc.connectAttr("time1.outTime", createdCacheFileNode+".time", f=1)   
                        print "connected attr: time1.outTime to "+createdCacheFileNode+".time"          


    def load_cloth_cacheV1(self, make_new_content, listed_folder):
        #startnaming
        filepath = make_new_content+"/"+listed_folder+"/"
        print "got here"
        grabsystem=mc.ls(type="nCloth")
        mc.select(grabsystem, r=1)       
        if ":" in grabsystem[0]:
            interroName = grabsystem[0].split(":")[-1]+"_"
        else:
            interroName=interroName+"_"
        # newName, cachFolder=self.checkCacheFile(interroName, filepath) 
        #endnaming
        getLowRange=mc.playbackOptions(q=1, ast=1)
        print getLowRange
        getHiRange=mc.playbackOptions(q=1, aet=1)
        print getHiRange
        if len(mc.ls(sl=1))<1:
            getHairSel = [(each) for each in mc.ls(type = "nCloth") if "Orig" not in each]
        else:
            getHairSel = mc.ls(sl=1)        
        createdict = [(name) for dirpath, dirnames, files in os.walk(str(filepath)) for name in files if name.lower().endswith(".mcx")]
        filecloth = [(name) for dirpath, dirnames, files in os.walk(str(filepath)) for name.split(".")[-1] in files]
        getSel=mc.ls(sl=1)
        if len(getHairSel)>0:
            for value in createdict:
                for hairbit in getHairSel:               
                    filexml=str(filepath)+value
                    grabName = hairbit.split(":")[-1]
                    if grabName in value:
                        getCache=[(nodes) for nodes in mc.listHistory(hairbit) if mc.nodeType(nodes) == "cacheBlend"]
                        if len(getCache)>0:
                            mc.delete(getCache)
                            print "deleted: " + getCache
                        getCache=[(nodes) for nodes in mc.listHistory(hairbit) if mc.nodeType(nodes) == "cacheFile"]
                        if len(getCache)>0:
                            mc.delete(getCache) 
                            print "deleted: " + getCache
                        presetName = value.split(".")[0]
                        cache_path = filepath
                        cache_name = presetName
                        shape = hairbit
                        createdCacheFileNode = mc.createNode("cacheFile", n=presetName+"Cache1")
                        mc.setAttr(createdCacheFileNode+".cachePath", filepath, type = "string")
                        mc.setAttr(createdCacheFileNode+".cacheName", presetName, type = "string")
                        mc.setAttr(createdCacheFileNode+".startFrame", getLowRange)
                        mc.setAttr(createdCacheFileNode+".originalStart", getLowRange)
                        mc.setAttr(createdCacheFileNode+".sourceStart", getLowRange)
                        mc.setAttr(createdCacheFileNode+".originalEnd", getHiRange)
                        mc.setAttr(createdCacheFileNode+".sourceEnd", getHiRange)
                        mc.setAttr(createdCacheFileNode+".inRange", 1)
                        mc.connectAttr(createdCacheFileNode+".inRange", hairbit+".playFromCache", f=1)
                        # mc.connectAttr(createdCacheFileNode+".outCacheData[0]", hairbit+".hairCounts", f=1)
                        # mc.connectAttr(createdCacheFileNode+".outCacheData[1]", hairbit+".vertexCounts", f=1)
                        mc.connectAttr(createdCacheFileNode+".outCacheData[0]", hairbit+".positions", f=1)
                        mc.connectAttr("time1.outTime", createdCacheFileNode+".time", f=1)    
                        # mc.connectAttr(createdCacheFileNode+".outCacheData[0]", createdCacheBlendNode+".vectorArray[1]", f=1)    

    def chunks(self, list, n):
        for i in range(0, len(list), n):
            yield list[i:i+n]

    def load_hair_cache_single(self, make_new_content, listed_folder):
        getname = listed_folder.split("/")[-1]
        getLowRange=mc.playbackOptions(q=1, ast=1)
        getHiRange=mc.playbackOptions(q=1, aet=1)
        if len(mc.ls(sl=1))<1:
            getHairSel = [(each) for each in mc.ls(type = "hairSystem") if "Orig" not in each]
        else:
            getHairSel = mc.ls(sl=1)    
        filepath = make_new_content+"/"+listed_folder+"/"
        createdict = [(name) for dirpath, dirnames, files in os.walk(str(filepath)) for name in files if name.lower().endswith(".xml")]
        filecloth = [(name) for dirpath, dirnames, files in os.walk(str(filepath)) for name.split(".")[-1] in files]
        getSel=mc.ls(sl=1)
        getLowRange = str(getLowRange)
        getHiRange = str(getHiRange)
        if len(getHairSel)>0:
            getFull_len=range(0, len(getHairSel)*3)
            getList = list(self.chunks(getFull_len, 3))
            for value in createdict:
                presetName = value.split(".")[0]
                cache_name = presetName
                createdCacheFileNode = mc.createNode("cacheFile", n=presetName+"Cache1")
                print "created cachefile "+presetName+"Cache1"
                mc.setAttr(createdCacheFileNode+".cachePath", filepath, type = "string")
                print "set attr: "+createdCacheFileNode+".cachePath to "+filepath
                mc.setAttr(createdCacheFileNode+".cacheName", presetName, type = "string")
                print "set attr: "+createdCacheFileNode+".cacheName to "+presetName
                mc.setAttr(createdCacheFileNode+".startFrame", getLowRange)
                print "set attr: "+createdCacheFileNode+".startFrame to "+getLowRange
                mc.setAttr(createdCacheFileNode+".originalStart", getLowRange)
                print "set attr: "+createdCacheFileNode+".originalStart to "+getLowRange
                mc.setAttr(createdCacheFileNode+".sourceStart", getLowRange)
                print "set attr: "+createdCacheFileNode+".sourceStart to "+getLowRange
                mc.setAttr(createdCacheFileNode+".originalEnd", getHiRange)
                print "set attr: "+createdCacheFileNode+".originalEnd to "+getHiRange
                mc.setAttr(createdCacheFileNode+".sourceEnd", getHiRange)
                print "set attr: "+createdCacheFileNode+".sourceEnd to "+getHiRange
                mc.setAttr(createdCacheFileNode+".inRange", 1)
                print "set attr: "+createdCacheFileNode+".inRange to 1"
                mc.connectAttr("time1.outTime", createdCacheFileNode+".time", f=1)           
                print "connected attr: time1.outTime to "+createdCacheFileNode+".time"
                for each_bit, hairbit in map(None, getList, getHairSel):    
                    grab_filename_match = getname   
                    filexml=str(filepath)+value
                    getCache=[(nodes) for nodes in mc.listHistory(hairbit) if mc.nodeType(nodes) == "cacheBlend"]
                    if len(getCache)>0:
                        mc.delete(getCache)
                    getCache=[(nodes) for nodes in mc.listHistory(hairbit) if mc.nodeType(nodes) == "cacheFile"]
                    if len(getCache)>0:
                        mc.delete(getCache)  
                    cache_path = filepath
                    shape = hairbit
                    mc.connectAttr(createdCacheFileNode+".inRange", hairbit+".playFromCache", f=1)
                    print "connected attr: "+createdCacheFileNode+".inRange to "+hairbit+".playFromCache"
                    mc.connectAttr(createdCacheFileNode+".outCacheData[%d]" %(each_bit[0], ), hairbit+".hairCounts", f=1)
                    print "connected attr: "+createdCacheFileNode+".outCacheData[0] to "+hairbit+".hairCounts"
                    mc.connectAttr(createdCacheFileNode+".outCacheData[%d]" %(each_bit[1], ), hairbit+".vertexCounts", f=1)
                    print "connected attr: "+createdCacheFileNode+".outCacheData[1] to "+hairbit+".vertexCounts"
                    mc.connectAttr(createdCacheFileNode+".outCacheData[%d]" %(each_bit[2], ), hairbit+".positions", f=1)  
                    print "connected attr: "+createdCacheFileNode+".outCacheData[2] to "+hairbit+".positions"
                    # mc.connectAttr(createdCacheFileNode+".outCacheData[0]", createdCacheBlendNode+".vectorArray[1]", f=1)             


    def load_hair_cache(self, make_new_content, listed_folder):
        getLowRange=mc.playbackOptions(q=1, ast=1)
        getHiRange=mc.playbackOptions(q=1, aet=1)
        if len(mc.ls(sl=1))<1:
            getHairSel = [(each) for each in mc.ls(type = "hairSystem") if "Orig" not in each]
        else:
            getHairSel = mc.ls(sl=1)    
        print getHairSel    
        filepath = make_new_content+"/"+listed_folder+"/"
        print filepath
        createdict = [(name) for dirpath, dirnames, files in os.walk(str(filepath)) for name in files if name.lower().endswith(".xml")]
        filecloth = [(name) for dirpath, dirnames, files in os.walk(str(filepath)) for name.split(".")[-1] in files]
        getSel=mc.ls(sl=1)
        print createdict
        if len(getHairSel)>0:
            for value in createdict:
                for hairbit in getHairSel:    
                    grab_filename_match = hairbit.replace(':', '_')   
                    presetName = value.split(".")[0]
                    filexml=str(filepath)+value
                    if grab_filename_match == presetName:
                        getCache=[(nodes) for nodes in mc.listHistory(hairbit) if mc.nodeType(nodes) == "cacheBlend"]
                        if len(getCache)>0:
                            mc.delete(getCache)
                        getCache=[(nodes) for nodes in mc.listHistory(hairbit) if mc.nodeType(nodes) == "cacheFile"]
                        if len(getCache)>0:
                            mc.delete(getCache)  
                        presetName = value.split(".")[0]
                        cache_path = filepath
                        cache_name = presetName
                        shape = hairbit
                        getLowRange = str(getLowRange)
                        getHiRange = str(getHiRange)
                        createdCacheFileNode = mc.createNode("cacheFile", n=presetName+"Cache1")
                        print "created cachefile "+presetName+"Cache1"
                        mc.setAttr(createdCacheFileNode+".cachePath", filepath, type = "string")
                        print "set attr: "+createdCacheFileNode+".cachePath to "+filepath
                        mc.setAttr(createdCacheFileNode+".cacheName", presetName, type = "string")
                        print "set attr: "+createdCacheFileNode+".cacheName to "+presetName
                        mc.setAttr(createdCacheFileNode+".startFrame", getLowRange)
                        print "set attr: "+createdCacheFileNode+".startFrame to "+getLowRange
                        mc.setAttr(createdCacheFileNode+".originalStart", getLowRange)
                        print "set attr: "+createdCacheFileNode+".originalStart to "+getLowRange
                        mc.setAttr(createdCacheFileNode+".sourceStart", getLowRange)
                        print "set attr: "+createdCacheFileNode+".sourceStart to "+getLowRange
                        mc.setAttr(createdCacheFileNode+".originalEnd", getHiRange)
                        print "set attr: "+createdCacheFileNode+".originalEnd to "+getHiRange
                        mc.setAttr(createdCacheFileNode+".sourceEnd", getHiRange)
                        print "set attr: "+createdCacheFileNode+".sourceEnd to "+getHiRange
                        mc.setAttr(createdCacheFileNode+".inRange", 1)
                        print "set attr: "+createdCacheFileNode+".inRange to 1"
                        mc.connectAttr(createdCacheFileNode+".inRange", hairbit+".playFromCache", f=1)
                        print "connected attr: "+createdCacheFileNode+".inRange to "+hairbit+".playFromCache"
                        mc.connectAttr(createdCacheFileNode+".outCacheData[0]", hairbit+".hairCounts", f=1)
                        print "connected attr: "+createdCacheFileNode+".outCacheData[0] to "+hairbit+".hairCounts"
                        mc.connectAttr(createdCacheFileNode+".outCacheData[1]", hairbit+".vertexCounts", f=1)
                        print "connected attr: "+createdCacheFileNode+".outCacheData[1] to "+hairbit+".vertexCounts"
                        mc.connectAttr(createdCacheFileNode+".outCacheData[2]", hairbit+".positions", f=1)  
                        print "connected attr: "+createdCacheFileNode+".outCacheData[2] to "+hairbit+".positions"
                        mc.connectAttr("time1.outTime", createdCacheFileNode+".time", f=1)           
                        print "connected attr: time1.outTime to "+createdCacheFileNode+".time"
                        # mc.connectAttr(createdCacheFileNode+".outCacheData[0]", createdCacheBlendNode+".vectorArray[1]", f=1)             
        else:
            for value in createdict:
                for hairbit in getHairSel:
                    filexml=str(filepath)+value
                    grabName = hairbit.split(":")[-1]
                    if grabName in value:
                        getCache=[(nodes) for nodes in mc.listHistory(hairbit) if mc.nodeType(nodes) == "cacheBlend"]
                        if len(getCache)>0:
                            mc.delete(getCache)
                        getCache=[(nodes) for nodes in mc.listHistory(hairbit) if mc.nodeType(nodes) == "cacheFile"]
                        if len(getCache)>0:
                            mc.delete(getCache)   
                        presetName = value.split(".")[0]
                        cache_path = filepath
                        cache_name = presetName
                        shape = hairbit
                        createdCacheFileNode = mc.createNode("cacheFile", n=presetName+"Cache1")
                        print "created cachefile "+presetName+"Cache1"
                        mc.setAttr(createdCacheFileNode+".cachePath", filepath, type = "string")
                        print "set attr: "+createdCacheFileNode+".cachePath to "+filepath
                        mc.setAttr(createdCacheFileNode+".cacheName", presetName, type = "string")
                        print "set attr: "+createdCacheFileNode+".cacheName to "+presetName
                        mc.setAttr(createdCacheFileNode+".startFrame", getLowRange)
                        print "set attr: "+createdCacheFileNode+".startFrame to "+getLowRange
                        mc.setAttr(createdCacheFileNode+".originalStart", getLowRange)
                        print "set attr: "+createdCacheFileNode+".originalStart to "+getLowRange
                        mc.setAttr(createdCacheFileNode+".sourceStart", getLowRange)
                        print "set attr: "+createdCacheFileNode+".sourceStart to "+getLowRange
                        mc.setAttr(createdCacheFileNode+".originalEnd", getHiRange)
                        print "set attr: "+createdCacheFileNode+".originalEnd to "+getHiRange
                        mc.setAttr(createdCacheFileNode+".sourceEnd", getHiRange)
                        print "set attr: "+createdCacheFileNode+".sourceEnd to "+getHiRange
                        mc.connectAttr(createdCacheFileNode+".inRange", hairbit+".playFromCache", f=1)
                        print "connected attr: "+createdCacheFileNode+".inRange to "+hairbit+".playFromCache"
                        mc.connectAttr(createdCacheFileNode+".outCacheData[0]", hairbit+".hairCounts", f=1)
                        print "connected attr: "+createdCacheFileNode+".outCacheData[0] to "+hairbit+".hairCounts"
                        mc.connectAttr(createdCacheFileNode+".outCacheData[1]", hairbit+".vertexCounts", f=1)
                        print "connected attr: "+createdCacheFileNode+".outCacheData[1] to "+hairbit+".vertexCounts"
                        mc.connectAttr(createdCacheFileNode+".outCacheData[2]", hairbit+".positions", f=1)
                        print "connected attr: "+createdCacheFileNode+".outCacheData[2] to "+hairbit+".positions"
                        mc.connectAttr("time1.outTime", createdCacheFileNode+".time", f=1)  
                        print "connected attr: time1.outTime to "+createdCacheFileNode+".time"


    def load_hair_cacheV1(self, listed_folder):
        if len(mc.ls(sl=1))<1:
            getSel = [(each) for each in mc.ls(type = "hairSystem") if "Orig" not in each]
        else:
            getSel = mc.ls(sl=1)
        for each in getSel:
            getCache = [(nodes) for nodes in mc.listHistory(each) if mc.nodeType(nodes) == "cacheBlend"]
            if len(getCache)>0:
                mc.delete(getCache)
            getCache = [(nodes) for nodes in mc.listHistory(each) if mc.nodeType(nodes) == "cacheFile"]
            if len(getCache)>0:
                mc.delete(getCache)           
            findName = each.replace(":", "_")
            newName = findName+'.xml'
            print newName
            filexml = listed_folder+'/'+newName
            print filexml
            pm.mel.doImportCacheFile(filexml, '', findName, each) 


    def load_cacheV1(self, make_new_content, listed_folder):
        filepath = make_new_content+"/"+listed_folder
        createdict = [{os.path.join(dirpath, name): name} for dirpath, dirnames, files in os.walk(filepath) for name in files if name.lower().endswith(".xml")]
        filecloth = [(name) for dirpath, dirnames, files in os.walk(filepath) for name in files if name.lower().endswith(".nCloth")]
        print createdict
        print filecloth
  
        getSel=mc.ls(sl=1)
        if len(getSel)>0:
            for selobj in getSel:
                for key, value in createdict.items():
                    getobjname=value[0].split('.')[0]
                    # print getobjname
                    if getobjname == str(selobj):
                        getShape=[(nodes) for nodes in mc.listHistory(selobj) if mc.nodeType(nodes) == "historySwitch"]
                        if len(getShape)>0:
                            maya.mel.eval('deleteCacheFile 2 { "keep", "" } ;')
                        getCommand='createHistorySwitch("%s",false)' %selobj
                        switch = maya.mel.eval(getCommand)
                        cacheNode = mc.cacheFile(f=key, ia='%s.inp[0]' % switch ,attachFile=True)
                        mc.setAttr( '%s.playFromCache' % switch, 1 )                
        else:
            for key, value in createdict.items():
                if filecloth in value:
                    getObj = mc.ls(filecloth)[0]
                    getShape=[(nodes) for nodes in mc.listHistory(getObj) if mc.nodeType(nodes) == "historySwitch"]
                    if len(getShape)>0:
                        maya.mel.eval('deleteCacheFile 2 { "keep", "" } ;')
                    getCommand='createHistorySwitch("%s",false)' %getObj
                    switch = maya.mel.eval(getCommand)
                    cacheNode = mc.cacheFile(f=filexml, ia='%s.inp[0]' % switch ,attachFile=True)
                    mc.setAttr( '%s.playFromCache' % switch, 1 )                
            
    def load_and_play(self, make_new_content, listed_folder):
        filepath = make_new_content+"/"+listed_folder
        filexml = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(filepath) for name in files if name.lower().endswith(".xml")][0]
        getSel = mc.ls(sl=1)
        if len(getSel)>0:
            for each in getSel:
                getShape=[(nodes) for nodes in mc.listHistory(each) if mc.nodeType(nodes) == "historySwitch"]
                #getShape=mc.listRelatives(each, ad=1, type="historySwitch")
                if len(getShape)>0:
                    maya.mel.eval('deleteCacheFile 2 { "keep", "" } ;')
                getCommand='createHistorySwitch("%s",false)' %each
                switch = maya.mel.eval(getCommand)
                cacheNode = mc.cacheFile(f=filexml, ia='%s.inp[0]' % switch ,attachFile=True)
                mc.setAttr( '%s.playFromCache' % switch, 1 )
            mc.select(clear=1)
            filepath = "_".join(filepath.split("."))
            filename = filepath.split('/')[-1]
            filepathname = filepath+'/'+filename
            print filepathname
            if not os.path.exists(filepath): os.makedirs(filepath)
            mc.playblast(clearCache=1, endTime=mc.playbackOptions(max=1, aet=1, q=1), filename=filepathname, format="image", offScreen=1, percent=100, quality=100, sequenceTime=0, showOrnaments = 1, startTime=mc.playbackOptions(min=1, ast=1, q=1), viewer=0, widthHeight=[2156, 1212])
            time.sleep(1.3)
            command = "rv "+ filepath
            subprocess.Popen(command, stdout = subprocess.PIPE, shell = True)
        else:
            print "select something"

inst=find_Path()
inst.show()            __author__="Elise Deglau"

import sys, os

import mrig_pyqt
from mrig_pyqt import QtCore, QtGui, QtWidgets
from mrig_pyqt.QtCore import SIGNAL


# import mrig_pyqt
# from mrig_pyqt import QtCore, QtGui
# from mrig_pyqt.QtGui import QWidget, QRadioButton, QGridLayout, QLabel, \
#     QTableWidget, QComboBox, QKeySequence, QToolButton, QPlainTextEdit, QPushButton,QBoxLayout, \
#     QClipboard, QTableWidgetItem, QCheckBox, QVBoxLayout, QHBoxLayout, \
#     QPixmap, QLineEdit, QListWidget, QTextEdit, QSizePolicy, QFrame, QPalette, QColor, \
#     QFont, QAbstractItemView, QMenu, QMessageBox
# from mrig_pyqt.QtCore import SIGNAL

import maya.cmds as mc
import pymel.core as pm

workSpace=mc.workspace(q=1, lfw=1)[-1]
M_USER = os.getenv("USER")
PROJECT=os.getenv("M_JOB")
SCENE=os.getenv("SEQUENCE_SHOT_")
SHOT=os.getenv("M_LEVEL")
DEPT=os.getenv("M_TASK")

class find_Path(QtWidgets.QWidget):
    def __init__(self):
        super(find_Path, self).__init__()
        self.initUI()

    def initUI(self):
        # getPath='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/cache/nCloth/batch/'    
        getPath='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/cache/'    
        if os.path.exists(getPath): 
            pass     
        else:
            print "no caches exist"
            return
        getFiles = [os.path.join(getPath, o) for o in os.listdir(getPath) if os.path.isdir(os.path.join(getPath, o))]
        getFiles.sort(key=lambda x: os.path.getmtime(x))
        getFiles = [(each).split('/')[-1] for each in getFiles]
        # self._choser_group_window(getFiles)             
        self.setWindowTitle("path to caches")
        self.layout = QtWidgets.QVBoxLayout()
        self.btnlayout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.btnlayout)
        self.fieldText = QtWidgets.QLineEdit(getPath)
        self.btnlayout.addWidget(self.fieldText)
        self.playlist = QtWidgets.QComboBox()
        self.btnlayout.addWidget(self.playlist)
        self.playlist.addItems(getFiles)
        self.back_button = QtWidgets.QPushButton("<<")
        self.set_button = QtWidgets.QPushButton(">>")
        self.load_button = QtWidgets.QPushButton("load cache")
        self.load_hair_button = QtWidgets.QPushButton("load hair cache")
        self.load_hair_single_button = QtWidgets.QPushButton("load hair single cache")
        self.load_cloth_button = QtWidgets.QPushButton("load cloth cache")
        self.L_P_button = QtWidgets.QPushButton("load and play")
        self.open_button = QtWidgets.QPushButton("open folder")
        self.connect(self.set_button, SIGNAL('clicked()'), lambda *args:self.set_button_function(make_new_content = self.fieldText.text() ))
        self.connect(self.back_button, SIGNAL('clicked()'), lambda *args:self.back_button_function(make_new_content = self.fieldText.text() ))
        self.connect(self.load_button, SIGNAL('clicked()'), lambda *args:self.load_button_function(self.fieldText.text()))
        self.connect(self.load_hair_button, SIGNAL('clicked()'), lambda *args:self.load_hair_function(self.fieldText.text()))
        self.connect(self.load_hair_single_button, SIGNAL('clicked()'), lambda *args:self.load_hair_single_function(self.fieldText.text()))
        self.connect(self.load_cloth_button, SIGNAL('clicked()'), lambda *args:self.load_cloth_function(self.fieldText.text()))
        self.connect(self.L_P_button, SIGNAL('clicked()'), lambda *args:self.L_P_button_function(self.fieldText.text()))
        self.connect(self.open_button, SIGNAL('clicked()'), lambda *args:self.open_folder_button_function(self.fieldText.text()))
        self.btnlayout.addWidget(self.back_button)
        self.btnlayout.addWidget(self.set_button)
        self.btnlayout.addWidget(self.load_button)
        self.btnlayout.addWidget(self.load_hair_button)
        self.btnlayout.addWidget(self.load_hair_single_button)
        self.btnlayout.addWidget(self.load_cloth_button)
        self.btnlayout.addWidget(self.L_P_button)
        self.btnlayout.addWidget(self.open_button)
        self.setLayout(self.layout)

# class find_Path(QtGui.QWidget):
#     def __init__(self):
#         super(find_Path, self).__init__()
#         self.initUI()

#     def initUI(self):
#         # getPath='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/cache/nCloth/batch/'    
#         getPath='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/cache/'    
#         if os.path.exists(getPath): 
#             pass     
#         else:
#             print "no caches exist"
#             return
#         getFiles = [os.path.join(getPath, o) for o in os.listdir(getPath) if os.path.isdir(os.path.join(getPath, o))]
#         getFiles.sort(key=lambda x: os.path.getmtime(x))
#         getFiles = [(each).split('/')[-1] for each in getFiles]
#         # self._choser_group_window(getFiles)             
#         self.setWindowTitle("path to caches")
#         self.layout = QVBoxLayout()
#         self.btnlayout = QVBoxLayout()
#         self.layout.addLayout(self.btnlayout)
#         self.fieldText=QLineEdit(getPath)
#         self.btnlayout.addWidget(self.fieldText)
#         self.playlist = QComboBox()
#         self.btnlayout.addWidget(self.playlist)
#         self.playlist.addItems(getFiles)
#         self.back_button = QPushButton("<<")
#         self.set_button = QPushButton(">>")
#         self.load_button = QPushButton("load cache")
#         self.load_hair_button = QPushButton("load hair cache")
#         self.load_hair_single_button = QPushButton("load hair single cache")
#         self.load_cloth_button = QPushButton("load cloth cache")
#         self.L_P_button = QPushButton("load and play")
#         self.open_button = QPushButton("open folder")
#         self.connect(self.set_button, SIGNAL('clicked()'), lambda *args:self.set_button_function(make_new_content = self.fieldText.text() ))
#         self.connect(self.back_button, SIGNAL('clicked()'), lambda *args:self.back_button_function(make_new_content = self.fieldText.text() ))
#         self.connect(self.load_button, SIGNAL('clicked()'), lambda *args:self.load_button_function(self.fieldText.text()))
#         self.connect(self.load_hair_button, SIGNAL('clicked()'), lambda *args:self.load_hair_function(self.fieldText.text()))
#         self.connect(self.load_hair_single_button, SIGNAL('clicked()'), lambda *args:self.load_hair_single_function(self.fieldText.text()))
#         self.connect(self.load_cloth_button, SIGNAL('clicked()'), lambda *args:self.load_cloth_function(self.fieldText.text()))
#         self.connect(self.L_P_button, SIGNAL('clicked()'), lambda *args:self.L_P_button_function(self.fieldText.text()))
#         self.connect(self.open_button, SIGNAL('clicked()'), lambda *args:self.open_folder_button_function(self.fieldText.text()))
#         self.btnlayout.addWidget(self.back_button)
#         self.btnlayout.addWidget(self.set_button)
#         self.btnlayout.addWidget(self.load_button)
#         self.btnlayout.addWidget(self.load_hair_button)
#         self.btnlayout.addWidget(self.load_hair_single_button)
#         self.btnlayout.addWidget(self.load_cloth_button)
#         self.btnlayout.addWidget(self.L_P_button)
#         self.btnlayout.addWidget(self.open_button)
#         self.setLayout(self.layout)

    # def gotoAppend(self):
    #     self.close()


    def open_folder_button_function(self, content):
        access_main = cache_functions()
        content=str(content)
        access_main.opening_folder(content)

    def L_P_button_function(self, make_new_content):
        make_new_content = str(make_new_content)
        listed_extension = self.playlist
        listed_folder = listed_extension.currentText()    
        listed_folder = str(listed_folder)
        listed_folder = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(listed_folder) for name in files if name.lower().endswith(".xml")]         
        access_main = cache_functions()
        access_main.load_and_play(make_new_content, listed_folder)

    def load_button_function(self, make_new_content):
        make_new_content = str(make_new_content)
        print make_new_content
        # listed_extension = self.playlist
        # listed_folder = listed_extension.currentText()    
        # listed_folder= str(listed_folder)         
        # print listed_folder
        # xmlfiles = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(listed_folder+'/') for name in files if name.lower().endswith(".xml")]   
        # get_folder_for_jpgs = [(each_file) for each_file in os.walk(get_selected_path) if "xml" in str(each_file)]     
        # print get_folder_for_jpgs   
        # print xmlfiles      
        access_main = cache_functions()
        access_main.load_cache(make_new_content)

    def load_hair_function(self, make_new_content):
        make_new_content = str(make_new_content)
        listed_extension = self.playlist
        listed_folder = listed_extension.currentText()    
        access_main = cache_functions()
        access_main.load_hair_cache(make_new_content, listed_folder)

    def load_hair_single_function(self, make_new_content):
        make_new_content = str(make_new_content)
        listed_extension = self.playlist
        listed_folder = listed_extension.currentText()    
        access_main = cache_functions()
        access_main.load_hair_cache_single(make_new_content, listed_folder)

    def load_cloth_function(self, make_new_content):
        make_new_content = str(make_new_content)
        listed_extension = self.playlist
        listed_folder = listed_extension.currentText()    
        access_main = cache_functions()
        access_main.load_cloth_cache(make_new_content, listed_folder)

    def set_button_function(self, make_new_content):
        make_new_content=str(make_new_content)
        listed_extension = self.playlist
        listed_folder = listed_extension.currentText()    
        listed_folder= str(listed_folder)      
        newgetpath = make_new_content+'/'+listed_folder
        self.fieldText.setText(newgetpath)     
        getFiles = [os.path.join(newgetpath, o) for o in os.listdir(newgetpath) if os.path.isdir(os.path.join(newgetpath, o)) and len(os.listdir(os.path.join(newgetpath, o)))>0]
        # getFiles = [os.path.join(newgetpath, o) for o in os.listdir(newgetpath) if os.path.isdir(os.path.join(newgetpath, o))]
        getFiles.sort(key=lambda x: os.path.getmtime(x))
        getFiles = [(each).split('/')[-1] for each in getFiles]        
        listed_extension.clear()
        listed_extension.addItems(getFiles)        

    def back_button_function(self, make_new_content):
        make_new_content=str(make_new_content)
        get_content_back = "/".join(make_new_content.split('/')[:-1])
        listed_extension = self.playlist
        listed_folder = listed_extension.currentText()    
        listed_folder= str(listed_folder)      
        self.fieldText.setText(get_content_back)     
        getFiles = [os.path.join(get_content_back, o) for o in os.listdir(get_content_back) if os.path.isdir(os.path.join(get_content_back, o))and len(os.listdir(os.path.join(get_content_back, o)))>0]
        getFiles.sort(key=lambda x: os.path.getmtime(x))
        getFiles = [(each).split('/')[-1] for each in getFiles]        
        self.playlist.clear()
        self.playlist.addItems(getFiles)  


class cache_functions(object):

    def opening_folder(self, folderPath):
        # newfolderPath=re.sub(r'\\',r'/', folderPath)
        os.system('xdg-open "%s"' % folderPath)

    def load_cache(self, listed_folder):
        if len(mc.ls(sl=1))<1:
            getSel = [(each) for each in mc.ls(type = "nCloth") if "Orig" not in each]
        else:
            getSel = mc.ls(sl=1)
        # filepath = make_new_content+"/"+listed_folder
        # filexml = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(filepath) for name in files if name.lower().endswith(".xml")][0]
        # getSel=mc.ls(sl=1)  
             
        # if len(getSel)>0:
        for each in getSel:
            getMesh = [(item) for clothitem in mc.ls(getSel) for item in mc.listHistory(clothitem) if mc.nodeType(item) == "mesh" if "Orig" not in item][0]
            # mc.select(each)
            findName = each.replace(":", "_")
            newName = findName+'.xml'
            filexml = listed_folder+'/'+newName
            pm.mel.doImportCacheFile(filexml, '', each, getMesh) 

    def checkCacheFile(self, interrogateName):
        cachefolderStart=getCachePath
        number = 0000
        getScene = mc.file(q=1, sn=1, shn=1)
        getFilename =  getScene.split(".")[:-1]
        getFilename ='_'.join(getFilename)+"_"+str(getUser)+"_nCache"
        getnewcachefolder = getFilename+"_"+str("%04d" % (number,))
        makecachefolder = cachefolderStart+"/"+getnewcachefolder
        if os.path.exists(makecachefolder): 
            get_vr_folders = [(dirnames) for dirpath, dirnames, files in os.walk(cachefolderStart)][0]
            get_vr_folders = [(each) for each in get_vr_folders if each.split("_")[-1].isdigit()]
            get_top = max(get_vr_folders)
            number = get_top.split("_")[-1]
            if "v" not in number:
                number = int(number)
            else:
                number = re.sub("\D", "", number)
            number = int(number)
            number +=1
            getnewcachefolder=getFilename+"_"+str("%04d" % (number,))
            makecachefolder = cachefolderStart+"/"+getnewcachefolder
            os.makedirs(makecachefolder)
            print "created "+makecachefolder
        if not os.path.exists(makecachefolder): 
            os.makedirs(makecachefolder) 
            print "created "+makecachefolder
        print getFilename, makecachefolder
        return getFilename, makecachefolder

    def load_cloth_cache(self, make_new_content, listed_folder):
        filepath = make_new_content+"/"+listed_folder+"/"
        grabsystem=mc.ls(type="nCloth")
        mc.select(grabsystem, r=1)       
        getLowRange=mc.playbackOptions(q=1, ast=1)
        getHiRange=mc.playbackOptions(q=1, aet=1)
        if len(mc.ls(sl=1))<1:
            getHairSel = [(each) for each in mc.ls(type = "nCloth") if "Orig" not in each]
        else:
            getHairSel = mc.ls(sl=1)        
        createdict = [(name) for dirpath, dirnames, files in os.walk(str(filepath)) for name in files if name.lower().endswith(".xml")]
        # createdict = [(name) for dirpath, dirnames, files in os.walk(str(filepath)) for name in files if name.lower().endswith(".mcx")]
        filecloth = [(name) for dirpath, dirnames, files in os.walk(str(filepath)) for name.split(".")[-1] in files]
        getSel=mc.ls(sl=1)
        if len(getHairSel)>0:
            for value in createdict:
                for hairbit in getHairSel:   
                    grab_filename_match = hairbit.replace(':', '_')   
                    if "Frame" in value:
                        presetName = value.split("Frame")[0]
                    else:
                        presetName = value.split(".")[0]
                    filexml=str(filepath)+value
                    if grab_filename_match == presetName:
                        getCache=[(nodes) for nodes in mc.listHistory(hairbit) if mc.nodeType(nodes) == "cacheBlend"]
                        if len(getCache)>0:
                            mc.delete(getCache)
                            print "deleted: " + str(getCache)
                        getCache=[(nodes) for nodes in mc.listHistory(hairbit) if mc.nodeType(nodes) == "cacheFile"]
                        if len(getCache)>0:
                            mc.delete(getCache)   
                            print "deleted: " + str(getCache)
                        presetName = value.split(".")[0]
                        cache_path = filepath.replace('//', '/')
                        cache_name = presetName
                        shape = hairbit      
                        createdCacheFileNode = mc.createNode("cacheFile", n=presetName+"Cache1")
                        print "created cachefile "+presetName+"Cache1"
                        mc.setAttr(createdCacheFileNode+".cachePath", filepath, type = "string")
                        print "set attr: "+createdCacheFileNode+".cachePath to "+filepath
                        mc.setAttr(createdCacheFileNode+".cacheName", presetName, type = "string")
                        print "set attr: "+createdCacheFileNode+".cacheName to "+presetName
                        mc.setAttr(createdCacheFileNode+".startFrame", getLowRange)
                        print "set attr: "+createdCacheFileNode+".startFrame to "+str(getLowRange)
                        mc.setAttr(createdCacheFileNode+".originalStart", getLowRange)
                        print "set attr: "+createdCacheFileNode+".originalStart to "+str(getLowRange)
                        mc.setAttr(createdCacheFileNode+".sourceStart", getLowRange)
                        print "set attr: "+createdCacheFileNode+".sourceStart to "+str(getLowRange)
                        mc.setAttr(createdCacheFileNode+".originalEnd", getHiRange)
                        print "set attr: "+createdCacheFileNode+".originalEnd to "+str(getHiRange)
                        mc.setAttr(createdCacheFileNode+".sourceEnd", getHiRange)
                        print "set attr: "+createdCacheFileNode+".sourceEnd to "+str(getHiRange)
                        mc.setAttr(createdCacheFileNode+".inRange", 1)
                        print "set attr: "+createdCacheFileNode+".inRange to 1"
                        mc.connectAttr(createdCacheFileNode+".inRange", hairbit+".playFromCache", f=1)
                        print "connected attr: "+createdCacheFileNode+".inRange to "+hairbit+".playFromCache"
                        mc.connectAttr(createdCacheFileNode+".outCacheData[0]", hairbit+".positions", f=1)           
                        print "connected attr: "+createdCacheFileNode+".outCacheData[0] to "+hairbit+".positions"
                        mc.connectAttr("time1.outTime", createdCacheFileNode+".time", f=1)   
                        print "connected attr: time1.outTime to "+createdCacheFileNode+".time"          


    def load_cloth_cacheV1(self, make_new_content, listed_folder):
        #startnaming
        filepath = make_new_content+"/"+listed_folder+"/"
        print "got here"
        grabsystem=mc.ls(type="nCloth")
        mc.select(grabsystem, r=1)       
        if ":" in grabsystem[0]:
            interroName = grabsystem[0].split(":")[-1]+"_"
        else:
            interroName=interroName+"_"
        # newName, cachFolder=self.checkCacheFile(interroName, filepath) 
        #endnaming
        getLowRange=mc.playbackOptions(q=1, ast=1)
        print getLowRange
        getHiRange=mc.playbackOptions(q=1, aet=1)
        print getHiRange
        if len(mc.ls(sl=1))<1:
            getHairSel = [(each) for each in mc.ls(type = "nCloth") if "Orig" not in each]
        else:
            getHairSel = mc.ls(sl=1)        
        createdict = [(name) for dirpath, dirnames, files in os.walk(str(filepath)) for name in files if name.lower().endswith(".mcx")]
        filecloth = [(name) for dirpath, dirnames, files in os.walk(str(filepath)) for name.split(".")[-1] in files]
        getSel=mc.ls(sl=1)
        if len(getHairSel)>0:
            for value in createdict:
                for hairbit in getHairSel:               
                    filexml=str(filepath)+value
                    grabName = hairbit.split(":")[-1]
                    if grabName in value:
                        getCache=[(nodes) for nodes in mc.listHistory(hairbit) if mc.nodeType(nodes) == "cacheBlend"]
                        if len(getCache)>0:
                            mc.delete(getCache)
                            print "deleted: " + getCache
                        getCache=[(nodes) for nodes in mc.listHistory(hairbit) if mc.nodeType(nodes) == "cacheFile"]
                        if len(getCache)>0:
                            mc.delete(getCache) 
                            print "deleted: " + getCache
                        presetName = value.split(".")[0]
                        cache_path = filepath
                        cache_name = presetName
                        shape = hairbit
                        createdCacheFileNode = mc.createNode("cacheFile", n=presetName+"Cache1")
                        mc.setAttr(createdCacheFileNode+".cachePath", filepath, type = "string")
                        mc.setAttr(createdCacheFileNode+".cacheName", presetName, type = "string")
                        mc.setAttr(createdCacheFileNode+".startFrame", getLowRange)
                        mc.setAttr(createdCacheFileNode+".originalStart", getLowRange)
                        mc.setAttr(createdCacheFileNode+".sourceStart", getLowRange)
                        mc.setAttr(createdCacheFileNode+".originalEnd", getHiRange)
                        mc.setAttr(createdCacheFileNode+".sourceEnd", getHiRange)
                        mc.setAttr(createdCacheFileNode+".inRange", 1)
                        mc.connectAttr(createdCacheFileNode+".inRange", hairbit+".playFromCache", f=1)
                        # mc.connectAttr(createdCacheFileNode+".outCacheData[0]", hairbit+".hairCounts", f=1)
                        # mc.connectAttr(createdCacheFileNode+".outCacheData[1]", hairbit+".vertexCounts", f=1)
                        mc.connectAttr(createdCacheFileNode+".outCacheData[0]", hairbit+".positions", f=1)
                        mc.connectAttr("time1.outTime", createdCacheFileNode+".time", f=1)    
                        # mc.connectAttr(createdCacheFileNode+".outCacheData[0]", createdCacheBlendNode+".vectorArray[1]", f=1)    

    def chunks(self, list, n):
        for i in range(0, len(list), n):
            yield list[i:i+n]

    def load_hair_cache_single(self, make_new_content, listed_folder):
        getname = listed_folder.split("/")[-1]
        getLowRange=mc.playbackOptions(q=1, ast=1)
        getHiRange=mc.playbackOptions(q=1, aet=1)
        if len(mc.ls(sl=1))<1:
            getHairSel = [(each) for each in mc.ls(type = "hairSystem") if "Orig" not in each]
        else:
            getHairSel = mc.ls(sl=1)    
        filepath = make_new_content+"/"+listed_folder+"/"
        createdict = [(name) for dirpath, dirnames, files in os.walk(str(filepath)) for name in files if name.lower().endswith(".xml")]
        filecloth = [(name) for dirpath, dirnames, files in os.walk(str(filepath)) for name.split(".")[-1] in files]
        getSel=mc.ls(sl=1)
        getLowRange = str(getLowRange)
        getHiRange = str(getHiRange)
        if len(getHairSel)>0:
            getFull_len=range(0, len(getHairSel)*3)
            getList = list(self.chunks(getFull_len, 3))
            for value in createdict:
                presetName = value.split(".")[0]
                cache_name = presetName
                createdCacheFileNode = mc.createNode("cacheFile", n=presetName+"Cache1")
                print "created cachefile "+presetName+"Cache1"
                mc.setAttr(createdCacheFileNode+".cachePath", filepath, type = "string")
                print "set attr: "+createdCacheFileNode+".cachePath to "+filepath
                mc.setAttr(createdCacheFileNode+".cacheName", presetName, type = "string")
                print "set attr: "+createdCacheFileNode+".cacheName to "+presetName
                mc.setAttr(createdCacheFileNode+".startFrame", getLowRange)
                print "set attr: "+createdCacheFileNode+".startFrame to "+getLowRange
                mc.setAttr(createdCacheFileNode+".originalStart", getLowRange)
                print "set attr: "+createdCacheFileNode+".originalStart to "+getLowRange
                mc.setAttr(createdCacheFileNode+".sourceStart", getLowRange)
                print "set attr: "+createdCacheFileNode+".sourceStart to "+getLowRange
                mc.setAttr(createdCacheFileNode+".originalEnd", getHiRange)
                print "set attr: "+createdCacheFileNode+".originalEnd to "+getHiRange
                mc.setAttr(createdCacheFileNode+".sourceEnd", getHiRange)
                print "set attr: "+createdCacheFileNode+".sourceEnd to "+getHiRange
                mc.setAttr(createdCacheFileNode+".inRange", 1)
                print "set attr: "+createdCacheFileNode+".inRange to 1"
                mc.connectAttr("time1.outTime", createdCacheFileNode+".time", f=1)           
                print "connected attr: time1.outTime to "+createdCacheFileNode+".time"
                for each_bit, hairbit in map(None, getList, getHairSel):    
                    grab_filename_match = getname   
                    filexml=str(filepath)+value
                    getCache=[(nodes) for nodes in mc.listHistory(hairbit) if mc.nodeType(nodes) == "cacheBlend"]
                    if len(getCache)>0:
                        mc.delete(getCache)
                    getCache=[(nodes) for nodes in mc.listHistory(hairbit) if mc.nodeType(nodes) == "cacheFile"]
                    if len(getCache)>0:
                        mc.delete(getCache)  
                    cache_path = filepath
                    shape = hairbit
                    mc.connectAttr(createdCacheFileNode+".inRange", hairbit+".playFromCache", f=1)
                    print "connected attr: "+createdCacheFileNode+".inRange to "+hairbit+".playFromCache"
                    mc.connectAttr(createdCacheFileNode+".outCacheData[%d]" %(each_bit[0], ), hairbit+".hairCounts", f=1)
                    print "connected attr: "+createdCacheFileNode+".outCacheData[0] to "+hairbit+".hairCounts"
                    mc.connectAttr(createdCacheFileNode+".outCacheData[%d]" %(each_bit[1], ), hairbit+".vertexCounts", f=1)
                    print "connected attr: "+createdCacheFileNode+".outCacheData[1] to "+hairbit+".vertexCounts"
                    mc.connectAttr(createdCacheFileNode+".outCacheData[%d]" %(each_bit[2], ), hairbit+".positions", f=1)  
                    print "connected attr: "+createdCacheFileNode+".outCacheData[2] to "+hairbit+".positions"
                    # mc.connectAttr(createdCacheFileNode+".outCacheData[0]", createdCacheBlendNode+".vectorArray[1]", f=1)             


    def load_hair_cache(self, make_new_content, listed_folder):
        getLowRange=mc.playbackOptions(q=1, ast=1)
        getHiRange=mc.playbackOptions(q=1, aet=1)
        if len(mc.ls(sl=1))<1:
            getHairSel = [(each) for each in mc.ls(type = "hairSystem") if "Orig" not in each]
        else:
            getHairSel = mc.ls(sl=1)    
        print getHairSel    
        filepath = make_new_content+"/"+listed_folder+"/"
        print filepath
        createdict = [(name) for dirpath, dirnames, files in os.walk(str(filepath)) for name in files if name.lower().endswith(".xml")]
        filecloth = [(name) for dirpath, dirnames, files in os.walk(str(filepath)) for name.split(".")[-1] in files]
        getSel=mc.ls(sl=1)
        print createdict
        if len(getHairSel)>0:
            for value in createdict:
                for hairbit in getHairSel:    
                    grab_filename_match = hairbit.replace(':', '_')   
                    presetName = value.split(".")[0]
                    filexml=str(filepath)+value
                    if grab_filename_match == presetName:
                        getCache=[(nodes) for nodes in mc.listHistory(hairbit) if mc.nodeType(nodes) == "cacheBlend"]
                        if len(getCache)>0:
                            mc.delete(getCache)
                        getCache=[(nodes) for nodes in mc.listHistory(hairbit) if mc.nodeType(nodes) == "cacheFile"]
                        if len(getCache)>0:
                            mc.delete(getCache)  
                        presetName = value.split(".")[0]
                        cache_path = filepath
                        cache_name = presetName
                        shape = hairbit
                        getLowRange = str(getLowRange)
                        getHiRange = str(getHiRange)
                        createdCacheFileNode = mc.createNode("cacheFile", n=presetName+"Cache1")
                        print "created cachefile "+presetName+"Cache1"
                        mc.setAttr(createdCacheFileNode+".cachePath", filepath, type = "string")
                        print "set attr: "+createdCacheFileNode+".cachePath to "+filepath
                        mc.setAttr(createdCacheFileNode+".cacheName", presetName, type = "string")
                        print "set attr: "+createdCacheFileNode+".cacheName to "+presetName
                        mc.setAttr(createdCacheFileNode+".startFrame", getLowRange)
                        print "set attr: "+createdCacheFileNode+".startFrame to "+getLowRange
                        mc.setAttr(createdCacheFileNode+".originalStart", getLowRange)
                        print "set attr: "+createdCacheFileNode+".originalStart to "+getLowRange
                        mc.setAttr(createdCacheFileNode+".sourceStart", getLowRange)
                        print "set attr: "+createdCacheFileNode+".sourceStart to "+getLowRange
                        mc.setAttr(createdCacheFileNode+".originalEnd", getHiRange)
                        print "set attr: "+createdCacheFileNode+".originalEnd to "+getHiRange
                        mc.setAttr(createdCacheFileNode+".sourceEnd", getHiRange)
                        print "set attr: "+createdCacheFileNode+".sourceEnd to "+getHiRange
                        mc.setAttr(createdCacheFileNode+".inRange", 1)
                        print "set attr: "+createdCacheFileNode+".inRange to 1"
                        mc.connectAttr(createdCacheFileNode+".inRange", hairbit+".playFromCache", f=1)
                        print "connected attr: "+createdCacheFileNode+".inRange to "+hairbit+".playFromCache"
                        mc.connectAttr(createdCacheFileNode+".outCacheData[0]", hairbit+".hairCounts", f=1)
                        print "connected attr: "+createdCacheFileNode+".outCacheData[0] to "+hairbit+".hairCounts"
                        mc.connectAttr(createdCacheFileNode+".outCacheData[1]", hairbit+".vertexCounts", f=1)
                        print "connected attr: "+createdCacheFileNode+".outCacheData[1] to "+hairbit+".vertexCounts"
                        mc.connectAttr(createdCacheFileNode+".outCacheData[2]", hairbit+".positions", f=1)  
                        print "connected attr: "+createdCacheFileNode+".outCacheData[2] to "+hairbit+".positions"
                        mc.connectAttr("time1.outTime", createdCacheFileNode+".time", f=1)           
                        print "connected attr: time1.outTime to "+createdCacheFileNode+".time"
                        # mc.connectAttr(createdCacheFileNode+".outCacheData[0]", createdCacheBlendNode+".vectorArray[1]", f=1)             
        else:
            for value in createdict:
                for hairbit in getHairSel:
                    filexml=str(filepath)+value
                    grabName = hairbit.split(":")[-1]
                    if grabName in value:
                        getCache=[(nodes) for nodes in mc.listHistory(hairbit) if mc.nodeType(nodes) == "cacheBlend"]
                        if len(getCache)>0:
                            mc.delete(getCache)
                        getCache=[(nodes) for nodes in mc.listHistory(hairbit) if mc.nodeType(nodes) == "cacheFile"]
                        if len(getCache)>0:
                            mc.delete(getCache)   
                        presetName = value.split(".")[0]
                        cache_path = filepath
                        cache_name = presetName
                        shape = hairbit
                        createdCacheFileNode = mc.createNode("cacheFile", n=presetName+"Cache1")
                        print "created cachefile "+presetName+"Cache1"
                        mc.setAttr(createdCacheFileNode+".cachePath", filepath, type = "string")
                        print "set attr: "+createdCacheFileNode+".cachePath to "+filepath
                        mc.setAttr(createdCacheFileNode+".cacheName", presetName, type = "string")
                        print "set attr: "+createdCacheFileNode+".cacheName to "+presetName
                        mc.setAttr(createdCacheFileNode+".startFrame", getLowRange)
                        print "set attr: "+createdCacheFileNode+".startFrame to "+getLowRange
                        mc.setAttr(createdCacheFileNode+".originalStart", getLowRange)
                        print "set attr: "+createdCacheFileNode+".originalStart to "+getLowRange
                        mc.setAttr(createdCacheFileNode+".sourceStart", getLowRange)
                        print "set attr: "+createdCacheFileNode+".sourceStart to "+getLowRange
                        mc.setAttr(createdCacheFileNode+".originalEnd", getHiRange)
                        print "set attr: "+createdCacheFileNode+".originalEnd to "+getHiRange
                        mc.setAttr(createdCacheFileNode+".sourceEnd", getHiRange)
                        print "set attr: "+createdCacheFileNode+".sourceEnd to "+getHiRange
                        mc.connectAttr(createdCacheFileNode+".inRange", hairbit+".playFromCache", f=1)
                        print "connected attr: "+createdCacheFileNode+".inRange to "+hairbit+".playFromCache"
                        mc.connectAttr(createdCacheFileNode+".outCacheData[0]", hairbit+".hairCounts", f=1)
                        print "connected attr: "+createdCacheFileNode+".outCacheData[0] to "+hairbit+".hairCounts"
                        mc.connectAttr(createdCacheFileNode+".outCacheData[1]", hairbit+".vertexCounts", f=1)
                        print "connected attr: "+createdCacheFileNode+".outCacheData[1] to "+hairbit+".vertexCounts"
                        mc.connectAttr(createdCacheFileNode+".outCacheData[2]", hairbit+".positions", f=1)
                        print "connected attr: "+createdCacheFileNode+".outCacheData[2] to "+hairbit+".positions"
                        mc.connectAttr("time1.outTime", createdCacheFileNode+".time", f=1)  
                        print "connected attr: time1.outTime to "+createdCacheFileNode+".time"


    def load_hair_cacheV1(self, listed_folder):
        if len(mc.ls(sl=1))<1:
            getSel = [(each) for each in mc.ls(type = "hairSystem") if "Orig" not in each]
        else:
            getSel = mc.ls(sl=1)
        for each in getSel:
            getCache = [(nodes) for nodes in mc.listHistory(each) if mc.nodeType(nodes) == "cacheBlend"]
            if len(getCache)>0:
                mc.delete(getCache)
            getCache = [(nodes) for nodes in mc.listHistory(each) if mc.nodeType(nodes) == "cacheFile"]
            if len(getCache)>0:
                mc.delete(getCache)           
            findName = each.replace(":", "_")
            newName = findName+'.xml'
            print newName
            filexml = listed_folder+'/'+newName
            print filexml
            pm.mel.doImportCacheFile(filexml, '', findName, each) 


    def load_cacheV1(self, make_new_content, listed_folder):
        filepath = make_new_content+"/"+listed_folder
        createdict = [{os.path.join(dirpath, name): name} for dirpath, dirnames, files in os.walk(filepath) for name in files if name.lower().endswith(".xml")]
        filecloth = [(name) for dirpath, dirnames, files in os.walk(filepath) for name in files if name.lower().endswith(".nCloth")]
        print createdict
        print filecloth
  
        getSel=mc.ls(sl=1)
        if len(getSel)>0:
            for selobj in getSel:
                for key, value in createdict.items():
                    getobjname=value[0].split('.')[0]
                    # print getobjname
                    if getobjname == str(selobj):
                        getShape=[(nodes) for nodes in mc.listHistory(selobj) if mc.nodeType(nodes) == "historySwitch"]
                        if len(getShape)>0:
                            maya.mel.eval('deleteCacheFile 2 { "keep", "" } ;')
                        getCommand='createHistorySwitch("%s",false)' %selobj
                        switch = maya.mel.eval(getCommand)
                        cacheNode = mc.cacheFile(f=key, ia='%s.inp[0]' % switch ,attachFile=True)
                        mc.setAttr( '%s.playFromCache' % switch, 1 )                
        else:
            for key, value in createdict.items():
                if filecloth in value:
                    getObj = mc.ls(filecloth)[0]
                    getShape=[(nodes) for nodes in mc.listHistory(getObj) if mc.nodeType(nodes) == "historySwitch"]
                    if len(getShape)>0:
                        maya.mel.eval('deleteCacheFile 2 { "keep", "" } ;')
                    getCommand='createHistorySwitch("%s",false)' %getObj
                    switch = maya.mel.eval(getCommand)
                    cacheNode = mc.cacheFile(f=filexml, ia='%s.inp[0]' % switch ,attachFile=True)
                    mc.setAttr( '%s.playFromCache' % switch, 1 )                
            
    def load_and_play(self, make_new_content, listed_folder):
        filepath = make_new_content+"/"+listed_folder
        filexml = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(filepath) for name in files if name.lower().endswith(".xml")][0]
        getSel = mc.ls(sl=1)
        if len(getSel)>0:
            for each in getSel:
                getShape=[(nodes) for nodes in mc.listHistory(each) if mc.nodeType(nodes) == "historySwitch"]
                #getShape=mc.listRelatives(each, ad=1, type="historySwitch")
                if len(getShape)>0:
                    maya.mel.eval('deleteCacheFile 2 { "keep", "" } ;')
                getCommand='createHistorySwitch("%s",false)' %each
                switch = maya.mel.eval(getCommand)
                cacheNode = mc.cacheFile(f=filexml, ia='%s.inp[0]' % switch ,attachFile=True)
                mc.setAttr( '%s.playFromCache' % switch, 1 )
            mc.select(clear=1)
            filepath = "_".join(filepath.split("."))
            filename = filepath.split('/')[-1]
            filepathname = filepath+'/'+filename
            print filepathname
            if not os.path.exists(filepath): os.makedirs(filepath)
            mc.playblast(clearCache=1, endTime=mc.playbackOptions(max=1, aet=1, q=1), filename=filepathname, format="image", offScreen=1, percent=100, quality=100, sequenceTime=0, showOrnaments = 1, startTime=mc.playbackOptions(min=1, ast=1, q=1), viewer=0, widthHeight=[2156, 1212])
            time.sleep(1.3)
            command = "rv "+ filepath
            subprocess.Popen(command, stdout = subprocess.PIPE, shell = True)
        else:
            print "select something"

inst=find_Path()
inst.show()            
