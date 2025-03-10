import os, subprocess, sys, platform, logging, signal, webbrowser, urllib, re, getpass, datetime, glob, random, numpy
import maya.cmds as mc
import maya.mel
import pymel.core as pm
from numpy import arange
from functools import partial
from os  import popen
from sys import stdin
from random import randint
from sys import argv

#import PyQt4
#from PyQt4 import QtCore, QtGui, Qt
#from PyQt4.QtGui import QWidget, QRadioButton, QGridLayout, QLabel, \
#    QTableWidget, QComboBox, QKeySequence, QToolButton, QPlainTextEdit, QPushButton,QBoxLayout, \
#    QClipboard, QTableWidgetItem, QCheckBox, QVBoxLayout, QHBoxLayout, \
#    QPixmap, QLineEdit, QListWidget, QTextEdit, QSizePolicy, QFrame, QPalette, QColor, \
#    QFont, QAbstractItemView, QMenu, QMessageBox
#from PyQt4.QtCore import SIGNAL
 
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets

detailMessge = ['X', 'Y', 'Z', 'XY', 'XZ', 'YZ']
class plotter_UI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(plotter_UI, self).__init__(parent = None)

        self.setWindowTitle("Plotter Window 2.0")
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
        self.layout.addLayout(self.SelectionSetupLayout, 0,0,1,1)        self.add_widgets()

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

        self.plot_obj_button = QtWidgets.QPushButton("Plot Object")
        self.plot_obj_button.clicked.connect(lambda: self._plotmattrix())
        self.plot_button_layout.addWidget(self.plot_obj_button)
        self.plot_ea_button = QtWidgets.QPushButton("Plot Each")
        self.plot_ea_button.clicked.connect(lambda: self._plot_each_vert())
        self.plot_button_layout.addWidget(self.plot_ea_button)  
        self.plot_vtx_button = QtWidgets.QPushButton("Plot Vert")
        self.plot_vtx_button.clicked.connect(lambda: self._plotter())
        self.plot_button_layout.addWidget(self.plot_vtx_button)        
        self.plot_ave_button = QtWidgets.QPushButton("Plot Averages")
        self.plot_ave_button.clicked.connect(lambda: self._plotter_avrg())
        self.plot_button_layout.addWidget(self.plot_ave_button)

        self.onion_button = QtWidgets.QPushButton("Onion")
        self.onion_button.clicked.connect(lambda: self._onion_skin())
        self.plot_button_layout.addWidget(self.onion_button)  
        self.loc_button = QtWidgets.QPushButton("Locate each")
        self.loc_button.clicked.connect(lambda: self.locator_select_verts())
        self.plot_button_layout.addWidget(self.loc_button)   

        self.loc_mas_button = QtWidgets.QPushButton("Locate Mass")
        self.loc_mas_button.clicked.connect(lambda: self.locator_selected_mass())
        self.plot_button_layout.addWidget(self.loc_mas_button)  

        self.lu_button = QtWidgets.QPushButton("lineup")
        self.lu_button.clicked.connect(lambda: self.aim_obj())
        self.plot_button_layout.addWidget(self.lu_button)

        self.mm_button = QtWidgets.QPushButton("Match Matrix")
        self.mm_button.clicked.connect(lambda: self.xformmove())
        self.plot_button_layout.addWidget(self.mm_button) 

        self.mo_button = QtWidgets.QPushButton("Match Orient")
        self.mo_button.clicked.connect(lambda: self.xformrot())
        self.plot_button_layout.addWidget(self.mo_button) 

        self.mm_button = QtWidgets.QPushButton("Match Pivot")
        self.mm_button.clicked.connect(lambda: self.matchpivot())
        self.plot_button_layout.addWidget(self.mm_button) 

        self.dm_button = QtWidgets.QPushButton("Dup Move")
        self.dm_button.clicked.connect(lambda: self.duplicateMove())
        self.plot_button_layout.addWidget(self.dm_button) 

        self.mm_xx_button = QtWidgets.QPushButton("Mirror Matrix +X--X")
        self.mm_xx_button.clicked.connect(lambda: self.xform_mirror_move())
        self.plot_button_layout.addWidget(self.mm_xx_button) 


        self.mc_button = QtWidgets.QPushButton("Mirror Create +X--X")
        self.mc_button.clicked.connect(lambda: self.xform_mirror_create())
        self.plot_button_layout.addWidget(self.mc_button) 

        self.rst_orig_button = QtWidgets.QPushButton("Set to Origin")
        self.rst_orig_button.clicked.connect(lambda: self.xform_set_origin())
        self.plot_button_layout.addWidget(self.rst_orig_button) 

        self.rst_obj_button = QtWidgets.QPushButton("Set to Obj")
        self.rst_obj_button.clicked.connect(lambda: self.xform_set_to_sel())
        self.plot_button_layout.addWidget(self.rst_obj_button) 

        self.rst_button = QtWidgets.QPushButton("Reset transforms")
        self.rst_button.clicked.connect(lambda: self.xform_reset_move())
        self.plot_button_layout.addWidget(self.rst_button) 

        self.dpcnst_button = QtWidgets.QPushButton("Dupe Constraint")
        self.dpcnst_button.clicked.connect(lambda: self.dup_cnst())
        self.plot_button_layout.addWidget(self.dpcnst_button) 

        self.vert_align_label = QtWidgets.QLabel("Vertice Align")        
        self.plot_slider_layout.addWidget(self.vert_align_label)

        self.reshape_edge_button = QtWidgets.QPushButton("Reshape to Edge")
        self.reshape_edge_button.clicked.connect(lambda: self.matchCurveShapes())
        self.plot_button_layout.addWidget(self.reshape_edge_button) 

        self.reshape_shape_button = QtWidgets.QPushButton("Reshape to Shape")
        self.reshape_shape_button.clicked.connect(lambda: self.matchFullShape())
        self.plot_button_layout.addWidget(self.reshape_shape_button)

        self.int_fix_button = QtWidgets.QPushButton("Intersection Fix")
        self.int_fix_button.clicked.connect(lambda: self.shrink_intersections())
        self.plot_button_layout.addWidget(self.int_fix_button)  


        self.transform_c_button = QtWidgets.QPushButton("Transform Cache")
        self.transform_c_button.clicked.connect(lambda: self.offset_cache_static())
        self.plot_button_layout.addWidget(self.transform_c_button)  

       self.off_c_button = QtWidgets.QPushButton("Offset Cache")
        self.off_c_button.clicked.connect(lambda: self.offset_cache())
        self.plot_button_layout.addWidget(self.off_c_button)  

        self.strLayout = QtWidgets.QGridLayout()
        self.strFrame = QtWidgets.QFrame()
        self.strFrame.setStyleSheet("color: #ccaaff; background-color: rgba(100,70,70,50);")
        # self.strFrame.setStyleSheet("color: #ccaaff; background-color: rgba(255,255,255,12);")
        self.strFrame.setLayout(self.strLayout)
        self.plot_slider_layout.addWidget(self.strFrame)


        self.strengthlabel = QtWidgets.QLabel("Strength")
        self.strLayout.addWidget(self.strengthlabel)
        self.strengthNum = QtWidgets.QLineEdit("100%")
        self.strengthNum.textChanged.connect(self.set_str_slider)
        # self.strengthNum.clicked.connect(self.strengthNum,QtCore.SIGNAL("returnPressed()"),self.set_str_slider)
        self.strLayout.addWidget(self.strengthNum)
        self.strength_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal) 
        self.strength_slider.setMinimum(1)
        self.strength_slider.setMaximum(100)
        self.strength_slider.setValue(100)        
        self.strength_slider.setTickInterval(5)
        self.strength_slider.setTickPosition(self.strength_slider.TicksBelow)
        self.strength_slider.valueChanged.connect(self.print_str_slider)
        self.strLayout.addWidget(self.strength_slider)  


        self.biasLayout = QtWidgets.QGridLayout()
        self.biasFrame = QtWidgets.QFrame()
        self.biasFrame.setStyleSheet("color: #ffccaa; background-color: rgba(70,100,70,50);")
        # self.biasFrame.setStyleSheet("color: #aaccff; background-color: rgba(255,255,255,12);")
        self.biasFrame.setLayout(self.biasLayout)
        self.plot_slider_layout.addWidget(self.biasFrame)


        self.biaslabel = QtWidgets.QLabel("Bias")        
        self.biasLayout.addWidget(self.biaslabel)
        self.biasNum = QtWidgets.QLineEdit("50%")
        self.strengthNum.textChanged.connect(self.set_str_slider)
        # self.biasNum.clicked.connect(self.biasNum,QtCore.SIGNAL("returnPressed()"),self.set_bias_slider)
        # self.biasNum.valueChanged.connect(self.set_bias_slider)
        self.biasLayout.addWidget(self.biasNum)
        self.bias_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.bias_slider.setMinimum(1)
        self.bias_slider.setMaximum(100)
        self.bias_slider.setValue(50)        
        self.bias_slider.setTickInterval(5)
        self.bias_slider.setTickPosition(self.bias_slider.TicksBelow)
        # self.bias_slider.valueChanged.clicked.connect(self.print_bias_slider)
        self.bias_slider.valueChanged.connect(self.print_bias_slider)
        self.biasLayout.addWidget(self.bias_slider) 
        self.driftLayout = QtWidgets.QGridLayout()
        self.driftFrame = QtWidgets.QFrame()
        self.driftFrame.setStyleSheet("color: #aaccff; background-color: rgba(70,70,100,50);")
        # self.driftFrame.setStyleSheet("color: #ffccaa; background-color: rgba(255,255,255,12);")
        self.driftFrame.setLayout(self.driftLayout)
        self.plot_slider_layout.addWidget(self.driftFrame)

        self.driftlabel = QtWidgets.QLabel("Drift")        
        self.driftLayout.addWidget(self.driftlabel)                
        self.driftNum = QtWidgets.QLineEdit("0%")
        self.driftNum.textChanged.connect(self.set_drift_slider)
        # self.driftNum.clicked.connect(self.driftNum,QtCore.SIGNAL("returnPressed()"),self.set_drift_slider)
        self.driftLayout.addWidget(self.driftNum)
        self.drift_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal) 
        self.drift_slider.setMinimum(1)
        self.drift_slider.setMaximum(100)
        self.drift_slider.setValue(0)        
        self.drift_slider.setTickInterval(5)
        self.drift_slider.setTickPosition(self.drift_slider.TicksBelow)
        # self.drift_slider.valueChanged.clicked.connect(self.print_drift_slider)
        self.drift_slider.valueChanged.connect(self.print_drift_slider)
        self.driftLayout.addWidget(self.drift_slider)   


        self.aligning = QtWidgets.QComboBox()
        self.aligning.addItems(detailMessge)
        self.plot_slider_layout.addWidget(self.aligning)
        self.align_button = QtWidgets.QPushButton("Align")
        self.align_button.clicked.connect(lambda: self._offset_verts())
        self.plot_slider_layout.addWidget(self.align_button)      
        self.align_mass_button = QtWidgets.QPushButton("Align Mass")
        self.align_mass_button.clicked.connect(lambda: self._offset_verts_mass())
        self.plot_slider_layout.addWidget(self.align_mass_button)  

    def selection_grab(self):
        '''--------------------------------------------------------------------------------------------------------------------------------------
        Common selection query
        --------------------------------------------------------------------------------------------------------------------------------------'''        
        getSel=mc.ls(sl=1, fl=1)
        if getSel:
            pass
        else:
            print "You need to make a selection for this tool to operate on."
            return
        return getSel

    def _plotter_avrg(self):
        self.plotter_avrg()
        
    def _plotter(self):
        self.plot_vert()

    def _plotmattrix(self):
        self.plot_matrix()

    def _offset_verts(self):
        strn = self.strength_slider.value()
        strength = float(strn) *.01
        amnt = self.drift_slider.value()
        amount = float(amnt) *.01
        bias = self.bias_slider.value()
        biases = float(bias) *.01   
        directn=self.aligning
        direction = str(directn.currentText())
        self.space_vert(strength, amount, direction, biases)

    def _offset_verts_mass(self):
        strn = self.strength_slider.value()
        strength = float(strn) *.01
        amnt = self.drift_slider.value()
        amount = float(amnt) *.01
        bias = self.bias_slider.value()
        biases = float(bias) *.01 
        directn=self.aligning
        direction = str(directn.currentText())        
        self.space_vert(strength, amount, direction, biases)
    def _plot_each_vert(self):
        self.plot_each_vert()

    def _onion_skin(self):
        self.onionSkin()      

    def matchCurveShapes(self):
        self.CurveShapes()

    def matchFullShape(self):
        getFirstGrp, getSecondGrp=self.CurveShapes()
        self.matchCurveShapes_andShrinkWrap(getFirstGrp, getSecondGrp)

    def onionSkin(self):
        selObj=mc.ls(sl=1, fl=1)       
        if len(selObj)==1:
            pass
        else:
            print "Select 1 object" 
        getRange=mc.playbackOptions(q=1, max=1)#get framerange of scene to set keys in iteration 
        getRange=int(getRange)#change framerange to an integer. May have to change this to a float iterator on a half key blur(butterfly wings)
        for each in range(getRange):
            for item in selObj:
                getloc=mc.spaceLocator(n=item+"cnstr_lctr")
                mc.normalConstraint(item, getloc[0])
                getNum="%04d" % (each,)
                placeloc=mc.spaceLocator(n=item+'FR'+str(getNum)+"_lctr")
                transform=mc.xform(item, q=True, ws=1, t=True)
                mc.xform(getloc[0], ws=1, t=transform)  
                mc.SetKeyTranslate(getloc[0])
                mc.xform(placeloc[0], ws=1, t=transform)
                mc.SetKeyTranslate(placeloc[0])               
                rotate=mc.xform(getloc[0], q=True, ws=1, ro=True)
                mc.xform(placeloc[0], ws=1, ro=rotate)  
                mc.SetKeyRotate(placeloc[0])
                maya.mel.eval( "playButtonStepForward;" )
                mc.delete(getloc[0])

    def plot_each_vert(self):
        '''plots a locator to a vertice or face per keyframe in a timeline'''
        selObj=mc.ls(sl=1, fl=1)
        for item in selObj:
            mc.select(item, r=1)
            self.plot_vert()
    def plotter_avrg(self):
        '''plots a locator to a vertice or face per keyframe in a timeline'''
        selObj=mc.ls(sl=1, fl=1)      
        if len(selObj)>0:
            pass
        else:
            print "Select 1 object" 
            return     
        getTopRange=mc.playbackOptions(q=1, max=1)+1#get framerange of scene to set keys in iteration 
        getLowRange=mc.playbackOptions(q=1, min=1)-1#get framerange of scene to set keys in iteration 
        edgeBucket=[]
        getRange=arange(getLowRange,getTopRange, 1 )
        getloc=mc.spaceLocator(n=selObj[0]+"cnstr_lctr")
        mc.normalConstraint(selObj[0], getloc[0])
        placeloc=mc.spaceLocator(n=selObj[0]+"lctr")
        for each in getRange:
            mc.currentTime(each)            
            transform=mc.xform(selObj, q=1, ws=1, t=1)
            posBucketx=self.array_median_find(transform[0::3])
            posBuckety=self.array_median_find(transform[1::3])
            posBucketz=self.array_median_find(transform[2::3])
            mc.xform(getloc[0], ws=1, t=(posBucketx, posBuckety, posBucketz))  
            mc.SetKeyTranslate(getloc[0])
            mc.xform(placeloc[0], ws=1, t=(posBucketx, posBuckety, posBucketz))
            mc.SetKeyTranslate(placeloc[0])               
            rotate=mc.xform(getloc[0], q=True, ws=1, ro=True)
            mc.xform(placeloc[0], ws=1, ro=rotate)  
            mc.SetKeyRotate(placeloc[0])
            mc.currentTime(each)
        mc.delete(getloc[0])
        return placeloc[0]

    def plot_vert(self):
        '''plots a locator to a vertice or face per keyframe in a timeline'''
        selObj=mc.ls(sl=1, fl=1)      
        if len(selObj)>0:
            pass
        else:
            print "Select 1 object" 
            return     
        getTopRange=mc.playbackOptions(q=1, max=1)+1#get framerange of scene to set keys in iteration 
        getLowRange=mc.playbackOptions(q=1, min=1)-1#get framerange of scene to set keys in iteration 
        edgeBucket=[]
        getRange=arange(getLowRange,getTopRange, 1 )
        getloc=mc.spaceLocator(n=selObj[0]+"cnstr_lctr")
        mc.normalConstraint(selObj[0], getloc[0])
        placeloc=mc.spaceLocator(n=selObj[0]+"lctr")
        for each in getRange:
            mc.currentTime(each)            
            transform=mc.xform(selObj[0], q=True, ws=1, t=True)
            if len(transform)<4:
                pass
            else:
                posBucket=[]
                posBucket.append(self.median_find(transform[0::3]))
                posBucket.append(self.median_find(transform[1::3]))
                posBucket.append(self.median_find(transform[2::3]))
                transform=posBucket
            mc.xform(getloc[0], ws=1, t=transform)  
            mc.SetKeyTranslate(getloc[0])
            mc.xform(placeloc[0], ws=1, t=transform)
            mc.SetKeyTranslate(placeloc[0])               
            rotate=mc.xform(getloc[0], q=True, ws=1, ro=True)
            mc.xform(placeloc[0], ws=1, ro=rotate)  
            mc.SetKeyRotate(placeloc[0])
            mc.currentTime(each)
        mc.delete(getloc[0])


    def _plotter_avrg(self):
        '''plots a locator to a vertice or face per keyframe in a timeline'''
        selObj=mc.ls(sl=1, fl=1)      
        if len(selObj)>0:
            pass
        else:
            print "Select 1 object" 
            return     
        getTopRange=mc.playbackOptions(q=1, max=1)+1#get framerange of scene to set keys in iteration 
        getLowRange=mc.playbackOptions(q=1, min=1)-1#get framerange of scene to set keys in iteration 
        edgeBucket=[]
        getRange=arange(getLowRange,getTopRange, 1 )
        getloc=mc.spaceLocator(n=selObj[0]+"cnstr_lctr")
        mc.normalConstraint(selObj[0], getloc[0])
        placeloc=mc.spaceLocator(n=selObj[0]+"lctr")
        for each in getRange:            mc.currentTime(each)            
            transform=mc.xform(selObj, q=1, ws=1, t=1)
            posBucketx=self.array_median_find(transform[0::3])
            posBuckety=self.array_median_find(transform[1::3])
            posBucketz=self.array_median_find(transform[2::3])
            mc.xform(getloc[0], ws=1, t=(posBucketx, posBuckety, posBucketz))  
            mc.SetKeyTranslate(getloc[0])
            mc.xform(placeloc[0], ws=1, t=(posBucketx, posBuckety, posBucketz))
            mc.SetKeyTranslate(placeloc[0])               
            rotate=mc.xform(getloc[0], q=True, ws=1, ro=True)
            mc.xform(placeloc[0], ws=1, ro=rotate)  
            mc.SetKeyRotate(placeloc[0])
            mc.currentTime(each)            

    def median_find(self, lst):
        even = (0 if len(lst) % 2 else 1) + 1
        half = (len(lst) - 1) / 2
        mysum= sum(sorted(lst)[half:half + even]) / float(even)
        return mysum

    def array_median_find(self, lst):
        mysum=numpy.median(numpy.array(lst))
        return mysum            

    def space_vert(self, strength, amount, direction, bias):
        '''offsets a vert from another'''
        strength=float(strength)
        amount=float(amount)
        bias=float(bias)
        selObj=mc.ls(sl=1, fl=1)   
        firstpart, secondpart = selObj[:len(selObj)/2], selObj[len(selObj)/2:]
        print firstpart, secondpart
        if len(firstpart)==len(secondpart):
            pass
        else:
            print "Odd number in length. Please pick exactly same amount of verts between two rows"
            return        for leadingVert, followVert in map(None, firstpart, secondpart):
            mc.select(leadingVert, r=1)
            mc.select(followVert, add=1)
            getfirst=mc.ls(sl=1)[0]
            getsecond=mc.ls(sl=1)[1]
            transform=mc.xform(getfirst, q=True, ws=1, t=True)
            transform_follvert=mc.xform(getsecond, q=True, ws=1, t=True)
            #calc x
            xsum = transform[0]-transform_follvert[0]
            startxsum = xsum*bias
            differencesum = 1.0 - bias
            addedsum=xsum*differencesum
            move_xfollow = transform_follvert[0] + startxsum * strength
            move_xlead = transform[0] - addedsum * strength
            ysum = transform[1]-transform_follvert[1]
            startysum = ysum*bias
            differenceysum = 1.0 - bias
            addedysum=ysum*differenceysum 
            move_yfollow = transform_follvert[1] + startysum * strength
            move_ylead = transform[1] - addedysum * strength            
            zsum = transform[2]-transform_follvert[2]
            startzsum = zsum*bias
            differencezsum = 1.0 - bias
            addedzsum=zsum*differencezsum
            move_zfollow = transform_follvert[2] + startzsum * strength
            move_zlead = transform[2] - addedzsum * strength    
            mc.move(move_xfollow, move_yfollow, move_zfollow, followVert, ws=1)
            mc.move(move_xlead, move_ylead, move_zlead, leadingVert, ws=1)
            if direction=="X":
                mc.move(amount, 0.0, 0.0, followVert, r=1, ls=1)
            if direction=="Y":
                mc.move(0.0, amount, 0.0, followVert, r=1, ls=1)
            if direction=="Z":
                mc.move(0.0, amount, 0.0, followVert, r=1, ls=1)
            if direction=="XY":
                mc.move(amount,amount, 0.0, followVert, r=1, ls=1)
            if direction=="XZ":
                mc.move(amount, 0.0, amount, followVert, r=1, ls=1)
            if direction=="YZ":
                mc.move(0.0, amount, amount, followVert, r=1, ls=1)
    def plot_matrix(self):
        selObj=mc.ls(sl=1, fl=1)      
        if len(selObj)>0:
            pass
        else:
            print "Select 1 object" 
        getTopRange=mc.playbackOptions(q=1, max=1)+1#get framerange of scene to set keys in iteration 
        getLowRange=mc.playbackOptions(q=1, min=1)-1#get framerange of scene to set keys in iteration 
        edgeBucket=[]
        getRange=arange(getLowRange,getTopRange, 1 )
        getloc=mc.spaceLocator(n=selObj[0]+"cnstr_lctr")
        for each in getRange:
            mc.currentTime(each)            
            matrix=mc.xform(selObj[0], q=1, ws=1, m=1)
            mc.xform(getloc[0], ws=1, m=matrix)       
            mc.SetKeyTranslate(getloc[0])          
            mc.SetKeyRotate(getloc[0])
            mc.currentTime(each)

    def aim_obj(self, arg=None):
        selObj=mc.ls(sl=1, fl=1)
        par_const = selObj[-1]
        if len(mc.ls(sl=1))>1:
            pass
        else:
            print "select more than one object for lineup. If adding many, select the driving aim object last"
            pass
        for each in selObj[:-1]:
            cret_cnst = mc.aimConstraint(par_const, each)
            mc.delete(cret_cnst)

    def locator_selected_mass(self, arg=None):
        selObj=mc.ls(sl=1, fl=1)
        # transform=mc.xform(selObj, q=1, ws=1, t=1)
        bucket_x = []
        bucket_y = []
        bucket_z = []
        bucketlist = []
        for each in selObj:
            transformWorldMatrix, rotateWorldMatrix=self.locationXForm(each)
            bucket_x.append(transformWorldMatrix[0])
            bucket_y.append(transformWorldMatrix[1])
            bucket_z.append(transformWorldMatrix[2])            
        posBucketx=self.median_find(bucket_x)
        posBuckety=self.median_find(bucket_y)
        posBucketz=self.median_find(bucket_z)
        getLoc=mc.spaceLocator()
        mc.xform(getLoc[0], t=(posBucketx, posBuckety, posBucketz))
        get_const = mc.normalConstraint(selObj[0], getLoc[0])
        mc.delete(get_const)
        return getLoc[0]    def dup_cnst(self, each):
        getSel=mc.ls(sl=1, fl=1)
        parentObj=getSel[0]
        for number, each in enumerate(getSel[1:]):
            if ":" in each:
                newname = each.split(":")[-1]
            else:
                newname = each
            rname = newname+'_poly'
            newObj=mc.duplicate(parentObj,n=rname)
            mc.parentConstraint(each, newObj) 



    def duplicateMove(self):
        getSel=cmds.ls(sl=1, fl=1)
        parentObj=getSel[0]
        for number, each in enumerate(getSel[1:]):
            getParent=cmds.listRelatives(each, p=1)  
            getobj=cmds.ls(each)
            transformWorldMatrix = cmds.xform(each, q=True, wd=1, t=True)
            rotateWorldMatrix = cmds.xform(each, q=True, ws=1, ro=True)
            newObj=cmds.duplicate(parentObj,n=parentObj+str(number))
            cmds.xform(newObj[0], ws=1, t=transformWorldMatrix)
            cmds.xform(newObj[0], ws=1, ro=rotateWorldMatrix)  


    def locationXForm(self, each):
        # getObj=mc.ls(each)
        #transform=getObj.getTranslation()
        transform=mc.xform(each , q=True, ws=1, t=True)
        if transform==[0.0, 0.0, 0.0]:
            transformWorldMatrix=each.getScalePivot(ws=1)[:3]
            # transformWorldMatrix=getObj.getScalePivot(ws=1)[:3]
            rotateWorldMatrix = mc.xform(each, q=True, wd=1, ra=True)
        else:
            transformWorldMatrix = mc.xform(each, q=True, ws=1, t=True)
            rotateWorldMatrix = mc.xform(each, q=True, ws=1, ro=True)
        return transformWorldMatrix, rotateWorldMatrix
    def locator_select_verts(self, arg=None):
        selObj=mc.ls(sl=1, fl=1)
        if len(selObj) >0:
            for each in selObj:
                print each
                transformWorldMatrix, rotateWorldMatrix=self.locationXForm(each)
                # transform=mc.xform(each, q=1, ws=1, t=1)
                # rotate_trns=mc.xform(selObj, q=1, ws=1, rp=1)
                # transformWorldMatrix = mc.xform(each, q=True, wd=1, sp=True)  
                # rotateWorldMatrix = mc.xform(each, q=True, wd=1, ra=True) 
                rotate=mc.xform(selObj[0], q=True, ws=1, ro=True)
                getLoc=mc.spaceLocator(n=str(each)+"_loc")
                mc.xform(getLoc[0], t=(transformWorldMatrix))                
                # mc.xform(getLoc[0], ro=(rotate))
                get_const = mc.normalConstraint(each, getLoc[0])
                mc.delete(get_const)                
        elif len(selObj)<1:
            print "select one or more vertices"
            pass               
        return getLoc[0]



    def locator_select_vertsv1(self, arg=None):
        selObj=mc.ls(sl=1, fl=1)
        if len(selObj) == 1:
            # transform=mc.xform(selObj, q=1, bb=1)
            # transform=mc.xform(selObj, q=1, ws=1, t=1)
            transformWorldMatrix, rotateWorldMatrix=self.locationXForm(selObj)
            posBucketx=self.median_find(transformWorldMatrix[0::3])
            posBuckety=self.median_find(transformWorldMatrix[1::3])
            posBucketz=self.median_find(transformWorldMatrix[2::3])
            getLoc=mc.spaceLocator(n=str(selObj[0])+"_loc")
            mc.xform(getLoc[0], t=(posBucketx, posBuckety, posBucketz))
        elif len(selObj)<1:
            print "select one or more vertices"
            pass        else:
            for each in selObj:
                print each
                transformWorldMatrix, rotateWorldMatrix=self.locationXForm(selObj)
                getLoc=mc.spaceLocator(n=str(each)+"_loc")
                mc.xform(getLoc[0], t=(transformWorldMatrix))                
        return getLoc[0]


    def helpWin(self, stringField):
        '''--------------------------------------------------------------------------------------------------------------------------------------
        Interface Layout
        --------------------------------------------------------------------------------------------------------------------------------------'''
        # def helpPage(self, arg=None):
        winName = "Description"
        winTitle = winName
        if mc.window(winName, exists=True):
                deleteUI(winName)
        window = mc.window(winName, title=winTitle, tbm=1, w=700, h=400 )
        mc.menuBarLayout(h=30)
        mc.rowColumnLayout  (' selectArrayRow ', nr=1, w=700)
        mc.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        mc.rowLayout  (' rMainRow ', w=700, numberOfColumns=6, p='selectArrayRow')
        mc.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        mc.setParent ('selectArrayColumn')
        mc.gridLayout('txvaluemeter', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(700, 400))
        self.list=mc.scrollField( editable=False, wordWrap=True, ebg=1,bgc=[0.11, 0.15, 0.15], w=700, text=str(stringField))
        mc.showWindow(window)

    def offset_cache(self):
        checkSel = mc.ls(sl=1)
        if len(checkSel)<2:
            print "you need to select two objects"
        leader = checkSel[1]
        mc.select(leader, r=1)
        mc.ConvertSelectionToVertices(leader)
        ld_lctr = self.plotter_avrg()
        follower = checkSel[0]
        mc.select(follower, r=1)
        mc.ConvertSelectionToVertices(follower)
        flw_lctr = self.plotter_avrg()
        # set the offset node for translate
        plsMns = mc.shadingNode("plusMinusAverage", asUtility = 1)
        mc.setAttr(plsMns+".operation", 2)
        mc.connectAttr(ld_lctr+".translate", plsMns+".input3D[0]", f=1)
        mc.connectAttr(flw_lctr+".translate", plsMns+".input3D[1]", f=1)
        # set cluster
        mc.select(checkSel[0])
        getpar=mc.listRelatives(checkSel[0], p=1)
        getchildren=[(nodes) for nodes in mc.listRelatives(getpar[0], ad=1, type="mesh") if "Orig" not in str(nodes) ]
        mc.select(getchildren, add =1 )
        create_cstr = mc.cluster()
        # connect result to cluster
        mc.connectAttr( plsMns+".output3D", create_cstr[0]+"Handle.translate", f = 1)

    def offset_cache_static(self):
        checkSel = mc.ls(sl=1)
        if len(checkSel)<2:
            print "you need to select two objects"
        leader = checkSel[1]
        mc.select(leader, r=1)
        mc.ConvertSelectionToVertices(leader)
        ld_lctr = self.locator_selected_mass()
        follower = checkSel[0]
        mc.select(follower, r=1)
        mc.ConvertSelectionToVertices(follower)
        flw_lctr = self.locator_selected_mass()
        # set the offset node for translate
        plsMns = mc.shadingNode("plusMinusAverage", asUtility = 1)
        mc.setAttr(plsMns+".operation", 2)
        mc.connectAttr(ld_lctr+".translate", plsMns+".input3D[0]", f=1)
        mc.connectAttr(flw_lctr+".translate", plsMns+".input3D[1]", f=1)
        # set cluster
        mc.select(checkSel[0])
        getpar=mc.listRelatives(checkSel[0], p=1)
        getchildren=[(nodes) for nodes in mc.listRelatives(getpar[0], ad=1, type="mesh") if "Orig" not in str(nodes) ]
        mc.select(getchildren, add =1 )
        create_cstr = mc.cluster()
        # connect result to cluster
        mc.connectAttr( plsMns+".output3D", create_cstr[0]+"Handle.translate", f = 1)    def CurveShapes(self):
        getSel=self.selection_grab()
        if getSel:
            pass
        else:
            return
        getNames=mc.ls(sl=1, fl=1)
        if ".e[" not in str(getNames[0]):
            print "selection needs to be continuous edges of two seperate polygon objects: first select one, then continuous edge and then the continuous edge on a seperate poly object that you want to deform it along"
            return
        else:
            pass
        getFirstGrp = getNames[0].split(".")[0]
        getSecondGrp = getNames[-1:][0].split(".")[0]
        if getFirstGrp == getSecondGrp:
            print "Only one poly object has been detected. Select one object and it's continuous edge and then select another object and select it's continuous edge for the first object to align to."
            return
        else:
            pass
        firstList=[(each) for each in getNames if each.split(".")[0]==getFirstGrp]
        secondList=[(each) for each in getNames if each.split(".")[0]==getSecondGrp]
        '''create childfirst curve'''
        mc.select(firstList)
        mc.CreateCurveFromPoly()
        getFirstCurve=mc.ls(sl=1, fl=1)
        '''get cv total of curve'''
        getFirstCurveInfo=mc.ls(sl=1, fl=1)
        print "this needs to be refactored to not use pymel: Line 725"
        numberCV=str(pm.PyNode(getFirstCurveInfo[0]).numCVs())
        mc.delete(getFirstCurve[0], ch=1)
        '''wrap child mesh to curve'''
        mc.select(mc.ls(getFirstGrp)[0], r=1)
        mc.wire(w=getFirstCurve[0], gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
        '''create parent curve'''
        mc.select(secondList)
        mc.CreateCurveFromPoly()
        getSecondCurve=mc.ls(sl=1, fl=1)
        getSecondCurveInfo=mc.ls(sl=1, fl=1)
        '''rebuilt curve to match first curve built'''        mc.rebuildCurve(getSecondCurve[0], getFirstCurve[0], rt=2 )
        getSecondCurve=mc.ls(sl=1, fl=1)
        getSecondCurveInfo=mc.ls(sl=1, fl=1)
        mc.delete(getSecondCurve[0], ch=1)
        '''wrap parent curve to parent mesh'''
        mc.select(getSecondCurve[0], r=1)
        mc.select(mc.ls(getSecondGrp)[0], add=1)
        mc.CreateWrap()
        '''blend child curve to parent curve'''
        mc.blendShape(getSecondCurve[0], getFirstCurve[0],w=(0, 1.0))
        return getFirstGrp, getSecondGrp


    def matchCurveShapes_andShrinkWrap(self, getFirstGrp, getSecondGrp):
        myDict={
                ".shapePreservationEnable":1,
                ".shapePreservationSteps":72,
                ".shapePreservationReprojection":1,
                ".shapePreservationIterations":1,
                ".shapePreservationMethod":0,
                ".envelope":1,
                ".targetSmoothLevel":1,
                ".continuity":1,
                ".keepBorder":0,
                ".boundaryRule":1,
                ".keepHardEdge":0,
                ".propagateEdgeHardness":0,
                ".keepMapBorders":1,
                ".projection":4,
                ".closestIfNoIntersection":0,
                ".closestIfNoIntersection":0 ,
                ".reverse":0,
                ".bidirectional":0,
                ".boundingBoxCenter":1,
                ".axisReference":0 ,
                ".alongX":1,
                ".alongY":1,
                ".alongZ":1,
                ".offset":0,
                ".targetInflation":0,
                ".falloff":0.3021390379,
                ".falloffIterations": 1
                }        
        mc.delete(getFirstGrp, ch=1)
        getShrink=mc.deformer(getFirstGrp, type="shrinkWrap")
        mc.connectAttr(getSecondGrp+".worldMesh[0]", getShrink[0]+".targetGeom", f=1)
        for key, value in myDict.items():
            mc.setAttr(getShrink[0]+key, value)
    def xformmove(self):
        '''move to matrix'''
        objSel=mc.ls(sl=1)
        matrix=mc.xform(objSel[0], q=1, ws=1, m=1)
        mc.xform(objSel[1], ws=1, m=matrix)   
        mc.select(objSel[1])



    def xformrot(self):
        '''move to matrix'''
        getornt = mc.orientConstraint (mc.ls(sl=1)[0], mc.ls(sl=1)[-1], mo=0)
        mc.delete(getornt)
        mc.select(mc.ls(sl=1)[-1])

    def matchpivot(self):
        '''move to matrix'''
        objSel=mc.ls(sl=1)
        matrix=mc.xform(objSel[0], q=1, ws=1, rp=1)
        mc.xform(objSel[1], ws=1, rp=matrix)   
        getornt = mc.orientConstraint (mc.ls(sl=1)[0], mc.ls(sl=1)[-1], mo=0)
        mc.delete(getornt)
        mc.select(objSel[1])



    def xform_mirror_move(self):
        '''mirror to matrix'''
        objSel=mc.ls(sl=1)
        mc.duplicate(objSel[0], n="new_place")
        getIt=mc.CreateEmptyGroup()
        mc.rename(mc.ls(sl=1)[0], "temp_grp")
        mc.parent("new_place", "temp_grp")
        mc.setAttr("temp_grp.scaleX", -1)
        mc.parent("new_place", w=1)
        matrix=mc.xform("new_place", q=1, ws=1, m=1)
        mc.delete("temp_grp")
        mc.xform(objSel[1], ws=1, m=matrix)
        mc.select(objSel[1])

    def xform_mirror_create(self):
        '''mirror to matrix'''
        objSel=mc.ls(sl=1)
        for each_obj in objSel:
            new_dup = mc.duplicate(each_obj, n=each_obj+"_dup")
            getIt=mc.CreateEmptyGroup()
            mc.rename(mc.ls(sl=1)[0], "temp_grp")
            mc.parent(new_dup, "temp_grp")
            mc.setAttr("temp_grp.scaleX", -1)
            mc.parent(new_dup[0], w=1)
            mc.delete("temp_grp")
    def xform_set_originV1(self):
        '''reset transforms to sit at origin'''
        objSel=mc.ls(sl=1)
        for each in objSel:
            mc.select(cl=1)
            mc.CreateEmptyGroup()
            getIt = mc.ls(sl=1)
            mc.select([each, getIt[0]], r=1)
            # mc.matchTransform(piv=1)
            maya.mel.eval( "MatchPivots;" )
            mc.select(each, r=1)
            mc.makeIdentity(apply='true', t=0, r=1, s=0)
            # maya.mel.eval( "ResetTransformations;" )
            print "reset {}".format(each)
            mc.delete(getIt)

    def xform_set_origin(self):
        '''reset transforms to sit at origin'''
        objSel=mc.ls(sl=1)
        for each in objSel:
            mc.select(cl=1)
            mc.CreateEmptyGroup()
            getIt = mc.ls(sl=1)
            mc.select([each, getIt[0]], r=1)
            maya.mel.eval( "MatchPivots;" )
            transformWorldMatrix, rotateWorldMatrix=self.locationXForm(each)
            # mc.select(each, r=1)
            mc.move(0,0,0, "{}.rotatePivot".format(each) ,r=1, rpr=1 )
            # mc.xform("{}.rotatePivot".format(each), a=1, ro=0,0,0)
            # mc.rotate(0,0,0, "{}.rotatePivot".format(each) , a =1)
            mc.xform("{}.rotatePivot".format(each), ws=1, ro=rotateWorldMatrix)
            print "reset {}".format(each)
            mc.delete(getIt)

    def xform_set_to_sel(self):
        '''reset transforms to sit at origin'''
        parObj=mc.ls(sl=1)[0]
        objSel=mc.ls(sl=1)[1]
        mc.select(cl=1)
        getIt = mc.ls(sl=1)
        mc.select([objSel, parObj], r=1)
        maya.mel.eval( "MatchPivots;" )
        mc.select(["{}.rotatePivot".format(objSel), parObj], r=1)
        maya.mel.eval( "MatchRotation;" )
        transformWorldMatrix, rotateWorldMatrix=self.locationXForm(parObj)
        mc.select(objSel, r=1)
        mc.xform("{}.rotatePivot".format(objSel),  ws=1, t=transformWorldMatrix)
        mc.xform("{}.rotatePivot".format(objSel), ws=1, ro=rotateWorldMatrix)
        print "reset {}".format(objSel)
        mc.delete(getIt)
    def xform_reset_move(self):
        '''reset transforms'''
        objSel=mc.ls(sl=1)
        matrix=mc.xform(objSel[0], q=1, ws=1, m=1)
        getloc=mc.spaceLocator(n="cnstr_lctr")
        mc.xform(getloc[0], m=matrix)
        maya.mel.eval( "ResetTransformations;" )
        # mc.makeIdentity(apply='false', t=1, r=1, s=1)
        mc.select([getloc[0], objSel[0]], r=1 )
        # self.xformmove()
        mc.xform(objSel[0], m=matrix)
        mc.delete(getloc[0])

    def shrink_intersections(self):
        myDict={
        ".alongX":0,
        ".alongY":0,
        ".alongZ":0,
        ".axisReference":0,
        ".bidirectional":0,
        ".boundaryRule":1,
        ".boundingBoxCenter":1,
        ".caching":0,
        ".closestIfNoIntersection":0,
        ".continuity":1.0,
        ".envelope":1.0,
        ".falloff":0.4185185189,
        ".falloffIterations":54,
        ".fchild1":0,
        ".fchild2":0,
        ".fchild3":0,
        ".frozen":0,
        ".innerGeom":0,
        ".innerGroupId":0,
        ".inputEnvelope":[()],
        ".isHistoricallyInteresting":2,
        ".keepBorder":0,
        ".keepHardEdge":0,
        ".keepMapBorders":1,
        ".nodeState":0,
        ".offset":0.03237410082,
        ".projection":1,
        ".propagateEdgeHardness":0,
        ".reverse":1,
        ".shapePreservationEnable":0,
        ".shapePreservationIterations":1,
        ".shapePreservationMethod":0,
        ".shapePreservationReprojection":0,
        ".shapePreservationSteps":1,
        ".smoothUVs":1,
        ".targetGeom":0,
        ".targetInflation":0.06115107902,
        ".targetSmoothLevel":1,
        }
        getSel=self.selection_grab()
        if getSel:
            pass
        else:
            return
        getShrink=mc.deformer(getSel[0], type="shrinkWrap")
        mc.connectAttr(getSel[1]+".worldMesh[0]", getShrink[0]+".targetGeom", f=1)
        for key, value in myDict.items():
            try:
                mc.setAttr(getShrink[0]+key, value)        
            except:
                pass



    def print_str_slider(self):
        size = self.strength_slider.value()
        self.strengthNum.setText(str(size)+"%")

    def print_bias_slider(self):
        size = self.bias_slider.value()
        self.biasNum.setText(str(size)+"%")

    def print_drift_slider(self):
        size = self.drift_slider.value()
        self.driftNum.setText(str(size)+"%")

    def set_str_slider(self):
        getText = self.strengthNum.text()
        getText = int(getText)
        self.strength_slider.setValue(getText)

    def set_bias_slider(self):
        getText = self.biasNum.text()
        getText = int(getText)
        self.bias_slider.setValue(getText)

    def set_drift_slider(self):
        getText = self.driftNum.text()
        getText = int(getText)
        self.drift_slider.setValue(getText)   

inst_mkwin=plotter_UI()
inst_mkwin.show()




