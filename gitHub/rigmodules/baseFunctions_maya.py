'''
Created on Apr 8, 2014

@author: Elise
'''

'''MG rigging modules'''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons License'
'http://creativecommons.org/licenses/by-sa/3.0/au/'
from pymel.core import *
import maya.cmds as cmds
import sys, os, glob

import maya.mel
getdef=[".sx", ".sy", ".sz", ".rx", ".ry", ".rz", ".tx", ".ty", ".tz", ".visibility"]
getScenePath=cmds.file(q=1, location=1)
getPathSplit=getScenePath.split("/")
folderPath='\\'.join(getPathSplit[:-1])+"\\"
guideFolderPath=folderPath+"Guides\\"
infFolderPath=folderPath+"Influences\\"
xmlFolderPath=folderPath+"XMLskinWeights\\"
objFolderPath=folderPath+"Obj\\"

# getfilePath=str(__file__)
# filepath= os.getcwd()
# objFolderPath=folderPath+"Obj\\"
# gtepiece=getfilePath.split("\\")
# getSSDFilepath='\\'.join(gtepiece[:-2])+"\\SSD\\"

class BaseClass():

    def median_find(self, lst):
        even = (0 if len(lst) % 2 else 1) + 1
        half = (len(lst) - 1) / 2
        mysum= sum(sorted(lst)[half:half + even]) / float(even)
        return mysum

    def loadSS(self):
        '''this builds my swim stream basic window'''
        import SS
        reload (SS)
        getClass=SS.ui() 
    
    def loadSSD(self):
        '''this loads my swim stream deluxe window'''
        import SSD
        reload (SSD)
        getClass=SSD.ui()

    def cleanModels(self, arg=None):       
        winName = "Clean object"
        winTitle = winName
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=500, h=100 )
        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=500)
        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        cmds.rowLayout  (' rMainRow ', w=500, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(240, 20)) 
        cmds.button (label='clean+history', p='listBuildButtonLayout', command = lambda *args:self.cleanObjHist()) 
        cmds.button (label='clean', p='listBuildButtonLayout', command = lambda *args:self.cleanObj())      
        cmds.showWindow(window)

    def cleanObjHist(self):
        result = cmds.confirmDialog ( 
            title='Clean object', 
            message="Warning! Any Orig shape and history will be deleted on all selected objects!", 
            button=['Continue','Cancel'],
            defaultButton='Continue', 
            cancelButton='Cancel', 
            dismissString='Cancel' )
        if result == 'Continue':
            pass
        else:
            print "nothing collected"         
        self.cleaningFunctionCallup()
        self.clearHistoryCallup() 

    def cleanObj(self):
        self.cleaningFunctionCallup()

    def clearHistoryCallup(self):
        objSel=cmds.ls(sl=1, fl=1)
        for each in objSel:        
            cmds.delete(each, ch=1)
            print "deleted history on "+each
            try:
                getShapes=cmds.listRelatives(each, c=1, typ="shape")
                for item in getShapes:
                    if "Orig" in item:
                        item=cmds.ls(item)
                        cmds.delete(item[0])
                        print "deleted "+item[0]
                    if "output" in item:
                        item=cmds.ls(item)
                        cmds.rename(item[0], each+"Shape")
                        print "renamed "+item[0]+" to "+each+"Shape"
            except:
                print "Object has no shapes. Passing on cleaning shapes."

    def freeTheAttrs(self, each):
        getdef=[".sx", ".sy", ".sz", ".rx", ".ry", ".rz", ".tx", ".ty", ".tz", ".visibility"]
        for eachAttr in getdef:
            cmds.setAttr(each+eachAttr, lock=0)
            cmds.setAttr(each+eachAttr, cb=1)   
            cmds.setAttr(each+eachAttr, k=1) 
        print each+eachAttr+" is now visible in channel box"

            

    def cleaningFunctionCallup(self):
        '''this deletes history, smooths and unlocks normals, removes user defined attributes, unused shapes and freezes out transformes'''
        objSel=cmds.ls(sl=1, fl=1)
        # getparentObj=cmds.listRelatives(objSel, c=1)
        for each in objSel:
            getControllerListAttr=cmds.listAttr (each, ud=1)
            if getControllerListAttr:
                for eachAttr in getControllerListAttr:
                    try:
                        cmds.setAttr(each+"."+eachAttr, l=0)
                        print "unlocked "+each+"."+eachAttr 
                    except:
                        pass  
                    try:                      
                        cmds.deleteAttr(each+"."+eachAttr)
                        print "deleted "+each+"."+eachAttr                    
                    except:
                        pass
            try:
                cmds.makeIdentity(each, a=True, t=1, r=1, s=1, n=0)
                print "zeroed out transforms for "+each
            except:
                print "Object isn't a transform or has already had it's transform zeroed. Passing on zeroing out transforms"
            try:
                if ":" in each:
                    newName=each.split(":")[-1:]
                    cmds.rename(each, newName)
                    print "renamed "+str(each)+" to "+str(newName)  
            except:
                print "Object has clean name space"
                pass
            try:
                self.freeTheAttrs(each)                
            except:
                pass

    def cleaningFunctionCallupV1(self):
        '''this deletes history, smooths and unlocks normals, removes user defined attributes, unused shapes and freezes out transformes'''
        getdef=[".sx", ".sy", ".sz", ".rx", ".ry", ".rz", ".tx", ".ty", ".tz", ".visibility"]
        objSel=cmds.ls(sl=1, fl=1)
        # getparentObj=cmds.listRelatives(objSel, c=1)
        for each in objSel:
            getControllerListAttr=cmds.listAttr (each, ud=1)
            if getControllerListAttr:
                for eachAttr in getControllerListAttr:
                    try:
                        cmds.setAttr(each+"."+eachAttr, l=0)
                        print "unlocked "+each+"."+eachAttr 
                    except:
                        pass  
                    try:                      
                        cmds.deleteAttr(each+"."+eachAttr)
                        print "deleted "+each+"."+eachAttr                    
                    except:
                        pass
            try:
                cmds.makeIdentity(each, a=True, t=1, r=1, s=1, n=0)
                print "zeroed out transforms for "+each
            except:
                print "Object isn't a transform or has already had it's transform zeroed. Passing on zeroing out transforms"
            try:
                for eachAttr in getdef:
                    cmds.setAttr(each+eachAttr, lock=0)
                    cmds.setAttr(each+eachAttr, cb=1)   
                    cmds.setAttr(each+eachAttr, k=1)  
                    print each+eachAttr+" is now visible in channel box"
                if ":" in each:
                    newName=each.split(":")[-1:]
                    cmds.rename(each, newName)
                    print "renamed "+str(each)+" to "+str(newName)  
            except:
                print "Object has clean name space"
                pass              

    def cleanScene(self):
        '''this deletes history and freezes out transformes'''
        objSel=cmds.ls(sl=1)
        for each in objSel:
            cmds.makeIdentity(each, a=True, t=1, r=1, s=1, n=0)
            cmds.delete(each, ch=1)
            print str(each)+" now has rotation, translation and scale frozen and construction history has been wiped"
            
    def displayViewAnim(self):
        cmds.modelEditor("modelPanel4", e=1,allObjects=0)
        cmds.modelEditor("modelPanel4", e=1,polymeshes=1)
        cmds.modelEditor("modelPanel4", e=1,nurbsCurves=1)


    def expObj(self, arg=None): 
        selObj=ls(sl=1, fl=1, sn=1)
        if len(selObj)>0:
            pass
        else:
            print "select something"
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
        winName = "Save obj"
        winTitle = winName
        if cmds.window(winName, exists=True):
                deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=620, h=100 )
        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=620)
        cmds.frameLayout('bottomFrame', label='', lv=0, nch=1, borderStyle='in', bv=1, p='selectArrayRow')     
        cmds.gridLayout('topGrid', p='bottomFrame', numberOfColumns=1, cellWidthHeight=(620, 20))   
        cmds.gridLayout('listBuildButtonLayout', p='bottomFrame', numberOfColumns=1, cellWidthHeight=(600, 20)) 
        cmds.text(label="")        
        fieldBucket=[]
        cmds.rowLayout  (' listBuildButtonLayout ', w=600, numberOfColumns=6, cw6=[350, 40, 40, 40, 40, 1], ct6=[ 'both', 'both', 'both',  'both', 'both', 'both'], p='bottomFrame')
        self.getName=cmds.textField(h=25, p='listBuildButtonLayout', text=newfolderPath)
        cmds.button (label='Save', w=90, p='listBuildButtonLayout', command = lambda *args:self.expObj_callup(objFolderPath=cmds.textField(self.getName, q=1, text=1)))            
        cmds.button (label='Open folder', w=60, p='listBuildButtonLayout', command = lambda *args:self._open_defined_path(destImagePath=cmds.textField(self.getName, q=1, text=1)))
        cmds.showWindow(window)        


    def expObj_callup(self, objFolderPath):
        '''this loads the obj plugin and exports a group of selected obj'''
        if "Windows" in OSplatform:         
            if not os.path.exists(objFolderPath): os.makedirs(objFolderPath)
            cmds.pluginInfo("C://Program Files//Autodesk//Maya2015//bin//plug-ins//objExport.mll", e=1, autoload=True)  
            getname=cmds.ls(sl=1)
            cmds.select(cl=1)
            for each in getname:
                cmds.select(each)
                cmds.file(str(objFolderPath)+str(each)+".obj", f=1, options="groups=1;ptgroups=1;materials=1;smoothing=1;normals=1", typ="OBJ", es=1)
        if "Linux" in OSplatform:
            if not os.path.exists(objFolderPath): os.makedirs(objFolderPath)
            # cmds.pluginInfo("C://Program Files//Autodesk//Maya2015//bin//plug-ins//objExport.mll", e=1, autoload=True) 
            getname=cmds.ls(sl=1)
            cmds.select(cl=1)
            for each in getname:
                cmds.select(each)
                cmds.file(str(objFolderPath)+str(each)+".obj", f=1, options="groups=1;ptgroups=1;materials=1;smoothing=1;normals=1", typ="OBJexport", es=1)
            
    def expObjV1(self):
        '''this loads the obj plugin and exports a group of selected obj'''
        result = cmds.promptDialog( 
                    title='save Obj', 
                    message="Enter path", 
                    text=objFolderPath, 
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
        if "Windows" in OSplatform:    
            # folderPath='/'.join(fileName.split('/')[:-1])+"/"
            # printFolder=re.sub(r'/',r'\\', folderPath)       
            if not os.path.exists(objFolderPath): os.makedirs(objFolderPath)
        if "Linux" in OSplatform:
            print objFolderPath
            inp=open(objFolderPath, 'w+')
        cmds.pluginInfo("C:/Program Files/Autodesk/Maya2015/bin/plug-ins/objExport.mll", e=1, autoload=True)
#         getname=cmds.ls(sl=1, sn=1)
        getname=cmds.ls(sl=1)
        cmds.select(cl=1)
        for each in getname:
            cmds.select(each)
#             cmds.file(str(objFolderPath)+str(each)+".obj", f=1, options="groups=1;ptgroups=1;materials=0;smoothing=1;normals=1", typ="OBJ", pr=1, es=1)
            cmds.file(str(objFolderPath)+str(each)+".obj", f=1, options="groups=1;ptgroups=1;materials=1;smoothing=1;normals=1", typ="OBJ", es=1)

    def fastFloat(self):
        '''this creates a fast float attribute on selection'''
        titleText=('Fast Float Attribute'),                        
        messageText=("Enter name"), 
        textText=("On"), 
        float=self.makeDialog(titleText, messageText, textText)
        for each in ls(sl=1):
            cmds.addAttr([each], ln=float, min=0, max=1, at="double", k=1, nn=float)
    
    def transferInfluence_selection(self):
        selObj=cmds.ls(sl=1, fl=1)
        controlObj=selObj[0]
        targetObj=selObj[1]
        getSkinCluster=cmds.skinCluster(controlObj, q=1, dt=1)
        skinID, getInf=self.skinClust(getSkinCluster, controlObj)
        targetgetSkinCluster=cmds.skinCluster(targetObj, q=1, dt=1)
        targetskinID, targetgetInf=self.skinClust(targetgetSkinCluster, targetObj)        
        for each in getInf:
            try:
                cmds.skinCluster(targetskinID, e=1, ai=each)
            except:
                print each+" is already attached to "+targetObj
                pass



    def reskin(self, arg=None):
        getMesh=cmds.ls(sl=1, fl=1)
        for each in getMesh:
            self.fullSkin_callup(each)
            
            
    def fullSkin_callup(self, each):
        '''selects the joint influences and reapplies to same mesh(for mesh changes)'''
        selObj=cmds.ls(sl=1, fl=1)
        for each in selObj:
            getSkinCluster=cmds.skinCluster(each, q=1, dt=1)
            skinID, getInf=self.skinClust(getSkinCluster, each)
            self.exportXMLSkinWeights_callup(xmlFolderPath, each)
            cmds.skinCluster(each, e=1, ub=1)
            cmds.select(getInf[0])
            for item in getInf[1:]:
                cmds.select(item, add=1)
            cmds.select(each, add=1)
            cmds.skinCluster(tsb=1)
            self.importXMLSkinWeights_callup(xmlFolderPath, each)
            skinID, getInf=self.skinnedBones(each)
            cmds.select(each)
            cmds.skinPercent(skinID, normalize=1)            
        

#     def fullSkin_callupV1OLD(self, each):
#         import saveInfluences
#         reload (saveInfluences)
#         getInfClass=saveInfluences.savingInfluences()        
#         getInfClass._save_influence_callup(infFolderPath, each)        
#         self.exportXMLSkinWeights_callup(xmlFolderPath, each)
#         cmds.skinCluster(each, e=1, ub=1)
#         getInfClass.open_influence_callup(infFolderPath, each, getMesh)
#         self.importXMLSkinWeights_callup(xmlFolderPath, each)
#         skinID, getInf=self.skinnedBones(each)
#         cmds.select(each)
#         cmds.skinPercent(skinID, normalize=1)

    def weightInf_transfer_to_copy(self):
        getControlObject, getTargetObject=self.getGroupedMesh_controller_target()
        self.weightInf_transfer_to_copy_callup(getControlObject, getTargetObject)

    def weightInf_transfer_to_copy_callup(self, getControlObject, getTargetObject):     
        '''weight transfer from a group to another group'''
        for eachControlItem, eachTargetItem in map(None, getControlObject, getTargetObject):         
            try:
                getSkinCluster=cmds.skinCluster(eachControlItem, q=1, dt=1)
                skinID, getInf=self.skinClust(getSkinCluster, eachControlItem)
                self.exportXMLSkinWeights_callup(xmlFolderPath, eachControlItem)
                cmds.select(getInf[0])
                for item in getInf[1:]:
                    cmds.select(item, add=1)
                cmds.select(eachTargetItem, add=1)
                try:
                    cmds.skinCluster(tsb=1)
                except:
                    print eachTargetItem+" already has a skincluster. passing"
                    pass          
                self.importXMLSkinWeights_callup(xmlFolderPath, eachTargetItem)
                skinID, getInf=self.skinnedBones(eachTargetItem)
                cmds.select(eachTargetItem)
                cmds.skinPercent(skinID, normalize=1)
            except:
                print eachControlItem+" missing influences. passing"
                pass     
 

    def weightInf_transfer_to_copy_single(self):
        '''weight transfer from selection of items'''
        getMesh=cmds.ls(sl=1)
        if len(getMesh)<2:
            print "select a skinned mesh group and an unskinned target mesh group"
            return
        else:
            pass        
        for eachController, eachChild in map(None, getMesh[::2], getMesh[1::2]): 
            print "attempting to copy from "+eachController+" to "+eachChild
            try:
                getSkinCluster=cmds.skinCluster(eachController, q=1, dt=1)
                pass
            except:
                print eachController+" missing influences. passing"
                pass               
            skinID, getInf=self.skinClust(getSkinCluster, eachController)
            self.exportXMLSkinWeights_callup(xmlFolderPath, eachController)
            cmds.select(getInf[0])
            for item in getInf[1:]:
                cmds.select(item, add=1)
            cmds.select(eachChild, add=1)
            try:
                cmds.skinCluster(tsb=1)
            except:
                print eachChild+" already has a skincluster. passing"
                pass
            self.importXMLSkinWeights_callup(xmlFolderPath, eachChild)
            skinID, getInf=self.skinnedBones(eachChild)
            cmds.select(eachChild)
            cmds.skinPercent(skinID, normalize=1) 
 
            
#     def weightInf_transfer_to_copy_singleV1(self):
#         getMesh=cmds.ls(sl=1)
#         if len(getMesh)<2:
#             print "select a skinned mesh group and an unskinned target mesh group"
#             return
#         else:
#             pass        
#         import saveInfluences
#         reload (saveInfluences)
#         getInfClass=saveInfluences.savingInfluences()  
#         for eachController, eachChild in map(None, getMesh[::2], getMesh[1::2]): 
#             print "attempting to copy from "+eachController+" to "+eachChild
#             try:
#                 getInfClass._save_influence_callup(infFolderPath, eachController)   
#                 getInfClass.open_influence_callup(infFolderPath, eachChild)
#                 self.exportXMLSkinWeights_callup(xmlFolderPath, eachController)
#                 self.importXMLSkinWeights_callup(xmlFolderPath, eachChild)
#                 skinID, getInf=self.skinnedBones(eachChild)
#                 cmds.select(eachChild)
#                 cmds.skinPercent(skinID, normalize=1)   
#             except:
#                 print eachController+"missing influences. passing"
#                 pass        
#     def weightInf_transfer_to_copy_callupV1(self, getControlObject, getTargetObject):
#         import saveInfluences
#         reload (saveInfluences)
#         getInfClass=saveInfluences.savingInfluences()       
#         for eachControlItem, eachTargetItem in map(None, getControlObject, getTargetObject):         
#             try:
#                 getInfClass._save_influence_callup(infFolderPath, eachControlItem)   
#                 getInfClass.open_influence_callup(infFolderPath, eachTargetItem)
#                 self.exportXMLSkinWeights_callup(xmlFolderPath, eachControlItem)
#                 self.importXMLSkinWeights_callup(xmlFolderPath, eachTargetItem)
#                 skinID, getInf=self.skinnedBones(eachTargetItem)
#                 cmds.select(eachTargetItem)
#                 cmds.skinPercent(skinID, normalize=1)   
#             except:
#                 print eachControlItem+"missing influences. passing"
#                 pass            

    def vertSkinCopyUneven(self):
#         cmds.copySkinWeights(nm=1,sa="closestComponent",ia="closestJoint", nr=1)
        cmds.copySkinWeights(nm=1,sa="rayCast",ia="closestJoint", nr=1)

    def vertSkinCopyEven(self):
        cmds.copySkinWeights(nm=1, sa="closestComponent", ia="oneToOne", nr=1)
        
    def meshSkinCopyEven(self): 
        cmds.copySkinWeights(nm=1, sa="closestPoint", ia="closestJoint")
        
    def meshSkinCopyUnEven(self): 
        cmds.copySkinWeights(nm=1, sa="closestPoint", ia="closestBone")
        
    def mirrorCopyEven(self):
        selObj=cmds.ls(sl=1, fl=1)
        for each in selObj:
            getSkinCluster=cmds.skinCluster(each, q=1, dt=1)
            skinID, getInf=self.skinClust(getSkinCluster, each)  
#             cmds.copySkinWeights(ss=skinID, ds=skinID, mm="YZ", mi=1, sa="closestPoint", ia="oneToOne", nr=1)
            cmds.copySkinWeights(ss=skinID, ds=skinID, mm="YZ", mi=1, sa="rayCast", ia="oneToOne", nr=1)
        

    def grabInfluence(self):
        getControlObject, getTargetObject=self.getTargetControl()
        self.grabInfluence_callup(getControlObject, getTargetObject)
        
    def grabWeightMatch(self):
        getControlObject, getTargetObject=self.getTargetControl()
        self.grabweightMatch_callup(getControlObject, getTargetObject)

    def grabInfWeightsMatch(self):
        getControlObject, getTargetObject=self.getTargetControl()
        self.grabInfluence_callup(getControlObject, getTargetObject)
        self.grabweightMatch_callup(getControlObject, getTargetObject)
        
    def grabInfWeightsUnMatch(self):
        getControlObject, getTargetObject=self.getTargetControl()
        self.grabInfluence_callup(getControlObject, getTargetObject)
        cmds.select(getControlObject)
        cmds.select(getTargetObject, add=1)
        self.vertSkinCopyUneven()

    def getTargetControl(self):
        selObj=cmds.ls(sl=1, fl=1)
        getControlObject=[selObj[0]]
        getTargetObject=[selObj[1]]
        return getControlObject, getTargetObject
       
    def grabInfluence_callup(self, getInfluenceObject, getTargetObject):
        getBones=self.bagOfBones(getInfluenceObject)
        try:
            getSkinCluster=cmds.skinCluster(getTargetObject, q=1, dt=1)
            skinID, getInf=self.skinClust(getSkinCluster, getTargetObject)
            if len(skinID)>0:
                for each in getBones:
                    cmds.skinCluster(getTargetObject, e=1, ai=each)
                    #cmds.skinCluster(str(skinID), e=1, ai=each)  
        except:
            cmds.select(getBones)
            cmds.select(getTargetObject, add=1)
            try:
                cmds.skinCluster()
                for each in getBones:
                    try:
                        print "bound "+each+" to "+getTargetObject
                    except:
                        pass        
            except:
                pass
        
    def grabweightMatch_callup(self, getWeightedObject, getTargetObject):
        self.exportXMLSkinWeights_callup(xmlFolderPath,getWeightedObject)
        for each, item in map(None, getWeightedObject, getTargetObject):
            self.grabweightMatchMulti_callup(each, item )

    def grabweightMatchMulti_callup(self, each, item):
        self.exportXMLSkinWeights_callup(xmlFolderPath,each)
        getCtrlItemName=each.split(":")
        getTgtItemName=item.split(":")
        getControlMesh=getCtrlItemName[-1:]
        getTargetMesh= getTgtItemName[-1:]    
        fleName =getControlMesh[0]+".xml"   
        pathText=xmlFolderPath+fleName
#             newPathText=xmlFolderPath+getTargetMesh+".xml"
        try:
            newname, skinID=getClass.getSkinWeightsforXML(each)
            cmds.deformerWeights (newname+".xml", p=xmlFolderPath,  ex=True, deformer=skinID)
            print "deformer weights have been exported from "+each
            self.rename_file_callup(fleName, xmlFolderPath, getControlMesh, getTargetMesh)
            self.change_file_content_callup( pathText, getControlMesh, getTargetMesh)
            self.importtXMLSkinWeights_callup(xmlFolderPath,getTargetObject)
        except:
            print "shape or weights missing"  

    def rename_file_callup(self,fleName, pathName, oldNamePart, newNamePart):
        for fleName in glob.glob(os.path.join(pathName, "*"+oldNamePart+"*")): 
            os.rename(fleName, fleName.replace(oldNamePart, newNamePart)) 
            
    def change_file_content_callup(self, pathText, oldJointText, newJointText):
        files=glob.glob(pathText)
        for each in files: 
            dataFromTextFile=open(each).read()
            dataFromTextFile=dataFromTextFile.replace(oldJointText, newJointText)
            replacedDataTextFile=open(each, 'w')
            replacedDataTextFile.write(dataFromTextFile)
            print dataFromTextFile
            replacedDataTextFile.close()    

    def getGroupedMesh_controller_target(self):
        getMesh=cmds.ls(sl=1)
        if len(getMesh)<2:
            print "select a skinned mesh group and an unskinned target mesh group"
            return
        else:
            pass
        getMeshController=getMesh[0]
        getMeshTarget=getMesh[1]
        getChildrenController=cmds.listRelatives(getMeshController, c=1, typ="transform")
        if getChildrenController==None:
            getChildrenController=([getMeshController])
        getChildrenTarget=cmds.listRelatives(getMeshTarget, c=1, typ="transform")
        if getChildrenTarget==None:
            getChildrenTarget=([getMeshTarget])        
#         getControlObject=self.getGroupedMesh(getMeshController)
#         getTargetObject=self.getGroupedMesh(getMeshTarget)
        return getChildrenController, getChildrenTarget        
     
        
    def getGroupedMesh(self, meshGroup):
        getObject=cmds.listRelatives(meshGroup, c=1, typ="transform")
        if getObject==None:
            getMeshObject=([getObject])
            return getMeshObject



            
    def outPutConnector(self):
        getSel=cmds.ls(sl=1)
        getConnOut=cmds.connectionInfo(getSel[0]+".worldMesh[0]", dfs=1)
        for each in getConnOut:
            cmds.connectAttr(getSel[1]+".worldMesh[0]", each, f=1)
#         getConnIn=cmds.connectionInfo(getSel[0]+".inMesh", sfd=1)    
#         cmds.connectAttr(getConnIn, getSel[1]+".inMesh", f=1)
    def inPutConnectorV1(self):
        getSel=cmds.ls(sl=1)
        masterMesh=getSel[0]
        for each in getSel[1:]:
            getConnIn=[cmds.connectionInfo(masterMesh+".inMesh", sfd=1)]
            print getConnIn[0]
            cmds.connectAttr(getConnIn[0], each+"GroupParts.inputGeometry", f=1)
            cmds.connectAttr(each+".outputGeometry[0]", masterMesh+".inMesh", f=1)
    def outPutConnector_mesh(self):
        getSel=cmds.ls(sl=1)
        if len(getSel)>1:
            masterMesh=getSel[0]
            getDef=getSel[1]
#             getSourceConnector=getSel[2]
            for each in getSel[1:]:
                getplug=[cmds.listConnections (masterMesh, p=1, d=1, s=0)]
            for item in getplug[0]:
                if "input" in item or "inMesh" in item or "worldMesh" in item or "geo" in item:
                    print item
                    getConnIn=[cmds.connectionInfo(item, sfd=1)]
                    print getConnIn
                    for Connect in getConnIn:
                        getConnectionPlug=Connect.split(".")[1]
                        print getConnectionPlug
                        cmds.connectAttr(getDef+'.'+getConnectionPlug, item, f=1)
        else:
            print " select a deforming shape and a target shape"
            return
    def inPutConnector_mesh(self):
        getSel=cmds.ls(sl=1)
        if len(getSel)>1:
            masterMesh=getSel[0]
            getDef=getSel[1]
#             getSourceConnector=getSel[2]
            for each in getSel[1:]:
                getplug=[cmds.listConnections (masterMesh, p=1, d=0, s=1)]
            for item in getplug[0]:
                if "output" in item or "outMesh" in item or "geo" in item or "worldMesh" in item:
                    print item
                    getConnIn=[cmds.connectionInfo(item, dfs=1)]
                    print getConnIn[0]
                    for Connect in getConnIn[0]:
                        getConnectionPlug=Connect.split(".")[1]
                        cmds.connectAttr(item, getDef+'.'+getConnectionPlug, f=1)
        else:
            print " select a deformed shape and a target shape "
            return
#     def inPutConnector(self):
#         getSel=cmds.ls(sl=1)
#         masterMesh=getSel[0]
#         getSourceConnector=getSel[2]
#         for each in getSel[1:]:
#             getConnIn=[cmds.connectionInfo(masterMesh+".worldMatrix[0]", dfs=1)]
#             print getConnIn[0]
# #             cmds.connectAttr(getConnIn[0], each+"GroupParts.inputGeometry", f=1)
#             cmds.connectAttr(each+".worldMatrix[0]", getConnIn[0], f=1)
    def inPutConnectorRig(self):
        '''pings source plug, pongs all outputs from source'''
        #dialog
        getSel=cmds.ls(sl=1)
        titleText=('Define Rig'),                        
        messageText=("Enter Rig name"), 
        textText=("LA0095_Crissy_Rig"), 
        newRig=self.makeDialog(titleText, messageText, textText)
        #function
        for each in getSel:
            getConnIn=[cmds.listConnections(each, p=1, s=1, d=0)]
            for item in getConnIn[0]:
                if ":" in item:
                    getRigPart=item.split(":")[1]
                    getNewRigPart=newRig+":"+getRigPart
                    getConnOut=[cmds.connectionInfo(item, dfs=1)]
                    for eachOut in getConnOut[0]:
                        print eachOut
                        try:
                            cmds.connectAttr(getNewRigPart, eachOut, f=1)
                        except:
                            print "skipped "+getNewRigPart+" for some reason. Passing."
                            pass

    def inPutConnectorRigName(self):
        '''pings source plug, pongs all outputs from source'''
        #dialog
        getSel=cmds.ls(sl=1)
        titleText=('Define Rig'),                        
        messageText=("Enter Rig name"), 
        textText=("LA0095_Crissy_Rig"), 
        newRig=self.makeDialog(titleText, messageText, textText)
        #function
        for each in getSel:
            getConnIn=[cmds.listConnections(each, p=1, s=1, d=0)]
            for item in getConnIn[0]:
                if ":" in item:
                    getRigPart=item.split(":")[1]
                    getNewRigPart=newRig+":"+getRigPart
                    getConnOut=[cmds.connectionInfo(item, dfs=1)]
                    for eachOut in getConnOut[0]:
                        print eachOut
                        try:
                            cmds.connectAttr(getNewRigPart, eachOut, f=1)
                        except:
                            print "skipped "+getNewRigPart+" for some reason. Passing."
                            pass

    def getSkinWeightsforXML(self, each):
        '''this collects the skinweights'''
#         selObj=cmds.ls(sl=1, fl=1)
#         for each in selObj:
#             vertexCnt=cmds.polyEvaluate(each, v=1)
#             cmds.select(cl=1)
#             for i in range(vertexCnt):
#                 cmds.select(each+'.vtx[0:'+str(vertexCnt)+']', add=True)
        try:
            getSkinCluster=cmds.skinCluster(each, q=1, dt=1)
            for item in getSkinCluster:
                if "GroupId" in item:
                    skinID=[eachDefObj for eachDefObj in cmds.listConnections(item, s=1) if cmds.nodeType(eachDefObj)=="skinCluster"][0]
                    #skinID=item.split("GroupId")[0]
            if ":" in each:
                newname=each.split(":")[-1:]
                newname=newname[0]
            else:
                newname=each                          
            return newname, skinID
        except:
            pass

    def importXMLSkinWeights(self):
        '''import skinweights'''
        result = cmds.promptDialog( 
                    title='find XML', 
                    message="Enter path", 
                    text=xmlFolderPath, 
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
        selObj=cmds.ls(sl=1, fl=1)
        for each in selObj:
            self.importXMLSkinWeights_callup(resultInfo, each)
            
    def importXMLSkinWeights_callup(self, resultInfo, each):
        '''import skinweights function'''        
        newname, skinID=self.getSkinWeightsforXML(each)     
        print newname   
        try:      
            cmds.deformerWeights (newname+".xml", p=resultInfo, im=True, deformer=skinID)
        except:
            print "unable to open xml file for "+newname
            pass 
        print "imported skinweights"
        try:
            cmds.select(each)
            cmds.skinPercent(skinID, normalize=1)
            print "normalized"
        except:
            pass

            
    def exportXMLSkinWeights(self):
        '''export skinweights'''
        selObj=cmds.ls(sl=1, fl=1)
        result = cmds.promptDialog( 
                    title='find XML', 
                    message="Enter path", 
                    text=xmlFolderPath, 
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
        for each in selObj:
            self.exportXMLSkinWeights_callup(resultInfo, each)
            
    def exportXMLSkinWeights_callup(self, resultInfo, each):
        '''export skinweights function'''        
        if not os.path.exists(resultInfo): os.makedirs(resultInfo)
        newname, skinID=self.getSkinWeightsforXML(each)
#         print newname, skinID
#         if type(newname)=="string":
#             newname=newname
#         elif type(newname)=="list":
#             newname=newname[0]
        cmds.deformerWeights (newname+".xml", p=resultInfo,  ex=True, deformer=skinID)    

  

    def skinclusterOneVert(self):
        '''this weights the vertices to a listed joint and zeros out all others(****MIGHT BE OBSOLETE)'''
        result = cmds.promptDialog( 
                    title='Confirm', 
                    message='Keep Bone', 
                    button=['Continue','Cancel'],
                    defaultButton='Continue', 
                    cancelButton='Cancel', 
                    dismissString='Cancel' )
        if result == 'Continue':
            keep=cmds.promptDialog(q=1)
            if keep:
                pass
            else:
                print "nothing collected"
            selObj=cmds.ls(sl=1, fl=1)
            if selObj:
                pass
            else:
                print "nothing selected"
            for each in selObj:
                try:
                    getSkinCluster=cmds.skinCluster(each, q=1, dt=1)
                    for item in getSkinCluster:
                        if "GroupId" in item:
                            skinID=[eachDefObj for eachDefObj in cmds.listConnections(item, s=1) if cmds.nodeType(eachDefObj)=="skinCluster"][0]
                            getInf=cmds.skinCluster(each, q=1, inf=1)
                        for Infitem in getInf:
                            if keep in Infitem:
                                cmds.skinPercent(str(skinID), str(each), nrm=1, tv=[(str(keep), 1)])
                            else:
                                cmds.skinPercent(str(skinID), str(each), nrm=1, tv=[(str(Infitem), 0)]) 
                except:
                    print "select skin cluster"   



    def skinClust(self, getSkinCluster, each):
        '''this returns the skin cluster ID and the joint influences'''
        for item in getSkinCluster:
            if "GroupId" in item:    
                skinID=[eachDefObj for eachDefObj in cmds.listConnections(item, s=1) if cmds.nodeType(eachDefObj)=="skinCluster"][0]
                try:
                    getInf=cmds.skinCluster(each, q=1, inf=1)
                    return skinID, getInf
                except:
                    print "cant find skincluster for "+each
                    pass
                

    def skinnedBones(self, each):
        '''obsolete function'''
        getSkinCluster=cmds.skinCluster(each, q=1, dt=1)
        skinID, getInf=self.skinClust(getSkinCluster, each)  
        return skinID, getInf           
            
    def selectSkinnedBones(self):
        '''selects the joint influences that are in a cluster'''
        selObj=cmds.ls(sl=1, fl=1)
        for each in selObj:
            getSkinCluster=cmds.skinCluster(each, q=1, dt=1)
            skinID, getInf=self.skinClust(getSkinCluster, each)
        cmds.select(getInf[0])
        for each in getInf[1:]:
            cmds.select(each, add=1) 
 
                 
    def selectOppSkinnedBones(self):
        '''selects the opposite joint influences'''
        selObj=cmds.ls(sl=1, fl=1)
        for each in selObj:
            getSkinCluster=cmds.skinCluster(each, q=1, dt=1)
            skinID, getInf=self.skinClust(getSkinCluster, each)        
        getOppInf=[]
        for each in getInf:
            if "Right" in each:
                lognm=each.replace("Right", 'Left')   
                getOppInf.append(lognm)
            elif "Left" in each:
                lognm=each.replace("Left", 'Right')   
                getOppInf.append(lognm)
            else:
                getOppInf.append(each)
        cmds.select(getOppInf[0])
        for each in getOppInf[1:]:
            cmds.select(each, add=1)
                
    def selectNewRigSkinnedBonesV1(self):
        '''selects another rig's bones of the same name'''
        getSel=cmds.ls(sl=1)
        titleText=('Define Rig'),                        
        messageText=("Enter Rig name"), 
        textText=("LA0095_Crissy_Rig"), 
        newRig=self.makeDialog(titleText, messageText, textText)        
        selObj=cmds.ls(sl=1, fl=1)
        for each in selObj:
            getSkinCluster=cmds.skinCluster(each, q=1, dt=1)
            skinID, getInf=self.skinClust(getSkinCluster, each)        
        getRigBones=[]
        for each in getInf:
            if ":" in item:
                getRigPart=each.split(":")[1]
                getNewRigPart=newRig+":"+getRigPart  
                getRigBones.append(getNewRigPart)          
        cmds.select(getRigBones[0])
        for each in getRigBones[1:]:
            cmds.select(each, add=1)
            
    def selectNewRigSkinnedBones(self, Arg=None):
        try:
            getallnames=cmds.ls("*Rig:*")
        except:
            print "No rig is loaded. Please ensure 'Rig' is at the end of the name"
        bucket=[]
        for each in  getallnames:
            foundFirst=each.split(":")[0]
            bucket.append(foundFirst)
        bucket=set(bucket)
        global jointSelect
        winName = "Swap Influence select"
        winTitle = winName
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)

        window = cmds.window(winName, title=winTitle, tbm=1, w=300, h=100 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=300)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        
        cmds.rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))
        jointSelect=cmds.optionMenu( label='joints')
        for each in bucket:
            cmds.menuItem( label=each)        
        cmds.button (label='select influences', p='listBuildButtonLayout', command = lambda *args:self.selectNewRigSkinnedBones_callup())
        cmds.showWindow(window)              
               
    def selectNewRigSkinnedBones_callup(self):
        '''selects another rig's bones of the same name'''
        newRig=cmds.optionMenu(jointSelect, q=1, v=1)     
        selObj=cmds.ls(sl=1, fl=1)
        for each in selObj:
            getSkinCluster=cmds.skinCluster(each, q=1, dt=1)
            skinID, getInf=self.skinClust(getSkinCluster, each)        
        getRigBones=[]
        for item in getInf:
            if ":" in item:
                getRigPart=item.split(":")[1]
                getNewRigPart=newRig+":"+getRigPart  
                getRigBones.append(getNewRigPart)    
            else:
              getRigBones.append(item)    
        cmds.select(getRigBones[0])
        for each in getRigBones[1:]:
            cmds.select(each, add=1)            
            
    def bagOfBones(self, skinnedObject):
        '''detects the joint influences that are in a cluster'''
        boneBag=[]
        getSkinCluster=cmds.skinCluster(skinnedObject, q=1, dt=1)
        skinID, getInf=self.skinClust(getSkinCluster, skinnedObject)
        for each in getInf:
            boneBag.append(each)
        return boneBag    

    def Reset(self):
        '''this resets selected'''
        selObj=cmds.ls(sl=1)
        for each in selObj:
            self.reset_Callup(each)

    def reset_callup(self, each):      
        ChildAttributes=(".tx", ".ty", ".tz" , ".rx", ".ry", ".rz")        
        for attribute in ChildAttributes:
            try:           
                cmds.setAttr(each+attribute, 0.0)
            except:
                pass
        
    def removekey_callup(self, each):
        cmds.select(each)
        cmds.cutKey()
        
    def removeKey(self):
        getCtrlBucket=[]
        if cmds.ls("*:*Ctrl"):
            selObj=cmds.ls("*:*Ctrl")
            for each in selObj:
                getCtrlBucket.append(each)
        elif cmds.ls("*Ctrl"):
            selObj=cmds.ls("*Ctrl")
            for each in selObj:
                getCtrlBucket.append(each)
        for each in getCtrlBucket:
            self.removekey_callup(each)
            
    def clearAnim(self):
        getCtrlBucket=[]
        if cmds.ls("*:*Ctrl"):
            selObj=cmds.ls("*:*Ctrl")
            for each in selObj:
                getCtrlBucket.append(each)
        elif cmds.ls("*Ctrl"):
            selObj=cmds.ls("*Ctrl")
            for each in selObj:
                getCtrlBucket.append(each)
        for each in getCtrlBucket:
            self.reset_callup(each)
            self.removekey_callup(each)
        
    def selectSkinnedVerts(self):
        '''this selects all the verts that are elected to a named influence'''
        titleText=('Define joint'),                        
        messageText=("Enter name"), 
        textText=("footballRight"), 
        jointName=self.makeDialog(titleText, messageText, textText)
        selObj=cmds.ls(sl=1, fl=1)
        for each in selObj:
            getSkinCluster=cmds.skinCluster(each, q=1, dt=1)
            skinID, getInf=self.skinClust(getSkinCluster, each)
        jointInf=cmds.ls("*:*"+jointName+"_jnt")
        if not jointInf:
            jointInf=cmds.ls("*"+jointName+"_jnt")
        getSkinCluster=cmds.skinCluster(skinID, e=1, siv=jointInf)     
        
         
    def isolateVertSkinSide(self):
        '''this removes the weight of a joint name type from selected vertice'''
        selObj=cmds.ls(sl=1, fl=1)
        result = cmds.promptDialog( 
                    title='Confirm', 
                    message='remove bone name(enter named part EG: "Right"', 
                    button=['Continue','Cancel'],
                    defaultButton='Continue', 
                    cancelButton='Cancel', 
                    dismissString='Cancel' )
        if result == 'Continue':
            remove=cmds.promptDialog(q=1)
            if remove:
                pass
            else:
                print "nothing collected"        
        for each in selObj:
            getSkinCluster=cmds.skinCluster(each, q=1, dt=1)
            skinID, getInf=self.skinClust(getSkinCluster, each)
            for Infitem in getInf:
                if remove in Infitem:
                    cmds.skinPercent(str(skinID), str(each), nrm=1, tv=[(str(Infitem), 0)])
                   

    def isolateJointSkin(self):
        '''this keeps the name portion of a skinned joint and removes all others from selected vertice weights'''
        selObj=cmds.ls(sl=1, fl=1)
        result = cmds.promptDialog( 
                    title='Confirm', 
                    message='keep only, remove all else', 
                    button=['Continue','Cancel'],
                    defaultButton='Continue', 
                    cancelButton='Cancel', 
                    dismissString='Cancel' )
        if result == 'Continue':
            remove=cmds.promptDialog(q=1)
            if remove:
                pass
            else:
                print "nothing collected"        
        for each in selObj:
            getSkinCluster=cmds.skinCluster(each, q=1, dt=1)
            skinID, getInf=self.skinClust(getSkinCluster, each)
            for Infitem in getInf:
                if remove not in Infitem:
                    #cmds.skinPercent(str(skinID), str(each), nrm=1, tv=[(str(Infitem), 0)])
                    cmds.skinCluster(str(skinID), e=1, ri=Infitem)

    def skinclusterOne(self):
        '''This collects all of the selected vertices weighted onto the one labelled bone'''
        selObj=cmds.ls(sl=1, fl=1)        
        result = cmds.promptDialog( 
                    title='Confirm', 
                    message='full weight on joint name(named part EG: "elbow")', 
                    button=['Continue','Cancel'],
                    defaultButton='Continue', 
                    cancelButton='Cancel', 
                    dismissString='Cancel' )
        if result == 'Continue':
            keep=cmds.promptDialog(q=1)
            if keep:
                pass
            else:
                print "nothing collected"  
        for each in selObj:
            try:
                getSkinCluster=cmds.skinCluster(each, q=1, dt=1)
                skinID, getInf=self.skinClust(getSkinCluster, each)
                for Infitem in getInf:
                    if keep in Infitem:
                        cmds.skinPercent(str(skinID), str(each), nrm=1, tv=[(str(Infitem), 1)])   
