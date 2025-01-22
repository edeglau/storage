
    def store_obj_matrix_pt(self, objectSel, fileName):
        '''plots transforms off of an object with constraint to a text file'''
        objectSel=cmds.ls(sl=1)
        if len(objectSel)>0:
            pass
        else:
            print "Select 1 object" 
            return     
        fileName=fileName+'.txt'
        print fileName
        if "Windows" in OSplatform:
            if not os.path.exists(fileName): os.makedirs(fileName)
        if "Linux" in OSplatform:
            inp=open(fileName, 'w+')
        getTopRange=cmds.playbackOptions(q=1, max=1)+1#get framerange of scene to set keys in iteration 
        getLowRange=cmds.playbackOptions(q=1, min=1)-1#get framerange of scene to set keys in iteration 
        getRange=arange(getLowRange,getTopRange, 1 )
        collection_of_valueTX={}
        collection_of_valueTY={}
        collection_of_valueTZ={}
        collection_of_valueRX={}
        collection_of_valueRY={}
        collection_of_valueRZ={}
        for each_obj in objectSel:            
            inp.write('\n'+str(each_obj)+">>")        
            for each_frame in getRange:
                cmds.currentTime(each_frame)            
                transform=cmds.xform(each_obj, q=True, ws=1, t=True)
                rotation=cmds.xform(each_obj, q=True, ws=1, ro=True)
                if len(transform)<4:
                    pass
                else:
                    posBucket=[]
                    posBucket.append(self.median_find(transform[0::3]))
                    posBucket.append(self.median_find(transform[1::3]))
                    posBucket.append(self.median_find(transform[2::3]))
                    transform=posBucket
                # print str(each_frame)+":"+str(transform[0])
                makeDictTX = {each_frame:transform[0]}
                collection_of_valueTX.update(makeDictTX)
                makeDictTY = {each_frame:transform[1]}
                collection_of_valueTY.update(makeDictTY)
                makeDictTZ = {each_frame:transform[2]}
                collection_of_valueTZ.update(makeDictTZ)
                makeDictRX = {each_frame:rotation[0]}
                collection_of_valueRX.update(makeDictRX)
                makeDictRY = {each_frame:rotation[1]}
                collection_of_valueRY.update(makeDictRY)
                makeDictRZ = {each_frame:rotation[2]}
                collection_of_valueRZ.update(makeDictRZ)
                cmds.currentTime(each_frame)
            inp.write("<translateX;")
            inp.write(str(collection_of_valueTX))
            inp.write("<translateY;")
            inp.write(str(collection_of_valueTY))
            inp.write("<translateZ;")
            inp.write(str(collection_of_valueTZ))
            inp.write("<rotateX;")
            inp.write(str(collection_of_valueRX))
            inp.write("<rotateY;")
            inp.write(str(collection_of_valueRY))
            inp.write("<rotateZ;")
            inp.write(str(collection_of_valueRZ))
        inp.close()
