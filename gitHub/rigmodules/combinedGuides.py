import maya.cmds as cmds
from functools import partial
from string import *
import re
import maya.mel
import os, subprocess, sys, platform
from os  import popen
from sys import stdin
#import win32clipboard
import operator

__author__ = "Elise Deglau"
__version__ = 1.00

filepath=( 'D:\\code\\git\\LiquidGit\\Liquid_egit\\rigmodules\\' )
sys.path.append(str(filepath))
import baseFunctions_maya
reload (baseFunctions_maya)
getClass=baseFunctions_maya.BaseClass()

filepath= os.getcwd()
sys.path.append(str(filepath))

class GuideUI(object):
    '''--------------------------------------------------------------------------------------------------------------------------------------
    Interface Layout
    --------------------------------------------------------------------------------------------------------------------------------------'''          
    def __init__(self, winName="rigGuides"):
        self.winTitle = "rigGuides"
        self.winName = winName

    def create(self):
        
        if cmds.window(self.winName, exists=True):
                cmds.deleteUI(self.winName)

        self.window = cmds.window(self.winName, title=self.winTitle, tbm=1, w=270, h=250 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=200)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')

        cmds.rowLayout  (' rMainRow ', w=350, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(80, 20))
        cmds.button (label='Arm Guides', p='listBuildButtonLayout', command = self.build_arm_guides)
        cmds.button (label='Foot Guides', p='listBuildButtonLayout', command = self.build_foot_guides)        
        cmds.button (label='Leg Guides', p='listBuildButtonLayout', command = self.build_leg_guides)
        cmds.button (label='Neck Guides', p='listBuildButtonLayout', command = self.build_neck_guides)
        cmds.button (label='Spine Guides', p='listBuildButtonLayout', command = self.build_spine_guides)
        cmds.button (label='Hand Guides', p='listBuildButtonLayout', command = self.build_hand_guides)
        cmds.button (label='Tail Guides', p='listBuildButtonLayout', command = self.build_tail_guides)    
        cmds.button (label='Pface Guides', p='listBuildButtonLayout', command = self.build_previs_face_guides)    
        cmds.button (label='Save Guides', p='listBuildButtonLayout', command = self.save_guides)
        cmds.button (label='Open Guides', p='listBuildButtonLayout', command = self.open_guides)        
        cmds.button (label='Extra Guides', p='listBuildButtonLayout', command = self.open_extra_guides)        
        cmds.text (label='Author: Elise Deglau',w=120, al='left', p='selectArrayColumn')
