def cleanbase(self):
    getBase = [(item) for item in mc.ls(type = "nurbsCurve") if "geoBaseWire" in item]
    for each_bse in getBase:
        findwire=[(wire_item) for wire_item in mc.listConnections("{}.worldSpace[0]".format(each_bse)) if mc.nodeType(wire_item) == "wire"][0]
        plugin = "{}_fcl".format(findwire.split("_output_crv_wr")[0])
        mc.parent(each_bse, plugin)
        
def create_cnstrnt(self, sel_obj, re_name, cnst_type):
    mc.select(sel_obj, r=1)
    command = 'createNConstraint {} 0;'.format(cnst_type)
    cnst = mm.eval(command)[0]
    cnstXform = mc.listRelatives(mc.ls(sl=1)[0], p=1, type= "transform")[0]
    mc.rename(cnstXform, '{}_cnst'.format(re_name))
    mc.parent('{}_cnst'.format(re_name), 'cloth_sim')
    try:
        rgd = [(each) for each in mc.listHistory(mc.ls(sl=1)[0], ag=1) if mc.nodeType(each) == "nRigid"][0]
        rgd_trfm = mc.listRelatives(rgd, p=1, type= "transform")[0]     
        mc.rename(rgd_trfm, '{}_rgd'.format(re_name))
        mc.parent('{}_rgd'.format(re_name), 'cloth_sim')  
    except:
        pass
        
self.create_rgd(sel_obj, 'drs_snk')
     
def create_rgd(self, sel_obj, re_name):
        mc.select(sel_obj, r=1)
        command = 'makeCollideNCloth;'
        cnst = mm.eval(command)[0]
        cnstXform = mc.listRelatives(mc.ls(sl=1)[0], p=1, type= "transform")[0]
        mc.rename(cnstXform, '{}_rgd'.format(re_name))
        mc.parent('{}_rgd'.format(re_name), 'cloth_sim')
        
def replugging(self, get_src_crvs, get_tgt_crvs):    
    for each_src_crv, each_tgt_crv in map(None, get_src_crvs, get_tgt_crvs):
        if each_src_crv != None and each_tgt_crv != None:
            if re.findall(r'\d+', each_src_crv)[0] == re.findall(r'\d+', each_tgt_crv)[0]:
                try:
                    getorigplug = [(each) for each in mc.listConnections("{}.create".format(mc.ls(sl=1)[0])) if "_tech_" in each]
                    if len(getorigplug)>0:
                        mc.disconnectAttr("{}.worldSpace[0]".format(getorigplug), "{}.create".format(each_tgt_crv))
                except:
                    pass
                try:
                    mc.connectAttr("{}.worldSpace[0]".format(each_src_crv), "{}.create".format(each_tgt_crv), f=1)
                except:
                    pass


import random             
    def shader_colors(self, each_item):
        name = "{}_shd".format(each_item)
        FVfirst = mc.shadingNode('lambert', asShader=True, n=name)
        getFVfirst=[FVfirst]
        setName="techanim_textures"
        if mc.objExists(setName):
            pass
        else:
            mc.sets(n=setName, co=3)
        mc.sets(getFVfirst, add=setName)
        mc.setAttr("{}.color".format(name), random.uniform(0.0,1.0), random.uniform(0.0,1.0), random.uniform(0.0,1.0), type="double3")
        mc.select(each_item)
        mc.hyperShade(assign=str(FVfirst))
        
        
    bodyLongFurGrp = "bodyLongFur"
    headLongFurGrp = "headLongFur"
    bodyFurGrp = "bodyFur"
    headFurGrp = "headFur"
 
    furGrp = [bodyFurGrp] + [headFurGrp] + [bodyLongFurGrp] + [headLongFurGrp]
 
    #=============================================================================
    #=============================================================================
    scalp_mesh = "scalpMidBody_scalp_geo"
    for each_fur_grp in furGrp:
        #=============================================================================STATIC FOLL
        static_grp = "{}_static_tech_grp".format(each_fur_grp)
        static_fol_group = "{}_static_tech_fol_grp".format(each_fur_grp)
        static_crv_group = "{}_static_tech_crv_grp".format(each_fur_grp)
        #create static group and put it into the hair sim group
        mc.select(cl=1)
        mc.Group()
        mc.rename(mc.ls(sl=1)[0], static_grp)
        mc.parent(static_grp, "hair_sim")
        mc.setAttr('{}.visibility'.format(static_grp), 0)
        #create static follicle and put it into the static group
        mc.select(cl=1)
        mc.Group()
        mc.rename(mc.ls(sl=1)[0], static_fol_group)
        mc.parent(static_fol_group, static_grp)
        #create static curve group and put it into the static group
        mc.select(cl=1)
        mc.Group()
        mc.rename(mc.ls(sl=1)[0], static_crv_group)
        mc.parent(static_crv_group, static_grp)
        mc.select(cl=1)       
        #taking the curves from the tech group for static setup
        getNewHair = self.create_static_fol( mc.ls("BodyColl_{}_mid_tech_grp".format(each_fur_grp))[0], static_fol_group, static_crv_group, scalp_mesh)
        mc.rename(getNewHair, "BodyColl_{}_static_hairSystem".format(each_fur_grp))
        mc.parent("BodyColl_{}_static_hairSystem".format(each_fur_grp), static_grp)
        mc.setAttr("{}.visibility".format(static_fol_group), 0)
 
 
 
 
