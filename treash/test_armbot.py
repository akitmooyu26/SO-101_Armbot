from armbot_controller import ArmbotController
import time

servo_ids = {
    "base": 1,
    "shoulder": 2,
    "elbow": 3,
    "wrist": 4,
    "wrist_lift": 5,
    "gripper": 6
}

armbot = ArmbotController(port="COM8", servo_ids=servo_ids)
time.sleep(2)

# 🏠 กลับบ้านก่อน
armbot.go_home()
time.sleep(1)

# 👋 ขยับไป pose ใหม่
target_pose = {
    "base": 2862,
    "shoulder": 1494,
    "elbow": 1496,
    "wrist": 81,
    "wrist_lift": 3802,
 
}

armbot.release()  # ปล่อย gripper


armbot.move_to_pose(target_pose, repeat=4)
time.sleep(1)

# ⏪ กลับบ้านอีกครั้ง


time.sleep(2)
armbot.grip()  # บีบ gripper


armbot.go_home()


# 🔚 ปิด torque ทุกข้อ
armbot.power_off()
