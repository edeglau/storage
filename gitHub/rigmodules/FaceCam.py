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
import baseFunctions_maya
reload (baseFunctions_maya)
getClass = baseFunctions_maya.BaseClass()

                        
class FaceCamera(object):
    def create(self):
        faceCamTgt=cmds.ls("BigBox_CC")
        transformWorldMatrix, rotateWorldMatrix=getClass.locationXForm(faceCamTgt[0])
        faceCamera=cmds.camera(n="FaceCam")
        cmds.xform(faceCamera[0], ws=1, t=transformWorldMatrix)
        cmds.move(0, 0, 50, faceCamera[0],r=1, rpr=1)
        getClass.buildGrp(faceCamera[0])
        getGrp=cmds.listRelatives(faceCamera[0], ap=1)
        cmds.parentConstraint(faceCamTgt, getGrp, mo=1)
    #     getAtts=[".tx", ".ty", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz", ".centerOfInterest"]
    #     for each in getAtts:
    #         cmds.setAttr(faceCamera[0]+each, keyable=0, lock=1)
        cmds.rename(faceCamera[0], "FaceCam")
        cmds.rename(getGrp, "FaceCam_grp")
        cmds.parent("FaceCam_grp", "FaceRig")
    def unlock(self):
        faceCam=cmds.ls("FaceCam")
        getAtts=[".tx", ".ty", ".tz", ".rx", ".ry", ".rz"]
        for each in getAtts:
            cmds.setAttr(faceCam[0]+each, cb=1)
            cmds.setAttr(faceCam[0]+each, keyable=1)
            cmds.setAttr(faceCam[0]+each, lock=0)
