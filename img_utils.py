import cv2


def draw_sCsS(img, positions, color, size = 25):
    """Draws the same color same shape pairing"""

    cv2.circle(img,positions[0][0], size, color, -1)
    cv2.circle(img,positions[0][1], size, color, -1)

    return img

def draw_sCdS(img, positions, color, size = 25):

    rec_center = positions[1][0]
    start = (rec_center[0]-size, rec_center[1]-size)
    end = (rec_center[0]+size, rec_center[1]+size)

    cv2.rectangle(img, start, end, color, -1)
    cv2.circle(img,positions[1][1], size, color, -1)


    return img

def draw_dCsS(img, positions, color1, color2, size = 25):

    cv2.circle(img,positions[2][0], size, color1, -1)
    cv2.circle(img,positions[2][1], size, color2, -1)

    return img

def draw_dCdS(img, positions, color1, color2, size = 25):

    rec_center = positions[3][0]
    start = (rec_center[0]-size, rec_center[1]-size)
    end = (rec_center[0]+size, rec_center[1]+size)

    cv2.rectangle(img, start, end, color1, -1)
    cv2.circle(img,positions[3][1], size, color2, -1)


    return img
    