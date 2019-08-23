import maya.cmds as mc
 
dropoff = .008
arclen_limit = .006
getsrcObj = [(each) for each in mc.listRelatives(mc.ls("")[0], ad=1, type="nurbsCurve")  if mc.arclen(each) > arclen_limit]
targetSelection_crvs = [(each) for each in mc.listRelatives(mc.ls("")[0], ad=1, type="nurbsCurve")  if mc.arclen(each) > arclen_limit]
print getsrcObj
print targetSelection_crvs
 
 
 
 
class sim_hair_functions(object):
 
 
    def setups():
        # STATIC FOLL
        static_grp = "bodyFur_static_tech_grp"
        static_fol_group = "bodyFur_static_tech_fol_grp"
        static_crv_group = "bodyFur_static_tech_crv_grp"
        #create static group and put it into the hair sim group
        mc.select(cl=1)
        mc.Group()
        mc.rename(mc.ls(sl=1)[0], static_grp)
        mc.parent(static_grp, "hair_sim")
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
        # get_curves=[(each) for each in mc.listRelatives(mc.ls("BodyColl_bodyLongFur_mid_tech_grp")[0], ad=1, type="nurbsCurve")]
        getNewHair = self.create_static_fol(mc.ls("BodyColl_bodyLongFur_mid_tech_grp")[0], static_fol_group, static_crv_group)
        mc.rename(getNewHair, "BodyColl_bodyLongFur_static_hairSystem")
        mc.parent("BodyColl_bodyLongFur_static_hairSystem", static_grp)
        mc.setAttr(static_fol_group+".visibility", 0)
 
        # #WIRE
        getsrcObj = [(each) for each in mc.listRelatives(mc.ls("simCurves_bodyLongFur_crv_postTech_grp")[0], ad=1, type="nurbsCurve")  if mc.arclen(each) > arclen_limit]
        targetSelection_crvs = [(each) for each in mc.listRelatives(mc.ls("bodyFur_static_tech_crv_grp")[0], ad=1, type="nurbsCurve")  if mc.arclen(each) > arclen_limit]
        self.wire_driver_curve(getsrcObj, targetSelection_crvs, dropoff)
 
        #reroute the postTech curves to read from the static curves
        get_src_crvs=[(each) for each in mc.listRelatives(mc.ls("bodyFur_static_tech_crv_grp")[0], ad=1, type="nurbsCurve") if "Orig" not in each]
        get_tgt_crvs=[(each) for each in mc.listRelatives(mc.ls("BodyColl_bodyFur_mid_postTech_grp")[0], ad=1, type="nurbsCurve")]
        self.replugging(get_src_crvs, get_tgt_crvs)
 
        get_tgt_crvs=[(each) for each in mc.listRelatives(mc.ls("BodyColl_bodyLongFur_mid_postTech_grp")[0], ad=1, type="nurbsCurve")]
        self.replugging(get_src_crvs, get_tgt_crvs)
 
    
 
    def wire_driver_curve(self):
        collectmycurve_ct={}
        for each_src in getsrcObj:
            collectmycurve = []
            sourcePoint = each_src+'.cv[0]'
            pos = mc.pointPosition(sourcePoint, w=1)
            x_pos_min, x_pos_max, y_pos_min, y_pos_max, z_pos_min, z_pos_max = pos[0]-dropoff, pos[0]+dropoff, pos[1]-dropoff, pos[1]+dropoff, pos[2]-dropoff, pos[2]+dropoff
            for each_tgt_crv  in targetSelection_crvs:
                tgt_sourcePoint = each_tgt_crv+'.cv[0]'
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
                            getbasecurve=[(base_item) for base_item in mc.listConnections(fnd+".baseWire[0]")]
                            fnd_crv = mc.listRelatives(getbasecurve[0], ad=1, type="shape")[0]
                            fnd_point = fnd_crv+'.cv[0]'
                            fnd_pos = mc.pointPosition(fnd_point, w=1)
                            sourcePoint = key+'.cv[0]'
                            src_pos = mc.pointPosition(sourcePoint, w=1)
                            tgt_point = each_tgt+'.cv[0]'
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
        grabWire = mc.wire(mc.ls(sl=1)[0], w=drivertop,n=str(target)+"_wr", gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
        mc.setAttr(grabWire[0]+".rotation", 0)
        mc.percent(str(target)+"_wr", str(target)+".cv[0]", v=0)
        mc.percent(str(target)+"_wr", str(target)+".cv[1]", v=1.0)
        mc.percent(str(target)+"_wr", str(target)+".cv[2]", v=.5)
        mc.percent(str(target)+"_wr", str(target)+".cv[3]", v=.75)
 
 
 
    def create_static_fol(self, group_to_do, static_fol_group, static_crv_group):
        get_curves=[(each) for each in mc.listRelatives(group_to_do, ad=1, type="nurbsCurve")]
        mc.select(get_curves, r=1)
        mc.select('c_body_mid_scalp_geo', add=1)       
        createFoll = mm.eval('makeCurvesDynamic 2 { "1", "0", "0", "1", "0"};')
        getHair = mc.ls(sl=1)[0]
        mc.setAttr(getHair+".active", 0)
        mc.pickWalk(direction = "up")
        getHair_transform = mc.ls(sl=1)[0]
        getfolObj=mc.listConnections(getHair, s=1, type="follicle")
        for each in getfolObj:
            try:
                mc.parent(each, static_fol_group)
                mc.setAttr(each+".simulationMethod", 0)
                get_follshp = [(thing) for thing in mc.listRelatives(each, ad=1, type = "follicle")][0]
                each_found_curve_output=[(newitem) for newitem in mc.listConnections(get_follshp+".outCurve", type="nurbsCurve")][0]
                get_src_crv=[(newcurveitem) for newcurveitem in mc.listConnections(get_follshp+".startPosition", type="nurbsCurve")][0]
                fol_name = get_src_crv.split('Shape')[0]+"_static_fcl"
                out_name = get_src_crv.split('Shape')[0]+"_static_output_crv"
                mc.rename(each, fol_name)
                mc.rename(each_found_curve_output, out_name)
                mc.parent(out_name, static_crv_group)
            except:
                pass
        return getHair_transform
 
 
    def cleanbase(self):
        getBase = [(item) for item in mc.ls(type = "nurbsCurve") if "geoBaseWire" in item]
        for each_bse in getBase:
            findwire=[(wire_item) for wire_item in mc.listConnections(each_bse+".worldSpace[0]") if mc.nodeType(wire_item) == "wire"][0]
            plugin = findwire.split("_output_crvShape_wr")[0]+"_fcl"
            try:
                mc.parent(each_bse, plugin)
            except:
                pass
