import maya.cmds as cmds
from functools import partial
from string import *
import re, glob
import maya.mel
import os, subprocess, sys, platform
from os  import popen
from sys import stdin
from pymel.core import *
#import win32clipboard
import operator
OSplatform=platform.platform()

'''MG rigging modules'''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons License'
'http://creativecommons.org/licenses/by-sa/3.0/au/'


colour1=13
colour2=6
colour3=27  
pipelineguides="//usr//people//elise-d//maya//projects//default//data"
filepath= os.getcwd()

from inspect import getsourcefile
from os.path import abspath
getfilePath=str(abspath(getsourcefile(lambda _: None)))
print getfilePath
if "Windows" in OSplatform:
    gtepiece=getfilePath.split("\\")
if "Linux" in OSplatform: 
    gtepiece=getfilePath.split("/")  
# gtepiece=getfilePath.split("/")
print gtepiece
getRigModPath='/'.join(gtepiece[:-2])+"/rigModules"
print getRigModPath



# sys.path.append(str(filepath))
# getfilePath=str(__file__)
# gtepiece=getfilePath.split("\\")
# getRigModPath='\\'.join(gtepiece[:-2])+"\\rigmodules\\"

#filepath=( 'D:\\code\\git\\LiquidGit\\Liquid_egit\\guides\\' )

getScenePath=cmds.file(q=1, location=1)
getPathSplit=getScenePath.split("/")
folderPath='\\'.join(getPathSplit[:-1])+"\\"

sys.path.append(str(getRigModPath))
import baseFunctions_maya
reload (baseFunctions_maya)
getClass=baseFunctions_maya.BaseClass()

guideFolderPath=folderPath+"Guides\\"
infFolderPath=folderPath+"Influences\\"
xmlFolderPath=folderPath+"XMLskinWeights\\"
# filepath= os.getcwd()
# sys.path.append(str(filepath))
class GuideUI():
    '''--------------------------------------------------------------------------------------------------------------------------------------
    Interface Layout
    --------------------------------------------------------------------------------------------------------------------------------------'''          
    # def __init__(self, winName="rigGuides"):
    def create(self, arg=None):
        winName="rigGuides"
        self.winTitle = "rigGuides"
        self.winName = winName    
        if cmds.window(self.winName, exists=True):
                cmds.deleteUI(self.winName)

        self.window = cmds.window(self.winName, title=self.winTitle, tbm=1, w=300, h=300, bgc=[0.5, 0.45, 0.3] )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=290)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')

        cmds.rowLayout  (' rMainRow ', w=350, numberOfColumns=6, p='selectArrayRow')
        cmds.scrollLayout ('selectArrayColumn', parent = 'rMainRow',w=350, h=400 )
        cmds.setParent ('selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout',bgc=[0.7, 0.65, 0.5] , p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))


        cmds.frameLayout('Externalfiles', bgc=[0.15, 0.15, 0.15], cll=1, label='External Files', lv=1, nch=1, borderStyle='out', bv=1, w=345, fn="tinyBoldLabelFont", p='selectArrayColumn') 
        cmds.gridLayout('listBuildButtonLayout', p='Externalfiles', numberOfColumns=2, cellWidthHeight=(150, 20))               
        cmds.button (label='Save Guides',bgc=[0.9, 0.85, 0.7], p='listBuildButtonLayout', command = self.save_guides)
        cmds.button (label='Open Guides',bgc=[0.9, 0.85, 0.7], p='listBuildButtonLayout', command = self.open_guides)

        cmds.frameLayout('sep0', cll=1, bgc=[0.0, 0.0, 0.0], label='File/session', lv=0, nch=1, borderStyle='out', bv=5, p='selectArrayColumn')
        cmds.separator(h=1, p='sep0', bgc=[0.0, 0.0, 0.0]) 

        cmds.frameLayout('Templates', bgc=[0.15, 0.15, 0.15], cll=1, cl=0, label='Templates', lv=1, nch=1, borderStyle='out', bv=1, w=345, fn="tinyBoldLabelFont", p='selectArrayColumn') 
        cmds.gridLayout('TemplatesButtonLayout', p='Templates', numberOfColumns=2, cellWidthHeight=(150, 20))            
        cmds.button (label='Biped',bgc=[0.8, 0.75, 0.6], p='TemplatesButtonLayout', command = self.template_guides)
        cmds.button (label='Quad-w-Paw',bgc=[0.8, 0.75, 0.6], p='TemplatesButtonLayout', command = self.template_quad_toe_guides)
        cmds.button (label='Quad-w-Hoof',bgc=[0.8, 0.75, 0.6], p='TemplatesButtonLayout', command = self.template_quad_hoof_guides)
        cmds.frameLayout('sep1', cll=1, bgc=[0.0, 0.0, 0.0], label='File/session', lv=0, nch=1, borderStyle='out', bv=5, p='selectArrayColumn')
        cmds.separator(h=1, p='sep1', bgc=[0.0, 0.0, 0.0]) 

        cmds.frameLayout('PartialTemplates', bgc=[0.15, 0.15, 0.15], cll=1, cl=1, label='Partial Templates', lv=1, nch=1, borderStyle='out', bv=1, w=345, fn="tinyBoldLabelFont", p='selectArrayColumn') 
        cmds.gridLayout('PartialTemplatesButtonLayout', p='PartialTemplates', numberOfColumns=2, cellWidthHeight=(150, 20))      

        cmds.button (label='Paw', p='PartialTemplatesButtonLayout', command = self.template_toe_guides)
        cmds.button (label='Hoof', p='PartialTemplatesButtonLayout', command = self.template_hoof_guides)
        cmds.button (label='Arm Guides', p='PartialTemplatesButtonLayout', command = self.build_arm_guides)
        cmds.button (label='Q-Arm', p='PartialTemplatesButtonLayout', command = self.template_qarm_guides)
        cmds.button (label='Foot', p='PartialTemplatesButtonLayout', command = self.build_foot_guides)        
        cmds.button (label='Leg', p='PartialTemplatesButtonLayout', command = self.build_leg_guides)
        cmds.button (label='Neck', p='PartialTemplatesButtonLayout', command = self.build_neck_guides)
        cmds.button (label='Q-Spine', p='PartialTemplatesButtonLayout', command = self.template_quad_spine_guides)
        cmds.button (label='Spine', p='PartialTemplatesButtonLayout', command = self.build_spine_guides)
        cmds.button (label='Hand', p='PartialTemplatesButtonLayout', command = self.build_hand_guides)
        cmds.button (label='Tail', p='PartialTemplatesButtonLayout', command = self.build_tail_guides)    
        cmds.button (label='Previs face', p='PartialTemplatesButtonLayout', command = self.build_previs_face_guides)    
        cmds.button (label='Aface', p='PartialTemplatesButtonLayout', command = self.build_anim_face_guides)    

        cmds.frameLayout('sep2', cll=1, bgc=[0.0, 0.0, 0.0], label='File/session', lv=0, nch=1, borderStyle='out', bv=5, p='selectArrayColumn')
        cmds.separator(h=1, p='sep2', bgc=[0.0, 0.0, 0.0]) 

        cmds.frameLayout('Editting', bgc=[0.15, 0.15, 0.15], cll=1, cl=0, label='Editting', lv=1, nch=1, borderStyle='out', bv=1, w=345, fn="tinyBoldLabelFont", p='selectArrayColumn') 
        cmds.gridLayout('EdittingButtonLayout', p='Editting', numberOfColumns=2, cellWidthHeight=(150, 20))      
        cmds.button (label='Build Guide ',bgc=[0.8, 0.75, 0.6], p='EdittingButtonLayout', command = self.build_helper_guides)    
        cmds.button (label='Recreate Guides ',bgc=[0.8, 0.75, 0.6], p='EdittingButtonLayout', command = self._recreate_guide)                          
        cmds.button (label='Clean Guides ',bgc=[0.8, 0.75, 0.6], p='EdittingButtonLayout', command = self._clean_guide)                          
        cmds.text(label="" , bgc=[0.5, 0.45, 0.3])          
        cmds.text (label='Author: Elise Deglau',w=120, al='left', p='selectArrayColumn')
#         cmds.text (label='This work is licensed under a Creative Commons License', hl=1, w=300, al='left', p='selectArrayColumn')
#         cmds.text (label='http://creativecommons.org/licenses/by/4.0/', hl=1, w=350, al='left', p='selectArrayColumn')        
        cmds.showWindow(self.window) 

    def build_helper_guides(self, arg=None):
        Guide=getClass.makeGuide() 
    
    def _recreate_guide(self, arg=None):
        getJoints=[(each) for each in cmds.ls("*_jnt") if "IK" not in each and "FK" not in each and "Clst" not in each and "RFL" not in each]
