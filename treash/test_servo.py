from st3215 import ST3215
import time

PORT = "COM8"
ID = 1

try:
    servo = ST3215(PORT)
    print("✅ Serial connected")

    servo.StartServo(ID)  # เปลี่ยนจาก enable_torque → StartServo
    print("✅ Torque enabled")

    servo.MoveTo(ID, 3000)  # ใช้ MoveTo แทน move หรือ WritePosition
    print("➡️ Moved to 3000")
    time.sleep(2)

    servo.MoveTo(ID, 1000)
    print("⬅️ Moved to 1000")
    time.sleep(2)

    servo.StopServo(ID)  # เปลี่ยนจาก disable_torque → StopServo
    print("❌ Torque disabled")

except Exception as e:
    print("❌ Error:", e)
