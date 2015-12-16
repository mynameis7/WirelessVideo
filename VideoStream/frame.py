class Frame(object):
    """
    Hold a frame (numpy array), with a sequence identifier
    """
    def __init__(self, nparray, framenum):
        """
        A container for a numpy array item with a sequence value for determining frame order
        :param nparray: Image of the frame as a numpy array
        :param framenum: Integer representing the index of the frame in the context of a video
        :return: Frame object
        """
        self.num = framenum
        self.nparray = nparray

    def __cmp__(self, other):
        return cmp(self.num, other.num)
