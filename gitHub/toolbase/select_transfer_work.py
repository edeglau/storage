'''Transfers selection to nearby verts of other objects'''
__author__="Elise Deglau"
import maya.cmds as mc
import os, sys
#import maya.mel
import numpy
from apiWrappers import getPoints
import mMesh
reload(mMesh)
import maya.api.OpenMaya as OpenMaya

checkHoudini = os.getenv("HOUDINI_VERSION")

checkMaya = os.getenv("REZ_MAYA_VERSION")
import PyQt4


if checkHoudini != None:
    import hutil
    from hutil.Qt import QtCore, QtWidgets, QtWidgets
    from hutil.Qt.QtCore import SIGNAL
#Author: Elise Deglau
#https://atlas.bydeluxe.com/confluence/display/~lime/2018-8-23+Elise+D

#to add to shelf:

# import sys 
# filepath=( '//sw/dev/deglaue/tools//' ) 
# if not filepath in sys.path: 
#     sys.path.append(str(filepath)) 
# import select_transfer
# reload (select_transfer)
# evokeTool = select_transfer.map_select_transfer()
# evokeTool()

#icon

# /sw/dev/deglaue/icons/deglaue_toolset_seltransfr.png




class wgtmap_select_gui(QtWidgets.QMainWindow):
    def __init__(self):
        super(wgtmap_select_gui, self).__init__()
        self.initUI()

    def initUI(self):     
        self.setWindowTitle("Select based on weightmap")
        self.central_widget=QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.masterLayout=QtWidgets.QGridLayout(self.central_widget)
        self.masterLayout.setAlignment(QtCore.Qt.AlignTop)


        self.myform = QtWidgets.QFormLayout()
        self.wgt_layout = QtWidgets.QGridLayout()
        self.masterLayout.addLayout(self.wgt_layout, 0,0,1,1)

        self.SelectionSetupLayout = QtWidgets.QGridLayout()
        self.selection_widgetframe = QtWidgets.QFrame()
        self.selection_widgetframe.setLayout(self.SelectionSetupLayout)
        self.SelectionSetupLayout.addLayout(self.myform, 0,0,1,1)
        self.wgt_layout.addLayout(self.SelectionSetupLayout, 0,0,1,1)

        self.add_widgets()

        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(self.selection_widgetframe)
        scroll.setWidgetResizable(False)
        self.wgt_layout.addWidget(scroll, 1,0,1,1)
        self.setLayout(self.wgt_layout)

    def add_widgets(self):
        self.sel_order_layout = QtWidgets.QHBoxLayout()
        self.myform.addRow(self.sel_order_layout) 
        self.sel_button_layout = QtWidgets.QHBoxLayout()
        self.myform.addRow(self.sel_button_layout)         
        self.value_label = QtWidgets.QLabel("value")
        self.sel_order_layout.addWidget(self.value_label)  
        # self.textNum = QtWidgets.QLabel("10%")
        self.textNum = QtWidgets.QLineEdit("10%")
        self.textNum.connect(self.textNum,QtCore.SIGNAL("returnPressed()"),self.set_slider)
        self.sel_order_layout.addWidget(self.textNum)        
        self.selection_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal) 
        self.selection_slider.Orientation = (0) 
        self.selection_slider.setMinimum(1)
        self.selection_slider.setMaximum(100)
        self.selection_slider.setValue(10)        
        self.selection_slider.valueChanged.connect(self.print_slider)
        self.sel_order_layout.addWidget(self.selection_slider) 
        self.drop_label = QtWidgets.QLabel("dropoff")
        self.sel_order_layout.addWidget(self.drop_label)     
        self.droppoff = QtWidgets.QLineEdit(".5")
        self.sel_order_layout.addWidget(self.droppoff)           
        self.swap_button = QtWidgets.QPushButton("Swap")
        self.connect(self.swap_button, SIGNAL("clicked()"),
                    lambda: self.sel_wgt_function(radius = self.selection_slider.value(), adding = False, reverse = False))
        self.sel_button_layout.addWidget(self.swap_button)     
        self.add_button = QtWidgets.QPushButton("Add")
        self.connect(self.add_button, SIGNAL("clicked()"),
                    lambda: self.sel_wgt_function(radius = self.selection_slider.value(), adding = True, reverse = False))
        self.sel_button_layout.addWidget(self.add_button)   
        self.swap_rev_button = QtWidgets.QPushButton("SwapReverseValue")
        self.connect(self.swap_rev_button, SIGNAL("clicked()"),
                    lambda: self.sel_wgt_function(radius = self.selection_slider.value(), adding = False, reverse = True))
        self.sel_button_layout.addWidget(self.swap_rev_button)     
        self.add_rev_button = QtWidgets.QPushButton("AddReverseValue")
        self.connect(self.add_rev_button, SIGNAL("clicked()"),
                    lambda: self.sel_wgt_function(radius = self.selection_slider.value(), adding = True, reverse = True))
        self.sel_button_layout.addWidget(self.add_rev_button)                                     
        self.sel_errant_button = QtWidgets.QPushButton("Grab Errant")
        self.connect(self.sel_errant_button, SIGNAL("clicked()"),
                    lambda: self.sel_errant_weight(adding = False, reverse = False))
        self.sel_button_layout.addWidget(self.sel_errant_button)   
        self.pt_fol_button = QtWidgets.QPushButton("paint fol")
        self.connect(self.pt_fol_button, SIGNAL("clicked()"),
                    lambda: self.paint_fol_function(radius = self.selection_slider.value(), adding = True, reverse = False))
        self.sel_button_layout.addWidget(self.pt_fol_button)     
        self.pt_crv_button = QtWidgets.QPushButton("paint crv")
        self.connect(self.pt_crv_button, SIGNAL("clicked()"),
                    lambda: self.paint_crv_function(radius = self.selection_slider.value(), adding = True, reverse = False))
        self.sel_button_layout.addWidget(self.pt_crv_button)     

    def set_slider(self):
        getText = self.textNum.text()
        getText = int(getText)
        self.selection_slider.setValue(getText)


    def print_slider(self):
        size = self.selection_slider.value()
        self.textNum.setText(str(size)+"%")

    def sel_errant_weight(self, adding, reverse):
        getobj = mc.ls(sl=1, fl=1)[0]        
        collect = []
        if ".v" in getobj:
            getobj = getobj.split('.v')[0]
        verts = mc.ls(getobj+'.vtx[*]', fl=True)
        try:
            blendShapeNode = mc.artAttrCtx(mc.currentCtx(), q=1, asl=1)
        except:
            print "select a paint type map to apply(right click: paint)"
            return
        blendShapeNode = blendShapeNode.split('.')[1]
        for index, each_vert in enumerate(verts):
            find = mc.getAttr('{0}.inputTarget[0].baseWeights[{1}]'.format(blendShapeNode, index))
            if "e" in str(find):
                collect.append(each_vert)  
        mc.select(cl=1)                                          
        mc.select(collect, add=1) 

    def sel_wgt_function(self, radius, adding, reverse):
        getobj = mc.ls(sl=1, fl=1)[0]        
        radius = float(radius) *.01
        collect = []
        if ".v" in getobj:
            getobj = getobj.split('.v')[0]
        verts = mc.ls(getobj+'.vtx[*]', fl=True)
        try:
            blendShapeNode = mc.artAttrCtx(mc.currentCtx(), q=1, asl=1)
        except:
            print "select a paint type map to apply(right click: paint)"
            return
        blendShapeNode = blendShapeNode.split('.')[1]
        for index, each_vert in enumerate(verts):
            find = mc.getAttr('{0}.inputTarget[0].baseWeights[{1}]'.format(blendShapeNode, index))
            if "e" not in str(find):
                # find = str(find).split('e')[0]
                # find = float(find)
                if reverse == True:
                    if find < radius:
                        collect.append(each_vert)
                else:
                    if find > radius:
                        collect.append(each_vert)  
        if adding == False:
            mc.select(cl=1)                                          
        mc.select(collect, add=1) 

    def paint_fol_function(self, radius, adding, reverse):
        dropoff = float(self.droppoff.text())
        targetSelection_crvs = [(each) for item in mc.ls(sl=1) if mc.listRelatives(item, ad=1, type="follicle") for each in mc.listRelatives(item, ad=1, type="follicle") ]
        self.sel_wgt_function(radius, adding, reverse)
        selObj = mc.ls(sl=1)
        collectmycurve = []
        for each_src in selObj:
            pos=mc.xform(each_src, ws=1, q=1, t=1)
            x_pos_min, x_pos_max, y_pos_min, y_pos_max, z_pos_min, z_pos_max = pos[0]-dropoff, pos[0]+dropoff, pos[1]-dropoff, pos[1]+dropoff, pos[2]-dropoff, pos[2]+dropoff 
            for each_tgt_crv  in targetSelection_crvs:
                getpar=mc.listRelatives(each_tgt_crv, p=1, type="transform")[0]
                tgt_pos=mc.xform(getpar, ws=1, q=1, t=1)
                if tgt_pos[0] >= x_pos_min and tgt_pos[0] <= x_pos_max and tgt_pos[1] >= y_pos_min and tgt_pos[1] <= y_pos_max and tgt_pos[2] >= z_pos_min and tgt_pos[2] <= z_pos_max:
                    collectmycurve.append(each_tgt_crv)    
        mc.select(collectmycurve, r=1)   


    def paint_crv_function(self, radius, adding, reverse):
        dropoff = float(self.droppoff.text())
        targetSelection_crvs = [(each) for item in mc.ls(sl=1) if mc.listRelatives(item, ad=1, type="nurbsCurve") for each in mc.listRelatives(item, ad=1, type="nurbsCurve") ]        
        # targetSelection_crvs = [(each) for each in mc.listRelatives(item, ad=1, type="nurbsCurve") for item in mc.ls(sl=1) if mc.listRelatives(item, ad=1, type="nurbsCurve")]
        self.sel_wgt_function(radius, adding, reverse)
        selObj = mc.ls(sl=1)
        if selObj:
            result = mc.confirmDialog(
                title="Select mode for curves",
                # message="Radius:",
                # text=".1",
                button=["CV","Crv","Cancel"],
                cancelButton="Cancel",
                dismissString="Cancel" )
            if result == "CV":
                selectcmpnt = True
            elif result == "Crv":
                selectcmpnt = False                                        
            else:
                print "selection transfer cancelled"  
                return
        # targetSelection_crvs = [(each) for each in mc.ls(type = "nurbsCurve") if "static" not in each]
        collectmycurve = []
        for each_src in selObj:
            pos=mc.xform(each_src, ws=1, q=1, t=1)
            x_pos_min, x_pos_max, y_pos_min, y_pos_max, z_pos_min, z_pos_max = pos[0]-dropoff, pos[0]+dropoff, pos[1]-dropoff, pos[1]+dropoff, pos[2]-dropoff, pos[2]+dropoff 
            for each_tgt_crv  in targetSelection_crvs:
                tgt_sourcePoint = '{}.cv[0]'.format(each_tgt_crv)
                tgt_pos = mc.pointPosition(tgt_sourcePoint, w=1) 
                if tgt_pos[0] >= x_pos_min and tgt_pos[0] <= x_pos_max and tgt_pos[1] >= y_pos_min and tgt_pos[1] <= y_pos_max and tgt_pos[2] >= z_pos_min and tgt_pos[2] <= z_pos_max:
                    if selectcmpnt == True:
                        collectmycurve.append(tgt_sourcePoint)    
                    else:
                        collectmycurve.append(each_tgt_crv) 
        mc.select(collectmycurve, r=1)   