#                     else:     
#                         cmds.skinPercent(str(skinID), str(each), nrm=1, tv=[(str(Infitem), 0)]) 
            except:
                getJoint=cmds.ls(keep)
                for item in getJoint:
                    cmds.skinCluster(each,item,sm=0 )
    def skinclusterZero(self):
        '''This sets targetted bone names to zero influence'''
        selObj=cmds.ls(sl=1, fl=1)        
        result = cmds.promptDialog( 
                    title='Confirm', 
                    message='pull weight off joint name(named part EG: "elbow")', 
                    button=['Continue','Cancel'],
                    defaultButton='Continue', 
                    cancelButton='Cancel', 
                    dismissString='Cancel' )
        if result == 'Continue':
            deassign=cmds.promptDialog(q=1)
            if deassign:
                pass
            else:
                print "nothing collected"  
        for each in selObj:
            getSkinCluster=cmds.skinCluster(each, q=1, dt=1)
            skinID, getInf=self.skinClust(getSkinCluster, each)
            for Infitem in getInf:
                if deassign in Infitem:
                    cmds.skinPercent(str(skinID), str(each), nrm=1, tv=[(str(Infitem), 0)])   


    def getJointInfluence(self):
        '''This removes a joint name from being an influence on a skin(this removes, it does not set to 0)'''
        selObj=cmds.ls(sl=1, fl=1)        
        result = cmds.promptDialog( 
                    title='Confirm', 
                    message='remove bone name influence(named part EG: "elbow"', 
                    button=['Continue','Cancel'],
                    defaultButton='Continue', 
                    cancelButton='Cancel', 
                    dismissString='Cancel' )
        if result == 'Continue':
            keep=cmds.promptDialog(q=1)
            if keep:
                pass
            else:
                print "nothing collected"  
        for each in selObj:
            getSkinCluster=cmds.skinCluster(each, q=1, dt=1)
            skinID, getInf=self.skinClust(getSkinCluster, each)
            return (keep, skinID, getInf)

                        
    def jointInfluenceRemove(self):
        '''if name is found as an influence, this will remove it'''
        keep, skinID, getInf=self.getJointInfluence()
        for Infitem in getInf:
            if keep in Infitem:
                cmds.skinCluster(str(skinID), e=1, ri=Infitem)

    def jointInfluenceHammer(self):
        '''if name is not identified as an influence this will remove it'''
        keep, skinID, getInf=self.getJointInfluence()
        for Infitem in getInf:
            if keep not in Infitem:
                cmds.skinCluster(str(skinID), e=1, ri=Infitem)
                
    def jointInfluenceHammer_callup(self, keep, each):
        '''if name is not identified as an influence this will remove it - calls from other controllers'''
        getSkinCluster=cmds.skinCluster(each, q=1, dt=1)
        skinID, getInf=self.skinClust(getSkinCluster, each)
        for Infitem in getInf:
            if keep not in Infitem:
                cmds.skinCluster(str(skinID), e=1, ri=Infitem)
                    
    def jointInfluenceRemoveMult(self):
        '''work in progress - joint remove multi from a skinweight'''
        selObj=cmds.ls(sl=1, fl=1)        
        result = cmds.promptDialog( 
                    title='Confirm', 
                    message='remove bone name influence(named part EG: "elbow"', 
                    button=['Continue','Cancel'],
                    defaultButton='Continue', 
                    cancelButton='Cancel', 
                    dismissString='Cancel' )
        if result == 'Continue':
            removeThis=cmds.promptDialog(q=1)   
            if "," in removeThis:
                throwAwayBucket=[]
                eachInfluenceRemove=removeThis.split(", ")
                throwAwayBucket.append(eachInfluenceRemove)
            else:
                throwAwayBucket=[removeThis]
        else:
            print "nothing collected"  
        for each in selObj:
            getSkinCluster=cmds.skinCluster(each, q=1, dt=1)
            skinID, getInf=self.skinClust(getSkinCluster, each)
            findMyItem=[(infItem) for infItem in getInf for throwItem in throwAwayBucket if str(throwItem) in infItem]
            for item in findMyItem:
                print "removing: "+item
                cmds.skinPercent(str(skinID), str(each), nrm=1, tv=[(str(item), 0)])   
                cmds.skinCluster(str(skinID), e=1, ri=item)
    def jointInfluenceAddMult(self):
        '''work in progress - joint add to skin'''
        selObj=cmds.ls(sl=1, fl=1)        
        result = cmds.promptDialog( 
                    title='Confirm', 
                    message='add bone name influence(named part EG: "elbow"', 
                    button=['Continue','Cancel'],
                    defaultButton='Continue', 
                    cancelButton='Cancel', 
                    dismissString='Cancel' )
        if result == 'Continue':
            addThis=cmds.promptDialog(q=1)   
            if "," in addThis:
                AddBucket=[]
                eachInfluenceAdd=addThis.split(", ")
                allObject=cmds.ls(sn=1)
                getItem=[(each)for each in allObject if addThis in each if cmds.nodeType(each)=="joint"]                
                AddBucket.append(getItem)
            else:
                allObject=cmds.ls(sn=1)
                getItem=[(each)for each in allObject if addThis in each if cmds.nodeType(each)=="joint"] 
                AddBucket=[getItem]
        else:
            print "nothing collected"  
        for each in selObj:
            getSkinCluster=cmds.skinCluster(each, q=1, dt=1)
            skinID, getInf=self.skinClust(getSkinCluster, each)
