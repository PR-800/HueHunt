import cv2
import numpy as np
import random
import time

colorsEasy = {
    "blue": (np.array([100, 50, 50]), np.array([130, 255, 255])),
    "green": (np.array([50, 50, 50]), np.array([70, 255, 255])),
    "red": (np.array([0, 100, 100]), np.array([10, 255, 255])),
}

strokeColorsEasy = {
    "blue": (255, 0, 0),    
    "green": (0, 255, 0),   
    "red": (0, 0, 255),     
}

colorsHard = {
    "blue": (np.array([100, 50, 50]), np.array([130, 255, 255])),
    "green": (np.array([50, 50, 50]), np.array([70, 255, 255])),
    "red": (np.array([0, 100, 100]), np.array([10, 255, 255])),
    "yellow": (np.array([20, 100, 100]), np.array([30, 255, 255])),
    "white": (np.array([0, 0, 200]), np.array([180, 50, 255])),
    "purple": (np.array([140, 50, 50]), np.array([160, 255, 255])),
    "orange": (np.array([0, 100, 100]), np.array([20, 255, 255]))
}

strokeColorsHard = {
    "blue": (255, 0, 0),    
    "green": (0, 255, 0),   
    "red": (0, 0, 255),     
    "yellow": (0, 255, 255),
    "white": (255, 255, 255),
    "purple": (128, 0, 128),
    "orange": (0, 165, 255),
}

def detectColor(frame, roi, color):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_frame, color[0], color[1])

    roi_mask = np.zeros_like(mask)
    roi_mask[roi[1]+50:roi[1]+roi[3]-80, roi[0]+10:roi[0]+roi[2]-10] = mask[roi[1]+50:roi[1]+roi[3]-80, roi[0]+10:roi[0]+roi[2]-10]
    # roi[1]+50 --> เริ่ม y ลงมา 50 หน่วย (ขอบบน) จะได้ไม่ตรวจโดนตัวอักษร
    # roi[1]+roi[3]-80 --> ความยาว y ลบออกอีก 30 จะได้ไม่เจอ quit
    # roi[0]+10 --> เริ่ม x เข้าไป 10 หน่วย (ขอบซ้าย)
    # roi[0]+roi[2]-10] --> ความยาว x

    area_count = calculateArea(roi_mask)

    return roi_mask.any(), area_count

def randomColorAndRoi(prevColor, mode):

    if mode == 'EASY':
        availableColors = [color for color in colorsEasy.keys() if color != prevColor]
        if availableColors:
            colorName = random.choice(availableColors)
            colorRange = colorsEasy[colorName]
    elif mode == 'HARD':
        availableColors = [color for color in colorsHard.keys() if color != prevColor]
        if availableColors:
            colorName = random.choice(availableColors)
            colorRange = colorsHard[colorName]

    roi = (random.randint(0, 800 - 350), random.randint(150, 600 - 300), 200, 200) 

    return colorName, colorRange, roi

def calculateArea(roi_mask):
    totalArea = np.prod(roi_mask.shape)
    matchingPixels = np.count_nonzero(roi_mask)
    percentage = (matchingPixels / totalArea) * 100
    return percentage

def lightBalance(frame):

    average_brightness = np.mean(frame) # คำนวณค่าความสว่างเฉลี่ยของภาพ

    brightness_threshold = 127  # ค่าสว่าง standard
    min_brightness = 50 
    max_brightness = 200 
    
    if average_brightness < brightness_threshold:   # มืดเกิน
        alpha = min_brightness / average_brightness
        balanced_frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=0)
    else:   # สว่างเกิน
        beta = (255 - max_brightness) * (1 - (average_brightness / 255))
        balanced_frame = cv2.convertScaleAbs(frame, alpha=1, beta=beta)

    return balanced_frame

