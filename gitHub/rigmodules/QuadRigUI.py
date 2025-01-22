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
# from rigmodules import chainRigSupplemental

__author__ = "Elise Deglau"
__version__ = 1.00

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

        self.window = cmds.window(self.winName, title=self.winTitle, tbm=1, w=270, h=250 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=200)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')

        cmds.rowLayout  (' rMainRow ', w=350, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(80, 20))
        cmds.button (label='QuadLeg', p='listBuildButtonLayout', command = self.build_quad_leg_rig)
        cmds.button (label='QuadArm', p='listBuildButtonLayout', command = self.build_quad_arm_rig)    
        cmds.button (label='Hoof', p='listBuildButtonLayout', command = self.hoof)      
        cmds.button (label='ConHoof', p='listBuildButtonLayout', command = self.connect_hoof) 
        cmds.button (label='QSpine', p='listBuildButtonLayout', command = self.quad_spine)                     
        cmds.button (label='Qneck', p='listBuildButtonLayout', command = self.quad_neck)      
        cmds.button (label='Tail', p='listBuildButtonLayout', command = self.build_tail_rig)  
        cmds.button (label='QuadBodLimb', p='listBuildButtonLayout', command = self.connect_quad_whole)
        cmds.button (label='QuadHead', p='listBuildButtonLayout', command = self.quad_head)                
        cmds.button (label='PrevisFace', p='listBuildButtonLayout', command = self.previs_face)  
        cmds.button (label='ConPrevHead', p='listBuildButtonLayout', command = self.con_previs_face)
        cmds.button (label='Quad_horse', p='listBuildButtonLayout', command = self._quad_whole)  
        cmds.button (label='Face', p='listBuildButtonLayout', command = self.Face)        
        cmds.button (label='Clean', p='listBuildButtonLayout', command = self.clean)        
        #cmds.symbolButton (p='listBuildButtonLayout', command = self.Face, image="D:\myGraphics\icons\SP.jpg") 
        cmds.text (label='Author: Elise Deglau',w=120, al='left', p='selectArrayColumn')      
        cmds.showWindow(self.window)

    def _quad_whole(self, arg=None):
        self.build_quad_leg_rig()
        self.build_quad_arm_rig()
        self.hoof()
        self.connect_hoof()
        self.quad_spine()
        self.quad_neck()
        self.build_tail_rig()
        self.connect_quad_whole()
        self.quad_head()
        self.con_previs_face()
        self._quad_whole_hoofs()
        
        
    def build_quad_arm_rig(self, arg=None):
        import QuadArmRig
        reload (QuadArmRig)
        getClass=QuadArmRig.ArmRig()
        #getClass.ArmRig()        


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
        import chainRigSupplemental 
        reload (chainRigSupplemental)
        mainName="tail"
        nrx=0
        nry=1
        nrz=0
        ControllerSize=10
        getClass=chainRigSupplemental.ChainRig(nrz, nry, nrx, mainName, ControllerSize)

    def clean(self, arg=None):    
        import QuadCleanup
        reload (QuadCleanup)
        getClass=QuadCleanup.cln()
        
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
        
    def connect_hoof(self, arg=None):
        import connectHooves
        reload (connectHooves)
        getClass=connectHooves.FootConn()        

    def quad_spine(self, arg=None):
        import QuadSpineRig
        reload (QuadSpineRig)
        getClass=QuadSpineRig.SpineRig()   
        
    def quad_neck(self, arg=None):
        import chainRigSupplemental 
        reload (chainRigSupplemental)
        mainName="neck"
        nrx=0
        nry=1
        nrz=0
        ControllerSize=20
        getClass=chainRigSupplemental.ChainRig(nrz, nry, nrx, mainName, ControllerSize)
        #getClass.Trigger(nrz, nry, nrx, mainName)              


    def quad_head(self, arg=None):
        import QuadHead
        reload (QuadHead)
        getClass=QuadHead.HeadRig()

inst = QuadUI()
inst.create()