#             findMyItem=[(infItem) for infItem in getInf for throwItem in AddBucket if str(throwItem) in infItem]
            if len(AddBucket)>0:
                for item in AddBucket:
                    for eachJoint in item:
    #                 cmds.skinPercent(str(skinID), str(each), nrm=1, tv=[(str(item), 0)])
                        try:   
                            cmds.skinCluster(str(skinID), e=1, ai=eachJoint)
                            print eachJoint+" has been added"
                        except:
                            print eachJoint+" has already been added"
                            pass
            else:
                print "cannot identify this influence in scene"
                  
    def skinClusterRemoveDialog(self):
        '''obsolete experiment'''
        result = cmds.promptDialog( 
                    title='Confirm', 
                    message='remove bone', 
                    button=['Continue','Cancel'],
                    defaultButton='Continue', 
                    cancelButton='Cancel', 
                    dismissString='Cancel' )
        if result == 'Continue':
            DoNotKeep=cmds.promptDialog(q=1)
            if DoNotKeep:
                pass
            else:
                print "nothing collected"
            selObj=cmds.ls(sl=1, fl=1)
            if selObj:
                pass
            else:
                print "nothing selected"
            for each in selObj:
                try:    
                    self.skinClusterRemove(DoNotKeep, selObj)
                except:
                    print "select skin cluster"                                   
                
    def skinClusterRemove(self, DoNotKeep, selObj):
        '''part of obsolete experiment'''
        selObj=cmds.ls(sl=1, fl=1)
        for each in selObj:
            for eachBone in DoNotKeep:
                getSkinCluster=cmds.skinCluster(each, q=1, dt=1)
                for item in getSkinCluster:
                    if "GroupId" in item:
                        skinID=[eachDefObj for eachDefObj in cmds.listConnections(item, s=1) if cmds.nodeType(eachDefObj)=="skinCluster"][0]
                getInf=cmds.skinCluster(each, q=1, inf=1)
                for Infitem in getInf:
                    if eachBone in Infitem:
                        #cmds.skinPercent(str(skinID), str(each), nrm=1, tv=[(str(Infitem), 0)])
                        cmds.skinCluster(str(skinID), e=1, ri=Infitem)
                        
    def MassCleanInfluence(self):
        '''clears out unused bones on all mesh items in scene'''
        meshList =cmds.ls(sl=1, fl=1)
        for each in meshList:
            maya.mel.eval( "removeUnusedInfluences;" )

    def accMirrorWeights(self):
        selObj=cmds.ls(sl=1, fl=1)
        for each in selObj:
            getSkinCluster=cmds.skinCluster(each, q=1, dt=1)
            skinID, getInf=self.skinClust(getSkinCluster, each)
        cmds.copySkinWeights(ss=str(skinID), ds=str(skinID), mm="YZ", mi=1, sa="rayCast", ia="closestJoint")

    def MassSkinClusterQuery(self):
        '''This removes a collection of bone name types from the skincluster mesh for the entire scene'''
        DoNotKeep=("IK", "FK", "Clst")
        meshList = cmds.ls(typ="mesh")
        for item in meshList:
            vtxCount = cmds.polyEvaluate(v=True)
            selObj=cmds.select(item+'.vtx[0:'+str(vtxCount)+']', add=True)        
        #meshList=[(item) for item in cmds.ls(typ="mesh") if cmds.objectType(item)]
        self.skinClusterRemove(DoNotKeep, selObj)
        
    def multipleWorldMeshConnect(self):
        '''select new mesh and select the first input to connect to on a multiple selection(useful for relinking rivets to new mesh)'''
        getObj=cmds.ls(sl=1)
        newmesh=getObj[0]
        for each in getObj[1:]:
            cmds.connectAttr(newmesh+".worldMesh[0]", each+".inputMesh", f=1)
            
            
    def directWorldMeshConnect(self):
        '''this replaces the first selection world mesh plug with the second selection(useful for plugging into an entire rig'''
        getObj=cmds.ls(sl=1)
        for eachController, eachChild in map(None, getObj[::2], getObj[1::2]):
            getConn=cmds.connectionInfo(eachController, dfs=1)
            for item in getConn:
                cmds.connectAttr(eachChild+".worldMesh[0]",  item+".inputMesh", f=1)
        

        
    def hideEyes(self):
        '''this hides unwanted curves'''
        getEyecurves=("eyeDirGuide_LeftEye_IndicatorShape", "eyeDirGuide_Leftpupil_IndicatorShape", "eyeDirGuide_RightEye_IndicatorShape", "eyeDirGuide_RightPupil_IndicatorShape")
        for each in getEyecurves:
            cmds.setAttr(each+".overrideDisplayType", 2)
            
    def buildGrpV1(self, each):
        '''this partners with the createGrpCtrl is the create group function'''
        selObjParent=cmds.listRelatives( each, allParents=True )
        cmds.CreateEmptyGroup(each+'_grp')
        grpObj=cmds.ls(sl=1)
        transformWorldMatrix, rotateWorldMatrix=self.locationXForm(each)
        #worldMatrix = cmds.xform(selObj[0], q=True, ws=1, m=True)
        #cmds.xform(grpObj[0], ws=1,  m=worldMatrix )
        cmds.xform(grpObj[0], ws=1, t=transformWorldMatrix)
        cmds.xform(grpObj[0], ws=1, ro=rotateWorldMatrix)         
        cmds.rename(grpObj[0], each+'_grp')      
        if selObjParent:
            cmds.parent(each+'_grp', selObjParent[0] )
        cmds.parent(each, each+'_grp')
        Child=cmds.listRelatives(each+'_grp', ad=1, typ="transform") 
        cmds.makeIdentity(Child, a=True, t=1, n=0)  

    def createGrpCtrl(self):
        '''creates a group above a selected object and zeroes it out'''
        selObj=cmds.ls(sl=1)
        for each in selObj:
            self.buildGrp(each)

    def buildGrp(self, each):
        '''this partners with the createGrpCtrl is the create group function'''
        transformWorldMatrix, rotateWorldMatrix=self.locationXForm(each)
        self.freeTheAttrs(each)
        # cmds.xform(each, ws=1, t=[0,0,0])
        # cmds.xform(each, ws=1, ro=[0,0,0])
        selObjParent=cmds.listRelatives( each, allParents=True )
        cmds.CreateEmptyGroup(each+'_grp')
        grpObj=cmds.ls(sl=1)
        cmds.xform(grpObj[0], ws=1, t=transformWorldMatrix)
        cmds.xform(grpObj[0], ws=1, ro=rotateWorldMatrix)         
        cmds.rename(grpObj[0], each+'_grp')      
        if selObjParent:
            cmds.parent(each+'_grp', selObjParent[0] )
        cmds.parent(each, each+'_grp')
        Child=cmds.listRelatives(each+'_grp', ad=1, typ="transform") 
        cmds.makeIdentity(Child, a=True, t=1, n=0) 

    def createClstr(self):
        selObj=cmds.ls(sl=1, fl=1)
        cmds.select(cl=1)
        for each in selObj:
            cmds.select(each, r=1)
            transformWorldMatrix, rotateWorldMatrix=self.locationXForm(each)
            self.freeTheAttrs(each)
            cmds.xform(each, ws=1, t=[0,0,0])
            cmds.xform(each, ws=1, ro=[0,0,0])
            cmds.cluster()
            clstrObj=cmds.ls(sl=1)        
            querySet=[(connectedObj) for connectedObj in cmds.listConnections(clstrObj[0], c=1) if cmds.nodeType(connectedObj) =="cluster"]
            setName=[(connectedObj) for connectedObj in cmds.listSets(o=querySet[0])]
            cmds.sets(each, add=setName[0])
            cmds.xform(clstrObj[0], ws=1, t=transformWorldMatrix)
            cmds.xform(clstrObj[0], ws=1, ro=rotateWorldMatrix)

    def createJnt(self):
        selObj=cmds.ls(sl=1, fl=1)
        for each in selObj:
            transformWorldMatrix, rotateWorldMatrix=self.locationXForm(each)
            self.freeTheAttrs(each)
            cmds.xform(each, ws=1, t=[0,0,0])
            cmds.xform(each, ws=1, ro=[0,0,0])
            jnt=self.buildJoint(each, [0,0,0], [0,0,0])
            cmds.skinCluster( jnt, each, dr=4.5, tsb=1)
            cmds.xform(jnt, ws=1, t=transformWorldMatrix)
            cmds.xform(jnt, ws=1, ro=rotateWorldMatrix)

    def buildGrpIsolated(self, each, grpName):
        selObjParent=cmds.listRelatives( each, allParents=True )
        cmds.CreateEmptyGroup()
        cmds.rename(grpName)
        grpObj=cmds.ls(sl=1)
        transformWorldMatrix, rotateWorldMatrix=self.locationXForm(each)
        #worldMatrix = cmds.xform(selObj[0], q=True, ws=1, m=True)
        #cmds.xform(grpObj[0], ws=1,  m=worldMatrix )
        cmds.xform(grpObj[0], ws=1, t=transformWorldMatrix)
        cmds.xform(grpObj[0], ws=1, ro=rotateWorldMatrix)     
        if selObjParent:
            cmds.parent(grpName, selObjParent[0] )
