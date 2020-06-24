import cv2
import sys
import threading
from sensecam_control import vapix_control


ip = '000.000.000.000'
login = 'login'
password = 'password'

exit_program = 0


def event_keyboard(k):
    global exit_program

    if k == 27:  # esc
        exit_program = 1

    elif k == ord('w') or k == ord('W'):
        X.relative_move(None, 1, None)

    elif k == ord('a') or k == ord('A'):
        X.relative_move(-1, None, None)

    elif k == ord('s') or k == ord('S'):
        X.relative_move(None, -1, None)

    elif k == ord('d') or k == ord('D'):
        X.relative_move(1, None, None)

    elif k == ord('h') or k == ord('H'):
        X.go_home_position()


def capture(ip_camera):
    global exit_program

    #url http login axis camera
    ip2 = 'http://' + login + ':' + password + '@' + ip_camera + '/mjpg/1/video.mjpg?'

    #url rtsp axis camera
    #ip2 = 'rtsp://' + login + ':' + password + '@' + ip_camera + '/axis-media/media.amp'

    cap = cv2.VideoCapture(ip2)

    while True:
        ret, frame = cap.read()
        if ret is not False:
            break

    while True:
        ret, frame = cap.read()

        if exit_program == 1:
            sys.exit()

        #cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)
        cv2.imshow('Camera', frame)
        event_keyboard(cv2.waitKey(1) & 0xff)


X = vapix_control.CameraControl(ip, login, password)
t = threading.Thread(target=capture, args=(ip,))
t.start()
