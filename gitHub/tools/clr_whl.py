UVmaplist = [ 
            "uv_mapper.jpg", 
            "uv_checker large_secondlife.png",
            "UV_1k_blenderartist.jpg", 
            "UV_Grid_Sm pln_welleslyedu.jpg",
            "uvbypeterdackers-pixelsham-uv-mapping-png-1000_1000.png",
            "fi_uv_1024_radial_rgb_uvc_grid_ang24th_radfrac_by_fisholith_d7870eu-pre.jpg",
            "ashUVgrid_pintrest.jpg",
            "checker-map_thomasSchmall.png",
            "UVMap_biggy_markCastle.png",
            ]
uv_select = []
# color_select = ['Apply', 'Grey' , 'Red' , 'Green' , 'Blue' ,'Teal' ,'Yellow' ,'Purple' ,'Random' ,'Dark' ,'Light' ,'slight grey' ,'save gamut', 'tech_geo', 'contrast', 'reverse contrast']

color_select = ['Random', 'Grey' , 'Red' , 'Green' , 'Blue' ,'Teal' ,'Yellow' ,'Purple' ,'Dark' ,'Light' ,'Slight grey' ,'tech_geo', 'Contrast', 'Reverse contrast']
for each in UVmaplist:
    uv_select.append(each)

maphome ='images/UVmaps/'