#        cmds.parent(each, grpName)
        Child=cmds.listRelatives(grpName, ad=1, typ="transform") 
        cmds.makeIdentity(Child, a=True, t=1, n=0)     
           

    def makeGuide(self):
        '''This is the initate buildguide function'''
        selectionCheck=cmds.ls(sl=1, fl=1)
        colour1=13
        colour2=6
        colour3=27
        namePortionTwo="_guide"   
        guideName=self.fetchName()
        if selectionCheck:
            for indexNumber, eachPoint in enumerate(xrange(len(selectionCheck))):
                try:
                    each, next_item = selectionCheck[eachPoint], selectionCheck[eachPoint + 1]  
                    transformWorldMatrixNext, rotateWorldMatrixNext=self.locationXForm(next_item)    
                    tempname, tempgrpname, tempsize, tempcolour="none", "none_grp", 6, 6
                    self.JackI(tempname, tempgrpname, tempsize, transformWorldMatrixNext, rotateWorldMatrixNext, tempcolour)                    
                except:
                    pass
                name=self.guide_names(indexNumber, guideName) 
                if objExists(name):
                    name=self.nameExist(guideName, namePortionTwo)               
                transformWorldMatrix, rotateWorldMatrix=self.locationXForm(selectionCheck[eachPoint])
                self.guideBuild(name, transformWorldMatrix, rotateWorldMatrix, colour1, colour2, colour3)
                getNewGuide=cmds.ls(sl=1, fl=1)
                try:
                    cmds.select(tempname, r=1)
                    getDelete=cmds.ls(sl=1, fl=1)
                    cmds.select(getNewGuide[0], add=1)
                    cmds.aimConstraint(offset=[0,0, 0], weight=1, aimVector=[1, 0, 0] , upVector=[0, 1, 0] ,worldUpType="vector" ,worldUpVector=[0, 1, 0])
                    cmds.delete(tempname)
                    cmds.delete(tempgrpname)
                except:
                    pass
        else:
            indexNumber=00
            name=self.guide_names(indexNumber, guideName) 
            if objExists(name):
                name=self.nameExist(guideName, namePortionTwo)
                # getNumbs=[]
                # getAll=cmds.ls(guideName+"*_guide")
                # for each in getAll:
                #     getLast=each.split(guideName)[1]
                #     getNumb=getLast.split("_guide")[0]
                #     getNumb=int(getNumb)
                #     getNumbs.append(getNumb)
                # name=self.guide_names(getNumbs[-1:][0], guideName)  
            else:            
                name=name
            transformWorldMatrix=(0, 0, 0) 
            rotateWorldMatrix=(0, 0, 0)           
            self.guideBuild(name, transformWorldMatrix, rotateWorldMatrix, colour1, colour2, colour3)

    def nameExist(self, prefix, suffix):
        getNumbs=[]
        getAll=cmds.ls(prefix+"*"+suffix)
        for each in getAll:
            getLast=each.split(prefix)[1]
            getNumb=getLast.split(suffix)[0]
            getNumb=int(getNumb)
            getNumbs.append(getNumb)
        newname=self.guide_names(getNumbs[-1:][0], prefix)   
        return newname


    def guide_names(self, indexNumber, guideName):                
        incrementals=indexNumber+1
        getNum="%02d" % (incrementals,)
        name=guideName+getNum+"_guide"  
        return name

    def guideBuild(self, each, transformWorldMatrix, rotateWorldMatrix, colour1, colour2, colour3):
        '''finds location for the build guides function'''
        xCircmake=self.makeguide_shapes(each, colour1, colour2, colour3)
        cmds.xform(xCircmake[0], ws=1, t=transformWorldMatrix)
        cmds.xform(xCircmake[0], ws=1, ro=rotateWorldMatrix)     
        #cmds.makeIdentity(xCircmake[0], a=True, t=1, s=1, r=1, n=0)
        cmds.select(xCircmake[0]) 

            
    def makeguide_shapes(self, each, colour1, colour2, colour3):
        '''builds shapes for the build guides function'''
        newBucket=[]  
        xCircmake=cmds.circle(n=each, r=1.5, nrx=1, nry=0, nrz=0)
        yCircmake=cmds.circle(n="yCirc", r=1.5, nrx=0, nry=1, nrz=0)
        zCircmake=cmds.circle(n="zCirc", r=1.5, nrx=0, nry=0, nrz=1)
        groupingShapes=[str(zCircmake[0]+"Shape"), str(yCircmake[0]+"Shape"), str(xCircmake[0])]
        newBucket.append(xCircmake[0])
        cmds.parent(groupingShapes,r=1, s=1)
        cmds.delete(yCircmake[0])
        cmds.delete(zCircmake[0])
        guidez=cmds.rename(zCircmake[0]+"Shape", xCircmake[0]+"Guidez")
        newBucket.append(guidez)
        guidey=cmds.rename(yCircmake[0]+"Shape", xCircmake[0]+"Guidey")
        newBucket.append(guidey)   
        for each in newBucket:
            cmds.setAttr(each+".overrideEnabled", 1)
        cmds.setAttr(newBucket[0]+".overrideColor", colour1)
        cmds.setAttr(newBucket[1]+".overrideColor", colour2)    
        cmds.setAttr(newBucket[2]+".overrideColor", colour3)     
        return xCircmake


    def build_a_curve(self):
        getTopOpenGuides=cmds.ls(sl=1, fl=1)
        self.build_a_curve_callup(getTopOpenGuides)

    def build_a_curve_callup(self, selectedObjects):
        values=[]
        for each in selectedObjects:#get point values to build curve
            transformWorldMatrix = cmds.xform(each, q=True, wd=1, t=True)  
            values.append(transformWorldMatrix)
        cmds.curve(n=selectedObjects[0]+"_crv", d=3, p=values)        

    def makeJoint(self):
        '''This creates a joint at a selection'''
        selectionCheck=cmds.ls(sl=1)
        if selectionCheck:
            for each in selectionCheck:
                transformWorldMatrix, rotateWorldMatrix=self.locationXForm(each)
                name=each                   
                self.buildJoint(name, transformWorldMatrix, rotateWorldMatrix)
        else:     
            name="joint"
            transformWorldMatrix=(0, 0, 0) 
            rotateWorldMatrix=(0, 0, 0)            
            self.buildJoint(name, transformWorldMatrix, rotateWorldMatrix)
            #getjoint=cmds.joint() 
            cmds.select(cl=1)
            
    def buildJoint(self, name, transformWorldMatrix, rotateWorldMatrix):
        '''this is the build joint function to work with makejoint'''
        jointName=name+"_jnt"
        getloc=cmds.spaceLocator(n=name+"_lctr")
        cmds.xform(getloc[0], ws=1, t=transformWorldMatrix)
        cmds.xform(getloc[0], ws=1, ro=rotateWorldMatrix)      
        getjoint=cmds.joint(n=jointName)
        cmds.xform(jointName, ws=1, t=transformWorldMatrix)
        cmds.xform(jointName, ws=1, ro=rotateWorldMatrix) 
        cmds.parent(jointName, w=1)
        cmds.delete(getloc[0])    
        cmds.select(cl=1)   
        return getjoint


    def buildJointFunction_callup(self):
        titleText=('Define name of joint chain'),                        
        messageText=("Enter name"), 
        textText=("name"), 
        mainName=self.makeDialog(titleText, messageText, textText)
        mainChain=(cmds.ls(mainName+"*_guide"))
        cmds.select(cl=1)
        lastmainChainJoint=mainChain[-1:]
        for each in mainChain:
            jointSuffix='_jnt'
            self.rigJoints(each, jointSuffix) 

    def buildLoc(self, name, grpname, transformWorldMatrix, rotateWorldMatrix, colour):
        '''this is the build locator function'''
        jointName=name+"_lctr"
        getloc=cmds.spaceLocator(n=name+"_lctr")
        cmds.xform(getloc[0], ws=1, t=transformWorldMatrix)
        cmds.xform(getloc[0], ws=1, ro=rotateWorldMatrix)   
        cmds.setAttr(getloc[0]+"Shape.overrideEnabled", 1)
        cmds.setAttr(getloc[0]+"Shape.overrideColor", colour)        
        self.buildGrp(getloc[0])   


    def makeCtrl(self):
        '''this builds a control at a selection'''
        selectionCheck=cmds.ls(sl=1)
        if selectionCheck:
            for each in selectionCheck:
                transformWorldMatrix, rotateWorldMatrix=self.locationXForm(each)
                size=1
                colour=6
                name=each+"_ctrl"
                grpname=each+"_grp"
                nrx=0
                nry=1
                nrz=0
                self.buildCtrl(each, name, grpname, transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)
        else:   
            each="newl"
            transformWorldMatrix=(0, 0, 0) 
            rotateWorldMatrix=(0, 0, 0)
            size=1
            colour=6
            name=each+"_ctrl"
            grpname=each+"_grp"   
            nrx=0
            nry=1
            nrz=0         
            self.guideBuild(each, name, grpname, transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)

            
    def buildCtrl(self, each, name, grpname, transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz):
        '''this builds a control at a selection- works with the makectrl and referenced for other uses'''
        yCircmake=cmds.circle(n=name, r=size, nrx=nrx, nry=nry, nrz=nrz)
        self.locationEcho(yCircmake[0], grpname, colour, transformWorldMatrix, rotateWorldMatrix)         
    
    
    def fullMatrixXform(self, each):
        transform=cmds.xform(each , q=True, ws=1, m=True)
        return  transform,

    def makesquareCtrl(self):
        '''This builds the square shaped control'''
        selectionCheck=cmds.ls(sl=1)
        colour=13
        if selectionCheck:
            for each in selectionCheck:
                transformWorldMatrix, rotateWorldMatrix=self.locationXForm(each)
                xSquaremake=self.makeSquare(each) 
                grpname=xSquaremake[0]+"_grp"
                self.locationEcho(xSquaremake[0], grpname, colour, transformWorldMatrix, rotateWorldMatrix)           
        else:   
            each="square"
            xSquaremake=self.makeSquare(each)
            grpname="square_grp"
            transformWorldMatrix, rotateWorldMatrix=[0.0,0.0,0.0],[0.0,0.0,0.0]
            self.locationEcho(xSquaremake[0], grpname, colour, transformWorldMatrix, rotateWorldMatrix)   

    def makeSquare(self, each):
        '''obsolete - makes a square control using nurbs'''
        newBucket=[]         
        xCircmake=cmds.nurbsSquare(n=each+"_ctrl", nr=(0,1,0), sl1=.5, sl2=.5)
        groupingShapes=["top"+each+"_ctrlShape",
                        "left"+each+"_ctrlShape",
                        "bottom"+each+"_ctrlShape",
                        "right"+each+"_ctrlShape",
                        each+"_ctrl"]
        newBucket.append(each+'ctrl')        
        cmds.parent(groupingShapes ,r=1, s=1)
        top=cmds.rename("top"+each+"_ctrlShape", xCircmake[0]+"top")
        newBucket.append(top)
        left=cmds.rename("left"+each+"_ctrlShape", xCircmake[0]+"left")
        newBucket.append(left)         
        bottom=cmds.rename("bottom"+each+"_ctrlShape", xCircmake[0]+"bottom")
        newBucket.append(bottom) 
        right=cmds.rename("right"+each+"_ctrlShape", xCircmake[0]+"right")
        newBucket.append(right)    
        cmds.delete("top"+each+"_ctrl")
        cmds.delete("left"+each+"_ctrl")   
        cmds.delete("bottom"+each+"_ctrl")
        cmds.delete("right"+each+"_ctrl")
        return xCircmake

    def moveto(self):
        objSel=cmds.ls(sl=1)
        transformWorldMatrix, rotateWorldMatrix=self.locationXForm(objSel[0])
        for each in objSel[1:]:
            cmds.xform(each, ws=1, t=transformWorldMatrix)
            cmds.xform(each, ws=1, ro=rotateWorldMatrix) 
 
    def xformmove(self):
        '''move to matrix'''
        objSel=cmds.ls(sl=1)
        matrix=cmds.xform(objSel[1], q=1, ws=1, m=1)
        cmds.xform(objSel[0], ws=1, m=matrix)   
        cmds.select(objSel[0])
    
    def xformtran(self):
        '''move to transform and rotation'''
        objSel=cmds.ls(sl=1)
        transformWorldMatrix, rotateWorldMatrix=self.locationXForm(objSel[1])
        cmds.xform(objSel[0], ws=1, t=transformWorldMatrix)
        cmds.xform(objSel[0], ws=1, ro=rotateWorldMatrix) 
        #cmds.xform(objSel[0], ws=1, m=matrix)   
        cmds.select(objSel[0])
    def xformmatch(self):
        '''move to transform and rotation relative'''
        selObj=cmds.ls(sl=1)
        for eachController, eachChild in map(None, selObj[::2], selObj[1::2]):
            transformWorldMatrix=cmds.xform(eachController, q=1, t=1)
            rotateWorldMatrix=cmds.xform(eachController, q=1, ro=1)
            cmds.xform(eachChild, r=1, t=transformWorldMatrix)
            cmds.xform(eachChild, r=1, ro=rotateWorldMatrix) 
        
    def rigJoints(self, each, jointsuf):
        '''build joints for rig'''
        getTranslation=cmds.xform(each, q=1, t=1, ws=1)
        getName=each.split("_")
        jointnames=str(getName[0]+jointsuf)
        cmds.joint(n=jointnames, p=getTranslation)   
    def rigJointnames(self, each, name):
        '''make jointnames'''
        getTranslation=cmds.xform(each, q=1, t=1, ws=1)
        cmds.joint(n=name, p=getTranslation)          
    def rigJointsnname(self, each, name):
        '''rig joints without a suffix'''
        getTranslation=cmds.xform(each, q=1, t=1, ws=1)
        cmds.joint(n=name, p=getTranslation)      
    def blendColors(self, each, Controller):
        '''this creates the ik fk blend rotation'''
        cmds.shadingNode('blendColors', n=each+'_blnd', asShader=True)
        cmds.connectAttr( each+"IK_jnt.rotate", each+'_blnd.color1', f=1)
        cmds.connectAttr( each+"FK_jnt.rotate", each+'_blnd.color2', f=1)    
        cmds.connectAttr( each+"_blnd.output", each+"_jnt.rotate", f=1)
        cmds.shadingNode('blendColors', n=each+'_sblnd', asShader=True)    
        cmds.connectAttr( each+"_sblnd.output.outputR", each+"_jnt.scale.scaleX", f=1)
        cmds.connectAttr( each+"IK_jnt.scale.scaleX", each+'_sblnd.color1.color1R', f=1)    
        cmds.connectAttr( each+"FK_jnt.scale.scaleX", each+'_sblnd.color2.color2R', f=1)   
        cmds.connectAttr(Controller, each+"_blnd.blender", f=1)
        cmds.connectAttr(Controller, each+"_sblnd.blender", f=1)
        
    def blendColors_callup(self, Controller, firstChild, secondChild, thirdChild):
        '''this creates a blend rotation based on selection(used in Rig kit)'''
        cmds.shadingNode('blendColors', n=firstChild+'_blnd', asShader=True)
        cmds.connectAttr( secondChild+".rotate", firstChild+'_blnd.color1', f=1)
        cmds.connectAttr( thirdChild+".rotate", firstChild+'_blnd.color2', f=1)    
        cmds.connectAttr( firstChild+"_blnd.output", firstChild+".rotate", f=1)
        cmds.shadingNode('blendColors', n=firstChild+'_sblnd', asShader=True)    
        cmds.connectAttr( firstChild+"_sblnd.output.outputR", firstChild+".scale.scaleX", f=1)
        cmds.connectAttr( secondChild+".scale.scaleX", firstChild+'_sblnd.color1.color1R', f=1)    
        cmds.connectAttr( thirdChild+".scale.scaleX", firstChild+'_sblnd.color2.color2R', f=1)   
        cmds.connectAttr(Controller, firstChild+"_blnd.blender", f=1)
        cmds.connectAttr(Controller, firstChild+"_sblnd.blender", f=1)
        
    def blendColorsTranslate(self, each, Controller):
        '''this creates the translate blend bexformmovetween ik and fk'''
        cmds.shadingNode('blendColors', n=each+'_tblnd', asShader=True)                 
        cmds.connectAttr( each+"_tblnd.output.outputR", each+"_jnt.translate.translateX", f=1)
        cmds.connectAttr( each+"IK_jnt.translate.translateX", each+'_tblnd.color1.color1R', f=1)    
        cmds.connectAttr( each+"FK_jnt.translate.translateX", each+'_tblnd.color2.color2R', f=1)   
        cmds.connectAttr( each+"_tblnd.output.outputG", each+"_jnt.translate.translateY", f=1)
        cmds.connectAttr( each+"IK_jnt.translate.translateY", each+'_tblnd.color1.color1G', f=1)    
        cmds.connectAttr( each+"FK_jnt.translate.translateY", each+'_tblnd.color2.color2G', f=1)   
        cmds.connectAttr( each+"_tblnd.output.outputB", each+"_jnt.translate.translateZ", f=1)
        cmds.connectAttr( each+"IK_jnt.translate.translateZ", each+'_tblnd.color1.color1B', f=1)    
        cmds.connectAttr( each+"FK_jnt.translate.translateZ", each+'_tblnd.color2.color2B', f=1)   
        cmds.connectAttr(Controller, each+"_tblnd.blender", f=1)       

    def curve_rig(self):
        '''this builds a curve rig'''
        result = cmds.promptDialog( 
                    title='Building a CurveRig', 
                    message="Enter dimensions for chain - EG:", 
                    text="name", 
                    button=['Continue','Cancel'],
                    defaultButton='Continue', 
                    cancelButton='Cancel', 
                    dismissString='Cancel' )
        if result == 'Continue':
            mainName=cmds.promptDialog(q=1)
            if mainName:
                self.build_curve_rig(mainName)
            else:
                print "nothing collected"     
                
    def build_curve_rig(self, mainName):   
        '''function for building a curve rig'''
        getTopOpenGuides = cmds.ls(mainName + "*_guide")
        getKnotValue = len(getTopOpenGuides)
        curvename = mainName + "_crv"
        values = []
        for each in getTopOpenGuides:#get point values to build curve
            translate, rotate = self.locationXForm(each)
            values.append(translate)
        self.buildCurves(values, curvename, getKnotValue)  #build top curve    
        self.buildJointClusters(getTopOpenGuides, curvename)#build controllers and the bound joints for the top lid curve(this pulls into shapes)
        getRigGrp=cmds.group( em=True, name=mainName+'_Rig' )
        cmds.parent(mainName+"01_Clst_jnt", getRigGrp)
        cmds.parent(mainName+"_crv", getRigGrp)
        getFreeStuff=[(each) for each in cmds.ls(mainName+"*_grp")]
        for each in getFreeStuff: 
            cmds.parent(each, getRigGrp)        
    def buildCurves(self, values, name, getKnotValue):
        getKnotValueList = list(range(getKnotValue))
        getKnotValueList.insert(0, 0)
        getKnotValueList.append(getKnotValue)
        try:
            CurveMake = cmds.curve(n=name, d=1, p=values)
        except:
            print "Check the name of the guide you are using to build this"        
    def buildJointClusters(self, Guides, curvename):       
        '''function for skinning bones to a curve and making a curv rig'''
        cmds.select(cl=1) 
        collectJoints=[]
        for each in Guides:
            getTranslation=cmds.xform(each, q=1, t=1, ws=1)
            jointnames=each.split("_guide")[0]+"_Clst_jnt"
            cmds.joint(n=jointnames, p=getTranslation)     
            collectJoints.append(jointnames)   
        cmds.select(cl=1)
        getIKCurveCVs=cmds.ls(curvename+".cv[*]", fl=1)
        for each , bone in map(None, getIKCurveCVs[:-1], collectJoints[:-1]):
            cmds.select(clear=1)
            cmds.select(each)
            cmds.select( bone, add=1)
            cmds.bindSkin(each, bone, tsb=1)
        getlastjoint=collectJoints[-1:] 
        getverylastCVs=getIKCurveCVs[-1:]
        for each in getverylastCVs:
            cmds.select(each) 
            createdCluster=cmds.cluster()
            cmds.select(each, add=1)    
            cmds.parent(createdCluster, getlastjoint)  
        result = cmds.promptDialog( 
                    title='Choose Controller type', 
                    message="Enter dimensions for chain - EG:", 
                    text="StarSphere, Controller", 
                    button=['Continue','Cancel'],
                    defaultButton='Continue', 
                    cancelButton='Cancel', 
                    dismissString='Cancel' )
        if result == 'Continue':
            mainName=cmds.promptDialog(q=1)
            if mainName=="StarSphere":
                self.buildStarSphereClusterControl(Guides, collectJoints)
            elif mainName=="Controller":
                self.buildControllerClusterControl(Guides, collectJoints)
            else:
                print "nothing collected"               
                
    def IKMaker(self):          
        '''builds a rotational plane ik on a group of selected bones'''
        selObj=cmds.ls(sl=1)
        for each in selObj:
            getChildForIK=cmds.listRelatives(each, ad=1, typ="joint")
            cmds.ikHandle(n=each.split("_jnt")[0]+"_ik", sj=each, ee=getChildForIK[0], sol="ikRPsolver")

    def constraintMaker(self):
        '''this builds a constraint on a group of selected items to the first selected item'''
        result = cmds.promptDialog( 
                    title='Define Constraint', 
                    message="Enter dimensions for multi function:", 
                    text="orient_constraint, aim_constraint, parent_constraint, point_constraint, extrude_tube, xform", 
                    button=['Continue','Cancel'],
                    defaultButton='Continue', 
                    cancelButton='Cancel', 
                    dismissString='Cancel' )
        if result == 'Continue':
            ConstraintType=cmds.promptDialog(q=1)  
            if ConstraintType=="orient_constraint":
                getObj=cmds.ls(sl=1)
                getParent=getObj[0]
                for each in getObj[1:]:
                    cmds.orientConstraint(getParent, each, mo=1)               
            elif ConstraintType=="aim_constraint":
                getObj=cmds.ls(sl=1)
                getParent=getObj[0]
                for each in getObj[1:]:
                    cmds.aimConstraint(getParent, each, mo=1)   
            elif ConstraintType=="parent_constraint":
                getObj=cmds.ls(sl=1)
                getParent=getObj[0]
                for each in getObj[1:]:
                    cmds.parentConstraint(getParent, each, mo=1)   
            elif ConstraintType=="point_constraint":
                getObj=cmds.ls(sl=1)
                getParent=getObj[0]
                for each in getObj[1:]:
                    cmds.pointConstraint(getParent, each, mo=1)              
            elif ConstraintType=="extrude_tube":
                getObj=cmds.ls(sl=1)
                getParent=getObj[0]
                for each in getObj[1:]:
                    extrude(getParent, each, ch=1, rn=0, po=1, et=2, ucp=1, fpt=1, upn=1, rotation=0, scale=1, rsp=1)  
            elif ConstraintType=="xform":
                getObj=cmds.ls(sl=1)
                getParent=getObj[0]
                for each in getObj[1:]:
                    getTranslation, getRotation=self.locationXForm(getParent)
                    each.setTranslation(getTranslation)
                    each.setTranslation(getRotation)
            else:
                print "nothing performed"

                    
    def buildStarSphereClusterControl(self, Guides, joints):
        '''uses the CCCircle(sphere controller) script to make a broken circle shaped controller(if you get tired of seeing circles)'''
        num0, num1, num2, num3 = 1, .5, .7, .9
        colour=13
        for each, joint in map(None, Guides, joints):
            name=each.split("_guide")[0]+"_Ctrl"
            grpname=each.split("_guide")[0]+"_grp"
            getTranslation, getRotation=self.locationXForm(each)
            self.CCCircle(name, grpname, num0, num1, num2, num3, getTranslation, getRotation, colour)
            cmds.parentConstraint(name,joint)
            
    def buildControllerClusterControl(self, Guides, joints):
        '''builds the sphere controller used in the build curve rig function'''
        result = cmds.promptDialog( 
                    title='Define Axis of Controller', 
                    message="Enter dimensions for chain - EG:", 
                    text="X, Y, Z", 
                    button=['Continue','Cancel'],
                    defaultButton='Continue', 
                    cancelButton='Cancel', 
                    dismissString='Cancel' )
        if result == 'Continue':
            mainName=cmds.promptDialog(q=1)
            if mainName=="X":
                nrx=1
                nry=0
                nrz=0                  
            elif mainName=="Y":
                nrx=0
                nry=1
                nrz=0   
            elif mainName=="Z":
                nrx=0
                nry=0
                nrz=1
            else:
                print "nothing collected"
        result = cmds.promptDialog( 
                    title='Define Colour of Controller', 
                    message="Enter dimensions for chain - EG:", 
                    text="Red, Green, Blue, Yellow, Maroon, FGreen", 
                    button=['Continue','Cancel'],
                    defaultButton='Continue', 
                    cancelButton='Cancel', 
                    dismissString='Cancel' )
        if result == 'Continue':
            mainName=cmds.promptDialog(q=1)
            if mainName=="Red":
                colour=13          
            elif mainName=="Blue":
                colour=6   
            elif mainName=="Green":
                colour=14
            elif mainName=="Yellow":
                colour=22
            elif mainName=="Maroon":
                colour=31        
            elif mainName=="FGreen":
                colour=23                      
            else:
                print "nothing collected"
        result = cmds.promptDialog( 
                    title='Define size of Controller', 
                    message="Enter dimensions for chain - EG:", 
                    text="6", 
                    button=['Continue','Cancel'],
                    defaultButton='Continue', 
                    cancelButton='Cancel', 
                    dismissString='Cancel' )
        if result == 'Continue':
            size=cmds.promptDialog(q=1)     
        else:
            print "nothing collected"     
        self.ClstrControl(size, colour, nrx, nry, nrz, Guides, joints)
            
    def ClstrControl(self, size, colour, nrx, nry, nrz, Guides, joints):       
        for each, joint in map(None, Guides, joints):
            name=each.split("_guide")[0]+"_Ctrl"
            grpname=each.split("_guide")[0]+"_grp"
            getTranslation, getRotation=self.locationXForm(each)
            self.buildCtrl(each, name, grpname, getTranslation, getRotation, size, colour, nrx, nry, nrz)
            cmds.parentConstraint(name,joint)

    def autoCurveRig(self, Guides, curvename, size, colour, nrx, nry, nrz):    
        '''the build curve rig function''' 
        getKnotValue = len(Guides)
        curvename = Guides + "_crv"
        values = []
        for each in Guides:#get point values to build curve
            translate, rotate = self.locationXForm(each)
            values.append(translate)
        getKnotValueList = list(range(getKnotValue))
        getKnotValueList.insert(0, 0)
        getKnotValueList.append(getKnotValue)
        CurveMake = cmds.curve(n=name, d=1, p=values)           
        cmds.select(cl=1) 
        collectJoints=[]
        for each in Guides:
            getTranslation=cmds.xform(each, q=1, t=1, ws=1)
            jointnames=each.split("_guide")[0]+"_Clst_jnt"
            cmds.joint(n=jointnames, p=getTranslation)     
            collectJoints.append(jointnames)   
        cmds.select(cl=1)
        getIKCurveCVs=cmds.ls(curvename+".cv[*]", fl=1)
        for each , bone in map(None, getIKCurveCVs[:-1], collectJoints[:-1]):
            cmds.select(clear=1)
            cmds.select(each)
            cmds.select( bone, add=1)
            cmds.bindSkin(each, bone, tsb=1)
        getlastjoint=collectJoints[-1:] 
        getverylastCVs=getIKCurveCVs[-1:]
        for each in getverylastCVs:
            cmds.select(each) 
            createdCluster=cmds.cluster()
            cmds.select(each, add=1)    
            cmds.parent(createdCluster, getlastjoint)  
        self.ClstrControl(size, colour, nrx, nry, nrz)

    def cubeI(self, name, grpname, num, transformWorldMatrix, rotateWorldMatrix, colour):
        '''builds a cube controller'''
        xCubeMake=cmds.curve(n=name, d=1, p =[(-num, num, num), (num, num, num), (num, num, -num), (-num, num, -num), (-num, num, num), (-num, -num, num), (-num, -num, -num), (num, -num, -num), (num, -num, num), (-num, -num, num), (num, -num, num), (num, num, num), (num, num, -num), (num, -num, -num), (-num, -num, -num), (-num, num, -num)])
        self.locationEcho(xCubeMake, grpname, colour, transformWorldMatrix, rotateWorldMatrix)   

    def squareI(self, name, grpname, num, transformWorldMatrix, rotateWorldMatrix, colour):
        '''builds a square controller'''
        xSquareMake=cmds.curve(n=name, d=1, p =[(-num, 0.0, num), (num, 0.0, num), (num, 0.0, -num), (-num, 0.0, -num),(-num, 0.0, num)])
        self.locationEcho(xSquareMake, grpname, colour, transformWorldMatrix, rotateWorldMatrix) 

    def rectI(self, name, grpname, numlen, numwid, transformWorldMatrix, rotateWorldMatrix, colour):
        '''builds a rectangle controller'''
        xSquareMake=cmds.curve(n=name, d=1, p =[(-numlen, 0.0, numwid), (numlen, 0.0, numwid), (numlen, 0.0, -numwid), (-numlen, 0.0, -numwid),(-numlen, 0.0, numwid)])
        self.locationEcho(xSquareMake, grpname, colour, transformWorldMatrix, rotateWorldMatrix)   
        
    def TriI(self, name, grpname, num, transformWorldMatrix, rotateWorldMatrix, colour):
        '''builds a triangle controller'''
        narrow=num/3.9
        xSquareMake=cmds.curve(n=name, d=1, p =[(0.0, 0.0, 0.0), (0.0, num, narrow), (0.0, num, -narrow), (0.0, 0.0,0.0)])
        cmds.move(0, 0, 0, xSquareMake+".rotatePivot" ,r=1, rpr=1 )
        self.locationEcho(xSquareMake, grpname, colour, transformWorldMatrix, rotateWorldMatrix)        

    def BuildJackI(self):
        name, grpname, num, transformWorldMatrix, rotateWorldMatrix, colour="Jack_Ctrl", "Jack_grp", 3, [0.0,0.0,0.0], [0.0,0.0,0.0], 13
        self.JackI(name, grpname, num, transformWorldMatrix, rotateWorldMatrix, colour)
 

    def JackI(self, name, grpname, num, transformWorldMatrix, rotateWorldMatrix, colour):
        '''creates a controller that looks like a locator'''
        narrow=num/3.9
        xSquareMake=cmds.curve(n=name, d=1, p =[(0.0, 0.0, num), (0.0,0.0,0.0), (0.0, 0.0, -num), (0.0,0.0,0.0), (num, 0.0, 0.0), (0.0,0.0,0.0), (-num, 0.0, 0.0), (0.0,0.0,0.0), (0.0, num, 0.0), (0.0,0.0,0.0), (0.0, -num, 0.0), (0.0,0.0,0.0)])
        self.locationEcho(xSquareMake, grpname, colour, transformWorldMatrix, rotateWorldMatrix)  

    def PrimI(self, name, grpname, num, transformWorldMatrix, rotateWorldMatrix, colour):
        '''creates a primitive controller'''
        xSquareMake=cmds.curve(n=name, d=1, p =[( num, 0, num ), (num, 0, -num), (-num*2, 0, 0 ), (num, num, 0), ( num, 0, 0), (num, -num, 0 ), (-num*2, 0, 0 ),( num, 0, num )])
        cmds.rotate(0, 90,0, name)
        cmds.makeIdentity(name, a=True, t=1, s=1, r=1, n=0)
        self.locationEcho(xSquareMake, grpname, colour, transformWorldMatrix, rotateWorldMatrix)  

    def ballArrowI(self, name, grpname, transformWorldMatrix, rotateWorldMatrix, colour):
        '''this creates a handle controller with an arrow'''
        xSquareMake=cmds.curve(n=name, d=1, p =[(0,24,0),
        (-4,24,0),
        (0,32,0),
        (4,24,0),
        (0,24,0),
        (0,4,0),
        (1.034188,3.860232,0),
        (1.998312,3.460872,0),(2.828448,2.82845,0),(3.460875,1.998311,0),(3.860228,1.034189,0),(4.00003,-2.3063e-007,0),
        (3.860228,-1.034188,0),(3.460875,-1.998312,0),(2.828448,-2.828448,0),(1.998312,-3.460875,0),(1.034188,-3.860228,0),
        (0,-4.00003,0),(-1.034188,-3.860228,0),(-1.998312,-3.460875,0),(-2.828448,-2.828448,0),(-3.460875,-1.998312,0),
        (-3.860228,-1.034188,0),(-4.00003,-2.3063e-007,0),(-3.860228,1.034189,0),(-3.460875,1.998311,0),
        (-2.828448,2.82845,0),(-1.998312,3.460872,0),(-1.034188,3.860232,0), (0,4,0)])
        self.locationEcho(xSquareMake, grpname, colour, transformWorldMatrix, rotateWorldMatrix)  

    def handleI(self, name, grpname, transformWorldMatrix, rotateWorldMatrix, colour):
        '''creates a handle controller'''
        xSquareMake=cmds.curve(n=name, d=1, p= [(0,10.112068,0),(-0.373493,10.162557,0),(-0.721682,10.306782,0),(-1.021482,10.53518,0),(-1.24988,10.83498,0),
        (-1.394105,11.183169,0),(-1.444594,11.556662,0),(-1.394105,11.930155,0),(-1.24988,12.278343,0),(-1.021482,12.578144,0),
        (-0.721682,12.806541,0),(-0.373493,12.950768,0),(0,13.001244,0),(0.373493,12.950768,0),(0.721682,12.806541,0),
        (1.021482,12.578144,0),(1.24988,12.278343,0),(1.394105,11.930155,0),(1.444594,11.556662,0),(1.394105,11.183169,0),
        (1.24988,10.83498,0),(1.021482,10.53518,0),(0.721682,10.306782,0),(0.373493,10.162557,0),(0,10.112068,0),(0,0,0)])
        self.locationEcho(xSquareMake, grpname, colour, transformWorldMatrix, rotateWorldMatrix)  

    def makeGuideCCC(self):
        '''stand alone build guides at a selection or creates new at world center'''
        selectionCheck=cmds.ls(sl=1)
        num0, num1, num2, num3, colour=1, .4, .9, .7, 22
        if selectionCheck:
            for each in selectionCheck:
                name, grpname=each+"_guide", each+"_guide_grp"
                transformWorldMatrix, rotateWorldMatrix=self.locationXForm(each)
                self.CCCircle(name, grpname, num0, num1, num2, num3, transformWorldMatrix, rotateWorldMatrix, colour) 
        else:
            name, grpname="name_guide", "name_guide_grp"
            transformWorldMatrix=(0, 0, 0) 
            rotateWorldMatrix=(0, 0, 0)           
            self.CCCircle(name, grpname, num0, num1, num2, num3, transformWorldMatrix, rotateWorldMatrix, colour)        
        
    def CCCircle(self, name, grpname, num0, num1, num2, num3, transformWorldMatrix, rotateWorldMatrix, colour):
        '''creates a sphere controller'''
        xSquareMake=cmds.curve(n=name, d=1, p =[(0,num0, 0),(0, num2, num1),(0, num3, num3),(0, num1, num2),(0, 0, num0),(0, -num1, num2),(0, -num3, num3),(0, -num2, num1),(0, -num0, 0),(0, -num2, -num1),(0, -num3, -num3),(0, -num1, -num2),
                                                (0, 0, -num0),(0, num1, -num2),(0, num3, -num3),(0, num2, -num1),(0,num0, 0),(num1, num2, 0),(num3, num3, 0),(num2, num1, 0),(num0, 0, 0),(num2, -num1, 0),(num3, -num3, 0),(num1, -num2, 0),
                                                (0, -num0, 0),(-num1, -num2, 0),(-num3, -num3, 0),(-num2, -num1, 0),(-num0, 0, 0),(-num2, num1, 0),(-num3, num3, 0),(-num1, num2, 0),(0,num0, 0),(0, num2, -num1),(0, num3, -num3),(0, num1, -num2),
                                                (0, 0, -num0),(-num1, 0, -num2),(-num3, 0, -num3),(-num2, 0, -num1),(-num0, 0, 0),(-num2, 0, num1),(-num3, 0, num3),(-num1, 0, num2),(0, 0, num0),(num1, 0, num2),(num3, 0, num3),(num2, 0, num1),
                                                (num0, 0, 0),(num2, 0, -num1),(num3, 0, -num3),(num1, 0, -num2),(0, 0, -num0)])
        self.locationEcho(xSquareMake, grpname, colour, transformWorldMatrix, rotateWorldMatrix)  
        
    def locationEcho(self, Shape, groupname, colour, transform, rotate):
        '''sets colour of shape, creates group and then moves group to location'''
        cmds.setAttr(Shape+".overrideEnabled", 1)
        cmds.setAttr(Shape+".overrideColor", colour)
        cmds.group(n=groupname)
        grpObj=cmds.ls(sl=1)
        cmds.xform(grpObj[0], ws=1, t=transform)
        cmds.xform(grpObj[0], ws=1, ro=rotate)

    def controlFirstValueChildOn(self, Controller, Child, defaultSet, ChildActivatedValue, ChildDeactivatedValue, ControllerOnValue, ControllerOffValue):
        '''sets a driven key on two items only. if child is in on state, the controller will be keyed to first value'''
        cmds.setAttr(Child, lock=0) 
        cmds.setAttr(Controller, ControllerOffValue)
        cmds.setAttr(Child,ChildActivatedValue)
        cmds.setDrivenKeyframe(Child, cd=Controller)
        cmds.setAttr(Controller, ControllerOnValue)
        cmds.setAttr(Child, ChildDeactivatedValue)
        cmds.setDrivenKeyframe(Child, cd=Controller)
        cmds.setAttr(Controller, defaultSet)
        cmds.setAttr(Child, lock=1)
        
    def controlSecondValueChildOn(self, Controller, Child, defaultSet, ChildActivatedValue, ChildDeactivatedValue, ControllerOnValue, ControllerOffValue):
        '''sets a driven key on two items only. if child is in on state, the controller will be keyed to second value'''
        cmds.setAttr(Child, lock=0) 
        cmds.setAttr(Controller, ControllerOnValue)
        cmds.setAttr(Child, ChildActivatedValue)
        cmds.setDrivenKeyframe(Child, cd=Controller)
        cmds.setAttr(Controller, ControllerOffValue)
        cmds.setAttr(Child, ChildDeactivatedValue)
        cmds.setDrivenKeyframe(Child, cd=Controller)
        cmds.setAttr(Controller, defaultSet)    
        cmds.setAttr(Child, lock=1)    
        
    def doubleSetDrivenKey_constraint(self, Controller, Child, child_one_constraint, child_two_constraint, firstValue, secondValue):
        '''sets a driven key on two items only. if child is in on state, the controller will be keyed to second value'''
        cmds.setAttr(child_one_constraint, lock=0)
        cmds.setAttr(child_two_constraint, lock=0) 
        cmds.setAttr(Controller, secondValue)     
        cmds.setAttr(child_one_constraint, secondValue)
        cmds.setAttr(child_two_constraint, firstValue)         
        cmds.setDrivenKeyframe(Child, cd=Controller)
        cmds.setAttr(Controller, firstValue)     
        cmds.setAttr(child_one_constraint, firstValue)
        cmds.setAttr(child_two_constraint, secondValue)         
        cmds.setDrivenKeyframe(Child, cd=Controller)
        cmds.setAttr(Controller, firstValue) 
        cmds.setAttr(child_one_constraint, lock=1)
        cmds.setAttr(child_two_constraint, lock=1) 

    def setBuilder(self, setName, getMarks):
        if objExists(setName):
            pass
        else:
            cmds.sets(n=setName, co=3)
        for each in getMarks:
            cmds.sets(each, add=setName)


    def buildRoughCalamari(self, size):
        '''this creates cubes as a low res standin for mesh on a bone heirarchy. handy to check for flipping and orientation'''
        selObj=cmds.ls(sl=1)
        #----get joint heirarchy
        getGrp=cmds.listRelatives(selObj[0], ad=1, typ="joint")
        getGrp.append(selObj[0])
        cmds.select(cl=1) 
        Ggrp=cmds.CreateEmptyGroup()
        #----create group
        cmds.rename(Ggrp, "calamari_grp")
        getSetMarks=[]      
        setName="calamari" 
        #----create lambert shaders
        FVfirst = cmds.shadingNode('lambert', asShader=True, n="calamariFVOne_shd")
        getFVfirst=[FVfirst]
        self.setBuilder(setName, getFVfirst)
        cmds.setAttr("calamariFVOne_shd.color", 1, 0, 0, type="double3")
        FVSecond = cmds.shadingNode('lambert', asShader=True, n="calamariFVTwo_shd")
        getFVSecond=[FVSecond]
        self.setBuilder(setName, getFVSecond)
        cmds.setAttr("calamariFVTwo_shd.color", 0, 1, 0, type="double3")
        FVThird = cmds.shadingNode('lambert', asShader=True, n="calamariFVThree_shd")
        getFVThird=[FVThird]
        self.setBuilder(setName, getFVThird)
        cmds.setAttr("calamariFVThree_shd.color", 0, 0, 1, type="double3")
        FVfourth = cmds.shadingNode('lambert', asShader=True, n="calamariFVFour_shd")
        getFVfourth=[FVfourth]
        self.setBuilder(setName, getFVfourth)
        cmds.setAttr("calamariFVFour_shd.color", 0.5, 0, 0.5, type="double3")
        FVfifth = cmds.shadingNode('lambert', asShader=True, n="calamariFVFive_shd")
        getFVfifth=[FVfifth]
        self.setBuilder(setName, getFVfifth)
        cmds.setAttr("calamariFVFive_shd.color", 1, 1, 0, type="double3")
        #----build cubes at joints and constrain
        for each in getGrp: 
            transformWorldMatrix, rotateWorldMatrix=self.locationXForm(each)
            buildCube=cmds.polyCube(n="calamari_"+each+"_GEO", w=size, h=size, d=size, sx=1, sy=1, sz=1, ax=[0, 1, 0], cuv=4, ch=1)
            getSetMarks.append(buildCube[0])
            cmds.move(transformWorldMatrix[0],transformWorldMatrix[1], transformWorldMatrix[2], buildCube[0])
            cmds.rotate(rotateWorldMatrix[0],rotateWorldMatrix[1], rotateWorldMatrix[2], buildCube[0])            
            cmds.parent(buildCube[0],"calamari_grp")
            cmds.parentConstraint(each, buildCube[0], mo=0, w=1)
        #----put cubes in set
        self.setBuilder(setName, getSetMarks)
        #---assign different cube faces to lambert colours
        for item in getSetMarks:
            select(item+".f[1]", r=1)
            cmds.hyperShade(assign=str(FVfirst))
            select(item+".f[2]", r=1)
            cmds.hyperShade(assign=str(FVSecond))
            select(item+".f[3]", r=1)
            cmds.hyperShade(assign=str(FVThird))
            select(item+".f[4]", r=1)
            cmds.hyperShade(assign=str(FVfourth))
            select(item+".f[5]", r=1)
            cmds.hyperShade(assign=str(FVfifth))



    def buildRoughCalamariV1(self, size):
        '''this creates cubes as a low res standin for mesh on a bone heirarchy. handy to check for flipping'''
        selObj=cmds.ls(sl=1)
        getGrp=cmds.listRelatives(selObj[0], ad=1, typ="joint")
        getGrp.append(selObj[0])
        for each in getGrp:
            transformWorldMatrix, rotateWorldMatrix=self.locationXForm(each)
            buildCube=cmds.polyCube(n="calamariCube", w=size, h=size, d=size, sx=1, sy=1, sz=1, ax=[0, 1, 0], cuv=4, ch=1)
            cmds.move(transformWorldMatrix[0],transformWorldMatrix[1], transformWorldMatrix[2], buildCube[0])
            cmds.rotate(rotateWorldMatrix[0],rotateWorldMatrix[1], rotateWorldMatrix[2], buildCube[0])
            cmds.parent(buildCube[0], each)



    def buildRoughCalamariV1(self, size):
        '''this creates cubes as a low res standin for mesh on a bone heirarchy. handy to check for flipping'''
        selObj=cmds.ls(sl=1)
        getGrp=cmds.listRelatives(selObj[0], ad=1, typ="joint")
        getGrp.append(selObj[0])
        for each in getGrp:
            transformWorldMatrix, rotateWorldMatrix=self.locationXForm(each)
            buildCube=cmds.polyCube(n="calamariCube", w=size, h=size, d=size, sx=1, sy=1, sz=1, ax=[0, 1, 0], cuv=4, ch=1)
            cmds.move(transformWorldMatrix[0],transformWorldMatrix[1], transformWorldMatrix[2], buildCube[0])
            cmds.rotate(rotateWorldMatrix[0],rotateWorldMatrix[1], rotateWorldMatrix[2], buildCube[0])
            cmds.parent(buildCube[0], each)
            
    def cubeCala(self, name, grpname, transformWorldMatrix, rotateWorldMatrix, size):
        buildCube=cmds.polyCube(n=name+"calaCube", w=size, h=size, d=size, sx=1, sy=1, sz=1, ax=[0, 1, 0], cuv=4, ch=1)
        cmds.move(transformWorldMatrix[0],transformWorldMatrix[1], transformWorldMatrix[2], buildCube[0])
        cmds.rotate(rotateWorldMatrix[0],rotateWorldMatrix[1], rotateWorldMatrix[2], buildCube[0])
            
    def groupShapes(self):
        selObj=cmds.ls(sl=1, fl=1)
        for item in selObj:
            try:
                cmds.parent(item, w=1)
            except:
                pass
            cmds.makeIdentity(item, a=True, t=1, s=1, r=1, n=0)
        shapeBucket=[]
        parentCurve=selObj[0]
        for item in selObj[1:]:
            getShapes= cmds.listRelatives(item, ad=1, typ="shape")
            shapeBucket.append(getShapes[0])
        shapeBucket.append(parentCurve)
        cmds.parent(shapeBucket, parentCurve, r=1, s=1)


            
    def buildSkinCasing(self):
        '''this creates a low res cylinder to a selected bone for simplistic skinning to copy from'''
        selObj=cmds.ls(sl=1)
        size=self.fetchSize()
        sizeHieght=(size/2)+size
        sizeFindPiv=size/2
        for each in selObj:
            transformWorldMatrix, rotateWorldMatrix=self.locationXForm(each)
            buildCube=cmds.polyCylinder(n=each+"loresskin", r=size, h=sizeHieght, sx=8, sy=5, sz=0, ax=(0, 1, 0), rcp=0, cuv=3, ch=1)
            cmds.move(0, sizeFindPiv, 0, buildCube[0]+".rotatePivot" ,r=1, rpr=1 )
            cmds.move(transformWorldMatrix[0],transformWorldMatrix[1], transformWorldMatrix[2], buildCube[0])
            cmds.rotate(rotateWorldMatrix[0],rotateWorldMatrix[1], rotateWorldMatrix[2], buildCube[0])
            #cmds.skinCluster(buildCube[0], each) 
            #cmds.parent(buildCube[0], each)
    def swapInfluenceSelect(self):
        '''this swaps influence selection to another joint collection of influences in scene by name type'''
        selObj=cmds.ls(sl=1)
        getallnames=cmds.ls("*Rig:*")
        bucket=[]
        for each in  getallnames:
            foundFirst=each.split(":")[0]
            bucket.append(foundFirst)
        bucket=set(bucket)
        global jointSelect
        winName = "Swap Influence select"
        winTitle = winName
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)

        window = cmds.window(winName, title=winTitle, tbm=1, w=250, h=100 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=150)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        
        cmds.rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))
        jointSelect=cmds.optionMenu( label='joints')
        for each in bucket:
            cmds.menuItem( label=each)            
        cmds.button (label='set joint', p='listBuildButtonLayout', command = self.set_joint_select)
        cmds.showWindow(window)
     
    def set_joint_select(self, arg=None):
        queryJoint=cmds.optionMenu(jointSelect, q=1, v=1)
        getSel=cmds.ls(sl=1)
        getNames=[]
        for each in getSel:
            getName=each.split(":")
            getPArt=getName[-1:]
            getNames.append(queryJoint+":"+getPArt[0])
        cmds.select(getNames[0])
        for each in getNames[1:]:
            cmds.select(each, add=1)
        
