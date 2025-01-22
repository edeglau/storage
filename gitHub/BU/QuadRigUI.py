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

class QuadUI(object):
    '''--------------------------------------------------------------------------------------------------------------------------------------
    Interface Layout
    --------------------------------------------------------------------------------------------------------------------------------------'''          
    def __init__(self, winName="Quad Rig"):
        self.winTitle = "Quad Rig"
        self.winName = winName

    def create(self):
        
        if cmds.window(self.winName, exists=True):
                cmds.deleteUI(self.winName)

        self.window = cmds.window(self.winName, title=self.winTitle, tbm=1, w=270, h=250, bgc=[0.0, 0.35, 0.0] )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=200)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')

        cmds.rowLayout  (' rMainRow ', w=350, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(120, 20), bgc=[0.55, 0.65, 0.55])
        cmds.button (label='QuadLeg', bgc=[0.6, 0.8, 0.6], p='listBuildButtonLayout', command = self.build_quad_leg_rig)
        cmds.button (label='QuadArm', p='listBuildButtonLayout', command = self.build_quad_arm_rig)    
        cmds.button (label='QuadArmRev', p='listBuildButtonLayout', command = self.build_quad_arm_opp_rig)    
        cmds.button (label='Hoof', p='listBuildButtonLayout', command = self.hoof)      
        cmds.button (label='Paw', p='listBuildButtonLayout', command = self.hoof_toe)      
        cmds.button (label='ConFoot', p='listBuildButtonLayout', command = self.connect_hoof) 
        cmds.button (label='QSpine', p='listBuildButtonLayout', command = self.quad_spine)                     
        cmds.button (label='QLongNeck', p='listBuildButtonLayout', command = self.quad_neck)      
        cmds.button (label='QNoNeck', p='listBuildButtonLayout', command = self.quad_no_neck)      
        cmds.button (label='Tail', p='listBuildButtonLayout', command = self.build_tail_rig)  
        cmds.button (label='QuadBodLimb', p='listBuildButtonLayout', command = self.connect_quad_whole)
        cmds.button (label='QHead4LongNeck', p='listBuildButtonLayout', command = self.quad_head)                
        cmds.button (label='PrevisFace', p='listBuildButtonLayout', command = self.previs_face)  
        cmds.button (label='ConPrevisHead', p='listBuildButtonLayout', command = self.con_previs_face)
        cmds.button (label='Clean', p='listBuildButtonLayout', command = self.clean)        
        cmds.button (label='PostCreateToe', p='listBuildButtonLayout', command = self._toe)        
        #cmds.symbolButton (p='listBuildButtonLayout', command = self.Face, image="D:\myGraphics\icons\SP.jpg") 
        cmds.text (label='Author: Elise Deglau',w=120, al='left', p='selectArrayColumn')      
        cmds.showWindow(self.window)

    def build_arm_rig(self, arg=None):
        import ArmRig
        reload (ArmRig)
        getClass=ArmRig.ArmRig()
        #getClass.ArmRig()
        
    def build_quad_arm_rig(self, arg=None):
        import QuadArmRig
        reload (QuadArmRig)
        getClass=QuadArmRig.ArmRig()
        #getClass.ArmRig()        
    def build_quad_arm_opp_rig(self, arg=None):
        import QuadArmRigRevElbow
        reload (QuadArmRigRevElbow)
        getClass=QuadArmRigRevElbow.ArmRig()
        #getClass.ArmRig()        

    def build_hand_rig(self, arg=None):
        import HandRig
        reload (HandRig)
        getClass=HandRig.HandRig()
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
        import connectWhole
        reload (connectWhole)
        getClass=connectWhole.BodConn()
        
    def build_spine_rig(self, arg=None):
        import SpineRig
        reload (SpineRig)
        getClass=SpineRig.SpineRig()

    def connect_arm_hand(self, arg=None):
        import connectHandToArm
        reload (connectHandToArm)
        getClass=connectHandToArm.HandConn()


    def connect_quad_whole(self, arg=None):
        import connectQuadWhole
        reload (connectQuadWhole)
        getClass=connectQuadWhole.BodConn()
                        
    def connect_leg_foot(self, arg=None): 
        import connectFootToLeg
        reload (connectFootToLeg)
        getClass=connectFootToLeg.FootConn()

    def build_tail_rig(self, arg=None): 
        import ChainWork 
        reload (ChainWork)
        mainName="tail"
        nrx=0
        nry=1
        nrz=0
        ControllerSize=10
        getClass=ChainWork.ChainRig(nrz, nry, nrx, mainName, ControllerSize)

    def clean(self, arg=None):    
        import QuadCleanup
        reload (QuadCleanup)
        getClass=QuadCleanup.cln()
    def _toe(self, arg=None):    
        import Toes
        reload (Toes)
        getClass=Toes.ToeAddition()
        
    def Face(self, arg=None):
        import FaceRig
        reload (FaceRig)
        getClass=FaceRig.faceSet()
     
    def previs_face(self, arg=None):
        import facialPrevis
        reload (facialPrevis)
        getClass=facialPrevis.faceRig()
        
    def con_previs_face(self, arg=None):
        import connectPrevFaceToHead
        reload (connectPrevFaceToHead)
        getClass=connectPrevFaceToHead.PFaceConn()      
        
    def hoof(self, arg=None):
        import HoofRig
        reload (HoofRig)
        getClass=HoofRig.FootRig()
    def hoof_toe(self, arg=None):
        import HoofRig_Toe
        reload (HoofRig_Toe)
        getClass=HoofRig_Toe.FootRig()
        
    def connect_hoof(self, arg=None):
        import connectHooves
        reload (connectHooves)
        getClass=connectHooves.FootConn()        

    def quad_spine(self, arg=None):
        import QuadSpineRig
        reload (QuadSpineRig)
        getClass=QuadSpineRig.SpineRig()   
    def quad_no_neck(self, arg=None):
        import QuadNeck
        reload (QuadNeck)
        getClass=QuadNeck.QuadNoNeckRig()   
        
    def quad_neck(self, arg=None):
        import ChainWork 
        reload (ChainWork)
        mainName="neck"
        nrx=0
        nry=1
        nrz=0
        ControllerSize=20
        getClass=ChainWork.ChainRig(nrz, nry, nrx, mainName, ControllerSize)
        #getClass.Trigger(nrz, nry, nrx, mainName)              


    def quad_head(self, arg=None):
        import QuadHead
        reload (QuadHead)
        getClass=QuadHead.HeadRig()

inst = QuadUI()
inst.create()
