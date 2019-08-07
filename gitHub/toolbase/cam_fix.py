focusedThing=cmds.ls(sl=1, fl=1)[1]
getOldCam=cmds.ls(sl=1, fl=1)[0]
newcam=cmds.camera()
cmds.select(newcam[0], r=1)
cmds.select(getOldCam, add=1)
getBaseClass.massTransfer()
cmds.select(focusedThing, r=1)
cmds.viewFit()
cmds.delete(newcam[0])
