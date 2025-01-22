import os, sys, subprocess
import re, random
from datetime import datetime
from time import gmtime, strftime
# import pymel.core as pm
import maya.cmds as cmds

# import commonUtil

import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets



# blendoptions=['blendType', 'Grp_to_Grp', "Mass_blnd", "Grp_search_blend", "Grp_search_conn", "Grp_search_blend_alias", "Grp_morph_alias", "wire_alias"]
blendoptions=['blendType', 'Grp_to_Grp', "Mass_blnd", "Grp_search_blend", "Grp_search_conn", "Grp_search_blend_alias", "wire_connect", "Corrective", "Add corrective"]


class get_set_sel_val(QtWidgets.QWidget):
    def __init__(self, trgt_ctrlrs, tgt, base):
        super(get_set_sel_val, self).__init__()
        self.initUI(trgt_ctrlrs, tgt, base)


    def initUI(self, trgt_ctrlrs, tgt, base):  
        """
        sel_obj object popup window setup
        """        
        print trgt_ctrlrs
        sel_obj = cmds.ls(sl=1)[0]
        if len(cmds.ls(sl=1))>0:
            each_attr = [(the_item) for the_item in cmds.listAttr (sel_obj, k=1) if 'visibility' not in the_item]
        else:
            each_attr = ["tx", "ty", "tz", "rx", "ry", "rz"]
        title = "Set Values for review titles"   
        self.setWindowTitle(title)
        self.layout = QtWidgets.QVBoxLayout()
        self.btnlayout = QtWidgets.QGridLayout()
        self.layout.addLayout(self.btnlayout)
        self.mirror_label = QtWidgets.QLabel("Mirror")
        self.mir_checked = QtWidgets.QCheckBox()

        self.strLayout = QtWidgets.QGridLayout()
        self.strFrame = QtWidgets.QFrame()
        self.strFrame.setLayout(self.strLayout)
        self.btnlayout.addWidget(self.strFrame)


        self.typeLayout = QtWidgets.QGridLayout()
        self.driftFrame = QtWidgets.QFrame()
        self.driftFrame.setLayout(self.typeLayout)

        self.typ_label = QtWidgets.QLabel("Type")    
        self.typeLayout.addWidget(self.typ_label)

        self.set_dir = trgt_ctrlrs
        self.dir_list = QtWidgets.QComboBox()
        self.dir_list.addItems(self.set_dir)   
        self.typeLayout.addWidget(self.dir_list)
        self.strLayout.addWidget(self.driftFrame)

        self.typ_label = QtWidgets.QLabel("TargetType")    
        self.typeLayout.addWidget(self.typ_label)

        self.set_dir =['tangentSpace']
        self.tgt_list = QtWidgets.QComboBox()
        self.tgt_list.addItems(self.set_dir)   
        self.typeLayout.addWidget(self.tgt_list)
        # self.strLayout.addWidget(self.driftFrame)
        self.set_num =[1,2,3,4,5,6,7,8,9]
        self.nm_list = QtWidgets.QComboBox()
        self.nm_list.addItems(self.set_num)   
        self.typeLayout.addWidget(self.nm_list)
        # self.strLayout.addWidget(self.driftFrame)

        self.fr_rng_layout = QtWidgets.QGridLayout()
        self.fr_rng_frame = QtWidgets.QFrame()
        self.fr_rng_frame.setLayout(self.fr_rng_layout)
        self.strLayout.addWidget(self.fr_rng_frame)


        self.ctrl_button = QtWidgets.QPushButton("Animate Controllers")
        self.ctrl_button.clicked.connect(lambda: self.build_ctrl_annot_one(trgt_ctrlrs, 'tangentSpace', tgt, base))

        self.fr_rng_layout.addWidget(self.ctrl_button)

        self.setLayout(self.layout)
        self.show()


    def build_ctrl_annot_one(self, trgt_ctrlrs, typeblend, tgt, base):
        """
        Gathers the attribute, min, max and range to animate
        """         
        print tgt
        if typeblend == 'tangentSpace':
            try:
                cmds.blendShape(trgt_ctrlrs, e=1, tangentSpace=1, t=(base, 0, tgt, 1.0), w=(0, 1.0)) 
            except:
                try:
                    cmds.blendShape(trgt_ctrlrs, e=1, tangentSpace=1, t=(base, 1, tgt, 1.0), w=(0, 1.0))
                except:
                    try:
                        cmds.blendShape(trgt_ctrlrs, e=1, tangentSpace=1, t=(base, 2, tgt, 1.0), w=(0, 1.0))
                    except:
                        try:
                            cmds.blendShape(trgt_ctrlrs, e=1, tangentSpace=1, t=(base, 3, tgt, 1.0), w=(0, 1.0))
                        except:
                            pass
