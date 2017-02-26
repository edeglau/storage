
__author__ = "Elise Deglau"
__ver__ = '1.0'


# standard
import os, sys, operator, re, glob, getpass, subprocess, shutil, string, random, ast, webbrowser, time, datetime
import ast
import os.path
import datetime
from subprocess import Popen, PIPE
from os import stat, listdir, walk
from pwd import getpwuid
from os.path import isfile, join

# 3rd party
import PyQt4
from PyQt4 import QtCore, QtGui, Qt
from PyQt4.QtGui import QWidget, QRadioButton, QGridLayout, QLabel, \
    QTableWidget, QComboBox, QKeySequence, QToolButton, QPlainTextEdit, QPushButton,QBoxLayout, \
    QClipboard, QTableWidgetItem, QCheckBox, QVBoxLayout, QHBoxLayout, \
    QPixmap, QLineEdit, QListWidget, QTextEdit, QSizePolicy, QFrame, QPalette, QColor, \
    QFont, QAbstractItemView, QMenu, QMessageBox
from PyQt4.QtCore import SIGNAL

buttonGrp = []
_failed_comments = [
                "defaultText", 
                "", 
                "-", 
                "_", 
                "asdf", 
                "asd", 
                ".", 
                "oo", 
                "0", 
                "00", 
                " ", 
                "qwer", 
                "qwerty"
                ]

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
defaultText = "defaultText"
presetlist = ["load"]
typesOfReview = ['review', 'review_anim', 'delivery']
availableStyles = ['darkOrange']
styleSheetFile = availableStyles[0]
headers = ('Name', 'Date', 'Path', 'Sub')
dsktop_rev_build = ["Create Artist Review", "Build list", "Append blast", "Remove blast"]
dsktop_rev_list = ['Artist Review List']
setDefaultType = ['review']
col1, col2, col3, col4 =  240, 160, 500, 50
regularDict = {"darkRed":(150,70,70), 
            "red":(180,50,50), 
            "yellow":(120,120,70), 
            "green":(70, 150, 70), 
            "blue":(50,100,200), 
            "grey":(50,50,50), 
            "light_grey":(70,70,70), 
            "shotgun":(70,80,100)
            }
_developer = [__author__]
_get_user = getpass.getuser()
_project = os.getenv("M_JOB")
_scene = os.getenv("SEQUENCE_SHOT_")
_shot = os.getenv("M_LEVEL")
_dept_task = os.getenv("M_TASK")
_getDeptrv_folder='/jobs/' + _project + '/' + _scene + '/' + _shot + '/PRODUCTS/images/'   
_projects = '/jobs/' + _project
_proj_scene_name = os.listdir(_projects)
_proj_scene_name = sorted(_proj_scene_name)
_format_ext = ".jpg"
_play_list_path = '/jobs/' + _project + '/' + _scene + '/' + _shot + '/TASKS/' + _dept_task + "/maya/"
_sgVarFilePath = '/jobs/%s/%s/%s/TECH/lib/shotgun/setshot.d/sgvars' % (_project, _scene, _shot)
_user_path_pbmovs = '/home/' + _get_user
by_detail = ["folder", "file"]
win_title="mSubmit Manager " + __ver__


class DropMenu(QtGui.QWidget):
    def __init__(self, detailMessge, title, make_new_content):
        super(DropMenu, self).__init__()
        self.initUI(detailMessge, title, make_new_content)

    def initUI(self, detailMessge, title, make_new_content):     
        self.setWindowTitle(title)
        self.layout = QVBoxLayout()
        self.btnlayout = QBoxLayout(1)
        self.playlist_names = QComboBox()
        self.playlist_names.addItems(detailMessge)
        self.layout.addWidget(self.playlist_names)
        self.layout.addLayout(self.btnlayout)
        self.sel_button = QPushButton("append")
        self.connect(self.sel_button, SIGNAL("clicked()"),
                    lambda: self.gotoAppend(make_new_content))
        self.btnlayout.addWidget(self.sel_button)
        self.setLayout(self.layout)

    def gotoAppend(self, make_new_content):
        get_artist_review_list = self.playlist_names
        get_artist_review_list = get_artist_review_list.currentText()
        access_main = mSubManagerWin()
        access_main.append_artist_review(get_artist_review_list, make_new_content)
        self.close()