#         cmds.text (label='This work is licensed under a Creative Commons License', hl=1, w=300, al='left', p='selectArrayColumn')
#         cmds.text (label='http://creativecommons.org/licenses/by/4.0/', hl=1, w=350, al='left', p='selectArrayColumn')        
        cmds.showWindow(self.window)

    def open_extra_guides(self, arg=None):
        import extraGuides
        reload(extraGuides)
        extraGuides.GuideUI()
        
    def build_arm_guides(self, arg=None):
        Ggrp=cmds.CreateEmptyGroup()
        cmds.rename(Ggrp, "Guides_Arm_grp")
        guideDict= {
                    'armcollarRight_guide':[-6.7072172366132268, 149.94747012321017, -9.8769280358770075],
                    'armelbowRight_guide':[-50.583802736485325, 143.78668591870758, -11.67773643630014],
                    'armshoulderRight_guide':[-18.763755961767572, 144.86111784853566, -9.8769280358770075],
                    'armwristRight_guide':[-75.951702321228368, 144.01692133224216, -11.322940637912122],
                    }
        colour1, colour2, colour3=17, 17, 17
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
        colour1, colour2, colour3=17, 17, 17
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
        colour1, colour2, colour3=17, 17, 17
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
        colour1, colour2, colour3=17, 17, 17
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
        colour1, colour2, colour3=17, 17, 17
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
        colour1, colour2, colour3=17, 17, 17
        for key, value in guideDict.items():
            Guide=getClass.makeguide_shapes(key, colour1, colour2, colour3)  
            cmds.move(value[0], value[1], value[2], Guide,r=1, rpr=1 )
            #cmds.makeIdentity(key, a=True, t=1, s=1, r=1, n=0)
            cmds.parent(key,"Guides_Spine_grp")
            
            

    def save_guides(self, arg=None):
        result = cmds.promptDialog( 
                    title='Confirm', 
                    message='filename', 
                    button=['Continue','Cancel'],
                    defaultButton='Continue', 
                    cancelButton='Cancel', 
                    dismissString='Cancel' )
        if result == 'Continue':
            filename=cmds.promptDialog(q=1)
        printFolder="C:\\temp\\"+filename+".txt"
        getGuides=cmds.ls("*guide")
        inp=open(printFolder, 'w+')
        for each in getGuides:
            transform=cmds.xform(each , q=True, ws=1, t=True)
            if transform==[0, 0, 0]:
                transformWorldMatrix = cmds.xform(each, q=True, wd=1, sp=True)  
                rotateWorldMatrix = cmds.xform(each, q=True, wd=1, ra=True) 
            else:
                transformWorldMatrix = cmds.xform(each, q=True, wd=1, t=True)  
                rotateWorldMatrix = cmds.xform(each, q=True, wd=1, ro=True) 
                print str(each)+":"+str(transformWorldMatrix)+":"+str(rotateWorldMatrix)
            inp=open(printFolder, 'a+')
            inp.write(str(each)+":"+str(transformWorldMatrix)+":"+str(rotateWorldMatrix)+'\r\n')
        inp.close()  
        
        
        if '\\\\' in printFolder:
            newpath=re.sub(r'\\\\',r'\\', printFolder)
            os.startfile(r'\\'+newpath[1:])    
        else:
            os.startfile(printFolder)
                        
    def open_guides(self, arg=None):    
        guideDict={}
        result = cmds.promptDialog( 
                    title='Confirm', 
                    message='open file', 
                    button=['Continue','Cancel'],
                    defaultButton='Continue', 
                    cancelButton='Cancel', 
                    dismissString='Cancel' )
        if result == 'Continue':
            filename=cmds.promptDialog(q=1)
            
        printFolder="C:\\temp\\"+filename+".txt"
        
        Ggrp=cmds.CreateEmptyGroup()
        cmds.rename(Ggrp, "Guides_"+filename+"_grp")
        
        inp=open(printFolder, 'r')
        
        List = open(printFolder).readlines()
        
        for each in List:
            newlocbucket=[]
            newrotbucket=[]    
            getDictParts=each.split(':')
            getlocpart=getDictParts[1].strip('[]')
            getlocpart=getlocpart.split(', ')
            for item in getlocpart:
                newlocbucket.append(item)
            getrotpart=getDictParts[2].strip('[]]\r\n')
            getrotpart=getrotpart.split(', ')
            for item in getrotpart:
                getit=item.split('.')
                getint=int(getit[0])
                newrotbucket.append(getint)
            newlocbucket.append(newrotbucket)
            makeDict={getDictParts[0]:newlocbucket}
            guideDict.update(makeDict)
                           
        for key, value in guideDict.items():
            colour1, colour2, colour3=17, 17, 17
            transformWorldMatrix, rotateWorldMatrix=[value[0], value[1], value[2]], value[3]
            getClass.guideBuild(key, transformWorldMatrix, rotateWorldMatrix, colour1, colour2, colour3)
            cmds.parent(key,"Guides_"+filename+"_grp")
           

    def build_tail_guides(self, arg=None):
        Ggrp=cmds.CreateEmptyGroup()
        cmds.rename(Ggrp, "Guides_Tail_grp")
        guideDict= {
                    'tail01_guide':[-0.0027999122373705276, 101.81306847273903, -12.802453296847265],
                    'tail02_guide':[-0.002799912237366739, 108.5464318918672, -14.738674607817812],
                    'tail03_guide':[-0.0027999122373669749, 113.58638894781204, -16.017880050963289],
                    'tail04_guide':[0.013779694044587801, 117.7259074130272, -18.154366850164259],
                    'tail05_guide':[0.013779694044602008, 122.0401413938731, -20.217515750401468],
                    'tail06_guide':[0.013779694044633962, 125.7192721232971, -21.368741829687444],
                    'tail07_guide':[0.041299145700635309, 130.33603197336751, -23.093919309815135],
                    'tail08_guide':[-0.0012049298241505538, 134.57698119414135, -23.567714955561129],
                    'tail09_guide':[-0.052538731083116019, 140.42369406499478, -22.999857579413948],
                    'tail10_guide':[-0.012650158967222359, 146.41747041660048, -21.545746695423997]}
        colour1, colour2, colour3=17, 17, 17
        for key, value in guideDict.items():
            Guide=getClass.makeguide_shapes(key, colour1, colour2, colour3)  
            cmds.move(value[0], value[1], value[2], Guide,r=1, rpr=1 )
            cmds.parent(key,"Guides_Tail_grp")

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
        colour1, colour2, colour3=17, 17, 17
        for key, value in guideDict.items():
            Guide=getClass.makeguide_shapes(key, colour1, colour2, colour3)  
            cmds.move(value[0], value[1], value[2], Guide,r=1, rpr=1 )
            cmds.parent(key,"Guides_PFace_grp")




inst = GuideUI()
inst.create()
