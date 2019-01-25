

# import maya.cmds as mc
import os, sys, subprocess
from datetime import datetime

# import xgenm as xg 
# import xgenm.xgGlobal as xgg
# import xgenm.XgExternalAPI as xge

import re

# from mshotgun import mShotgun
import mrig_pyqt
from mrig_pyqt import QtCore, QtGui
from mrig_pyqt.QtGui import QWidget, QRadioButton, QGridLayout, QLabel, QScrollArea, \
    QTableWidget, QComboBox, QKeySequence, QToolButton, QPlainTextEdit, QPushButton,QBoxLayout, \
    QClipboard, QTableWidgetItem, QCheckBox, QVBoxLayout, QHBoxLayout, \
    QPixmap, QLineEdit, QListWidget, QTextEdit, QSizePolicy, QFrame, QPalette, QColor, \
    QFont, QAbstractItemView, QMenu, QMessageBox
from mrig_pyqt.QtCore import SIGNAL

from time import gmtime, strftime
        
_project = os.getenv("M_JOB")
_scene = os.getenv("M_SEQUENCE")
_shot = os.getenv("M_LEVEL")
_dept_task = os.getenv("M_TASK")
_get_partial_folder='/jobs/' + _project + '/' + _scene + '/' + _shot + '/PRODUCTS/instances/'
path_build='/jobs/'+_project+'/'+_scene+'/'+_shot+'/TASKS/'+_dept_task+'/maya/scenes/pub_MSG/'
_get_cfx_folder = [(dirpath) for dirpath, dirnames, files in os.walk(_get_partial_folder) if "techanim" in dirpath and "groom" not in dirpath]
collect_assets=[]
for item in _get_cfx_folder:
    find = re.search(r"\d+$", item)
    if find != None:
        ab_seq=item.split("/techanim")[0]
        b_seq=ab_seq.split("instances/")[-1]
        collect_assets.append(b_seq)
get_assets =  set(collect_assets)


title = str(_shot)+" cfx versions"

if len(get_assets) <1:
    _get_cfx_folder = [(dirpath) for dirpath, dirnames, files in os.walk(_get_partial_folder) if "techanim" in dirpath]
    collect_assets=[]
    for item in _get_cfx_folder:
        find = re.search(r"\d+$", item)
        if find != None:
            ab_seq=item.split("/techanim")[0]
            b_seq=ab_seq.split("instances/")[-1]
            collect_assets.append(b_seq)
    get_assets =  set(collect_assets)
    print get_assets

