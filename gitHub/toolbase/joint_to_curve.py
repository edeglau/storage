import maya.cmds as mc
import maya.mel as mm
anim_left_curve = "ear_left_anim_crv"
anim_right_curve = "ear_right_anim_crv"


if len(mc.ls(sl=1))>0:
    if "Tech" in mc.ls(sl=1)[0]:
        findTechrig = [(each) for each in mc.ls(sl=1) if "Tech" in each][0]
        if len(findTechrig)>0:
            findTechrig = findTechrig.split(":")[0]+":techRig"
            asset = findTechrig.split("Tech:")[0]
            print "found asset: {} and techrig:{}".format(asset, getTechrig)
            # self.blend_function(getTechrig) 
        else:
            print "select a techrig asset"
    else:
        print "select a techrig asset"
elif len(mc.ls('*:techRig'))>0:
    findTechrig = mc.ls('*:techRig')[0]
    asset = findTechrig.split("Tech:")[0]
    print "found asset: {} and techrig:{}".format(asset, getTechrig)
    # self.blend_function(getTechrig) 
else:
    print "no techrig in this scene"




grp = mc.ls("{}Tech:shotWorkGrp".format(asset))[0]
getbody = "{}Tech:c_body_mid_postTech_geo".format(asset)
ear_body = mc.duplicate(getbody, n="{}earbody".format(asset))[0]


getleftearbones = mc.ls('{}:l_ear_seg_01_jnt'.format(asset))
getleftearjoints = getleftearbones+sorted([(each) for each in mc.listRelatives(getleftearbones, ad=1) if mc.nodeType(each) == "joint"])

getrightearbones = ['{}:r_ear_seg_01_jnt'.format(asset)]
getrightearjoints = getrightearbones+sorted([(each) for each in mc.listRelatives(getrightearbones, ad=1) if mc.nodeType(each) == "joint"])

class curveDrivenRigBuild(object):
           
    def build_curve_rig(self, getpoint, curvename, grp):  
        '''function for building a curve rig'''
        getTopOpenGuides = getpoint
        getKnotValue = len(getTopOpenGuides)
        values = []
        for each in getTopOpenGuides:#get point values to build curve
            translate, rotate = self.locationXForm(each)
            values.append(translate)
        anim_curve = self.buildCurves(values, curvename, getKnotValue)  #build top curve    
        get_sim_crv = mc.duplicate(anim_curve, n = '{}_sim_crv'.format(anim_curve))[0]
        get_out_crv = mc.duplicate(anim_curve, n = '{}_out_crv'.format(anim_curve))[0]
        anim_jnt = self.bindClusters(getTopOpenGuides, curvename)#build controllers and the bound joints for the top lid curve(this pulls into shapes)
        hair_jnt = self.buildJointClusters(getTopOpenGuides, get_out_crv)
        return get_out_crv, hair_jnt, anim_jnt, get_sim_crv, anim_curve

    def buildCurves(self, values, name, getKnotValue):
        getKnotValueList = list(range(getKnotValue))
        getKnotValueList.insert(0, 0)
        getKnotValueList.append(getKnotValue)
        try:
            CurveMake = mc.curve(d=1, p=values)
            mc.rename(mc.ls(sl=1)[0], name)
        except:
            print "Check the name of the guide you are using to build this"   
        return name     
            
    def buildJointClusters(self, Guides, curvename):       
        '''function for skinning bones to a curve and making a curv rig'''
        mc.select(cl=1) 
        collectJoints=[]
        for each in Guides:
            getTranslation=mc.xform(each, q=1, t=1, ws=1)
            jointnames=each.split("_guide")[0]+"_hair_jnt"
            grabjnt = mc.joint(n=jointnames, p=getTranslation)     
            collectJoints.append(grabjnt)   
        mc.select(cl=1)
        return jointnames


    def bindClusters(self, Guides, curvename):       
        '''function for skinning bones to a curve and making a curv rig'''
        mc.select(cl=1) 
        collectJoints=[]
        for each in Guides:
            getTranslation=mc.xform(each, q=1, t=1, ws=1)
            jointnames=each.split("_guide")[0]+"_anim_jnt"
            mc.joint(n=jointnames, p=getTranslation)
            collectJoints.append(jointnames)
            mc.parentConstraint(each,jointnames)
            #mc.select(cl=1)
        #mc.select(cl=1)
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
        return jointnames  
      def locationXForm(self, each):
        getObj=mc.ls(each)[0]
        transform=mc.xform(each , q=True, ws=1, t=True)
        if transform==[0.0, 0.0, 0.0]:
            transformWorldMatrix=getObj.getScalePivot(ws=1)[:3]
            rotateWorldMatrix = mc.xform(each, q=True, wd=1, ra=True)
        else:
            transformWorldMatrix = mc.xform(each, q=True, ws=1, t=True)
            rotateWorldMatrix = mc.xform(each, q=True, ws=1, ro=True)
        return transformWorldMatrix, rotateWorldMatrix


inst = curveDrivenRigBuild()
get_ear_out_left, hair_jnt_left, anim_jnt_left, get_earhair_left, anim_left_curve = inst.build_curve_rig(getleftearjoints, anim_left_curve, grp)
print anim_jnt_left
inst = curveDrivenRigBuild()
get_ear_out_right, hair_jnt_right, anim_jnt_right, get_earhair_right, anim_right_curve = inst.build_curve_rig(getrightearjoints, anim_right_curve, grp)

