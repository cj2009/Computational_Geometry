'''
Created on Dec 5, 2014
@author: chris joseph

This class represents a Triangulation object. The methods in this class can be
used to take a polygon and triangulate it. There are also methods for drawing the
polygon and/or triangulations on a Tkinter canvas.

Triangulation objects have two instance variables: HEAD and SIZE

HEAD is the reference to the head node of a polygon. The polygon should be a
circularly-linked list of Point objects, representing the vertices in CCW order.

SIZE is the number of nodes in the linked list.

Note: after a polygon is triangulated, its linked list will be broken by the 
triangulating algorithm (due to clipping off the ears)

'''
import Tkinter
class Triangulation:


    def __init__(self, head = None, size = 0):
        self.HEAD = head
        self.SIZE = size


    def Area2(self, a, b, c):
        return ((b.x - a.x) * (c.y - a.y)) - ((c.x - a.x) * (b.y - a.y))

    def Xor(self, x, y):
        return x is not y



    def AreaSign(self, a, b, c):
        a1 = (b.x - a.x) * 1.0 * (c.y - a.y)
        a2 = (c.x - a.x) * 1.0 * (b.y - a.y)

        area2 = a1 - a2

        if area2 > 0.5:
            return 1
        if area2 < -0.5:
            return -1
        return 0


    def Left(self, a,b,c):
        return self.AreaSign(a,b,c) > 0

    def LeftOn(self, a,b,c):
        return self.AreaSign(a,b,c) >= 0

    def Collinear(self, a,b,c):
        return self.AreaSign(a,b,c) == 0

    def Between(self, a, b, c):
        if not self.Collinear(a, b, c):
            return False

        if a.x != b.x:
            return (a.x <= c.x and c.x <= b.x) or (a.x >= c.x and c.x >= b.x)

        else:
            return (a.y <= c.y and c.y <= b.y) or (a.y >= c.y and c.y >= b.y)


    def Intersect(self, a, b, c , d):
        if self.IntersectProp(a, b, c, d):
            return True
        elif self.Between(a, b, c) or self.Between(a, b, d) or self.Between(c, d, a) or self.Between(c, d, b):
            return True
        return False


    def Diagonalie(self, a, b):
        c = self.HEAD
        c1 = None

        while True:
            c1 = c.next
            if (c is not a) and (c1 is not a) and (c is not b) and (c1 is not b) and self.Intersect(a, b, c, c1):
                return False
            c = c.next
            if c is self.HEAD:
                break
        return True



    def IntersectProp(self, a, b, c, d):
        if self.Collinear(a,b,c) or self.Collinear(a,b,d) or self.Collinear(c,d,a) or self.Collinear(c,d,b):
            return False

        return self.Xor(self.Left(a,b,c), self.Left(a,b,d)) and self.Xor(self.Left(c,d,a) , self.Left(c,d,b))


    def InCone(self, a, b):
        a0 = None
        a1 = None

        a1 = a.next
        a0 = a.prev

        if self.LeftOn(a, a1, a0):
            return self.Left(a,b,a0) and self.Left(b,a,a1)
        else:
            return not (self.LeftOn(a,b,a1) and self.Left(b,a,a0))


    def Diagonal(self, a, b):
        return self.InCone(a,b) and self.InCone(b, a) and self.Diagonalie(a, b)


    def EarInit(self):
        v0 = None
        v1 = None
        v2 = None

        v1 = self.HEAD
        while True:
            v2 = v1.next
            v0 = v1.prev
            v1.ear = self.Diagonal(v0, v2)
            v1 = v1.next

            if v1 is self.HEAD:
                break

    def Triangulate(self):
        v0 = None
        v1 = None
        v2 = None
        v3 = None
        v4 = None
        earfound = False
        returnlist = []
        n = self.SIZE

        self.EarInit()
        while n > 3:
            v2 = self.HEAD
            earfound = False
            while True:
                if v2.ear:
                    earfound = True
                    #print(str(v2.name) + " is an ear")

                    # Ear found; fill variables:
                    v3 = v2.next
                    v4 = v3.next
                    v1 = v2.prev
                    v0 = v1.prev


                    # v1,v3 is a diagonal
                    diag = [v1.name, v2.name, v3.name]
                    returnlist.append(diag)

                    # Update earity of diagonal endpoints:
                    v1.ear = self.Diagonal(v0, v3)
                    v3.ear = self.Diagonal(v1, v4)

                    # Cut off the ear v2:
                    v1.next = v3
                    v3.prev = v1
                    self.HEAD = v3
                    n -= 1
                    
                    #### BEGIN SPECIAL CASE
                    #### BEGIN SPECIAL CASE
                    
                    if n == 3:
                        # the polygon has been reduced down to 3 vertices, so
                        # output that as the last triangulation and return:
                        v2 = self.HEAD
                        v1 = v2.prev
                        v3 = v2.next
                        diag = [v1.name, v2.name, v3.name]
                        returnlist.append(diag)
                        return returnlist
                    
                    #### END SPECIAL CASE
                    #### END SPECIAL CASE
                    
                    
                    break
                v2 = v2.next
                if v2 is self.HEAD:
                    break

            if not earfound:
                print("Error! Ear not found")
                break
        return returnlist



    '''
    This function draws the polygon on a canvas and displays them.
    
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
    
    
    Note that since the polygon linked-list will be broken after the triangulation
    is performed, this function cannot be called if the triangulation was already performed. 
    Instead, the 'triangles' parameter should be the return value from
    another identical Triangulation object that did the triangulation.
    '''
    def drawTriangles(self, canvas, triangles):
        
        pointlist = []
        cursor = self.HEAD
        while True:
            pointlist.append(cursor)
            cursor = cursor.next
            if cursor.equals(self.HEAD):
                break
        
        
        if len(triangles) > 0:
            for t in triangles:
                # Find the 3 vertices with the matching indices:
                p0 = pointlist[ int( t[0] ) - 1 ]
                p1 = pointlist[ int( t[1] ) - 1 ]
                p2 = pointlist[ int( t[2] ) - 1 ]
                
                canvas.create_line(p0.x, 700 - p0.y, p1.x, 700 - p1.y, width = 1.0, fill = 'red')
                canvas.create_line(p0.x, 700 - p0.y, p2.x, 700 - p2.y, width = 1.0, fill = 'red')
                canvas.create_line(p2.x, 700 - p2.y, p1.x, 700 - p1.y, width = 1.0, fill = 'red')
                



    '''
    This method does some translating and scaling so that the polygon is displayed
    nicely on the canvas.
    
    First, all points are translated so that the point with the minimum x-coordinate
    is very close to the y-axis, and the point with the minimum y-coordinate is
    very close to the x-axis (about 10 pixels). No points will have negative
    coordinates after this translation.
    
    What this translation does is make all points very close to the x and y axes
    in the first quadrant of the plane.
    
    Then, each point's x and y values are multiplied by k1 and k2, respectively.
    These are the scaling factors. They are calculated such that the most extreme
    points will still remain inside the canvas after they're scaled.
    
    
    @param uniform: True if x and y coordinates should be scaled by the same factor.
    If True, both x and y will be scaled by min(k1, k2).
    '''
    def scale(self, uniform = False):
        xmin = 10000000                           # Initialize to some huge numbers
        ymin = 10000000
    
        
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
        xmin = 100000000
        ymin = 100000000
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
        
            