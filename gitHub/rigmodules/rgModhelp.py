import maya.cmds as cmds
from pymel.core import *

'''MG rigging modules'''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons Attribution 4.0 International 4.0 (CC BY 4.0)'
'http://creativecommons.org/licenses/by/4.0/'
# 'This work is licensed under a Creative Commons Attribution-ShareAlike 3.0 Australia (CC BY-SA 3.0 AU)'
# 'http://creativecommons.org/licenses/by-sa/3.0/au/'

# TopicDict={"File/Session":0, "MiniRigs":10, "Tools":30,"Controllers":40,"Attributes":50,"Modelling":80, "External Folders":70}
# TopicDict=["Attributes","Controllers", "External Folders","File/Session","MiniRigs", "Modelling", "Tools"]
TopicDict=["*File/Session", 
"*MiniRigs", 
"*Tools",
"*Controllers",
"*Attributes",
"*Modelling", 
"*External Folders"]

SubTopics=["Guides Tool", 
"Insert Grp/Clst/Jnt", 
"CurveRig", "ChainRig", 
"Multi Rivet", 
"Multi Point", 
"Connect to curve", 
"Select array tool", 
"Renamer tool", 
"Edit sets", 
"Cull CVs", 
"Plot Vertrex",
"Multi Functions",
"Hidden Grp",
"Copy To Grps",
"Match Matrix",
"Reset Selected",
"Wipe Anim From Obj",
"Shade Network Sel",
"Duplicate Move",
"Controller",
"Shapes Tool",
"Colours",
"Combine Shapes",
"Fetch Attribute",
"Fast Float",
"Fast Attr Alias",
"Copy Single Attr",
"Set Range Multi Attr",
"Copy Anim/Att",
"Transfer Mass Attr",
"Blend Groups",
"Reshape To Edge",
"Poly Check",
"Build Curve",
"Clean Model",
"Mirror Blend",
"Save Attr/Anim",
"Load Attr/Anim",
"Change Multi File Contents",
"Change Multi File Names",
"Export Multiple Obj",
"Open Image Gimp",
"Open Work Folder"
]

SubTopics=sorted(SubTopics)
TopicDict=TopicDict+SubTopics