class mSubManagerWin(QtGui.QMainWindow):
    '''mSubmit Manager
    This is a GUI for artists to manage and submit playblasts. 
    Query the known areas in which Method playblasts live. 
    This also compares between shot gun variable file (sgvar) for parameters such as frame range.
    '''
    def __init__(self, parent = None):
        super(mSubManagerWin, self).__init__(parent)
        shot_len_value, cut_in_value, cut_out_value, wk_strt_value, wk_out_value, cut_shouldbe_in_value, cut_shouldbe_out_value\
                ,versioning_dictionary = self.set_defaults(_scene, _shot)        
        try:
            winTitle = win_title + '              ' + _project + " : " + _shot + " : (F" + str(shot_len_value) + ")   :   ( " + str(wk_strt_value-1) + "  |[ " + str(wk_strt_value) + " <<<[" + str(cut_in_value) + "-" + str(cut_out_value) + "]>>> " + str(wk_out_value) + " ]|  " + str(wk_out_value + 1) + " )"
        except IndexError:
            winTitle = win_title + '              ' + _project + " : " + _shot           
        print 'Launching: ' + win_title
        get_depts = os.listdir(_getDeptrv_folder)

        ssh_file = open(os.path.join(__location__, styleSheetFile + ".stylesheet"), 'r')
        self.style_data = ssh_file.read()
        ssh_file.close
        self.setStyleSheet(self.style_data)

        ##WINDOW SETUP
        self.setWindowTitle(winTitle)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.masterLayout = QGridLayout(self.central_widget)
        self.masterLayout.setAlignment(QtCore.Qt.AlignTop)

        ##VERTICAL LAYOUT
        self.vertical_order_layout = QtGui.QBoxLayout(2)
        self.vertical_order_layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignVCenter)
        self.masterLayout.addLayout(self.vertical_order_layout, 0,0,1,1)

        self.topDivideLayout = QGridLayout()
        self.botDivideLayout = QGridLayout()
        self.upper_layout = QGridLayout()
        self.topDivideLayout.addLayout(self.upper_layout, 0,0,1,1)

        self.lower_layout = QGridLayout()
        self.lower_layout.setAlignment(QtCore.Qt.AlignTop)
        self.botDivideLayout.addLayout(self.lower_layout, 0,0,1,1)

        self.midLayout = QGridLayout()
        self.midLayout.setAlignment(QtCore.Qt.AlignTop)
        self.topDivideLayout.addLayout(self.midLayout, 2,0,1,1)

        self.base_layout = QGridLayout()
        self.base_layout.setAlignment(QtCore.Qt.AlignTop)
        self.botDivideLayout.addLayout(self.base_layout, 2,0,1,1)        

        self.top = QtGui.QFrame(self)
        self.top.setFrameShape(QtGui.QFrame.StyledPanel)
        self.top.setLayout(self.topDivideLayout)
        
        self.bottom = QtGui.QFrame(self)
        self.bottom.setFrameShape(QtGui.QFrame.StyledPanel)
        self.bottom.setLayout(self.botDivideLayout)
        
        self.splitPlane = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.splitPlane.addWidget(self.top)
        self.splitPlane.addWidget(self.bottom)
        self.splitPlane.setSizes([650, 650])
        self.vertical_order_layout.addWidget(self.splitPlane)

        ##LAYERS
        self.top_upper_layer = QGridLayout()
        self.upper_layout.addLayout(self.top_upper_layer,1,0,1,1)

        self.top_lower_layer = QGridLayout()
        self.upper_layout.addLayout(self.top_lower_layer, 2,0,1,1)

        self.custom_path_layer = QGridLayout()
        self.upper_layout.addLayout(self.custom_path_layer, 3,0,1,1)

        self.playblast_list_layer = QGridLayout()
        self.midLayout.addLayout(self.playblast_list_layer,4,0,1,1)

        self.lower_framed_layer = QGridLayout()
        self.lower_framed_layer.setAlignment(QtCore.Qt.AlignTop)
        self.lower_layout.addLayout(self.lower_framed_layer, 0,0,1,1)
        
        ##FRAMES
        self.btm_upper_layer = QtGui.QGridLayout()
        self.btm_upper_layer.setContentsMargins(5,10,5,10)
        self.lower_but_frame = QtGui.QFrame()
        self.lower_but_frame.setFixedHeight(80)
        self.lower_but_frame.setLayout(self.btm_upper_layer)
        self.lower_layout.addWidget(self.lower_but_frame, 1,0,1,1)

        self.btm_lower_layer = QtGui.QGridLayout()
        self.btm_lower_layer.setAlignment(QtCore.Qt.AlignTop)
        self.btm_lower_layer.setContentsMargins(5,10,5,10)   
        self.web_frame = QtGui.QFrame()
        self.web_frame.setStyleSheet("background-color: #434343; border-style: solid; border-width: 2px; border-color:#434343;border-radius:8px;")
        self.btm_over_layout = QtGui.QGridLayout()
        self.btm_over_layout.setAlignment(QtCore.Qt.AlignTop)
        self.btm_over_layout.addLayout(self.btm_lower_layer, 0,0,1,1)
        self.btm_over_layout.addWidget(self.web_frame, 0,0,1,1)

        self.framed_setup_layer = QtGui.QGridLayout()
        self.framed_setup_layer.setContentsMargins(5,10,5,10)
        self.framed_setup_frame = QtGui.QFrame()
        self.framed_setup_frame.setStyleSheet("background-color: #434343; border-style: solid; border-width: 2px; border-color:#434343;border-radius:8px;")
        self.framed_setup_frame.setFixedHeight(100)
        self.framed_setup_frame.setLayout(self.framed_setup_layer)
        self.lower_framed_layer.addWidget(self.framed_setup_frame, 0,0,1,1)

        self.customLayout = QtGui.QGridLayout()
        self.customLayout.setContentsMargins(5,10,5,10)
        self.customFrame = QtGui.QFrame()
        self.customFrame.setStyleSheet("background-color: #454545; border-style: solid; border-width: 2px; border-color:#565656;border-radius:8px;")
        self.customFrame.setFixedHeight(80)
        self.customFrame.setLayout(self.customLayout)
        self.custom_path_layer.addWidget(self.customFrame, 0,0,1,1)

        self.list_frame = QFrame()
        self.list_frame.setStyleSheet("color: rgb" + str(regularDict.get("grey")))
        self.list_layout = QHBoxLayout()
        self.list_frame.setLayout(self.list_layout)

        ##FRAMED SUBLAYER
        self.frame_title_layout = QGridLayout()
        self.framed_setup_layer.addLayout(self.frame_title_layout, 0,0,1,1)
        self.frame_radio_layout = QGridLayout()
        self.framed_setup_layer.addLayout(self.frame_radio_layout, 1,0,1,1)
        self.frame_btn_layout = QGridLayout()
        self.lower_framed_layer.addLayout(self.frame_btn_layout, 2,0,1,1)
        self.msgBox = QGridLayout()
        self.frame_title_layout.addLayout(self.msgBox, 0,0,1,1)
        self.radiobox = QGridLayout()
        self.frame_title_layout.addLayout(self.radiobox, 1,0,1,1)

        ##WIDGETS

        ##TOP UPPER

        self.count_frames_checkbox=QCheckBox("live updates (may be slow)")
        self.count_frames_checkbox.setStyleSheet("color: #aaccff; background-color: rgba(255,255,255,25);")
        self.count_frames_checkbox.setToolTip("This will update the interface (counts frames, update dropdowns) as items are clicked and dropdowns change. If this is off, you need to hit 'Refresh' to force update the lists, dropdowns and frame counts")
        self.count_frames_checkbox.setContentsMargins(5,0,0,0)
        self.count_frames_checkbox.setChecked(0)
        self.count_frames_checkbox.stateChanged.connect(self.frame_set)
        self.top_upper_layer.addWidget(self.count_frames_checkbox, 0,0,1,1)

        self.dept_drp = QComboBox()
        self.dept_drp.addItems(get_depts)
        self.dept_drp.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self.dept_drp, SIGNAL("customContextMenuRequested(QPoint)"), self.dept_drp_r_click)
        deptindex = self.dept_drp.findText(_dept_task, QtCore.Qt.MatchFixedString)
        self.dept_drp.setCurrentIndex(deptindex)
        self.top_upper_layer.addWidget(self.dept_drp, 1,0,1,1)

        self.reviewtype_drp = QComboBox()
        self.reviewtype_drp.addItems(typesOfReview)
        self.top_upper_layer.addWidget(self.reviewtype_drp, 1,1,1,1)

        self.scene_drp = QComboBox()
        self.top_upper_layer.addWidget(self.scene_drp, 1,2,1,1)
        self.scene_drp.addItems(_proj_scene_name)
        self.scene_drp.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.scene_drp.customContextMenuRequested.connect(self.scene_drp_r_click)
        self.shot_drp = QComboBox()
        self.top_upper_layer.addWidget(self.shot_drp, 1,3,1,1)
        self.shot_drp.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self.shot_drp, SIGNAL("customContextMenuRequested(QPoint)"), self.shot_drp_r_click)

        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setToolTip("reset to current shot")
        self.connect(self.reset_btn, SIGNAL('clicked()'), lambda *args:self.reset_window(cut_in_value, cut_out_value))
        self.top_upper_layer.addWidget(self.reset_btn, 1,5,1,1)

        ##TOP LOWER

        self.launch_shotgun_btn = QPushButton("launch shotgun")
        self.launch_shotgun_btn.setStyleSheet("color: #b1b1b1; background-color: rgba%s;" %str(regularDict.get("shotgun")))
        self.connect(self.launch_shotgun_btn, SIGNAL('clicked()'), self.launch_shotgun)
        self.top_lower_layer.addWidget(self.launch_shotgun_btn, 0,0,1,1)

        self.launch_help_btn = QPushButton("Help")
        self.launch_help_btn.setStyleSheet("color: #b1b1b1; background-color: rgba%s;" %str(regularDict.get("shotgun")))
        self.connect(self.launch_help_btn, SIGNAL('clicked()'), self.launch_help)
        self.top_lower_layer.addWidget(self.launch_help_btn, 0,1,1,1)

        self.work_folder_btn = QPushButton("open workfolder")
        self.connect(self.work_folder_btn, SIGNAL('clicked()'), self._open_work_folder)
        self.top_lower_layer.addWidget(self.work_folder_btn, 0,2,1,1)

        self.artistlist_build_drp = QComboBox()
        self.artistlist_build_drp.addItems(dsktop_rev_build)
        self.artistlist_build_drp.setStyleSheet("color: #b1b1b1; background-color: rgba(175,70,70,50);")
        QtCore.QObject.connect(self.artistlist_build_drp, SIGNAL("currentIndexChanged(QString)"),
                                self.build_artist_review)
        self.artistlist_build_drp.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self.artistlist_build_drp, SIGNAL("customContextMenuRequested(QPoint)"), self.artist_rev_list_drp_r_click)
        self.list_layout.addWidget(self.artistlist_build_drp)
        self.top_lower_layer.addWidget(self.artistlist_build_drp, 0,4,1,1)

        self.artistlist_collection_drp = QComboBox()
        self.artistlist_collection_drp.setStyleSheet("color: #b1b1b1; background-color: rgba(175,70,70,50);")
        preset = self.find_playlists(_play_list_path)
        preset = [(each.split("/")[-1]) for each in preset]
        artist_reviews_listnames = [(each.split("_storedText.txt")[0]) for each in preset]
        QtCore.QObject.connect(self.artistlist_collection_drp, SIGNAL("currentIndexChanged(QString)"),self.load_artist_review)
        self.artistlist_collection_drp.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self.artistlist_collection_drp, SIGNAL("customContextMenuRequested(QPoint)"), self.artist_rev_list_drp_r_click)
        self.artistlist_collection_drp.addItems(dsktop_rev_list)
        self.artistlist_collection_drp.addItems(artist_reviews_listnames)
        self.top_lower_layer.addWidget(self.artistlist_collection_drp, 0,5,1,1)
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setToolTip("refresh")
        self.connect(self.refresh_btn, SIGNAL('clicked()'), self.refresh_window)    
        self.top_lower_layer.addWidget(self.refresh_btn, 0,6,0,1)

        ##CUSTOM PATH
        self.cust_path_label = QLabel("Custom path: ")
        self.cust_path_label.setStyleSheet('background-color:transparent')
        self.cust_path_label.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
        self.customLayout.addWidget(self.cust_path_label, 0,0,1,1)

        self.cust_path_field = QLineEdit()
        self.cust_path_field.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        self.cust_path_field.setVisible(1)
        self.cust_path_field.setText("//")
        self.cust_path_field.setFixedWidth(600)
        self.customLayout.addWidget(self.cust_path_field, 0,1,1,1)

        self.file_type_drp = QComboBox()
        self.file_type_drp.addItems(by_detail)
        self.file_type_drp.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.list_layout.addWidget(self.file_type_drp)
        self.customLayout.addWidget(self.list_frame, 0,2,1,1)

        self.default_proj_btn = QPushButton("Set to _project default")
        self.default_proj_btn.setToolTip("set list to load from custom path")
        self.connect(self.default_proj_btn, SIGNAL('clicked()'), self.set_to_project)
        self.customLayout.addWidget(self.default_proj_btn, 2,0,1,1)

        self.user_folder_btn = QPushButton("Load from user folder")
        self.user_folder_btn.setToolTip("set list to load from custom path")
        self.connect(self.user_folder_btn, SIGNAL('clicked()'), self.set_to_user)
        self.customLayout.addWidget(self.user_folder_btn, 2,1,1,1)

        self.set_btn = QPushButton("Set")
        self.set_btn.setToolTip("set list to load from custom path")
        self.connect(self.set_btn, SIGNAL('clicked()'), self.set_toCustom)
        self.customLayout.addWidget(self.set_btn, 2,2,1,1)

        ##PLAYBLAST LIST
        self.playBlastList = QTableWidget(1, 4)
        self.playBlastList.setHorizontalHeaderLabels(headers)
        self.playBlastList.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)     
        col1, col2, col3, col4 =  240, 160, 500, 50
        self.playBlastList.setColumnWidth(0, col1)
        self.playBlastList.setColumnWidth(1, col2)
        self.playBlastList.setColumnWidth(2, col3)
        self.playBlastList.setColumnWidth(3, col4)
        self.playBlastList.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.playBlastList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.playBlastList.customContextMenuRequested.connect(self.playblast_list_r_click)
        self.playBlastList.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.connect(self.playBlastList, SIGNAL("itemClicked(QTableWidgetItem *)"), self.count_frames_selected_playblast)
        self.connect(self.playBlastList, SIGNAL("itemDoubleClicked(QTableWidgetItem *)"), self.playblast_list_d_click)
        self.playblast_list_layer.addWidget(self.playBlastList, 0,0,1,1)

        ##FRAMED

        self.comment_LbL = QLabel("Comment: ")
        self.comment_LbL.setStyleSheet('background-color:transparent')
        self.comment_LbL.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
        self.msgBox.addWidget(self.comment_LbL, 0,0,1,1)

        self.comment_field = QLineEdit()
        self.comment_field.setStyleSheet("color: #b1b1b1; background-color: rgba(255,255,255,25);")
        self.comment_field.setVisible(1)
        self.comment_field.setText(defaultText)
        self.comment_field.setFixedWidth(600)
        self.msgBox.addWidget(self.comment_field, 0,1,1,1)
        
        self.range_group=QtGui.QButtonGroup(self.radiobox)

        self.comment_LbL = QLabel("Submit at range:")
        self.comment_LbL.setStyleSheet('background-color:transparent')
        self.comment_LbL.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
        self.msgBox.addWidget(self.comment_LbL, 1,0,1,1)

        self.submit_work_checkbox=QRadioButton("Work: " + str(int(wk_strt_value-1)) + '-' + str(int(wk_out_value+1)))
        self.submit_work_checkbox.clicked.connect(self.frame_set)
        self.submit_work_checkbox.setToolTip("Take this range into consideration for submitting to shotgun")
        self.submit_work_checkbox.setChecked(1)
        self.submit_work_checkbox.setStyleSheet("color: #ffff12;")
        self.range_group.addButton(self.submit_work_checkbox)
        self.radiobox.addWidget(self.submit_work_checkbox, 2,0,1,1)

        self.submit_cut_checkbox=QRadioButton("Cut: " + str(cut_in_value) + '-' + str(cut_out_value))
        self.submit_cut_checkbox.clicked.connect(self.frame_set)
        self.submit_cut_checkbox.setToolTip("Take this range into consideration for submitting to shotgun")
        self.submit_cut_checkbox.setChecked(0)
        self.range_group.addButton(self.submit_cut_checkbox)
        self.radiobox.addWidget(self.submit_cut_checkbox, 2, 1, 1,1)

        self.submit_range_checkbox=QRadioButton("Custom:")
        self.submit_range_checkbox.setToolTip("Take this range into consideration for submitting to shotgun")
        self.submit_range_checkbox.clicked.connect(self.frame_set)
        self.submit_range_checkbox.setChecked(0)
        self.range_group.addButton(self.submit_range_checkbox)
        self.radiobox.addWidget(self.submit_range_checkbox, 2,2,1,1)

        self.head_lbl = QLabel("start")
        self.head_lbl.setStyleSheet("color: #787878; background-color: rgba(255,255,255,0);")
        self.radiobox.addWidget(self.head_lbl, 2,3,1,1)
        
        self.head_field = QLineEdit("")
        self.head_field.setStyleSheet("color: #767676; background-color: rgba(255,255,255,25);")
        self.head_field.setFixedHeight(25)
        self.head_field.setFixedWidth(100)
        self.radiobox.addWidget(self.head_field, 2,4,1,1)
        
        self.toe_lbl = QLabel("end")
        self.toe_lbl.setStyleSheet("color: #787878; background-color: rgba(255,255,255,0);")
        self.radiobox.addWidget(self.toe_lbl, 2,5,1,1)
        
        self.toe_field = QLineEdit("")
        self.toe_field.setFixedHeight(25)
        self.toe_field.setFixedWidth(100)
        self.toe_field.setStyleSheet("color: #767676; background-color: rgba(255,255,255,25);")
        self.radiobox.addWidget(self.toe_field, 2,6,1,1)

        ##BOTTOM UPPER
        self.play_in_rv_button = QPushButton("play in RV")
        self.connect(self.play_in_rv_button, SIGNAL('clicked()'), self.play_in_rv)
        self.frame_btn_layout.addWidget(self.play_in_rv_button, 0,0,0,1)
        
        self.rv_wipe_btn = QPushButton("compare")
        self.connect(self.rv_wipe_btn, SIGNAL('clicked()'), self.compare_in_rv)
        self.frame_btn_layout.addWidget(self.rv_wipe_btn, 0,1, 0,1)

        self.delete_preroll_btn = QPushButton("Clean roll frames")
        self.delete_preroll_btn.setToolTip("remove roll frames from folder for playblast review - removes preroll frames and postroll for better review(with 1 frame buffer for frame blur)")
        self.connect(self.delete_preroll_btn, SIGNAL('clicked()'), self.clean_playblasts_jpgs)
        self.frame_btn_layout.addWidget(self.delete_preroll_btn, 0,2, 0,1)

        self.mSubmit_btn = QPushButton("Submit To Shotgun")
        self.connect(self.mSubmit_btn, SIGNAL('clicked()'), lambda *args:self.pub_to_shotgun(shot_len_value, cut_in_value, cut_out_value, wk_strt_value, wk_out_value, cut_shouldbe_in_value, cut_shouldbe_out_value))
        self.frame_btn_layout.addWidget(self.mSubmit_btn, 0,4, 1,1)

        self.mSubmit_clr_btn = QPushButton("Clean submit to Shotgun")
        self.connect(self.mSubmit_clr_btn, SIGNAL('clicked()'), lambda *args:self.cln_pub_to_shotgun(shot_len_value, cut_in_value, cut_out_value, wk_strt_value, wk_out_value, cut_shouldbe_in_value, cut_shouldbe_out_value))
        self.frame_btn_layout.addWidget(self.mSubmit_clr_btn, 0,3, 1,1)

        ##BOTTOM LOWER

        open_folder=False
        render_an_call = False
        render_pub_call = True

        self.play_anim_btn = QPushButton()
        self.play_anim_btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        from_an_dept = "anim"
        self.play_anim_btn.customContextMenuRequested.connect(lambda *args:self.anim_daily_drp_r_click(from_an_dept, render_an_call))
        self.connect(self.play_anim_btn, SIGNAL('clicked()'), lambda *args:self.play_latest_anim(from_an_dept, render_an_call, open_folder))
        self.btm_upper_layer.addWidget(self.play_anim_btn,1,3,1,1)

        self.play_anim_pub_btn = QPushButton()   
        self.play_anim_pub_btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.play_anim_pub_btn.customContextMenuRequested.connect(lambda *args:self.anim_daily_drp_r_click(from_an_dept, render_pub_call))
        self.connect(self.play_anim_pub_btn, SIGNAL('clicked()'), lambda *args:self.play_latest_anim(from_an_dept, render_pub_call, open_folder))
        self.btm_upper_layer.addWidget(self.play_anim_pub_btn,2,3,1,1)
        
        self.play_light_btn = QPushButton()     
        self.play_light_btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        from_lit_dept = "lightcomp"
        self.play_light_btn.customContextMenuRequested.connect(lambda *args:self.anim_daily_drp_r_click(from_lit_dept, render_an_call))
        self.connect(self.play_light_btn, SIGNAL('clicked()'), lambda *args:self.play_latest_anim(from_lit_dept, render_an_call, open_folder))
        self.btm_upper_layer.addWidget(self.play_light_btn,1,6,1,1)
        
        self.play_comp_btn = QPushButton()          
        self.play_comp_btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        from_comp_dept = "comp"
        self.play_comp_btn.customContextMenuRequested.connect(lambda *args:self.anim_daily_drp_r_click(from_comp_dept, render_an_call))
        self.connect(self.play_comp_btn, SIGNAL('clicked()'), lambda *args:self.play_latest_anim(from_comp_dept, render_an_call, open_folder))
        self.btm_upper_layer.addWidget(self.play_comp_btn,1,7,1,1)
        
        self.play_track_btn = QPushButton()         
        self.play_track_btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        from_track_dept = "trackcomp"
        self.play_track_btn.customContextMenuRequested.connect(lambda *args:self.anim_daily_drp_r_click(from_track_dept, render_an_call))
        self.connect(self.play_track_btn, SIGNAL('clicked()'), lambda *args:self.play_latest_anim(from_track_dept, render_an_call, open_folder))
        self.btm_upper_layer.addWidget(self.play_track_btn,1,0,1,1)
        
        self.play_fx_btn = QPushButton()         
        self.play_fx_btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        from_fx_dept = "fxflip"
        self.play_fx_btn.customContextMenuRequested.connect(lambda *args:self.anim_daily_drp_r_click(from_fx_dept, render_an_call))
        self.connect(self.play_fx_btn, SIGNAL('clicked()'), lambda *args:self.play_latest_anim(from_mm_dept, render_an_call, open_folder))
        self.btm_upper_layer.addWidget(self.play_fx_btn,1,5,1,1)

        self.play_mm_btn = QPushButton()
        self.play_mm_btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        from_mm_dept = "matchmove"
        self.play_mm_btn.customContextMenuRequested.connect(lambda *args:self.anim_daily_drp_r_click(from_mm_dept, render_an_call))
        self.connect(self.play_mm_btn, SIGNAL('clicked()'),  lambda *args:self.play_latest_anim(from_mm_dept, render_an_call, open_folder))
        self.btm_upper_layer.addWidget(self.play_mm_btn,1,1,1,1)

        self.play_mm_pub_btn = QPushButton()
        self.play_mm_pub_btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.play_mm_pub_btn.customContextMenuRequested.connect(lambda *args:self.anim_daily_drp_r_click(from_mm_dept, render_pub_call))
        self.connect(self.play_mm_pub_btn, SIGNAL('clicked()'),  lambda *args:self.play_latest_anim(from_mm_dept, render_pub_call, open_folder))
        self.btm_upper_layer.addWidget(self.play_mm_pub_btn,2,1,1,1)

        self.play_roto_btn = QPushButton()
        self.play_roto_btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        from_roto_dept = "roto"
        self.play_roto_btn.customContextMenuRequested.connect(lambda *args:self.anim_daily_drp_r_click(from_roto_dept, render_an_call))
        self.connect(self.play_roto_btn, SIGNAL('clicked()'), lambda *args:self.play_latest_anim(from_roto_dept, render_pub_call, open_folder))
        self.btm_upper_layer.addWidget(self.play_roto_btn,1,2,1,1)
        
        self.play_ta_btn = QPushButton()           
        self.play_ta_btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        from_ta_dept="techanim"
        self.play_ta_btn.customContextMenuRequested.connect(lambda *args:self.anim_daily_drp_r_click(from_ta_dept, render_an_call))
        self.connect(self.play_ta_btn, SIGNAL('clicked()'), lambda *args:self.play_latest_anim(from_ta_dept, render_an_call, open_folder))
        self.btm_upper_layer.addWidget(self.play_ta_btn,1,4,1,1)

        self.play_ta_pub_btn = QPushButton()               
        self.play_ta_pub_btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.play_ta_pub_btn.customContextMenuRequested.connect(lambda *args:self.anim_daily_drp_r_click(from_ta_dept, render_pub_call))
        self.connect(self.play_ta_pub_btn, SIGNAL('clicked()'), lambda *args:self.play_latest_anim(from_ta_dept, render_pub_call, open_folder))
        self.btm_upper_layer.addWidget(self.play_ta_pub_btn,2,4,1,1)

        self.update_review_latest_buttons(versioning_dictionary)

        QtCore.QObject.connect(self.scene_drp, SIGNAL("currentIndexChanged(QString)"),
                                self.on_scene_drp_changed)
        
        QtCore.QObject.connect(self.shot_drp, SIGNAL("currentIndexChanged(QString)"),
                                self.on_shot_drp_changed)

        QtCore.QObject.connect(self.dept_drp, SIGNAL("currentIndexChanged(QString)"),
                                self.on_dept_drp_changed)

        print "launching window"
        self.start_window(cut_in_value, cut_out_value)

    ##COMMON DEFAULT DIALOGS AND WARNINGS

    def frame_set(self):
        if self.submit_range_checkbox.isChecked() == True:
            self.submit_range_checkbox.setStyleSheet("color: #ffff12;")
            self.head_lbl.setStyleSheet("color: #aaaa12;")
            self.toe_lbl.setStyleSheet("color: #aaaa12;")
            self.submit_work_checkbox.setStyleSheet("color: #b1b1b1;")
            self.submit_cut_checkbox.setStyleSheet("color: #b1b1b1;")
            self.head_field.setStyleSheet("color: #ffff12; background-color: rgba(255,255,255,25);")
            self.toe_field.setStyleSheet("color: #ffff12; background-color: rgba(255,255,255,25);")
            if self.count_frames_checkbox.isChecked() == True:
                self.head_field.setStyleSheet("color: #aaccff; background-color: rgba(255,255,255,25);")
                self.toe_field.setStyleSheet("color: #aaccff; background-color: rgba(255,255,255,25);")                
        elif self.submit_work_checkbox.isChecked() == True:
            self.submit_range_checkbox.setStyleSheet("color: #b1b1b1;")
            self.head_lbl.setStyleSheet("color: #787878;")
            self.toe_lbl.setStyleSheet("color: #787878;")            
            self.submit_work_checkbox.setStyleSheet("color: #ffff12;")
            self.submit_cut_checkbox.setStyleSheet("color: #b1b1b1;")
            self.head_field.setStyleSheet("color: #767676; background-color: rgba(255,255,255,25);")
            self.toe_field.setStyleSheet("color: #767676; background-color: rgba(255,255,255,25);")
            if self.count_frames_checkbox.isChecked() == True:
                self.head_field.setStyleSheet("color: #557799; background-color: rgba(255,255,255,25);")
                self.toe_field.setStyleSheet("color: #557799; background-color: rgba(255,255,255,25);")             
        elif self.submit_cut_checkbox.isChecked() == True:
            self.submit_range_checkbox.setStyleSheet("color: #b1b1b1;")
            self.head_lbl.setStyleSheet("color: #787878;")
            self.toe_lbl.setStyleSheet("color: #787878;")             
            self.submit_work_checkbox.setStyleSheet("color: #b1b1b1;")
            self.submit_cut_checkbox.setStyleSheet("color: #ffff12;")
            self.head_field.setStyleSheet("color: #767676; background-color: rgba(255,255,255,25);")
            self.toe_field.setStyleSheet("color: #767676; background-color: rgba(255,255,255,25);") 
            if self.count_frames_checkbox.isChecked() == True:
                self.head_field.setStyleSheet("color: #557799; background-color: rgba(255,255,255,25);")
                self.toe_field.setStyleSheet("color: #557799; background-color: rgba(255,255,255,25);") 

    def _select_warning(self):
        sel_warning_text =  "Must select something in list"
        return sel_warning_text

    def _select_toofew_warning(self):
        sel_warning_text =  "Must select more than one object in list"
        return sel_warning_text

    def _submit_warning(self):
        sub_warning_text = "This version has already been submitted to shotgun. Unable to submit again."
        return sub_warning_text

    def _comment_warning(self):
        com_warning_text =  "Please provide a meaningful comment for submit"
        return com_warning_text

    def message_box_callup(self, note):
        '''Default warning dialog'''
        QtGui.QMessageBox.question(None, 'Message' , note)
        
    def make_body(self, prompt):
        '''Default grab text dialog'''
        text, ok = QtGui.QInputDialog.getText(None, 'Intput Dialog', prompt)
        if ok:
            _project = (str(text))
        else:
            return
        return _project

    ##BUTTON LCLICK FUNCTIONS
    
    def launch_shotgun(self):
        '''open firefox to shotgun'''
        url = "http://sg.methodstudios.com"
        subprocess.Popen('firefox "%s"' % url, stdout = subprocess.PIPE, shell = True)

    def launch_help(self):
        '''open help page'''
        url = "https://atlas.bydeluxe.com/confluence/display/~deglaue/mSubmit+Manager"
        subprocess.Popen('firefox "%s"' % url, stdout = subprocess.PIPE, shell = True) 

    def launch_folder(self, path):
        '''This launches dolphin to the custom path'''
        command = "dolphin '%s'"%path
        subprocess.Popen(command, stdout = subprocess.PIPE, shell = True)

    def refresh_window(self):
        '''This refreshes list with current interface layout(eg: changing to view anim and hitting 'refresh' will repopulate face with anim)'''
        listed_dept, listed_scene, listed_shot=self.identify_shot()
        temp_play_list_path = '/jobs/' + _project + '/' + listed_scene + '/' + listed_shot + '/TASKS/' + listed_dept + "/maya/"
        shot_len_value, cut_in_value, cut_out_value, wk_strt_value, wk_out_value, cut_shouldbe_in_value, cut_shouldbe_out_value\
        ,versioning_dictionary = self.set_defaults(listed_scene, listed_shot)
        self.update_review_latest_buttons(versioning_dictionary)
        try:
            winTitle = win_title + '              ' + _project + " : " + listed_shot + " : (F" + str(shot_len_value) + ")   :   ( " + str(wk_strt_value-1) + "  |[ " + str(wk_strt_value) + " <<<[" + str(cut_in_value) + "-" + str(cut_out_value) + "]>>> " + str(wk_out_value) + " ]|  " + str(wk_out_value + 1) + " )"
        except IndexError:
            winTitle = win_title + '              ' + _project + " : " + listed_shot
        self.setWindowTitle(winTitle)
        self.playblast_list_create(listed_dept, listed_scene, listed_shot)
        self.count_frame_function()

    def refresh_artist_reviews(self, play_path):
        '''The combined function to refresh the playlist'''
        play_path=str(play_path)
        preset = self.find_playlists(play_path)
        preset = [(each.split("/")[-1]) for each in preset]
        artist_reviews_listnames = [(each.split("_storedText.txt")[0]) for each in preset]
        self.artistlist_collection_drp.clear()
        self.artistlist_collection_drp.addItems(dsktop_rev_list)
        self.artistlist_collection_drp.addItems(artist_reviews_listnames)     

    def reset_window(self, cut_in_value, cut_out_value):
        '''This resets the window to default settings as is set in the shell env: resets shot and dept back to default'''
        deptindex = self.dept_drp.findText(_dept_task, QtCore.Qt.MatchFixedString)
        self.dept_drp.setCurrentIndex(deptindex)
        self.start_window(cut_in_value, cut_out_value)
        shot_len_value, cut_in_value, cut_out_value, wk_strt_value, wk_out_value, cut_shouldbe_in_value, cut_shouldbe_out_value\
        ,versioning_dictionary = self.set_defaults(_scene, _shot)
        self.update_review_latest_buttons(versioning_dictionary)
        try:
            winTitle = win_title + '              ' + _project + " : " + _shot + " : (F" + str(shot_len_value) + ")   :   ( " + str(wk_strt_value-1) + "  |[ " + str(wk_strt_value) + " <<<[" + str(cut_in_value) + "-" + str(cut_out_value) + "]>>> " + str(wk_out_value) + " ]|  " + str(wk_out_value + 1) + " )"
        except IndexError:
            winTitle = win_title + '              ' + _project + " : " + _shot
        self.setWindowTitle(winTitle)
        self.playblast_list_create(_dept_task, _scene, _shot)
        self.refresh_artist_reviews(_play_list_path)


    def play_in_rv(self):
        '''This will launch rv and play on what is selected in list'''
        selected_in_list = self.is_listWid_item_selected()
        if len(selected_in_list)<1:
            print self._select_warning()
            return
        else:
            pass
        command = "rv " + str(selected_in_list[0]) + "/*"
        print "you are running command: " + command
        subprocess.Popen(command, stdout = subprocess.PIPE, shell = True)  

    def clean_playblasts_jpgs(self):
        '''This is the function that removes preroll jpgs from image folder on selected playblast'''
        shot_len_value, cut_in_value, cut_out_value, wk_strt_value, wk_out_value, cut_shouldbe_in_value, cut_shouldbe_out_value\
        ,versioning_dictionary = self.set_defaults(_scene, _shot)
        selected_in_list = self.is_listWid_item_selected()
        get_file_name = selected_in_list[0].split('/')[-1]      
        get_preset = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(selected_in_list[0]) for name in files if name.lower().endswith(".jpg")]
        for item in get_preset:
            get_num_part = item.split(".")[-2]     
            if get_num_part.isdigit():
                try:
                    get_num_part = int(get_num_part)
                    get_strt_val = int(wk_strt_value)-1
                    if get_num_part < get_strt_val:
                        # getit = item.split("/")[-1]
                        print "removing " + item
                        os.remove(item)
                except IndexError:
                    pass
                try:
                    get_end_val = int(wk_out_value) + 1
                    if int(get_num_part) > get_end_val:
                        print "removing " + item
                        os.remove(item)                 
                except IndexError:
                    print "no frames to remove"
                    pass
            else:
                print "skipping " + item

    def compare_in_rv(self):
        '''This is the compare (rv -wipe) function that runs when user selects more than one playblast and uses compare.'''
        selected_in_list = self.is_listWid_item_selected()
        if len(selected_in_list)<2:
            print self._select_toofew_warning()
            return
        else:
            command = "rv -wipe " + str(selected_in_list[0]) + "/* " + str(selected_in_list[1]) + "/*"
            print "you are running command: " + command
            subprocess.Popen(command, stdout = subprocess.PIPE, shell = True)

    def cln_pub_to_shotgun(self, shot_len_value, cut_in_value, cut_out_value, wk_strt_value, wk_out_value, cut_shouldbe_in_value, cut_shouldbe_out_value):
        '''This combines the cleaning frame function with the msubmit function to submit a workrange playblast'''
        self.clean_playblasts_jpgs()
        self.pub_to_shotgun(shot_len_value, cut_in_value, cut_out_value, wk_strt_value, wk_out_value, cut_shouldbe_in_value, cut_shouldbe_out_value)

    def pub_to_shotgun(self, shot_len_value, cut_in_value, cut_out_value, wk_strt_value, wk_out_value, cut_shouldbe_in_value, cut_shouldbe_out_value):
        '''This builds the mSubmit command based on .jpg and executes it'''
        selected_in_list = self.is_listWid_item_selected()
        if len(selected_in_list)>0:
            pass
        else:
            print self._select_warning()
            self.message_box_callup(self._select_warning())
            return
        check_for_mov = [(each_file) for each_file in os.listdir(selected_in_list[0]) if "_mov" in each_file]
        if len(check_for_mov)>0:
            print self._submit_warning()
            self.message_box_callup(self._submit_warning())
            return
        else:
            pass
        get_comment_box = self.comment_field
        get_comment_from_box = get_comment_box.text()
        get_comment_from_box = str(get_comment_from_box)
        get_review_type = self.reviewtype_drp
        get_the_review_type = get_review_type.currentText()
        get_the_review_type = str(get_the_review_type)
        for each_comment in _failed_comments:
            if get_comment_from_box  ==  each_comment:
                get_comment_from_box = self.make_body(self._comment_warning())
                print self._comment_warning()
            else:
                pass
        get_selected_path = selected_in_list[0] + '/'
        get_items = os.listdir(get_selected_path)
        get_folder_for_jpgs = [(each_file) for each_file in get_items if "jpg" in each_file]
        get_play_folder = selected_in_list[0] + '/' + get_folder_for_jpgs[0] + '/'
        get_list = os.listdir(get_play_folder)
        get_list = [(each_file) for each_file in get_list if not each_file.startswith('.')]
        get_image_name = get_list[0].split('.')[0]
        get_plate = get_play_folder + get_image_name + '.%04d' + _format_ext
        get_frame_length_exists = [os.path.join(get_play_folder, o) for o in os.listdir(get_play_folder)]
        get_frame_length_exists.sort(key = lambda x: os.path.getmtime(x)) 
        get_true_last = int(get_frame_length_exists[-3].split('.')[-2:-1][0])
        if self.submit_range_checkbox.isChecked() == True:
            first_frame = self.head_field
            get_first_frame = first_frame.toPlainText()
            get_first_frame = get_first_frame.split('.')[0]
            get_first_frame = str(get_first_frame)
            get_last = self.toe_field  
            get_last_frame = get_last.toPlainText()  
            get_last_frame = get_last_frame.split('.')[0]
            get_last_frame = str(get_last_frame)
            if get_true_last<int(get_last_frame):
                get_last_frame = get_true_last
            else:
                get_last_frame = get_last_frame
        elif self.submit_cut_checkbox.isChecked() == True:
            get_first_frame = str(cut_in_value)
            get_last_frame = str(cut_out_value)
        elif self.submit_work_checkbox.isChecked() == True:
            get_first_frame = str(int(wk_strt_value)-1)
            get_last_frame = str(int(wk_out_value)+1)
        command = 'msubmitCmd -p ' + get_plate + ' -s ' + str(get_first_frame) + ' -e ' + str(get_last_frame) + ' -n "' + get_comment_from_box + '" -t ' + get_the_review_type + ' --task ' + _dept_task
        print "you are running command: " + command
        subprocess.Popen(command, stdout = subprocess.PIPE, shell = True)
        print "submitted"

    def identify_shot(self):
        listed_dept = self.dept_drp
        listed_dept = listed_dept.currentText()   
        listed_scene = self.scene_drp
        listed_scene = listed_scene.currentText() 
        listed_shot = self.shot_drp
        listed_shot = listed_shot.currentText()
        return listed_dept, listed_scene, listed_shot

    def _open_work_folder(self):
        '''This launches dolphin to the workfolder for the department listed in the dept dropdown'''
        listed_dept, listed_scene, listed_shot=self.identify_shot()
        path = '/jobs/' + _project + '/' + listed_scene + "/" + listed_shot + '/TASKS/' + listed_dept + "/maya/scenes/"
        self.launch_folder(path)

    def set_to_project(self):
        '''This is for the custom paths - this repopulates the list to _project default'''
        type_list = self.file_type_drp
        list_type = type_list.currentText()       
        get_the_path_slot = self.cust_path_field
        get_the_path_slot.setText(_project_path_pbMovs)
        self.cust_playblast_list_create(_project_path_pbMovs, list_type)

    def set_to_user(self):
        '''This is for the custom paths - this repopulates the list to user directory'''
        type_list = self.file_type_drp
        list_type = type_list.currentText()   
        get_the_path_slot = self.cust_path_field
        get_the_path_slot.setText(_user_path_pbmovs)
        self.cust_playblast_list_create(_user_path_pbmovs, list_type)

    def set_toCustom(self):
        '''This is for the custom paths - this repopulates the list to custom path'''
        type_list = self.file_type_drp
        list_type = type_list.currentText()           
        get_the_path_slot = self.cust_path_field
        user_path = get_the_path_slot.text()
        self.cust_playblast_list_create(user_path,list_type)

    def play_latest_anim(self, from_dept, pub_render_call, open_folder):
        '''This plays the latest msubmitted animation images'''
        listed_dept, listed_scene, listed_shot=self.identify_shot()
        shot_len_value, cut_in_value, cut_out_value, wk_strt_value, wk_out_value, cut_shouldbe_in_value, cut_shouldbe_out_value\
        ,versioning_dictionary = self.set_defaults(listed_scene, listed_shot)
        if from_dept == "anim" and pub_render_call == False:
            set_versioning = versioning_dictionary.get('get_an_ver')
        elif from_dept == "anim" and pub_render_call == True:
            set_versioning = versioning_dictionary.get('get_an_pub_ver')
        elif from_dept == "lightcomp":
            set_versioning = versioning_dictionary.get("get_light_ver")
        elif from_dept == "comp":
            set_versioning = versioning_dictionary.get("get_comp_ver")
        elif from_dept == "fxflip":
            set_versioning = versioning_dictionary.get("get_fx_ver")
        elif from_dept == "techanim" and pub_render_call == False:
            set_versioning = versioning_dictionary.get("get_ta_ver")
        elif from_dept == "techanim" and pub_render_call == True:
            set_versioning = versioning_dictionary.get("get_ta_pub_ver")
        elif from_dept == "matchmove" and pub_render_call == False:
            set_versioning = versioning_dictionary.get("get_mm_ver")
        elif from_dept == "matchmove" and pub_render_call == True:
            set_versioning = versioning_dictionary.get("get_mm_pub_ver")
        elif from_dept == "trackcomp":
            set_versioning = versioning_dictionary.get("get_track_ver")
        elif from_dept == "roto":
            set_versioning = versioning_dictionary.get("get_roto_ver")
        if open_folder == True:
            self.launch_folder(set_versioning)
        else:
            self.direct_play_rv(set_versioning)

    ##RIGHT CLICKS

    def anim_daily_drp_r_click(self, from_dept, pub_render_call):
        open_folder=True
        self.play_latest_anim(from_dept, pub_render_call, open_folder)

    def artist_rev_list_drp_r_click(self):
        '''This opens dolphin to the artist review path'''
        listed_dept, listed_scene, listed_shot=self.identify_shot()
        play_list_path = '/jobs/' + _project + '/' + listed_scene + '/' + listed_shot + '/TASKS/' + listed_dept + "/maya/"
        self.launch_folder(play_list_path)

    def playblast_list_r_click(self):
        '''This launches dolphin to the current selected in list'''
        selected_in_list = self.is_listWid_item_selected()
        path = str(selected_in_list[0]) + "/"
        self.launch_folder(path)
  
    def scene_drp_r_click(self):
        '''this launches dolphin to the listed _scene folder'''
        listed_dept, listed_scene, listed_shot=self.identify_shot()  
        path = '/jobs/' + _project + '/' + listed_scene + "/"
        self.launch_folder(path)

    def shot_drp_r_click(self):
        '''This launches dolphin to the listed shot folder'''
        listed_dept, listed_scene, listed_shot=self.identify_shot()     
        path = '/jobs/' + _project + '/' + listed_scene + "/" + listed_shot
        self.launch_folder(path)

    def dept_drp_r_click(self):
        '''This launches dolphin to the listed department images folder'''
        listed_dept, listed_scene, listed_shot=self.identify_shot()          
        path = '/jobs/' + _project + '/' + listed_scene + "/" + listed_shot + '/PRODUCTS/images/' + listed_dept
        self.launch_folder(path)       

    ##DOUBLE CLICKS

    def playblast_list_d_click(self):
        '''This is the function when the user double clicks the playlist item'''
        selected_in_list = self.is_listWid_item_selected()
        self.replayblast_list_create(selected_in_list[0])

    ##SELECT

    def count_frames_selected_playblast(self):
        '''This fetches the frames of the images to populate the start end field for revealing the frame range available of a given selected playblast'''
        if self.count_frames_checkbox.isChecked() == True:
            self.count_frame_function()
        else:
            return

    def count_frame_function(self):
        selected_in_list = self.is_listWid_item_selected()
        if len(selected_in_list)>0:
            get_items_jpg = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(selected_in_list[0]) for name in files if name.lower().endswith(".jpg")]
            get_items_exr = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(selected_in_list[0]) for name in files if name.lower().endswith(".exr")]
            if len(get_items_exr)>0:
                get_items = get_items_exr
            elif len(get_items_jpg)>0:
                get_items = get_items_jpg
            else:
                get_items = False
            if get_items != False:
                get_frame_length_exists=[ (each) for each in get_items if each.split('.')[-2:-1][0].isdigit() == True]
                get_frame_length_exists.sort(key = lambda x: os.path.getmtime(x)) 
                try:
                    get_true_first = int(get_frame_length_exists[0].split('.')[-2:-1][0])
                    get_true_last = int(get_frame_length_exists[-1].split('.')[-2:-1][0])
                    self.head_field.setText(str(float(get_true_first)))
                    self.toe_field.setText(str(float(get_true_last)))
                except IndexError:
                    self.zero_field()
            else:
                self.zero_field()                    
        else:
            self.zero_field()

    def zero_field(self):
        self.head_field.setText("0")
        self.toe_field.setText("0") 

    ##DROP DOWNS

    def on_scene_drp_changed(self):
        '''This repopulates the shot drop down with the corresponding shots to _scene when the _scene dropdown is changed'''
        self.get_scene()
        if self.count_frames_checkbox.isChecked() == True:
            self.refresh_window()
        else:
            return

    def on_shot_drp_changed(self):
        '''This repopulates the list when the shotdrop down changes'''
        if self.count_frames_checkbox.isChecked() == True:
            self.refresh_window()
        else:
            return

    def on_dept_drp_changed(self):
        if self.count_frames_checkbox.isChecked() == True:
            self.refresh_window()
        else:
            return

    def build_artist_review(self):
        '''This is the build artist review function'''
        selected_in_list = self.is_listWid_item_selected()
        list_build = self.artistlist_build_drp
        list_build_function = list_build.currentText()
        if list_build_function == dsktop_rev_build[0]:
            return
        elif list_build_function == dsktop_rev_build[1]:
            if len(selected_in_list)<1:
                print "need to select something"
                return
            else:
                pass            
            getitems = [(each.split("/")[-1]) for each in selected_in_list]
            name_to_save = ' '.join(getitems)
            prompt = "name of list:"
            getget_comment_from_box = self.make_body(prompt)
            if getget_comment_from_box == None:
                print "needs name"
                return
            else:
                pass
            getget_comment_from_box = getget_comment_from_box.replace(' ', '_')
            shotList = getget_comment_from_box + "_storedText.txt"
            file_path_build = _play_list_path + shotList
            copyfilemessage = "creating " + file_path_build
            reply = QtGui.QMessageBox.question(None, 'Message' ,copyfilemessage, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply  ==  QtGui.QMessageBox.Yes:
                if os.path.isfile(file_path_build) == True:
                    c_message = "create over " + file_path_build
                    replay = QtGui.QMessageBox.question(None, 'Message' ,c_message, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                    if reply  ==  QtGui.QMessageBox.Yes:
                        inp = open(file_path_build, "w + ")
                        print selected_in_list
                        inp.write(str(selected_in_list))
                        inp.close()
                        print "created " + file_path_build
                    else:
                        print "cancelled"
                        return
                else:
                    inp = open(file_path_build, "w + ")
                    print selected_in_list
                    inp.write(str(selected_in_list))
                    inp.close()
                    print "created " + file_path_build
            else:
                print "cancelled"
                return
            self.refresh_artist_reviews(_play_list_path)         
        elif list_build_function == dsktop_rev_build[2]:
            if len(selected_in_list)<1:
                print "need to select something"
                return
            else:
                pass                
            get_preset = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(_play_list_path) for name in files if "_storedText.txt" in name]
            if len(get_preset)<1:
                print "there are no lists available to append to"
                return
            else:
                pass
            make_content = self.obtain_presets([get_preset[0]]) 
            print make_content
            make_new_content = list(set(make_content + selected_in_list))
            print make_new_content
            title = "new"
            inst_win = DropMenu(get_preset, title, make_new_content)
            inst_win.show()
        elif list_build_function == dsktop_rev_build[3]:
            not_selected_in_list = self.is_listWid_item_not_selected()
            if len(not_selected_in_list)<1:
                print "Not enough items to exclude from list"
                return
            else:
                pass           
            playlist_load = self.artistlist_collection_drp
            playlist_name = playlist_load.currentText()                    
            getitems = [(each.split("/")[-1]) for each in not_selected_in_list]
            name_to_save = ' '.join(getitems)
            shotList = playlist_name + "_storedText.txt"
            file_path_build = _play_list_path + shotList
            copyfilemessage = "updating " + file_path_build
            reply = QtGui.QMessageBox.question(None, 'Message' ,copyfilemessage, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply  ==  QtGui.QMessageBox.Yes:
                if os.path.isfile(file_path_build) == True:
                    if reply  ==  QtGui.QMessageBox.Yes:
                        inp = open(file_path_build, "w + ")
                        print not_selected_in_list
                        inp.write(str(not_selected_in_list))
                        inp.close()
                        print "created " + file_path_build
                else:
                    print "cancelled"
                    return
            else:
                print "cancelled"
                return
            playlist_load = self.artistlist_collection_drp
            playlist_name = playlist_load.currentText()     
            self.load_artist_review()
        reset_dropdown = self.artistlist_build_drp.findText(dsktop_rev_build[0], QtCore.Qt.MatchFixedString)
        self.artistlist_build_drp.setCurrentIndex(reset_dropdown)

    def load_artist_review(self):
        '''This populates the playblast list with the contents for selected artist review list from dropdown'''
        playlist_load = self.artistlist_collection_drp
        playlist_name = playlist_load.currentText()
        if playlist_name == dsktop_rev_list[0]:
            pass
        else:
            get_preset = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(_play_list_path) for name in files if playlist_name + "_storedText.txt" == name]
            file_dict = []
            make_content = self.obtain_presets(get_preset)
            if make_content:
                pass
            else:
                return
            for each in make_content:
                getFolders = [(folderItem) for folderItem in os.listdir(each) if "mov" in folderItem]
                if getFolders:
                    sub = "yes"
                else:
                    sub = "no"                
                get_actual_time = time.ctime(os.path.getmtime(each))
                stat_buffer = os.stat(each)   
                time_format = datetime.datetime.fromtimestamp(stat_buffer.st_mtime).strftime('%c')
                time_format = time_format.split(" ")[:4]
                time_format = " ".join(time_format)
                if "  " in str(get_actual_time):
                    get_actual_time = get_actual_time.split("  ")
                    get_actual_time = get_actual_time[1].split(" ")[1]
                else:
                    get_actual_time = get_actual_time.split(" ")[3]
                time_format = time_format + "  " + get_actual_time + '>' + sub
                make_dict = (each, time_format)
                file_dict.append(make_dict)
            count = len(file_dict)
            file_dict = reversed(file_dict)     
            count = len(make_content)
            self.playBlastList.setColumnCount(4)
            self.playBlastList.setRowCount(count)
            self.playBlastList.setHorizontalHeaderLabels(headers)
            self.set_table_withsub(file_dict)

    def append_artist_review(self, get_artist_review_list, make_new_content):
        '''This is the append to artist review list function'''
        inp = open(get_artist_review_list, "w + ")
        inp.write(str(make_new_content))
        inp.close()
        print "appended " + str(make_new_content) + " into " + get_artist_review_list

    #AUXILLARY FUNCTIONS

    ##SETUP

    def start_window(self, cut_in_value, cut_out_value):
        '''runs once window is launched to prefill the playblast list'''
        index = self.scene_drp.findText(_scene, QtCore.Qt.MatchFixedString)
        self.scene_drp.setCurrentIndex(index)
        self.get_scene()
        index2 = self.shot_drp.findText(_shot, QtCore.Qt.MatchFixedString)
        self.shot_drp.setCurrentIndex(index2)
        index6 = self.reviewtype_drp.findText(setDefaultType[0], QtCore.Qt.MatchFixedString)
        self.reviewtype_drp.setCurrentIndex(index6)
        try:
            self.head_field.setText(str(float(cut_in_value)))
            self.toe_field.setText(str(float(cut_out_value)))
        except IndexError:
            self.head_field.setText("0")
            self.toe_field.setText("0")
        self.playblast_list_create(_dept_task, _scene, _shot)

    def get_scene(self):
        '''This reads the scene drop down and then fills the shot drop down'''
        listed_scene = self.scene_drp
        listed_scene = listed_scene.currentText()         
        get_selected_path = '/jobs/' + _project + '/' + listed_scene
        get_items = os.listdir(get_selected_path)
        get_items = sorted(get_items)
        self.get_shot(get_items)

    def get_shot(self, get_items):
        '''This fills the shot drop down'''
        getDrop_scene = self.shot_drp
        getDrop_scene.clear()
        getDrop_scene.addItems(get_items)

    def find_playlists(self, prodding_directory):
        '''This is triggered to find any stored artist review lists'''
        preset = False
        format = ".txt"
        prodding_directory=str(prodding_directory)
        get_preset = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(prodding_directory) for name in files if name.lower().endswith(format)]
        preset = [(each) for each in get_preset if "storedText" in each]
        return preset

    def playblast_list_create(self, set_dept, set_scene, set_shot):
        '''This populates the playblast list'''   
        self.playBlastList.setColumnCount(4)
        file_dict, count = self.grab_folder_items(set_dept, set_scene, set_shot) 
        self.playBlastList.setRowCount(count)
        self.playBlastList.setHorizontalHeaderLabels(headers)
        if file_dict == False:
            return
        else:
            self.set_table_withsub(file_dict)

    def set_folder_items(self, directory):
        '''This sorts the playlist items by date'''
        try:
            get_files = [os.path.join(directory, o) for o in os.listdir(directory) if os.path.isdir(os.path.join(directory, o))]
            pass
        except IndexError:
            return  
        get_files.sort(key = lambda x: os.path.getmtime(x))
        file_dict = []
        for each in get_files:
            stat_buffer = os.stat(each)           
            get_actual_time = time.ctime(os.path.getmtime(each))
            time_format = datetime.datetime.fromtimestamp(stat_buffer.st_mtime).strftime('%c')
            time_format = time_format.split(" ")[:4]
            time_format = " ".join(time_format)
            if "  " in str(get_actual_time):
                get_actual_time = get_actual_time.split("  ")
                get_actual_time = get_actual_time[1].split(" ")[1]
            else:
                get_actual_time = get_actual_time.split(" ")[3]
            time_format = time_format + "  " + get_actual_time
            make_dict = (each, time_format)
            file_dict.append(make_dict)
        count = len(file_dict)
        file_dict = reversed(file_dict)
        return file_dict, count

    def update_review_latest_buttons(self, versioning_dictionary): 
        '''This gathers latest from deptartments information and sets button info and activity'''
        department_list = [
        "matchmove",
        "mm pub",
        "anim",
        "an pub",
        "techanim",
        "ta pub",
        "light",
        "comp",
        "track",
        "fx", 
        "roto"]
        for each_dept in department_list:
            if each_dept == "matchmove":
                window_button=self.play_mm_btn
                getMov = versioning_dictionary.get("get_mm_ver")
                set_date = versioning_dictionary.get("get_mm_date")
                self.set_butt(each_dept, getMov, window_button, set_date)
            elif each_dept == "mm pub":
                window_button=self.play_mm_pub_btn
                getMov = versioning_dictionary.get("get_mm_pub_ver")
                set_date = versioning_dictionary.get("get_mm_pub_date")
                self.set_butt(each_dept, getMov, window_button, set_date)
            elif each_dept == "anim":
                window_button=self.play_anim_btn
                getMov = versioning_dictionary.get("get_an_ver")
                set_date = versioning_dictionary.get("get_an_date")
                self.set_butt(each_dept, getMov, window_button, set_date)
            elif each_dept == "an pub":
                window_button=self.play_anim_pub_btn
                getMov = versioning_dictionary.get("get_an_pub_ver")
                set_date = versioning_dictionary.get("get_an_pub_date")
                self.set_butt(each_dept, getMov, window_button, set_date)
            elif each_dept == "techanim":
                window_button=self.play_ta_btn
                getMov = versioning_dictionary.get("get_ta_ver")
                set_date = versioning_dictionary.get("get_ta_date")
                self.set_butt(each_dept, getMov, window_button, set_date)
            elif each_dept == "ta pub":
                window_button=self.play_ta_pub_btn
                getMov = versioning_dictionary.get("get_ta_pub_ver")
                set_date = versioning_dictionary.get("get_ta_pub_date")
                self.set_butt(each_dept, getMov, window_button, set_date)
            elif each_dept == "light":
                window_button=self.play_light_btn
                getMov = versioning_dictionary.get("get_light_ver")
                set_date = versioning_dictionary.get("get_light_date")
                self.set_butt(each_dept, getMov, window_button, set_date)
            elif each_dept == "comp":
                window_button=self.play_comp_btn
                getMov = versioning_dictionary.get("get_comp_ver")
                set_date = versioning_dictionary.get("get_comp_date")
                self.set_butt(each_dept, getMov, window_button, set_date)
            elif each_dept == "track":
                window_button=self.play_track_btn
                getMov = versioning_dictionary.get("get_track_ver")
                set_date = versioning_dictionary.get("get_track_date")
                self.set_butt(each_dept, getMov, window_button, set_date)
            elif each_dept == "fx":
                window_button=self.play_fx_btn
                getMov = versioning_dictionary.get("get_fx_ver")
                set_date = versioning_dictionary.get("get_fx_date")
                self.set_butt(each_dept, getMov, window_button, set_date)
            elif each_dept == "roto":
                window_button=self.play_roto_btn
                getMov = versioning_dictionary.get("get_roto_ver")
                set_date = versioning_dictionary.get("get_roto_date")
                self.set_butt(each_dept, getMov, window_button, set_date)
            

    def set_butt(self, each_dept, getMov, window_button, set_date):
        '''This populates the latest quicktimes from depts buttons'''
        if type(getMov) != type(None):
            if getMov != 'no ver':
                getitem = getMov.split('/')[-2]
                ver_attr = getitem.split('_')[-1]
                title=each_dept+" "+ver_attr                
                window_button.setText(title)
                window_button.setToolTip(set_date)
                window_button.setEnabled(True)
                window_button.setStyleSheet("color: #b1b1b1; background-color: rgba%s;" %str(regularDict.get("shotgun")))
            else:
                self.off_button(each_dept, window_button)
        else:
            self.off_button(each_dept, window_button)

    def off_button(self, each_dept, window_button):
        '''This sets off button status'''
        title=each_dept+" no ver"
        window_button.setText(title)
        window_button.setEnabled(False)
        window_button.setStyleSheet("color: rgb%s; background-color: rgba%s;" %(str(regularDict.get("grey")), str(regularDict.get("light_grey"))))

    def get_listset_directory(self):
        '''This fetches any artist review playlist txt files that have been saved into directory'''
        list_array = self.playBlastList
        count_data = list_array.rowCount()
        model = list_array.model()
        return model, count_data, list_array

    def obtain_presets(self, prodding_file):
        '''This is triggered during the append function to grab the information in the existing text file'''
        for each in prodding_file:
            List = open(each).readlines()
            for aline in List:
                make_content = ast.literal_eval(aline)
                return make_content
            
    def cust_playblast_list_create(self, pathFound, list_type):
        '''This is the function that populates the playblast list based on custom paths'''
        self.playBlastList.setColumnCount(4)
        try:
            if list_type == "file":
                get_files = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(_play_list_path) for name in files]
            elif list_type == "folder":
                get_files = [os.path.join(pathFound, o) for o in os.listdir(pathFound) if os.path.isdir(os.path.join(pathFound, o))]
            pass
        except IndexError:
            print "nothing found"
            return
        get_files.sort(key = lambda x: os.path.getmtime(x))
        file_dict = []
        sub = "no"
        for each in get_files:
            stat_buffer = os.stat(each)
            get_actual_time = time.ctime(os.path.getmtime(each))
            time_format = datetime.datetime.fromtimestamp(stat_buffer.st_mtime).strftime('%c')
            time_format = time_format.split(" ")[:4]
            time_format = " ".join(time_format)
            if "  " in str(get_actual_time):
                get_actual_time = get_actual_time.split("  ")
                get_actual_time = get_actual_time[1].split(" ")[1]
            else:
                get_actual_time = get_actual_time.split(" ")[3]
            time_format = time_format + "  " + get_actual_time + '>' + sub
            make_dict = (each, time_format)
            file_dict.append(make_dict)
        count = len(file_dict)
        file_dict = reversed(file_dict)
        dictItems = file_dict
        self.playBlastList.setRowCount(count)
        self.playBlastList.setHorizontalHeaderLabels(headers)
        self.set_table_withsub(file_dict)

    def replayblast_list_create(self, directory):
        '''This fetches information of the subfolder when the user double clicked the playblast list item'''
        self.playBlastList.setColumnCount(4)
        file_dict, count = self.set_folder_items(directory)        
        self.playBlastList.setRowCount(count)
        self.playBlastList.setHorizontalHeaderLabels(headers)
        sub = 'no'
        self.set_table_nosub(file_dict, sub)

    def set_table_nosub(self, file_dict, sub):
        for row, item in enumerate(file_dict):
            key = item[0].split('/')[-1]
            path = item[0]
            value = item[1].split('>')[0]
            self.playBlastList.setItem(row, 0, QTableWidgetItem(key))
            self.playBlastList.setItem(row, 1, QTableWidgetItem(value))
            self.playBlastList.setItem(row, 2, QTableWidgetItem(path))
            self.playBlastList.setItem(row, 3, QTableWidgetItem(sub))

    def set_table_withsub(self, file_dict):
        for row, item in enumerate(file_dict):
            key = item[0].split('/')[-1]
            path = item[0]
            value = item[1].split('>')[0]
            sub = item[1].split('>')[1]
            self.playBlastList.setItem(row, 0, QTableWidgetItem(key))
            self.playBlastList.setItem(row, 1, QTableWidgetItem(value))
            self.playBlastList.setItem(row, 2, QTableWidgetItem(path))
            self.playBlastList.setItem(row, 3, QTableWidgetItem(sub))

    def direct_play_rv(self, item):
        '''This is the function that plays the latest dept daily button and if something is selected in playblast list, it will compare to it'''
        selected_in_list = self.is_listWid_item_selected()
        if selected_in_list:
            converted_items = '/* '.join(selected_in_list)
            command = "rv -wipe " + str(item) + "/* " + converted_items + "/*"
            print "you are running command: " + command
            subprocess.Popen(command, stdout = subprocess.PIPE, shell = True)       
        else:
            command = "rv " + str(item)
            print "you are running command: " + command
            subprocess.Popen(command, stdout = subprocess.PIPE, shell = True)   

    def is_listWid_item_selected(self):
        '''This detects which row is selected. This will default to a row regardless of column selected'''
        list_widget = self.playBlastList
        (data_in_playblast_listWidget, count_data) = self.get_listWidgetData()
        get_string_id = []
        for index in xrange(count_data):
            get = list_widget.item(index, 0).isSelected()
            if get == True:
                get_table_data = list_widget.item(index, 2).text()
                get_table_data = str(get_table_data)
                get_string_id.append(get_table_data)
            else:
                get = list_widget.item(index, 1).isSelected()
                if get == True:
                    get_table_data = list_widget.item(index, 2).text()
                    get_table_data = str(get_table_data)
                    get_string_id.append(get_table_data)
                else:
                    get = list_widget.item(index, 2).isSelected()
                    if get == True:
                        get_table_data = list_widget.item(index, 2).text()
                        get_table_data = str(get_table_data)
                        get_string_id.append(get_table_data)
                    else:
                        get = list_widget.item(index, 3).isSelected()
                        if get == True:
                            get_table_data = list_widget.item(index, 3).text()
                            get_table_data = str(get_table_data)
                            get_string_id.append(get_table_data)                        
        return get_string_id

    def is_listWid_item_not_selected(self):
        '''This detects which row is not selected. This will default to a row regardless of column selected'''
        list_widget = self.playBlastList
        (data_in_playblast_listWidget, count_data) = self.get_listWidgetData()
        get_string_id = []
        for index in xrange(count_data):
            get = list_widget.item(index, 0).isSelected()
            if get == False:
                get_table_data = list_widget.item(index, 2).text()
                get_table_data = str(get_table_data)
                get_string_id.append(get_table_data)
            else:
                get = list_widget.item(index, 1).isSelected()
                if get == False:
                    get_table_data = list_widget.item(index, 2).text()
                    get_table_data = str(get_table_data)
                    get_string_id.append(get_table_data)
                else:
                    get = list_widget.item(index, 2).isSelected()
                    if get == False:
                        get_table_data = list_widget.item(index, 2).text()
                        get_table_data = str(get_table_data)
                        get_string_id.append(get_table_data)
                    else:
                        get = list_widget.item(index, 3).isSelected()
                        if get == False:
                            get_table_data = list_widget.item(index, 3).text()
                            get_table_data = str(get_table_data)
                            get_string_id.append(get_table_data)                        
        return get_string_id

    def get_listWidgetData(self):
        '''This obtains data from the playblast list items'''
        model, count_data, list_array  = self.get_listset_directory()   
        data_in_playblast_listWidget = []
        for row in range(model.rowCount()):
            data_in_playblast_listWidget.append([])
            for column in range(model.columnCount()):
                index = model.index(row, column)
                data_in_playblast_listWidget[row].append(str(model.data(index).toString()))
        return data_in_playblast_listWidget, count_data

    def grab_folder_items(self, set_dept, set_scene, set_shot):
        '''This obtains information about the selected item in the playblast list'''
        dept_image_path ='/jobs/' + _project + '/' + set_scene + '/' + set_shot + '/PRODUCTS/images/'
        if os.path.isdir(dept_image_path) == True:
            get_depts = os.listdir(dept_image_path)
            rv_folder = dept_image_path
            directory = dept_image_path + set_dept
            directory = str(directory)            
            deptload = self.dept_drp
            deptType = deptload.currentText()
            deptType = str(deptType)
            file_dict = []
            get_files_exists = False
            count = False
            if os.path.isdir(directory):
                get_files = [os.path.join(directory, o) for o in os.listdir(directory) if os.path.isdir(os.path.join(directory, o))]
                get_files.sort(key = lambda x: os.path.getmtime(x))
                get_files_exists = True
            else:
                get_files_exists = False
                count = False
                file_dict = False
            if get_files_exists == True:
                for each_folder in get_files:
                    getFolders = [(folderItem) for folderItem in os.listdir(each_folder) if "mov" in folderItem]
                    if getFolders:
                        sub = "yes"
                    else:
                        sub = "no"
                    stat_buffer = os.stat(each_folder)
                    get_actual_time = time.ctime(os.path.getmtime(each_folder))
                    time_format = datetime.datetime.fromtimestamp(stat_buffer.st_mtime).strftime('%c')
                    time_format = time_format.split(" ")[:4]
                    time_format = " ".join(time_format)
                    if "  " in str(get_actual_time):
                        get_actual_time = get_actual_time.split("  ")
                        get_actual_time = get_actual_time[1].split(" ")[1]
                    else:
                        get_actual_time = get_actual_time.split(" ")[3]
                    time_format = time_format + "  " + get_actual_time + '>' + sub
                    make_dict = (each_folder, time_format)
                    file_dict.append(make_dict)
                count = len(file_dict)
                file_dict = reversed(file_dict)
                dictItems = file_dict
        else:
            dept_image_path ='/jobs/' + _project + '/' + set_scene + '/' + set_shot
            directory = dept_image_path
            count = False
            file_dict = False        
        return file_dict, count

    def set_defaults(self, scene_name, shot_name):
        '''This is the main function for setting up the defaults for latest movs from each dept and getting cut length'''
        sgvar_file_path = '/jobs/%s/%s/%s/TECH/lib/shotgun/setshot.d/sgvars' % (_project, scene_name, shot_name)
        if os.path.isfile(sgvar_file_path) == True:
            franges = {'WORK_IN': None, 'CUT_IN': None,
                       'WORK_OUT': None, 'CUT_OUT': None}
            for line in open(sgvar_file_path, 'r'):
                if "CUT_DURATION" in line:
                    shot_len_value = line.split('=')[-1].strip()
                    if shot_len_value != "None":
                        try:
                            shot_len_value = int(shot_len_value)
                        except IndexError:
                            shot_len_value = 0.0
                    else:
                        shot_len_value = 0.0
                if 'CUT_IN' in line:
                    cut_in_value = line.split('=')[-1].strip()
                    if cut_in_value != "None":
                        try:
                            cut_in_value = int(cut_in_value)
                        except IndexError:
                            cut_in_value = 0.0
                    else:
                        cut_in_value = 0.0
                if 'CUT_OUT' in line:
                    cut_out_value = line.split('=')[-1].strip()
                    if cut_out_value != "None":
                        try:
                            cut_out_value = int(cut_out_value)
                        except IndexError:
                            cut_out_value = 0.0
                    else:
                        cut_out_value = 0.0
                if 'WORK_IN' in line:
                    wk_strt_value = line.split('=')[-1].strip()
                    if wk_strt_value != "None":
                        try:
                            wk_strt_value = int(wk_strt_value)
                        except IndexError:
                            wk_strt_value = 0.0
                    else:
                        wk_strt_value = 0.0
                if 'WORK_OUT' in line:
                    wk_out_value = line.split('=')[-1].strip()
                    if wk_out_value != "None":
                        try:
                            wk_out_value = int(wk_out_value)
                        except IndexError:
                            wk_out_value = 0.0
                    else:
                        wk_out_value = 0.0
                if 'CUT_IN' in line:
                    cut_shouldbe_in_value = line.split('=')[-1].strip()
                    if cut_shouldbe_in_value != "None":
                        try:
                            cut_shouldbe_in_value = int(cut_shouldbe_in_value)-8
                        except IndexError:
                            cut_shouldbe_in_value = 0.0
                    else:
                        cut_shouldbe_in_value = 0.0
                if 'CUT_OUT' in line:
                    cut_shouldbe_out_value = line.split('=')[-1].strip()
                    if cut_shouldbe_out_value != "None":
                        try:
                            cut_shouldbe_out_value = int(cut_shouldbe_out_value) + 8
                        except IndexError:
                            cut_shouldbe_out_value = 0.0
                    else:
                        cut_shouldbe_out_value = 0.0
        else:
            shot_len_value, cut_in_value, cut_out_value, wk_strt_value, wk_out_value, cut_shouldbe_in_value, cut_shouldbe_out_value = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        dept_list = {
        "matchmove": "mm",
        "trackcomp" : "track",
        "roto": "roto",
        "anim": "an",
        "techanim": "ta",
        "fxflip" : "fx", 
        "lightcomp": "light",
        "comp" : "comp",
        }
        versioning_dictionary={}
        for key, value in dept_list.items():
            ver_var = "get_"+value+"_ver"
            date_var = "get_"+value+"_date"                    
            play_folder = '/jobs/' + _project + '/' + scene_name + '/' + shot_name + '/PRODUCTS/images/' + key
            if os.path.isdir(play_folder) == True:
                file_dict = self.rv_latest_mov_nopub(play_folder)
                if len(file_dict)>0:
                    get_play = file_dict[-1][0]
                    create_temp_dict={ver_var : get_play}
                    versioning_dictionary.update(create_temp_dict)
                    create_attr = file_dict[-1][1] 
                    create_temp_dict={date_var : create_attr}
                    versioning_dictionary.update(create_temp_dict)
                else:
                    create_attr = 'no ver'
                    create_temp_dict={ver_var : create_attr}
                    versioning_dictionary.update(create_temp_dict)
                    create_temp_dict={date_var : create_attr}
                    versioning_dictionary.update(create_temp_dict)
            else:
                create_attr = 'no ver'
                create_temp_dict={ver_var : create_attr}
                versioning_dictionary.update(create_temp_dict)
                create_temp_dict={date_var : create_attr}
                versioning_dictionary.update(create_temp_dict)
        dept_list = {
        "matchmove": "mm_pub",
        "anim": "an_pub",
        "techanim":"ta_pub"        
        }
        for key, value in dept_list.items():
            ver_var = "get_"+value+"_ver"
            date_var = "get_"+value+"_date"                    
            play_folder = '/jobs/' + _project + '/' + scene_name + '/' + shot_name + '/PRODUCTS/images/' + key
            if os.path.isdir(play_folder) == True:
                file_dict = self.rv_latest_mov_pubonly(play_folder)
                if len(file_dict)>0:
                    get_play = file_dict[-1][0]
                    create_temp_dict={ver_var : get_play}
                    versioning_dictionary.update(create_temp_dict)
                    date_attr = file_dict[-1][1]
                    create_temp_dict={date_var : create_attr}
                    versioning_dictionary.update(create_temp_dict)
                else:
                    create_attr = 'no ver'
                    create_temp_dict={ver_var : create_attr}
                    versioning_dictionary.update(create_temp_dict)
                    create_temp_dict={date_var : create_attr}
                    versioning_dictionary.update(create_temp_dict)
            else:
                create_attr = 'no ver'
                create_temp_dict={ver_var : create_attr}
                versioning_dictionary.update(create_temp_dict)
                create_temp_dict={date_var : create_attr}
                versioning_dictionary.update(create_temp_dict)        
        return shot_len_value, cut_in_value, cut_out_value, wk_strt_value, wk_out_value, cut_shouldbe_in_value, cut_shouldbe_out_value\
                ,versioning_dictionary

    def rv_latest_mov_pubonly(self, play_folder):
        '''This returns the latest pubrender of the dept listed(This should only be assigned to depts that pubRender EG: anim, techanim)'''
        play_folder=str(play_folder)
        if os.path.isdir(play_folder) == True:
            get_files = [os.path.join(play_folder, o) for o in os.listdir(play_folder) if os.path.isdir(os.path.join(play_folder, o))]
        else:
            return
        get_files.sort(key = lambda x: os.path.getmtime(x))
        file_dict = []
        for each_file in get_files:
            get_the_mov_folders = [(folderItem) for folderItem in os.listdir(each_file) if "mov" in folderItem and "pubRender" in folderItem]
            if get_the_mov_folders:
                make_dict = self.gather_files(get_the_mov_folders, each_file, file_dict)
                file_dict.append(make_dict)
        return file_dict

    def rv_latest_mov_nopub(self, play_folder):
        '''This returns the latest playblast of the dept listed(This should only be assigned to depts that pubRender EG: anim, techanim)'''
        play_folder=str(play_folder)
        if os.path.isdir(play_folder) == True:
            get_files = [os.path.join(play_folder, o) for o in os.listdir(play_folder) if os.path.isdir(os.path.join(play_folder, o))]
            pass
        else:
            return
        get_files.sort(key = lambda x: os.path.getmtime(x))
        file_dict = []
        for each_file in get_files:
            get_the_mov_folders = [(folderItem) for folderItem in os.listdir(each_file) if "mov" in folderItem and "pubRender" not in folderItem]
            if get_the_mov_folders:
                make_dict = self.gather_files(get_the_mov_folders, each_file, file_dict)
                file_dict.append(make_dict)
        return file_dict                

    def gather_files(self, get_the_mov_folders, each_file, file_dict):
        '''get files and date information'''
        stat_buffer = os.stat(each_file)
        get_actual_time = time.ctime(os.path.getmtime(each_file))
        get_movie = each_file + '/' + get_the_mov_folders[0]
        time_format = datetime.datetime.fromtimestamp(stat_buffer.st_mtime).strftime('%c')
        time_format = time_format.split(" ")[:4]
        time_format = " ".join(time_format)
        if "  " in str(get_actual_time):
            get_actual_time = get_actual_time.split("  ")
            get_actual_time = get_actual_time[1].split(" ")[1]
        else:
            get_actual_time = get_actual_time.split(" ")[3]
        time_format = time_format + "  " + get_actual_time
        make_dict = (get_movie, time_format)
        return make_dict

app = QtGui.QApplication(sys.argv)
inst = mSubManagerWin()
inst.show()
sys.exit(app.exec_())

