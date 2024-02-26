import cv2
import numpy as np

def detect_color(frame, roi, color):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_frame, color[0], color[1])
    roi_mask = mask[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]]
    return roi_mask.any()

def main():

    cap = cv2.VideoCapture(0)

    # Define color range for detection (example: blue color)
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([130, 255, 255])
    blue_color = (lower_blue, upper_blue)

    # สี่เหลี่ยม
    roi = (100, 100, 200, 200)  # (x, y, width, height)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

         # Flip the frame horizontally
        frame = cv2.flip(frame, 1)

        # วาดกล่อง
        cv2.rectangle(frame, (roi[0], roi[1]), (roi[0]+roi[2], roi[1]+roi[3]), (0, 255, 0), 2)

        #จับสีในกล่อง
        color_detected = detect_color(frame, roi, blue_color)

        # แสดงข้อความ detect สี
        if color_detected:
            cv2.putText(frame, 'Blue item detected!', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
     
        else:
            cv2.putText(frame, 'Blue item Not detected!', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.imshow('frame', frame)
       
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

 
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
