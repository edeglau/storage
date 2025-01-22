    def offset_cache(self):
        checkSel = cmds.ls(sl=1)
        if len(checkSel)<2:
            print "you need to select two objects"
        leader = checkSel[1]
        cmds.select(leader, r=1)
        cmds.ConvertSelectionToVertices(leader)
        ld_lctr = self.plotter_avrg()
        follower = checkSel[0]
        cmds.select(follower, r=1)
        cmds.ConvertSelectionToVertices(follower)
        flw_lctr = self.plotter_avrg()
        # set the offset node for translate
        plsMns = cmds.shadingNode("plusMinusAverage", asUtility = 1)
        cmds.setAttr(plsMns+".operation", 2)
        cmds.connectAttr(ld_lctr+".translate", plsMns+".input3D[0]", f=1)
        cmds.connectAttr(flw_lctr+".translate", plsMns+".input3D[1]", f=1)
        # set cluster
        cmds.select(checkSel[0])
        getpar=cmds.listRelatives(checkSel[0], p=1)
        getchildren=[(nodes) for nodes in cmds.listRelatives(getpar[0], ad=1, type="mesh") if "Orig" not in str(nodes) ]
        cmds.select(getchildren, add =1 )
        create_cstr = cmds.cluster()
        # connect result to cluster
        cmds.connectAttr( plsMns+".output3D", create_cstr[0]+"Handle.translate", f = 1)


    def plotter_avrg(self):
        '''plots a locator to a vertice or face per keyframe in a timeline'''
        selObj=cmds.ls(sl=1, fl=1)      
        if len(selObj)>0:
            pass
        else:
            print "Select 1 object" 
            return     
        getTopRange=cmds.playbackOptions(q=1, max=1)+1#get framerange of scene to set keys in iteration 
        getLowRange=cmds.playbackOptions(q=1, min=1)-1#get framerange of scene to set keys in iteration 
        edgeBucket=[]
        getRange=arange(getLowRange,getTopRange, 1 )
        getloc=cmds.spaceLocator(n=selObj[0]+"cnstr_lctr")
        cmds.normalConstraint(selObj[0], getloc[0])
        placeloc=cmds.spaceLocator(n=selObj[0]+"lctr")
        for each in getRange:
            cmds.currentTime(each)            
            transform=cmds.xform(selObj, q=1, ws=1, t=1)
            posBucketx=self.array_median_find(transform[0::3])
            posBuckety=self.array_median_find(transform[1::3])
            posBucketz=self.array_median_find(transform[2::3])
            cmds.xform(getloc[0], ws=1, t=(posBucketx, posBuckety, posBucketz))  
            cmds.SetKeyTranslate(getloc[0])
            cmds.xform(placeloc[0], ws=1, t=(posBucketx, posBuckety, posBucketz))
            cmds.SetKeyTranslate(placeloc[0])               
            rotate=cmds.xform(getloc[0], q=True, ws=1, ro=True)
            cmds.xform(placeloc[0], ws=1, ro=rotate)  
            cmds.SetKeyRotate(placeloc[0])
            cmds.currentTime(each)
        cmds.delete(getloc[0])
        return placeloc[0]

    def array_median_find(self, lst):
        mysum=numpy.median(numpy.array(lst))
        return mysum