class helpClass(object):
    '''--------------------------------------------------------------------------------------------------------------------------------------
    Interface Layout
    --------------------------------------------------------------------------------------------------------------------------------------'''          
    def __init__(self, winName="help"):
    # def helpPage(self, arg=None):
        winName = "Description"
        winTitle = winName
        if cmds.window(winName, exists=True):
                deleteUI(winName)
        window = cmds.window(winName, title=winTitle, tbm=1, w=700, h=800 )
        menuBarLayout(h=30)
        rowColumnLayout  (' selectArrayRow ', nr=1, w=700)
        frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        rowLayout  (' rMainRow ', w=700, numberOfColumns=6, p='selectArrayRow')
        columnLayout ('selectArrayColumn', parent = 'rMainRow')
        setParent ('selectArrayColumn')
        cmds.gridLayout('findlayout', p='selectArrayColumn', numberOfColumns=4, cellWidthHeight=(300, 25 ))
        self.colMenu=cmds.optionMenu( label='Topics', w=200, cc=lambda *args:self._find_in_list())
        for key in TopicDict:
            cmds.menuItem( label=key)        
        cmds.gridLayout('txvaluemeter', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(700, 800))     
        self.list=cmds.scrollLayout( ebg=1, pe=1, bgc=[0.11, 0.15, 0.15],w=700)
        self.info=cmds.text(al="left", label=
'''Button interface: what the buttons do

File/session

"Outliner win" (script) brings up outliner as I'm always closing it

"Clean interface"(script closes all superfluous windows (hypershade, hypergraph) to clean up interface

"Revert" (launches window)rolls back file to last saved

"Fix Playblast" (script)resets the playblast if in case it breaks in scene

"Undos back on" (script)resets the undos to be on. Maya has a bug where some plugins will turn this off




Minirigs


Guides tool (launches another toolkit window) launches another interface to place guides;
    lays out some sphere guides (this will layout the rig skel+controllers for an autorig
    system)

        *More information can be found in "help" menu on this tool's interface

"Insert grp/clst/jnt"(dropdown) inserts selections under their own group whilst zeroing out 
    (handy for sandwiching a control in a rig), or adds a cluster or joint skin to selection
        * Step 1: Select items
        * Step 2: execute script will add object to a group, cluster or joint

        "GROUP"  will place group to object's current transform, parent object under group,
            and will put the group within the same heirarchy structure as object was
            previously creating a buffer in transform(common in rigging to zero out a
            controller especially if a shift needed to happen)
        "CLUSTER" will add the object to a cluster and place cluster at object's current
            transform
        "JOINT" will skin object to joint and place joint at object's transform

"Curve Rig" - (launches window)simple curve rig, no FK or IK.

        *More information can be found in "help" menu on this tool's interface

"ChainRig" - (launches window) FK and IK chain(use the tail guide layout) if you've chosen a 
    particular axis for your guides, use the same axis for your controls.(the spheres have a 
    colored shape to help guide the dimensions they are building in. (this is still in 
    development. use at own risk)

        *More information can be found in "help" menu on this tool's interface

"Multi Rivet" (script)creates multiple rivets on selection of points
        * Step 1: Select vertices
        * Step 2: run script will place a rivet at each point

"Multi Point" (script)creates mulitple Point on Poly constraints on selection of points
        * Step 1: Select vertices
        * Step 2: run script will place a locator at each point with a point on poly
            constraint

"Connect to curve" - (script)add objects to a curve. 
        * Step 1: Select curve first 
        * Step 2: then objects to follow
        * Step 3: run script



Tools


"Select array tool" - (launches window)a tool for finding nodes and making a 
    temp work area of selections of verts. (find things in full scenes by name
    and node type)

        *More information can be found in "help" menu on this tool's interface

"Renamer tool" - (launches window)a basic renamer. has the ability to strip number, shift 
    name parts, remove underscores, shift numbers, remove isolated numbers, replace names 
    in bulk

        *More information can be found in "help" menu on this tool's interface

"Edit sets" - (launches window)this tool allows for adding and subtracting of verts to a 
    blenshape or a dynamic constraint set or a regular objectSet

        *More information can be found in "help" menu on this tool's interface

"Cull CV" (launches window)removes every first or every other cv in a selection(you can use 
    this to remove the (1) cv will remove the second in chain(as the vine tool fails if 
    second and first cv are too close together). also has a rebuild function to rebuild a 
    mass of curves using mathematic array and matching now

        *More information can be found in "help" menu on this tool's interface

"Plot vertex" - (launches window)if you're familiar with rivets, it's similar except that 
    there is no dependency set up. it bakes a locator in space for the animation duration 
    to the face or vertex of your choice
        
        *More information can be found in "help" menu on this tool's interface

"MultiFunctions" (launches window)does a mass constraint or extrude. Constrains all items 
    to the first selected item or extrudes first selected item as a tube along several 
    curves

        *More information can be found in "help" menu on this tool's interface     

"Hidden Grp" (launches window) an interface to toggle visibility on grped heirarchy
        
        *More information can be found in "help" menu on this tool's interface


"Copy To Grps" (script) Select object and group nodes group and it will create a copied 
    object into the groups
        * Step 1: select object
        * Step 2: select multiple grp transforms
        * Step 3: run script will duplicate copies of this object into groups    

"Matchmatrix" (script)moves one object to another based on the xform command
        * Step 1: select object
        * Step 2: select an object to follow it to
        * Step 3: run script will match first object to the second object's matrix  

"Reset selected" (script)will res et object to zeroed out transform. won't remove animation
        * Step 1: select object
        * Step 2: run script will zero out transform

"Wipe anim from obj" (script)will wipe animation curves and reset transforms to zero
        * Step 1: select object
        * Step 2: run script will zero out transform and remove animation curves

"ShadeNetworkSel" (script)this brings up the hypershade and networks the shader(s)for the 
    selected object(s)
        * Step 1: select object(s)
        * Step 2: run script open hypershade and map networks shader of selected objects

"Duplicate move" (script)duplicates the first selected item to the subsequent selected items 
    positions and heirarchy (used this on a string tent in which I selected all cvs on a 
    curve and then a cube and duplicated along curve - warning: does not perform variations)
        * Step 1: select object
        * Step 2: select multiple objects you want to copy first item to
        * Step 3: run script will duplicate object to positions of proceeding objects


Controllers:

"Controller" (launches window)some premade shapes for controllers that will be created at
    selections. can also choose to create multiple locators and joints. Will add a constraint
    with selection

        *More information can be found in "help" menu on this tool's interface

"Shapes Tool" (launches window)some premade shapes that will be created at selections. can
    also choose to create multiple locators and joints. These are not constrained with the
    selection so it' only creates a shape and nothing more (unlike "Controller" which will
    add a constraint with selection")
    
        *More information can be found in "help" menu on this tool's interface

"Colours"  (launches window)colour multiple objects(controllers) without having to go through
    attribute editor

        *More information can be found in "help" menu on this tool's interface

"Combine shapes" (script)this merges shapes together to make one object transform(custom
    controller)
        * Step 1: select curve object(s)
        * Step 2: launching script will combine the shapes under one transform


Attributes:


"Fetch Attribute" (launches window)an interface to query a selected items attributes that
    you can hunt by name portion or values. You can also change attribute value through this
    window if number values apply(handy for heavy attribute lists like on skinDef)

        *More information can be found in "help" menu on this tool's interface

"Fast float" (launches window)creates a 0-1 fast float. handy for making an attribute to hook
    up blends, constraints etc.
        * Step 1: select object(s)
        * Step 2: launch window
        * Step 3: set name of attribute
        * Step 4: press continue will create a float attribute on all selected objects

"Fast attr alias" (launches window)creates a custom attribute on the second selected object
    to hook up the attribute of the first object to.(handy to link an attribute to a
    controller)

        *More information can be found in "help" menu on this tool's interface

"Copy single Attribute" (launches window) copies one attribute value to another selected
    object's attribute

        *More information can be found in "help" menu on this tool's interface

"Set Range Multi Attr" (launches window)This has a window that will call up a list of
    attributes. you can then set a range in which a group of items attributes can be changed
    to that range. It has random option that will set a random value within the range. and
    relative so that if you want to transform in local, it will only range within a local
    area(randomizing curve CV position for example) or make a range of attributes across
    multiple items for more random feel(ive been using this to randomize cvs on curves)
        *More information can be found in "help" menu on this tool's interface

"copyAnim/Att" (script)copies the animation curves and attribute values from one object to
    another
        * Step 1: select two objects
        * Step 2: launch script will duplicate the animation curves onto the second object

"transfer mass attribute" (script)transfers all attribute values(but not animation curves)
    from one object to another.
        * Step 1: select two objects
        * Step 2: launch script will set all attributes on the second object to first values


Modelling


"Blend Groups" (dropdown)this creates a blend between group heirarchies based on matching
    names within the group or selection
        "GrpToGrp" - popup    
            * Step 1: select two GRPs
            * Step 2: launch script will blend objects from first to second based on name
                and location in heirarchy if matching
        "GrpToGrp" - popup    
            * Step 1: sequence a selection matching first objects to second
            * Step 2: launch script will zigzag blend from first to second:
                EG: object one, two, three, four
                    object one will blend to two
                    object three will blend to four
                    and so on..
        "GrpSearchAndBlend" - popup    
            * Step 1: select two GRPs
            * Step 2: launch script will blend objects within first to second based on name
                (it doesn't care about heirarchy, just needs to have matching name parts and
                topology)

"Reshape to Edge" (dropdown)Select a continuous edge on one object and a continuous edge on a
    target object. This will bend the edge of the first object to the second(veins on leaves
    or quills on feathers). Reshape to edge: better for cylindrical shapes to curve along a 
    surface edge. Reshape to shape: better for flat planes against another surface(plane
    should have some bias on which way it leans or it might twist - uses shrink wrap to place
    on surface)
        "Reshape To Edge" - popup    
            * Step 1: select a continuous edge on one object and a continuous edge on another
            * Step 2: launch script make first object line up along second object contoring
                to edge
        "Reshape To Shape" - popup    
            * Step 1: select a continuous edge on one object and a continuous edge on another
            * Step 2: launch script make first object line up along second object contoring
                to edge and also match the facing angle(plane on plane)

"PolyCheck" (launches window)checks poles and ngons on component selections
    
        *More information can be found in "help" menu on this tool's interface

"Build Curve" (script)use to build a curve based on selection. Best to use guide layouts on
    selected vertice and then use this to create curve
        * Step 1: select multiple objects or vertices
        * Step 2: launch script will draw a cv curve based on selection

"Clean model" (script)wipes history, resets transforms and averages normals on a
    model(modelling)
        "CLEAN+HISTORY" - button
            * Step 1: Select object
            * Step 2: pressing this button cleans history, zeros out object and
                cleans shape name, removes custom attr, averages normals(hard edges)
        "CLEAN" - button
            * Step 1: Select object
            * Step 2: pressing this button zeros out object and
                cleans shape name, removes custom attr, averages normals(hard edges)

"Mirror blend" (script)for mirroring face, arm, leg blends(right blink//left blink, arm
    muscles, etc)(rigging)
        * Step 1: select blend shape(EG: R eyebrow down)
        * Step 2: select base shape(neutral pose)
        * Step 3: running script will create a mirrored blend shape and blend it into
            the neutral pose(check for reflect blendshape name on neutral shape)


External folders


"Save Anim/Attr" (launches window)a home made scripted save anim keys and attribute values
    into external file(s)(works on a heirarchy). Put full file path with preferred name of
    object in text field("/usr/people/<user>/joint4"). save button saves out file. Can add
    more to save from add selected at top. Will save out a txt file.

        *More information can be found in "help" menu on this tool's interface

"Load Anim/Attr" (launches window)Opens anim keys and attribute values from external file(s)
    (works on a heirarchy). Put full path with no of object in the text field("/usr/people/
    <user>/"). Press refresh and it will repopulate the drop down for available .txt files;
    stick to the name of your object to reload anim.

        *More information can be found in "help" menu on this tool's interface

"Change multi file contents" (launches window)home made change contents of all files in a
    specific folder(eg: names of a joint in an xml skin export)

        *More information can be found in "help" menu on this tool's interface

"Change multi file names" (launches window)home made change the names of all files in a
    specific folder(eg: render images)

        *More information can be found in "help" menu on this tool's interface

"Export multiple obj" export multiple selections into separate .obj files.
    ("/usr/people/<user>/")
        * Step 1: select multiple polygonal objects
        * Step 2: set path in feild
        * Step 3: press "Save" will save polygonal objects into seperate object files

"Open image in gimp" (script runs on selected texture node)Will load selected image in a
    selected texture node in gimp
        * Step 1: select texture node
        * Step 2: launching script will open image in gimp

"Open work folder" (launches window)opens current workfolder for current scene. if untitled,
    will open top hierarchy.



''')


        showWindow(window)

    def _find_in_list(self, arg=None):
        '''----------------------------------------------------------------------------------
        This locates the object by name in list
        ----------------------------------------------------------------------------------'''          
        queryColor=cmds.optionMenu(self.colMenu, q=1, sl=1)    
        getSel=cmds.ls(sl=1)
        if queryColor==1:#Files
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
        elif queryColor==2:#Minirigs
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 180))
        elif queryColor==3:#Tools
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 850))
        elif queryColor==4:#Controllers
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 1845))
        elif queryColor==5:#Attributes
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 2170))
        elif queryColor==6:#Modelling
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 2755))
        elif queryColor==7:#External
            cmds.scrollLayout(self.list, e=1, sbp=("down", 8000))
        elif queryColor==8:#Blend grps
            cmds.scrollLayout(self.list, e=1, sbp=("down", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("up", 600))
        elif queryColor==9:#Build Curve
            cmds.scrollLayout(self.list, e=1, sbp=("down", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("up", 90))
        elif queryColor==10:#Chain Rig
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 550))
        elif queryColor==11:#Chang Multi File Contents
            cmds.scrollLayout(self.list, e=1, sbp=("down", 8000))
        elif queryColor==12:#Chang Multi File
            cmds.scrollLayout(self.list, e=1, sbp=("down", 8000))
        elif queryColor==13:#Clean Model
            cmds.scrollLayout(self.list, e=1, sbp=("down", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("up", 50))
        elif queryColor==14:#colours
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 2030))
        elif queryColor==15:#Combine Shapes
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 2100))
        elif queryColor==16:#Connect To Curve
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 755))
        elif queryColor==17:#Controller
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 1870))
        elif queryColor==18:#CopyAnimAttr
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 2630))
        elif queryColor==19:#Copy Single Attr
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 2450))
        elif queryColor==20:#Copy To grps
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 1380))
        elif queryColor==21:#Cull CV
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 1100))            
        elif queryColor==22:#Curve Rig
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 500))
        elif queryColor==23:#Duplicate Move
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 1745))
        elif queryColor==24:#Edit sets
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 1050))
        elif queryColor==25:#Export multi obj
            cmds.scrollLayout(self.list, e=1, sbp=("down", 8000))
        elif queryColor==26:#Fast Attr Alias
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 2350))
        elif queryColor==27:#Fast Attr Alias
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 2250))
        elif queryColor==28:#Fetch Attribute
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 2200))
        elif queryColor==29:#Guides
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 240))
        elif queryColor==30:#Hidden grp
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 1350))
        elif queryColor==31:#Insert grp
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 300))
        elif queryColor==32:#Load Attr/Anim
            cmds.scrollLayout(self.list, e=1, sbp=("down", 8000))
        elif queryColor==33:#Match Matrix
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 1500)) 
        elif queryColor==34:#Mirror Blend
            cmds.scrollLayout(self.list, e=1, sbp=("down", 8000))
        elif queryColor==35:#Multi functions
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 1250))
        elif queryColor==36:#Multi Point
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 700))
        elif queryColor==37:#Multi Rivet
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 650))
        elif queryColor==38:#Open image gimp
            cmds.scrollLayout(self.list, e=1, sbp=("down", 8000))
        elif queryColor==39:#Open work folder
            cmds.scrollLayout(self.list, e=1, sbp=("down", 8000))
        elif queryColor==40:#PlotVertex
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 1200))
        elif queryColor==41:#PolyCheck
            cmds.scrollLayout(self.list, e=1, sbp=("down", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("up", 110))
        elif queryColor==42:#Renamer
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 950))
        elif queryColor==43:#Reset selected
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 1550))
        elif queryColor==44:#Reshape to edge
            cmds.scrollLayout(self.list, e=1, sbp=("down", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("up", 350))
        elif queryColor==45:#save attr/anim
            cmds.scrollLayout(self.list, e=1, sbp=("down", 8000))
        elif queryColor==46:#Select array
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 880))
        elif queryColor==47:#Set Range Multi
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 2530))
        elif queryColor==48:#Shade Network sel
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 1645))
        elif queryColor==49:#Shapes tool
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 1910))     
        elif queryColor==50:#Transfer mass attr
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 2700))
        elif queryColor==51:#Wipe Anim object
            cmds.scrollLayout(self.list, e=1, sbp=("up", 8000))
            cmds.scrollLayout(self.list, e=1, sbp=("down", 1620))
        # cmds.scrollLayout(self.list, e=1, sl=1) 
        # getList=listArray.split(" ")
        # for each in getList:
        #     print each
        # if nameFieldText and listArray:
        #     foundExistantListObj=[(eachObj) for eachObj in getList if nameFieldText in str(eachObj)]
        #     if foundExistantListObj:
        #         cmds.scrollLayout(self.list, e=1, sbp=200) 
        #         # self.deselect_in_list_function()   
        #         # self.select_list_item_function(foundExistantListObj)                  
        #         print 'Objects containing "'+nameFieldText+'" found'
        #     else:
        #         cmds.scrollLayout(self.list, e=1, sl=0)                        
        #         print 'Objects containing "' +nameFieldText+'" not found in this list.'
        # else:
        #     self.selection_field_error()       

    # def deselect_in_list_function(self, arg=None):
    #     '''----------------------------------------------------------------------------------
    #     Common deselect in list function
    #     ----------------------------------------------------------------------------------'''              
    #     cmds.scrollLayout(self.list, e=1, sl=0)
        
    # def select_list_item_function(self, eachSortedObj):
    #     '''----------------------------------------------------------------------------------
    #     Common select in list function
    #     ----------------------------------------------------------------------------------'''          
    #     cmds.scrollLayout(self.list, e=1, sl=1) 

    # def selection_field_error(self):
    #     print "Check that there is a name in the field, spelling and/or if the list has anything in it"            