class set_pubAssets_win(QtGui.QWidget):
    # def __init__(self): 
    def __init__(self):
        super(set_pubAssets_win, self).__init__()
        self.initUI()

    def initUI(self):    
        print "This might take a moment. This tool accesses folders on the network and mas. If there are network issues, tools like this will be affected."  
        self.setWindowTitle(title)

        self.myform = QtGui.QFormLayout()
        self.layout=QtGui.QGridLayout()


        self.color_layout=QGridLayout()
        self.color_layout.setAlignment(QtCore.Qt.AlignTop)
        
        
        self.colorSetupLayout=QtGui.QGridLayout()
        self.colorOverride=QtGui.QFrame()
        # self.colorOverride.setFixedHeight(400)
        self.colorOverride.setLayout(self.colorSetupLayout)
        self.colorSetupLayout.addLayout(self.myform, 0,0,1,1)
        self.layout.addLayout(self.colorSetupLayout, 0,0,1,1)

        self.btnlayout = QVBoxLayout()
                  
        self.add_widgets()

        scroll = QtGui.QScrollArea()
        scroll.setWidget(self.colorOverride)
        scroll.setWidgetResizable(False)
        # scroll.setFixedHeight(400)
        self.layout.addWidget(scroll, 1,0,1,1)


        self.layout.addLayout(self.btnlayout, 0,0,1,1)    
        self.sel_button = QPushButton("Print")
        self.connect(self.sel_button, SIGNAL("clicked()"),
                    lambda: self.buildVers(self.store_vars))
        self.btnlayout.addWidget(self.sel_button)
        self.save_button = QPushButton("Save")
        self.connect(self.save_button, SIGNAL("clicked()"),
                    lambda: self.saveVers(self.store_vars))
        self.btnlayout.addWidget(self.save_button)
        self.open_folder_button = QPushButton("Open folder")
        self.connect(self.open_folder_button, SIGNAL("clicked()"),
                    lambda: self.open_defined_path())
        self.btnlayout.addWidget(self.open_folder_button)
        self.open_letter_button = QPushButton("Open last msg")
        self.connect(self.open_letter_button, SIGNAL("clicked()"),
                    lambda: self.open_asset_info())
        self.btnlayout.addWidget(self.open_letter_button)    
        self.prnt_letter_button = QPushButton("Print last msg")
        self.connect(self.prnt_letter_button, SIGNAL("clicked()"),
                    lambda: self.print_saved_asset_info())
        self.btnlayout.addWidget(self.prnt_letter_button)     
        self.prnt_verbose_button = QPushButton("Print sources")
        self.connect(self.prnt_verbose_button, SIGNAL("clicked()"),
                    lambda: self.print_verbose(self.store_vars))
        self.btnlayout.addWidget(self.prnt_verbose_button)      
        self.btnlayout_lower = QVBoxLayout()
        self.check_all_button = QPushButton("Check all")
        self.connect(self.check_all_button, SIGNAL("clicked()"),
                    lambda: self.check_butts(self.store_vars))
        self.btnlayout_lower.addWidget(self.check_all_button)      
        self.uncheck_all_button = QPushButton("Uncheck all")
        self.connect(self.uncheck_all_button, SIGNAL("clicked()"),
                    lambda: self.uncheck_butts(self.store_vars))
        self.btnlayout_lower.addWidget(self.uncheck_all_button)    
        self.layout.addLayout(self.btnlayout_lower, 3,0,1,1)                     
        self.setLayout(self.layout)
        self.show()

    def add_widgets(self):
        self.asset_dict = {}
        self.store_vars = []
        for each in get_assets:
            gr_container={}
            vr_container = {}
            _get_formal_cfx_folder = [(dirpath) for dirpath, dirnames, files in os.walk(_get_partial_folder) if "techanim" in dirpath and "groom" not in dirpath and each in dirpath]
            _get_grm_folder = [(dirpath) for dirpath, dirnames, files in os.walk(_get_partial_folder) if "techanim" in dirpath and "groom" in dirpath and each in dirpath and "backupFxModule" not in dirpath and "Clumping" not in dirpath and "paintmaps" not in dirpath and "xgenData" not in dirpath ]
            if len(_get_grm_folder)>0:
                # _get_grm_folder = sorted(_get_grm_folder)
                for item in _get_grm_folder:
                    find = re.search(r"\d+$", item)
                    if find != None:
                        a_seq=item.split("techanim/")[-1]
                        ab_seq=item.split("/techanim")[0]
                        b_seq=ab_seq.split("instances/")[-1]
                        container_item={item:a_seq}
                        gr_container.update(container_item)
            # _get_formal_cfx_folder = sorted(_get_formal_cfx_folder)
            for item in _get_formal_cfx_folder:
                find = re.search(r"\d+$", item)
                if find != None:
                    a_seq=item.split("techanim/")[-1]
                    ab_seq=item.split("/techanim")[0]
                    b_seq=ab_seq.split("instances/")[-1]
                    collect_assets.append(b_seq)
                    container_item={item:a_seq}
                    vr_container.update(container_item) 
            get_geo_list = sorted(vr_container.values())
            get_gr_list = sorted(gr_container.values())
            get_geo_list = get_geo_list[::-1]
            get_gr_list = get_gr_list[::-1]
            self.cust_path_label = QCheckBox(each)
            self.cust_path_label.setCheckState(mrig_pyqt.QtCore.Qt.Checked)
            self.vertical_order_layout = QtGui.QHBoxLayout()
            # self.cust_path_label = QLabel(each)
            self.ttop_line = QtGui.QFrame()
            self.ttop_line.setFrameShape(QFrame.HLine)
            self.ttop_line.setFrameShadow(QFrame.Sunken)
            self.cust_techanim = QLabel("techanim")
            self.vertical_order_layout_ta = QtGui.QHBoxLayout()
            self.techanim_geo_asset = QComboBox()
            self.techanim_geo_asset.addItems(get_geo_list)    
            self.cust_grm = QLabel("groom")
            self.vertical_order_layout_grm = QtGui.QHBoxLayout()
            self.techanim_gr_asset = QComboBox()
            self.techanim_gr_asset.addItems(get_gr_list)
            # self.myform.addRow(self.cust_path_label) 
            self.myform.addRow(self.vertical_order_layout) 
            self.myform.addRow(self.vertical_order_layout_ta) 
            self.myform.addRow(self.vertical_order_layout_grm) 
            self.myform.addRow(self.ttop_line)          
            buildlist= (self.techanim_geo_asset, self.techanim_gr_asset)
            self.vertical_order_layout.addWidget(self.cust_path_label)            
            self.vertical_order_layout_ta.addWidget(self.cust_techanim)       
            self.vertical_order_layout_grm.addWidget(self.cust_grm)       
            self.vertical_order_layout_grm.addWidget(self.techanim_gr_asset)
            self.vertical_order_layout_ta.addWidget(self.techanim_geo_asset)
            create_dict=(self.cust_path_label, buildlist)
            self.store_vars.append(create_dict)

    def uncheck_butts(self,asset_dict):
        for each in asset_dict:          
            each[0].setCheckState(mrig_pyqt.QtCore.Qt.Unchecked)

    def check_butts(self,asset_dict):
        for each in asset_dict:          
            each[0].setCheckState(mrig_pyqt.QtCore.Qt.Checked)        
        # self.cust_path_label.setCheckState(mrig_pyqt.QtCore.Qt.Checked)

    def buildVers(self, asset_dict):
        access_main = _shot_asset_identification_Win()
        access_main.set_pub_info(asset_dict)
        # self.close()

    def saveVers(self, asset_dict):
        access_main = _shot_asset_identification_Win()
        access_main.save_pub_asset_info(asset_dict)
        # self.close()

    def print_saved_asset_info(self):
        access_main = _shot_asset_identification_Win()
        access_main._print_saved_asset_info()

    def open_asset_info(self):     
        access_main = _shot_asset_identification_Win()
        access_main._open_asset_info()

    def open_defined_path(self): 
        access_main = _shot_asset_identification_Win()
        access_main._open_defined_path()


    def print_verbose(self, asset_dict): 
        access_main = _shot_asset_identification_Win()
        access_main._print_verbose(asset_dict)

    # def openpub_r_click(self, variables, asset):
    #     print variables, asset
    #     Rtf_text = asset
    #     Temp_Obj = QtGui.QTextEdit()
    #     Temp_Obj.setText(Rtf_text)
    #     pl_getitle = Temp_Obj.toPlainText()
    #     pl_getitle = str(pl_getitle)
    #     print pl_getitle
    #     PROJECT = os.getenv("M_JOB")
    #     SCENE = os.getenv("M_SEQUENCE")
    #     SHOT = os.getenv("M_LEVEL")
    #     DEPT = os.getenv("M_TASK")
    #     variables=str(variables)
    #     _get_partial_folder='/jobs/' + PROJECT + '/' + SCENE + '/' + SHOT + '/PRODUCTS/instances/'
    #     getsuch=_get_partial_folder+pl_getitle+'/'+DEPT+'/'+variables+'/'
    #     getsuch=str(getsuch)
    #     print getsuch



