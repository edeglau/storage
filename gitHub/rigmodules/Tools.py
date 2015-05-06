import maya.cmds as cmds
from functools import partial
from string import *
import re
import maya.mel
import os, subprocess, sys, platform, logging, signal, webbrowser, urllib, re, getpass, datetime
from os  import popen
from sys import stdin
import subprocess
import os
import random
from random import randint
from pymel.core import *
#import win32clipboard
import operator
from sys import argv
from datetime import datetime
from operator import itemgetter

OSplatform=platform.platform()
getFolderName=getpass.getuser()

trans=[".tx", ".ty", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz"]  

'''MG rigging tool functions'''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons License'
'http://creativecommons.org/licenses/by-sa/3.0/au/'

photoshop = r"C:\\Program Files\\Adobe\\Adobe Photoshop CC 2014\\Photoshop.exe"
gimp="C:\\Program Files\\GIMP 2\\bin\\gimp-2.6.exe"


BbxName="eyeDirGuide"
BbxFilepath="G:\\_PIPELINE_MANAGEMENT\\Published\\maya\\"+BbxName+".ma"


scriptPath="//usr//people//elise-d//workspace//techAnimTools//personal//elise-d//rigModules"
sys.path.append(str(scriptPath))



getBasePath=str(scriptPath)+"/baseFunctions_maya.py"
exec(open(getBasePath))
getBaseClass=BaseClass()




from inspect import getsourcefile
from os.path import abspath

getfilePath=str(abspath(getsourcefile(lambda _: None)))
print getfilePath
if "Windows" in OSplatform:
    gtepiece=getfilePath.split("\\")
if "Linux" in OSplatform: 
    gtepiece=getfilePath.split("/")  
# gtepiece=getfilePath.split("/")
getRigModPath='/'.join(gtepiece[:-2])+"/rigModules"

# basepath=str(getRigModPath)+"/baseFunctions_maya.py"
# exec(open(basepath))
# getClass=BaseClass()

# exec(open('//usr//people//elise-d//workspace//sandBox//rigModules//baseFunctions_maya.py'))
# getClass=BaseClass()

# stretchIKpath=str(getRigModPath)+"/stretchIK.py"
# exec(open(stretchIKpath))
# getIKClass=stretchIKClass()

gtepiece=getfilePath.split("/")
getguideFilepath='/'.join(gtepiece[:-2])+"/guides/"
sys.path.append(str(getguideFilepath))


getrenamerFilepath='/'.join(gtepiece[:-2])+"/renamer/"
sys.path.append(str(getrenamerFilepath))

getValueFilepath='/'.join(gtepiece[:-2])+"/Values/"
sys.path.append(str(getValueFilepath))

getSelArrayPath='/'.join(gtepiece[:-2])+"/selectArray/"
sys.path.append(str(getSelArrayPath))

getSSDArrayPath='/'.join(gtepiece[:-2])+"/SSD/"
sys.path.append(str(getSSDArrayPath))

getToolArrayPath='/'.join(gtepiece[:-2])+"/tools/"
sys.path.append(str(getToolArrayPath))


class ToolFunctions(object):
               
    def list_array(self, titleName, windowName, listBuildLayout, listLayout, windowColumnLayout, listName):
        '''--------------------------------------------------------------------------------------------------------------------------------------
        This is a list array interface. Intended interface addon
        --------------------------------------------------------------------------------------------------------------------------------------'''  
        self.listCountLabel=cmds.text (label='Selection list', p=listBuildLayout)             
        cmds.gridLayout(listLayout, p=windowColumnLayout, numberOfColumns=1, cellWidthHeight=(600, 200))       
        self.nodeList=cmds.textScrollList(listName, numberOfRows=8, ra=1, allowMultiSelection=True, sc=self.list_item_selectability, io=True, w=550, h=300, p=listLayout)            
        cmds.gridLayout('calcButtonLayout', p=windowColumnLayout, numberOfColumns=10, cellWidthHeight=(40, 20))
        cmds.button (label='clr', p='calcButtonLayout', command = lambda *args:self._clear_list())
        cmds.button (label='+', p='calcButtonLayout', command = lambda *args:self._add_selected_to_list(listArray=cmds.textScrollList(self.nodeList, q=1, ai=1)))
        cmds.button (label='-', p='calcButtonLayout', command = lambda *args:self._remove_from_list(selectedListItems=cmds.textScrollList(self.nodeList, q=1, selectItem=1)))
        cmds.button (label='><', p='calcButtonLayout', ann='swap out selected in list with selected in scene', command = lambda *args:self._swap_with_selected(selectedListItems=cmds.textScrollList(self.nodeList, q=1, selectItem=1),listArray=cmds.textScrollList(self.nodeList, q=1, ai=1)))
        cmds.button (label='sel all', p='calcButtonLayout', w=50, ann='select all', command = lambda *args:self._select_all_in_list(listArray=cmds.textScrollList(self.nodeList, q=1, ai=1)))
        cmds.button (label='sel- ', p='calcButtonLayout', w=40, ann='select none', command = lambda *args:self._clear_selection())
        cmds.button (label='sort', p='calcButtonLayout', w=40, ann='sort alphabetically-numerally', command = lambda *args:self._sort_list(listArray=cmds.textScrollList(self.nodeList, q=1, ai=1)))
        cmds.button (label='set', p='calcButtonLayout', w=40, ann='create set from selected in list', command = lambda *args:self._make_set_from_selection_list(selectedListItems=cmds.textScrollList(self.nodeList, q=1, selectItem=1)))
        cmds.gridLayout('sep', p=windowColumnLayout, numberOfColumns=2, cellWidthHeight=(600, 20))
        cmds.separator(h=10, p='sep')


    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    
    def _sets_win(self, titleName, windowName, annot):
        '''--------------------------------------------------------------------------------------------------------------------------------------
        This is the sets window interface
        --------------------------------------------------------------------------------------------------------------------------------------'''   
        winName = titleName
        winTitle = winName
        listLayout='setslistLayout'
        rowColumnLayout='windowMenuRow'
        windowColumnLayout='windowMenuColumn'
        listBuildLayout='listBuildLayout'
        listName='mySets'        
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)
        theWindow = cmds.window(winName, title=winTitle, tbm=1, w=600, h=150 )
        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (rowColumnLayout, nr=1, w=600)
        cmds.frameLayout('frameLayout', label='', lv=0, nch=1, borderStyle='out', bv=1, p=rowColumnLayout)
        cmds.rowLayout  ('rowLayout', w=600, numberOfColumns=6, p=rowColumnLayout)
        cmds.columnLayout (windowColumnLayout, p= 'rowLayout')
#         cmds.setParent (windowColumnLayout)
        cmds.separator(h=10, p=windowColumnLayout)
        cmds.gridLayout(listBuildLayout, p=windowColumnLayout, numberOfColumns=1, cellWidthHeight=(600, 20))
        self.getSetTyp=optionMenu( label='SetType', cc=lambda *args:self.change_set(), w=120, ann="Select set type to edit(Dynamic ncloth constraints or Blenshape memberships)")
        menuItem( label="Blendshape sets")
        menuItem( label="Dynamic sets")
        self.setMenu=cmds.optionMenu( label=windowName, ann=annot)
