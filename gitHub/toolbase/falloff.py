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
            for 
