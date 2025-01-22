##nuc initiate
import maya.cmds as cmds

getNode=cmds.ls(type="nucleus")
getStartValue=cmds.getAttr(getNode[0]+".startFrame")
getStateValue=cmds.getAttr(getNode[0]+".enable")
getLowRange=cmds.playbackOptions(q=1,min=1)
if getStartValue != getLowRange:
    cmds.setAttr(getNode[0]+".startFrame", getLowRange)
if getStateValue != 1:
    cmds.setAttr(getNode[0]+".enable", 1)
setinit = int(getLowRange)+1
cmds.currentTime(getLowRange)
cmds.currentTime(setinit)
cmds.currentTime(getLowRange)
cmds.select(getNode[0])
