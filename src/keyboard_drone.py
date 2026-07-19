import asyncio
import keyboard
from mavsdk import System
from mavsdk.offboard import OffboardError, VelocityBodyYawspeed

async def run():

    drone = System()
    await drone.connect(system_address="udpin://0.0.0.0:14551")

    print("Waiting for drone connection...")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone connected!")
            break

    print("""
Controls:
T → Takeoff
L → Land
W → Forward
S → Backward
A → Left
D → Right
Q → Rotate Left
E → Rotate Right
ESC → Exit
""")

    await drone.action.arm()

    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0)
    )

    try:
        await drone.offboard.start()
    except OffboardError as error:
        print("Offboard start failed:", error)
        return

    while True:

        forward = 0
        right = 0
        yaw = 0

        if keyboard.is_pressed('w'):
            forward = 1

        if keyboard.is_pressed('s'):
            forward = -1

        if keyboard.is_pressed('a'):
            right = -1

        if keyboard.is_pressed('d'):
            right = 1

        if keyboard.is_pressed('q'):
            yaw = -30

        if keyboard.is_pressed('e'):
            yaw = 30

        if keyboard.is_pressed('t'):
            print("Takeoff")
            await drone.action.takeoff()

        if keyboard.is_pressed('l'):
            print("Landing")
            await drone.action.land()

        if keyboard.is_pressed('esc'):
            print("Stopping")
            break

        await drone.offboard.set_velocity_body(
            VelocityBodyYawspeed(forward, right, 0.0, yaw)
        )

        await asyncio.sleep(0.1)

asyncio.run(run())