import maya.cmds as cmds
from functools import partial
from string import *
import re
import maya.mel
import os, subprocess, sys, platform
from os  import popen
from sys import stdin
import subprocess
import os
from random import randint
import random
from pymel.core import *
#import win32clipboard
import operator
trans=[".tx", ".ty", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz"]  

'''MG rigging modules'''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons License'
'http://creativecommons.org/licenses/by-sa/3.0/au/'

photoshop = r"C:\\Program Files\\Adobe\\Adobe Photoshop CC 2014\\Photoshop.exe"
gimp="C:\\Program Files\\GIMP 2\\bin\\gimp-2.6.exe"


BbxName="eyeDirGuide"
BbxFilepath="G:\\_PIPELINE_MANAGEMENT\\Published\\maya\\"+BbxName+".ma"

getfilePath=str(__file__)
filepath= os.getcwd()

sys.path.append(str(filepath))
import baseFunctions_maya
reload (baseFunctions_maya)
getClass=baseFunctions_maya.BaseClass()

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

getScenePath=cmds.file(q=1, location=1)
getPathSplit=getScenePath.split("/")
folderPath='\\'.join(getPathSplit[:-1])+"\\"

      
class ToolKitUI(object):
    '''--------------------------------------------------------------------------------------------------------------------------------------
    Interface Layout
    --------------------------------------------------------------------------------------------------------------------------------------'''          
    def __init__(self, winName="Rig Tool Kit"):
        self.winTitle = "Rig Tool Kit"
        self.winName = winName

    def create(self):
        
        if cmds.window(self.winName, exists=True):
                cmds.deleteUI(self.winName)

        self.window = cmds.window(self.winName, title=self.winTitle, tbm=1, w=350, h=550 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=350)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')

        cmds.rowLayout  (' rMainRow ', w=350, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))
        cmds.text(label="Rig setup")          
        cmds.text(label="")  
        cmds.button (label='Guides Tool', ann="This is the guide tool menu to build the guides that creates the MG rig system", bgc=[0.7, 0.7, 0.7],p='listBuildButtonLayout', command = self._guides)
        cmds.button (label='Build Biped', ann="This is the biped MG rig system - non-mirrored arms", bgc=[0.55, 0.55, 0.55], p='listBuildButtonLayout', command = self._rig_biped)
        cmds.button (label='Build BipedMirror', ann="This is the biped MG rig system - mirrored arms", bgc=[0.6, 0.65, 0.65], p='listBuildButtonLayout', command = self._rig_biped_mirror)
        cmds.button (label='Build Quad', ann="This is the Quad MG rig system", bgc=[0.6, 0.65, 0.65], p='listBuildButtonLayout', command = self._rig_quad)
        cmds.button (label='Face Hugger', ann="This is the Face Hugger rig", bgc=[0.45, 0.5, 0.5], p='listBuildButtonLayout', command = self._rig_face)                
        cmds.button (label='Skinning Tool', ann="This is the Skinning tool", bgc=[0.45, 0.5, 0.5], p='listBuildButtonLayout', command = self._skinning)        
        cmds.text(label="Mini rigs")          
        cmds.text(label="")              
        cmds.button (label='CurveRig', bgc=[0.45, 0.5, 0.5], ann="Joints that control CVs along a curve. Create a guide chain and use this to create a curve rig", p='listBuildButtonLayout', command = self._curve_rig)    
        cmds.button (label='ChainRig', bgc=[0.45, 0.5, 0.5], ann="An FK/IK tail rig. Create a guide chain and then create a rig chain that has both IK/FK and a stretch attribute", p='listBuildButtonLayout', command = self.chain_rig)    
        cmds.button (label='FinallingRig', bgc=[0.45, 0.5, 0.5], ann="Mini joint rigs. Creates a bone connected to a controller to be added to outfits or to a simple prop. Select object or vert to add. If using vert, the resulting joint needs to be added and weight painted", p='listBuildButtonLayout', command = self._finalling_rig)
        cmds.button (label='Grp insert', ann="Inserts a group above a controller or object, zeroes out object",  p='listBuildButtonLayout', command = self._grp_insert)          
        cmds.button (label='Rivet', ann="Surface constraint. Uses the common Rivet tool built by Michael Bazhutkin. (must have mel script installed in scripts folder), constrains a locator to two selected edges on a surface.", p='listBuildButtonLayout', command = self._rivet)             
        cmds.button (label='Rivet Obj', ann="Uses the common Rivet tool built by Michael Bazhutkin. adds selected object to rivet.", p='listBuildButtonLayout', command = self._rivet_obj)             
        cmds.button (label='Bone rivet', ann="Builds a rivet and parents a joint to that locator", p='listBuildButtonLayout', command = self._bone_rivet) 
        cmds.button (label='Joint chain', ann="builds a simple bone chain based on guides", p='listBuildButtonLayout', command = self._build_joints) 
        cmds.button (label='build IK', ann="Adds ik to handle. Select root bone, select end bone and select controller. Will parent ik handle to controller", p='listBuildButtonLayout', command = self._build_ik)         
        cmds.button (label='Stretch IK',ann="select controller and ikhandle to link up and add stretch attribute", p='listBuildButtonLayout', command = self._stretch_ik)    
        cmds.button (label='Stretch IKspline', ann="adds a stretch to a spline IK", p='listBuildButtonLayout', command = self._stretch_ik_spline)    
        cmds.button (label='ConstraintMaker',ann="this builds a constraint on a group of selected items to the first selected item", p='listBuildButtonLayout',  command = self._constraint_maker)
        cmds.button (label='EyeDir', ann="Adds a curve to represent a pupil to the eye joint. Must have 'EyeOrient_*_jnt' in scene to parent to.", p='listBuildButtonLayout', command = self.addEyeDir)   
        cmds.button (label='Switch Constraint SDK', ann="Switch constraint SDK(used in switching a double constraint in IK/FK mode):select single item with two constraints and then select control item with user defined float in the attribute and connects an SDK switch for the two constraints",  p='listBuildButtonLayout',command = self._switch_driven_key_window)                  
        cmds.button (label='Blend Colour Switch', ann="Blend colour tool(used in blend IK to FK chains): Select a controller with a user attribute, a follow object, then a '0' rotate/scale leading object and a '1' rotate/scale leading object",  p='listBuildButtonLayout',command = self._blend_colour_window)
        cmds.text(label="") 
        cmds.text(label="Tools")
        cmds.text(label="")         
        cmds.button (label='Anim Tools', ann="This opens the animator tools menu", bgc=[0.1, 0.5, 0.5], p='listBuildButtonLayout', command = self._anim_tools)         
        cmds.button (label='Material tool', ann="This opens a material tool for manipulating and naming shaders and shader nodes" , bgc=[0.1, 0.5, 0.5], p='listBuildButtonLayout', command = self._material_namer)  
        cmds.button (label='Add to Body set', ann="This adds a selection to the MG named bodyset(used when adding wardrobe finalling controllers)", bgc=[0.45, 0.5, 0.5], p='listBuildButtonLayout', command = self._sets_win)
        cmds.button (label='Edit sets', ann="Add and subtract selected objects/verts from a set", bgc=[0.45, 0.5, 0.5], p='listBuildButtonLayout', command = self._edit_sets_win)            
        cmds.button (label='Edit Dyn sets', ann="Add and subtract selected objects/verts from a dynamic set", bgc=[0.45, 0.5, 0.5], p='listBuildButtonLayout', command = self._edit_nsets_win) 
        cmds.button (label='SDKAny', ann="Select your driving object and then a group of objects to set the driven. This detects the attribute from the driver you can select and sets a driven key on all transforms (tx, ty, tz, rx, ry, rz) of selected objects. Useful for setting predetermined phonemes in a facerig", bgc=[0.45, 0.5, 0.5],p='listBuildButtonLayout', command = self._set_any)               
        cmds.button (label='SelectArray Tool', ann="Launches Select Array tool. Workspace for creating selections, sets and finding nodes in complicated scenes.", bgc=[0.45, 0.5, 0.5], p='listBuildButtonLayout', command = self._select_array) 
        cmds.button (label='Renamer Tool', ann="Launches a renamer tool.", bgc=[0.45, 0.5, 0.5],p='listBuildButtonLayout', command = self._renamer)          
        cmds.button (label='Create Edit Grps', ann="Creates edit groups.",p='listBuildButtonLayout', command = self._defEditGrp)
        cmds.button (label='Copy To Grps', ann="Copy's object to group selected.",p='listBuildButtonLayout', command = self._copy_into_grp)
        cmds.button (label='Wrap TA Groups', ann="Wrap objects under selection 2 group to selection 1.",p='listBuildButtonLayout', command = self._wrap_ta_grp)
        cmds.button (label='Wipe Anim From Asset', ann="Resets all Ctrl to zero. Wipes animation", p='listBuildButtonLayout', command = self._reset_asset)                               
        cmds.button (label='Wipe Anim From Obj', ann="Resets all Ctrl to zero. Wipes animation", p='listBuildButtonLayout', command = self._remove_anim)   
        cmds.button (label='Nullify object', ann="Hides object and makes unkeyable", p='listBuildButtonLayout', command = self._disappear)                               
        cmds.button (label='Cleanup asset', ann="Hides finalling rig locators in skinned asset file, switches wardrobe joint interpolation('Dressvtx' and 'Skirtvtx') to noflip. if char light present, reconstrains it to master", p='listBuildButtonLayout', command = self._clean_up)                               
        cmds.button (label='Cleanup rig', ann="Hides stretch locators, hides and unkeyable shoulder, resets some attributes to no longer go in negative value(fingers)", p='listBuildButtonLayout', command = self._clean_up_rig)
        cmds.button (label='Move', ann="moves first selected to second selected(mass select first and then where to move last)", p='listBuildButtonLayout', command = self._mass_movecstr)                               
        cmds.button (label='Plot vertex', ann="Plots a locator along a vertex or face within keyframe range", p='listBuildButtonLayout', command = self._plot_vert)                               
        cmds.text(label="") 
        cmds.text(label="Controllers")
        cmds.text(label="")           
        cmds.button (label='Shapes Tool', ann="Creates a predetermined controller shape, joint or locator at selection or at origin (if nothing selected)", bgc=[0.45, 0.5, 0.5], p='listBuildButtonLayout', command = self._make_shape)
        cmds.button (label='Sandwich ctrl', bgc=[0.45, 0.5, 0.5], ann="Adds a helper control. (SDK=Set Driven Key). Sandwiches a controller between a selected controller and it's parent. Used for adding a set driven key to maintain a specific movement while the regular controller can be used as it's offset.", p='listBuildButtonLayout', command = self._sandwich_control)          
        cmds.button (label='Colours', ann="Changes colors on a group of selected objects",  bgc=[0.45, 0.5, 0.5], p='listBuildButtonLayout', command = self._change_colours)    
        cmds.button (label='Limits', ann="An interface for creating limits on rigs. Can globally set, load or reset a rig.", bgc=[0.45, 0.5, 0.5], p='listBuildButtonLayout', command = self._change_limit_values)    
        cmds.button (label='Combine Shapes', ann="Combines selected curves into a single shape", p='listBuildButtonLayout', command = self._group_shapes)   
        cmds.text(label="")  
        cmds.text(label="Attributes")          
        cmds.text(label="")  
        cmds.button (label='Fast Float', bgc=[0.45, 0.5, 0.5], ann="Add a simple 0-1 float attribute to selected",  p='listBuildButtonLayout',command = self._fast_float)
        cmds.button (label='Fast Connect', bgc=[0.45, 0.5, 0.5], ann="Connect attributes between two selections",  p='listBuildButtonLayout',command = self._quickCconnect_window)
        cmds.button (label='Fast Attr Alias', bgc=[0.45, 0.5, 0.5], ann="Creates a float alias attributes from first selection to second(no min/max)",  p='listBuildButtonLayout',command = self._createAlias_window)                  
        cmds.button (label='Fast SDK Alias', bgc=[0.45, 0.5, 0.5], ann="Creates and connects attribute between two objects, first attribute to a new attribute on the second with the option to set SDK",  p='listBuildButtonLayout',command = self._createSDK_alias_window)
        cmds.button (label='Fast SDK Connect', bgc=[0.45, 0.5, 0.5], ann="Connects between two attributes with the option to set SDK",  p='listBuildButtonLayout',command = self._connSDK_alias_window)
        cmds.button (label='Copy Single Attr', bgc=[0.45, 0.5, 0.5], ann="copies a singular attribute properties from one selection to another",  p='listBuildButtonLayout',command = self._quickCopy_single_Attr_window)
        cmds.button (label='Find Attribute', bgc=[0.45, 0.5, 0.5], ann="searches for attribute by name",  p='listBuildButtonLayout', command = self._findAttr_window)                                                         
        cmds.button (label='Set Range Multi Attr', bgc=[0.45, 0.5, 0.5], ann="sets same attribute across an object selection between a set range",  p='listBuildButtonLayout', command = self._range_attr_window)                                                         
        cmds.button (label='Copy All Attr', ann="transfers animation and attribute settings to another",  p='listBuildButtonLayout',command = self._transfer_anim_attr)
        cmds.button (label='Transfer Mass Attr', ann="Transfers attributes from one group of objects to another group of objects. Alternate a selections between  objects with attributes to other objects you want to transfer to. Useful to swap or transfer SDK",  p='listBuildButtonLayout', command = self._tran_att)                                                         
        cmds.text(label="Modelling")          
        cmds.text(label="")               
        cmds.button (label='MirrorObject', ann="Mirrors duplicate object across the X axis", p='listBuildButtonLayout', command = self._mirror_object)         
        cmds.button (label='Export multiple obj', ann="Exports a group of selected objects as separate .obj files.",p='listBuildButtonLayout', command = self._exp_obj)   
        cmds.button (label='Clean model', ann="Deletes history on a selected mesh and zeroes out transforms", p='listBuildButtonLayout', command = self._clean_mod)           
        cmds.button (label='MirrorBlend', ann="Creates a mirrored blend shape. Select blendShape and select main object.", p='listBuildButtonLayout', command = self._mirror_blend)              
        cmds.text(label="External folders")
        cmds.text(label="")                       
        cmds.button (label='Open Image PS', ann="Select a texture node and this will open the texture file in photoshop - change the file path in 'photohop' at the top to your local exe", p='listBuildButtonLayout', command = self._open_texture_file_ps)  
        cmds.button (label='Open Image Gmp', ann="Select a texture node and this will open the texture file in gimp - change the file path in 'gimp' at the top to your local exe",p='listBuildButtonLayout', command = self._open_texture_file_gmp)  
        cmds.button (label='Open Work folder', ann="Opens the folder in which the current open file is located. Refresh this interface if opening a new file elsewhere.",  p='listBuildButtonLayout', command = self._open_work_folder)  
        cmds.button (label='Add Revert', ann="Adds the revert (mel - Author: NextDesign - from Highend/Creative crash) script to the File drop down in Maya.", p='listBuildButtonLayout', command = self._revert)          
        cmds.button (label='stream swim', p='listBuildButtonLayout', command = self._load_ssd)  
        cmds.text (label='Author: Elise Deglau',w=120, al='left', p='selectArrayColumn')      
        cmds.text (label='http://creativecommons.org/licenses/by-sa/3.0/au/',w=500, al='left', p='selectArrayColumn')      
        cmds.text (label='available: https://github.com/edeglau/storage/tree/master/gitHub/',w=500, al='left', p='selectArrayColumn')      
        cmds.showWindow(self.window)
        
        
        
    def _set_any(self, arg=None):
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceSetup()    
        getClass.TR_SDKKeys()   
                
    def _bone_rivet(self, arg=None): 
        global RivetName
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
        cmds.button (label='Create Lash Rivet', p='listBuildButtonLayout', command = lambda *args:self._add_bone_rivet())        

    def _add_bone_rivet(self, arg=None):
        queryRivet=cmds.textField(RivetName, q=1, text=1)       
        selObj=cmds.ls(sl=1, fl=1)
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
        import ChainWork
        reload (ChainWork)
        result = cmds.promptDialog( 
                    title='Building a chainrig', 
                    message="Enter dimensions for chain - EG:", 
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
            getClass=ChainWork.ChainRig(nrz, nry, nrx, mainName, ControllerSize) 
            
    def _sets_win(self, arg=None):
        try:
            getallnames=cmds.ls("*:*BodyControl")
        except:
            print "No BodyControl set is present"
        getAllSets=[(each) for each in cmds.ls(typ="objectSet") if "BodyControl" in each]
        global setMenu
        winName = "Sets"
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
        setMenu=cmds.optionMenu( label='joints')
        for each in getAllSets:
            cmds.menuItem( label=each)        
        cmds.button (label='Add to set', p='listBuildButtonLayout', command = lambda *args:self._add_to_set())

        cmds.showWindow(window)
        
    def _mirror_blend(self, arg=None): 
        getBaseClass.mirrorBlendshape()       

    def _add_to_set(self, arg=None):
        querySet=cmds.optionMenu(setMenu, q=1, v=1)
        getSel=cmds.ls(sl=1)
        for each in getSel:
            cmds.sets(each, add=querySet)
            
    def _remove_from_set(self, arg=None):
        querySet=cmds.optionMenu(setMenu, q=1, v=1)
        getSel=cmds.ls(sl=1)
        for each in getSel:
            cmds.sets(each, rm=querySet)            
            
    def _add_to_nset(self, dropDownData):
        getSel=cmds.ls(sl=1)
        for each in getSel:
            cmds.select(dropDownData, add=1)
            maya.mel.eval( 'dynamicConstraintMembership "add";' )

    def _remove_from_nset(self, dropDownData):
        getSel=cmds.ls(sl=1)
        for each in getSel:
            cmds.select(dropDownData, add=1)
            maya.mel.eval( 'dynamicConstraintMembership "remove";' )            
            
    def _edit_sets_win(self, arg=None):
#         try:
#             getallnames=cmds.ls("*:*BodyControl")
#         except:
#             print "No BodyControl set is present"
        getAllSets=[(each) for each in cmds.ls(typ="objectSet") if "tweak" not in each]
        global setMenu
        winName = "Sets"
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
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=1, cellWidthHeight=(200, 20))
        setMenu=cmds.optionMenu( label='joints')
        for each in getAllSets:
            cmds.menuItem( label=each)        
        cmds.button (label='Add to set', p='listBuildButtonLayout', command = lambda *args:self._add_to_set())
        cmds.button (label='remove from set', p='listBuildButtonLayout', command = lambda *args:self._remove_from_set())

        cmds.showWindow(window)
            
    def _material_namer(self, arg=None):
        import Material_UI
        reload (Material_UI)
        Material_UI.Mat_Namer()

    def _edit_nsets_win(self, arg=None):
        titleName="Dynamic Sets"
        getAllSets=[(each) for each in cmds.ls(typ="dynamicConstraint")]
        self._sets_win(titleName, getAllSets)
        self._set_nbuttons()
        
        
    def _sets_win(self, titleName, getAllSets):
        winName = titleName
        winTitle = winName
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=550, h=100 )
        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=550)
        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        cmds.rowLayout  (' rMainRow ', w=550, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildLayout', p='selectArrayColumn', numberOfColumns=1, cellWidthHeight=(550, 20))
        setMenu=cmds.optionMenu( label='joints')
        for each in getAllSets:
            cmds.menuItem( label=each)        
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(275, 20))
        cmds.button (label='Add relatives', p='listBuildButtonLayout', command = lambda *args:self._add_to_nset(dropDownData=optionMenu(setMenu, q=1, v=1)))
        cmds.button (label='remove relatives', p='listBuildButtonLayout', command = lambda *args:self._remove_from_nset(dropDownData=optionMenu(setMenu, q=1, v=1)))
        cmds.showWindow(window)        

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

        
    def _guides(self, arg=None):
        import combinedGuides
        reload (combinedGuides)
        combinedGuides.GuideUI()
        
    def _renamer(self, arg=None):
        import renamer
        reload (renamer)
        renamer.myUI()    
            
    def _change_limit_values(self, arg=None):
        import LimitValues
        reload (LimitValues)
        LimitValues.ValueClass()
        
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
#        getSel=cmds.ls(sl=1)[0]
#        for each in trans:
#            cmds.setAttr(getSel+each, l=1)
#            cmds.setAttr(getSel+each, k=0)
    def _rivet_obj(self, arg=None): 
        selObj=cmds.ls(sl=1, fl=1)
        getFirst=selObj[:-1]
        constrainObj=selObj[-1]
        maya.mel.eval( "rivet" )
        getRiv=cmds.ls(sl=1)
        cmds.parent(constrainObj, getRiv)
    def _disappear(self, arg=None):
        getSel=cmds.ls(sl=1)
        for item in getSel:
            for each in trans:
