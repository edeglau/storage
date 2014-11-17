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
'This work is licensed under a Creative Commons License'
'http://creativecommons.org/licenses/by-sa/3.0/au/'

filepath= os.getcwd()
sys.path.append(str(filepath))

class BipeddUI(object):
    '''--------------------------------------------------------------------------------------------------------------------------------------
    Interface Layout
    --------------------------------------------------------------------------------------------------------------------------------------'''          
    def __init__(self, winName="Rig Modules"):
        self.winTitle = "Rig Modules"
        self.winName = winName

    def create(self):
        
        if cmds.window(self.winName, exists=True):
                cmds.deleteUI(self.winName)

        self.window = cmds.window(self.winName, title=self.winTitle, tbm=1, w=270, h=250 , bgc=[0.35, 0.25, 0.35])

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=200)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')

        cmds.rowLayout  (' rMainRow ', w=350, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn',bgc=[0.75, 0.65, 0.75], numberOfColumns=2, cellWidthHeight=(80, 20))
        cmds.button (label='Arm', p='listBuildButtonLayout', command = self.build_arm_rig)
        cmds.button (label='Hand', p='listBuildButtonLayout', command = self.build_hand_rig)
        cmds.button (label='ConHand', p='listBuildButtonLayout', command = self.connect_arm_hand)                
        cmds.button (label='Foot', p='listBuildButtonLayout', command = self.build_foot_rig)        
        cmds.button (label='Leg', p='listBuildButtonLayout', command = self.build_leg_rig)
        cmds.button (label='ConFoot', p='listBuildButtonLayout', command = self.connect_leg_foot)  
        cmds.button (label='Spine', p='listBuildButtonLayout', command = self.build_spine_rig)
        cmds.button (label='ConBodLimb', p='listBuildButtonLayout', command = self.connect_whole)
        cmds.button (label='PrevisFace', p='listBuildButtonLayout', command = self.previs_face)  
        #cmds.button (label='PPollyFAce', p='listBuildButtonLayout', command = self.previs_polly_face)  
        cmds.button (label='ConPrevHead', p='listBuildButtonLayout', command = self.con_previs_face)
        cmds.button (label='ChainRig', p='listBuildButtonLayout', command = self.chain_rig)
        #cmds.button (label='Face', p='listBuildButtonLayout', command = self.Face)        
        #cmds.button (label='Eye', p='listBuildButtonLayout', command = self.eye)        
        cmds.button (label='Clean', p='listBuildButtonLayout', command = self.clean)        
#         cmds.button (label='Tail', p='listBuildButtonLayout', command = self.build_tail_rig)          
        #cmds.symbolButton (p='listBuildButtonLayout', command = self.Face, image="D:\myGraphics\icons\SP.jpg") 
        cmds.text (label='Author: Elise Deglau',w=120, al='left', p='selectArrayColumn')      
        cmds.showWindow(self.window)

    def build_arm_rig(self, arg=None):
        import ArmMirrorRig
        reload (ArmMirrorRig)
        getClass=ArmMirrorRig.ArmRig()
        #getClass.ArmRig()
        
    def build_quad_arm_rig(self, arg=None):
        import QuadArmRig
        reload (QuadArmRig)
        getClass=QuadArmRig.ArmRig()
        #getClass.ArmRig()        

    def build_hand_rig(self, arg=None):
        import HandMirrorRig
        reload (HandMirrorRig)
        getClass=HandMirrorRig.HandRig()
        #getClass.HandRig()
            
    def build_foot_rig(self, arg=None):
        import FootRig
        reload (FootRig)
        getClass=FootRig.FootRig()
        
    def build_leg_rig(self, arg=None):
        import LegRig
        reload (LegRig)
        getClass=LegRig.LegRig()        

    def build_quad_leg_rig(self, arg=None):
        import QuadLegRig
        reload (QuadLegRig)
        getClass=QuadLegRig.LegRig()           

    def connect_whole(self, arg=None):
        import connectWholeMirror
        reload (connectWholeMirror)
        getClass=connectWholeMirror.BodConn()
        
    def build_spine_rig(self, arg=None):
        import SpineRig
        reload (SpineRig)
        getClass=SpineRig.SpineRig()

    def connect_arm_hand(self, arg=None):
        import connectHandToArmMirror
        reload (connectHandToArmMirror)
        getClass=connectHandToArmMirror.HandConn()


    def connect_quad_whole(self, arg=None):
        import connectQuadWhole
        reload (connectQuadWhole)
        getClass=connectQuadWhole.BodConn()
                        
    def connect_leg_foot(self, arg=None): 
        import connectFootToLeg
        reload (connectFootToLeg)
        getClass=connectFootToLeg.FootConn()

    def build_tail_rig(self, arg=None): 
        import TailRig
        reload (TailRig)
        getClass=TailRig.tailRig()

    def clean(self, arg=None):    
        import cleanupMirror
        reload (cleanupMirror)
        getClass=cleanupMirror.cln()
        
    def Face(self, arg=None):
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceRigger()
        getClass.Face()
     
    def previs_face(self, arg=None):
        import facialPrevis
        reload (facialPrevis)
        getClass=facialPrevis.faceRig()
        
    def previs_polly_face(self, arg=None):
        import facialPrev_Polly
        reload (facialPrev_Polly)
        getClass=facialPrev_Polly.faceRig()

    def eye(self, arg=None):
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.FaceRigger()
        getClass.Cavity()
        
    def con_previs_face(self, arg=None):
        import connectPrevFaceToHead
        reload (connectPrevFaceToHead)
        getClass=connectPrevFaceToHead.PFaceConn()      
        
    def hoof(self, arg=None):
        import HoofRig
        reload (HoofRig)
        getClass=HoofRig.FootRig()
        
    def connect_hoof(self, arg=None):
        import connectHooves
        reload (connectHooves)
        getClass=connectHooves.FootConn()        

    def quad_spine(self, arg=None):
        import QuadSpineRig
        reload (QuadSpineRig)
        getClass=QuadSpineRig.SpineRig()        


    def chain_rig(self, arg=None):
        import ChainWork
        reload (ChainWork)
        result = cmds.promptDialog( 
                    title='Building a chainrig', 
                    message="Enter dimentions for chain - EG:", 
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
inst = BipeddUI()
inst.create()