#         getJoints=[(each) for each in getJoints if "RFL" not in each and "RT" not in each and "SH" not in each and "_L_" not in each and "Left" not in each or "heel" in each]
        getJoints=[(each) for each in getJoints if "Ctrl" not in each and "RFL" not in each and "RT" not in each and "SH" not in each and "_L_" not in each and "Left" not in each or "heel" in each]
        for each in getJoints:
            print each
            getName=each.split("|")[0]
            if "Eye" in each or "Lid" in each or "Chin" in each or "Jaw" in each:
                name=getName.split("_jnt")[0]+"_Ctrl_guide"
            else:
                name=getName.split("_jnt")[0]+"_guide"
            transformWorldMatrix, rotateWorldMatrix=getClass.locationXForm(each)
            getClass.guideBuild(name, transformWorldMatrix, rotateWorldMatrix, colour1, colour2, colour3)
#             Guide=getClass.makeguide_shapes(name, colour1, colour2, colour3)
#             cmds.move(transformWorldMatrix[0], transformWorldMatrix[1], transformWorldMatrix[2], Guide,r=1, rpr=1 )
#             cmds.rotate(transformWorldMatrix[0], transformWorldMatrix[1], transformWorldMatrix[2], Guide )  
    def _clean_guide(self, arg=None):
        getGuide=cmds.ls("*guide")
        for each in getGuide:
            cmds.delete(each)
            

    def build_arm_guides(self, arg=None):
        Ggrp=cmds.CreateEmptyGroup()
        cmds.rename(Ggrp, "Guides_Arm_grp")
        guideDict= {
                    'armcollarRight_guide':[-6.7072172366132268, 149.94747012321017, -9.8769280358770075],
                    'armelbowRight_guide':[-50.583802736485325, 143.78668591870758, -11.67773643630014],
                    'armshoulderRight_guide':[-18.763755961767572, 144.86111784853566, -9.8769280358770075],
                    'armwristRight_guide':[-75.951702321228368, 144.01692133224216, -11.322940637912122],
                    }
        for key, value in guideDict.items():
            Guide=getClass.makeguide_shapes(key, colour1, colour2, colour3)  
            cmds.move(value[0], value[1], value[2], Guide,r=1, rpr=1 )
            cmds.parent(key,"Guides_Arm_grp")


    def build_hand_guides(self, arg=None):
        Ggrp=cmds.CreateEmptyGroup()
        cmds.rename(Ggrp, "Guides_Hand_grp")
        guideDict= {
                    'armindexFingerBaseKnuckleRight_guide':[-88.253374121657814, 144.01692133224216, -7.0716275892342884],
                    'armindexFingerEndKnuckleRight_guide':[-96.290618960361471, 143.35236691979648, -7.0716275892342884],
                    'armindexFingerMidKnuckleRight_guide':[-93.413650637416396, 143.35236691979648, -7.0716275892342884],
                    'armindexFingerTipRight_guide':[-98.850100714499462, 143.35236691979648, -7.1793952420400977],
                    'armmidFingerBaseKnuckleRight_guide':[-88.886548405503433, 144.01692133224216, -9.6646270373640277],
                    'armmidFingerEndKnuckleRight_guide':[-98.293778159895197, 143.35236691979648, -9.9340461693785542],
                    'armmidFingerMidKnuckleRight_guide':[-94.868815870674894, 143.35236691979648, -9.7993366033712928],
                    'armmidFingerTipRight_guide':[-100.71855034802591, 143.35236691979648, -10.122639561788722],
                    'armpinkyFingerBaseKnuckleRight_guide':[-88.404129903525785, 144.01692133224216, -15.423497904721945],
                    'armpinkyFingerEndKnuckleRight_guide':[-95.254054481966421, 143.35236691979648, -15.477381731124852],
                    'armpinkyFingerMidKnuckleRight_guide':[-92.696749306015263, 143.35236691979648, -15.36961407831904],
                    'armpinkyFingerTipRight_guide':[-96.89751118725502, 143.35236691979648, -15.477381731124852],
                    'armringFingerBaseKnuckleRight_guide':[-88.993395740698645, 144.01692133224216, -12.498835736482585],
                    'armringFingerEndKnuckleRight_guide':[-96.802309760120934, 143.35236691979648, -12.76825486849711],
                    'armringFingerMidKnuckleRight_guide':[-94.245004584169777, 143.35236691979648, -12.57966147608694],
                    'armringFingerTipRight_guide':[-99.227081948251666, 143.35236691979648, -13.010732087310185],
                    'armthumbBaseKnuckleRight_guide':[-79.029845397717466, 143.78668591870755, -8.2973513374931596],
                    'armthumbEndKnuckleRight_guide':[-84.729818523215542, 142.61663694228434, -0.70693599450071609],
                    'armthumbMidKnuckleRight_guide':[-82.223142846937492, 143.09597967810379, -3.815302700885312],
                    'armthumbTipRight_guide':[-86.16136069503726, 142.61663694228434, 1.8731690826198053],
                    'armhandRight_guide':[-75.951702321228368, 144.01692133224216, -11.322940637912122]
                    }
        for key, value in guideDict.items():
            Guide=getClass.makeguide_shapes(key, colour1, colour2, colour3)  
            cmds.move(value[0], value[1], value[2], Guide,r=1, rpr=1 )
            cmds.parent(key,"Guides_Hand_grp")
            
    def build_foot_guides(self, arg=None):
        Ggrp=cmds.CreateEmptyGroup()
        cmds.rename(Ggrp, "Guides_Foot_grp")
        guideDict= {
                    'footankleRight_guide':[-10.36678446286045, 11.15333347932399, -6.8495026498425169],
                    'footballRight_guide':[-10.36678446286045, 0.0, 2.784463848434255],
                    'footheelLeft_guide':[10.366784462860448, 0.0, -12.528854659360343],
                    'footheelRight_guide':[-10.366784462860448, 0.0, -12.528854659360343],
                    'foottoeRight_guide':[-10.36678446286045, 0.0, 16.453363091522633],
                    }
        for key, value in guideDict.items():
            Guide=getClass.makeguide_shapes(key, colour1, colour2, colour3)  
            cmds.move(value[0], value[1], value[2], Guide,r=1, rpr=1 )
            cmds.parent(key,"Guides_Foot_grp")
            
    def build_leg_guides(self, arg=None):
        Ggrp=cmds.CreateEmptyGroup()
        cmds.rename(Ggrp, "Guides_Leg_grp")
        guideDict= {
                    'foottalusRight_guide':[-10.36678446286045, 11.15333347932399, -6.8495026498425169],
                    'legRight_guide':[-4.4218265670009682, 95.818461874681006, -8.4510633158422905],
                    'leghipRight_guide':[-10.367000000000001, 94.364926382303793, -8.2429837358801024],
                    'legkneeRight_guide':[-10.367000000000001, 53.329762969964527, -3.3604067424031392],
                    }
        for key, value in guideDict.items():
            Guide=getClass.makeguide_shapes(key, colour1, colour2, colour3)  
            cmds.move(value[0], value[1], value[2], Guide,r=1, rpr=1 )
            cmds.parent(key,"Guides_Leg_grp")

    def build_neck_guides(self, arg=None):
        Ggrp=cmds.CreateEmptyGroup()
        cmds.rename(Ggrp, "Guides_Neck_grp")
        guideDict= {
                    'head01_guide':[0.036888599395751953, 173.3537236310807, 1.4218314896285058],
                    'head02_guide':[0.036888599395751953, 193.90279273168952, -4.7428892405541339],                
                    'neck01_guide':[0.019192695907063816, 151.96837795130287, -19.920213708718613],
                    'neck02_guide':[-0.12042593955993654, 157.93266698080015, -10.722912705272485],
                    'neck03_guide':[-0.12042593955993654, 165.5462195313095, -5.6565674980466936],
                    }
        for key, value in guideDict.items():
            Guide=getClass.makeguide_shapes(key, colour1, colour2, colour3)  
            cmds.move(value[0], value[1], value[2], Guide,r=1, rpr=1 )
            #cmds.makeIdentity(key, a=True, t=1, s=1, r=1, n=0)
            cmds.parent(key,"Guides_Neck_grp")



    def build_spine_guides(self, arg=None):
        Ggrp=cmds.CreateEmptyGroup()
        cmds.rename(Ggrp, "Guides_Spine_grp")
        guideDict= {
                    'spine01_guide':[-0.0027999122373705276, 101.81306847273903, -12.802453296847265],
                    'spine02_guide':[-0.002799912237366739, 108.5464318918672, -14.738674607817812],
                    'spine03_guide':[-0.0027999122373669749, 113.58638894781204, -16.017880050963289],
                    'spine04_guide':[0.013779694044587801, 117.7259074130272, -18.154366850164259],
                    'spine05_guide':[0.013779694044602008, 122.0401413938731, -20.217515750401468],
                    'spine06_guide':[0.013779694044633962, 125.7192721232971, -21.368741829687444],
                    'spine07_guide':[0.041299145700635309, 130.33603197336751, -23.093919309815135],
                    'spine08_guide':[-0.0012049298241505538, 134.57698119414135, -23.567714955561129],
                    'spine09_guide':[-0.052538731083116019, 140.42369406499478, -22.999857579413948],
                    'spine10_guide':[-0.012650158967222359, 146.41747041660048, -21.545746695423997]}             
        for key, value in guideDict.items():
            Guide=getClass.makeguide_shapes(key, colour1, colour2, colour3)  
            cmds.move(value[0], value[1], value[2], Guide,r=1, rpr=1 )
            #cmds.makeIdentity(key, a=True, t=1, s=1, r=1, n=0)
            cmds.parent(key,"Guides_Spine_grp")
            
    def template_guides(self, arg=None):
        Ggrp=cmds.CreateEmptyGroup()
        cmds.rename(Ggrp, "Guides_Template_grp")
        guideDict= {
                    "BottomLid_R_Ctrl_guide":[-6.439449787139893, 117.65327276352865, 9.309892654418945],
                    "Chin_Ctrl_guide":[-9.844079613685608e-07, 108.55262266820495, 10.37376594543457],
                    "EyeOrient_R_Ctrl_guide":[-6.439449787139893, 120.22750245784006, 9.309892654418945],
                    "Eye_R_Ctrl_guide":[-4.32306182384491, 121.13178253173828, 2.3530614376068115],
                    "Jaw_Ctrl_guide":[-9.844079627033985e-07, 112.25226985464661, -0.5260112003405668],
                    "TopLid_R_Ctrl_guide":[-6.439449787139893, 122.92882094826075, 9.309892654418945],
                    "armcollarRight_guide":[-4.000204129346329, 98.14868024266529, -1.4915170577489343],
                    "armelbowRight_guide":[-27.96979121906894, 100.31671448221181, -1.3781118699151886],
                    "armhandRight_guide":[-44.278072192829406, 100.52519129711487, 0.4339435199957209],
                    "armindexFingerBaseKnuckleRight_guide":[-51.31276654667921, 100.81422557953606, 3.3354080991213717],
                    "armindexFingerEndKnuckleRight_guide":[-54.33125215856398, 100.49445756207844, 3.3938946952734987],
                    "armindexFingerMidKnuckleRight_guide":[-53.22483269639785, 100.62436655488632, 3.367506949413091],
                    "armindexFingerTipRight_guide":[-55.620125179772224, 100.58992129121117, 3.5130147344171077],
                    "armmidFingerBaseKnuckleRight_guide":[-51.42435867134522, 101.16000381684705, 1.868231449990775],
                    "armmidFingerEndKnuckleRight_guide":[-55.05199116197157, 100.69284149103098, 2.2102998893630716],
                    "armmidFingerMidKnuckleRight_guide":[-53.43162561164243, 100.86227837397776, 2.0404507332631256],
                    "armmidFingerTipRight_guide":[-56.61073784837662, 100.58010466415851, 2.4016016685291284],
                    "armpinkyFingerBaseKnuckleRight_guide":[-51.367361164754676, 100.77480501876202, -0.8371856985672759],
                    "armpinkyFingerEndKnuckleRight_guide":[-54.108770475051195, 100.48514803975034, -0.6561879948371419],
                    "armpinkyFingerMidKnuckleRight_guide":[-52.829785378401645, 100.63161004052444, -0.7435774685370196],
                    "armpinkyFingerTipRight_guide":[-55.159129915730226, 100.54999630653427, -0.5221116056200763],
                    "armringFingerBaseKnuckleRight_guide":[-51.22217504673055, 101.13775958277746, 0.45289991572560706],
                    "armringFingerEndKnuckleRight_guide":[-55.192052585812796, 100.66312426057047, 0.7066504430642577],
                    "armringFingerMidKnuckleRight_guide":[-53.46943183642533, 100.90260122174867, 0.5059079263955256],
                    "armringFingerTipRight_guide":[-56.27798268947977, 100.66096860386153, 0.9509476305879998],
                    "armshoulderRight_guide":[-7.930580232926842, 99.807, -1.4915059253714595],
                    "armthumbBaseKnuckleRight_guide":[-45.901228819328935, 100.25258586490192, 2.107380378206472],
                    "armthumbEndKnuckleRight_guide":[-48.13516914888813, 97.93331107099169, 5.593987356945003],
                    "armthumbMidKnuckleRight_guide":[-47.09182018549044, 99.12801436574917, 3.796950794496591],
                    "armthumbTipRight_guide":[-49.09803410746045, 97.23484128468061, 6.907571081342239],
                    "armwristRight_guide":[-44.278072192829406, 100.52519129711487, 0.4339435199957209],
                    "footankleRight_guide":[-6.335221188346742, 7.195998296499542, -6.278131192832437],
                    "footballRight_guide":[-6.454370027841123, 0.0, -0.9287533177042198],
                    "footheelLeft_guide":[6.454163114047583, 0.0, -9.252115930078556],
                    "footheelRight_guide":[-6.454370027841123, 0.0, -9.252097617512451],
                    "foottalusRight_guide":[-6.335221188346742, 7.195998296499542, -6.278131192832437],
                    "foottoeRight_guide":[-6.733316449954667, 0.0, 8.973008818311147],
                    "head01_guide":[9.103464176405105e-05, 107.33668938344094, -1.4877901823731514],
                    "head02_guide":[0.00010505583528281357, 143.1482556448036, -2.243470571302005],
                    "legRight_guide":[-3.1371477852210754, 74.55845158669612, -2.7330103698552333],
                    "leghipRight_guide":[-6.335127970741827, 72.99125979291045, -2.750407263257606],
                    "legkneeRight_guide":[-6.33517893323665, 40.6879347052273, -2.445020565863744],
                    "neck01_guide":[4.556780314743531e-05, 104.28619260556489, -1.211881912385235],
                    "spine01_guide":[0.0, 75.1327893865559, -2.49870591411967],
                    "spine02_guide":[0.0, 78.95319897483435, -1.3225079158160087],
                    "spine03_guide":[0.0, 82.72224266586177, -0.21952185384372935],
                    "spine04_guide":[0.0, 86.3720654418478, 0.1988720556919572],
                    "spine05_guide":[0.0, 89.95708526186003, 0.17683705284208084],
                    "spine06_guide":[0.0, 93.74887532652156, -0.06311212096350349],
                    "spine07_guide":[0.0, 97.52915120738277, -1.0099481470264298],
                    "spine08_guide":[0.0, 100.56825398222462, -1.0099481470264298],
#                     "tail01_guide":[-0.0027999122373705276, 139.32547412575613, -16.560473551717184]:[130.0, -0.0, 0.0],
#                     "tail02_guide":[-0.002799912237366739, 145.33790458485328, -21.309766579673866]:[118.00000000000001, -0.0, 0.0],
#                     "tail03_guide":[-0.002799912237352764, 147.48609880402128, -27.681829194440045]:[80.00000000000001, -0.0, 0.0],
#                     "tail04_guide":[0.013779694044602012, 144.6112987278719, -33.811153557044385]:[28.0, -0.0, 0.0],
#                     "tail05_guide":[0.013779694044616219, 137.8550774614288, -35.558003735930484]:[-2.0, 0.0, 0.0],
#                     "tail06_guide":[0.013779694044648173, 131.80802250930606, -34.73236280677202]:[-13.0, 0.0, 0.0],
#                     "tail07_guide":[0.04129914570064952, 124.32635626769634, -33.373627753726346]:[-14.000000000000002, 0.0, 0.0],
#                     "tail08_guide":[-0.0012049298241647646, 116.46887939679007, -31.94963107136564]:[-9.0, 0.0, 0.0],
#                     "tail09_guide":[-0.05253873108310181, 108.55659788887004, -31.67198885313664],
#                     "tail10_guide":[-0.012650158967208149, 101.1076785830534, -33.40694874609076]:[23.000000000000004, -0.0, 0.0],
                    }             
        for key, value in guideDict.items():
            Guide=getClass.makeguide_shapes(key, colour1, colour2, colour3)  
            cmds.move(value[0], value[1], value[2], Guide,r=1, rpr=1 )
            if "armthumbEndKnuckleRight" in key:
                    cmds.rotate(9.99999999999999, 237.00000000000003, 40.99999999999997, key)
            if "armthumbMidKnuckleRight" in key:
                    cmds.rotate(4.999999999999995, 221.99999999999997, 43.999999999999986, key)
            if "armthumbTipRight" in key:
                    cmds.rotate(-15.999999999999995, 65.99999999999999, 32.999999999999986, key)           
            #cmds.makeIdentity(key, a=True, t=1, s=1, r=1, n=0)
            cmds.parent(key,"Guides_Template_grp")
    def template_quad_toe_guides(self, arg=None):
        Ggrp=cmds.CreateEmptyGroup()
        cmds.rename(Ggrp, "Guides_Template_grp")
        guideDict= {
                    "BottomLid_R_Ctrl_guide":[-4.312976837158203, 28.415931701660156, 16.51548194885254, 0.0, -0.0, 0.0],
                    "Chin_Ctrl_guide":[0.0, 22.47719383239746, 18.62457275390625, 0.0, -0.0, 0.0],
                    "EyeOrient_R_Ctrl_guide":[-4.374000072479248, 30.205890655517578, 16.379894256591797, 0.0, -0.0, 0.0],
                    "Eye_R_Ctrl_guide":[-3.7920114547014236, 29.788776397705078, 12.98980188369751, 0.0, -0.0, 0.0],
                    "Jaw_Ctrl_guide":[0.0, 23.303964594667914, 9.262282735509427, 0.0, -0.0, 0.0],
                    "TopLid_R_Ctrl_guide":[-4.388728141784668, 31.996784210205078, 16.197351455688477, 0.0, -0.0, 0.0],
                    "anklefrontRight_guide":[-5.0, 3.1118345297879775, 8.047503453420148, 0.0, -0.0, 0.0],
                    "anklerearRight_guide":[-5.0, 3.0970688461279243, -8.513027336231843, 0.0, -0.0, 0.0],
                    "armcollarRight_guide":[-3.089627453372503, 18.587303670001095, 7.285996154876258, 0.0, -0.0, 79.0],
                    "armelbowRight_guide":[-5.0, 7.913475345259108, 6.523239359103034, 0.0, 0.0, -7.000000000000002],
                    "armshoulderRight_guide":[-5.0, 14.021601789305993, 7.37196049886393, 0.0, 0.0, -3.000000000000001],
                    "armwristRight_guide":[-5.0, 3.1118345297879775, 8.047503453420148, 0.0, -0.0, 0.0],
                    "foottalusRight_guide":[-5.0, 3.0970688461279243, -8.513027336231843, 0.0, -0.0, 0.0],
                    "head01_guide":[0.0, 21.661623001098633, 8.568779945373535, -127.00000000000001, 0.0, 0.0],
                    "head02_guide":[0.0, 38.46185302734375, 6.802534103393555, 0.0, -0.0, 0.0],
                    "heelfrontLeft_guide":[5.0, 2.465190328815662e-31, 7.51108154717235, 0.0, -0.0, 0.0],
                    "heelfrontRight_guide":[-5.0, 2.465190328815662e-31, 7.51108154717235, 0.0, -0.0, 0.0],
                    "heelrearLeft_guide":[5.0, 2.465190328815662e-31, -10.650904482274765, 0.0, -0.0, 0.0],
                    "heelrearRight_guide":[-5.0, 2.465190328815662e-31, -10.650904482274765, 0.0, -0.0, 0.0],
                    "legRight_guide":[-5.0, 15.403244833047285, -7.06433088383838, 0.0, -0.0, 0.0],
                    "leghipRight_guide":[-5.000000000000001, 10.892456095597892, -6.354492014588729, 0.0, -0.0, 0.0],
                    "legkneeRight_guide":[-5.0, 8.42174149755165, -10.498079514765895, 0.0, -0.0, 0.0],
                    "neck01_guide":[0.0, 20.0, 8.0, 9.0, -0.0, 0.0],
                    "neck02_guide":[0.0, 21.661623001098633, 8.568779945373535, 106.0, -0.0, 0.0],
                    "neck07_guide":[0.0, 21.661623001098633, 8.568779945373535, -127.00000000000001, 0.0, 0.0],
                    "spine01_guide":[0.0, 18.68492637166078, -7.463167718021331, 124.0, -0.0, 0.0],
                    "spine02_guide":[0.0, 17.699004311867505, -5.429869673438407, 110.0, -0.0, 0.0],
                    "spine03_guide":[0.0, 17.082617779839456, -3.4186441510700334, 106.0, -0.0, 0.0],
                    "spine04_guide":[0.0, 16.68423733122612, -1.280643028345716, 88.0, -0.0, 0.0],
                    "spine05_guide":[0.0, 16.717738812519286, 1.0578541389575156, 91.0, -0.0, 0.0],
                    "spine06_guide":[0.0, 17.10131708087264, 3.7081083023785806, 66.0, -0.0, 0.0],
                    "spine07_guide":[0.0, 17.89655499239929, 5.7251174566241305, 53.00000000000001, -0.0, 0.0],
                    "spine08_guide":[0.0, 20.0, 8.0, 9.0, -0.0, 0.0],
                    "tail01_guide":[0.0, 21.258071899414062, -8.342629432678223, 119.0, -0.0, 0.0],
                    "tail02_guide":[0.0, 22.641915198560646, -11.077921056166275, 91.0, -0.0, 0.0],
                    "tail03_guide":[0.0, 23.631355276591528, -14.867601204659916, 93.00000000000001, -0.0, 0.0],
                    "tail04_guide":[0.0, 23.88710681850392, -18.582714047929795, 87.00000000000001, -0.0, 0.0],
                    "tail05_guide":[0.0, 23.888545429894087, -22.01705648477851, 88.0, -0.0, 0.0],
                    "tail06_guide":[0.0, 23.889408772051553, -25.18929078794835, 88.0, -0.0, 0.0],
                    "tail07_guide":[0.0, 23.889408772051553, -29.06369612001063, 91.0, -0.0, 0.0],
                    "toeTipFrontRight_guide":[-4.999999795034595, 1.0373128559286908e-14, 14.985817311891347, 0.0, -0.0, 0.0],
                    "toeTipRearRight_guide":[-5.000000000000002, -3.810384843470966e-15, -3.1231798833917024, 0.0, -0.0, 0.0],
                    "toefrontRight_guide":[-4.999999867018048, 8.881784197001252e-15, 11.627608356667464, 0.0, -0.0, 0.0],
                    "toerearRight_guide":[-5.082752227783203, 0.026624999940395355, -6.458255767822266, 0.0, -0.0, 0.0],
                    }             
        for key, value in guideDict.items():
            Guide=getClass.makeguide_shapes(key, colour1, colour2, colour3)  
            cmds.move(value[0], value[1], value[2], Guide,r=1, rpr=1 )
            cmds.rotate(value[3], value[4], value[5], Guide )       
            #cmds.makeIdentity(key, a=True, t=1, s=1, r=1, n=0)
            cmds.parent(key,"Guides_Template_grp")
            
    def template_quad_hoof_guides(self, arg=None):
        Ggrp=cmds.CreateEmptyGroup()
        cmds.rename(Ggrp, "Guides_Template_grp")
        guideDict= {
                    "BottomLid_R_Ctrl_guide":[-10.345947665688616, 154.62057594844183, 87.52932618542728, 0.0, -0.0, 0.0],
                    "Chin_Ctrl_guide":[-9.844079897902702e-07, 126.43277550564268, 105.19492052994094, 0.0, -0.0, 0.0],
                    "EyeOrient_R_Ctrl_guide":[-10.345947665688616, 158.98675035299377, 87.52932618542728, 0.0, -0.0, 0.0],
                    "Eye_R_Ctrl_guide":[-6.8228936639266, 158.4088897705078, 77.61321204395729, 0.0, -0.0, 0.0],
                    "Jaw_Ctrl_guide":[-9.84407991125108e-07, 135.8019856686587, 89.80186081587338, 0.0, -0.0, 0.0],
                    "TopLid_R_Ctrl_guide":[-10.345947665688616, 164.18014441989737, 87.74424623531327, 0.0, -0.0, 0.0],
                    "anklefrontRight_guide":[-14.70997426726339, 12.845521710752848, 36.098380761477124, 0.0, -0.0, 0.0],
                    "anklerearRight_guide":[-14.825695393086242, 13.021493845700569, -37.19130571392873, 0.0, -0.0, 0.0],
                    "armcollarRight_guide":[-14.70997426726322, 92.68234207015746, 27.547325179065517, 0.0, -0.0, 79.0],
                    "armelbowRight_guide":[-14.609741513227979, 38.71696360045209, 38.19959807521909, 0.0, 0.0, -7.000000000000002],
                    "armshoulderRight_guide":[-14.709974267263163, 79.31792899396093, 34.35970107793036, 0.0, 0.0, -3.000000000000001],
                    "armwristRight_guide":[-14.70997426726339, 12.845521710752848, 36.098380761477124, 0.0, -0.0, 0.0],
                    "foottalusRight_guide":[-14.825695393086242, 13.021493845700569, -37.19130571392873, 0.0, -0.0, 0.0],
                    "head01_guide":[0.036888599395780375, 144.11617158434336, 64.24948161217213, -127.00000000000001, 0.0, 0.0],
                    "head02_guide":[0.03688859939572353, 179.8652390605068, 75.74668603498378, 0.0, -0.0, 0.0],
                    "heelfrontLeft_guide":[14.709974267263398, 0.0, 31.081703401625113, 0.0, 180.0, 0.0],
                    "heelfrontRight_guide":[-14.709974267263396, 0.0, 31.081703401625113, 0.0, -0.0, 0.0],
                    "heelrearLeft_guide":[14.709974267263402, 0.0, -44.55302582227539, 0.0, 180.0, 0.0],
                    "heelrearRight_guide":[-14.709974267263402, 0.0, -44.55302582227539, 0.0, -0.0, 0.0],
                    "legRight_guide":[-14.826, 92.54541214992332, -33.88014194665299, 0.0, -0.0, 0.0],
                    "leghipRight_guide":[-14.825910930225792, 75.19695820649581, -26.088312543247913, 0.0, -0.0, 0.0],
                    "legkneeRight_guide":[-15.046664650175586, 44.283251815515364, -45.658280108504016, 0.0, -0.0, 0.0],
                    "neck01_guide":[-0.05253873108311602, 100.67881686971084, 31.21677618922334, 59.00000000000001, -0.0, 0.0],
                    "neck02_guide":[-0.05253873108311602, 105.5849137246376, 38.992697032464726, 107.0, -0.0, 0.0],
                    "neck03_guide":[-0.05253873108311602, 113.32232598989702, 45.13683248497903, 35.0, -0.0, 0.0],
                    "neck04_guide":[-0.05253873108311602, 121.71430835017541, 49.80445416625082, 32.0, -0.0, 0.0],
                    "neck05_guide":[-0.05253873108311602, 129.61927413464446, 53.09650450537797, 14.000000000000002, -0.0, 0.0],
                    "neck06_guide":[-0.05253873108311602, 136.844349197958, 56.516155068946574, 32.0, -0.0, 0.0],
                    "neck07_guide":[0.036888599395780375, 144.11617158434336, 64.24948161217213, -127.00000000000001, 0.0, 0.0],
                    "spine01_guide":[-0.0027999122373705276, 98.7795002943503, -32.30058592130949, 124.0, -0.0, 0.0],
                    "spine02_guide":[-0.002799912237366739, 97.550927562225, -23.787227952036204, 107.0, -0.0, 0.0],
                    "spine03_guide":[-0.002799912237366975, 95.2090883369707, -15.576522023738733, 107.0, -0.0, 0.0],
                    "spine04_guide":[0.0137796940445878, 93.13185505468658, -5.839827301817629, 88.0, -0.0, 0.0],
                    "spine05_guide":[0.013779694044602008, 92.76580235044054, 2.064750367812266, 91.0, -0.0, 0.0],
                    "spine06_guide":[0.013779694044633962, 94.1352587515801, 11.06260290691969, 86.0, -0.0, 0.0],
                    "spine07_guide":[0.04129914570063531, 95.69285771433076, 20.40892586483784, 74.0, -0.0, 0.0],
                    "spine08_guide":[-0.05253873108311602, 100.67881686971084, 31.21677618922334, 59.00000000000001, -0.0, 0.0],
                    "tail01_guide":[-0.0027999122373705276, 108.33859011538082, -47.297604842005825, 119.0, -0.0, 0.0],
                    "tail02_guide":[-0.002799912237366739, 108.77489783494201, -56.20451049135762, 91.0, -0.0, 0.0],
                    "tail03_guide":[-0.0027999122373243424, 108.34463696522515, -64.69882953679877, 93.00000000000001, -0.0, 0.0],
                    "tail04_guide":[0.013779694044630433, 107.78995184903675, -74.60612566488922, 87.00000000000001, -0.0, 0.0],
                    "tail05_guide":[0.013779694044616219, 107.83050491098442, -83.58211579947252, 88.0, -0.0, 0.0],
                    "tail06_guide":[0.013779694044648173, 107.75495222926028, -94.36210837970947, 88.99999999999999, -0.0, 0.0],
                    "tail07_guide":[0.04129914570064952, 107.41012946609311, -104.52986342434481, 91.0, -0.0, 0.0],
                    "toefrontRight_guide":[-14.709974267263394, 0.0, 48.64282038139009, 0.0, -0.0, 0.0],
                    "toerearRight_guide":[-14.7099742672634, 0.0, -27.51874235190337, 0.0, -0.0, 0.0],
                    }             
        for key, value in guideDict.items():
            Guide=getClass.makeguide_shapes(key, colour1, colour2, colour3)  
            cmds.move(value[0], value[1], value[2], Guide,r=1, rpr=1 )
            cmds.rotate(value[3], value[4], value[5], Guide)       
            #cmds.makeIdentity(key, a=True, t=1, s=1, r=1, n=0)
            cmds.parent(key,"Guides_Template_grp")
            
    def template_hoof_guides(self, arg=None):
        Ggrp=cmds.CreateEmptyGroup()
        cmds.rename(Ggrp, "Guides_Template_grp")
        guideDict= {
                    "anklefrontRight_guide":[-5.0, 3.1118345297879775, 8.047503453420148, 0.0, -0.0,  0.0],
                    "anklerearRight_guide":[-5.0, 3.0970688461279243, -8.513027336231843, 0.0, -0.0,  0.0],
                    "armwristRight_guide":[-5.0, 3.1118345297879775, 8.047503453420148, 0.0, -0.0,  0.0],
                    "foottalusRight_guide":[-5.0, 3.0970688461279243, -8.513027336231843, 0.0, -0.0,  0.0],
                    "heelfrontLeft_guide":[5.0, 2.465190328815662e-31, 7.51108154717235, 0.0, -0.0,  0.0],
                    "heelfrontRight_guide":[-5.0, 2.465190328815662e-31, 7.51108154717235, 0.0, -0.0,  0.0],
                    "heelrearLeft_guide":[5.0, 2.465190328815662e-31, -10.650904482274765, 0.0, -0.0,  0.0],
                    "heelrearRight_guide":[-5.0, 2.465190328815662e-31, -10.650904482274765, 0.0, -0.0,  0.0],
                    "toeTipFrontRight_guide":[-4.999999795034595, 1.0373128559286908e-14, 14.985817311891347, 0.0, -0.0,  0.0],
                    "toeTipRearRight_guide":[-5.000000000000002, -3.810384843470966e-15, -3.1231798833917024, 0.0, -0.0,  0.0],
                    "toefrontRight_guide":[-4.999999867018048, 8.881784197001252e-15, 11.627608356667464, 0.0, -0.0,  0.0],
                    "toerearRight_guide":[-5.082752227783203, 0.026624999940395355, -6.458255767822266, 0.0, -0.0,  0.0],
                    }             
        for key, value in guideDict.items():
            Guide=getClass.makeguide_shapes(key, colour1, colour2, colour3)  
            cmds.move(value[0], value[1], value[2], Guide,r=1, rpr=1 )
            cmds.rotate(value[3], value[4], value[5], Guide)       
            #cmds.makeIdentity(key, a=True, t=1, s=1, r=1, n=0)
            cmds.parent(key,"Guides_Template_grp")
            
    def template_qarm_guides(self, arg=None):
        Ggrp=cmds.CreateEmptyGroup()
        cmds.rename(Ggrp, "Guides_Template_grp")
        guideDict= {
                    "anklefrontRight_guide":[-5.0, 3.1118345297879775, 8.047503453420148, 0.0, -0.0, 0.0],
                    "armcollarRight_guide":[-3.089627453372503, 18.587303670001095, 7.285996154876258, 0.0, -0.0, 79.0],
                    "armelbowRight_guide":[-5.0, 7.913475345259108, 6.523239359103034, 0.0, 0.0, -7.000000000000002],
                    "armshoulderRight_guide":[-5.0, 14.021601789305993, 7.37196049886393, 0.0, 0.0, -3.000000000000001],
                    "armwristRight_guide":[-5.0, 3.1118345297879775, 8.047503453420148, 0.0, -0.0, 0.0],
                    }             
        for key, value in guideDict.items():
            Guide=getClass.makeguide_shapes(key, colour1, colour2, colour3)  
            cmds.move(value[0], value[1], value[2], Guide,r=1, rpr=1 )
            cmds.rotate(value[3], value[4], value[5], Guide)       
            #cmds.makeIdentity(key, a=True, t=1, s=1, r=1, n=0)
            cmds.parent(key,"Guides_Template_grp")
            
    def template_toe_guides(self, arg=None):
        Ggrp=cmds.CreateEmptyGroup()
        cmds.rename(Ggrp, "Guides_Template_grp")
        guideDict= {
                    "anklefrontRight_guide":[-5.0, 3.1118345297879775, 8.047503453420148, 0.0, -0.0, 0.0],
                    "anklerearRight_guide":[-5.0, 3.0970688461279243, -8.513027336231843, 0.0, -0.0, 0.0],
                    "armwristRight_guide":[-5.0, 3.1118345297879775, 8.047503453420148, 0.0, -0.0, 0.0],
                    "foottalusRight_guide":[-5.0, 3.0970688461279243, -8.513027336231843, 0.0, -0.0, 0.0],
                    "heelfrontLeft_guide":[5.0, 2.465190328815662e-31, 7.51108154717235, 0.0, -0.0, 0.0],
                    "heelfrontRight_guide":[-5.0, 2.465190328815662e-31, 7.51108154717235, 0.0, -0.0, 0.0],
                    "heelrearLeft_guide":[5.0, 2.465190328815662e-31, -10.650904482274765, 0.0, -0.0, 0.0],
                    "heelrearRight_guide":[-5.0, 2.465190328815662e-31, -10.650904482274765, 0.0, -0.0, 0.0],
                    "toeTipFrontRight_guide":[-4.999999795034595, 1.0373128559286908e-14, 14.985817311891347, 0.0, -0.0, 0.0],
                    "toeTipRearRight_guide":[-5.000000000000002, -3.810384843470966e-15, -3.1231798833917024, 0.0, -0.0, 0.0],
                    "toefrontRight_guide":[-4.999999867018048, 8.881784197001252e-15, 11.627608356667464, 0.0, -0.0, 0.0],
                    "toerearRight_guide":[-5.082752227783203, 0.026624999940395355, -6.458255767822266, 0.0, -0.0, 0.0],
                    }             
        for key, value in guideDict.items():
            Guide=getClass.makeguide_shapes(key, colour1, colour2, colour3)  
            cmds.move(value[0], value[1], value[2], Guide,r=1, rpr=1 )
            cmds.rotate(value[3], value[4], value[5], Guide)       
            #cmds.makeIdentity(key, a=True, t=1, s=1, r=1, n=0)
            cmds.parent(key,"Guides_Template_grp")
    def template_quad_spine_guides(self, arg=None):
        Ggrp=cmds.CreateEmptyGroup()
        cmds.rename(Ggrp, "Guides_Template_grp")
        guideDict= {
                    "spine01_guide":[0.0, 18.68492637166078, -7.463167718021331, 124.0, -0.0, 0.0],
                    "spine02_guide":[0.0, 17.699004311867505, -5.429869673438407, 110.0, -0.0, 0.0],
                    "spine03_guide":[0.0, 17.082617779839456, -3.4186441510700334, 106.0, -0.0, 0.0],
                    "spine04_guide":[0.0, 16.68423733122612, -1.280643028345716, 88.0, -0.0, 0.0],
                    "spine05_guide":[0.0, 16.717738812519286, 1.0578541389575156, 91.0, -0.0, 0.0],
                    "spine06_guide":[0.0, 17.10131708087264, 3.7081083023785806, 66.0, -0.0, 0.0],
                    "spine07_guide":[0.0, 17.89655499239929, 5.7251174566241305, 53.000000000000014, -0.0, 0.0],
                    }             
        for key, value in guideDict.items():
            Guide=getClass.makeguide_shapes(key, colour1, colour2, colour3)  
            cmds.move(value[0], value[1], value[2], Guide,r=1, rpr=1 )
            cmds.rotate(value[3], value[4], value[5], Guide)       
            #cmds.makeIdentity(key, a=True, t=1, s=1, r=1, n=0)
            cmds.parent(key,"Guides_Template_grp")
            
            

    def save_guides(self, arg=None):  
        winName = "Save guides filename"
        winTitle = winName
        global fileName
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)

        window = cmds.window(winName, title=winTitle, tbm=1, w=250, h=200 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=250)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        
        cmds.rowLayout  (' rMainRow ', w=250, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=1, cellWidthHeight=(200, 20))    
        fileName=cmds.textField(w=200, h=25, p='listBuildButtonLayout')    
        cmds.button (label='SaveInProject', p='listBuildButtonLayout', command = lambda *args:self._save_guide_function())
        cmds.button (label='SaveInPipelineGuides', p='listBuildButtonLayout', command = lambda *args:self._save_to_pipeline())        
        cmds.button (label='Open folder', p='listBuildButtonLayout', command = lambda *args:self._launch_exp_open(guideFolderPath))
        cmds.showWindow(window)            

    def _launch_exp_save(self, folderPath):
        destImagePath=cmds.textField(fileName, q=1, text=True)
        print destImagePath
        self.get_path(destImagePath)    
        
    def get_path(self, path):
        print path
        if '\\\\' in path:
            newpath=re.sub(r'\\\\',r'\\', path)
            print newpath
            os.startfile(r'\\'+newpath[1:])    
        else:
            os.startfile(path)
                     
    def _save_guide_function(self):
        fileSavePath=cmds.file(q=1, location=1)
        getPath= '/'.join(fileSavePath.split('/')[:-1])+'/'
        print getPath+" file save path"
        if fileSavePath =="unknown":
            print "This file has not been saved into a location yet. Cannot determine where you want to put this."
            return
        else:
            pass        
        filename=cmds.textField(fileName, q=1, text=True)
        print filename
        if filename:
            pass
        else:
            print "you need to give it a name"
            return   
        if "Windows" in OSplatform:
            printFolder=getPath+filename+".txt"
            if not os.path.exists(printFolder): os.makedirs(printFolder) 
        if "Linux" in OSplatform:
            printFolder=getPath+filename+".txt"   
            if not os.path.exists(printFolder):open(printFolder, 'w')
        self.guide_writer(printFolder)
        
    def _save_to_pipeline(self):
        filename=cmds.textField(fileName, q=1, text=True)
        if filename:
            pass
        else:
            print "you need to give it a name"
            return    
        printFolder=pipelineguides+filename+".txt"
        self.guide_writer(printFolder)
        
    def guide_writer(self, printFolder):
        getGuides=cmds.ls("*_guide")
        inp=open(printFolder, 'w+')
        for each in getGuides:
            transform=cmds.xform(each , q=True, ws=1, t=True)
            if transform==[0, 0, 0]:
                transformWorldMatrix = cmds.xform(each, q=True, wd=1, sp=True)  
                rotateWorldMatrix = cmds.xform(each, q=True, wd=1, ra=True) 
                scaleWorldMatrix = cmds.xform(each, q=True, s=True) 
            else:
                transformWorldMatrix = cmds.xform(each, q=True, wd=1, t=True)  
                rotateWorldMatrix = cmds.xform(each, q=True, wd=1, ro=True) 
                scaleWorldMatrix = cmds.xform(each, q=True, s=True) 
                print str(each)+":"+str(transformWorldMatrix)+":"+str(rotateWorldMatrix)+":"+str(scaleWorldMatrix)
            inp=open(printFolder, 'a+')
            getName=each.split("|")[0]
            inp.write(str(getName)+":"+str(transformWorldMatrix)+":"+str(rotateWorldMatrix)+":"+str(scaleWorldMatrix)+'\r\n')
        inp.close()  
        print "saved as "+printFolder
        
        #open file function
        if '\\\\' in printFolder:
            newpath=re.sub(r'\\\\',r'\\', printFolder)
            os.startfile(r'\\'+newpath[1:])    
        else:
            os.startfile(printFolder)
                        
    def open_guides(self, arg=None):    
        if guideFolderPath:
            pathFolder=guideFolderPath
            getPath=guideFolderPath+"*.*"
        else:
            getPath=folderPath+"*.*"
            pathFolder=folderPath
        print pathFolder
        files=glob.glob(getPath)   
        makeBucket=[] 
        for each in files:
            getfileName=each.split("\\")
            getFile=getfileName[-1:][0]
            makeBucket.append(getFile)
        winName = "Open guides filename"
        winTitle = winName
        global fileName
