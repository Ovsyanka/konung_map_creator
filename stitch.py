import cv2
import numpy as np


def load_images(dir_path, window=(0, 556, 140, None)):
    """
    Load all files in a directory as images and take a subimage of each one specified by 'window'.
    :param window: (y begin, y end, x begin, x end)
    :return: list of images
    """
    from os import listdir
    from os.path import isfile, join
    files = [join(dir_path, filename) for filename in listdir(dir_path)]
    return [cv2.imread(f, cv2.IMREAD_UNCHANGED)[window[0]:window[1], window[2]:window[3], :]
            for f in files if isfile(f)]


def matching_pixels(img1, img2):
    return cv2.countNonZero(cv2.compare(img1, img2, cv2.CMP_EQ))


def slice_shifted(shiftX, shiftY):
    """
    Get the indexes slice corresponding to the shifts. Positive shifts crop the image on the left/top, negative ones
    crop it on the right/bottom.
    :return: (yBegin, yEnd, xBegin, xEnd)
    """
    if shiftY >= 0:
        yBegin = shiftY
        yEnd = None
    else:
        yBegin = None
        yEnd = shiftY
    if shiftX >= 0:
        xBegin = shiftX
        xEnd = None
    else:
        xBegin = None
        xEnd = shiftX
    return yBegin, yEnd, xBegin, xEnd


def sign(x):
    """Signum function (except 0 isn't handled separately)"""
    return 1 if x > 0 else -1


def draw_shift(img, shiftX, shiftY, color=(255, 255, 255)):
    """
    Draw a rectangle corresponding to the shift
    """
    maxY, maxX = (n - 1 for n in img.shape[0:2])
    yBegin, yEnd, xBegin, xEnd = slice_shifted(shiftX, shiftY)
    top = yBegin if yBegin else 0
    bottom = maxY + yEnd if yEnd else maxY
    left = xBegin if xBegin else 0
    right = maxX + xEnd if xEnd else maxX
    cv2.rectangle(img, (left, top), (right, bottom), color)


def stitch_screenshots(screensDir):
    imgs = load_images(screensDir)
    height, width = imgs[0].shape[0:2]
    imgArea = height * width
    matchThresh = imgArea * 0.8
    maxX, maxY = width - 1, height - 1  # TODO: Think of limiting the search range
    for img1, img2 in zip(imgs[:-1], imgs[1:]):
        gray1, gray2 = map(lambda img: cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (img1, img2))
        x = y = bestX = bestY = 0
        bestMatch = 0
        while True:
            slice1 = slice_shifted(x, y)
            slice2 = slice_shifted(-x, -y)
            match = matching_pixels(gray1[slice1[0]:slice1[1], slice1[2]:slice1[3]],
                                    gray2[slice2[0]:slice2[1], slice2[2]:slice2[3]])
            if match > bestMatch:
                bestX = x
                bestY = y
                bestMatch = match
                if bestMatch >= matchThresh:
                    break
            # Move to next location. Scans in a spiral, starting with small shifts in every direction.
            if x == y and x <= 0:  # End of a circle, go to the next one
                y -= 1
                dx = 1
                dy = 0
            else:
                if abs(x) == abs(y):  # A corner
                    if dy == 0:  # We were moving horizontally
                        dy = dx
                        dx = 0
                    else:
                        dx = -dy
                        dy = 0
                x += dx
                y += dy
            # If we've gone out of the search range (image borders), skip a part of the spiral
            if abs(x) > maxX:
                x -= sign(x)
                y = -(y + sign(y))
                dx = -dx
            elif abs(y) > maxY:
                y -= sign(y)
                x = -(x + sign(x))
                dy = -dy
            if abs(x) > maxX or abs(y) > maxY:  # All positions checked
                break
        print "Best match: %.1f%%, shift: (%d, %d)" % (bestMatch / float(imgArea) * 100, bestX, bestY)
        displayCopy1, displayCopy2 = np.array(img1), np.array(img2)
        draw_shift(displayCopy1, bestX, bestY)
        draw_shift(displayCopy2, -bestX, -bestY)
        cv2.imshow("from", displayCopy1)
        cv2.imshow("to", displayCopy2)
        cv2.waitKey()

if __name__ == "__main__":
    stitch_screenshots('screenshots')
