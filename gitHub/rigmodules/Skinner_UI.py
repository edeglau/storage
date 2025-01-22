import maya.cmds as cmds
from functools import partial
from string import *
import re
import maya.mel
import os, subprocess, sys, platform
from os  import popen
from sys import stdin
import sys
#import win32clipboard
import operator

'''MG rigging modules'''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons Attribution 4.0 International 4.0 (CC BY 4.0)'
# 'This work is licensed under a Creative Commons Attribution-ShareAlike 3.0 Australia (CC BY-SA 3.0 AU)'
'http://creativecommons.org/licenses/by-sa/3.0/au/'

# infFolderPath="C:\\temp\\influences\\"
# xmlFolderPath="C:\\temp\\xmlskin\\"
filepath= os.getcwd()
sys.path.append(str(filepath))
getScenePath=cmds.file(q=1, location=1)
getPathSplit=getScenePath.split("/")
folderPath='\\'.join(getPathSplit[:-1])+"\\"
guideFolderPath=folderPath+"Guides\\"
infFolderPath=folderPath+"Influences\\"
xmlFolderPath=folderPath+"XMLskinWeights\\"

class SkinningUI(object):
    '''--------------------------------------------------------------------------------------------------------------------------------------
    Interface Layout
    --------------------------------------------------------------------------------------------------------------------------------------'''          
    def __init__(self, winName="Skin Modules"):
        self.winTitle = "Skin Modules"
        self.winName = winName

    def create(self):
        
        if cmds.window(self.winName, exists=True):
                cmds.deleteUI(self.winName)

        self.window = cmds.window(self.winName, title=self.winTitle, tbm=1, w=350, h=700 ,bgc=[.45, 0.3, 0.3])

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=350)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')

        cmds.rowLayout  (' rMainRow ', w=350, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')                
        cmds.gridLayout('listBuildButtonLayout' ,bgc=[.65, 0.55, 0.55], p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))
        cmds.text(label="External files", bgc=[.45, 0.3, 0.3]) 
        cmds.text(label="", bgc=[.45, 0.3, 0.3])                        
        cmds.button (label='ExportXMLweight',bgc=[.8, 0.7, 0.7], p='listBuildButtonLayout', ann="exports vertice weights to an xml file",command = self._expxml)
        cmds.button (label='ImportXMLweight', p='listBuildButtonLayout', ann="imports xml weights", command = self._impxml)
        cmds.button (label='Save Influence',  p='listBuildButtonLayout', ann="saves influence joints into an external file", command = self._save_inf)    
        cmds.button (label='Open Influence', p='listBuildButtonLayout', ann="imports influence joints from an xml file", command = self._open_inf)
        cmds.button (label='Edit File', p='listBuildButtonLayout', ann="alters external text files in a folder", command = self._alter_xml)
        cmds.text(label="", bgc=[.45, 0.3, 0.3])        
        cmds.text(label="Influence manipulation", bgc=[.45, 0.3, 0.3])  
        cmds.text(label="", bgc=[.45, 0.3, 0.3])          
        cmds.button (label='Name=1weight', p='listBuildButtonLayout', ann="will set a name type influence to 1.0(will not remove others)", command = self._assign_to_one_bone)    
        cmds.button (label='Name=0weight', p='listBuildButtonLayout', ann="will set a name type influence to 0.0(will not remove)", command = self._set_bone_type_zero)            
        cmds.button (label='Remove joint', p='listBuildButtonLayout', ann="This will remove all influences with a given name", command = self._remove_bone_type)    
        cmds.button (label='Isolate to joint', p='listBuildButtonLayout', ann="This will remove all influences without a given name and sets full ewight to given name", command = self._hammer)    
        cmds.button (label='Add joint', p='listBuildButtonLayout', ann="This will add a joint with a given name", command = self._add_joint)    
        cmds.button (label='Clean zero weights', p='listBuildButtonLayout', ann="This will remove unweighted bones from selected bind",command = self._mass_clean_influence)          
        cmds.text(label="Influence selection", bgc=[.45, 0.3, 0.3])     
        cmds.text(label="", bgc=[.45, 0.3, 0.3])        
        cmds.button (label='Select Influences', ann="This tool will grab all influences of a skinned mesh", p='listBuildButtonLayout', command = self._select_skinned_bones)    
        cmds.button (label='Select Opp Influences', ann="This tool will grab all opposite sided influences of a skinned mesh", p='listBuildButtonLayout', command = self._select_opp_skinned_bones)    
        cmds.button (label='Swap Rig Influences', ann="This tool will grab the same influences on another rig", p='listBuildButtonLayout', command = self._inf_rig_name)    
        cmds.button (label='Select Vertices', ann="This tool will grab all vertices of a joint", p='listBuildButtonLayout', command = self._select_skinned_verts)    
        cmds.button (label='Transfer Influence', ann="transfers influences from one mesh and adds to another mesh", p='listBuildButtonLayout', command = self._inf_transfer_sel)       
        cmds.text(label="", bgc=[.45, 0.3, 0.3])             
        cmds.text(label="Locking", bgc=[.45, 0.3, 0.3])
        cmds.text(label="", bgc=[.45, 0.3, 0.3])              
        cmds.button (label='LockBody', ann="lock all the all body influences", p='listBuildButtonLayout', command = self._lock_body)    
        cmds.button (label='LockFace', ann="lock all face influences", p='listBuildButtonLayout', command = self._lock_face)    
        cmds.button (label='LockLeft', ann="lock all the left side influences while weighting", p='listBuildButtonLayout', command = self._lock_left)    
        cmds.button (label='LockRight', ann="lock all the left side influences while weighting", p='listBuildButtonLayout', command = self._lock_right)    
        cmds.button (label='LockAll', ann="locks all influences", p='listBuildButtonLayout', command = self._lock_all)    
        cmds.button (label='UnlockAll', ann="unlocks all influences", p='listBuildButtonLayout', command = self._lock_none)
        cmds.text(label="Weight manipulation", bgc=[.45, 0.3, 0.3])         
        cmds.text(label="", bgc=[.45, 0.3, 0.3])                          
        cmds.button (label='CopyVertWeightMatched', ann="copies an overlapping selection of vertices that match up to carry the same skin(eyes to eyes)", p='listBuildButtonLayout', command = self._copy_even)    
        cmds.button (label='CopyVertWeightUnmatched', ann="copies an overlapping selection of vertices that don't match up to carry the same skin(overlapping clothes - works predictably on localized mesh.)", p='listBuildButtonLayout', command = self._copy_uneven)    
        cmds.button (label='CopyMeshWeightMatched', ann="transfers selected weights to another matched mesh(feet to feet)", p='listBuildButtonLayout', command = self._mesh_copy_even)    
        cmds.button (label='CopyMeshWeightUnMatched', ann="transfers selected weights to another unmatched mesh(feet to shoes)", p='listBuildButtonLayout', command = self._mesh_copy_uneven)    
