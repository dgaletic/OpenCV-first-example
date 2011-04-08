import cv
import sys

def parse(filename, image_list):
    extension = filename[filename.rfind("."):]
    fil = open(filename, "r")
    if extension == ".yaml":
        for line in fil:
            left = line.find("\"")
            if left != -1:
                right = line.rfind("\"")
                image_file = line[left+1:right]
                image_list.append(image_file)
        fil.close()
        return True
    elif extension == ".xml":
        data = fil.read()
        data = data[data.find("<images>") + len("<images>"): data.find("</images>")]
        data = data.replace("\n", "").replace("  ", " ")
        names = data[1:].split(" ")
        print names
        image_list = image_list.extend(names)
        return True
    else:
        return False

# Mimicking the interface from the C++ original example,
# but using the parse() function before either:
#   a) I figure out FileStorage is ported to Python
#   b) FileStorage gets ported to Python
def readStringList(filename, l):
    return parse(filename, l)

def help(name):
    print "\nThis program gets you started being able to read images from a list in a file."
    print "Usage:\n./" + name + " image_list.yaml"
    print "\tThis is a starter sample, to get you up and going in a copy pasta fashion."
    print "\tThe program reads in an list of images from a yaml or xml file and displays"
    print "\tone at a time\n"
    print "\tTry running imagelist_creator to generate a list of images.\n"
    # print "Using OpenCV version" + CV_VERSION


def process(images):
    # Second param should be CV_WINDOW_KEEPRATIO, doesn't seem to be
    # available in Python.
    cv.NamedWindow("image", 0)
    # I suppose the parsing used in the C++ version puts only proper image 
    # names in the "images" parameter. try-except block is needed because we 
    # don't have that guaranteed here.
    for img in images:
        try: 
            image = cv.LoadImage(img, cv.CV_LOAD_IMAGE_GRAYSCALE)
            cv.ShowImage("image", image)
            print "Press a key to see the next image in the list."
            cv.WaitKey()
        except:
            print "Could not open image " + img

if __name__ == "__main__":
    if len(sys.argv) != 2:
        help(sys.argv[0])
        quit()

    arg = sys.argv[1]
    imagelist = []
    if (readStringList(arg, imagelist) == False):
        print "Failed to read image list\n"
        help(sys.argv[0])
        quit()

    process(imagelist)
    
