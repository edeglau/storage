import sys, os
filepath= os.getcwd()
sys.path.append(str(filepath))

scriptPath="//usr//people//elise-d//workspace//techAnimTools//personal//elise-d//rigModules"
sys.path.append(str(scriptPath))

getToolArrayPath=str(scriptPath)+"/Tools.py"
exec(open(getToolArrayPath))
toolClass=ToolFunctions()


getBasePath=str(scriptPath)+"/baseFunctions_maya.py"
exec(open(getBasePath))
getBaseClass=BaseClass()



import stretchIK
reload (stretchIK)
getIKClass=stretchIK.stretchIKClass()

'''MG rigging modules'''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons Attribution 4.0 International 4.0 (CC BY 4.0)'
# 'This work is licensed under a Creative Commons Attribution-ShareAlike 3.0 Australia (CC BY-SA 3.0 AU)'
'http://creativecommons.org/licenses/by-sa/3.0/au/'



import maya.cmds as cmds
import maya.mel
class Finalling(object):

    def __init__(self, winName="Controller"):
        self.winTitle = "Controller"
        self.winName = winName

    def create_controller_window(self, winName="Controller"):
        global colMenu
        if cmds.window(self.winName, exists=True):
                cmds.deleteUI(self.winName)

        self.window = cmds.window(self.winName, title=self.winTitle, tbm=1, w=150, h=100 )

        cmds.menuBarLayout(h=30)
        cmds.rowColumnLayout  (' selectArrayRow ', nr=1, w=150)

        cmds.frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')


        getCtrlType=["cluster", "circle"]        
        cmds.rowLayout  (' rMainRow ', w=300, numberOfColumns=6, p='selectArrayRow')
        cmds.columnLayout ('selectArrayColumn', parent = 'rMainRow')
        cmds.setParent ('selectArrayColumn')
        cmds.separator(h=10, p='selectArrayColumn')
        cmds.gridLayout('listBuildButtonLayout', p='selectArrayColumn', numberOfColumns=1, cellWidthHeight=(150, 20))
#         colMenu=cmds.optionMenu( label='ControllerType')
#         for each in getCtrlType:
#             cmds.menuItem( label=each)            
        cmds.button (label='make cluster control', p='listBuildButtonLayout', command = self.make_cluster_ctrl)
        cmds.button (label='make circle control', p='listBuildButtonLayout', command = self.make_circle_ctrl)
        cmds.button (label='make locator control', p='listBuildButtonLayout', command = self.make_loc_ctrl)
        cmds.showWindow(self.window)    
        
    def _makeCtrl(self, arg=None): 
        queryType=cmds.optionMenu(colMenu, q=1, v=1)                    
        if queryType==1:
            print "Cluster"
            self.make_cluster_ctrl(getName, position, rotation)         
        elif queryType==2:
            self.make_circle_ctrl(each, getName, position, rotation)       

    def make_cluster_ctrl(self, arg=None):
        try:
            selObj=cmds.ls(sl=1, fl=1)
        except:
            print "must select a vert"
        for each in selObj:
            try:
                getObjName=each.split(":")[1]
            except:
                getObjName=each
            try:
                getName=getObjName.split(".")
                secondName=getName[1].replace("[", "_")
                secondName=secondName.replace("]", "")
                getName=getName[0]+secondName
            except:
                print "must select a vert"
            position, rotation=getBaseClass.locationXForm(each)
            try:
                getSkinCluster=cmds.skinCluster(each, q=1, dt=1)
                if getSkinCluster:
                    for item in getSkinCluster:
                        if "GroupId" in item:
                            skinID=[eachDefObj for eachDefObj in cmds.listConnections(item, s=1) if cmds.nodeType(eachDefObj)=="skinCluster"][0]        
                    getBaseClass.buildJoint(getName, position, rotation)
#                     cmds.skinCluster(skinID, e=1, ai=getName+"_jnt", lw=1, wt=0) 
                    name=getName+"_Ctrl"
                    grpname=getName+"_grp"                
                    self.cluster_shape(each, name, grpname, position, rotation)
                    cmds.parentConstraint(name, getName+"_jnt", mo=1 )  
                else:
                    pass               
            except:
                getNewName=getName[0]+'0001'
                getBaseClass.buildJoint(getNewName, position, rotation)
                try:
                    cmds.skinCluster(each, thisIsAVariableName+"_jnt", tsb=1) 
#                     cmds.skinCluster(skinID, e=1, ai=getNewName+"_jnt", lw=1, wt=0)                    
                except:
#                     cmds.skinCluster(each, getNewName+"_jnt", tsb=1) 
                    print "object already belongs to a skin cluster. add to skin cluster"
                    pass                    
                name=getName[0]+"_Ctrl"
                grpname=getName[0]+"_grp"
                self.cluster_shape(each, name, grpname, position, rotation)
                cmds.parentConstraint(name, getNewName+"_jnt", mo=1 )


    def cluster_shape(self,each, name, grpname, position, rotation):
            colour=28
            num0, num1, num2, num3, colour=1, .4, .9, .7, 22
            getBaseClass.CCCircle(name, grpname, num0, num1, num2, num3, position, rotation, colour) 
             
    def circle_shape(self, each, name, grpname, position, rotation):
        nrx, nry, nrz=getBaseClass.fetchDirection()
        size=5 
        colour=22
        getBaseClass.buildCtrl(each, name, grpname, position, rotation, size, colour, nrx, nry, nrz)       
        
