import maya.cmds as cmds
from pymel.core import *

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
        window = cmds.window(winName, title=winTitle, tbm=1, w=600, h=900 )
        menuBarLayout(h=30)
        rowColumnLayout  (' selectArrayRow ', nr=1, w=600)
        frameLayout('LrRow', label='', lv=0, nch=1, borderStyle='out', bv=1, p='selectArrayRow')
        rowLayout  (' rMainRow ', w=600, numberOfColumns=6, p='selectArrayRow')
        columnLayout ('selectArrayColumn', parent = 'rMainRow')
        setParent ('selectArrayColumn')
        cmds.gridLayout('txvaluemeter', p='selectArrayColumn', numberOfColumns=2, cellWidthHeight=(600, 900)) 
        self.list=cmds.scrollField( editable=False, wordWrap=True, text=
'''Button interface: what the buttons do

"Guides tool" - launches another interface to place guides; lays out some sphere guides (this will layout the rig skel+controllers for an autorig system)"

"Tail":this lays out a line of guides in a range that you set( eg: -15 /15 will layout a chosen number in a range within this value in a direction)"

"Build Guides" will build a guide per selected item(objects, verts and cvs)"

"Clean guides" clears all guides in your scene(generally not needed after a rig is built but dont use if more than one rig with more than one guide set. will wipe all '_guide' from scene"

"Rebuild guides" will search a specific joint heirarchy that is named within the guide system and rebuild guides to the joints


Minirigs

"Curve Rig" - simple curve rig, no FK or IK.

"ChainRig" - FK and IK chain(use the tail guide layout) if you've chosen a particular axis for your guides, use the same axis for your controls.(the spheres have a colored shape to help guide the dimensions they are building in

Tools

"Edit sets" - this tool allows for easy adding and subtracting of verts to a blenshape or a dynamic constraint set

"Select array tool" - a tool i built up for just finding nodes and making a temp work area of selections of verts. (constantly using this to find things in full scenes by name and node type)

"Renamer tool" - a basic renamer. has the ability to strip number, shift name parts, remove underscores, shift numbers, remove isolated numbers, replace names in bulk

"Plot vertex" - if you're familiar with rivets, it's similar except that there is no dependency set up. it bakes a locator in space for the animation duration to the face or vertex of your choice

"Matchmatrix" moves one object to another based on the xform command

"MirrorTransform" mirrors a reflected transform rotation. used in animations to mirror an arm or leg

"Reset selected" will reset object to zeroed out transform. won't remove animation

"Wipe anim from obj" will wipe animation curves and reset transforms to zero

"ShadeNetworkSel" - this brings up the hypershade and networks the shader(s)for the selected object(s)

Reset selected

"Duplicate move" duplicates the first selected item to the subsequent selected items positions and heirarchy

"MultiFunctions" does a mass constraint or extrude. Constrains all items to the first selected item or extrudes first selected item as a tube along several curves(vines)

"Cull CV" removes every first or every other cv in a selection(you can use this to remove the (1) cv will remove the second in chain(as the vine tool fails if second and first cv are too close together)

"Fix Playblast" resets the playblast if in case it breaks in scene

"Revert" rolls back file to last saved

"Undos back on" resets the undos to be on. Maya has a bug where some plugins will turn this off

Controllers:

"Shapes Tool" some premade shapes for controllers that will be created at selections. can also choose to create multiple locators and joints.

"Grp insert" used in rigging to transfer an objects transform onto a group that it's parented under and zeroed out for clean transforms in animation

"Colours"  colour your controllers without having to go through attribute editor

"Combine shapes "this merges shapes together to make one object transform(custom controller)

Attributes:

"Fast float" creates a 0-1 fast float. handy for making an attribute to hook up blends, constraints etc.

"Fast connect" - basically the connection editor but works on selection

"Fast attr alias" - creates a custom attribute on the second selected object to hook up the attribute of the first object to.(handy to link an attribute to a controller)

"Fast SDK alias" - my own version of creating a fast set driven key. you can set your range within the window rather than manually

"Fast SDK connect" - similar to the last tool except no creation, just a hook up between attributes with an SDK range.

"SDK Any" - first selected object is the driver. Everything selected therafter will have an tx, ty, tz, rx, ry, rz SDK - this is a manual set but it will always key these attributes to the first(was useful for facial animation phoneme)

"Copy single Attribute" - copies one attribute value to another selected objects attribute

"Find Attribute" an interface to query a selected items attributes that you can hunt by name portion. You can also change attribute value through this window if number values apply
( does anyone feel lost with the sheer amount of attributes on the skin deformer to hunt through? later: making a way to copy preset attribute settings to an external file to load in another file to get around loading a reference file to copy )

"Set Range Multi Attr" This has a window that will call up a list of attributes. you can then set a range in which a group of items attributes can be changed to that range. It has random option that will set a random value within the range. and relative so that if you want to transform in local, it will only range within a local area(randomizing curve CV position for example) or make a range of attributes across multiple items for more random feel(ive been using this to randomize cvs on curves)

"copyAnim/Att" copies the animation curves and attributes from one object to another

"transfer mass attribute" transfers all attribute values from one object to another. Does use the same transfer values which can be limited with channel box active

Modelling

"Mirror Object" mirrors objects in the X axis (rigging)

"Clean model" wipes history, resets transforms and averages normals on a model(modelling)

"Mirror blend" for mirroring face blends(right blink//left blink, etc)(rigging)

External folders

"Open image in gimp" Will load selected image in a selected texture node in gimp

"pen work folder" opens current workfolder for current scene. if untitled, will open top heirarchy.

''')
        showWindow(window)
