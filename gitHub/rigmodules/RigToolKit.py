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
OSplatform=platform.platform()
trans=[".tx", ".ty", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz"]  

python("playblast = None");

'''MG rigging modules'''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons Attribution 4.0 International 4.0 (CC BY 4.0)'
'http://creativecommons.org/licenses/by/4.0/'
# 'This work is licensed under a Creative Commons Attribution-ShareAlike 3.0 Australia (CC BY-SA 3.0 AU)'
# 'http://creativecommons.org/licenses/by-sa/3.0/au/'



scriptPath="//usr//people//elise-d//workspace//techAnimTools//personal//elise-d//rigModules"
sys.path.append(str(scriptPath))

getToolArrayPath=str(scriptPath)+"/Tools.py"
exec(open(getToolArrayPath))
toolClass=ToolFunctions()


getBasePath=str(scriptPath)+"/baseFunctions_maya.py"
exec(open(getBasePath))
getBaseClass=BaseClass()

#gtepiece=getfilePath.split("\\")
getguideFilepath='/'.join(gtepiece[:-2])+"/guides/"
sys.path.append(str(getguideFilepath))

getSAFilepath='/'.join(gtepiece[:-2])+"/selectArray/"
sys.path.append(str(getSAFilepath))

getrenamerFilepath='/'.join(gtepiece[:-2])+"/renamer/"
sys.path.append(str(getrenamerFilepath))

getValueFilepath='/'.join(gtepiece[:-2])+"/Values/"
sys.path.append(str(getValueFilepath))

getSSDArrayPath='/'.join(gtepiece[:-2])+"/SSD/"
sys.path.append(str(getSSDArrayPath))

getToolArrayPath='/'.join(gtepiece[:-2])+"/tools/"
sys.path.append(str(getToolArrayPath))

getScenePath=cmds.file(q=1, location=1)
getPathSplit=getScenePath.split("/")
folderPath='\\'.join(getPathSplit[:-1])+"\\"

closeWindow=[
            'CommandWindow', 
            'MayaWindow', 
            'shelfEditorWin', 
            'ColorEditor',
            'outlinerPanel1Window',
            'scriptEditorPanel1Window',
            'Rig_Tool_Kit',
            'selectArrayWindow']

class ToolKitUI(object):
    '''--------------------------------------------------------------------------------------------------------------------------------------
    Interface Layout
    --------------------------------------------------------------------------------------------------------------------------------------'''          
    def __init__(self, winName="Tool Kit"):
        self.winTitle = "Tool Kit"
        self.winName = winName

    def create(self):
        
        if cmds.window(self.winName, exists=True):
                cmds.deleteUI(self.winName)

        self.window = cmds.window(self.winName, title=self.winTitle, tbm=1, w=380, h=700 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=380)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')

        cmds.rowLayout  (' rMainRow ', w=380, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=1, p='selectArrayColumn')

        cmds.frameLayout('FileInterface', cll=1,bgc=[0.15, 0.15, 0.15], cl=0, label='File/session', lv=1, nch=1, borderStyle='out', bv=2, w=345, fn="tinyBoldLabelFont",p='selectArrayColumn') 
        cmds.gridLayout('listBuildButtonLayout', p='FileInterface', numberOfColumns=2, cellWidthHeight=(150, 20))      
        cmds.button (label='Outliner win',bgc=[0.65, 0.75, 0.75], p='listBuildButtonLayout', command = self.outlinerWindow_callup)  
        cmds.button (label='Help',bgc=[0.2, 0.2, 0.2],p='listBuildButtonLayout', command = self._help)
        cmds.button (label='Clean Interface',bgc=[0.2, 0.2, 0.2], p='listBuildButtonLayout', command = lambda *args:self.clear_superflous_windows())
        cmds.button (label='revert',bgc=[0.2, 0.2, 0.2], p='listBuildButtonLayout', command = self._revert)
        cmds.button (label='fix playblast',bgc=[0.2, 0.2, 0.2], p='listBuildButtonLayout', command = self._fix_playblast)
        cmds.button (label='fix undos',bgc=[0.2, 0.2, 0.2], ann="This turns undos back on", p='listBuildButtonLayout', command = self._turn_on_undo)   

        cmds.frameLayout('sep1', cll=1, bgc=[0.0, 0.0, 0.0], label='File/session', lv=0, nch=1, borderStyle='out', bv=5, p='selectArrayColumn')
        cmds.separator(h=1, p='sep1', bgc=[0.0, 0.0, 0.0]) 

        cmds.frameLayout('MiniRigs', bgc=[0.15, 0.15, 0.15], cll=1, label='Mini Rigs', lv=1, nch=1, borderStyle='out', bv=1, w=345, fn="tinyBoldLabelFont", p='selectArrayColumn') 
        cmds.gridLayout('MiniRigsButtonLayout', p='MiniRigs', numberOfColumns=2, cellWidthHeight=(150, 20))                  
        cmds.button (label='Guides Tool', bgc=[0.65, 0.75, 0.75], ann="This is the guide tool menu to build the guides that creates the MG rig system",p='MiniRigsButtonLayout', command = self._guides)
        cmds.button (label='Insert Grp/Clst/Jnt', bgc=[0.7, 0.7, 0.7], ann="Inserts a group or add a joint or cluster above or as an influence to a controller or object; zeroes out object. USES: set default position in a rig controller/use a deformer joint or cluster to set position of an object",  p='MiniRigsButtonLayout', command = self._grp_insert)
        cmds.popupMenu(button=1)
        cmds.menuItem  (label='Grp insert', command = self._grp_insert)
        cmds.menuItem  (label='Clstr insert', command = self._clstr_insert)
        cmds.menuItem  (label='Jnt insert', command = self._jnt_insert)  
        cmds.button (label='CurveRig', bgc=[0.55, 0.6, 0.6], ann="Isolated joints that control CVs along a curve with no IK or FK dependencies. Create a guide chain then use this to create a curve rig. USES: Tongue, worm, eyelash line rig", p='MiniRigsButtonLayout', command = self._curve_rig)    
        cmds.button (label='ChainRig', bgc=[0.55, 0.6, 0.6], ann="An FK/IK tail rig. Create a guide chain and then create a rig chain that has both IK/FK and a stretch attribute. USES: Rope rig", p='MiniRigsButtonLayout', command = self.chain_rig)    
        cmds.button (label='Multi Rivet', ann="places multiple rivets based on vert selection.", p='MiniRigsButtonLayout', command = self._rivet)             
        cmds.button (label='Multi Point', ann="places multiple point constrained locators based on vert selection.", p='MiniRigsButtonLayout', command = self._point_const)         
        cmds.button (label='Connect to Curve', ann="connects objects to a curve - select curve first and then objects",  p='MiniRigsButtonLayout',command = self._connect_to_curve)

        cmds.frameLayout('sep2', cll=1, bgc=[0.0, 0.0, 0.0], label='File/session', lv=0, nch=1, borderStyle='out', bv=5, p='selectArrayColumn')
        cmds.separator(h=1, p='sep2') 

        cmds.frameLayout('Tool', bgc=[0.15, 0.15, 0.15], cll=1, label='Tools', lv=1, nch=1, borderStyle='out', bv=1, w=345, fn="tinyBoldLabelFont", p='selectArrayColumn') 
        cmds.gridLayout('ToolButtonLayout', p='Tool', numberOfColumns=2, cellWidthHeight=(150, 20))  
        cmds.button (label='SelectArray Tool', bgc=[0.65, 0.75, 0.75], ann="Launches Select Array tool. Workspace for creating selections, sets and finding nodes in complicated scenes.", p='ToolButtonLayout', command = self._select_array) 
        cmds.button (label='Renamer Tool', bgc=[0.55, 0.6, 0.6], ann="Launches a renamer tool.",p='ToolButtonLayout', command = self._renamer)          
        cmds.button (label='Edit sets', bgc=[0.55, 0.6, 0.6], ann="Add and subtract selected objects/verts from a set", p='ToolButtonLayout', command = self._edit_sets_win)            
        cmds.button (label='Cull CVs', bgc=[0.55, 0.6, 0.6], ann="Reduce or multiply CVs in a particular order from a group of selected curves", p='ToolButtonLayout', command = self._remove_CV) 
        cmds.button (label='Plot vertex', bgc=[0.55, 0.6, 0.6], ann="Plots a locator along a vertex or face within keyframe range", p='ToolButtonLayout', command = self._plot_vert)
        cmds.button (label='Multi functions', bgc=[0.55, 0.6, 0.6],ann="this builds a constraint/extrude function on a group of selected items to the first selected item", p='ToolButtonLayout',  command = self._constraint_maker)                             
        cmds.button (label='Hidden Grp', bgc=[0.55, 0.6, 0.6], p='ToolButtonLayout', ann="A menu for toggle hiding in heirarchies" ,command = self._hidden)
        cmds.button (label='Copy To Grps', ann="Copy's object to group selected.",p='ToolButtonLayout', command = self._copy_into_grp)        
        cmds.button (label='MatchMatrix', p='ToolButtonLayout', ann="This will match the exact matrix of the first selection", command = self._match_matrix) 
        cmds.button (label='ResetSelected', p='ToolButtonLayout', ann="This will reset the selected to 0.0(transforms only - will not affect control box attributes)", command = self._reset_selected)
        cmds.button (label='Wipe Anim From Obj', ann="Resets all Ctrl on selected to zero. Wipes animation", p='ToolButtonLayout', command = self._remove_anim)           
        cmds.button (label='ShadeNetworkSel', ann="selects and networks the shader attribute in the hypershade based on object selected", p='ToolButtonLayout', command = self._shade_network)
        cmds.button (label='Duplicate Move', ann="this copies the first selected object to all positions of the sequential selected objects(EG: duplicated spheres placed on CVs along a curve)", p='ToolButtonLayout', command = self._dup_move) 

        cmds.frameLayout('sep3', cll=1, bgc=[0.0, 0.0, 0.0], label='File/session', lv=0, nch=1, borderStyle='out', bv=5, p='selectArrayColumn')
        cmds.separator(h=1, p='sep3') 

        cmds.frameLayout('ControllerFrameLayout', bgc=[0.15, 0.15, 0.15], cll=1, label='Controllers', lv=1, nch=1, borderStyle='out', bv=1, w=345, fn="tinyBoldLabelFont", p='selectArrayColumn') 
        cmds.gridLayout('ControllerButtonLayout', p='ControllerFrameLayout', numberOfColumns=2, cellWidthHeight=(150, 20)) 
        cmds.button (label='Controller', bgc=[0.55, 0.6, 0.6], ann="parent constraints to a controller.", p='ControllerButtonLayout', command = self._control)
        cmds.button (label='Shapes Tool', ann="Creates a predetermined controller shape, joint or locator at selection or at origin (if nothing selected)", bgc=[0.55, 0.6, 0.6], p='ControllerButtonLayout', command = self._make_shape)
        cmds.button (label='Colours', ann="Changes colors on a group of selected objects", bgc=[0.55, 0.6, 0.6], p='ControllerButtonLayout', command = self._change_colours)
        cmds.button (label='Combine Shapes', ann="Combines selected curves into a single shape", p='ControllerButtonLayout', command = self._group_shapes)   

        cmds.frameLayout('sep4', cll=1, bgc=[0.0, 0.0, 0.0], label='File/session', lv=0, nch=1, borderStyle='out', bv=5, p='selectArrayColumn')
        cmds.separator(h=1, p='sep4') 

        cmds.frameLayout('AttributesFrameLayout', bgc=[0.15, 0.15, 0.15], cll=1, label='Attributes', lv=1, nch=1, borderStyle='out', bv=1, w=345, fn="tinyBoldLabelFont", p='selectArrayColumn') 
        cmds.gridLayout('AttributeButtonLayout', p='AttributesFrameLayout', numberOfColumns=2, cellWidthHeight=(150, 20)) 
        cmds.button (label='Fetch Attribute', bgc=[0.65, 0.75, 0.75], ann="searches for attribute by name",  p='AttributeButtonLayout', command = self._findAttr_window)                                                         
        cmds.button (label='Fast Float', bgc=[0.55, 0.6, 0.6], ann="Add a simple 0-1 float attribute to selected",  p='AttributeButtonLayout',command = self._fast_float)
        # cmds.button (label='Fast Connect', bgc=[0.55, 0.6, 0.6], ann="Connect attributes between two selections",  p='AttributeButtonLayout',command = self._quickCconnect_window)
        cmds.button (label='Fast Attr Alias', bgc=[0.55, 0.6, 0.6], ann="Creates a float alias attributes from first selection to second(no min/max)",  p='AttributeButtonLayout',command = self._createAlias_window)                  
        cmds.button (label='Copy Single Attr', bgc=[0.55, 0.6, 0.6], ann="copies a singular attribute properties from one selection to another",  p='AttributeButtonLayout',command = self._quickCopy_single_Attr_window)
        cmds.button (label='Set Range Multi Attr', bgc=[0.55, 0.6, 0.6], ann="sets values within a set range on selected attribute(EG: randomize speed within a range between different dynamic settings)",  p='AttributeButtonLayout', command = self._range_attr_window)                                                         
        cmds.button (label='Copy Anim/Att', ann="transfers animation and attribute settings to another",  p='AttributeButtonLayout',command = self._transfer_anim_attr)
        cmds.button (label='Transfer Mass Attr', ann="Transfers attributes from one group of objects to another group of objects. Alternate a selections between objects to objects you want to transfer to. Not restricted to transform",  p='AttributeButtonLayout', command = self._tran_att)                                                         

        cmds.frameLayout('sep5', cll=1, bgc=[0.0, 0.0, 0.0], label='File/session', lv=0, nch=1, borderStyle='out', bv=5, p='selectArrayColumn')
        cmds.separator(h=1, p='sep5') 

        cmds.frameLayout('ModelFrameLayout', bgc=[0.15, 0.15, 0.15], cll=1, label='Modelling', lv=1, nch=1, borderStyle='out', bv=1, w=345, fn="tinyBoldLabelFont", p='selectArrayColumn') 
        cmds.gridLayout('ModelButtonLayout', p='ModelFrameLayout', numberOfColumns=2, cellWidthHeight=(150, 20))              
        cmds.button (label='Blend Groups', bgc=[0.7, 0.7, 0.7], ann="Blend a group of objects to another group of objects(needs to be same meshes in heirarchy). Select deformer group and then deformee group.", p='ModelButtonLayout', command = self._blend_grp)
        cmds.popupMenu(button=1)
        cmds.menuItem  (label='GrpToGrp', command = self._blend_grp)
        cmds.menuItem  (label='massBlend', command = self._mass_blend)
        cmds.menuItem  (label='GrpSearchAndBlend', command = self._srch_and_blend)        
        cmds.button (label='Reshape to Edge', bgc=[0.7, 0.7, 0.7], ann="aligns and deforms an object by continuous edge of one poly object to another (EG: aligning a vein to the surface of a leaf). 'Reshape to Edge' is better for cylindrical shapes, 'Reshape to Shape' is better for flat planes.", p='ModelButtonLayout', command = self._reshape_to_curve)
        cmds.popupMenu(button=1)
        cmds.menuItem  (label='Reshape to Edge', command = self._reshape_to_curve)
        cmds.menuItem  (label='Reshape to Shape', command = self._reshape_to_shape)
        cmds.button (label='PolyCheck', p='ModelButtonLayout', bgc=[0.55, 0.6, 0.6],ann="checks poles on mesh and highlights the vertices involved to check poly integrity", command = self._poly_check)
        cmds.button (label='Build curve', ann="Build a curve from selected items.", p='ModelButtonLayout', command = self._build_curve)
        cmds.button (label='Clean model', ann="Deletes history on a selected mesh and zeroes out transforms", p='ModelButtonLayout', command = self._clean_mod)           
        cmds.button (label='MirrorBlend', ann="(Face expressions)Creates a mirrored blend shape(X axis). Select the one sided blendShape and then select main object to operate.", p='ModelButtonLayout', command = self._mirror_blend) 

        cmds.frameLayout('sep6', cll=1, bgc=[0.0, 0.0, 0.0], label='File/session', lv=0, nch=1, borderStyle='out', bv=5, p='selectArrayColumn')
        cmds.separator(h=1, p='sep6') 

        cmds.frameLayout('ExtFolderFrameLayout', bgc=[0.15, 0.15, 0.15], cll=1, cl=1, label='External folders', lv=1, nch=1, borderStyle='out', bv=1, w=345, fn="tinyBoldLabelFont",p='selectArrayColumn') 
        cmds.gridLayout('ExtFolderButtonLayout', p='ExtFolderFrameLayout', numberOfColumns=2, cellWidthHeight=(150, 20)) 
        cmds.button (label='Save Attr/Anim', bgc=[0.55, 0.6, 0.6], ann="saves all attributes/animation keys into an external file into project",  p='ExtFolderButtonLayout', command = self._save_att) 
        cmds.button (label='Load Attr/Anim', bgc=[0.55, 0.6, 0.6], ann="loads attributes/animation keys from an external file into project",  p='ExtFolderButtonLayout', command = self._load_att)
        cmds.button (label='Change multi file contents',bgc=[0.2, 0.2, 0.2], ann="changes multiple file contents(EG: joint names within skin xml files).",  p='ExtFolderButtonLayout', command = self._changing_file_contents)  
        cmds.button (label='Change multi file names',bgc=[0.2, 0.2, 0.2], ann="changes multiple file names(EG: render images/version numbers).",  p='ExtFolderButtonLayout', command = self._changing_files)  
        cmds.button (label='Export multiple obj',bgc=[0.2, 0.2, 0.2], ann="Exports a group of selected objects as separate .obj files.",p='ExtFolderButtonLayout', command = self._exp_obj)                        
        cmds.button (label='Open Image Gimp',bgc=[0.2, 0.2, 0.2], ann="Select a texture node and this will open the texture file in gimp - change the file path in 'gimp' at the top to your local exe",p='ExtFolderButtonLayout', command = self._open_texture_file_gmp)  
        cmds.button (label='Open Work folder',bgc=[0.2, 0.2, 0.2], ann="Opens the folder in which the current open file is located. Refresh this interface if opening a new file elsewhere.",  p='ExtFolderButtonLayout', command = self._open_work_folder)  
        cmds.text (label='Author: Elise Deglau',w=120, al='left', p='selectArrayColumn', fn="smallObliqueLabelFont")      
        # cmds.text (label='http://creativecommons.org/licenses/by-sa/3.0/au/',w=500, al='left', fn="smallObliqueLabelFont", p='selectArrayColumn')      
        cmds.showWindow(self.window)


    def clear_superflous_windows(self, arg=None):
        '''----------------------------------------------------------------------------------
        This clears the interface of window clutter and puts display in wire to lower file load time
        ----------------------------------------------------------------------------------'''          
        windows = cmds.lsUI(wnd=1)
        getDeleteWindows=((each) for each in windows if each not in closeWindow)
        for each in getDeleteWindows:
            try:
                print each
                cmds.deleteUI(each, window=1)
            except:
                pass

    def outlinerWindow_callup(self, arg=None):    #################
        maya.mel.eval( "OutlinerWindow;" )

    def _copy_into_grp(self, arg=None):
        toolClass._copy_into_grp()

    def _build_curve(self, arg=None):
        getBaseClass.build_a_curve()

    def _fix_playblast(self, arg=None):
        # python("from mpc.maya.mpcPlayblast import mpcPlayblastMaya");
        # python("from mpc.maya.mpcPlayblast import mpcPlayblastFromHubInterface");
        # python("import maya.mel as mel");
        python("playblast = None");
        # python("playblastMel = None");

    def _point_const(self, arg=None): 
        toolClass._point_const()


    def _save_att(self, arg=None):
        toolClass.saveAttributesWindow()

    def _load_att(self, arg=None):
        toolClass.openAttributesWindow()

    def _exp_obj(self, arg=None):
        getBaseClass.expObj()

    def _reshape_to_curve(self, arg=None):
        toolClass.matchCurveShapes()

    def _reshape_to_shape(self, arg=None):
        toolClass.matchFullShape()

    def _connect_to_curve(self, arg=None):
        toolClass.connect_to_curve()

    def _control(self, arg=None):
        getBaseClass.controllerUI()

    def _blend_grp(self, arg=None):
        getBaseClass.blendGroupToGroup()

    def _mass_blend(self, arg=None):
        getBaseClass.blendMass()

    def _srch_and_blend(self, arg=None):
        getBaseClass.blendSearch()

    def _hidden(self, arg=None):
        toolClass.visibility_UI()

    def _remove_CV(self, arg=None):
        toolClass.cv_remove_window()
        
    def _mirror_transform(self, arg=None): 
        getBaseClass.mirrorXform()

    def _reset_selected(self, arg=None):
        toolClass._reset()
        
    def _match_matrix(self, arg=None):
        getBaseClass.xformmove()   

    def _shade_network(self, arg=None):
        toolClass._shade_network()

    def _rivet(self, arg=None):
        toolClass._rivet()

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
        #toolClass.chain_rig()
        chainpath=str(getRigModPath)+"/ChainWork.py"
        exec(open(chainpath))
        getChainClass=ChainRig()  
        getChainClass.build_chain()
            
    def _sets_win(self, arg=None):
        toolClass._sets_win()  
            
    def _edit_sets_win(self, arg=None):
        toolClass._edit_sets_win()
            
    def _material_namer(self, arg=None):
        import Material_UI
        reload (Material_UI)
        Material_UI.Mat_Namer()

    def _help(self, arg=None):
        import rgModhelp
        reload (rgModhelp)
        rgModhelp.helpClass()

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

    def _revert(self, arg=None):
        getFileToolFilepath='/'.join(gtepiece[:-2])+"/tools/revert.py"
        exec(open(getFileToolFilepath))
        getRevertClass=RevertUI()
        getRevertClass.create()

    def _poly_check(self, arg=None):
        getPolyToolFilepath='/'.join(gtepiece[:-2])+"/tools/polyChecker.py"
        exec(open(getPolyToolFilepath))
        getPolyClass=PolyUI()
        getPolyClass.create()

    def _changing_file_contents(self, arg=None):
        toolClass.change_file_countents_UI()        

    def _changing_files(self, arg=None):
        toolClass.change_file_UI()  

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

    def _curve_rig(self, arg=None):
        toolClass.curve_rig()

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
        toolClass.cleanModels()
        

    def _constraint_maker(self, arg=None):
        getmultifFilepath='/'.join(gtepiece[:-1])+"/multiFunctions.py"
        exec(open(getmultifFilepath))
        getMultiClass=MultiFunctionClass()

    def _make_shape(self, arg=None):
        getBaseClass.makeShape()

    def _mirror_object(self, arg=None):
        getBaseClass.mirrorObject()
        
    def _blink_sculpt(self, arg=None):
        getBaseClass.BlinkSculpt()
        
    def _dup_move(self, arg=None):
        getBaseClass.duplicateMove()
        

        
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

    def _clstr_insert(self, arg=None):
        getBaseClass.createClstr()


    def _jnt_insert(self, arg=None):
        getBaseClass.createJnt()
        
    def _mass_movecstr(self, arg=None):
        getBaseClass.massMove()

        
    def _load_ssd(self, arg=None):
        import SSD
        reload (SSD)
        SSD.ui()
        
    def _group_shapes(self, arg=None):
        getBaseClass.groupShapes()

    def _plot_vert(self, arg=None):
        toolClass.vertex_UI()

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


    def _turn_on_undo(self, arg=None):
        toolClass.turn_on_undo()

inst = ToolKitUI()
inst.create()


