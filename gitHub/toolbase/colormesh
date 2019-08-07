

import os, sys, subprocess
import re, random
from datetime import datetime
from time import gmtime, strftime

import maya.cmds as mc


checkHoudini = os.getenv("HOUDINI_VERSION")

checkMaya = os.getenv("REZ_MAYA_VERSION")


if checkMaya != None:
    import mrig_pyqt
    from mrig_pyqt import QtCore, QtGui, QtWidgets
    from mrig_pyqt.QtCore import SIGNAL


if checkHoudini != None:
    import hutil
    from hutil.Qt import QtCore, QtWidgets, QtWidgets
    from hutil.Qt.QtCore import SIGNAL


color_select = ['Apply', 'Grey' , 'Red' , 'Green' , 'Blue' ,'Teal' ,'Yellow' ,'Purple' ,'Random' ,'Dark' ,'Light' ,'slight grey' ,'save gamut']

class set_colors_win(QtWidgets.QWidget):
    # def __init__(self): 
    def __init__(self):
        super(set_colors_win, self).__init__()
        self.initUI()

    def initUI(self):    

        self.setWindowTitle("set colors")

        self.myform = QtWidgets.QFormLayout()
        self.layout = QtWidgets.QGridLayout()

        self.colorSetupLayout = QtWidgets.QGridLayout()
        self.colorOverride = QtWidgets.QFrame()
        self.colorOverride.setLayout(self.colorSetupLayout)
        self.colorSetupLayout.addLayout(self.myform, 0,0,1,1)
        self.layout.addLayout(self.colorSetupLayout, 0,0,1,1)

        self.add_widgets()

        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(self.colorOverride)
        scroll.setWidgetResizable(False)
        self.layout.addWidget(scroll, 1,0,1,1)
        self.setLayout(self.layout)

    def add_widgets(self):
        self.color_dial = QtWidgets.QComboBox()
        self.color_dial.addItems(color_select)
        self.vertical_order_layout_ta = QtWidgets.QHBoxLayout()
        self.myform.addRow(self.vertical_order_layout_ta) 
        self.vertical_order_layout_ta.addWidget(self.color_dial)
        self.prnt_verbose_button = QtWidgets.QPushButton("Go")
        self.connect(self.prnt_verbose_button, SIGNAL("clicked()"),
                    lambda: self.create_rgb())
        self.vertical_order_layout_ta.addWidget(self.prnt_verbose_button)     



    def create_rgb(self):
        color_load=self.color_dial
        color_name=color_load.currentText()
        if color_name==color_select[0]:
            self._apply_colors()
        if color_name==color_select[1]:
            self._change_primary_gry()
        if color_name==color_select[2]:
            self._change_primary_red()
        if color_name==color_select[3]:
            self._change_primary_grn()
        if color_name==color_select[4]:
            self._change_primary_blue()
        if color_name==color_select[5]:
            self._change_primary_teal()
        if color_name==color_select[6]:
            self._change_primary_orange()
        if color_name==color_select[7]:
            self._change_primary_prpl()
        if color_name==color_select[8]:
            self._change_colors()
        if color_name==color_select[9]:
            self._change_darker()
        if color_name==color_select[10]:
            self._change_lighter()
        if color_name==color_select[11]:
            self._slight_to_gry()            
        if color_name==color_select[12]:
            self.save_gamut()     


    def _apply_colors(self):
        getgrp = mc.ls(sl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        for each in getgrp:
            name = each+"_shd"
            FVfirst = mc.shadingNode('lambert', asShader=True, n=name)
            getFVfirst=[FVfirst]
            setName="techanim_textures" 
            if mc.objExists(setName):
                pass
            else:
                mc.sets(n=setName, co=3)
            mc.sets(getFVfirst, add=setName)
            mc.select(each)
            mc.hyperShade(assign=str(FVfirst))
            mc.setAttr(name+".color", random.uniform(0.0,1.0), random.uniform(0.0,1.0), random.uniform(0.0,1.0), type="double3")
        mc.select(getgrp, r=1)        

    def _apply_grey_colors(self):
        getgrp = mc.ls(sl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        for each in getgrp:
            name = each+"_shd"
            FVfirst = mc.shadingNode('lambert', asShader=True, n=name)
            getFVfirst=[FVfirst]
            setName="techanim_textures" 
            if mc.objExists(setName):
                pass
            else:
                mc.sets(n=setName, co=3)
            mc.sets(getFVfirst, add=setName)
            mc.select(each)
            mc.hyperShade(assign=str(FVfirst))
            getval = random.uniform(0.0,1.0)
            mc.setAttr(name+".color", getval, getval, getval, type="double3")
        mc.select(getgrp, r=1)        

    def get_geo_techanim(self):
        get_tech=mc.ls("*:*_tech_geo")
        get_tech_two=mc.ls("*_tech_geo")
        get_posttech=mc.ls("*:*_postTech_geo")
        get_posttech_two=mc.ls("*_postTech_geo")
        get_geo=get_tech+get_tech_two+get_posttech+get_posttech_two
        mc.select(get_geo, r=1)
        self._apply_colors()

    def _change_colors(self):
        getgrp = mc.ls(sl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        mc.hyperShade (getgrp[0], smn=1)
        for each in mc.ls(sl = 1):
            mc.setAttr(each+".color", random.uniform(0.0,1.0), random.uniform(0.0,1.0), random.uniform(0.0,1.0), type="double3")
        mc.select(getgrp, r=1)      

    def _change_primary_gry(self):
        getgrp = mc.ls(sl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        mc.hyperShade (getgrp[0], smn=1)
        for each in mc.ls(sl = 1):
            getval = random.uniform(0.0,1.0)
            mc.setAttr(each+".color", getval, getval, getval, type="double3")
        mc.select(getgrp, r=1)    

    def _slight_to_gry(self):
        getgrp = mc.ls(sl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        mc.hyperShade (getgrp[0], smn=1)
        for each in mc.ls(sl = 1):
            getval = mc.getAttr(each+".color")
            getvallow = random.uniform(getval[0][0],getval[0][2])
            mc.setAttr(each+".color", getvallow, getvallow, getvallow, type="double3")
        mc.select(getgrp, r=1) 


    def _change_primary_grn(self):
        getgrp = mc.ls(sl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        mc.hyperShade (getgrp[0], smn=1)
        for each in mc.ls(sl = 1):
            getval = random.uniform(0.0,1.0)
            getvallow = random.uniform(0.0,0.25)
            mc.setAttr(each+".color", getvallow, getval, getvallow, type="double3")
        mc.select(getgrp, r=1)     


    def _change_primary_red(self):
        getgrp = mc.ls(sl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        mc.hyperShade (getgrp[0], smn=1)
        for each in mc.ls(sl = 1):
            getvallow = random.uniform(0.0,0.25)
            getval = random.uniform(0.0,1.0)
            mc.setAttr(each+".color", getval, getvallow, getvallow, type="double3")
        mc.select(getgrp, r=1)     


    def _change_primary_blue(self):
        getgrp = mc.ls(sl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        mc.hyperShade (getgrp[0], smn=1)
        for each in mc.ls(sl = 1):
            getvallow = random.uniform(0.0,0.25)
            getval = random.uniform(0.0,1.0)
            mc.setAttr(each+".color", getvallow, getvallow, getval, type="double3")
        mc.select(getgrp, r=1)     

    def _change_primary_teal(self):
        getgrp = mc.ls(sl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        mc.hyperShade (getgrp[0], smn=1)
        for each in mc.ls(sl = 1):
            getvallow = random.uniform(0.0,0.25)
            getval = random.uniform(0.0,1.0)
            mc.setAttr(each+".color", getvallow, getval, getval, type="double3")
        mc.select(getgrp, r=1) 

    def _change_primary_orange(self):
        getgrp = mc.ls(sl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        mc.hyperShade (getgrp[0], smn=1)
        for each in mc.ls(sl = 1):
            getvallow = random.uniform(0.0,0.25)
            getval = random.uniform(0.0,1.0)
            mc.setAttr(each+".color", getval, getval, getvallow, type="double3")
        mc.select(getgrp, r=1) 

    def _change_primary_prpl(self):
        getgrp = mc.ls(sl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        mc.hyperShade (getgrp[0], smn=1)
        for each in mc.ls(sl = 1):
            getvallow = random.uniform(0.0,0.25)
            getval = random.uniform(0.0,1.0)
            mc.setAttr(each+".color", getval, getvallow, getval, type="double3")
        mc.select(getgrp, r=1) 

    def _change_darker(self):
        getgrp = mc.ls(sl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        mc.hyperShade (getgrp[0], smn=1)
        for each in mc.ls(sl = 1):
            getval = mc.getAttr(each+".color")
            getvallow = random.uniform(0.0,0.25)
            newval = getval[0][0]-getvallow, getval[0][1]-getvallow, getval[0][2]-getvallow
            mc.setAttr(each+".color", newval[0], newval[1], newval[2], type="double3")
        mc.select(getgrp, r=1) 

    def _change_lighter(self):
        getgrp = mc.ls(sl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        mc.hyperShade (getgrp[0], smn=1)
        for each in mc.ls(sl = 1):
            getval = mc.getAttr(each+".color")
            getvallow = random.uniform(0.0,0.25)
            newval = getval[0][0]+getvallow, getval[0][1]+getvallow, getval[0][2]+getvallow
            mc.setAttr(each+".color", newval[0], newval[1], newval[2], type="double3")
        mc.select(getgrp, r=1) 

    def _change_grey(self):
        getgrp = mc.ls(sl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        mc.hyperShade (getgrp[0], smn=1)
        for each in mc.ls(sl = 1):
            getval = random.uniform(0.0,1.0)
            mc.setAttr(each+".color", getval, getval, getval, type="double3")
        mc.select(getgrp, r=1)     

    def _change_ambient(self):
        getgrp = mc.ls(sl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        mc.hyperShade (getgrp[0], smn=1)
        for each in mc.ls(sl = 1):
            get_float = random.uniform(0.0,1.0)
            mc.setAttr(each+".incandescence", get_float, get_float, get_float, type="double3")
        mc.select(getgrp, r=1)  

inst_mkwin=set_colors_win()
inst_mkwin.show()





