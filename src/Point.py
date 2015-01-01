'''
Created on Dec 6, 2014
@author: chris joseph

This class represents a single point in the plane. A point has an x and a y
coordinate. Also, the point has references to 'next' and 'prev', which are its
immediate neighbors. This is necessary when creating the linked-list structure
to represent a polygon.

Other attributes:
ear: Boolean value indicating or not this vertex is an ear of the polygon
name: a string/integer, used to identify a vertex
'''

class Point:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ear = False
        self.name = -1
        self.next = None
        self.prev = None
        
        
    def ___str___(self):
        return self.name
    
    
    '''
    Compares this point to the given point. Only the x and y coordinates are compared.
    '''
    def equals(self, p):
        if p.x == self.x and p.y == self.y:
            return True
        return False
    

    '''
    Multiplies this point's x by k1 and y by k2.
    '''
    def scale(self, k1, k2):
        self.x = int(self.x * k1)
        self.y = int(self.y * k2)