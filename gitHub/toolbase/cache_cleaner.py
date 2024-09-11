'''(This launches a GUI) for options on cleaning corrupt caches'''

import maya.cmds as cmds
import os, sys

import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets



class cache_management(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(cache_management, self).__init__(parent = None)

        self.setWindowTitle("Cache clean")
        self.central_widget=QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.masterLayout=QtWidgets.QGridLayout(self.central_widget)
        self.masterLayout.setAlignment(QtCore.Qt.AlignTop)


        self.myform = QtWidgets.QFormLayout()
        self.layout = QtWidgets.QGridLayout()
        self.masterLayout.addLayout(self.layout, 0,0,1,1)

        self.SelectionSetupLayout = QtWidgets.QGridLayout()
        self.selection_widgetframe = QtWidgets.QFrame()
        self.selection_widgetframe.setLayout(self.SelectionSetupLayout)
        self.SelectionSetupLayout.addLayout(self.myform, 0,0,1,1)
        self.layout.addLayout(self.SelectionSetupLayout, 0,0,1,1)

        self.add_widgets()

        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(self.selection_widgetframe)
        scroll.setWidgetResizable(False)
        self.layout.addWidget(scroll, 1,0,1,1)
        self.setLayout(self.layout)
    def add_widgets(self):
        self.plot_order_layout = QtWidgets.QHBoxLayout()
        self.myform.addRow(self.plot_order_layout) 
        self.plot_button_layout = QtWidgets.QVBoxLayout()
        self.plot_order_layout.addLayout(self.plot_button_layout)
        self.plot_slid_layout = QtWidgets.QVBoxLayout()
        self.plot_order_layout.addLayout(self.plot_slid_layout)   
        self.plot_slider_layout = QtWidgets.QVBoxLayout()     
        self.plot_slid_layout.addLayout(self.plot_slider_layout)   

        self.cache_cln_button=QtWidgets.QPushButton("clean caches")
        self.cache_cln_button.setToolTip("This will delete any cache related nodes(cacheBlend and cacheFile) connected to object. This does NOT remove the (xml, mcx) cache in your directory. you will have to reattach manually")
        # self.connect(self.cache_cln_button, SIGNAL('clicked()'),lambda: self.clearCache())
        self.cache_cln_button.clicked.connect(lambda: self.clearCache())
        self.plot_button_layout.addWidget(self.cache_cln_button)



    def clearCache(self):     
        grabsystem = []
        if len(cmds.ls(sl=1)) <1:
            grabsystem=cmds.ls(type="hairSystem")
            print (grabsystem)
            if len(grabsystem) >0:
                pass
            else:
                grabsystem=cmds.ls(type="nCloth")
                print (grabsystem)
            if len(grabsystem) >0:
                pass
            else:
                grabsystem=cmds.ls(type="cacheFile")
                print (grabsystem)
        else:
            grabsystem = cmds.ls(sl=1)
            print (grabsystem)
        cmds.select(grabsystem, r=1)
        for each in grabsystem:
            getCache=[(nodes) for nodes in cmds.listHistory(each) if cmds.nodeType(nodes) == "cacheBlend"]
            if len(getCache)>0:
                cmds.delete(getCache)
                print ("deleted cacheBlend on "+each)
            getCache=[(nodes) for nodes in cmds.listHistory(each) if cmds.nodeType(nodes) == "cacheFile"]
            if len(getCache)>0:
                cmds.delete(getCache) 
                print ("deleted cacheFile on "+each)  

    def refreshCache(self):
        grabsystem = []
        if len(cmds.ls(sl=1)) <1:
            print ("Please select object with cache connected")
        else:
            grabsystem = cmds.ls(sl=1)
        cmds.select(grabsystem, r=1)
        for each in grabsystem:

            getCacheBlend=[(nodes) for nodes in cmds.listHistory(each) if cmds.nodeType(nodes) == "cacheBlend"]
            if len(getCacheBlend)>0:
                cmds.delete(getCacheBlend)
                print ("deleted cacheBlend on "+each)
            getCacheFile=[(nodes) for nodes in cmds.listHistory(each) if cmds.nodeType(nodes) == "cacheFile"]
            if len(getCacheFile)>0:
                for cache_file_item in getCacheFile:
                    find_file_value = cmds.getAttr('{}.cachePath'.format(cache_file_item))
                    filexml = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(find_file_value) for name in files if name.lower().endswith(".xml")][0]
                cmds.delete(getCacheFile)
                print ("deleted cacheFile on "+each)   
                getShape=[(nodes) for nodes in cmds.listHistory(each) if cmds.nodeType(nodes) == "historySwitch"]
                #getShape=cmds.listRelatives(each, ad=1, type="historySwitch")
                if len(getShape)>0:
                    print ("clearing history switch")
                    maya.mel.eval('deleteCacheFile 2 { "keep", "" } ;')
                getCommand='createHistorySwitch("{}",false)'.format(each)
                switch = maya.mel.eval(getCommand)
                print ("created {}".format(switch))
                cacheNode = cmds.cacheFile(f=filexml, ia='{}.inp[0]'.format(switch) ,attachFile=True)
                print ("Attached {} to {}".format(filexml, each))
                cmds.setAttr( '{}.playFromCache'.format(switch), 1 )
                print ("Setting {}.playFromCache to {}".format(switch, 1))




inst=cache_management()
inst.show()            
