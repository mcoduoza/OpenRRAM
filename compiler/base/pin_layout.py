import debug
from tech import GDS, drc
from vector import vector
from tech import layer

class pin_layout:
    """
    A class to represent a rectangular design pin. It is limited to a
    single shape.
    """

    def __init__(self, name, rect, layer_name_num):
        self.name = name
        # repack the rect as a vector, just in case
        if type(rect[0])==vector:
            self.rect = rect
        else:
            self.rect = [vector(rect[0]),vector(rect[1])]
        # snap the rect to the grid
        self.rect = [x.snap_to_grid() for x in self.rect]
        # if it's a layer number look up the layer name. this assumes a unique layer number.
        if type(layer_name_num)==int:
            self.layer = list(layer.keys())[list(layer.values()).index(layer_name_num)]
        else:
            self.layer=layer_name_num
        self.layer_num = layer[self.layer]

    def __str__(self):
        """ override print function output """
        return "({} layer={} ll={} ur={})".format(self.name,self.layer,self.rect[0],self.rect[1])

    def __repr__(self):
        """ 
        override repr function output (don't include 
        name since pin shapes could have same shape but diff name e.g. blockage vs A)
        """
        return "(layer={} ll={} ur={})".format(self.layer,self.rect[0],self.rect[1])

    def __hash__(self):
        """ Implement the hash function for sets etc. """
        return hash(repr(self))
    
    def __lt__(self, other):
        """ Provide a function for ordering items by the ll point """
        (ll, ur) = self.rect
        (oll, our) = other.rect
        
        if ll.x < oll.x and ll.y < oll.y:
            return True
            
        return False
    
    def __eq__(self, other):
        """ Check if these are the same pins for duplicate checks """
        if isinstance(other, self.__class__):
            return (self.layer==other.layer and self.rect == other.rect)
        else:
            return False    

    def inflate(self, spacing=None):
        """ 
        Inflate the rectangle by the spacing (or other rule) 
        and return the new rectangle. 
        """
        if not spacing:
            spacing = drc["{0}_to_{0}".format(self.layer)]
            
        (ll,ur) = self.rect
        spacing = vector(spacing, spacing)
        newll = ll - spacing
        newur = ur + spacing
        
        return (newll, newur)

    def intersection(self, other):
        """ Check if a shape overlaps with a rectangle  """
        (ll,ur) = self.rect
        (oll,our) = other.rect

        min_x = max(ll.x, oll.x)
        max_x = min(ll.x, oll.x)
        min_y = max(ll.y, oll.y)
        max_y = min(ll.y, oll.y)

        return [vector(min_x,min_y),vector(max_x,max_y)]
    
    def overlaps(self, other):
        """ Check if a shape overlaps with a rectangle  """
        (ll,ur) = self.rect
        (oll,our) = other.rect

        # Can only overlap on the same layer
        if self.layer != other.layer:
            return False
        
        # Start assuming no overlaps
        x_overlaps = False
        y_overlaps = False
        # check if self is within other x range
        if (ll.x >= oll.x and ll.x <= our.x) or (ur.x >= oll.x and ur.x <= our.x):
            x_overlaps = True
        # check if other is within self x range
        if (oll.x >= ll.x and oll.x <= ur.x) or (our.x >= ll.x and our.x <= ur.x):
            x_overlaps = True
            
        # check if self is within other y range
        if (ll.y >= oll.y and ll.y <= our.y) or (ur.y >= oll.y and ur.y <= our.y):
            y_overlaps = True
        # check if other is within self y range
        if (oll.y >= ll.y and oll.y <= ur.y) or (our.y >= ll.y and our.y <= ur.y):
            y_overlaps = True

        return x_overlaps and y_overlaps
    
    def height(self):
        """ Return height. Abs is for pre-normalized value."""
        return abs(self.rect[1].y-self.rect[0].y)
    
    def width(self):
        """ Return width. Abs is for pre-normalized value."""
        return abs(self.rect[1].x-self.rect[0].x)

    def normalize(self):
        """ Re-find the LL and UR points after a transform """
        (first,second)=self.rect
        ll = vector(min(first[0],second[0]),min(first[1],second[1]))
        ur = vector(max(first[0],second[0]),max(first[1],second[1]))
        self.rect=[ll,ur]
        
    def transform(self,offset,mirror,rotate):
        """ Transform with offset, mirror and rotation to get the absolute pin location. 
        We must then re-find the ll and ur. The master is the cell instance. """
        (ll,ur) = self.rect
        if mirror=="MX":
            ll=ll.scale(1,-1)
            ur=ur.scale(1,-1)
        elif mirror=="MY":
            ll=ll.scale(-1,1)
            ur=ur.scale(-1,1)
        elif mirror=="XY":
            ll=ll.scale(-1,-1)
            ur=ur.scale(-1,-1)
            
        if rotate==90:
            ll=ll.rotate_scale(-1,1)
            ur=ur.rotate_scale(-1,1)
        elif rotate==180:
            ll=ll.scale(-1,-1)
            ur=ur.scale(-1,-1)
        elif rotate==270:
            ll=ll.rotate_scale(1,-1)
            ur=ur.rotate_scale(1,-1)

        self.rect=[offset+ll,offset+ur]
        self.normalize()

    def center(self):
        return vector(0.5*(self.rect[0].x+self.rect[1].x),0.5*(self.rect[0].y+self.rect[1].y))

    def cx(self):
        """ Center x """
        return 0.5*(self.rect[0].x+self.rect[1].x)

    def cy(self):
        """ Center y """
        return 0.5*(self.rect[0].y+self.rect[1].y)
    
    # The four possible corners
    def ll(self):
        """ Lower left point """
        return self.rect[0]

    def ul(self):
        """ Upper left point """
        return vector(self.rect[0].x,self.rect[1].y)

    def lr(self):
        """ Lower right point """
        return vector(self.rect[1].x,self.rect[0].y)

    def ur(self):
        """ Upper right point """
        return self.rect[1]
    
    # The possible y edge values 
    def uy(self):
        """ Upper y value """
        return self.rect[1].y

    def by(self):
        """ Bottom y value """
        return self.rect[0].y

    # The possible x edge values
    
    def lx(self):
        """ Left x value """
        return self.rect[0].x
    
    def rx(self):
        """ Right x value """
        return self.rect[1].x
    
    
    # The edge centers
    def rc(self):
        """ Right center point """
        return vector(self.rect[1].x,0.5*(self.rect[0].y+self.rect[1].y))

    def lc(self):
        """ Left center point """
        return vector(self.rect[0].x,0.5*(self.rect[0].y+self.rect[1].y))
    
    def uc(self):
        """ Upper center point """
        return vector(0.5*(self.rect[0].x+self.rect[1].x),self.rect[1].y)

    def bc(self):
        """ Bottom center point """
        return vector(0.5*(self.rect[0].x+self.rect[1].x),self.rect[0].y)


    def gds_write_file(self, newLayout):
        """Writes the pin shape and label to GDS"""
        debug.info(4, "writing pin (" + str(self.layer) + "):" 
                   + str(self.width()) + "x" + str(self.height()) + " @ " + str(self.ll()))
        newLayout.addBox(layerNumber=layer[self.layer],
                         purposeNumber=0,
                         offsetInMicrons=self.ll(),
                         width=self.width(),
                         height=self.height(),
                         center=False)
        # Add the tet in the middle of the pin.
        # This fixes some pin label offsetting when GDS gets imported into Magic.
        newLayout.addText(text=self.name,
                          layerNumber=layer[self.layer],
                          purposeNumber=0,
                          offsetInMicrons=self.center(),
                          magnification=GDS["zoom"],
                          rotate=None)
    
