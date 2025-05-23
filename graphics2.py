# graphics2.py

# pylint: disable-all
# flake8: noqa
# mypy: ignore-errors

"""Simple object oriented graphics library  

The library is designed to make it very easy for novice programmers to
experiment with computer graphics in an object oriented fashion. It is
written by John Zelle for use with the book "Python Programming: An
Introduction to Computer Science" (Franklin, Beedle & Associates).

LICENSE: This is open-source software released under the terms of the
GPL (http://www.gnu.org/licenses/gpl.html).

PLATFORMS: The package is a wrapper around Tkinter and should run on
any platform where Tkinter is available.

INSTALLATION: Put this file somewhere where Python can see it.

OVERVIEW: There are two kinds of objects in the library. The GraphWin
class implements a window where drawing can be done and various
GraphicsObjects are provided that can be drawn into a GraphWin. As a
simple example, here is a complete program to draw a circle of radius
10 centered in a 100x100 window:

--------------------------------------------------------------------
from graphics import *

def main():
    win = GraphWin("My Circle", 100, 100)
    c = Circle(Point(50,50), 10)
    c.draw(win)
    win.getMouse() # Pause to view result
    win.close()    # Close window when done

main()
--------------------------------------------------------------------
GraphWin objects support coordinate transformation through the
setCoords method and mouse and keyboard interaction methods.

The library provides the following graphical objects:
    Point
    Line
    Circle
    Oval
    Rectangle
    Polygon
    Text
    Entry (for text-based input)
    Image

Various attributes of graphical objects can be set such as
outline-color, fill-color and line-width. Graphical objects also
support moving and hiding for animation effects.

The Image class provides for some simple pixel-based image manipulation.  

DOCUMENTATION: For more documentation, see Chapter 4 of "Python
Programming: An Introduction to Computer Science" by John Zelle,
published by Franklin, Beedle & Associates.  Also see
http://mcsp.wartburg.edu/zelle/python for a quick reference

Also, Dr. Forrest Stonedahl has made several enahancements to the original
graphics.py, and these described in a separate document.
"""

__version__ = "6.1"


# TODO LIST FOR FUTURE FEATURES:
#    - Polygon.containsPoint(pt) : True/False
#             - see: https://stackoverflow.com/questions/36399381/whats-the-fastest-way-of-checking-if-a-point-is-inside-a-polygon-in-python)
#                    (will probably require matplotlib package dependency, but can import it dynamically with try/except)
#    - left/right justification for Text objects?
#    - create Turtle class (takes a GraphicsObject shape as parameter, or defaults to triangle?)
#           - right/left/forward? setheading?  pen-down / pen-color?  clear-drawing? (keep track of line segments drawn?)
#    - Maybe: create ShapeGroup class (moves/scales/rotates together)
#         - which methods to override? draw?
#    - consider adding optional keyword parameter for "mouseButtonNum" to isMouseDown()?  checkMouseButton(btnNum)/getMouseButton(btnNum)?
#    - add type checking to many of the graphics methods?  e.g. helpful error message for Text(msgFirst, pointSecond)
#
#    - If you call setCoords(...) again after creating some shapes, does everything work reasonably as one would expect?
#    - add isKeyDown('KeyCode') -> boolean?

#Version 6.2 Ideas:
#    - try to improve Mac performance... what about calling update_idletasks() instead of update() ? check on Mac
#      (tried this on Isabelle's Mac, and then we lost some updates.  Also didn't seem hugely faster?)
#
#
# Version 6.1 modifications:
#   Added (...topLeftX=?,topLeftY=?) optional keyword parameters to GraphWin constructor to position window on screen
#   Added comments at top to avoid mypy & flake8 & pylint checking, so it won't flood
#   students "Assistant" tab.
#
# Version 6.01 changelog:
#    * changed several abstract methods to raise NotImplementedError instead of generic Exception,
#      to silence pylint warnings in older Python versions.
#
# Version 6 modifications:
#
#  Added GraphWin.checkMousePointer() -- mouse movement x & y
#  Added GraphWin.isMouseDown() -- checking if the mouse button is currently HELD down
#  Added GraphWin.clear() method - undraws everything
#  Added GraphWin.setTitle()
#
#  Added GraphicsObject.scale(xFactor,yFactor) method (including negative scaling to flip/mirror),
#        for everything except Text & Entry objects
#
#     setShapeSize(newWidth,newHeight)
#     getShapeWidth(), getShapeHeight() 
#
#     getFill(), getOutline(), getOutlineWidth() (and setOutlineWidth() alias for setWidth(), which was a BAD method name choice by Zelle)
#
#     orbitAround(orbitAngle, orbitCenterPoint)
#   
#
#  Added Polygon.rotate(angleInDegrees)
#        Polygon.getBoundingRectangle()
#
#  Added Image.getBoundingRectangle()
#        Image.load(filename)
#        - added LRU caching for images loaded from files, to allow good animation performance using load(...) to change images
#
# Version 5.0.2FS - Made update() method public again. (oops)

# Version 5.0.1FS - Forrest Stonedahl tidied up some things 
#              causing warnings/errors in Thonny and renamed
#              some private variables with prefix _ so they
#              wouldn't show up in Thonny's debugger)

# Version 5 8/26/2016
#     * update at bottom to fix MacOS issue causing askopenfile() to hang
#     * update takes an optional parameter specifying update rate
#     * Entry objects get focus when drawn
#     * __repr_ for all objects
#     * fixed offset problem in window, made canvas borderless

# Version 4.3 4/25/2014
#     * Fixed Image getPixel to work with Python 3.4, TK 8.6 (tuple type handling)
#     * Added interactive keyboard input (getKey and checkKey) to GraphWin
#     * Modified setCoords to cause redraw of current objects, thus
#       changing the view. This supports scrolling around via setCoords.
#
# Version 4.2 5/26/2011
#     * Modified Image to allow multiple undraws like other GraphicsObjects
# Version 4.1 12/29/2009
#     * Merged Pixmap and Image class. Old Pixmap removed, use Image.
# Version 4.0.1 10/08/2009
#     * Modified the autoflush on GraphWin to default to True
#     * Autoflush check on close, setBackground
#     * Fixed getMouse to flush pending clicks at entry
# Version 4.0 08/2009
#     * Reverted to non-threaded version. The advantages (robustness,
#         efficiency, ability to use with other Tk code, etc.) outweigh
#         the disadvantage that interactive use with IDLE is slightly more
#         cumbersome.
#     * Modified to run in either Python 2.x or 3.x (same file).
#     * Added Image.getPixmap()
#     * Added update() -- stand alone function to cause any pending
#           graphics changes to display.
#
# Version 3.4 10/16/07
#     Fixed GraphicsError to avoid "exploded" error messages.
# Version 3.3 8/8/06
#     Added checkMouse method to GraphWin
# Version 3.2.3
#     Fixed error in Polygon init spotted by Andrew Harrington
#     Fixed improper threading in Image constructor
# Version 3.2.2 5/30/05
#     Cleaned up handling of exceptions in Tk thread. The graphics package
#     now raises an exception if attempt is made to communicate with
#     a dead Tk thread.
# Version 3.2.1 5/22/05
#     Added shutdown function for tk thread to eliminate race-condition
#        error "chatter" when main thread terminates
#     Renamed various private globals with _
# Version 3.2 5/4/05
#     Added Pixmap object for simple image manipulation.
# Version 3.1 4/13/05
#     Improved the Tk thread communication so that most Tk calls
#        do not have to wait for synchonization with the Tk thread.
#        (see _tkCall and _tkExec)
# Version 3.0 12/30/04
#     Implemented Tk event loop in separate thread. Should now work
#        interactively with IDLE. Undocumented autoflush feature is
#        no longer necessary. Its default is now False (off). It may
#        be removed in a future version.
#     Better handling of errors regarding operations on windows that
#       have been closed.
#     Addition of an isClosed method to GraphWindow class.

