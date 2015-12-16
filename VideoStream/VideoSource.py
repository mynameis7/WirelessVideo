from cv2 import VideoCapture
from pygame import Surface
from pygame import surfarray
import pyscreenshot as ImageGrab
import numpy as np
import autopy


class VideoSource(object):
    """
    Container object for some video source.
    """
    def __init__(self, source):
        """
        Initialize the video source object with a source.
        Identifies the type of the source and wraps the primary image grabbing function
        Source can be:
            OpenCV VideoCapture
            Pygame Surface
        :param source: Source of the video
        :return: VideoSource object
        """
        self.source = source
        self.get_frame = None
        if isinstance(self.source, type(VideoCapture())):
            self.get_frame = self.cv_read
            self.kill = self.source.release
        elif isinstance(self.source, Surface):
            self.get_frame = self.surface_as_frame
            self.kill = self.kill_surface
        elif self.source is autopy.bitmap:
            self.get_frame = self.autopy_image_grab
            self.kill = self.kill_surface
        elif self.source is ImageGrab:
            self.get_frame = self.image_grab_read
            self.kill = self.kill_surface
            
    def image_grab_read(self):
        """
        Wrapper around ImageGrab from PIL
        :return: numpy ndarray
        """
        screen = self.source.grab((0,0,512,512))
        printscreen_numpy = np.array(screen.getdata(),dtype='uint8')\
        .reshape((screen.size[1],screen.size[0],3))
        return printscreen_numpy
        
    def cv_read(self):
        """
        Wrapper around cv2.VideoCapture.read
        :return: numpy ndarray
        """
        ret, data = self.source.read()
        return data

    def autopy_image_grab(self):
        """
        Wrapper around autopy screen capture
        :return:
        """
        image = self.source.capture_screen()
        w = image.width
        h = image.height
        a = np.empty((h, w), dtype="uint8")

        for r in xrange(h):
            for c in xrange(w):
                v = image.get_color(c, r)
                a[r, c] = v#autopy.color.hex_to_rgb(v)
        return a
    
    def surface_as_frame(self):
        """
        function to return pygame surface from source as a numpy array
        :return: numpy ndarray
        """
        return surfarray.array2d(self.source)

    def kill_surface(self):
        """
        Empty function for handling pygame surfaces
        :return: None
        """
        return None