#        for each in getAllSets:
#            cmds.menuItem( label=each)    
        return theWindow    

    def change_set(self):
        '''----------------------------------------------------------------------------------
        ----------------------------------------------------------------------------------''' 
        deformSets=["blendShape", "simpleBlendShape", "cluster"]
        getSetType=optionMenu(self.getSetTyp, q=1, v=1)  
        if getSetType=="Dynamic sets":
            menuItems = cmds.optionMenu(self.setMenu, q=True, ill=True)
            if menuItems:
                cmds.deleteUI(menuItems)             
            getAllSets=[(each) for each in cmds.ls(typ="dynamicConstraint")]
            cmds.optionMenu(self.setMenu, e=1)
            for each in getAllSets:
                cmds.menuItem( label=each)   
        elif getSetType=="Blendshape sets":
            menuItems = cmds.optionMenu(self.setMenu, q=True, ill=True)
            if menuItems:
                cmds.deleteUI(menuItems)             
            getAllSets=[(each) for each in cmds.ls(typ="objectSet") if "tweak" not in each]
            collectBlendSets=[]
            for each in getAllSets:
                try:
                    keepEach=[(connectedObj) for connectedObj in cmds.listConnections(each, s=1) for eachDeform in deformSets if cmds.nodeType(connectedObj) ==eachDeform]
                    if keepEach:
                        collectBlendSets.append(each)
                except:
                    pass
            cmds.optionMenu(self.setMenu, e=1)
            for each in collectBlendSets:
                cmds.menuItem( label=each)


    def _edit_sets_win(self, arg=None):
        '''--------------------------------------------------------------------------------------------------------------------------------------
        This detects all the blendshape sets in a scene to allow easier add and remove for selections
        --------------------------------------------------------------------------------------------------------------------------------------'''   
        titleName="Membership Sets"
        Name="Sets"
        annot="Select vertices and then select set from drop down. Select add to or remove from set"
        theWindow=self._sets_win(titleName, Name, annot)
        self.set_buttons(annot)
        cmds.showWindow(theWindow)
        
    def set_buttons(self, annot):
        '''--------------------------------------------------------------------------------------------------------------------------------------
        blendshape set button interface addon
        --------------------------------------------------------------------------------------------------------------------------------------'''  
        cmds.gridLayout('setBuildButtonLayout', p='windowMenuColumn', numberOfColumns=2, cellWidthHeight=(275, 20))
        cmds.button (label='Add to set', p='setBuildButtonLayout', command = lambda *args:self._add_to_set(querySet=cmds.optionMenu(self.setMenu, q=1, v=1)))
        cmds.button (label='remove from set', p='setBuildButtonLayout', command = lambda *args:self._remove_from_set(querySet=cmds.optionMenu(self.setMenu, q=1, v=1)))

    def _add_to_set(self, querySet):
        '''--------------------------------------------------------------------------------------------------------------------------------------
        This adds the current selection to the current blendshape set membership in the drop down menu
        --------------------------------------------------------------------------------------------------------------------------------------'''
        getSetType=optionMenu(self.getSetTyp, q=1, v=1)  
        getSel=self.selection_grab()
        if getSetType=="Dynamic sets":
            for each in getSel:
                cmds.select(querySet, add=1)
                maya.mel.eval( 'dynamicConstraintMembership "add";' )              
        elif getSetType=="Blendshape sets":   
            if getSel and querySet:
                for each in getSel:
                    cmds.sets(each, add=querySet)
            else:
                print self.default_error()
                return
            
    def _remove_from_set(self, querySet):
        '''--------------------------------------------------------------------------------------------------------------------------------------
        This removes the current selection from the current blendshape set membership in the drop down menu
        --------------------------------------------------------------------------------------------------------------------------------------'''
        getSetType=optionMenu(self.getSetTyp, q=1, v=1)  
        getSel=self.selection_grab()
        if getSetType=="Dynamic sets":
            for each in getSel:
                cmds.select(querySet, add=1)
                maya.mel.eval( 'dynamicConstraintMembership "remove";' )            
        elif getSetType=="Blendshape sets":            
            if getSel and querySet:
                for each in getSel:
                    cmds.sets(each, rm=querySet)
            else:
                print self.default_error()
                return            

            
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
                
    def selection_grab(self):
        '''--------------------------------------------------------------------------------------------------------------------------------------
        Common selection query
        --------------------------------------------------------------------------------------------------------------------------------------'''        
        getSel=cmds.ls(sl=1, fl=1)
        if getSel:
            pass
        else:
            print "You need to make a selection for this tool to operate on."
            return
        return getSel
    
    def default_error(self):
        '''--------------------------------------------------------------------------------------------------------------------------------------
        Common default error prompting user to check script editor for details
        --------------------------------------------------------------------------------------------------------------------------------------'''        
        my_message="Something went wrong. See script editor for error messages"
        return my_message
            
    '''==========================================================================================================================================
    COMMON LIST FUNCTIONS
    =========================================================================================================================================='''          
     
    def count_objects_in_list(self, arg=None):
        '''----------------------------------------------------------------------------------
        Gets the length of list items and any selected items function
        ----------------------------------------------------------------------------------'''          
        countObj=cmds.textScrollList(self.nodeList, q=1, ni=1)
        countSelObj=cmds.textScrollList(self.nodeList, q=1, nsi=1)
        cmds.text (self.listCountLabel, e=1, label='Selection list    '+ str(countObj)+' Items    '+str(countSelObj)+' Selected list items' )                               
    
    def add_to_list_function(self, eachSortedObj):
        '''----------------------------------------------------------------------------------
        Common add to list function
        ----------------------------------------------------------------------------------'''          
        cmds.textScrollList(self.nodeList, e=1, a=eachSortedObj)
        self.count_objects_in_list()
        
    def select_list_item_function(self, eachSortedObj):
        '''----------------------------------------------------------------------------------
        Common select in list function
        ----------------------------------------------------------------------------------'''          
        cmds.textScrollList(self.nodeList, e=1, si=eachSortedObj) 
        self.count_objects_in_list()
        
    def repopulate_list(self, eachSortedObj):
        '''----------------------------------------------------------------------------------
        Common refill the list function
        ----------------------------------------------------------------------------------'''          
        cmds.textScrollList(self.nodeList, e=1, ra=1)
        cmds.textScrollList(self.nodeList, e=1, append=eachSortedObj[0::1])
        self.count_objects_in_list()     

    '''==========================================================================================================================================
    BOTTOM BUTTON FUNCTIONS
    =========================================================================================================================================='''  
        
    def _clear_list(self, arg=None):
        '''----------------------------------------------------------------------------------
        this clears the list
        ----------------------------------------------------------------------------------'''          
        cmds.textScrollList(self.nodeList, e=1, ra=1)
        self.count_objects_in_list() 

    def deselect_in_list_function(self, arg=None):
        '''----------------------------------------------------------------------------------
        Common deselect in list function
        ----------------------------------------------------------------------------------'''              
        cmds.textScrollList(self.nodeList, e=1, da=1)
        self.count_objects_in_list()
             
    def adding_to_list_function_main(self, selectedObject, foundExistantListObj):
        '''----------------------------------------------------------------------------------
        Main populate list function
        ----------------------------------------------------------------------------------'''              
        if selectedObject>1:
            sortObjects=sorted(selectedObject, key=lower)
        if len(selectedObject)==1:
            sortObjects=selectedObject                                       
        if foundExistantListObj:
            for eachObject in sortObjects:
                if eachObject in foundExistantListObj:
                    self.deselect_in_list_function()
                    self.already_in_list_error(eachObject)
                    self.select_list_item_function(eachObject)                                           
                else:
                    self.add_to_list_function(eachObject) 
        else:
            for eachObject in sortObjects:
                self.add_to_list_function(eachObject)        
        
    def _add_selected_to_list(self, listArray):
        '''----------------------------------------------------------------------------------
        Adds selected objects to the list
        ----------------------------------------------------------------------------------'''          
        selectedObject=self.selection_grab()
        if selectedObject:
            self.adding_to_list_function_main(selectedObject, listArray)  
            
    def _remove_from_list(self, selectedListItems):
        '''----------------------------------------------------------------------------------
        This removes the selected item in the list from the list
        ----------------------------------------------------------------------------------'''          
        if selectedListItems<1:
            print 'Select item to subtract from list.'
        else:
            cmds.textScrollList(self.nodeList, e=1, ri=selectedListItems)
            self.count_objects_in_list() 
    
    def _swap_with_selected(self, selectedListItems, listArray):
        '''----------------------------------------------------------------------------------
        This swaps the selected list item with the selected object
        ----------------------------------------------------------------------------------'''          
        selectedObject=cmds.ls(sl=1, fl=1)
        if selectedObject:
            if selectedObject[0] in listArray:
                cmds.textScrollList(self.nodeList, e=1, si=selectedObject)
                self.already_in_list_error(selectedObject)
            else:
                cmds.textScrollList(self.nodeList, e=1, ri=selectedListItems)
                cmds.textScrollList(self.nodeList, e=1, a=selectedObject[0::1])
                self.count_objects_in_list()         
        else:
            print 'Select list item first and then object to swap with.'
    
    def _select_all_in_list(self, listArray):
        '''----------------------------------------------------------------------------------
        This selects all items in list
        ----------------------------------------------------------------------------------'''          
        if listArray:
            self.select_list_item_function(listArray)
            cmds.select(listArray)           
        else:
            print "List is empty."
            
    def _clear_selection(self):
        '''----------------------------------------------------------------------------------
        This clears the selection of the items in the list
        ----------------------------------------------------------------------------------'''          
        self.deselect_in_list_function()
    
    def _sort_list(self, listArray):
        '''----------------------------------------------------------------------------------
        This sorts the list by alphabetical and numerical
        ----------------------------------------------------------------------------------'''          
        if listArray:
            sortedObjList=sorted(listArray, key=lower)
            self.repopulate_list(sortedObjList)                              
        else:
            print "Check that list is present."
            
    def _make_set_from_selection_list(self,selectedListItems):
        '''----------------------------------------------------------------------------------
        This create a set from selected items in list
        ----------------------------------------------------------------------------------'''          
        if selectedListItems:
            result = cmds.promptDialog( 
                title='Confirm', 
                message='Name of set:', 
                button=['Continue','Cancel'],
                defaultButton='Continue', 
                cancelButton='Cancel', 
                dismissString='Cancel' )
            if result == 'Continue':
                text = cmds.promptDialog(query=True, text=True)
                cmds.sets(n=text)
            else:
                print "create set cancelled"
                return
        else:
            print "Select something from selection list."
            
    def list_item_selectability(self):
        '''----------------------------------------------------------------------------------
        This selects items in scene from list
        ----------------------------------------------------------------------------------'''          
        selectedListItems=cmds.textScrollList(self.nodeList, q=1, selectItem=1)
        cmds.select(selectedListItems, r=1)
        self.count_objects_in_list()
        print selectedListItems

    '''==========================================================================================================================================
    =========================================================================================================================================='''          
     
        
    def _bone_rivet(self, arg=None): 
        '''--------------------------------------------------------------------------------------------------------------------------------------
        Bone rivet interface: This creates a rivet at selection and parents a bone to the rivet
        --------------------------------------------------------------------------------------------------------------------------------------'''        
        winName = "Bone Rivets"
        winTitle = winName
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=400, h=100 )
        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=400)
        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        cmds.rowLayout  (' rMainRow ', w=400, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(200, 20))
        RivetName=cmds.textField(w=120, h=25, p='listBuildButtonLayout')    
        cmds.button (label='Create Bone Rivet', p='listBuildButtonLayout', command = lambda *args:self._add_bone_rivet(queryRivet=cmds.textField(RivetName, q=1, text=1) ))        
        cmds.showWindow(window)
        
    def _add_bone_rivet(self, queryRivet):
        '''--------------------------------------------------------------------------------------------------------------------------------------
        Bone rivet function: This creates a rivet at selection and parents a bone to the rivet
        --------------------------------------------------------------------------------------------------------------------------------------'''         
        selObj=self.selection_grab()
        getLists=zip(selObj[::2], selObj[1::2])
        for each in getLists:
            cmds.select(each[0])
            cmds.select(each[1], add=1)
            maya.mel.eval( "rivet;" )
            getRiv=cmds.ls(sl=1)
            cmds.rename(getRiv[0], queryRivet)
            getNewRiv=cmds.ls(sl=1)
            getClass.makeJoint()
            cmds.parent(getNewRiv[0]+"_jnt", getNewRiv[0]) 
        
    def chain_rig(self, arg=None):
        '''--------------------------------------------------------------------------------------------------------------------------------------
        Creates a full IK/FK chain rig based on guides setup in scene
        --------------------------------------------------------------------------------------------------------------------------------------'''         
        import ChainWork
        reload (ChainWork)
        result = cmds.promptDialog( 
                    title='Building a chainrig', 
                    message="Details for chain - EG: name, direction, controller size", 
                    text="name, Y, 10", 
                    button=['Continue','Cancel'],
                    defaultButton='Continue', 
                    cancelButton='Cancel', 
                    dismissString='Cancel' )
        if result == 'Continue':
            resultInfo=cmds.promptDialog(q=1)
            if resultInfo:
                pass
            else:
                print "nothing collected"
            getInfo=resultInfo.split(', ')
            getDir=getInfo[1]
            mainName=getInfo[0]
            if getDir=="X":
                nrx=1
                nry=0
                nrz=0  
            if getDir=="Y":
                nrx=0
                nry=1
                nrz=0   
            if getDir=="Z":
                nrx=0
                nry=0
                nrz=1
            ControllerSize=int(getInfo[2])
            # getChainClass=ChainRig()
            # getChainClass.create(nrz, nry, nrx, mainName, ControllerSize) 
            chainpath=str(getRigModPath)+"/ChainWork.py"
            exec(open(chainpath))
            getChainClass=ChainRig(nrz, nry, nrx, mainName, ControllerSize)
            #getChainClass.create(nrz, nry, nrx, mainName, ControllerSize) 


    def _open_texture_file_gmp(self, arg=None):
        '''--------------------------------------------------------------------------------------------------------------------------------------
        This opens the texture within selected file node in Gimp(if windows, set details above for path)
        --------------------------------------------------------------------------------------------------------------------------------------'''                 
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
                    if "Windows" in OSplatform:
                        subprocess.Popen([gimp, getValue])
                    if "Linux" in OSplatform: 
                        subprocess.Popen('gimp "%s"' % getValue, stdout=subprocess.PIPE, shell=True)                     
