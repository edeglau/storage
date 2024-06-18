###intersections
import maya.cmds as cmds

name_shdr_nde = "intersection_colors"
lst_sg_node = ['intersection_colors']
shd_set_name = 'helper_textures'
msh_set_name = 'helper_mesh'


class inter_chk():
    def __init__(self):
        get_sel = cmds.ls(sl=1)
        if len(get_sel)<1:
            print ("Select two objects")
        elif len(get_sel)>2:
            print ("Select only two objects")
        else:
            self.intersect(get_sel)

    def intersect(self, get_sel):
        ##check to see if object has already been interrogated before
        nm_grp = []        for each_msh in get_sel:
            if ":" in each_msh:
                nm_prt = each_msh.split(":")[-1]
                if "|" in each_msh:
                    nw_nm_prt = each_msh.split("|")[-1]
                else:
                    nw_nm_prt = nm_prt
                nm_grp.append(nw_nm_prt)
        new_nm_cut = '_w_'.join(nm_grp)+'_cut'
        chk_rev_strt = '_w_'.join(nm_grp[::-1])+'_cut'
        if cmds.objExists(new_nm_cut) == True:
            print ("{} have already been interrogated. cancelling operation".format(get_sel))
        elif cmds.objExists(chk_rev_strt) == True:
            print ("{} have already been interrogated in reverse. cancelling operation".format(get_sel))
        else:
            name_shdr_nde = self.create_texture()
            dup_shape_grp = self.create_grp()
            msh_set_name = self.msh_set()
            ###create boolean
            cmds.duplicate(get_sel)
            new_sel = cmds.ls(sl=1)
            cmds.polyCBoolOp(new_sel[0], new_sel[1], op=3, cls = 2, ch=0,name=new_nm_cut)
            new_intersection = cmds.ls(sl=1)[0]
            cmds.rename(new_intersection, new_nm_cut)
            if cmds.polyEvaluate(new_nm_cut, v=1)>0:                try:
                    cmds.parent(new_nm_cut, dup_shape_grp)
                    cmds.select(new_nm_cut, r=1)
                    cmds.hyperShade(assign=str(name_shdr_nde))
                    cmds.sets(new_nm_cut, add=msh_set_name)
                except:
                    pass
            else:
                print ("no crossover is detected between these two shapes.")
                cmds.delete(new_nm_cut)    def msh_set(self):
        maya_msh_sets=[(each) for each in cmds.ls(typ="objectSet") if each == msh_set_name]
        if len(maya_msh_sets)<1:
            cmds.sets(n=msh_set_name, co=3)
        else:
            pass
        return msh_set_name

    def create_texture(self):
        #####create shader for boolean - brighter is better
        if cmds.objExists(name_shdr_nde) == False:
            create_shade_node = cmds.shadingNode('lambert', asShader=True, n=name_shdr_nde)
            cmds.setAttr('{}.color'.format(name_shdr_nde), 0,1,1, type='double3')
            cmds.setAttr('{}.incandescence'.format(name_shdr_nde), 0,1,1, type='double3')
        ####create a set for the shader.
        maya_sets=[(each) for each in cmds.ls(typ="objectSet") if each == shd_set_name]
        if len(maya_sets)<1:
            cmds.sets(n=shd_set_name, co=3)
            cmds.sets(lst_sg_node, add=shd_set_name)
        else:
            cmds.sets(lst_sg_node, add=shd_set_name)
        return name_shdr_nde    def create_grp(self):
        #Setup the intersection shape group
        dup_shape_grp = cmds.ls("*INTERSECTION_GRP*")
        if len(dup_shape_grp)<1:
            dup_shape_grp = cmds.CreateEmptyGroup()
            cmds.rename(dup_shape_grp, "INTERSECTION_GRP")
            dup_shape_grp = cmds.ls("*INTERSECTION_GRP*")
        else:
            dup_shape_grp = cmds.ls("*INTERSECTION_GRP*")
        return dup_shape_grp

import sys
import importlib
importlib.reload
path = '/net/homes/edeglau/scripts/tools/'
if path not in sys.path:
    sys.path.append(path)

import intersection_chk
importlib.reload(intersection_chk)
intersection_chk.inter_chk()
