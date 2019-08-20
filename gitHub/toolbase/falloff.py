def wire_driver_curve(self, getsrcObj, targetSelection_crvs, dropoff):
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
        for each_tgt in value:
            shapetgt=mc.listRelatives(each_tgt, ad=1, type="nurbsCurve")[0]
            mc.select(clear=1)
            mc.select([each_tgt], r=1)
            try:
                fnd=mc.listConnections(shapetgt, s=1, type="wire")[0]
                if len(fnd)>0:
                    fnd_crv=[(curve_item.split("Base")[0]) for curve_item in mc.listConnections(fnd, p=1) if 'Base' in curve_item][0]
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
    grabWire = mc.wire(w=driver,n=str(target)+"_wr", gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
    mc.setAttr(grabWire[0]+".rotation", 0)
    mc.percent(str(target)+"_wr", str(target)+".cv[0]", v=0)
    mc.percent(str(target)+"_wr", str(target)+".cv[1]", v=.25)
    mc.percent(str(target)+"_wr", str(target)+".cv[2]", v=.5)
    mc.percent(str(target)+"_wr", str(target)+".cv[3]", v=.75) 
    each_found_base=[(each) for each in mc.listConnections(grabWire[0], type="shape") if "BaseWire" in each]
    each_found_follicle=[(each) for each in mc.listHistory(grabWire[0]) if mc.nodeType(each) == "follicle" if "tech_geo" in each][0]
    get_foll = [(each) for each in mc.listRelatives(each_found_follicle, p=1, type = "transform")][0]
    mc.parent(each_found_base[0], get_foll)