#                        os.system('gimp "%s"' % getValue)                  
        else:
            print "need to select a texture node"

    def _view_texture_file(self, arg=None):
        '''--------------------------------------------------------------------------------------------------------------------------------------
        This opens the texture view(opens in default image viewer as set on windows or linux)
        --------------------------------------------------------------------------------------------------------------------------------------'''        
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
                    if "Windows" in OSplatform:
                        subprocess.Popen(getValue)
                    if "Linux" in OSplatform:  
                       os.system('xdg-open "%s"' % getValue)                  
        else:
            print "need to select a texture node"

    def _open_texture_file_gmpV1(self, arg=None):
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
            



    def _open_work_folderV1(self, arg=None):
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
                    if "Windows" in OSplatform:
                        subprocess.Popen([photoshop, getValue])
                    if "Linux" in OSplatform:  
                        os.system('photoshop "%s"' % getValue)                         
                    
        else:
            print "need to select a texture node"

        
    def _eye_directions(self, arg=None):
        cmds.file(BbxFilepath, i=1,  type="mayaAscii", iv=1, mnc=0, gr=1, gn="FaceRig", op=1, rpr="ControlBox")
        try:
            getBox=cmds.ls("BigBox_CC_grp") 
        except:
            getBox=cmds.ls("*:BigBox_CC_grp")  
        getTranslation, getRotation=getClass.locationXForm(getHeadCtrl)
        cmds.move(getTranslation[0]+40, getTranslation[1], getTranslation[2], getBox)
        cmds.parentConstraint(getHeadCtrl,getBox, mo=1)
        print "Eye Direction Present"
        

    def addEyeDir(self, arg=None):
        '''this sandwitches a circle control to another control for an easy override switch(face controllers for SDK keys)'''
        colour=6
        size=1 
        selObj=("EyeOrient_L_jnt", "EyeOrient_R_jnt")
        for each in selObj:
            selObjParent=cmds.listRelatives( each, allParents=True )
            transformWorldMatrix, rotateWorldMatrix=getClass.locationXForm(each)        
            nrx, nry, nrz = 0.0, 0.0, 1.0 
            getcolour=cmds.getAttr(each+".overrideColor")
            name=each.split("_jnt")[0]+"_dir"
            grpname=each.split("_jnt")[0]+"_dir_grp"
            getClass.buildCtrl(each, name, grpname, transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)   
            cmds.parent(name, each)      
    def _rivet(self, arg=None):
        maya.mel.eval( "rivet;" )

    def _rivet_obj(self, arg=None): 
        selObj=cmds.ls(sl=1, fl=1)
        getFirst=selObj[:-1]
        constrainObj=selObj[-1]
        maya.mel.eval( "rivet" )
        getRiv=cmds.ls(sl=1)
        cmds.parent(constrainObj, getRiv)
        
    def _disappear(self, arg=None):
        getSel=self.selection_grab()
        for item in getSel:
            get_V_Value=getAttr(item+".visibility") 
            for each in trans:
                if get_V_Value==1:
                    cmds.setAttr(item+each, l=1)                    
                    cmds.setAttr(item+each, k=0)
                    cmds.setAttr(item+".visibility", 0)
                else:
                    cmds.setAttr(item+each, l=0)                    
                    cmds.setAttr(item+each, k=1)
                    cmds.setAttr(item+".visibility", 1)

#                getValue=getattr(item,each).get()
#                getChangeAttr=getattr(item,each)
#                if getValue==0:
#                    getChangeAttr.set(0)
#                else:
#                    getChangeAttr.set(1)
                
    def char_light_cleanup(self):
        try:    
            cmds.pointConstraint("*:Master_Ctrl", "*:LA0095_CharBaseLighting_Master:Lights", mo=1)
        except:
            print "no CharBased lighting present. Passing on relinking it."
            pass        
        try:
            if cmds.ls("*:LA0095_CharBaseLighting_Master:LightCtrl"):
                getLightObj=cmds.ls("*:LA0095_CharBaseLighting_Master:LightCtrl")
                for each in getLightObj:
                    getChildConstraint=[(each) for each in cmds.listRelatives(each, ad=1, typ="parentConstraint")]
                    if len(getChildConstraint)>0:
                        cmds.delete(getChildConstraint[0])
        except:
            pass        
    def _clean_up(self, arg=None): 
        self.char_light_cleanup()
        if cmds.ls("*Skirtvtx*jnt") :                      
            getSel=cmds.ls("*Skirtvtx*jnt") 
            for item in getSel:
                    cmds.setAttr(item+"_parentConstraint1.interpType", 0 )    
                    print item+" -set joint interpolation type to No Flip"    
        if cmds.ls("*Dressvtx*jnt") :                      
            getSel=cmds.ls("*Dressvtx*jnt") 
            for item in getSel:
                    cmds.setAttr(item+"_parentConstraint1.interpType", 0 )    
                    print item+" -set joint interpolation type to No Flip"    
        if cmds.ls(typ="locator") :                      
            getSel=cmds.ls(typ="locator")
            for item in getSel:
                getTransform=cmds.listRelatives(item, ap=1)[0]
                for each in trans:
                    try:
                        cmds.setAttr(getTransform+each, k=0)
                    except:
                        print "cannot set keyable state in this file for "+getTransform+each
                        pass
                    try:
                        cmds.setAttr(item+".visibility", 0)
                    except:
                        print "unable to set visibility on shape node of locator: " +getTransform
                        pass        
        if cmds.ls("Lash*RIV"):
            getSel=cmds.ls("Lash*RIV")
            getSel.append("Lash_attribute_holder")
            for item in getSel:
                for each in trans:
                    try:
                        cmds.setAttr(item+each, k=0)
                        print "keyframe ability turned off for : "+item+each
                    except:
                        pass
                    try:
                        cmds.setAttr(item+".visibility", 0)
                        print "hid "+item
                    except:
                        pass
        if cmds.ls("Eye_*_scptStretchOrigin"):
            getSel=cmds.ls("Eye_*_scptStretchOrigin") 
            for item in getSel:
                for each in trans:
                    cmds.setAttr(item+each, k=0)
                    print "keyframe ability turned off for : "+item+each
                    cmds.setAttr(item+".visibility", 0)   
            getSel=cmds.ls("Eye_*_scpt.en") 
            for item in getSel:                 
                cmds.setAttr(item, l=1)  
                print "locked "+item
        if cmds.ls("Eyes_txt_CC") :                      
            getSel=cmds.ls("Eyes_txt_CC")  
            getEye=cmds.ls("Eyes_select")  
            getSel=getSel+getEye
            for item in getSel:
                for each in trans:
                    cmds.setAttr(item+each, k=0)
                    print "keyframe ability turned off for : "+item+each
                    cmds.setAttr(item+".visibility", 0)    
                    print "hid "+item            
