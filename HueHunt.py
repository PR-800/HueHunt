import cv2
import numpy as np
import random
import time

colors = {
    "blue": (np.array([100, 50, 50]), np.array([130, 255, 255])),
    "green": (np.array([50, 50, 50]), np.array([70, 255, 255])),
    "red": (np.array([0, 100, 100]), np.array([10, 255, 255])),
    "yellow": (np.array([20, 100, 100]), np.array([30, 255, 255]))
}

def detectColor(frame, roi, color):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_frame, color[0], color[1])
    roi_mask = mask[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]]
    return roi_mask.any()

def randomColorAndRoi(prevColor=None):

    availableColors = [color for color in colors.keys() if color != prevColor]

    if availableColors:
        colorName = random.choice(availableColors)
        colorRange = colors[colorName]

    roi = (random.randint(0, 800 - 350), random.randint(0, 600 - 300), 200, 200) 

    return colorName, colorRange, roi

def main():
    
    cap = cv2.VideoCapture(0)

    colorName, colorRange, roi = randomColorAndRoi(None)

    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('frame', 800, 600)

    countdownStart = time.time() #เก็บเวลา ณ ตอนรันไว้
    countdownTime = 5 

    score = 0
    detect = False
    over = False
    
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1) 

        diff = int(time.time() - countdownStart)        # เวลาตอนนี้ - ตอนนู้น (จะเพิ่มเรื่อย ๆ)
        remainingTime = max(0, countdownTime - diff)   # เวลาถอยหลัง - ส่วนต่าง

        if diff >= countdownTime:
            if detect == True:
                score += 1
            else:
                over = True
            detect = False
            colorName, colorRange, roi = randomColorAndRoi(colorName)
            countdownStart = time.time()
           
        if not over:

            cv2.rectangle(frame, (roi[0], roi[1]), (roi[0]+roi[2], roi[1]+roi[3]), (0, 255, 0), 2)

            cv2.putText(frame, f'Time Remaining: {remainingTime}s', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f'{colorName.capitalize()} ', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

            # if diff < countdownTime:
            color_detected = detectColor(frame, roi, colorRange)
            if color_detected:
                cv2.putText(frame, f'{colorName.capitalize()} detected!', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                detect = True
            else:
                cv2.putText(frame, f'{colorName.capitalize()} not detected!', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                    
            cv2.putText(frame, f'Score: {score} ', (400, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f'Detect: {detect} ', (400, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

        if over:
            cv2.rectangle(frame, (0, 200), (800, 280), (255, 255, 255, 70), -1) # top-left, bottom-right, color, index
            cv2.putText(frame, f'Game Over! You got {score}', (150, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                countdownStart = time.time()
                countdownTime = 5  
                score = 0
                detect = False
                over = False

        cv2.imshow('frame', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
