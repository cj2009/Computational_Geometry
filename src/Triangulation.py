'''
Created on Dec 5, 2014
@author: Chris Joseph, Joseph O'Rourke (see below)

This class represents a Triangulation object. The methods in this class can be
used to take a polygon and triangulate it. There are also methods for drawing the
polygon and/or triangulations on a Tkinter canvas.

Triangulation objects have two instance variables: HEAD and SIZE

HEAD is the reference to the head node of a polygon. The polygon should be a
circularly-linked list of Point objects, representing the vertices in CCW order.

SIZE is the number of nodes in the linked list.

The mathematical functions for performing the triangulation (such as Left, 
LeftOn, Intersect, IntersectProp, etc. ) are adapted from the textbook 
'Computational Geometry in C' by O'Rourke. These functions in my project are 
translations of the the author's C code into Python.

'''
import Tkinter
from Point import Point
import IOClass
class Triangulation:


    def __init__(self, head = None, size = 0):
        self.HEAD = head
        self.SIZE = size
        
        
    '''
    Creates a copy of the linked list of points.
    @return: Reference to the head of the new linked list and n (number of 
            points)
    '''
    def cloneLinkedList(self):
        cursor = self.HEAD
        
        # make a copy of the head first:
        newHead = Point(cursor.x, cursor.y)
        newHead.ear = cursor.ear
        newHead.name = cursor.name
        
        # use a loop to create clones of the rest of the points:
        cursor = cursor.next
        newCursor = newHead
        while cursor is not self.HEAD:
            newPoint = Point(cursor.x, cursor.y)
            newPoint.ear = cursor.ear
            newPoint.name = cursor.name
            
            # link the previous point to the new one:
            newCursor.next = newPoint
            newPoint.prev = newCursor
            
            cursor = cursor.next
            newCursor = newPoint           # same as: newCursor = newCursor.next

        # finally, link the new head and tail before returning the head:
        newHead.prev = newCursor
        newCursor.next = newHead
        return newHead, self.SIZE


    '''
    Adapted from O'Rourke. This function actually returns twice the area of the 
    triangle defined by points a, b and c. The area calculation is based on the 
    determinant method (signed area).
    '''
    def Area2(self, a, b, c):
        return ((b.x - a.x) * (c.y - a.y)) - ((c.x - a.x) * (b.y - a.y))


    '''
    A convenience function that performs Xor on the two arguments
    '''
    def Xor(self, x, y):
        return x is not y


    '''
    Adapted from O'Rourke. This is another convenient function that returns 1,
    -1 or 0 depending on whether the area of the triangle a,b,c is positive,
    negative or zero, respectively.
    '''
    def AreaSign(self, a, b, c):
        # Multiplication by 1.0 is to force conversion to float
        a1 = (b.x - a.x) * 1.0 * (c.y - a.y)
        a2 = (c.x - a.x) * 1.0 * (b.y - a.y)

        area2 = a1 - a2

        if area2 > 0.5:
            return 1
        if area2 < -0.5:
            return -1
        return 0


    '''
    Adapted from O'Rourke.
    '''
    def Left(self, a,b,c):
        return self.AreaSign(a,b,c) > 0


    '''
    Adapted from O'Rourke.
    '''
    def LeftOn(self, a,b,c):
        return self.AreaSign(a,b,c) >= 0


    '''
    Adapted from O'Rourke. Checks if points a,b,c are collinear by performing
    a quick area calculation of the triangle a,b,c.
    '''
    def Collinear(self, a,b,c):
        return self.AreaSign(a,b,c) == 0


    '''
    Adapted from O'Rourke. Checks if point c is geometrically in between 
    points a and b. In between means either in terms of x or y coordinate 
    ranges.
    '''
    def Between(self, a, b, c):
        if not self.Collinear(a, b, c):
            return False

        if a.x != b.x:
            return (a.x <= c.x and c.x <= b.x) or (a.x >= c.x and c.x >= b.x)

        else:
            return (a.y <= c.y and c.y <= b.y) or (a.y >= c.y and c.y >= b.y)


    '''
    Adapted from O'Rourke. Returns true if the line segment a,b intersects the 
    line segment c,d.
    '''
    def Intersect(self, a, b, c , d):
        if self.IntersectProp(a, b, c, d):
            return True
        elif self.Between(a, b, c) or self.Between(a, b, d) or self.Between(c, 
            d, a) or self.Between(c, d, b):
            return True
        return False


    '''
    Adapted from O'Rourke. Returns true if the line segment a,b is a diagonal 
    of the polygon.
    '''
    def Diagonalie(self, a, b, HEAD):
        c = HEAD
        c1 = None

        while True:
            c1 = c.next
            if (c is not a) and (c1 is not a) and (c is not b) and (c1 is not 
                b) and self.Intersect(a, b, c, c1):
                return False
            c = c.next
            if c is HEAD:
                break
        return True



    '''
    Adapted from O'Rourke. Returns true if the line segments a,b and c,d 
    intersect "properly." A proper intersection is when the two segments fully 
    cross each other. If one segment's endpoint lies on the other segment, it's 
    not considered a proper intersection.
    '''
    def IntersectProp(self, a, b, c, d):
        if self.Collinear(a,b,c) or self.Collinear(a,b,d) or self.Collinear(c,d,a) or self.Collinear(c,d,b):
            return False

        return self.Xor(self.Left(a,b,c), self.Left(a,b,d)) and self.Xor(self.Left(c,d,a) , self.Left(c,d,b))


    '''
    Adapted from O'Rourke. This function is needed to distinguish internal 
    diagonals from the external ones.
    '''
    def InCone(self, a, b):
        a0 = None
        a1 = None

        a1 = a.next
        a0 = a.prev

        if self.LeftOn(a, a1, a0):
            return self.Left(a,b,a0) and self.Left(b,a,a1)
        else:
            return not (self.LeftOn(a,b,a1) and self.Left(b,a,a0))


    '''
    Adapted from O'Rourke. 
    '''
    def Diagonal(self, a, b, HEAD):
        return self.InCone(a,b) and self.InCone(b, a) and self.Diagonalie(a, 
            b, HEAD)



    '''
    Adapted from O'Rourke. This function must be called initially before the 
    triangulation is performed, because the ear status of each vertex must be
    initialized before triangulation can take place.
    '''
    def EarInit(self, HEAD):
        v0 = None
        v1 = None
        v2 = None

        v1 = HEAD
        while True:
            v2 = v1.next
            v0 = v1.prev
            v1.ear = self.Diagonal(v0, v2, HEAD)
            v1 = v1.next

            if v1 is HEAD:
                break

    '''
    This is the actual triangulation function, which makes use of all the helper
    functions defined above. Note that since the linked list will be
    destroyed during the triangulation process (since the polygon's ears are
    clipped off), a new linked list is created so that the original linked 
    list is preserved.
    
    @return: A list of 3-tuples. Each 3-tuple is of the form [v1, v2, v3], 
            which represents a triangle. All of these tuples, taken together,
            represents the triangulated polygon.
            
    Note that the return value can be modified easily so that some other values 
    of the polygon can be returned instead - for example, the coordinates of 
    the triangles or the Point objects themselves.
    '''
    def Triangulate(self):
        v0 = None
        v1 = None
        v2 = None
        v3 = None
        v4 = None
        earfound = False
        returnlist = []

        self.EarInit(self.HEAD)
        # Create a clone of the linked list just before starting the 
        # triangulation process:
        HEAD, n = self.cloneLinkedList()
        
        # Each step of the outer loop clips off one ear
        while n > 3:
            v2 = HEAD
            earfound = False
            while True:
                if v2.ear:
                    earfound = True
                    # Ear found
                    v3 = v2.next
                    v4 = v3.next
                    v1 = v2.prev
                    v0 = v1.prev


                    # v1,v3 is a diagonal
                    tri = [v1.name, v2.name, v3.name]
                    returnlist.append(tri)

                    # Update the ear status of the diagonal endpoints:
                    v1.ear = self.Diagonal(v0, v3, HEAD)
                    v3.ear = self.Diagonal(v1, v4, HEAD)

                    # Cut off the ear v2:
                    v1.next = v3
                    v3.prev = v1
                    HEAD = v3
                    n -= 1
                    
                    
                    if n == 3:
                        # the polygon has been reduced down to 3 vertices, so
                        # output that as the last triangulation and return:
                        v2 = HEAD
                        v1 = v2.prev
                        v3 = v2.next
                        tri = [v1.name, v2.name, v3.name]
                        returnlist.append(tri)
                        return returnlist
                    
                    
                    break
                v2 = v2.next
                if v2 is HEAD:
                    break

            if not earfound:
                print("Error! Ear not found")
                break
        return returnlist



    '''
    This function draws the polygon on a canvas and displays them. This is done 
    by simply drawing lines between consecutive points. Also, small dots are 
    drawn for easy identification of the vertices, and a small text label is
    also drawn next to each vertex (this text is the name of each Point object).
    
    @param canvas: The Tkinter Canvas widget on which to draw the polygon
    '''
    def drawPolygon(self, canvas):
            
        # Draw the polygon as a collection of lines:
        cursor = self.HEAD
        while True:
            x1 = cursor.x
            y1 = cursor.y
            x2 = cursor.next.x
            y2 = cursor.next.y
            
            # First, draw text labels. Labels will be placed next to each vertex.
            label = Tkinter.Label(canvas, text = cursor.name, font = "Times 8")
            label.place(x = x1 + 5, y = 700 - (y1 + 5))
            
            # Draw a line from the current vertex to the next vertex:
            canvas.create_line(x1, 700 - y1, x2, 700 - y2, width = 2.0, fill = 'black')
            
            # Finally, draw a little dot at the vertex:
            canvas.create_oval(x1 - 4, 700 - (y1 - 4), x1 + 4, 700 - (y1 + 4), fill = 'black')
            
            cursor = cursor.next
            if cursor.equals(self.HEAD):
                break
            
            
            
    '''
    This function draws triangles, after a polygon is triangulated.
    
    @param canvas: A Tkinter Canvas widget on which to draw the triangles
    @param triangles: This should be the return value of the 'Triangulate' function
    
    The function draws triangles by simply drawing lines between the 3 points 
    of each triangle.
    '''
    def drawTriangles(self, canvas, triangles):
        # It's convenient to have the points as a list instead of a linked list:
        pointlist = []
        cursor = self.HEAD
        while True:
            pointlist.append(cursor)
            cursor = cursor.next
            if cursor.equals(self.HEAD):
                break
        
        
        # The triangulation output is a list of triangles, where each triangle 
        # is specified by the indices of 3 points. Get those 3 points from the
        # 'pointlist' and draw lines between them:
        if len(triangles) > 0:
            for t in triangles:
                # Find the 3 vertices with the matching indices:
                p0 = pointlist[ int( t[0] ) - 1 ]
                p1 = pointlist[ int( t[1] ) - 1 ]
                p2 = pointlist[ int( t[2] ) - 1 ]
                
                # Draw the 3 lines:
                canvas.create_line(p0.x, 700 - p0.y, p1.x, 700 - p1.y, 
                                   width = 1.0, fill = 'red')
                canvas.create_line(p0.x, 700 - p0.y, p2.x, 700 - p2.y, 
                                   width = 1.0, fill = 'red')
                canvas.create_line(p2.x, 700 - p2.y, p1.x, 700 - p1.y, 
                                   width = 1.0, fill = 'red')
                



    '''
    This method does some translating and scaling so that the polygon is displayed
    nicely on the canvas.
    
    First, all points are translated so that the point with the minimum x-coordinate
    is very close to the y-axis, and the point with the minimum y-coordinate is
    very close to the x-axis (about 10 pixels). No points will have negative
    coordinates after this translation.
    
    What this translation does is make all points very close to the x and y axes
    in the first quadrant of the plane.
    
    Then, each point's x and y values are multiplied by two scaling factors 
    k1 and k2, respectively. These are calculated such that the most extreme
    points will still remain inside the canvas after they're scaled.
    
    
    @param uniform: True if x and y coordinates should be scaled by the same 
    factor. If True, both x and y will be scaled by min(k1, k2).
    '''
    def scale(self, uniform = False):
        xmin = 1000000000                      # Initialize to some huge numbers
        ymin = 1000000000
    
        
        # Traverse the list and find the smallest x and y values:
        cursor = self.HEAD
        while True:
            if cursor.x < xmin:
                xmin = cursor.x
            if cursor.y < ymin:
                ymin = cursor.y
            cursor = cursor.next
            if cursor.equals(self.HEAD):
                break
            
            
        # The following loop translates all x- and y-values to make them all positive
        # (in order to make them as close to the origin as possible):
        cursor = self.HEAD
        while True:
            cursor.x = cursor.x - xmin + 10
            cursor.y = cursor.y - ymin + 10
            cursor = cursor.next
            if cursor.equals(self.HEAD):
                break
    
    
        # Find the new xmin and ymin, and also xmax and ymax:
        xmin = 1000000000
        ymin = 1000000000
        xmax = 0
        ymax = 0
        cursor = self.HEAD
        while True:
            if cursor.x < xmin:
                xmin = cursor.x
            if cursor.y < ymin:
                ymin = cursor.y
            if cursor.x > xmax:
                xmax = cursor.x
            if cursor.y > ymax:
                ymax = cursor.y
                
            cursor = cursor.next
            if cursor.equals(self.HEAD):
                break
            
        # Find the scaling factor:
        # 1250 and 690 are based on the canvas dimensions (1280 x 720)
        k1 = 1250.0 / xmax
        k2 = 690.0 / ymax
        
    
        if uniform:
            # Set both k1 and k2 to be min(k1, k2)
            if k1 < k2:
                k2 = k1
            else:
                k1 = k2
            
            
        # Multiply each point by the scaling factor:
        cursor = self.HEAD
        while True:
            cursor.scale(k1, k2)
            cursor = cursor.next
            if cursor.equals(self.HEAD):
                break
        
            