#         if cmds.ls("rivet*") :                      
#             getSel=cmds.ls("rivet*") 
#             for item in getSel:
#                 for each in trans:
#                     cmds.setAttr(item+each, k=0)
#                     print "keyframe ability turned off for : "+item+each
#                     cmds.setAttr(item+".visibility", 0)    
#                     print "hid "+item            
        if cmds.nodeType(typ="locator") :                      
            getSel=mds.nodeType(typ="locator")
            for item in getSel:
                print item
                for each in trans:
                    cmds.setAttr(item+each, k=0)
                    print "keyframe ability turned off for : "+item+each
                    cmds.setAttr(item+".visibility", 0)      
                    print "hid "+item  
                            
    def _clean_up_rig(self, arg=None):
        getTransShoulder=[".tx", ".ty", ".tz"]
        if cmds.ls("Shoulder_*_Ctrl"):
            getSel=cmds.ls("Shoulder_*_Ctrl")
            for item in getSel:
                for each in getTransShoulder:
                    cmds.setAttr(item+each, cb=0)
                    cmds.setAttr(item+each, l=1)
                    cmds.setAttr(item+each, k=0)
        if cmds.ls("Hips_Ctrl"):
            getSel=cmds.ls("Hips_Ctrl")   
            for item in getSel: 
                cmds.setAttr(item+".spineFK_IK", 0)                
        if cmds.ls(typ="locator") :                      
            getSel=cmds.ls(typ="locator")
            for item in getSel:
                getTransform=cmds.listRelatives(item, ap=1)[0]
                for each in trans:
                    try:
                        cmds.setAttr(getTransform+each, k=0)
                        print "keyframe ability turned off for : "+getTransform+each
                    except:
                        print "cannot set keyable state in this file"
                        pass
                    try:
                        cmds.setAttr(item+".visibility", 0)
                        print "hid "+item
                    except:
                        print "unable to set visibility on shape node of locator: " +getTransform
                        pass        
        if cmds.ls("Hand_*_Fingers_Ctrl"):
            selObj=cmds.ls("Hand_*_Fingers_Ctrl")
            for each in selObj:
                cmds.addAttr(each+".SpreadFingers", e=1, min=-0, max=90)
                print "reset " +each+".SpreadFingers"
                cmds.addAttr(each+".CurlFingers", e=1, min=-160, max=0)
                print "reset " +each+".CurlFingers"
        if cmds.ls("*_Finger_*_Ctrl"):
            selObj=cmds.ls("*_Finger_*_Ctrl")
            for each in selObj:
                if "|" not in each:
                    cmds.addAttr(each+".MiddleJoint", e=1, min=-160, max=0)
                    print "reset " +each+".MiddleJoint"
                    cmds.addAttr(each+".LastJoint", e=1, min=-160, max=0)
                    print "reset " +each+".LastJoint"
                    cmds.addAttr(each+".FingerFullCurl", e=1, min=-160, max=0)  
                    print "reset " +each+".FingerFullCurl"     
        Side=["Right", "Left"]
        for eachSide in Side:
            try:
                SDK_Fingers=("Index_Finger_"+eachSide+"_M_Ctrl.rotateY",
                            "Mid_Finger_"+eachSide+"_M_Ctrl.rotateY",
                            "Ring_Finger_"+eachSide+"_M_Ctrl.rotateY",
                            "Pinky_Finger_"+eachSide+"_M_Ctrl.rotateY",
                            "Thumbmid_"+eachSide+"_M_Ctrl.rotateY",
                            "Thumbbase_"+eachSide+"_M_Ctrl.rotateY",
                            "Index_Finger_"+eachSide+"_M_Ctrl.ry")
                for each in SDK_Fingers:
                    cmds.setAttr(each, lock=1) 
                    print each+" attribute has been locked"
            except:
                pass    


    def _blend_colour_window(self, arg=None):
        getSel=cmds.ls(sl=1)        
        global attributeSel
        geteattr=cmds.listAttr (getSel[0], ud=1)        
        winName = "select attribute to link the switch constraint driven key to"
        winTitle = winName
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)

        window = cmds.window(winName, title=winTitle, tbm=1, w=300, h=100 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=150)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        
        cmds.rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))
        attributeSel=cmds.optionMenu( label='user attribute')
        for each in geteattr:
            cmds.menuItem( label=each)            
        cmds.button (label='Go', p='listBuildButtonLayout', command = self._blend_colour)
        cmds.showWindow(window)   
          
    def _blend_colour(self, arg=None):
        geteattr=cmds.optionMenu(attributeSel, q=1, v=1)          
        selObj=cmds.ls(sl=1)
        if len(selObj)>3:
            pass
        else:
            print "select a controller with a user attribute, a follow object, then a '0' rotate/scale leading object and a '1' rotate/scale leading object"
            return
        Controller=selObj[0]
        firstChild=selObj[1]
        secondChild=selObj[2]
        thirdChild=selObj[3]  
        Controller=Controller+"."+geteattr      
        getClass.blendColors_callup(Controller, firstChild, secondChild, thirdChild)  
        
    def _quickCconnect_window(self, arg=None):
        getSel=cmds.ls(sl=1) 
        if len(getSel)>1:
            pass
        else:
            print "select two objects to connect"
            return 
        getFirst=getSel[:-1]
        getSecond=getSel[-1] 
        global attributeFirstSel
        global attributeSecondSel        
        getFirstAttr=cmds.listAttr (getFirst[0])      
        getFirstAttr=sorted(getFirstAttr)
        getSecondAttr=cmds.listAttr (getSecond)
        getSecondAttr=sorted(getSecondAttr)         
        winName = "Quick connect attributes"
        winTitle = winName
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)

        window = cmds.window(winName, title=winTitle, tbm=1, w=350, h=100 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=150)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        cmds.rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))
        cmds.text(label=getFirst[0])
        cmds.text(label=getSecond)        
        attributeFirstSel=cmds.optionMenu( label='From')
        for each in getFirstAttr:
            cmds.menuItem( label=each) 
        attributeSecondSel=cmds.optionMenu( label='To')               
        for each in getSecondAttr:
            cmds.menuItem( label=each)                    
        cmds.button (label='Go', p='listBuildButtonLayout', command=lambda *args:self._quickCconnect(getFirst, getSecond))
        cmds.showWindow(window)   
          
    def _quickCconnect(self, getFirst, getSecond):
        getFirstattr=cmds.optionMenu(attributeFirstSel, q=1, v=1)          
        getSecondattr=cmds.optionMenu(attributeSecondSel, q=1, v=1) 
        getFirstAttr=getFirst[0]  
        for each in getFirst:    
            cmds.connectAttr(getSecond+"."+getSecondattr, each+"."+getFirstattr, f=1)

    def _quickCopy_single_Attr_window(self, arg=None):
        getSel=cmds.ls(sl=1)  
        getChildren=getSel[1:]
        getParent=getSel[:1]
        global attributeFirstSel
        global attributeSecondSel        
        getFirstAttr=cmds.listAttr (getChildren[0])      
        getFirstAttr=sorted(getFirstAttr)
        getSecondAttr=cmds.listAttr (getParent)
        getSecondAttr=sorted(getSecondAttr)         
        winName = "Quick transfer single attribute"
        winTitle = winName
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=350, h=100 )
        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=150)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        cmds.rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))
        self.theParent=cmds.text(label=getParent[0])
        self.theChild=cmds.text(label=getChildren[0])        
        self.attributeFirstSel=cmds.optionMenu( label='From', cc=lambda *args:self._change_second_attr_menu())
        for each in getFirstAttr:
            cmds.menuItem( label=each) 
        self.attributeSecondSel=cmds.optionMenu( label='To')               
        for each in getSecondAttr:
            cmds.menuItem( label=each)                    
        cmds.button (label='Go', p='listBuildButtonLayout', command=lambda *args:self._copy_single_attr(getChildren, getParent))
        cmds.showWindow(window)   

    def _change_second_attr_menu(self):
        '''----------------------------------------------------------------------------------
        ----------------------------------------------------------------------------------''' 
        getFirstattr=optionMenu(self.attributeFirstSel, q=1, v=1)  
        try:
            getSecondattr=optionMenu(self.attributeSecondSel, e=1, v=getFirstattr)
        except:
            print "this attribute cannot be found in second menu"
            pass

    def _copy_single_attr(self, getChildren, getParent):
        getParentAttr=cmds.optionMenu(attributeFirstSel, q=1, v=1)
        getChildAttr=cmds.optionMenu(attributeSecondSel, q=1, v=1)
        getSel=cmds.ls(sl=1)  
        getChildren=getSel[1:]
        getParent=getSel[:1]      
        getValue=getAttr(getParent[0]+'.'+getParentAttr)    
        for each in getChildren:
            get=cmds.keyframe(getParent[0]+'.'+getParentAttr, q=1, kc=1) 
            if get!=0:
                try:
                    getSource=connectionInfo(getParent[0]+'.'+getParentAttr, sfd=1)
                    newAnimSrce=duplicate(getSource) 
                    lognm=newAnimSrce[0].replace(str(getParent[0]), str(each))
                    #===========================================================
                    # remove numbers at end
                    #===========================================================
                    newname=re.sub("\d+$", "", lognm)
                    cmds.rename(newAnimSrce, newname)
                    getChangeAttr=each+'.'+getChildAttr
                    connectAttr(newname+'.output', getChangeAttr, f=1)
                except:
                    pass
            else:
                try:                    
                    getChangeAttr=each+'.'+getChildAttr
                    setAttr(getChangeAttr, getValue)
                except:
                    pass
        
    def _createAlias_window(self, arg=None):
        getSel=ls(sl=1)  
        if len(getSel)>1:
            pass
        else:
            print "need to select 2 or more items" 
            return       
        getFirst=getSel[0]
        global attributeFirstSel
        global makeAttr        
        getFirstAttr=listAttr (getFirst, w=1, a=1, s=1,u=1)      
        getFirstAttr=sorted(getFirstAttr)        
        winName = "Quick connect attributes"
        winTitle = winName
        if cmds.window(winName, exists=True):
                deleteUI(winName)

        window = cmds.window(winName, title=winTitle, tbm=1, w=350, h=100 )

        menuBarLayout(h=30)
        rowColumnLayout  (' selectArrayRow ', nr=1, w=150)

        frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        
        rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        columnLayout ('selectArrayColumn', parent = 'rMainRow')
        setParent ('selectArrayColumn')
        separator(h=10, p='selectArrayColumn')
        gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))
        attributeFirstSel=optionMenu( label='From')
        for each in getFirstAttr:
            menuItem( label=each)                
        makeAttr=textField()
        button (label='Go', p='listBuildButtonLayout', command = self._create_alias)
        showWindow(window)   
          
    def _create_alias(self, arg=None):
        getSel=ls(sl=1)
        getFirstattr=optionMenu(attributeFirstSel, q=1, v=1)       
        floater=textField(makeAttr, q=1, text=1)
        getFirst=getSel[:-1]
        getSecond=getSel[-1]  
        for each in getFirst:
            get=cmds.keyframe(each+'.'+getFirstattr, q=1, kc=1)
            if get>0:
                getSource=connectionInfo(each+'.'+getFirstattr, sfd=1) 
                addAttr([getSecond], ln=floater, at="double", k=1, nn=floater)
                connectAttr(getSource, getSecond+"."+floater, f=1)
                connectAttr(getSecond+"."+floater, each+"."+getFirstattr, f=1)
            else:
                getValue=getattr(each,getFirstattr).get()
                addAttr([getSecond], ln=floater, at="double", k=1, nn=floater)
                connectAttr(getSecond+"."+floater, each+"."+getFirstattr, f=1)
                getChangeAttr=getattr(getSecond,floater)
                getChangeAttr.set(getValue)
#                setAttr(getSecond+"."+floater, getValue)

    def _transfer_anim_attr(self, arg=None):
        '''This copies values and animcurve nodes of a first selection to all secondary selections'''
        getSel=ls(sl=1)
        getChildren=getSel[1:]
        getParent=getSel[:1]
        for each in getChildren:
            getFirstattr=listAttr (getParent[0], w=1, a=1, s=1, u=1, m=0)
            for item in getFirstattr:
                if "." not in item:
                    get=cmds.keyframe(getParent[0]+'.'+item, q=1, kc=1) 
                    if get!=0:
                        try:
                            getSource=connectionInfo(getParent[0]+'.'+item, sfd=1)
                            newAnimSrce=duplicate(getSource) 
                            lognm=newAnimSrce[0].replace(str(getParent[0]), str(each))
                            #===========================================================
                            # remove numbers at end
                            #===========================================================
                            newname=re.sub("\d+$", "", lognm)
                            cmds.rename(newAnimSrce, newname)
                            getChangeAttr=each+'.'+item                        
                            connectAttr(newname+'.output', getChangeAttr, f=1)                             
#                            connectAttr(getSource, each+"."+item, f=1)
                        except:
                            pass
                    else:
                        try:
                            getValue=getattr(getParent[0],item).get()
                            getChangeAttr=getattr(each,item)
                            getChangeAttr.set(getValue)
                        except:
                            pass

    def _findAttr_window(self, arg=None): 
        try:
            getSel=ls(sl=1)     
            getFirst=getSel[0]
        except:
            print "must select something"
            return
#        global attributeFirstSel
#        global makeAttr        
        getFirstAttr=listAttr (getFirst, w=1, a=1, s=1,u=1)      
        getFirstAttr=sorted(getFirstAttr)        
        winName = "Fetch Attributes"
        winTitle = winName
        if cmds.window(winName, exists=True):
                deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=450, h=100)
        menuBarLayout(h=30)
        rowColumnLayout  (' selectArrayRow ', nr=1, w=450)
        frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        rowLayout  (' rMainRow ', w=450, numberOfColumns=6, p='selectArrayRow')
        columnLayout ('selectArrayColumn', parent = 'rMainRow')
        setParent ('selectArrayColumn')
        separator(h=10, p='selectArrayColumn')
   
        gridLayout('valuebuttonlayout', p='selectArrayColumn', numberOfColumns=3, cellWidthHeight=(150, 20))
        text(label="Att Value:", p='valuebuttonlayout', align="left")
        self.attrVal=text(label="Select from drop down", p='valuebuttonlayout')
        button (label='Refresh Selection', p='valuebuttonlayout', command = lambda *args:self._refresh())