#         cmds.button (label='WeightTopologyMatched', ann="transfers selected weights to another matched topology mesh", p='listBuildButtonLayout', command = self._wgt_transfer_sel_matched)       
        cmds.button (label='MassMirrorWeightMatched', ann="mirrors skinweights across mirrored mesh", p='listBuildButtonLayout', command = self._mirror_copy)           
#         cmds.button (label='rig skin transfer*', ann="select a skinned reference mesh(with rig present) and select an unskinned mesh and it transfers the skinned weights to another detected rig - intended for reskinning the same character", p='listBuildButtonLayout', command = self._skin_transfer)    
#         cmds.button (label='mass copy*', ann="copies all skin from one mesh group to another depending on short name matches", p='listBuildButtonLayout', command = self._mass_copy_weight)
        cmds.text(label="", bgc=[.45, 0.3, 0.3]) 
        cmds.text(label="Skin swap", bgc=[.45, 0.3, 0.3])
        cmds.text(label="", bgc=[.45, 0.3, 0.3])                   
        cmds.button (label='Reskin', ann="reskins a selected mesh. Reset dag pose, reapplies influences and saves and re-applies xml weights. Good for resetting skin after moving the mesh (EG: feet to ground)", p='listBuildButtonLayout', command = self._reskin)    
        cmds.button (label='Copy skin group to copy', ann="transfers skin/weights of the mesh group to group copy of the same mesh(skins copy of mesh). If needing to reskin entire character - no topology change.", p='listBuildButtonLayout', command = self._reskin_to_copy)    
        cmds.button (label='Copy skin mesh to copy', ann="transfers skin/weights of one mesh to copy", p='listBuildButtonLayout', command = self._reskin_to_copy_single)    
        cmds.button (label='Transfer Input Rig', ann="swaps the input from one rig to skincluster to another via name", p='listBuildButtonLayout', command = self._connect_inputs_rig)    
        cmds.button (label='Transfer Input Mesh', ann="inserts output of the deformers from one to another via selection (Mesh with connection then target)", p='listBuildButtonLayout', command = self._connect_inputs_mesh)    
        cmds.button (label='Transfer Output Mesh', ann="inserts the output of the mesh to deformer via selected meshes(Mesh with connection then target - rivet transfers)", p='listBuildButtonLayout', command = self._connect_inputs_geo)    
