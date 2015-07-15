import maya.cmds as cmds
from pymel.core import *

'''MG rigging modules'''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons Attribution 4.0 International 4.0 (CC BY 4.0)'
'http://creativecommons.org/licenses/by/4.0/'
# 'This work is licensed under a Creative Commons Attribution-ShareAlike 3.0 Australia (CC BY-SA 3.0 AU)'
# 'http://creativecommons.org/licenses/by-sa/3.0/au/'



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
        cmds.gridLayout('txvaluemeter', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(700, 800)) 
        self.list=cmds.scrollField( editable=False, wordWrap=True, w=700, text=
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

"Tail":(launches window)this lays out a line of guides in a range that you set( eg: -15 /15 
    will layout a chosen number in a range within this value in a direction)
        * Step 1: set axis on direction to layout guides
        * Step 2: set name of guides(the autorig uses this name to detect the correct
            guide string to build from so you can build with multiple in same scene 
            with unique names)
        * Step 3: set amount
        * Step 4: set size
        * Step 5: set range: this will determine the length and position to layout the
            guides in a straight line

"Build Guides" (lanches a window to name)will build a guide per selected item(objects, verts 
    and cvs)
        * Step 1: Select a series of objects or components(verts) and set a name
        * Step 1(alternative): Select nothing and create with a set name. This will
            place guide at origin

"Clean guides" (script)clears all guides in your scene(generally not needed after a rig is 
    built but dont use if more than one rig with more than one guide set. will wipe all 
    '_guide' from scene


"Insert grp/clst/jnt"(dropdown) inserts selections under their own group whilst zeroing out 
    (handy for sandwiching a control in a rig), or adds a cluster or joint skin to selection


"Curve Rig" - (launches window)simple curve rig, no FK or IK.

"ChainRig" - (launches window) FK and IK chain(use the tail guide layout) if you've chosen a 
    particular axis for your guides, use the same axis for your controls.(the spheres have a 
    colored shape to help guide the dimensions they are building in. (this is still in 
    development. use at own risk)

"Multi Rivet" (script)creates multiple rivets on selection of points

"Multi Point" (script)creates mulitple Point on Poly constraints on selection of points

"Connect to curve" - (script)add objects to a curve. 
        * Step 1: Select curve first 
        * Step 2: then objects to follow
        * Step 3: run script



Tools


"Select array tool" - (launches window)a tool i built up for just finding nodes and making a 
    temp work area of selections of verts. (constantly using this to find things in full 
    scenes by name and node type)

"Renamer tool" - (launches window)a basic renamer. has the ability to strip number, shift 
    name parts, remove underscores, shift numbers, remove isolated numbers, replace names 
    in bulk

"Edit sets" - (launches window)this tool allows for adding and subtracting of verts to a 
    blenshape or a dynamic constraint set or a regular objectSet
        * Step 1: Set the type of set from the drop down menu
        * Step 2: Select objects/verts
        * Step 3: add or remove  

"Cull CV" (launches window)removes every first or every other cv in a selection(you can use 
    this to remove the (1) cv will remove the second in chain(as the vine tool fails if 
    second and first cv are too close together). also has a rebuild function to rebuild a 
    mass of curves using mathematic array and matching now
        * Step 1: Select curve(s)
        * Step 2: determine if you want to rebuild by number or remove a CV
        * Step 3: if rebuilding, select math type from dropdown menu
        * Step 4: Press either ok button depending on which one you decide

"Plot vertex" - (launches window)if you're familiar with rivets, it's similar except that 
    there is no dependency set up. it bakes a locator in space for the animation duration 
    to the face or vertex of your choice
        "PLOT"
            * Step 1: Select a vertex
            * Step 2: press "plot" - locator will follow vertex anim
        "PLOT EACH"
            * Step 1: Select multiple vertex
            * Step 2: press "plot each" - locator will follow each vertex anim
        "ONION"
            * Step 1: Select a vertex
            * Step 2: press "onion" - locators will be created at each frame
        "LOCATE"
            * Step 1: Select a vertex or a group of vertices
            * Step 2: press "locate" - a locator will place in center of selection

"MultiFunctions" (launches window)does a mass constraint or extrude. Constrains all items 
    to the first selected item or extrudes first selected item as a tube along several 
    curves
        * Step 1: select object to constrain items to(or run on path)
        * Step 2: select multiple objects to constrain (or run a path on)
        * Step 3: select function from dropdown menu
        * Step 4: if using paths, set length and wide spans
        * Step 5: Press go      

"Hidden Grp" (launches window) an interface to toggle visibility on grped heirarchy
        "EYEDROPPER NAME" - button
            * Step 1: Select object with a desired name
            * Step 2: pressing this button populates the name field with selected
        "TOGGLE NAME" - button
            * Step 1: fill in feild('*' is legal wildcard char)
            * Step 2: press"Toggle name"
        "TOGGLE EXCLUDE PEERS" - button
            * Step 1: select object under a grouped heirarchy
            * Step 2: press this button toggles visibility of all of it's peers
        "TOGGLE CHILDREN" - button
            * Step 1: Select parent GRP
            * Step 2: pressing this button toggles visibilty of first level
                children
        "TOGGLE LEAF CHILDREN" - button
            * Step 1: Select parent GRP
            * Step 2: pressing this button toggles visibilty of children inside of
                tree
        "CHILDREN OFF"
            * Step 1: Select parent GRP
            * Step 2: pressing this button deactivates visibilty of first level
                children
        "CHILDREN ON"
            * Step 1: Select parent GRP
            * Step 2: pressing this button activates visibilty of first level
                children


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
        * Step 1: select object(s)
        * Step 2: launch window
        * Step 3: set size
        * Step 4: select shape type of controller from drop down menu
        * Step 5: press "go" will create a controller in which selected objects are
            constrained to

"Shapes Tool" (launches window)some premade shapes that will be created at selections. can
    also choose to create multiple locators and joints. These are not constrained with the
    selection so it' only creates a shape and nothing more (unlike "Controller" which will
    add a constraint with selection")
        * Step 1: select object(s)
        * Step 2: launch window
        * Step 3: set size
        * Step 4: select shape type of controller from drop down menu
        * Step 5: press "go" will create a controller shape at position of selected object
            but won't constrain anything

"Colours"  (launches window)colour multiple objects(controllers) without having to go through
    attribute editor
        * Step 1: select object(s)
        * Step 2: launch window
        * Step 3: set colour from dropdown menu
        * Step 4: press "go" will change the display colors of all selected items

"Combine shapes" (script)this merges shapes together to make one object transform(custom
    controller)
        * Step 1: select curve object(s)
        * Step 2: launching script will combine the shapes under one transform


Attributes:


"Fetch Attribute" (launches window)an interface to query a selected items attributes that
    you can hunt by name portion or values. You can also change attribute value through this
    window if number values apply(handy for heavy attribute lists like on skinDef)
        * Step 1: select object(s)
        * Step 2: launch window
        * Step 3: enter a partial name in the "search" window beside the 
            "Fetch Attribute Name" button
        * Step 3(alternative: enter a value in the "search" window beside the 
            "Fetch Attribute Value" button            
        * Step 4: pressing the button beside either feild will repopulate the
            drop down menu with the attributes that have these names or values
        * Step 5(optional): fill in the "Change Value" field with a new value
        * Step 6: press the "Apply Value" button to change the attribute that
            is currently visible in the drop down menu
        * Step 7(optional): select a new object or keep current object selected
        * Step 8: press "Refresh Selection" will repopulate the drop down menu
            with current selection's full attributes
        "REFRESH SELECTION" - button
            Repopulates the drop down menu with attributes from current
                selection
        "APPLY VALUE" - button
            Will change the value on the attribute that is currently
                visible in the drop down menu
        "FETCH ATTRIBUTE NAME" - button
            Repopulates the drop down menu with all attributes on selected
                object that matches this name
        "FETCH ATTRIBUTE VALUE" - button
            Repopulates the drop down menu with all attributes on selected
                object that matches this value

"Fast float" (launches window)creates a 0-1 fast float. handy for making an attribute to hook
    up blends, constraints etc.
        * Step 1: select object(s)
        * Step 2: launch window
        * Step 3: set name of attribute
        * Step 4: press continue will create a float attribute on all selected objects

"Fast attr alias" (launches window)creates a custom attribute on the second selected object
    to hook up the attribute of the first object to.(handy to link an attribute to a
    controller)
        * Step 1: select 2 objects
        * Step 2: launch window
        * Step 3: select attribute of first object in drop down menu      
        * Step 4: set a desired name of attribute in second field on second object
        * Step 5: press continue will create an attribute on second object to override
            the attribute selected on the first

"Copy single Attribute" (launches window) copies one attribute value to another selected
    object's attribute
        * Step 1: select two objects
        * Step 2: launch window
        * Step 3: select attribute of first object in drop down menu  
        * Step 4: select attribute of second object in drop down menu          
        * Step 5: press continue set the value of the second attribute from the first

"Set Range Multi Attr" (launches window)This has a window that will call up a list of
    attributes. you can then set a range in which a group of items attributes can be changed
    to that range. It has random option that will set a random value within the range. and
    relative so that if you want to transform in local, it will only range within a local
    area(randomizing curve CV position for example) or make a range of attributes across
    multiple items for more random feel(ive been using this to randomize cvs on curves)
        "Randomizing globally"
            * Step 1: select multiple objects(more than 2)
            * Step 2: launch window
            * Step 3: Select attribute from dropdown(this will set same attribute on all)
            * Step 4: Set randomize to "on"
            * Step 5: Leave relative to "off"
            * Step 6: Set a minimal range and a maximum range
            * Step 7: pressing "go" will set the attribute on all to a randomized value
                within the range set that will be in absolute world value (location only)
        "Randomizing relatively"
            * Step 1: select multiple objects(more than 2)
            * Step 2: launch window
            * Step 3: Select attribute from dropdown(this will set same attribute on all)
            * Step 4: Set randomize to "on"
            * Step 5: Leave relative to "on"
            * Step 6: Set a minimal range and a maximum range
            * Step 7: pressing "go" will set the attribute on all to a randomized value
                within the range set that will be in a relative value of current value
                (location only)
        "Range globally"
            * Step 1: select multiple objects(more than 2)
            * Step 2: launch window
            * Step 3: Select attribute from dropdown(this will set same attribute on all)
            * Step 4: Set randomize to "off"
            * Step 5: Leave relative to "off"
            * Step 6: Set a minimal range and a maximum range
            * Step 7: pressing "go" will set the attribute on all to a uniformed value
                divided within the range that will be in absolute world value
                (location only)
        "Range relatively"
            * Step 1: select multiple objects(more than 2)
            * Step 2: launch window
            * Step 3: Select attribute from dropdown(this will set same attribute on all)
            * Step 4: Set randomize to "off"
            * Step 5: Leave relative to "on"
            * Step 6: Set a minimal range and a maximum range
            * Step 7: pressing "go" will set the attribute on all to a uniformed value
                divided within the range that will be in relative value of current value
                (location only)  

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
        "Check (faces) Ngons" - button
            * Step 1: select faces of a polygon object
            * Step 2: launch script will create sets that will highlight any tris or ngons
                (more than 4 sided polies)
        "Check (Object) Poly" - button
            * Step 1: select polygon object
            * Step 2: launch script will clean manifold faces or errors in poly(cleanup poly
                function in maya)
        "Check (vertices) Poles" - button
            * Step 1: select vertices of a polygon object
            * Step 2: launch script will create sets that will highlight poles(edges)
                that are more or less than 4 eges coming out of a vertex

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
    more to save from add selected at top. Will save out a file
    EG:"/usr/people/<user>/joint4.txt"
        * Step 1: select object
        * Step 2: pressing save will create .txt files that will contain the animation
            and attriute values for heirarchy(if applicable) within the path indicated
            and name of file indicated in field 
         "ADD SELECTION" - button
            Adds a slot for new object (each parent is added seperately)
        "SAVE" - button
            Will change the value on the attribute that is currently
                visible in the drop down menu
        "OPEN FOLDER" - button
            opens the folder window for path indicated
        "ATTR DICT" - button
            prints out an attriubute dictionary for personal use(see script editor)
            useful for writing a "setAttr" script on custom setups

"Load Anim/Attr" (launches window)Opens anim keys and attribute values from external file(s)
    (works on a heirarchy). Put full path with no of object in the text field("/usr/people/
    <user>/"). Press refresh and it will repopulate the drop down for available .txt files;
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
            opens the folder window for path indicated    

"Change multi file contents" (launches window)home made change contents of all files in a
    specific folder(eg: names of a joint in an xml skin export)
        * Step 1: launch window
        * Step 2: set path in feild with name of file('*' acts as a wildcard)
        * Step 3: fill in the "old string" field with the string you wish to replace
        * Step 4: Fill in the "new string" field with the string you wish to override with
        * Step 5: pressing "Change" will rewrite all content of files indicated in path

"Change multi file names" (launches window)home made change the names of all files in a
    specific folder(eg: render images)
        * Step 1: launch window
        * Step 2: set path in feild (no file name)
        * Step 3: set file name portion('*' acts as a wildcard)
        * Step 3: fill in the "old string" field with the string you wish to replace
        * Step 4: Fill in the "new string" field with the string you wish to override with
        * Step 5: pressing "Change" will rewrite all names of files to new name

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