class set_blendgrp_win(QtWidgets.QWidget):
    # def __init__(self): 
    def __init__(self):
        super(set_blendgrp_win, self).__init__()
        self.initUI()

    def initUI(self):    

        self.setWindowTitle("Blend Groups")

        self.myform = QtWidgets.QFormLayout()
        self.layout = QtWidgets.QGridLayout()

        self.colorSetupLayout = QtWidgets.QGridLayout()
        self.colorOverride = QtWidgets.QFrame()
        self.colorOverride.setLayout(self.colorSetupLayout)
        self.colorSetupLayout.addLayout(self.myform, 0,0,1,1)
        self.layout.addLayout(self.colorSetupLayout, 0,0,1,1)

        self.add_widgets()

        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(self.colorOverride)
        scroll.setWidgetResizable(False)
        self.layout.addWidget(scroll, 1,0,1,1)
        self.setLayout(self.layout)

    def add_widgets(self):
        self.blend_types = QtWidgets.QComboBox()
        self.blend_types.addItems(blendoptions)
        self.vertical_order_layout_ta = QtWidgets.QHBoxLayout()
        self.myform.addRow(self.vertical_order_layout_ta) 
        self.vertical_order_layout_ta.addWidget(self.blend_types)
        self.prnt_verbose_button = QtWidgets.QPushButton("Go")
        self.prnt_verbose_button.clicked.connect(lambda: self._blend_options())
        self.vertical_order_layout_ta.addWidget(self.prnt_verbose_button)     
        self.prnt_help_button = QtWidgets.QPushButton("Help")
        self.prnt_help_button.clicked.connect( lambda: self.help())
        self.vertical_order_layout_ta.addWidget(self.prnt_help_button)   

    def _blend_options(self):
        blend_load=self.blend_types
        blend_name=blend_load.currentText()
        if blend_name==blendoptions[0]:
            pass        
        if blend_name==blendoptions[1]:
            self.blendGroupToGroup()   
        if blend_name==blendoptions[2]:
            self.blendMass()   
        if blend_name==blendoptions[3]:
            self.blendSearch() 
        if blend_name==blendoptions[4]:
            self.connSearch()  
        if blend_name==blendoptions[5]:
            self.blendSearchGroups_alias() 
        if blend_name==blendoptions[6]:
            self.connWireSearch() 
        if blend_name==blendoptions[7]:
            self.corrBlnd() 
        if blend_name==blendoptions[8]:
            self.addCorrective() 
        # if blend_name==blendoptions[6]:
        #     self.blendSearchGroups_alias_morph()   
        # if blend_name==blendoptions[7]:
        #     self.WireSearchGroups_alias()  



    
#    @commonUtil.undochunk 
    def blendGroupToGroup(self):
        selObj=cmds.ls(sl=1, fl=1)
        if len(selObj) == 2:
            parentObj=selObj[0]
            childrenObj=selObj[1]
            getparentObj=cmds.listRelatives(parentObj, c=1)
            getchildObj=cmds.listRelatives(childrenObj, c=1)
            for parentItem, childItem in map(None, getparentObj,getchildObj):
                parentItemls=cmds.ls(parentItem)
                childItemls=cmds.ls(childItem)
                cmds.select(parentItemls)
                cmds.select(childItemls, add=1)
                defName=str(parentItem)+"_BShape"
                print defName
                cmds.blendShape(n=defName, w=(0, 1.0), o="world", af=1) 
        else:
            print "need to select two groups"

#    @commonUtil.undochunk 
    def corrBlnd(self):
        selObj=cmds.ls(sl=1, fl=1)
        for eachPar in selObj:
            print eachPar
            defName=str(eachPar)+"_CorBSP"
            print defName
            cmds.select(eachPar, r=1)
            cmds.blendShape(n=defName, o="world", bf=1) 

