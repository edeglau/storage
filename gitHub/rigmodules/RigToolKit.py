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
getBaseClass=baseFunctions_maya.BaseClass()

sys.path.append(str(filepath))
import Tools
reload (Tools)
toolClass=Tools.ToolFunctions()

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
#        cmds.button (label='Build Biped', ann="This is the biped MG rig system - non-mirrored arms", bgc=[0.55, 0.55, 0.55], p='listBuildButtonLayout', command = self._rig_biped)
        cmds.button (label='Build BipedMirror', ann="This is the biped MG rig system - mirrored arms", bgc=[0.6, 0.65, 0.65], p='listBuildButtonLayout', command = self._rig_biped_mirror)
        cmds.button (label='Build Quad', ann="This is the Quad MG rig system", bgc=[0.6, 0.65, 0.65], p='listBuildButtonLayout', command = self._rig_quad)
        cmds.button (label='Face Hugger', ann="This is the Face Hugger rig", bgc=[0.45, 0.5, 0.5], p='listBuildButtonLayout', command = self._rig_face)                
        cmds.button (label='Skinning Tool', ann="This is the Skinning tool", bgc=[0.45, 0.5, 0.5], p='listBuildButtonLayout', command = self._skinning)        
        cmds.text(label="") 
        cmds.text(label="Mini rigs")          
        cmds.text(label="")              
        cmds.button (label='CurveRig', bgc=[0.45, 0.5, 0.5], ann="Isolated joints that control CVs along a curve with no IK or FK dependencies. Create a guide chain then use this to create a curve rig. USES: Tongue, worm, eyelash line rig", p='listBuildButtonLayout', command = self._curve_rig)    
        cmds.button (label='ChainRig', bgc=[0.45, 0.5, 0.5], ann="An FK/IK tail rig. Create a guide chain and then create a rig chain that has both IK/FK and a stretch attribute. USES: Rope rig", p='listBuildButtonLayout', command = self.chain_rig)    
        cmds.button (label='FinallingRig', bgc=[0.45, 0.5, 0.5], ann="Mini joint rigs. Creates a bone connected to a controller to be added to outfits or to a simple prop. Select object or vert to add. If using vert, the resulting joint needs to be added and weight painted", p='listBuildButtonLayout', command = self._finalling_rig)
        cmds.button (label='Grp insert', ann="Inserts a group above a controller or object, zeroes out object. USES: changing default position in a rig controller",  p='listBuildButtonLayout', command = self._grp_insert)          
        cmds.button (label='Rivet', ann="Surface constraint. Uses the common Rivet tool built by Michael Bazhutkin. (must have mel script installed in scripts folder), constrains a locator to two selected edges on a surface.", p='listBuildButtonLayout', command = self._rivet)             
        cmds.button (label='Rivet Obj', ann="Uses the common Rivet tool built by Michael Bazhutkin. Adds selected object to a new created rivet. Select two edges of one object and then the object you want to rivet to the first. USES: buttons", p='listBuildButtonLayout', command = self._rivet_obj)             
        cmds.button (label='Bone rivet', ann="Builds a rivet and parents a joint to that locator for skinning geometry to. USES: eyelashes", p='listBuildButtonLayout', command = self._bone_rivet) 
        cmds.button (label='Joint chain', ann="builds a simple bone chain based on guides. USES: insect leg chains with no prebuilt rig", p='listBuildButtonLayout', command = self._build_joints) 
        cmds.button (label='build IK', ann="Adds ik to handle. Select root bone, select end bone and select controller. Will parent ik handle to controller.", p='listBuildButtonLayout', command = self._build_ik)         
        cmds.button (label='Stretch IK',ann="select controller and ikhandle to link up and add stretch attribute.", p='listBuildButtonLayout', command = self._stretch_ik)    
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
        cmds.button (label='**Create Edit Grps', bgc=[0.33, 0.27, 0.30], ann="Creates edit groups.",p='listBuildButtonLayout', command = self._defEditGrp)
        cmds.button (label='Copy To Grps', ann="Copy's object to group selected.",p='listBuildButtonLayout', command = self._copy_into_grp)
        cmds.button (label='Wrap TA Groups', ann="Wrap objects under selection 2 group to selection 1.",p='listBuildButtonLayout', command = self._wrap_ta_grp)
        cmds.button (label='Wipe Anim From Obj', ann="Resets all Ctrl on selected to zero. Wipes animation", p='listBuildButtonLayout', command = self._remove_anim)   
        cmds.button (label='Nullify object', ann="Hides object and makes unkeyable. USES: hide locators from animators", p='listBuildButtonLayout', command = self._disappear)                               
        cmds.button (label='Mass Move', ann="moves first selected to second selected(mass select first and then where to move last)", p='listBuildButtonLayout', command = self._mass_movecstr)                               
        cmds.button (label='Plot vertex', ann="Plots a locator along a vertex or face within keyframe range", p='listBuildButtonLayout', command = self._plot_vert)                               
