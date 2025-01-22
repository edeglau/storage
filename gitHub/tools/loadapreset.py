import ast, os, sys
import maya.cmds as cmds




notAttr=["isHierarchicalConnection", "solverDisplay", "isHierarchicalNode", "publishedNodeInfo", "fieldScale_Position", "fieldScale", "fieldScale.fieldScale_Position"]         

class load_preset():
    def __init__(self):
        
        printFolder = '/job/gen/dev/character/Krypto/work/edeglau/maya/data/presets/'
        ##load global flex
        selObj = [
        "sim_primary_default_:body_:flex_FLX",
        ]
        grabFileName = 'flex_FLX.txt'
        setPath = os.path.join(printFolder, grabFileName )   
        if os.path.exists(setPath):
            self.preset_apply(selObj, setPath)
        else:
            print (setPath+"does not exist")

        ##load local flex
        selObj = [
        "sim_primary_default_:body_:render_anatomy_default_topology_:*_L_extensorDigitorumLongusB_GE?",
        ]
        grabFileName = 'muscles_GRP.txt'
        setPath = os.path.join(printFolder, grabFileName )    
        if os.path.exists(setPath):
            self.preset_apply(selObj, setPath)
        else:
            print (setPath+"does not exist")    def preset_apply(self, selObj, setPath):
        for each in selObj:
            attribute_container=[]
            getListedAttr=[(attrib) for attrib in cmds.listAttr(each, k=1, s=1, iu=1, u=1, lf=1, m=0) for item in notAttr if item not in attrib]             
            List = open(setPath).readlines()
            for aline in List:
                if ">>" in aline:
                    getObj=aline.split('>>')[0]
                    getExistantInfo=aline.split('>>')[1]
                    if getExistantInfo!="\n":
                        findAtt=getExistantInfo.split("<")
                        for eachInfo in findAtt:
                            getAnimDicts=eachInfo.split(";")
                            for eachctrl in range(len(getAnimDicts) - 1):
                                current_item, next_item = getAnimDicts[eachctrl], getAnimDicts[eachctrl + 1]
                                gethis=ast.literal_eval(next_item)
                                try:
                                    if len(gethis)<2:
                                        for key, value in gethis.items():
                                            for listeditem in getListedAttr:
                                                if current_item==listeditem:
                                                    cmds.setAttr(cmds.ls(getObj)[0]+'.'+current_item, value)                                                 
                                    else:
                                         for key, value in gethis.items():
                                            for listeditem in getListedAttr:
                                                if current_item==listeditem:                                               
                                                    cmds.setKeyframe( cmds.ls(getObj)[0], t=key, at=current_item, v=value )  
                                except:
                                    pass                                              
                    else:
                        pass
load_preset()