# Version 2.2 8/26/04
#     Fixed cloning bug reported by Joseph Oldham.
#     Now implements deep copy of config info.
# Version 2.1 1/15/04
#     Added autoflush option to GraphWin. When True (default) updates on
#        the window are done after each action. This makes some graphics
#        intensive programs sluggish. Turning off autoflush causes updates
#        to happen during idle periods or when flush is called.
# Version 2.0
#     Updated Documentation
#     Made Polygon accept a list of Points in constructor
#     Made all drawing functions call TK update for easier animations
#          and to make the overall package work better with
#          Python 2.3 and IDLE 1.0 under Windows (still some issues).
#     Removed vestigial turtle graphics.
#     Added ability to configure font for Entry objects (analogous to Text)
#     Added setTextColor for Text as an alias of setFill
#     Changed to class-style exceptions
#     Fixed cloning of Text objects

# Version 1.6
#     Fixed Entry so StringVar uses _root as master, solves weird
#            interaction with shell in Idle
#     Fixed bug in setCoords. X and Y coordinates can increase in
#           "non-intuitive" direction.
#     Tweaked wm_protocol so window is not resizable and kill box closes.

# Version 1.5
#     Fixed bug in Entry. Can now define entry before creating a
#     GraphWin. All GraphWins are now toplevel windows and share
#     a fixed root (called _root).

# Version 1.4
#     Fixed Garbage collection of Tkinter images bug.
#     Added ability to set text atttributes.
#     Added Entry boxes.

import time as _time
import os as _os
import math as _math
import functools as _functools

try:  # import as appropriate for 2.x vs. 3.x
    import tkinter as _tk
except:
    import Tkinter as _tk


##########################################################################
# Module Exceptions

class GraphicsError(Exception):
    """Generic error class for graphics module exceptions."""
    pass

_OBJ_ALREADY_DRAWN = "Object currently drawn"
_UNSUPPORTED_METHOD = "Object doesn't support operation"
_BAD_OPTION = "Illegal option value"

##########################################################################
# global variables and funtions

_root = _tk.Tk()
_root.withdraw()

_update_lasttime = _time.time()

def update(rate=None):
    global _update_lasttime
    if rate:
        now = _time.time()
        pauseLength = 1/rate-(now-_update_lasttime)
        if pauseLength > 0:
            _time.sleep(pauseLength)
            _update_lasttime = now + pauseLength
        else:
            _update_lasttime = now

    _root.update()

############################################################################
# Graphics classes start here
        
class GraphWin(_tk.Canvas):

    """A GraphWin is a toplevel window for displaying graphics."""

    def __init__(self, title="Graphics Window",
                 width=200, height=200, autoflush=True,topLeftX=None,topLeftY=None):
        assert type(title) == type(""), "Title must be a string"
        master = _tk.Toplevel(_root)
        master.protocol("WM_DELETE_WINDOW", self.close)
        _tk.Canvas.__init__(self, master, width=width, height=height,
                           highlightthickness=0, bd=0)
        self.master.title(title)
        self.pack()
        master.resizable(0,0)
        if topLeftX != None and topLeftY != None:
            master.geometry(f"+{topLeftX}+{topLeftY}")
        self.foreground = "black"
        self.items = []
        self.mouseX = None
        self.mouseY = None
        self._mouseMoveX = 0
        self._mouseMoveY = 0
        self._isMouseDown = False
        self.bind("<Button-1>", self._onClick)
        self.bind("<ButtonRelease-1>", self._onClickRelease)
        self.bind('<Motion>', self._onMouseMove)
        self.bind_all("<Key>", self._onKey)
        self.height = int(height)
        self.width = int(width)
        self.autoflush = autoflush
        self._mouseCallback = None
        self.trans = None
        self.closed = False
        master.lift()
        self.lastKey = ""
        if autoflush: _root.update()

    def __repr__(self):
        try: 
            if self.isClosed():
                return "<Closed GraphWin>"
            else:
                return "GraphWin('{}', {}, {})".format(self.master.title(),
                                                 self.getWidth(),
                                                 self.getHeight())
        except:
            return "<Uninitialized GraphWin>"

    def __str__(self):
        return repr(self)
     
    def __checkOpen(self):
        if self.closed:
            raise GraphicsError("window is closed")

    def _onKey(self, evnt):
        self.lastKey = evnt.keysym


    def setBackground(self, color):
        """Set background color of the window"""
        self.__checkOpen()
        self.config(bg=color)
        self.__autoflush()
        
    def setCoords(self, x1, y1, x2, y2):
        """Set coordinates of window to run from (x1,y1) in the
        lower-left corner to (x2,y2) in the upper-right corner."""
        self.trans = Transform(self.width, self.height, x1, y1, x2, y2)
        self.redraw()

    def close(self):
        """Close the window"""

        if self.closed: return
        self.closed = True
        self.master.destroy()
        self.__autoflush()


    def isClosed(self):
        return self.closed

    def isOpen(self):
        return not self.closed


    def __autoflush(self):
        if self.autoflush:
            _root.update()

    
    def plot(self, x, y, color="black"):
        """Set pixel (x,y) to the given color"""
        self.__checkOpen()
        xs,ys = self.toScreen(x,y)
        self.create_line(xs,ys,xs+1,ys, fill=color)
        self.__autoflush()
        
    def plotPixel(self, x, y, color="black"):
        """Set pixel raw (independent of window coordinates) pixel
        (x,y) to color"""
        self.__checkOpen()
        self.create_line(x,y,x+1,y, fill=color)
        self.__autoflush()
      
    def flush(self):
        """Update drawing to the window"""
        self.__checkOpen()
        self.update_idletasks()
        
    def getMouse(self):
        """Wait for mouse click and return Point object representing
        the click"""
        self.update()      # flush any prior clicks
        self.mouseX = None
        self.mouseY = None
        while self.mouseX == None or self.mouseY == None:
            self.update()
            if self.isClosed(): raise GraphicsError("getMouse in closed window")
            _time.sleep(.1) # give up thread
        x,y = self.toWorld(self.mouseX, self.mouseY)
        self.mouseX = None
        self.mouseY = None
        return Point(x,y)

    def checkMouse(self):
        """Return last mouse click or None if mouse has
        not been clicked since last call"""
        if self.isClosed():
            raise GraphicsError("checkMouse in closed window")
        self.update()
        if self.mouseX != None and self.mouseY != None:
            x,y = self.toWorld(self.mouseX, self.mouseY)
            self.mouseX = None
            self.mouseY = None
            return Point(x,y)
        else:
            return None

    def checkMousePointer(self):
        """Return point where the mouse pointer is currently at.
          (i.e. tracks mouse movement, not just clicks)"""
        if self.isClosed():
            raise GraphicsError("checkMousePointer in closed window")
        self.update()
        return Point(*self.toWorld(self._mouseMoveX, self._mouseMoveY))

    def isMouseButtonDown(self):
        """Return True if the primary mouse button is currently held down, false otherwise"""
        if self.isClosed():
            raise GraphicsError("isMouseDown in closed window")
        self.update()
        return self._isMouseDown

    def getKey(self):
        """Wait for user to press a key and return it as a string."""
        self.lastKey = ""
        while self.lastKey == "":
            self.update()
            if self.isClosed(): raise GraphicsError("getKey in closed window")
            _time.sleep(.1) # give up thread

        key = self.lastKey
        self.lastKey = ""
        return key

    def checkKey(self):
        """Return last key pressed or None if no key pressed since last call"""
        if self.isClosed():
            raise GraphicsError("checkKey in closed window")
        self.update()
        key = self.lastKey
        self.lastKey = ""
        return key
            
    def getHeight(self):
        """Return the height of the window"""
        return self.height
        
    def getWidth(self):
        """Return the width of the window"""
        return self.width

    def clear(self):
        """Undraws everything in this window"""
        for item in self.items.copy():
            item.undraw()

    def setTitle(self,newTitle):
        """changes the window's title to newTitle"""
        if self.closed:
            raise GraphicsError("Can't change the title of a close window")
        self.master.title(newTitle)
        self.update()
    
    def toScreen(self, x, y):
        trans = self.trans
        if trans:
            return self.trans.screen(x,y)
        else:
            return x,y
                      
    def toWorld(self, x, y):
        trans = self.trans
        if trans:
            return self.trans.world(x,y)
        else:
            return x,y
        
    def setMouseHandler(self, func):
        self._mouseCallback = func
        
    def _onClick(self, e):
        self.mouseX = e.x
        self.mouseY = e.y
        self._isMouseDown = True
        if self._mouseCallback:
            self._mouseCallback(Point(e.x, e.y))

    def _onClickRelease(self, _):
        self._isMouseDown = False

    def _onMouseMove(self, e):
        self._mouseMoveX = e.x
        self._mouseMoveY = e.y

    def addItem(self, item):
        self.items.append(item)

    def delItem(self, item):
        self.items.remove(item)

    def redraw(self):
        for item in self.items[:]:
            item.undraw()
            item.draw(self)
        self.update()
        
                      
