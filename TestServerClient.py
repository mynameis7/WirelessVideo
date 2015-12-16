import cv2
import VideoStream as VS

import threading
import logging

import time

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

if __name__ == "__main__":
    true_source = cv2.VideoCapture(0)

    source = VS.VideoSource.VideoSource(true_source)
    receiver = VS.VideoReceiver.VideoReceiver()
    recv_thread = threading.Thread(target=receiver.start)
    recv_thread.setDaemon(True)
    recv_thread.start()

    sender = VS.VideoSender.VideoSender(source)
    send_thread = threading.Thread(target=sender.start)
    send_thread.setDaemon(True)
    send_thread.start()
    total = 0
    while True:
        cv2.imshow("Frame", receiver.get_frame())
        total += 1
        if total % 100000 == 0:
            logging.debug("Still Running")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            sender.stop()
            receiver.stop()
            break