class _shot_asset_identification_Win():


    def print_info(self):     
        mainRig=[(each) for each in mc.ls("*:*animGeo") if mc.listRelatives(each, p=1) ==None]
        if len(mainRig)<1:
            findobjects = mc.ls("*:*.file")
            mainRig = [(each.split('.')[0]) for each in findobjects]  
        if len(mainRig)>0:
            pass
        else:
            self.print_info_abc()
        collect_comments = []
        saved_name = []
        for item in mainRig:
            if mc.getAttr(item+".type") == "char":
                comment, save_name = self.find_comment_for_asset(item)    
                collect_comments.append(comment)
                saved_name.append(save_name)  
            else:
                comment, save_name = self.find_comment_for_prop(item)   
                collect_comments.append(comment) 
                saved_name.append(save_name)     
        if len(saved_name)>0:
            saved_name = saved_name[0]
        else:
            saved_name = saved_name
        create_comment="\n\n".join(collect_comments)
        print str(create_comment)        


    def print_info_abc(self):     
        mainRig=[(each) for each in mc.ls("*:*_hi") if mc.listRelatives(each, p=1) ==None]
        collect_comments = []
        saved_name = []
        for item in mainRig:
            if mc.getAttr(item+".type") == "char":
                comment, save_name = self.find_comment_for_asset(item)    
                collect_comments.append(comment)
                saved_name.append(save_name)  
            else:
                comment, save_name = self.find_comment_for_prop(item)   
                collect_comments.append(comment) 
                saved_name.append(save_name)     
        if len(saved_name)>0:
            saved_name = saved_name[0]
        else:
            saved_name = saved_name
        create_comment="\n\n".join(collect_comments)
        print str(create_comment)        


    def save_asset_info(self):
        mainRig=[(each) for each in mc.ls("*:*animGeo") if mc.listRelatives(each, p=1) ==None]
        if len(mainRig)<1:
            findobjects = mc.ls("*:*.file")
            mainRig = [(each.split('.')[0]) for each in findobjects]     
        collect_comments = []
        saved_name = []
        for item in mainRig:
            if mc.getAttr(item+".type") == "char":
                comment, save_name = self.find_comment_for_asset(item)    
                collect_comments.append(comment)
                saved_name.append(save_name)  
            else:
                comment, save_name = self.find_comment_for_prop(item)   
                collect_comments.append(comment) 
                saved_name.append(save_name)     
        if len(saved_name)>0:
            saved_name = saved_name[0]
        else:
            saved_name = saved_name
        create_comment="\n\n".join(collect_comments)
        path_build='/jobs/'+_project+'/'+_scene+'/'+_shot+'/TASKS/'+_dept_task+'/maya/scenes/pub_MSG/'
        if not os.path.exists(path_build): os.makedirs(path_build)
        file_path_build='/jobs/'+_project+'/'+_scene+'/'+_shot+'/TASKS/'+_dept_task+'/maya/scenes/pub_MSG/'+save_name+'.txt'
        inp = open(file_path_build, 'w+')
        inp.write(str(create_comment))
        inp.close()  
        print str(create_comment)         
        print "saving text file: "+save_name+" in "+path_build


    def what_did_anim_say(self):   
        PROJECT = os.getenv("M_JOB")
        SCENE = os.getenv("M_SEQUENCE")
        SHOT = os.getenv("M_LEVEL")
        DEPT = os.getenv("M_TASK")          
        _get_TAV_folder='/jobs/' + PROJECT + '/' + SCENE + '/' + SHOT + '/PRODUCTS/instances/'   
        mainRig=[(each) for each in mc.ls("*:*animGeo") if mc.listRelatives(each, p=1) ==None]        
        if len(mainRig)<1:
            findobjects = mc.ls("*:*.file")
            mainRig = [(each.split('.')[0]) for each in findobjects]      
        for item in mainRig:
            getRef = [(each) for each in mc.ls(type = "reference") if item.split(":")[0] in str(each) and "Anim" in str(each)][0]
            getfileRef=mc.referenceQuery( getRef, filename=True)        
            b_curves= str(getfileRef).split("bakedcurves_v")[-1]
            a_curves= b_curves.split(".mb")[0]
            curves_ver= a_curves               
            # cullpath=getfileRef.split("_")[-1]
            # getAnimVer=cullpath.split(".mb")[0]     
            # grabPathpart=getfileRef.split(getAnimVer)[0]+'/'+getAnimVer+'/'
            # get_preset = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(grabPathpart) for name in files if name.lower().endswith(".yaml")][0]
            # timeFormat=os.stat(get_preset)
            get_preset = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(_get_TAV_folder) for name in files if name.lower().endswith(".yaml") and "anim" in dirpath]
            if "null" in curves_ver:
                print "anim ver can't be found in your published asset file for "+each+". defaulting to latest"
                get_item=max(get_items)
            else:
                get_item = [(each) for each in get_preset for name in files if curves_ver in each][0]                
            List = open(get_item).readlines()
            for aline in List:
                if "comment" in aline:
                    animCmnt= aline.split("comment:")[-1]
                    animCmntline= animCmnt.split('\n')[0]
            #find mas comment
            verver=int(curves_ver)
            from mas.service_client import ServiceClient
            mas_client = ServiceClient()
            for version in mas_client.search_versions(
                job=PROJECT,
                seq=SCENE,
                shot=SHOT,
                task='anim',
                version=verver,
                asset_type='collection'):
                if not version.name == item:
                    continue
            mas_comment = version.notes  
            #continue to message
            timeFormat=os.stat(get_item) 
            print item+' '+curves_ver+" last comment: '"+animCmntline+"' - This was set at: "+datetime.fromtimestamp(timeFormat.st_mtime).strftime('%c') 
            print "VS mas:"
            print item+' '+curves_ver+" last mas comment: '"+mas_comment+"'"
            print "check against history of events on version in mas-browser"

    def find_comment_for_prop(self, item):  
        # if mc.getAttr(item+".type") == "char"
        print "For Asset: "+item.split(":")[0]+":"
        _get_TAV_folder='/jobs/' + _project + '/' + _scene + '/' + _shot + '/PRODUCTS/instances/'+item.split(':')[0]+'/'+_dept_task+"/" 
        if os.path.exists(_get_TAV_folder):
            get_vr_folders = [(dirnames) for  dirnames in os.walk(_get_TAV_folder)][0][1]
            get_top_ta =  max(get_vr_folders)
            find_path_folder_max = os.path.join(_get_TAV_folder, get_top_ta)
            timeFormat=os.stat(os.path.join(_get_TAV_folder, get_top_ta)) 
            print "Checking for techanim - CURRENT highest available techanim: "+ get_top_ta + " finished publish at: "+datetime.fromtimestamp(timeFormat.st_mtime).strftime('%c')    
        else:
            get_top_ta = "v0001"
            print "No techanim available yet" 
        getRigVer= mc.getAttr(item+".version")
        getRef = []
        ref_collect = [(each) for each in mc.ls(type = "reference") if item.split(":")[0] in str(each) and "Anim" in str(each)]
        if len(ref_collect)>1:
            for each in ref_collect:
                m = re.search(r'\d+$', each)
                if m == None:
                    getRef.append(each)        
        else:
            getRef = ref_collect
        getfileRef=mc.referenceQuery( getRef, filename=True)
        cullpath=getfileRef.split("_")[-1]
        getAnimVer=cullpath.split(".mb")[0]
        getFile= mc.file(q=1, sn=1).split('/')[-1]
        getFilename=getFile.split('.mb')[0]
        comment =  "For: "+item+"\nTechanim Export using Anim:'<insert anim lock confirmation from mas>' version "+ getAnimVer +", animRig version "+getRigVer +" < hand off msg EG: techanim: '"+item.split(":")[0]+" ("+get_top_ta+") saved from: "+getFilename        
        savename = "AN"+ getAnimVer +"_RIG"+getRigVer +"_TA"+item.split(":")[0]+get_top_ta+"_pubmsg_"+getFilename
        return comment , savename 

    def find_comment_for_asset(self, item):  
        # if mc.getAttr(item+".type") == "char"
        print "For Asset: "+item.split(":")[0]+":"
        _get_TAV_folder='/jobs/' + _project + '/' + _scene + '/' + _shot + '/PRODUCTS/instances/'+item.split(':')[0]+'/'+_dept_task+"/" 
        _get_Grm_folder='/jobs/' + _project + '/' + _scene + '/' + _shot + '/PRODUCTS/instances/'+item.split(':')[0]+'_groom/'+_dept_task+"/"    
        print _get_Grm_folder             
        if os.path.exists(_get_TAV_folder):
            get_vr_folders = [(dirnames) for  dirnames in os.walk(_get_TAV_folder)][0][1]
            get_top_ta =  max(get_vr_folders)
            find_path_folder_max = os.path.join(_get_TAV_folder, get_top_ta)
            timeFormat=os.stat(os.path.join(_get_TAV_folder, get_top_ta)) 
            print "Checking for techanim - CURRENT highest available techanim: "+ get_top_ta + " finished publish at: "+datetime.fromtimestamp(timeFormat.st_mtime).strftime('%c')    
        else:
            get_top_ta = "v0001"
            print "No techanim available yet" 
        if os.path.exists(_get_Grm_folder):
            get_vr_folders = [(dirnames) for  dirnames in os.walk(_get_Grm_folder)][0][1]
            get_top_groom =  max(get_vr_folders)
            timeFormat=os.stat(os.path.join(_get_Grm_folder, get_top_groom)) 
            print "Checking for groom - CURRENT highest available groom: "+ get_top_groom + " finished publish at: "+datetime.fromtimestamp(timeFormat.st_mtime).strftime('%c')    
        else:
            get_top_groom = "v0001"
            print "No groom from techanim available for this asset (yet)" 
        getRigVer= mc.getAttr(item+".version")
        getRef = [(each) for each in mc.ls(type = "reference") if item.split(":")[0] in str(each) and "Anim" in str(each)]
        if len(getRef)>0:
            getfileRef=mc.referenceQuery( getRef, filename=True)
        else:
            getRef = [(each) for each in mc.ls(type = "reference") if item.split(":")[0] in str(each) ]
            getfileRef=mc.referenceQuery( getRef, filename=True)
        cullpath=getfileRef.split("_")[-1]
        getAnimVer=cullpath.split(".mb")[0]
        # getGroomVer = self.findGroom()
        getGroomVer = 'nil'
        getFile= mc.file(q=1, sn=1).split('/')[-1]
        getFilename=getFile.split('.mb')[0]
        comment = "For: "+item+"\nTechanim Export using Anim:'<insert anim lock confirmation from mas>' version "+ getAnimVer +", animRig version "+getRigVer +" < hand off msg EG: techanim: '"+item.split(":")[0]+" ("+get_top_ta+") use with techanim Groom ("+item.split(":")[0]+" "+get_top_groom+")(Groom:"+getGroomVer+")' OR: techanim: '"+item.split(":")[0]+" ("+get_top_ta+") - Use Anim Groom' > saved from: "+getFilename        
        if getGroomVer == "Anim's groom":
            savename = "AN"+ getAnimVer +"_RIG"+getRigVer +"_TA"+item.split(":")[0]+get_top_ta+"_ANG_pubmsg_"+getFilename
        else:
            savename = "AN"+ getAnimVer +"_RIG"+getRigVer +"_TA"+item.split(":")[0]+get_top_ta+"_TAG"+item.split(":")[0]+get_top_groom+"_GR"+getGroomVer+"_pubmsg_"+getFilename
        return comment , savename 





    def mas_browser(self):        
        subprocess.Popen('mas-browser', stdout=subprocess.PIPE, shell=True) 



    def set_pub_info(self, asset_dict):      
        getcomments = self.create_pub_info(asset_dict)
        for each in getcomments:
            print each

    def create_pub_info(self, asset_dict):      
        # from mas.service_client import ServiceClient
        # mas_client = ServiceClient()      
        # gr_workFile = "techanim groom workfile non existant"
        get_top_groom = "techanim fur NA"
        grm_ver = "--"      
        PROJECT = os.getenv("M_JOB")
        SCENE = os.getenv("M_SEQUENCE")
        SHOT = os.getenv("M_LEVEL")
        DEPT = os.getenv("M_TASK")          
        mas_comment = None
        comment = []
        grm_asset_true=False
        _get_TAV_folder='/jobs/' + PROJECT + '/' + SCENE + '/' + SHOT + '/PRODUCTS/instances/'
        #groom techanim version
        _get_partial_folder='/jobs/' + PROJECT + '/' + SCENE + '/' + SHOT + '/PRODUCTS/instances/'
        commentData = []
        for each in asset_dict:
            gr_workFile = "Groom autogen"
            tech_rig = "null"
            techanimCm = "null"
            curves_ver = "null"
            timeLine = "null"
            workFile = "null"
            animrig = "null"        
            modver = "null"       
            gr_pubnote = "null"          
            getState = int(each[0].checkState())
            if getState == 2:
                pl_getitle = each[0].text()
                pl_getitle = str(pl_getitle)
                # Rtf_text = each[0].text()
                # Temp_Obj = QtGui.QTextEdit()
                # Temp_Obj.setText(Rtf_text)
                # pl_getitle = Temp_Obj.toPlainText()
                # pl_getitle = str(pl_getitle)
                getgeover = each[1][0].currentText()
                getgeover = str(getgeover)
                getgrver = each[1][1].currentText()
                getgrver = str(getgrver)
                getsuch=_get_partial_folder+pl_getitle+'/'+DEPT+'/'+getgeover+'/'
                getsuch=str(getsuch)
                try:
                    get_yaml_item = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(getsuch) for name in files if name.lower().endswith(".yaml")][0]  
                    timeFormat_techanimGeo=os.stat(get_yaml_item)     
                    trueTime = timeFormat_techanimGeo
                    List = open(get_yaml_item).readlines()
                    for aline in List:
                        if "comment" in aline:
                            animCmnt= aline.split("comment:")[-1]
                            techanimCm= animCmnt.split('\n')[0]
                        if "curvesFilePath" in aline:
                            b_curves= aline.split("anim/")[-1]
                            a_curves= b_curves.split("/lodagnostic")[0]
                            curves_ver= a_curves
                        if "timestamp" in aline:
                            animCmnt= aline.split("timestamp:")[-1]
                            timeLine= animCmnt.split('\n')[0]   
                        if "userFilePath" in aline:
                            b_curves= aline.split("/")[-1]
                            workFile= b_curves.split('\n')[0]  
                        if "rig_animAll" in aline:
                            b_curves= aline.split("animAll/")[-1]
                            a_curves= b_curves.split("/mb")[0]
                            animrig= a_curves.split('\n')[0]     
                        if "mid_modelPath:" in aline:
                            b_curves= aline.split("/mid/")[-1]
                            a_curves= b_curves.split("/mb")[0]
                            modver= a_curves.split('\n')[0]
                        if "techRigVersion:" in aline:
                            b_curves= aline.split("techRigVersion: ")[-1]
                            a_curves= b_curves.split(", ")[0]
                            tech_rig= a_curves                        
                except:
                    if "_groom" not in pl_getitle:
                        pl_new_getitle = pl_getitle.split("_groom")[0]
                        print "It's possible the current version publish of "+pl_new_getitle+" ta:"+getgeover+" gr:"+getgrver+" has not finished publishing, failed OR was depreciated. Setting dependencies to anim's"
                        get_anim=_get_partial_folder+pl_new_getitle+'/anim/'
                    else:
                        pl_new_getitle = pl_getitle
                        print "Groom from techanim present only. Setting geo dependencies to anim's"
                        get_anim=_get_partial_folder+pl_new_getitle.split("_groom")[0]+'/anim/'
                    get_yaml_item = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(get_anim) for name in files if name.lower().endswith(".yaml")]
                    get_yaml_item=max(get_yaml_item)
                    b_curves= get_yaml_item.split("anim/")[-1]
                    a_curves= b_curves.split("/.metadata/")[0]
                    curves_ver= a_curves                    
                    List = open(get_yaml_item).readlines()
                    for aline in List:
                        if "comment" in aline:
                            animCmnt= aline.split("comment:")[-1]
                            techanimCm= animCmnt.split('\n')[0]
                        if "timestamp" in aline:
                            animCmnt= aline.split("timestamp:")[-1]
                            timeLine= animCmnt.split('\n')[0]   
                        if "userFilePath" in aline:
                            b_curves= aline.split("/")[-1]
                            workFile= b_curves.split('\n')[0]  
                        if "rig_animAll" in aline:
                            b_curves= aline.split("animAll/")[-1]
                            a_curves= b_curves.split("/mb")[0]
                            animrig= a_curves.split('\n')[0]   
                        if "mid_modelPath:" in aline:
                            b_curves= aline.split("/mid/")[-1]
                            a_curves= b_curves.split("/mb")[0]
                            modver= a_curves.split('\n')[0]   
                get_item = []
                get_items = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(_get_TAV_folder) for name in files if name.lower().endswith(".yaml") and "anim" in name]
                # print get_items
                if "null" in curves_ver:
                    print "anim ver can't be found in your published asset file for "+pl_getitle+". defaulting to latest"
                    get_item=max(get_items)
                else:
                    # print curves_ver
                    try:
                        # get_item = [(item) for item in get_items for name in files if curves_ver in item][0]  
                        get_item = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(_get_TAV_folder) for name in files if name.lower().endswith(".yaml") and "anim" in name and curves_ver in dirpath][0]
                    except:
                        curves_ver = curves_ver
                    # print get_item
                if len(get_item)>0:
                    timeFormat=os.stat(get_item)
                    List = open(get_item).readlines()
                    for aline in List:
                        if "comment" in aline:
                            animCmnt= aline.split("comment:")[-1]
                            animCmntline= animCmnt.split('\n')[0]       
                else:
                    animCmntline = "null"
               #findAniMAsComment
                if "null" in curves_ver:
                    print "cannot determine animation version from your publish of "+pl_getitle+" Will default to anim's yaml but will need to be crosschecked to the mas version"
                    mas_comment = animCmntline
                    pass
                else:
                    verver=curves_ver.split('v')[-1]
                    verver=int(verver)
                    from mas.service_client import ServiceClient
                    mas_client = ServiceClient()
                    for version in mas_client.search_versions(
                          job=PROJECT,
                          seq=SCENE,
                          shot=SHOT,
                          task='anim',
                          version=verver,
                          asset_type='collection'):
                      if not version.name == pl_getitle:
                          continue
                      mas_comment = version.notes 
                #get groom asset info
                if len(getgrver)>0:
                    if "groom" in pl_getitle:
                        each_grm_item = pl_getitle
                    else:
                        each_grm_item = pl_getitle+'_groom'
                    findLatestGroom=_get_partial_folder+each_grm_item+'/'+DEPT+'/'+getgrver+'/'
                    findLatestGroom=str(findLatestGroom)
                    try:
                        get_jsn_item = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(findLatestGroom) for name in files if name ==".pubInfo.json"][0]
                        timeFormat_jsn=os.stat(get_jsn_item) 
                        # if timeFormat_techanimGeo<timeFormat_jsn:
                        #     trueTime = timeFormat_jsn
                        # print "' - This was set at: "+datetime.fromtimestamp(timeFormat.st_mtime).strftime('%c')              
                        List = open(get_jsn_item).readlines()
                        for aline in List:
                            if "xgenVersion" in aline:
                                bline= aline.split('"xgenVersion": ')[-1] 
                                grm_ver= bline.split('\n')[0] 
                            if "xgenRep" in aline:
                                bline= aline.split('"xgenRep": ')[-1] 
                                grm_flav= bline.split('\n')[0]   
                            if "pubNote" in aline:
                                bline= aline.split('"pubNote": ')[-1] 
                                gr_pubnote= bline.split('\n')[0]                             
                            try:
                                if "userSourceFile" in aline:
                                    b_curves= aline.split("/")[-1]
                                    a_curves= b_curves.split(",")[0]
                                    gr_workFile= a_curves.split('\n')[0]
                            except:
                                gr_workFile = "grm auto generated"
                    except:
                        print "ERROR: A PUBINFO HAS NOT BEEN GENERATED FOR : "+pl_getitle+" groom version: "+getgrver+". Please check if this publish has finished."
                        grm_asset_items="None"
                        gr_workFile = "None"
                        grm_ver = "None"
                        getgrver = getgrver+" = EMPTY FOLDER"
                    # each_grm_item = pl_getitle+"_groom"
                    if "_groom" in pl_getitle:
                        comment_partial = "For: "+SHOT+" / "+pl_getitle+":\nCFX applying groom to Anim: "+ curves_ver +" '"+str(mas_comment)+"', animRig "+animrig +", midmodel "+modver+", techanim Groom: ("+each_grm_item+":"+getgrver+")(XgenGRM:"+grm_ver+", flavour:"+grm_flav+"), techanim comment: " +gr_pubnote+" Groom generated from: ("+gr_workFile+")\n[grm - "+datetime.fromtimestamp(timeFormat_jsn.st_mtime).strftime('%c')+"]"
                    else:
                        comment_partial = "For: "+SHOT+" / "+pl_getitle+":\nCFX Export using Anim: "+ curves_ver +" '"+str(mas_comment)+"', animRig "+animrig +", midmodel "+modver+", techanim abc: ("+pl_getitle+" "+getgeover+" using techrig: "+tech_rig+"), techanim Groom: ("+each_grm_item+":"+getgrver+")(XgenGRM:"+grm_ver+", flavour:"+grm_flav+"), techanim comment: '" +techanimCm+"' / "+gr_pubnote+" ABC generated from: ("+workFile +"), Groom generated from: ("+gr_workFile+")\n[geo - "+datetime.fromtimestamp(timeFormat_techanimGeo.st_mtime).strftime('%c')+"/ grm - "+datetime.fromtimestamp(timeFormat_jsn.st_mtime).strftime('%c')+"]"
                else:
                    grm_asset_items="None"      
                    comment_partial = "For: "+SHOT+" / "+pl_getitle+":\nCFX Export using Anim: "+ curves_ver +" '"+str(mas_comment)+"', animRig "+animrig +", midmodel "+modver+", techanim abc: ("+pl_getitle+" "+getgeover+" using techrig: "+tech_rig+"), techanim comment: '" +techanimCm+"' TA saved from: ("+workFile  +")\n[geo - "+datetime.fromtimestamp(timeFormat_techanimGeo.st_mtime).strftime('%c')+"]"
                comment.append(comment_partial)
            # return mas_comment, curves_ver, timeLine, workFile, animrig, grm_ver, workFile, getgrver, gr_workFile, getgeover, techanimCm, pl_getitle, comment, timeFormat, grm_asset_items
        return comment


    def save_pub_asset_info(self,asset_dict):
        PROJECT = os.getenv("M_JOB")
        SCENE = os.getenv("M_SEQUENCE")
        SHOT = os.getenv("M_LEVEL")
        DEPT = os.getenv("M_TASK")           
        path_build='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/scenes/pub_MSG/'
        getcomments = self.create_pub_info(asset_dict)
        gettime=strftime("%Y_%m_%d_%H%M%S", gmtime())
        save_name = "AN_cfx_"+ gettime
        if not os.path.exists(path_build): os.makedirs(path_build)
        file_path_build=path_build+save_name+'.txt'
        inp = open(file_path_build, 'w+')
        for each in getcomments:
            inp.write(str(each))
            inp.write('\n')
            print str(each)         
        inp.close()  
        print "saving text file: "+save_name+" in "+path_build


    def _print_saved_asset_info(self):
        PROJECT = os.getenv("M_JOB")
        SCENE = os.getenv("M_SEQUENCE")
        SHOT = os.getenv("M_LEVEL")
        DEPT = os.getenv("M_TASK")           
        path_build='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/scenes/pub_MSG/'        
        get_items_txt = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(path_build) for name in files if name.lower().endswith(".txt")]
        latest_file = max(get_items_txt, key=os.path.getctime)
        timeFormat=os.stat(os.path.join(path_build, latest_file))         
        if os.path.exists(path_build):
            List = open(latest_file).readlines()
            for aline in List:
                print aline
                print str(latest_file.split('/')[-1])+" made at "+datetime.fromtimestamp(timeFormat.st_mtime).strftime('%c') 

    def _open_asset_info(self):     
        getcommentfolder = '/jobs/'+_project+'/'+_scene+'/'+_shot+'/TASKS/'+_dept_task+'/maya/scenes/pub_MSG/'
        if os.path.exists(getcommentfolder):
            path_build='/jobs/'+_project+'/'+_scene+'/'+_shot+'/TASKS/'+_dept_task+'/maya/scenes/pub_MSG/'
        else:
            path_build='/jobs/'+_project+'/'+_scene+'/'+_shot+'/TASKS/anim/maya/scenes/pub_MSG/'
        get_items_txt = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(path_build) for name in files if name.lower().endswith(".txt")]
        try:
            latest_file = max(get_items_txt, key=os.path.getctime)
            pass
        except:
            print "something went wrong"
            return
        subprocess.Popen('gedit "%s"' % latest_file, stdout=subprocess.PIPE, shell=True)

    def _open_defined_path(self): 
        PROJECT = os.getenv("M_JOB")
        SCENE = os.getenv("M_SEQUENCE")
        SHOT = os.getenv("M_LEVEL")
        DEPT = os.getenv("M_TASK")
        if PROJECT == None and SCENE == None and SHOT == None and DEPT == None:
            print "need to mss into shot"
            return
        else:
            pass
        path_build='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/scenes/pub_MSG/'
        if os.path.exists(path_build):
            os.system('xdg-open "%s"' % path_build) 
        else:
            print "This shot hasn't had a message saved for it yet. Please use 'save pubbed asset info' to build the file"
            return



    def _print_verbose(self,asset_dict): 
        get_top_groom = "techanim fur NA"
        grm_ver = "--"      
        PROJECT = os.getenv("M_JOB")
        SCENE = os.getenv("M_SEQUENCE")
        SHOT = os.getenv("M_LEVEL")
        DEPT = os.getenv("M_TASK")          
        mas_comment = None
        comment = []
        grm_asset_true=False
        _get_TAV_folder='/jobs/' + PROJECT + '/' + SCENE + '/' + SHOT + '/PRODUCTS/instances/'
        #groom techanim version
        _get_partial_folder='/jobs/' + PROJECT + '/' + SCENE + '/' + SHOT + '/PRODUCTS/instances/'
        commentData = []
        for each in asset_dict:
            gr_workFile = "Groom autogen"
            tech_rig = "null"
            techanimCm = "null"
            curves_ver = "null"
            timeLine = "null"
            workFile = "null"
            animrig = "null"        
            modver = "null"       
            gr_pubnote = "null"          
            Rtf_text = each[0].text()
            Temp_Obj = QtGui.QTextEdit()
            Temp_Obj.setText(Rtf_text)
            pl_getitle = Temp_Obj.toPlainText()
            pl_getitle = str(pl_getitle)
            getgeover = each[1][0].currentText()
            getgeover = str(getgeover)
            getgrver = each[1][1].currentText()
            getgrver = str(getgrver)
            getsuch=_get_partial_folder+pl_getitle+'/'+DEPT+'/'+getgeover+'/'
            getsuch=str(getsuch)
            try:
                get_yaml_item = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(getsuch) for name in files if name.lower().endswith(".yaml")][0]   
                print '\n'
                print pl_getitle+' techanim: '+get_yaml_item 
                print '\n'  
                timeFormat=os.stat(get_yaml_item) 
                print "' - This was set at: "+datetime.fromtimestamp(timeFormat.st_mtime).strftime('%c') 
                print '\n'                         
            except:
                if "_groom" not in pl_getitle:
                    pl_new_getitle = pl_getitle.split("_groom")[0]
                    print "It's possible the current version publish of "+pl_new_getitle+" ta:"+getgeover+" gr:"+getgrver+" has not finished publishing, failed OR was depreciated. Setting dependencies to anim's"
                    get_anim=_get_partial_folder+pl_new_getitle+'/anim/'
                else:
                    pl_new_getitle = pl_getitle
                    print "Groom from techanim present only. Setting geo dependencies to anim's"
                    get_anim=_get_partial_folder+pl_new_getitle.split("_groom")[0]+'/anim/'
                get_yaml_item = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(get_anim) for name in files if name.lower().endswith(".yaml")]
                get_yaml_item=max(get_yaml_item)
                print pl_getitle+' anim: '+str(get_yaml_item)
                print '\n'
                timeFormat=os.stat(get_yaml_item) 
                print "' - This was set at: "+datetime.fromtimestamp(timeFormat.st_mtime).strftime('%c') 
                print '\n'  
            get_item = []
            get_items = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(_get_TAV_folder) for name in files if name.lower().endswith(".yaml") and "anim" in name]
            # print get_items
            if "null" in curves_ver:
                print "anim ver can't be found in your published asset file for "+pl_getitle+". defaulting to latest"
                get_item=max(get_items)
                print pl_getitle+' anim: '+get_item
                print '\n'
                timeFormat=os.stat(get_item) 
                print "' - This was set at: "+datetime.fromtimestamp(timeFormat.st_mtime).strftime('%c') 
                print '\n'                  
            else:
                # print curves_ver
                try:
                    # get_item = [(item) for item in get_items for name in files if curves_ver in item][0]  
                    get_item = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(_get_TAV_folder) for name in files if name.lower().endswith(".yaml") and "anim" in name and curves_ver in dirpath][0]
                    print pl_getitle+' anim: '+get_item
                    print '\n'
                    timeFormat=os.stat(get_item) 
                    print "' - This was set at: "+datetime.fromtimestamp(timeFormat.st_mtime).strftime('%c') 
                    print '\n'                    
                except:
                    curves_ver = curves_ver
                # print get_item
            #get groom asset info
            if len(getgrver)>0:
                if "groom" in pl_getitle:
                    each_grm_item = pl_getitle
                else:
                    each_grm_item = pl_getitle+'_groom'
                findLatestGroom=_get_partial_folder+each_grm_item+'/'+DEPT+'/'+getgrver+'/'
                findLatestGroom=str(findLatestGroom)
                try:
                    get_jsn_item = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(findLatestGroom) for name in files if name ==".pubInfo.json"][0]
                    print '\n'
                    print pl_getitle+' groom: '+get_jsn_item
                    print '\n'
                    timeFormat=os.stat(get_jsn_item) 
                    print "' - This was set at: "+datetime.fromtimestamp(timeFormat.st_mtime).strftime('%c') 
                    print '\n'
                except:
                    print "ERROR: A JSON HAS NOT BEEN GENERATED FOR : "+pl_getitle+" groom version: "+getgrver+". Please check if this publish has finished."