#     def make_cluster_ctrlV1(self, arg=None):
#         try:
#             selObj=cmds.ls(sl=1, fl=1)
#         except:
#             print "must select a vert"
#         for each in selObj:
#             try:
#                 getObjName=each.split(":")[1]
#             except:
#                 getObjName=each
#             try:
#                 getName=getObjName.split(".")
#                 secondName=getName[1].replace("[", "_")
#                 secondName=secondName.replace("]", "")
#                 getName=getName[0]+secondName
#             except:
#                 print "must select a vert"
#             position, rotation=getBaseClass.locationXForm(each)
#             getSkinCluster=cmds.skinCluster(each, q=1, dt=1)
#             for item in getSkinCluster:
#                 if "GroupId" in item:
#                     skinID=[eachDefObj for eachDefObj in cmds.listConnections(item, s=1) if cmds.nodeType(eachDefObj)=="skinCluster"][0]        
#             getBaseClass.buildJoint(getName, position, rotation)
# #             cmds.joint(n=getName+"_jnt", p=position) 
#             cmds.skinCluster(skinID, e=1, ai=getName+"_jnt", lw=1, wt=0) 
#             colour=28          
#             name=getName+"_Ctrl"
#             grpname=getName+"_grp"
#             num0, num1, num2, num3, colour=1, .4, .9, .7, 22
#             getBaseClass.CCCircle(name, grpname, num0, num1, num2, num3, position, rotation, colour)      
#             cmds.parentConstraint(name, getName+"_jnt", mo=1 )      
#             
    def make_circle_ctrl(self, arg=None):
        try:
            selObj=cmds.ls(sl=1, fl=1)
        except:
            print "must select a vert"
        for each in selObj:
            try:
                getObjName=each.split(":")[1]
            except:
                getObjName=each
            try:
                getName=getObjName.split(".")
                secondName=getName[1].replace("[", "_")
                secondName=secondName.replace("]", "")
                getName=getName[0]+secondName
            except:
                print "must select a vert"
            position, rotation=getBaseClass.locationXForm(each)
            try:
                getSkinCluster=cmds.skinCluster(each, q=1, dt=1)
                if getSkinCluster:
                    for item in getSkinCluster:
                        if "GroupId" in item:
                            skinID=[eachDefObj for eachDefObj in cmds.listConnections(item, s=1) if cmds.nodeType(eachDefObj)=="skinCluster"][0]        
                    getBaseClass.buildJoint(getName, position, rotation)
#                     cmds.skinCluster(skinID, e=1, ai=getName+"_jnt", lw=1, wt=0) 
                    name=getName+"_Ctrl"
                    grpname=getName+"_grp"                
                    self.circle_shape(each, name, grpname, position, rotation)
                    cmds.parentConstraint(name, getName+"_jnt", mo=1 )  
                else:
                    pass               
            except:
                thisIsAVariableName=getName[0]+'0001'
                getBaseClass.buildJoint(thisIsAVariableName, position, rotation)
                try:
                    cmds.skinCluster(each, thisIsAVariableName+"_jnt", tsb=1) 
#                     cmds.skinCluster(skinID, e=1, ai=thisIsAVariableName+"_jnt", lw=1, wt=0)                    
                except:
#                     cmds.skinCluster(each, thisIsAVariableName+"_jnt", tsb=1) 
                    print "object already belongs to a skin cluster. add to skin cluster"
                    pass
                name=getName[0]+"_Ctrl"
                grpname=getName[0]+"_grp"
                self.circle_shape(each, name, grpname, position, rotation)
                cmds.parentConstraint(name, thisIsAVariableName+"_jnt", mo=1 ) 

    
    def make_loc_ctrl(self, arg=None):
        try:
            selObj=cmds.ls(sl=1, fl=1)
        except:
            print "must select a vert"
        for each in selObj:
            try:
                getObjName=each.split(":")[1]
            except:
                getObjName=each
            try:
                getName=getObjName.split(".")
                secondName=getName[1].replace("[", "_")
                secondName=secondName.replace("]", "")
                getName=getName[0]+secondName
            except:
                print "must select a vert"
            position, rotation=getBaseClass.locationXForm(each)
            try:
                getSkinCluster=cmds.skinCluster(each, q=1, dt=1)
                if getSkinCluster:
                    for item in getSkinCluster:
                        if "GroupId" in item:
                            skinID=[eachDefObj for eachDefObj in cmds.listConnections(item, s=1) if cmds.nodeType(eachDefObj)=="skinCluster"][0]        
                    getBaseClass.buildJoint(getName, position, rotation)
#                     cmds.skinCluster(skinID, e=1, ai=getName+"_jnt", lw=1, wt=0) 
                    name=getName+"_Ctrl"
                    grpname=getName+"_grp"                
                    self.circle_shape(each, name, grpname, position, rotation)
                    cmds.parentConstraint(name, getName+"_jnt", mo=1 )  
                else:
                    pass               
            except:
                thisIsAVariableName=getName[0]+'0001'
                getBaseClass.buildJoint(thisIsAVariableName, position, rotation)
                try:
                    cmds.skinCluster(each, thisIsAVariableName+"_jnt", tsb=1) 
#                     cmds.skinCluster(skinID, e=1, ai=thisIsAVariableName+"_jnt", lw=1, wt=0)                    
                except:
#                     cmds.skinCluster(each, thisIsAVariableName+"_jnt", tsb=1) 
                    print "object already belongs to a skin cluster. add to skin cluster"
                    pass
                name=getName[0]+"_Ctrl"
                grpname=getName[0]+"_grp"
                colour=13
                getBaseClass.buildLoc(name, grpname, position, rotation, colour)
                # self.circle_shape(each, name, grpname, position, rotation)
                cmds.parentConstraint(name, thisIsAVariableName+"_jnt", mo=1 ) 

inst = Finalling()
inst.create_controller_window()        