#         cmds.button (label='Transfer Output Mesh(world)', ann="connects worldMesh connection ouput from first selected mesh to second (matched topo - use for transferring rivets)", p='listBuildButtonLayout', command = self._connect_outputs)    
#         cmds.button (label='SkinTransferMatched', ann="transfers the influences and weights from one skin to another if the topology matches", p='listBuildButtonLayout', command = self._transfer_weight_inf_matched)    
        cmds.button (label='SkinTransferUnmatched', ann="transfers the influences and weights from one skin to another regardless of topology so long as they are similar in shape", p='listBuildButtonLayout', command = self._transfer_weight_inf_unmatched)  
        #cmds.button (label='mass single copy', ann="copies all skin from one mesh group to another depending on short name matches", p='listBuildButtonLayout', command = self._mass_copy_weight_single)
#         cmds.text(label="", bgc=[.45, 0.3, 0.3])             
#         cmds.text(label="hypergraph manipulation", bgc=[.45, 0.3, 0.3])        
#         cmds.text(label="", bgc=[.45, 0.3, 0.3]) 
#         cmds.button (label='MultiWorldMesh', ann="swaps multiple selected worldmeshes", p='listBuildButtonLayout', command = self._multi_world_mesh)    
#         cmds.button (label='WorldMeshDirect', ann="plugs in a single worldmesh to multiple plugs", p='listBuildButtonLayout', command = self._world_mesh_direct)     
        cmds.text(label="", bgc=[.45, 0.3, 0.3]) 
        cmds.text(label="other", bgc=[.45, 0.3, 0.3])                   
        cmds.text(label="", bgc=[.45, 0.3, 0.3])  
        cmds.button (label='Max skinning', p='listBuildButtonLayout', command = self._max_skinning_tools)    
        cmds.text(label="", bgc=[.45, 0.3, 0.3])  
        cmds.text (label='Author: Elise Deglau',w=120, al='left', p='selectArrayColumn')      
        cmds.showWindow(self.window)

    def _expxml(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.exportXMLSkinWeights()
        
    def _impxml(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.importXMLSkinWeights()
    def _inf_transfer_sel(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.transferInfluence_selection()
    def _wgt_transfer_sel_matched(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.grabWeightMatch()
        
    def _isolate_to_one_bone(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.isolateJointSkin()

    def _assign_to_one_bone(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.skinclusterOne()
    def _set_bone_type_zero(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.skinclusterZero()
    def _mass_clean_influence(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.MassCleanInfluence()
        
    def _remove_bone_type(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.jointInfluenceRemoveMult()
    def _add_joint(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.jointInfluenceAddMult()
    def _hammer(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.jointInfluenceHammer()
        
    def _alter_xml(self, arg=None):
        import bulkChangeXML
        reload (bulkChangeXML)
        getClass=bulkChangeXML.changeXML()
    def _save_inf(self, arg=None):
        import saveInfluences
        reload (saveInfluences)
        getClass=saveInfluences.savingInfluences()
        getClass.save_influences()
        
    def _open_inf(self, arg=None):
        import saveInfluences
        reload (saveInfluences)
        getClass=saveInfluences.savingInfluences()
        getClass.open_influence()
        
#     def _reskin(self, arg=None):
#         import saveInfluences
#         reload (saveInfluences)
#         getInfClass=saveInfluences.savingInfluences()
#         import baseFunctions_maya
#         reload (baseFunctions_maya)
#         getBaseClass=baseFunctions_maya.BaseClass()
#         getMesh=cmds.ls(sl=1, fl=1)
#         for each in getMesh:
#             getInfClass._save_influence_callup(infFolderPath, each)        
#             getBaseClass.exportXMLSkinWeights_callup(xmlFolderPath, each)
#             cmds.skinCluster(each, e=1, ub=1)
#             getInfClass.open_influence_callup(infFolderPath, each, getMesh)
#             getBaseClass.importXMLSkinWeights_callup(xmlFolderPath, each)
#             getSkinCluster=cmds.skinCluster(each, q=1, dt=1)
#             skinID, getInf=getBaseClass.skinClust(getSkinCluster, each)
#             cmds.select(each)
#             cmds.skinPercent(skinID, normalize=1)
    def _reskin(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.reskin()
    def _reskin_to_copy(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.weightInf_transfer_to_copy()
    def _reskin_to_copy_single(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.weightInf_transfer_to_copy_single()
    def _connect_outputs(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.outPutConnector()
    def _connect_inputs_geo(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.outPutConnector_mesh()
    def _connect_inputs_mesh(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.inPutConnector_mesh()
    def _connect_inputs_rig(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.inPutConnectorRig()
    def _inf_rig_name(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.selectNewRigSkinnedBones()
                    
    def _transfer_weight_inf_matched(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.grabInfWeightsMatch()
        
    def _transfer_weight_inf_unmatched(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.grabInfWeightsUnMatch()
    def _clear_bones(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.MassSkinClusterQuery()
    def _select_skinned_bones(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.selectSkinnedBones()
    def _select_opp_skinned_bones(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.selectOppSkinnedBones()
    def _select_skinned_verts(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.selectSkinnedVerts()
    def _mass_copy_weight(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.massCopyWeight()
    def _mass_copy_weight_single(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.massCopyWeightSingleToMass()
    def _transfer_select_inf(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.swapInfluenceSelect()
    def _skin_transfer(self, arg=None):
        import skinTransfer
        reload (skinTransfer)
        getClass=skinTransfer.skinTrans()
        getClass.performTransfer()
    def _mirror_skin(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.accMirrorWeights()
    def _lock_left(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.lockLeftWeights()
    def _lock_right(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.lockRightWeights()
    def _lock_body(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.lockBodyWeights()
    def _lock_face(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.lockFaceWeights()
    def _lock_all(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.lockAllWeights()
    def _lock_none(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.unLockWeights()
    def _world_mesh_direct(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.directWorldMeshConnect()
    def _copy_even(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.vertSkinCopyEven()
    def _copy_uneven(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.vertSkinCopyUneven()
    def _mirror_copy(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.mirrorCopyEven()
    def _mesh_copy_even(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.meshSkinCopyEven()
    def _mesh_copy_uneven(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.meshSkinCopyUnEven()
    def _multi_world_mesh(self, arg=None):
        import baseFunctions_maya
        reload (baseFunctions_maya)
        getClass=baseFunctions_maya.BaseClass()
        getClass.multipleWorldMeshConnect()
    def _max_skinning_tools(self, arg=None):
        maya.mel.eval( "MAXSkinWeightTool;" )


inst = SkinningUI()
inst.create()

