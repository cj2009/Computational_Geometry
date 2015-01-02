'''
Created on Dec 6, 2014
@author: chris joseph

This class handles some input/output. It reads input from file, parses the points,
creates a linked-list that represents a polygon, etc.
'''
from Point import Point
import sys

'''
This function compares each Point object to every other Point object in the 
given list and removes any duplicates. Only the x and y coordinates are 
compared.

@param listofpoints: A list of Point objects.
'''
def removeDuplicates(listofpoints):
    length = len(listofpoints)
    i = 0
    j = 0
    
    while i < length - 1:
        j = i + 1
        while j < length:
            p1 = listofpoints[i]
            p2 = listofpoints[j]
            if p1.equals(p2):
                length -= 1
                listofpoints.remove(p2)
            else:
                j += 1
        i += 1
        

'''
This function takes in the name of an input file, opens it, reads the list of
points and creates a linked-list structure out of it. The linked-list structure
will represent the polygon's points in counterclockwise order.

Thi input file should be in the following format: The first line is n (the 
number of points); each of the subsequent lines should be the coordinates of a 
single point, in the form [Xi,Yi], where Xi and Yi are integers. Therefore the 
file should have a total of n+1 lines.

@return: Reference to the head of the linked-list and n (number of points)
'''
def createLinkedList(filename = 'input.txt'):
    
    # Open a file object, read the contents and create a list out of the input points:
    inputfile = open(filename, 'r')                     # 'r' for read-only mode
    # The first line should be the number of points:
    n = int(inputfile.readline())
    
    
    
    # Then read all the points and store them in a list:
    list1 = [x for x in inputfile.readlines()]
    inputfile.close()

    
    # The size of the list must match the number that was specified:
    if n is not len(list1):
        return None, 0
    
    # Go through the list and check the input for any inconsistencies
    for x in list1:
        if len(x) < 2:
            return None, 0                      # Something wrong with the input
        x = x.strip()
    
    
    points = []
    # Go thru the list and remove the '[' and ']' signs, and create Point
    # objects using the x and y coordinates:
    for i in range(n):
        p = list(list1[i])
        p.remove('[')
        p.remove(']')
        p = "".join(p)
        p = p.split(',')
        x = int(p[0])
        y = int(p[1])
        # construct a Point object:
        pt = Point(x, y)
        points.append(pt)

        
    # Remove any duplicate points from the list:
    removeDuplicates(points)
    
    
    # This list is now treated as the points that comprise the polygon, in
    # counterclockwise order. Use this to create the linked-list structure:
    firstPoint = points[0]
    lastPoint = points[len(points) - 1]
    for i in range(len(points) - 1):
        p1 = points[i]
        p2 = points[i+1]
        
        # Link them together:
        p1.next = p2
        p2.prev = p1
        
        
    # To complete the structure, link the first and last vertices together to
    # create a circular linked-list:
    firstPoint.prev = lastPoint
    lastPoint.next = firstPoint
    
    
    # Also, give the Points simple names to help out with visualization/debugging:
    for i in range(len(points)):
        points[i].name = str(i + 1)
        
    return firstPoint, len(points)



'''
Behaves exactly like the C library function printf.
'''
def printf(format, *args):
    sys.stdout.write(format % args)


'''
Prints the number of triangles and the three vertices of each triangle on each
line.
'''
def printTrianglesToConsole(triangles):
    printf("%d", len(triangles))
    for i in range(len(triangles)):
        t = triangles[i]
        printf("\n[%s,%s,%s]", t[0], t[1], t[2])