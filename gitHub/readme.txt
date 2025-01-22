
------->>

'''MG rigging modules'''
__author__ = "Elise Deglau"
__version__ = 1.00
'This work is licensed under a Creative Commons Attribution 4.0 International 4.0 (CC BY 4.0)'
'http://creativecommons.org/licenses/by/4.0/au/'


------->>How to install:


exec(open('<path//RigToolKit.py>'))
ToolKitUI()

------->>button interface: what the buttons do(this is also located in the "help button" in the tool interface)



File/session


"Outliner win" (script) brings up outliner as I'm always closing it

"Clean interface"(script closes all superfluous windows (hypershade, hypergraph) to clean up interface

"Revert" (launches window)rolls back file to last saved

"Fix Playblast" (script)resets the playblast if in case it breaks in scene

"Undos back on" (script)resets the undos to be on. Maya has a bug where some plugins will turn this off



Minirigs


Guides tool (launches another toolkit window) launches another interface to place guides; lays out some sphere guides (this will layout the rig skel+controllers for an autorig system)"


"Tail":(launches window)this lays out a line of guides in a range that you set( eg: -15 /15 will layout a chosen number in a range within this value in a direction)"

"Build Guides" (lanches a window to name)will build a guide per selected item(objects, verts and cvs)"

"Clean guides" (script)clears all guides in your scene(generally not needed after a rig is built but dont use if more than one rig with more than one guide set. will wipe all '_guide' from scene"



"Insert grp/clst/jnt"(dropdown) inserts selections under their own group whilst zeroing out (handy for sandwiching a control in a rig), or adds a cluster or joint skin to selection

"Curve Rig" - (launches window)simple curve rig, no FK or IK.

"ChainRig" - (launches window) FK and IK chain(use the tail guide layout) if you've chosen a particular axis for your guides, use the same axis for your controls.(the spheres have a colored shape to help guide the dimensions they are building in. (this is still in development. use at own risk)

"Multi Rivet" (script)creates multiple rivets on selection of points

"Multi Point" (script)creates mulitple Point on Poly constraints on selection of points

"Connect to curve" - (script)add objects to a curve. Select curve first and then objects to follow



Tools


"Select array tool" - (launches window)a tool i built up for just finding nodes and making a temp work area of selections of verts. (constantly using this to find things in full scenes by name and node type)

"Renamer tool" - (launches window)a basic renamer. has the ability to strip number, shift name parts, remove underscores, shift numbers, remove isolated numbers, replace names in bulk

"Edit sets" - (launches window)this tool allows for adding and subtracting of verts to a blenshape or a dynamic constraint set or a regular objectSet

"Cull CV" (launches window)removes every first or every other cv in a selection(you can use this to remove the (1) cv will remove the second in chain(as the vine tool fails if second and first cv are too close together). also has a rebuild function to rebuild a mass of curves using mathematic array and matching now

"Plot vertex" - (launches window)if you're familiar with rivets, it's similar except that there is no dependency set up. it bakes a locator in space for the animation duration to the face or vertex of your choice

"MultiFunctions" (launches window)does a mass constraint or extrude. Constrains all items to the first selected item or extrudes first selected item as a tube along several curves(i was using this in early day layout of main vines)

"Matchmatrix" (script)moves one object to another based on the xform command

"Reset selected" (script)will res et object to zeroed out transform. won't remove animation

"Wipe anim from obj" (script)will wipe animation curves and reset transforms to zero

"ShadeNetworkSel" (script)this brings up the hypershade and networks the shader(s)for the selected object(s)

"Duplicate move" (script)duplicates the first selected item to the subsequent selected items positions and heirarchy
(used this on a string tent in which i selected all cvs on a curve and then a cube and duplicated along curve - there are better scripts than this however like "copier" in SOuP which you can get variations)



Controllers:


"Controller" (launches window)some premade shapes for controllers that will be created at selections. can also choose to create multiple locators and joints. Will add a constraint with selection

"Shapes Tool" (launches window)some premade shapes that will be created at selections. can also choose to create multiple locators and joints. These are not constrained with the selection so it' only creates a shape and nothing more (unlike "Controller" which will add a constraint with selection")

"Colours"  (launches window)colour multiple objects(controllers) without having to go through attribute editor

"Combine shapes" (script)this merges shapes together to make one object transform(custom controller)



Attributes:


"Fetch Attribute" (launches window)an interface to query a selected items attributes that you can hunt by name portion or values. You can also change attribute value through this window if number values apply(handy for heavy attribute lists like on skinDef)


"Fast float" (launches window)creates a 0-1 fast float. handy for making an attribute to hook up blends, constraints etc.


"Fast attr alias" (launches window)creates a custom attribute on the second selected object to hook up the attribute of the first object to.(handy to link an attribute to a controller)

"Copy single Attribute" (launches window) copies one attribute value to another selected objects attribute

"Set Range Multi Attr" (launches window)This has a window that will call up a list of attributes. you can then set a range in which a group of items attributes can be changed to that range. It has random option that will set a random value within the range. and relative so that if you want to transform in local, it will only range within a local area(randomizing curve CV position for example) or make a range of attributes across multiple items for more random feel(ive been using this to randomize cvs on curves)

"copyAnim/Att" (script)copies the animation curves and attribute values from one object to another

"transfer mass attribute" (script)transfers all attribute values(but not animation curves) from one object to another.



Modelling


"Blend Groups" (dropdown)this creates a blend between group heirarchies based on matching names within the group or selection

"Reshape to Edge" (dropdown)Select a continuous edge on one object and a continuous edge on a target object. This will bend the edge of the first object to the second(veins on leaves or quills on feathers). Reshape to edge: better for cylindrical shapes to curve along a surface edge. Reshape to shape: better for flat planes against another surface(plane should have some bias on which way it leans or it might twist - uses shrink wrap to place on surface)

"PolyCheck" (launches window)checks poles and ngons on component selections

"Build Curve" (script)use to build a curve based on selection. Best to use guide layouts on selected vertice and then use this to create curve

"Clean model" (script)wipes history, resets transforms and averages normals on a model(modelling)

"Mirror blend" (script)for mirroring face, arm, leg blends(right blink//left blink, arm muscles, etc)(rigging)



External folders


"Save Anim/Attr" (launches window)a home made scripted save anim keys and attribute values into external file(s)(works on a heirarchy). Put full file path with preferred name of object in text field("/usr/people/<user>/joint4"). save button saves out file. Can add more to save from add selected at top. Will save out a file EG:"/usr/people/<user>/joint4.txt"
 
"Load Anim/Attr" (launches window)Opens anim keys and attribute values from external file(s)(works on a heirarchy). Put full path with no of object in the text field("/usr/people/<user>/"). Hit refresh and it will repopulate the drop down for available .txt files; stick to the name of your object to reload anim

"Export multiple obj" export multiple selections into separate .obj files

"Change multi file contents" (launches window)home made change contents of all files in a specific folder(eg: names of a joint in an xml skin export)

"Change multi file names" (launches window)home made change the names of all files in a specific folder(eg: render images)

"Export multiple obj" (launches window)Will export a selection to multiple external .obj files. ("/usr/people/<user>/")

"Open image in gimp" (script runs on selected texture node)Will load selected image in a selected texture node in gimp

"Open work folder" (launches window)opens current workfolder for current scene. if untitled, will open top hierarchy.