# curveleftname = "ear_LEFT_anim_crv"

#create hair system
mc.select(cl=1)
mc.select([get_earhair_left, get_earhair_right, ear_body], r=1)
mm.eval('makeCurvesDynamic 2 { "1", "1", "1", "1", "0"};')
getleftfol = [(each) for each in mc.listHistory(get_earhair_left, f=1) if mc.nodeType(each) == "follicle"]
getrightfol = [(each) for each in mc.listHistory(get_earhair_right, f=1) if mc.nodeType(each) == "follicle"]
getfol = getleftfol + getrightfol
print getfol
for each_fol in getfol:
    print each_fol
    getoutcrv = [(each) for each in mc.listHistory(each_fol) if mc.nodeType(each) == "nurbsCurve"][0]
    getout_crv = [(each) for each in mc.listHistory(each_fol, f=1) if mc.nodeType(each) == "nurbsCurve"][0]
    getout_crvtransfrm = mc.listRelatives(getoutcrv, p=1, type="transform")[0]
    print getoutcrv
    print getout_crv
    getoutcrvtransfrm = mc.listRelatives(getoutcrv, p=1, type="transform")[0]     
    print getoutcrvtransfrm    
    getfoltransform = mc.listRelatives(each_fol, p=1, type="transform")[0]
    mc.setAttr("{}.pointLock".format(each_fol), 1)
    mc.setAttr("{}.restPose".format(each_fol), 3)
    mc.setAttr("{}.startDirection".format(each_fol), 1)    
    if "left" in getoutcrvtransfrm:    
        mc.createNode("blendCurves")
        bc_node = mc.rename(mc.ls(sl=1)[0], "left_ear_bc") 
        mc.connectAttr(get_earhair_left+"Shape.worldSpace[0]", bc_node+".inCurves[0]", f=1)
        mc.connectAttr(anim_left_curve+"Shape.worldSpace[0]", bc_node+".inCurves2[0]", f=1)
        mc.connectAttr(bc_node+".outCurves[0]", get_ear_out_left+".create", f=1)  
        #mc.rename(getoutcrvtransfrm, "{}_out_crv".format(anim_left_curve))
        #print getfoltransform, anim_jnt_left
        #mc.parent(getfoltransform, anim_jnt_left)
        mc.rename(getfoltransform, "{}_out_fcl".format(anim_left_curve))   
        mc.rename(getout_crvtransfrm, "{}_out_sim_crv".format(anim_left_curve))         
    else:        
        mc.createNode("blendCurves")
        bc_node = mc.rename(mc.ls(sl=1)[0], "right_ear_bc") 
        mc.connectAttr(get_earhair_right+"Shape.worldSpace[0]", bc_node+".inCurves[0]", f=1)
        mc.connectAttr(anim_right_curve+"Shape.worldSpace[0]", bc_node+".

getIkCurveCFx = mc.ls("{}.cv[*]".format(curvename), fl=1)
ikname = "{}_ik".format(curvename)
collectJoints[-1]
mc.ikHandle(n=ikname, sj= collectJoints[0], ee=collectJoints[-1], sol= "ikSplineSolver", ccv=0, ns=4, snc=1, tws="easeIn", rtm=1, c=curvename)
        
gethrsys = [(each) for each in mc.listHistory("{}_out_fcl".format(anim_right_curve), ac=1) if mc.nodeType(each) == "hairSystem"][0]
gethrtransform = mc.listRelatives(gethrsys, p=1, type="transform")[0]
#sort out where the hair goes
mc.parent(gethrtransform, grp)
mc.parent("{}Follicles".format(gethrtransform), grp)
mc.parent("{}OutputCurves".format(gethrtransform), grp)
mc.rename(gethrtransform, "ear_hrsys")

#sort out nucleus
get_nuc_to_remove = mc.listConnections("ear_hrsysShape", p=1, type = "nucleus")
for each in get_nuc_to_remove:
    getprop = [(item) for item in mc.listConnections(each, p=1, d=1) if "ear_hrsysShape" in item][0]
    print "disconnected {} from {}".format(getprop, each)
    try:
        mc.disconnectAttr(each, getprop)
        print "disconnected {} from {}".format(getprop, each)
    except:
        pass
mc.select("ear_hrsys", r=1)
mm.eval('assignNSolver "";')
mc.rename(mc.ls(sl=1)[0], "ear_ncls")
mc.parent("ear_ncls","{}Tech:nucleus_nodes".format(asset))
mc.connectAttr('{}Tech:techRig.Start_Frame'.format(asset),'ear_ncls.startFrame')
mc.addAttr('{}Tech:techRig'.format(asset),ln ="ear_nucleus",  at = 'long', dv = 1 )
mc.setAttr("{}Tech:techRig.ear_nucleus".format(asset), edit =True, channelBox = True, keyable = 0)
mc.connectAttr('{}Tech:techRig.ear_nucleus'.format(asset),'ear_ncls.enable')

#mc.blendShape(getbody, ear_body, n=ear_body+"_bsp", w=(0, 1.0))