#    @commonUtil.undochunk 
    def addCorrective(self):
        #select target first and then object with blendshape
        selObj=cmds.ls(sl=1, fl=1)
        foundinput= cmds.listRelatives(selObj[-1], ad=1, type="mesh")[0]   
        trgt_ctrlrs=[eachDefObj for eachDefObj in cmds.listConnections(foundinput, s=1) if cmds.nodeType(eachDefObj)=="blendShape"]
        print trgt_ctrlrs
        inst_win = get_set_sel_val(trgt_ctrlrs, selObj[0], selObj[-1])





#    @commonUtil.undochunk 
    def blendMass(self):
        selObj=cmds.ls(sl=1, fl=1)
        if len(selObj) >1:
            for eachController, eachChild in map(None, selObj[::2], selObj[1::2]):
                parentItem=cmds.ls(eachController)
                childItem=cmds.ls(eachChild)
                cmds.select(parentItem)
                cmds.select(childItem, add=1)
                cmds.blendShape(n=str(parentItem[0])+"_BShape", w=(0, 1.0), o="world", af=1) 
        else:
            print "need to select more than one thing"

#    @commonUtil.undochunk 
    def blendSearchGroups(self):
        #only prefix
        selObj=cmds.ls(sl=1, fl=1)
        if selObj:
            pass
        else:
            print "must select a driver group and a driven group(same shortnames)"
            return
        parentObj=selObj[0]
        childrenObj=selObj[1]
        getparentObj=cmds.listRelatives(parentObj, ad=1, type="mesh")
        if getparentObj:
            pass
        else:
            getparentObj=cmds.listRelatives(parentObj, ad=1, type="nurbsCurve")
        getchildObj=cmds.listRelatives(childrenObj, ad=1, type="mesh")
        if getchildObj:
            pass
        else:
            getchildObj=cmds.listRelatives(childrenObj, ad=1, type="nurbsCurve")        for childItem  in getchildObj:
            for parentItem in getparentObj:
                if "Orig" not in str(childItem) and "Orig" not in str(parentItem):    
                    grabNameChild=cmds.listRelatives(childItem, p=1, type="transform")[0] 
                    grabNameParent=cmds.listRelatives(parentItem, p=1, type="transform")[0]      
                    if ":" in grabNameChild:
                        grabNameChild=grabNameChild.split(":")[-1]
                    if ":" in grabNameParent:
                        grabNameParent=grabNameParent.split(":")[-1]
                    grabNameChild=grabNameChild.split("Shape")[0]    
                    grabNameParent=grabNameParent.split("Shape")[0]
                    if grabNameParent in grabNameChild:
                        print "blending: "+childItem+' to '+parentItem
                        try:
                            BlendShapeName=cmds.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", o="world", w=(0, 1.0))
                        except:
                            pass
                    elif grabNameChild in grabNameParent:
                        print "blending: "+childItem+' to '+parentItem
                        try:
                            BlendShapeName=cmds.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", o="world", w=(0, 1.0))
                        except:
                            pass
                    elif grabNameChild==grabNameParent:
                        print "blending: "+childItem+' to '+parentItem
                        try:
                            BlendShapeName=cmds.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", o="world", w=(0, 1.0))
                        except:
                            pass#    @commonUtil.undochunk 
    def blendSearchGroups_alias(self):
        #only prefix
        selObj=cmds.ls(sl=1, fl=1)
        if selObj:
            pass
        else:
            print "must select a driver group and a driven group(same shortnames)"
            return
        parentObj=selObj[0]
        childrenObj=selObj[1]
        if ":" in childrenObj:
            name_blend=childrenObj.split(":")[-1]
        else:
            name_blend=childrenObj
        name_blend = name_blend+"_BSPS"
        # print parentObj
        cmds.addAttr(cmds.ls(parentObj)[0], ln=name_blend, min=0, max=1, at="double", dv=0, k=1, nn=name_blend)
        getparentObj=cmds.listRelatives(parentObj, ad=1, type="mesh")
        if getparentObj:
            getType = "isMesh"
            pass
        else:
            getparentObj=cmds.listRelatives(parentObj, ad=1, type="nurbsCurve")
            getType = "isCrv"
        getchildObj=cmds.listRelatives(childrenObj, ad=1, type="mesh")
        if getchildObj:
            pass
        else:
            getchildObj=cmds.listRelatives(childrenObj, ad=1, type="nurbsCurve")
        for childItem  in getchildObj:
            for parentItem in getparentObj:
                if "Orig" not in str(childItem) and "Orig" not in str(parentItem):    
                    grabNameChild=cmds.listRelatives(childItem, p=1, type="transform")[0] 
                    grabNameParent=cmds.listRelatives(parentItem, p=1, type="transform")[0]      
                    if ":" in grabNameChild:
                        grabNameChild=grabNameChild.split(":")[-1]
                    if ":" in grabNameParent:
                        grabNameParent=grabNameParent.split(":")[-1]
                    grabNameChild=grabNameChild.split("Shape")[0]    
                    grabNameParent=grabNameParent.split("Shape")[0]
                    if grabNameParent in grabNameChild:
                        print "attempt name match parent to child"
                        try:                            print "blending: "+childItem+' to '+ parentItem
                            # self.blendCurves_callup(parentObj, parentItem,childItem,grabNameParent)
                            if getType == "isCrv":
                                cmds.select(parentItem, r=1)
                                cmds.pickWalk(direction = "up")
                                aparent = cmds.ls(sl=1)[0]
                                getNew = cmds.duplicate(cmds.ls(sl=1)[0])
                                new_rebuilt = cmds.rebuildCurve(getNew[0], childItem, rt=2 )
                                cmds.setAttr(getNew[0]+".visibility", 0)
                                cmds.delete(new_rebuilt[0], ch=1)
                                cmds.select(getNew[0], r=1)   
                                wireName = parentItem+'_wr'
                                cmds.select(aparent, add=1)
                                cmds.CreateWrap()                                
                                # cmds.wire(w=parentItem,n=wireName, gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )                         
                                BlendShapeName=cmds.blendShape(getNew[0], childItem, n=str(grabNameParent)+"_bs", o="world", w=(0, 1.0))
                                cmds.connectAttr(parentObj+"."+name_blend, grabNameParent+"_bs."+getNew[0],  f=1)
                            else:
                                BlendShapeName=cmds.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", w=(0, 1.0))                            
                                cmds.connectAttr(parentObj+"."+name_blend, grabNameParent+"_bs."+grabNameParent+"Shape",  o="world", f=1)
                            print "succeeded: "+parentItem+' to '+childItem
                        except:
                            pass
                    elif grabNameChild in grabNameParent:
                        print "attempt name match child to parent"
                        try:
                            print "blending: "+childItem+' to '+parentItem
                            # self.blendCurves_callup(parentObj, parentItem,childItem,grabNameParent)
                            if getType == "isCrv":
                                cmds.select(parentItem, r=1)
                                cmds.pickWalk(direction = "up")
                                aparent = cmds.ls(sl=1)[0]
                                getNew = cmds.duplicate(cmds.ls(sl=1)[0])
                                new_rebuilt = cmds.rebuildCurve(getNew[0], childItem, rt=2 )
                                cmds.setAttr(getNew[0]+".visibility", 0)
                                cmds.delete(new_rebuilt[0], ch=1)
                                cmds.select(getNew[0], r=1)   
                                wireName = parentItem+'_wr'
                                cmds.select(aparent, add=1)
                                cmds.CreateWrap()          
                                BlendShapeName=cmds.blendShape(getNew[0], childItem, n=str(grabNameParent)+"_bs", o="world", w=(0, 1.0))
                                cmds.connectAttr(parentObj+"."+name_blend, grabNameParent+"_bs."+getNew[0],  f=1)
                            else:
                                BlendShapeName=cmds.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", o="world", w=(0, 1.0))
                                cmds.connectAttr(parentObj+"."+name_blend, grabNameParent+"_bs."+grabNameParent+"Shape",  f=1)                            print "succeeded: "+childItem+' to '+parentItem
                        except:
                            pass
                    elif grabNameChild==grabNameParent:
                        print "attempt exact name match"
                        try:
                            print "blending: "+childItem+' to '+parentItem
                            # self.blendCurves_callup(parentObj, parentItem,childItem,grabNameParent)
                            if getType == "isCrv":
                                cmds.select(parentItem, r=1)
                                cmds.pickWalk(direction = "up")
                                aparent = cmds.ls(sl=1)[0]
                                getNew = cmds.duplicate(cmds.ls(sl=1)[0])
                                new_rebuilt = cmds.rebuildCurve(getNew[0], childItem, rt=2 )
                                cmds.setAttr(getNew[0]+".visibility", 0)
                                cmds.delete(new_rebuilt[0], ch=1)
                                cmds.select(getNew[0], r=1)   
                                wireName = parentItem+'_wr'
                                cmds.select(aparent, add=1)
                                cmds.CreateWrap()                                    
                                # cmds.wire(w=parentItem,n=wireName, gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )                         
                                BlendShapeName=cmds.blendShape(getNew[0], childItem, n=str(grabNameParent)+"_bs", o="world", w=(0, 1.0))
                                cmds.connectAttr(parentObj+"."+name_blend, grabNameParent+"_bs."+getNew[0],  f=1)
                            else:
                                BlendShapeName=cmds.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", o="world", w=(0, 1.0))                            
                                cmds.connectAttr(parentObj+"."+name_blend, grabNameParent+"_bs."+grabNameParent+"Shape",  f=1)                            print "succeeded: "+childItem+' to '+parentItem
                        except:
                            pass
        cmds.setAttr(parentObj+"."+name_blend, 1.0)    def blendSearchGroups_alias_morph(self):
        selObj=cmds.ls(sl=1, fl=1)
        if selObj:
            pass
        else:
            print "must select a driver group and a driven group(same shortnames)"
            return
        parentObj=selObj[0]
        childrenObj=selObj[1]
        if ":" in childrenObj:
            name_blend=childrenObj.split(":")[-1]+"_BSPS"
        else:
            name_blend = childrenObj+"_BSPS"
        print name_blend
        cmds.addAttr(parentObj, ln=name_blend, min=0, max=1, at="double", k=1, nn=name_blend)
        getparentObj=cmds.listRelatives(parentObj, ad=1, type="mesh")
        if getparentObj:
            pass
        else:
            getparentObj=cmds.listRelatives(parentObj, ad=1, type="nurbsCurve")
        getchildObj=cmds.listRelatives(childrenObj, ad=1, type="mesh")
        if getchildObj:
            pass
        else:
            getchildObj=cmds.listRelatives(childrenObj, ad=1, type="nurbsCurve")
        for childItem  in getchildObj:
            for parentItem in getparentObj:
                if "Orig" not in str(childItem) and "Orig" not in str(parentItem):    
                    grabNameChild=cmds.listRelatives(childItem, p=1, type="transform")[0] 
                    grabNameParent=cmds.listRelatives(parentItem, p=1, type="transform")[0]      
                    if ":" in grabNameChild:
                        grabNameChild=grabNameChild.split(":")[-1]
                    if ":" in grabNameParent:
                        grabNameParent=grabNameParent.split(":")[-1]
                    grabNameChild=grabNameChild.split("Shape")[0]    
                    grabNameParent=grabNameParent.split("Shape")[0]
                    if grabNameParent in grabNameChild:
                        try:
                            cmds.select(childItem, r=1)
                            truchild = cmds.ls(childItem.split("Shape")[0])[0]
                            truparent = cmds.ls(parentItem.split("Shape")[0])[0]
                            getpartial = parentItem.split("Shape")[0]
                            truparentmph = getpartial+"_mph"
                            print "morphing: "+truchild+' to '+truparent
                            cmds.deformer(typ="morph", foc=False,name=truparentmph)
                            #Morph().add(truparentmph, truchild, truparent)
                            Morph().add(truparentmph, truchild, truparent, threshold=-1.0, neutral=False, 
                                force=True, transform=None, surface=False, connect=False, additive=False, 
                                inbetweens=False, combinations=False, alternativeName=None, safe=False)
                            cmds.connectAttr(parentObj+"."+name_blend, truparentmph+".envelope", f=1)
                            cmds.setAttr(truparentmph+"."+truparent, 1)
                        except:
                            pass            

