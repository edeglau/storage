
try:
    maya.mel.eval('deleteCacheFile 2 { "keep", "" } ;')
except:
    pass
filepath="/jobs/vfx_motherland/dev/dev1502/TASKS/techanim/maya/cache/nCloth/batch/deglaue/pyJob/wkabi1Tech/c_cloak_01_simCage_lo_sim_outputClothShape/v0002/scalingRelation_0.0__spaceScale_0.09"
filexml = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(filepath) for name in files if name.lower().endswith(".xml")][0]
getSel=cmds.ls(sl=1)
for each in getSel:
    getCommand='createHistorySwitch("%s",false)' %each
    switch = maya.mel.eval(getCommand)
    cacheNode = cmds.cacheFile(f=filexml, ia='%s.inp[0]' % switch ,attachFile=True)
    cmds.setAttr( '%s.playFromCache' % switch, 1 )
filepath="_".join(filepath.split("."))
filename=filepath.split('/')[-1]
filepathname=filepath+'/'+filename
if not os.path.exists(filepath): os.makedirs(filepath)
cmds.playblast(clearCache=1, endTime=cmds.playbackOptions(max=1, aet=1, q=1), filename=filepathname, format="image", offScreen=1, percent=100, quality=100, sequenceTime=0, showOrnaments=1, startTime=cmds.playbackOptions(min=1, ast=1, q=1), viewer=0, widthHeight=[2156, 1212])

