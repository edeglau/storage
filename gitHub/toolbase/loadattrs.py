
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
import glob
from random import randint
from pymel.core import *
import pymel.core as pm
#import win32clipboard
import operator
from sys import argv
from datetime import datetime
from operator import itemgetter
from inspect import getsourcefile
from os.path import abspath
OSplatform=platform.platform()
import baseMockFunctions_maya
reload (baseMockFunctions_maya)
import ast
from numpy import arange

getBaseClass=baseMockFunctions_maya.BaseClass() 
workSpace=cmds.workspace(q=1, lfw=1)[-1]
M_USER = os.getenv("USER")
PROJECT=os.getenv("M_JOB")
SCENE=os.getenv("SEQUENCE_SHOT_")
SHOT=os.getenv("M_LEVEL")
DEPT=os.getenv("M_TASK")

projectFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/scenes/'
sceneFolder='/jobs/'+PROJECT+'/'+SCENE
animFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/instances/'
abcFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/cache/alembic/'
pbFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/TASKS/'+DEPT+'/maya/movies/'
rvFolder='/jobs/'+PROJECT+'/'+SCENE+'/'+SHOT+'/PRODUCTS/images/'+DEPT


getType=["nCloth", "nucleus", "dynamicConstraint", "nRigid", "nHair", "hairSystem"]

proj_commonFolder='/jobs/'+PROJECT+'/COMMON/rig/users/deglaue/dyn_att_presets/'