#    @commonUtil.undochunk 
    def blendSearch(self):
        selObj=cmds.ls(sl=1, fl=1)
        if len(selObj) == 2: 
            if selObj:
                pass
            else:
                print "must select a driver group and a driven group(same shortnames)"
                return
            parentObj=selObj[0]
            childrenObj=selObj[1]
            getparentObj=cmds.listRelatives(parentObj, ad=1, type="mesh")
            if getparentObj:
                pass            else:
                getparentObj=cmds.listRelatives(parentObj, ad=1, type="nurbsCurve")
            getchildObj=cmds.listRelatives(childrenObj, ad=1, type="mesh")
            if getchildObj:
                pass
            else:
                getchildObj=cmds.listRelatives(childrenObj, ad=1, type="nurbsCurve")
            for childItem  in getchildObj:
                for parentItem in getparentObj:
                    if "Orig" not in str(childItem) and "Orig" not in str(parentItem):    
                        grabNameChild=cmds.listRelatives(childItem, p=1, type="transform")[0] 
                        grabNameParent=cmds.listRelatives(parentItem, p=1, type="transform")[0]      
                        if ":" in grabNameChild:
                            grabNameChild=grabNameChild.split(":")[-1]
                        if ":" in grabNameParent:
                            grabNameParent=grabNameParent.split(":")[-1]
                        grabNameChild=grabNameChild.split("Shape")[0]    
                        grabNameParent=grabNameParent.split("Shape")[0]
                        if grabNameParent in grabNameChild:
                            print "blending: "+childItem+' to '+parentItem
                            try:
                                BlendShapeName=cmds.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", w=(0, 1.0), o = "world")
                            except:
                                pass
                        elif grabNameChild in grabNameParent:
                            print "blending: "+childItem+' to '+parentItem
                            try:
                                BlendShapeName=cmds.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", w=(0, 1.0), o = "world")
                            except:
                                pass                        elif grabNameChild==grabNameParent:
                            print "blending: "+childItem+' to '+parentItem
                            try:
                                BlendShapeName=cmds.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", w=(0, 1.0),  o = "world")
                            except:
                                pass
