from Triangulation import Triangulation
import Tkinter                      # May need to change 'Tkinter' to 'tkinter'
import IOClass
'''
Created on Nov 17, 2014
@author: chris joseph
'''





def main():
    FILENAME = 'input.txt'

    # Open the file from disk, read the points and create a linked-list
    # structure that represents the Polygon:
    headnode1, size1 = IOClass.createLinkedList(FILENAME)
    headnode2, size2 = IOClass.createLinkedList(FILENAME)
    headnode3, size3 = IOClass.createLinkedList(FILENAME)
    # 3 copies will be created, which are all the same, because 2 are required
    # for the GUI and 1 for the console output.


    # Check if the file reading was successful or if there were inconsistencies:
    if not headnode1 or size1 < 3:
        print("No triangulations to output")
        return



    # The linked-list will be broken after the triangulation is performed (due to
    # the clipping off of the ears). Therefore 3 Triangulation objects are needed:
    t1 = Triangulation()
    t1.HEAD = headnode1
    t1.SIZE = size1


    t2 = Triangulation()
    t2.HEAD = headnode2
    t2.SIZE = size2
    t2.scale(True)
    t2.scale(True)

    t3 = Triangulation()
    t3.HEAD = headnode3
    t3.SIZE = size3
    t3.scale(True)
    t3.scale(True)

    # The scaling is just to make the polygon look better when viewing on a canvas.
    # Doing it multiple times is inefficient but makes the picture better.


    # Do the triangulation. The return value is a list of 3-tuples, which represent
    # the vertices of each triangle.
    triangles = t1.Triangulate()                # This one is for the console output
    triangles2 = t2.Triangulate()               # This one is for the GUI



    # Now for the GUI. Both the polygon and its triangulation have been scaled,
    # as specified above. Now draw them on a Tkinter Canvas:
    # Setup and init a canvas:
    canvas_width = 1280
    canvas_height = 720
    master = Tkinter.Tk()
    canvas = Tkinter.Canvas(master, width=canvas_width, height=canvas_height)
    canvas.pack()


    t3.drawTriangles(canvas, triangles2)
    t3.drawPolygon(canvas)
    # Note that t3 is used to draw, but it takes t2's triangulation. This is
    # because t2's polygon is now broken.


    # The last step is to output the triangulation of the original, non-scaled
    # polygon to the console:
    IOClass.printTrianglesToConsole(triangles)


    # Display the canvas:
    Tkinter.mainloop()

    x = input("\n\nPress any key to continue...")

main()