def create_static_fol(self, group_to_do, static_fol_group, static_crv_group, scalp_mesh):
    get_curves=[(each) for each in mc.listRelatives(group_to_do, ad=1, type="nurbsCurve")]
    mc.select(get_curves, r=1)
    mc.select(scalp_mesh, add=1)
    createFoll = mm.eval('makeCurvesDynamic 2 { "1", "0", "0", "1", "0"};')
    getHair = mc.ls(sl=1)[0]
    mc.setAttr("{}.active".format(getHair), 0)
    mc.pickWalk(direction = "up")
    getHair_transform = mc.ls(sl=1)[0]
    getfolObj=mc.listConnections(getHair, s=1, type="follicle")
    for each in getfolObj:
        try:
            mc.parent(each, static_fol_group)
            mc.setAttr("{}.simulationMethod".format(each), 0)
            get_follshp = [(thing) for thing in mc.listRelatives(each, ad=1, type = "follicle")][0]
            each_found_curve_output=[(newitem) for newitem in mc.listConnections("{}.outCurve".format(get_follshp), type="nurbsCurve")][0]
            get_src_crv=[(newcurveitem) for newcurveitem in mc.listConnections("{}.startPosition".format(get_follshp), type="nurbsCurve")][0]
            fol_name = "{}_static_fcl".format(get_src_crv.split('Shape')[0])
            out_name = "{}_static_output_crv".format(get_src_crv.split('Shape')[0])
            mc.rename(each, fol_name)
            mc.rename(each_found_curve_output, out_name)
            mc.parent(out_name, static_crv_group)
        except:
            pass
    return getHair_transform
    
    getsrcObj = [(each) for each in mc.listRelatives(mc.ls("simCurves_headLongFur_crv_postTech_grp")[0], ad=1, type="nurbsCurve")  if mc.arclen(each) > arclen_limit]
    targetSelection_crvs = [(each) for each in mc.listRelatives(mc.ls("headLongFur_static_tech_crv_grp")[0], ad=1, type="nurbsCurve")  if mc.arclen(each) > arclen_limit]
    self.wire_driver_curve(getsrcObj, targetSelection_crvs, dropoff)

def wire_driver_curve(self, driverCurves, drivenCurves, dropoff):
    driverPnts = [mc.pointPosition('{}.cv[0]'.format(crv), w=1) for crv in driverCurves]
    drivenPnts = [mc.pointPosition('{}.cv[0]'.format(crv), w=1) for crv in drivenCurves]
    driverArray = np.array(driverPnts)[:, :3]
    drivenArray = np.array(drivenPnts)[:, :3]
    mytree = ckdtree.cKDTree(driverArray)
    distances, indexes = mytree.query(drivenArray)
    for driven, dist, driverIdx in zip(drivenCurves, distances, indexes):
        if dist < dropoff:
            self.build_wire(driverCurves[driverIdx], driven)