#    @commonUtil.undochunk 
    def connWireSearch(self):
        selObj=cmds.ls(sl=1, fl=1)
        if len(selObj) == 2:        
            if selObj:
                pass
            else:
                print "must select a driver group and a driven group(same shortnames)"
                return
            # selObj=cmds.ls(sl=1, fl=1)
            parentObj=selObj[0]
            childrenObj=selObj[1]
            getparentObj=cmds.listRelatives(parentObj, ad=1, type="mesh")
            if getparentObj:
                pass
            else:
                getparentObj=cmds.listRelatives(parentObj, ad=1, type="nurbsCurve")
            getchildObj=cmds.listRelatives(childrenObj, ad=1, type="mesh")
            if getchildObj:
                pass
            else:
                getchildObj=cmds.listRelatives(childrenObj, ad=1, type="nurbsCurve")
            for childItem  in getchildObj:                for parentItem in getparentObj:
                    if "Orig" not in str(childItem) and "Orig" not in str(parentItem):    
                        grabNameChild=cmds.listRelatives(childItem, p=1, type="transform")[0] 
                        grabNameParent=cmds.listRelatives(parentItem, p=1, type="transform")[0]      
                        if ":" in grabNameChild:
                            grabNameChild=grabNameChild.split(":")[-1]
                        if ":" in grabNameParent:
                            grabNameParent=grabNameParent.split(":")[-1]
                        grabNameChild=grabNameChild.split("Shape")[0]    
                        grabNameParent=grabNameParent.split("Shape")[0]
                        if grabNameParent in grabNameChild:
                            print "connecting: "+childItem+' to '+parentItem
                            try:
                                cmds.connectAttr(parentItem+".worldSpace[0]", childItem+".create", f=1)
                            except:
                                pass
                        elif grabNameChild in grabNameParent:
                            print "connecting: "+childItem+' to '+parentItem
                            try:
                                cmds.connectAttr(parentItem+".worldSpace[0]", childItem+".create", f=1)
                            except:
                                pass
                        elif grabNameChild==grabNameParent:
                            print "connecting: "+childItem+' to '+parentItem
                            try:
                                cmds.connectAttr(parentItem+".worldSpace[0]", childItem+".create", f=1)
                            except:
                                pass
        else:
            print "need to select two groups"   

