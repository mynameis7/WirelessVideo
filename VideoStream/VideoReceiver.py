from Queue import Queue
from threading import Thread, Condition
from frame import Frame
import socket
import cv2
import numpy


class VideoReceiver(object):
    """
    Receive a stream of jpg images on a TCP Socket from the given port and ip address
    """
    def __init__(self, ip='localhost', port=12345):
        """
        Initialize the video receiver with an ip address and port for a TCP connection
        :param ip: TCP IP address
        :param port: TCP Port number
        :return: VideoReceiver object
        """
        self.ip = ip
        self.port = port
        self.frame = 0
        self.frame_buffer = Queue()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receiver_thread = Thread(target=self.receive)
        self.receiver_thread.setDaemon(True)
        self.frame_ready = Condition()
        self.serving = False
        self.addr = (self.ip, self.port)
        self.conn = None

    def start(self):
        """
        Start the receiving thread to fill the frame buffer
        :return: None
        """
        self.sock.bind(self.addr)
        self.sock.listen(True)
        print "Listening Receiver"
        self.conn, addr = self.sock.accept()
        self.serving = True
        print "Starting Receiver"
        self.receiver_thread.start()

    def stop(self):
        """
        Stop the receiving thread and close the video socket.
        :return: None
        """
        self.serving = False
        self.receiver_thread.join()
        print "Receiver joined"
        self.sock.close()

    def recv_all(self, count):
        """
        Receive all the bytes from the socket given by count
        :param count: number of bytes to receive
        :return: rawbytes in a string
        """
        buf = b''
        while count and self.serving:
            newbuf = self.conn.recv(count)
            if not newbuf or not self.serving:
                return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def receive(self):
        """
        Receive jpg images from the tcp socket
        :return: None
        """
        print "Receiving"
        while self.serving:
            size = self.recv_all(16)
            if size:
                data = self.recv_all(int(size))
                nparray = numpy.fromstring(data, dtype='uint8')
                img = cv2.imdecode(nparray, 1)
                self.frame_buffer.put(Frame(img, self.frame))
        print "Stop Receiving"

    def get_frame(self):
        """
        Get a frame out of the frame buffer
        :return: numpy ndarray
        """
        frame = self.frame_buffer.get()
        return frame.nparray