def main():
    
    cap = cv2.VideoCapture(0)

    cv2.namedWindow('HueHunt', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('HueHunt', 800, 600)

    quitGame = False
    
    while not quitGame: 
        startScreen = True
        playingScreen = False
        gameMode = None
        startGame = None
        startTime = 3

        while startScreen:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)

            # frame[:] = (0, 0, 0) 
            bg = cv2.imread("bg.jpg")
            resizedBG = cv2.resize(bg, (800, 600))

            cv2.putText(resizedBG, "HueHunt", (210, 220), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 5, cv2.LINE_AA)
            cv2.putText(resizedBG, "Press 's' to start", (260, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

            cv2.putText(resizedBG, "Press 'q' to quit game", (300, 550), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

            cv2.imshow('HueHunt', resizedBG)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'): 
                quitGame = True
                break

            elif key == ord('s'):  
                while True:
                    bg = cv2.imread("bg.jpg")
                    resizedBG = cv2.resize(bg, (800, 600))

                    cv2.putText(resizedBG, "Choose difficulty", (280, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
                    
                    cv2.putText(resizedBG, "Fewer color, Longer timer", (160, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                    cv2.putText(resizedBG, "EASY", (190, 345), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3, cv2.LINE_AA)
                    cv2.putText(resizedBG, "Press 'e'", (230, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                    cv2.putText(resizedBG, "to continue with easy mode", (150, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

                    cv2.putText(resizedBG, "More color, Shorter timer", (460, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                    cv2.putText(resizedBG, "HARD", (480, 345), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3, cv2.LINE_AA)
                    cv2.putText(resizedBG, "Press 'h'", (530, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                    cv2.putText(resizedBG, "to continue with hard mode", (450, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

                    cv2.imshow('HueHunt', resizedBG)

                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('e'): 
                        gameMode = "EASY"
                        colorName, colorRange, roi = randomColorAndRoi(None, gameMode)
                        print("easy mode on")
                        break
                    elif key == ord('h'): 
                        gameMode = "HARD"
                        colorName, colorRange, roi = randomColorAndRoi(None, gameMode)
                        print("hard mode on")
                        break
                
                startGame = time.time()
                while True:
                    diff = int(time.time() - startGame)
                    remainingTime = max(0, startTime - diff)

                    bg = cv2.imread("bg.jpg")
                    resizedBG = cv2.resize(bg, (800, 600))
                    cv2.putText(resizedBG, "Game will start in", (260, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
                    cv2.putText(resizedBG, f'{remainingTime}', (350, 330), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 0), 5, cv2.LINE_AA)
                    cv2.putText(resizedBG, "Prepare yourself !", (260, 410), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

                    cv2.imshow('HueHunt', resizedBG)
                    cv2.waitKey(1000)  

                    if diff >= startTime:
                        break
                startScreen = False
                playingScreen = True
                countdownStart = time.time()    # เก็บเวลา ณ ตอนรันไว้
                if gameMode == 'EASY':
                    countdownTime = 8 
                elif gameMode == 'HARD':
                    countdownTime = 5 
                score = 0
                detect = False
                over = False
                
        while playingScreen:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1) 

            frame = lightBalance(frame)   # ทำ light balance

            diff = int(time.time() - countdownStart)        # เวลาตอนนี้ - ตอนนู้น (จะเพิ่มเรื่อย ๆ)
            remainingTime = max(0, countdownTime - diff)    # เวลาถอยหลัง - ส่วนต่าง

            if diff >= countdownTime:
                if detect:
                    score += 1
                    cv2.putText(frame, "Well Done !", (150, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3, cv2.LINE_AA)
                    cv2.putText(frame, f'Current Score: {score} ', (200, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
                    cv2.imshow('HueHunt', frame)
                    cv2.waitKey(2000)
                else:
                    over = True
                detect = False
                colorName, colorRange, roi = randomColorAndRoi(colorName, gameMode)
                countdownStart = time.time()
            
            if not over:

                if gameMode == 'EASY':
                    cv2.rectangle(frame, (roi[0], roi[1]), (roi[0]+roi[2], roi[1]+roi[3]), strokeColorsEasy[colorName], 2)
                    cv2.putText(frame, f'{colorName.capitalize()}', (roi[0]+10, roi[1]+30), cv2.FONT_HERSHEY_SIMPLEX, 1, strokeColorsEasy[colorName], 2, cv2.LINE_AA)
                    
                    color_detected, area_count = detectColor(frame, roi, colorRange)
                    if color_detected and area_count > 0.5:
                        cv2.rectangle(frame, (roi[0]-10, roi[1]-10), (roi[0]+roi[2]+10, roi[1]+roi[3]+10), strokeColorsEasy[colorName], 2)
                        detect = True
                        print(f"Percentage of {colorName}: {area_count}")

                elif gameMode == 'HARD':
                    cv2.rectangle(frame, (roi[0], roi[1]), (roi[0]+roi[2], roi[1]+roi[3]), strokeColorsHard[colorName], 2)
                    cv2.putText(frame, f'{colorName.capitalize()}', (roi[0]+10, roi[1]+30), cv2.FONT_HERSHEY_SIMPLEX, 1, strokeColorsHard[colorName], 2, cv2.LINE_AA)
  
                    color_detected, area_count = detectColor(frame, roi, colorRange)
                    if color_detected and area_count > 0.5:
                        cv2.rectangle(frame, (roi[0]-10, roi[1]-10), (roi[0]+roi[2]+10, roi[1]+roi[3]+10), strokeColorsHard[colorName], 2)
                        detect = True
                        print(f"Percentage of {colorName}: {area_count}")
                
                cv2.putText(frame, "Time Remaining", (200, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
                cv2.putText(frame, f'{remainingTime}', (300, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3, cv2.LINE_AA)
                cv2.putText(frame, "Press 'q' to quit game", (250, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

                cv2.imshow('HueHunt', frame)
            
            if over:
                bg = cv2.imread("bg.jpg")
                resizedBG = cv2.resize(bg, (800, 600))
                cv2.putText(resizedBG, f'Game Over !', (220, 220), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3, cv2.LINE_AA)
                cv2.putText(resizedBG, f'You got {score}', (320, 280), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
                cv2.putText(resizedBG, "Try again ? (y/n)", (260, 380), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
                cv2.imshow('HueHunt', resizedBG)

                key = cv2.waitKey(1) & 0xFF
                if key == ord('y'):
                    break
                elif key == ord('q') or key == ord('n'): 
                    quitGame = True
                    break
        
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
