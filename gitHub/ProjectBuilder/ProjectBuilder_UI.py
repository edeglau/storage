
import os, PyQt4, sys, glob, shutil
import getpass
import webbrowser
#import win32clipboard
from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtCore import SIGNAL
#from PyQt4.QtGui import *
from PyQt4.QtGui import QWidget, QGridLayout, QLabel, QKeySequence, QPushButton, QClipboard, QCheckBox, QHBoxLayout, \
QPixmap, QLineEdit, QListWidget, QTextEdit, QComboBox
import re
getUser=getpass.getuser()

'''Pipeliner'''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons License'
'http://creativecommons.org/licenses/by-sa/3.0/au/'

DummyFolder=r"C:\\temp\\"
ProjectMain=r'G:\\CURRENT PROJECTS\\'
ProjectMasterFolder=ProjectMain
# dummyfolder="C:\\temp\\CURRENT PROJECTS\\LA0095_Polly_Pocket\\_Assets\\00_Maya\\"
mayaFolder='\\_Assets\\00_Maya\\'
# defaultImage=r'\\rb_main\\common\\TechArt\\Templates\\Placeholder_Templates\\Placeholder_Grad.png'

filepath= os.getcwd()
sys.path.append(str(filepath))

Type=["Pick Asset Type", "Episodic", "Series"]
Asset=["Pick Category", "01_Characters", "02_Props", "03_Sets", "04_FX", "05_Lighting"]

ProductionFolders=["Master", "Working"]