#         global fileSaveName
        global fileDropName
        openFolderPath=folderPath+"\\"
#         files=glob.glob(getPath)       
        if cmds.window(winName, exists=True):
                cmds.deleteUI(winName)

        window = cmds.window(winName, title=winTitle, tbm=1, w=500, h=280 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=500)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        
        cmds.rowLayout  (' rMainRow ', w=500, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=1, cellWidthHeight=(480, 20))      
        fileDropName=cmds.optionMenu( label='files')
        for each in makeBucket:
            cmds.menuItem( label=each) 
        fileName=cmds.textField(w=120, h=25, p='listBuildButtonLayout')    
        cmds.button (label='refresh', p='listBuildButtonLayout', command = lambda *args:self._refresh_function())
        cmds.button (label='PipelineGuides', p='listBuildButtonLayout', command = lambda *args:self._pipeline_guides())
        cmds.button (label='Open', p='listBuildButtonLayout', command = lambda *args:self._open_guide_function())
        cmds.button (label='Open folder', p='listBuildButtonLayout', command = lambda *args:self._launch_exp_open(openFolderPath))
        cmds.showWindow(window)                 
    def _launch_exp_open(self, folderPath):
#         os.system('explorer'+folderPath)
        destImagePath=cmds.textField(fileName, q=1, text=True)
