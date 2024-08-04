import threading #this is for multiple instance to handle multiple function at the same time
import winsound #this is for the alarm sound.
import cv2
import imutils #The imutils library in Python is a package of convenience functions designed to make basic image processing tasks easier when working with OpenCV. It simplifies many common tasks, such as resizing, rotating, translating, and displaying images, which would otherwise require more verbose code in OpenCV.

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640) #setting the windows frame width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) #setting the windows frame height

#Reading, grayscaling and smoothing the starting frame
_, starting_frame = cap.read()
starting_frame = imutils.resize(starting_frame, width=500)
starting_frame = cv2.cvtColor(starting_frame, cv2.COLOR_BGR2GRAY)
starting_frame = cv2.GaussianBlur(starting_frame, (21,21), 0)

#defining alarm varibles
alarm = False
alarm_mode = False
alarm_counter = 0

#generanting an email to send to the user

#creating function to beep alarm
def beep_alarm() :
    global alarm
    for _ in range(5):
        if not alarm_mode: #if alarm mode is false
            break
        print("Alarm")
        winsound.Beep(2500, 1000) #beep the alarm(sound)
    alarm = False

#Main code
while True:
    _, frame = cap.read()
    frame = imutils.resize(frame, width=500)

    if alarm_mode:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5,5), 0)

        difference = cv2.absdiff(frame_bw, starting_frame)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
        starting_frame = frame_bw

        if threshold.sum() > 1000:
            alarm_counter += 1
        else:
            if alarm_counter > 0:
                alarm_counter -= 1

        cv2.imshow("CAM", threshold)

    else:
        cv2.imshow("CAM", frame)

    if alarm_counter > 50:
        if not alarm:
            alarm = True
            threading.Thread(target=beep_alarm).start()
    
    key_pressed = cv2.waitKey(30)
    if key_pressed == ord("t"):
        alarm_mode = not alarm_mode
        alarm_counter = 0
    if key_pressed == ord("q"):
        alarm_mode = False
        break

cv2.destroyAllWindows()
cap.release()