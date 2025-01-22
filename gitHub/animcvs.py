
    def blendWeightExecutionCallup(self, getCVrange, weightList, blendShapeInputCurves, getSel):
        '''>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..
        cv weight name in blendshape template: cmds.select('blendShape1.inputTarget[1].inputTargetGroup[0].targetWeights[4]')
        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'''
        setAttrDict={}
        print blendShapeInputCurves
        print weightList
        for eachCVInCaptureRange, targetWeightValue in map(None, getCVrange, weightList):
            for blendConnection, eachCurve in blendShapeInputCurves.items():
                print "continue"
                if '|' in eachCurve:
                    next_item = eachCurve.split('|')[1]
                else:
                    next_item=pm.ls(eachCurve, an=1)[0] 
                for eachCV in pm.PyNode(next_item).cv:
                    findName=eachCV.split('.cv')[1]
                    builtAttribute=blendConnection+findName
                    if eachCV.index() == eachCVInCaptureRange:
                        makeDict={builtAttribute:targetWeightValue}
                        setAttrDict.update(makeDict)
            for key, value in setAttrDict.items():
                print key+" setting at "+ str(value)
                cmds.setAttr(key, value)



    def blendWeightExecutionCallup_anim(self, getCVrange, weightList, blendShapeInputuCrves, getSel):
        '''>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..
        cv weight name in blendshape template: cmds.select('blendShape1.inputTarget[1].inputTargetGroup[0].targetWeights[4]')
        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'''
        if len(blendShapeInputuCrves)>1:
            self.add_anim(getCVrange, weightList, blendShapeInputuCrves, getSel)
        else:
            self.first_anim(getCVrange, weightList, blendShapeInputuCrves, getSel)
        
    def add_anim(self, getCVrange, weightList, blendShapeInputCurves, getSel):
        grab_branch=[]
        for each in blendShapeInputCurves:
            if "_targetWeights" in each:
                grab_branch.append(each)
        component=sorted(grab_branch)
        getcurrent=cmds.currentTime(q=1)
        for key, value in map(None, component, weightList):
            complete=key.split('targetWeights')[:-1]
            key='targetWeights'.join(complete)            
            cmds.setKeyframe( key, t=getcurrent, v=value )  

    def first_anim(self, getCVrange, weightList, blendShapeInputCurves, getSel):
        '''>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..
        cv weight name in blendshape template: cmds.select('blendShape1.inputTarget[1].inputTargetGroup[0].targetWeights[4]')
        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'''
        setAttrDict={}
        for eachCVInCaptureRange, targetWeightValue in map(None, getCVrange, weightList):
            for blendConnection, eachCurve in blendShapeInputCurves.items():
                next_item=pm.ls(eachCurve)[0]
                if next_item in getSel:
                    for eachCV in pm.PyNode(next_item).cv:
                        findName=eachCV.split('.cv')[1]
                        builtAttribute=blendConnection+findName
                        if eachCV.index() == eachCVInCaptureRange:
                            makeDict={builtAttribute:targetWeightValue}
                            setAttrDict.update(makeDict)
        getcurrent=cmds.currentTime(q=1)
        for key, value in setAttrDict.items():
            cmds.setAttr(key, value)
            cmds.setKeyframe( key, t=getcurrent, at=key, v=value ) 
