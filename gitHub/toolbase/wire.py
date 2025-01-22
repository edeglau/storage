import maya.cmds as mc

dropoff = .008
arclen_limit = .006
print getsrcObj
print targetSelection_crvs




class sim_hair_functions(object):


    def setups():
        #Workaround for guide group inconsistencies: Pick the right group with the most curves
        bodyLongFurGrp = "bodyLongFur"
        headLongFurGrp = "headLongFur"
        bodyFurGrp = "bodyFur"
        headFurGrp = "headFur"

        furGrp = [bodyFurGrp] + [headFurGrp] + [bodyLongFurGrp] + [headLongFurGrp]

        #=============================================================================
        #=============================================================================

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
            getNewHair = self.create_static_fol( mc.ls("BodyColl_{}_mid_tech_grp".format(each_fur_grp))[0], static_fol_group, static_crv_group)
            mc.rename(getNewHair, "BodyColl_{}_static_hairSystem".format(each_fur_grp))
            mc.parent("BodyColl_{}_static_hairSystem".format(each_fur_grp), static_grp)
            mc.setAttr("{}.visibility".format(static_fol_group), 0)



        #=============================================================================WIRE
        getsrcObj = [(each) for each in mc.listRelatives(mc.ls("simCurves_headLongFur_crv_postTech_grp")[0], ad=1, type="nurbsCurve")  if mc.arclen(each) > arclen_limit]
        targetSelection_crvs = [(each) for each in mc.listRelatives(mc.ls("headLongFur_static_tech_crv_grp")[0], ad=1, type="nurbsCurve")  if mc.arclen(each) > arclen_limit]
        self.wire_driver_curve(getsrcObj, targetSelection_crvs, dropoff)
        
        targetSelection_crvs = [(each) for each in mc.listRelatives(mc.ls("headFur_static_tech_crv_grp")[0], ad=1, type="nurbsCurve")  if mc.arclen(each) > arclen_limit]
        self.wire_driver_curve(getsrcObj, targetSelection_crvs, dropoff)

        getsrcObj = [(each) for each in mc.listRelatives(mc.ls("simCurves_bodyLongFur_crv_postTech_grp")[0], ad=1, type="nurbsCurve")  if mc.arclen(each) > arclen_limit]
        targetSelection_crvs = [(each) for each in mc.listRelatives(mc.ls("bodyLongFur_static_tech_crv_grp")[0], ad=1, type="nurbsCurve")  if mc.arclen(each) > arclen_limit]
        self.wire_driver_curve(getsrcObj, targetSelection_crvs, dropoff)

        targetSelection_crvs = [(each) for each in mc.listRelatives(mc.ls("bodyFur_static_tech_crv_grp")[0], ad=1, type="nurbsCurve")  if mc.arclen(each) > arclen_limit]
        self.wire_driver_curve(getsrcObj, targetSelection_crvs, dropoff)
   

    def wire_driver_curve(self):
        collectmycurve_ct={}
        for each_src in getsrcObj:
            collectmycurve = []
            sourcePoint = '{}.cv[0]'.format(each_src)
            pos = mc.pointPosition(sourcePoint, w=1)
            x_pos_min, x_pos_max, y_pos_min, y_pos_max, z_pos_min, z_pos_max = pos[0]-dropoff, pos[0]+dropoff, pos[1]-dropoff, pos[1]+dropoff, pos[2]-dropoff, pos[2]+dropoff 
            for each_tgt_crv  in targetSelection_crvs:
                tgt_sourcePoint = '{}.cv[0]'.format(each_tgt_crv)
                tgt_pos = mc.pointPosition(tgt_sourcePoint, w=1) 
                if tgt_pos[0] >= x_pos_min and tgt_pos[0] <= x_pos_max and tgt_pos[1] >= y_pos_min and tgt_pos[1] <= y_pos_max and tgt_pos[2] >= z_pos_min and tgt_pos[2] <= z_pos_max:
                    collectmycurve.append(each_tgt_crv)
            newdict = {each_src:collectmycurve}
            collectmycurve_ct.update(newdict) 
        for key, value in collectmycurve_ct.items():
            if len(value)>0:
                for each_tgt in value:
                    try:
                        fnd=mc.listConnections(each_tgt, s=1, type="wire")[0]
                        if len(fnd)>0:
                            getbasecurve=[(base_item) for base_item in mc.listConnections("{}.baseWire[0]".format(fnd))]
                            fnd_crv = mc.listRelatives(getbasecurve[0], ad=1, type="shape")[0]
                            fnd_point = '{}.cv[0]'.format(fnd_crv)
                            fnd_pos = mc.pointPosition(fnd_point, w=1)
                            sourcePoint = '{}.cv[0]'.format(key)
                            src_pos = mc.pointPosition(sourcePoint, w=1)
                            tgt_point = '{}.cv[0]'.format(each_tgt)
                            tgt_pos = mc.pointPosition(tgt_point, w=1)                
                            x_fnd_pos, y_fnd_pos, z_fnd_pos = abs(tgt_pos[0]-fnd_pos[0]), abs(tgt_pos[1]-fnd_pos[1]), abs(tgt_pos[2]-fnd_pos[2])
                            x_src_pos, y_src_pos, z_src_pos = abs(tgt_pos[0]-src_pos[0]), abs(tgt_pos[1]-src_pos[1]), abs(tgt_pos[2]-src_pos[2])
                            if x_fnd_pos > x_src_pos and y_fnd_pos > y_src_pos and z_fnd_pos>z_src_pos:
                                mc.delete(fnd)
                                self.build_wire(key, each_tgt)
                    except:     
                        self.build_wire(key, each_tgt)    
  


    def build_wire(self, driver, target):
        drivertop = mc.listRelatives(driver, p=1, type= "transform")[0]
        mc.select(target, r=1)
        mc.pickWalk(direction = "up")
        grabWire = mc.wire(mc.ls(sl=1)[0], w=drivertop,n="{}_wr".format(target), gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
        mc.setAttr("{}.rotation".format(grabWire[0]), 0)
        mc.percent("{}_wr".format(target), "{}.cv[0]".format(target), v=0)
        mc.percent("{}_wr".format(target), "{}.cv[1]".format(target), v=.25)
        mc.percent("{}_wr".format(target), "{}.cv[2]".format(target), v=.5)
        mc.percent("{}_wr".format(target), "{}.cv[3]".format(target), v=.75)

  

    def create_static_fol(self, group_to_do, static_fol_group, static_crv_group):
        get_curves=[(each) for each in mc.listRelatives(group_to_do, ad=1, type="nurbsCurve")]
        mc.select(get_curves, r=1)
        mc.select('c_body_mid_scalp_geo', add=1)
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


    def cleanbase(self):
        getBase = [(item) for item in mc.ls(type = "nurbsCurve") if "geoBaseWire" in item]
        for each_bse in getBase:
            findwire=[(wire_item) for wire_item in mc.listConnections("{}.worldSpace[0]".format(each_bse)) if mc.nodeType(wire_item) == "wire"][0]
            plugin = "{}_fcl".format(findwire.split("_output_crvShape_wr")[0]) 
            try:
                mc.parent(each_bse, plugin)
            except:
                pass
