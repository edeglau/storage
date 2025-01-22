__author__="Elise Deglau"
import os, sys, glob, shutil
import getpass
import webbrowser
import re
import maya.cmds as cmds
import maya.mel
import inspect
import subprocess
from datetime import datetime
import time
getUser=getpass.getuser()
import maya.mel as mm


import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets

try:
    currentShot=cmds.workspace(q=1, openWorkspace = 1)
    currentdir=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    scriptPath=currentdir
    sys.path.insert(0, scriptPath)
    filename_string=currentShot.split(".")[0]
    getScenePathWorkPath=cmds.file(q=1, location=1)
    getScenePathWorkPath=getScenePathWorkPath.split(".")[0]
    getScenePath=getScenePathWorkPath.split('/')
    getScenePath = '/'.join(getScenePath)
    makecachefolder=getScenePath+"/"
    getScene = cmds.file(q=1, sn=1, shn=1)
    getCachePath=cmds.workspace(listWorkspaces=1)[1]+"/cache/nCache"
    filename_string=getScene.split(".")[0]
except:
    print ("please save file before launching this tool")
saveList=(
    'increment+play',
    'save+play',
    'play',
    'increment, cache & play all clth',
    'increment, cache & play all hr',
    'increment, cache & play sel',
    'cache & play all clth',
    'cache & play all hr',
    'cache & play sel',
    'cache all clth',
    'cache all hr',
    'cache all nstuff',
    'cache sel',
    )
workSpace = cmds.workspace(q=1, lfw=1)[-1]
M_USER = os.environ["USER"]
PROJECT = os.environ["PL_SHOW"]
SCENE = os.environ["PL_SEQ"]
SHOT = os.environ["PL_SHOT"]
DEPT = "creaturefx"


spaceWork = workSpace
projectFolder = '/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/scenes/'
animFolder = '/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/instances/'
abcFolder = '/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/cache/alembic/'
pbFolder = '/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/movies/'
rvFolder = '/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/'+DEPT
cacheFolder = '/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/cache/'

getCacheimages = '/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/techanim/'
pathways={'open folder':spaceWork, "work":spaceWork, "project":projectFolder, "products":animFolder, "alembic":abcFolder, "blasts":rvFolder, "cache": cacheFolder}
getLowRange = cmds.playbackOptions(q=1, min=1)
getHiRange = cmds.playbackOptions(q=1, max=1)
sgVarFilePath = '/jobs/%s/%s/%s/TECH/lib/shotgun/setshot.d/sgvars' % (PROJECT, SCENE, SHOT)

if os.path.isfile(sgVarFilePath):
    # get available in/out values
    franges = {'WORK_IN': None, 'CUT_IN': None,
               'WORK_OUT': None, 'CUT_OUT': None}
    for line in open(sgVarFilePath, 'r'):
        if "CUT_DURATION" in line:
            shot_len_value = line.split(' = ')[-1].strip()
            try:
                shot_len_value = int(shot_len_value)
            except:
                shot_len_value = 0.0
        if 'CUT_IN' in line:
            cut_in_value = line.split(' = ')[-1].strip()
            try:
                cut_in_value = int(cut_in_value)
            except:
                cut_in_value = 0.0
        if 'CUT_OUT' in line:
            cut_out_value = line.split(' = ')[-1].strip()
            try:
                cut_out_value = int(cut_out_value)
            except:
                cut_out_value = 0.0
        if 'WORK_IN' in line:
            wk_strt_value = line.split(' = ')[-1].strip()
            try:
                wk_strt_value = int(wk_strt_value)
            except:
                wk_strt_value = 0.0
        if 'WORK_OUT' in line:
            wk_out_value = line.split(' = ')[-1].strip()
            try:
                wk_out_value = int(wk_out_value)
            except:
                wk_out_value = 0.0
        if 'CUT_IN' in line:
            cut_shouldbe_in_value = line.split(' = ')[-1].strip()
            try:
                cut_shouldbe_in_value = int(cut_shouldbe_in_value)-8
            except:
                cut_shouldbe_in_value = 0.0
        if 'CUT_OUT' in line:
            cut_shouldbe_out_value = line.split(' = ')[-1].strip()
            try:
                cut_shouldbe_out_value = int(cut_shouldbe_out_value)+8
            except:
                cut_shouldbe_out_value = 0.0
else:
  wk_strt_value = 0.0
  wk_out_value = 0.0
  cut_in_value = 0.0
  cut_out_value = 0.0

folder_strt = '/'.join(cmds.file(q=1, location=1).split('/')[:-5])
scn_name=str(cmds.file(q=1, location=1)).split('/')[-1].split(".")[0]
gotten_name=str(cmds.file(q=1, location=1)).split('/')[-1].split(".")[0]+"-playblast-half1712x903_vdf8"
gotten_path = "{}/PRODUCTS/images/{}/{}/playblast-half1712x903_vdf8_jpg/{}".format(folder_strt, DEPT, scn_name, gotten_name)