class Transform:

    """Internal class for 2-D coordinate transformations"""
    
    def __init__(self, w, h, xlow, ylow, xhigh, yhigh):
        # w, h are width and height of window
        # (xlow,ylow) coordinates of lower-left [raw (0,h-1)]
        # (xhigh,yhigh) coordinates of upper-right [raw (w-1,0)]
        xspan = (xhigh-xlow)
        yspan = (yhigh-ylow)
        self.xbase = xlow
        self.ybase = yhigh
        self.xscale = xspan/float(w-1)
        self.yscale = yspan/float(h-1)
        
    def screen(self,x,y):
        # Returns x,y in screen (actually window) coordinates
        xs = (x-self.xbase) / self.xscale
        ys = (self.ybase-y) / self.yscale
        return int(xs+0.5),int(ys+0.5)
        
    def world(self,xs,ys):
        # Returns xs,ys in world coordinates
        x = xs*self.xscale + self.xbase
        y = self.ybase - ys*self.yscale
        return x,y

#For some reason, tkinter scales the font differently (points to pixels) on HiDPI machines
#and we need to adjust for that.
try:
    _HIDPI_FONT_SCALING_RATIO = 100.0 / _tk.font.Font(family="Courier",size=100,weight="normal").measure('A')
except:
    _HIDPI_FONT_SCALING_RATIO = 1.0

def setFontScalingRatio(newScalingRatio):
    """Setting this ratio manually adjusts all font sizes for future Text & Entry objects.
       (different high resolution monitors may use different DPI for as 12 point font.)
       A larger ratio will cause the text/entry fonts to appear larger."""
    global _HIDPI_FONT_SCALING_RATIO
    _HIDPI_FONT_SCALING_RATIO = newScalingRatio
    _DEFAULT_CONFIG["font"] = ("helvetica", round(12 * _HIDPI_FONT_SCALING_RATIO), "normal")

    
# Default values for various item configuration options. Only a subset of
#   keys may be present in the configuration dictionary for a given item
_DEFAULT_CONFIG = {"fill":"",
      "outline":"black",
      "width":"1",
      "arrow":"none",
      "text":"",
      "justify":"center",
                  "font": ("helvetica", round(12 * _HIDPI_FONT_SCALING_RATIO), "normal")}

