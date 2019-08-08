
import os, sys, subprocess
import re, random
from datetime import datetime
from time import gmtime, strftime

import maya.cmds as mc


checkHoudini = os.getenv("HOUDINI_VERSION")

checkMaya = os.getenv("REZ_MAYA_VERSION")


if checkMaya != None:
    import mrig_pyqt
    from mrig_pyqt import QtCore, QtGui, QtWidgets
    from mrig_pyqt.QtCore import SIGNAL


if checkHoudini != None:
    import hutil
    from hutil.Qt import QtCore, QtWidgets, QtWidgets
    from hutil.Qt.QtCore import SIGNAL


blendoptions=['blendType', 'Grp_to_Grp', "Mass_blnd", "Grp_search_blend", "Grp_search_conn", "Grp_search_blend_alias", "Grp_morph_alias", "wire_alias"]

class set_blendgrp_win(QtWidgets.QWidget):
    # def __init__(self): 
    def __init__(self):
        super(set_blendgrp_win, self).__init__()
        self.initUI()

    def initUI(self):    

        self.setWindowTitle("set colors")

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
        self.color_dial = QtWidgets.QComboBox()
        self.color_dial.addItems(blendoptions)
        self.vertical_order_layout_ta = QtWidgets.QHBoxLayout()
        self.myform.addRow(self.vertical_order_layout_ta) 
        self.vertical_order_layout_ta.addWidget(self.color_dial)
        self.prnt_verbose_button = QtWidgets.QPushButton("Go")
        self.connect(self.prnt_verbose_button, SIGNAL("clicked()"),
                    lambda: self.create_rgb())
        self.vertical_order_layout_ta.addWidget(self.prnt_verbose_button)     



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
            self.blendSearchGroups_alias_morph()   
        if blend_name==blendoptions[7]:
            self.WireSearchGroups_alias()  

    def blendGroupToGroup(self):
        selObj=mc.ls(sl=1, fl=1)
        if len(selObj) == 2:
            parentObj=selObj[0]
            childrenObj=selObj[1]
            getparentObj=mc.listRelatives(parentObj, c=1)
            getchildObj=mc.listRelatives(childrenObj, c=1)
            for parentItem, childItem in map(None, getparentObj,getchildObj):
                parentItemls=mc.ls(parentItem)
                childItemls=mc.ls(childItem)
                mc.select(parentItemls)
                mc.select(childItemls, add=1)
                defName=str(parentItem)+"_BShape"
                print defName
                mc.blendShape(n=defName, w=(0, 1.0), o="world", af=1) 
        else:
            print "need to select two groups"

    def blendMass(self):
        selObj=mc.ls(sl=1, fl=1)
        if len(selObj) >1:
            for eachController, eachChild in map(None, selObj[::2], selObj[1::2]):
                parentItem=mc.ls(eachController)
                childItem=mc.ls(eachChild)
                mc.select(parentItem)
                mc.select(childItem, add=1)
                mc.blendShape(n=str(parentItem[0])+"_BShape", w=(0, 1.0), o="world", af=1) 
        else:
            print "need to select more than one thing"

    def blendSearchGroups(self):
        #only prefix
        selObj=mc.ls(sl=1, fl=1)
        if selObj:
            pass
        else:
            print "must select a driver group and a driven group(same shortnames)"
            return
        parentObj=selObj[0]
        childrenObj=selObj[1]
        getparentObj=mc.listRelatives(parentObj, ad=1, type="mesh")
        if getparentObj:
            pass
        else:
            getparentObj=mc.listRelatives(parentObj, ad=1, type="nurbsCurve")
        getchildObj=mc.listRelatives(childrenObj, ad=1, type="mesh")
        if getchildObj:
            pass
        else:
            getchildObj=mc.listRelatives(childrenObj, ad=1, type="nurbsCurve")
        for childItem  in getchildObj:
            for parentItem in getparentObj:
                if "Orig" not in str(childItem) and "Orig" not in str(parentItem):    
                    grabNameChild=str(pm.PyNode(childItem).nodeName())
                    grabNameParent=str(pm.PyNode(parentItem).nodeName())     
                    if ":" in grabNameChild:
                        grabNameChild=grabNameChild.split(":")[-1]
                    if ":" in grabNameParent:
                        grabNameParent=grabNameParent.split(":")[-1]
                    grabNameChild=grabNameChild.split("Shape")[0]    
                    grabNameParent=grabNameParent.split("Shape")[0]
                    if grabNameParent in grabNameChild:
                        print "blending: "+childItem+' to '+parentItem
                        try:
                            BlendShapeName=mc.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", o="world", w=(0, 1.0))
                        except:
                            pass
                    elif grabNameChild in grabNameParent:
                        print "blending: "+childItem+' to '+parentItem
                        try:
                            BlendShapeName=mc.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", o="world", w=(0, 1.0))
                        except:
                            pass
                    elif grabNameChild==grabNameParent:
                        print "blending: "+childItem+' to '+parentItem
                        try:
                            BlendShapeName=mc.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", o="world", w=(0, 1.0))
                        except:
                            pass




    def blendSearchGroups_alias(self):
        #only prefix
        selObj=mc.ls(sl=1, fl=1)
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
        mc.addAttr(mc.ls(parentObj)[0], ln=name_blend, min=0, max=1, at="double", dv=0, k=1, nn=name_blend)
        getparentObj=mc.listRelatives(parentObj, ad=1, type="mesh")
        if getparentObj:
            getType = "isMesh"
            pass
        else:
            getparentObj=mc.listRelatives(parentObj, ad=1, type="nurbsCurve")
            getType = "isCrv"
        getchildObj=mc.listRelatives(childrenObj, ad=1, type="mesh")
        if getchildObj:
            pass
        else:
            getchildObj=mc.listRelatives(childrenObj, ad=1, type="nurbsCurve")
        for childItem  in getchildObj:
            for parentItem in getparentObj:
                if "Orig" not in str(childItem) and "Orig" not in str(parentItem):    
                    grabNameChild=str(pm.PyNode(childItem).nodeName())
                    grabNameParent=str(pm.PyNode(parentItem).nodeName())     
                    if ":" in grabNameChild:
                        grabNameChild=grabNameChild.split(":")[-1]
                    if ":" in grabNameParent:
                        grabNameParent=grabNameParent.split(":")[-1]
                    grabNameChild=grabNameChild.split("Shape")[0]    
                    grabNameParent=grabNameParent.split("Shape")[0]
                    if grabNameParent in grabNameChild:
                        print "attempt name match parent to child"
                        try:
                            print "blending: "+childItem+' to '+ parentItem
                            # self.blendCurves_callup(parentObj, parentItem,childItem,grabNameParent)
                            if getType == "isCrv":
                                mc.select(parentItem, r=1)
                                mc.pickWalk(direction = "up")
                                aparent = mc.ls(sl=1)[0]
                                getNew = mc.duplicate(mc.ls(sl=1)[0])
                                new_rebuilt = mc.rebuildCurve(getNew[0], childItem, rt=2 )
                                mc.setAttr(getNew[0]+".visibility", 0)
                                mc.delete(new_rebuilt[0], ch=1)
                                mc.select(getNew[0], r=1)   
                                wireName = parentItem+'_wr'
                                mc.select(aparent, add=1)
                                mc.CreateWrap()                                
                                # mc.wire(w=parentItem,n=wireName, gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )                         
                                BlendShapeName=mc.blendShape(getNew[0], childItem, n=str(grabNameParent)+"_bs", w=(0, 1.0))
                                mc.connectAttr(parentObj+"."+name_blend, grabNameParent+"_bs."+getNew[0],  f=1)
                            else:
                                BlendShapeName=mc.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", w=(0, 1.0))                            
                                mc.connectAttr(parentObj+"."+name_blend, grabNameParent+"_bs."+grabNameParent+"Shape",  f=1)
                            # if getType == "isCrv":
                            #     new_rebuilt = mc.rebuildCurve(parentItem, childItem, rt=2 )
                            # else:
                            #     pass
                            # BlendShapeName=mc.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", w=(0, 1.0))
                            print "succeeded: "+parentItem+' to '+childItem
                        except:
                            pass
                    elif grabNameChild in grabNameParent:
                        print "attempt name match child to parent"
                        try:
                            print "blending: "+childItem+' to '+parentItem
                            # self.blendCurves_callup(parentObj, parentItem,childItem,grabNameParent)
                            if getType == "isCrv":
                                mc.select(parentItem, r=1)
                                mc.pickWalk(direction = "up")
                                aparent = mc.ls(sl=1)[0]
                                getNew = mc.duplicate(mc.ls(sl=1)[0])
                                new_rebuilt = mc.rebuildCurve(getNew[0], childItem, rt=2 )
                                mc.setAttr(getNew[0]+".visibility", 0)
                                mc.delete(new_rebuilt[0], ch=1)
                                mc.select(getNew[0], r=1)   
                                wireName = parentItem+'_wr'
                                mc.select(aparent, add=1)
                                mc.CreateWrap()                                    
                                # mc.wire(w=parentItem,n=wireName, gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )                        
                                BlendShapeName=mc.blendShape(getNew[0], childItem, n=str(grabNameParent)+"_bs", w=(0, 1.0))
                                mc.connectAttr(parentObj+"."+name_blend, grabNameParent+"_bs."+getNew[0],  f=1)
                            else:
                                BlendShapeName=mc.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", w=(0, 1.0))
                                mc.connectAttr(parentObj+"."+name_blend, grabNameParent+"_bs."+grabNameParent+"Shape",  f=1)
                            # if getType == "isCrv":
                            #     new_rebuilt = mc.rebuildCurve(parentItem, childItem, rt=2 )
                            # else:
                            #     pass                            
                            # BlendShapeName=mc.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", w=(0, 1.0))
                            print "succeeded: "+childItem+' to '+parentItem
                        except:
                            pass
                    elif grabNameChild==grabNameParent:
                        print "attempt exact name match"
                        try:
                            print "blending: "+childItem+' to '+parentItem
                            # self.blendCurves_callup(parentObj, parentItem,childItem,grabNameParent)
                            if getType == "isCrv":
                                mc.select(parentItem, r=1)
                                mc.pickWalk(direction = "up")
                                aparent = mc.ls(sl=1)[0]
                                getNew = mc.duplicate(mc.ls(sl=1)[0])
                                new_rebuilt = mc.rebuildCurve(getNew[0], childItem, rt=2 )
                                mc.setAttr(getNew[0]+".visibility", 0)
                                mc.delete(new_rebuilt[0], ch=1)
                                mc.select(getNew[0], r=1)   
                                wireName = parentItem+'_wr'
                                mc.select(aparent, add=1)
                                mc.CreateWrap()                                    
                                # mc.wire(w=parentItem,n=wireName, gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )                         
                                BlendShapeName=mc.blendShape(getNew[0], childItem, n=str(grabNameParent)+"_bs", w=(0, 1.0))
                                mc.connectAttr(parentObj+"."+name_blend, grabNameParent+"_bs."+getNew[0],  f=1)
                            else:
                                BlendShapeName=mc.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", w=(0, 1.0))                            
                                mc.connectAttr(parentObj+"."+name_blend, grabNameParent+"_bs."+grabNameParent+"Shape",  f=1)
                            # if getType == "isCrv":
                            #     new_rebuilt = mc.rebuildCurve(parentItem, childItem, rt=2 )
                            # else:
                            #     pass                            
                            # BlendShapeName=mc.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", w=(0, 1.0))
                            print "succeeded: "+childItem+' to '+parentItem
                        except:
                            pass
        mc.setAttr(parentObj+"."+name_blend, 1.0)



    def blendSearchGroups_alias_morph(self):
        #only prefix
        # mc.select("rocket1Tech:c_bodySuit_simCage_hi_restShape_geo")
        # mc.deformer(typ="morph", foc=False,name='preWrinklesMorph')
        # mc.setAttr("preWrinklesMorph.preWrinkles",0.5)    
        selObj=mc.ls(sl=1, fl=1)
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
        mc.addAttr(parentObj, ln=name_blend, min=0, max=1, at="double", k=1, nn=name_blend)
        getparentObj=mc.listRelatives(parentObj, ad=1, type="mesh")
        if getparentObj:
            pass
        else:
            getparentObj=mc.listRelatives(parentObj, ad=1, type="nurbsCurve")
        getchildObj=mc.listRelatives(childrenObj, ad=1, type="mesh")
        if getchildObj:
            pass
        else:
            getchildObj=mc.listRelatives(childrenObj, ad=1, type="nurbsCurve")
        for childItem  in getchildObj:
            for parentItem in getparentObj:
                if "Orig" not in str(childItem) and "Orig" not in str(parentItem):    
                    grabNameChild=str(pm.PyNode(childItem).nodeName())
                    grabNameParent=str(pm.PyNode(parentItem).nodeName())     
                    if ":" in grabNameChild:
                        grabNameChild=grabNameChild.split(":")[-1]
                    if ":" in grabNameParent:
                        grabNameParent=grabNameParent.split(":")[-1]
                    grabNameChild=grabNameChild.split("Shape")[0]    
                    grabNameParent=grabNameParent.split("Shape")[0]
                    if grabNameParent in grabNameChild:
                        try:
                            mc.select(childItem, r=1)
                            truchild = mc.ls(childItem.split("Shape")[0])[0]
                            truparent = mc.ls(parentItem.split("Shape")[0])[0]
                            getpartial = parentItem.split("Shape")[0]
                            truparentmph = getpartial+"_mph"
                            print "morphing: "+truchild+' to '+truparent
                            mc.deformer(typ="morph", foc=False,name=truparentmph)
                            #Morph().add(truparentmph, truchild, truparent)
                            Morph().add(truparentmph, truchild, truparent, threshold=-1.0, neutral=False, force=True, transform=None, surface=False, connect=False, additive=False, inbetweens=False, combinations=False, alternativeName=None, safe=False)
                            mc.connectAttr(parentObj+"."+name_blend, truparentmph+".envelope", f=1)
                            mc.setAttr(truparentmph+"."+truparent, 1)
                        except:
                            pass            

    def blendSearch(self):
        selObj=mc.ls(sl=1, fl=1)
        if len(selObj) == 2: 
            if selObj:
                pass
            else:
                print "must select a driver group and a driven group(same shortnames)"
                return
            parentObj=selObj[0]
            childrenObj=selObj[1]
            getparentObj=mc.listRelatives(parentObj, ad=1, type="mesh")
            if getparentObj:
                pass
            else:
                getparentObj=mc.listRelatives(parentObj, ad=1, type="nurbsCurve")
            getchildObj=mc.listRelatives(childrenObj, ad=1, type="mesh")
            if getchildObj:
                pass
            else:
                getchildObj=mc.listRelatives(childrenObj, ad=1, type="nurbsCurve")
            for childItem  in getchildObj:
                for parentItem in getparentObj:
                    if "Orig" not in str(childItem) and "Orig" not in str(parentItem):    
                        grabNameChild=str(pm.PyNode(childItem).nodeName())
                        grabNameParent=str(pm.PyNode(parentItem).nodeName())     
                        if ":" in grabNameChild:
                            grabNameChild=grabNameChild.split(":")[-1]
                        if ":" in grabNameParent:
                            grabNameParent=grabNameParent.split(":")[-1]
                        grabNameChild=grabNameChild.split("Shape")[0]    
                        grabNameParent=grabNameParent.split("Shape")[0]
                        if grabNameParent in grabNameChild:
                            print "blending: "+childItem+' to '+parentItem
                            try:
                                BlendShapeName=mc.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", w=(0, 1.0), o = "world")
                            except:
                                pass
                        elif grabNameChild in grabNameParent:
                            print "blending: "+childItem+' to '+parentItem
                            try:
                                BlendShapeName=mc.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", w=(0, 1.0), o = "world")
                            except:
                                pass
                        elif grabNameChild==grabNameParent:
                            print "blending: "+childItem+' to '+parentItem
                            try:
                                BlendShapeName=mc.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", w=(0, 1.0),  o = "world")
                            except:
                                pass

    def reconnSearch(self):
        selObj=mc.ls(sl=1, fl=1)
        if len(selObj) == 2:        
            if selObj:
                pass
            else:
                print "must select a driver group and a driven group(same shortnames)"
                return
            selObj=mc.ls(sl=1, fl=1)
            parentObj=selObj[0]
            childrenObj=selObj[1]
            getparentObj=mc.listRelatives(parentObj, ad=1, type="mesh")
            if getparentObj:
                pass
            else:
                getparentObj=mc.listRelatives(parentObj, ad=1, type="nurbsCurve")
            getchildObj=mc.listRelatives(childrenObj, ad=1, type="mesh")
            if getchildObj:
                pass
            else:
                getchildObj=mc.listRelatives(childrenObj, ad=1, type="nurbsCurve")
            for childItem  in getchildObj:
                for parentItem in getparentObj:
                    if "Orig" not in str(childItem) and "Orig" not in str(parentItem):    
                        grabNameChild=str(pm.PyNode(childItem).nodeName())
                        grabNameParent=str(pm.PyNode(parentItem).nodeName())     
                        if ":" in grabNameChild:
                            grabNameChild=grabNameChild.split(":")[-1]
                        if ":" in grabNameParent:
                            grabNameParent=grabNameParent.split(":")[-1]
                        grabNameChild=grabNameChild.split("Shape")[0]    
                        grabNameParent=grabNameParent.split("Shape")[0]
                        if grabNameParent in grabNameChild:
                            print "connecting: "+childItem+' to '+parentItem
                            try:
                                mc.connectAttr(parentItem+".outMesh", childItem+".inMesh", f=1)
                            except:
                                pass
                        elif grabNameChild in grabNameParent:
                            print "connecting: "+childItem+' to '+parentItem
                            try:
                                mc.connectAttr(parentItem+".outMesh", childItem+".inMesh", f=1)
                            except:
                                pass
                        elif grabNameChild==grabNameParent:
                            print "connecting: "+childItem+' to '+parentItem
                            try:
                                mc.connectAttr(parentItem+".outMesh", childItem+".inMesh", f=1)
                            except:
                                pass
        else:
            print "need to select two groups"

    def connSearch(self):
        selObj=mc.ls(sl=1, fl=1)
        if len(selObj) == 2:        
            if selObj:
                pass
            else:
                print "must select a driver group and a driven group(same shortnames)"
                return
            # selObj=mc.ls(sl=1, fl=1)
            parentObj=selObj[0]
            childrenObj=selObj[1]
            getparentObj=mc.listRelatives(parentObj, ad=1, type="mesh")
            if getparentObj:
                pass
            else:
                getparentObj=mc.listRelatives(parentObj, ad=1, type="nurbsCurve")
            getchildObj=mc.listRelatives(childrenObj, ad=1, type="mesh")
            if getchildObj:
                pass
            else:
                getchildObj=mc.listRelatives(childrenObj, ad=1, type="nurbsCurve")
            for childItem  in getchildObj:
                for parentItem in getparentObj:
                    if "Orig" not in str(childItem) and "Orig" not in str(parentItem):    
                        grabNameChild=str(pm.PyNode(childItem).nodeName())
                        grabNameParent=str(pm.PyNode(parentItem).nodeName())     
                        if ":" in grabNameChild:
                            grabNameChild=grabNameChild.split(":")[-1]
                        if ":" in grabNameParent:
                            grabNameParent=grabNameParent.split(":")[-1]
                        grabNameChild=grabNameChild.split("Shape")[0]    
                        grabNameParent=grabNameParent.split("Shape")[0]
                        if grabNameParent in grabNameChild:
                            print "connecting: "+childItem+' to '+parentItem
                            try:
                                mc.connectAttr(parentItem+".outMesh", childItem+".inMesh", f=1)
                            except:
                                pass
                        elif grabNameChild in grabNameParent:
                            print "connecting: "+childItem+' to '+parentItem
                            try:
                                mc.connectAttr(parentItem+".outMesh", childItem+".inMesh", f=1)
                            except:
                                pass
                        elif grabNameChild==grabNameParent:
                            print "connecting: "+childItem+' to '+parentItem
                            try:
                                mc.connectAttr(parentItem+".outMesh", childItem+".inMesh", f=1)
                            except:
                                pass
        else:
            print "need to select two groups"                                                                                        


    def WireSearchGroups_alias(self):
        #only prefix
        selObj=mc.ls(sl=1, fl=1)
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
        mc.addAttr(mc.ls(parentObj)[0], ln=name_blend, min=0, max=1, at="double", dv=0, k=1, nn=name_blend)
        getparentObj=mc.listRelatives(parentObj, ad=1, type="mesh")
        if getparentObj:
            getType = "isMesh"
            pass
        else:
            getparentObj=mc.listRelatives(parentObj, ad=1, type="nurbsCurve")
            getType = "isCrv"
        getchildObj=mc.listRelatives(childrenObj, ad=1, type="mesh")
        if getchildObj:
            pass
        else:
            getchildObj=mc.listRelatives(childrenObj, ad=1, type="nurbsCurve")
        for childItem  in getchildObj:
            for parentItem in getparentObj:
                if "Orig" not in str(childItem) and "Orig" not in str(parentItem):    
                    grabNameChild=str(pm.PyNode(childItem).nodeName())
                    grabNameParent=str(pm.PyNode(parentItem).nodeName())     
                    if ":" in grabNameChild:
                        grabNameChild=grabNameChild.split(":")[-1]
                    if ":" in grabNameParent:
                        grabNameParent=grabNameParent.split(":")[-1]
                    grabNameChild=grabNameChild.split("Shape")[0]    
                    grabNameParent=grabNameParent.split("Shape")[0]
                    if grabNameParent in grabNameChild:
                        print "attempt name match parent to child"
                        try:
                            print "wire: "+childItem+' to '+ parentItem
                            mc.select([childItem], r=1)   
                            mc.pickWalk(d="up")
                            # getNode=mc.deformer(parentItem, type="wire")
                            mc.wire(w=parentItem,n=str(grabNameParent)+"_wr", gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
                            mc.connectAttr(parentObj+"."+name_blend, grabNameParent+"_bs."+grabNameParent+"Shape",  f=1)
                            print "succeeded: "+parentItem+' to '+childItem
                        except:
                            pass
                    elif grabNameChild in grabNameParent:
                        print "attempt name match child to parent"
                        try:
                            print "wire: "+childItem+' to '+parentItem                   
                            mc.select([childItem], r=1)   
                            mc.pickWalk(d="up")
                            # getNode=mc.deformer(parentItem, type="wire")
                            mc.wire(w=parentItem,n=str(grabNameParent)+"_wr", gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
                            mc.connectAttr(parentObj+"."+name_blend, grabNameParent+"_bs."+grabNameParent+"Shape",  f=1)
                            print "succeeded: "+childItem+' to '+parentItem
                        except:
                            pass
                    elif grabNameChild==grabNameParent:
                        print "attempt exact name match"
                        try:
                            print "wire: "+childItem+' to '+parentItem                        
                            mc.select([childItem], r=1)   
                            mc.pickWalk(d="up")
                            # getNode=mc.deformer(parentItem, type="wire")
                            mc.wire(w=parentItem,n=str(grabNameParent)+"_wr", gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
                            mc.connectAttr(parentObj+"."+name_blend, grabNameParent+"_bs."+grabNameParent+"Shape",  f=1)
                            print "succeeded: "+childItem+' to '+parentItem
                        except:
                            pass
        mc.setAttr(parentObj+"."+name_blend, 1.0)



inst_mkwin=set_blendgrp_win()
inst_mkwin.show()