#         destImagePath=folderPath
        print destImagePath
        self.get_path(destImagePath)            
#         result = cmds.promptDialog( 
#                     title='Confirm', 
#                     message='open file', 
#                     button=['Continue','Cancel'],
#                     defaultButton='Continue', 
#                     cancelButton='Cancel', 
#                     dismissString='Cancel' )
#         if result == 'Continue':
#             filename=cmds.promptDialog(q=1)

    def _refresh_function(self):
        fileTextname=cmds.textField(fileName, q=1, text=True)
        fileTextname=fileTextname+"\\*.txt"
        files=glob.glob(fileTextname)
        makeBucket=[] 
        for each in files:
            getfileName=each.split("\\")
            getFile=getfileName[-1:][0]
            makeBucket.append(getFile)        
        cmds.optionMenu(fileDropName, e=1)
        for each in makeBucket:
            cmds.menuItem( label=each)
    def _pipeline_guides(self):
        fileTextname=pipelineguides+"\\*.txt"
        cmds.textField(fileName, edit=True, text=pipelineguides)
        files=glob.glob(fileTextname)
        makeBucket=[] 
        for each in files:
            getfileName=each.split("\\")
            getFile=getfileName[-1:][0]
            makeBucket.append(getFile)        
        cmds.optionMenu(fileDropName, e=1)
        for each in makeBucket:
            cmds.menuItem( label=each)        
        
    def _open_guide_function(self):   
        guideDict={}
        getPath=cmds.textField(fileName, q=1, text=True)
        if getPath:
            pass
        else:
            print "no path entered"
            return
        try:
            filename=cmds.optionMenu(fileDropName, q=1, v=1)
            printFolder=getPath+"\\"+filename
        except:
            if "\\" in getPath:
                filename=getPath.split("\\")[-1:][0]
            elif "/" in getPath:
                filename=getPath.split("/")[-1:][0]        
            printFolder=getPath