#        button (label='Get Current Value', p='valuebuttonlayout', command = lambda *args:self._get_attr(getFirstattr=optionMenu(self.attributeFirstSel, q=1, v=1)))
        gridLayout('listBuildLayout', p='selectArrayColumn', numberOfColumns=1, cellWidthHeight=(450, 20))   
        self.attributeFirstSel=optionMenu( label='Find', cc=lambda *args:self.change_attr_output())
        for each in getFirstAttr:
            menuItem( label=each)
        gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=3, cellWidthHeight=(150, 20))
        text(label="Change Value:", align="left", w=50)        
        makeAttr=textField(w=150, text="enter value EG:'50'")
        button (label='Apply Value', p='listBuildButtonLayout', w=150, command = lambda *args:self._apply_att(getFirstattr=optionMenu(self.attributeFirstSel, q=1, v=1), makeAttr=textField(makeAttr, q=1, text=1)))
        text(label="Search:", align="left", w=50) 
        findAttr=textField(AttributeName, text="Enter name EG:'translate'")
        button (label='Fetch Attribute Name', bgc=[0.55, 0.35, 0.20], p='listBuildButtonLayout', command = lambda *args:self._find_att(getFirstattr=optionMenu(self.attributeFirstSel, q=1, ill=1), attribute=textField(findAttr, q=1, text=1)))
        text(label="Search:", align="left", w=50)
        valueAttr=textField(text="Enter value EG:'1.0'")
        button (label='Fetch Attribute Value', bgc=[0.55, 0.35, 0.20], p='listBuildButtonLayout', command = lambda *args:self._find_value(getFirstattr=optionMenu(self.attributeFirstSel, q=1, ill=1), attribute=textField(findAttr, q=1, text=1), values=textField(valueAttr, q=1, text=1)))
        showWindow(window)   

    def _refresh(self, arg=None):
        menuItems = cmds.optionMenu(self.attributeFirstSel, q=True, ill=True)
        if menuItems:
            cmds.deleteUI(menuItems)        
        newSel=ls(sl=1, fl=1)
        getListAttr=listAttr (newSel[0], w=1, a=1, s=1,u=1)
        getListAttr=sorted(getListAttr) 
        cmds.optionMenu(self.attributeFirstSel, e=1) 
        for each in getListAttr:
            menuItem(label=each, parent=self.attributeFirstSel)     
                
    def _get_attr(self, getFirstattr):
        getSel=ls(sl=1, fl=1)        
        newAttr=getattr(getSel[0],getFirstattr)
        getChangeAttr=getattr(getSel[0],getFirstattr).get()
        select(newAttr, add=1)
        self.count_attr_output(getChangeAttr) 
        print newAttr, getChangeAttr
        
    def _find_att(self, getFirstattr, attribute):         
        getSel=ls(sl=1, fl=1)        
        collectAttr=[]
        for each in getFirstattr:
            find=menuItem(each, q=1, label=1)
            if attribute in find:
                collectAttr.append(find) 
        optionMenu(self.attributeFirstSel, e=1, v=collectAttr[0]) 
        newAttr=getattr(getSel[0],collectAttr[0])
        select(newAttr, add=1)
        getChangeAttr=getattr(getSel[0],collectAttr[0]).get() 
        menuItems = cmds.optionMenu(self.attributeFirstSel, q=True, ill=True)
        if menuItems:
            cmds.deleteUI(menuItems)        
        getListAttr=sorted(collectAttr) 
        cmds.optionMenu(self.attributeFirstSel, e=1) 
        for each in getListAttr:
            menuItem(label=each, parent=self.attributeFirstSel)  
        self.count_attr_output(getChangeAttr)
        print newAttr, getChangeAttr


    def _find_value(self, getFirstattr, attribute, values):
        try:
            values=float(values) 
        except:
            values=int(values)
        getSel=ls(sl=1, fl=1)        
        collectAttr=[]
        for each in getFirstattr:
            getSel=ls(getSel[0])
            find=menuItem(each, q=1, label=1)
            try:
                foundAttr=getattr(getSel[0],find).get()
            except:
                pass
            if foundAttr == values:
                print foundAttr
                collectAttr.append(find)                 
        optionMenu(self.attributeFirstSel, e=1, v=collectAttr[0]) 
        print "hi"
        newAttr=getattr(getSel[0],collectAttr[0])
        select(newAttr, add=1)
        getChangeAttr=getattr(getSel[0],collectAttr[0]).get() 
        menuItems = cmds.optionMenu(self.attributeFirstSel, q=True, ill=True)
        if menuItems:
            cmds.deleteUI(menuItems)        
        getListAttr=sorted(collectAttr) 
        cmds.optionMenu(self.attributeFirstSel, e=1) 
        for each in getListAttr:
            menuItem(label=each, parent=self.attributeFirstSel)  
        self.count_attr_output(getChangeAttr)
        print newAttr, getChangeAttr

    def count_attr_output(self, getChangeAttr):
        '''----------------------------------------------------------------------------------
        ----------------------------------------------------------------------------------''' 
        cmds.text(self.attrVal, e=1, label=getChangeAttr )

    def change_attr_output(self):
        '''----------------------------------------------------------------------------------
        ----------------------------------------------------------------------------------''' 
        getSel=ls(sl=1, fl=1)
        getFirstattr=optionMenu(self.attributeFirstSel, q=1, v=1)  
        newAttr=getattr(getSel[0],getFirstattr)
        try:
            getChangeAttr=getattr(getSel[0],getFirstattr).get()
            pass
        except:
            print "Can't obtain value for "+getSel[0],getFirstattr
            return               
        cmds.text(self.attrVal, e=1, label=getChangeAttr )
        
    def _apply_att(self, getFirstattr, makeAttr):
        getSel=ls(sl=1, fl=1)        
#        getAttri=optionMenu(attributeFirstSel, q=1, v=1)
        getChangeAttr=getattr(getSel[0],getFirstattr)
        try:
            makeAttr=float(makeAttr)
        except:
            print "Field must have number"
        try:
            getChangeAttr.set(makeAttr)
            pass
        except:
            print "Unable to change "+getSel[0],getFirstattr+" in this way"
            return
        getChangeAttr=getattr(getSel[0],getFirstattr).get()
        self.count_attr_output(getChangeAttr) 
       

    def _erase_anim(self, arg=None):
        getSel=cmds.ls(sl=1, fl=1)
        for each in getSel:
            getFirstattr=listAttr (each, w=1, a=1, s=1, u=1, m=0)
            for item in getFirstattr:
                if "." not in item:
                    get=cmds.keyframe(each+'.'+item, q=1, kc=1)
                    if get>0:
                        getSource=connectionInfo(each+'.'+item, sfd=1) 
                        delete(getSource.split(".")[0])
                    else:
                        pass

    def _reset(self, arg=None):
        getSel=cmds.ls(sl=1, fl=1)
        for each in getSel:
            getFirstattr=[(item) for item in cmds.listAttr (each, w=1, a=1, s=1, u=1, k=1, v=1, m=0) if "visibility" not in item and "scaleX" not in item and "scaleY" not in item and "scaleZ" not in item] 
            for item in getFirstattr:
                setAttr(each+'.'+item, 0)
#                if "." not in item:
#                    get=cmds.keyframe(each+'.'+item, q=1, kc=1)
#                    if get>0:
#                        setAttr(each+'.'+item, 0)
#                    else:
#                        setAttr(each+'.'+item, 1)
  
                    
                        
    def _copy_into_grp(self, arg=None):
        getSel=ls(sl=1)
        getFirst=getSel[:-1]
        getGrp=getSel[-1]
        for each in getFirst:
            newDupe=duplicate(each)
            parent(newDupe, getGrp)
            rename(newDupe[0], each)

    def _createSDK_alias_window(self, arg=None):
        getSel=ls(sl=1, fl=1)  
        if len(getSel)>1:
            pass
        else:
            print "need to select 2 or more items" 
            return       
        getFirst=getSel[0]
#        global attributeFirstSel
#        global makeAttr   
#        global firstMinValue
#        global firstMaxValue
#        global secondMinValue
#        global secondMaxValue
        getFirstAttr=listAttr (getFirst, w=1, a=1, s=1,u=1)      
        getFirstAttr=sorted(getFirstAttr)        
        winName = "Quick SDK alias"
        winTitle = winName
        if cmds.window(winName, exists=True):
                deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=350, h=100 )
        menuBarLayout(h=30)
        rowColumnLayout  (' selectArrayRow ', nr=1, w=150)
        frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        columnLayout ('selectArrayColumn', parent = 'rMainRow')