class GraphicsObject:

    """Generic base class for all of the drawable objects"""
    # A subclass of GraphicsObject should override methods
    #  _draw, _move, _scale, and getCenter()
    
    def __init__(self, options):
        # options is a list of strings indicating which options are
        # legal for this object.
        
        # When an object is drawn, canvas is set to the GraphWin(canvas)
        #    object where it is drawn and id is the TK identifier of the
        #    drawn shape.
        self.canvas = None
        self.id = None

        # config is the dictionary of configuration options for the widget.
        config = {}
        for option in options:
            config[option] = _DEFAULT_CONFIG[option]
        self.config = config
        
    def setFill(self, color):
        """Set interior color to color (str)"""
        self._reconfig("fill", color)
        
    def getFill(self):
        """returns the interior color (str) of this shape"""
        return self.config["fill"]

    def setOutline(self, color):
        """Set outline color to color (str)"""
        self._reconfig("outline", color)

    def getOutline(self):
        """returns the outline color (str) of this shape"""
        return self.config["outline"]

    def setOutlineWidth(self, width):
        """Set outline line weight to width"""
        self._reconfig("width", width)

    def getOutlineWidth(self):
        """returns the current line width of this shape's outline (line weight)"""
        return float(self.config["width"])

    def setWidth(self, width): #LEGACY/COMPATIBLIY - poor method name by Zelle!
        """Set outline line weight to width"""
        self._reconfig("width", width)
            
    def setCenter(self, newCenterPoint):
        """moves this object so that its center point is at the specified location"""
        oldCenterPoint= self.getCenter()
        self.move(newCenterPoint.x-oldCenterPoint.x,newCenterPoint.y-oldCenterPoint.y)        

    def draw(self, graphwin):

        """Draw the object in graphwin, which should be a GraphWin
        object.  A GraphicsObject may only be drawn into one
        window. Raises an error if attempt made to draw an object that
        is already visible."""

        if self.canvas and not self.canvas.isClosed(): raise GraphicsError(_OBJ_ALREADY_DRAWN)
        if graphwin.isClosed(): raise GraphicsError("Can't draw to closed window")
        self.canvas = graphwin
        self.id = self._draw(graphwin, self.config)
        graphwin.addItem(self)
        if graphwin.autoflush:
            _root.update()
        return self

            
    def undraw(self):

        """Undraw the object (i.e. hide it). Returns silently if the
        object is not currently drawn."""
        
        if not self.canvas: return
        if not self.canvas.isClosed():
            self.canvas.delete(self.id)
            self.canvas.delItem(self)
            if self.canvas.autoflush:
                _root.update()
        self.canvas = None
        self.id = None


    def move(self, dx, dy):

        """move object dx units in x direction and dy units in y
        direction"""
        
        self._move(dx,dy)
        canvas = self.canvas
        if canvas and not canvas.isClosed():
            trans = canvas.trans
            if trans:
                x = dx/ trans.xscale 
                y = -dy / trans.yscale
            else:
                x = dx
                y = dy
            self.canvas.move(self.id, x, y)
            if canvas.autoflush:
                _root.update()

    def setShapeSize(self, newShapeWidth, newShapeHeight=None):
        """scales this graphics object to match newShapeWidth and newShapeHeight.
           if newShapeHeight is not provided, it will be scaled proportionally to match the width.
           (Note: Image objects scaling is limited to certain ratios, so the resulting Image may not end
             up exactly the size/shape that you specify)."""
        if newShapeHeight == None:
            self.scale(newShapeWidth/self.getShapeWidth())
        else:
            self.scale(newShapeWidth/self.getShapeWidth(),newShapeHeight/self.getShapeHeight())


    def scale(self, scalingFactorX, scalingFactorY=None):
        """
            resizes this object by the given scaling factor(s)
            scaling factor <1.0 shrinks, >1.0 grows.
            If only one parameter is given, it is used to scale both X and Y.
            If two parameters are given, the first scales X, and the second scales Y.
            If the x or y scaling factor is negative, the shape will be mirrored/flipped.
            
            Note: For shapes with an outline, the outline line width does not get scaled
        """
        if scalingFactorY == None:
            scalingFactorY = scalingFactorX
        
        canvas = self.canvas
        # TODO: not necessary to do pixel conversion?
#         xPixelScale = scalingFactor
#         yPixelScale = scalingFactor
# 
#         if canvas and not canvas.isClosed() and canvas.trans:
#             xPixelScale = scalingFactorX / canvas.trans.xscale 
#             yPixelScale = scalingFactorY / canvas.trans.yscale
        self._scale(scalingFactorX,scalingFactorY)
            
        if canvas and not canvas.isClosed():
            if canvas.autoflush:
                _root.update()

    def flipHorizontal(self):
        """ flips this shape horizontally (mirror image)"""
        self.scale(-1,1)

    def flipVertical(self):
        """ flips this shape vertically"""
        self.scale(1,-1)

    def orbitAround(self,angleInDegrees,orbitCenterPoint):
        """ orbits the object around the given orbitCenterPoint by the given angle.
            (positive angle goes clockwise, negative counter-clockwise)"""
        centerPt = self.getCenter()
        centerPt.orbitAround(angleInDegrees,orbitCenterPoint)
        self.setCenter(centerPt)
    
    def _reconfig(self, option, setting):
        # Internal method for changing configuration of the object
        # Raises an error if the option does not exist in the config
        #    dictionary for this object
        if option not in self.config:
            raise GraphicsError(_UNSUPPORTED_METHOD)
        options = self.config
        options[option] = setting
        if self.canvas and not self.canvas.isClosed():
            self.canvas.itemconfig(self.id, options)
            if self.canvas.autoflush:
                _root.update()


    def _draw(self, canvas, options):
        """draws appropriate figure on canvas with options provided
        Returns Tk id of item drawn"""
        raise NotImplementedError("must override _draw in subclasses")

    def _move(self, dx, dy):
        """updates internal state of object to move it dx,dy units"""
        raise NotImplementedError("must override _move in subclasses")

    def _scale(self, scalingFactorX, scalingFactorY):
        """updates internal state of object to scale it by the given factors"""
        raise NotImplementedError("must override _scale in subclasses")
    
    def getShapeWidth(self):
        """Returns the width of the bounding box containing this graphics object"""
        #override in subclasses
        raise NotImplementedError("Sorry, this feature is not implemented yet for this type of graphics object.")

    def getShapeHeight(self):
        """Returns the height of the bounding box containing this graphics object"""
        #override in subclasses
        raise NotImplementedError("Sorry, this feature is not implemented yet for this type of graphics object.")

    def setShapeWidth(self, newWidth):
        """sets the width of the bounding box containing this graphics object"""
        self.setShapeSize(newWidth,self.getShapeHeight())

    def setShapeHeight(self, newHeight):
        """sets the height of the bounding box containing this graphics object"""
        self.setShapeSize(self.getShapeWidth(),newHeight)

    def getCenter(self):
        """returns a Point representing the center location of this shape"""
        raise NotImplementedError("must override getCenter in subclasses")

         
class Point(GraphicsObject):
    def __init__(self, x, y):
        GraphicsObject.__init__(self, ["outline", "fill"])
        self.setFill = self.setOutline
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        try:
            return "Point({}, {})".format(self.x, self.y)
        except:
            return "Uninitialized Point"
        
    def _draw(self, canvas, options):
        x,y = canvas.toScreen(self.x,self.y)
        return canvas.create_rectangle(x,y,x+1,y+1,options)
        
    def _move(self, dx, dy):
        self.x = self.x + dx
        self.y = self.y + dy

    def _scale(self,scalingFactorX,scalingFactorY):
        """ Points can't be rescaled"""
        pass

    def setShapeSize(self, newShapeWidth, newShapeHeight=None):
        """ Points can't change size"""
        pass

    def orbitAround(self,angleInDegrees,orbitCenterPoint):
        """ rotates the point by the given angle around the given orbitCenterPoint.
            (positive goes clockwise, negative counter-clockwise)"""
        cx,cy = orbitCenterPoint.x,orbitCenterPoint.y
        
        r = _math.sqrt((self.x - cx) ** 2 + (self.y-cy)**2)
        theta = _math.atan2(self.y-cy,self.x-cx) + _math.radians(angleInDegrees)
        newX = cx + r * _math.cos(theta)
        newY = cy + r * _math.sin(theta)
        self.move(newX-self.x,newY-self.y)

    def getShapeWidth(self):
        """Note: we're pretending points have no area/size, even though they do take
         up a little space on the screen when drawn"""
        return 0
    
    def getShapeHeight(self):
        """Note: we're pretending points have no area/size, even though they do take
         up a little space on the screen when drawn"""
        return 0

    def clone(self):
        other = Point(self.x,self.y)
        other.config = self.config.copy()
        return other
                
    def getX(self): return self.x
    def getY(self): return self.y
    
    def getCenter(self):
        return Point(self.x,self.y)
    