#                 cmds.setAttr(item+each, l=1)
                cmds.setAttr(item+each, k=0)
                cmds.setAttr(item+".visibility", 0)
                
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

        
    def _revert(self, arg=None):
        maya.mel.eval( "revert();" )
        
    def _change_colours(self, arg=None):
        import Colours
        reload (Colours)
        Colours.ColourPalet()
        
    def _anim_tools(self, arg=None):
        import Anim_Tools
        reload (Anim_Tools)
        Anim_Tools.AnimMoveTools()

        
    def _rig_biped(self, arg=None):
        import RiggerUI
        reload (RiggerUI)
        RiggerUI.BipeddUI()
        
    def _rig_biped_mirror(self, arg=None):
        import BipedMirrorUI
        reload (BipedMirrorUI)
        BipedMirrorUI.BipeddUI()

    def _rig_quad(self, arg=None):
        import QuadRigUI
        reload (QuadRigUI)
        QuadRigUI.QuadUI()
            
    def _rig_face(self, arg=None):
        import Face_Rig_UI
        reload (Face_Rig_UI)
        Face_Rig_UI.FaceRigger()
                
    def _skinning(self, arg=None):
        import Skinner_UI
        reload (Skinner_UI)
        getClass=Skinner_UI.SkinningUI()        

    def _select_array(self, arg=None):
        import selectArray
        reload (selectArray)
        selectArray.SelectionPalettUI()         
        
    def _tran_att(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass() 
        getClass.massTransfer()      

    def _reset_asset(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass() 
        getClass.clearAnim()    
        self.char_light_cleanup()    

    def _fast_float(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass() 
        getClass.fastFloat()

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
        getFirst=getSel[:-1]
        print getFirst
        getSecond=getSel[-1] 
        print getSecond        
#        getFirst=getSel[0]      
#        getSecond=getSel[1] 
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
        cmds.text(label=getParent[0])
        cmds.text(label=getChildren[0])        
        attributeFirstSel=cmds.optionMenu( label='From')
        for each in getFirstAttr:
            cmds.menuItem( label=each) 
        attributeSecondSel=cmds.optionMenu( label='To')               
        for each in getSecondAttr:
            cmds.menuItem( label=each)                    
        cmds.button (label='Go', p='listBuildButtonLayout', command=lambda *args:self._copy_single_attr(getChildren, getParent))
        cmds.showWindow(window)   
        
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
                            getChangeAttr=getSecond+'.'+item                        
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
        getSel=ls(sl=1)     
        getFirst=getSel[0]
        global attributeFirstSel
        global makeAttr        
        getFirstAttr=listAttr (getFirst, w=1, a=1, s=1,u=1)      
        getFirstAttr=sorted(getFirstAttr)        
        winName = "find attributes"
        winTitle = winName
        if cmds.window(winName, exists=True):
                deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=450, h=100 )
        menuBarLayout(h=30)
        rowColumnLayout  (' selectArrayRow ', nr=1, w=450)
        frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        rowLayout  (' rMainRow ', w=450, numberOfColumns=6, p='selectArrayRow')
        columnLayout ('selectArrayColumn', parent = 'rMainRow')
        setParent ('selectArrayColumn')
        separator(h=10, p='selectArrayColumn')
        gridLayout('listBuildLayout', p='selectArrayColumn', numberOfColumns=1, cellWidthHeight=(450, 20))
        attributeFirstSel=optionMenu( label='Find')
        for each in getFirstAttr:
            menuItem( label=each)
        gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(225, 20))
        findAttr=textField(AttributeName, text="use a full or partial name EG:'translate'")
        button (label='Find', p='listBuildButtonLayout', command = lambda *args:self._find_att(getSel, getFirstattr=optionMenu(attributeFirstSel, q=1, ill=1), attribute=textField(findAttr, q=1, text=1)))
        makeAttr=textField(text="fill with number EG:'50' and applt attribute")
        button (label='Apply', p='listBuildButtonLayout', command = lambda *args:self._apply_att(getSel, getFirstattr=optionMenu(attributeFirstSel, q=1, ils=1), makeAttr=textField(makeAttr, q=1, text=1)))
        showWindow(window)   
        
    def _find_att(self, getSel, getFirstattr, attribute):
        collectAttr=[]
        for each in getFirstattr:
            find=menuItem(each, q=1, label=1)
            if attribute in find:
                collectAttr.append(find)
                select(getSel[0]+'.'+find)         
                optionMenu(attributeFirstSel, e=1, v=find)     
        select(getSel[0]+'.'+collectAttr[0], r=1)
        for each in collectAttr[1:]:
            select(getSel[0]+'.'+each, add=1)

    def _apply_att(self,getSel, getFirstattr, makeAttr):
        getAttri=optionMenu(attributeFirstSel, q=1, v=1)
        getChangeAttr=getattr(getSel[0],getAttri)
        try:
            makeAttr=float(makeAttr)
        except:
            print "field must have number"
        getChangeAttr.set(makeAttr)        

  
    def _remove_anim(self, arg=None):
        self._reset() 
        self._erase_anim()
       

    def _erase_anim(self, arg=None):
        getSel=ls(sl=1)
        getFirst=getSel
        for each in getFirst:
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
        getSel=ls(sl=1)
        getFirst=getSel
        for each in getFirst:
            getFirstattr=listAttr (each, w=1, a=1, s=1, u=1, m=0)
            for item in getFirstattr:
                if "." not in item:
                    if "scaleX" not in item and "scaleY" not in item and "scaleZ" not in item:
                        get=cmds.keyframe(each+'.'+item, q=1, kc=1)
                        if get>0:
                            setAttr(each+'.'+item, 0)
                    else:
                        setAttr(each+'.'+item, 1)
  
                    
                        
    def _copy_into_grp(self, arg=None):
        getSel=ls(sl=1)
        getFirst=getSel[:-1]
        getGrp=getSel[-1]
        for each in getFirst:
            newDupe=duplicate(each)
            parent(newDupe, getGrp)
            rename(newDupe[0], each)

    def _createSDK_alias_window(self, arg=None):
        getSel=ls(sl=1)  
        if len(getSel)>1:
            pass
        else:
            print "need to select 2 or more items" 
            return       
        getFirst=getSel[0]
        global attributeFirstSel
        global makeAttr   
        global firstMinValue
        global firstMaxValue
        global secondMinValue
        global secondMaxValue
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
        setParent ('selectArrayColumn')
        separator(h=10, p='selectArrayColumn')
        gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))
        attributeFirstSel=optionMenu( label='From')
        for each in getFirstAttr:
            menuItem( label=each)                
        makeAttr=textField()
        cmds.gridLayout('txvaluemeter', p='selectArrayColumn', numberOfColumns=3, cellWidthHeight=(80, 18)) 
        cmds.text(label="1st min/max", w=80, h=25) 
        self.firstMinValue=cmds.textField(w=40, h=25, p='txvaluemeter', text="0")
        self.firstMaxValue=cmds.textField(w=40, h=25, p='txvaluemeter', text="1")  
        cmds.text(label="2nd min/max", w=80, h=25) 
        self.secondMinValue=cmds.textField(w=40, h=25, p='txvaluemeter', text="0")
        self.secondMaxValue=cmds.textField(w=40, h=25, p='txvaluemeter', text="1")
        gridLayout('BuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))             
        button (label='Go', p='BuildButtonLayout', command = lambda *args:self._create_SDK_alias())
        showWindow(window)   
          
    def _create_SDK_alias(self, arg=None):
        getSel=ls(sl=1)
        firstMinValue=float(textField(self.firstMinValue,q=1, text=1))
        firstMaxValue=float(textField(self.firstMaxValue,q=1, text=1))
        secondMinValue=float(textField(self.secondMinValue,q=1, text=1))
        secondMaxValue=float(textField(self.secondMaxValue,q=1, text=1))
        getFirstattr=optionMenu(attributeFirstSel, q=1, v=1)
        floater=textField(makeAttr, q=1, text=1)
        getFirst=getSel[:-1]
        getSecond=getSel[-1]
        anAttr=addAttr([getSecond], ln=floater, min=0, max=1, at="double", k=1, nn=floater)
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
        gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))
        attributeFirstSel=optionMenu( label='From')
        for each in getFirstAttr:
            menuItem( label=each)                
        self.randomized=checkBox(label="randomize", ann="If on, number within range is randomized. If off, numbers will increment via percentage based on selection against the range")
        cmds.gridLayout('txvaluemeter', p='selectArrayColumn', numberOfColumns=3, cellWidthHeight=(80, 18)) 
        cmds.text(label="range", w=80, h=25) 
        self.firstMinValue=cmds.textField(w=40, h=25, p='txvaluemeter', text="0.0")
        self.firstMaxValue=cmds.textField(w=40, h=25, p='txvaluemeter', text="1.0")  
        gridLayout('BuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))             
        button (label='Go', p='BuildButtonLayout', command = lambda *args:self._range_attr(getSel, randomized=cmds.checkBox(self.randomized,q=True, value=1), getFirstattr=optionMenu(attributeFirstSel, q=1, v=1), firstMinValue=float(textField(self.firstMinValue,q=1, text=1)), firstMaxValue=float(textField(self.firstMaxValue,q=1, text=1))))
        showWindow(window)
        
    def _range_attr(self, getSel, randomized, getFirstattr, firstMinValue, firstMaxValue):
        if randomized==False:
            self._range_inc(getSel, getFirstattr, firstMinValue, firstMaxValue)
        else:
            self._range_random(getSel, getFirstattr, firstMinValue, firstMaxValue)
            
    
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

      

    def _connSDK_alias_window(self, arg=None):
        getSel=ls(sl=1)  
        if len(getSel)>1:
            pass
        else:
            print "need to select 2 or more items" 
            return       

        global attributeFirstSel
        global makeAttr   
        global firstMinValue
        global firstMaxValue
        global secondMinValue
        global secondMaxValue


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
        self.firstMinValue=cmds.textField(w=40, h=25, p='txvaluemeter', text="0")
        self.firstMaxValue=cmds.textField(w=40, h=25, p='txvaluemeter', text="1")  
        cmds.text(label="2nd min/max", w=80, h=25) 
        self.secondMinValue=cmds.textField(w=40, h=25, p='txvaluemeter', text="0")
        self.secondMaxValue=cmds.textField(w=40, h=25, p='txvaluemeter', text="1")
        gridLayout('BuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))             
        button (label='Go', p='BuildButtonLayout', command = lambda *args:self._conn_SDK_alias())
        showWindow(window)   
          
    def _conn_SDK_alias(self, arg=None):
        getSel=ls(sl=1)
        firstMinValue=float(textField(self.firstMinValue,q=1, text=1))
        firstMaxValue=float(textField(self.firstMaxValue,q=1, text=1))
        secondMinValue=float(textField(self.secondMinValue,q=1, text=1))
        secondMaxValue=float(textField(self.secondMaxValue,q=1, text=1))
        getFirstattr=optionMenu(attributeFirstSel, q=1, v=1)
        floater=optionMenu(makeAttr, q=1, v=1)
        getFirst=getSel[:-1]
        getSecond=getSel[-1]
        #anAttr=addAttr([getSecond], ln=floater, min=0, max=1, at="double", k=1, nn=floater)
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
        cmds.button (label='Go', p='listBuildButtonLayout', command = self._switch_driven_key)
        cmds.showWindow(window)   
                
    def _switch_driven_key(self, arg=None):
        getSel=cmds.ls(sl=1)
        if getSel:
            pass
        else:
            print "make sure to select a controller with a user attribute and an object with two constraints to switch between"
            return        
        geteattr=cmds.optionMenu(attributeSel, q=1, v=1)
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

    def _build_ik(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass() 
        getClass.buildIK()      
        
    def _build_joints(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass() 
        getClass.buildJointFunction_callup()   

    def _exp_obj(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.expObj()
    def _clean_mod(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.cleanModels()
    def _constraint_maker(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass() 
        getClass.constraintMaker()      
    def _make_shape(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.makeShape()

    def _mirror_object(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.mirrorObject()
        
    def _blink_sculpt(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.BlinkSculpt()
        
    def _curve_rig(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getit=baseFunctions_maya.BaseClass()
        getit.curve_rig()
        
    def _finalling_rig(self, arg=None):
        import FinallingRig
        reload (FinallingRig)
        getClass=FinallingRig.Finalling()
        
    def _stretch_ik(self, arg=None):
        getSel=cmds.ls(sl=1)
        if getSel:
            pass
        else:
            print "select a controller to add an attribute and an ikHandle"        
        Controller=getSel[0]
        ikHandle=getSel[1]
        import stretchIK
        reload (stretchIK)
        getIKClass=stretchIK.stretchIKClass()
        getIKClass.get_ik_chain(Controller, ikHandle)
        
    def _stretch_ik_spline(self, arg=None):
        getParentJoint=cmds.ls(sl=1)[0]
        if getParentJoint:
            pass
        else:
            print "select a parent joint and ik handle needs to be present"
        import stretchIK
        reload (stretchIK)
        getIKClass=stretchIK.stretchIKClass()
        getIKClass.stretchSpline(getParentJoint)
        
    def _sandwich_control(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.sandwichControl()
        
    def _grp_insert(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.createGrpCtrl()
    def _mass_movecstr(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.massMove()

        
    def _load_ssd(self, arg=None):
        import SSD
        reload (SSD)
        SSD.ui()
        
    def _group_shapes(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.groupShapes()

    def _plot_vert(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.plot_vert()


    def _defEditGrp(self, arg=None):
        import DefEditGrps
        reload (DefEditGrps)
        getgrp=DefEditGrps.myGrps() 
        getgrp.ta_grps()
        
    def _wrap_ta_grp(self, arg=None):
        import DefEditGrps
        reload (DefEditGrps)
        getgrp=DefEditGrps.myGrps()
        getgrp.grab_grp()  
        
                    #===========================================================
                    # remove numbers at beginning
                    #===========================================================
#                    s = re.sub(r"(^|\W)\d+", "", s)
                    #===========================================================
                    # remove all numbers
                    #===========================================================
#                    sub_Name=re.sub(r'\d[1-9]*', '', lognm) 

inst = ToolKitUI()
inst.create()


