import asyncio
import cv2
import mediapipe as mp
from mavsdk import System
from mavsdk.offboard import VelocityBodyYawspeed, OffboardError

# =========================
# MEDIAPIPE SETUP
# =========================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

# =========================
# FINGER COUNT FUNCTION
# =========================
def count_fingers(hand_landmarks):
    tips = [8, 12, 16, 20]
    count = 0

    for tip in tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            count += 1

    return count


# =========================
# MAIN DRONE CONTROL
# =========================
async def drone_control():

    drone = System(mavsdk_server_address="localhost", port=50051)
    await drone.connect(system_address="udp://127.0.0.1:14540")

    print("🔄 Waiting for drone connection...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("✅ Drone connected!")
            break

    # =========================
    # SEND INITIAL SETPOINTS
    # =========================
    print("📡 Sending initial setpoints...")
    for _ in range(20):
        await drone.offboard.set_velocity_body(
            VelocityBodyYawspeed(0, 0, 0, 0)
        )
        await asyncio.sleep(0.05)

    # =========================
    # START OFFBOARD MODE
    # =========================
    try:
        await drone.offboard.start()
        print("🚀 Offboard mode started")
    except OffboardError as e:
        print(f"❌ Offboard failed: {e}")
        return

    await asyncio.sleep(1)

    # =========================
    # ARM DRONE
    # =========================
    await drone.action.arm()
    print("🟢 Drone armed")

    # =========================
    # CAMERA START
    # =========================
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Default movement
        forward = 0
        right = 0
        down = 0
        yaw = 0

        gesture = "None"

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:

                fingers = count_fingers(hand_landmarks)

                # =========================
                # GESTURE MAPPING
                # =========================
                if fingers == 1:
                    right = 1.5
                    gesture = "RIGHT →"

                elif fingers == 2:
                    right = -1.5
                    gesture = "← LEFT"

                elif fingers == 3:
                    forward = 2.0
                    gesture = "FORWARD ↑"

                elif fingers == 4:
                    forward = -2.0
                    gesture = "BACKWARD ↓"

                elif fingers == 0:
                    gesture = "LANDING ✊"
                    print("🛑 Landing...")
                    await drone.action.land()
                    await asyncio.sleep(3)
                    continue

        # =========================
        # SEND CONTINUOUS COMMAND
        # =========================
        await drone.offboard.set_velocity_body(
            VelocityBodyYawspeed(forward, right, down, yaw)
        )

        # Display gesture
        cv2.putText(frame, f"Gesture: {gesture}", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Gesture Control", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

        await asyncio.sleep(0.05)

    cap.release()
    cv2.destroyAllWindows()


# =========================
# RUN PROGRAM
# =========================
asyncio.run(drone_control())