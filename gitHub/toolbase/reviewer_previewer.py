#!/usr/bin/env python
# -*- coding: utf-8 -*- 

__author__="Elise Deglau"
__developer__="deglaue"

import maya.cmds as mc
import os, sys
import maya.mel as mm



import Qt_py
from Qt_py.Qt import QtCore, QtGui, QtWidgets
class preview_ports(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(preview_ports, self).__init__(parent = None)

        self.setWindowTitle("Mem Blast Preview")
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
        self.pprev_order_layout = QtWidgets.QHBoxLayout()
        self.myform.addRow(self.pprev_order_layout) 
        self.pprev_button_layout = QtWidgets.QVBoxLayout()
        self.pprev_order_layout.addLayout(self.pprev_button_layout)
        self.pprev_slid_layout = QtWidgets.QVBoxLayout()
        self.pprev_order_layout.addLayout(self.pprev_slid_layout)   
        self.pprev_slider_layout = QtWidgets.QVBoxLayout()     
        self.pprev_slid_layout.addLayout(self.pprev_slider_layout) 
        
        self.subs_layout = QtWidgets.QHBoxLayout()     
        self.pprev_button_layout.addLayout(self.subs_layout)
        self.fps_lbl = QtWidgets.QLabel("Playback Substep")  
        self.subs_layout.addWidget(self.fps_lbl)
        self.fps_fieldText = QtWidgets.QLineEdit("1.0")
        self.subs_layout.addWidget(self.fps_fieldText)

        self.add_lit_button = QtWidgets.QPushButton("Add test light")
        self.add_lit_button.clicked.connect(lambda: self.no_duct_tape_on_mars())
        self.pprev_button_layout.addWidget(self.add_lit_button)

        self.add_pubcam_button = QtWidgets.QPushButton("Add publishing cam")
        self.add_pubcam_button.clicked.connect(lambda: self.publishable_cam())
        self.pprev_button_layout.addWidget(self.add_pubcam_button)

        self.sel_lit_button = QtWidgets.QPushButton("Tape light to selected")
        self.sel_lit_button.clicked.connect(lambda: self.snap_light_to_selected())
        self.pprev_button_layout.addWidget(self.sel_lit_button)
        

        self.pprev_obj_button = QtWidgets.QPushButton("Whisker mode (VP2)")
        self.pprev_obj_button.setStyleSheet("color: #eeffaa; background-color: rgba(105,110,70,100);")
        self.pprev_obj_button.clicked.connect(lambda: self.sim_whsker_mode())
        self.pprev_button_layout.addWidget(self.pprev_obj_button)

        self.prim_button = QtWidgets.QPushButton("Primitive Mode (VP2)")
        self.prim_button.setStyleSheet("color: #eeffaa; background-color: rgba(100,110,70,50);")
        self.prim_button.clicked.connect(lambda: self.prim_mode())
        self.pprev_button_layout.addWidget(self.prim_button)

        self.blast_button = QtWidgets.QPushButton("Blast Mode (LGCY)")
        self.blast_button.setStyleSheet("color: #aaccff; background-color: rgba(70,70,100,50);")
        self.blast_button.clicked.connect(lambda: self.blast_mode())
        self.pprev_button_layout.addWidget(self.blast_button)   
        

        self.restore_button = QtWidgets.QPushButton("restore whisker for export")
        self.restore_button.setStyleSheet("color: #aaaaaa; background-color: rgba(50,50,50,50);")
        self.restore_button.clicked.connect(lambda: self.restore())
        self.pprev_button_layout.addWidget(self.restore_button)


        self.memblast_button = QtWidgets.QPushButton("Memory Blast cust")
        self.memblast_button.setStyleSheet("color: #eeffaa; background-color: rgba(100,110,70,50);")
        self.memblast_button.clicked.connect(lambda: self.mem_blast_cust())
        self.pprev_button_layout.addWidget(self.memblast_button)

        self.memblast_button = QtWidgets.QPushButton("Memory Blast VP2")
        self.memblast_button.setStyleSheet("color: #eeffaa; background-color: rgba(100,110,70,50);")
        self.memblast_button.clicked.connect(lambda: self.mem_blast())
        self.pprev_button_layout.addWidget(self.memblast_button)
        

        self.memblast_button_nrol = QtWidgets.QPushButton("Memory Blast VP2 no roll")
        self.memblast_button_nrol.setStyleSheet("color: #eeffaa; background-color: rgba(100,110,70,50);")
        self.memblast_button_nrol.clicked.connect(lambda: self.mem_blast_no_roll())
        self.pprev_button_layout.addWidget(self.memblast_button_nrol)

        self.blast_button_nrol = QtWidgets.QPushButton("Blast no roll (LGCY)")
        self.blast_button_nrol.setStyleSheet("color: #aaccff; background-color: rgba(70,70,100,50);")
        self.blast_button_nrol.clicked.connect(lambda: self.blast_no_roll())
        self.pprev_button_layout.addWidget(self.blast_button_nrol)

        self.blast_def_button_nrol = QtWidgets.QPushButton("Blast (LGCY)")
        self.blast_def_button_nrol.setStyleSheet("color: #aaccff; background-color: rgba(70,70,100,50);")
        self.blast_def_button_nrol.clicked.connect(lambda: self.blast_def())
        self.pprev_button_layout.addWidget(self.blast_def_button_nrol)
        

        self.pcon_button = QtWidgets.QPushButton("Toggle polycount HUD")
        self.pcon_button.clicked.connect(lambda: self.switch_pc_hud_tgl())
        self.pprev_button_layout.addWidget(self.pcon_button)


        self.pcoff_button = QtWidgets.QPushButton("Toggle selection in View")
        self.pcoff_button.clicked.connect(lambda: self.sel_tgl())
        self.pprev_button_layout.addWidget(self.pcoff_button)

        self.add_cam_lit_button = QtWidgets.QPushButton("Add light")
        self.add_cam_lit_button.clicked.connect(lambda: self.lights_cam())
        self.pprev_button_layout.addWidget(self.add_cam_lit_button)
        
        self.add_cam_sun_button = QtWidgets.QPushButton("Add sunlight")
        self.add_cam_sun_button.clicked.connect(lambda: self.sunlights_cam())
        self.pprev_button_layout.addWidget(self.add_cam_sun_button)


        self.wit_cam_lit_button = QtWidgets.QPushButton("Wit-cam")
        self.wit_cam_lit_button.clicked.connect(lambda: self.wit_cam())
        self.pprev_button_layout.addWidget(self.wit_cam_lit_button)
        
    def publishable_cam(self):
        nm_space = 'shotcam1'
        mc.file(pub_cam, r=1, ns=nm_space)

    def blast_no_roll(self): 
        fps_set = float(str(self.fps_fieldText.text()))
        mc.playbackOptions(fps = fps_set, e=1)
        focPane = [(each) for each in mc.getPanel(vis=1) if "model" in each]
        for each in focPane:
            if mc.modelEditor(each, q=1, av=1) == True:
                mc.modelEditor(each, e=1, rnm="base_OpenGL_Renderer")          
        strt_rng =int(wk_strt_value)-1
        end_rng=mc.playbackOptions(q=1, max=1)      
        folder_strt = '/'.join(mc.file(q=1, location=1).split('/')[:-5])
        scn_name=str(mc.file(q=1, location=1)).split('/')[-1].split(".")[0]
        gotten_name=str(mc.file(q=1, location=1)).split('/')[-1].split(".")[0]+"-playblast-half1712x903_vdf8"
        gotten_path = "{}/PRODUCTS/images/{}/{}/playblast-half1712x903_vdf8_jpg/{}".format(folder_strt, _dept_task, scn_name, gotten_name)
        sel_NumMn=mc.playbackOptions(q=1, min=1)
        sel_NumMn_reset=mc.playbackOptions(q=1, min=1)+1
        mc.currentTime(sel_NumMn)
        mc.currentTime(sel_NumMn_reset)
        mc.currentTime(sel_NumMn)
        mc.playblast(format="image", st=strt_rng, et=end_rng, filename=gotten_path, sequenceTime=0, clearCache=1, viewer= 1,  showOrnaments=1, offScreen=1, fp=4, percent = 100, compression = "jpg",  quality = 100, widthHeight = (1712, 903))
        mc.playbackOptions(fps = 1.0, e=1)

    def blast_def(self): 
        fps_set = float(str(self.fps_fieldText.text()))
        mc.playbackOptions(fps = fps_set, e=1)
        focPane = [(each) for each in mc.getPanel(vis=1) if "model" in each]
        for each in focPane:
            if mc.modelEditor(each, q=1, av=1) == True:
                mc.modelEditor(each, e=1, rnm="base_OpenGL_Renderer")          
        strt_rng=mc.playbackOptions(q=1, min=1)      
        end_rng=mc.playbackOptions(q=1, max=1)      
        folder_strt = '/'.join(mc.file(q=1, location=1).split('/')[:-5])
        scn_name=str(mc.file(q=1, location=1)).split('/')[-1].split(".")[0]
        gotten_name=str(mc.file(q=1, location=1)).split('/')[-1].split(".")[0]+"-playblast-half1712x903_vdf8"
        gotten_path = "{}/PRODUCTS/images/{}/{}/playblast-half1712x903_vdf8_jpg/{}".format(folder_strt, _dept_task, scn_name, gotten_name)
        sel_NumMn=mc.playbackOptions(q=1, min=1)
        sel_NumMn_reset=mc.playbackOptions(q=1, min=1)+1
        mc.currentTime(sel_NumMn)
        mc.currentTime(sel_NumMn_reset)        
        mc.currentTime(sel_NumMn)
        mc.playblast(format="image", st=strt_rng, et=end_rng, filename=gotten_path, sequenceTime=0, clearCache=1, viewer= 1,  showOrnaments=1, offScreen=1, fp=4, percent = 100, compression = "jpg",  quality = 100, widthHeight = (1712, 903))
        mc.playbackOptions(fps = 1.0, e=1)

    def mem_blast_cust (self):
        strt_rng = mc.playbackOptions(q=1, min=1)
        end_rng = mc.playbackOptions(q=1, max=1)
        fps_set = float(str(self.fps_fieldText.text()))
        focPane = [(each) for each in mc.getPanel(vis=1) if "model" in each]
        for each in focPane:
            if mc.modelEditor(each, q=1, av=1) == True:
                mm.eval('setRendererInModelPanel "vp2Renderer" {0}'.format(each))        
        mm.eval('setPolyCountVisibility(1);')
        folder_strt = '/'.join(mc.file(q=1, location=1).split('/')[:-5])
        scn_name=str(mc.file(q=1, location=1)).split('/')[-1].split(".")[0]
        gotten_name=str(mc.file(q=1, location=1)).split('/')[-1].split(".")[0]+"-playblast-half1712x903_vdf8"
        gotten_path = "{}/PRODUCTS/images/{}/{}/playblast-half1712x903_vdf8_jpg/{}".format(folder_strt, _dept_task, scn_name, gotten_name)
        mc.playbackOptions(fps = fps_set, e=1)
        sel_NumMn=mc.playbackOptions(q=1, min=1)
        sel_NumMn_reset=mc.playbackOptions(q=1, min=1)+1
        mc.currentTime(sel_NumMn)
        mc.currentTime(sel_NumMn_reset)        
        mc.currentTime(sel_NumMn)
        mc.playblast(format="image", st=strt_rng, et=end_rng, filename=gotten_path, sequenceTime=0, clearCache=1, viewer= 1,  showOrnaments=1, offScreen=1, fp=4, percent = 100, compression = "jpg",  quality = 100, widthHeight = (1712, 903))
        mc.playbackOptions(fps = 1.0, e=1)        
        mm.eval('setPolyCountVisibility(0);')
        for each in focPane:
            if mc.modelEditor(each, q=1, av=1) == True:
                mc.modelEditor(each, e=1, rnm="base_OpenGL_Renderer") 

    def mem_blast(self):
        fps_set = float(str(self.fps_fieldText.text()))
        focPane = [(each) for each in mc.getPanel(vis=1) if "model" in each]
        for each in focPane:
            if mc.modelEditor(each, q=1, av=1) == True:
                mm.eval('setRendererInModelPanel "vp2Renderer" {0}'.format(each))        
        mm.eval('setPolyCountVisibility(1);')
        folder_strt = '/'.join(mc.file(q=1, location=1).split('/')[:-5])
        scn_name=str(mc.file(q=1, location=1)).split('/')[-1].split(".")[0]
        gotten_name=str(mc.file(q=1, location=1)).split('/')[-1].split(".")[0]+"-playblast-half1712x903_vdf8"
        gotten_path = "{}/PRODUCTS/images/{}/{}/playblast-half1712x903_vdf8_jpg/{}".format(folder_strt, _dept_task, scn_name, gotten_name)
        mc.playbackOptions(fps = fps_set, e=1)
        sel_NumMn=mc.playbackOptions(q=1, min=1)
        sel_NumMn_reset=mc.playbackOptions(q=1, min=1)+1
        mc.currentTime(sel_NumMn)
        mc.currentTime(sel_NumMn_reset)        
        mc.currentTime(sel_NumMn)
        mc.playblast(format="image", filename=gotten_path, sequenceTime=0, clearCache=1, viewer= 1,  showOrnaments=1, offScreen=1, fp=4, percent = 100, compression = "jpg",  quality = 100, widthHeight = (1712, 903))
        mc.playbackOptions(fps = 1.0, e=1)        
        mm.eval('setPolyCountVisibility(0);')
        for each in focPane:
            if mc.modelEditor(each, q=1, av=1) == True:
                mc.modelEditor(each, e=1, rnm="base_OpenGL_Renderer") 
                
    def mem_blast_no_roll(self):
        fps_set = float(str(self.fps_fieldText.text()))
        mc.playbackOptions(fps = fps_set, e=1)        
        strt_rng =int(wk_strt_value)-1
        end_rng=mc.playbackOptions(q=1, max=1)
        focPane = [(each) for each in mc.getPanel(vis=1) if "model" in each]
        for each in focPane:
            if mc.modelEditor(each, q=1, av=1) == True:
                mm.eval('setRendererInModelPanel "vp2Renderer" {0}'.format(each))        
        mm.eval('setPolyCountVisibility(1);')
        folder_strt = '/'.join(mc.file(q=1, location=1).split('/')[:-5])
        scn_name=str(mc.file(q=1, location=1)).split('/')[-1].split(".")[0]
        gotten_name=str(mc.file(q=1, location=1)).split('/')[-1].split(".")[0]+"-playblast-half1712x903_vdf8"
        gotten_path = "{}/PRODUCTS/images/{}/{}/playblast-half1712x903_vdf8_jpg/{}".format(folder_strt, _dept_task, scn_name, gotten_name)
        sel_NumMn=mc.playbackOptions(q=1, min=1)
        sel_NumMn_reset=mc.playbackOptions(q=1, min=1)+1
        mc.currentTime(sel_NumMn)
        mc.playblast(format="image", st=strt_rng, et=end_rng, filename=gotten_path, sequenceTime=0, clearCache=1, viewer= 1,  showOrnaments=1, offScreen=1, fp=4, percent = 100, compression = "jpg",  quality = 100, widthHeight = (1712, 903))
        mm.eval('setPolyCountVisibility(0);')
        for each in focPane:
            if mc.modelEditor(each, q=1, av=1) == True:
                mc.modelEditor(each, e=1, rnm="base_OpenGL_Renderer")        
        mc.playbackOptions(fps = 1.0, e=1)

    def lights_cam(self):
        if mc.objExists("*:camlight_loc"):
            print "cam lights already exist - won't import"
            pass
        elif mc.objExists("*:light_loc"):
            print "lights already exist - won't will skip"
            pass
        else:
            try:
                getCameraGrp=mc.ls("*:*.cameraPreset")
                getNode=str(pm.PyNode(getCameraGrp[0]).node())
                getCam=[each for each in mc.listRelatives(getNode, ad=1) if mc.nodeType(each) =="camera"]
                gettransformCam=[each for each in mc.listRelatives(getCam[0], p=1) if mc.nodeType(each) =="transform"][0]
                getLocCam=mc.ls('cam_light_loc*:camlight_loc')[0]
                mc.select(gettransformCam, r=1)
                mc.select(getLocCam, add=1)
                print mc.ls(sl=1)
                self._transfer_anim_attr()
            except:
                pass
            getcamlightPath='/sw/dev/deglaue/cam_light_loc.mb'
            namer='cam_light_loc'
            
    def sunlights_cam(self):
        if mc.objExists("*:cam_sun"):
            print "cam lights already exist - won't import"
            pass
        elif mc.objExists("*:light_loc"):
            print "lights already exist - won't will skip"
            pass
        else:
            try:
                getCameraGrp=mc.ls("*:*.cameraPreset")
                getNode=str(pm.PyNode(getCameraGrp[0]).node())
                getCam=[each for each in mc.listRelatives(getNode, ad=1) if mc.nodeType(each) =="camera"]
                gettransformCam=[each for each in mc.listRelatives(getCam[0], p=1) if mc.nodeType(each) =="transform"][0]
                getLocCam=mc.ls('cam_light_loc*:camlight_loc')[0]
                mc.select(gettransformCam, r=1)
                mc.select(getLocCam, add=1)
                print mc.ls(sl=1)
                self._transfer_anim_attr()
            except:
                pass
            getcamlightPath='/sw/dev/deglaue/cam_sun.mb'
            namer='cam_sun_light_loc'
            mc.file(getcamlightPath, i=1, type="mayaBinary", ignoreVersion=1, ra=True, mergeNamespacesOnClash=False, namespace=namer, options="v=0;", pr=1)
            print "imported cam lights" 

    def no_duct_tape_on_mars(self):
        focPane = [(each) for each in mc.getPanel(vis=1) if "model" in each]
        for each in focPane:
            mc.modelEditor(each, e=1, dl='all')
            mc.modelEditor(each, e=1, lights=False)
        if mc.objExists("duct_tape_loc") == True:
            print "This light already exist -  will skip creating it"
            if mc.objExists("*:*.cameraPreset") == True:
                getCameraGrp=mc.ls("*:*.cameraPreset")[0]
                print 'taping light to shotcam'
                getNode=getCameraGrp.split(".")[0]
                selcnst = mc.parentConstraint(getNode, 'duct_tape_loc', mo=0)
            elif mc.objExists("shotcam*:camera") == True:
                getCameraGrp=mc.ls("shotcam*:camera")[0]
                print 'taping light to shotcam'
                getNode=getCameraGrp.split(".")[0]
                selcnst = mc.parentConstraint(getNode, 'duct_tape_loc', mo=0)
            else:
                print 'taping light to perspective'
                try:
                    mc.delete('light_duct_tape_par')
                except:
                    pass
                try:
                    getNode = [(mc.listRelatives(item, ap=1, type='transform')[0]) for item in mc.ls(type = 'camera') if 'persp' in item][0]
                    selcnst = mc.parentConstraint(getNode, 'duct_tape_loc', mo=0)
                    mc.rename(selcnst, 'light_duct_tape_par')
                except:
                    print "couldn't find a light or cam in scene. skipping"
                    pass
        else:
            mc.select(cl=1)
            mc.CreateEmptyGroup('duct_tape_loc')
            mc.rename(mc.ls(sl=1)[0], 'duct_tape_loc')
            command = 'defaultDirectionalLight(1, 1,1,1, "0", 0,0,0, 0);  '
            mm.eval(command)
            mc.rename(mc.ls(sl=1)[0], 'flash_light')
            mc.parent('flash_light', 'duct_tape_loc')
            if mc.objExists("*:*.cameraPreset") == True:
                getCameraGrp=mc.ls("*:*.cameraPreset")[0]
                print 'taping light to shotcam'
                getNode=getCameraGrp.split(".")[0]
                selcnst = mc.parentConstraint(getNode, 'duct_tape_loc', mo=0)
            elif mc.objExists("shotcam*:camera") == True:
                getCameraGrp=mc.ls("shotcam*:camera")[0]
                print 'taping light to shotcam'
                getNode=getCameraGrp.split(".")[0]
                selcnst = mc.parentConstraint(getNode, 'duct_tape_loc', mo=0)
            else:
                print 'taping light to perspective'
                try:
                    getNode = [(mc.listRelatives(item, ap=1, type='transform')[0]) for item in mc.ls(type = 'camera') if 'persp' in item][0]
                    selcnst = mc.parentConstraint(getNode, 'duct_tape_loc', mo=0)
                    mc.rename(selcnst, 'light_duct_tape_par')
                except:
                    print "couldn't find a light or cam in scene. skipping"
                    pass


    def snap_light_to_selected(self):
        focPane = [(each) for each in mc.getPanel(vis=1) if "model" in each]
        for each in focPane:
            mc.modelEditor(each, e=1, dl='all')
            mc.modelEditor(each, e=1, lights=False)
        try:
            getNode = mc.ls(sl=1)[0]
            if mc.objExists("duct_tape_loc") == True:
                print "This light already exist -  will skip creating it"
                print 'taping light to selected'
                try:
                    mc.delete('light_duct_tape_par')
                except:
                    pass
                try:
                    selcnst = mc.parentConstraint(getNode, 'duct_tape_loc', mo=0)
                    mc.rename(selcnst, 'light_duct_tape_par')
                except:
                    print "Nothing selected. skipping"
                    pass
            else:
                mc.select(cl=1)
                mc.CreateEmptyGroup('duct_tape_loc')
                mc.rename(mc.ls(sl=1)[0], 'duct_tape_loc')
                command = 'defaultDirectionalLight(1, 1,1,1, "0", 0,0,0, 0);  '
                mm.eval(command)
                mc.rename(mc.ls(sl=1)[0], 'flash_light')
                mc.parent('flash_light', 'duct_tape_loc')
                print 'taping light to selected'
                try:
                    selcnst = mc.parentConstraint(getNode, 'duct_tape_loc', mo=0)
                    mc.rename(selcnst, 'light_duct_tape_par')
                except:
                    print "Nothing selected. skipping"
                    pass
        except:
            print "something needs to be selected for stuff to happen here"
            pass
          
    def wit_cam(self):
        focusedThing=mc.ls(sl=1, fl=1)[0]
        if mc.nodeType(focusedThing)=="transform":
            focPane = [(each) for each in mc.getPanel(vis=1) if "model" in each][0]
            command='postModelEditorSelectCamera "%s" "%s" 0' % (focPane, focPane)
            mm.eval( command )   
            getOldCam=mc.ls(sl=1, fl=1)[0]
            newcam=mc.duplicate(getOldCam, n=focusedThing+"wit_cam")[0]
            command='lookThroughModelPanel "%s" "%s"' % (newcam, focPane)
            mm.eval( command )        
        elif mc.nodeType(focusedThing)=="mesh":
            command='rivet;'
            mm.eval( command )
            locatorObj=mc.ls(sl=1, fl=1)[0]
            focPane = [(each) for each in mc.getPanel(vis=1) if "model" in each][0]
            command='postModelEditorSelectCamera "%s" "%s" 0' % (focPane, focPane)
            mm.eval( command )   
            getOldCam=mc.ls(sl=1, fl=1)[0]
            newcam=mc.duplicate(getOldCam, n=focusedThing+"wit_cam")[0]
            mc.parentConstraint(locatorObj,newcam, mo=1)
            command='lookThroughModelPanel "%s" "%s"' % (newcam, focPane)
            mm.eval( command ) 
            mc.setAttr(locatorObj+".visibility", 0)

    def _transfer_anim_attr(self, arg=None):
        '''This copies values and animcurve nodes of a first selection to all secondary selections'''
        getSel=mc.ls(sl=1)
        getChildren=getSel[1:]
        getParent=getSel[:1]
        for each in getChildren:
            getFirstattr=mc.listAttr (getParent[0], w=1, a=1, s=1, u=1, m=0)
            for item in getFirstattr:
                if "." not in item:
                    get=mc.keyframe(getParent[0]+'.'+item, q=1, kc=1)
                    if get!=0:
                        try:
                            getSource=mc.connectionInfo(getParent[0]+'.'+item, sfd=1)
                            newAnimSrce=duplicate(getSource)
                            lognm=newAnimSrce[0].replace(str(getParent[0]), str(each))
                            #===========================================================
                            # remove numbers at end
                            #===========================================================
                            newname=re.sub("\d+$", "", lognm)
                            mc.rename(newAnimSrce, newname)
                            getChangeAttr=each+'.'+item                        
                            mc.connectAttr(newname+'.output', getChangeAttr, f=1)                             
                        except:
                            pass
                    else:
                        try:
                            getValue=getattr(getParent[0],item).get()
                            getChangeAttr=getattr(each,item)
                            getChangeAttr.set(getValue)
                        except:
                            pass

    def sel_tgl(self):
        focPane = [(each) for each in mc.getPanel(vis=1) if "model" in each]
        for each in focPane:
            if mc.modelEditor(each, q=1, av=1) == True:
                if mc.modelEditor(each, q=1, sel=1) == True:
                    mc.modelEditor(each, e=1, sel = 0)
                else:
                    mc.modelEditor(each, e=1, sel = 1)     
                    
    def switch_pc_hud_tgl(self):
        mm.eval('setPolyCountVisibility(!`optionVar -q polyCountVisibility`);')

    def switch_pc_hud_off(self):
        mm.eval('setPolyCountVisibility(0);')

    def sim_whsker_mode_mult(self):
        print "Uncommon techrig: this tool is still under construction for multiple techrigs in file"
                    

    def sim_whsker_mode(self):
        if len(mc.ls(sl=1))>0:
            if len(mc.ls(sl=1))>1:
                self.sim_whsker_mode_mult()
            elif len(mc.ls(sl=1))==1:
                self.sim_whsker_mode_single()
        elif len(mc.ls(sl=1))==0:
            getAnimGeo=mc.ls("*:animGeo")
            if len(getAnimGeo)>1:
                self.sim_whsker_mode_mult()
            elif len(getAnimGeo)==1:
                self.sim_whsker_mode_single()          
                
    def sim_whsker_mode_single(self):
        getAnimGeo=mc.ls("*:animGeo")
        for item in getAnimGeo:
            try:
                mc.setAttr("{}.ctrlVis".format(item), 0)
                mc.setAttr("{}.res".format(item) , 3)
                mc.setAttr("{}.jntVis".format(item), 0)
            except:
                pass
        self.break_connections()
        for item in getAnimGeo:
            try:
                mc.setAttr('{}.visibility'.format(item), 1)
                mc.setAttr("{}.whisker".format(item), 1)
                command = 'CBdeleteConnection "{}.whisker";'.format(item)
                mm.eval(command)
            except:
                pass         
        mc.select(getAnimGeo, r=1)  
        sel_post_grp = mc.ls('*Tech:postTech') [0]
        mc.setAttr('{}.visibility'.format(sel_post_grp), 1)      
        mc.setAttr('*Tech:techRig.visibility', 1)    
        try:
           get_post_children=mc.listRelatives('*Tech:postTech_mid_geo_grp', c=1)
        except:
            "error : cannot find 'postTech_mid_geo_grp'"
            return
        for each_child in get_post_children:
            try:
                mc.setAttr('{}.visibility'.format(each_child), 0)
            except:
                pass
        mc.setAttr('*Tech:whiskers.visibility', 1)
        mc.setAttr('*Tech:preTech.visibility', 0)
        mc.setAttr('*Tech:tech.visibility', 0)
        mc.setAttr('*Tech:sim.visibility', 0)       
        # #set viewport
        focPane = [(each) for each in mc.getPanel(vis=1) if "model" in each]
        for each in focPane:
            if mc.modelEditor(each, q=1, av=1) == True:
                mc.isolateSelect(each, state=0)
                mc.modelEditor(each, e=1, alo=0, nurbsCurves = 1, polymeshes = 1, imagePlane = 1, pluginShapes = 1)
                mm.eval('setRendererInModelPanel "vp2Renderer" {0}'.format(each))                  
        # #change rebuild curve degree
        sel_rebuilds = mc.ls(type = 'rebuildCurve')
        for each_build_curve in sel_rebuilds:
            sel_value = mc.getAttr('{}.degree'.format(each_build_curve))
            if sel_value == 3:
                pass
            else:
                mc.setAttr('{}.degree'.format(each_build_curve), 3)
        mc.select(cl=1)        
        

    def prim_mode(self):
        focPane = [(each) for each in mc.getPanel(vis=1) if "model" in each]
        for each in focPane:
            if mc.modelEditor(each, q=1, av=1) == True:
                mm.eval('setRendererInModelPanel "vp2Renderer" {0}'.format(each))
                mc.setAttr("hardwareRenderingGlobals.multiSampleEnable", 1)
                mc.setAttr("hardwareRenderingGlobals.lineAAEnable", 1)
                mc.setAttr("hardwareRenderingGlobals.multiSampleCount" ,16)
                mc.setAttr("hardwareRenderingGlobals.ssaoEnable", 1)
                mc.setAttr("hardwareRenderingGlobals.ssaoAmount", 1)
                mc.setAttr("hardwareRenderingGlobals.ssaoRadius", 7)
                mc.setAttr("hardwareRenderingGlobals.ssaoFilterRadius", 16)
                
    def blast_mode(self):
        focPane = [(each) for each in mc.getPanel(vis=1) if "model" in each]
        for each in focPane:
            if mc.modelEditor(each, q=1, av=1) == True:
                mc.modelEditor(each, e=1, rnm="base_OpenGL_Renderer")
                mc.setAttr("hardwareRenderingGlobals.multiSampleEnable", 0)
                mc.setAttr("hardwareRenderingGlobals.lineAAEnable", 0)
                mc.setAttr("hardwareRenderingGlobals.multiSampleCount" ,16)
                mc.setAttr("hardwareRenderingGlobals.ssaoEnable", 0)
                mc.setAttr("hardwareRenderingGlobals.ssaoAmount", 0)
                mc.setAttr("hardwareRenderingGlobals.ssaoRadius", 7)
                mc.setAttr("hardwareRenderingGlobals.ssaoFilterRadius", 16)
                
    def break_connections(self):
        getAnimGeo=mc.ls("*:animGeo")
        for item in getAnimGeo:
            try:
                command = 'CBdeleteConnection "{}.ctrlVis";'.format(item)
                mm.eval(command)                                
                command = 'CBdeleteConnection "{}.res";'.format(item)
                mm.eval(command)                
                command = 'CBdeleteConnection "{}.jntVis";'.format(item)
                mm.eval(command)                
                command = 'CBdeleteConnection "{}.selectableGeo";'.format(item)
                mm.eval(command)
            except:
                pass
        return getAnimGeo
                

inst_mppwin=preview_ports()
inst_mppwin.show()
