from ultralytics import YOLO
import cv2
import serial
import time

MODEL_PATH = "best.pt"
SERIAL_PORT = "COM9"
BAUD_RATE = 9600
FRAME_SIZE = 640

model = YOLO(MODEL_PATH)
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

time.sleep(2)

cap = cv2.VideoCapture(0)

state = "neutral"

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (FRAME_SIZE, FRAME_SIZE))

    results = model(frame)

    # 🧠 Flags for priority logic
    microsleep_detected = False
    yawning_detected = False

    for box in results[0].boxes:

        conf = float(box.conf[0])
        cls_id = int(box.cls[0])
        class_name = model.names[cls_id]

        if conf > 0.6:

            if class_name == "microsleep":
                microsleep_detected = True

            elif class_name == "yawning":
                yawning_detected = True

    # 🏆 PRIORITY DECISION ⭐⭐⭐⭐⭐
    if microsleep_detected:
        state = "microsleep"

    elif yawning_detected:
        state = "yawning"

    else:
        state = "neutral"

    # -------- SERIAL SIGNALS --------
    if state == "microsleep":
        ser.write(b'D')   # CRITICAL

    elif state == "yawning":
        ser.write(b'W')   # WARNING

    else:
        ser.write(b'A')   # NORMAL

    annotated = results[0].plot()

    cv2.putText(annotated, f"STATE: {state}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2)

    cv2.imshow("Driver Monitoring", annotated)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
ser.close()