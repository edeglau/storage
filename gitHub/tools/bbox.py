geo = mc.ls(techRigNS+':moustachHair*_output_crv')
    if mc.objExists('bbCube_grp') == 0:
        mc.file(get_bbbox, i=1, uns=0)
    hairconstraint_set = False
    selectCvsByVolume(geo, mc.ls(['bbCube_0001_geo','bbCube_0002_geo']))
     
    ####setting dynamic constraints###
    try:
        hairCnst = mm.eval('createNConstraint pointToPoint 0 ;')[0]
        hairCnstXform = mc.listRelatives(hairCnst,p=True)[0]
        hairCnstXform = mc.rename(hairCnstXform,techRigNS+':moustachHair_dyn_cnst')
        hairCnst = mc.listRelatives(hairCnstXform,s=True)[0]
        mc.hide(hairCnstXform)
        mc.parent(hairCnstXform,techRigNS+':nHairNodes_grp')
        hairconstraint_set = True
    except:
        hairconstraint_set = False
        print "skipped hair constraints for hair A. please check scene after build"

class BoundingBox():    @classmethod
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
        cvs = len(mc.ls(obj+'.cv[*]',fl=True))
        for i in range(0, cvs):
            objPos = mc.xform(obj+'.cv['+str(i)+']', q=True, t=True, ws=True)
            # NOTE - Optional alternative means to determine objects within volume.
            # If the center of the object is contained
            if boundingBox.ContainsPoint(objPos):
                newSelection.append("%s.cv[%s]" %(obj, i))
    # Update selection
    if newSelection:
        if not append:
            mc.select(cl=1)
        mc.select(newSelection, add=True)
    elif not append:
        mc.select(clear=True)

def selectCvsByVolume(geo, bbObjs):
    mc.select(clear=True)
    for bb in bbObjs:
        selectByVolume(geo, bb, append=True)
