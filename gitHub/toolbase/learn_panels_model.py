    def mem_blast(self):
        fps_set = float(str(self.fps_fieldText.text()))
        focPane = [(each) for each in mc.getPanel(vis=1) if "model" in each]
        for each in focPane:
            if mc.modelEditor(each, q=1, av=1) == True:
                mm.eval('setRendererInModelPanel "vp2Renderer" {0}'.format(each))        
        mm.eval('setPolyCountVisibility(1);')
        folder_strt = '/'.join(mc.file(q=1, location=1).split('/')[:-5])
        scn_name=str(mc.file(q=1, location=1)).split('/')[-1].split(".")[0]
        gotten_name=str(mc.file(q=1, location=1)).split('/')[-1].split(".")[0]+"-playblast-half1712x903_vdf8"
        gotten_path = "{}/PRODUCTS/images/{}/{}/playblast-half1712x903_vdf8_jpg/{}".format(folder_strt, _dept_task, scn_name, gotten_name)
        mc.playbackOptions(fps = fps_set, e=1)
        sel_NumMn=mc.playbackOptions(q=1, min=1)
        sel_NumMn_reset=mc.playbackOptions(q=1, min=1)+1
        mc.currentTime(sel_NumMn)
        mc.currentTime(sel_NumMn_reset)        
        mc.c
