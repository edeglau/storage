attrsToEdit = ["tx", "tz", "rx", "rz"]
for each in attrsToEdit:
    mc.setAttr("c_topBlades__ctrl.{}".format(each), l=1)
    mc.setAttr("c_topBlades__ctrl.{}".format(each), cb=0, keyable =0)
attrsToEdit = ["tx", "ty", "tz", "ry", "rz"]
for each in attrsToEdit:
    mc.setAttr("c_backBlades__ctrl.{}".format(each), l=1)
    mc.setAttr("c_backBlades__ctrl.{}".format(each), cb=0, keyable =0)
    
   
mc.addAttr('c_topBlades__ctrl',ln ="curvature",  at = 'long', dv = 0 )
mc.setAttr("c_topBlades__ctrl.curvature", edit =True, channelBox = True, keyable = 0)
 
defNames_bnd = ["fTopBladeBend", "bTopBladeBend", "rTopBladeBend", "lTopBladeBend"]
for def_name_bnd in defNames_bnd:
    mc.select("c_propeller_001_mid", r=1)
    mc.nonLinear(type = "bend", lowBound = 0, highBound = 1, curvature = 0)
    print "applied bend {}".format(def_name_bnd)
    mc.rename(mc.ls(sl=1)[0], def_name_bnd)
    get_transform = mc.ls(sl=1)[0]
    getChild = [(each) for each in mc.listRelatives(def_name_bnd, ad=1)][0]
    getdef = [(each) for each in mc.listConnections(getChild, s=1) if mc.nodeType(each) == "nonLinear"][0]
    mc.rename(getdef, "{}_def".format(def_name_bnd))
    userScriptDir = os.path.join(os.path.dirname("///mWeights/"), 'nonLinear')
    wt="{}_def".format(def_name_bnd)
    mWeights.load(wt, filePath=os.path.join(userScriptDir, '%s.wts' % wt))
    mc.parent( def_name_bnd, "c_topBlades__ctrl")
    mc.connectAttr('c_topBlades__ctrl.curvature', '{}_def.curvature'.format(def_name_bnd))
mc.setAttr("fTopBladeBend.rx", 90)
mc.setAttr("fTopBladeBend.rz", 90)
mc.setAttr("bTopBladeBend.rx", -90)
mc.setAttr("bTopBladeBend.rz", 90)
mc.setAttr("rTopBladeBend.rz", 90)
mc.setAttr("lTopBladeBend.ry", 180)
mc.setAttr("lTopBladeBend.rz", -90)
mc.setAttr("bTopBladeBend.v", 0)
mc.setAttr("fTopBladeBend.v", 0)
mc.setAttr("rTopBladeBend.v", 0)
mc.setAttr("lTopBladeBend.v", 0)


mc.addAttr('c_topBlades__ctrl',ln ="startAngle",  at = 'long', dv = 0 )
mc.setAttr("c_topBlades__ctrl.startAngle", edit =True, channelBox = True, keyable = 0)
 
mc.addAttr('c_topBlades__ctrl',ln ="endAngle",  at = 'long', dv = 0 )
mc.setAttr("c_topBlades__ctrl.endAngle", edit =True, channelBox = True, keyable = 0)
 
defNames_twist = ["fTopBladeTwst", "bTopBladeTwst", "rTopBladeTwst", "lTopBladeTwst"]
for def_name_twst in defNames_twist:
    mc.select("c_propeller_001_mid", r=1)
    mc.nonLinear(type = "twist", lowBound = 0, highBound = 1)
    print "applied twist {}".format(def_name_twst)
    mc.rename(mc.ls(sl=1)[0], def_name_twst)
    get_transform = mc.ls(sl=1)[0]
    getChild = [(each) for each in mc.listRelatives(def_name_twst, ad=1)][0]
    getdef = [(each) for each in mc.listConnections(getChild, s=1) if mc.nodeType(each) == "nonLinear"][0]
    mc.rename(getdef, "{}_def".format(def_name_twst))
    userScriptDir = os.path.join(os.path.dirname("///mWeights/"), 'nonLinear')
    wt="{}_def".format(def_name_twst)
    mWeights.load(wt, filePath=os.path.join(userScriptDir, '%s.wts' % wt))
    mc.parent( def_name_twst, "c_topBlades__ctrl")
    mc.connectAttr('c_topBlades__ctrl.startAngle', '{}_def.startAngle'.format(def_name_twst))
    mc.connectAttr('c_topBlades__ctrl.endAngle', '{}_def.endAngle'.format(def_name_twst))
mc.setAttr("bTopBladeTwst.rx", -90)
mc.setAttr("bTopBladeTwst.v", 0)
mc.setAttr("fTopBladeTwst.rx", 90)
mc.setAttr("fTopBladeTwst.v", 0)
mc.setAttr("rTopBladeTwst.rz", 90)
mc.setAttr("rTopBladeTwst.v", 0)
mc.setAttr("lTopBladeTwst.rz", -90)
mc.setAttr("lTopBladeTwst.v", 0)
