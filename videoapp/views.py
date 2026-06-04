from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
import cv2
import numpy as np
import pyttsx3
import pytesseract
import re
import time
from cvzone.HandTrackingModule import HandDetector
import threading

# ==============================
# TESSERACT PATH
# ==============================

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ==============================
# CAMERA + HAND DETECTOR
# ==============================

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=2, detectionCon=0.8, minTrackCon=0.8)

# ==============================
# GLOBAL STATES
# ==============================

# -------- AIRWRITING --------
response_text = "Write..."
canvas = None
prev_pos = None
smooth_pos = None
calculated = False
is_processing = False

# -------- GESTURE CALCULATOR --------
expression = ""
gesture_result = "Show gesture..."
gesture_buffer = []
last_added_time = 0

# ==============================
# OCR + CALCULATION
# ==============================

def calculate_expression(canvas_input):
    global response_text

    print("CALCULATION STARTED")

    try:
        # Convert to grayscale
        gray = cv2.cvtColor(canvas_input, cv2.COLOR_BGR2GRAY)

        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        thresh = cv2.bitwise_not(thresh)

        thresh = cv2.resize(thresh, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        kernel = np.ones((3,3), np.uint8)
        thresh = cv2.dilate(thresh, kernel, iterations=1)
        text = pytesseract.image_to_string(
        thresh,
        config='--psm 7 -c tessedit_char_whitelist=0123456789+-*/'
)

        print("RAW OCR:", text)

        text = text.replace(" ", "").replace("\n", "")
        text = text.replace("x", "*").replace("X", "*").replace("÷", "/")

        expression = re.sub(r'[^0-9+\-*/]', '', text)

        print("CLEAN EXPRESSION:", expression)
        print("NUMBERS FOUND:", re.findall(r'\d+', expression))

        # Expression must contain operator
        if not any(op in expression for op in ['+', '-', '*', '/']):
            response_text = "Write Clearly"
            return

        try:
            result = eval(expression, {"__builtins__": None}, {})
            response_text = f"{expression} = {result}"
            engine = pyttsx3.init()
            engine.say("Hey. Great.! The answer of.. " + response_text)
            engine.runAndWait()
        except:
            response_text = "Write Clearly"

    except Exception as e:
        print("ERROR:", e)
        response_text = "Invalid Expression"

def run_calculation_async(canvas_copy):
    global is_processing

    calculate_expression(canvas_copy)

    is_processing = False

# ==============================
# AIRWRITING STREAM
# ==============================

def airwriting_stream():
    global prev_pos, smooth_pos, canvas
    global response_text, is_processing

    while True:
        success, img = cap.read()
        if not success:
            break

        img = cv2.flip(img, 1)

        if canvas is None:
            canvas = np.zeros_like(img)

        hands, img = detector.findHands(img, draw=True)

        if hands:
            hand = hands[0]
            fingers = detector.fingersUp(hand)

            index_tip = hand["lmList"][8]
            curr_pos = np.array([index_tip[0], index_tip[1]])

            # ===== DRAW (Index Only)
            if fingers == [0, 1, 0, 0, 0]:

                if smooth_pos is None:
                    smooth_pos = curr_pos.astype(float)
                else:
                    alpha = 0.3
                    smooth_pos = alpha * curr_pos + (1 - alpha) * smooth_pos

                draw_point = tuple(smooth_pos.astype(int))

                if prev_pos is not None:
                    cv2.line(canvas, prev_pos, draw_point, (0,0,255), 20)

                prev_pos = draw_point
            else:
                prev_pos = None
                smooth_pos = None

            # ===== CLEAR (Thumb Only)
            if fingers == [1, 0, 0, 0, 0]:
                canvas = np.zeros_like(img)
                response_text = "Canvas Cleared"

            # ===== CALCULATE (Pinky Only)
            if fingers == [0, 0, 0, 0, 1] and not is_processing:
                is_processing = True
                response_text = "Processing..."

                canvas_copy = canvas.copy()

                thread = threading.Thread(
                    target=run_calculation_async,
                    args=(canvas_copy,)
                )
                thread.daemon = True
                thread.start()

        # ===== MERGE
        canvas_gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(canvas_gray, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)

        img_bg = cv2.bitwise_and(img, img, mask=mask_inv)
        img_fg = cv2.bitwise_and(canvas, canvas, mask=mask)

        combined = cv2.add(img_bg, img_fg)

        cv2.rectangle(combined, (0, 0),
                      (combined.shape[1], 60),
                      (0, 0, 0), -1)

        cv2.putText(combined, response_text,
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2)

        ret, buffer = cv2.imencode(".jpg", combined)

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + buffer.tobytes()
            + b"\r\n"
        )

