from ultralytics import YOLO
import cv2

MODEL_PATH = "best.pt"
FRAME_SIZE = 640

# Load model
model = YOLO(MODEL_PATH)

# Open webcam
cap = cv2.VideoCapture(0)

state = "neutral"

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (FRAME_SIZE, FRAME_SIZE))

    results = model(frame)

    detected_state = "neutral"

    for box in results[0].boxes:
        conf = float(box.conf[0])
        cls_id = int(box.cls[0])
        class_name = model.names[cls_id]

        if conf > 0.6:  # Stability filter
            if class_name == "microsleep":
                detected_state = "microsleep"
                break  # Highest priority
            elif class_name == "yawning":
                detected_state = "yawning"

    state = detected_state

    annotated = results[0].plot()

    cv2.putText(
        annotated,
        f"STATE: {state}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

    cv2.imshow("Driver Monitoring", annotated)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()