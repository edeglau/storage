
import maya.cmds as cmds
import maya.mel
import os, subprocess, sys, platform, logging, signal, re, getpass, datetime

class witCam_rivet(object):
    '''--------------------------------------------------------------------------------------------------------------------------------------
    Interface Layout
    --------------------------------------------------------------------------------------------------------------------------------------'''          
    def __init__(self):
        self.wit_cam()

    def wit_cam(self, arg=None):
        focusedThing=cmds.ls(sl=1, fl=1)[0]
        if cmds.nodeType(focusedThing)=="transform":
            focPane = [(each) for each in cmds.getPanel(vis=1) if "model" in each][0]
            command='postModelEditorSelectCamera "%s" "%s" 0' % (focPane, focPane)
            maya.mel.eval( command )  
            getOldCam=cmds.ls(sl=1, fl=1)[0]
            newcam=cmds.camera()
            cmds.select(newcam[0], r=1)
            cmds.select(getOldCam, add=1)
            self.massTransfer()
            cmds.select(focusedThing, r=1)
            command='lookThroughModelPanel "%s" "%s"' % (newcam[0], focPane)
            print (command)
            maya.mel.eval( command )
        elif cmds.nodeType(focusedThing)=="mesh":
            print ("mesh evoked")
            command='Rivet;'
            maya.mel.eval( command )
            locatorObj=cmds.ls(sl=1, fl=1)[0]
            focPane = [(each) for each in cmds.getPanel(vis=1) if "model" in each][0]
            command='postModelEditorSelectCamera "%s" "%s" 0' % (focPane, focPane)
            maya.mel.eval( command )  
            getOldCam=cmds.ls(sl=1, fl=1)[0]
            newcam=cmds.camera()
            cmds.select(newcam[0], r=1)
            cmds.select(getOldCam, add=1)
            rl_loc = 'pinOutput'
            self.massTransfer(rl_loc)
            cmds.select(locatorObj, r=1)
            command='lookThroughModelPanel "%s" "%s"' % (newcam[0], focPane)
            maya.mel.eval( command )


    def massTransfer(self, locatorObj):
        '''alternates a selection to sequentially mass transfer attributes from pairs of objects'''
#        selObj=self.selection_grab()
        selObj=cmds.ls(sl=1)
        print (selObj[0], selObj[1])
        eachController = selObj[1]
        eachChild =selObj[0]
        cnst = cmds.parentConstraint(eachController, eachChild, mo=0)[0]
        cmds.delete(cnst)
        print (locatorObj)
        cmds.pointConstraint(locatorObj, eachChild, mo=1)
inst = witCam_rivet()
