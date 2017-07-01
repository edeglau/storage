class clothCheck_UI(QtGui.QWidget):
	def __init__(self):
		super(clothCheck_UI, self).__init__()
		self.initUI()

	def initUI(self):
		self.setWindowTitle("Check cloth scene health")
		self.checklayout = QVBoxLayout()
		self.checkLayout = QBoxLayout(2)
		self.playlist_names = QComboBox()
		self.checklayout.addLayout(self.checkLayout)
		self.check_all = QPushButton("check all")
		self.connect(self.check_all, SIGNAL("clicked()"),lambda: self._check_all())
		self.checkLayout.addWidget(self.check_all)
		self.check_none = QPushButton("check none")
		self.connect(self.check_none, SIGNAL("clicked()"),lambda: self._check_none())
		self.checkLayout.addWidget(self.check_none)
		self.checkRange = QCheckBox("Framerange")
		self.checkRange.setCheckState(0)
		self.checkLayout.addWidget(self.checkRange)
		self.nuc_category = QLabel("Nucleus")
		self.nuc_enable = QCheckBox("nuc enabled")
		self.nuc_enable.setCheckState(1)
		self.checkLayout.addWidget(self.nuc_enable)
		self.checkLayout.addWidget(self.nuc_category)
		self.nuc_strt = QCheckBox("Nucleus startframe")
		self.nuc_strt.setCheckState(1)
		self.checkLayout.addWidget(self.nuc_strt)
		self.space_scale = QCheckBox("space scale")
		self.space_scale.setCheckState(1)
		self.checkLayout.addWidget(self.space_scale)
		self.nuc_subs = QCheckBox("substeps")
		self.nuc_subs.setCheckState(1)
		self.checkLayout.addWidget(self.nuc_subs)
		self.coll_iter = QCheckBox("collision iterations")
		self.coll_iter.setCheckState(1)
		self.checkLayout.addWidget(self.coll_iter)
		self.rgd_category = QLabel("Rigids")
		self.checkLayout.addWidget(self.rgd_category)
		self.rgd_pnt_mass = QCheckBox("rgd point mass")
		self.rgd_pnt_mass.setCheckState(1)
		self.checkLayout.addWidget(self.rgd_pnt_mass)
		self.clth_category = QLabel("Cloth")
		self.checkLayout.addWidget(self.clth_category)
		self.scale_rel = QCheckBox("scale relations")
		self.scale_rel.setCheckState(1)
		self.checkLayout.addWidget(self.scale_rel)
		self.trap_check = QCheckBox("trapped check")
		self.trap_check.setCheckState(1)
		self.checkLayout.addWidget(self.trap_check)
		self.clth_enable = QCheckBox("enabled")
		self.clth_enable.setCheckState(1)
		self.checkLayout.addWidget(self.clth_enable)
		self.dyn_cnstrnt_category = QLabel("Dynamic Constraints")
		self.checkLayout.addWidget(self.dyn_cnstrnt_category)
		self.dyncnstrnt_exc = QCheckBox("dconstrnt exclusions")
		self.dyncnstrnt_exc.setCheckState(1)
		self.checkLayout.addWidget(self.dyncnstrnt_exc)
		self.dry_button = QPushButton("dry run")
		self.connect(self.dry_button, SIGNAL("clicked()"),lambda: self.dry_run())
		self.checkLayout.addWidget(self.dry_button)
		self.doit_button = QPushButton("check cloth scene")
		self.connect(self.doit_button, SIGNAL("clicked()"),lambda: self.checkit())
		self.checkLayout.addWidget(self.doit_button)
		self.close_button = QPushButton("close")
		self.connect(self.close_button, SIGNAL("clicked()"),lambda: self.gotoAppend())
		# self.checkLayout.addWidget(self.label)
		self.checkLayout.addWidget(self.close_button)
		self.setLayout(self.checklayout)

	def gotoAppend(self):
		self.close()

	def dry_run(self):
		get_baseTools=mockTools.mToolKit() 
		get_baseTools.troubleshoot_clth()

	def checkit(self):
		check_dict={}
		getrange={"range":self.checkRange.checkState()}
		check_dict.update(getrange)
		getnucstart={"nucstart":self.nuc_strt.checkState()}
		check_dict.update(getnucstart)
		getnucenable={"nucenable":self.nuc_enable.checkState()}
		check_dict.update(getnucenable)
		getspcscl={"nuc_spc_scl":self.space_scale.checkState()}
		check_dict.update(getspcscl)
		getnucsubstp={"nuc_sub_stp":self.nuc_subs.checkState()}
		check_dict.update(getnucsubstp)
		getnuccoliter={"nuc_col_itr":self.coll_iter.checkState()}
		check_dict.update(getnuccoliter)
		getrdgmss={"rgd_mass":self.rgd_pnt_mass.checkState()}
		check_dict.update(getrdgmss)
		getsclerel={"scl_rel":self.scale_rel.checkState()}
		check_dict.update(getsclerel)
		getdyncnstrntexcl={"dyn_cnstrnt_exc":self.dyncnstrnt_exc.checkState()}
		check_dict.update(getdyncnstrntexcl)
		getclthenble={"clthenable":self.clth_enable.checkState()}
		check_dict.update(getclthenble)
		getclthtrpchk={"clth_trp_chk":self.trap_check.checkState()}
		check_dict.update(getclthtrpchk)
		get_baseTools=mockTools.mToolKit() 
		get_baseTools.set_troubleshoot(check_dict)

	def _check_all(self):
		self.checkRange.setCheckState(1)
		self.nuc_strt.setCheckState(1)
		self.clth_enable.setCheckState(1)
		self.nuc_enable.setCheckState(1)
		self.space_scale.setCheckState(1)
		self.nuc_subs.setCheckState(1)
		self.coll_iter.setCheckState(1)
		self.rgd_pnt_mass.setCheckState(1)
		self.scale_rel.setCheckState(1)
		self.dyncnstrnt_exc.setCheckState(1)
		self.clth_enable.setCheckState(1)

	def _check_none(self):
		self.checkRange.setCheckState(0)
		self.nuc_strt.setCheckState(0)
		self.clth_enable.setCheckState(0)
		self.nuc_enable.setCheckState(0)
		self.space_scale.setCheckState(0)
		self.nuc_subs.setCheckState(0)
		self.coll_iter.setCheckState(0)
		self.rgd_pnt_mass.setCheckState(0)
		self.scale_rel.setCheckState(0)
		self.dyncnstrnt_exc.setCheckState(0)
		self.trap_check.setCheckState(0)
    
   def set_troubleshoot(self, check_dict):
        if check_dict.get("range") == 1:        
            getNumStrt=cmds.playbackOptions(q=1, ast=1)
            getNumMn=cmds.playbackOptions(q=1, min=1)
            getNumMx=cmds.playbackOptions(q=1, max=1)
            getNumEnd=cmds.playbackOptions(q=1, aet=1)
            if getNumStrt <> wk_strt_value - 15:
                print "CHANGING>>>> "+str(getNumStrt)+" to "+str(wk_strt_value - 15)
                self.initialize_strt_based_on_wkrange()
            elif getNumMn <> wk_strt_value - 15:
                print "CHANGING>>>> "+str(getNumMn)+" to "+str(wk_strt_value - 15)
                self.initialize_strt_based_on_wkrange()        
            else:
                pass       
            if getNumEnd <> wk_out_value:
                print "CHANGING>>>> "+str(getNumEnd)+" to "+str(wk_out_value)
                cmds.playbackOptions(aet=wk_out_value)  
            elif getNumMx <> wk_out_value:
                print "CHANGING>>>> "+str(getNumMx)+" to "+str(wk_out_value)
                cmds.playbackOptions(max=wk_out_value)
            else:
                pass 
        else:
            print "Skipping range check"
        if check_dict.get("dyn_cnstrnt_exc") == 1: 
            for each in cmds.ls(type="dynamicConstraint"):
                print each, cmds.getAttr(each+".excludeCollisions")
                if cmds.getAttr(each+".excludeCollisions") != 1:        
                    cmds.setAttr(each+".excludeCollisions", 1)
                    print "CHANGED>>>> "+each, cmds.getAttr(each+".excludeCollisions")
                else:
                    print each+"excludeCollisions is already on - leaving as is"      
        else:
            print "Skipping dynamic constraint collide exclusion check"                          
        for each in cmds.ls(type="nucleus"):
            if check_dict.get("nuc_spc_scl") == 1:     
                print each+".spaceScale", cmds.getAttr(each+".spaceScale")
                if cmds.getAttr(each+".spaceScale") ==1.0:
                    cmds.setAttr(each+".spaceScale", 0.1)
                    print "CHANGED>>>> "+each+".spaceScale", cmds.getAttr(each+".spaceScale")
                else:
                    print "spaceScale check is healthy - leaving as is"
            else:
                print "Skipping space scale check"     
            if check_dict.get("nuc_sub_stp") == 1:                          
                print each+".subSteps", cmds.getAttr(each+".subSteps")
                if cmds.getAttr(each+".subSteps") >3:
                    print "subSteps check is healthy - leaving as is"
                else:
                    cmds.setAttr(each+".subSteps", 30)
                    print "CHANGED>>>> "+each+".subSteps", cmds.getAttr(each+".subSteps")        
            else:
                print "Skipping substep check"
            if check_dict.get("nuc_col_itr") == 1:       
                print each+".maxCollisionIterations", cmds.getAttr(each+".maxCollisionIterations")
                if cmds.getAttr(each+".maxCollisionIterations") >4:
                    print "maxCollisionIterations check is healthy - leaving as is"
                else:
                    cmds.setAttr(each+".maxCollisionIterations", 20)
                    print "CHANGED>>>> "+each+".maxCollisionIterations", cmds.getAttr(each+".maxCollisionIterations")
            else:
                print "Skipping max collision iteration check"     
            if check_dict.get("nucstart") == 1:     
                print each+".startFrame", cmds.getAttr(each+".startFrame")
                print str(int(wk_strt_value) - 15)
                if cmds.getAttr(each+".startFrame") != wk_strt_value - 15:
                    cmds.setAttr(each+".startFrame", int(wk_strt_value - 15))
                    print "CHANGED>>>> "+each+".startFrame", cmds.getAttr(each+".startFrame")
                else:
                    print "startFrame check is healthy - leaving as is"
            else:
                print "Skipping nucleus start frame check"
            if check_dict.get("nucenable") == 1: 
                print each+".enable", cmds.getAttr(each+".enable")
                if cmds.getAttr(each+".enable")!=1:
                    cmds.setAttr(each+".enable", 1)
                    print "CHANGED>>>> "+each+".enable", cmds.getAttr(each+".enable")           
                else:
                    print "enabled check is good - leaving as is"
            else:
                print "Skipping enabled nucleus check"
        for each in cmds.ls(type="nRigid"):
            if check_dict.get("rgd_mass") == 1: 
                print each+".pointMass", cmds.getAttr(each+".pointMass")
                if cmds.getAttr(each+".pointMass")<20:
                    cmds.setAttr(each+".pointMass", 20)
                    print "CHANGED>>>> "+each+".pointMass", cmds.getAttr(each+".pointMass")                    
                else:
                    print "pointMass check is good - leaving as is"
            else:
                print "Skipping rigid point mass check"
        for each in cmds.ls(type="nCloth"):
            if check_dict.get("scl_rel") == 1: 
                print each+".scalingRelation", cmds.getAttr(each+".scalingRelation")
                if cmds.getAttr(each+".scalingRelation")==2:
                    cmds.setAttr(each+".scalingRelation", 1)
                    print "CHANGED>>>> "+each+".scalingRelation", cmds.getAttr(each+".scalingRelation")                  
                else:
                    print "scalingRelation check is good but check resolution. hires is good on 'object(1)' where as lores may be better on 'link(0)'"
            else:
                print "Skipping scale relation check"
            if check_dict.get("clth_trp_chk") == 1: 
                print each+".trappedCheck", cmds.getAttr(each+".trappedCheck")
                if each+".trappedCheck"==1:
                    cmds.setAttr(each+".trappedCheck", 0)
                    print "CHANGED>>>> "+each+".trappedCheck", cmds.getAttr(each+".trappedCheck")                        
                else:
                    print "trappedCheck check is good"
            else:
                print "Skipping cloth trap check"
            if check_dict.get("clthenable") == 1: 
                print each+".isDynamic", cmds.getAttr(each+".isDynamic")
                if each+".isDynamic"==1:
                    cmds.setAttr(each+".isDynamic", 0)
                    print "CHANGED>>>> "+each+".isDynamic", cmds.getAttr(each+".isDynamic")                        
                else:
                    print "isDynamic check is good"
            else:
                print "Skipping cloth enabled check"

    def troubleshoot_clth(self):
        getNumStrt=cmds.playbackOptions(q=1, ast=1)
        getNumEnd=cmds.playbackOptions(q=1, aet=1)
        if getNumStrt == wk_strt_value:
            print "maybe you want some preroll?"  
        else:
            pass        
        if getNumEnd == wk_out_value:
            "Maybe you want to set the frame end to the work end range?"  
        else:
            pass               
        for each in cmds.ls("*:*.excludeCollisions"):
            if each != 1:
                print "maybe you want "+each+" on?"     
            else:
                print "exclusions passed"  
        for each in cmds.ls(type="nucleus"):
            print each, cmds.getAttr(each+".spaceScale")
            if cmds.getAttr(each+".spaceScale") ==1.0:
                print "maybe you want "+each+" spaceScale lower?" 
            else:
                print "spaceScale check is healthy"
            print each, cmds.getAttr(each+".subSteps")
            if cmds.getAttr(each+".subSteps") >3:
                print "subSteps check is healthy"
            else:
                print "maybe you want "+each+" subSteps higher?"                 
            print each, cmds.getAttr(each+".maxCollisionIterations")
            if cmds.getAttr(each+".maxCollisionIterations") >4:
                print "maxCollisionIterations check is healthy"
            else:
                print "maybe you want "+each+" maxCollisionIterations higher?"            
            print each, cmds.getAttr(each+".startFrame")
            if cmds.getAttr(each+".startFrame") ==getNumStrt:
                print "startFrame is good"
            else:
                print "you might want to check this startFrame attribute"
            print each, cmds.getAttr(each+".enable")
            if cmds.getAttr(each+".enable")!=1:
                print "maybe you want "+each+" enabled?"            
            else:
                print "enabled check is good"
        for each in cmds.ls(type="nRigid"):
            print each+".pointMass", cmds.getAttr(each+".pointMass")
            if each+".pointMass"<20:
                print "you might want to check this pointMass attribute"                   
            else:
                print "pointMass check is good"
        for each in cmds.ls(type="nCloth"):
            print each+".scalingRelation", cmds.getAttr(each+".scalingRelation")
            if each+".scalingRelation"==2:
                print "you might want to check this scalingRelation attribute - setting to 'world(2)' is varying results"                   
            else:
                print "scalingRelation check is good but check resolution. hires is good on 'object(1)' where as lores may be better on 'link(0)'"
            print each+".trappedCheck", cmds.getAttr(each+".trappedCheck")
            if each+".trappedCheck"==1:
                print "you might want to check this trappedCheck attribute...off may have better results"                  
            else:
                print "trappedCheck check is good"
