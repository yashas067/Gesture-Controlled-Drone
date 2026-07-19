import cv2
from deepface import DeepFace

reference_img_path = "person1.jpg"

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

STATE_SEARCH = "SEARCH"
STATE_FOLLOW = "FOLLOW"

current_state = STATE_SEARCH

cap = cv2.VideoCapture(0)

print("Drone Tracker Activated... Press Q to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    h, w, _ = frame.shape
    frame_center_x = w // 2
    frame_center_y = h // 2

    target_found = False

    for (x, y, w_face, h_face) in faces:
        face_img = frame[y:y+h_face, x:x+w_face]

        try:
            result = DeepFace.verify(
                reference_img_path,
                face_img,
                enforce_detection=False
            )
            if result["verified"]:
                target_found = True
                cv2.rectangle(frame, (x, y), (x+w_face, y+h_face), (0,255,0), 2)

                face_center_x = x + w_face // 2
                face_center_y = y + h_face // 2

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

        except:
            pass

    if current_state == STATE_SEARCH:
        cv2.putText(frame, "STATE: SEARCHING", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

        if target_found:
            current_state = STATE_FOLLOW

    elif current_state == STATE_FOLLOW:
        cv2.putText(frame, "STATE: FOLLOWING", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        if not target_found:
            current_state = STATE_SEARCH

    cv2.circle(frame, (frame_center_x, frame_center_y), 5, (255,0,0), -1)

    cv2.imshow("Drone Tracker", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()