class _BBox(GraphicsObject):
    # Internal base class for objects represented by bounding box
    # (opposite corners) Line segment is a degenerate case.
    
    def __init__(self, p1, p2, options=("outline","width","fill")):
        GraphicsObject.__init__(self, list(options))
        self.p1 = p1.clone()
        self.p2 = p2.clone()

    def _move(self, dx, dy):
        self.p1.x = self.p1.x + dx
        self.p1.y = self.p1.y + dy
        self.p2.x = self.p2.x + dx
        self.p2.y = self.p2.y  + dy
                
    def getP1(self): return self.p1.clone()

    def getP2(self): return self.p2.clone()

    def setP1(self,newP1):
        """ changes the location of point P1
            Param: newP1 (Point) new location"""
        self.p1 = Point(newP1.x,newP1.y)
        self._updatePointsOnCanvas()
    
    def setP2(self,newP2):
        """ changes the location of point P2
            Param: newP2 (Point) new location"""
        self.p2 = Point(newP2.x,newP2.y)
        self._updatePointsOnCanvas()
        
    def _updatePointsOnCanvas(self):
        if self.canvas and not self.canvas.isClosed():
            x1,y1 = self.canvas.toScreen(self.p1.x,self.p1.y)
            x2,y2 = self.canvas.toScreen(self.p2.x,self.p2.y)
            self.canvas.coords(self.id, x1, y1, x2, y2)
            if self.canvas.autoflush:
                _root.update()
        
    def getCenter(self):
        p1 = self.p1
        p2 = self.p2
        return Point((p1.x+p2.x)/2.0, (p1.y+p2.y)/2.0)

    def getShapeWidth(self):
        return abs(self.p2.x - self.p1.x)
    
    def getShapeHeight(self):
        return abs(self.p2.y - self.p1.y)

    def _scale(self,scalingFactorX,scalingFactorY):
        """ Resizes the bounding box by the given scaling factors."""
        cx,cy = (self.p1.x+self.p2.x)/2.0, (self.p1.y+self.p2.y)/2.0
        p1x = cx + (self.p1.x-cx) * scalingFactorX
        p2x = cx + (self.p2.x-cx) * scalingFactorX
        p1y = cy + (self.p1.y-cy) * scalingFactorY
        p2y = cy + (self.p2.y-cy) * scalingFactorY
        self.p1 = Point(p1x,p1y)
        self.p2 = Point(p2x,p2y)
        
        if self.canvas and not self.canvas.isClosed():
            x1,y1 = self.canvas.toScreen(self.p1.x,self.p1.y)
            x2,y2 = self.canvas.toScreen(self.p2.x,self.p2.y)
            self.canvas.coords(self.id, x1, y1, x2, y2)
    
class Rectangle(_BBox):
    
    def __init__(self, p1, p2):
        _BBox.__init__(self, p1, p2)

    def __repr__(self):
        try:
            return "Rectangle({}, {})".format(str(self.p1), str(self.p2))
        except:
            return "Uninitialized Rect"
    
    def _draw(self, canvas, options):
        p1 = self.p1
        p2 = self.p2
        x1,y1 = canvas.toScreen(p1.x,p1.y)
        x2,y2 = canvas.toScreen(p2.x,p2.y)
        return canvas.create_rectangle(x1,y1,x2,y2,options)
        
    def clone(self):
        other = Rectangle(self.p1, self.p2)
        other.config = self.config.copy()
        return other


class Oval(_BBox):
    
    def __init__(self, p1, p2):
        _BBox.__init__(self, p1, p2)

    def __repr__(self):
        try:
            return "Oval({}, {})".format(str(self.p1), str(self.p2))
        except:
            return "Uninitialized Oval"

    def clone(self):
        other = Oval(self.p1, self.p2)
        other.config = self.config.copy()
        return other
   
    def _draw(self, canvas, options):
        p1 = self.p1
        p2 = self.p2
        x1,y1 = canvas.toScreen(p1.x,p1.y)
        x2,y2 = canvas.toScreen(p2.x,p2.y)
        return canvas.create_oval(x1,y1,x2,y2,options)
    
class Circle(Oval):
    
    def __init__(self, center, radius):
        p1 = Point(center.x-radius, center.y-radius)
        p2 = Point(center.x+radius, center.y+radius)
        Oval.__init__(self, p1, p2)
        self.radius = radius

    def __repr__(self):
        try:
            return "Circle({}, {})".format(str(self.getCenter()), str(self.radius))
        except:
            return "Uninitialized Circle"
        
    def clone(self):
        other = Circle(self.getCenter(), self.radius)
        other.config = self.config.copy()
        return other
        
    def getRadius(self):
        return self.radius

    def setRadius(self,newRadius):
        """Changes the size of this circle to have the specified radius"""
        self.radius=newRadius
        self.setShapeSize(newRadius*2,newRadius*2)

    def _scale(self,scalingFactorX,scalingFactorY):
        """ Resizes the Circle by the given scaling factors."""
        if scalingFactorX != scalingFactorY:
            raise GraphicsError("You can't scale X/Y differently for a Circle object!  Use the Oval class instead!")
        Oval._scale(self,scalingFactorX,scalingFactorX)
        self.radius = self.radius * scalingFactorX
                  
class Line(_BBox):
    
    def __init__(self, p1, p2):
        _BBox.__init__(self, p1, p2, ["arrow","fill","width"])
        self.setFill(_DEFAULT_CONFIG['outline'])
        self.setOutline = self.setFill

    def __repr__(self):
        try:
            return "Line({}, {})".format(str(self.p1), str(self.p2))
        except:
            return "Uninitialized Line"
            

    def clone(self):
        other = Line(self.p1, self.p2)
        other.config = self.config.copy()
        return other
  
    def _draw(self, canvas, options):
        p1 = self.p1
        p2 = self.p2
        x1,y1 = canvas.toScreen(p1.x,p1.y)
        x2,y2 = canvas.toScreen(p2.x,p2.y)
        return canvas.create_line(x1,y1,x2,y2,options)
        
    def setArrow(self, option):
        if not option in ["first","last","both","none"]:
            raise GraphicsError(_BAD_OPTION)
        self._reconfig("arrow", option)
        
    def rotate(self,angleInDegrees):
        """ rotates the line by the given angle around its center point
            (positive angle goes clockwise, negative counter-clockwise)"""
        centerPt = self.getCenter()
        self.p1.orbitAround(angleInDegrees,centerPt)
        self.p2.orbitAround(angleInDegrees,centerPt)
        
        if self.canvas and not self.canvas.isClosed():
            x1,y1 = self.canvas.toScreen(self.p1.x,self.p1.y)
            x2,y2 = self.canvas.toScreen(self.p2.x,self.p2.y)
            self.canvas.coords(self.id, x1, y1, x2, y2)