#         selObj=cmds.ls(sl=1)
#         size=self.fetchSize()
#         sizeHieght=(size/2)+size
#         sizeFindPiv=size/2
#         for each in selObj:
#             transformWorldMatrix, rotateWorldMatrix=self.locationXForm(each)
#             buildCube=cmds.polyCylinder(n=each+"loresskin", r=size, h=sizeHieght, sx=8, sy=5, sz=0, ax=(0, 1, 0), rcp=0, cuv=3, ch=1)
#             cmds.move(0, sizeFindPiv, 0, buildCube[0]+".rotatePivot" ,r=1, rpr=1 )
#             cmds.move(transformWorldMatrix[0],transformWorldMatrix[1], transformWorldMatrix[2], buildCube[0])
#             cmds.rotate(rotateWorldMatrix[0],rotateWorldMatrix[1], rotateWorldMatrix[2], buildCube[0])
#             #cmds.skinCluster(buildCube[0], each) 
#             #cmds.parent(buildCube[0], each)
            
    def BlinkSculpt(self):
        '''this attaches a blink sculpt if a characters eyes are hollowing out'''
        eyeBones=[]
        Eye_L_joint=(cmds.ls("*:*Eye_L_jnt")[0])
        eyeBones.append(Eye_L_joint)
        Eye_R_joint=(cmds.ls("*:*Eye_R_jnt")[0])
        eyeBones.append(Eye_R_joint)
        selObj=cmds.ls(sl=1)
        mesh=selObj[0]
        for each in eyeBones:
            try:
                getname=each.split(":")[1]
            except:
                getname=each
            transformWorldMatrix, rotateWorldMatrix=self.locationXForm(each)
            createSculpt=cmds.sculpt(mesh, n=getname.split("_jnt")[0]+"_scpt", mode="flip", insideMode="even", maxDisplacement=2, dropoffType="linear", dropoffDistance=7, groupWithLocator=1, objectCentered=1)
            cmds.move(transformWorldMatrix[0], transformWorldMatrix[1], transformWorldMatrix[2], createSculpt)
            cmds.parent(createSculpt, each)


    def makeDialog(self, titleText, messageText, textText):
        '''make dialog box function'''
        result = cmds.promptDialog( 
            title=str(titleText[0]), 
            message=str(messageText[0]), 
            text=str(textText[0]),
            button=['Continue','Cancel'],
            defaultButton='Continue', 
            cancelButton='Cancel', 
            dismissString='Cancel' )
        if result == 'Continue':            
            mainName=cmds.promptDialog(q=1)
            return mainName
        else:
            print "nothing collected"    
            
    def makeShapeV1(self):
        '''this builds controller shapes'''
        titleText=('Controller'), 
        messageText=("enter controller type"), 
        textText=("cube, sphere, circle, square, rectangle, prim, triangle, cube, jack, ballarrow, handle, joint, locator"), 
        mainName=self.makeDialog(titleText, messageText, textText)
        selectionCheck=self.selection_grab()
        if selectionCheck:
