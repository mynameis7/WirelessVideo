from Queue import PriorityQueue
from threading import Thread
from frame import Frame
import socket
import cv2
import numpy


class VideoSender(object):
    """
    Send video from a specified source on a TCP Server
    """
    def __init__(self, source, ip='localhost', port=12345):
        """
        Initialize the video sender object with a socket address and a source
        :param source: VideoSource object containing the video source
        :param ip: IP address of the VideoReciever
        :param port: Port of the VideoReciever
        :return: VideoSender object
        """
        self.ip = ip
        self.port = port
        self.frame = 1
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.frame_buffer = PriorityQueue()
        self.capture_thread = Thread(target=self.capture_video)
        self.sending_thread = Thread(target=self.send_video)
        self.capture_thread.setDaemon(True)
        self.sending_thread.setDaemon(True)
        self.capturing = False
        self.source = source
        self.addr = (self.ip, self.port)
        self.encode_param = [1, 90]#[int(cv2.IMWRITE_JPEG_QUALITY), 90]

    def start(self):
        """
        start the capture thread and begin sending video over TCP connection
        :return: None
        """
        self.capturing = True
        print "Connecting Sender"
        self.sock.connect(self.addr)
        self.capture_thread.start()
        print "Starting Sender"
        self.sending_thread.start()

    def stop(self):
        """
        Stop the capture thread and stop sending video
        :return: None
        """
        self.capturing = False
        self.source.kill()
        self.capture_thread.join()
        print "Capture joined"
        self.sending_thread.join()
        self.sock.close()
        print "Sending joined"


    def capture_video(self):
        """
        Capture video from the specified source and store it in the queue, used as the target of a thread
        :return: None
        """
        while self.capturing:
            nparray = self.source.get_frame()
            self.frame_buffer.put(Frame(nparray, self.frame))
            self.frame += 1
        print "Stopping Capture"

    def send_video(self):
        """
        Send frames over the TCP connection
        :return: None
        """
        print "Sending"
        while self.capturing:
            self.send_frame()
        print "Stopping Send"

    def send_frame(self):
        """
        Send a single frame over the TCP connection
        :return: None
        """
        frame = self.frame_buffer.get()
        result, jpeg = cv2.imencode(".jpg", frame.nparray)#, self.encode_param)
        data = numpy.array(jpeg)
        string_data = data.tostring()
        self.sock.send(str(len(string_data)).ljust(16))
        self.sock.send(string_data)