class Polygon(GraphicsObject):
    
    def __init__(self, *points):
        # if points passed as a list, extract it
        if len(points) == 1 and type(points[0]) == type([]):
            points = points[0]
        self.points = list(map(Point.clone, points))
        GraphicsObject.__init__(self, ["outline", "width", "fill"])

    def __repr__(self):
        try:
            return "Polygon"+str(tuple(p for p in self.points))
        except:
            return "Uninitialized Polygon"
        
    def clone(self):
        other = Polygon(*self.points)
        other.config = self.config.copy()
        return other

    def getPoints(self):
        return list(map(Point.clone, self.points))

    def _getBoundingCoords(self):
        xMin = xMax = self.points[0].x
        yMin = yMax = self.points[0].y
        for p in self.points[1:]:
            xMin = min(xMin,p.x)
            xMax = max(xMax,p.x)
            yMin = min(yMin,p.y)
            yMax = max(yMax,p.y)
        return xMin,yMin,xMax,yMax
    
    def getBoundingRectangle(self):
        """returns the smallest Rectangle that fully contains this polygon"""
        xMin,yMin,xMax,yMax = self._getBoundingCoords()
        return Rectangle(Point(xMin,yMin),Point(xMax,yMax))
    
    def getCenter(self):
        """returns the center point of the bounding rectangle that contains this polygon"""
        xMin,yMin,xMax,yMax = self._getBoundingCoords()
        return Point((xMin+xMax)/2,(yMin+yMax)/2)

    def getShapeWidth(self):
        xMin,_,xMax,_ = self._getBoundingCoords()
        return xMax-xMin
    
    def getShapeHeight(self):
        _,yMin,_,yMax = self._getBoundingCoords()
        return yMax-yMin

    def _move(self, dx, dy):
        for p in self.points:
            p.move(dx,dy)
   
    def _draw(self, canvas, options):
        args = [canvas]
        for p in self.points:
            x,y = canvas.toScreen(p.x,p.y)
            args.append(x)
            args.append(y)
        args.append(options)
        return GraphWin.create_polygon(*args) 

    def _updateScreenPoints(self):
        newPointCoords = []
        for p in self.points:
            xScreen,yScreen = self.canvas.toScreen(p.x,p.y)
            newPointCoords.extend([xScreen,yScreen])
        self.canvas.coords(self.id, newPointCoords)
        
    def _scale(self,scalingFactorX,scalingFactorY):
        """ Resizes the polygon by the given scaling factors."""
        cPt = self.getCenter()
        cx,cy = cPt.x,cPt.y
        newPoints = []
        
        for p in self.points:
            newPx = cx + (p.x - cx) * scalingFactorX
            newPy = cy + (p.y - cy) * scalingFactorY
            newPoints.append(Point(newPx,newPy))

        self.points = newPoints

        if self.canvas and not self.canvas.isClosed():
            self._updateScreenPoints()

    def rotate(self,angleInDegrees):
        """ rotates the polygon by the given angle around its center point
            (positive goes clockwise, negative counter-clockwise)"""
        angleInRadians = _math.radians(angleInDegrees)
        centerPt = self.getCenter()
        cx,cy = centerPt.x,centerPt.y
        newPoints = []
        
        for p in self.points:
            r = _math.sqrt((p.x - cx) ** 2 + (p.y-cy)**2)
            theta = _math.atan2(p.y-cy,p.x-cx) + angleInRadians
            newPx = cx + r * _math.cos(theta)
            newPy = cy + r * _math.sin(theta)
            newPoints.append(Point(newPx,newPy))
        
        self.points = newPoints
        if self.canvas and not self.canvas.isClosed():
            self._updateScreenPoints()
            if self.canvas.autoflush:
                _root.update()

class Text(GraphicsObject):
    
    def __init__(self, p, text):
        GraphicsObject.__init__(self, ["justify","fill","text","font"])
        self.setText(text)
        self.anchor = p.clone()
        self.setFill(_DEFAULT_CONFIG['outline'])
        self.setOutline = self.setFill

    def __repr__(self):
        try:
            return "Text({}, '{}')".format(self.anchor, self.getText())
        except:
            return "Uninitialized Text"
    
    def _draw(self, canvas, options):
        p = self.anchor
        x,y = canvas.toScreen(p.x,p.y)
        return canvas.create_text(x,y,options)
        
    def _move(self, dx, dy):
        self.anchor.move(dx,dy)
        
    def clone(self):
        other = Text(self.anchor, self.config['text'])
        other.config = self.config.copy()
        return other

    def setText(self,text):
        self._reconfig("text", text)
        
    def getText(self):
        return self.config["text"]
            
    def getAnchor(self):
        return self.anchor.clone()

    def getCenter(self):
        return self.getAnchor()

    def setFace(self, face):
        if face in ['helvetica','arial','courier','times roman']:
            _,s,b = self.config['font']
            self._reconfig("font",(face,s,b))
        else:
            raise GraphicsError(_BAD_OPTION)

    def getFace(self):
        f,_,_ = self.config['font']
        return f

    def setSize(self, size):
        if size >= 2:
            f,_,b = self.config['font']
            self._reconfig("font", (f,round(size * _HIDPI_FONT_SCALING_RATIO),b))
        else:
            raise GraphicsError("Font size too small.")

    def getSize(self):
        _,s,_ = self.config['font']
        return s

    def setStyle(self, style):
        if style in ['bold','normal','italic', 'bold italic']:
            f,s,_ = self.config['font']
            self._reconfig("font", (f,s,style))
        else:
            raise GraphicsError(_BAD_OPTION)

    def getStyle(self):
        _,_,b = self.config['font']
        return b

    def setTextColor(self, color):
        self.setFill(color)

    def _scale(self,scalingFactorX,scalingFactorY):
        raise GraphicsError("Cannot scale a Text object - use setSize(...) to change font size instead.")
        