#    @commonUtil.undochunk 
    def reconnSearch(self):
        selObj=cmds.ls(sl=1, fl=1)
        if len(selObj) == 2:        
            if selObj:
                pass
            else:
                print "must select a driver group and a driven group(same shortnames)"
                return
            selObj=cmds.ls(sl=1, fl=1)
            parentObj=selObj[0]
            childrenObj=selObj[1]
            getparentObj=cmds.listRelatives(parentObj, ad=1, type="mesh")
            if getparentObj:
                pass
            else:
                getparentObj=cmds.listRelatives(parentObj, ad=1, type="nurbsCurve")
            getchildObj=cmds.listRelatives(childrenObj, ad=1, type="mesh")
            if getchildObj:
                pass
            else:
                getchildObj=cmds.listRelatives(childrenObj, ad=1, type="nurbsCurve")
            for childItem  in getchildObj:
                for parentItem in getparentObj:
                    if "Orig" not in str(childItem) and "Orig" not in str(parentItem):    
                        grabNameChild=cmds.listRelatives(childItem, p=1, type="transform")[0] 
                        grabNameParent=cmds.listRelatives(parentItem, p=1, type="transform")[0]      
                        if ":" in grabNameChild:
                            grabNameChild=grabNameChild.split(":")[-1]
                        if ":" in grabNameParent:
                            grabNameParent=grabNameParent.split(":")[-1]
                        grabNameChild=grabNameChild.split("Shape")[0]    
                        grabNameParent=grabNameParent.split("Shape")[0]
                        if grabNameParent in grabNameChild:
                            print "connecting: "+childItem+' to '+parentItem
                            try:
                                cmds.connectAttr(parentItem+".outMesh", childItem+".inMesh", f=1)
                            except:
                                pass                        elif grabNameChild in grabNameParent:
                            print "connecting: "+childItem+' to '+parentItem
                            try:
                                cmds.connectAttr(parentItem+".outMesh", childItem+".inMesh", f=1)
                            except:
                                pass
                        elif grabNameChild==grabNameParent:
                            print "connecting: "+childItem+' to '+parentItem
                            try:
                                cmds.connectAttr(parentItem+".outMesh", childItem+".inMesh", f=1)
                            except:
                                pass
        else:
            print "need to select two groups"

