from st3215 import ST3215
from st3215.group_sync_write import GroupSyncWrite
import time

class ArmbotController:
    def __init__(self, port, servo_ids: dict):
        self.servo = ST3215(port)
        self.ids = servo_ids
        print("✅ Armbot connected!")

        # 📌 EEPROM-based Limit Positions (จาก FT SCServo Debug)
        self.limits = {
            "base":       (810, 3370),
            "shoulder":   (130, 2100),
            "elbow":      (935, 3000),
            "wrist":      (2130, 4095),
            "wrist_lift": (220, 3840),
            "gripper":    (1786, 2940),
        }

    def clamp_position(self, joint, pos):
        if joint not in self.limits:
            return pos
        min_pos, max_pos = self.limits[joint]
        return max(min_pos, min(max_pos, pos))

    def set_pose_sync(self, speed=700, acc=30, **kwargs):
        gsync = GroupSyncWrite(self.servo, 0x2A, 2)
        for name, pos in kwargs.items():
            sid = self.ids[name]
            self.servo.SetSpeed(sid, speed)
            self.servo.SetAcceleration(sid, acc)
            clamped = self.clamp_position(name, pos)
            gsync.addParam(sid, [clamped & 0xFF, (clamped >> 8) & 0xFF])
        gsync.txPacket()
        gsync.clearParam()

    def is_at_position(self, joint, target, threshold=25):
        sid = self.ids[joint]
        try:
            pos = self.servo.ReadPosition(sid)
            print(f"{joint} = {pos} (target {target})")
            if pos is not None and abs(pos - target) < threshold:
                return True
        except Exception as e:
            print(f"ReadPosition error {joint}: {e}")
        return False

    def go_home(self, repeat=4):
        home_pose = {
            "base": 2102,
            "shoulder": 4093,
            "elbow": 2648,
            "wrist": 2042,
            "wrist_lift": 3808,
            "gripper": 1827
        }
        for _ in range(repeat):
            self.set_pose_sync(**home_pose)
            time.sleep(0.45)

        for attempt in range(4):
            all_at_home = True
            for joint in home_pose:
                if not self.is_at_position(joint, home_pose[joint]):
                    print(f"Resending {joint} to {home_pose[joint]}")
                    self.set_pose_sync(**{joint: home_pose[joint]})
                    all_at_home = False
            if all_at_home:
                break
            time.sleep(0.2)
        print("🏠 แขนกลับบ้านเป๊ะทุกข้อแล้ว!")
        

    def grip(self, grip_value=1900, repeat=3):
        """บีบ gripper เพื่อหยิบของ"""
        pose = {
            "gripper": grip_value
        }
        for _ in range(repeat):
            self.set_pose_sync(**pose)
            time.sleep(0.25)
        print("🤏 Gripper: หยิบของเรียบร้อย")


    def release(self, release_value=2700, repeat=3):
        """คลาย gripper เพื่อปล่อยของ"""
        pose = {
            "gripper": release_value
        }
        for _ in range(repeat):
            self.set_pose_sync(**pose)
            time.sleep(0.25)
        print("🖐️ Gripper: ปล่อยของแล้ว")
    

    def power_off(self):
        for sid in self.ids.values():
            self.servo.StopServo(sid)
        print("❌ Torque OFF ทุกข้อแล้ว")


    def move_to_pose(self, pose_dict, repeat=4, wait=0.45):
        for _ in range(repeat):
            self.set_pose_sync(**pose_dict)
            time.sleep(wait)

        for attempt in range(4):
            all_at_pose = True
            for joint in pose_dict:
                if not self.is_at_position(joint, pose_dict[joint]):
                    print(f"Resending {joint} to {pose_dict[joint]}")
                    self.set_pose_sync(**{joint: pose_dict[joint]})
                    all_at_pose = False
            if all_at_pose:
                break
            time.sleep(0.1)
        print("🦾 ขยับไปที่ pose เป๊ะทุกข้อแล้ว!")