#         if fileSaveName:
#             printFolder=fileSaveName
#         else:
#             printFolder=folderPath+filename
        Ggrp=cmds.CreateEmptyGroup()
        getName=filename.split(".")[0]
        cmds.rename(Ggrp, "Guides_"+getName+"_grp")
        inp=open(printFolder, 'r')
        
        List = open(printFolder).readlines()
        
        for each in List:
            newlocbucket=[]
            newrotbucket=[]    
            newsclbucket=[]    
            getDictParts=each.split(':')
            print len(getDictParts)
            getlocpart=getDictParts[1].strip('[]')
            getlocpart=getlocpart.split(', ')
            for item in getlocpart:
                newlocbucket.append(item)
            if len(getDictParts)==3:
                getrotpart=getDictParts[2].strip('[]]\r\n')
                getrotpart=getrotpart.split(', ')
                for item in getrotpart:
                    getit=item.split('.')
                    getint=int(getit[0])
                    newrotbucket.append(getint)
                newlocbucket.append(newrotbucket)
            if len(getDictParts)==4:
                getrotpart=getDictParts[2].strip('[]')
                getrotpart=getrotpart.split(', ')
                for item in getrotpart:
                    getit=item.split('.')
                    getint=int(getit[0])
                    newrotbucket.append(getint)
                newlocbucket.append(newrotbucket)
                getsclpart=getDictParts[3].strip('[]]\r\n')
                getsclpart=getsclpart.split(', ')
                for item in getsclpart:
                    getit=item.split('.')
                    getint=int(getit[0])
                    newsclbucket.append(getint)
                newlocbucket.append(newsclbucket)
            makeDict={getDictParts[0]:newlocbucket}
            guideDict.update(makeDict)
                           
        for key, value in guideDict.items():
            key=key.split("|")[-1:][0]
            getName=key.split("|")[0]