class set_select_win(QtWidgets.QWidget):
    # def __init__(self): 
    def __init__(self):
        super(set_select_win, self).__init__()
        self.initUI()

    def initUI(self):    

        self.setWindowTitle("Transfer Selection across objects")

        self.myform = QtWidgets.QFormLayout()
        self.layout = QtWidgets.QGridLayout()

        self.selectSetupLayout = QtWidgets.QGridLayout()
        self.selectOverride = QtWidgets.QFrame()
        self.selectOverride.setLayout(self.selectSetupLayout)
        self.selectSetupLayout.addLayout(self.myform, 0,0,1,1)
        self.layout.addLayout(self.selectSetupLayout, 0,0,1,1)

        self.add_widgets()

        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(self.selectOverride)
        scroll.setWidgetResizable(False)
        self.layout.addWidget(scroll, 1,0,1,1)
        self.setLayout(self.layout)

    def add_widgets(self):
        self.vertical_order_layout_ta = QtWidgets.QHBoxLayout()
        self.myform.addRow(self.vertical_order_layout_ta) 
        self.sel_label_button = QtWidgets.QLabel("Use Space:")
        self.vertical_order_layout_ta.addWidget(self.sel_label_button)          
        self.sel_world_button = QtWidgets.QPushButton("World")
        self.connect(self.sel_world_button, SIGNAL("clicked()"),
                    lambda: self.map_select_transfer())
        self.vertical_order_layout_ta.addWidget(self.sel_world_button) 
        self.sel_uv_button = QtWidgets.QPushButton("UV")
        self.connect(self.sel_uv_button, SIGNAL("clicked()"),
                    lambda: self.UV_select_transfer())
        self.vertical_order_layout_ta.addWidget(self.sel_uv_button)     
        self.sel_pnt_button = QtWidgets.QPushButton("Current Paint")
        self.connect(self.sel_pnt_button, SIGNAL("clicked()"),
                    lambda: self.sel_window_paint())
        self.vertical_order_layout_ta.addWidget(self.sel_pnt_button)     
        self.sel_fol_button = QtWidgets.QPushButton("Follicle")
        self.connect(self.sel_fol_button, SIGNAL("clicked()"),
                    lambda: self.follicle_selecting())
        self.vertical_order_layout_ta.addWidget(self.sel_fol_button)   
        self.sel_crv_button = QtWidgets.QPushButton("Curve")
        self.connect(self.sel_crv_button, SIGNAL("clicked()"),
                    lambda: self.curve_selecting())
        self.vertical_order_layout_ta.addWidget(self.sel_crv_button)     

    def sel_window_paint(self):
        # Transfers selection to nearby verts of other objects.
        #query if selected
        getobj = mc.ls(sl=1, fl=1)[0]        
        if getobj:
            if len(getobj)<0:
                print "select an object and go into paint mode."
                return
            else:
                pass               
        inst_win = wgtmap_select_gui()
        inst_win.show()


    def map_select_transfer(self):
        # print "start"
        # Transfers selection to nearby verts of other objects.
        NDIM = 3
        selObj=mc.ls(sl=1, fl=1)
        #query if selected
        if selObj:
            if len(selObj)<2:
                print "select a group of verts and an object or two objects near eachother."
                return
            else:
                pass         
            #get falloff amount 
            result = mc.promptDialog(
                title="Confirm",
                message="Radius:",
                text=".001",
                button=["Swap","Add","Cancel"],
                cancelButton="Cancel",
                dismissString="Cancel" )
            if result == "Add":
                radius = mc.promptDialog(query=True, text=True)
                radius = float(radius)
                radius = radius * radius
                adding=True        
            elif result == "Swap":
                radius = mc.promptDialog(query=True, text=True)
                radius = float(radius)
                radius = radius * radius
                adding=False
            else:
                print "selection transfer cancelled"  
                return
        else:
            print "select a group of verts and an object or two objects near eachother."
            return
        # mc.select(selObj[0])
        #determine if the mapper is a vertex selection or object
        result = []
        if ".v" in selObj[0]:
            #collect the mapper verts
            getFirstGrp = selObj[0].split(".")[0]
            sourceName=[(each) for each in selObj if each.split(".")[0]==getFirstGrp]
            #determine the mapping selections
            targetName=[(each) for each in selObj if each.split(".")[0]!=getFirstGrp]
            # print sourceName, targetName
            if adding == False:
                mc.select(cl=1)
            for eachtarget in targetName:
                mc.select(eachtarget, d=1)
                mc.select(mMesh.get_closest_points(eachtarget, transform=0, mesh=0, mesh_vtx=sourceName, distance=radius), add=1)
        else:
            #transfer the mapper into verts
            sourceName = selObj[0]
            #determine the mapping selections
            targetName=[(each) for each in selObj if each != sourceName]
            #targetpoints into array
            if adding == False:
                mc.select(cl=1)    
            for eachtarget in targetName:
                mc.select(eachtarget, d=1)
                a = getPoints(mc.ls(eachtarget)[0], space='world')
                a.shape = a.size / NDIM, NDIM
                #sourcepoints into array
                srcPoints = getPoints(mc.ls(sourceName)[0], space = "world") 
                #create empty set
                result = set()
                for point in srcPoints:
                    d = ((a-point)**2).sum(axis = 1) #compute distance
                    ndx = d.argsort()
                    max_idx = next((i for i, v in enumerate(ndx) if d[v] >radius), None)
                    if max_idx:
                        result.update(ndx[:max_idx])
            result = list(result)
            mc.select(['{}.vtx[{}]'.format(eachtarget, x) for x in result], add =1)


    def follicle_selecting(self):
        selObj=mc.ls(sl=1, fl=1)
        #query if selected
        if selObj:
            if len(selObj)<2:
                print "select a group of verts and an object or two objects near eachother."
                return
            else:
                pass         
            #get falloff amount 
            result = mc.promptDialog(
                title="Confirm",
                message="Radius:",
                text=".1",
                button=["Add","Swap","Cancel"],
                cancelButton="Cancel",
                dismissString="Cancel" )
            if result == "Add":
                radius = mc.promptDialog(query=True, text=True)
                radius = float(radius)
                radius = radius * radius
                adding=True
            elif result == "Swap":
                radius = mc.promptDialog(query=True, text=True)
                radius = float(radius)
                radius = radius * radius
                adding=False
            else:
                print "selection transfer cancelled"  
                return
        else:
            print "select a group of verts and a group of follicles."
            return        
        targetSelection_crvs = [(each) for item in mc.ls(sl=1) if ".vtx" not in item for each in mc.listRelatives(item, ad=1, type="follicle")]
        verts = [(item) for item in mc.ls(sl=1) if ".vtx" in item]
        dropoff = radius
        if adding == False:
            mc.select(cl=1)
        collectmycurve = []
        for each_src in selObj:
            pos=mc.xform(each_src, ws=1, q=1, t=1)
            x_pos_min, x_pos_max, y_pos_min, y_pos_max, z_pos_min, z_pos_max = pos[0]-dropoff, pos[0]+dropoff, pos[1]-dropoff, pos[1]+dropoff, pos[2]-dropoff, pos[2]+dropoff 
            for each_tgt_crv  in targetSelection_crvs:
                getpar=mc.listRelatives(each_tgt_crv, p=1, type="transform")[0]
                tgt_pos=mc.xform(getpar, ws=1, q=1, t=1)
                if tgt_pos[0] >= x_pos_min and tgt_pos[0] <= x_pos_max and tgt_pos[1] >= y_pos_min and tgt_pos[1] <= y_pos_max and tgt_pos[2] >= z_pos_min and tgt_pos[2] <= z_pos_max:
                    collectmycurve.append(each_tgt_crv)    
        mc.select(collectmycurve, add=1)   

    def curve_selecting(self):
        selObj=mc.ls(sl=1, fl=1)
        #query if selected
        if selObj:
            if len(selObj)<2:
                print "select a group of verts and an object or two objects near eachother."
                return
            else:
                pass         
            #get falloff amount 
            result = mc.promptDialog(
                title="Confirm",
                message="Radius:",
                text=".1",
                button=["SwapToCV","AddCV","SwapToCrv","AddCrv","Cancel"],
                cancelButton="Cancel",
                dismissString="Cancel" )
            if result == "SwapToCV":
                radius = mc.promptDialog(query=True, text=True)
                radius = float(radius)
                radius = radius * radius
                selectcmpnt = True
                adding=False
            elif result == "SwapToCrv":
                radius = mc.promptDialog(query=True, text=True)
                radius = float(radius)
                radius = radius * radius
                selectcmpnt = False
                adding=False
            elif result == "AddCV":
                radius = mc.promptDialog(query=True, text=True)
                radius = float(radius)
                radius = radius * radius
                selectcmpnt = True
                adding=True
            elif result == "AddCrv":
                radius = mc.promptDialog(query=True, text=True)
                radius = float(radius)
                radius = radius * radius
                selectcmpnt = False
                adding=True                                                
            else:
                print "selection transfer cancelled"  
                return
        else:
            print "select a group of verts and a group of curves"
            return        
        targetSelection_crvs = [(each) for item in mc.ls(sl=1) if ".vtx" not in item for each in mc.listRelatives(item, ad=1, type="nurbsCurve")]
        verts = [(item) for item in mc.ls(sl=1) if ".vtx" in item]
        dropoff = radius
        if adding == False:
            mc.select(cl=1)
        else:
            mc.select(cl=1)
            mc.select(verts)
        collectmycurve = []
        for each_src in selObj:
            pos=mc.xform(each_src, ws=1, q=1, t=1)
            x_pos_min, x_pos_max, y_pos_min, y_pos_max, z_pos_min, z_pos_max = pos[0]-dropoff, pos[0]+dropoff, pos[1]-dropoff, pos[1]+dropoff, pos[2]-dropoff, pos[2]+dropoff 
            for each_tgt_crv  in targetSelection_crvs:
                # getpar=mc.listRelatives(each_tgt_crv, p=1, type="transform")[0]
                # tgt_pos=mc.xform(getpar, ws=1, q=1, t=1)
                tgt_sourcePoint = '{}.cv[0]'.format(each_tgt_crv)
                tgt_pos = mc.pointPosition(tgt_sourcePoint, w=1) 
                if tgt_pos[0] >= x_pos_min and tgt_pos[0] <= x_pos_max and tgt_pos[1] >= y_pos_min and tgt_pos[1] <= y_pos_max and tgt_pos[2] >= z_pos_min and tgt_pos[2] <= z_pos_max:
                    if selectcmpnt == True:
                        collectmycurve.append(tgt_sourcePoint)   
                    else:
                        collectmycurve.append(each_tgt_crv)  
        mc.select(collectmycurve, add=1)   


    def UV_select_transfer(self):
        selObj=mc.ls(sl=1, fl=1)
        if selObj:
            if len(selObj)<2:
                print "select a group of verts and another object which have similar UV maps(currently only works on 'map1')."
                return
            else:
                pass         
            #get falloff amount 
            result = mc.promptDialog(
                title="Confirm",
                message="Radius:",
                text=".5",
                button=["Swap","Add","Cancel"],
                cancelButton="Cancel",
                dismissString="Cancel" )
            if result == "Add":
                radius = mc.promptDialog(query=True, text=True)
                radius = float(radius)
                radius = radius * radius
                adding=True        
            elif result == "Swap":
                radius = mc.promptDialog(query=True, text=True)
                radius = float(radius)
                radius = radius * radius
                adding=False
            else:
                print "selection transfer cancelled"  
                return
        else:
            print "select a group of verts and another object which have similar UV maps(currently only works on 'map1')."
            return
        result = []
        bookit = [] 
        sourceSelection = selObj[:-1]
        targetSelection = selObj[-1]   
        if '.' in targetSelection :
            print "select object as last selection"
            return
        for each_src in sourceSelection:    
            selection_source = OpenMaya.MSelectionList()
            selection_source.add(each_src)
            nodeDagPath = selection_source.getDagPath(0)
            mfnMesh_src = OpenMaya.MFnMesh(nodeDagPath)        
            a = mc.xform(each_src,q=True,ws=True, t=True)
            getmpoint = OpenMaya.MPoint(a[0], a[1], a[2])
            uvSet = 'map1'
            placement = mfnMesh_src.getUVAtPoint(getmpoint, OpenMaya.MSpace.kWorld, uvSet)
            u = placement[0]
            v = placement[1]
            getlocators = self.newset(u, v, targetSelection)       
            try:
                returnselect = mMesh.get_closest_points(targetSelection, transform=getlocators, mesh=0, mesh_vtx=0, distance=radius)
                try:
                    mc.delete(getlocators)
                except:
                    pass
                try:
                    if type(returnselect[0]) != "NoneType":
                        bookit.append(returnselect)
                except:
                    pass
            except:
                pass
        if adding == False:
            mc.select(cl=1)   
        else:
            mc.select(sourceSelection, r=1)                 
        if bookit != None:
            for each_vert in bookit:
                try:
                    mc.select(each_vert, add=1)
                except:
                    # print "skipped"+ each_vert
                    pass



    def newset(self, u, v, targetSelection):
        mc.select(targetSelection, r=1)
        selection_last = OpenMaya.MSelectionList()
        selection_last.add(targetSelection)    
        nodeDagPath = selection_last.getDagPath(0)
        mfnMesh_tgt = OpenMaya.MFnMesh(nodeDagPath)    
        uvSet = 'map1'
        try:
            targetPoints = mfnMesh_tgt.getPointsAtUV(u, v, OpenMaya.MSpace.kWorld, uvSet, tolerance=1e-5)
            # print targetPoints
            objplace = (targetPoints[1][0][0], targetPoints[1][0][1] , targetPoints[1][0][2])
            transforms = []
            for each in objplace:
                if "e" in str(each):
                    newnum = str(each).split('e')[0]
                    transforms.append(float(newnum))
                else:
                    newnum = each
                    transforms.append(float(newnum))
            createtargetspace = mc.spaceLocator(n="newplace")
            mc.xform(createtargetspace[0], ws=1, t=transforms)
            return createtargetspace[0]
        except:
            pass

            def curve_select_nearest_crv(self):
        selObj=mc.ls(sl=1, fl=1)
        #query if selected
        if selObj:
            if len(selObj)<2:
                print "select two groups of curves."
                return
            else:
                pass         
            #get falloff amount 
            result = mc.promptDialog(
                title="Confirm",
                message="Radius:",
                text=".1",
                button=["Engage!","Cancel"],
                cancelButton="Cancel",
                dismissString="Cancel" )
            if result == "Engage!":
                radius = mc.promptDialog(query=True, text=True)
                radius = float(radius)
                radius = radius * radius
                selectcmpnt = True
                adding=True                                            
            else:
                print "selection transfer cancelled"  
                return
        else:
            print "select a group of verts and a group of curves"
            return
        targetSelection_crvs = [(mc.listRelatives(each, p=1, type="transform")[0]) for each in mc.listRelatives(selObj[1], ad=1, type="nurbsCurve")]
        driverSelection_crvs = [("{}.cv[0]".format(each)) for each in mc.listRelatives(selObj[0], ad=1, type="nurbsCurve")]
        if len(driverSelection_crvs)>0:
            pass
        else:
            pass
        dropoff = radius
        if adding == False:
            mc.select(cl=1)   
        collectmycurve = []
        for each_src in driverSelection_crvs:
            pos=mc.xform(each_src, ws=1, q=1, t=1)
            x_pos_min, x_pos_max, y_pos_min, y_pos_max, z_pos_min, z_pos_max = pos[0]-dropoff, pos[0]+dropoff, pos[1]-dropoff, pos[1]+dropoff, pos[2]-dropoff, pos[2]+dropoff 
            for tgt_cfv  in targetSelection_crvs:
                tgt_sourcePoint = "{}Shape.cv[0]".format(tgt_cfv)
                tgt_pos = mc.pointPosition(tgt_sourcePoint, w=1) 
                if tgt_pos[0] >= x_pos_min and tgt_pos[0] <= x_pos_max and tgt_pos[1] >= y_pos_min and tgt_pos[1] <= y_pos_max and tgt_pos[2] >= z_pos_min and tgt_pos[2] <= z_pos_max:
                    collectmycurve.append(tgt_cfv)
        mc.select(collectmycurve, r=1) 
    def curve_rename_nearest_crv(self):
        selObj=mc.ls(sl=1, fl=1)
        #query if selected
        if selObj:
            if len(selObj)<2:
                print "select two groups of curves."
                return
            else:
                pass         
            #get falloff amount 
            result = mc.promptDialog(
                title="Confirm",
                message="Radius:",
                text=".1",
                button=["Engage!","Cancel"],
                cancelButton="Cancel",
                dismissString="Cancel" )
            if result == "Engage!":
                radius = mc.promptDialog(query=True, text=True)
                radius = float(radius)
                radius = radius * radius
                selectcmpnt = True
                adding=True                                            
            else:
                print "selection transfer cancelled"  
                return
        else:
            print "select a group of verts and a group of curves"
            return
        targetSelection_crvs = [(mc.listRelatives(each, p=1, type="transform")[0]) for each in mc.listRelatives(selObj[1], ad=1, type="nurbsCurve")]
        driverSelection_crvs = [("{}.cv[0]".format(each)) for each in mc.listRelatives(selObj[0], ad=1, type="nurbsCurve")]
        if len(driverSelection_crvs)>0:
            pass
        else:
            pass
        dropoff = radius
        if adding == False:
            mc.select(cl=1)
        collectmycurve = []
        make_dict = {}
        for each_src in driverSelection_crvs:
            pos=mc.xform(each_src, ws=1, q=1, t=1)
            x_pos_min, x_pos_max, y_pos_min, y_pos_max, z_pos_min, z_pos_max = pos[0]-dropoff, pos[0]+dropoff, pos[1]-dropoff, pos[1]+dropoff, pos[2]-dropoff, pos[2]+dropoff 
            for tgt_cfv  in targetSelection_crvs:
                tgt_sourcePoint = "{}Shape.cv[0]".format(tgt_cfv)
                tgt_pos = mc.pointPosition(tgt_sourcePoint, w=1) 
                if tgt_pos[0] >= x_pos_min and tgt_pos[0] <= x_pos_max and tgt_pos[1] >= y_pos_min and tgt_pos[1] <= y_pos_max and tgt_pos[2] >= z_pos_min and tgt_pos[2] <= z_pos_max:
                    dict_new ={tgt_cfv:each_src+"_02_crv"}
                    make_dict.update(dict_new)
        for key, value in make_dict.items():
            try:
                mc.rename(key, value)
            except:
                pass         