class save_gen(QtWidgets.QMainWindow):
    def __init__(self):
        super(save_gen, self).__init__()
        self.initUI()


    def initUI(self):
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.masterLayout = QtWidgets.QGridLayout(self.central_widget)
        self.gBox = QtWidgets.QGroupBox(self.central_widget)

        self.gBox.clicked.connect(lambda:self.collapse(self.gBox))

        self.window_layer_00 = QtWidgets.QGridLayout()
        self.masterLayout.addLayout(self.window_layer_00, 0, 0, 1, 1)
        self.window_layer_01 = QtWidgets.QGridLayout()
        self.masterLayout.addLayout(self.window_layer_01, 5, 0, 1, 1)
        self.gBox.setLayout(self.masterLayout)

        self.save_spinner = QtWidgets.QComboBox()
        self.save_spinner.addItems(saveList)
        self.window_layer_00.addWidget(self.save_spinner, 0,0,1,1)

        self.cache_radiobox = QtWidgets.QGridLayout()
        self.masterLayout.addLayout(self.cache_radiobox, 1,0,1,1)
        self.cache_range_group = QtWidgets.QButtonGroup(self.cache_radiobox)
        self.cache_title = QtWidgets.QLabel("Cache length")
        self.cache_title.setStyleSheet("color: #787878; background-color: rgba(255,255,255,0);")
        self.cache_radiobox.addWidget(self.cache_title)


        self.cache_work_checkbox = QtWidgets.QRadioButton("Work: " + str(int(wk_strt_value-1)) + '-' + str(int(wk_out_value+1)))
        self.cache_work_checkbox.setToolTip("Take this range into consideration for playblastting to shotgun")
        self.cache_work_checkbox.setChecked(0)
        self.cache_work_checkbox.setStyleSheet("color: #ffff12;")
        self.cache_range_group.addButton(self.cache_work_checkbox)
        self.cache_radiobox.addWidget(self.cache_work_checkbox, 2,0,1,1)

        self.cache_cut_checkbox = QtWidgets.QRadioButton("Cut: " + str(cut_in_value) + '-' + str(cut_out_value))
        self.cache_cut_checkbox.setToolTip("Take this range into consideration for playblastting to shotgun")
        self.cache_cut_checkbox.setChecked(0)
        self.cache_range_group.addButton(self.cache_cut_checkbox)
        self.cache_radiobox.addWidget(self.cache_cut_checkbox, 2,1,1,1)

        self.cache_range_checkbox = QtWidgets.QRadioButton("Custom:")
        self.cache_range_checkbox.setToolTip("Take this range into consideration for playblastting to shotgun")
        self.cache_range_checkbox.setChecked(1)
        self.cache_range_group.addButton(self.cache_range_checkbox)
        self.cache_radiobox.addWidget(self.cache_range_checkbox, 2,2,1,1)

        self.cache_head_lbl = QtWidgets.QLabel("start")
        self.cache_head_lbl.setStyleSheet("color: #787878; background-color: rgba(255,255,255,0);")
        self.cache_radiobox.addWidget(self.cache_head_lbl, 2,3,1,1)
        self.cache_head_field = QtWidgets.QLineEdit(str(getLowRange))
        self.cache_head_field.setStyleSheet("color: #767676; background-color: rgba(255,255,255,25);")
        self.cache_head_field.setFixedHeight(25)
        self.cache_head_field.setFixedWidth(100)
        self.cache_radiobox.addWidget(self.cache_head_field, 2,4,1,1)
        self.cache_toe_lbl = QtWidgets.QLabel("end")
        self.cache_toe_lbl.setStyleSheet("color: #787878; background-color: rgba(255,255,255,0);")
        self.cache_radiobox.addWidget(self.cache_toe_lbl, 2,5,1,1)
        self.cache_toe_field = QtWidgets.QLineEdit(str(getHiRange+1))
        # self.cache_toe_field = QtWidgets.QLineEdit(str(wk_out_value + 1))
        self.cache_toe_field.setFixedHeight(25)
        self.cache_toe_field.setFixedWidth(100)
        self.cache_toe_field.setStyleSheet("color: #767676; background-color: rgba(255,255,255,25);")
        self.cache_radiobox.addWidget(self.cache_toe_field, 2, 6,1,1)

        self.playblast_radiobox = QtWidgets.QGridLayout()
        self.masterLayout.addLayout(self.playblast_radiobox, 2,0,1,1)
        self.playblast_range_group = QtWidgets.QButtonGroup(self.playblast_radiobox)
        self.blast_title = QtWidgets.QLabel("Blast length")
        self.blast_title.setStyleSheet("color: #787878; background-color: rgba(255,255,255,0);")
        self.playblast_radiobox.addWidget(self.blast_title)

        self.playblast_work_checkbox = QtWidgets.QRadioButton("Work: " + str(int(wk_strt_value-1)) + '-' + str(int(wk_out_value+1)))
        self.playblast_work_checkbox.setToolTip("Take this range into consideration for playblastting to shotgun")
        self.playblast_work_checkbox.setChecked(0)
        self.playblast_work_checkbox.setStyleSheet("color: #ffff12;")
        self.playblast_radiobox.addWidget(self.playblast_work_checkbox, 2,0,1,1)

        self.playblast_cut_checkbox = QtWidgets.QRadioButton("Cut: " + str(cut_in_value) + '-' + str(cut_out_value))
        self.playblast_cut_checkbox.setToolTip("Take this range into consideration for playblastting to shotgun")
        self.playblast_cut_checkbox.setChecked(0)
        self.playblast_radiobox.addWidget(self.playblast_cut_checkbox, 2, 1, 1,1)

        self.playblast_range_checkbox = QtWidgets.QRadioButton("Custom:")
        self.playblast_range_checkbox.setToolTip("Take this range into consideration for playblastting to shotgun")
        self.playblast_range_checkbox.setChecked(1)
        self.playblast_radiobox.addWidget(self.playblast_range_checkbox, 2,2,1,1)

        self.playblast_head_lbl = QtWidgets.QLabel("start")
        self.playblast_head_lbl.setStyleSheet("color: #787878; background-color: rgba(255,255,255,0);")
        self.playblast_radiobox.addWidget(self.playblast_head_lbl, 2,3,1,1)
        
        self.playblast_head_field = QtWidgets.QLineEdit(str(getLowRange - 1))
        self.playblast_head_field.setStyleSheet("color: #767676; background-color: rgba(255,255,255,25);")
        self.playblast_head_field.setFixedHeight(25)
        self.playblast_head_field.setFixedWidth(100)
        self.playblast_radiobox.addWidget(self.playblast_head_field, 2,4,1,1)        self.playblast_toe_lbl = QtWidgets.QLabel("end")
        self.playblast_toe_lbl.setStyleSheet("color: #787878; background-color: rgba(255,255,255,0);")
        self.playblast_radiobox.addWidget(self.playblast_toe_lbl, 2,5,1,1)
        self.playblast_toe_field = QtWidgets.QLineEdit(str(getHiRange + 1))
        self.playblast_toe_field.setFixedHeight(25)
        self.playblast_toe_field.setFixedWidth(100)
        self.playblast_toe_field.setStyleSheet("color: #767676; background-color: rgba(255,255,255,25);")
        self.playblast_radiobox.addWidget(self.playblast_toe_field, 2,6,1,1)

        self.nuc_button = QtWidgets.QPushButton("activate all nucleus")
        self.nuc_button.clicked.connect(lambda :self.turn_on_nuc())
        self.window_layer_01.addWidget(self.nuc_button)

        self.sim_vis_button = QtWidgets.QPushButton("Enforce Sim Visibility")
        self.sim_vis_button.clicked.connect(lambda:self.sim_vis())
        self.window_layer_01.addWidget(self.sim_vis_button)

        self.post_vis_button = QtWidgets.QPushButton("Enforce postTech Visibility")
        self.post_vis_button.clicked.connect(lambda:self.postTech_vis())
        self.window_layer_01.addWidget(self.post_vis_button)

        self.anim_vis_button = QtWidgets.QPushButton("Enforce Anim Visibility")
        self.anim_vis_button.clicked.connect(lambda:self.anim_vis())
        self.window_layer_01.addWidget(self.anim_vis_button)

        self.open_folder_button = QtWidgets.QPushButton("Open folder")
        self.open_folder_button.clicked.connect(lambda:self.open_folder_button_function())
        self.window_layer_01.addWidget(self.open_folder_button)

        self.load_button = QtWidgets.QPushButton("launch")
        self.load_button.clicked.connect(lambda:self._performFunct())
        self.window_layer_01.addWidget(self.load_button)
    def open_folder_button_function(self):
        os.system('xdg-open "%s"' % getCachePath)

    def sim_vis(self):
        getall_postT = cmds.ls("*:*sim")
        if len(getall_postT)>0:
            for each in getall_postT:
                try:
                    get_val_active = cmds.getAttr(each+".visibility")
                    if get_val_active == 1:
                        print (each+ " is already visibile. skipping.")
                        pass
                    else:
                        cmds.setAttr(each+".visibility", 1)
                        print (each + " is now visibile")
                except:
                    pass 
        getall_preT = cmds.ls("*:*preTech")
        if len(getall_preT)>0:
            for each in getall_preT:
                try:
                    get_val_active = cmds.getAttr(each+".visibility")
                    if get_val_active == 0:
                        print (each+ " is already invisibile. skipping.")
                        pass
                    else:
                        cmds.setAttr(each+".visibility", 0)
                        print (each + " is now invisibile" )
                except:
                    pass 
        getall_rig = cmds.ls("*:*postTech")
        if len(getall_rig)>0:
            for each in getall_rig:
                try:
                    get_val_active = cmds.getAttr(each+".visibility")
                    if get_val_active == 0:
                        print (each+ " is already invisibile. skipping.")
                        pass
                    else:
                        cmds.setAttr(each+".visibility", 0)
                        print (each + " is now invisibile" )
                except:
                    pass          
        getall_rig = cmds.ls("*:animGeo")
        if len(getall_rig)>0:
            for each in getall_rig:
                try:
                    get_val_active = cmds.getAttr(each+".visibility")
                    if get_val_active == 0:
                        print (each+ " is already invisibile. skipping.")
                        pass
                    else:
                        cmds.setAttr(each+".visibility", 0)
                        print (each + " is now invisibile" )
                except:
                    pass        

    def anim_vis(self):
        getall_postT = cmds.ls("*:animGeo")
        if len(getall_postT)>0:
            for each in getall_postT:
                try:
                    get_val_active = cmds.getAttr(each+".visibility")
                    if get_val_active == 1:
                        print (each+ " is already visibile. skipping.")
                        pass
                    else:
                        cmds.setAttr(each+".visibility", 1)
                        print( each + " is now visibile" )
                except:
                    pass 
        getall_preT = cmds.ls("*:*preTech")
        if len(getall_preT)>0:
            for each in getall_preT:
                try:
                    get_val_active = cmds.getAttr(each+".visibility")
                    if get_val_active == 0:
                        print (each+ " is already invisibile. skipping.")
                        pass
                    else:
                        cmds.setAttr(each+".visibility", 0)
                        print (each + " is now invisibile" )
                except:
                    pass 
        getall_rig = cmds.ls("*:*postTech")
        if len(getall_rig)>0:
            for each in getall_rig:
                try:
                    get_val_active = cmds.getAttr(each+".visibility")
                    if get_val_active == 0:
                        print (each+ " is already invisibile. skipping.")
                        pass
                    else:
                        cmds.setAttr(each+".visibility", 0)
                        print (each + " is now invisibile") 
                except:
                    pass                     
        getall_rig = cmds.ls("*:*sim")
        if len(getall_rig)>0:
            for each in getall_rig:
                try:
                    get_val_active = cmds.getAttr(each+".visibility")
                    if get_val_active == 0:
                        print (each+ " is already invisibile. skipping.")
                        pass
                    else:
                        cmds.setAttr(each+".visibility", 0)
                        print (each + " is now invisibile") 
                except:
                    pass                     


    def postTech_vis(self):
        getall_postT = cmds.ls("*:*postTech")
        if len(getall_postT)>0:
            for each in getall_postT:
                try:
                    get_val_active = cmds.getAttr(each+".visibility")
                    if get_val_active == 1:
                        print (each+ " is already visibile. skipping.")
                        pass
                    else:
                        cmds.setAttr(each+".visibility", 1)
                        print (each + " is now visibile") 
                except:
                    pass 
        getall_preT = cmds.ls("*:*preTech")
        if len(getall_preT)>0:
            for each in getall_preT:
                try:
                    get_val_active = cmds.getAttr(each+".visibility")
                    if get_val_active == 0:
                        print (each+ " is already invisibile. skipping.")
                        pass
                    else:
                        cmds.setAttr(each+".visibility", 0)
                        print (each + " is now invisibile") 
                except:
                    pass 
        getall_rig = cmds.ls("*:*animGeo")
        if len(getall_rig)>0:
            for each in getall_rig:
                try:
                    get_val_active = cmds.getAttr(each+".visibility")
                    if get_val_active == 0:
                        print (each+ " is already invisibile. skipping.")
                        pass
                    else:
                        cmds.setAttr(each+".visibility", 0)
                        print (each + " is now invisibile" )
                except:
                    pass                     
        getall_rig = cmds.ls("*:*sim")
        if len(getall_rig)>0:
            for each in getall_rig:
                try:
                    get_val_active = cmds.getAttr(each+".visibility")
                    if get_val_active == 0:
                        print (each+ " is already invisibile. skipping.")
                        pass
                    else:
                        cmds.setAttr(each+".visibility", 0)
                        print (each + " is now invisibile" )
                except:
                    pass                     
    def blast_and_play(self):
        # startframe, endFrame = self.get_range_for_cache()
        # cmds.playbackOptions(min=startframe,  max=endFrame)     
        wk_strt_value, wk_out_value = self.get_range_for_play()   
        # strt_rng =int(wk_strt_value)-1
        # end_rng=cmds.playbackOptions(q=1, max=1)
        focPane = [(each) for each in cmds.getPanel(vis=1) if "model" in each]
        for each in focPane:
            if cmds.modelEditor(each, q=1, av=1) == True:
                mm.eval('setRendererInModelPanel "vp2Renderer" {0}'.format(each))        
        mm.eval('setPolyCountVisibility(1);')
        folder_strt = '/'.join(cmds.file(q=1, location=1).split('/')[:-5])
        scn_name=str(cmds.file(q=1, location=1)).split('/')[-1].split(".")[0]
        gotten_name=str(cmds.file(q=1, location=1)).split('/')[-1].split(".")[0]+"-playblast-half1712x903_vdf8"
        gotten_path = "{}/work/edeglau/maya/images/temp/{}".format(folder_strt, M_USER, gotten_name)
        print (gotten_path)
        sel_NumMn=cmds.playbackOptions(q=1, min=1)
        sel_NumMn_reset=cmds.playbackOptions(q=1, min=1)+1
        cmds.currentTime(sel_NumMn)
        cmds.playblast(format="image", st=wk_strt_value, et=wk_out_value, filename=gotten_path, sequenceTime=0, clearCache=1, viewer= 1,  showOrnaments=1, offScreen=1, fp=4, percent = 100, compression = "jpg",  quality = 100, widthHeight = (1712, 903))
        mm.eval('setPolyCountVisibility(0);')
        for each in focPane:
            if cmds.modelEditor(each, q=1, av=1) == True:
                cmds.modelEditor(each, e=1, rnm="base_OpenGL_Renderer")  

    def turn_on_nuc(self):
        getall_technuc = cmds.ls("*:techRig")
        if len(getall_technuc)>0:
            for each in getall_technuc:
                try:
                    get_val_active = cmds.getAttr(each+".Nucleus")
                    if get_val_active == 1:
                        print (each+ ".Nucleus is already active. skipping.")
                        pass
                    else:
                    else:
                        cmds.setAttr(each+".Nucleus", 1)
                        print (each + " is now active") 
                except:
                    pass 
        getall_nuc = cmds.ls(type = "nucleus")
        if len(getall_nuc)>0:
            for each in getall_nuc:
                get_val_active = cmds.getAttr(each+".enable")
                if get_val_active == 1:
                    print( each + ".enable is already active. skipping.")
                    pass
                else:
                    try:
                        cmds.setAttr(each+".enable", 1)
                        print (each + " is now active")    
                    except:
                        pass    def _performFunct(self):
        # self.postTech_vis()
        self.turn_on_nuc()
        disName = self.save_spinner
        queryColor = disName.currentText()
        getSel = cmds.ls(sl=1)
        if queryColor == 'increment+play':
            getNewFile = self.checkFile()
            if getNewFile == True:
                return
            else:
                pass
            self.incrementalSave()
            self.blast_and_play()
        elif queryColor == 'save+play':
            self.fileSave()
            self.blast_and_play()     
        elif queryColor == 'increment, cache & play all clth':
            self.incrementalSave()
            time.sleep(1.3)
            try:
                self.createNCloth()
            except:
                return
            time.sleep(1.3)
            self.blast_and_play()     
        elif queryColor == 'increment, cache & play all hr':
            getNewFile = self.checkFile()
            if getNewFile == True:
                return
            else:
                pass
            self.incrementalSave()
            try:
                self.createHCache()
            except:
                return
            self.blast_and_play()         
        elif queryColor == 'increment, cache & play sel':
            getNewFile = self.checkFile()
            if getNewFile == True:
                return
            else:
                pass
            self.incrementalSave()
            try:
                self.createCacheselected()
            except:
                return
            self.blast_and_play() 
        elif queryColor == 'cache & play all clth':
            try:
                self.createNCloth()
            except:
                return
            self.blast_and_play()
            self.just_Save() 
        elif queryColor == 'cache & play all hr':
            print ("hair")
            try:
                self.createHCache()
            except:
                return
            self.blast_and_play() 
            self.just_Save() 
        elif queryColor == 'cache & play sel':
            print ("plog")
            try:
                self.createCacheselected()
            except:
                return
            self.blast_and_play()
        elif queryColor == 'cache all clth':
            try:
                self.createNCloth()
            except:
                return
        elif queryColor == 'cache all hr':
            try:
                self.createHCache()
            except:
                return
        elif queryColor == 'cache all nstuff':
            try:
                self.createNCloth()
            except:
                print ("no ncloth found")
                return            
            try:
                self.createHCache()
            except:
                print ("no nhair found")
                return        elif queryColor == 'play':
            self.blast_and_play() 
        elif queryColor == 'cache sel':
            getNewFile = self.checkFile()
            if getNewFile == True:
                return
            else:
                pass
            # self.incrementalSave()
            try:
                self.createCacheselected()
            except:
                return
            # self.blast_and_play()             

    def get_range_for_cache(self):
        print (self.cache_range_checkbox.isChecked())
        if self.cache_range_checkbox.isChecked() == True:
            first_frame = self.cache_head_field
            get_first_frame = first_frame.text()
            print (get_first_frame)
            # get_first_frame = get_first_frame.split('.')[0]
            get_first_frame = str(get_first_frame)
            get_last = self.cache_toe_field  
            get_last_frame = get_last.text()  
            # get_last_frame = get_last_frame.split('.')[0]
            get_last_frame = str(get_last_frame)
            # if get_true_last<int(get_last_frame):
            #     get_last_frame = get_true_last
            # else:
            #     get_last_frame = get_last_frame        
        elif self.cache_cut_checkbox.isChecked() == True:
            get_first_frame = str(cut_in_value)
            get_last_frame = str(cut_out_value)
        elif self.cache_work_checkbox.isChecked() == True:
            get_first_frame = str(int(wk_strt_value)-1)
            get_last_frame = str(int(wk_out_value)+1)
        print ("cache_range")
        print (get_first_frame, get_last_frame)
        return get_first_frame, get_last_frame
    def get_range_for_play(self):
        if self.playblast_range_checkbox.isChecked() == True:
            first_frame = self.playblast_head_field
            get_first_frame = first_frame.text()
            # get_first_frame = get_first_frame.split('.')[0]
            get_first_frame = str(get_first_frame)
            get_last = self.playblast_toe_field  
            get_last_frame = get_last.text()  
            # get_last_frame = get_last_frame.split('.')[0]
            get_last_frame = str(get_last_frame)
            # if get_true_last<int(get_last_frame):
            #     get_last_frame = get_true_last
            # else:
            #     get_last_frame = get_last_frame        
        elif self.playblast_cut_checkbox.isChecked() == True:
            get_first_frame = str(cut_in_value)
            get_last_frame = str(cut_out_value)
        elif self.playblast_work_checkbox.isChecked() == True:
            get_first_frame = str(int(wk_strt_value)-1)
            get_last_frame = str(int(wk_out_value)+1)
        print ("play range")
        print (get_first_frame, get_last_frame)
        return get_first_frame, get_last_frame

    def incrementalSave(self):
        maya.mel.eval('IncrementAndSave;')
        getScenePath=cmds.file(q=1, location=1)
        print ("file save: "+getScenePath)

    def just_Save(self):
        maya.mel.eval('file -save')
        getScenePath = cmds.file(q=1, location=1)
        print ("file save: "+getScenePath)
    def createCacheselected(self):
        getNSystems = cmds.ls(sl=1, fl=1)
        self.createCache_callup(getNSystems)
        
        
    def createHCache(self):
        focPane = [(each) for each in cmds.getPanel(vis=1) if "model" in each]
        for each in focPane:
            if cmds.modelEditor(each, q=1, av=1) == True:
                cmds.modelEditor(each, e=1, allObjects=0)  
        grabsystem = cmds.ls(type = "hairSystem")
        cmds.select(grabsystem, r=1)
        for each in grabsystem:
            getCache = [(nodes) for nodes in cmds.listHistory(each) if cmds.nodeType(nodes) == "cacheBlend"]
            if len(getCache)>0:
                cmds.delete(getCache)
            getCache = [(nodes) for nodes in cmds.listHistory(each) if cmds.nodeType(nodes) == "cacheFile"]
            if len(getCache)>0:
                cmds.delete(getCache)  
            else:
                pass
        print ("cleared caches" )       
        cmds.select(grabsystem, r=1)
        if ":" in grabsystem[0]:
            interroName = grabsystem[0].split(":")[-1]+"_"
        else:
            interroName = grabsystem[0]+"_"
        newName, cachFolder = self.checkCacheFile()    
        startframe, endFrame = self.get_range_for_cache()
        cmds.playbackOptions(min=startframe,  max=endFrame)
        print (cachFolder)        command = 'doCreateNclothCache 5{"2", "1", "10", "OneFile", "0", "%s", "1", "", "0", "new", "0", "1", "1", "0", "1", "mcx"};' %( cachFolder)
        maya.mel.eval(command)
        for each in focPane:
            if cmds.modelEditor(each, q=1, av=1) == True:
                cmds.modelEditor(each, e=1, allObjects=1)  

    def createNCloth(self):
        focPane = [(each) for each in cmds.getPanel(vis=1) if "model" in each]
        for each in focPane:
            if cmds.modelEditor(each, q=1, av=1) == True:
                cmds.modelEditor(each, e=1, allObjects=0)         
                print ("ALL OBJECTS ARE HIDDEN  IN VIEWPORT!!! improves cache speed.")
        if len(cmds.ls(sl=1)) <1:
            grabsystem = cmds.ls(type = "nCloth")
        else:
            allgrabs = cmds.ls(sl=1)
            grabonlysystem = [(each) for each in allgrabs if cmds.nodeType(each) == "nCloth"]
            grabtransform = [(each) for each in allgrabs if cmds.nodeType(each) == "transform"]
            grabmoresystem = [(each) for each in allgrabs if cmds.listRelatives(each, c=1, type = "nCloth") ]
            grabsystem = grabonlysystem+grabmoresystem
        try:
            cmds.select(grabsystem, r=1)
            print ("found {}".format(grabsystem))
        except:
            print ("nCloth can't be located")
        for each in grabsystem:
            print ("checking for clean cache in {}".format(each))
            getCache = [(nodes) for nodes in cmds.listHistory(each) if cmds.nodeType(nodes) == "cacheBlend"]
            if len(getCache)>0:
                cmds.delete(getCache)
                print ("deleted cacheBlend: "+str(getCache) )
            getCache = [(nodes) for nodes in cmds.listHistory(each) if cmds.nodeType(nodes) == "cacheFile"]
            if len(getCache)>0:
                cmds.delete(getCache)   
                print ("deleted cacheFiles: "+str(getCache) )
        print ("done checking the cleanliness of caches")
        if ":" in grabsystem[0]:
            interroName = grabsystem[0].split(":")[-1]+"_"
        else:
            interroName = grabsystem[0]+"_"
        print ("cache name = {}".format(interroName))
        newName, cachFolder = self.checkCacheFile()        command = 'doCreateNclothCache 5{"2", "1", "10", "OneFile", "0", "%s", "1", "", "0", "new", "0", "1", "1", "0", "1", "mcx"};' %( cachFolder)
        maya.mel.eval(command)   
        for each in focPane:
            if cmds.modelEditor(each, q=1, av=1) == True:
                cmds.modelEditor(each, e=1, allObjects=1) 
                print ("ALL OBJECTS ARE UNHIDDEN IN VIEWPORT!!!") 


    def createNClothV1(self):
        grabsystem = cmds.ls(type = "nCloth")
        cmds.select(grabsystem, r=1)
        for each in grabsystem:
            getCache = [(nodes) for nodes in cmds.listHistory(each) if cmds.nodeType(nodes) == "cacheBlend"]
            if len(getCache)>0:
                cmds.delete(getCache)
            getCache = [(nodes) for nodes in cmds.listHistory(each) if cmds.nodeType(nodes) == "cacheFile"]
            if len(getCache)>0:
                cmds.delete(getCache)          
        cmds.select(grabsystem, r=1)        newName, cachFolder=self.checkCacheFile()         
        startframe, endFrame = self.get_range_for_cache()
        cmds.playbackOptions(min=startframe,  max=endFrame)        command = 'doCreateNclothCache 5{"2", "1", "10", "OneFile", "0", "%s", "1", "", "0", "new", "0", "1", "1", "0", "1", "mcx"};' %( cachFolder)
        maya.mel.eval(command)    def createNClothV2(self):
        print ("cloths")
        if len(cmds.ls(sl=1)) <1:
            grabsystem = cmds.ls(type = "nCloth")
        else:
            grabsystem = cmds.ls(sl=1)
        print (grabsystem)
        cmds.select(grabsystem, r=1)
        for each in grabsystem:
            getCache = [(nodes) for nodes in cmds.listHistory(each) if cmds.nodeType(nodes) == "cacheBlend"]
            if len(getCache)>0:
                cmds.delete(getCache)
            getCache = [(nodes) for nodes in cmds.listHistory(each) if cmds.nodeType(nodes) == "cacheFile"]
            if len(getCache)>0:
                cmds.delete(getCache) 
        print ("deleted histories" )        
        if ":" in grabsystem[0]:
            interroName = grabsystem[0].split(":")[-1]+"_"
        else:
            interroName = interroName+"_"
        newName, cachFolder = self.checkCacheFile()        print ("got here")
        command = 'doCreateNclothCache 5{"2", "1", "10", "OneFilePerFrame", "0", "%s", "1", "", "0", "new", "0", "1", "1", "0", "1", "mcx"};' %( cachFolder)
        # command = 'doCreateNclothCache 5{"2", "1", "10", "OneFile", "0", "%s", "1", "", "0", "new", "0", "1", "1", "0", "1", "mcx"};' %( cachFolder)
        maya.mel.eval(command)   

    def getCache(self):
        getNsystems = cmds.ls(type = "nCloth")
        cmds.select(getNSystems)
        getSel = cmds.ls(sl=1, fl=1)
        self.createCache_callup(getNsystems)
    
    def createCache_callup(self, getNSystems):
        print ("got here")
        if len(getNSystems)>0:
            for the_sel in getNSystems:
                if cmds.nodeType(the_sel) == "mesh":
                    try:
                        grabMesh = [(each) for each in cmds.listRelatives(the_sel, ad=1, type = "mesh") if "Orig" not in each]
                    except:
                        print ("can't")
                        pass
                if cmds.nodeType(the_sel) != "nCloth":
                    try:
                        grabmoresystem = [(each) for each in cmds.listRelatives(the_sel, ad=1, type = "nCloth") ]
                    except:
                        pass
                if cmds.nodeType(the_sel) != "hairSystem":
                    try:
                        grabmorechildHairsystem = [(each) for each in cmds.listRelatives(the_sel, ad=1, type = "hairSystem") ]        
                    except:
                        pass
                grabsystem = grabonlysystem+grabmoresystem+grabonlyHairsystem+grabmorechildHairsystem+grabMesh
                collectionHair = grabonlysystem+grabmoresystem
                collectionCloth = grabonlyHairsystem+grabmorechildHairsystem
        else:
            print ("select something")
            return        print (grabsystem)
        for each in grabsystem:
            getCache = [(nodes) for nodes in cmds.listHistory(each) if cmds.nodeType(nodes) == "cacheBlend"]
            if len(getCache)>0:
                cmds.delete(getCache)
            getCache = [(nodes) for nodes in cmds.listHistory(each) if cmds.nodeType(nodes) == "cacheFile"]
            if len(getCache)>0:
                cmds.delete(getCache)          
        print (getNSystems)
        # cmds.select(getNsystems, r=1)
        if ":" in getNSystems[0]:
            interroName = getNSystems[0].split(":")[-1]+"_"
        else:
            interroName = interroName+"_"
        newName, cachFolder=self.checkCacheFile()       
        startframe, endFrame = self.get_range_for_cache()
        cmds.playbackOptions(min=startframe,  max=endFrame)
        # newName = filename_string
        print (cachFolder)
        if len(collectionHair)>0:
        # if cmds.nodeType(getNSystems[0])=="hairSystem":
            print ("hair here")
            cmds.select(collectionHair)
            # command = 'doCreateNclothCache 5{"2", "1", "10", "OneFile", "0", "", "1", "%s", "0", "rename", "0", "1", "1", "0", "1", "mcx"};'%newName
            command = 'doCreateNclothCache 5{"2", "1", "10", "OneFile", "0", "%s", "1", "", "0", "new", "0", "1", "1", "0", "1", "mcx"};' %( cachFolder)
            maya.mel.eval(command)
        if len(collectionCloth)>0:
        # if cmds.nodeType(getNSystems[0])=="nCloth":
            print (" cloth here ")
            cmds.select(collectionCloth)
            # command = 'doCreateNclothCache 5{"2", "1", "10", "OneFile", "0", "", "0", "%s", "0", "rename", "0", "1", "1", "0", "1", "mcx"};'%newName
            command = 'doCreateNclothCache 5{"2", "1", "10", "OneFile", "0", "%s", "1", "", "0", "new", "0", "1", "1", "0", "1", "mcx"};' %( cachFolder)
            maya.mel.eval(command)          
        if len(grabMesh)>0:
            print ("mesh here")
        # if cmds.nodeType(cmds.ls(sl=1)[0])=="transform":
            cmds.select(grabMesh)
            command = 'doCreateGeometryCache 6 { "2", "1", "10", "OneFile", "0", "%s","0","","0", "add", "0", "1", "1","0","1","mcx","0" } ;' %( cachFolder)
            maya.mel.eval(command)

    def checkFile(self):
        interrogateName = getScenePath.split(".")[0]
        grabfiles = [(name) for dirpath, dirnames, files in os.walk(currentShot) for name in files if interrogateName in name and re.split(r'(\d+)', name)]
        try:
            findFiles = [(each) for each in files if each.split(".")[-2:-1][0].isdigit()]
            getLast = max(findFiles)
            subname = getLast.split(".")[-2:-1][0]
            getNum = "%04d" %(int(subname)+1,)
            newName = interrogateName+getNum
        except:
            newName = interrogateName+str(0000)
        return newName
    def checkCacheFileV1(self, interrogateName):
        print (getCachePath)
        grabfiles=[(name) for dirpath, dirnames, files in os.walk(getCachePath) for name in files if interrogateName in name and re.split(r'(\d+)', name)]
        print (grabfiles)
        print (interrogateName)
        if grabfiles:
            try:
                findFiles = [(each) for each in grabfiles if each.split("_")[-1].split(".")[0].isdigit()]
                getLast = max(findFiles)
                subname = getLast.split("_")[-1].split("_")[0]
                getNum = "%04d" %(int(subname)+1,)
                newName = interrogateName+str(getNum)
            except:
                newName = interrogateName+'0000'
        else:
            newName = interrogateName+'0000'
        print (newName)
        return newName
    

    def checkCacheFile(self):
        cachefolderStart=getCachePath
        number = 0000
        getScene = cmds.file(q=1, sn=1, shn=1)
        getFilename = getScene.split(".")[:-1]
        getFilename = '_'.join(getFilename)+"_"+str(getUser)+"_nCache"
        getnewcachefolder = getFilename+"_"+str("%04d" % (number,))
        makecachefolder = cachefolderStart+"/"+getnewcachefolder
        if os.path.exists(makecachefolder): 
            get_vr_folders=[(dirnames) for dirpath, dirnames, files in os.walk(cachefolderStart)][0]
            get_vr_folders=[(each) for each in get_vr_folders if each.split("_")[-1].isdigit()]
            get_top = max(get_vr_folders)
            number = get_top.split("_")[-1]
            if "v" not in number:
                number = int(number)            else:
                number = re.sub("\D", "", number)
            number = int(number)
            number += 1
            getnewcachefolder = getFilename+"_"+str("%04d" % (number,))
            makecachefolder = cachefolderStart+"/"+getnewcachefolder
            os.makedirs(makecachefolder)
            print ("created " + makecachefolder)
        if not os.path.exists(makecachefolder): 
            os.makedirs(makecachefolder) 
            print ("created " + makecachefolder)
        print (getFilename, makecachefolder)
        return getFilename, makecachefolder



cachwin=save_gen()
cachwin.show()