class attributeSwapper(object):


        def saveAttributesWindow(self, arg=None):
            folderBucket=[]
            winName = "Save attribute"
            winTitle = winName
            if cmds.window(winName, exists=True):
                    deleteUI(winName)
            window = cmds.window(winName, title=winTitle, tbm=1, w=620, h=100 )
            cmds.menuBarLayout(h=30)
            stringField='''"Save Anim/Attr" (launches window)a home made scripted save anim keys and attribute values
        into external file(s)(works on a heirarchy). Put full file path with preferred name of
        object in text field("/usr/people/<user>/joint4"). save button saves out file. Can add
        more to save from add selected at top. Will save out a file
        EG:"/usr/people/<user>/joint4.txt"

            * Step 1: select object
            * Step 2: pressing save will create .txt files that will contain the animation
                and attriute values for heirarchy(if applicable) within the path indicated
                and name of file indicated in field

             "ADD SELECTION" - button
                Adds a slot for new object (each parent is added seperately)
            "SAVE" - button
                Will change the value on the attribute that is currently
                    visible in the drop down menu
            "OPEN FOLDER" - button
                opens the folder window for path indicated
            "ATTR DICT" - button
                prints out an attriubute dictionary for personal use(see script editor)
                useful for writing a "setAttr" script on custom setups'''
            self.fileMenu = cmds.menu( label='Help', pmc=lambda *args:self.helpWin(stringField))        
            cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=620)
            cmds.frameLayout('bottomFrame', label='', lv=0, nch=1, borderStyle='in', bv=1, p='selectArrayRow')     
            cmds.gridLayout('topGrid', p='bottomFrame', numberOfColumns=1, cellWidthHeight=(620, 20))   
            cmds.text("Objects to save/load attributes:")
            # cmds.button (label='Add selected(one at a time)', p='topGrid', command = lambda *args:self._add_function())
            cmds.gridLayout('topBuild', p='bottomFrame', numberOfColumns=1, cellWidthHeight=(600, 20))
            cmds.text(label="")        
            fieldBucket=[]
            getpaths=[proj_commonFolder]
            # getpaths.append(sceneFolder)
            getpaths.append(projectFolder)
            getpaths.append("custom")
            self.foundPath=cmds.optionMenu( label='Path')            
            for each in getpaths:
                cmds.menuItem( label=each)
            cmds.rowColumnLayout( 'midBuild',  p='bottomFrame', numberOfColumns=2, columnWidth=[(1, 100), (2, 500)])
            # cmds.rowLayout  (' midBuild ', w=600, numberOfColumns=6, cw6=[150, 140, 140, 140, 140, 1], ct6=[ 'both', 'both', 'both',  'both', 'both', 'both'], p='bottomFrame')
            cmds.text("sim type:" , p='midBuild')
            self.getName=cmds.textField(h=25, p='midBuild', text="runningThenStop")
            # cmds.rowColumnLayout( 'lowerBuild',  p='bottomFrame', numberOfColumns=2, columnWidth=[(1, 150), (2, 500)])
            cmds.text("custom path:")
            self.getPath=cmds.textField(h=25, text=projectFolder)
            # cmds.button (label='Save Anim', w=60, p='listBuildButtonLayout', command = lambda *args:self._save_anim(each, fileName=cmds.textField(self.getName, q=1, text=1)))
            cmds.gridLayout('listBuildButtonLayout', p='bottomFrame', numberOfColumns=3, cellWidthHeight=(150, 30))
            # cmds.rowLayout  (' listBuildButtonLayout ', w=600, numberOfColumns=6, cw6=[40, 40, 40, 40, 40, 1], ct6=[ 'both', 'both', 'both',  'both', 'both', 'both'], p='bottomFrame')
            cmds.button (label='Save Dyn', p='listBuildButtonLayout', command = lambda *args:self._save_anim_heirarchy(fileName=cmds.textField(self.getName, q=1, text=1), getPathCustom=cmds.textField(self.getPath, q=1, text=1), optionPath=cmds.optionMenu(self.foundPath, q=1, v=1)))            
            cmds.button (label='Save General', p='listBuildButtonLayout', command = lambda *args:self._save_gen_anim_heirarchy(fileName=cmds.textField(self.getName, q=1, text=1), getPathCustom=cmds.textField(self.getPath, q=1, text=1), optionPath=cmds.optionMenu(self.foundPath, q=1, v=1)))            
            cmds.button (label='Save AllDyn', p='listBuildButtonLayout', command = lambda *args:self._save_allDyn_heirarchy(fileName=cmds.textField(self.getName, q=1, text=1), getPathCustom=cmds.textField(self.getPath, q=1, text=1), optionPath=cmds.optionMenu(self.foundPath, q=1, v=1)))
            cmds.button (label='Save Selected', p='listBuildButtonLayout', command = lambda *args:self._save_gen_sel_anim_heirarchy(fileName=cmds.textField(self.getName, q=1, text=1), getPathCustom=cmds.textField(self.getPath, q=1, text=1), optionPath=cmds.optionMenu(self.foundPath, q=1, v=1)))            
            cmds.button (label='Save-plot Constrained', p='listBuildButtonLayout', command = lambda *args:self.store_obj_matrix_pt(fileName=cmds.textField(self.getName, q=1, text=1), getPathCustom=cmds.textField(self.getPath, q=1, text=1), optionPath=cmds.optionMenu(self.foundPath, q=1, v=1)))
            # cmds.button (label='Save Constrained', p='listBuildButtonLayout', command = lambda *args:self.store_obj_matrix_pt(each, fileName=cmds.textField(self.getName, q=1, text=1)))
            cmds.button (label='Load atts', p='listBuildButtonLayout', w=150, command = lambda *args:self.openAttributesWindow(getPathCustom=cmds.textField(self.getPath, q=1, text=1), optionPath=cmds.optionMenu(self.foundPath, q=1, v=1)))
            cmds.button (label='Open folder', p='listBuildButtonLayout', command = lambda *args:self.opening_folder_callup(getPathCustom=cmds.textField(self.getPath, q=1, text=1), optionPath=cmds.optionMenu(self.foundPath, q=1, v=1)))
            cmds.button (label='Attr dict', w=60, ann=" prints a dictionary with attributes(for dev)", p='listBuildButtonLayout', command = lambda *args:self._printAttributes())
            cmds.showWindow(window)  

        def opening_folder_callup(self, getPathCustom, optionPath):
            if optionPath=="custom":   
                FoundPath=getPathCustom
            else:
                FoundPath=optionPath
            self.opening_folder(FoundPath)

        def opening_folder(self, folderPath):
            os.system('caja "%s"' % folderPath)   

        def store_obj_matrix_pt(self, fileName, getPathCustom, optionPath):    
            '''plots transforms off of an object with constraint to a text file'''
            if optionPath=="custom":   
                FoundPath=getPathCustom
            else:
                FoundPath=optionPath   
            objectSel=cmds.ls(sl=1)
            if len(objectSel)>0:
                pass
            else:
                print "Select 1 object" 
                return     
            fileName=FoundPath+'/'+fileName+'.txt'
            print fileName
            if "Windows" in OSplatform:
                if not os.path.exists(fileName): os.makedirs(fileName)
            if "Linux" in OSplatform:
                inp=open(fileName, 'w+')
            getTopRange=cmds.playbackOptions(q=1, max=1)+1#get framerange of scene to set keys in iteration 
            getLowRange=cmds.playbackOptions(q=1, min=1)-1#get framerange of scene to set keys in iteration 
            getRange=arange(getLowRange,getTopRange, 1 )
            collection_of_valueTX={}
            collection_of_valueTY={}
            collection_of_valueTZ={}
            collection_of_valueRX={}
            collection_of_valueRY={}
            collection_of_valueRZ={}
            for each_obj in objectSel:            
                inp.write('\n'+str(each_obj)+">>")        
                for each_frame in getRange:
                    cmds.currentTime(each_frame)            
                    transform=cmds.xform(each_obj, q=True, ws=1, t=True)
                    rotation=cmds.xform(each_obj, q=True, ws=1, ro=True)
                    if len(transform)<4:
                        pass
                    else:
                        posBucket=[]
                        posBucket.append(self.median_find(transform[0::3]))
                        posBucket.append(self.median_find(transform[1::3]))
                        posBucket.append(self.median_find(transform[2::3]))
                        transform=posBucket
                    # print str(each_frame)+":"+str(transform[0])
                    makeDictTX = {each_frame:transform[0]}
                    collection_of_valueTX.update(makeDictTX)
                    makeDictTY = {each_frame:transform[1]}
                    collection_of_valueTY.update(makeDictTY)
                    makeDictTZ = {each_frame:transform[2]}
                    collection_of_valueTZ.update(makeDictTZ)
                    makeDictRX = {each_frame:rotation[0]}
                    collection_of_valueRX.update(makeDictRX)
                    makeDictRY = {each_frame:rotation[1]}
                    collection_of_valueRY.update(makeDictRY)
                    makeDictRZ = {each_frame:rotation[2]}
                    collection_of_valueRZ.update(makeDictRZ)
                    cmds.currentTime(each_frame)
                inp.write("<translateX;")
                inp.write(str(collection_of_valueTX))
                inp.write("<translateY;")
                inp.write(str(collection_of_valueTY))
                inp.write("<translateZ;")
                inp.write(str(collection_of_valueTZ))
                inp.write("<rotateX;")
                inp.write(str(collection_of_valueRX))
                inp.write("<rotateY;")
                inp.write(str(collection_of_valueRY))
                inp.write("<rotateZ;")
                inp.write(str(collection_of_valueRZ))
            inp.close()

        # def _printAttributesv1(self):
        #     notAttr=["isHierarchicalConnection", "fieldDistance", "dieOnEmissionVolumeExit", "solverDisplay", "isHierarchicalNode", "currentTime", "publishedNodeInfo", "fieldScale_Position", "solverDisplay"] 
        #     selObj=cmds.ls(sl=1, fl=1)
        #     newDict={}
        #     print "{"
        #     for each in selObj:            
        #         getListedAttr=sorted(set([(attrib) for attrib in listAttr (each, w=1, a=1, s=1,u=1) for dontwantattr in notAttr if dontwantattr not in attrib]))
        #         for eachAttribute in getListedAttr:
        #             if "." not in eachAttribute:
        #                 try:
        #                     getVal=cmds.getAttr(each+"."+str(eachAttribute))
        #                     print '"'+each+'.'+str(eachAttribute)+'":'+str(getVal)+","
        #                 except:
        #                     pass
        #     print "}"
        def _printAttributes_base(self):
            notAttr=[
            "isHierarchical", 
            "Emission",
            "fieldDistance", 
            "event", 
            "ghost", 
            "PerVertex", 
            "localWind", 
            "localField", 
            "position", 
            "maxVisibilitySamples*", 
            "next*", 
            "parentMatrixDirty", 
            "particleId0", 
            "override", 
            "Override", 
            "Color", 
            # "dieOnEmissionVolumeExit", 
            "useObjectColor", 
            "solverDisplay", 
            "isHierarchicalNode", 
            "useOutlinerColor", 
            "currentTime", 
            "publishedNodeInfo", 
            "fieldScale_Position",
            "viewMode",
            "visibility",
            "uiTreatment",
            "startEmittedIndex",
            "velocity"] 
            selObj=cmds.ls(sl=1, fl=1)
            newDict={}
            print "{"
            for each in selObj:            
                getListedAttr=sorted(set([(attrib) for attrib in listAttr (each, w=1, a=1, s=1,u=1)for dontwantattr in notAttr if dontwantattr not in attrib]))
                for eachAttribute in getListedAttr:
                    if "." not in eachAttribute:
                        try:
                            getVal=cmds.getAttr(each+"."+str(eachAttribute))
                            if len(getVal)>0:
                                print '"'+each+'.'+str(eachAttribute)+'":'+str(getVal)+","
                        except:
                            pass
            print "}"

        def _printAttributes(self):
            if cmds.nodeType(cmds.ls(sl=1)[0]) == "nCloth":
                self._printAttributes_cloth()
            else:
                self._printAttributes_base()

        def _printAttributes_cloth(self):
            takeAttr=[
            "isDynamic", 
            "pointMass", 
            "startFrame", 
            "cacheData", 
            "collideLastThreshold",
            "collide",
            "collisionFlag",
            "maxIterations",
            "maxSelfCollisionIterations",
            "selfCollide", 
            "collisionLayer", 
            "thickness", 
            "selfCollideWidthScale", 
            "selfCrossoverPush", 
            "selfTrappedCheck", 
            "selfCollisionFlag", 
            "bounce", 
            "friction", 
            "stickiness", 
            "bendResistance", 
            "stretchResistance", 
            "compressionResistance", 
            "bendAngleDropoff", 
            "bendAngleScale", 
            "shearResistance", 
            "restitutionAngle", 
            "restitutionTension", 
            "rigidity",
            "addCrossLinks",
            "crossoverPush",
            "pushOutRadius",
            "airPushVorticity",
            "airPushDistance",
            "pushOut",
            "sortLinks",
            # "dieOnEmissionVolumeExit", 
            "inputMeshAttract", 
            "inputAttractDamp", 
            "inputMotionDrag", 
            "restLengthScale", 
            "mass", 
            "lift",
            "drag",
            "tangentialDrag",
            "damp",
            "stretchDamp",
            "incompressibility",
            "sealHoles",
            "pumpRate",
            "pressureDamping",
            "pressure",
            "inputGeometrySpace",
            "targetGeometrySpace",
            "scalingRelation"] 
            selObj=cmds.ls(sl=1, fl=1)
            print "{"
            for each in selObj:             
                getListedAttr=[(attrib) for attrib in listAttr (each, w=1, a=1, s=1,u=1) for item in takeAttr if item == attrib]
                for item in getListedAttr:
                    if "PerVertex" not in item:
            # for each, item in map(None, selObj, getListedAttr):             
                        try:
                            getVal=cmds.getAttr(each+"."+str(item))
                            print '"'+each+'.'+str(item)+'":'+str(getVal)+","
                        except:
                            pass
            print "}"

        def _printAttributesv2(self):
            notAttr=[
            "isHierarchical", 
            "die", 
            "fieldDistance", 
            "event", 
            "ghost", 
            "PerVertex", 
            "localWind", 
            "localField", 
            "position", 
            "maxVisibilitySamples*", 
            "next*", 
            "parentMatrixDirty", 
            "particleId0", 
            "override", 
            "Override", 
            "Color", 
            "dieOnEmissionVolumeExit", 
            "useObjectColor", 
            "solverDisplay", 
            "isHierarchicalNode", 
            "useOutlinerColor", 
            "currentTime", 
            "publishedNodeInfo", 
            "fieldScale_Position",
            "viewMode",
            "visibility",
            "uiTreatment",
            "startEmittedIndex",
            "velocity"] 
            selObj=cmds.ls(sl=1, fl=1)
            newDict={}
            print "{"
            for each in selObj:            
                getListedAttr=[(attrib) for attrib in listAttr (each, w=1, a=1, s=1,u=1) if "solverDisplay" not in attrib]
                for eachAttribute in getListedAttr:
                    if eachAttribute not in notAttr:
                        for item in getListedAttr:
                            if "." not in item:
                                try:
                                    getVal=cmds.getAttr(each+"."+item)
                                    if len(getVal)>0:
                                        print '"'+each+'.'+str(item)+'":'+str(getVal)+","
                                    else:
                                        pass
                                except:
                                    pass
            # for key, value in newDict.items():
                # print "'"+str(key)+"':"+str(value)+","
            print "}"


        def _open_defined_path(self, destImagePath):
            print destImagePath
            folderPath='\\'.join(destImagePath.split("/")[:-1])+"\\"        
            self.opening_folder(folderPath)

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

        def openAttributesWindow(self, getPathCustom, optionPath):
            # getPath=proj_commonFolder
            # print optionPath
            if optionPath=="custom":   
                getPath=getPathCustom
            else:
                getPath=optionPath             
            getFiles=[os.path.join(getPath, o) for o in os.listdir(getPath) if os.path.isdir(os.path.join(getPath, o))]
            getFiles.sort(key=lambda x: os.path.getmtime(x))
            self._choser_group_window(getFiles) 

        def _choser_group_window(self, getListAttr):
            winGrpName = "Pick from below"
            if cmds.window(winGrpName, exists=True):
                cmds.deleteUI(winGrpName)
            choose_window = cmds.window(winGrpName, title=winGrpName, tbm=1, w=800, h=150)
            cmds.menuBarLayout(h=30)
            cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=800)
            cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
            cmds.rowLayout  (' rMainRow ', w=800, numberOfColumns=1, p='selectArrayRow')
            cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
            cmds.setParent ('selectArrayColumn')
            cmds.separator(h=10, p='selectArrayColumn')
            cmds.frameLayout('title1', bgc=[0.15, 0.15, 0.15], cll=1, label='Select version', lv=1, nch=1, borderStyle='out', bv=1, w=800, fn="tinyBoldLabelFont", p='selectArrayColumn')
            cmds.gridLayout('valuebuttonlayout', p='title1', numberOfColumns=2, cellWidthHeight=(800, 20))  
            self.attributeFirstSel=cmds.optionMenu( label='Find')
            getListAttr = sorted (getListAttr)
            for each in getListAttr:
                cmds.menuItem( label=each)
            cmds.gridLayout('listBuildButtonLayout', p='title1', numberOfColumns=3, cellWidthHeight=(148, 20))
            cmds.button (label='Selected', p='listBuildButtonLayout', w=150, command = lambda *args:self._applyallatt_selected(folderType=cmds.optionMenu(self.attributeFirstSel, q=1, v=1)))
            cmds.button (label='SelectedDyn', p='listBuildButtonLayout', w=150, command = lambda *args:self._applyallatt_dynselected(folderType=cmds.optionMenu(self.attributeFirstSel, q=1, v=1)))
            cmds.button (label='Load All', p='listBuildButtonLayout', w=150, command = lambda *args:self._apply_found_att(folderType=cmds.optionMenu(self.attributeFirstSel, q=1, v=1)))
            cmds.button (label='Force Selected', p='listBuildButtonLayout', w=150, command = lambda *args:self.open_genAttributefolderWindow(getFolderFiles=cmds.optionMenu(self.attributeFirstSel, q=1, v=1)))
            cmds.button (label='open folder', p='listBuildButtonLayout', w=150, command = lambda *args:self._open_defined_path(cmds.optionMenu(self.attributeFirstSel, q=1, v=1)))
            cmds.showWindow(choose_window) 
              


        def _apply_found_att(self, folderType):
            getallfiles=os.listdir(folderType)
            notAttr=["isHierarchicalConnection", "solverDisplay", "isHierarchicalNode", "publishedNodeInfo", "fieldScale_Position", "fieldScale", "fieldScale.fieldScale_Position"]         
            for filename in getallfiles:
                isolateFileName=filename.split('.')[0]
                # if ":" in isolateFileName:
                #     isolateitemName=isolateFileName.split(':')[-1]        
                # else:
                isolateitemName=isolateFileName
                print isolateitemName
                try:
                    getItemInScene=cmds.ls('*:'+isolateitemName)[0]
                except:
                    getItemInScene=isolateitemName
                if cmds.objExists(getItemInScene):
                    attribute_container=[]
                    getListedAttr=[(attrib) for attrib in cmds.listAttr(getItemInScene, k=1, s=1, iu=1, u=1, lf=1, m=0) for item in notAttr if item not in attrib]             
                    printFolder=folderType+'/'+filename
                    List = open(printFolder).readlines()
                    for aline in List:
                        if ">>" in aline:
                            # getObj=aline.split('>>')[0]
                            getExistantInfo=aline.split('>>')[1]
                            if getExistantInfo!="\n":
                                findAtt=getExistantInfo.split("<")
                                for eachInfo in findAtt:
                                    getAnimDicts=eachInfo.split(";")
                                    for eachctrl in xrange(len(getAnimDicts) - 1):
                                        current_item, next_item = getAnimDicts[eachctrl], getAnimDicts[eachctrl + 1]
                                        # cmds.setAttr(cmds.ls(getObj)[0]+'.'+current_item, value)
                                        gethis=ast.literal_eval(next_item)
                                        print "setting: "+str(cmds.ls(getItemInScene)[0])+"."+str(eachInfo)+" at "+str(gethis)
                                        try:
                                            if len(gethis)<2:
                                                for key, value in gethis.items():
                                                    for listeditem in getListedAttr:
                                                        if current_item==listeditem:
                                                            cmds.setAttr(cmds.ls(getItemInScene)[0]+'.'+current_item, value)   
                                                            # cmds.setAttr(cmds.ls(getObj)[0]+'.'+current_item, value)                                                 
                                                            # print "set "+ cmds.ls(getObj)[0]+'.'+current_item+" at "+str(value)
                                            else:
                                                 for key, value in gethis.items():
                                                    for listeditem in getListedAttr:
                                                        if current_item==listeditem:
                                                            cmds.setKeyframe( cmds.ls(getItemInScene)[0], t=key, at=current_item, v=value )  
                                                            # print "set "+ cmds.ls(getObj)[0]+'.'+current_item+' at '+str(value)+" frame "+str(key)                               
                                        except:
                                            pass                                              
                            else:
                                pass

 



        def _applyallatt_selected(self, folderType):
            # print folderType
            getallfiles=os.listdir(folderType)
            getallfiles=[(each) for each in getallfiles if each.endswith('.txt')]
            # print getallfiles             
            notAttr=["isHierarchicalConnection", "solverDisplay", "isHierarchicalNode", "publishedNodeInfo", "fieldScale_Position", "fieldScale", "fieldScale.fieldScale_Position"]         
            # selObj=cmds.ls(sl=1, fl=1)
            for each in cmds.ls(sl=1):
                # if ":" in each:
                #     shortname=each.split(':')[-1]
                #     print shortname
                shortname=each
                for filename in getallfiles:
                    if "." in filename:
                        isolateFilename=filename.split('.')[0] 
                        if ":" in isolateFilename:
                            isolateFilename=shortname
                        else:
                            isolateFilename=isolateFilename
                        if isolateFilename == shortname:
                            print isolateFilename+" proceeding to apply to "+each
                            attribute_container=[]
                            getListedAttr=[(attrib) for attrib in cmds.listAttr(each, k=1, s=1, iu=1, u=1, lf=1, m=0) for item in notAttr if item not in attrib]             
                            printFolder=folderType+'/'+filename
                            List = open(printFolder).readlines()
                            for aline in List:
                                if ">>" in aline:
                                    getObj=aline.split('>>')[0]
                                    getExistantInfo=aline.split('>>')[1]
                                    if getExistantInfo!="\n":
                                        findAtt=getExistantInfo.split("<")
                                        for eachInfo in findAtt:
                                            getAnimDicts=eachInfo.split(";")
                                            for eachctrl in xrange(len(getAnimDicts) - 1):
                                                current_item, next_item = getAnimDicts[eachctrl], getAnimDicts[eachctrl + 1]
                                                # cmds.setAttr(cmds.ls(getObj)[0]+'.'+current_item, value)
                                                gethis=ast.literal_eval(next_item)
                                                print "setting: "+str(each)+"."+str(eachInfo)+" at "+str(gethis)
                                                try:
                                                    if len(gethis)<2:
                                                        for key, value in gethis.items():
                                                            for listeditem in getListedAttr:
                                                                if current_item==listeditem:
                                                                    cmds.setAttr(each+'.'+current_item, value)                                                 
                                                    else:
                                                         for key, value in gethis.items():
                                                            for listeditem in getListedAttr:
                                                                if current_item==listeditem:
                                                                    cmds.setKeyframe( each, t=key, at=current_item, v=value )  
                                                except:
                                                    pass                                              
                                    else:
                                        pass



        def forceAtt(self, getPath, getPathfile):
            folderType=getPath+'/'+getPathfile
            # folderType=getPathfile
            # print folderType    
            notAttr=["isHierarchicalConnection", "solverDisplay", "isHierarchicalNode", "publishedNodeInfo", "fieldScale_Position", "fieldScale", "fieldScale.fieldScale_Position"]
            List = open(folderType).readlines()
            for each in cmds.ls(sl=1):
                for aline in List:
                    attribute_container=[]
                    getListedAttr=[(attrib) for attrib in cmds.listAttr(each, k=1, s=1, iu=1, u=1, lf=1, m=0) for item in notAttr if item not in attrib]             
                    # printFolder=folderType+'/'+filename
                    # List = open(printFolder).readlines()
                    # for aline in List:
                    if ">>" in aline:
                        getObj=aline.split('>>')[0]
                        getExistantInfo=aline.split('>>')[1]
                        if getExistantInfo!="\n":
                            findAtt=getExistantInfo.split("<")
                            for eachInfo in findAtt:
                                getAnimDicts=eachInfo.split(";")
                                for eachctrl in xrange(len(getAnimDicts) - 1):
                                    current_item, next_item = getAnimDicts[eachctrl], getAnimDicts[eachctrl + 1]
                                    gethis=ast.literal_eval(next_item)
                                    # cmds.setAttr(cmds.ls(getObj)[0]+'.'+current_item, value)
                                    print "changing: "+str(each)+"."+str(eachInfo)+" at "+str(gethis)
                                    gethis=ast.literal_eval(next_item)
                                    try:
                                        if len(gethis)<2:
                                            for key, value in gethis.items():
                                                # oldAttr=cmds.getAttr(str(each)+"."+str(eachInfo))
                                                # print oldAttr, value
                                                #     print "changing: "+str(each)+"."+str(eachInfo)+" at "+str(gethis)
                                                for listeditem in getListedAttr:
                                                    if current_item==listeditem:
                                                        cmds.setAttr(each+'.'+current_item, value)                                                 
                                        else:
                                             for key, value in gethis.items():
                                                # oldAttr=cmds.getAttr(str(each)+"."+str(eachInfo))
                                                # print oldAttr, value
                                                # if oldAttr != value:
                                                #     print "changing: "+str(each)+"."+str(eachInfo)+" at "+str(gethis)                                                
                                                for listeditem in getListedAttr:
                                                    if current_item==listeditem:
                                                        cmds.setKeyframe( each, t=key, at=current_item, v=value )  
                                    except:
                                        pass                                              
                        else:
                            pass



        def _applyallatt_dynselected(self, folderType):
            # print folderType
            '''This copies values and animcurve nodes of all dyn in scene'''
            # getType=["nCloth", "nucleus"]
            collectItem=[(item) for each in getType for item in cmds.ls(type=each) ]
            getallfiles=os.listdir(folderType)
            # print getallfiles
            collectItem=[]
            for each in cmds.ls(sl=1):
                if cmds.nodeType(each)=="transform":
                    getRelatives=cmds.listRelatives(each , c=1)
                    for eachRelative in getRelatives:
                        collectItem.append(eachRelative)
                else:
                    collectItem.append(each)
            collectItem=set(collectItem)               
            notAttr=["isHierarchicalConnection", "solverDisplay", "isHierarchicalNode", "publishedNodeInfo", "fieldScale_Position", "fieldScale", "fieldScale.fieldScale_Position"]         
            # selObj=cmds.ls(sl=1, fl=1)
            for each in collectItem:
                for filename in getallfiles:
                    isolateFilename=filename.split('.')[0] 
                    isolateitemName=each.split(':')[1]
                    if isolateFilename == isolateitemName:
                        attribute_container=[]
                        getListedAttr=[(attrib) for attrib in cmds.listAttr(each, k=1, s=1, iu=1, u=1, lf=1, m=0) for item in notAttr if item not in attrib]             
                        printFolder=folderType+'/'+filename
                        List = open(printFolder).readlines()
                        for aline in List:
                            if ">>" in aline:
                                getObj=aline.split('>>')[0]
                                getExistantInfo=aline.split('>>')[1]
                                if getExistantInfo!="\n":
                                    findAtt=getExistantInfo.split("<")
                                    for eachInfo in findAtt:
                                        getAnimDicts=eachInfo.split(";")
                                        for eachctrl in xrange(len(getAnimDicts) - 1):
                                            current_item, next_item = getAnimDicts[eachctrl], getAnimDicts[eachctrl + 1]
                                            # cmds.setAttr(cmds.ls(getObj)[0]+'.'+current_item, value)
                                            gethis=ast.literal_eval(next_item)
                                            print "setting: "+str(each)+"."+str(eachInfo)+" at "+str(gethis)
                                            try:
                                                if len(gethis)<2:
                                                    for key, value in gethis.items():
                                                        for listeditem in getListedAttr:
                                                            if current_item==listeditem:
                                                                cmds.setAttr(cmds.ls(getObj)[0]+'.'+current_item, value)                                                 
                                                else:
                                                     for key, value in gethis.items():
                                                        for listeditem in getListedAttr:
                                                            if current_item==listeditem:
                                                                cmds.setKeyframe( cmds.ls(getObj)[0], t=key, at=current_item, v=value )  
                                            except:
                                                pass                                              
                                else:
                                    pass


        def open_genAttributefolderWindow(self, getFolderFiles):
            getPath=getFolderFiles      
            getFiles=os.listdir(getPath)
            # getFiles=[os.path.join(getPath, o) for o in os.listdir(getPath) if os.path.isdir(os.path.join(getPath, o))]
            getFiles = sorted(getFiles)
            # getFiles.sort(key=lambda x: os.path.getmtime(x))
            self._choser_gen_group_window(getFiles, getPath) 

        def _choser_gen_group_window(self, getFiles, getPath):
            getFiles.sort()
            choose_gen_grp_win = "Pick from text files"
            if cmds.window(choose_gen_grp_win, exists=True):
                cmds.deleteUI(choose_gen_grp_win)
            chooser_gen_window = cmds.window(choose_gen_grp_win, title=choose_gen_grp_win, tbm=1, w=800, h=150)
            cmds.menuBarLayout(h=30)
            cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=800)
            cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
            cmds.rowLayout  (' rMainRow ', w=800, numberOfColumns=1, p='selectArrayRow')
            cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
            cmds.setParent ('selectArrayColumn')
            cmds.separator(h=10, p='selectArrayColumn')
            cmds.frameLayout('title1', bgc=[0.15, 0.15, 0.15], cll=1, label='Select version', lv=1, nch=1, borderStyle='out', bv=1, w=800, fn="tinyBoldLabelFont", p='selectArrayColumn')
            cmds.gridLayout('valuebuttonlayout', p='title1', numberOfColumns=2, cellWidthHeight=(800, 20))  
            self.attributepath=cmds.optionMenu( label='Find')
            for each in getFiles:
                cmds.menuItem( label=each)
            cmds.gridLayout('listBuildButtonLayout', p='title1', numberOfColumns=3, cellWidthHeight=(148, 20))
            cmds.button (label='Ok', p='listBuildButtonLayout', w=150, command = lambda *args:self.forceAtt(getPath, getPathfile=cmds.optionMenu(self.attributepath, q=1, v=1)))
            cmds.button (label='open folder', p='listBuildButtonLayout', w=150, command = lambda *args:self._open_defined_path(cmds.optionMenu(self.attributepath, q=1, v=1)))
            cmds.showWindow(chooser_gen_window) 


        def makeFolder(self, folderType):
            if os.path.exists(folderType):
                pass
            else:
                os.makedirs(folderType)


        def _save_anim_heirarchy(self, fileName, getPathCustom, optionPath):   
            # print optionPath
            if optionPath=="custom":   
                FoundPath=getPathCustom
            else:
                FoundPath=optionPath
            selObj=ls(sl=1, fl=1, sn=1)
            if len(selObj)<1:
                print "select something"
                return
            else:
                pass            
            '''This copies values and animcurve nodes of shapes other than transforms'''
            folderType=FoundPath+'/'+fileName
            if os.path.exists(folderType):
                pass
            else:
                self.makeFolder(folderType)
            collectItem=[]
            for each in cmds.ls(sl=1):
                if cmds.nodeType(each)=="transform":
                    getRelatives=cmds.listRelatives(each , c=1)
                    for eachRelative in getRelatives:
                        collectItem.append(eachRelative)
                else:
                    collectItem.append(each)
            collectItem=set(collectItem)        
            print "alibrary={"
            self.save_att_function(collectItem, folderType)


        def _save_gen_sel_anim_heirarchy(self, fileName, getPathCustom, optionPath): 
            '''This copies values and animcurve nodes of selected'''
            if optionPath=="custom":   
                FoundPath=getPathCustom
            else:
                FoundPath=optionPath            
            selObj=ls(sl=1, fl=1, sn=1)
            if len(selObj)<1:
                print "select something"
                return
            else:
                pass            
            folderType=FoundPath+'/'+fileName
            if os.path.exists(folderType):
                pass
            else:
                self.makeFolder(folderType)
            filterNode=["animCurve"]
            dirDict={}
            collectItem=cmds.ls(sl=1)        
            self.save_literal_att_function(collectItem, folderType)



        def _save_gen_anim_heirarchy(self, fileName, getPathCustom,optionPath): 
            '''This copies values and animcurve nodes of selected'''
            selObj=ls(sl=1, fl=1, sn=1)
            if len(selObj)<1:
                print "select something"
                return
            else:
                pass            
            print radioType
            folderType=proj_commonFolder+'/'+fileName
            if os.path.exists(folderType):
                pass
            else:
                self.makeFolder(folderType)
            filterNode=["animCurve"]
            dirDict={}
            collectItem=cmds.ls(sl=1)        
            self.save_att_function(collectItem, folderType)


        def _save_allDyn_heirarchy(self, fileName, getPathCustom, optionPath): 
            '''This copies values and animcurve nodes of all dyn in scene'''
            if optionPath=="custom":   
                FoundPath=getPathCustom
            else:
                FoundPath=optionPath              
            # getType=["nCloth", "nucleus", "dynamicConstraint", "nRigid", "nHair"]
            collectItem=[(item) for each in getType for item in cmds.ls(type=each) ]
            folderType=FoundPath+'/'+fileName
            if os.path.exists(folderType):
                pass
            else:
                self.makeFolder(folderType)
            filterNode=["animCurve"]
            dirDict={}
            self.save_att_function(collectItem, folderType)


        def save_literal_att_function(self, collectItem, folderType):
            filterNode=["animCurve"]
            dirDict={}            
            notAttr=["isHierarchicalConnection", "fieldDistance", "dieOnEmissionVolumeExit", "solverDisplay", "isHierarchicalNode", "currentTime", "publishedNodeInfo", "fieldScale_Position"] 
            getStrtRange=cmds.playbackOptions(q=1, ast=1)#get framerange of scene to set keys in iteration
            getEndRange=cmds.playbackOptions(q=1, aet=1)#get framerange of scene to set keys in iteration            
            for each in collectItem:
                print "proceeding"
                # try:
                #     namer=each.split(":")[1]
                # except:
                namer=each
                fileName=folderType+'/'+namer+'.txt'
                print fileName
                inp=open(fileName, 'w+')                
                getChildren=[each]
                for eachChildTree in getChildren:
                    inp.write('\n'+str(eachChildTree)+">>")
                    getListedAttr=[(attrib) for attrib in listAttr (eachChildTree, w=1, a=1, s=1,u=1) if "solverDisplay" not in attrib]
                    for eachAttribute in getListedAttr:
                        try:
                            findFact=cmds.listConnections( eachChildTree+'.'+eachAttribute, d=False, s=True )
                            # findFact=[(eachConnected) for eachConnected in cmds.nodeType(ls_str[0].split(".")[0], i=1) for eachFilter in filterNode if eachConnected==eachFilter]
                            if findFact==None:
                                try:
                                    attrVal=cmds.getAttr(eachChildTree+"."+eachAttribute)
                                    inp.write("<"+str(eachAttribute+";"))
                                    makeDict={0.0:attrVal}
                                    inp.write(str(makeDict))
                                except:
                                    pass
                            else:
                                try:
                                    dirDict={}
                                    frames=cmds.keyframe(eachChildTree, attribute=eachAttribute, time=(getStrtRange,getEndRange), query=True, timeChange=True)
                                    values=cmds.keyframe(eachChildTree, attribute=eachAttribute, time=(getStrtRange,getEndRange), query=True, valueChange=True)
                                    for eachFrame, valueitem in map(None, frames, values):
                                        makeDict={eachFrame:valueitem}
                                        dirDict.update(makeDict)
                                    inp.write("<"+str(eachAttribute+";"))                                    
                                    inp.write(str(dirDict))
                                except:
                                    pass
                        except:
                            pass
                inp.close()   
                print "saved as "+fileName


        def save_att_function(self, collectItem, folderType):
            filterNode=["animCurve"]
            dirDict={}            
            notAttr=["isHierarchicalConnection", "fieldDistance", "dieOnEmissionVolumeExit", "solverDisplay", "isHierarchicalNode", "currentTime", "publishedNodeInfo", "fieldScale_Position"] 
            getStrtRange=cmds.playbackOptions(q=1, ast=1)#get framerange of scene to set keys in iteration
            getEndRange=cmds.playbackOptions(q=1, aet=1)#get framerange of scene to set keys in iteration            
            for each in collectItem:
                print "proceeding"
                # try:
                #     namer=each.split(":")[1]
                # except:
                namer=each
                fileName=folderType+'/'+namer+'.txt'
                print fileName
                inp=open(fileName, 'w+')                
                allChildren=cmds.listRelatives(each, ad=1)
                getChildren=allChildren
                try:
                    getChildren=[each]+getChildren
                except:
                    getChildren=[each]
                for eachChildTree in getChildren:
                    inp.write('\n'+str(eachChildTree)+">>")
                    getListedAttr=[(attrib) for attrib in listAttr (eachChildTree, w=1, a=1, s=1,u=1) if "solverDisplay" not in attrib]
                    for eachAttribute in getListedAttr:
                        try:
                            findFact=cmds.listConnections( eachChildTree+'.'+eachAttribute, d=False, s=True )
                            # findFact=[(eachConnected) for eachConnected in cmds.nodeType(ls_str[0].split(".")[0], i=1) for eachFilter in filterNode if eachConnected==eachFilter]
                            if findFact==None:
                                try:
                                    attrVal=cmds.getAttr(eachChildTree+"."+eachAttribute)
                                    inp.write("<"+str(eachAttribute+";"))
                                    makeDict={0.0:attrVal}
                                    inp.write(str(makeDict))
                                except:
                                    pass
                            else:
                                try:
                                    dirDict={}
                                    frames=cmds.keyframe(eachChildTree, attribute=eachAttribute, time=(getStrtRange,getEndRange), query=True, timeChange=True)
                                    values=cmds.keyframe(eachChildTree, attribute=eachAttribute, time=(getStrtRange,getEndRange), query=True, valueChange=True)
                                    for eachFrame, valueitem in map(None, frames, values):
                                        makeDict={eachFrame:valueitem}
                                        dirDict.update(makeDict)
                                    inp.write("<"+str(eachAttribute+";"))                                    
                                    inp.write(str(dirDict))
                                except:
                                    pass
                        except:
                            pass
                inp.close()   
                print "saved as "+fileName


        def save_setting_function(self, collectItem, folderType):
            filterNode=["animCurve"]
            dirDict={}            
            notAttr=["isHierarchicalConnection", "fieldDistance", "dieOnEmissionVolumeExit", "solverDisplay", "isHierarchicalNode", "currentTime", "publishedNodeInfo", "fieldScale_Position"] 
            getStrtRange=cmds.playbackOptions(q=1, ast=1)#get framerange of scene to set keys in iteration
            getEndRange=cmds.playbackOptions(q=1, aet=1)#get framerange of scene to set keys in iteration            
            for each in collectItem:
                print "proceeding"
                # try:
                #     namer=each.split(":")[1]+"_att"
                # except:
                namer=each+"_att"
                fileName=folderType+'/'+namer+'.txt'
                print fileName
                inp=open(fileName, 'w+')                
                allChildren=cmds.listRelatives(each, ad=1)
                getChildren=allChildren
                try:
                    getChildren=[each]+getChildren
                except:
                    getChildren=[each]
                for eachChildTree in getChildren:
                    inp.write('\n'+str(eachChildTree)+">>")
                    getListedAttr=[(attrib) for attrib in listAttr (eachChildTree, w=1, a=1, s=1,u=1) if "solverDisplay" not in attrib]
                    for eachAttribute in getListedAttr:
                        try:
                            findFact=cmds.listConnections( eachChildTree+'.'+eachAttribute, d=False, s=True )
                            # findFact=[(eachConnected) for eachConnected in cmds.nodeType(ls_str[0].split(".")[0], i=1) for eachFilter in filterNode if eachConnected==eachFilter]
                            if findFact==None:
                                try:
                                    attrVal=cmds.getAttr(eachChildTree+"."+eachAttribute)
                                    inp.write("<"+str(eachAttribute+";"))
                                    makeDict={0.0:attrVal}
                                    inp.write(str(makeDict))
                                except:
                                    pass
                            else:
                                try:
                                    dirDict={}
                                    frames=cmds.keyframe(eachChildTree, attribute=eachAttribute, time=(getStrtRange,getEndRange), query=True, timeChange=True)
                                    values=cmds.keyframe(eachChildTree, attribute=eachAttribute, time=(getStrtRange,getEndRange), query=True, valueChange=True)
                                    for eachFrame, valueitem in map(None, frames, values):
                                        makeDict={eachFrame:valueitem}
                                        dirDict.update(makeDict)
                                    inp.write("<"+str(eachAttribute+";"))                                    
                                    inp.write(str(dirDict))
                                except:
                                    pass
                        except:
                            pass
                inp.close()   
                print "saved as "+fileName






