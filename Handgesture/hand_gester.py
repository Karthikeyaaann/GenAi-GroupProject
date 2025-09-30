import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui

detector = HandDetector(detectionCon=0.5, maxHands=2)
cap = cv2.VideoCapture(0)import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui

detector = HandDetector(detectionCon=0.5, maxHands=2)
cap = cv2.VideoCapture(0)
cap.set(3, 600)
cap.set(4, 400)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    if hands and hands[0]["type"] == "Left":
        fingers = detector.fingersUp(hands[0])
        totalFingers = fingers.count(1)

        cv2.putText(img, f'Fingers: {totalFingers}',
                    (50, 50), cv2.FONT_HERSHEY_PLAIN,
                    2, (0, 255, 0), 2)

        if totalFingers == 5:  # Gas
            pyautogui.keyDown("right")
            pyautogui.keyUp("left")

        elif totalFingers == 0:  # Brake
            pyautogui.keyDown("left")
            pyautogui.keyUp("right")

        elif totalFingers == 3:  # Neutral
            pyautogui.keyUp("left")
            pyautogui.keyUp("right")

    cv2.imshow('Camera Feed', img)
    cv2.waitKey(1)

cap.set(3, 600)
cap.set(4, 400)

def set_controls(press_right=False, press_left=False):
    pyautogui.keyUp("right")
    pyautogui.keyUp("left")
    if press_right:
        pyautogui.keyDown("right")
    elif press_left:
        pyautogui.keyDown("left")

try:
    while True:
        success, img = cap.read()
        if not success:
            print("Failed to grab frame from camera.")
            break

        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img)

        if hands:
            hand = hands[0]
            if hand["type"] == "Left":
                fingers = detector.fingersUp(hand)
                totalFingers = fingers.count(1)

                cv2.putText(img, f'Fingers: {totalFingers}',
                            (50, 50), cv2.FONT_HERSHEY_PLAIN,
                            2, (0, 255, 0), 2)

                if totalFingers == 5:       # Gas
                    set_controls(press_right=True)
                elif totalFingers == 0:     # Brake
                    set_controls(press_left=True)
                elif totalFingers == 3:     # Neutral
                    set_controls()
                else:
                    set_controls()
        else:
            set_controls()

        cv2.imshow('Camera Feed', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    pass
finally:
    pyautogui.keyUp("right")
    pyautogui.keyUp("left")
    cap.release()
    cv2.destroyAllWindows()

