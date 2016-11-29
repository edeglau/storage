class makeToolKit(object):

        def fix_cam(self):
            getSelectedStuff=cmds.ls(sl=1)
            print len(getSelectedStuff)
            if len(getSelectedStuff)==2:
                    pass
            else:
                    print "you need to select a camera and an object to frame to"
                    return
            focusedThing=cmds.ls(sl=1, fl=1)[1]
            getOldCam=cmds.ls(sl=1, fl=1)[0]
            newcam=cmds.camera()
            cmds.select(newcam[0], r=1)
            cmds.select(getOldCam, add=1)
            getBaseClass.massTransfer()
            cmds.select(focusedThing, r=1)
            cmds.viewFit()
            cmds.delete(newcam[0])


        def grab_blend(self):
            findThisType="blendShape"
            getSel=cmds.ls(sl=1)
            if len(getSel)==0:
                getSel=cmds.ls(type=findThisType)  
                cmds.select(getSel, r=1)
                return    
            else:
                pass
            cmds.select(cl=1)
            collect=[]
            for each in getSel:
                getShape=cmds.listRelatives(each, ad=1, type="shape")
                if getShape != None:
                    for item in getShape:
                        getNode=cmds.findType(item, type=findThisType)
                        if getNode != None:
                            print getNode
                            collect.append(getNode)
                            cmds.select(getNode, add=1)


        def selectNclothcloth(self):
            findThisType="nCloth"
            getSel=cmds.ls(sl=1)
            if len(getSel)==0:
                getSel=cmds.ls(type=findThisType)  
                cmds.select(getSel, r=1)
                return    
            else:
                pass
            cmds.select(cl=1)
            collect=[]
            for each in getSel:
                getShape=cmds.listRelatives(each, ad=1, type="shape")
                if getShape != None:
                    for item in getShape:
                        getNode=cmds.listConnections(item, scn=1, et=1, sh=1, type=findThisType)
                        if getNode != None:
                            print getNode
                            collect.append(getNode)
                            cmds.select(getNode, add=1)


        def grab_nucleus(self):
            findThisType="nucleus"
            getSel=cmds.ls(sl=1)
            if len(getSel)==0:
                getSel=cmds.ls(type=findThisType)  
                cmds.select(getSel, r=1)
                return    
            else:
                pass       
            cmds.select(cl=1)
            collect=[]
            for each in getSel:
                getShape=cmds.listRelatives(each, ad=1, type="shape")
                if getShape != None:
                    for item in getShape:
                        getNode=cmds.findType(item, type=findThisType)
                        if getNode != None:
                            print getNode
                            collect.append(getNode)
                            cmds.select(getNode, add=1)


            # nType="nucleus"
            # getSel=cmds.ls(sl=1)
            # if len(getSel)<1:
            #     print "select something"
            #     return
            # else:
            #     pass
            # cmds.select(cl=1)
            # collect=[]
            # for each in getSel:
            #     # if cmds.nodeType(each) == "mesh":
            #     #     getShape=each
            #     # elif cmds.nodeType(each) == "transform":
            #     getShape=cmds.listRelatives(each, type="shape")
            #     for item in getShape:
            #         getNode=cmds.findType(item, type=nType)
            #         if getNode != None:
            #             print getNode
            #             collect.append(getNode)
            #             pass
            #         else:
            #             print "no nucleus in scene found connected to this object"
            #             return
            # cmds.select(collect, r=1)



        def selectNclothMesh(self):
            typeN="mesh"
            getSel=cmds.ls(sl=1)
            if len(getSel)<1:
                getSel=[(item) for each in cmds.ls(type=typeN) for item in cmds.listRelatives(each, p=1, type="transform") if "Orig" not in str(each)]
            else:
                pass                 
            cmds.select(cl=1)
            collect=[]
            for each in getSel:
                getShape=cmds.listRelatives(each, ad=1, type="shape")
                if getShape != None:
                    for item in getShape:
                        getNode=cmds.listConnections(item, s=1, d=1, type=typeN)
                        if getNode != None:
                            print getNode
                            collect.append(getNode)
                            cmds.select(getNode, add=1)





        def streamSelector(self):
            getSel=cmds.ls(sl=1)
            if len(getSel)<1:
                print "select something"
                return
            else:
                pass
            cmds.select(cl=1)
            collect=[]
            for each in getSel:
                if cmds.nodeType(each) == "mesh":
                    getShape=each
                    pass
                elif cmds.nodeType(each) == "transform":
                    getShape=cmds.listRelatives(each, type="shape")
                    pass
                else:
                    print "need to select a transform mesh or shape"
                    return
                for item in getShape:
                    getNode=cmds.findType(item, type=nType)
                    if getNode != None:
                        print getNode
                        collect.append(getNode)
                        pass
                    else:
                        print "no nucleus in scene found connected to this object"
                        return
            cmds.select(collect, r=1)



        def selectNclothCache(self):
            typeN="cacheFile"
            getSel=cmds.ls(sl=1)
            if len(getSel)==0:
                getSel=cmds.ls(type=typeN)
            else:
                pass       
            cmds.select(cl=1)
            collect=[]
            for each in getSel:
                getShape=cmds.listRelatives(each, ad=1, type="shape")
                if getShape != None:
                    for item in getShape:
                        getNode=cmds.listConnections(item, s=1, d=1, type=typeN)
                        if getNode != None:
                            print getNode
                            collect.append(getNode)
                            cmds.select(getNode, add=1)



        def streamSelectorV1(self, typeN):
            getSel=cmds.ls(sl=1)
            cmds.select(cl=1)
            collect=[]
            for each in getSel:
                getShape=cmds.listRelatives(each, ad=1, type="shape")
                if getShape != None:
                    for item in getShape:
                        getNode=cmds.listConnections(item, s=1, d=1, type=typeN)
                        if getNode != None:
                            collect.append(getNode)
                            cmds.select(getNode, add=1)                



        def initialize_strt_based_on_nucleus(self):
            getNode=cmds.ls(type="nucleus")
            getStartValue=cmds.getAttr(getNode[0]+".startFrame")
            getLowRange=cmds.playbackOptions(min=getStartValue)


        def initialize_strt_based_on_first(self):
            getLowRange=cmds.playbackOptions(q=1, min=1)
            print getLowRange
            getNode=cmds.ls(type="nucleus")
            for each in getNode:
                cmds.setAttr(each+".startFrame", getLowRange)

        def initialize_strt(self):
            '''COPY OF THE ABOVE : initialize_strt_based_on_nucleus - FOR LEGACY ONLY'''
            getNode=cmds.ls(type="nucleus")
            getStartValue=cmds.getAttr(getNode[0]+".startFrame")
            getLowRange=cmds.playbackOptions(min=getStartValue)


        def initialize_strt_based_on_wkrange(self):
            getNode=cmds.ls(".startFrame")
            for each in cmds.ls("*:*.startFrame"):
                getNode.append(each)
            getPrerollRange=wk_strt_value-15
            print str(wk_strt_value)+" = old start range"
            getLowRange=cmds.playbackOptions(min=getPrerollRange, ast=getPrerollRange)
            print str(getPrerollRange)+" = new start cache range"
            postRollRange=wk_out_value+1
            print str(wk_out_value)+" = old end range"
            cmds.playbackOptions(max=postRollRange, aet=postRollRange)
            print str(postRollRange)+" = new end cache range"
            for each in getNode:
                try:
                    cmds.setAttr(each, getLowRange)
                    print "setting "+each+" to "+str(getLowRange)
                except:
                    pass


        def reset_wraps(self):
            getit=cmds.ls(type="cape")
            cmds.select(getit)
            for each in getit:
                cmds.setAttr(each+".envelope", 0)
                cmds.setAttr(each+".envelope", 1)    
                cmds.setAttr(each+".interpolation", 1)      
                cmds.setAttr(each+".interpolation", 0)
            getit=cmds.ls(type="wrap")
            cmds.select(getit)
            for each in getit:
                cmds.setAttr(each+".envelope", 0)
                cmds.setAttr(each+".envelope", 1)    
                cmds.setAttr(each+".exclusiveBind", 0)
                cmds.setAttr(each+".exclusiveBind", 1)       

        def grabCameraLights(self):
            if cmds.objExists("*:camlight_loc"):
                print "cam lights already exist - won't import"
                pass
            else:
                getCameraGrp=cmds.ls("*:*.cameraPreset")
                getNode=str(pm.PyNode(getCameraGrp[0]).node())
                getCam=[each for each in cmds.listRelatives(getNode, ad=1) if cmds.nodeType(each) =="camera"]
                gettransformCam=[each for each in cmds.listRelatives(getCam[0], p=1) if cmds.nodeType(each) =="transform"][0]
                getcamlightPath='/jobs/'+PROJECT+'/COMMON/rig/template/cam_light_loc.mb'
                namer='cam_light_loc'
                cmds.file(getcamlightPath, i=1, type="mayaBinary", ignoreVersion=1, ra=True, mergeNamespacesOnClash=False, namespace=namer, options="v=0;", pr=1)
                getLocCam=cmds.ls('cam_light_loc*:camlight_loc')[0]
                cmds.select(gettransformCam, r=1)
                cmds.select(getLocCam, add=1)
                self._transfer_anim_attr()
                print "imported cam lights"
            if cmds.objExists("okja_techanim_playblast_shd"):
                FVfirst=cmds.ls("okja_techanim_playblast_shd")[0]
                print "shader already exists. Won't create"
                print cmds.getAttr("okja_techanim_playblast_shd.color")
                if cmds.getAttr("okja_techanim_playblast_shd.color")==[(1.0, 1.0, 1.0)]:
                    print "default grey blast"
                    self.makeDefaultsetup(FVfirst)
                else:
                    print "occ blast"
                    self.makeOccsetup(FVfirst)
            else:               
                FVfirst = cmds.shadingNode('blinn', asShader=True, n="okja_techanim_playblast_shd")
                self.makeOccsetup(FVfirst)

        def makeDefaultsetup(self, FVfirst):
            maya.mel.eval( "setRendererInModelPanel base_OpenGL_Renderer modelPanel3;" )
            cmds.modelEditor('modelPanel4', e=1, dl="default")
            cmds.modelEditor( 'modelPanel4', e=1, twoSidedLighting=False) # Query for non-UI names for any render overrides
            cmds.modelEditor( 'modelPanel4', e=1, shadows=False) # Query for non-UI names for any render overrides
            # cmds.setAttr("piggo_okja*:animGeo.res", 4)            
            '''---------------------------------
            assign shader
            ---------------------------------'''
            getType=["*:noTransform", "*:c_okja_001_mid", "*:c_okja_001_hi","*:c_okja_001_xhi", "c_okja_001_hi", "c_okja_001_mid", "c_okja_001_xhi"]
            collectItem=[(item) for each in getType for item in cmds.ls(each) ]  
            setName="sash" 
            # getSel=cmds.listRelatives(cmds.ls('postTech'), ad=1, type="mesh")        
            cmds.setAttr("okja_techanim_playblast_shd.color", 0.5, 0.5, 0.5, type="double3")
            cmds.setAttr("okja_techanim_playblast_shd.eccentricity", 0.0)
            cmds.setAttr("okja_techanim_playblast_shd.specularRollOff", 0.0)
            cmds.setAttr("okja_techanim_playblast_shd.specularColor", .0, .0, .0, type="double3")
            cmds.setAttr("okja_techanim_playblast_shd.reflectivity", 0.0)
            if cmds.objExists(setName):
                pass
            else:
                cmds.sets(n=setName, co=3)
            for selected in collectItem:
                cmds.sets(selected, add=setName)
                cmds.select(selected)
                cmds.hyperShade(assign=str(FVfirst))
                cmds.select( cl=True )
            print "set for default"

        def makeOccsetup(self, FVfirst):
            cmds.setAttr("hardwareRenderingGlobals.ssaoEnable", 1)
            cmds.setAttr("hardwareRenderingGlobals.ssaoAmount", 2.26)
            cmds.setAttr("hardwareRenderingGlobals.ssaoRadius", 1)
            cmds.setAttr("hardwareRenderingGlobals.ssaoFilterRadius", 4)
            cmds.setAttr("hardwareRenderingGlobals.ssaoSamples", 32)
            maya.mel.eval( "ActivateViewport20;" )
            maya.mel.eval( "DisplayLight;" )
            cmds.modelEditor( 'modelPanel4', e=1, twoSidedLighting=True) # Query for non-UI names for any render overrides
            cmds.modelEditor( 'modelPanel4', e=1, shadows=True) # Query for non-UI names for any render overrides
            # cmds.setAttr("piggo_okja*:animGeo.res", 4)            
            '''---------------------------------
            assign shader
            ---------------------------------'''
            getType=["*:noTransform", "*:c_okja_001_mid", "*:c_okja_001_hi","*:c_okja_001_xhi", "c_okja_001_hi", "c_okja_001_mid", "c_okja_001_xhi"]
            collectItem=[(item) for each in getType for item in cmds.ls(each) ]  
            setName="sash" 
            # getSel=cmds.listRelatives(cmds.ls('postTech'), ad=1, type="mesh")        
            cmds.setAttr("okja_techanim_playblast_shd.color", 1.0, 1.0, 1.0, type="double3")
            cmds.setAttr("okja_techanim_playblast_shd.eccentricity", 0.453)
            cmds.setAttr("okja_techanim_playblast_shd.specularRollOff", 0.222)
            cmds.setAttr("okja_techanim_playblast_shd.specularColor", .470, .470, .470, type="double3")
            cmds.setAttr("okja_techanim_playblast_shd.reflectivity", 0.0)
            if cmds.objExists(setName):
                pass
            else:
                cmds.sets(n=setName, co=3)
            for selected in collectItem:
                cmds.sets(selected, add=setName)
                cmds.select(selected)
                cmds.hyperShade(assign=str(FVfirst))
                cmds.select( cl=True )
            print "set for occlusion"

        def grabCameraLightsV1(self):
            getCameraGrp=cmds.ls("*:*.cameraPreset")
            getNode=str(pm.PyNode(getCameraGrp[0]).node())
            getCam=[each for each in cmds.listRelatives(getNode, ad=1) if cmds.nodeType(each) =="camera"]
            gettransformCam=[each for each in cmds.listRelatives(getCam[0], p=1) if cmds.nodeType(each) =="transform"][0]
            getcamlightPath='/jobs/'+PROJECT+'/COMMON/rig/template/cam_light_loc.mb'
            namer='cam_light_loc'
            # cmds.file(getcamlightPath, i=1, type="mayaAscii", ignoreVersion=1, ra=True, mergeNamespacesOnClash=False, namespace=namer, options="v=0;", pr=1)
            cmds.file(getcamlightPath, i=1, type="mayaBinary", ignoreVersion=1, ra=True, mergeNamespacesOnClash=False, namespace=namer, options="v=0;", pr=1)
            getLocCam=cmds.ls('cam_light_loc*:camlight_loc')[0]
            cmds.select(gettransformCam, r=1)
            cmds.select(getLocCam, add=1)
            self._transfer_anim_attr()
            cmds.setAttr("hardwareRenderingGlobals.ssaoEnable", 1)
            cmds.setAttr("hardwareRenderingGlobals.ssaoAmount", 2.26)
            cmds.setAttr("hardwareRenderingGlobals.ssaoRadius", 1)
            cmds.setAttr("hardwareRenderingGlobals.ssaoFilterRadius", 4)
            cmds.setAttr("hardwareRenderingGlobals.ssaoSamples", 32)
            maya.mel.eval( "ActivateViewport20;" )
            maya.mel.eval( "DisplayLight;" )
            cmds.modelEditor( 'modelPanel4', e=1, twoSidedLighting=True) # Query for non-UI names for any render overrides
            cmds.modelEditor( 'modelPanel4', e=1, shadows=True) # Query for non-UI names for any render overrides
            # cmds.setAttr("piggo_okja*:animGeo.res", 4)            
            '''---------------------------------
            assign shader
            ---------------------------------'''
            getType=["*:noTransform", "*:c_okja_001_mid", "*:c_okja_001_hi","*:c_okja_001_xhi", "c_okja_001_hi", "c_okja_001_mid", "c_okja_001_xhi"]
            collectItem=[(item) for each in getType for item in cmds.ls(each) ]  
            setName="sash" 
            # getSel=cmds.listRelatives(cmds.ls('postTech'), ad=1, type="mesh")        
            FVfirst = cmds.shadingNode('blinn', asShader=True, n="okja_techanim_playblast_shd")
            getFVfirst=[FVfirst]
            cmds.setAttr("okja_techanim_playblast_shd.color", 1.0, 1.0, 1.0, type="double3")
            cmds.setAttr("okja_techanim_playblast_shd.eccentricity", 0.453)
            cmds.setAttr("okja_techanim_playblast_shd.specularRollOff", 0.222)
            cmds.setAttr("okja_techanim_playblast_shd.specularColor", .470, .470, .470, type="double3")
            cmds.setAttr("okja_techanim_playblast_shd.reflectivity", 0.0)
            if cmds.objExists(setName):
                pass
            else:
                cmds.sets(n=setName, co=3)
            for selected in collectItem:
                cmds.sets(selected, add=setName)
                cmds.select(selected)
                cmds.hyperShade(assign=str(FVfirst))
                cmds.select( cl=True )


        def _transfer_anim_attr(self, arg=None):
            '''This copies values and animcurve nodes of a first selection to all secondary selections'''
            getSel=cmds.ls(sl=1)
            getChildren=getSel[1:]
            getParent=getSel[:1]
            for each in getChildren:
                getFirstattr=cmds.listAttr (getParent[0], w=1, a=1, s=1, u=1, m=0)
                for item in getFirstattr:
                    if "." not in item:
                        if "direction" not in item:
                            get=cmds.keyframe(getParent[0]+'.'+item, q=1, kc=1)
                            if get!=0:
                                try:
                                    getSource=connectionInfo(getParent[0]+'.'+item, sfd=1)
                                    newAnimSrce=duplicate(getSource)
                                    lognm=newAnimSrce[0].replace(str(getParent[0]), str(each))
                                    #===========================================================
                                    # remove numbers at end
                                    #===========================================================
                                    newname=re.sub("\d+$", "", lognm)
                                    cmds.rename(newAnimSrce, newname)
                                    getChangeAttr=each+'.'+item                        
                                    connectAttr(newname+'.output', getChangeAttr, f=1)                             
                                except:
                                    pass
                            else:
                                try:
                                    getValue=getattr(getParent[0],item).get()
                                    getChangeAttr=getattr(each,item)
                                    getChangeAttr.set(getValue)
                                except:
                                    pass





        def saveSelection(self, arg=None):
            getScenePath=cmds.file(q=1, location=1)
            getPathSplit=getScenePath.split("/")
            folderPath='\\'.join(getPathSplit[:-1])+"\\"        
            if "Windows" in OSplatform:
                newfolderPath=re.sub(r'/',r'\\', folderPath)
            if "Linux" in OSplatform:
                newfolderPath=re.sub(r'\\',r'/', folderPath)
            folderBucket=[]
            winName = "Save selected externally"
            winTitle = winName
            if cmds.window(winName, exists=True):
                    deleteUI(winName)
            window = cmds.window(winName, title=winTitle, tbm=1, w=620, h=100 )
            cmds.menuBarLayout(h=30)
            stringField='''"Save selected" (launches window)a home made scripted save selection externally.
        Put full file path with preferred name of
        object in text field("/usr/people/<user>/joint4"). save button saves out file. Can add
        more to save from add selected at top. Will save out a file
        EG:"/usr/people/<user>/joint4.txt"

            * Step 1: select object or components
            * Step 2: pressing save will create .txt files that will contain the component names within the
                path indicated and name of file indicated in field

             "ADD SELECTION" - button
                Adds a slot for new object (each parent is added seperately)
            "SAVE" - button
                Will change the value on the attribute that is currently
                    visible in the drop down menu
            "OPEN FOLDER" - button
                opens the folder window for path indicated
            "ATTR DICT" - button
                prints out an attriubute dictionary for personal use(see script editor)
                useful for writing a "setAttr" script on custom setups'''
            self.fileMenu = cmds.menu( label='Help', pmc=lambda *args:self.helpWin(stringField))        
            cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=620)
            cmds.frameLayout('bottomFrame', label='', lv=0, nch=1, borderStyle='in', bv=1, p='selectArrayRow')      
            cmds.gridLayout('listBuildButtonLayout', p='bottomFrame', numberOfColumns=1, cellWidthHeight=(600, 20))         
            fieldBucket=[]
            objNameFile=newfolderPath+str(selObj[0])
            cmds.rowLayout  (' listBuildButtonLayout ', w=600, numberOfColumns=6, cw6=[350, 40, 40, 40, 40, 1], ct6=[ 'both', 'both', 'both',  'both', 'both', 'both'], p='bottomFrame')
            self.getName=cmds.textField(h=25, p='listBuildButtonLayout', text=objNameFile)
            cmds.button (label='Save', w=90, p='listBuildButtonLayout', command = lambda *args:self._save_select(fileName=cmds.textField(self.getName, q=1, text=1)))            
            cmds.button (label='Open folder', w=60, p='listBuildButtonLayout', command = lambda *args:self._open_defined_path(destImagePath=cmds.textField(self.getName, q=1, text=1)))
            cmds.showWindow(window)

        def _save_select(self, fileName):   
            # selObj=ls(sl=1, fl=1, sn=1)
            selObj=cmds.ls(sl=1, fl=1)        
            fileName=fileName+'_select.txt'
            print fileName
            if "Windows" in OSplatform:         
                if not os.path.exists(fileName): os.makedirs(fileName)
            if "Linux" in OSplatform:
                inp=open(fileName, 'w+')
            filterNode=["animCurve"]
            dirDict={}
            getStrtRange=cmds.playbackOptions(q=1, ast=1)#get framerange of scene to set keys in iteration
            getEndRange=cmds.playbackOptions(q=1, aet=1)#get framerange of scene to set keys in iteration
            for each in selObj:
                try:
                    inp.write(str(each+","))
                except:
                    pass
            inp.close()   
            print "saved as "+fileName

        def openSelection(self, arg=None):
            getScenePath=cmds.file(q=1, location=1)
            files, getPath, newfolderPath, filebucket=self.getWorkPath(getScenePath)    
            winName = "Open external selection"
            winTitle = winName
            openFolderPath=newfolderPath+"\\"   
            selObj=cmds.ls(sl=1, fl=1)
            if cmds.window(winName, exists=True):
                    cmds.deleteUI(winName)
            window = cmds.window(winName, title=winTitle, tbm=1, w=600, h=280 )
            cmds.menuBarLayout(h=30)
            stringField='''"Load selection" (launches window) Opens a selection. Put full path with no
        of object in the text field("/usr/people/<user>/").
        Press refresh and it will repopulate the drop down for available .txt files;
        stick to the name of your object to reload anim

            * Step 1: select object - needs to have a matching name
            * Step 2: fill in path(without name EG: "/usr/people/<user>/")
            * Step 3: press "refresh folder"
            * Step 4: if text file available, it should populate in the
                drop down menu. Check path name and if animation is saved first
                if drop down remains empty
            * Step 5: press "Load" button will load animation onto selection

             "REFRESH FOLDER" - button
                Adds a slot for new object (each parent is added seperately)
            "WORKPATH" - button
                Will change the value on the attribute that is currently
                    visible in the drop down menu
            "LOAD" - button
                loads animation
            "OPEN FOLDER" - button
                opens the folder window for path indicated '''
            self.fileMenu = cmds.menu( label='Help', pmc=lambda *args:self.helpWin(stringField))         
            cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=600)
            cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
            cmds.rowLayout  (' rMainRow ', w=600, numberOfColumns=6, p='selectArrayRow')
            cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
            cmds.setParent ('selectArrayColumn')
            cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=1, cellWidthHeight=(480, 20))
            cmds.button (label='refresh folder', p='listBuildButtonLayout', command = lambda *args:self.refresh_text())
            cmds.button (label='workpath', p='listBuildButtonLayout', command = lambda *args:self.refresh_work_text())      
            self.fileDropName=cmds.optionMenu( label='files')
            for each in filebucket:
                cmds.menuItem( label=each)
            self.pathFile=cmds.textField(h=25, p='listBuildButtonLayout', text=newfolderPath)
            cmds.button (label='Load', p='listBuildButtonLayout', command = lambda *args:self._load_selection(printFolder=cmds.textField(self.pathFile, q=1, text=1), grabFileName=cmds.optionMenu(self.fileDropName, q=1, v=1)))
            cmds.button (label='Open folder', p='listBuildButtonLayout', command = lambda *args:self._open_defined_path(destImagePath=cmds.textField(self.pathFile, q=1, text=1)))         
            cmds.showWindow(window)

        def _load_selection(self, printFolder, grabFileName):
            import ast
            notAttr=["isHierarchicalConnection", "solverDisplay", "isHierarchicalNode", "publishedNodeInfo", "fieldScale_Position", "fieldScale", "fieldScale.fieldScale_Position"]         
            printFolder=printFolder+grabFileName    
            selObj=cmds.ls(sl=1, fl=1)
            if os.path.exists(printFolder):
                pass
            else:
                print printFolder+"does not exist"
                return
            getBucket=[]
            attribute_container=[]
            List = open(printFolder).readlines()
            for aline in List:
                if "," in aline:
                    getObj=aline.split(',')
                else:
                    getObj=aline
            for item in getObj:
                if item != "":
                    getBucket.append(item)
            cmds.select(getBucket)                

        def saveConnection(self, arg=None):
            selObj=ls(sl=1, fl=1, sn=1)
            getScenePath=cmds.file(q=1, location=1)
            getPathSplit=getScenePath.split("/")
            folderPath='\\'.join(getPathSplit[:-1])+"\\"        
            if "Windows" in OSplatform:
                newfolderPath=re.sub(r'/',r'\\', folderPath)
            if "Linux" in OSplatform:
                newfolderPath=re.sub(r'\\',r'/', folderPath)
            folderBucket=[]
            winName = "Save connections"
            winTitle = winName
            if cmds.window(winName, exists=True):
                    deleteUI(winName)
            window = cmds.window(winName, title=winTitle, tbm=1, w=620, h=100 )
            cmds.menuBarLayout(h=30)
            stringField='''"Save selected" (launches window)a home made scripted save selection externally.
        Put full file path with preferred name of
        object in text field("/usr/people/<user>/joint4"). save button saves out file. Can add
        more to save from add selected at top. Will save out a file
        EG:"/usr/people/<user>/joint4.txt"

            * Step 1: select object or components
            * Step 2: pressing save will create .txt files that will contain the component names within the
                path indicated and name of file indicated in field

             "ADD SELECTION" - button
                Adds a slot for new object (each parent is added seperately)
            "SAVE" - button
                Will change the value on the attribute that is currently
                    visible in the drop down menu
            "OPEN FOLDER" - button
                opens the folder window for path indicated
            "ATTR DICT" - button
                prints out an attriubute dictionary for personal use(see script editor)
                useful for writing a "setAttr" script on custom setups'''
            self.fileMenu = cmds.menu( label='Help', pmc=lambda *args:self.helpWin(stringField))        
            cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=620)
            cmds.frameLayout('bottomFrame', label='', lv=0, nch=1, borderStyle='in', bv=1, p='selectArrayRow')      
            cmds.gridLayout('listBuildButtonLayout', p='bottomFrame', numberOfColumns=1, cellWidthHeight=(600, 20))         
            fieldBucket=[]
            objNameFile=newfolderPath+str(selObj[0])
            cmds.rowLayout  (' listBuildButtonLayout ', w=600, numberOfColumns=6, cw6=[350, 40, 40, 40, 40, 1], ct6=[ 'both', 'both', 'both',  'both', 'both', 'both'], p='bottomFrame')
            self.getName=cmds.textField(h=25, p='listBuildButtonLayout', text=objNameFile)
            cmds.button (label='Save', w=90, p='listBuildButtonLayout', command = lambda *args:self._save_connection(fileName=cmds.textField(self.getName, q=1, text=1)))
            cmds.button (label='Open folder', w=60, p='listBuildButtonLayout', command = lambda *args:self._open_defined_path(destImagePath=cmds.textField(self.getName, q=1, text=1)))
            cmds.showWindow(window)

        def _save_connection(self, fileName):   
            selObj=cmds.ls(sl=1, fl=1)        
            fileName=fileName+'_connect.txt'
            if "Windows" in OSplatform:    
                # folderPath='/'.join(fileName.split('/')[:-1])+"/"
                # printFolder=re.sub(r'/',r'\\', folderPath)       
                if not os.path.exists(fileName): os.makedirs(fileName)
            if "Linux" in OSplatform:
                inp=open(fileName, 'w+')
            dirDict={}
            getStrtRange=cmds.playbackOptions(q=1, ast=1)#get framerange of scene to set keys in iteration
            getEndRange=cmds.playbackOptions(q=1, aet=1)#get framerange of scene to set keys in iteration
            sourceOutBucket=[]
            sourceInBucket=[]        
            for each in selObj:
                getOutPutConnection=cmds.listConnections(each, p=1, c=1, s=0, d=1)
                for eachController, eachChild in map(None, getOutPutConnection[::2], getOutPutConnection[1::2]):
                    getPlug="MainOBJ."+eachController.split(".")[1]  
                    getoutConnection=getPlug+">"+eachChild
                    if "initialShadingGroup" not in eachChild or "dagSetMembers" not in eachChild:
                        sourceOutBucket.append(getoutConnection)
                getInputConnection=cmds.listConnections(each, p=1, c=1, s=1, d=0)
                for eachController, eachChild in map(None, getInputConnection[::2], getInputConnection[1::2]):
                    getPlug="MainOBJ."+eachController.split(".")[1]  
                    getinConnection=eachChild+">"+getPlug
                    if "instObjGroups" not in getPlug:
                        sourceInBucket.append(getinConnection)
            inp.write("output$")
            for each in sourceOutBucket:
                inp.write(str(each)+",")
            inp.write("input$")         
            for each in sourceInBucket:           
                inp.write(str(each)+",")
            inp.close()   
            print "saved as "+fileName


        def openConnection(self, arg=None):
            getScenePath=cmds.file(q=1, location=1)
            files, getPath, newfolderPath, filebucket=self.getWorkPath(getScenePath)    
            winName = "Open external selection"
            winTitle = winName
            openFolderPath=folderPath+"\\"   
            selObj=cmds.ls(sl=1, fl=1)
            if cmds.window(winName, exists=True):
                    cmds.deleteUI(winName)
            window = cmds.window(winName, title=winTitle, tbm=1, w=600, h=280 )
            cmds.menuBarLayout(h=30)
            stringField='''"Load selection" (launches window) Opens a selection. Put full path with no
        of object in the text field("/usr/people/<user>/").
        Press refresh and it will repopulate the drop down for available .txt files;
        stick to the name of your object to reload anim

            * Step 1: select object - needs to have a matching name
            * Step 2: fill in path(without name EG: "/usr/people/<user>/")
            * Step 3: press "refresh folder"
            * Step 4: if text file available, it should populate in the
                drop down menu. Check path name and if animation is saved first
                if drop down remains empty
            * Step 5: press "Load" button will load animation onto selection

             "REFRESH FOLDER" - button
                Adds a slot for new object (each parent is added seperately)
            "WORKPATH" - button
                Will change the value on the attribute that is currently
                    visible in the drop down menu
            "LOAD" - button
                loads animation
            "OPEN FOLDER" - button
                opens the folder window for path indicated '''
            self.fileMenu = cmds.menu( label='Help', pmc=lambda *args:self.helpWin(stringField))         
            cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=600)
            cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
            cmds.rowLayout  (' rMainRow ', w=600, numberOfColumns=6, p='selectArrayRow')
            cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
            cmds.setParent ('selectArrayColumn')
            cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=1, cellWidthHeight=(480, 20))
            cmds.button (label='refresh folder', p='listBuildButtonLayout', command = lambda *args:self.refresh_text())
            cmds.button (label='workpath', p='listBuildButtonLayout', command = lambda *args:self.refresh_work_text())      
            self.fileDropName=cmds.optionMenu( label='files')
            for each in filebucket:
                cmds.menuItem( label=each)
            self.pathFile=cmds.textField(h=25, p='listBuildButtonLayout', text=newfolderPath)
            cmds.button (label='Load in', p='listBuildButtonLayout', command = lambda *args:self._load_connection_in(printFolder=cmds.textField(self.pathFile, q=1, text=1), grabFileName=cmds.optionMenu(self.fileDropName, q=1, v=1)))
            cmds.button (label='Load out', p='listBuildButtonLayout', command = lambda *args:self._load_connection_out(printFolder=cmds.textField(self.pathFile, q=1, text=1), grabFileName=cmds.optionMenu(self.fileDropName, q=1, v=1)))
            cmds.button (label='Load both', p='listBuildButtonLayout', command = lambda *args:self._load_connection_both(printFolder=cmds.textField(self.pathFile, q=1, text=1), grabFileName=cmds.optionMenu(self.fileDropName, q=1, v=1)))
            cmds.button (label='Open folder', p='listBuildButtonLayout', command = lambda *args:self._open_defined_path(destImagePath=cmds.textField(self.pathFile, q=1, text=1)))         
            cmds.showWindow(window)


        def _load_connection_both(self, printFolder, grabFileName):
            self._load_connection_in(printFolder, grabFileName)
            self._load_connection_out(printFolder, grabFileName)

        def _load_connection_in(self, printFolder, grabFileName):
            import ast
            selObj=cmds.ls(sl=1, fl=1)
            printFolder=printFolder+grabFileName
            if os.path.exists(printFolder):
                pass
            else:
                print printFolder+"does not exist"
                return
            getBucket=[]
            attribute_container=[]
            List = open(printFolder).readlines()
            for aline in List:
                if "input$" in aline:
                    getInput=aline.split("input$")[1]
            getObj=getInput.split(',')
            for item in getObj:
                if len(item)>0:
                    getOutSourcePlug=item.split(">")[0]
                    getSocket=item.split(">")[1]
                    socket=getSocket.replace("MainOBJ", selObj[0])
                    print "connecting: "+str(getOutSourcePlug)+">"+socket
                    try:
                        cmds.connectAttr(getOutSourcePlug, socket, f=1)
                        print "connected: "+str(getOutSourcePlug)+">"+socket
                    except:
                        print "can't connect: "+str(getOutSourcePlug)+">"+socket
                        pass


        def _load_connection_out(self, printFolder, grabFileName):
            selObj=cmds.ls(sl=1, fl=1)
            printFolder=printFolder+grabFileName
            if os.path.exists(printFolder):
                pass
            else:
                print printFolder+"does not exist"
                return
            getBucket=[]
            attribute_container=[]
            List = open(printFolder).readlines()
            for aline in List:
                if "output$" in aline:
                    getOutput=aline.split("output$")[1]
                    getInput=getOutput.split("input$")[0]
            getObj=getInput.split(',')
            for item in getObj:
                if len(item)>0:         
                    getOutSourcePlug=item.split(">")[0]
                    sourcePlug=getOutSourcePlug.replace("MainOBJ", selObj[0])
                    getSocket=item.split(">")[1]
                    print "connecting: "+str(sourcePlug)+">"+getSocket
                    try:
                        cmds.connectAttr(sourcePlug, getSocket, f=1)
                        print "connected: "+str(sourcePlug)+">"+getSocket
                    except:
                        print "can't connect: "+str(sourcePlug)+">"+getSocket
                        pass


        def blendSearchGroups(self):
            #only prefix
            selObj=cmds.ls(sl=1, fl=1)
            if selObj:
                pass
            else:
                print "must select a driver group and a driven group(same shortnames)"
                return
            parentObj=selObj[0]
            childrenObj=selObj[1]
            getparentObj=cmds.listRelatives(parentObj, ad=1, type="mesh")
            getchildObj=cmds.listRelatives(childrenObj, ad=1, type="mesh")
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
                        if grabNameChild==grabNameParent:
                            print "blending: "+childItem+' to '+parentItem
                            try:
                                BlendShapeName=cmds.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", w=(0, 1.0))
                            except:
                                pass



        def blendSearchGroups(self):
            #only prefix
            selObj=cmds.ls(sl=1, fl=1)
            if selObj:
                pass
            else:
                print "must select a driver group and a driven group(same shortnames)"
                return
            parentObj=selObj[0]
            childrenObj=selObj[1]
            getparentObj=cmds.listRelatives(parentObj, ad=1, type="mesh")
            getchildObj=cmds.listRelatives(childrenObj, ad=1, type="mesh")
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
                        if grabNameChild==grabNameParent:
                            print "blending: "+childItem+' to '+parentItem
                            try:
                                BlendShapeName=cmds.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", w=(0, 1.0))
                            except:
                                pass


        def testBlend(self):
            #only prefix
            import pymel.core as pm
            selObj=cmds.ls(sl=1, fl=1)
            parentObj=selObj[0]
            childrenObj=selObj[1]
            getparentObj=cmds.listRelatives(parentObj, ad=1, type="mesh")
            getchildObj=cmds.listRelatives(childrenObj, ad=1, type="mesh")
            for childItem in getchildObj:
                grabNameChild=str(pm.PyNode(childItem).nodeName())
                grabNameChild=grabNameChild.split(":")[-1]
                grabNameChild=grabNameChild.split("Shape")[0]
                for parentItem in getparentObj:
                    grabNameParent=str(pm.PyNode(parentItem).nodeName())
                    grabNameParent=grabNameParent.split(":")[-1]
                    grabNameParent=grabNameParent.split("Shape")[0]
                if grabNameChild==grabNameParent:
                    print "blending: "+childItem+' to '+parentItem
                    try:
                        BlendShapeName=cmds.blendShape(parentItem, childItem, n=str(grabNameParent)+"_bs", w=(0, 1.0))
                    except:
                        pass


        def connect_to_curve(self):
            selObj=cmds.ls(sl=1)
            microLeadCurve=[selObj[0]]
            CVbucketbuckList=[]
            childControllers=selObj[1:]
            for each in microLeadCurve:
                each=cmds.ls(each)[0]
                for eachCV, eachCtrlGro in map(None, pm.PyNode(each).cv, childControllers):
                # for eachCV, eachCtrlGro in map(None, each.cv, childControllers):
                    CVbucketbuckList.append(eachCV)
            microLeadCurve=ls(microLeadCurve)[0]        
            for eachCtrlGro in childControllers:
                try:
                    pgetCVpos=cmds.xform(eachCtrlGro, ws=1, q=1, t=1)
                except:
                    pass
                getpoint=microLeadCurve.closestPoint(pgetCVpos, tolerance=0.001, space='preTransform')
                getParam=microLeadCurve.getParamAtPoint(getpoint, space='preTransform')
                select(eachCtrlGro, r=1)
                select(microLeadCurve, add=1)
                motionPath=cmds.pathAnimation(fractionMode=1, follow=1, followAxis="x", upAxis="y", worldUpType="vector", worldUpVector=[0, 1, 0], inverseUp=0, inverseFront=0, bank=0)        
                disconnectAttr(motionPath+"_uValue.output", motionPath+".uValue")
                getpth=str(motionPath)
                setAttr(motionPath+".fractionMode", False)
                setAttr(motionPath+".uValue", getParam)        

        def matchCurveShapes(self):
            self.CurveShapes()

        def matchFullShape(self):
            getFirstGrp, getSecondGrp=self.CurveShapes()
            self.matchCurveShapes_andShrinkWrap(getFirstGrp, getSecondGrp)


        def CurveShapes(self):
            getSel=cmds.ls(sl=1, fl=1)
            if getSel:
                pass
            else:
                print "need to select something"
                return
            getNames=cmds.ls(sl=1, fl=1)
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
            cmds.select(firstList)
            cmds.CreateCurveFromPoly()
            getFirstCurve=cmds.ls(sl=1, fl=1)
            '''get cv total of curve'''
            getFirstCurveInfo=cmds.ls(sl=1, fl=1)
            numberCV=pm.PyNode(getFirstCurveInfo[0]).numCVs()
            cmds.delete(getFirstCurve[0], ch=1)
            '''wrap child mesh to curve'''
            cmds.select(cmds.ls(getFirstGrp)[0], r=1)
            cmds.wire(w=getFirstCurve[0], gw=0, en=1.000000, ce=0.000000, li=0.000000, dds=[(0, 500)] )
            '''create parent curve'''
            cmds.select(secondList)
            cmds.CreateCurveFromPoly()
            getSecondCurve=cmds.ls(sl=1, fl=1)
            getSecondCurveInfo=cmds.ls(sl=1, fl=1)
            '''rebuilt curve to match first curve built'''
            cmds.rebuildCurve(getSecondCurve[0], getFirstCurve[0], rt=2 )
            getSecondCurve=cmds.ls(sl=1, fl=1)
            getSecondCurveInfo=cmds.ls(sl=1, fl=1)
            cmds.delete(getSecondCurve[0], ch=1)
            '''wrap parent curve to parent mesh'''
            cmds.select(getSecondCurve[0], r=1)
            cmds.select(cmds.ls(getSecondGrp)[0], add=1)
            cmds.CreateWrap()
            '''blend child curve to parent curve'''
            cmds.blendShape(getSecondCurve[0], getFirstCurve[0],w=(0, 1.0))
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
            cmds.delete(getFirstGrp, ch=1)
            getShrink=cmds.deformer(getFirstGrp, type="shrinkWrap")
            cmds.connectAttr(getSecondGrp+".worldMesh[0]", getShrink[0]+".targetGeom", f=1)
            for key, value in myDict.items():
                cmds.setAttr(getShrink[0]+key, value)
            # cmds.delete(getFirstGrp, ch=1)
            # cmds.select(getFirstGrp, r=1)
            # cmds.select(cmds.ls(getSecondGrp)[0], add=1)
            # cmds.CreateWrap()



        def cleanModels(self, arg=None):       
            winName = "Clean object"
            winTitle = winName
            if cmds.window(winName, exists=True):
                    cmds.deleteUI(winName)
            window = cmds.window(winName, title=winTitle, tbm=1, w=500, h=100 )
            cmds.menuBarLayout(h=30)
            stringField='''"Clean model" (script)wipes history, resets transforms and averages normals on a
        model(modelling)

            "CLEAN+HISTORY" - button
                * Step 1: Select object
                * Step 2: pressing this button cleans history, zeros out object and
                    cleans shape name, removes custom attr, averages normals(hard edges)
            "CLEAN" - button
                * Step 1: Select object
                * Step 2: pressing this button zeros out object and
                    cleans shape name, removes custom attr, averages normals(hard edges)'''
            self.fileMenu = cmds.menu( label='Help', hm=1, pmc=lambda *args:toolClass.helpWin(stringField))           
            cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=500)
            cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
            cmds.rowLayout  (' rMainRow ', w=500, numberOfColumns=6, p='selectArrayRow')
            cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
            cmds.setParent ('selectArrayColumn')
            cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(240, 20))
            cmds.button (label='clean+history', p='listBuildButtonLayout', command = lambda *args:getBaseClass.cleanObjHist(winName))
            cmds.button (label='clean', p='listBuildButtonLayout', command = lambda *args:getBaseClass.cleanObj(winName))  
            showWindow(window)


        def pointGlue_mass_to_one(self):
            blenderShape=cmds.ls(sl=1)[0]
            for each in cmds.ls(sl=1)[1:]:
                command='pointGlue -s "%s" -t "%s" -max 1' % (str(blenderShape), each)
                maya.mel.eval( command )


        def opening_folder(self, folderPath):
            # newfolderPath=re.sub(r'\\',r'/', folderPath)
            os.system('xdg-open "%s"' % folderPath)
