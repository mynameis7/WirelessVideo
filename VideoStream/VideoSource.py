from cv2 import VideoCapture
import numpy as np


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
            
        
    def cv_read(self):
        """
        Wrapper around cv2.VideoCapture.read
        :return: numpy ndarray
        """
        ret, data = self.source.read()
        return data