def build_wire(self, driver, driven):
    if not mc.nodeType(driver) == 'transform':
        driver = mc.listRelatives(driver, p=1, type= "transform")[0]
    if not mc.nodeType(driven) == 'transform':
        driven = mc.listRelatives(driven, p=1, type= "transform")[0]
    results = mc.wire(driven, w=driver, n="{}_wr".format(driven), gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
    wireDef = results[0]
    # mc.connectAttr('techRig.wiresim_OR',"{}.enable".format(wireDef))       
    mc.setAttr("{}.rotation".format(wireDef), 0)
    mc.percent(wireDef, "{}.cv[0]".format(driven), v=0)
    mc.percent(wireDef, "{}.cv[1]".format(driven), v=.25)
    mc.percent(wireDef, "{}.cv[2]".format(driven), v=.5)
    mc.percent(wireDef, "{}.cv[3]".format(driven), v=.75)
            

self.wrapDeformer("c_body_collider_wrp_tech_geo", "c_body_mid_tech_geo")
     
    def wrapDeformer(self, driver, driven):
        # WRAP
        wrp_nm = str(driven) + '_anim_geo_wrap'
        bs_nm = str(driver) + str(driven)+ 'baseWRP'
        mc.select(driven, r=1)
        mc.select(driver, add=1)
        mc.CreateWrap()
        getWrap = mc.ls(mc.listHistory(mc.ls(sl=1)[0]), type='wrap')[0]
        mc.rename(getWrap, wrp_nm)
        findwire = [(wire_item) for wire_item in mc.listConnections("{}.basePoints[0]".format(wrp_nm))][0]
        if mc.objExists(findwire) == True:
            mc.rename(findwire, bs_nm)
            try:
                mc.parent(bs_nm, 'noTransform')
            except:
                pass
        mc.select(clear=1)
        
=====================
mc.addAttr('c_body_ctrl',ln ="tether_blend",  at = 'long', dv = 0 )
mc.setAttr("c_body_ctrl.tether_blend", edit =True, channelBox = True, keyable = 0)
 
mc.blendShape("c_tether_blendshape_0001_mid","c_tether_mid", w=(0, 0.0), n = "tether_bsp")
 
mc.connectAttr('c_body_ctrl.tether_blend', 'tether_bsp.envelope')
 
grabNameChild = "c_tether_mid"
grabNameParent = "tether_wire"
name_blend = grabNameChild + "_wr"
results = mc.wire(grabNameChild, w=grabNameParent, n="{}_wr".format(grabNameChild), gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
selected = ['tether_wire.cv[0]','tether_wire.cv[1]','tether_wire.cv[2]','tether_wire.cv[3]','tether_wire.cv[4]', 'tether_wire.cv[5]' ]
for each in selected:
    mc.select(each, r=1)
    mc.cluster()
    mc.parent(mc.ls(sl=1)[0], "c_body_ctrl")
 
mc.setAttr("tether_bsp.c_tether_blendshape_0001_mid", 1)
mc.setAttr("tether_wire.visibility", 0)
mc.setAttr("c_tether_blendshape_0001_mid.visibility", 0)
mc.parent("tether_wire", "noTransform")
mc.parent("tether_wireBaseWire", "noTransform")
 
 
mc.pointConstraint("c_wire01__ctrl", "cluster1Handle", mo=1)
mc.pointConstraint("c_wire02__ctrl", "cluster2Handle", mo=1)
mc.pointConstraint("c_wire03__ctrl", "cluster3Handle", mo=1)
mc.pointConstraint("c_wire04__ctrl", "cluster4Handle", mo=1)
mc.pointConstraint("c_wire05__ctrl", "cluster5Handle", mo=1)
mc.pointConstraint("c_wire06__ctrl", "cluster6Handle", mo=1)

mc.setAttr("cluster1Handle.visibility", 0)
mc.setAttr("cluster2Handle.visibility", 0)
mc.setAttr("cluster3Handle.visibility", 0)
mc.setAttr("cluster4Handle.visibility", 0)
mc.setAttr("cluster5Handle.visibility", 0)
mc.setAttr("cluster6Handle.visibility", 0)
 
mc.setAttr("c_root_jnt.visibility", 0)
 
# mc.rename("wire_shape1Orig", "wireOrig01")
mc.rename("tether_wireBaseWire|wire_shape1Orig", "wireOrig02")

=========================

#cleanup bases

    #mesh deformers
getBase = [(item) for item in mc.ls(type="mesh") if "hiBase" in item]
for each_bse in getBase:
    findwire = [(wire_item) for wire_item in mc.listConnections("{}.worldMesh[0]".format(each_bse)) if
                mc.nodeType(wire_item) == "wrap"][0]
    if mc.objExists(findwire) == True:
        get_trsnfm_node = mc.listRelatives(each_bse, p=1, type='transform')[0]
        mc.parent(get_trsnfm_node, twk_noTransform_grp)
 
getBase = [(item) for item in mc.ls(type="mesh") if "midBase" in item]
for each_bse in getBase:
    findwire = [(wire_item) for wire_item in mc.listConnections("{}.worldMesh[0]".format(each_bse)) if
                mc.nodeType(wire_item) == "wrap"][0]
    if mc.objExists(findwire) == True:
        get_trsnfm_node = mc.listRelatives(each_bse, p=1, type='transform')[0]
        mc.parent(get_trsnfm_node, 'twk_noTransform_grp')
 #wire

def cleanbase(self):
    getBase = [(item) for item in mc.ls(type = "nurbsCurve") if "geoBaseWire" in item]
    for each_bse in getBase:
        findwire=[(wire_item) for wire_item in mc.listConnections("{}.worldSpace[0]".format(each_bse)) if mc.nodeType(wire_item) == "wire"][0]
        plugin = "{}_fcl".format(findwire.split("_output_crv_wr")[0])
        mc.parent(each_bse, plugin)
        
#finding dupes in scene:

duplicates = [(f.split("|")[-1]) for f in mc.ls(dag=1) ]
 collect_dups = [(item, count) for item, count in collections.Counter(duplicates).items() if count >1]
 return collect_dups


#precision

    #USE IF SKINNING
    self.createLocalSkeleton()
    #parent constrain only models that are skinned
    mc.parentConstraint('c_root_jnt', 'veh_f35A__model__mid', mo=1)
    
def createLocalSkeleton(self):
    '''Precision rig script'''
 
    # '''duplicate skeleton'''
    lcl_skel_grp = mc.group(name="localSkeleton_grp", empty=1)
    mc.setAttr("localSkeleton_grp.v", 0)
    # '''duplicate all joint heirarchy without constraints'''
    transform.duplicate("c_root_jnt", search='_jnt', replace='Local_jnt', hierarchy=True,
                        ignoreTypes=["transform", "parentConstraint", "aimConstraint", "orientConstraint",
                                     "annotationShape"])
    # '''move to hierarchy'''
    mc.parent("c_rootLocal_jnt", lcl_skel_grp)
    # '''Set root local to zero'''
    mc.setAttr("c_rootLocal_jnt.translateX",0)
    mc.setAttr("c_rootLocal_jnt.translateY",0)
    mc.setAttr("c_rootLocal_jnt.translateZ",0)
    # '''set list of just the children joints of the local root'''
    get_prnt = mc.ls('c_rootLocal_jnt')[0]
    jnt_locals = mc.listRelatives(get_prnt, c=1, ad=1)
    # '''connect children joints of local joint to the transform and rotate of original dependent joints'''
    for each_jnt in jnt_locals:
        if each_jnt.endswith("Local_jnt"):
            orig_jnt = each_jnt.replace("Local_jnt","_jnt")
            mc.connectAttr(orig_jnt+".translate",each_jnt+".translate")
            mc.connectAttr(orig_jnt+".rotate",each_jnt+".rotate")
        #'''remove errant joints'''
        else :
            try :
                mc.delete(each_jnt)
            except:
                print
                "already delete : " + each_jnt
 
    #'''Set root local to the cog'''
    mc.parent(lcl_skel_grp,"animGeo")
    mc.setAttr(lcl_skel_grp + ".ty", mc.getAttr('c_root_jnt.ty'))
    mc.setAttr(lcl_skel_grp + ".tz", mc.getAttr('c_root_jnt.tz'))
   # '''connect scale'''
    UNIFORMSCALE = "worldTransformSub_02_ctrl.uniformScale"
    mc.connectAttr(UNIFORMSCALE, "localSkeleton_grp.scaleX", f=1)
    mc.connectAttr(UNIFORMSCALE, "localSkeleton_grp.scaleY", f=1)
    mc.connectAttr(UNIFORMSCALE, "localSkeleton_grp.scaleZ", f=1)
    
    #multiple rivet
    self.button_attach('c_suit', ['buckle'], ['mid', 'lo'], 'buckle_rivets')
def button_attach(self, wrap_mesh_driver, buttons, lods, grp_nm):
    for each_lod in lods:
        for each_plane in buttons:
            mc.select('{}_{}_pln_geo.e[1]'.format(each_plane, each_lod), '{}_{}_pln_geo.e[2]'.format(each_plane, each_lod), r=1)
            mm.eval('rivet;')
            cnst = '{}_{}_rvt'.format(each_plane, each_lod)
            mc.rename(mc.ls(sl=1)[0], cnst)
            rvt_cnst = [(each) for each in mc.listRelatives(mc.ls(sl=1)[0], c=1) if
                        mc.nodeType(each) == 'aimConstraint']
            new_cnsrnt_nm = '{}_{}_aim_cnstrnt'.format(each_plane, each_lod)
            mc.rename(rvt_cnst, new_cnsrnt_nm)
            mc.parentConstraint(cnst, '{}_{}_jnt'.format(each_plane, each_lod), mo=1)
            self.wrapDeformer('{}_{}'.format(wrap_mesh_driver, each_lod), '{}_{}_pln_geo'.format( each_plane, each_lod))
            mc.parent('{}_{}_rvt'.format(each_plane, each_lod), '{}_{}'.format(grp_nm, each_lod))
def button_attach(self, wrap_mesh_driver, buttons, lods, grp_nm):
    for each_lod in lods:
        for each_plane in buttons:
            mc.select('{}_{}_pln_geo.e[1]'.format(each_plane, each_lod), '{}_{}_pln_geo.e[2]'.format(each_plane, each_lod), r=1)
            mm.eval('rivet;')
            cnst = '{}_{}_rvt'.format(each_plane, each_lod)
            mc.rename(mc.ls(sl=1)[0], cnst)
            rvt_cnst = [(each) for each in mc.listRelatives(mc.ls(sl=1)[0], c=1) if
                        mc.nodeType(each) == 'aimConstraint']
            new_cnsrnt_nm = '{}_{}_aim_cnstrnt'.format(each_plane, each_lod)
            mc.rename(rvt_cnst, new_cnsrnt_nm)
            mc.parentConstraint(cnst, '{}_{}_jnt'.format(each_plane, each_lod), mo=1)
            self.wrapDeformer('{}_{}'.format(wrap_mesh_driver, each_lod), '{}_{}_pln_geo'.format( each_plane, each_lod))
        mc.parent('{}_{}_rvt'.format(each_plane, each_lod), '{}_{}'.format(grp_nm, each_lod))
        mc.parent('{}_{}{}_{}_pln_geobaseWRP'.format(wr

arc_len = .4
targetSelection_crvs = [(each) for each in mc.listRelatives(mc.ls("Body_Coll_headFurDesc_crv_grp")[0], ad=1, type="nurbsCurve")  if mc.arclen(each) < arc_len]
 
mc.select( targetSelection_crvs, r=1)
 
for each in targetSelection_crvs:
    print mc.arclen(each)
#for cleaning out curves that are too long
selected = [
'Body_Coll_tailFurDesc_crv_grp]
mc.delete(selected)
arc_len = .4
targetSelection_crvs = [(mc.listRelatives(each, p=1, type="transform")[0] ) for each in mc.listRelatives(mc.ls("Body_Coll_headFurDesc_crv_grp")[0], ad=1, type="nurbsCurve")  if mc.arclen(each) < arc_len]
mc.delete( targetSelection_crvs)
 
 
simSelection = [(mc.listRelatives(each, p=1, type="transform" )) for each in mc.listRelatives(mc.ls("sim"), ad=1, type="mesh") if "rest" not in each]
    

        #blendshape
        cntrl = 'c_ulnaHook_base_ctrl'
        ctrl_attr_name = 'UlnaFix'
        driver_geo = 'r_forearmPartC_0001_hi_bsp_geo'
        driven_geo = 'r_forearmPartC_0001_hi'
        parent_grp = 'noTransform'
        parent_cnst = 'r_arm_elbow_jnt'
        def_name = '{}_bsp'.format(driver_geo)
 
        blendAnim = attrLib.addFloat(cntrl, ln=ctrl_attr_name, dv=0, min=0, max=1, k=1)
        mc.parentConstraint(cntrl, driver_geo, mo=1)
        try:
            mc.parent(driver_geo, parent_grp)
        except:
            pass
        try:
            mc.setAttr('{}.visibility'.format(driver_geo), 0)
        except:
            pass
        mc.blendShape(driver_geo, driven_geo, origin = 'world',
                      n=def_name, w=(0, 0.0))
        mc.connectAttr('{}.{}'.format(cntrl, ctrl_attr_name), '{}.{}'.format(def_name, driver_geo), f=1)

    
#xgen

    descriptionList = [xgenNS+'_moustachHair',
                        xgenNS+'_beardHair',
                        xgenNS+'_eyeBrowsHair',
                        xgenNS+'_headHair',
                        xgenNS+'_earsTipHair',
                        xgenNS+'_toesHair',
                        xgenNS+'_tailHair']
  
    for description in descriptionList:
        result=description.split('_')
        curvelist=(techRigNS+':'+result[-1]+'_simCurves_postTech_grp')
        XgenAttachGuideCurves(description,curvelist)
 
def XgenAttachGuideCurves(description,curveList=[]):
    collection = xg.palette(description)
    mc.select(curveList)
    #make sure get only nurbsCurve shapes.
    sel = mc.ls(sl=True,ni=True,dag=True,type='nurbsCurve')
    if sel is None or sel ==[]:
        mc.warning("//Fail!! no valid curve for guideAnimation Found!")
        return []
    else:
        #Set to use guideAnimation
        xg.setAttr("useCache",'true', collection,description,"SplinePrimitive")
        #set LiveMode true since attatch fresh curves
        xg.setAttr('liveMode','true', collection, description, 'SplinePrimitive')
        mc.select(sel,r=1)
        mc.xgmFindAttachment(d=description,m='SplinePrimitive')
        #mm.eval(cmd)
        print sel
        mc.warning("//curve total:%s attach to guideAnimation HairSystem"%(len(sel)))
    #end if
    return sel
    
    #box constraints
    contrnt_whole_geo = {
        'bbox_001':'c_clothesTop_0001_mid_sim_geo',
        'bbox_002':'c_clothesTop_0001_mid_sim_geo',
        }
    for index, key in enumerate(contrnt_whole_geo):
        value = contrnt_whole_geo.get(key)
        self.glue_box_callup(index, key, value)
 
def glue_box_callup(self, index, bbObj, geo):
    print bbObj, geo
    cnst_name = 'ptp_{}_{}_cnst'.format(geo, index)
    if mc.objExists('rigids') == False:
        mc.CreateEmptyGroup()
        mc.rename(mc.ls(sl=1)[0], 'rigids')
        mc.parent('rigids', 'cloth_sim')
    if mc.objExists('constraints') == False:
        mc.CreateEmptyGroup()
        mc.rename(mc.ls(sl=1)[0], 'constraints')
        mc.parent('constraints', 'cloth_sim')
    mc.select([bbObj, geo], r=1)
    command = 'select - r `VolumeComponentSelect`;'
    mm.eval(command)
    print mc.ls(sl=1)
    mm.eval('createNConstraint pointToPoint 0;')[0]
    cnstXform = mc.listRelatives(mc.ls(sl=1)[0], p=1, type="transform")[0]
    mc.rename(cnstXform, cnst_name)
    