#             print getName
#             colour1, colour2, colour3=17, 17, 17
            if len(value)==5:
                scaleWorldMatrix=value[-1:][0]
                transformWorldMatrix, rotateWorldMatrix=[value[0], value[1], value[2]], value[3]
            elif len(value)==4:
                transformWorldMatrix, rotateWorldMatrix=[value[0], value[1], value[2]], value[3]
            else:
                transformWorldMatrix=value[0], value[1], value[2]
            try:
                getClass.guideBuild(getName, transformWorldMatrix, rotateWorldMatrix, colour1, colour2, colour3)
                if scaleWorldMatrix:
                    cmds.scale(scaleWorldMatrix[0], scaleWorldMatrix[1],scaleWorldMatrix[2], getName)
                else:
                    pass
                cmds.parent(getName, "Guides_"+getName+"_grp")
            except:
                pass
            getDeleted=cmds.ls("*_guide1")
            for each in getDeleted:
                cmds.delete(each) 

    def build_tail_guides(self, arg=None):
        axisList=["X", "Y", "Z"]  
        winName = "create tail guides"
        winTitle = winName
        if cmds.window(winName, exists=True):
                deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=350, h=150 )
        menuBarLayout(h=30)
        rowColumnLayout  (' selectArrayRow ', nr=1, w=350)
        frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')      
        rowLayout  (' rMainRow ', w=350, numberOfColumns=6, p='selectArrayRow')
        columnLayout ('selectArrayColumn', parent = 'rMainRow')
        setParent ('selectArrayColumn')
        separator(h=10, p='selectArrayColumn')
        gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))
        direction=optionMenu( label='Axis')
        for each in axisList:
            menuItem( label=each)         
        cmds.text(label="", w=80, h=25)            
        cmds.text(label="name", w=80, h=25)             
        self.namefield=cmds.textField(w=40, h=25, p='listBuildButtonLayout', text="name")          
        cmds.text(label="amount", w=80, h=25) 
        self.amount=cmds.textField(w=40, h=25, p='listBuildButtonLayout', text="10")
        cmds.text(label="size", w=80, h=25) 
        self.size=cmds.textField(w=40, h=25, p='listBuildButtonLayout', text="10")
        cmds.gridLayout('txvaluemeter', p='selectArrayColumn', numberOfColumns=3, cellWidthHeight=(80, 18)) 
        cmds.text(label="range", w=80, h=25) 
        self.firstMinValue=cmds.textField(w=40, h=25, p='txvaluemeter', text="-20.0")
        self.firstMaxValue=cmds.textField(w=40, h=25, p='txvaluemeter', text="20.0")  
        gridLayout('BuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(150, 20))             
        button (label='Go', p='BuildButtonLayout', command = lambda *args:self.create_tail_guides(firstMinValue=float(textField(self.firstMinValue,q=1, text=1)), firstMaxValue=float(textField(self.firstMaxValue,q=1, text=1)), amount=int(textField(self.amount,q=1, text=1)), size=int(textField(self.size,q=1, text=1)), namefield=textField(self.namefield,q=1, text=1), direction=optionMenu(direction, q=1, v=1)))
        showWindow(window)




    def create_tail_guides(self, firstMinValue, firstMaxValue, amount, size, namefield, direction):
        nameBucket=[]
        namePortionTwo="_guide"
        for each in range(amount):
            numbername=each+1
            stringname=str(numbername)
            numbername=[each for each in stringname]
            if len(numbername)==1:
                newname=namefield+'0'+stringname+"_guide"
                if objExists(newname):
                    newname=getClass.nameExist(namefield, namePortionTwo)                
            elif len(numbername)>1:
                newname=namefield+stringname+"_guide"
                if objExists(newname):
                    newname=getClass.nameExist(namefield, namePortionTwo)             
            nameBucket.append(newname)  
        getSelected=range(amount)
        BucketValue=getClass.Percentages(getSelected, firstMinValue, firstMaxValue)
        guideDict={}
        for eachName, eachValue in map(None, nameBucket, BucketValue):
            if direction=="X":
                nrx=eachValue
                nry=0
                nrz=0  
            if direction=="Y":
                nrx=0
                nry=eachValue
                nrz=0   
            if direction=="Z":
                nrx=0
                nry=0
                nrz=eachValue            
            getValueBucket=(nrx, nry, nrz)
            print getValueBucket
            lineData={eachName:getValueBucket}       
            guideDict.update(lineData)  
        Ggrp=cmds.CreateEmptyGroup()
        cmds.rename(Ggrp, "Guides_"+namefield+"_grp")
        for key, value in guideDict.items():
            Guide=getClass.makeguide_shapes(key, colour1, colour2, colour3)  
            cmds.move(value[0], value[1], value[2], Guide,r=1, rpr=1 )
            cmds.parent(key,"Guides_"+namefield+"_grp")

    def create_tail_guidesV1(self, firstMinValue, firstMaxValue, amount, size, namefield, direction):
        colour1=13
        colour2=6
        colour3=27          
        nameBucket=[]
        for each in range(amount):
            numbername=each+1
            stringname=str(numbername)
            numbername=[each for each in stringname]
            if len(numbername)==1:
                newname=namefield+'0'+stringname+"_guide"
            elif len(numbername)>1:
                newname=namefield+stringname+"_guide"
            nameBucket.append(newname)  
        getSelected=range(amount)
        BucketValue=getClass.Percentages(getSelected, firstMinValue, firstMaxValue)
        guideDict={}
        for eachName, eachValue in map(None, nameBucket, BucketValue):
            if direction=="X":
                nrx=eachValue
                nry=0
                nrz=0  
            if direction=="Y":
                nrx=0
                nry=eachValue
                nrz=0   
            if direction=="Z":
                nrx=0
                nry=0
                nrz=eachValue            
            getValueBucket=(nrx, nry, nrz)
            print getValueBucket
            lineData={eachName:getValueBucket}       
            guideDict.update(lineData)  
        Ggrp=cmds.CreateEmptyGroup()
        cmds.rename(Ggrp, "Guides_"+namefield+"_grp")
        for key, value in guideDict.items():
            Guide=getClass.makeguide_shapes(key, colour1, colour2, colour3)  
            cmds.move(value[0], value[1], value[2], Guide,r=1, rpr=1 )
            cmds.parent(key,"Guides_"+namefield+"_grp")


            
#                   
#        Ggrp=cmds.CreateEmptyGroup()
#        cmds.rename(Ggrp, "Guides_Tail_grp")
#        guideDict= {
#                    'tail01_guide':[-0.0027999122373705276, 101.81306847273903, -12.802453296847265],
#                    'tail02_guide':[-0.002799912237366739, 108.5464318918672, -14.738674607817812],
#                    'tail03_guide':[-0.0027999122373669749, 113.58638894781204, -16.017880050963289],
#                    'tail04_guide':[0.013779694044587801, 117.7259074130272, -18.154366850164259],
#                    'tail05_guide':[0.013779694044602008, 122.0401413938731, -20.217515750401468],
#                    'tail06_guide':[0.013779694044633962, 125.7192721232971, -21.368741829687444],
#                    'tail07_guide':[0.041299145700635309, 130.33603197336751, -23.093919309815135],
#                    'tail08_guide':[-0.0012049298241505538, 134.57698119414135, -23.567714955561129],
#                    'tail09_guide':[-0.052538731083116019, 140.42369406499478, -22.999857579413948],
#                    'tail10_guide':[-0.012650158967222359, 146.41747041660048, -21.545746695423997]}
#        for key, value in guideDict.items():
#            Guide=getClass.makeguide_shapes(key, colour1, colour2, colour3)  
#            cmds.move(value[0], value[1], value[2], Guide,r=1, rpr=1 )
#            cmds.parent(key,"Guides_Tail_grp")

    def build_previs_face_guides(self, arg=None):
        Ggrp=cmds.CreateEmptyGroup()
        cmds.rename(Ggrp, "Guides_PFace_grp")
        guideDict= {
                    'BottomLid_R_Ctrl_guide':[-6.439449787139893, 117.65327276352865, 9.309892654418945],
                    'Chin_Ctrl_guide':[-9.844079613685608e-07, 108.55262266820495, 10.37376594543457],
                    'EyeOrient_R_Ctrl_guide':[-6.439449787139893, 120.22750245784006, 9.309892654418945],
                    'Eye_R_Ctrl_guide':[-4.32306182384491, 121.13178253173828, 2.3530614376068115],
                    'Jaw_Ctrl_guide':[-9.844079627033985e-07, 112.25226985464661, -0.5260112003405668],
                    'TopLid_R_Ctrl_guide':[-6.439449787139893, 122.92882094826075, 9.309892654418945]
                    }
#         colour1, colour2, colour3=17, 17, 17
        for key, value in guideDict.items():
            Guide=getClass.makeguide_shapes(key, colour1, colour2, colour3)  
            cmds.move(value[0], value[1], value[2], Guide,r=1, rpr=1 )
            cmds.parent(key,"Guides_PFace_grp")
            
    def build_anim_face_guides(self, arg=None):
        Ggrp=cmds.CreateEmptyGroup()
        cmds.rename(Ggrp, "Guides_PFace_grp")
        guideDict= {"faceLid_Closed01_R_guide":[-8.896372856267416, 120.4456706032946, 8.049177473193442],
                    "faceLid_Closed02_R_guide":[-8.037413846165487, 119.26016491653817, 8.376691925324028],
                    "faceLid_Closed03_R_guide":[-6.232463731077276, 118.61598833865641, 9.080693942188791],
                    "faceLid_Closed04_R_guide":[-4.598158148310122, 118.67326844902203, 9.324813570370708],
                    "faceLid_Closed05_R_guide":[-3.4460911750793457, 118.84195744966804, 9.31334400177002],
                    "faceLid_Open01_B_R_guide":[-9.691352844238281, 122.22998046875, 7.6546502113342285],
                    "faceLid_Open01_T_R_guide":[-9.691352844238281, 122.22998046875, 7.6546502113342285],
                    "faceLid_Open02_B_R_guide":[-9.319539070129395, 119.46768951416016, 7.733199119567871],
                    "faceLid_Open02_T_R_guide":[-8.310280799865723, 123.4416275024414, 8.545402526855469],
                    "faceLid_Open03_B_R_guide":[-7.204860687255859, 118.03981018066406, 8.750569343566895],
                    "faceLid_Open03_T_R_guide":[-5.540938854217529, 123.34326171875, 9.492467880249023],
                    "faceLid_Open04_B_R_guide":[-5.117918014526367, 117.8886947631836, 9.295153617858887],
                    "faceLid_Open04_T_R_guide":[-3.806987762451172, 121.0884017944336, 9.805170059204102],
                    "faceLid_Open05_B_R_guide":[-3.4460911750793457, 118.33078002929688, 9.31334400177002],
                    "faceLid_Open05_T_R_guide":[-3.4460911750793457, 118.33078002929688, 9.31334400177002],
                    "faceLid_Pivot_R_guide":[-4.32306182384491, 121.13178253173828, 2.3530614376068115],
                    "faceBrow01_R_guide":[-4.649524216651916, 126.33473052978516, 11.41671956062317],
                    "faceBrow02_R_guide":[-6.1532183830719145, 127.07677568258379, 11.029437819072257],
                    "faceBrow03_R_guide":[-7.7906457951764, 127.3533911178894, 10.326720765791066],
                    "faceBrow04_R_guide":[-9.259915647506714, 127.0462956237793, 9.47455855369568],
                    "faceBrow05_R_guide":[-10.325699672698974, 126.41309783935547, 8.244106769561768],
                    "faceCheekBone_R_guide":[-11.197915086746216, 116.4941877746582, 5.7716323232650755],
                    "faceCheek_R_guide":[-7.375286254882813, 113.8609376525879, 8.72200032234192],
                    "faceCheek_T_R_guide":[-6.2760679817199705, 116.14335647583007, 9.33484082221985],
                    "faceJaw_R_guide":[-4.604631729125977, 109.51376113891602, 7.858884401321411],
                    "faceLip_B_guide":[1.999999856394652e-06, 110.89708755493164, 10.713265647888184],
                    "faceLip_Corner_R_guide":[-3.211460952758789, 112.24456344604492, 10.275378131866455],
                    "faceLip_B_R_guide":[-1.9539768433570863, 111.4278303527832, 10.497671976089478],
                    "faceLip_T_R_guide":[-1.857512891292572, 112.46697235107422, 11.21329568862915],
                    "faceLip_T_guide":[1.999999856394652e-06, 112.65124404907226, 11.606070890426636],
                    "faceNose_guide":[1.999999856394652e-06, 116.0290998840332, 13.066232490539551],
                    "faceNose_R_guide":[-3.115836036205292, 114.36648818969726, 10.94296335220337],
                    "faceTeeth_B_guide":[1.999999856394652e-06, 111.55121633391455, 6.899612959996568],
                    "faceTeeth_T_guide":[1.999999856394652e-06, 111.72055569146573, 6.899612959996568],
                    "faceTongue01_guide":[1.999999856394652e-06, 107.4649715592315, 0.1317209521177194],
                    "faceTongue02_guide":[1.999999856394652e-06, 109.53932817579798, 1.258378006877365],
                    "faceTongue03_guide":[0.21653302099723604, 110.66061902385435, 2.8572037269408446],
                    "faceTongue04_guide":[0.21653302099723604, 111.10769364773783, 4.629074884485468],
                    "faceTongue05_guide":[0.21653302099723604, 111.13297025688654, 7.34287880047511],
                    }
#         colour1, colour2, colour3=17, 17, 17
        for key, value in guideDict.items():
            Guide=getClass.makeguide_shapes(key, colour1, colour2, colour3)  
            cmds.move(value[0], value[1], value[2], Guide,r=1, rpr=1 )
            cmds.parent(key,"Guides_PFace_grp")



# inst = GuideUI()
# inst.create()