#    @commonUtil.undochunk 
    def connSearch(self):
        selObj=cmds.ls(sl=1, fl=1)
        if len(selObj) == 2:        
            if selObj:
                pass
            else:
                print "must select a driver group and a driven group(same shortnames)"
                return
            # selObj=cmds.ls(sl=1, fl=1)
            parentObj=selObj[0]
            childrenObj=selObj[1]
            getparentObj=cmds.listRelatives(parentObj, ad=1, type="mesh")
            if getparentObj:
                pass
            else:
                getparentObj=cmds.listRelatives(parentObj, ad=1, type="nurbsCurve")
            getchildObj=cmds.listRelatives(childrenObj, ad=1, type="mesh")
            if getchildObj:
                pass
            else:
                getchildObj=cmds.listRelatives(childrenObj, ad=1, type="nurbsCurve")            for childItem  in getchildObj:
                for parentItem in getparentObj:
                    if "Orig" not in str(childItem) and "Orig" not in str(parentItem):    
                        grabNameChild=cmds.listRelatives(childItem, p=1, type="transform")[0] 
                        grabNameParent=cmds.listRelatives(parentItem, p=1, type="transform")[0]      
                        if ":" in grabNameChild:
                            grabNameChild=grabNameChild.split(":")[-1]
                        if ":" in grabNameParent:
                            grabNameParent=grabNameParent.split(":")[-1]
                        grabNameChild=grabNameChild.split("Shape")[0]    
                        grabNameParent=grabNameParent.split("Shape")[0]
                        if grabNameParent in grabNameChild:
                            print "connecting: "+childItem+' to '+parentItem
                            try:
                                cmds.connectAttr(parentItem+".outMesh", childItem+".inMesh", f=1)
                            except:
                                pass
                        elif grabNameChild in grabNameParent:
                            print "connecting: "+childItem+' to '+parentItem
                            try:
                                cmds.connectAttr(parentItem+".outMesh", childItem+".inMesh", f=1)
                            except:
                                pass
                        elif grabNameChild==grabNameParent:
                            print "connecting: "+childItem+' to '+parentItem
                            try:
                                cmds.connectAttr(parentItem+".outMesh", childItem+".inMesh", f=1)
                            except:
                                pass
        else:
            print "need to select two groups"   

