'''select skinned mesh and run script'''
inf_dropoff = 0.4
selObj=cmds.ls(sl=1, fl=1)[0]

getSkinCluster=cmds.skinCluster(selObj, q=1, dt=1)
'''this returns the skin cluster ID and the joint influences'''
for item in getSkinCluster:
    if "GroupId" in item:    
        skinID=[eachDefObj for eachDefObj in cmds.listConnections(item, s=1) if cmds.nodeType(eachDefObj)=="skinCluster"][0]
        try:
            getInf=cmds.skinCluster(selObj, q=1, inf=1)
        except:
            print "cant find skincluster for "+selObj
            pass
for each in getInf[1:]:
    cmds.select(each, add=1) 
jointInf = cmds.ls(sl=1, fl=1)
for each_jnt in jointInf:
    newname = '{}_geo'.format(each_jnt)
    skinbucket = []
    get_vtx = cmds.skinCluster(skinID, e=1, siv=each_jnt)  
    for each in mc.ls(sl=1, fl=1):
        if '.v' in each:
            if mc.skinPercent(skinID, each, t=each_jnt, q=1) > inf_dropoff:
                skinbucket.append(each)
    mc.select(skinbucket, r=1)
    maya.mel.eval("ConvertSelectionToFaces;")
    grabbed_faces = mc.ls(sl=1, fl=1)
    set_for_later = []
    mc.duplicate(selObj, n=newname)
    for each in grabbed_faces:
        new_set = each.replace(each.split('.')[0], newname)
        set_for_later.append(new_set)
    mc.select(set_for_later, r=1)
    maya.mel.eval("InvertSelection;;")
    if len(mc.ls(sl=1)) > 0:
        mc.delete(mc.ls(sl=1))
        mc.delete(newname, ch=1)
        attrs = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz']
        for each in attrs:
            mc.setAttr('{}{}'.format(newname, each), l=0)
        mc.parentConstraint(each_jnt, newname, mo=1)
    else:
        mc.delete(newname)  