class set_colors_win(QtWidgets.QMainWindow):
    # def __init__(self)
    def __init__(self):
        super(set_colors_win, self).__init__()
        self.initUI()

    def initUI(self):    
        '''
        Main window setup
        '''
        self.setWindowTitle("set colors")
        self.central_widget=QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.masterLayout=QtWidgets.QGridLayout(self.central_widget)
        self.masterLayout.setAlignment(QtCore.Qt.AlignTop)
        fileMenu = QtWidgets.QMenu("&Help", self)
        fileFile = QtWidgets.QMenu("&File", self)
        self.menuBar().addMenu(fileMenu)
        self.menuBar().addMenu(fileFile)

        fileMenu.addAction("&Open help page...", self.extractAction, "Ctrl+L")
        fileFile.addAction("&Save/Load Gamut...", self.save_gamut, "Ctrl+S")

        self.myform = QtWidgets.QFormLayout()
        self.layout = QtWidgets.QGridLayout()
        self.masterLayout.addLayout(self.layout, 0,0,1,1)



        self.colorSetupLayout = QtWidgets.QGridLayout()
        self.colorOverride = QtWidgets.QFrame()
        self.colorOverride.setStyleSheet("color: #efefef; background-color: rgba(100,100,100,70); ")
        self.colorOverride.setLayout(self.colorSetupLayout)

        self.vertical_order_layout_ta = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.vertical_order_layout_ta, 0,0,1,1)
        self.vertical_order_layout_ta.addWidget(self.colorOverride)

        self.color_dial = QtWidgets.QComboBox()
        self.color_dial.addItems(color_select)
        self.colorSetupLayout.addWidget(self.color_dial)

        self.colorchkLayout = QtWidgets.QHBoxLayout()
        self.colorchkOverride = QtWidgets.QFrame()
        self.colorchkOverride.setLayout(self.colorchkLayout)
        self.colorSetupLayout.addWidget(self.colorchkOverride)

        self.checkerLabel = QtWidgets.QLabel("Checker")
        self.colorchkLayout.addWidget(self.checkerLabel)        
        self.checker_checked = QtWidgets.QCheckBox()
        self.colorchkLayout.addWidget(self.checker_checked)
 
        self.prnt_verbose_button = QtWidgets.QPushButton("Apply Color")
        self.connect(self.prnt_verbose_button, SIGNAL("clicked()"),
                    lambda: self.create_rgb())
        self.colorSetupLayout.addWidget(self.prnt_verbose_button)  
        

        #sliders
        self.SSSetupLayout = QtWidgets.QGridLayout()
        self.SSOverride = QtWidgets.QFrame()
        self.SSOverride.setStyleSheet("color: #ffffff; background-color: rgba(120,120,120,50); border-style: solid; border-color:#434343;")
        self.SSOverride.setLayout(self.SSSetupLayout)

        self.ss_order_layout_ta = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.ss_order_layout_ta, 1,0,1,1)

        self.uv_label_row_layout = QtWidgets.QVBoxLayout()
        self.ss_order_layout_ta.addLayout(self.uv_label_row_layout)

        self.u_sliderinside_stack_layout = QtWidgets.QVBoxLayout()



        #tiles

        self.tileSetupLayout = QtWidgets.QGridLayout()
        self.tileOverride = QtWidgets.QFrame()
        self.tileOverride.setStyleSheet("color: #ffffff; background-color: rgba(120,120,120,50); border-style: solid; border-color:#434343;")
        self.tileOverride.setLayout(self.tileSetupLayout)

        self.u_sliderinside_stack_layout.addWidget(self.tileOverride)
        self.uv_label_row_layout.addLayout(self.u_sliderinside_stack_layout)

        self.utile_button = QtWidgets.QPushButton("U tile")
        self.connect(self.utile_button, SIGNAL("clicked()"),
                    lambda: self.util_set())
        self.tileSetupLayout.addWidget(self.utile_button,0,0,1,1)
        # self.uv_stack_tile_slide_row_layout.addWidget(self.utile_button) 
        self.vtile_button = QtWidgets.QPushButton("V tile")
        self.connect(self.vtile_button, SIGNAL("clicked()"),
                    lambda: self.vtil_set())
        self.tileSetupLayout.addWidget(self.vtile_button,1,0,1,1)

        self.UtextNum = QtWidgets.QLineEdit("1.0")
        self.UtextNum.setFixedWidth(50)
        self.UtextNum.connect(self.UtextNum,QtCore.SIGNAL("returnPressed()"),self.set_Uslider)
        self.tileSetupLayout.addWidget(self.UtextNum, 0,1,1,1)
        self.Utl_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal) 
        self.Utl_slider.setFixedWidth(200)
        self.Utl_slider.setSingleStep(0.1)
        self.Utl_slider.setMinimum(0)
        self.Utl_slider.setMaximum(200)
        self.Utl_slider.setValue(1)        
        self.Utl_slider.setTickInterval(2)
        self.Utl_slider.setTickPosition(self.Utl_slider.TicksBelow)
        self.Utl_slider.valueChanged.connect(self.print_Uslider)
        self.tileSetupLayout.addWidget(self.Utl_slider, 0,2,1,1)   


        self.VtextNum = QtWidgets.QLineEdit("1.0")
        self.VtextNum.setFixedWidth(50)
        self.VtextNum.connect(self.VtextNum,QtCore.SIGNAL("returnPressed()"),self.set_Vslider)
        self.tileSetupLayout.addWidget(self.VtextNum,1,1,1,1)
        self.Vtl_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal) 
        self.Vtl_slider.setFixedWidth(200)
        self.Vtl_slider.setSingleStep(0.1)
        self.Vtl_slider.setMinimum(0)
        self.Vtl_slider.setMaximum(200)
        self.Vtl_slider.setValue(1)        
        self.Vtl_slider.setTickInterval(2)
        self.Vtl_slider.setTickPosition(self.Vtl_slider.TicksBelow)
        self.Vtl_slider.valueChanged.connect(self.print_Vslider)
        self.tileSetupLayout.addWidget(self.Vtl_slider,1,2,1,1)
        
        

        #rot

        self.rotSetupLayout = QtWidgets.QGridLayout()
        self.rotOverride = QtWidgets.QFrame()
        self.rotOverride.setStyleSheet("color: #ffffff; background-color: rgba(120,120,120,50); border-style: solid; border-color:#434343;")
        self.rotOverride.setLayout(self.rotSetupLayout)

        self.u_sliderinside_stack_layout.addWidget(self.rotOverride)

        self.uvrot_button = QtWidgets.QLabel("UV rotate")
        # self.connect(self.uvrot_button, SIGNAL("clicked()"),
        #             lambda: self.utrn_set())
        self.rotSetupLayout.addWidget(self.uvrot_button, 0,0,1,1)
        self.UrottextNum = QtWidgets.QLineEdit("0")
        self.UrottextNum.setFixedWidth(50)
        self.UrottextNum.connect(self.UrottextNum,QtCore.SIGNAL("returnPressed()"),self.set_UV_rotslider)
        self.rotSetupLayout.addWidget(self.UrottextNum, 0,1,1,1)
        self.UVrot_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal) 
        self.UVrot_slider.setFixedWidth(200)
        self.UVrot_slider.setMinimum(0)
        self.UVrot_slider.setMaximum(360)
        self.UVrot_slider.setValue(0)        
        self.UVrot_slider.setTickInterval(5)
        self.UVrot_slider.setTickPosition(self.UVrot_slider.TicksBelow)
        self.UVrot_slider.valueChanged.connect(self.print_UvRotslider)
        self.rotSetupLayout.addWidget(self.UVrot_slider, 0,2,1,1)
        
      
        #trans
        self.trnsSetupLayout = QtWidgets.QGridLayout()
        self.trnsOverride = QtWidgets.QFrame()
        self.trnsOverride.setStyleSheet("color: #ffffff; background-color: rgba(120,120,120,50); border-style: solid; border-color:#434343;")
        self.trnsOverride.setLayout(self.trnsSetupLayout)

        self.u_sliderinside_stack_layout.addWidget(self.trnsOverride)

        self.utrns_button = QtWidgets.QPushButton("U translate")
        self.connect(self.utrns_button, SIGNAL("clicked()"),
                    lambda: self.utrn_set())
        self.trnsSetupLayout.addWidget(self.utrns_button, 0,0,1,1)
        
        self.UtrnstextNum = QtWidgets.QLineEdit("0.0")
        self.UtrnstextNum.setFixedWidth(50)
        self.UtrnstextNum.connect(self.UtrnstextNum,QtCore.SIGNAL("returnPressed()"),self.set_U_trnsslider)
        self.trnsSetupLayout.addWidget(self.UtrnstextNum, 0,1,1,1)
        self.Utrns_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal) 
        self.Utrns_slider.setFixedWidth(200)
        self.Utrns_slider.setMinimum(0)
        self.Utrns_slider.setMaximum(200)
        self.Utrns_slider.setValue(0)        
        self.Utrns_slider.setTickInterval(2)
        self.Utrns_slider.setTickPosition(self.Utrns_slider.TicksBelow)
        self.Utrns_slider.valueChanged.connect(self.print_Utrnsslider)
        self.trnsSetupLayout.addWidget(self.Utrns_slider, 0,2,1,1)
        
        
        

        self.vtrns_button = QtWidgets.QPushButton("V translate")
        self.connect(self.vtrns_button, SIGNAL("clicked()"),
                    lambda: self.vtrn_set())
        self.trnsSetupLayout.addWidget(self.vtrns_button, 1,0,1,1)
        self.VtrnstextNum = QtWidgets.QLineEdit("0.0")
        self.VtrnstextNum.setFixedWidth(50)
        self.VtrnstextNum.connect(self.VtrnstextNum,QtCore.SIGNAL("returnPressed()"),self.set_V_trnsslider)
        self.trnsSetupLayout.addWidget(self.VtrnstextNum, 1,1,1,1)
        self.Vtrns_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal) 
        self.Vtrns_slider.setFixedWidth(200)
        self.Vtrns_slider.setMinimum(0)
        self.Vtrns_slider.setMaximum(200)
        self.Vtrns_slider.setValue(0)        
        self.Vtrns_slider.setTickInterval(2)
        self.Vtrns_slider.setTickPosition(self.Vtrns_slider.TicksBelow)
        self.Vtrns_slider.valueChanged.connect(self.print_Vtrnsslider)
        self.trnsSetupLayout.addWidget(self.Vtrns_slider, 1,2,1,1)
        
        
        
        self.uvtile_butt_row_layout = QtWidgets.QVBoxLayout()
        self.ss_order_layout_ta.addLayout(self.uvtile_butt_row_layout)
        self.uvtile_button = QtWidgets.QPushButton("Apply UV only")
        self.connect(self.uvtile_button, SIGNAL("clicked()"),
                    lambda: self.vtil_set_only())
        self.SSSetupLayout.addWidget(self.uvtile_button) 

        self.uveyedrp_button = QtWidgets.QPushButton("Eyedrop UV")
        self.connect(self.uveyedrp_button, SIGNAL("clicked()"),
                    lambda: self.vtil_get())
        self.SSSetupLayout.addWidget(self.uveyedrp_button) 

        self.uvreset_button = QtWidgets.QPushButton("Reset sliders")
        self.connect(self.uvreset_button, SIGNAL("clicked()"),
                    lambda: self.vtil_reset())
        self.SSSetupLayout.addWidget(self.uvreset_button) 

        self.ss_order_layout_ta.addWidget(self.SSOverride)
        #UVMAP
        

        self.UVSetupLayout = QtWidgets.QGridLayout()
        self.UVOverride = QtWidgets.QFrame()
        self.UVOverride.setStyleSheet("color: #ffffff; background-color: rgba(255,255,255,30); border-style: solid; border-color:#434343;")
        self.UVOverride.setLayout(self.UVSetupLayout)

        self.text_order_layout_ta = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.text_order_layout_ta, 2,0,1,1)
        self.text_order_layout_ta.addWidget(self.UVOverride)

        self.uv_dial = QtWidgets.QComboBox()
        self.uv_dial.addItems(uv_select)
        self.UVSetupLayout.addWidget(self.uv_dial)
            
        self.uvmap_button = QtWidgets.QPushButton("Apply UVmap")
        self.connect(self.uvmap_button, SIGNAL("clicked()"),
                    lambda: self.type_uv(uv_load=self.uv_dial))
        self.UVSetupLayout.addWidget(self.uvmap_button)   

        self.setLayout(self.layout)
            

    def extractAction(self):
        '''
        opens the helppage for tool
        '''
        url="https://"
        subprocess.Popen('firefox open "%s"' % url, stdout=subprocess.PIPE, shell=True) 

    def vtil_set(self):
        '''
        forces the U tile slider to match the value on V tile slider
        '''
        getText = self.VtextNum.text()
        getText = float(getText)*10
        self.Utl_slider.setValue(getText)

    def util_set(self):
        '''
        forces the V tile slider to match the value on U tile slider
        '''        
        getText = self.UtextNum.text()
        getText = float(getText)*10
        self.Vtl_slider.setValue(getText)


    def vtrn_set(self):
        '''
        forces the V offset slider to match the value on U offset slider
        '''              
        getText = self.VtrnstextNum.text()
        getText = float(getText)*10
        self.Utrns_slider.setValue(getText)

    def utrn_set(self):
        '''
        forces the U offset slider to match the value on V offset slider
        '''          
        getText = self.UtrnstextNum.text()
        getText = float(getText)*10
        self.Vtrns_slider.setValue(getText)

    def print_Uslider(self):
        '''
        This connects the U tile slider to the field
        '''          
        size = self.Utl_slider.value()
        size_mult = size*0.10
        self.UtextNum.setText(str(size_mult))

    def print_UvRotslider(self):
        '''
        This connects the rotation slider value to the field of the rotation
        '''         
        size = self.UVrot_slider.value()
        self.UrottextNum.setText(str(size))

    def set_UV_rotslider(self):
        '''
        This updates the rotation slider value to the value in the field(in case of user input)
        '''
        getText = self.UrottextNum.text()
        getText = int(getText)
        self.UVrot_slider.setValue(getText)

    def print_Utrnsslider(self):
        '''
        This updates the rotation slider value to the value in the field(in case of user input)
        '''        
        size = self.Utrns_slider.value()
        size_mult = size*0.10
        self.UtrnstextNum.setText(str(size_mult))
            
            
    def set_U_trnsslider(self):
        getText = self.UtrnstextNum.text()
        getText = float(getText)*10
        self.Utrns_slider.setValue(getText)

    def print_Vtrnsslider(self):
        size = self.Vtrns_slider.value()
        size_mult = size*0.10
        self.VtrnstextNum.setText(str(size_mult))

    def set_V_trnsslider(self):
        getText = self.VtrnstextNum.text()
        getText = float(getText)*10
        self.Vtrns_slider.setValue(getText)


    def print_Vslider(self):
        size = self.Vtl_slider.value()
        size_mult = size*0.10
        self.VtextNum.setText(str(size_mult))

    def set_Uslider(self):
        getText = self.UtextNum.text()
        getText = float(getText)*10
        self.Utl_slider.setValue(getText)

    def set_Vslider(self):
        getText = self.VtextNum.text()
        getText = float(getvtText)*10
        self.Vtl_slider.setValue(getText)

    def getUV(self):
        Unsize = float(self.UtextNum.text())
        Vnsize = float(self.VtextNum.text())
        UV_rot = self.UVrot_slider.value()
        UV_rotnum = int(UV_rot)
        U_trnnum = float(self.VtrnstextNum.text())
        V_trnnum = float(self.VtrnstextNum.text())
        return Unsize, Vnsize, UV_rotnum, U_trnnum, V_trnnum




    def vtil_get(self): 
        try:
            getsel = mc.ls(sl=1, fl=1)[0]
            if len(getsel)>0:
                plcname = getsel+"_p2dt"
                if mc.objExists(plcname) == True:
                    Unsize = mc.getAttr(plcname+".repeatU")
                    self.Utl_slider.setValue(Unsize*10)
                    Vnsize = mc.getAttr(plcname+".repeatV")
                    self.Vtl_slider.setValue(Vnsize*10)
                    U_trnnum = mc.getAttr(plcname+".offsetU")
                    self.Utrns_slider.setValue(U_trnnum*10)
                    V_trnnum = mc.getAttr(plcname+".offsetV")
                    self.Vtrns_slider.setValue(V_trnnum*10)
                    UV_rotnum = mc.getAttr(plcname+".rotateUV")
                    self.UVrot_slider.setValue(UV_rotnum)
                else:
                    print " no object in scene called {}".format(plcname)
        except:
            print "nothing selected"
            return


    def vtil_reset(self):  
        getgrp = mc.ls(sl=1, fl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        self.Utl_slider.setValue(10)
        self.Vtl_slider.setValue(10)
        self.Utrns_slider.setValue(0)
        self.Vtrns_slider.setValue(0.0)
        self.UVrot_slider.setValue(0.0)

    def vtil_set_only(self):
        Unsize, Vnsize, UV_rotnum, U_trnnum, V_trnnum =self.getUV()  
        getgrp = mc.ls(sl=1, fl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        for each in getgrp:
            print each
            # if ":" in each:
            #     plcname = each.split(":")[-1]+"_p2dt"
            # else:
            plcname = each+"_p2dt"
            mc.setAttr(plcname+".repeatU", Unsize)
            mc.setAttr(plcname+".repeatV", Vnsize)
            mc.setAttr(plcname+".offsetU", U_trnnum)
            mc.setAttr(plcname+".offsetV", V_trnnum)
            
            
    def type_uv(self, uv_load):
        Unsize, Vnsize, UV_rotnum, U_trnnum, V_trnnum =self.getUV()   
        imgfile_name=uv_load.currentText() 
        imgfile = maphome+imgfile_name
        getgrp = mc.ls(sl=1, fl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        for each in getgrp:
            plcname = each+"_p2dt"
            namefile = each+"_file"
            chkname = each+"_ckr"
            name = each+"_shd"
            nameSG = each+"_shdSG"
            if len(mc.ls(name))>0:
                    mc.delete(name)
                    mc.delete(nameSG)
                    try:
                        mc.delete(plcname)
                    except:
                        pass
                    try:
                        mc.delete(namefile)
                    except:
                        pass
                    try:
                        mc.delete(chkname)
                    except:
                        pass
            FVfirst = mc.shadingNode('lambert', asShader=True, n=name)
            pdfirst = mc.shadingNode('place2dTexture', asUtility=True, n=plcname)
            filefirst = mc.shadingNode('file', asTexture = 1, isColorManaged = 1, n=namefile)
            getFVfirst=[FVfirst]
            setName="techanim_textures" 
            if mc.objExists(setName):
                pass
            else:
                mc.sets(n=setName, co=3)
            mc.sets(getFVfirst, add=setName)
            mc.select(each)
            mc.hyperShade(assign=str(FVfirst))           
            mc.connectAttr( plcname+'.outUV',namefile+'.uv', force=1)            
            mc.connectAttr( plcname+'.outUvFilterSize', namefile+'.uvFilterSize', force=1)    
            mc.connectAttr(namefile+".outColor",  each+"_shd.color", f=1)
            mc.setAttr(namefile+".fileTextureName",  imgfile, type = "string")
            mc.setAttr(plcname+".repeatU", Unsize)
            mc.setAttr(plcname+".repeatV", Vnsize)
            mc.setAttr(plcname+".offsetU", U_trnnum)
            mc.setAttr(plcname+".offsetV", V_trnnum)
            mc.setAttr(plcname+".rotateUV", UV_rotnum)    
        mc.select(getgrp, r=1)           
            
    def create_rgb(self):
        color_load=self.color_dial
        color_name=color_load.currentText()
        if color_name=='Apply':
            self._apply_colors()
        if color_name=='Grey':
            self._change_primary_gry()
        if color_name=='Red':
            self._change_primary_red()
        if color_name=='Green':
            self._change_primary_grn()
        if color_name=='Blue':
            self._change_primary_blue()
        if color_name=='Teal':
            self._change_primary_teal()
        if color_name=='Yellow':
            self._change_primary_orange()
        if color_name=='Purple':
            self._change_primary_prpl()
        if color_name=='Random':
            self._change_colors()
        if color_name=='Dark':
            self._change_darker()
        if color_name=='Light':
            self._change_lighter()
        if color_name=='Slight grey':
            self._slight_to_gry()            
        # if color_name=='Save gamut':
        #     self.save_gamut() 
        if color_name=='tech_geo':
            self.get_geo_techanim()     
        if color_name=='Contrast':
            self._strong_contrast()     
        if color_name=='Reverse contrast':
            self._rev_contrast() 
            
            
    def shd_changer(self, typecolor):
        Unsize, Vnsize, UV_rotnum, U_trnnum, V_trnnum =self.getUV() 
        getgrp = mc.ls(sl=1, fl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        checkerChecked = self.checker_checked
        if checkerChecked.isChecked():
            for each in getgrp:
                plcname = each+"_p2dt"
                namefile = each+"_file"
                chkname = each+"_ckr"
                name = each+"_shd"
                nameSG = each+"_shdSG"
                if len(mc.ls(name))>0:
                    mc.delete(name)
                    mc.delete(nameSG)
                    try:
                        mc.delete(plcname)
                    except:
                        pass
                    try:
                        mc.delete(namefile)
                    except:
                        pass
                    try:
                        mc.delete(chkname)
                    except:
                        pass
                FVfirst = mc.shadingNode('lambert', asShader=True, n=name)
                pdfirst = mc.shadingNode('place2dTexture', asUtility=True, n=plcname)
                mc.createNode( 'checker', n=chkname )
                getFVfirst=[FVfirst]
                setName="techanim_textures" 
                if mc.objExists(setName):
                    pass
                else:
                    mc.sets(n=setName, co=3)
                mc.sets(getFVfirst, add=setName)
                mc.select(each)
                mc.hyperShade(assign=str(FVfirst))
                mc.connectAttr( chkname+'.outColor', name+'.color', force=1)            
                mc.connectAttr( plcname+'.outUV',chkname+'.uv', force=1)            
                mc.connectAttr( plcname+'.outUvFilterSize',chkname+'.uvFilterSize', force=1)
                self.appSingleOrDouble(each, typecolor, plcname)   
        else:            
            for each in getgrp:
                plcname = each+"_p2dt"
                namefile = each+"_file"
                chkname = each+"_ckr"
                name = each+"_shd"
                nameSG = each+"_shdSG"              
                if len(mc.ls(name))>0:
                    mc.delete(name)
                    mc.delete(nameSG)
                    try:
                        mc.delete(plcname)
                    except:
                        pass
                    try:
                        mc.delete(namefile)
                    except:
                        pass
                    try:
                        mc.delete(chkname)
                    except:
                        pass
                # else:                
                FVfirst = mc.shadingNode('lambert', asShader=True, n=name)
                getFVfirst=[FVfirst]
                setName="techanim_textures" 
                if mc.objExists(setName):
                    pass
                else:
                    mc.sets(n=setName, co=3)
                mc.sets(getFVfirst, add=setName)
                mc.select(each)
                mc.hyperShade(assign=str(FVfirst))
                try:
                    set1, set2, set3  = self.gamble(typecolor) 
                    mc.setAttr(name+".color", set1, set2, set3, type="double3")
                except:
                    self.appSingleOrDouble(each, typecolor, plcname)                 
        mc.select(getgrp, r=1)   


    def appSingleOrDouble(self, shader_obj, typecolor, plcname):
        shdname = shader_obj
        Unsize, Vnsize, UV_rotnum, U_trnnum, V_trnnum =self.getUV()
        set1, set2, set3  = self.gamble(typecolor) 
        mc.setAttr(shdname+"_ckr.color1", set1, set2, set3, type="double3")
        set1, set2, set3  = self.gamble(typecolor) 
        mc.setAttr(shdname+"_ckr.color2", set1, set2, set3, type="double3") 
        mc.setAttr(shdname+"_p2dt.repeatU", Unsize)
        mc.setAttr(shdname+"_p2dt.repeatV", Vnsize)   
        mc.setAttr(shdname+"_p2dt.offsetU", U_trnnum)
        mc.setAttr(shdname+"_p2dt.offsetV", V_trnnum)
        mc.setAttr(shdname+"_p2dt.rotateUV", UV_rotnum) 

    def _change_primary_grn(self):
        self.shd_changer("green")

    def _change_primary_red(self):
        self.shd_changer("red")

    def _change_primary_blue(self):
        self.shd_changer("blue")

    def _apply_colors(self):
        self.shd_changer("random")

    def _change_primary_teal(self):
        self.shd_changer("teal")

    def _change_primary_orange(self):
        self.shd_changer("orange")

    def _change_primary_prpl(self):
        self.shd_changer("purple")

    def _apply_grey_colors(self):
        self.shd_changer("grey")

    def _change_primary_gry(self):
        self.shd_changer("grey")

    def _change_colors(self):
        self.shd_changer("random")

    def gamble(self, typecolor):
        getval = random.uniform(0.0,1.0)
        getvallow = random.uniform(0.0,0.25)   
        if typecolor == "green":
            set1= getvallow  
            set2=getval                        
            set3= getvallow  
        if typecolor == "red":
            set1= getval  
            set2=getvallow                        
            set3= getvallow     
        if typecolor == "blue":
            set1= getvallow  
            set2= getvallow                        
            set3= getval   
        if typecolor == "teal":
            set1= getvallow  
            set2= getval
            set3= getval         
        if typecolor == "orange":
            set1= getval  
            set2= getval                        
            set3= getvallow  
        if typecolor == "purple":
            set1= getval  
            set2= getvallow                        
            set3= getval    
        if typecolor == "grey":
            set1= getval  
            set2= getval                        
            set3= getval   
        if typecolor == "random":
            set1= random.uniform(0.0,1.0)  
            set2= random.uniform(0.0,1.0)                        
            set3= random.uniform(0.0,1.0)           
        return set1, set2, set3

    def get_geo_techanim(self):
        get_tech=mc.ls("*:*_tech_geo")
        get_tech_two=mc.ls("*_tech_geo")
        get_posttech=mc.ls("*:*_postTech_geo")
        get_posttech_two=mc.ls("*_postTech_geo")
        get_geo=get_tech+get_tech_two+get_posttech+get_posttech_two
        mc.select(get_geo, r=1)
        self._apply_colors()

    def _slight_to_gry(self):
        self.shader_slight("sl_grey")

    def _change_darker(self):
        self.shader_slight("dark")

    def _change_lighter(self):
        self.shader_slight("light")


    def gamble_slight(self, getval, typecolor):
        if typecolor == "sl_grey":
            getvallow = random.uniform(getval[0][0],getval[0][2])  
            set1= getvallow  
            set2= getvallow                        
            set3= getvallow 
        if typecolor == "dark":
            getvallow = random.uniform(0.0,0.25)
            newval = getval[0][0]-getvallow, getval[0][1]-getvallow, getval[0][2]-getvallow 
            set1= newval[0] 
            set2= newval[1]               
            set3= newval[2]
        if typecolor =="light":
            getvallow = random.uniform(0.0,0.25)
            newval = getval[0][0]+getvallow, getval[0][1]+getvallow, getval[0][2]+getvallow
            set1= newval[0] 
            set2= newval[1]               
            set3= newval[2] 
        return set1, set2, set3


    def shader_slight(self, typecolor):
        getgrp = mc.ls(sl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        mc.hyperShade (getgrp[0], smn=1)
        checkerChecked = self.checker_checked
        if checkerChecked.isChecked():
            for each in mc.ls(sl=1):
                self.appSingleOrDoubleSlight(each, typecolor)                                    
        else:                        
            for each in mc.ls(sl=1):
                try:
                    set1, set2, set3  = self.gamble_slight( each, typecolor) 
                    mc.setAttr(each+".color", set1, set2, set3, type="double3")
                except:
                    self.appSingleOrDoubleSlight(each, typecolor)                
        mc.select(getgrp, r=1)


    def appSingleOrDoubleSlight(self, shader_obj,  typecolor):
        shdname = shader_obj.split("_shd")[0]
        single = shader_obj+".color"
        double = shdname+"_ckr.color1"
        Unsize, Vnsize, UV_rotnum, U_trnnum, V_trnnum =self.getUV()
        if mc.objExists(single) == True:
            getval = mc.getAttr(shader_obj+".color")
            set1, set2, set3  = self.gamble_slight(getval, typecolor)
            try:
                mc.setAttr(shader_obj+".color", set1, set2, set3, type="double3")
            except:
                getval = mc.getAttr(shdname+"_ckr.color1")
                set1, set2, set3  = self.gamble_slight(getval, typecolor)                   
                mc.setAttr(shdname+"_ckr.color1", set1, set2, set3, type="double3")
                getval = mc.getAttr(shdname+"_ckr.color2")
                set1, set2, set3  = self.gamble_slight(getval, typecolor)                   
                mc.setAttr(shdname+"_ckr.color2", set1, set2, set3, type="double3")
        elif mcobjExists(double) == True:
            getval = mc.getAttr(shdname+"_ckr.color1")
            set1, set2, set3  = self.gamble_slight(getval, typecolor)                   
            mc.setAttr(shdname+"_ckr.color1", set1, set2, set3, type="double3")
            getval = mc.getAttr(shdname+"_ckr.color2")
            set1, set2, set3  = self.gamble_slight(getval, typecolor)                   
            mc.setAttr(shdname+"_ckr.color2", set1, set2, set3, type="double3")  
            # plcname = shdname+"_p2dt"
            mc.setAttr(shdname+"_p2dt.repeatU", Unsize)
            mc.setAttr(shdname+"_p2dt.repeatV", Vnsize)   
            mc.setAttr(shdname+"_p2dt.offsetU", U_trnnum)
            mc.setAttr(shdname+"_p2dt.offsetV", V_trnnum)
            mc.setAttr(shdname+"_p2dt.rotateUV", UV_rotnum)
        else:
            print "action not applicable"
            
    def _strong_contrast(self):
        Unsize, Vnsize, UV_rotnum, U_trnnum, V_trnnum =self.getUV()
        getgrp = mc.ls(sl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        for each in mc.ls(sl=1):
            try:
                getval = mc.getAttr(each.split("_shd")[0]+"_ckr.color1")
                getvallow = random.uniform(0.0,0.25)
                newval = getval[0][0]-getvallow, getval[0][1]-getvallow, getval[0][2]-getvallow             
                mc.setAttr(each.split("_shd")[0]+"_ckr.color1",newval[0], newval[1], newval[2],type="double3")
                getval = mc.getAttr(each.split("_shd")[0]+"_ckr.color2")
                getvallow = random.uniform(0.0,0.25)
                newval = getval[0][0]+getvallow, getval[0][1]+getvallow, getval[0][2]+getvallow           
                mc.setAttr(each.split("_shd")[0]+"_ckr.color2",newval[0], newval[1], newval[2],type="double3")
                plcname = each.split("_shd")[0]+"_p2dt"  
                mc.setAttr( each.split("_shd")[0]+"_p2dt.repeatU", Unsize)
                mc.setAttr( each.split("_shd")[0]+"_p2dt.repeatV", Vnsize)
                mc.setAttr( each.split("_shd")[0]+"_p2dt.offsetU", U_trnnum)
                mc.setAttr( each.split("_shd")[0]+"_p2dt.offsetV", V_trnnum)
                mc.setAttr( each.split("_shd")[0]+"_p2dt.rotateUV", UV_rotnum)
            except:
                print "only affects checkered textures"               
                pass           
        mc.select(getgrp, r=1)

    def _rev_contrast(self):
        Unsize, Vnsize, UV_rotnum, U_trnnum, V_trnnum =self.getUV()
        getgrp = mc.ls(sl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        for each in mc.ls(sl=1):
            try:
                getval = mc.getAttr(each.split("_shd")[0]+"_ckr.color1")
                getvallow = random.uniform(0.0,0.25)
                newval = getval[0][0]+getvallow, getval[0][1]+getvallow, getval[0][2]+getvallow             
                mc.setAttr(each.split("_shd")[0]+"_ckr.color1",newval[0], newval[1], newval[2],type="double3")
                getval = mc.getAttr(each.split("_shd")[0]+"_ckr.color2")
                getvallow = random.uniform(0.0,0.25)
                newval = getval[0][0]-getvallow, getval[0][1]-getvallow, getval[0][2]-getvallow           
                mc.setAttr(each.split("_shd")[0]+"_ckr.color2",newval[0], newval[1], newval[2],type="double3")  
                mc.setAttr(each.split("_shd")[0]+"_p2dt.repeatU", Unsize)
                mc.setAttr(each.split("_shd")[0]+"_p2dt.repeatV", Vnsize)
                mc.setAttr(each.split("_shd")[0]+"_p2dt.offsetU", U_trnnum)
                mc.setAttr(each.split("_shd")[0]+"_p2dt.offsetV", V_trnnum)
                mc.setAttr(each.split("_shd")[0]+"_p2dt.rotateUV", UV_rotnum)                
            except:
                print "only affects checkered textures"               
                pass           
        mc.select(getgrp, r=1) 


    def _change_ambient(self):
        getgrp = mc.ls(sl=1)
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        mc.hyperShade (getgrp[0], smn=1)
        for each in mc.ls(sl = 1):
            get_float = random.uniform(0.0,1.0)
            mc.setAttr(each+".incandescence", get_float, get_float, get_float, type="double3")
        mc.select(getgrp, r=1)  



    def save_gamut(self, arg=None):
        self.saveSelection()

    def saveSelection(self, arg=None):
        getScenePath=mc.file(q=1, location=1)
        getPathSplit=getScenePath.split("/")
        folderPath='\\'.join(getPathSplit[:-1])+"\\"
        selObj=mc.ls(sl=1, sn=1)
        getScenePath=mc.file(q=1, location=1)
        getPathSplit=getScenePath.split("/")
        newfolderPath=re.sub(r'\\',r'/', folderPath)
        folderBucket=[]
        winName = "Save selected externally"
        winTitle = winName
        if mc.window(winName, exists=True):
                deleteUI(winName)
        window = mc.window(winName, title=winTitle, tbm=1, w=620, h=100 )
        mc.rowColumnLayout  (' selectArrayRow ', nr=1, w=620)
        mc.frameLayout('bottomFrame', label='', lv=0, nch=1, borderStyle='in', bv=1, p='selectArrayRow')      
        mc.gridLayout('listBuildButtonLayout', p='bottomFrame', numberOfColumns=1, cellWidthHeight=(600, 20))         
        fieldBucket=[]
        objNameFile=str(newfolderPath)
        filebucket = [os.path.join(dirpath, name) for dirpath, dirnames, files in os.walk(objNameFile) for name in files if name.lower().endswith(".txt")]
        self.fileDropName=mc.optionMenu( label='files')
        for each in filebucket:
            mc.menuItem( label=each)        
        mc.rowLayout  (' listBuildButtonLayout ', w=600, numberOfColumns=6, cw6=[350, 40, 40, 40, 40, 1], ct6=[ 'both', 'both', 'both',  'both', 'both', 'both'], p='bottomFrame')
        self.getName=mc.textField(h=25, p='listBuildButtonLayout', text=objNameFile)
        mc.button (label='Save', w=90, p='listBuildButtonLayout', command = lambda *args:self._save_select(fileName=mc.textField(self.getName, q=1, text=1)))            
        mc.button (label='Load', p='listBuildButtonLayout', command = lambda *args:self._load_selection(printFolder=mc.textField(self.getName, q=1, text=1), grabFileName=mc.optionMenu(self.fileDropName, q=1, v=1)))
        mc.showWindow(window)
                                                                                                           
    def _save_select(self, fileName):   
        getgrp=mc.ls(sl=1, fl=1)   
        if len(getgrp)>0:
            pass
        else:
            print "nothing selected"
            return
        fileName=fileName+'_color.txt'
        print fileName
        inp=open(fileName, 'w+')
        # inp.write(str("colorDictionary = {"))
        mc.hyperShade (getgrp[0], smn=1)
        for each in mc.ls(sl = 1):
            getItemName = each.split("_shd")[0]
            if mc.objExists(getItemName+"_ckr") == True:
                chkcl1 = mc.getAttr(getItemName+"_ckr.color1")
                chkcl2 = mc.getAttr(getItemName+"_ckr.color2")
                Unsize = mc.getAttr(getItemName+"_p2dt.repeatU")
                Vnsize = mc.getAttr(getItemName+"_p2dt.repeatV")
                U_trnnum = mc.getAttr(getItemName+"_p2dt.offsetU")
                V_trnnum = mc.getAttr(getItemName+"_p2dt.offsetV")
                UV_rotnum = mc.getAttr(getItemName+"_p2dt.rotateUV")                                                                                                  
                chkname = getItemName+"_ckr"
                inp.write(str(chkname)+"|"+str(chkcl1)+"<"+str(chkcl2)+"<"+str(Unsize)+">"+str(Vnsize)+">"+str(U_trnnum)+">"+str(V_trnnum)+">"+str(UV_rotnum)+" , ")
            elif mc.objExists(getItemName+"_file") == True: 
                print "file"
                namefile = getItemName+"_file"
                getItemName = each.split("_shd")[0]
                getUVimage = mc.getAttr(namefile+".fileTextureName")
                Unsize = mc.getAttr(getItemName+"_p2dt.repeatU")
                Vnsize = mc.getAttr(getItemName+"_p2dt.repeatV")
                U_trnnum = mc.getAttr(getItemName+"_p2dt.offsetU")
                V_trnnum = mc.getAttr(getItemName+"_p2dt.offsetV")
                UV_rotnum = mc.getAttr(getItemName+"_p2dt.rotateUV")      
                inp.write(str(namefile)+"|"+str(getUVimage)+"<"+str(Unsize)+">"+str(Vnsize)+">"+str(U_trnnum)+">"+str(V_trnnum)+">"+str(UV_rotnum)+" , ")
            else:
                try:
                    getval = mc.getAttr(each+".color")
                    inp.write(str(each)+"|"+str(getval)+" , ")  
                except:
                    print "{} does not have a shader group assigned in scene. Skipping".format(each)          
        inp.close()   
        print "saved as "+fileName
            
    def _load_selection(self, printFolder, grabFileName): 
        printFolder=grabFileName  
        if os.path.exists(printFolder):
            pass
        else:
            print printFolder+"does not exist"
            return
        getBucket=[]
        attribute_container=[]
        List = open(printFolder).readlines()
        create_dict = {}
        for aline in List:
            a_list = list(aline)
            a_list = aline.split(" , ")
        if len(a_list)>0:
            for each in a_list:
                listp1=each.split("|")
                print listp1[0]
                if len(listp1)>1:
                    if "_ckr" in listp1[0]:
                        chkname = listp1[0]                 
                        shdr_name=listp1[0].split("_ckr")[0]+"_shd"
                        scnobject = listp1[0].split("_ckr")[0]
                        plcname=listp1[0].split("_ckr")[0]+"_p2dt"
                        namefile=listp1[0].split("_ckr")[0]+"_file"
                        if mc.objExists(namefile) == True:
                            mc.delete(namefile) 
                        if mc.objExists(shdr_name) == False: 
                            FVfirst = mc.shadingNode('lambert', asShader=True, n=shdr_name)
                            mc.hyperShade(assign=str(FVfirst))
                            getFVfirst=[FVfirst]
                            setName="techanim_textures" 
                            if mc.objExists(setName):
                                pass
                            else:
                                mc.sets(n=setName, co=3)       
                            mc.sets(getFVfirst, add=setName)
                            mc.select(scnobject)
                            mc.hyperShade(assign=str(FVfirst))
                        if mc.objExists(plcname) == False:    
                            mc.shadingNode('place2dTexture', asUtility=True, n=plcname)
                        if mc.objExists(chkname) == False: 
                            mc.createNode( 'checker', n=chkname )
                        mc.connectAttr( chkname+'.outColor', shdr_name+'.color', force=1)            
                        mc.connectAttr( plcname+'.outUV',chkname+'.uv', force=1)            
                        mc.connectAttr( plcname+'.outUvFilterSize',chkname+'.uvFilterSize', force=1)
                        colget=listp1[-1].split("<")
                        clrs1 = ast.literal_eval(colget[0])
                        clrs2 = ast.literal_eval(colget[1])
                        mc.setAttr(chkname+".color1", clrs1[0][0],clrs1[0][1], clrs1[0][2], type="double3")
                        mc.setAttr(chkname+".color2", clrs2[0][0],clrs2[0][1], clrs2[0][2], type="double3")
                        plc_get=colget[-1].split(">")
                        mc.setAttr(plcname+".repeatU", float(plc_get[0]))
                        mc.setAttr(plcname+".repeatV", float(plc_get[1]))
                        mc.setAttr(plcname+".offsetU", float(plc_get[2]))
                        mc.setAttr(plcname+".offsetV", float(plc_get[3]))
                        mc.setAttr(plcname+".rotateUV", float(plc_get[4]))    
                    elif "_file" in listp1[0]:
                        namefile = listp1[0]
                        shdr_name=listp1[0].split("_file")[0]+"_shd"
                        scnobject = listp1[0].split("_file")[0]
                        plcname=listp1[0].split("_file")[0]+"_p2dt"
                        chkname=listp1[0].split("_file")[0]+"_ckr"
                        if mc.objExists(chkname) == True:
                            mc.delete(chkname) 
                        if mc.objExists(shdr_name) == False: 
                            FVfirst = mc.shadingNode('lambert', asShader=True, n=shdr_name)
                            mc.hyperShade(assign=str(FVfirst))
                            getFVfirst=[FVfirst]
                            setName="techanim_textures" 
                            if mc.objExists(setName):
                                pass
                            else:
                                mc.sets(n=setName, co=3)          
                            mc.sets(getFVfirst, add=setName)
                            mc.select(scnobject)
                            mc.hyperShade(assign=str(FVfirst))          
                        if mc.objExists(plcname) == False:    
                            mc.shadingNode('place2dTexture', asUtility=True, n=plcname)
                        if mc.objExists( listp1[0]) == False: 
                            filefirst = mc.shadingNode('file', asTexture = 1, isColorManaged = 1, n=namefile)        
                        mc.connectAttr( plcname+'.outUV',namefile+'.uv', force=1)            
                        mc.connectAttr( plcname+'.outUvFilterSize', namefile+'.uvFilterSize', force=1)    
                        mc.connectAttr(namefile+".outColor",  shdr_name+".color", f=1)
                        filegrb=listp1[-1].split("<")
                        mc.setAttr(namefile+".fileTextureName",  filegrb[0], type = "string")
                        plc_get=filegrb[-1].split(">")
                        mc.setAttr(plcname+".repeatU", float(plc_get[0]))
                        mc.setAttr(plcname+".repeatV", float(plc_get[1]))
                        mc.setAttr(plcname+".offsetU", float(plc_get[2]))
                        mc.setAttr(plcname+".offsetV", float(plc_get[3]))
                        mc.setAttr(plcname+".rotateUV", float(plc_get[4]))
                    else:
                        scnobject = listp1[0].split("_shd")[0]
                        if mc.objExists(scnobject) == True:
                            chkname=listp1[0].split("_shd")[0]+"_ckr"
                            plcname=listp1[0].split("_shd")[0]+"_p2dt"
                            namefile=listp1[0].split("_shd")[0]+"_file"
                            if mc.objExists(chkname) == True:
                                mc.delete(chkname) 
                            if mc.objExists(namefile) == True:
                                mc.delete(namefile)     
                            if mc.objExists(plcname) == True:
                                mc.delete(plcname)                                       
                            s = eval(str(listp1[1]))
                            mc.setAttr(listp1[0]+".color", s[0][0],s[0][1], s[0][2], type="double3")
                        else:
                            print "{} does not exist in scene. Skipping".format(scnobject) 
inst_mkwin=set_colors_win()
inst_mkwin.show()                        
                        
                                          