inst_mkwin=set_select_win()
inst_mkwin.show()

# def get_dag_path(node):
#     """Get the MDagPath of the given node.

#     :param node: Node name
#     :return: Node MDagPath
#     """
#     selection_list = OpenMaya.MSelectionList()
#     print selection_list
#     selection_list.add(node)
#     path = OpenMaya.MDagPath()
#     selection_list.getDagPath(0)
#     return path 


# def getPosition(point):
#     print point
#     '''
#     Return the position of any point or transform
#     @param point: Point to return position for
#     @type point: str or list or tuple
#     '''
#     # Initialize point value
#     pos = []
#     if (type(point) == list) or (type(point) == tuple):
#         if len(point) < 3:
#             raise Exception('Invalid point value supplied! Not enough list/tuple elements!')
#         pos = point[0:3]
#     elif (type(point) == str) or (type(point) == unicode):
#         # Check Transform
#         mObject = getMObject(point)
#         if mObject.hasFn(OpenMaya.MFn.kTransform):
#             try: 
#                 pos = mc.xform(point,q=True,ws=True,rp=True)
#                 print pos
#             except: 
#                 pass
         
#         # pointPosition query
#         if not pos:
#             try: 
#                 pos = mc.pointPosition(point)
#                 print pos
#             except: 
#                 pass
#         # xform - rotate pivot query
#         if not pos:
#             try: 
#                 pos = mc.xform(point,q=True,ws=True,rp=True)
#                 print pos
#             except: 
#                 pass
#     #     # Unknown type
#     #     if not pos:
#     #         raise Exception('Invalid point value supplied! Unable to determine type of point "'+str(point)+'"!')
#     # else:
#     #     raise Exception('Invalid point value supplied! Invalid argument type!')
         
#     # # Return result
#     return pos