ProductionSubFolders=["Anim\scenes", "Mesh\scenes\sourceimages", "Mesh\scenes\Resources","Mesh\scenes\Reviews","Mesh\scenes\Images","Previz\scenes", "Rig\scenes", "Shaders\scenes"]
class fileFolderRenamerCreater(QtGui.QMainWindow):
    
    '''==========================================================================================================================================
    GUI Class.
    =========================================================================================================================================='''
    
    def __init__(self):
        '''----------------------------------------------------------------------------------------------------------------------------------
        GUI Window
        ----------------------------------------------------------------------------------------------------------------------------------'''
        QtGui.QMainWindow.__init__(self)       

        self.resize(600, 100)
        self.setWindowTitle("Renamer")
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QGridLayout(self.central_widget)

        '''----------------------------------------------------------------------------------------------------------------------------------
        Layout of the GUI.
        ----------------------------------------------------------------------------------------------------------------------------------'''      
        self.window_layer_01 = QGridLayout()
        self.main_layout.addLayout(self.window_layer_01, 0, 0, 1, 1)           
        self.window_layer_02 = QGridLayout()
        self.main_layout.addLayout(self.window_layer_02, 1, 0, 1, 1)   
        self.window_layer_03 = QGridLayout()
        self.main_layout.addLayout(self.window_layer_03, 2, 0, 1, 1)
        self.window_layer_04 = QGridLayout()
        self.main_layout.addLayout(self.window_layer_04, 3, 0, 1, 1)
        self.window_layer_05 = QGridLayout()
        self.main_layout.addLayout(self.window_layer_05, 4, 0, 1, 1)
        self.window_layer_05 = QGridLayout()
        self.main_layout.addLayout(self.window_layer_05, 5, 0, 1, 1)
        self.window_layer_06 = QGridLayout()
        self.main_layout.addLayout(self.window_layer_06, 6, 0, 1, 1)
        self.window_layer_07 = QGridLayout()
        self.main_layout.addLayout(self.window_layer_07, 7, 0, 1, 1)        

        self.window_column_02 =QHBoxLayout()
        self.main_layout.addLayout(self.window_column_02, 4, 1, 1, 1) 
        self.window_column_03 =QHBoxLayout()
        self.main_layout.addLayout(self.window_column_03, 2, 1, 1, 1)            
        self.window_column_04 =QHBoxLayout()        
        self.main_layout.addLayout(self.window_column_04, 3, 1, 1, 1)

        '''----------------------------------------------------------------------------------------------------------------------------------
        Widgets
        ----------------------------------------------------------------------------------------------------------------------------------'''  

        self.asset_name_label_01 = QLabel("Project")
        self.asset_name_label_01.setMinimumWidth(70)
        self.asset_name_label_01.setMaximumWidth(70)
        self.window_layer_02.addWidget(self.asset_name_label_01, 0, 0, 1, 1)         
        
        self.project_name_folder = QComboBox()
        self.project_name_folder.setMinimumWidth(200)
        self.project_name_folder.setMaximumWidth(200)
        self.window_layer_02.addWidget(self.project_name_folder, 0, 1, 1, 1)
        srcfileName = os.listdir(ProjectMasterFolder)
        getFolders=[(each) for each in srcfileName if "." not in each]
        firstPick=["Pick Project"]
        self.project_name_folder.addItems(firstPick)
        self.project_name_folder.addItems(getFolders)

        self.asset_name_label_01 = QLabel("AssetName")
        self.asset_name_label_01.setMinimumWidth(70)
        self.asset_name_label_01.setMaximumWidth(70)
        self.window_layer_02.addWidget(self.asset_name_label_01, 0, 2, 1, 1) 

        
        self.asset_name_field_01 = QtGui.QLineEdit()
        self.asset_name_field_01.setText("")
        self.asset_name_field_01.setMinimumHeight(25)
        self.asset_name_field_01.setMaximumHeight(50) 
        self.asset_name_field_01.setMinimumWidth(100)
        self.asset_name_field_01.setMaximumWidth(100)
        self.window_layer_02.addWidget(self.asset_name_field_01, 0, 3, 1, 1)      
        
        self.asset_label = QLabel("Category")
        self.asset_label.setMinimumWidth(120)
        self.asset_label.setMaximumWidth(120)
        self.window_layer_02.addWidget(self.asset_label, 0, 4, 1, 1) 

        self.asset_dropdown_01 = QComboBox()
        self.asset_dropdown_01.setMinimumWidth(120)
        self.asset_dropdown_01.setMaximumWidth(120)
        self.window_layer_02.addWidget(self.asset_dropdown_01, 0, 5, 1, 1)
        self.asset_dropdown_01.addItems(Asset)
        #self.populateSequence(spinner=self.asset_dropdown_01)
        #self.asset_dropdown_01.currentIndexChanged[str].connect(self.on_langComboBox_IndexChanged)

        self.type_label = QLabel("Type")
        self.type_label.setMinimumWidth(120)
        self.type_label.setMaximumWidth(120)
        self.window_layer_02.addWidget(self.type_label, 0, 6, 1, 1) 

        self.type_dropdown_01 = QComboBox()
        self.type_dropdown_01.setMinimumWidth(120)
        self.type_dropdown_01.setMaximumWidth(120)
        self.window_layer_02.addWidget(self.type_dropdown_01, 0, 7, 1, 1)
        self.type_dropdown_01.addItems(Type)
        #self.populateSequence(spinner=self.type_dropdown_01)
        #self.type_dropdown_01.currentIndexChanged[str].connect(self.on_langComboBox_IndexChanged)

        self.ep_name_label = QLabel("Episode")
        self.ep_name_label.setMinimumWidth(70)
        self.ep_name_label.setMaximumWidth(70)
        self.window_layer_02.addWidget(self.ep_name_label, 0, 8, 1, 1) 
        
        self.ep_name_field = QtGui.QLineEdit()
        self.ep_name_field.setText("802")
        self.ep_name_field.setMinimumHeight(25)
        self.ep_name_field.setMaximumHeight(50) 
        self.ep_name_field.setMinimumWidth(100)
        self.ep_name_field.setMaximumWidth(100)
        self.window_layer_02.addWidget(self.ep_name_field, 0, 9, 1, 1)     

  
   
        self.dest_label_01 = QLabel("new path:")
        self.dest_label_01.setMinimumWidth(100)
        self.dest_label_01.setMaximumWidth(100)
        self.window_layer_05.addWidget(self.dest_label_01, 0, 0, 1, 1) 
        
        self.dest_folder_field_01 = QtGui.QLineEdit()
        self.dest_folder_field_01.setText(mayaFolder)        
        #self.dest_folder_field_01.setText(mayaFolder)        
        self.dest_folder_field_01.setMinimumHeight(25)
        self.dest_folder_field_01.setMaximumHeight(50) 
        self.dest_folder_field_01.setMinimumWidth(450)
        self.dest_folder_field_01.setMaximumWidth(450)
        self.window_layer_05.addWidget(self.dest_folder_field_01, 0, 1, 1, 1) 


        self.get_src_button = QPushButton("refresh")
        self.get_src_button.setMinimumHeight(25)

        self.get_dest_button = QPushButton("refresh")
        self.get_dest_button.setMinimumHeight(25)
        self.get_dest_button.setMaximumHeight(50) 
        self.get_dest_button.setMinimumWidth(100)
        self.get_dest_button.setMaximumWidth(100)
        self.connect(self.get_dest_button, SIGNAL('clicked()'), self._refresh)
        self.window_layer_05.addWidget(self.get_dest_button, 0, 4, 1, 1)   
        
        self.get_src_button = QPushButton("open folder")
        self.get_src_button.setMinimumHeight(25)

        self.get_dest_button = QPushButton("open folder")
        self.get_dest_button.setMinimumHeight(25)
        self.get_dest_button.setMaximumHeight(50) 
        self.get_dest_button.setMinimumWidth(100)
        self.get_dest_button.setMaximumWidth(100)
        self.connect(self.get_dest_button, SIGNAL('clicked()'), self._open_destination)
        self.window_layer_05.addWidget(self.get_dest_button, 0, 5, 1, 1)   

        self.do_it_buttton = QPushButton("Create!")
        self.do_it_buttton.setMinimumHeight(25)
        self.do_it_buttton.setMaximumHeight(50) 
        self.do_it_buttton.setMinimumWidth(100)
        self.do_it_buttton.setMaximumWidth(150)
        #self.do_it_buttton.clicked.connect(self._start)
        self.connect(self.do_it_buttton, SIGNAL('clicked()'), self._operation)
        self.window_layer_06.addWidget(self.do_it_buttton, 0, 0, 1, 1)   