#            for each in selectionCheck:
            self.CreateShapeFunction(selectionCheck, mainName)
        else:
            selectionCheck=None
            self.CreateShapeFunction(selectionCheck, mainName)  



    def controllerUI(self):
        # selectionCheck=self.selection_grab()
        shapes=["cube", "sphere", "circle", "square", "rectangle", "prim", "triangle", "calamari", "jack", "ballarrow", "handle", "joint", "locator"]
        winName = "Controller"
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
        cmds.text(label="Size",  p='txvaluemeter', w=80, h=25)       
        self.size=cmds.textField(w=40, h=25, p='txvaluemeter', text="1")  
        self.colour=13 
        self.shapeType=optionMenu( label='')   
        for item in shapes:
            menuItem(item)   
        button (label='Go', p='txvaluemeter', command = lambda *args:self.CreateControlFunction(mainName=cmds.optionMenu(self.shapeType, q=1, sl=1), size=textField(self.size,q=1, text=1), colour=self.colour))
        showWindow(window)

    def CreateControlFunction(self, mainName, size, colour):
        selectionCheck=self.selection_grab()
        colour=13
        size=int(size)   
        try:
            for item in selectionCheck:  
                item=[item]
                self.optionFunctionForShape(item, mainName, size, colour)
                cmds.pickWalk(d="Down")
                getControl=cmds.ls(sl=1, fl=1)
                # cmds.parentConstraint(getControl, item)
                cmds.parentConstraint(getControl[0], item, mo=1)
        except:
            print "you need to make a selection to add this control to"
            return


    def makeShape(self, arg=None):
        # selectionCheck=self.selection_grab()
        shapes=["cube", "sphere", "circle", "square", "rectangle", "prim", "triangle", "calamari", "jack", "ballarrow", "handle", "joint", "locator"]
        winName = "Shapes"
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
        cmds.text(label="Size",  p='txvaluemeter', w=80, h=25)         
        # cmds.gridLayout('infotext', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(80, 18))         
        self.size=cmds.textField(w=40, h=25, p='txvaluemeter', text="1")   
        self.colour=13
        self.shapeType=optionMenu( label='')   
        for item in shapes:
            menuItem(item)   
        button (label='Go', p='txvaluemeter', command = lambda *args:self.CreateShapeFunction(mainName=cmds.optionMenu(self.shapeType, q=1, sl=1), size=textField(self.size,q=1, text=1), colour=self.colour))
        showWindow(window)

    def CreateShapeFunction(self, mainName, size, colour):
        selectionCheck=self.selection_grab()
        size=int(size)   
        try:
            for item in selectionCheck:  
                item=[item]
                self.optionFunctionForShape(item, mainName, size, colour)
        except:
            self.optionFunctionForShape(selectionCheck, mainName, size, colour)

    def optionFunctionForShape(self, each, mainName, size, colour):
        if mainName==2:#sphere
            # colour=self.fetchColour()
            self.getSphere(each, colour, size)
        if mainName==3:#circle
            # colour=self.fetchColour()
            self.getcircle(each, colour, size)
        if mainName==4:#square
            # colour=self.fetchColour()
            self.getsquare(each, colour, size)
        if mainName==5:#rectangle
            # colour=self.fetchColour()
            self.getrectangle(each, colour, size)
        if mainName==6:#prim
            # colour=self.fetchColour()
            self.getprim(each, colour, size)
        if mainName==7:#triangle
            # colour=self.fetchColour()
            self.gettri(each, colour, size)
        if mainName==1:#cube
            # colour=self.fetchColour()
            self.getcube(each, colour, size)
        if mainName==9:#jack
            # colour=self.fetchColour()
            self.getjack(each, colour, size)
        if mainName==12:#joint
            self.getJoint(each, size)      
        if mainName==10:#ballarrow
            # colour=self.fetchColour()
            self.getballarrow(each, colour, size) 
        if mainName==8:#calamari
            # colour=self.fetchColour()
            self.getCubeCala(each, colour, size)   
        if mainName==11:#handle
            # colour=self.fetchColour()
            self.gethandle(each, colour, size)
        if mainName==13:#locator
            # colour=self.fetchColour()
            self.getLoc(each, colour, size) 
            
    def getSphere(self, selectionCheck, colour, size):
        # titleText=('Define dimension'),                        
        # messageText=("Enter 4 numbers"), 
        number=("1, .4, .9, .7, 22")
        # size=self.makeDialog(titleText, messageText, textText)
        getNumbers= number.split(', ')
        numberBucket=[]
        for each in getNumbers:
            each=float(each)
            each=each*size
            numberBucket.append(each)
        num0, num1, num2, num3=numberBucket[0],numberBucket[1],numberBucket[2],numberBucket[3]
        if selectionCheck:
            for each in selectionCheck:
                transformWorldMatrix, rotateWorldMatrix=self.selection_location_type(each)
                name, grpname=each+"_Ctrl", each+"_grp"
                self.CCCircle(name, grpname, num0, num1, num2, num3, transformWorldMatrix, rotateWorldMatrix, colour)
        else:
            name, grpname="name_Ctrl", "name_grp"
            transformWorldMatrix=(0, 0, 0) 
            rotateWorldMatrix=(0, 0, 0)  
            self.CCCircle(name, grpname, num0, num1, num2, num3, transformWorldMatrix, rotateWorldMatrix, colour)

    def getcircle(self, selectionCheck, colour, size):            
        nrx, nry, nrz = 0, 1, 0
        # size=self.fetchSize()
        if selectionCheck:
            for each in selectionCheck:
                name, grpname=each+"_Ctrl", each+"_grp"
                transformWorldMatrix, rotateWorldMatrix=self.selection_location_type(each)            
                self.buildCtrl(each, name, grpname, transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)
        else:
            each=None
            name, grpname="name_Ctrl", "name_grp"
            transformWorldMatrix=(0, 0, 0) 
            rotateWorldMatrix=(0, 0, 0)         
            self.buildCtrl(each, name, grpname, transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)            
    def getsquare(self, selectionCheck, colour, size):           
        # size=self.fetchSize()
        if selectionCheck:
            for each in selectionCheck:
                name, grpname=each+"_Ctrl", each+"_grp"
                transformWorldMatrix, rotateWorldMatrix=self.selection_location_type(each)            
                self.squareI(name, grpname, size, transformWorldMatrix, rotateWorldMatrix, colour)
        else:
            name, grpname="name_Ctrl", "name_grp"
            transformWorldMatrix=(0, 0, 0) 
            rotateWorldMatrix=(0, 0, 0)            
            self.squareI(name, grpname, size, transformWorldMatrix, rotateWorldMatrix, colour)
            
    def getrectangle(self, selectionCheck, colour, size):                        
        # titleText=('Define dimension'),                        
        # messageText=("Enter 2 numbers"), 
        size=("4, 5")
        # size=self.makeDialog(titleText, messageText, textText)
        getParts=size.split(', ')
        numlen, numwid= int(getParts[0]), int(getParts[1])
        if selectionCheck:
            for each in selectionCheck:
                name, grpname=each+"_Ctrl", each+"_grp"
                transformWorldMatrix, rotateWorldMatrix=self.selection_location_type(each)           
                self.rectI(name, grpname, numlen, numwid, transformWorldMatrix, rotateWorldMatrix, colour)
        else:
            name, grpname="name_Ctrl", "name_grp"
            transformWorldMatrix=(0, 0, 0) 
            rotateWorldMatrix=(0, 0, 0)    
            self.rectI(name, grpname, numlen, numwid, transformWorldMatrix, rotateWorldMatrix, colour)
                                  
    def getprim(self, selectionCheck, colour, size):                                    
        # size=self.fetchSize()
        if selectionCheck:
            for each in selectionCheck:
                name, grpname=each+"_Ctrl", each+"_grp"
                transformWorldMatrix, rotateWorldMatrix=self.selection_location_type(each)           
                self.PrimI(name, grpname, size, transformWorldMatrix, rotateWorldMatrix, colour)
        else:
            name, grpname="name_Ctrl", "name_grp"
            transformWorldMatrix=(0, 0, 0) 
            rotateWorldMatrix=(0, 0, 0)    
            self.PrimI(name, grpname, size, transformWorldMatrix, rotateWorldMatrix, colour)                     
    def gettri(self, selectionCheck, colour, size):                                                
        # size=self.fetchSize()
        if selectionCheck:
            for each in selectionCheck:
                name, grpname=each+"_Ctrl", each+"_grp"
                transformWorldMatrix, rotateWorldMatrix=self.selection_location_type(each)           
                self.TriI(name, grpname, size, transformWorldMatrix, rotateWorldMatrix, colour)
        else:
            name, grpname="name_Ctrl", "name_grp"
            transformWorldMatrix=(0, 0, 0) 
            rotateWorldMatrix=(0, 0, 0)    
            self.TriI(name, grpname, size, transformWorldMatrix, rotateWorldMatrix, colour)             
    def getcube(self, selectionCheck, colour, size):                                                       
        # size=self.fetchSize()
        if selectionCheck:
            for each in selectionCheck:
                name, grpname=each+"_Ctrl", each+"_grp"
                transformWorldMatrix, rotateWorldMatrix=self.selection_location_type(each)           
                self.cubeI(name, grpname, size, transformWorldMatrix, rotateWorldMatrix, colour)    
        else:
            name, grpname="name_Ctrl", "name_grp"
            transformWorldMatrix=(0, 0, 0) 
            rotateWorldMatrix=(0, 0, 0)        
            self.cubeI(name, grpname, size, transformWorldMatrix, rotateWorldMatrix, colour)    
                     
    def getjack(self, selectionCheck, colour, size):                                                
        # size=self.fetchSize()
        if selectionCheck:
            for each in selectionCheck:
                name, grpname=each+"_Ctrl", each+"_grp"
                transformWorldMatrix, rotateWorldMatrix=self.selection_location_type(each)           
                self.JackI(name, grpname, size, transformWorldMatrix, rotateWorldMatrix, colour)
        else:
            name, grpname="name_Ctrl", "name_grp"
            transformWorldMatrix=(0, 0, 0) 
            rotateWorldMatrix=(0, 0, 0)              
            self.JackI(name, grpname, size, transformWorldMatrix, rotateWorldMatrix, colour)   
    def getJoint(self, selectionCheck, size):
        if selectionCheck:
            for each in selectionCheck:
                transformWorldMatrix, rotateWorldMatrix=self.selection_location_type(each)           
                self.buildJoint(each, transformWorldMatrix, rotateWorldMatrix)
        else:
            name, grpname="name", "name_grp"
            transformWorldMatrix=(0, 0, 0) 
            rotateWorldMatrix=(0, 0, 0)
            self.buildJoint(name, transformWorldMatrix, rotateWorldMatrix)

    def getLoc(self, selectionCheck, colour, size):
        if selectionCheck:
            for each in selectionCheck:
                name, grpname=each+"_loc", each+"_grp"
                transformWorldMatrix, rotateWorldMatrix=self.selection_location_type(each)           
                self.buildLoc(name, grpname, transformWorldMatrix, rotateWorldMatrix, colour)
        else:
            name, grpname="name_loc", "name_grp"
            transformWorldMatrix=(0, 0, 0) 
            rotateWorldMatrix=(0, 0, 0)   
            self.buildLoc(name, grpname, transformWorldMatrix, rotateWorldMatrix, colour)
                          
    def getballarrow(self, selectionCheck, colour, size):   
        if selectionCheck:
            for each in selectionCheck:
                name, grpname=each+"_Ctrl", each+"_grp"
                transformWorldMatrix, rotateWorldMatrix=self.selection_location_type(each)                                                        
                self.ballArrowI(name, grpname, transformWorldMatrix, rotateWorldMatrix, colour)
        else:
            name, grpname="name_Ctrl", "name_grp"
            transformWorldMatrix=(0, 0, 0) 
            rotateWorldMatrix=(0, 0, 0)                 
            self.ballArrowI(name, grpname, transformWorldMatrix, rotateWorldMatrix, colour)

    def getCubeCala(self, selectionCheck, colour, size):   
        if selectionCheck:
            for each in selectionCheck:
                name, grpname=each+"_Ctrl", each+"_grp"
                transformWorldMatrix, rotateWorldMatrix=self.selection_location_type(each)                                                        
                self.cubeCala(name, grpname, transformWorldMatrix, rotateWorldMatrix, size)
        else:
            name, grpname="name_Ctrl", "name_grp"
            transformWorldMatrix=(0, 0, 0) 
            rotateWorldMatrix=(0, 0, 0)                 
            self.cubeCala(name, grpname, transformWorldMatrix, rotateWorldMatrix, size)
            
    def gethandle(self, selectionCheck, colour, size):
        if selectionCheck:
            for each in selectionCheck:
                name, grpname=each+"_Ctrl", each+"_grp"
                transformWorldMatrix, rotateWorldMatrix=self.selection_location_type(each)           
                self.handleI(name, grpname, transformWorldMatrix, rotateWorldMatrix, colour)
        else:
            name, grpname="name_Ctrl", "name_grp"
            transformWorldMatrix=(0, 0, 0) 
            rotateWorldMatrix=(0, 0, 0)                 
            self.handleI(name, grpname, transformWorldMatrix, rotateWorldMatrix, colour)
                               
    def fetchDirection(self):
        titleText=('Define Axis of Controller'),                        
        messageText=("Enter direction"), 
        textText=("X, Y, Z"), 
        direction=self.makeDialog(titleText, messageText, textText)
        if direction=="X":
            nrx=1
            nry=0
            nrz=0                  
        elif direction=="Y":
            nrx=0
            nry=1
            nrz=0   
        elif direction=="Z":
            nrx=0
            nry=0
            nrz=1 
        return nrx, nry, nrz   
    def fetchColour(self):
        titleText=('Define Colour of Controller'),                        
        messageText=("Enter colour"), 
        textText=("red, green, blue, yellow"), 
        colour=self.makeDialog(titleText, messageText, textText)
        if colour=="red":
            colour=13          
        elif colour=="blue":
            colour=6   
        elif colour=="green":
            colour=14
        elif colour=="yellow":
            colour=22  
        return colour       
    
    def fetchSize(self, arg=None):
        titleText=('Define size of Controller'),                        
        messageText=("Enter size"), 
        textText=("6"), 
        size=self.makeDialog(titleText, messageText, textText)
        return float(size)  

    def fetchName(self, arg=None):
        titleText=('Define name'),                        
        messageText=("Enter name"), 
        textText=("name"), 
        name=self.makeDialog(titleText, messageText, textText)
        return name
    
    def mirrorController(self):
        selObj=cmds.ls(sl=1)
        for eachController, eachChild in map(None, selObj[::2], selObj[1::2]):
            translate, rotated=self.locationXForm(eachController)
            cmds.move(-translate[0], translate[1], translate[2], eachChild)
            cmds.rotate(-rotated[0], -rotated[1], rotated[2], eachChild)

    def massTransfer(self):
#        selObj=self.selection_grab()
        selObj=cmds.ls(sl=1)
        if len(selObj)<2:
            print "select more than one object"
        else:
            pass
        for eachController, eachChild in map(None, selObj[::2], selObj[1::2]):
            getControllerListAttr=listAttr (eachController, w=1, a=1, s=1, u=1)
            getChildListAttr=listAttr (eachChild, w=1, a=1, s=1, u=1)
            for eachControllerAttr, eachChildAttr in map(None, getControllerListAttr, getChildListAttr):
                if eachControllerAttr == eachChildAttr:
                    try:
                        getChildObj=ls(eachChild)[0]
                        getChildAttrToChange=getattr(getChildObj, eachChildAttr)
                        getParentObj=ls(eachController)[0]
                        getChangeAttr=getattr(getParentObj,eachControllerAttr).get()
                        print "setting"+ eachChild, eachChildAttr, getChangeAttr                    
                        getChildAttrToChange.set(getChangeAttr)
                    except:
                        print eachChild, eachChildAttr+" skipped (locked or otherwise)"
                        pass

    def mirrorSelection(self):
        selObj=cmds.ls(sl=1)
        getSelected=[]
        for each in selObj:
            if "_R_" in each:
                lognm=each.replace("_R_", "_L_")
                getSelected.append(lognm)
            elif "_L_" in each:
                lognm=each.replace("_L_", "_R_")
                getSelected.append(lognm)
            else:
                getSelected.append(each)
        cmds.select(getSelected[0])
        for each in getSelected[1:]:
            cmds.select(each, add=1)
            
    def combineSelect(self):
        selObj=cmds.ls(sl=1)
        getSelected=[]
        for each in selObj:
            if "_R_" in each:
                lognm=each.replace("_R_", "_L_")
                getSelected.append(lognm)
            elif "_L_" in each:
                lognm=each.replace("_L_", "_R_")
                getSelected.append(lognm)
            else:
                getSelected.append(each)
        cmds.select(selObj[0])
        for each, item in map(None, selObj[1:], getSelected):
            cmds.select(item, add=1)
            cmds.select(each, add=1)
             

    def matchXform(self, arg=None):
        '''This matches a matrix value to a group selection'''
        selObj=cmds.ls(sl=1)
        for eachController, eachChild in map(None, selObj[::2], selObj[1::2]):
            getValue=cmds.xform(eachController, q=True, m=True)
            cmds.xform(eachChild, m=getValue)
            
#         selObj=cmds.ls(sl=1)
#         Controller=selObj[0]
#         Child=selObj[1]
#         getValue=cmds.xform(Controller, q=True, m=True)
#         cmds.xform(Child, m=getValue) 
    def mirrorXformV1(self, arg=None):
        '''this mirrors a group selection on a face'''
        selObj=cmds.ls(sl=1)
        for eachController, eachChild in map(None, selObj[::2], selObj[1::2]):
            translate, rot=self.locationXForm(eachController)
            #translate, rot=self.forcedlocationXForm(eachController)
            cmds.move(-translate[0], translate[1], translate[2], eachChild)
            cmds.rotate(rot[0], -rot[1], -rot[2], eachChild)
    def mirrorXform(self, arg=None):
        ''''''
        selObj=cmds.ls(sl=1)
        for eachController, eachChild in map(None, selObj[::2], selObj[1::2]):
            translate, rot=self.forcedlocationXForm(eachController)
            translate=cmds.xform(eachController, q=1, t=1)
            cmds.xform(eachChild, t=[-translate[0], translate[1], translate[2]])
            if "Wrist" in eachChild or "hand" in eachChild:
                cmds.rotate(rot[0], -rot[1], -rot[2],eachChild)
            else:
                cmds.rotate(-rot[0], -rot[1], -rot[2],eachChild)
    def mirrorXformProper(self, arg=None):
        ''''''
        selObj=cmds.ls(sl=1)
        for eachController, eachChild in map(None, selObj[::2], selObj[1::2]):
            translate, rot=self.forcedlocationXForm(eachController)
            translate=cmds.xform(eachController, q=1, t=1)
            cmds.xform(eachChild, t=[-translate[0], translate[1], translate[2]])
            cmds.rotate(-rot[0], -rot[1], -rot[2],eachChild)
    def mirrorXformface(self, arg=None):
        ''''''
        selObj=cmds.ls(sl=1)
        for eachController, eachChild in map(None, selObj[::2], selObj[1::2]):
            translate, rot=self.forcedlocationXForm(eachController)
            translate=cmds.xform(eachController, q=1, t=1)
            cmds.xform(eachChild, t=[-translate[0], translate[1], translate[2]])
            if "Wrist" in eachChild or "hand" in eachChild:
                cmds.rotate(rot[0], -rot[1], -rot[2],eachChild)
            else:
                cmds.rotate(-rot[0], rot[1], -rot[2],eachChild)
    def mirrorXformRig(self, arg=None):
        ''''''
        selObj=cmds.ls(sl=1)
        for eachController, eachChild in map(None, selObj[::2], selObj[1::2]):
            translate, rot=self.forcedlocationXForm(eachController)
            translate=cmds.xform(eachController, q=1, t=1)
            cmds.xform(eachChild, t=[-translate[0], translate[1], translate[2]])
            cmds.rotate(rot[0], -rot[1], -rot[2],eachChild)
    def lockLeftWeights(self, arg=None):
        '''this locks all left bone weights'''
        getRefJoints=cmds.ls("*:*_jnt")
        getJoints=cmds.ls("*_jnt")
        for each in getJoints:
            try:
                cmds.setAttr(each+".liw", 0)
            except:
                pass 
        for each in getRefJoints:
            try:
                cmds.setAttr(each+".liw", 0)
            except:
                pass
        getLeftJoints=cmds.ls("*:*_L_jnt")
        getLeftFaceJoints=cmds.ls("*L_jnt")
        getLeftBodyRefJoints=cmds.ls("*:*Left*_jnt")
        getLeftBodyJoints=cmds.ls("*Left*_jnt")
        for each in getLeftJoints:
            try:
                cmds.setAttr(each+".liw", 1)
            except:
                pass
        for each in getLeftFaceJoints:
            try:
                cmds.setAttr(each+".liw", 1)
            except:
                pass
        for each in getLeftBodyRefJoints:
            try:
                cmds.setAttr(each+".liw", 1)
            except:
                pass            
        for each in getLeftBodyJoints:
            try:
                cmds.setAttr(each+".liw", 1)
            except:
                pass 
            
    def massDef(self, arg=None):    
        getMesh=cmds.ls(sl=1)
        if len(getMesh)<2:
            print "select two groups"
        else:
            pass
        getMeshTarget=getMesh[0]
        getMeshController=getMesh[1]
        getChildrenController=cmds.listRelatives(getMeshController, c=1, typ="transform")
        if getChildrenController==None:
            getChildrenController=([getMeshController])
        getChildrenTarget=cmds.listRelatives(getMeshTarget, c=1, typ="transform")
        if getChildrenTarget==None:
            getChildrenTarget=([getMeshTarget]) 
        for eachController, eachChild in map(None, getChildrenController, getChildrenTarget):
            if eachController ==eachChild :
                try:    
                    cmds.select(eachChild)
                    cmds.select(eachController, add=1)
                    cmds.deformer(type="wrap")
                except:
                    pass

    def massMove(self):
        getSel=cmds.ls(sl=1)
        getFirst=getSel[:-1]
        getSecond=getSel[-1]  
        for each in getFirst:
            cmds.select(getSecond)
            cmds.select(each, add=1)
            cmds.parentConstraint(getSecond, each, mo=0, n="deleteme")
            cmds.delete("deleteme")        

                                 
    def lockRightWeights(self, arg=None):
        '''this locks all Right bone weights'''
        getRefJoints=cmds.ls("*:*_jnt")
        getJoints=cmds.ls("*_jnt")
        for each in getJoints:
            try:
                cmds.setAttr(each+".liw", 0)
            except:
                pass 
        for each in getRefJoints:
            try:
                cmds.setAttr(each+".liw", 0)
            except:
                pass
        getRightJoints=cmds.ls("*:*_R_jnt")
        getRightFaceJoints=cmds.ls("*L_jnt")
        getRightBodyRefJoints=cmds.ls("*:*Right*_jnt")
        getRightBodyJoints=cmds.ls("*Right*_jnt")
        for each in getRightJoints:
            try:
                cmds.setAttr(each+".liw", 1)
            except:
                pass
        for each in getRightFaceJoints:
            try:
                cmds.setAttr(each+".liw", 1)
            except:
                pass
        for each in getRightBodyRefJoints:
            try:
                cmds.setAttr(each+".liw", 1)
            except:
                pass            
        for each in getRightBodyJoints:
            try:
                cmds.setAttr(each+".liw", 1)
            except:
                pass            
    def lockBodyWeights(self, arg=None):
        '''this locks all body joint weights'''
        getLegJoints=cmds.ls("*:leg*_jnt")
        getSpineJoints=cmds.ls("*:spine*_jnt")
        getArmJoints=cmds.ls("*:arm*_jnt")
        getFootJoints=cmds.ls("*:foot*_jnt")
        for each in getLegJoints:
            try:
                cmds.setAttr(each+".liw", 1)
            except:
                pass
        for each in getSpineJoints:
            try:
                cmds.setAttr(each+".liw", 1)
            except:
                pass
        for each in getArmJoints:
            try:
                cmds.setAttr(each+".liw", 1)
            except:
                pass            
        for each in getFootJoints:
            try:
                cmds.setAttr(each+".liw", 1)
            except:
                pass            
    def lockFaceWeights(self, arg=None):
        '''this locks all body joint weights'''
        getFaceJoints=cmds.ls("face*_jnt")
        for each in getFaceJoints:
            try:
                cmds.setAttr(each+".liw", 1)
            except:
                pass      
    def lockAllWeights(self, arg=None):
        '''this locks all weights'''
        getRefJoints=cmds.ls("*:*_jnt")
        getJoints=cmds.ls("*_jnt")
        for each in getJoints:
            try:
                cmds.setAttr(each+".liw", 1)
            except:
                pass 
        for each in getRefJoints:
            try:
                cmds.setAttr(each+".liw", 1)
            except:
                pass                           
    def unLockWeights(self, arg=None):
        '''this unlocks all weights'''
        getRefJoints=cmds.ls("*:*_jnt")
        getJoints=cmds.ls("*_jnt")    
        for each in getJoints:
            try:
                cmds.setAttr(each+".liw", 0)
            except:
                pass            
        for each in getRefJoints:
            try:
                cmds.setAttr(each+".liw", 0)
            except:
                pass   
                    
    def massCopyWeight(self, arg=None):
        getMesh=cmds.ls(sl=1)
        if len(getMesh)<2:
            print "select a skinned mesh group and target skinned mesh"
        else:
            pass
        getMeshController=getMesh[0]
        getMeshTarget=getMesh[1]
        getChildrenController=cmds.listRelatives(getMeshController, c=1, typ="transform")
        if getChildrenController==None:
            getChildrenController=([getMeshController])
        getChildrenTarget=cmds.listRelatives(getMeshTarget, c=1, typ="transform")
        if getChildrenTarget==None:
            getChildrenTarget=([getMeshTarget])
        for each, item in map(None, getChildrenController, getChildrenTarget):
            if each!=None:
                getCtrlItemName=each.split(":")
                getTgtItemName=item.split(":")
                getOldMeshNameSpace=':'.join(getCtrlItemName[:-1])+":"
                newAssetsNamespace=':'.join(getTgtItemName[:-1])+":"
                if getCtrlItemName[-1:][0] ==getTgtItemName[-1:][0]:
                    cmds.select(each)
                    cmds.select(item, add=1)
                    cmds.copySkinWeights(noMirror=1, surfaceAssociation="closestPoint", influenceAssociation="closestJoint")
                    
    def massCopyWeightSingleToMass(self, arg=None):
        getMesh=cmds.ls(sl=1)
        if len(getMesh)<2:
            print "select a skinned mesh group and target skinned mesh"
        else:
            pass
        getMeshController=getMesh[0]
        for each in getMesh[1:]:
            cmds.select(getMeshController)
            cmds.select(each, add=1)
            cmds.copySkinWeights(noMirror=1, surfaceAssociation="closestPoint", influenceAssociation="closestJoint")
                    
            
            