#        setParent ('selectArrayColumn')
#        separator(h=10, p='selectArrayColumn')
        gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))
        self.attributeFirstSel=optionMenu( label='From', p='listBuildButtonLayout')
        for each in getFirstAttr:
            menuItem( label=each)  
        self.makeAttr=cmds.textField(w=40, h=25, p='listBuildButtonLayout', text="attribute name")                          
        cmds.gridLayout('txvaluemeter', p='selectArrayColumn', numberOfColumns=3, cellWidthHeight=(80, 18)) 
        cmds.text(label="1st min/max", w=80, h=25, p='txvaluemeter',) 
        self.firstMinValue=cmds.textField(w=40, h=25, p='txvaluemeter', text="0")
        self.firstMaxValue=cmds.textField(w=40, h=25, p='txvaluemeter', text="1")  
        cmds.text(label="2nd min/max", w=80, h=25, p='txvaluemeter') 
        self.secondMinValue=cmds.textField(w=40, h=25, p='txvaluemeter', text="0")
        self.secondMaxValue=cmds.textField(w=40, h=25, p='txvaluemeter', text="1")
        gridLayout('BuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))             
        button (label='Go', p='BuildButtonLayout', command = lambda *args:self._create_SDK_alias(firstMinValue=float(textField(self.firstMinValue,q=1, text=1)), firstMaxValue=float(textField(self.firstMaxValue,q=1, text=1)), secondMinValue=float(textField(self.secondMinValue,q=1, text=1)), secondMaxValue=float(textField(self.secondMaxValue,q=1, text=1)), getFirstattr=optionMenu(self.attributeFirstSel, q=1, v=1), floater=textField(self.makeAttr, q=1, text=1)))
        showWindow(window)   
          
    def _create_SDK_alias(self, firstMinValue, firstMaxValue, secondMinValue, secondMaxValue, getFirstattr, floater):
        getSel=ls(sl=1)
        print firstMinValue, firstMaxValue, secondMinValue, secondMaxValue, getFirstattr, floater
#        firstMinValue=float(textField(self.firstMinValue,q=1, text=1))
#        firstMaxValue=float(textField(self.firstMaxValue,q=1, text=1))
#        secondMinValue=float(textField(self.secondMinValue,q=1, text=1))
#        secondMaxValue=float(textField(self.secondMaxValue,q=1, text=1))
#        getFirstattr=optionMenu(attributeFirstSel, q=1, v=1)
#        floater=textField(makeAttr, q=1, text=1)
        getFirst=getSel[:-1]
        getSecond=getSel[-1]
        anAttr=addAttr([getSecond], ln=floater, at="double", k=1, nn=floater)
        Controller=getSecond+"."+floater
        for each in getFirst:
            Child=each+"."+getFirstattr
            setAttr(Child, lock=0) 
            setAttr(Controller, secondMinValue)
            setAttr(Child,firstMinValue)
            setDrivenKeyframe(Child, cd=Controller)
            setAttr(Controller, secondMaxValue)
            setAttr(Child, firstMaxValue)
            setDrivenKeyframe(Child, cd=Controller)
            setAttr(Controller, secondMinValue)
            setAttr(Child, lock=1)        


    def _range_attr_window(self, arg=None):
        getSel=ls(sl=1, fl=1)  
        if len(getSel)>2:
            pass
        else:
            print "need to select 3 or more items" 
            return       
        getFirst=getSel[0]
        global attributeFirstSel
        global makeAttr
        getFirstAttr=[]
        getAttrs=listAttr (getFirst, w=1, a=1, s=1,u=1) 
        for each in getAttrs:
            if ']' in each:
                getNewEach=each.split('.')[-1:]
                getFirstAttr.append(getNewEach[0])
            else:
                getFirstAttr.append(each)
        getFirstAttr=sorted(getFirstAttr)        
        winName = "Randomize/Increment Attribute on Multi Select"
        winTitle = winName
        if cmds.window(winName, exists=True):
                deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=350, h=100 )
        menuBarLayout(h=30)
        rowColumnLayout  (' selectArrayRow ', nr=1, w=150)
        frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        columnLayout ('selectArrayColumn', parent = 'rMainRow')
        setParent ('selectArrayColumn')
        separator(h=10, p='selectArrayColumn')
        gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=1, cellWidthHeight=(150, 20))
        self.attributeFirstSel=optionMenu( label='From')
        for each in getFirstAttr:
            menuItem( label=each)
        gridLayout('checkboxlayout', p='selectArrayColumn', numberOfColumns=3, cellWidthHeight=(80, 20))                
        cmds.text(label="options", w=80, h=25)
        self.randomized=checkBox(label="randomize", ann="If on, number within range is randomized. If off, numbers will increment via percentage based on selection against the range")
        self.relative=checkBox(label="relative", ann="If on, number within range is randomized. If off, numbers will increment in relative position only as opposed to absolute(default)")
        cmds.gridLayout('txvaluemeter', p='selectArrayColumn', numberOfColumns=3, cellWidthHeight=(80, 18)) 
        cmds.text(label="range", w=80, h=25) 
        self.firstMinValue=cmds.textField(w=40, h=25, p='txvaluemeter', text="0.0")
        self.firstMaxValue=cmds.textField(w=40, h=25, p='txvaluemeter', text="1.0")  
        gridLayout('BuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))             
        button (label='Go', p='BuildButtonLayout', command = lambda *args:self._range_attr(randomized=cmds.checkBox(self.randomized,q=True, value=1), relative=cmds.checkBox(self.relative,q=True, value=1), getFirstattr=optionMenu(self.attributeFirstSel, q=1, v=1), firstMinValue=float(textField(self.firstMinValue,q=1, text=1)), firstMaxValue=float(textField(self.firstMaxValue,q=1, text=1))))
        showWindow(window)
   
        
    def _range_attr(self, randomized, relative, getFirstattr, firstMinValue, firstMaxValue):
        getSel=ls(sl=1, fl=1)        
        if relative==False:
            if randomized==False:
                self._range_inc(getSel, getFirstattr, firstMinValue, firstMaxValue)
            else:
                self._range_random(getSel, getFirstattr, firstMinValue, firstMaxValue)
        else:
            if randomized==False:
                self._range_relative(getSel, getFirstattr, firstMinValue, firstMaxValue)
            else:
                self._range_rel_random(getSel, getFirstattr, firstMinValue, firstMaxValue)
            
    
    def _range_inc(self, getSel, getFirstattr, firstMinValue, firstMaxValue):
        BucketValue=getClass.Percentages(getSel, firstMinValue, firstMaxValue)
        for each, item in map(None, getSel, BucketValue):
            getChangeAttr=each+'.'+getFirstattr
            cmds.setAttr(getChangeAttr, item)


    def _range_random(self, getSel, getFirstattr, firstMinValue, firstMaxValue):
        for each in getSel:
            getChangeAttr=each+'.'+getFirstattr
            getVal=random.uniform(firstMinValue,firstMaxValue)
            cmds.setAttr(getChangeAttr, getVal)

    def _range_relative(self, getSel, getFirstattr, firstMinValue, firstMaxValue):
        BucketValue=getClass.Percentages(getSel, firstMinValue, firstMaxValue)
        for each, item in map(None, getSel, BucketValue):
            getChangeAttr=each+'.'+getFirstattr
            getValue=cmds.getAttr(each+'.'+getFirstattr)
            newValue=getValue+item
            print newValue
            cmds.setAttr(getChangeAttr, newValue)

    def _range_rel_random(self, getSel, getFirstattr, firstMinValue, firstMaxValue):
        for each in getSel:
            getChangeAttr=each+'.'+getFirstattr
            getValue=cmds.getAttr(each+'.'+getFirstattr)
            getVal=random.uniform(firstMinValue,firstMaxValue)
            newValue=getValue+getVal
            print newValue             
            cmds.setAttr(getChangeAttr, newValue)      



    def cv_remove_window(self, arg=None):
        getSel=ls(sl=1, fl=1)  
        if len(getSel)>0:
            pass
        else:
            print "need to select something" 
            return       
        getFirst=getSel[0]
        global attributeFirstSel
        global makeAttr
        getFirstAttr=[]
        getAttrs=listAttr (getFirst, w=1, a=1, s=1,u=1) 
        for each in getAttrs:
            if ']' in each:
                getNewEach=each.split('.')[-1:]
                getFirstAttr.append(getNewEach[0])
            else:
                getFirstAttr.append(each)
        getFirstAttr=sorted(getFirstAttr)  
        winName = "Cull CV"
        winTitle = winName
        if cmds.window(winName, exists=True):
                deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=350, h=100 )
        menuBarLayout(h=30)
        rowColumnLayout  (' selectArrayRow ', nr=1, w=150)
        frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        columnLayout ('selectArrayColumn', parent = 'rMainRow')
        setParent ('selectArrayColumn')
        cmds.gridLayout('txvaluemeter', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(80, 18)) 
        cmds.text(label="every",  p='txvaluemeter', w=80, h=25)         
        cmds.text(label="every other",  p='txvaluemeter', w=80, h=25) 
        self.remove=cmds.textField(w=40, h=25, p='txvaluemeter', text="1")
        self.removeNth=cmds.textField(w=40, h=25, p='txvaluemeter', text="2")  
        gridLayout('BuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(80, 20))             
        button (label='Go', p='BuildButtonLayout', command = lambda *args:self.removeCV(remove=int(textField(self.remove,q=1, text=1))))
        button (label='Go', p='BuildButtonLayout', command = lambda *args:self.remove_Nth(removeNth=int(textField(self.removeNth,q=1, text=1))))
        showWindow(window)
        
                
    def remove_Nth(self, removeNth):  
        getSel=ls(sl=1, fl=1)   
        getSel=getSel[:1]  
        if nodeType(getSel[0])=="transform":
            for each in getSel:
                for item in each.cv[::removeNth]:
                    delete(item)
        elif nodeType(getSel[0])=="nurbsCurve":
            for each in getSel[::removeNth]:         
                delete(each)

    def removeCV(self, remove):
        getSel=ls(sl=1, fl=1)
        if nodeType(getSel[0])=="transform":         
            for each in getSel:
                for item in each.cv[remove]:
                    delete(item)
        elif nodeType(getSel[0])=="nurbsCurve":                
            for each in getSel:
                delete(each.cv[remove])

    def _connSDK_alias_window(self, arg=None):
        getSel=ls(sl=1)  
        if len(getSel)>1:
            pass
        else:
            print "need to select 2 or more items" 
            return       
#        global attributeFirstSel
#        global makeAttr   
#        global firstMinValue
#        global firstMaxValue
#        global secondMinValue
#        global secondMaxValue
        getSel=cmds.ls(sl=1)  
        getFirst=getSel[0]      
        getSecond=getSel[1]      
        getFirstAttr=listAttr (getFirst, w=1, a=1, s=1,u=1)     
        getFirstAttr=sorted(getFirstAttr)
        getSecondAttr=cmds.listAttr (getSecond)
        getSecondAttr=sorted(getSecondAttr)         
        winName = "Quick SDK alias"
        winTitle = winName
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=350, h=100 )
        menuBarLayout(h=30)
        rowColumnLayout  (' selectArrayRow ', nr=1, w=150)
        frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        columnLayout ('selectArrayColumn', parent = 'rMainRow')
        setParent ('selectArrayColumn')
        separator(h=10, p='selectArrayColumn')
        gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))
        attributeFirstSel=optionMenu( label='From')
        for each in getFirstAttr:
            menuItem( label=each)                
