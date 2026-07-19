import cv2
import mediapipe as mp

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path="hand_landmarker.task"),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1
)

landmarker = HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

frame_id = 0

print("Press ESC to exit")

while True:

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

    result = landmarker.detect_for_video(mp_image, frame_id)

    if result.hand_landmarks:

        for hand_landmarks in result.hand_landmarks:

            h, w, _ = frame.shape

            for lm in hand_landmarks:
                cx = int(lm.x * w)
                cy = int(lm.y * h)
                cv2.circle(frame,(cx,cy),5,(0,255,0),-1)

            # fingertip indexes
            thumb = hand_landmarks[4]
            index = hand_landmarks[8]
            middle = hand_landmarks[12]
            ring = hand_landmarks[16]
            pinky = hand_landmarks[20]

            gesture = ""

            if index.y < hand_landmarks[6].y and middle.y < hand_landmarks[10].y:
                gesture = "OPEN HAND"

            if index.y > hand_landmarks[6].y and middle.y > hand_landmarks[10].y:
                gesture = "FIST"

            cv2.putText(frame, gesture,(50,50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,(0,255,0),3)

    cv2.imshow("Gesture Recognition", frame)

    frame_id += 1

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()