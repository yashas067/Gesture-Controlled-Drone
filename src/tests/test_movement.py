import asyncio
import cv2
import mediapipe as mp
from mavsdk import System
from mavsdk.offboard import VelocityBodyYawspeed

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

def count_fingers(hand_landmarks):
    tips = [8, 12, 16, 20]
    count = 0
    for tip in tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            count += 1
    return count

async def drone_control():
    drone = System()
    await drone.connect(system_address="udp://127.0.0.1:14540")

    print("Connected")

    # Initial setpoints
    for _ in range(20):
        await drone.offboard.set_velocity_body(
            VelocityBodyYawspeed(0, 0, 0, 0)
        )
        await asyncio.sleep(0.05)

    await drone.offboard.start()
    await drone.action.arm()

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        forward = 0
        right = 0
        down = 0
        yaw = 0

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                fingers = count_fingers(hand_landmarks)

                # 🎯 Gesture mapping
                if fingers == 1:
                    right = 1.0
                elif fingers == 2:
                    right = -1.0
                elif fingers == 3:
                    forward = 1.0
                elif fingers == 4:
                    forward = -1.0
                elif fingers == 0:
                    print("Landing...")
                    await drone.action.land()
                    break

        # 🔥 CONTINUOUS COMMAND (MOST IMPORTANT)
        await drone.offboard.set_velocity_body(
            VelocityBodyYawspeed(forward, right, down, yaw)
        )

        await asyncio.sleep(0.05)

        cv2.imshow("Gesture", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

asyncio.run(drone_control())