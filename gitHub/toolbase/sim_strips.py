


import maya.cmds as mc
import os, sys

import PyQt4
from PyQt4 import QtCore, QtGui, Qt
from PyQt4.QtGui import QWidget, QRadioButton, QGridLayout, QLabel, \
    QTableWidget, QComboBox, QKeySequence, QToolButton, QPlainTextEdit, QPushButton,QBoxLayout, \
    QClipboard, QTableWidgetItem, QCheckBox, QVBoxLayout, QHBoxLayout, \
    QPixmap, QLineEdit, QListWidget, QTextEdit, QSizePolicy, QFrame, QPalette, QColor, \
    QFont, QAbstractItemView, QMenu, QMessageBox
from PyQt4.QtCore import SIGNAL

class sim_mod_UI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(sim_mod_UI, self).__init__(parent = None)

        self.setWindowTitle("sim models")
        self.central_widget=QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.masterLayout=QtWidgets.QGridLayout(self.central_widget)
        self.masterLayout.setAlignment(QtCore.Qt.AlignTop)


        self.myform = QtWidgets.QFormLayout()
        self.layout = QtWidgets.QGridLayout()
        self.masterLayout.addLayout(self.layout, 0,0,1,1)

        self.SelectionSetupLayout = QtWidgets.QGridLayout()
        self.selection_widgetframe = QtWidgets.QFrame()
        self.selection_widgetframe.setLayout(self.SelectionSetupLayout)
        self.SelectionSetupLayout.addLayout(self.myform, 0,0,1,1)
        self.layout.addLayout(self.SelectionSetupLayout, 0,0,1,1)

        self.add_widgets()

        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(self.selection_widgetframe)
        scroll.setWidgetResizable(False)
        self.layout.addWidget(scroll, 1,0,1,1)
        self.setLayout(self.layout)

    def add_widgets(self):
        self.sim_mod_order_layout = QtWidgets.QHBoxLayout()
        self.myform.addRow(self.sim_mod_order_layout) 
        self.sim_model_button_layout = QtWidgets.QVBoxLayout()
        self.sim_mod_order_layout.addLayout(self.sim_model_button_layout)
        self.sim_mod_slid_layout = QtWidgets.QVBoxLayout()
        self.sim_mod_order_layout.addLayout(self.sim_mod_slid_layout)   
        self.sim_mod_slider_layout = QtWidgets.QVBoxLayout()     
        self.sim_mod_slid_layout.addLayout(self.sim_mod_slider_layout)

        self.sim_model_fx_button=QtWidgets.QPushButton("build wire wrap")
        self.sim_model_fx_button.setToolTip("name fx nodes")
        self.connect(self.sim_model_fx_button, SIGNAL('clicked()'),lambda:  self.fastwire_build())
        self.sim_model_button_layout.addWidget(self.sim_model_fx_button) 

        self.init_frm_button=QtWidgets.QPushButton("cloth strips")
        self.init_frm_button.setToolTip("name dyn nodes")
        self.connect(self.init_frm_button, SIGNAL('clicked()'),lambda:  self.build_a_cloth_short_callup())
        self.sim_model_button_layout.addWidget(self.init_frm_button) 

        self.bld_crv_button=QtWidgets.QPushButton("build a curve")
        self.bld_crv_button.setToolTip("name dyn nodes")
        self.connect(self.bld_crv_button, SIGNAL('clicked()'),lambda:  self.build_a_curve())
        self.sim_model_button_layout.addWidget(self.bld_crv_button) 

        self.ext_button=QtWidgets.QPushButton("extrude strips")
        self.ext_button.setToolTip("extrudes shape across a selected group of curves")
        self.connect(self.ext_button, SIGNAL('clicked()'),lambda:  self.extrude_strips())
        self.sim_model_button_layout.addWidget(self.ext_button) 

        self.ext_button=QtWidgets.QPushButton("extrude tubes")
        self.ext_button.setToolTip("extrudes shape across a selected group of curves")
        self.connect(self.ext_button, SIGNAL('clicked()'),lambda:  self.extrude_tubes())
        self.sim_model_button_layout.addWidget(self.ext_button) 


        self.wr_button=QtWidgets.QPushButton("Wire")
        self.wr_button.setToolTip("")
        self.connect(self.wr_button, SIGNAL('clicked()'),lambda:  self.wirewrap())
        self.sim_model_button_layout.addWidget(self.wr_button) 

        self.wr_alias_button=QtWidgets.QPushButton("Wire Alias")
        self.wr_alias_button.setToolTip("")
        self.connect(self.wr_alias_button, SIGNAL('clicked()'),lambda:  self.WireSearchGroups_alias())
        self.sim_model_button_layout.addWidget(self.wr_alias_button) 


        self.rshp_edge_button=QtWidgets.QPushButton("Reshape to edge")
        self.rshp_edge_button.setToolTip("")
        self.connect(self.rshp_edge_button, SIGNAL('clicked()'),lambda:  self.matchCurveShapes())
        self.sim_model_button_layout.addWidget(self.rshp_edge_button) 

        self.rshp_shp_button=QtWidgets.QPushButton("Reshape to shape")
        self.rshp_shp_button.setToolTip("")
        self.connect(self.rshp_shp_button, SIGNAL('clicked()'),lambda:  self.matchFullShape())
        self.sim_model_button_layout.addWidget(self.rshp_shp_button) 


    def build_a_curve(self):
        # getTopOpenGuides=mc.ls(sl=1, fl=1)
        if len(mc.ls(sl=1))<1:
            print "need to select some verts"
            return
        getSelectPref = mc.selectPref(q=1, tso=1)
        if getSelectPref == False:
            mc.selectPref(tso=1)
            getTopOpenGuides = mc.ls(os=1, fl=1)
        else:
            getTopOpenGuides = mc.ls(os=1, fl=1)        
        if len(getTopOpenGuides)>3:
            get_crv = self.build_a_curve_callup(getTopOpenGuides)
        else:
            get_crv = self.build_a_curve_short_callup(getTopOpenGuides)
        mc.select(get_crv, r=1)


    def build_a_curve_callup(self, selectedObjects):
        values=[]
        for each in selectedObjects:#get point values to build curve
            transformWorldMatrix = mc.xform(each, q=True, wd=1, t=True) 
            # transformWorldMatrix=pm.PyNode(each).getPosition() 
            values.append(transformWorldMatrix)
        get_crv = mc.curve(n=selectedObjects[0]+"_crv", d=3, p=values)       
        return get_crv 


    def build_a_curve_short_callup(self, selectedObjects):
        values=[]
        for each in selectedObjects:#get point values to build curve
            transformWorldMatrix = mc.xform(each, q=True, wd=1, t=True) 
            # transformWorldMatrix=pm.PyNode(each).getPosition() 
            values.append(transformWorldMatrix)
        values.append(transformWorldMatrix)
        values.append(transformWorldMatrix)
        get_crv = mc.curve(n=selectedObjects[0]+"_crv", d=3, p=values) 
        mc.rebuildCurve(get_crv, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=7, d=3, tol=0.01)
        mc.rebuildCurve(get_crv, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=7, d=3, tol=0.01)
        return get_crv 

    def fastwire_build(self):
        if len(mc.ls(sl=1))<1:
            print "need to select some verts"
            return
        getObj = mc.ls(sl=1)[0].split(".")[0]
        self.build_a_curve()
        getCrv = mc.ls(sl=1)[0]
        mc.select([getObj, getCrv])
        self.wirewrap()

    def wirewrap(self):
        # getshapenode_one=[(each) for each in mc.ls(sl=1) if mc.nodeType(mc.listRelatives(each, ad=1)) == "mesh"]
        # getshapenode_one = [(each) for each in mc.listRelatives(mc.ls(sl=1)[0], c=1, s=1)]
        getshapenode_one=[(each) for each in mc.ls(sl=1) if mc.listRelatives(each, c=1, s=1)]
        # getshapenode_two=[(each) for each in mc.ls(sl=1) if mc.nodeType(mc.listRelatives(each, c=1)) == "nurbsCurve"]
        getshapenode_two=[(each) for each in mc.ls(sl=1) if mc.listRelatives(each, c=1, type = "nurbsCurve")]
        # getshapenode_two = [(each) for each in mc.listRelatives(mc.ls(sl=1)[1:], ad=1, type="nurbsCurve")]
        # getNode=mc.deformer(getshapenode_one[0], type="wire")
        mc.wire(getshapenode_one[0], gw=0, en=1.000000, ce=0.000000, li=0.000000, w=getshapenode_two[0], dds=[(0, 20)])
        # mc.connectAttr(getshapenode_two[0]+".worldSpace[0]", getNode[0]+".deformedWire[0]", f=1)
        # mc.setAttr(getNode[0]+".dropoffDistance[0]", 50)
        mc.pickWalk(getshapenode_one, d="up")
        mc.pickWalk(getshapenode_one, d="up")
        mc.pickWalk(getshapenode_one, d="up")
        mc.setAttr(mc.ls(sl=1)[0]+".visibility", 0)


    def extrude_strips(self):
        selfU=12
        selfV=1            
        # maya.mel.eval( 'nurbsToPolygonsPref -un %d -vn %d;',  %(selfU, ) %(selfV, )
        mc.nurbsToPolygonsPref(un=selfU, vn=selfV)
        # nurbsToPolygonsPref -un 1 -vn 90
        getObj=mc.ls(sl=1)
        getParent=getObj[0]
        # mc.nurbsToPolygonsPref(un=selfU, uv=selfV)
        gettgtObj = [(each) for each in mc.listRelatives(getObj[1:], ad=1, type="nurbsCurve")]
        for each in gettgtObj: 
            mc.extrude(getParent, each, ch=1, rn=0, po=1, et=1, ucp=1, fpt=1, upn=1, rotation=0, scale=1, rsp=1) 


    def extrude_tubes(self):
        selfU=12
        selfV=1       
        # maya.mel.eval( 'nurbsToPolygonsPref -un %d -vn %d;',  %(selfU, ) %(selfV, )
        mc.nurbsToPolygonsPref(un=selfU, vn=selfV)
        # nurbsToPolygonsPref -un 1 -vn 90
        getObj=mc.ls(sl=1)
        getParent=getObj[0]
        # mc.nurbsToPolygonsPref(un=selfU, uv=selfV)
        gettgtObj = [(each) for each in mc.listRelatives(getObj[1:], ad=1, type="nurbsCurve")]
        for each in gettgtObj: 
            mc.extrude(getParent, each, n=each,  ch=1, rn=0, po=1, et=2, ucp=1, fpt=1, upn=1, rsp=1, rotation=0, scale=1)
                

    def build_a_cloth_short_callup(self):
        if len(mc.ls(sl=1))<1:
            print "need to select some verts"
            return
        getObj = mc.ls(sl=1)[0].split(".")[0]
        self.build_a_curve()
        getCrv=mc.ls(sl=1)
        mc.select([getObj, getCrv[0]], r =1)
        getshapenode_one=[(each) for each in mc.ls(sl=1) if mc.listRelatives(each, c=1, s=1)]
        getshapenode_two=[(each) for each in mc.ls(sl=1) if mc.listRelatives(each, c=1, type = "nurbsCurve")]   
        selfU=mc.textField(text="12")
        selfV=mc.textField(text="1")
        mc.nurbsToPolygonsPref(un=selfU, vn=selfV)
        getIt=mc.ls("extCurve")
        if len(getIt)<1:
            name = "extCurve"
            xCubeMake=mc.curve(n=name, d=1, p =[(-1.0, 0.0, 0.0), (-.5, 0.0, 0.0),(0.0, 0.0, 0.0), (.5, 0.0, 0.0), (1.0, 0.0, 0.0)])
            mc.extrude(xCubeMake, getshapenode_two, ch=1, rn=0, po=1, et=1, ucp=1, fpt=1, upn=1, rotation=0, scale=1, rsp=1) 
        else:
            name=mc.ls("extCurve")[0]  
        getStrip = mc.ls(sl=1)
        mc.select(getObj, r=1)
        mc.select(getStrip[0], add=1)
        mc.CreateWrap()

    @undo
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
        # print parentObj
        mc.addAttr(mc.ls(parentObj)[0], ln=name_blend, min=0, max=1, at="double", dv=0, k=1, nn=name_blend)
        getparentObj=[(each) for each in mc.listRelatives(parentObj, ad=1, type="nurbsCurve") if "Orig" not in each]
        getchildObj=[(each) for each in mc.listRelatives(childrenObj, ad=1, type="mesh") if "Orig" not in each]
        if getchildObj:
            pass
        else:
            getchildObj=[(each) for each in mc.listRelatives(childrenObj, ad=1, type="nurbsCurve") if "Orig" not in each]
        for childItem, parentItem  in map(None, getchildObj, getparentObj):
            grabNameChild = mc.listRelatives(childItem, p=1, type= "transform")[0]            
            grabNameParent = mc.listRelatives(parentItem, p=1, type= "transform")[0]  
            if ":" in grabNameChild:
                foundNameChild=grabNameChild.split(":")[-1]
            else:
                foundNameChild=grabNameChild
            if ":" in grabNameParent:
                foundNameParent=grabNameParent.split(":")[-1]
            else:
                foundNameParent=grabNameParent            
            if foundNameParent in foundNameChild:
                try:
                    print "wire: "+grabNameChild+' to '+ grabNameParent
                    results = mc.wire(grabNameChild, w=grabNameParent, n="{}_wr".format(grabNameChild), gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
                    mc.connectAttr(parentObj+"."+name_blend, "{}_wr.envelope".format(grabNameChild),  f=1)
                    # mc.connectAttr("{}.worldSpace[0]".format(parentItem), parentItem.split("Shape")[0]+"BaseWireShape.create", f=1)  
                    print "succeeded: "+parentItem+' to '+childItem
                except:
                    pass
            elif foundNameChild in foundNameParent:
                try:
                    print "wire: "+grabNameChild+' to '+ grabNameParent                
                    results = mc.wire(grabNameChild, w=grabNameParent, n="{}_wr".format(grabNameChild), gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
                    mc.connectAttr(parentObj+"."+name_blend, "{}_wr.envelope".format(grabNameChild),  f=1)
                    # mc.connectAttr("{}.worldSpace[0]".format(parentItem), parentItem.split("Shape")[0]+"BaseWireShape.create", f=1)                            
                    print "succeeded: "+childItem+' to '+parentItem
                except:
                    pass
            elif foundNameChild==foundNameParent:
                try:
                    print "wire: "+grabNameChild+' to '+ grabNameParent                
                    results = mc.wire(grabNameChild, w=grabNameParent, n="{}_wr".format(grabNameChild), gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
                    mc.connectAttr(parentObj+"."+name_blend, "{}_wr.envelope".format(grabNameChild),  f=1)
                    # mc.connectAttr("{}.worldSpace[0]".format(parentItem), parentItem.split("Shape")[0]+"BaseWireShape.create", f=1)  
                    print "succeeded: "+childItem+' to '+parentItem
                except:
                    pass
        mc.setAttr(parentObj+"."+name_blend, 1.0)


    def matchCurveShapes(self):
        self.CurveShapes()

    def matchFullShape(self):
        getFirstGrp, getSecondGrp=self.CurveShapes()
        self.matchCurveShapes_andShrinkWrap(getFirstGrp, getSecondGrp)


    def CurveShapes(self):
        getSel=self.selection_grab()
        if getSel:
            pass
        else:
            return
        getNames=mc.ls(os=1, fl=1)
        if ".e[" not in str(getNames[0]):
            print "selection needs to be continuous edges of two seperate polygon objects: first select one, then continuous edge and then the continuous edge on a seperate poly object that you want to deform it along"
            return
        else:
            pass
        getFirstGrp = getNames[0].split(".")[0]
        getSecondGrp = getNames[-1:][0].split(".")[0]
        if getFirstGrp == getSecondGrp:
            print "Only one poly object has been detected. Select one object and it's continuous edge and then select another object and select it's continuous edge for the first object to align to."
            return
        else:
            pass
        firstList=[(each) for each in getNames if each.split(".")[0]==getFirstGrp]
        secondList=[(each) for each in getNames if each.split(".")[0]==getSecondGrp]
        '''create childfirst curve'''
        mc.select(firstList)
        mc.CreateCurveFromPoly()
        getFirstCurve=mc.ls(sl=1, fl=1)
        '''get cv total of curve'''
        getFirstCurveInfo=mc.ls(sl=1, fl=1)
        # numberCV=getFirstCurveInfo[0].numCVs()
        getFirstCurveInfo=mc.ls("{}.cv[*]".format(mc.ls(sl=1)[0]), fl=1)
        mc.delete(getFirstCurve[0], ch=1)
        '''wrap child mesh to curve'''
        mc.select(mc.ls(getFirstGrp)[0], r=1)
        mc.wire(w=getFirstCurve[0], gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
        '''create parent curve'''
        mc.select(secondList)
        mc.CreateCurveFromPoly()
        getSecondCurve=mc.ls(sl=1, fl=1)
        getSecondCurveInfo=mc.ls(sl=1, fl=1)
        '''rebuilt curve to match first curve built'''
        mc.rebuildCurve(getSecondCurve[0], getFirstCurve[0], rt=2 )
        getSecondCurve=mc.ls(sl=1, fl=1)
        getSecondCurveInfo=mc.ls(sl=1, fl=1)
        mc.delete(getSecondCurve[0], ch=1)
        '''wrap parent curve to parent mesh'''
        mc.select(getSecondCurve[0], r=1)
        mc.select(mc.ls(getSecondGrp)[0], add=1)
        mc.CreateWrap()
        '''blend child curve to parent curve'''
        mc.blendShape(getSecondCurve[0], getFirstCurve[0],w=(0, 1.0), o="world")
        return getFirstGrp, getSecondGrp




    def matchCurveShapes_andShrinkWrap(self, getFirstGrp, getSecondGrp):
        myDict={
                ".shapePreservationEnable":1,
                ".shapePreservationSteps":72,
                ".shapePreservationReprojection":1,
                ".shapePreservationIterations":1,
                ".shapePreservationMethod":0,
                ".envelope":1,
                ".targetSmoothLevel":1,
                ".continuity":1,
                ".keepBorder":0,
                ".boundaryRule":1,
                ".keepHardEdge":0,
                ".propagateEdgeHardness":0,
                ".keepMapBorders":1,
                ".projection":4,
                ".closestIfNoIntersection":0,
                ".closestIfNoIntersection":0 ,
                ".reverse":0,
                ".bidirectional":0,
                ".boundingBoxCenter":1,
                ".axisReference":0 ,
                ".alongX":1,
                ".alongY":1,
                ".alongZ":1,
                ".offset":0,
                ".targetInflation":0,
                ".falloff":0.3021390379,
                ".falloffIterations": 1
                }        
        mc.delete(getFirstGrp, ch=1)
        getShrink=mc.deformer(getFirstGrp, type="shrinkWrap")
        mc.connectAttr(getSecondGrp+".worldMesh[0]", getShrink[0]+".targetGeom", f=1)
        for key, value in myDict.items():
            mc.setAttr(getShrink[0]+key, value)

    def selection_grab(self):
        '''--------------------------------------------------------------------------------------------------------------------------------------
        Common selection query
        --------------------------------------------------------------------------------------------------------------------------------------'''        
        getSel=mc.ls(sl=1, fl=1)
        if getSel:
            pass
        else:
            print "You need to make a selection for this tool to operate on."
            return
        return getSel
    

inst_win = sim_mod_UI()
inst_win.show()        
