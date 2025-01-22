        geo=["c_pants_simCage_mid_sim_geo"]
        bbObjs = mc.ls('bbox_001')
        selectVtxByVolume(geo, bbObjs)
        print mc.ls(sl=1)
        mc.select('c_body_mid_coll_geo', add=1)
        cnst = mm.eval('createNConstraint pointToSurface 0;')[0]
        cnstXform = mc.listRelatives(mc.ls(sl=1)[0], p=1, type= "transform")[0]
        rgd = [(each) for each in mc.listHistory(mc.ls(sl=1)[0], ag=1) if mc.nodeType(each) == "nRigid"][0]
        rgd_trfm = mc.listRelatives(rgd, p=1, type= "transform")[0]
        mc.rename(cnstXform, 'pants_cnst')
        mc.parent('pants_cnst', 'cloth_sim')
        mc.rename(rgd_trfm, 'pants_rgd')
        mc.parent('pants_rgd', 'cloth_sim')
 
        mc.delete('bbCube_grp')
 
        geo=["c_pants_simCage_mid_sim_geo"]
        bbObjs = mc.ls('bbox_001')
        selectVtxByVolume(geo, bbObjs)
        print mc.ls(sl=1)
        mc.select('c_body_mid_coll_geo', add=1)
        cnst = mm.eval('createNConstraint pointToSurface 0;')[0]
        cnstXform = mc.listRelatives(mc.ls(sl=1)[0], p=1, type= "transform")[0]
        rgd = [(each) for each in mc.listHistory(mc.ls(sl=1)[0], ag=1) if mc.nodeType(each) == "nRigid"][0]
        rgd_trfm = mc.listRelatives(rgd, p=1, type= "transform")[0]
        mc.rename(cnstXform, 'pants_cnst')
        mc.parent('pants_cnst', 'cloth_sim')
        mc.rename(rgd_trfm, 'pants_rgd')
        mc.parent('pants_rgd', 'cloth_sim')
 
        mc.delete('bbCube_grp')
 
 
 
 
class BoundingBox():
    @classmethod
    def FromShape(cls, shapeObj):
   
        boundingBox = BoundingBox()
        bb = mc.xform(shapeObj, q=True, bb=True)
        boundingBox.minX = bb[0]
        boundingBox.minY = bb[1]
        boundingBox.minZ = bb[2]
        boundingBox.maxX = bb[3]
        boundingBox.maxY = bb[4]
        boundingBox.maxZ = bb[5]
        return boundingBox
   
    def ContainsPoint(self, point):
        return (point[0] > self.minX and point[0] < self.maxX and point[1] > self.minY and point[1] < self.maxY and point[2] > self.minZ and point[2] < self.maxZ)
   
    def ContainsShape(self, shape):
        shapeBB = BoundingBox.FromShape(shape)
        return (shapeBB.minX < self.maxX and shapeBB.maxX > self.minX) and (shapeBB.minY < self.maxY and shapeBB.maxY > self.minY) and(shapeBB.maxZ < self.maxZ and shapeBB.maxZ > self.minZ)
    
def selectByVolume(geos, bbObj, append=False):
    # Create bounding box class from object
    boundingBox = BoundingBox.FromShape(bbObj)
    if isinstance(geos, basestring):
        geos = [geos]
    # Compare against every object in our scene to determine what is in our volume
    newSelection = list()
    for obj in geos:
        # get the vertices
        # vertices = mc.polyEvaluate(obj, vertex=True)
        cvs = len(mc.ls(obj+'.vtx[*]',fl=True))
        for i in range(0, cvs):
            objPos = mc.xform(obj+'.vtx['+str(i)+']', q=True, t=True, ws=True)
            # NOTE - Optional alternative means to determine objects within volume.
            # If the center of the object is contained
            if boundingBox.ContainsPoint(objPos):
                newSelection.append("%s.vtx[%s]" %(obj, i))
    # Update selection
    if newSelection:
        if not append:
            mc.select(cl=1)
        mc.select(newSelection, add=True)
    elif not append:
        mc.select(clear=True)
  
def selectVtxByVolume(geo, bbObjs):
    mc.select(clear=True)
    for bb in bbObjs:
        selectByVolume(geo, bb, append=True)