class Entry(GraphicsObject):

    def __init__(self, p, width):
        GraphicsObject.__init__(self, [])
        self.anchor = p.clone()
        #print self.anchor
        self.width = width
        self.text = _tk.StringVar(_root)
        self.text.set("")
        self.fill = "gray"
        self.color = "black"
        self.font = _DEFAULT_CONFIG['font']
        self.entry = None

    def __repr__(self):
        try:
            return "Entry({}, {})".format(self.anchor, self.width)
        except:
            return "Uninitialized Point"

    def _draw(self, canvas, options):
        p = self.anchor
        x,y = canvas.toScreen(p.x,p.y)
        frm = _tk.Frame(canvas.master)
        self.entry = _tk.Entry(frm,
                              width=self.width,
                              textvariable=self.text,
                              bg = self.fill,
                              fg = self.color,
                              font=self.font)
        self.entry.pack()
        #self.setFill(self.fill)
        self.entry.focus_set()
        return canvas.create_window(x,y,window=frm)

    def getText(self):
        return self.text.get()

    def _move(self, dx, dy):
        self.anchor.move(dx,dy)

    def getAnchor(self):
        return self.anchor.clone()

    def getCenter(self):
        return self.getAnchor()

    def clone(self):
        other = Entry(self.anchor, self.width)
        other.config = self.config.copy()
        other.text = _tk.StringVar()
        other.text.set(self.text.get())
        other.fill = self.fill
        return other

    def setText(self, t):
        self.text.set(t)
            
    def setFill(self, color):
        self.fill = color
        if self.entry:
            self.entry.config(bg=color)
            
    def _setFontComponent(self, which, value):
        font = list(self.font)
        font[which] = value
        self.font = tuple(font)
        if self.entry:
            self.entry.config(font=self.font)


    def setFace(self, face):
        if face in ['helvetica','arial','courier','times roman']:
            self._setFontComponent(0, face)
        else:
            raise GraphicsError(_BAD_OPTION)

    def setSize(self, size):
        if size >= 2:
            self._setFontComponent(1,round(size * _HIDPI_FONT_SCALING_RATIO))
        else:
            raise GraphicsError("Font size too small.")

    def setStyle(self, style):
        if style in ['bold','normal','italic', 'bold italic']:
            self._setFontComponent(2,style)
        else:
            raise GraphicsError(_BAD_OPTION)

    def setTextColor(self, color):
        self.color=color
        if self.entry:
            self.entry.config(fg=color)

    def _scale(self,scalingFactorX,scalingFactorY):
        raise GraphicsError("Cannot scale an Entry object - use setSize(...) to change font size instead.")