################################################
#     def on_comboBoxParent_currentIndexChanged(self, index):
#         '''----------------------------------------------------------------------------------------------------------------------------------
#         Once the source sequence is chosen, 
#         this will populate the source shot spinner
#         ----------------------------------------------------------------------------------------------------------------------------------'''   
#         sourceSequence=self.sourceSequenceSpinner
#         getText=sourceSequence.currentText()
#         sourceShot=self.sourceShotSpinner
#         shotContainer=self._getShotFolder(getText)
#         shotContainer.append('')
#         shotContainer.reverse()
#         noshow="select sequence"
#         sourceShot.clear()
#         sourceShot.addItems(shotContainer)
# 
#     def deston_comboBoxParent_currentIndexChanged(self, index):
#         '''----------------------------------------------------------------------------------------------------------------------------------
#         Once the destination sequence is chosen, 
#         this will populate the destination shot spinner
#         ----------------------------------------------------------------------------------------------------------------------------------'''   
#         srcfileName=[]   
#         for (root, directories, files) in os.walk(ProjectMasterFolder):
#             for filename in files:
#                 srcfileName.append(filename)   
#         destinationShot=self.destinationSequenceSpinner
#         destinationShot.clear()
#         destinationShot.addItems(srcfileName)
        
              
        
    def _refresh(self):
        Project=self.project_name_folder
        Project=Project.currentText()
        Project=str(Project)        
        Asset=self.asset_dropdown_01
        Asset=Asset.currentText()
        Asset=str(Asset)
        Type=self.type_dropdown_01
        Type=Type.currentText()
        Type=str(Type)
        AssetName=self.asset_name_field_01
        AssetName=AssetName.text()
        AssetName=str(AssetName)        
        Episode=self.ep_name_field
        Episode=Episode.text()
        Episode=str(Episode)        
        destination=self.dest_folder_field_01
        destination=destination.text()
        destination=str(destination)        
        if Project =="Pick Project":
            print "You must assign a project"
            return
        elif len(AssetName)==0:
            print "you must give the asset a name"
            return
        elif Asset =="Pick Category":
            print "You must pick a Category"
            return
        elif Type=="Pick Asset Type":
            print "you much pick an Asset Type"
            return
        elif Type =="Episodic" and len(Episode)==0:
            print "if asset is episodic, you must fill in the episode field"
            return
        else:
            try:
                makeMayaFile=AssetName.split("_")[1]
            except:
                print "AssetName does not have a number assigned. Please give it a number EG:'01_'"   
                return         
            if Type=="Episodic":
                folderPath=ProjectMasterFolder+Project+mayaFolder+Asset+"\\"+Type+"\\"+Episode+"\\"+AssetName+"\\"
                self.dest_folder_field_01.setText(folderPath)
            elif Type=="Series":
                folderPath=ProjectMasterFolder+Project+mayaFolder+Asset+"\\"+Type+"\\"+AssetName+"\\"
                self.dest_folder_field_01.setText(folderPath)        
                
                
                
    def _open_destination(self):
        dest_field_01=self.dest_folder_field_01
        destImagePath=dest_field_01.text()
        destImagePath=str(destImagePath)
        self.get_path(destImagePath)  
                        
    def get_path(self, path):
        try:
            if '\\\\' in path:
                newpath=re.sub(r'\\\\',r'\\', path)
                os.startfile(r'\\'+newpath[1:])    
            else:
                os.startfile(path)
        except:
            print "cannot open path. check if it exists"
            return
            
    def _operation(self):
        Project=self.project_name_folder
        Project=Project.currentText()
        Project=str(Project)         
        Asset=self.asset_dropdown_01
        Asset=Asset.currentText()
        Asset=str(Asset)
        Type=self.type_dropdown_01
        Type=Type.currentText()
        Type=str(Type)
        AssetName=self.asset_name_field_01
        AssetName=AssetName.text()
        AssetName=str(AssetName)        
        Episode=self.ep_name_field
        Episode=Episode.text()
        Episode=str(Episode)        
        destination=self.dest_folder_field_01
        destination=destination.text()
        destination=str(destination)        
        if Project =="Pick Project":
            print "You must assign a project"
            return
        elif len(AssetName)==0:
            print "you must give the asset a name"
            return
        elif Asset =="Pick Category":
            print "You must pick a Category"
            return
        elif Type=="Pick Asset Type":
            print "you much pick an Asset Type"
            return
        elif Type =="Episodic" and len(Episode)==0:
            print "if asset is episodic, you must fill in the episode field"
            return
        else:
            try:
                makeMayaFile=AssetName.split("_")[1]
            except:
                print "AssetName does not have a number assigned. Please give it a number EG:'01_Name'"   
                return         
            if Type=="Episodic":
                folderPath=ProjectMasterFolder+Project+mayaFolder+Asset+"\\"+Type+"\\"+Episode+"\\"+AssetName
                for each in ProductionFolders:
                    makeProject=folderPath+"\\"+each
                    for item in ProductionSubFolders:
                        getAssetNameSuf=item.split("\\")[0]                  
                        ProjectBuild=makeProject+"\\"+item
                        newFile="LA0095_"+makeMayaFile+"_"+getAssetNameSuf+".txt"
                        fname = ProjectBuild+"\\"+newFile
                        if not os.path.exists(ProjectBuild): os.makedirs(ProjectBuild)
                        if not fname:
                            inp=open(fname, 'w+')
                            inp.write("hi"+'\r\n')
                            inp.close()
                            thisFile = fname
                            base = os.path.splitext(thisFile)[0]
                            os.rename(thisFile, base + ".ma")
                            print fname+" has been created"  
                        else:
                            pass                       
            else:
                folderPath=ProjectMasterFolder+Project+mayaFolder+Asset+"\\"+Type+"\\"+AssetName
                for each in ProductionFolders:
                    makeProject=folderPath+"\\"+each
                    for item in ProductionSubFolders:
                        getAssetNameSuf=item.split("\\")[0]
                        ProjectBuild=makeProject+"\\"+item
                        newFile="LA0095_"+makeMayaFile+"_"+getAssetNameSuf+".txt"
                        fname = ProjectBuild+"\\"+newFile
                        if not os.path.exists(ProjectBuild): os.makedirs(ProjectBuild)
                        if not fname:
                            inp=open(fname, 'w+')
                            inp.write("hi"+'\r\n')
                            inp.close()
                            thisFile = fname
                            base = os.path.splitext(thisFile)[0]
                            os.rename(thisFile, base + ".ma")
                            print fname+" has been created"  
                        else:
                            pass         
    def copying(self, root, filename, filepath, dstfolderPath):  
        for each in filename:
            filepath = os.path.join(root, each)
            shutil.copy(filepath, dstfolderPath)
            
    def renaming(self, root, filename, oldNamePart, newNamePart):
        for each in filename:
            filepath = os.path.join(root, each)
            print filepath
            os.rename(filepath, filepath.replace(oldNamePart, newNamePart))
