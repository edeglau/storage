

import os, sys, subprocess
from datetime import datetime
import maya.cmds as cmds
import re
import pymel.core as pm
import mrig_pyqt
from mrig_pyqt import QtCore, QtGui, QtWidgets
from mrig_pyqt.QtCore import SIGNAL


class sim_strips_win(QtWidgets.QWidget):
    # def __init__(self): 
    def __init__(self):
        super(sim_strips_win, self).__init__()
        self.initUI()

    def initUI(self):    
        self.setWindowTitle("sim strips")

        self.layout=QtWidgets.QGridLayout()
        
        self.btnlayout = QtWidgets.QVBoxLayout()

        self.layout.addLayout(self.btnlayout, 0,0,1,1)  
        self.U_label = QtWidgets.QLabel("U spans(cloth strip)")
        self.btnlayout.addWidget(self.U_label)        
        self.U_textfeild = QtWidgets.QTextEdit("12")
        self.U_textfeild.setFixedHeight(25)
        self.btnlayout.addWidget(self.U_textfeild)
        self.V_label = QtWidgets.QLabel("V spans(cloth strip)")
        self.btnlayout.addWidget(self.V_label)        
        self.V_textfeild = QtWidgets.QTextEdit("1")
        self.V_textfeild.setFixedHeight(25)
        self.btnlayout.addWidget(self.V_textfeild)

        self.build_crv_button = QtWidgets.QPushButton("build curve")
        self.connect(self.build_crv_button, SIGNAL("clicked()"),
                    lambda: self.build_a_curve())
        self.btnlayout.addWidget(self.build_crv_button)
        self.clth_strps_button = QtWidgets.QPushButton("cloth strips")
        self.connect(self.clth_strps_button, SIGNAL("clicked()"),
                    lambda: self.build_a_cloth_short_callup())
        self.btnlayout.addWidget(self.clth_strps_button)                
        self.wrap_crv_button = QtWidgets.QPushButton("wrap curve")
        self.connect(self.wrap_crv_button, SIGNAL("clicked()"),
                    lambda: self.wirewrap())
        self.btnlayout.addWidget(self.wrap_crv_button)
        self.wre_wrp_button = QtWidgets.QPushButton("wire wrap")
        self.connect(self.wre_wrp_button, SIGNAL("clicked()"),
                    lambda: self.fastwire())
        self.btnlayout.addWidget(self.wre_wrp_button)
        self.clth_wrp_button = QtWidgets.QPushButton("cloth wrap")
        self.connect(self.clth_wrp_button, SIGNAL("clicked()"),
                    lambda: self.build_a_cloth_wrap_callup())
        self.btnlayout.addWidget(self.clth_wrp_button)                      
        self.setLayout(self.layout)
        self.show()



    def build_a_curve(self):
        '''
        creates a curve based on selected line of vertices of a mesh
        '''
        # getTopOpenGuides=cmds.ls(sl=1, fl=1)
        if len(cmds.ls(sl=1))<1:
            print "need to select some verts"
            return
        #turn on track selected if it's not on already
        getSelectPref = cmds.selectPref(q=1, tso=1)
        if getSelectPref == False:
            cmds.selectPref(tso=1)
        getTopOpenGuides = cmds.ls(os=1, fl=1)#set ordered selection which is necessary for drawing curves
        if len(getTopOpenGuides)>3:
            get_crv = self.build_a_curve_callup(getTopOpenGuides)
        else:
            get_crv = self.build_a_curve_short_callup(getTopOpenGuides)
        cmds.select(get_crv, r=1)


    def build_a_curve_callup(self, selectedObjects):
        '''
        builds a curve on more than three selected verts
        '''
        values=[]
        for each in selectedObjects:#get point values to build curve
            # transformWorldMatrix = cmds.xform(each, q=True, wd=1, t=True) 
            transformWorldMatrix=pm.PyNode(each).getPosition() 
            values.append(transformWorldMatrix)
        get_crv = cmds.curve(n=selectedObjects[0]+"_crv", d=3, p=values)       
        return get_crv 


    def build_a_curve_short_callup(self, selectedObjects):
        '''
        builds a curve on less than 4 selected verts and use a rebuild to smooth it out
        '''
        values=[]
        for each in selectedObjects:#get point values to build curve
            # transformWorldMatrix = cmds.xform(each, q=True, wd=1, t=True) 
            transformWorldMatrix=pm.PyNode(each).getPosition() 
            values.append(transformWorldMatrix)
        # values.append(transformWorldMatrix)
        # values.append(transformWorldMatrix)
        get_crv = cmds.curve(n=selectedObjects[0]+"_crv", d=3, p=values) 
        cmds.rebuildCurve(get_crv, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=7, d=3, tol=0.01)
        cmds.rebuildCurve(get_crv, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=7, d=3, tol=0.01)
        return get_crv 



    def wirewrap(self):
        '''
        creates a wirewrap based on selected objects
        '''
        getshapenode_one=[(each) for each in cmds.ls(sl=1) if cmds.listRelatives(each, c=1, type = "mesh")]
        getshapenode_two=[(each) for each in cmds.ls(sl=1) if cmds.listRelatives(each, c=1, type = "nurbsCurve")]
        cmds.wire(getshapenode_one[0], gw=0, en=1.000000, ce=0.000000, li=0.000000, w=getshapenode_two[0], dds=[(0, 20)])
        cmds.pickWalk(getshapenode_one, d="up")
        cmds.pickWalk(getshapenode_one, d="up")
        cmds.pickWalk(getshapenode_one, d="up")
        cmds.setAttr(getshapenode_two[0]+".visibility", 0)

    def fastwire(self):
        '''
        create a curve and then wire wrap mesh to resulting curve
        '''
        if len(cmds.ls(sl=1))<1:
            print "need to select some verts"
            return
        getObj = cmds.ls(sl=1, fl=1)[0].split(".")[0]
        self.build_a_curve()
        getCrv = cmds.ls(sl=1, fl=1)[0]
        cmds.select([getObj, getCrv])
        self.wirewrap()


                
    def build_a_cloth_short_callup(self):
        '''
        create an extruded mesh out of some selected verts
        '''
        if len(cmds.ls(sl=1))<1:
            print "need to select some verts"
            return
        getObj = cmds.ls(sl=1)[0].split(".")[0]
        self.build_a_curve()
        getCrv=cmds.ls(sl=1)
        cmds.select([getObj, getCrv[0]], r =1)
        getshapenode_one=[(each) for each in cmds.ls(sl=1) if cmds.listRelatives(each, c=1, s=1)]
        getshapenode_two=[(each) for each in cmds.ls(sl=1) if cmds.listRelatives(each, c=1, type = "nurbsCurve")]   
        selfU=str(self.U_textfeild)
        selfV=str(self.V_textfeild)
        cmds.nurbsToPolygonsPref(un=selfU, vn=selfV)
        getIt=cmds.ls("extCurve")
        if len(getIt)<1:
            name = "extCurve"
            xCubeMake=cmds.curve(n=name, d=1, p =[(-1.0, 0.0, 0.0), (-.5, 0.0, 0.0),(0.0, 0.0, 0.0), (.5, 0.0, 0.0), (1.0, 0.0, 0.0)])
        else:
            name=cmds.ls("extCurve")[0]  
        cmds.extrude(xCubeMake, getshapenode_two, ch=1, rn=0, po=1, et=1, ucp=1, fpt=1, upn=1, rotation=0, scale=1, rsp=1) 
        # cmds.delete()


    def build_a_cloth_wrap_callup(self):
        '''
        create an extruded mesh out of some selected verts which then creates the wrap
        '''        
        if len(cmds.ls(sl=1))<1:
            print "need to select some verts"
            return
        getObj = cmds.ls(sl=1)[0].split(".")[0]
        self.build_a_curve()
        getCrv=cmds.ls(sl=1)
        cmds.select([getObj, getCrv[0]], r =1)
        getshapenode_one=[(each) for each in cmds.ls(sl=1) if cmds.listRelatives(each, c=1, s=1)]
        getshapenode_two=[(each) for each in cmds.ls(sl=1) if cmds.listRelatives(each, c=1, type = "nurbsCurve")]   
        selfU=str(self.U_textfeild)
        selfV=str(self.V_textfeild)
        cmds.nurbsToPolygonsPref(un=selfU, vn=selfV)
        getIt=cmds.ls("extCurve")
        if len(getIt)<1:
            name = "extCurve"
            xCubeMake=cmds.curve(n=name, d=1, p =[(-1.0, 0.0, 0.0), (-.5, 0.0, 0.0),(0.0, 0.0, 0.0), (.5, 0.0, 0.0), (1.0, 0.0, 0.0)])
        else:
            name=cmds.ls("extCurve")[0]  
        cmds.extrude(xCubeMake, getshapenode_two, ch=1, rn=0, po=1, et=1, ucp=1, fpt=1, upn=1, rotation=0, scale=1, rsp=1) 
        getStrip = cmds.ls(sl=1)
        cmds.select(getObj, r=1)
        cmds.select(getStrip[0], add=1)
        cmds.CreateWrap()