class Image(GraphicsObject):

    idCount = 0
    imageCache = {} # tk photoimages go here to avoid GC while drawn 
    
    def __init__(self, p, *pixmap):
        GraphicsObject.__init__(self, [])
        self.anchor = p.clone()
        self.imageId = Image.idCount
        Image.idCount = Image.idCount + 1
        if len(pixmap) == 1: # file name provided
            self._setPhotoImage(Image._loadPhotoImageFromFile(pixmap[0]))
            self.possiblyUsingSharedCacheImage = True
        else: # width and height provided
            width, height = pixmap
            self._setPhotoImage(_tk.PhotoImage(master=_root, width=width, height=height))
            self.possiblyUsingSharedCacheImage = False

    def _setPhotoImage(self, photoImg):
        self.img = photoImg
        self.scaleFactorX = 1.0
        self.scaleFactorY = 1.0
        self.originalSizeImage = self.img
        if self.canvas and not self.canvas.isClosed():
            # update img reference, so even if this object gets GC'd, canvas can still draw it
            self.imageCache[self.imageId] = self.img 
            self.canvas.itemconfig(self.id, image=self.img)
            if self.canvas.autoflush:
                _root.update()

    def __repr__(self):
        try:
            return "Image({}, {}, {})".format(self.anchor, self.getWidth(), self.getHeight())
        except:
            return "Uninitialized Image"            
                
    def _draw(self, canvas, options):
        p = self.anchor
        x,y = canvas.toScreen(p.x,p.y)
        self.imageCache[self.imageId] = self.img # save a reference  
        return canvas.create_image(x,y,image=self.img)
    
    def _move(self, dx, dy):
        self.anchor.move(dx,dy)
        
    def undraw(self):
        try:
            del self.imageCache[self.imageId]  # allow gc of tk photoimage
        except KeyError:
            pass
        GraphicsObject.undraw(self)

    def getAnchor(self):
        return self.anchor.clone()
    
    def getCenter(self):
        return self.getAnchor()
        
    def clone(self):
        other = Image(Point(0,0), 0, 0)
        other.img = self.img.copy()
        other.anchor = self.anchor.clone()
        other.config = self.config.copy()
        return other

    def getWidth(self):
        """Returns the width of the image in pixels"""
        return self.img.width() 

    def getHeight(self):
        """Returns the height of the image in pixels"""
        return self.img.height()

    def getShapeWidth(self):
        if self.canvas and not self.canvas.isClosed() and self.canvas.trans:
            # in window coordinate units if drawn on a transformed GraphWin
            return abs(self.canvas.trans.xscale) * self.img.width()
        else:
            return self.img.width() # use pixels if not drawn

    def getShapeHeight(self):
        if self.canvas and not self.canvas.isClosed() and self.canvas.trans:
            # in window coordinate units if drawn on a transformed GraphWin
            return abs(self.canvas.trans.yscale) * self.img.height()
        else:
            return self.img.height() # use pixels if not drawn
    
    def getBoundingRectangle(self):
        """returns the bounding rectangle (in window coordinates) for this Image"""
        width,height = self.getShapeWidth(), self.getShapeHeight()
        p1 = Point(self.anchor.x-width/2,self.anchor.y-height/2)
        p2 = Point(self.anchor.x+width/2,self.anchor.y+height/2)
        return Rectangle(p1,p2)


    def getPixel(self, x, y):
        """Returns a list [r,g,b] with the RGB color values for pixel (x,y)
        r,g,b are in range(256)

        """
        
        value = self.img.get(x,y) 
        if type(value) ==  type(0):
            return [value, value, value]
        elif type(value) == type((0,0,0)):
            return list(value)
        else:
            return list(map(int, value.split())) 

    def setPixel(self, x, y, color):
        """Sets pixel (x,y) to the given color
        
        """
        if self.possiblyUsingSharedCacheImage and (self.img is self.originalSizeImage):
            self._setPhotoImage(self.img.copy())
            self.possiblyUsingSharedCacheImage = False
            
        self.img.put("{" + color +"}", (x, y))
         # if the image gets modified, we'll have to rescale the image from the current image, instead of the original loaded image.
        self.originalSizeImage = self.img
        self.scaleFactorX = 1.0
        self.scaleFactorY = 1.0

    def save(self, filename):
        """Saves the pixmap image to filename.
        The format for the save image is determined from the filname extension.

        """
        
        _, name = _os.path.split(filename)
        ext = name.split(".")[-1]
        self.img.write( filename, format=ext)

    def load(self, imageFileName):
        """loads file imageFileName to be displayed by this Image object."""
        
        self._setPhotoImage(Image._loadPhotoImageFromFile(imageFileName))
        self.possiblyUsingSharedCacheImage = True

    ## Helper function for loading & caching images from files
    @staticmethod
    @_functools.lru_cache(40)
    def _loadPhotoImageFromFile(filename):
        return _tk.PhotoImage(file=filename, master=_root)

    ## Helper function for resizing images (approximately)
    # since TK only allows integer zooming & integer subsampling (*sigh*)
    @staticmethod
    @_functools.lru_cache(1)
    def _generateFractionLookupTable(numeratorLimit,denominatorLimit):
        uniqueFractions = set()
        lookup=[]

        for num in range(1,numeratorLimit+1):
            for den in range(1,denominatorLimit+1):
                comDivisor = _math.gcd(num,den)
                a = num // comDivisor
                b = den // comDivisor
                if (a,b) not in uniqueFractions:
                    uniqueFractions.add((a,b))
                    lookup.append((a/b, (a,b)))
        
        floats,fractions = zip(*sorted(lookup))
        return floats,fractions
        
    ## Helper function for resizing images (approximately)
    # since TK only allows integer zooming & integer subsampling (*sigh*)
    @staticmethod
    def _chooseClosestUsableFraction(scaleFactor):
        if scaleFactor == 0:
            return (0,1)
        if scaleFactor > 100:
            raise GraphicsError("Image does not support scaling larger than a factor of 100")
        if scaleFactor > 20:
            return (round(scaleFactor), 1)
        if 1 / scaleFactor > 40:
            return (1, round(1/scaleFactor))
        if float(scaleFactor).is_integer():
            return (int(scaleFactor),1)
        else:
            floats,fractions = Image._generateFractionLookupTable(20,40)
            minIndex = min(range(len(floats)), key = lambda i: abs(floats[i]-scaleFactor))
            return fractions[minIndex]        

    @staticmethod
    def _tkFlip(img, flipX, flipY):
        """returns a potentially flipped version of the tk PhotoImage, depending
           on whether flipX and flipY are True/False"""
        if not flipX and not flipY:
            return img

        width,height = img.width(),img.height()

        startX, endX, incrementX = (width - 1, -1, -1) if flipX else (0, width, 1)
        startY, endY, incrementY = (height - 1, -1, -1) if flipY else (0, height, 1)

        dataList = []
        transpList = [] #record (x,y) of any transparent pixel
        for y in range(startY, endY, incrementY):
            dataList.append("{")
            for x in range(startX, endX, incrementX):
                dataList.append("#%02x%02x%02x " % img.get(x, y))
                if img.tk.call(img.name, "transparency", "get",x, y):
                    newX = width - 1 - x if flipX else x
                    newY = height - 1 - y if flipY else y
                    transpList.append((newX,newY))

            dataList.append("} ")
        flippedImg = _tk.PhotoImage(width=width,height=height)
        flippedImg.put(''.join(dataList), to=(0,0,width,height))
        #set transparency on all the pixels
        for x,y in transpList:
            flippedImg.tk.call(flippedImg.name, "transparency", "set", x, y,True)
                
        return flippedImg

    #@staticmethod
    #def _tkRotate(img, angle):
        #"""returns a rotated tk.PhotoImage object -90 or +90 degrees"""
        #angle = angle % 360 #note -90 % 360 -> 270 in Python
        #if angle not in [-90, 90]:
        #    raise GraphicsError("Can only rotate Images -90 or +90 degrees")
        # TODO: modify the _tkFlip approach above, or see answers at:
        #  https://stackoverflow.com/questions/41248426/how-to-rotate-an-image-on-a-canvas-without-using-pil

    def _scale(self,scalingFactorX,scalingFactorY):
        """ Resizes the image by the given scalingFactor.
        
        Caveat: resizing images can be very SLOW.  
        Also, the performance is unpredictable since it depends on the closest 
        usable rational fraction to the scaling ratio.  Scaling by simple factors
         like 2 or 3, or 1/2 or 1/3 will generally be fastest, and smaller images
         will scale more quickly.        
        
        """
        self.scaleFactorX *= scalingFactorX
        self.scaleFactorY *= scalingFactorY
        numX,denX = Image._chooseClosestUsableFraction(abs(self.scaleFactorX))
        numY,denY = Image._chooseClosestUsableFraction(abs(self.scaleFactorY))
        flipX = (self.scaleFactorX < 0)
        flipY = (self.scaleFactorY < 0)
        if numX == 1 and denX == 1 and numY == 1 and denY == 1:
            self.img = self.originalSizeImage
        elif numX == 1 and numY == 1:
            self.img = self.originalSizeImage.subsample(denX, denY)
        elif denX == 1 and denY == 1:
            self.img = self.originalSizeImage.zoom(numX, numY)
        else:
            self.img = self.originalSizeImage.zoom(numX,numY).subsample(denX,denY)
        
        self.img=Image._tkFlip(self.img,flipX,flipY)
        
        if self.canvas and not self.canvas.isClosed():
            # update img reference, so even if this object gets GC'd, canvas can still draw it
            self.imageCache[self.imageId] = self.img 
            self.canvas.itemconfig(self.id, image=self.img)

        
def color_rgb(r,g,b):
    """r,g,b are intensities of red, green, and blue in range(256)
    Returns color specifier string for the resulting color"""
    return "#%02x%02x%02x" % (r,g,b)

def _test():
    win = GraphWin("Test", 800, 800)
    win.setCoords(0,0,10,10)
    t = Text(Point(5,5), "Centered Text")
    t.draw(win)
    p = Polygon(Point(1,1), Point(5,3), Point(2,7))
    p.draw(win)
    e = Entry(Point(5,6), 10)
    e.draw(win)
    win.getMouse()
    p.setFill("red")
    p.setOutline("blue")
    p.setWidth(2)
    s = ""
    for pt in p.getPoints():
        s = s + "(%0.1f,%0.1f) " % (pt.getX(), pt.getY())
    t.setText(e.getText())
    e.setFill("green")
    e.setText("Spam!")
    e.move(2,0)
    win.getMouse()
    p.move(2,3)
    s = ""
    for pt in p.getPoints():
        s = s + "(%0.1f,%0.1f) " % (pt.getX(), pt.getY())
    t.setText(s)
    win.getMouse()
    p.undraw()
    e.undraw()
    t.setStyle("bold")
    win.getMouse()
    t.setStyle("normal")
    win.getMouse()
    t.setStyle("italic")
    win.getMouse()
    t.setStyle("bold italic")
    win.getMouse()
    t.setSize(14)
    win.getMouse()
    t.setFace("arial")
    t.setSize(20)
    win.getMouse()
    win.close()

#MacOS fix 2
#_tk.Toplevel(_root).destroy()

# MacOS fix 1
update()

if __name__ == "__main__":
    _test()
