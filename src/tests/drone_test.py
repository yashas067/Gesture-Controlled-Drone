import asyncio
from mavsdk import System

async def run():
    print("Starting script...")

    drone = System()
    await drone.connect(system_address="udpin://0.0.0.0:14551")

    print("Waiting for drone connection...")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone connected!")
            break

    print("Arming...")
    await drone.action.arm()

    print("Taking off...")
    await drone.action.takeoff()

    await asyncio.sleep(5)

    print("Landing...")
    await drone.action.land()

if __name__ == "__main__":
    asyncio.run(run())