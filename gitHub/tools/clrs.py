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
        self.setWindowTitle('set colors')
        self.central_widget=QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.master_layout=QtWidgets.QGridLayout(self.central_widget)
        self.master_layout.setAlignment(QtCore.Qt.AlignTop)
        file_menu = QtWidgets.QMenu('&Help', self)
        file_save_load_menu = QtWidgets.QMenu('&File', self)
        self.menuBar().addMenu(file_menu)
        self.menuBar().addMenu(file_save_load_menu)

        file_menu.addAction('&Open help page...', self.help_page_launch, 'Ctrl+L')
        file_save_load_menu.addAction('&Save/Load Gamut...', self.saveGamut, 'Ctrl+S')

        self.myform = QtWidgets.QFormLayout()
        self.layout = QtWidgets.QGridLayout()
        self.master_layout.addLayout(self.layout, 0,0,1,1)

        self.myform = QtWidgets.QFormLayout()
        self.layout = QtWidgets.QGridLayout()
        self.master_layout.addLayout(self.layout, 0,0,1,1)

        self.color_setup_layout = QtWidgets.QGridLayout()
        self.color_override = QtWidgets.QFrame()
        self.color_override.setStyleSheet('color: #efefef; background-color: rgba(100,100,100,70); ')
        self.color_override.setLayout(self.color_setup_layout)

        self.vertical_order_layout_ta = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.vertical_order_layout_ta, 0,0,1,1)
        self.vertical_order_layout_ta.addWidget(self.color_override)


        self.color_dial = QtWidgets.QComboBox()
        self.color_dial.addItems(color_select)
        self.color_setup_layout.addWidget(self.color_dial)

        self.color_chk_layout = QtWidgets.QHBoxLayout()
        self.color_chk_frame = QtWidgets.QFrame()
        self.color_chk_frame.setLayout(self.color_chk_layout)
        self.color_setup_layout.addWidget(self.color_chk_frame)

        self.checker_label = QtWidgets.QLabel('Checker')
        self.color_chk_layout.addWidget(self.checker_label)        
        self.checker_checked = QtWidgets.QCheckBox()
        self.color_chk_layout.addWidget(self.checker_checked)
 
        self.prnt_verbose_button = QtWidgets.QPushButton('Apply Color')
        self.connect(self.prnt_verbose_button, SIGNAL('clicked()'),
                    lambda: self.apply_rgb())
        self.color_setup_layout.addWidget(self.prnt_verbose_button) 

        self.ss_order_layout_ta = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.ss_order_layout_ta, 1,0,1,1)

        #UV tiles
        self.tile_setup_layout = QtWidgets.QGridLayout()
        self.uv_tile_frame = QtWidgets.QFrame()
        self.uv_tile_frame.setStyleSheet('color: #ffffff; background-color: rgba(120,120,120,50); border-style: solid; border-color:#434343;')
        self.uv_tile_frame.setLayout(self.tile_setup_layout)

        self.u_sliderinside_stack_layout = QtWidgets.QVBoxLayout()
        self.u_sliderinside_stack_layout.addWidget(self.uv_tile_frame)

        self.uv_label_row_layout = QtWidgets.QVBoxLayout()
        self.ss_order_layout_ta.addLayout(self.uv_label_row_layout)


        self.uv_label_row_layout.addLayout(self.u_sliderinside_stack_layout)

        self.u_tile_button = QtWidgets.QPushButton('U tile')
        self.connect(self.u_tile_button, SIGNAL('clicked()'),
                    lambda: self.u_tile_force())
        self.tile_setup_layout.addWidget(self.u_tile_button,0,0,1,1)
        self.vtile_button = QtWidgets.QPushButton('V tile')
        self.connect(self.vtile_button, SIGNAL('clicked()'),
                    lambda: self.v_tile_force())
        self.tile_setup_layout.addWidget(self.vtile_button,1,0,1,1)

        self.u_tile_line_edit = QtWidgets.QLineEdit('1.0')
        self.u_tile_line_edit.setFixedWidth(50)
        self.u_tile_line_edit.connect(self.u_tile_line_edit,QtCore.SIGNAL('returnPressed()'),self.text_set_u_tile_slider)
        self.tile_setup_layout.addWidget(self.u_tile_line_edit, 0,1,1,1)
        self.u_tile_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal) 
        self.u_tile_slider.setFixedWidth(200)
        self.u_tile_slider.setSingleStep(0.1)
        self.u_tile_slider.setMinimum(0)
        self.u_tile_slider.setMaximum(200)
        self.u_tile_slider.setValue(1)        
        self.u_tile_slider.setTickInterval(2)
        self.u_tile_slider.setTickPosition(self.u_tile_slider.TicksBelow)
        self.u_tile_slider.valueChanged.connect(self.slider_set_u_tile_text)
        self.tile_setup_layout.addWidget(self.u_tile_slider, 0,2,1,1)
            
        self.v_tile_line_edit = QtWidgets.QLineEdit('1.0')
        self.v_tile_line_edit.setFixedWidth(50)
        self.v_tile_line_edit.connect(self.v_tile_line_edit,QtCore.SIGNAL('returnPressed()'),self.text_set_v_tile_slider)
        self.tile_setup_layout.addWidget(self.v_tile_line_edit,1,1,1,1)
        self.v_tile_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal) 
        self.v_tile_slider.setFixedWidth(200)
        self.v_tile_slider.setSingleStep(0.1)
        self.v_tile_slider.setMinimum(0)
        self.v_tile_slider.setMaximum(200)
        self.v_tile_slider.setValue(1)        
        self.v_tile_slider.setTickInterval(2)
        self.v_tile_slider.setTickPosition(self.v_tile_slider.TicksBelow)
        self.v_tile_slider.valueChanged.connect(self.slider_set_v_tile_text)
        self.tile_setup_layout.addWidget(self.v_tile_slider,1,2,1,1)

            

        #uv rot

        self.uv_rot_setup_layout = QtWidgets.QGridLayout()
        self.uv_rot_frame = QtWidgets.QFrame()
        self.uv_rot_frame.setStyleSheet('color: #ffffff; background-color: rgba(120,120,120,50); border-style: solid; border-color:#434343;')
        self.uv_rot_frame.setLayout(self.uv_rot_setup_layout)

        self.u_sliderinside_stack_layout.addWidget(self.uv_rot_frame)

        self.uv_rot_button = QtWidgets.QLabel('UV rotate')
        self.uv_rot_setup_layout.addWidget(self.uv_rot_button, 0,0,1,1)
        self.uv_rot_line_edit = QtWidgets.QLineEdit('0')
        self.uv_rot_line_edit.setFixedWidth(50)
        self.uv_rot_line_edit.connect(self.uv_rot_line_edit,QtCore.SIGNAL('returnPressed()'),self.text_set_rot_slider)
        self.uv_rot_setup_layout.addWidget(self.uv_rot_line_edit, 0,1,1,1)
        self.uv_rot_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal) 
        self.uv_rot_slider.setFixedWidth(200)
        self.uv_rot_slider.setMinimum(0)
        self.uv_rot_slider.setMaximum(360)
        self.uv_rot_slider.setValue(0)        
        self.uv_rot_slider.setTickInterval(5)
        self.uv_rot_slider.setTickPosition(self.uv_rot_slider.TicksBelow)
        self.uv_rot_slider.valueChanged.connect(self.slider_set_rot_text)
        self.uv_rot_setup_layout.addWidget(self.uv_rot_slider, 0,2,1,1)

        #uv trans
        self.uv_trns_setup_layout = QtWidgets.QGridLayout()
        self.uv_trns_frame = QtWidgets.QFrame()
        self.uv_trns_frame.setStyleSheet('color: #ffffff; background-color: rgba(120,120,120,50); border-style: solid; border-color:#434343;')
        self.uv_trns_frame.setLayout(self.uv_trns_setup_layout)

        self.u_sliderinside_stack_layout.addWidget(self.uv_trns_frame)

        self.u_trns_button = QtWidgets.QPushButton('U translate')
        self.connect(self.u_trns_button, SIGNAL('clicked()'),
                    lambda: self.u_trns_force())
        self.uv_trns_setup_layout.addWidget(self.u_trns_button, 0,0,1,1)
            
        self.u_trns_line_edit = QtWidgets.QLineEdit('0.0')
        self.u_trns_line_edit.setFixedWidth(50)
        self.u_trns_line_edit.connect(self.u_trns_line_edit,QtCore.SIGNAL('returnPressed()'),self.text_set_u_trns_slider)
        self.uv_trns_setup_layout.addWidget(self.u_trns_line_edit, 0,1,1,1)
        self.u_trns_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal) 
        self.u_trns_slider.setFixedWidth(200)
        self.u_trns_slider.setMinimum(0)
        self.u_trns_slider.setMaximum(200)
        self.u_trns_slider.setValue(0)        
        self.u_trns_slider.setTickInterval(2)
        self.u_trns_slider.setTickPosition(self.u_trns_slider.TicksBelow)
        self.u_trns_slider.valueChanged.connect(self.slider_set_u_trns_text)
        self.uv_trns_setup_layout.addWidget(self.u_trns_slider, 0,2,1,1)

        self.v_trns_button = QtWidgets.QPushButton('V translate')
        self.connect(self.v_trns_button, SIGNAL('clicked()'),
                    lambda: self.v_trns_force())
        self.uv_trns_setup_layout.addWidget(self.v_trns_button, 1,0,1,1)
        self.v_trns_line_edit = QtWidgets.QLineEdit('0.0')
        self.v_trns_line_edit.setFixedWidth(50)
        self.v_trns_line_edit.connect(self.v_trns_line_edit,QtCore.SIGNAL('returnPressed()'),self.text_set_v_trns_slider)
        self.uv_trns_setup_layout.addWidget(self.v_trns_line_edit, 1,1,1,1)
        self.v_trns_sider = QtWidgets.QSlider(QtCore.Qt.Horizontal) 
        self.v_trns_sider.setFixedWidth(200)
        self.v_trns_sider.setMinimum(0)
        self.v_trns_sider.setMaximum(200)
        self.v_trns_sider.setValue(0)        
        self.v_trns_sider.setTickInterval(2)
        self.v_trns_sider.setTickPosition(self.v_trns_sider.TicksBelow)
        self.v_trns_sider.valueChanged.connect(self.slider_set_v_trns_text)
        self.uv_trns_setup_layout.addWidget(self.v_trns_sider, 1,2,1,1)


        #end window for uv placement


        self.uv_app_butt_layout = QtWidgets.QGridLayout()
        self.uv_app_frame = QtWidgets.QFrame()
        self.uv_app_frame.setStyleSheet('color: #ffffff; background-color: rgba(120,120,120,50); border-style: solid; border-color:#434343;')
        self.uv_app_frame.setLayout(self.uv_app_butt_layout)

        self.uvtile_butt_row_layout = QtWidgets.QVBoxLayout()
        self.ss_order_layout_ta.addLayout(self.uvtile_butt_row_layout)
        self.uv_app_button = QtWidgets.QPushButton('Apply UV only')
        self.connect(self.uv_app_button, SIGNAL('clicked()'),
                    lambda: self.apply_uv_setting())
        self.uv_app_butt_layout.addWidget(self.uv_app_button) 
        self.uv_eye_drp_button = QtWidgets.QPushButton('Eyedrop UV')
        self.connect(self.uv_eye_drp_button, SIGNAL('clicked()'),
                    lambda: self.obtain_uv_Setting())
        self.uv_app_butt_layout.addWidget(self.uv_eye_drp_button) 

        self.uv_reset_button = QtWidgets.QPushButton('Reset sliders')
        self.connect(self.uv_reset_button, SIGNAL('clicked()'),
                    lambda: self.reset_uv_ui())
        self.uv_app_butt_layout.addWidget(self.uv_reset_button) 

        self.ss_order_layout_ta.addWidget(self.uv_app_frame)
            
            
        #UVMAP
        self.uv_map_layout = QtWidgets.QGridLayout()
        self.uv_map_frame = QtWidgets.QFrame()
        self.uv_map_frame.setStyleSheet('color: #ffffff; background-color: rgba(255,255,255,30); border-style: solid; border-color:#434343;')
        self.uv_map_frame.setLayout(self.uv_map_layout)

        self.uv_map_drpdwn_vbox_layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.uv_map_drpdwn_vbox_layout, 2,0,1,1)
        self.uv_map_drpdwn_vbox_layout.addWidget(self.uv_map_frame)

        self.uv_dial_combobox = QtWidgets.QComboBox()
        self.uv_dial_combobox.addItems(uv_select)
        self.uv_map_layout.addWidget(self.uv_dial_combobox)


        self.uv_map_button = QtWidgets.QPushButton('Apply UVmap')
        self.connect(self.uv_map_button, SIGNAL('clicked()'),
                    lambda: self.apply_uv_map(uv_load=self.uv_dial_combobox))
        self.uv_map_layout.addWidget(self.uv_map_button)   

        self.setLayout(self.layout)


    def help_page_launch(self):
        """
        opens the helppage for tool in confluence
        """
        url='https://atlas.bydeluxe.com/confluence/display/~deglaue/Set+Color+Tool'
        subprocess.Popen('gio open %s' % url, stdout=subprocess.PIPE, shell=True) 


    def v_tile_force(self):
        """
        forces the U tile slider to match the value on V tile slider
        """
        get_text_from_field = self.v_tile_line_edit.text()
        get_text_from_field = float(get_text_from_field)*10
        self.u_tile_slider.setValue(get_text_from_field)

    def u_tile_force(self):
        """
        forces the V tile slider to match the value on U tile slider
        """        
        get_text_from_field = self.u_tile_line_edit.text()
        get_text_from_field = float(get_text_from_field)*10
        self.v_tile_slider.setValue(get_text_from_field)
            
    def v_trns_force(self):
        """
        forces the V offset slider to match the value on U offset slider
        """              
        get_text_from_field = self.v_trns_line_edit.text()
        get_text_from_field = float(get_text_from_field)*10
        self.u_trns_slider.setValue(get_text_from_field)

    def u_trns_force(self):
        """
        forces the U offset slider to match the value on V offset slider
        """          
        get_text_from_field = self.u_trns_line_edit.text()
        get_text_from_field = float(get_text_from_field)*10
        self.v_trns_sider.setValue(get_text_from_field)
            

    def slider_set_u_tile_text(self):
        """
        This connects the U tile slider to the field
        """          
        get_size_from_slider = self.u_tile_slider.value()
        size_mult = get_size_from_slider*0.10
        self.u_tile_line_edit.setText(str(size_mult))

    def slider_set_rot_text(self):
        """
        This connects the rotation slider value to the field of the rotation
        """         
        get_size_from_slider = self.uv_rot_slider.value()
        self.uv_rot_line_edit.setText(str(get_size_from_slider))

    def text_set_rot_slider(self):
        """
        This updates the rotation slider value to the value in the field(in case of user input)
        """
        get_text_from_field = self.uv_rot_line_edit.text()
        get_text_from_field = int(get_text_from_field)
        self.uv_rot_slider.setValue(get_text_from_field)
            
    def slider_set_u_trns_text(self):
        """
        This updates the rotation slider value to the value in the field(in case of user input)
        """        
        get_size_from_slider = self.u_trns_slider.value()
        size_mult = get_size_from_slider*0.10
        self.u_trns_line_edit.setText(str(size_mult))

    def text_set_u_trns_slider(self):
        """
        sets the U translate slider to text number
        """         
        get_text_from_field = self.u_trns_line_edit.text()
        get_text_from_field = float(get_text_from_field)*10
        self.u_trns_slider.setValue(get_text_from_field)
            

    def slider_set_v_trns_text(self):
        """
        sets the V translate slider to text number
        """         
        get_size_from_slider = self.v_trns_sider.value()
        size_mult = get_size_from_slider*0.10
        self.v_trns_line_edit.setText(str(size_mult))

    def text_set_v_trns_slider(self):
        """
        sets the V translate text to the slider value
        """         
        get_text_from_field = self.v_trns_line_edit.text()
        get_text_from_field = float(get_text_from_field)*10
        self.v_trns_sider.setValue(get_text_from_field)

    def slider_set_v_tile_text(self):
        """
        sets the U tile slider to text number
        """          
        get_size_from_slider = self.v_tile_slider.value()
        size_mult = get_size_from_slider*0.10
        self.v_tile_line_edit.setText(str(size_mult))

    def text_set_u_tile_slider(self):
        """
        Sets the U tile slider to the text value
        """           
        get_text_from_field = self.u_tile_line_edit.text()
        get_text_from_field = float(get_text_from_field)*10
        self.u_tile_slider.setValue(get_text_from_field)
            
    def text_set_v_tile_slider(self):
        """
        Sets the V tile slider to the text value
        """         
        get_text_from_field = self.v_tile_line_edit.text()
        get_text_from_field = float(getvtText)*10
        self.v_tile_slider.setValue(get_text_from_field)

    def uv_collection(self):
        """
        Function to return all values currently set in the UV placement interface
        """          
        u_tile_value = float(self.u_tile_line_edit.text())
        v_tile_value = float(self.v_tile_line_edit.text())
        UV_rot = self.uv_rot_slider.value()
        UV_rotnum = int(UV_rot)
        u_trns_value = float(self.v_trns_line_edit.text())
        v_trns_value = float(self.v_trns_line_edit.text())
        return u_tile_value, v_tile_value, UV_rotnum, u_trns_value, v_trns_value


    def obtain_uv_Setting(self): 
        """This function will interrogate the current selected object shader for the UV settings and update interface with this"""
        try:
            get_sel_obj = mc.ls(sl=1, fl=1)[0]
            if len(get_sel_obj)>0:
                placement_node_p2dt = '{}_p2dt'.format(get_sel_obj)
                if mc.objExists(placement_node_p2dt) == True:
                    u_tile_value = mc.getAttr('{}.repeatU'.format(placement_node_p2dt))
                    self.u_tile_slider.setValue(u_tile_value*10)
                    v_tile_value = mc.getAttr('{}.repeatV'.format(placement_node_p2dt))
                    self.v_tile_slider.setValue(v_tile_value*10)
                    u_trns_value = mc.getAttr('{}.offsetU'.format(placement_node_p2dt))
                    self.u_trns_slider.setValue(u_trns_value*10)
                    v_trns_value = mc.getAttr('{}.offsetV'.format(placement_node_p2dt))
                    self.v_trns_sider.setValue(v_trns_value*10)
                    UV_rotnum = mc.getAttr('{}.rotateUV'.format(placement_node_p2dt))
                    self.uv_rot_slider.setValue(UV_rotnum)
                else:
                    print ' no object in scene called {}'.format(placement_node_p2dt)
        except:
            print 'nothing selected'
            return

    def reset_uv_ui(self):  
        """This resets the interface to default values so you dont have to reload or reset manually"""
        get_sel_obj = mc.ls(sl=1, fl=1)
        if len(get_sel_obj)>0:
            pass
        else:
            print 'nothing selected'
            return
        self.u_tile_slider.setValue(10)
        self.v_tile_slider.setValue(10)
        self.u_trns_slider.setValue(0)
        self.v_trns_sider.setValue(0.0)
        self.uv_rot_slider.setValue(0.0)
            
    def apply_uv_setting(self):
        """This applies the current UV slider values to the current selection in scene"""
        u_tile_value, v_tile_value, UV_rotnum, u_trns_value, v_trns_value =self.uv_collection()  
        get_sel_obj = mc.ls(sl=1, fl=1)
        if len(get_sel_obj)>0:
            pass
        else:
            print 'nothing selected'
            return
        for each_sel_obj in get_sel_obj:
            placement_node_p2dt = '{}_p2dt'.format(each_sel_obj)
            mc.setAttr('{}.repeatU'.format(placement_node_p2dt), u_tile_value)
            mc.setAttr('{}.repeatV'.format(placement_node_p2dt), v_tile_value)
            mc.setAttr('{}.offsetU'.format(placement_node_p2dt), u_trns_value)
            mc.setAttr('{}.offsetV'.format(placement_node_p2dt), v_trns_value)
            mc.setAttr('{}.rotateUV'.format(placement_node_p2dt), UV_rotnum)
            
            
    def apply_uv_map(self, uv_load):
        """This is the function that applies a uv map from the dropdown menu"""
        u_tile_value, v_tile_value, UV_rotnum, u_trns_value, v_trns_value =self.uv_collection()   
        imgfile_name=uv_load.currentText() 
        imgfile = maphome+imgfile_name
        get_sel_obj = mc.ls(sl=1, fl=1)
        if len(get_sel_obj)>0:
            pass
        else:
            print 'nothing selected'
            return
        for each_sel_obj in get_sel_obj:
            """First clear any remaining maps on current selected objects"""
            placement_node_p2dt = '{}_p2dt'.format(each_sel_obj)
            name_file_node = '{}_file'.format(each_sel_obj)
            name_chkr_node = '{}_ckr'.format(each_sel_obj)
            name_shdr_nde = '{}_shd'.format(each_sel_obj)
            name_SG_node = '{}_shdSG'.format(each_sel_obj)
            if len(mc.ls(name_shdr_nde))>0:
                    mc.delete(name_shdr_nde)
                    mc.delete(name_SG_node)
                    try:
                        mc.delete(placement_node_p2dt)
                    except:
                        pass
                    try:
                        mc.delete(name_file_node)
                    except:
                        pass
                    try:
                        mc.delete(name_chkr_node)
                    except:
                        pass
            """Now create fresh shaders and nodes for the map"""
            create_shade_node = mc.shadingNode('lambert', asShader=True, n=name_shdr_nde)
            mc.shadingNode('place2dTexture', asUtility=True, n=placement_node_p2dt)
            mc.shadingNode('file', asTexture = 1, isColorManaged = 1, n=name_file_node)
            lst_sg_node=[create_shade_node]
            """put it inside the texture set for easy finding later"""
            set_name='techanim_textures' 
            if mc.objExists(set_name):
                pass
            else:
                mc.sets(n=set_name, co=3)
            """now set and hook everything up"""
            mc.sets(lst_sg_node, add=set_name)
            mc.select(each_sel_obj)
            mc.hyperShade(assign=str(create_shade_node))           
            mc.connectAttr('{}.outUV'.format(placement_node_p2dt),'{}.uv'.format(name_file_node), force=1)            
            mc.connectAttr('{}.outUvFilterSize'.format(placement_node_p2dt), '{}.uvFilterSize'.format(name_file_node), force=1)    
            mc.connectAttr('{}.outColor'.format(name_file_node),  '{}_shd.color'.format(each_sel_obj), f=1)
            mc.setAttr('{}.fileTextureName'.format(name_file_node),  imgfile, type = 'string')
            mc.setAttr('{}.repeatU'.format(placement_node_p2dt), u_tile_value)
            mc.setAttr('{}.repeatV'.format(placement_node_p2dt), v_tile_value)
            mc.setAttr('{}.offsetU'.format(placement_node_p2dt), u_trns_value)
            mc.setAttr('{}.offsetV'.format(placement_node_p2dt), v_trns_value)
            mc.setAttr('{}.rotateUV'.format(placement_node_p2dt), UV_rotnum)              
        mc.select(get_sel_obj, r=1) 


    def apply_rgb(self):
        """This color sets for calling up the random shader function"""
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
        if color_name=='tech_geo':
            self.get_geo_techanim()     
        if color_name=='Contrast':
            self.enhanceContrastChecker()     
        if color_name=='Reverse contrast':
            self.reverseContrastChecker() 


    def shd_changer(self, type_color):
        """This is the function for applying random shaders for RGB values that applies to solids and checkered material"""
        u_tile_value, v_tile_value, UV_rotnum, u_trns_value, v_trns_value =self.uv_collection() 
        get_sel_obj = mc.ls(sl=1, fl=1)
        if len(get_sel_obj)>0:
            pass
        else:
            print 'nothing selected'
            return
        checkerChecked = self.checker_checked
        """This removes any pre-existing nodes from other materials and applies a clean checker material"""
        if checkerChecked.isChecked():
            for each_sel_obj in get_sel_obj:
                placement_node_p2dt = '{}_p2dt'.format(each_sel_obj)
                name_file_node = '{}_file'.format(each_sel_obj)
                name_chkr_node = '{}_ckr'.format(each_sel_obj)
                name_shdr_nde = '{}_shd'.format(each_sel_obj)
                name_SG_node = '{}_shdSG'.format(each_sel_obj)
                if len(mc.ls(name_shdr_nde))>0:
                    mc.delete(name_shdr_nde)
                    mc.delete(name_SG_node)
                    try:
                        mc.delete(placement_node_p2dt)
                    except:
                        pass
                    try:
                        mc.delete(name_file_node)
                    except:
                        pass
                    try:
                        mc.delete(name_chkr_node)
                    except:
                        pass
                create_shade_node = mc.shadingNode('lambert', asShader=True, n=name_shdr_nde)
                pdfirst = mc.shadingNode('place2dTexture', asUtility=True, n=placement_node_p2dt)
                mc.createNode( 'checker', n=name_chkr_node )
                lst_sg_node = [create_shade_node]
                set_name = 'techanim_textures' 
                if mc.objExists(set_name):
                    pass
                else:
                    mc.sets(n=set_name, co=3)
                mc.sets(lst_sg_node, add=set_name)
                mc.select(each_sel_obj)
                mc.hyperShade(assign=str(create_shade_node))
                mc.connectAttr( '{}.outColor'.format(name_chkr_node), '{}.color'.format(name_shdr_nde), force=1)            
                mc.connectAttr( '{}.outUV'.format(placement_node_p2dt),'{}.uv'.format(name_chkr_node), force=1)            
                mc.connectAttr( '{}.outUvFilterSize'.format(placement_node_p2dt),'{}.uvFilterSize'.format(name_chkr_node), force=1)
                self.randomize_double(each_sel_obj, type_color, placement_node_p2dt)
        else:            
            """This removes any pre-existing nodes from other materials and applies a clean solid material"""
            for each_sel_obj in get_sel_obj:
                placement_node_p2dt = '{}_p2dt'.format(each_sel_obj)
                name_file_node = '{}_file'.format(each_sel_obj)
                name_chkr_node = '{}_ckr'.format(each_sel_obj)
                name_shdr_nde = '{}_shd'.format(each_sel_obj)
                name_SG_node = '{}_shdSG'.format(each_sel_obj)                       
                if len(mc.ls(name_shdr_nde))>0:
                    mc.delete(name_shdr_nde)
                    mc.delete(name_SG_node)
                    try: 
                        mc.delete(placement_node_p2dt)
                    except:
                        pass
                    try:
                        mc.delete(name_file_node)
                    except:
                        pass
                    try:
                        mc.delete(name_chkr_node)
                    except:
                        pass
                # else:                
                create_shade_node = mc.shadingNode('lambert', asShader=True, n=name_shdr_nde)
                lst_sg_node = [create_shade_node]
                set_name = 'techanim_textures' 
                if mc.objExists(set_name):
                    pass
                else:
                    mc.sets(n=set_name, co=3)
                mc.sets(lst_sg_node, add=set_name)
                mc.select(each_sel_obj)
                mc.hyperShade(assign=str(create_shade_node))
                try:
                    set1, set2, set3  = self.gamble_dice(type_color) 
                    mc.setAttr('{}.color'.format(name_shdr_nde), set1, set2, set3, type='double3')
                except:
                    self.randomize_double(each_sel_obj, type_color, placement_node_p2dt)                 
        mc.select(get_sel_obj, r=1)   

    def randomize_double(self, shader_obj, type_color, placement_node_p2dt):
        """This is the function for applying a checker and the current uv settings for the placement node"""
        shd_name = shader_obj
        u_tile_value, v_tile_value, UV_rotnum, u_trns_value, v_trns_value =self.uv_collection()
        set1, set2, set3  = self.gamble_dice(type_color) 
        mc.setAttr('{}_ckr.color1'.format(shader_obj), set1, set2, set3, type='double3')
        set1, set2, set3  = self.gamble_dice(type_color) 
        mc.setAttr('{}_ckr.color2'.format(shader_obj), set1, set2, set3, type='double3') 
        mc.setAttr('{}_p2dt.repeatU'.format(shader_obj), u_tile_value)
        mc.setAttr('{}_p2dt.repeatV'.format(shader_obj), v_tile_value)   
        mc.setAttr('{}_p2dt.offsetU'.format(shader_obj), u_trns_value)
        mc.setAttr('{}_p2dt.offsetV'.format(shader_obj), v_trns_value)
        mc.setAttr('{}_p2dt.rotateUV'.format(shader_obj), UV_rotnum) 


    def _change_primary_grn(self):
        self.shd_changer('green')

    def _change_primary_red(self):
        self.shd_changer('red')

    def _change_primary_blue(self):
        self.shd_changer('blue')

    def _apply_colors(self):
        self.shd_changer('random')

    def _change_primary_teal(self):
        self.shd_changer('teal')

    def _change_primary_orange(self):
        self.shd_changer('orange')

    def _change_primary_prpl(self):
        self.shd_changer('purple')

    def _apply_grey_colors(self):
        self.shd_changer('grey')

    def _change_primary_gry(self):
        self.shd_changer('grey')

    def _change_colors(self):
        self.shd_changer('random')


    def gamble_dice(self, type_color):
        get_clr_value = random.uniform(0.0,1.0)
        get_dice_value = random.uniform(0.0,0.25)   
        if type_color == 'green':
            set1 = get_dice_value  
            set2 = get_clr_value                        
            set3 = get_dice_value  
        if type_color == 'red':
            set1 = get_clr_value  
            set2 = get_dice_value                        
            set3 = get_dice_value     
        if type_color == 'blue':
            set1 = get_dice_value  
            set2 = get_dice_value                        
            set3 = get_clr_value   
        if type_color == 'teal':
            set1 = get_dice_value  
            set2 = get_clr_value
            set3 = get_clr_value         
        if type_color == 'orange':
            set1 = get_clr_value  
            set2 = get_clr_value                        
            set3 = get_dice_value  
        if type_color == 'purple':
            set1 = get_clr_value  
            set2 = get_dice_value                        
            set3 = get_clr_value    
        if type_color == 'grey':
            set1 = get_clr_value  
            set2 = get_clr_value                        
            set3 = get_clr_value   
        if type_color == 'random':
            set1 = random.uniform(0.0,1.0)  
            set2 = random.uniform(0.0,1.0)                        
            set3 = random.uniform(0.0,1.0)           
        return set1, set2, set3    

    def get_geo_techanim(self):
        """This will apply the color swatches to a pre existing tech rig"""
        get_tech = mc.ls('*:*_tech_geo')
        get_tech_two = mc.ls('*_tech_geo')
        get_posttech = mc.ls('*:*_postTech_geo')
        get_posttech_two = mc.ls('*_postTech_geo')
        get_geo = get_tech + get_tech_two + get_posttech + get_posttech_two
        mc.select(get_geo, r=1)
        self._apply_colors()

    def _slight_to_gry(self):
        self.shader_slighter('sl_grey')

    def _change_darker(self):
        self.shader_slighter('dark')

    def _change_lighter(self):
        self.shader_slighter('light')


    def shader_slighter(self, type_color):
        get_sel_obj = mc.ls(sl=1)
        if len(get_sel_obj)>0:
            pass
        else:
            print 'nothing selected'
            return
        mc.hyperShade (get_sel_obj[0], smn=1)
        checkerChecked = self.checker_checked
        if checkerChecked.isChecked():
            for each_sel_shdr in mc.ls(sl=1):
                self.slight_single_or_double(each_sel_shdr, type_color)                                    
        else:                        
            for each_sel_shdr in mc.ls(sl=1):
                try:
                    set1, set2, set3  = self.gamble_slight( type_color, each_sel_shdr) 
                    mc.setAttr('{}.color'.format(each_sel_shdr), set1, set2, set3, type='double3')
                except:
                    self.slight_single_or_double(each_sel_shdr, type_color)                
        mc.select(get_sel_obj, r=1)

    def slight_single_or_double(self, shader_obj,  type_color):
         shd_name = shader_obj.split('_shd')[0]
        single = '{}.color'.format(shader_obj)
        double = '{}_ckr.color1'.format(shd_name)
        u_tile_value, v_tile_value, UV_rotnum, u_trns_value, v_trns_value =self.uv_collection()
        if mc.objExists(single) == True:
            get_clr_value = mc.getAttr('{}.color'.format(shader_obj))
            set1, set2, set3  = self.gamble_slight( type_color, get_clr_value)
            try:
                mc.setAttr('{}.color'.format(shader_obj), set1, set2, set3, type='double3')
            except:
                get_clr_value = mc.getAttr('{}_ckr.color1'.format(shd_name))
                set1, set2, set3  = self.gamble_slight( type_color, get_clr_value)                  
                mc.setAttr('{}_ckr.color1'.format(shd_name), set1, set2, set3, type='double3')
                get_clr_value = mc.getAttr('{}_ckr.color2'.format(shd_name))
                set1, set2, set3  = self.gamble_slight( type_color, get_clr_value)                  
                mc.setAttr('{}_ckr.color2'.format(shd_name), set1, set2, set3, type='double3')
        elif mcobjExists(double) == True:
            get_clr_value = mc.getAttr('{}_ckr.color1'.format(shd_name))
            set1, set2, set3  = self.gamble_slight( type_color, get_clr_value)                  
            mc.setAttr('{}_ckr.color1'.format(shd_name), set1, set2, set3, type='double3')
            get_clr_value = mc.getAttr('{}_ckr.color2'.format(shd_name))
            set1, set2, set3  = self.gamble_slight( type_color, get_clr_value)                  
            mc.setAttr('{}_ckr.color2'.format(shd_name), set1, set2, set3, type='double3')  
            mc.setAttr('{}_p2dt.repeatU'.format(shd_name), u_tile_value)
            mc.setAttr('{}_p2dt.repeatV'.format(shd_name), v_tile_value)   
            mc.setAttr('{}_p2dt.offsetU'.format(shd_name), u_trns_value)
            mc.setAttr('{}_p2dt.offsetV'.format(shd_name), v_trns_value)
            mc.setAttr('{}_p2dt.rotateUV'.format(shd_name), UV_rotnum)
        else:
            print 'action not applicable'
            
    def gamble_slight(self, type_color, get_clr_value):
        if type_color == 'sl_grey':
            get_dice_value = random.uniform(get_clr_value[0][0],get_clr_value[0][2])  
            set1 = get_dice_value  
            set2 = get_dice_value
            set3 = get_dice_value 
        if type_color == 'dark':
            get_dice_value = random.uniform(0.0,0.25)
            newval = get_clr_value[0][0]-get_dice_value, get_clr_value[0][1]-get_dice_value, get_clr_value[0][2]-get_dice_value 
            set1 = newval[0] 
            set2 = newval[1]               
            set3 = newval[2]
        if type_color =='light':
            get_dice_value = random.uniform(0.0,0.25)
            newval = get_clr_value[0][0]+get_dice_value, get_clr_value[0][1]+get_dice_value, get_clr_value[0][2]+get_dice_value
            set1 = newval[0] 
            set2 = newval[1]               
            set3 = newval[2] 
        return set1, set2, set3 
            
    def checker_contrast_gamble(self, contrast_type, get_shad_val_1, get_shad_val_2):
        if contrast_type == 'enhance':
            #contrast - subtract from first color. add to second.
            dice_value = random.uniform(0.0,0.25)
            get_first = get_shad_val_1[0][0]-dice_value, get_shad_val_1[0][1]-dice_value, get_shad_val_1[0][2]-dice_value           
            dice_value = random.uniform(0.0,0.25)
            get_second = get_shad_val_2[0][0]+dice_value, get_shad_val_2[0][1]+dice_value, get_shad_val_2[0][2]+dice_value
        elif contrast_type == 'reverse':
            #reverse - add to first color, subtract from second
            dice_value = random.uniform(0.0,0.25)
            get_first = get_shad_val_1[0][0]+dice_value, get_shad_val_1[0][1]+dice_value, get_shad_val_1[0][2]+dice_value        
            dice_value = random.uniform(0.0,0.25)
            get_second = get_shad_val_2[0][0]-dice_value, get_shad_val_2[0][1]-dice_value, get_shad_val_2[0][2]-dice_value 
        return get_first, get_second


    def contrast_function(self, contrast_type):
        u_tile_value, v_tile_value, UV_rotnum, u_trns_value, v_trns_value =self.uv_collection()
        get_sel_obj = mc.ls(sl=1)
        mc.hyperShade (get_sel_obj[0], smn=1)
        if len(get_sel_obj)<1:
            print 'nothing selected'
            return
        else:
            for each_sel_obj in mc.ls(sl=1):
                print each_sel_obj
                try:
                    get_shad_val_1 = mc.getAttr('{}_ckr.color1'.format(each_sel_obj.split('_shd')[0]))
                    get_shad_val_2 = mc.getAttr('{}_ckr.color2'.format(each_sel_obj.split('_shd')[0]))
                    get_first_value, get_second_value = self.checker_contrast_gamble(contrast_type, get_shad_val_1, get_shad_val_2)
                    mc.setAttr('{}_ckr.color1'.format(each_sel_obj.split('_shd')[0]),get_first_value[0], get_first_value[1], get_first_value[2],type='double3')          
                    mc.setAttr('{}_ckr.color2'.format(each_sel_obj.split('_shd')[0]),get_second_value[0], get_second_value[1], get_second_value[2],type='double3')            
                except:
                    print 'only affects checkered textures'               
                    pass           
            mc.select(get_sel_obj, r=1)       
            

    def enhanceContrastChecker(self):
        self.contrast_function('enhance')


    def reverseContrastChecker(self):
        self.contrast_function('reverse')

 
    def ambientRandomizer(self):
        get_sel_obj = mc.ls(sl=1)
        if len(get_sel_obj)>0:
            pass
        else:
            print 'nothing selected'
            return
        mc.hyperShade (get_sel_obj[0], smn=1)
        for each_sel_shdr in mc.ls(sl = 1):
            get_float = random.uniform(0.0,1.0)
            mc.setAttr('{}.incandescence'.format, get_float, get_float, get_float, type='double3')
        mc.select(get_sel_obj, r=1)  


    def saveGamut(self, arg=None):
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
        print fileName
        get_sel_obj=mc.ls(sl=1, fl=1)   
        if len(get_sel_obj)>0:
            pass
        else:
            print 'nothing selected'
            return
        newfileName='{}_color.txt'.format(fileName)
        if '/color_gamut/_color.txt' in newfileName:
            print "add a name for this gamut"
            return
        else:
            pass
        folderPath='\\'.join(newfileName.split("/")[:-1])+"//"
        newfolderPath=re.sub(r'\\',r'/', folderPath)
        print folderPath
        if not os.path.exists(newfolderPath): 
            os.makedirs(newfolderPath)    
            print "created {}".format(newfolderPath)     
        # if not os.path.exists(folderPath): os.makedirs(folderPath)
        inp=open(newfileName, 'w+')        
        # inp=open(fileName, 'w+')
        # inp.write(str('colorDictionary = {'))
        mc.hyperShade (get_sel_obj[0], smn=1)
        for each_sel_shdr in mc.ls(sl = 1):
            get_item_name = each_sel_shdr.split('_shd')[0]
            if mc.objExists('{}_ckr'.format(get_item_name)) == True:
                chkcl1 = mc.getAttr('{}_ckr.color1'.format(get_item_name))
                chkcl2 = mc.getAttr('{}_ckr.color2'.format(get_item_name))
                u_tile_value = mc.getAttr('{}_p2dt.repeatU'.format(get_item_name))
                v_tile_value = mc.getAttr('{}_p2dt.repeatV'.format(get_item_name))
                u_trns_value = mc.getAttr('{}_p2dt.offsetU'.format(get_item_name))
                v_trns_value = mc.getAttr('{}_p2dt.offsetV'.format(get_item_name))
                UV_rotnum = mc.getAttr('{}_p2dt.rotateUV'.format(get_item_name))
                name_chkr_node = '{}_ckr'.format(get_item_name)
                obj_string_line = '{}|{}<{}<{}>{}>{}>{}>{} , '.format(name_chkr_node, chkcl1, chkcl2, u_tile_value, v_tile_value, u_trns_value, v_trns_value, UV_rotnum)
                inp.write(obj_string_line)
            elif mc.objExists('{}_file'.format(get_item_name)) == True: 
                print 'file'
                name_file_node = '{}_file'.format(get_item_name)
                get_item_name = each_sel_shdr.split('_shd')[0]
                uv_collectionimage = mc.getAttr('{}.fileTextureName'.format(name_file_node))
                u_tile_value = mc.getAttr('{}_p2dt.repeatU'.format(get_item_name))
                v_tile_value = mc.getAttr('{}_p2dt.repeatV'.format(get_item_name))
                u_trns_value = mc.getAttr('{}_p2dt.offsetU'.format(get_item_name))
                v_trns_value = mc.getAttr('{}_p2dt.offsetV'.format(get_item_name))
                UV_rotnum = mc.getAttr('{}_p2dt.rotateUV'.format(get_item_name))
                obj_string_line = '{}|{}<{}>{}>{}>{}>{} , '.format(name_file_node, uv_collectionimage, u_tile_value, v_tile_value, u_trns_value, v_trns_value, UV_rotnum)
                inp.write(obj_string_line)
            else:
                try:
                    get_val = mc.getAttr('{}.color'.format(each_sel_shdr))
                    obj_string_line = '{}|{} , '.format(each_sel_shdr, get_val)
                    # obj_string_line = '{}:{} , '.format(each_sel_shdr, get_val)
                    inp.write(obj_string_line)  
                except:
                    print '{} does not have a shader group assigned in scene. Skipping'.format(each_sel_shdr)          
        inp.close()   
        print 'saved as {}'.format(newfileName)
            
            
    def loadSelect(self, printFolder): 
        print printFolder
        if os.path.exists(printFolder):
            pass
        else:
            print '{} does not exist'.format(printFolder)
            return
        List = open(printFolder).readlines()
        create_dict = {}
        for aline in List:
            a_list = list(aline)
            a_list = aline.split(' , ')
        if len(a_list) > 0:
            for each in a_list:
                listp1 = each.split('|')
                print listp1[0]
                if len(listp1)>1:
                    if '_ckr' in listp1[0]:
                        name_chkr_node = listp1[0]                 
                        shdr_name = '{}_shd'.format(listp1[0].split('_ckr')[0])
                        scnobject = listp1[0].split('_ckr')[0]
                        placement_node_p2dt = '{}_p2dt'.format(listp1[0].split('_ckr')[0])
                        name_file_node = '{}_file'.format(listp1[0].split('_ckr')[0])
                        if mc.objExists(name_file_node) == True:
                            mc.delete(name_file_node) 
                        if mc.objExists(shdr_name) == False: 
                            create_shade_node = mc.shadingNode('lambert', asShader=True, n=shdr_name)
                            mc.hyperShade(assign=str(create_shade_node))
                            lst_sg_node=[create_shade_node]
                            set_name='techanim_textures' 
                            if mc.objExists(set_name):
                                pass
                            else:
                                mc.sets(n=set_name, co=3)
                            mc.sets(lst_sg_node, add=set_name)
                            mc.select(scnobject)
                            mc.hyperShade(assign=str(create_shade_node))
                        if mc.objExists(placement_node_p2dt) == False:    
                            mc.shadingNode('place2dTexture', asUtility=True, n=placement_node_p2dt)
                        if mc.objExists(name_chkr_node) == False: 
                            mc.createNode( 'checker', n=name_chkr_node )
                        mc.connectAttr( '{}.outColor'.format(name_chkr_node), '{}.color'.format(shdr_name), force=1)            
                        mc.connectAttr( '{}.outUV'.format(placement_node_p2dt),'{}.uv'.format(name_chkr_node), force=1)            
                        mc.connectAttr( '{}.outUvFilterSize'.format(placement_node_p2dt),'{}.uvFilterSize'.format(name_chkr_node), force=1)
                        col_get = listp1[-1].split('<')
                        clrs1 = ast.literal_eval(col_get[0])
                        clrs2 = ast.literal_eval(col_get[1])
                        mc.setAttr('{}.color1'.format(name_chkr_node), clrs1[0][0],clrs1[0][1], clrs1[0][2], type='double3')
                        mc.setAttr('{}.color2'.format(name_chkr_node), clrs2[0][0],clrs2[0][1], clrs2[0][2], type='double3')
                        plc_get = col_get[-1].split('>')
                        mc.setAttr('{}.repeatU'.format(placement_node_p2dt), float(plc_get[0]))
                        mc.setAttr('{}.repeatV'.format(placement_node_p2dt), float(plc_get[1]))
                        mc.setAttr('{}.offsetU'.format(placement_node_p2dt), float(plc_get[2]))
                        mc.setAttr('{}.offsetV'.format(placement_node_p2dt), float(plc_get[3]))
                        mc.setAttr('{}.rotateUV'.format(placement_node_p2dt), float(plc_get[4]))
                    elif '_file' in listp1[0]:
                        name_file_node = listp1[0]
                        shdr_name = '{}_shd'.format(listp1[0].split('_file')[0])
                        scnobject = listp1[0].split('_file')[0]
                        placement_node_p2dt = '{}_p2dt'.format(listp1[0].split('_file')[0])
                        name_chkr_node = '{}_ckr'.format(listp1[0].split('_file')[0])
                        if mc.objExists(name_chkr_node) == True:
                            mc.delete(name_chkr_node) 
                        if mc.objExists(shdr_name) == False: 
                            create_shade_node = mc.shadingNode('lambert', asShader=True, n=shdr_name)
                            mc.hyperShade(assign=str(create_shade_node))
                            lst_sg_node=[create_shade_node]
                            set_name = 'techanim_textures' 
                            if mc.objExists(set_name):
                                pass
                            else:
                                mc.sets(n=set_name, co=3)
                            mc.sets(lst_sg_node, add=set_name)
                            mc.select(scnobject)
                            mc.hyperShade(assign=str(create_shade_node))          
                        if mc.objExists(placement_node_p2dt) == False:    
                            mc.shadingNode('place2dTexture', asUtility=True, n=placement_node_p2dt)
                        if mc.objExists( listp1[0]) == False: 
                            filefirst = mc.shadingNode('file', asTexture = 1, isColorManaged = 1, n=name_file_node)   
                        mc.connectAttr( '{}.outUV'.format(placement_node_p2dt),'{}.uv'.format(name_file_node), force=1)            
                        mc.connectAttr( '{}.outUvFilterSize'.format(placement_node_p2dt), '{}.uvFilterSize'.format(name_file_node), force=1)    
                        mc.connectAttr('{}.outColor'.format(name_file_node),  '{}.color'.format(shdr_name), f=1)
                        filegrb=listp1[-1].split('<')
                        mc.setAttr('{}.fileTextureName'.format(name_file_node),  filegrb[0], type = 'string')
                        plc_get=filegrb[-1].split('>')
                        mc.setAttr('{}.repeatU'.format(placement_node_p2dt), float(plc_get[0]))
                        mc.setAttr('{}.repeatV'.format(placement_node_p2dt), float(plc_get[1]))
                        mc.setAttr('{}.offsetU'.format(placement_node_p2dt), float(plc_get[2]))
                        mc.setAttr('{}.offsetV'.format(placement_node_p2dt), float(plc_get[3]))
                        mc.setAttr('{}.rotateUV'.format(placement_node_p2dt), float(plc_get[4]))
                    else:
                        scnobject = listp1[0].split('_shd')[0]
                        if mc.objExists(scnobject) == True:
                            name_chkr_node = '{}_ckr'.format(listp1[0].split('_shd')[0])
                            placement_node_p2dt = '{}_p2dt'.format(listp1[0].split('_shd')[0])
                            name_file_node = '{}_file'.format(listp1[0].split('_shd')[0])
                            if mc.objExists(name_chkr_node) == True:
                                mc.delete(name_chkr_node) 
                            if mc.objExists(name_file_node) == True:
                                mc.delete(name_file_node)     
                            if mc.objExists(placement_node_p2dt) == True:
                                mc.delete(placement_node_p2dt)                                       
                            s = eval(str(listp1[1]))
                            mc.setAttr('{}.color'.format(listp1[0]), s[0][0],s[0][1], s[0][2], type='double3')
                        else:
                            print '{} does not exist in scene. Skipping'.format(scnobject) 


inst_mkwin=set_colors_win()
inst_mkwin.show()                        
                        
                                          
