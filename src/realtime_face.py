import cv2
from deepface import DeepFace

reference_img_path = "person1.jpg"

cap = cv2.VideoCapture(0)

print("Starting camera... Press Q to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    try:
        result = DeepFace.verify(
            reference_img_path,
            frame,
            enforce_detection=False
        )

        if result["verified"]:
            cv2.putText(frame, "TARGET FOUND", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 3)
        else:
            cv2.putText(frame, "NO MATCH", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 3)

    except:
        pass

    cv2.imshow("Drone Vision", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()