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

maphome ='/jobs/rnd_rigging11/COMMON/images/UVmaps/'

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
        
        
        
