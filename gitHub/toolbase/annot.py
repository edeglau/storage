

# import mrig_pyqt
# from mrig_pyqt import QtCore, QtGui
# from mrig_pyqt.QtGui import QWidget, QRadioButton, QGridLayout, QLabel, \
#     QTableWidget, QComboBox, QKeySequence, QToolButton, QPlainTextEdit, QPushButton,QBoxLayout, \
#     QClipboard, QTableWidgetItem, QCheckBox, QVBoxLayout, QHBoxLayout, \
#     QPixmap, QLineEdit, QListWidget, QTextEdit, QSizePolicy, QFrame, QPalette, QColor, \
#     QFont, QAbstractItemView, QMenu, QMessageBox
# from mrig_pyqt.QtCore import SIGNAL

import mrig_pyqt
from mrig_pyqt import QtCore, QtGui, QtWidgets
from mrig_pyqt.QtCore import SIGNAL

import maya.cmds as mc
import random

__author__="Elise Deglau"
colorlist=[13, 6, 14, 17, 4, 8, 5, 7, 15, 5, 20, 24, 29, 31, 10, 16, 9, 30, 1, 2]

class annot_win(QtWidgets.QWidget):
    def __init__(self):
        super(annot_win, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Annotate")
        self.layout = QtWidgets.QVBoxLayout()
        self.btnlayout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.btnlayout)        
        self.annot_sel_button = QtWidgets.QPushButton("Annotate Selected")
        self.annot_sel_button.setToolTip("Pipeline issues/data retrieval/IT")
        self.connect(self.annot_sel_button, SIGNAL("clicked()"),
                    lambda: self.annotations_list())       
        self.auto_annot_button = QtWidgets.QPushButton("Auto Annotate")
        self.connect(self.auto_annot_button, SIGNAL("clicked()"),
                    lambda: self.dealers_choice())                     
        self.colour_annot_button = QtWidgets.QPushButton("Change Annot Colours")
        self.connect(self.colour_annot_button, SIGNAL("clicked()"),
                    lambda: self._change_anot_colors())                      
        self.btnlayout.addWidget(self.auto_annot_button)     
        self.btnlayout.addWidget(self.annot_sel_button)
        self.btnlayout.addWidget(self.colour_annot_button)
        self.setLayout(self.layout)


    def annotations_list(self):
        getName=["namespace"]
        selObj = mc.ls(sl=1)
        getIt=mc.ls("*ANNOTATE_GRP*")
        if len(getIt)<1:
            getIt=mc.CreateEmptyGroup()
            mc.rename(getIt, "ANNOTATE_GRP")
            getIt=mc.ls("*ANNOTATE_GRP*")
        else:
            getIt=mc.ls("*ANNOTATE_GRP*")         
        for item in selObj:
            getparentObj=[(each.split("|")[1]) for each in mc.listRelatives(item, f=1, ap=1)][0]
            Attrs=[(attrItem) for attrItem in mc.listAttr (getparentObj) for attrName in getName if attrName in attrItem] 
            if len(Attrs)>0:        
                for attributeitem in Attrs:
                    newItem=getparentObj+"."+attributeitem
                    getTitle=mc.getAttr(newItem)
            else:
                getTitle = getparentObj
            random.shuffle(colorlist, random.random)
            offset = colorlist[0]
            mc.select(item, r=1)
            self.point_const()
            selected = mc.ls(sl=1)
            if len(selected)>1:
                selected = selected[-1]
            else:
                selected = selected[0]
            mc.parent(selected, getIt)
            transformWorldMatrix=mc.xform(selected, q=True, ws=1, t=True)
            plusnum=random.uniform(0,5)
            newTransform = [transformWorldMatrix[0], transformWorldMatrix[1]+plusnum, transformWorldMatrix[2]]
            getAnnot = mc.annotate(selected, p=newTransform)
            buildParent = mc.group(n=getTitle+"_grp")
            mc.CenterPivot()
            mc.setAttr(getAnnot+".text", getTitle, type="string")
            mc.setAttr(getAnnot+".overrideEnabled", 1)
            mc.setAttr(getAnnot+".overrideColor", offset)
            getparent = mc.listRelatives(getAnnot, p=1)[0]
            mc.pointConstraint(selected, buildParent, mo=1)
            mc.rename(getparent, getTitle+"_ant")
            mc.rename(selected, item)
            mc.parent(buildParent, getIt)
            

    def point_const(self, arg=None):
        getSel=mc.ls(sl=1, fl=1)
        self.point_const_callup(getSel)


    def point_const_callup(self, getSel):
        edgeBucket=[]
        if ".vtx[" in getSel[0]:
            pass
        else:
            print "You need to make some vertex selections for this tool to operate on."
        for each in getSel:
            if ":" in each:
                findName=each.split(":")[-1:][0]
            else:
                findName=each
            if ":" in getSel[0]:
                getObj=getSel[0].split(":")[-1:]
            else:
                getObj=getSel
            getObj=getObj[0].split('.')[0]
            getUVmap = mc.polyListComponentConversion(each, fv=1, tuv=1)
            getCoords=mc.polyEditUV(getUVmap, q=1)
            getNew=mc.spaceLocator(n=str(findName)+"ploc")
            mc.select(each, r=1)
            mc.select(getNew[0], add=1)
            buildConst=mc.pointOnPolyConstraint(each, getNew[0], mo=0, offset=(0.0, 0.0, 0.0))
            mc.setAttr(buildConst[0]+"."+getObj+"U0", getCoords[0])
            mc.setAttr(buildConst[0]+"."+getObj+"V0", getCoords[1])    

    def dealers_choice(self):
        collectedVtx=[]
        if len(mc.ls(sl=1))<1:
            nameSpacerig = [(each) for each in mc.ls("*:*") if mc.nodeType(each) == "transform" and mc.listRelatives(each, p=1) == None]
            normalrig = [(each) for each in mc.ls("*") if mc.nodeType(each) == "transform" and mc.listRelatives(each, p=1) == None]
            rigs = nameSpacerig +normalrig
            for item in rigs:
                if mc.listRelatives(item, ad=1, type="mesh"):
                    getparentObj=[(each) for each in mc.listRelatives(item, ad=1, type="mesh")][0]
                    getvert=getparentObj+".vtx[0]"
                    collectedVtx.append(getvert)
            mc.select(collectedVtx, r=1)
            self.annotations_list()              
        elif mc.nodeType(mc.ls(sl=1)[0]) == "transform":
            rigs = mc.ls(sl=1)
            for item in rigs:
                if mc.listRelatives(item, ad=1, type="mesh"):
                    getparentObj=[(each) for each in mc.listRelatives(item, ad=1, type="mesh")][0]
                    getvert=getparentObj+".vtx[0]"
                    collectedVtx.append(getvert)
            mc.select(collectedVtx, r=1)
            self.annotations_list()            
        elif mc.nodeType(mc.ls(sl=1)[0]) == "mesh":
            self.annotations_list()

    def _change_anot_colors(self):
        getgrp = mc.ls(sl=1)
        if len(getgrp)<1:
            getgrp = mc.ls(type="annotationShape")
        if len(getgrp)>0:
            pass
        else:
            print "annotations not present in scene"
            return
        for each in getgrp:
            random.shuffle(colorlist, random.random)
            offset = colorlist[0]
            mc.setAttr(each+".overrideEnabled", 1)
            mc.setAttr(each+".overrideColor", offset)


inst=annot_win()
inst.show()            



