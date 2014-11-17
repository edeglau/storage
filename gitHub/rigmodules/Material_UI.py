import maya.cmds as cmds
from functools import partial
from string import *
import re, os, subprocess
import maya.mel
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons License'
'http://creativecommons.org/licenses/by-sa/3.0/au/'

photoshop = r"C:\\Program Files\\Adobe\\Adobe Photoshop CC 2014\\Photoshop.exe"
gimp="C:\\Program Files\\GIMP 2\\bin\\gimp-2.8.exe"
getScenePath=cmds.file(q=1, location=1)
getPathSplit=getScenePath.split("/")
folderPath='\\'.join(getPathSplit[:-1])+"\\"
class Mat_Namer(object):
    '''--------------------------------------------------------------------------------------------------------------------------------------
    Interface Layout
    --------------------------------------------------------------------------------------------------------------------------------------'''          
    def __init__(self, winName="Material ID"):
        self.winTitle = "MaterialID"
        self.winName = winName
    def create_MATID_win(self, winName="MaterialID"):
        global colMenu
        if cmds.window(self.winName, exists=True):
                cmds.deleteUI(self.winName)

        self.window = cmds.window(self.winName, title=self.winTitle, tbm=1, w=300, h=250 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=300)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        
        cmds.rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))
        colMenu=cmds.optionMenu( label='ID')
        cmds.menuItem( label='Skin' )
        cmds.menuItem( label='Eye' )
        cmds.menuItem( label='Spec' )
        cmds.menuItem( label='Lash' )
        cmds.menuItem( label='Brows' )    
        cmds.menuItem( label='Hair' )        
        cmds.menuItem( label='Mouth' )        
        cmds.menuItem( label='Other' )    
        cmds.menuItem( label='Costume' )             
        cmds.button (label='Mat ID', p='listBuildButtonLayout', command = self._add_id)
        cmds.button (label='Add CH Pref', p='listBuildButtonLayout', command = self._add_pref)
        cmds.button (label='Add type Suf', p='listBuildButtonLayout', command = self._add_suf)
        cmds.button (label='ShadeNetworkSel', p='listBuildButtonLayout', command = self._shade_network)
        cmds.button (label='selectMissingID', p='listBuildButtonLayout', command = self._select_nonID)
        cmds.button (label='vray gamma', p='listBuildButtonLayout', command = self._vray_gamma)     
        cmds.button (label='FTM', p='listBuildButtonLayout', command = self._file_texture_manager)     
        cmds.button (label='Open work folder', p='listBuildButtonLayout', command = self._open_work_folder) 
        cmds.button (label='Open texture folder', p='listBuildButtonLayout', command = self._open_texture_folder)   
        cmds.button (label='Open Image in PS', p='listBuildButtonLayout', command = self._open_texture_file_ps)  
        cmds.button (label='Open Image in Gimp', p='listBuildButtonLayout', command = self._open_texture_file_gmp) 

        cmds.showWindow(self.window)
    def _file_texture_manager(self, arg=None):
        maya.mel.eval( "FileTextureManager;" )
    def _open_texture_file_ps(self, arg=None):
        try:
            selObj=cmds.ls(sl=1, fl=1)[0]
            pass
        except:
            print "nothing selected"
        getNodeType=cmds.nodeType(selObj)
        if getNodeType=="file":
            Attr=cmds.listAttr(selObj)
            for each in Attr:
                if "fileTextureName" in each and "Pattern" not in each:
                    getValue=cmds.getAttr(selObj+'.'+each)   
                    getpath=getValue.split("/")
                    getpPath="\\".join(getpath[:-1])
                    getFile=getpath[-1:]
                    getValue=getpPath+"\\"+getFile[0]
                    getValue = r"%s"%getValue           
                    subprocess.Popen([photoshop, getValue])
        else:
            print "need to select a texture node"
    def _open_texture_folder(self, arg=None):
        try:
            selObj=cmds.ls(sl=1, fl=1)[0]
            pass
        except:
            print "nothing selected"
            return
        getNodeType=cmds.nodeType(selObj)
        if getNodeType=="file":
            Attr=cmds.listAttr(selObj)
            for each in Attr:
                if "fileTextureName" in each and "Pattern" not in each:
                    getValue=cmds.getAttr(selObj+'.'+each)  
                    getpath=getValue.split("/")
                    getpPath="\\".join(getpath[:-1])+"\\"
                    print getpPath
                    self.get_path(getpPath)
        else:
            print "need to select a texture node"
    def _open_work_folder(self, arg=None):
        destImagePath=folderPath
        print destImagePath
        self.get_path(destImagePath)  
    def get_path(self, path):
        print path
        if '\\\\' in path:
            newpath=re.sub(r'\\\\',r'\\', path)
            os.startfile(r'\\'+newpath[1:])    
        else:
            os.startfile(path)            
    def _open_texture_file_gmp(self, arg=None):
        try:
            selObj=cmds.ls(sl=1, fl=1)[0]
            pass
        except:
            print "nothing selected"
            return
        getNodeType=cmds.nodeType(selObj)
        if getNodeType=="file":
            Attr=cmds.listAttr(selObj)
            for each in Attr:
                if "fileTextureName" in each and "Pattern" not in each:
                    getValue=cmds.getAttr(selObj+'.'+each)   
                    subprocess.Popen([gimp, getValue])
        else:
            print "need to select a texture node"
    def _add_id(self, arg=None):
        '''----------------------------------------------------------------------------------
        Common add to list function
        ----------------------------------------------------------------------------------'''  
        queryColor=cmds.optionMenu(colMenu, q=1, sl=1)
        if queryColor==1:
            color=int(1)      
        elif queryColor==2:
            color=int(6)  
        elif queryColor==3:
            color=int(7)
        elif queryColor==4:
            color=int(8)
        elif queryColor==5:
            color=int(9)
        elif queryColor==6:
            color=int(10  ) 
        elif queryColor==7:
            color=int(16)
        elif queryColor==8:
            color=int(20)
        elif queryColor==9:
            color=int(30)
        selObj=cmds.ls(sl=1)
        for each in range(len(selObj)):
            try:
                cmds.vray("addAttributesFromGroup", selObj[each], "vray_material_id", 1)
            except:
                pass
            try:
                cmds.setAttr (selObj[each]+".vrayMaterialId", color+each)
            except:
                pass        
            
    def _vray_gamma(self, arg=None):
        selObj=cmds.ls(sl=1)
        for each in selObj:
            getNodeType=cmds.nodeType(each)
            if getNodeType=="file":           
                try:
                    cmds.vray("addAttributesFromGroup", each, "vray_file_gamma", 1)
                except:
                    pass       

    def _add_suf(self, arg=None):
        selObj=cmds.ls(sl=1)
        for each in selObj:
            getNode=cmds.nodeType(each)
            if "shadingEngine" in getNode:
                getNode="SG"
            elif "VRay" in getNode or "phong" in getNode or "blinn" in getNode:
                getNode="Shader"
            elif "file" in getNode:
                getNode="FileTexture"
            else:
                getNode=getNode
            if getNode not in each:
                getnewname=each+'_'+getNode
                cmds.rename(each, getnewname)
                
                
    def _shade_network(self, arg=None):
        selObj=cmds.ls(sl=1)[0]
        cmds.hyperShade(selObj, smn=1)
        maya.mel.eval('hyperShadePanelGraphCommand("hyperShadePanel1", "showUpAndDownstream");')
            
    def _add_pref(self, arg=None):
        selObj=cmds.ls(sl=1)        
        getMeshController=cmds.ls("Mesh")[0]
        getChildrenController=cmds.listRelatives(getMeshController, c=1, typ="transform")[0]
        cutName=getChildrenController.split("_")[0:2]
        getNewName='_'.join(cutName)
        for each in selObj:
            if getNewName not in each:
                getnewname=getNewName+'_'+each
                cmds.rename(each, getnewname)
    def _select_nonID(self, arg=None):
        try:
            selObj=cmds.ls(sl=1, fl=1)
            pass
        except:
            print "nothing selected"  
        Attr=[(each) for each in selObj if "vrayMaterialId" not in cmds.listAttr(each)]    
        if Attr:
            cmds.select(Attr[0])            
            for each in Attr[1:]:
                cmds.select(each, add=1)
        else:
            print "no missing material ID"


inst = Mat_Namer()
inst.create_MATID_win()