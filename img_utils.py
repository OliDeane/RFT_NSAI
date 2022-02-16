import cv2
import numpy as np

def get_object_position(size, center):

    start = (center[0]-size, center[1]-size)
    end = (center[0]+size, center[1]+size)

    return start, end, center

def draw_sCsS(img, positions, color, color_id, objects, size = 25):
    """Draws the same color same shape pairing"""

    # Draw objec A and add it to the object list
    start, end, center = get_object_position(size, center = positions[0][0])
    cv2.circle(img,center, size, color, -1)
    objects.append((color_id, center, 'c', (start[0], start[1], end[0], end[1])))

    # Draw object B and add to th eobject list
    start, end, center = get_object_position(size, center = positions[0][1])
    cv2.circle(img,center, size, color, -1)
    objects.append((color_id, center, 'c', (start[0], start[1], end[0], end[1])))


    return img, objects

def draw_sCdS(img, positions, color, color_id, objects, size = 25):
    """Draws the same color different shape pairing"""

    # Draw and add first object 
    start, end, center = get_object_position(size, center = positions[1][0])
    cv2.rectangle(img, start, end, color, -1)
    objects.append((color_id, center, 'r', (start[0], start[1], end[0], end[1])))


    # Draw and add second object
    start, end, center = get_object_position(size, center = positions[1][1])
    cv2.circle(img,center, size, color, -1)
    objects.append((color_id, center, 'c', (start[0], start[1], end[0], end[1])))

    return img, objects

def draw_dCsS(img, positions, color1, color2, color1_id, color2_id, objects, size = 25):
    """Draws the different color same shape pairing"""

    # Draw and add first object 
    start, end, center = get_object_position(size, center = positions[2][0])
    cv2.circle(img,center, size, color1, -1)
    objects.append((color1_id, center, 'c', (start[0], start[1], end[0], end[1])))

    # Draw and add first object 
    start, end, center = get_object_position(size, center = positions[2][1])
    cv2.circle(img,center, size, color2, -1)
    objects.append((color2_id, center, 'c', (start[0], start[1], end[0], end[1])))

    return img, objects

def draw_dCdS(img, positions, color1, color2, color1_id, color2_id, objects, size = 25):
    """Draws the different color different shape pairing"""


    # Draw and add first object 
    start, end, center = get_object_position(size, center = positions[3][0])
    cv2.rectangle(img, start, end, color1, -1)
    objects.append((color1_id, center, 'r', (start[0], start[1], end[0], end[1])))

        # Draw and add first object 
    start, end, center = get_object_position(size, center = positions[3][1])
    cv2.circle(img,center, size, color2, -1)
    objects.append((color2_id, center, 'c', (start[0], start[1], end[0], end[1])))

    return img, objects
    