#        makeAttr=textField()
        makeAttr=cmds.optionMenu( label='To')               
        for each in getSecondAttr:
            cmds.menuItem( label=each)   
        cmds.gridLayout('txvaluemeter', p='selectArrayColumn', numberOfColumns=3, cellWidthHeight=(80, 18)) 
        cmds.text(label="1st min/max", w=80, h=25) 
        firstMinValue=cmds.textField(w=40, h=25, p='txvaluemeter', text="0")
        firstMaxValue=cmds.textField(w=40, h=25, p='txvaluemeter', text="1")  
        cmds.text(label="2nd min/max", w=80, h=25) 
        secondMinValue=cmds.textField(w=40, h=25, p='txvaluemeter', text="0")
        secondMaxValue=cmds.textField(w=40, h=25, p='txvaluemeter', text="1")
        gridLayout('BuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))             
        button (label='Go', p='BuildButtonLayout', command = lambda *args:self._conn_SDK_alias(firstMinValue=float(textField(firstMinValue,q=1, text=1)), firstMaxValue=float(textField(firstMaxValue,q=1, text=1)), secondMinValue=float(textField(secondMinValue,q=1, text=1)), secondMaxValue=float(textField(secondMaxValue,q=1, text=1)), getFirstattr=optionMenu(attributeFirstSel, q=1, v=1), floater=optionMenu(makeAttr, q=1, v=1)))
        showWindow(window)   
          
    def _conn_SDK_alias(self, firstMinValue, firstMaxValue, secondMinValue, secondMaxValue, getFirstattr, floater):
        getSel=ls(sl=1)
        getFirst=getSel[:-1]
        getSecond=getSel[-1]
        Controller=getSecond+"."+floater
        print Controller
        for each in getFirst:
            Child=each+"."+getFirstattr
            setAttr(Child, lock=0) 
            setAttr(Controller, secondMinValue)
            setAttr(Child,firstMinValue)
            setDrivenKeyframe(Child, cd=Controller)
            setAttr(Controller, secondMaxValue)
            setAttr(Child, firstMaxValue)
            setDrivenKeyframe(Child, cd=Controller)
            setAttr(Controller, secondMinValue)
            setAttr(Child, lock=1)  
            
    def _switch_driven_key_window(self, arg=None):
        getSel=cmds.ls(sl=1)        
        geteattr=cmds.listAttr (getSel[0], ud=1)        
        winName = "select attribute to link the switch constraint driven key to"
        winTitle = winName
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=300, h=100 )
        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=150)
        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        cmds.rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))
        attributeSel=cmds.optionMenu( label='user attribute')
        for each in geteattr:
            cmds.menuItem( label=each)            
        cmds.button (label='Go', p='listBuildButtonLayout', command = lambda *args:self._switch_driven_key(geteattr=cmds.optionMenu(attributeSel, q=1, v=1)))
        cmds.showWindow(window)   
                
    def _switch_driven_key(self, geteattr):
        getSel=cmds.ls(sl=1)
        if getSel:
            pass
        else:
            print "make sure to select a controller with a user attribute and an object with two constraints to switch between"
            return        
        Child=getSel[1]
        firstValue=0
        print firstValue
        secondValue=1
        print secondValue
        Wbucket=[]
        getChild=[(each) for each in cmds.listRelatives(Child, ad=1) if "Constraint" in each]
        print getChild
        for wach in getChild:
            childGetAttr=cmds.listAttr(wach)
            print childGetAttr
        for item in childGetAttr:
            if "W0" in item or "W1" in item :
                Wbucket.append(item)
        if Wbucket:
            print Wbucket
        else:
            print "not enough constraints on child object"
        child_one_constraint=getChild[0]+"."+Wbucket[0]  
        child_two_constraint=getChild[0]+"."+Wbucket[1] 
        print child_two_constraint+" is the first value"        
        print child_one_constraint+" is the second value"
