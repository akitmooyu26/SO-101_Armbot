import csv
import os
from datetime import datetime

class PoseRecorder:
    def __init__(self, filename="poses/wave.csv"):
        os.makedirs("poses", exist_ok=True)
        self.file = open(filename, mode="w", newline='')
        self.writer = csv.writer(self.file)
        self.writer.writerow([
            "timestamp",
            "m_base", "m_shoulder", "m_elbow", "m_wrist", "m_wrist_lift", "m_gripper",
            "s_base", "s_shoulder", "s_elbow", "s_wrist", "s_wrist_lift", "s_gripper"
        ])
        print(f"[Recorder] เริ่มบันทึก → {filename}")

    def record(self, mpos, spos):
        row = [datetime.now().isoformat()]
        for key in ["base", "shoulder", "elbow", "wrist", "wrist_lift", "gripper"]:
            row.append(mpos.get(key, 0))
        for key in ["base", "shoulder", "elbow", "wrist", "wrist_lift", "gripper"]:
            row.append(spos.get(key, 0))
        self.writer.writerow(row)

    def close(self):
        self.file.close()
        print("[Recorder] หยุดบันทึกและปิดไฟล์เรียบร้อยแล้ว")