#             translate, rot=self.forcedlocationXForm(eachController)
# #             transformWorldMatrix = cmds.xform(eachController, q=True, wd=1, m=True)
# #             cmds.xform(eachChild, m=transformWorldMatrix)
# #             cmds.rotate(rot[0], -rot[1], -rot[2],eachChild)
#             translate=cmds.xform(eachController, q=1, t=1)
#             transformWorldMatrix = cmds.xform(eachController, q=True, wd=1, m=True)
#             cmds.move(-translate[0], 0, 0,eachChild, r=1, rpr=1)
#             cmds.rotate(rot[0], -rot[1], -rot[2],eachChild)            
            
    def mirrorSDKMouth(self, arg=None):
        dominateSide="R"
        subordinateSide="L"  
        selObj=(
        "Lip_T_"+dominateSide+"_SDK",
        "Lip_T_"+subordinateSide+"_SDK",
        "Lip_Corner_"+dominateSide+"_SDK",
        "Lip_Corner_"+subordinateSide+"_SDK",
        "Lip_B_"+dominateSide+"_SDK",
        "Lip_B_"+subordinateSide+"_SDK",)
        for eachController, eachChild in map(None, selObj[::2], selObj[1::2]):
            translate, rot=self.forcedlocationXForm(eachController)
            translate=cmds.xform(eachController, q=1, t=1)
            cmds.xform(eachChild, t=[-translate[0], translate[1], translate[2]])
            cmds.rotate(rot[0], -rot[1], -rot[2],eachChild)
            
    def mirrorMouth(self, arg=None):
        '''this mirrors the mouth controls'''
        getSelChar=cmds.ls(sl=1)
        getName=getSelChar[0].split(":")
        getCharNameCtrlPref=':'.join(getName[:-1])+":"
        titleText=('Define dominatingside'),                        
        messageText=("Enter Side"), 
        textText=("R, L"), 
        side=self.makeDialog(titleText, messageText, textText)  
        if side =="R":
            dominateSide="R"
            subordinateSide="L"  
        else:
            dominateSide="L"
            subordinateSide="R"  
        selObj=(
        getCharNameCtrlPref+"Lip_T_"+dominateSide+"_Ctrl",
        getCharNameCtrlPref+"Lip_T_"+subordinateSide+"_Ctrl",
        getCharNameCtrlPref+"Lip_Corner_"+dominateSide+"_Ctrl",
        getCharNameCtrlPref+"Lip_Corner_"+subordinateSide+"_Ctrl",
        getCharNameCtrlPref+"Lip_B_"+dominateSide+"_Ctrl",
        getCharNameCtrlPref+"Lip_B_"+subordinateSide+"_Ctrl",)
        for eachController, eachChild in map(None, selObj[::2], selObj[1::2]):
#             translate, rot=self.forcedlocationXForm(eachController)
#             transformWorldMatrix = cmds.xform(eachController, q=True, wd=1, m=True)
#             cmds.xform(eachChild, m=transformWorldMatrix)
#             cmds.move(-translate[0], translate[1], translate[2], eachChild)
#             cmds.rotate(rot[0], -rot[1], -rot[2],eachChild)
            translate, rot=self.forcedlocationXForm(eachController)
            translate=cmds.xform(eachController, q=1, t=1)
            cmds.xform(eachChild, t=[-translate[0], translate[1], translate[2]])
            cmds.rotate(rot[0], -rot[1], -rot[2],eachChild)
            


    def mirrorBrows(self, arg=None):
        '''This mirrors the eyebrows for SDK creation'''  
        selObj=("Lip_T_R_SDK",
        "Brow05_R_SDK",
        "Brow05_L_SDK",
        "Brow04_R_SDK",
        "Brow04_L_SDK",
        "Brow03_R_SDK",
        "Brow03_L_SDK",
        "Brow02_R_SDK",
        "Brow02_L_SDK",
        "Brow01_R_SDK",
        "Brow01_L_SDK",)
        #selObj=cmds.ls(sl=1)
        for eachController, eachChild in map(None, selObj[::2], selObj[1::2]):
            translate, rot=self.forcedlocationXForm(eachController)
            translate=cmds.xform(eachController, q=1, t=1)
            cmds.xform(eachChild, t=[-translate[0], translate[1], translate[2]])
            cmds.rotate(rot[0], -rot[1], -rot[2],eachChild)
               
#             translate, rot=self.forcedlocationXForm(eachController)
#             translate=cmds.xform(eachController, q=1, t=1)
#             transformWorldMatrix = cmds.xform(eachController, q=True, wd=1, m=True)
#             cmds.move(-translate[0], 0, 0,eachChild, r=1, rpr=1)
#             cmds.rotate(rot[0], -rot[1], -rot[2],eachChild)            
    def mirrorAnimBrows(self, arg=None):
        '''This mirrors the eyebrows'''
        try:
            getSel=cmds.ls(sl=1)[0]
            pass
        except:
            print "select something"
        getParent=getSel.split(":")
        getAsset= ':'.join(getParent[:-1])+":"
        titleText=('Define dominatingside'),                        
        messageText=("Enter Side"), 
        textText=("R, L"), 
        side=self.makeDialog(titleText, messageText, textText)  
        if side =="R":
            dominateSide="R"
            subordinateSide="L"  
        else:
            dominateSide="L"
            subordinateSide="R"    
        selObj=(
        getAsset+"Brow05_"+dominateSide+"_Ctrl",
        getAsset+"Brow05_"+subordinateSide+"_Ctrl",
        getAsset+"Brow04_"+dominateSide+"_Ctrl",
        getAsset+"Brow04_"+subordinateSide+"_Ctrl",
        getAsset+"Brow03_"+dominateSide+"_Ctrl",
        getAsset+"Brow03_"+subordinateSide+"_Ctrl",
        getAsset+"Brow02_"+dominateSide+"_Ctrl",
        getAsset+"Brow02_"+subordinateSide+"_Ctrl",
        getAsset+"Brow01_"+dominateSide+"_Ctrl",
        getAsset+"Brow01_"+subordinateSide+"_Ctrl",)
        #selObj=cmds.ls(sl=1)
        for eachController, eachChild in map(None, selObj[::2], selObj[1::2]):
            translate, rot=self.forcedlocationXForm(eachController)
            translate=cmds.xform(eachController, q=1, t=1)
            cmds.xform(eachChild, t=[-translate[0], translate[1], translate[2]])
            cmds.rotate(rot[0], -rot[1], -rot[2],eachChild)
               
    def mirrorAnimEyes(self, arg=None):
        '''This mirrors the eyebrows'''
        try:
            getSel=cmds.ls(sl=1)[0]
            pass
        except:
            print "select something"
        getParent=getSel.split(":")
        getAsset= ':'.join(getParent[:-1])+":"
        titleText=('Define dominatingside'),                        
        messageText=("Enter Side"), 
        textText=("R, L"), 
        side=self.makeDialog(titleText, messageText, textText)  
        if side =="R":
            dominateSide="R"
            subordinateSide="L"  
        else:
            dominateSide="L"
            subordinateSide="R"     
        selObj=(
                getAsset+"Lid_Open03_T_"+dominateSide+"_Ctrl",
                getAsset+"Lid_Open03_T_"+subordinateSide+"_Ctrl",
                getAsset+"Lid_Open04_T_"+dominateSide+"_Ctrl",
                getAsset+"Lid_Open04_T_"+subordinateSide+"_Ctrl",
                getAsset+"Lid_Open05_B_"+dominateSide+"_Ctrl",
                getAsset+"Lid_Open05_B_"+subordinateSide+"_Ctrl",
                getAsset+"Lid_Open04_B_"+dominateSide+"_Ctrl",
                getAsset+"Lid_Open04_B_"+subordinateSide+"_Ctrl",
                getAsset+"Lid_Open03_B_"+dominateSide+"_Ctrl",
                getAsset+"Lid_Open03_B_"+subordinateSide+"_Ctrl",
                getAsset+"Lid_Open02_B_"+dominateSide+"_Ctrl",
                getAsset+"Lid_Open02_B_"+subordinateSide+"_Ctrl",
                getAsset+"Lid_Open02_T_"+dominateSide+"_Ctrl",                
                getAsset+"Lid_Open02_T_"+subordinateSide+"_Ctrl",                
                )
        for eachController, eachChild in map(None, selObj[::2], selObj[1::2]):
            translate, rot=self.forcedlocationXForm(eachController)
            translate=cmds.xform(eachController, q=1, t=1)
            cmds.xform(eachChild, t=[-translate[0], translate[1], translate[2]])
            cmds.rotate(rot[0], -rot[1], -rot[2],eachChild)
       
    def mirrorAnimFace(self, arg=None):
        '''This mirrors the eyebrows'''
        try:
            getSel=cmds.ls(sl=1)[0]
            pass
        except:
            print "select something"
        getParent=getSel.split(":")
        getAsset= ':'.join(getParent[:-1])+":"
        titleText=('Define dominatingside'),                        
        messageText=("Enter Side"), 
        textText=("R, L"), 
        side=self.makeDialog(titleText, messageText, textText)  
        if side =="R":
            dominateSide="R"
            subordinateSide="L"  
        else:
            dominateSide="L"
            subordinateSide="R"      
        selObj=(
                getAsset+"Lid_Open03_T_"+dominateSide+"_Ctrl",
                getAsset+"Lid_Open03_T_"+subordinateSide+"_Ctrl",
                getAsset+"Lid_Open04_T_"+dominateSide+"_Ctrl",
                getAsset+"Lid_Open04_T_"+subordinateSide+"_Ctrl",
                getAsset+"Lid_Open05_B_"+dominateSide+"_Ctrl",
                getAsset+"Lid_Open05_B_"+subordinateSide+"_Ctrl",
                getAsset+"Lid_Open04_B_"+dominateSide+"_Ctrl",
                getAsset+"Lid_Open04_B_"+subordinateSide+"_Ctrl",
                getAsset+"Lid_Open03_B_"+dominateSide+"_Ctrl",
                getAsset+"Lid_Open03_B_"+subordinateSide+"_Ctrl",
                getAsset+"Lid_Open02_B_"+dominateSide+"_Ctrl",
                getAsset+"Lid_Open02_B_"+subordinateSide+"_Ctrl",
                getAsset+"Lid_Open02_T_"+dominateSide+"_Ctrl",
                getAsset+"Lid_Open02_T_"+subordinateSide+"_Ctrl",
                getAsset+"Brow01_"+dominateSide+"_Ctrl",
                getAsset+"Brow01_"+subordinateSide+"_Ctrl",
                getAsset+"Brow02_"+dominateSide+"_Ctrl",
                getAsset+"Brow02_"+subordinateSide+"_Ctrl",
                getAsset+"Brow03_"+dominateSide+"_Ctrl",
                getAsset+"Brow03_"+subordinateSide+"_Ctrl",
                getAsset+"Brow04_"+dominateSide+"_Ctrl",
                getAsset+"Brow04_"+subordinateSide+"_Ctrl",
                getAsset+"Brow05_"+dominateSide+"_Ctrl",
                getAsset+"Brow05_"+subordinateSide+"_Ctrl",
                getAsset+"CheekBone_"+dominateSide+"_Ctrl",
                getAsset+"CheekBone_"+subordinateSide+"_Ctrl",
                getAsset+"Cheek_T_"+dominateSide+"_Ctrl",
                getAsset+"Cheek_T_"+subordinateSide+"_Ctrl",
                getAsset+"Cheek_"+dominateSide+"_Ctrl",
                getAsset+"Cheek_"+subordinateSide+"_Ctrl",
                getAsset+"Nose_"+dominateSide+"_Ctrl",
                getAsset+"Nose_"+subordinateSide+"_Ctrl",
                getAsset+"Jaw_"+dominateSide+"_Ctrl",
                getAsset+"Jaw_"+subordinateSide+"_Ctrl",
                getAsset+"Lip_Corner_"+dominateSide+"_Ctrl",
                getAsset+"Lip_Corner_"+subordinateSide+"_Ctrl",
                getAsset+"Lip_T_"+dominateSide+"_Ctrl",
                getAsset+"Lip_T_"+subordinateSide+"_Ctrl",
                getAsset+"Lip_B_"+dominateSide+"_Ctrl",              
                getAsset+"Lip_B_"+subordinateSide+"_Ctrl",              
                )
        for eachController, eachChild in map(None, selObj[::2], selObj[1::2]):
            translate, rot=self.forcedlocationXForm(eachController)
            translate=cmds.xform(eachController, q=1, t=1)
            cmds.xform(eachChild, t=[-translate[0], translate[1], translate[2]])
            cmds.rotate(rot[0], -rot[1], -rot[2],eachChild)
       

    def setBoxX(self, arg=None):
        '''this sets an SDK key on a group of controls if a parent controller box moves in the X axis'''        
        selObj=cmds.ls(sl=1)
        Controller=selObj[0]
        ChildAttributes=(".tx", ".ty", ".tz" , ".rx", ".ry", ".rz")
        ControllerAttributesHz=".tx"
        ControllerAttributesVrt=".ty"
        for Child in selObj[1:]:
            for attribute in ChildAttributes:
                cmds.setDrivenKeyframe(Child+attribute, cd=Controller+ControllerAttributesHz)

    def setBoxY(self, arg=None):
        '''this sets an SDK key on a group of controls if a parent controller box moves in the Y axis'''
        selObj=cmds.ls(sl=1)
        Controller=selObj[0]
        ChildAttributes=(".tx", ".ty", ".tz" , ".rx", ".ry", ".rz")
        ControllerAttributesHz=".tx"
        ControllerAttributesVrt=".ty"
        for Child in selObj[1:]:
            for attribute in ChildAttributes:
                cmds.setDrivenKeyframe(Child+attribute, cd=Controller+ControllerAttributesVrt)
    def buildContainerBulkSelected(self, arg=None):
        getSel=cmds.ls(sl=1)
        makeContainer=cmds.container(n=getSel[0]+"_CTR")
        for each in getSel:
            cmds.container(makeContainer, e=1, an=each)
    def buildContainerMassSelected(self, arg=None):
        getSel=cmds.ls(sl=1)
        for each in getSel:
            makeContainer=cmds.container(n=each+"_CTR")

    def sandwichControl(self):
        '''this sandwitches a circle control to another control for an easy override switch(face controllers for SDK keys)'''
        titleText=('Define type of Controller'),                        
        messageText=("Enter type"), 
        textText=("SDK"), 
        typeCtrl=self.makeDialog(titleText, messageText, textText)   
        colour=self.fetchColour()
        size=self.fetchSize()     
        selObj=cmds.ls(sl=1)
        for each in selObj:
            self.sandwichControlFunct(colour, size, each, typeCtrl)
        
    def sandwichControlFunct(self, colour, size, each, typeCtrl):
        selObjParent=cmds.listRelatives( each, allParents=True )
        transformWorldMatrix, rotateWorldMatrix=self.locationXForm(each)        
        nrx, nry, nrz = 0.0, 0.0, 1.0 
        getcolour=cmds.getAttr(each+".overrideColor")
        name=each.split("_Ctrl")[0]+typeCtrl+"_Ctrl"
        grpname=each.split("_Ctrl")[0]+typeCtrl+"_grp"
        self.buildCtrl(each, name, grpname, transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)   
        cmds.setAttr(name+"Shape.visibility", 1)
        if selObjParent:
            cmds.parent(each.split("_Ctrl")[0]+typeCtrl+"_grp", selObjParent[0] )
        cmds.parent(each, each.split("_Ctrl")[0]+typeCtrl+"_Ctrl")

    def sandwichAuto(self, each, typeCtrl, colour, size ):
        selObjParent=cmds.listRelatives( each, allParents=True )
        transformWorldMatrix, rotateWorldMatrix=self.locationXForm(each)        
        nrx, nry, nrz = 0.0, 0.0, 1.0 
        getcolour=cmds.getAttr(each+".overrideColor")
        name=each.split("_Ctrl")[0]+typeCtrl+"_Ctrl"
        grpname=each.split("_Ctrl")[0]+typeCtrl+"_grp"
        self.buildCtrl(each, name, grpname, transformWorldMatrix, rotateWorldMatrix, size, colour, nrx, nry, nrz)   
        if selObjParent:
            cmds.parent(each.split("_Ctrl")[0]+typeCtrl+"_grp", selObjParent[0] )
        cmds.parent(each, each.split("_Ctrl")[0]+typeCtrl+"_Ctrl")




    def blendGroupToGroup(self):
        selObj=cmds.ls(sl=1, fl=1)
        parentObj=selObj[0]
        childrenObj=selObj[1]
        getparentObj=cmds.listRelatives(parentObj, c=1)
        getchildObj=cmds.listRelatives(childrenObj, c=1)
        for parentItem, childItem in map(None, getparentObj,getchildObj):
            parentItemls=cmds.ls(parentItem)
            childItemls=cmds.ls(childItem)
            cmds.select(parentItemls)
            cmds.select(childItemls, add=1)
            defName=str(parentItem)+"_BShape"
            print defName
            cmds.blendShape(n=defName, w=(0, 1.0)) 

    def blendMass(self):
        selObj=cmds.ls(sl=1, fl=1)
        for eachController, eachChild in map(None, selObj[::2], selObj[1::2]):
            parentItem=cmds.ls(eachController)
            childItem=cmds.ls(eachChild)
            cmds.select(parentItem)
            cmds.select(childItem, add=1)
            cmds.blendShape(n=str(parentItem[0])+"_BShape", w=(0, 1.0)) 

    def blendSearch(self):
        selObj=cmds.ls(sl=1, fl=1)
        parentObj=selObj[0]
        childrenObj=selObj[1]
        getparentObj=cmds.listRelatives(parentObj, c=1)
        getchildObj=cmds.listRelatives(childrenObj, c=1)
        for parentItem in getparentObj:
            for childItem in getchildObj:
                if parentItem in childItem:
                    parentItemls=cmds.ls(parentItem)
                    childItemls=cmds.ls(childItem)
                    cmds.select(parentItemls)
                    cmds.select(childItemls, add=1)
                    defName=str(parentItem)+"_BShape"
                    cmds.blendShape(n=defName, w=(0, 1.0)) 

    def mirrorBlendshape(self):
        selObj=cmds.ls(sl=1)
        if len(selObj)<2:
            print "Must select a deformed shape and the neutral shape to apply the reverse mirror to."
            return
        else:
            pass
        cmds.duplicate(selObj[1],n="shape_Scale")
        cmds.setAttr("shape_Scale.scaleX", -1)
        cmds.duplicate(selObj[1], n="shape_Wrap")
        cmds.select(selObj[0])
        cmds.select("shape_Scale", add=1)
        cmds.blendShape(n="reflectBlend")
        cmds.select("shape_Wrap")
        cmds.select("shape_Scale", add=1)
        cmds.CreateWrap()
        cmds.setAttr( "reflectBlend."+selObj[0], 1)        
        cmds.duplicate("shape_Wrap", n="reflectedBlend")
        remove=("shape_Wrap", "shape_Scale")
        for each in remove:
            cmds.delete(each)
    def mirrorBlendshapeFace(self):
        selObj=cmds.ls(sl=1)
        if len(selObj)<2:
            print "must select a deformed shape and the mesh to apply the reverse mirror to"
        else:
            pass
        cmds.duplicate(selObj[1],n="shape_Scale")
        cmds.setAttr("shape_Scale.scaleX", -1)
        cmds.duplicate(selObj[1], n="shape_Wrap")
        cmds.select(selObj[0])
        cmds.select("shape_Scale", add=1)
        if "_R_" in selObj[0]:
            lognm=selObj[0].replace("_R_", '_L_')
            cmds.blendShape(n=lognm)
        else:
            cmds.blendShape(n="reflectBlend")
        cmds.select("shape_Wrap")
        cmds.select("shape_Scale", add=1)
        cmds.CreateWrap()
        cmds.setAttr( "reflectBlend."+selObj[0], 1)        
        cmds.duplicate("shape_Wrap", n="reflectedBlend")
        remove=("shape_Wrap", "shape_Scale")
        for each in remove:
            cmds.delete(each)
            
    def selectNthCV(self):
        getit=ls(sl=1, fl=1)
        for each in getit:
            for item in each.cv:
                print item.getPosition()   
                
    def mirrorObject(self, arg=None):
        titleText=('Define Sides'),                        
        messageText=("Enter Enter sides or leave blank, will add 'opp' to new object"), 
        textText=("Right, _R_","_R"), 
        Side=self.makeDialog(titleText, messageText, textText)
        if Side=="Right":
            otherSide="Left"
        elif Side=="_R_":
            otherSide="_L_"
        elif Side=="_R":
            otherSide="_L"
        elif Side=="R_":
            otherSide="L_"
        elif Side=="Left":
            otherSide="Right"
        elif Side=="_L_":
            otherSide="_R_"
        elif Side=="_L":
            otherSide="_R"
        elif Side=="L_":
            otherSide="R_"
        getObj=cmds.ls(sl=1)
        if Side:
            for each in getObj:
                NewString=each.replace(Side, otherSide)
                cmds.duplicate(each, n=NewString, rr=1)
                cmds.CreateEmptyGroup()
                grp=cmds.ls(sl=1)[0]
                cmds.parent(NewString, grp)
                cmds.setAttr(grp+".scaleX", -1)
                cmds.parent(NewString, w=1) 
                cmds.delete(grp)
        else:
            for each in getObj:
                NewString=each+"_oppSide"
                cmds.duplicate(each, n=NewString, rr=1)
                cmds.CreateEmptyGroup()
                grp=cmds.ls(sl=1)[0]
                cmds.parent(NewString, grp)
                cmds.setAttr(grp+".scaleX", -1)
                cmds.parent(NewString, w=1) 
                cmds.delete(grp)
            
    def mirrorObject_callup(self, getObj, Side, otherSide):
            NewString=getObj.replace(Side, otherSide)
            cmds.duplicate(getObj, n=NewString, rr=1)
            cmds.CreateEmptyGroup()
            grp=cmds.ls(sl=1)[0]
            cmds.parent(NewString, grp)
            cmds.setAttr(grp+".scaleX", -1)
            cmds.parent(NewString, w=1) 
            cmds.delete(grp)
            
    def ikToFK_Arm(self, arg=None):
        try:
            getSel=cmds.ls(sl=1)[0]
            pass
        except:
            print "select something"
        getParent=getSel.split(":")
        getAsset= ':'.join(getParent[:-1])+":"
        if "_R_" in getSel:
            IkWrist=getAsset+"Armhand_IK_R_Ctrl"
            FKWrist=getAsset+"Wrist_R_Ctrl"
            IKPoleElbow=getAsset+"elbow_R_PoleVector_Ctrl"
            FKPoleElbow=getAsset+"armelbowRightFK_target"   
            IKPoleWrist=getAsset+"wrist_R_PoleVector_Ctrl"
            FKPoleWrist=getAsset+"armwristRightFK_target"     
        if "_L_" in getSel:
            IkWrist=getAsset+"Armhand_IK_L_Ctrl"
            FKWrist=getAsset+"Wrist_L_Ctrl"    
            IKPoleElbow=getAsset+"elbow_L_PoleVector_Ctrl"
            FKPoleElbow=getAsset+"armelbowLeftFK_target"      
            IKPoleWrist=getAsset+"wrist_L_PoleVector_Ctrl"
            FKPoleWrist=getAsset+"armwristLeftFK_target" 
        self.xformAutoMove(IkWrist, FKWrist)
        self.xformAutoMove(IKPoleElbow, FKPoleElbow)
        #getClass.xformAutoMove(IKPoleWrist, FKPoleWrist)

    def fkToIK_Arm(self, arg=None):
        try:
            getSel=cmds.ls(sl=1)[0]
            pass
        except:
            print "select something"
        getParent=getSel.split(":")
        getAsset= ':'.join(getParent[:-1])+":"
        if "_R_" in getSel:
            FK_Shoulder=getAsset+"Shoulder_R_Ctrl"
            FK_Elbow=getAsset+"Elbow_R_Ctrl"
            FK_Wrist=getAsset+"Wrist_R_Ctrl"
            IK_Shoulder=getAsset+"armshoulderRightIK_jnt"
            IK_Elbow=getAsset+"armelbowRightIK_jnt"            
            IK_Wrist=getAsset+"armwristRightIK_jnt"
        if "_L_" in getSel:
            FK_Shoulder=getAsset+"Shoulder_L_Ctrl"
            FK_Elbow=getAsset+"Elbow_L_Ctrl"
            FK_Wrist=getAsset+"Wrist_L_Ctrl"
            IK_Shoulder=getAsset+"armshoulderLeftIK_jnt"
            IK_Elbow=getAsset+"armelbowLeftIK_jnt"            
            IK_Wrist=getAsset+"armwristLeftIK_jnt"
        rotateWorldMatrix=cmds.xform(IK_Shoulder, q=1, ro=1)
        cmds.xform(FK_Shoulder, ro=rotateWorldMatrix) 
        rotateWorldMatrix=cmds.xform(IK_Elbow, q=1, ro=1)
        cmds.xform(FK_Elbow, ro=rotateWorldMatrix)         