#        cmds.button (label='*Cleanup asset', bgc=[0.00, 0.22, 0.00], ann="Hides finalling rig locators in skinned asset file, switches wardrobe joint interpolation('Dressvtx' and 'Skirtvtx') to noflip. if char light present, reconstrains it to master", p='listBuildButtonLayout', command = self._clean_up)                               
#        cmds.button (label='*Cleanup rig', bgc=[0.00, 0.22, 0.00], ann="Hides stretch locators, hides and unkeyable shoulder, resets some attributes to no longer go in negative value(fingers)", p='listBuildButtonLayout', command = self._clean_up_rig)
#        cmds.button (label='*Wipe Anim From Asset', bgc=[0.00, 0.22, 0.00], ann="Resets all Ctrl to zero. Wipes animation", p='listBuildButtonLayout', command = self._reset_asset)                               
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

    def _rivet(self, arg=None):
        maya.mel.eval( "rivet;" )

    def _revert(self, arg=None):
        maya.mel.eval( "revert();" )

    def _mirror_blend(self, arg=None): 
        getBaseClass.mirrorBlendshape()
        
    def _set_any(self, arg=None):
        import FaceRig
        reload (FaceRig)
        getBaseClass=FaceRig.FaceSetup()    
        getBaseClass.TR_SDKKeys()   
                
    def _bone_rivet(self, arg=None): 
        toolClass._bone_rivet()
        
    def chain_rig(self, arg=None):
        toolClass.chain_rig()
            
    def _sets_win(self, arg=None):
        toolClass._sets_win()  
            
    def _edit_sets_win(self, arg=None):
        toolClass._edit_sets_win()
            
    def _material_namer(self, arg=None):
        import Material_UI
        reload (Material_UI)
        Material_UI.Mat_Namer()

    def _edit_nsets_win(self, arg=None):
        toolClass._edit_nsets_win()  

    def _open_texture_file_gmp(self, arg=None):
        toolClass._open_texture_file_gmp()
        
    def _open_work_folder(self, arg=None):
        toolClass._open_work_folder()           
            
    def _open_texture_file_ps(self, arg=None):
        toolClass._open_texture_file_ps()

        
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
        toolClass._eye_directions()
        
    def addEyeDir(self, arg=None):
        toolClass.addEyeDir()        

    def _rivet_obj(self, arg=None): 
        toolClass._rivet_obj()
        
    def _disappear(self, arg=None):
        toolClass._disappear()
                
    def char_light_cleanup(self):
        toolClass.char_light_cleanup()
               
    def _clean_up(self, arg=None):
        toolClass._clean_up
                            
    def _clean_up_rig(self, arg=None):
        toolClass._clean_up_rig()


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
        getBaseClass=Skinner_UI.SkinningUI()        

    def _select_array(self, arg=None):
        import selectArray
        reload (selectArray)
        selectArray.SelectionPalettUI()         
        
    def _tran_att(self, arg=None):
        getBaseClass.massTransfer()      

    def _reset_asset(self, arg=None):
        getBaseClass.clearAnim()    
        self.char_light_cleanup()    

    def _fast_float(self, arg=None):
        getBaseClass.fastFloat()

    def _blend_colour_window(self, arg=None):
        toolClass._blend_colour_window()
        
    def _quickCconnect_window(self, arg=None):
        toolClass._quickCconnect_window()

    def _quickCopy_single_Attr_window(self, arg=None):
        toolClass._quickCopy_single_Attr_window()
        
    def _createAlias_window(self, arg=None):
        toolClass._createAlias_window()

    def _transfer_anim_attr(self, arg=None):
        toolClass._transfer_anim_attr()

    def _findAttr_window(self, arg=None):  
        toolClass._findAttr_window()

    def _remove_anim(self, arg=None):
        toolClass._reset() 
        toolClass._erase_anim()

    def _erase_anim(self, arg=None):
        toolClass._erase_anim()

    def _reset(self, arg=None):
        toolClass._reset()          
                        
    def _copy_into_grp(self, arg=None):
        toolClass._copy_into_grp()

    def _createSDK_alias_window(self, arg=None):
        toolClass._createSDK_alias_window()     


    def _range_attr_window(self, arg=None):
        toolClass._range_attr_window()

    def _connSDK_alias_window(self, arg=None):
        toolClass._connSDK_alias_window()
                
    def _switch_driven_key_window(self, arg=None):
        toolClass._switch_driven_key()
        
    def _build_ik(self, arg=None):
        getBaseClass.buildIK()      
        
    def _build_joints(self, arg=None):
        getBaseClass.buildJointFunction_callup()   

    def _exp_obj(self, arg=None):
        getBaseClass.expObj()
        
    def _clean_mod(self, arg=None):
        getBaseClass.cleanModels()
        
    def _constraint_maker(self, arg=None):
        getBaseClass.constraintMaker()  
            
    def _make_shape(self, arg=None):
        getBaseClass.makeShape()

    def _mirror_object(self, arg=None):
        getBaseClass.mirrorObject()
        
    def _blink_sculpt(self, arg=None):
        getBaseClass.BlinkSculpt()
        
    def _curve_rig(self, arg=None):
        getBaseClass.curve_rig()
        
    def _finalling_rig(self, arg=None):
        import FinallingRig
        reload (FinallingRig)
        getBaseClass=FinallingRig.Finalling()
        
    def _stretch_ik(self, arg=None):
        toolClass._stretch_ik()
        
    def _stretch_ik_spline(self, arg=None):
        toolClass._stretch_ik_spline()
        
    def _sandwich_control(self, arg=None):
        getBaseClass.sandwichControl()
        
    def _grp_insert(self, arg=None):
        getBaseClass.createGrpCtrl()
        
    def _mass_movecstr(self, arg=None):
        getBaseClass.massMove()

        
    def _load_ssd(self, arg=None):
        import SSD
        reload (SSD)
        SSD.ui()
        
    def _group_shapes(self, arg=None):
        getBaseClass.groupShapes()

    def _plot_vert(self, arg=None):
        getBaseClass.plot_vert()


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


