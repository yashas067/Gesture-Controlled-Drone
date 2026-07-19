import cv2
from deepface import DeepFace

reference_img_path = "person1.jpg"

STATE_SEARCH = "SEARCH"
STATE_FOLLOW = "FOLLOW"

current_state = STATE_SEARCH

cap = cv2.VideoCapture(0)

print("Drone Brain Activated...")
print("Press Q to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    frame_center_x = w // 2
    frame_center_y = h // 2

    try:
        result = DeepFace.verify(
            reference_img_path,
            frame,
            enforce_detection=False
        )

        target_found = result["verified"]

    except:
        target_found = False

    if current_state == STATE_SEARCH:
        cv2.putText(frame, "STATE: SEARCHING", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        if target_found:
            current_state = STATE_FOLLOW

    elif current_state == STATE_FOLLOW:
        cv2.putText(frame, "STATE: FOLLOWING", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if not target_found:
            current_state = STATE_SEARCH
        else:
            # Simulated movement logic
            face_center_x = frame_center_x
            face_center_y = frame_center_y

            offset_x = face_center_x - frame_center_x
            offset_y = face_center_y - frame_center_y

            if offset_x > 50:
                print("Move Right")
            elif offset_x < -50:
                print("Move Left")

            if offset_y > 50:
                print("Move Down")
            elif offset_y < -50:
                print("Move Up")

    cv2.imshow("Drone Brain", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()