#         geteattr=cmds.listAttr (getSel[0], ud=1, st="*IK")
#         getIKItem=[]
#         for item in geteattr:
#             getIKItem=item   
#         Controller=getSel[0]+"."+getIKItem
#         Controller=getSel[0]+"."+geteattr[0]
        Controller=getSel[0]+"."+geteattr
        print Controller+ " is the Control value I hook up to"
        Child=getChild[0]
        print Child+" is the attribute that is being driven"
        getClass.doubleSetDrivenKey_constraint(Controller, Child, child_one_constraint, child_two_constraint, firstValue, secondValue)


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
           

    def _add_id(self, queryColor):
        '''----------------------------------------------------------------------------------
        Common add to list function
        ----------------------------------------------------------------------------------'''  
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
        cmds.HypershadeWindow()
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

    def TR_SDKKeys(self):
        '''this sets sdk keys for selected'''
        selObj=cmds.ls(sl=1)
        Controller=selObj[0]
        #getAttrBucket=[]
        getAttr=cmds.listAttr(Controller, k=1, v=1)
        winName = "SDK"
        winTitle = winName
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)

        window = cmds.window(winName, title=winTitle, tbm=1, w=200, h=100 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=150)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        
        cmds.rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(110, 20))
        colMenu=cmds.optionMenu( label='Attributes')
        for each in getAttr:
            cmds.menuItem( label=each)            
        cmds.button (label='setSDKkeys', p='listBuildButtonLayout', command = lambda *args:self.TR_SDKKeys_funct(queryAttr=cmds.optionMenu(colMenu, q=1, v=1) ))
        cmds.showWindow(window)    
        
    def TR_SDKKeys_funct(self, queryAttr):
        selObj=cmds.ls(sl=1)
        Controller=selObj[0]
        ChildAttributes=(".tx", ".ty", ".tz" , ".rx", ".ry", ".rz") 
        ControllerAttributesHz="."+str(queryAttr)    
        for Child in selObj[1:]:
            for attribute in ChildAttributes:
                cmds.setDrivenKeyframe(Child+attribute, cd=Controller+ControllerAttributesHz)
                
                
    def turn_on_undo(self, arg=None):
        cmds.undoInfo(state=1)


    def visibility_UI(self, arg=None):
        winName = "visibility"
        winTitle = winName
        if cmds.window(winName, exists=True):
                deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=300, h=100 )
        menuBarLayout(h=30)
        rowColumnLayout  (' selectArrayRow ', nr=1, w=300)
        frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        columnLayout ('selectArrayColumn', parent = 'rMainRow')
        setParent ('selectArrayColumn')
        cmds.gridLayout('txvaluemeter', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 18)) 
        self.hideToggle=cmds.textField( w=40, h=25, p='txvaluemeter', text="polySphere*")
        button (label='eyedropper name', p='txvaluemeter', command = lambda *args:self.eye_dropper(hide))
        gridLayout('BuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))             
        button (label='Toggle name', p='BuildButtonLayout', command = lambda *args:self.visibility_name(hide=textField(self.hideToggle,q=1, text=1)))
        button (label='Toggle exclude peers', p='BuildButtonLayout', command = lambda *args:self.visibility_peers())
        button (label='Toggle children', p='BuildButtonLayout', command = lambda *args:self.visibility_children())
        button (label='Toggle leaf children', p='BuildButtonLayout', command = lambda *args:self.visibility_leaf_children())
        button (label='children off', p='BuildButtonLayout', command = lambda *args:self.visibility_children_off())        
        button (label='children on', p='BuildButtonLayout', command = lambda *args:self.visibility_children_on())
        showWindow(window)

    def eye_dropper(self, hide):
        selectedObject=cmds.ls(sl=1)
        objListLength=len(selectedObject)
        if objListLength:
            if objListLength >= 1:
                cmds.textField(self.hideToggle , e=1, text=selectedObject[0])  
        else:
            print "nothing selected"

    def visibility_name(self, hide):
        getAllList=ls(hide)
        for each in getAllList:
            self.toggleVis(each)

    def visibility_children(self, arg=None):
        selObj=cmds.ls(sl=1, fl=1)
        for each in selObj:
            getchildren=listRelatives(each, c=1)
            for eachChild in getchildren:
                self.toggleVis(eachChild)

    def visibility_children_on(self, arg=None):
        selObj=cmds.ls(sl=1, fl=1)
        for each in selObj:
            getchildren=listRelatives(each, c=1)
            for eachChild in getchildren:
                self.visOn(eachChild)

    def visibility_children_off(self, arg=None):
        selObj=cmds.ls(sl=1, fl=1)
        for each in selObj:
            getchildren=listRelatives(each, c=1)
            for eachChild in getchildren:
                self.visOff(eachChild)

    def visibility_leaf_children(self, arg=None):
        selObj=cmds.ls(sl=1, fl=1)
        for each in selObj:
            getchildren=listRelatives(each, c=1, ad=1)
            for eachChild in getchildren:
                self.toggleVis(eachChild)


    def visibility_peers(self, arg=None):
        selObj=cmds.ls(sl=1, fl=1)
        getpar=listRelatives(selObj[0], p=1)
        getchildren=listRelatives(getpar[0], c=1)
        for each in selObj:
            self.toggleVis(each)
        print "hi"
        excGrp=[(eachChild) for eachChild in getchildren for each in selObj if eachChild not in each]
        for eachChild in excGrp:
            # if str(each) != str(eachChild):
            self.toggleVis(eachChild)
      

    def toggleVis(self, foundObject):
        try:
            if foundObject.visibility.get()==1:
                foundObject.visibility.set(0)
            else:
                foundObject.visibility.set(1)  
        except:
            pass

    def visOn(self, foundObject):
        try:
            foundObject.visibility.set(1)
        except:
            pass

    def visOff(self, foundObject):
        try:
            foundObject.visibility.set(0)
        except:
            pass

    def saveAttributesWindow(self, arg=None): 
        selObj=ls(sl=1, fl=1, sn=1)
        if len(selObj)==1:
            pass
        elif len(selObj)<1:
            print "select something"
            return
        else:
            print "add one at a time"
            return
        getScenePath=cmds.file(q=1, location=1)
        getPathSplit=getScenePath.split("/")
        folderPath='\\'.join(getPathSplit[:-1])+"\\"        
        if "Windows" in OSplatform:
            print "windows"
            newfolderPath=re.sub(r'/',r'\\', folderPath)
        if "Linux" in OSplatform:
            print "Linux"
            newfolderPath=re.sub(r'\\',r'/', folderPath)
        folderBucket=[]

        winName = "Save attribute"
        winTitle = winName
        if cmds.window(winName, exists=True):
                deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=600, h=100 )
        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=600)
        cmds.frameLayout('bottomFrame', label='', lv=0, nch=1, borderStyle='in', bv=1, p='selectArrayRow')     
        cmds.gridLayout('topGrid', p='bottomFrame', numberOfColumns=1, cellWidthHeight=(480, 20))   
        text("Objects to save attributes from:")
        cmds.button (label='Add', p='topGrid', command = lambda *args:self._refresh_function())
        cmds.gridLayout('listBuildButtonLayout', p='bottomFrame', numberOfColumns=1, cellWidthHeight=(480, 20)) 
        cmds.text(label="")        
        fieldBucket=[]
        for each in selObj:
            objNameFile=newfolderPath+str(each)
            cmds.rowLayout  (' listBuildButtonLayout ', w=600, numberOfColumns=6, cw6=[400, 65, 65, 1, 1, 1], ct6=[ 'both', 'both', 'both',  'both', 'both', 'both'], p='bottomFrame')
            self.getName=cmds.textField(w=400, h=25, p='listBuildButtonLayout', text=objNameFile)
            cmds.button (label='Save', w=150, p='listBuildButtonLayout', command = lambda *args:self.saved_attributes(each, fileName=cmds.textField(self.getName, q=1, text=1)))
            cmds.button (label='Open folder', p='listBuildButtonLayout', command = lambda *args:self._open_defined_path(destImagePath=cmds.textField(self.getName, q=1, text=1)))
        cmds.showWindow(window)        


    def saved_attributes(self, each, fileName):   
        fileName=fileName+'.txt'     
        if "Windows" in OSplatform:    
            # folderPath='/'.join(fileName.split('/')[:-1])+"/"
            # printFolder=re.sub(r'/',r'\\', folderPath)       
            if not os.path.exists(fileName): os.makedirs(fileName) 
        if "Linux" in OSplatform:
            # folderPath='\\'.join(fileName.split('/')[:-1])+"\\"
            # print folderPath
            # printFolder=re.sub(r'\\',r'/', folderPath)
            # print printFolder
            open(fileName, 'w')
        attrValBucket=[]            
        getListedAttr=[(attrib) for attrib in listAttr (each, w=1, a=1, s=1,u=1) if "solverDisplay" not in attrib]
        for eachAttribute in getListedAttr:
            try:
                attrVal=getattr(each,eachAttribute).get()
                attrWithVal=str(eachAttribute)+":"+str(attrVal)
                attrValBucket.append(attrWithVal)
            except:
                pass
        fullString=str(attrValBucket)
        inp=open(fileName, 'w+') 
        for each in attrValBucket:
            inp.write(str(each)+'\n')
        inp.close()  
        print "saved as "+fileName

    def _refresh_function(self):
        selObj=ls(sl=1, fl=1, sn=1)
        if len(selObj)==1:
            pass
        elif len(selObj)<1:
            print "select something"
            return
        else:
            print "add one at a time"
            return
        getScenePath=cmds.file(q=1, location=1)
        getPathSplit=getScenePath.split("/")
        folderPath='\\'.join(getPathSplit[:-1])+"\\"        
        if "Windows" in OSplatform:
            newfolderPath=re.sub(r'/',r'\\', folderPath)
        if "Linux" in OSplatform:
            newfolderPath=re.sub(r'\\',r'/', folderPath)        
        for each in selObj:
            objNameFile=str(each)
            fullPathName=newfolderPath+objNameFile
            cmds.rowLayout  (' nlistBuildButtonLayout ', w=400, numberOfColumns=6, cw6=[400, 80, 80, 1, 1, 1], ct6=[ 'both', 'both', 'both',  'both', 'both', 'both'], p='bottomFrame')
            self.getName=cmds.textField(w=120, h=25, p='nlistBuildButtonLayout', text=fullPathName)
            cmds.button (label='Save', w=150, p='nlistBuildButtonLayout', command = lambda *args:self.saved_attributes(each, fileName=cmds.textField(self.getName, q=1, text=1)))
            cmds.button (label='Open folder', p='nlistBuildButtonLayout', command = lambda *args:self._open_defined_path(destImagePath=cmds.textField(self.getName, q=1, text=1)))


    def openAttributesWindow(self, arg=None):    
        # getScenePath=cmds.file(q=1, location=1)
        # getPathSplit=getScenePath.split("/")
        # folderPath='\\'.join(getPathSplit[:-1])+"\\"        
        # if "Windows" in OSplatform:
        #     newfolderPath=re.sub(r'/',r'\\', folderPath)
        # if "Linux" in OSplatform:
        #     newfolderPath=re.sub(r'\\',r'/', folderPath)
        # getPath=newfolderPath+"*.txt"
        # files=glob.glob(getPath)
        getScenePath=cmds.file(q=1, location=1)
        files, getPath, newfolderPath, filebucket=self.getWorkPath(getScenePath)    
        winName = "Open attributes"
        winTitle = winName
        openFolderPath=folderPath+"\\"   
        selObj=cmds.ls(sl=1, fl=1)
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=500, h=280 )
        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=500)
        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        cmds.rowLayout  (' rMainRow ', w=500, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=1, cellWidthHeight=(480, 20)) 
        cmds.button (label='refresh folder', p='listBuildButtonLayout', command = lambda *args:self.refresh_text()) 
        cmds.button (label='workpath', p='listBuildButtonLayout', command = lambda *args:self.refresh_work_text())      
        self.fileDropName=cmds.optionMenu( label='files')
        for each in filebucket:
            cmds.menuItem( label=each) 
        # cmds.button (label='Load', p='listBuildButtonLayout', command = lambda *args:self._load_defined_path(newfolderPath, grabFileName=cmds.optionMenu(self.fileDropName, q=1, v=1)))
        # cmds.button (label='Open folder', p='listBuildButtonLayout', command = lambda *args:self._open_work_folder())
        self.pathFile=cmds.textField(w=120, h=25, p='listBuildButtonLayout', text=newfolderPath+selObj[0]) 
        cmds.button (label='Load', p='listBuildButtonLayout', command = lambda *args:self.load_attributes(printFolder=cmds.textField(self.pathFile, q=1, text=1), grabFileName=cmds.optionMenu(self.fileDropName, q=1, v=1)))        
        cmds.button (label='Open folder', p='listBuildButtonLayout', command = lambda *args:self._open_defined_path(destImagePath=cmds.textField(self.pathFile, q=1, text=1)))         
        cmds.showWindow(window)

    def getWorkPath(self, getScenePath):
        filebucket=[]
        getPathSplit=getScenePath.split("/")
        folderPath='\\'.join(getPathSplit[:-1])+"\\"        
        if "Windows" in OSplatform:
            newfolderPath=re.sub(r'/',r'\\', folderPath)
        if "Linux" in OSplatform:
            newfolderPath=re.sub(r'\\',r'/', folderPath)
        getPath=newfolderPath+"*.txt"
        files=glob.glob(getPath)
        for each in files:
            if "Windows" in OSplatform:
                getfileName=each.split("\\")
            if "Linux" in OSplatform:
                getfileName=each.split("/")         
            getFile=getfileName[-1:][0]
            filebucket.append(getFile)         
        return files, getPath, newfolderPath, filebucket

    def refresh_work_text(self, arg=None):
        menuItems = cmds.optionMenu(self.fileDropName, q=True, ill=True)
        if menuItems:
            cmds.deleteUI(menuItems)
        getScenePath=cmds.file(q=1, location=1)
        files, getPath, newfolderPath, filebucket=self.getWorkPath(getScenePath)        
        cmds.optionMenu(self.fileDropName, e=1) 
        self.pathFile=cmds.textField(self.pathFile, e=1, text=newfolderPath) 
        for each in filebucket:
            menuItem(label=each, parent=self.fileDropName)

    def refresh_text(self, arg=None):
        menuItems = cmds.optionMenu(self.fileDropName, q=True, ill=True)
        if menuItems:
            cmds.deleteUI(menuItems)
        getPathSplit=cmds.textField(self.pathFile, q=1, text=1)
        files, getPath, newfolderPath, filebucket=self.getWorkPath(getPathSplit)  
        # folderPath=getPathSplit 
        # print folderPath
        # getPath=folderPath+"*.txt"
        # files=glob.glob(getPath)          
        cmds.optionMenu(self.fileDropName, e=1) 
        for each in filebucket:
            menuItem(label=each, parent=self.fileDropName)

    def _open_work_folder(self, arg=None):
        '''--------------------------------------------------------------------------------------------------------------------------------------
        This opens the workfolder for the current saved file - file must be saved for query. untitled will not prompt an open folder.
        --------------------------------------------------------------------------------------------------------------------------------------'''        
        getScenePath=cmds.file(q=1, location=1)
        getPathSplit=getScenePath.split("/")
        folderPath='\\'.join(getPathSplit[:-1])+"\\"
        self.opening_folder(folderPath)

    def opening_folder(self, folderPath):
        if "Windows" in OSplatform:
            folderPath=re.sub(r'/',r'\\', folderPath)
            os.startfile(folderPath)
        if "Linux" in OSplatform:
            newfolderPath=re.sub(r'\\',r'/', folderPath)
            os.system('xdg-open "%s"' % newfolderPath) 

    def _open_defined_path(self, destImagePath):
        folderPath='\\'.join(destImagePath.split("/")[:-1])+"\\"        
        self.opening_folder(folderPath)

    def _load_defined_path(self, newfolderPath, grabFileName):
        printFolder=newfolderPath+grabFileName     
        self.load_attributes(printFolder)

    def load_attributes(self, printFolder, grabFileName):
        # folderPath='\\'.printFolderjoin(printFolder.split("/")[:-1])+"\\"
        printFolder=printFolder+grabFileName
        print printFolder
        notAttr=["isHierarchicalConnection", "solverDisplay", "isHierarchicalNode", "publishedNodeInfo", "fieldScale_Position", "fieldScale", "fieldScale.fieldScale_Position"]    
        selObj=cmds.ls(sl=1, fl=1)
        for each in selObj:
            getListedAttr=[(attrib) for attrib in listAttr(each, k=1, s=1, iu=1, u=1, lf=1, m=0) for item in notAttr if item not in attrib]     
            if os.path.exists(printFolder):
                pass
            else:
                print printFolder+"does not exist"
                pass 
            List = open(printFolder).readlines()
            dirDict={}
            for aline in List: 
                print aline
                getKeyDict=aline.split(':')[0]
                getValueDict=aline.split(':')[1]
                makeDict={getKeyDict:getValueDict}
                dirDict.update(makeDict)
            for eachAttribute in getListedAttr:
                objectToQuery=ls(each)
                try:
                    getChangeAttr=getattr(objectToQuery[0], eachAttribute).get()
                    getTypeAttr=type(getChangeAttr)
                except:
                    pass
                for key, value in dirDict.items():
                    if key==eachAttribute:
                        value=getTypeAttr(value)
                        try:
                            setAttr(each+'.'+eachAttribute, value)
                            print str(each)+'.'+str(eachAttribute)+" set to " + str(value)
                        except:
                            pass

    def load_attributesV1(self, printFolder):
        print printFolder
        if "_attributes.txt" in printFolder:
            printFolder=printFolder
        # elif"_attributes" in printFolder:
        #     printFolder=printFolder+".txt"
        else:
            printFolder=printFolder+"_attributes.txt"
        notAttr=["isHierarchicalConnection", "solverDisplay", "isHierarchicalNode", "publishedNodeInfo"]    
        selObj=cmds.ls(sl=1, fl=1)
        for each in selObj:
            getListedAttr=[(attrib) for attrib in listAttr(each, k=1, s=1, iu=1, u=1, lf=1) for item in notAttr if item not in attrib]     
            if os.path.exists(printFolder):
                pass
            else:
                print printFolder+"does not exist"
                pass 
            List = open(printFolder).readlines()
            dirDict={}
            for aline in List: 
                print aline
                getKeyDict=aline.split(':')[0]
                getValueDict=aline.split(':')[1]
                makeDict={getKeyDict:getValueDict}
                dirDict.update(makeDict)
            for eachAttribute in getListedAttr:
                objectToQuery=ls(each)
                getChangeAttr=getattr(objectToQuery[0], eachAttribute).get()
                getTypeAttr=type(getChangeAttr)
                for key, value in dirDict.items():
                    if key==eachAttribute:
                        value=getTypeAttr(value)
                        try:
                            setAttr(each+'.'+eachAttribute, value)
                            print str(each)+'.'+str(eachAttribute)+" set to " + str(value)
                        except:
                            pass
