from Triangulation import Triangulation
import Tkinter            # May need to change 'Tkinter' to 'tkinter' on Windows
import IOClass
'''
Created on Nov 17, 2014
@author: chris joseph
'''



def main():
    FILENAME = 'input1.txt'

    # Open the file from disk, read the points and create a linked-list
    # structure that represents the Polygon:
    headnode1, size1 = IOClass.createLinkedList(FILENAME)


    # Check if the file reading was successful or if there were inconsistencies:
    if not headnode1 or size1 < 3:
        print("No triangulations to output")
        return

    # Create a Triangulation object from the linked list:
    t1 = Triangulation()
    t1.HEAD = headnode1
    t1.SIZE = size1
    
    
    # Create a copy of the linked list and use that to create a new 
    # Triangulation object. This is an identical copy, but it will be scaled
    # and translated in order to be graphed on the canvas.
    headnode2, size2 = t1.cloneLinkedList()
    t2 = Triangulation()
    t2.HEAD = headnode2
    t2.SIZE = size2
    t2.scale(True)
    t2.scale(True)
    # The scaling is just to make the polygon look better when viewing on a 
    # canvas. Doing it multiple times is inefficient but makes the picture 
    # better.


    # Do the triangulation. The return value is a list of 3-tuples, which 
    # represent the vertices of each triangle.
    triangles1 = t1.Triangulate()
    triangles2 = t2.Triangulate()

    # Now for the GUI. Both the polygon and its triangulation have been scaled,
    # as specified above. Now we need to draw them on a Tkinter Canvas.
    # Setup and init a canvas:
    canvas_width = 1280
    canvas_height = 720
    master = Tkinter.Tk()
    canvas = Tkinter.Canvas(master, width=canvas_width, height=canvas_height)
    canvas.pack()


    t2.drawTriangles(canvas, triangles2)
    t2.drawPolygon(canvas)


    # The last step is to output the triangulation of the original, non-scaled
    # polygon to the console:
    IOClass.printTrianglesToConsole(triangles1)


    # Display the canvas:
    Tkinter.mainloop()


main()