#################################
#######  Gesture Stream  ########
#################################
def gesture_stream():
    global gesture_result, expression, gesture_buffer, last_added_time

    # Define number and operator gestures
    NUMBER_GESTURES = {
        (0,1,0,0,0): "1",
        (0,1,1,0,0): "2",
        (0,1,1,1,0): "3",
        (0,1,1,1,1): "4",
        (1,1,1,1,1): "5",
        (1,1,0,0,0): "6",
        (1,1,1,0,0): "7",
        (1,1,1,1,0): "8",
        (0,1,1,0,1): "9",
        (0,0,0,0,0): "10",
    }

    OPERATOR_GESTURES = {
        (1,1,0,0,1): "+",
        (0,0,1,0,0): "-",
        (1,0,1,0,0): "*",
        (1,0,0,1,1): "/",
    }

    CLEAR_GESTURE = (1,0,0,0,0)
    EQUAL_GESTURE = (0,0,0,0,1)

    while True:
        success, img = cap.read()
        if not success:
            break

        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img)

        current_time = time.time()

        if hands:
            fingers = detector.fingersUp(hands[0])
            pattern = tuple(fingers)

            # Stability buffer
            gesture_buffer.append(pattern)
            if len(gesture_buffer) > 20:
                gesture_buffer.pop(0)

            stable = None
            if gesture_buffer.count(pattern) > 15:
                stable = pattern

            if stable and current_time - last_added_time > 1.2:

                # CLEAR
                if stable == CLEAR_GESTURE:
                    expression = ""
                    gesture_result = "Cleared"
                    gesture_buffer.clear()

                # NUMBER
                elif stable in NUMBER_GESTURES:
                    expression += NUMBER_GESTURES[stable]

                # OPERATOR
                elif stable in OPERATOR_GESTURES:
                    if expression and expression[-1] not in "+-*/":
                        expression += OPERATOR_GESTURES[stable]

                # EQUAL
                elif stable == EQUAL_GESTURE and expression:
                    try:
                        result = str(eval(expression))
                        gesture_result = expression + " = " + result
                        engine = pyttsx3.init()
                        engine.say("Hey. Great.! The answer of.. "  +  gesture_result)
                        engine.runAndWait()
                    except:
                        gesture_result = "Invalid"
                    expression = ""
                    gesture_buffer.clear()

                last_added_time = current_time

            if expression:
                gesture_result = expression

        else:
            gesture_buffer.clear()
            # Keep last gesture_result (no reset)

        # --- Removed text overlay ---
        # cv2.putText(img, gesture_result, (20, 70),
        #             cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

        ret, buffer = cv2.imencode(".jpg", img)
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + buffer.tobytes()
            + b"\r\n"
        )

# ==============================
# DJANGO VIEWS
# ==============================

def index(request):
    return render(request, "index.html")

def airwriting_page(request):
    return render(request, "airwriting.html")

def gesture_page(request):
    return render(request, "gesture.html")

def airwriting_video_feed(request):
    return StreamingHttpResponse(
        airwriting_stream(),
        content_type="multipart/x-mixed-replace; boundary=frame"
    )

def gesture_video_feed(request):
    return StreamingHttpResponse(
        gesture_stream(),
        content_type="multipart/x-mixed-replace; boundary=frame"
    )

def get_airwriting_result(request):
    global response_text
    return JsonResponse({"result": response_text})

def get_gesture_result(request):
    global gesture_result
    return JsonResponse({"result": gesture_result})