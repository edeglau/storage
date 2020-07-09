from toolbase.cache_stuff import wk_strt_value


    def blast_def(self):
        fps_set = float(str(self.fps_fieldText.text()))
        mc.playbackOptions(fps = fps_set, e=1)
        strt_rng = mc.playbackOptions(q=1, min=1)
        end_rng = mc.playbackOptions(q=1, max=1)
        focPane = [(each) for each in mc.getPanel(vis=1) if "model" in each]
        for each in focPane:
            if mc.modelEditor(each, q=1, av=1) == True:
                mc.modelEditor(each, e=1, rnm = "base_OpenGL_Renderer")     
        folder_strt = '/'.join(mc.file(q=1, location=1).split('/')[:-5])
        scn_name=str(mc.file(q=1, location=1)).split('/')[-1].split(".")[0]
        gotten_name=str(mc.file(q=1, location=1)).split('/')[-1].split(".")[0]+"-playblast-half1712x903_vdf8"
        gotten_path = "{}/PRODUCTS/images/{}/{}/playblast-half1712x903_vdf8_jpg/{}".format(folder_strt, _dept_task, scn_name, gotten_name)
        sel_NumMn=mc.playbackOptions(q=1, min=1)
        sel_NumMn_reset=mc.playbackOptions(q=1, min=1)+1    
        mc.currentTime(sel_NumMn)
        mc.currentTime(sel_NumMn_reset)        
        mc.currentTime(sel_NumMn)
        mc.playblast(format="image", filename=gotten_path, sequenceTime=0, clearCache=1, viewer= 1,  showOrnaments=1, offScreen=1, fp=4, percent = 100, compression = "jpg",  quality = 100, widthHeight = (1712, 903))
        mc.playbackOptions(fps = 1.0, e=1)        
        mm.eval('setPolyCountVisibility(0);') 
                
    def mem_blast(self):
        fps_set = float(str(self.fps_fieldText.text()))
        mc.playbackOptions(fps = fps_set, e=1)
        focPane = [(each) for each in mc.getPanel(vis=1) if "model" in each]
        for each in focPane:
            if mc.modelEditor(each, q=1, av=1) == True:
                mm.eval('setRendererInModelPanel "vp2Renderer" {0}'.format(each))        
        mm.eval('setPolyCountVisibility(1);')
        folder_strt = '/'.join(mc.file(q=1, location=1).split('/')[:-5])
        scn_name=str(mc.file(q=1, location=1)).split('/')[-1].split(".")[0]
        gotten_name=str(mc.file(q=1, location=1)).split('/')[-1].split(".")[0]+"-playblast-half1712x903_vdf8"
        gotten_path = "{}/PRODUCTS/images/{}/{}/playblast-half1712x903_vdf8_jpg/{}".format(folder_strt, _dept_task, scn_name, gotten_name)
        sel_NumMn=mc.playbackOptions(q=1, min=1)
        sel_NumMn_reset=mc.playbackOptions(q=1, min=1)+1    
        mc.currentTime(sel_NumMn)
        mc.currentTime(sel_NumMn_reset)        
        mc.currentTime(sel_NumMn)
        mc.playblast(format="image", filename=gotten_path, sequenceTime=0, clearCache=1, viewer= 1,  showOrnaments=1, offScreen=1, fp=4, percent = 100, compression = "jpg",  quality = 100, widthHeight = (1712, 903))
        mc.playbackOptions(fps = 1.0, e=1)        
        mm.eval('setPolyCountVisibility(0);')
        for each in focPane:
            if mc.modelEditor(each, q=1, av=1) == True:
                mc.modelEditor(each, e=1, rnm="base_OpenGL_Renderer") 
                
    def mem_blast_no_roll(self):
        fps_set = float(str(self.fps_fieldText.text()))
        mc.playbackOptions(fps = fps_set, e=1)
        strt_rng = int(wk_strt_value)-1
        end_rng = mc.playbackOptions(q=1, max=1)
        focPane = [(each) for each in mc.getPanel(vis=1) if "model" in each]
        for each in focPane:
            if mc.modelEditor(each, q=1, av=1) == True:
                mm.eval('setRendererInModelPanel "vp2Renderer" {0}'.format(each))        
        mm.eval('setPolyCountVisibility(1);')
        folder_strt = '/'.join(mc.file(q=1, location=1).split('/')[:-5])
        scn_name=str(mc.file(q=1, location=1)).split('/')[-1].split(".")[0]
        gotten_name=str(mc.file(q=1, location=1)).split('/')[-1].split(".")[0]+"-playblast-half1712x903_vdf8"
        gotten_path = "{}/PRODUCTS/images/{}/{}/playblast-half1712x903_vdf8_jpg/{}".format(folder_strt, _dept_task, scn_name, gotten_name)
        sel_NumMn=mc.playbackOptions(q=1, min=1)
        sel_NumMn_reset=mc.playbackOptions(q=1, min=1)+1    
        mc.currentTime(sel_NumMn)
        mc.currentTime(sel_NumMn_reset)        
        mc.currentTime(sel_NumMn)
        mc.playblast(format="image", filename=gotten_path, sequenceTime=0, clearCache=1, viewer= 1,  showOrnaments=1, offScreen=1, fp=4, percent = 100, compression = "jpg",  quality = 100, widthHeight = (1712, 903))
        mc.playbackOptions(fps = 1.0, e=1)        
        mm.eval('setPolyCountVisibility(0);')
        for each in focPane:
            if mc.modelEditor(each, q=1, av=1) == True:
                mc.modelEditor(each, e=1, rnm="base_OpenGL_Renderer") 
        mc.playbackOptions(fps = 1.0, e=1) 

    def wit_cam(self, arg=None):
        focusedThing=cmds.ls(sl=1, fl=1)[0]
        if cmds.nodeType(focusedThing)=="transform":
            focPane = [(each) for each in cmds.getPanel(vis=1) if "model" in each][0]
            command='postModelEditorSelectCamera "%s" "%s" 0' % (focPane, focPane)
            maya.mel.eval( command )  
            getOldCam=cmds.ls(sl=1, fl=1)[0]
            newcam=cmds.duplicate(getOldCam, n=focusedThing+"wit_cam")[0]
            command='lookThroughModelPanel "%s" "%s"' % (newcam, focPane)
            maya.mel.eval( command )       
        elif cmds.nodeType(focusedThing)=="mesh":
            command='rivet;'
            maya.mel.eval( command )
            locatorObj=cmds.ls(sl=1, fl=1)[0]
            focPane = [(each) for each in cmds.getPanel(vis=1) if "model" in each][0]
            command='postModelEditorSelectCamera "%s" "%s" 0' % (focPane, focPane)
            maya.mel.eval( command )  
            getOldCam=cmds.ls(sl=1, fl=1)[0]
            newcam=cmds.duplicate(getOldCam, n=focusedThing+"wit_cam")[0]
            cmds.parentConstraint(locatorObj,newcam, mo=1)
            command='lookThroughModelPanel "%s" "%s"' % (newcam, focPane)
            maya.mel.eval( command )
            cmds.setAttr(locatorObj+".visibility", 0)
 