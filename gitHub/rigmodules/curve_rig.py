import maya.cmds as mc

class curveRigBuild(object):
    def __init__(self):
        self.build_curve_rig()     
        
    def build_curve_rig(self):   
        '''function for building a curve rig'''
        getTopOpenGuides = mc.ls(sl=1)
        getKnotValue = len(getTopOpenGuides)
        curvename =  "A_crv"
        values = []
        for each in getTopOpenGuides:#get point values to build curve
            translate, rotate = self.locationXForm(each)
            values.append(translate)
        self.buildCurves(values, curvename, getKnotValue)  #build top curve    
        self.buildJointClusters(getTopOpenGuides, curvename)#build controllers and the bound joints for the top lid curve(this pulls into shapes)
        getRigGrp=mc.group( em=True, name='_Rig' )
        #mc.parent("01_Clst_jnt", getRigGrp)
        mc.parent("A_crv", getRigGrp)
       
    def buildCurves(self, values, name, getKnotValue):
        getKnotValueList = list(range(getKnotValue))
        getKnotValueList.insert(0, 0)
        getKnotValueList.append(getKnotValue)
        try:
            CurveMake = mc.curve(n=name, d=1, p=values)
        except:
            print "Check the name of the guide you are using to build this"        
    def buildJointClusters(self, Guides, curvename):       
        '''function for skinning bones to a curve and making a curv rig'''
        mc.select(cl=1) 
        collectJoints=[]
        for each in Guides:
            getTranslation=mc.xform(each, q=1, t=1, ws=1)
            jointnames=each.split("_guide")[0]+"Clst_jnt"
            grabjnt = mc.joint(n=jointnames, p=getTranslation)     
            collectJoints.append(grabjnt)   
        mc.select(cl=1)
        getIKCurveCVs=mc.ls(curvename+".cv[*]", fl=1)
        for each , bone in map(None, getIKCurveCVs[:-1], collectJoints[:-1]):
            mc.select(clear=1)
            mc.select(each)
            mc.select( bone, add=1)
            mc.bindSkin(each, bone, tsb=1)
        getlastjoint=collectJoints[-1:] 
        getverylastCVs=getIKCurveCVs[-1:]
        for each in getverylastCVs:
            mc.select(each) 
            createdCluster=mc.cluster()
            mc.select(each, add=1)    
            mc.parent(createdCluster, getlastjoint)  
 
    def locationXForm(self, each):
        getObj=mc.ls(each)[0]
        #transform=getObj.getTranslation()
        transform=mc.xform(each , q=True, ws=1, t=True)
        if transform==[0.0, 0.0, 0.0]:
            transformWorldMatrix=getObj.getScalePivot(ws=1)[:3]
            #transformWorldMatrix = mc.xform(each, q=True, wd=1, sp=True)
            rotateWorldMatrix = mc.xform(each, q=True, wd=1, ra=True)
        else:
#            transformWorldMatrix=getObj.getScalePivot(ws=1)[:3]
            transformWorldMatrix = mc.xform(each, q=True, ws=1, t=True)
            rotateWorldMatrix = mc.xform(each, q=True, ws=1, ro=True)
        return transformWorldMatrix, rotateWorldMatrix
                    
inst = curveRigBuild()
