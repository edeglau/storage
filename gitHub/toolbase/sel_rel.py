'''(This launches a GUI) Select or set your strands to static or dynamic'''
''''latest update: signal change'''
import maya.cmds as mc
import os, sys

import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets


class select_rel_win(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(select_rel_win, self).__init__(parent = None)

        self.setWindowTitle("Select Related")
        self.central_widget=QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.masterLayout=QtWidgets.QGridLayout(self.central_widget)
        self.masterLayout.setAlignment(QtCore.Qt.AlignTop)        self.myform = QtWidgets.QFormLayout()
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
        self.plot_order_layout = QtWidgets.QHBoxLayout()
        self.myform.addRow(self.plot_order_layout) 
        self.plot_button_layout = QtWidgets.QVBoxLayout()
        self.plot_order_layout.addLayout(self.plot_button_layout)
        self.plot_slid_layout = QtWidgets.QVBoxLayout()
        self.plot_order_layout.addLayout(self.plot_slid_layout)   
        self.plot_slider_layout = QtWidgets.QVBoxLayout()     
        self.plot_slid_layout.addLayout(self.plot_slider_layout)   

        self.sel_nuc_button=QtWidgets.QPushButton("grab nucleus")
        self.sel_nuc_button.setToolTip("grab dynamic nucleus connected with selection")
        self.sel_nuc_button.clicked.connect(lambda: self.grab_nucleus())
        self.plot_button_layout.addWidget(self.sel_nuc_button)

        self.sel_msh_h_button=QtWidgets.QPushButton("grab mesh heirarchy")
        self.sel_msh_h_button.setToolTip("grab dynamic nucleus connected with selection")
        self.sel_msh_h_button.clicked.connect(lambda: self.select_mesh_heirarchy())
        self.plot_button_layout.addWidget(self.sel_nuc_button)
        self.sel_msh_button=QtWidgets.QPushButton("grab mesh")
        self.sel_msh_button.setToolTip("grab the mesh of the selected cloth")
        self.sel_msh_button.clicked.connect(lambda: self._grab_mesh())
        self.plot_button_layout.addWidget(self.sel_msh_button)

        self.sel_clth_button=QtWidgets.QPushButton("grab ncloth")
        self.sel_clth_button.setToolTip("grab the cloth of the selected mesh")
        self.sel_clth_button.clicked.connect(lambda: self.selectNcloth())
        self.plot_button_layout.addWidget(self.sel_clth_button)

        self.sel_hr_button=QtWidgets.QPushButton("grab nhair")
        self.sel_hr_button.setToolTip("grab the cloth of the selected mesh")
        self.sel_hr_button.clicked.connect(lambda: self.selectNhair())
        self.plot_button_layout.addWidget(self.sel_hr_button)

        self.sel_crvW_button=QtWidgets.QPushButton("grab crv w wire")
        self.sel_crvW_button.setToolTip("grab the cloth of the selected mesh")
        self.sel_crvW_button.clicked.connect(lambda: self.seleccrvwwire())
        self.plot_button_layout.addWidget(self.sel_crvW_button)

        self.sel_cche_button=QtWidgets.QPushButton("grab cache")
        self.sel_cche_button.setToolTip("grab the cache file of the selected object")
        self.sel_cche_button.clicked.connect(lambda: self.selectNclothCache())
        self.plot_button_layout.addWidget(self.sel_cche_button)

        self.sel_blnd_button=QtWidgets.QPushButton("grab blend shape")
        self.sel_blnd_button.setToolTip("grab the blend file of the selected object")
        self.sel_blnd_button.clicked.connect(lambda: self.grab_blend())
        self.plot_button_layout.addWidget(self.sel_blnd_button)
        self.sel_cntstrnt_button=QtWidgets.QPushButton("grab nConstraint")
        self.sel_cntstrnt_button.setToolTip("grab the nconstraints")
        self.sel_cntstrnt_button.clicked.connect(lambda: self.selectNconstraint())
        self.plot_button_layout.addWidget(self.sel_cntstrnt_button)

        self.sel_crv_button=QtWidgets.QPushButton("grab crv")
        self.sel_crv_button.setToolTip("grab the nconstraints")
        self.sel_crv_button.clicked.connect(lambda: self.seleccrv())
        self.plot_button_layout.addWidget(self.sel_crv_button)

    def seleccrvwwire(self):
        getall = mc.listRelatives(mc.ls(sl=1), ap=1)
        getcrv = [(each) for item in getall for each in mc.listRelatives(item, ad=1,  type = "nurbsCurve") if mc.listConnections(each, s=1, type="wire")]
        mc.select(getcrv, r=1)
                                                
    def seleccrv(self):
        getall = mc.listRelatives(mc.ls(sl=1), ap=1)
        getcrv = [(each) for item in getall for each in mc.listRelatives(item, ad=1,  type = "nurbsCurve")]
        mc.select(getcrv, r=1)


    def selectNconstraint(self):
        findThisType=["dynamicConstraint"]
        self.grab_item(findThisType)        



    def grab_blend(self):
        findThisType=["blendShape"]
        getSel=mc.ls(sl=1)
        mc.select(cl=1)
        collect=[]
        if len(getSel)==0:
            getSel=mc.ls(type=findThisType)  
            collect.append(getSel) 
        else:
            for each in getSel:
                if mc.nodeType(each)== "transform":
                    getitem=mc.listRelatives(each, ad=1, type="shape")
                    for item in getitem:
                        getNode=mc.listConnections(item, type='blendShape')
                        if getNode != None:
                            collect.append(getNode)   
                else:
                    for item in getSel:
                        try:
                            getNode=mc.listConnections(each, type='blendShape')
                        except:
                            pass
                        if len(getNode)>0:
                            print getNode
                            collect.append(getNode)   
        if len(collect)>0: 
            mc.select(collect[0], add=1)        


    def selectNclothCache(self):
        findThisType = ["cacheFile", "AlembicNode"]
        self.grab_item(findThisType)    
                                        
    def selectNhair(self):
        findThisType = ["hairSystem"]
        self.grab_item(findThisType)        


    def _grab_mesh(self):
        findThisType = ["mesh"]
        self.grab_item(findThisType)         


    def selectNclothMesh(self):
        # findThisType = ["mesh"]
        # self.grab_item(findThisType)           
        typeN="mesh"
        getSel=mc.ls(sl=1)
        if len(getSel)<1:
            getNode=[(item) for each in mc.ls(type=typeN) for item in mc.listRelatives(each, c=1, type="transform") if "Orig" not in str(each)]
        else:
            getNode=[(item) for each in mc.ls(sl=1) for item in mc.listHistory(each, f=1) if mc.nodeType(item) == "mesh"]
        if getNode != None:
            mc.select(getNode, r=1)

    def select_mesh_heirarchy(self):
        grabMesh = [(each) for each in mc.listRelatives(mc.ls(sl=1), ad=1, type="mesh") if "Orig" and "Deformed" not in each]
        mc.select(grabMesh, r=1)


    def selectNcloth(self):
        findThisType=["nCloth"]
        self.grab_item(findThisType)        


    def grab_nucleus(self):
        findThisType=["nucleus"]
        self.grab_item(findThisType)



    def grab_item(self, findThisType):
        getSel=mc.ls(sl=1)
        mc.select(cl=1)
        collect=[]
        if len(getSel)==0:
            getSel=mc.ls(type=findThisType)  
            collect.append(getSel) 
        else:
            for each in getSel:
                getNode=[each_node for each_node in mc.listHistory(each, ac=1) for eachCacheNode in findThisType if mc.nodeType(each_node) == eachCacheNode]
                if getNode != None:
                    collect.append(getNode)           
        mc.select(collect[0], add=1)



inst_win = select_rel_win()
inst_win.show()    	   