#         rotateWorldMatrix=cmds.xform(IK_Elbow, q=1, ws=1, rp=1)
#         cmds.xform(FK_Elbow, ro=rotateWorldMatrix)
        rotateWorldMatrix=cmds.xform(IK_Wrist, q=1, ro=1)
        cmds.xform(FK_Wrist, ro=rotateWorldMatrix)

    def ikToFK_Leg(self, arg=None):
        try:
            getSel=cmds.ls(sl=1)[0]
            pass
        except:
            print "select something"
        getParent=getSel.split(":")
        getAsset= ':'.join(getParent[:-1])+":"
        if "_R_" in getSel:
            IkHeel=getAsset+"Footheel_IK_R_Ctrl"
            FKHeel=getAsset+"footheelRight_jnt"
            IKPoleKnee=getAsset+"Knee_PoleVector_Right_Ctrl"
            FKPoleKnee=getAsset+"legkneeRightFK_target"     
        if "_L_" in getSel:
            IkHeel=getAsset+"Footheel_IK_L_Ctrl"
            FKHeel=getAsset+"footheelLeft_jnt"
            IKPoleKnee=getAsset+"Knee_PoleVector_Left_Ctrl"
            FKPoleKnee=getAsset+"legkneeLeftFK_target" 
        self.xformAutoMove(IkHeel, FKHeel)
        self.xformAutoMove(IKPoleKnee, FKPoleKnee)
        
    def fkToIK_Leg(self, arg=None):
        try:
            getSel=cmds.ls(sl=1)[0]
            pass
        except:
            print "select something"
        getParent=getSel.split(":")
        getAsset= ':'.join(getParent[:-1])+":"
        print getAsset
        if "_R_" in getSel:
            IK_Hip=cmds.ls(getAsset+"leghipRightIK_jnt")
            IK_Knee=cmds.ls(getAsset+"legkneeRightIK_jnt")            
            IK_Ankle=cmds.ls(getAsset+"foottalusRightIK_jnt")
            FK_Hip=cmds.ls(getAsset+"Hip_R_Ctrl")
            FK_Knee=cmds.ls(getAsset+"Knee_R_Ctrl")
            FK_Ankle=cmds.ls(getAsset+"Talus_R_Ctrl")
        if "_L_" in getSel:
            IK_Hip=cmds.ls(getAsset+"leghipLeftIK_jnt")
            IK_Knee=cmds.ls(getAsset+"legkneeLeftIK_jnt")            
            IK_Ankle=cmds.ls(getAsset+"foottalusLeftIK_jnt")
            FK_Hip=cmds.ls(getAsset+"Hip_L_Ctrl")
            FK_Knee=cmds.ls(getAsset+"Knee_L_Ctrl")
            FK_Ankle=cmds.ls(getAsset+"Talus_L_Ctrl")
        rotateWorldMatrix=cmds.xform(IK_Hip, q=1, ro=1)
        cmds.xform(FK_Hip, ro=rotateWorldMatrix) 
        rotateWorldMatrix=cmds.xform(IK_Knee, q=1, ro=1)
        cmds.xform(FK_Knee, ro=rotateWorldMatrix)
        rotateWorldMatrix=cmds.xform(IK_Ankle, q=1, ro=1)
        cmds.xform(FK_Ankle, ro=rotateWorldMatrix)

    def buildIK(self):
        getSelObj=cmds.ls(sl=1)
        getController=getSelObj[2]
        getParent=getSelObj[0]
        getChild=getSelObj[1]
        self.fixIK_callup(getController, getParent, getChild)
        
    def fixIK_callup(self, getController, getParent, getChild):
#         getChild=cmds.listRelatives(getParent, ad=1, typ="joint")
        cmds.joint( getParent, e=1, children=1, zso=1, oj='xyz', sao='yup', spa=1)  
        createHandle=cmds.ikHandle(n=getParent+"_ik", sj=getParent, ee=getChild, sol="ikSCsolver")#create IK handle
        cmds.parent(getParent+"_ik", getController)

    def switchArmIKConst(self, arg=None):
        winName = "constraint set"
        global typeMenu
        winTitle = winName
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)

#         self.window = cmds.window(self.winName, title=self.winTitle, tbm=1, w=150, h=100 )
        window = cmds.window(winName, title=winTitle, tbm=1, w=200, h=100 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=200)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        
        cmds.rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(120, 20))
        typeMenu=cmds.optionMenu( label='constriant')
        cmds.menuItem( label="on" )
        cmds.menuItem( label="World" )
        cmds.menuItem( label="Main" )           
        cmds.button (label='Change Selection', p='listBuildButtonLayout', command = lambda *args:self.switchArmIKConstFunct())
        cmds.showWindow(window)

    def switchArmIKConstFunct(self):
        queryType=cmds.optionMenu(typeMenu, q=1, sl=1)
        getArm=cmds.ls(sl=1)
        colour=6
        if queryType==1:
            attributeType=0
        elif queryType==2:
            attributeType=1
        elif queryType==3:
            attributeType=2
        self.getLoc(getArm, colour)
        cmds.pickWalk(d="up")
        getLocation=cmds.ls(sl=1)
        cmds.setAttr(getArm[0]+".ArmFollow", attributeType)
        matrix=cmds.xform(getLocation, q=1, ws=1, m=1)
        cmds.xform(getArm, ws=1, m=matrix)   
        cmds.select(getArm)        
        cmds.setKeyframe()   
        cmds.delete(getLocation) 


    def plot_vert(self):
        '''plots a locator to a vertice or face per keyframe in a timeline'''
        selObj=cmds.ls(sl=1, fl=1)       
        if len(selObj)>0:
            pass
        else:
            print "Select 1 object" 
            return     
        getRange=cmds.playbackOptions(q=1, max=1)#get framerange of scene to set keys in iteration 
        getRange=int(getRange)#change framerange to an integer. May have to change this to a float iterator on a half key blur(butterfly wings)
        getloc=cmds.spaceLocator(n=selObj[0]+"cnstr_lctr")
        cmds.normalConstraint(selObj[0], getloc[0])
        placeloc=cmds.spaceLocator(n=selObj[0]+"lctr")
        for each in range(getRange):
            transform=cmds.xform(selObj, q=True, ws=1, t=True)
            if len(transform)<4:
                pass
            else:
                posBucket=[]
                posBucket.append(self.median_find(transform[0::3]))
                posBucket.append(self.median_find(transform[1::3]))
                posBucket.append(self.median_find(transform[2::3]))
                transform=posBucket
            cmds.xform(getloc[0], ws=1, t=transform)  
            cmds.SetKeyTranslate(getloc[0])
            cmds.xform(placeloc[0], ws=1, t=transform)
            cmds.SetKeyTranslate(placeloc[0])               
            rotate=cmds.xform(getloc[0], q=True, ws=1, ro=True)
            cmds.xform(placeloc[0], ws=1, ro=rotate)  
            cmds.SetKeyRotate(placeloc[0])
            maya.mel.eval( "playButtonStepForward;" )
        cmds.delete(getloc[0])

    def plot_each_vert(self):
        '''plots a locator to a vertice or face per keyframe in a timeline'''
        selObj=cmds.ls(sl=1, fl=1)
        for item in selObj:
            cmds.select(item, r=1)
            self.plot_vert()




    # def plot_each_vertV1(self):
    #     '''plots a locator to a vertice or face per keyframe in a timeline'''
    #     selObj=cmds.ls(sl=1, fl=1)       
    #     if len(selObj)==1:
    #         pass
    #     else:
    #         print "Select 1 object" 
    #     getRange=cmds.playbackOptions(q=1, max=1)#get framerange of scene to set keys in iteration 
    #     getRange=range(int(getRange))#change framerange to an integer. May have to change this to a float iterator on a half key blur(butterfly wings)
    #     dirDict={}
    #     for item in selObj:
    #         getloc=cmds.spaceLocator(n=item+"cnstr_lctr")
    #         cmds.normalConstraint(item, getloc[0])
    #         placeloc=cmds.spaceLocator(n=item+"lctr")
    #         lst=[placeloc[0], getloc[0]]
    #         makeDict={item:lst}
    #         dirDict.update(makeDict)   
    #     for each in getRange: 
    #         for key, value in dirDict.items(): 
    #             plotterLoc=ls(value[0])
    #             constrainedLoc=ls(value[1])
    #             transform=cmds.xform(key, q=True, ws=1, t=True)
    #             cmds.xform(plotterLoc, ws=1, t=transform)  
    #             cmds.SetKeyTranslate(plotterLoc)       
    #             rotate=cmds.xform(constrainedLoc, q=True, ws=1, ro=True)
    #             cmds.xform(plotterLoc, ws=1, ro=rotate)  
    #             cmds.SetKeyRotate(plotterLoc)
    #         maya.mel.eval( "playButtonStepForward;" )
    #         # cmds.currentTime(each)
    #         #cmds.delete(value[0])

                
    # def plot_each_vertV1(self):
    #     '''plots a locator to a vertice or face per keyframe in a timeline'''
    #     selObj=cmds.ls(sl=1, fl=1)       
    #     if len(selObj)==1:
    #         pass
    #     else:
    #         print "Select 1 object" 
    #     getRange=cmds.playbackOptions(q=1, max=1)#get framerange of scene to set keys in iteration 
    #     getRange=int(getRange)#change framerange to an integer. May have to change this to a float iterator on a half key blur(butterfly wings)
    #     for item in selObj:
    #         getloc=cmds.spaceLocator(n=item+"cnstr_lctr")
    #         cmds.normalConstraint(item, getloc[0])
    #         placeloc=cmds.spaceLocator(n=item+"lctr")
    #         for each in range(getRange):
    #             transform=cmds.xform(item, q=True, ws=1, t=True)
    #             cmds.xform(getloc[0], ws=1, t=transform)  
    #             cmds.SetKeyTranslate(getloc[0])
    #             cmds.xform(placeloc[0], ws=1, t=transform)
    #             cmds.SetKeyTranslate(placeloc[0])               
    #             rotate=cmds.xform(getloc[0], q=True, ws=1, ro=True)
    #             cmds.xform(placeloc[0], ws=1, ro=rotate)  
    #             cmds.SetKeyRotate(placeloc[0])
    #             maya.mel.eval( "playButtonStepForward;" )
    #         cmds.delete(getloc[0])

    def onionSkin(self):
        selObj=cmds.ls(sl=1, fl=1)       
        if len(selObj)==1:
            pass
        else:
            print "Select 1 object" 
        getRange=cmds.playbackOptions(q=1, max=1)#get framerange of scene to set keys in iteration 
        getRange=int(getRange)#change framerange to an integer. May have to change this to a float iterator on a half key blur(butterfly wings)
        for each in range(getRange):
            for item in selObj:
                getloc=cmds.spaceLocator(n=item+"cnstr_lctr")
                cmds.normalConstraint(item, getloc[0])
                getNum="%04d" % (each,)
                placeloc=cmds.spaceLocator(n=item+'FR'+str(getNum)+"_lctr")
                transform=cmds.xform(item, q=True, ws=1, t=True)
                cmds.xform(getloc[0], ws=1, t=transform)  
                cmds.SetKeyTranslate(getloc[0])
                cmds.xform(placeloc[0], ws=1, t=transform)
                cmds.SetKeyTranslate(placeloc[0])               
                rotate=cmds.xform(getloc[0], q=True, ws=1, ro=True)
                cmds.xform(placeloc[0], ws=1, ro=rotate)  
                cmds.SetKeyRotate(placeloc[0])
                maya.mel.eval( "playButtonStepForward;" )
                cmds.delete(getloc[0])


    def Percentages(self, getSel, minValue, maxValue):
        collectNewNumbers=[]  
        '''add first value to bucket'''
        collectNewNumbers.append(minValue)  
        '''find incremental percentile to add to bucket'''
        getSeln=getSel[1:-1]#isolate midrange selection
        RangeSel=getSel[:-1]#isolate all but the last (full 100%) list item
        findRangeSpace=maxValue-minValue#find difference of range            
        percentTop=findRangeSpace*100#find the 100% value that could be added to the minimum range to reach the maximum cap amount
        getPercentile=percentTop/len(RangeSel)#divide the cap by the ranged list length to find the incremented value
        BucketValue=[(key+1)*getPercentile*.01 for key in range(len(getSeln))]#reference the mid list length to append the incremented value to bucket
        for each in BucketValue:#Add each value to the minimum number to get true value to add to bucket
            getNum=minValue+each
            collectNewNumbers.append(getNum)
        '''add last value to bucket'''
        collectNewNumbers.append(maxValue)
        return collectNewNumbers
    
    def selection_grab(self):
        '''--------------------------------------------------------------------------------------------------------------------------------------
        Common selection query
        --------------------------------------------------------------------------------------------------------------------------------------'''        
        getSel=ls(sl=1, fl=1)
        if getSel:
            pass
        else:
            print "You need to make a selection for this tool to operate on."
            return
        return getSel

    def selection_location_type(self, selection):
        if objectType(selection)=="transform":
            selection=ls(selection)
            transformWorldMatrix, rotateWorldMatrix=self.locationXForm(selection)
#            for item in selection.getPoints():
#                posBucket=[]
#                posBucket.append(self.median_find(item[0::3]))
#                posBucket.append(self.median_find(item[1::3]))
#                posBucket.append(self.median_find(item[2::3]))
#            transformWorldMatrix=posBucket 
#            selection=ls(selection)
#            rotateWorldMatrix = cmds.xform(selection, q=True, wd=1, ra=True)
        elif objectType(selection)=="joint":
            selection=ls(selection)
            maintransformWorldMatrix=cmds.xform(selection, q=True, ws=1, t=True)
            rotateWorldMatrix=[0, 0, 0]    
            transformWorldMatrix=maintransformWorldMatrix          
        else:
            transforms = listTransforms(selection.node())
            transform = transforms[0]
            maintransformWorldMatrix, mainrotateWorldMatrix=self.locationXForm(transforms)           
            transformWorldVertex=selection.getPosition()
            rotateWorldMatrix=[0, 0, 0]    
            transformWorldMatrix=[x + y for x, y in zip(maintransformWorldMatrix, transformWorldVertex)]
        return transformWorldMatrix, rotateWorldMatrix        

    def locationXFormV2(self, each):
        transform=cmds.xform(each , q=True, ws=1, t=True)
        if transform==[0, 0, 0]:
            transformWorldMatrix = cmds.xform(each, q=True, wd=1, sp=True)  
            rotateWorldMatrix = cmds.xform(each, q=True, wd=1, ra=True) 
        else:
#            transformWorldMatrix = cmds.xform(each, q=True, wd=1, sp=True)  
            transformWorldMatrix = cmds.xform(each, q=True, ws=1, t=True)  
            rotateWorldMatrix = cmds.xform(each, q=True, ws=1, ro=True)  
        return  transformWorldMatrix, rotateWorldMatrix

    def duplicateMove(self):
        getSel=cmds.ls(sl=1, fl=1)
        parentObj=getSel[0]
        for number, each in enumerate(getSel[1:]):
            getParent=cmds.listRelatives(each, p=1)  
            getobj=ls(each)
            transformWorldMatrix = cmds.xform(each, q=True, wd=1, t=True)
            #transformWorldMatrix=getobj[0].getScalePivot(ws=1)[:3]
            rotateWorldMatrix = cmds.xform(each, q=True, ws=1, ro=True)
            newObj=cmds.duplicate(parentObj,n=parentObj+str(number))
            cmds.xform(newObj[0], ws=1, t=transformWorldMatrix)
            cmds.xform(newObj[0], ws=1, ro=rotateWorldMatrix)  
            cmds.select(parentObj, r=1)
            cmds.select(newObj[0], add=1)      
            cmds.parent(newObj[0],getParent)
    
    def locationXForm(self, each):
        getObj=ls(each)[0]
        #transform=getObj.getTranslation()
        transform=cmds.xform(each , q=True, ws=1, t=True)
        if transform==[0.0, 0.0, 0.0]:
            transformWorldMatrix=getObj.getScalePivot(ws=1)[:3]
            #transformWorldMatrix = cmds.xform(each, q=True, wd=1, sp=True)
            rotateWorldMatrix = cmds.xform(each, q=True, wd=1, ra=True)
        else:
#            transformWorldMatrix=getObj.getScalePivot(ws=1)[:3]
            transformWorldMatrix = cmds.xform(each, q=True, ws=1, t=True)
            rotateWorldMatrix = cmds.xform(each, q=True, ws=1, ro=True)
        return transformWorldMatrix, rotateWorldMatrix

    def locationXFormV1(self, each):
        transform=cmds.xform(each , q=True, ws=1, t=True)
        if transform==[0, 0, 0]:
            transformWorldMatrix = cmds.xform(each, q=True, wd=1, sp=True)  
            rotateWorldMatrix = cmds.xform(each, q=True, wd=1, ra=True) 
        else:
            transformWorldMatrix = cmds.xform(each, q=True, ws=1, t=True)  
            rotateWorldMatrix = cmds.xform(each, q=True, ws=1, ro=True)  
        return  transformWorldMatrix, rotateWorldMatrix

    def forcedlocationXForm(self, each):
        transform=cmds.xform(each , q=True, ws=1, t=True)
        transformWorldMatrix = cmds.xform(each, q=True, r=1, sp=True)  
        rotateWorldMatrix = cmds.xform(each, q=True, r=1, ro=True)  
        return  transformWorldMatrix, rotateWorldMatrix
    
    def xformAutoMove(self, aim, target):
        '''move to matrix'''
        matrix=cmds.xform(target, q=1, ws=1, m=1)
        cmds.xform(aim, ws=1, m=matrix)  

    def xformAutoMatch(self, aim, target):
        '''move to transform and rotation relative'''
        transformWorldMatrix=cmds.xform(target, q=1, t=1)
        rotateWorldMatrix=cmds.xform(target, q=1, ro=1) 

    def xformAutoTran(self, aim, target):
        '''move to transform and rotation'''
        transformWorldMatrix, rotateWorldMatrix=self.locationXForm(target)
        cmds.xform(aim, ws=1, t=transformWorldMatrix)
        cmds.xform(aim, ws=1, ro=rotateWorldMatrix)
        
    def xformAutoTranWrist(self, aim, target):
        '''move to transform and rotation'''
        transformWorldMatrix, rotateWorldMatrix=self.locationXForm(target)
        cmds.move(transformWorldMatrix[0], 0.0, transformWorldMatrix[0], aim, r=1, rpr=1 )    

    def _open_defined_path(self, destImagePath):
        folderPath='\\'.join(destImagePath.split("/")[:-1])+"\\"        
        self.opening_folder(folderPath)

    def opening_folder(self, folderPath):
        if "Windows" in OSplatform:
            folderPath=re.sub(r'/',r'\\', folderPath)
            os.startfile(folderPath)
        if "Linux" in OSplatform:
            newfolderPath=re.sub(r'\\',r'/', folderPath)
            os.system('xdg-open "%s"' % newfolderPath) 