#    @commonUtil.undochunk 
    def WireSearchGroups_alias(self):
        #only prefix
        selObj=cmds.ls(sl=1, fl=1)
        if selObj:
            pass
        else:
            print "must select a driver group and a driven group(same shortnames)"
            return
        parentObj=selObj[0]
        childrenObj=selObj[1]
        if ":" in childrenObj:
            name_blend=childrenObj.split(":")[-1]
        else:
            name_blend=childrenObj
        name_blend = name_blend+"_BSPS"
        print parentObj
        cmds.addAttr(cmds.ls(parentObj)[0], ln=name_blend, min=0, max=1, at="double", dv=0, k=1, nn=name_blend)
        getparentObj=cmds.listRelatives(parentObj, ad=1, type="mesh")
        if getparentObj:
            getType = "isMesh"
            pass
        else:
            getparentObj=cmds.listRelatives(parentObj, ad=1, type="nurbsCurve")
            getType = "isCrv"
        getchildObj=cmds.listRelatives(childrenObj, ad=1, type="mesh")
        if getchildObj:
            pass
        else:
            getchildObj=cmds.listRelatives(childrenObj, ad=1, type="nurbsCurve")
        for childItem  in getchildObj:
            for parentItem in getparentObj:
                if "Orig" not in str(childItem) and "Orig" not in str(parentItem):    
                    grabNameChild=cmds.listRelatives(childItem, p=1, type="transform")[0] 
                    grabNameParent=cmds.listRelatives(parentItem, p=1, type="transform")[0]      
                    if ":" in grabNameChild:
                        grabNameChild=grabNameChild.split(":")[-1]
                    if ":" in grabNameParent:
                        grabNameParent=grabNameParent.split(":")[-1]
                    grabNameChild=grabNameChild.split("Shape")[0]    
                    grabNameParent=grabNameParent.split("Shape")[0]
                    if grabNameParent in grabNameChild:                        print "attempt name match parent to child"
                        try:
                            print "wire: "+childItem+' to '+ parentItem
                            cmds.select([childItem], r=1)   
                            cmds.pickWalk(d="up")
                            # getNode=cmds.deformer(parentItem, type="wire")
                            cmds.wire(w=parentItem,n=str(grabNameParent)+"_wr", gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
                            cmds.connectAttr(parentObj+"."+name_blend, grabNameParent+"_bs."+grabNameParent+"Shape",  f=1)
                            print "succeeded: "+parentItem+' to '+childItem
                        except:
                            pass
                    elif grabNameChild in grabNameParent:
                        print "attempt name match child to parent"
                        try:
                            print "wire: "+childItem+' to '+parentItem                   
                            cmds.select([childItem], r=1)   
                            cmds.pickWalk(d="up")
                            # getNode=cmds.deformer(parentItem, type="wire")
                            cmds.wire(w=parentItem,n=str(grabNameParent)+"_wr", gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
                            cmds.connectAttr(parentObj+"."+name_blend, grabNameParent+"_bs."+grabNameParent+"Shape",  f=1)
                            print "succeeded: "+childItem+' to '+parentItem
                        except:
                            pass
                    elif grabNameChild==grabNameParent:
                        print "attempt exact name match"
                        try:
                            print "wire: "+childItem+' to '+parentItem                        
                            cmds.select([childItem], r=1)   
                            cmds.pickWalk(d="up")
                            # getNode=cmds.deformer(parentItem, type="wire")
                            cmds.wire(w=parentItem,n=str(grabNameParent)+"_wr", gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
                            cmds.connectAttr(parentObj+"."+name_blend, grabNameParent+"_bs."+grabNameParent+"Shape",  f=1)
                            print "succeeded: "+childItem+' to '+parentItem
                        except:
                            pass
        cmds.setAttr(parentObj+"."+name_blend, 1.0)
    def help ( self):
        url="https://atlas.bydeluxe.com/confluence/display/~deglaue/Blend+Groups"
        subprocess.Popen('xdg-open "%s"' % url, stdout=subprocess.PIPE, shell=True)


inst_mkwin=set_blendgrp_win()
inst_mkwin.show()