#     def on_langComboBox_IndexChanged(self):
#         '''----------------------------------------------------------------------------------------------------------------------------------
#         This changes the functions of the interface dependent on whether language has been selected
#         ----------------------------------------------------------------------------------------------------------------------------------'''            
#         interfaceWidgetsAccess=[self.size_field_01,
#                                 self.r_field_01, 
#                                 self.g_field_01, 
#                                 self.b_field_01, 
#                                 self.textMode, 
#                                 self.imageMode,
#                                 self.source_folder_field_01, 
#                                 self.source_button, 
#                                 self.source_dropdown_01,
#                                 self.number_field_01,
#                                 self.suf_name_field_01,
#                                 self.format_name_field_01,
#                                 self.srcImage_field_01
#                                 ]
#         langDrop=self.lang_dropdown_01
#         languageType=langDrop.currentText()        
#         getSrcWidget=self.source_folder_field_01
#         srcFolderStuff=self.source_dropdown_01 
#         if languageType!="none":           
#             if languageType =="ES":
#                 langIndex="Placeholder_ES.png"
#                 self.language_lock_down(langIndex, interfaceWidgetsAccess)
#             elif languageType=="ZH":
#                 langIndex="Placeholder_ZH.png"
#                 self.language_lock_down(langIndex, interfaceWidgetsAccess)             
#             elif languageType=="FR":
#                 langIndex="Placeholder_FR.png"
#                 self.language_lock_down(langIndex, interfaceWidgetsAccess)
#         else:
#             for eachWidget in  interfaceWidgetsAccess:
#                 eachWidget.setEnabled(True)            
#             self.dest_field_01.setText(dummyfolder)
#             self.source_folder_field_01.clear()
#             self.source_folder_field_01.setText(mayaFolder)
#             self.r_field_01.setText(redColour)
#             self.g_field_01.setText(greenColour)
#             self.b_field_01.setText(blueColour)
#             getIndex=srcFolderStuff.findText(defaultImage)
#             srcFolderStuff.setCurrentIndex(getIndex) 



    def error(self):
        print "name required to change"

def main():
    app = QtGui.QApplication(sys.argv)
    showWindow =  fileFolderRenamerCreater()
    showWindow.show()
    sys.exit(app.exec_())
    #embed.App.getTheApp().exec_()
    
if __name__ == "__main__":
    main()
    

# for fleName in glob.glob(os.path.join(folderPath, "*"+oldNamePart+"*")): 
#     os.rename(fleName, fleName.replace(oldNamePart, newNamePart)) 
