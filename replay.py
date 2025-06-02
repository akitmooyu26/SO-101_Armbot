import csv
import time
from st3215 import ST3215  # ST3215 サーボライブラリのインポート // Import ST3215 servo control library

# 🧠 サーボの名前とIDのマッピング // Mapping servo names to their IDs
servo_ids = {
    "base": 1,
    "shoulder": 2,
    "elbow": 3,
    "wrist": 4,
    "wrist_lift": 5,
    "gripper": 6,
}

# 🔒 スレーブ側サーボの安全範囲 // Safe movement limits for each slave servo
servo_limits = {
    "base": (850, 3280),
    "shoulder": (940, 3000),
    "elbow": (1000, 3060),
    "wrist": (1000, 2800),
    "wrist_lift": (930, 3080),
    "gripper": (1820, 3110),
}

# 🧾 再生するポーズファイルのパス // Path to pose CSV file to replay
pose_file = "poses/grab_and_place.csv"  # ← 必要に応じてファイル名を変更 // Change this to your desired file

# 📡 スレーブとの通信ポートを開く // Open serial connection to the slave
slave = ST3215("COM8")

# ⚙️ すべてのサーボのトルクをオン // Enable torque on all servos
for sid in servo_ids.values():
    slave.StartServo(sid)
    print(f"[Init] 開始 Servo ID {sid}")

print(f"\n🎬 CSVファイルからポーズを再生: {pose_file}\n")  # Start replay message

# 📖 CSVファイルを読み込んで再生実行 // Read and replay motions from CSV
with open(pose_file, newline='') as f:
    reader = csv.DictReader(f)

    for row in reader:
        for name, sid in servo_ids.items():
            sval = int(row.get(f"s_{name}", 0))  # CSV から s_◯◯ の値を取得 // Get value from column like s_base, s_elbow
            smin, smax = servo_limits[name]
            clamped = max(smin, min(smax, sval))  # 範囲を超えた場合は制限 // Clamp value to safe limits
            slave.MoveTo(sid, clamped)  # サーボを目的位置に移動 // Move servo to target position
            print(f"[Replay] {name:10s} → {clamped}")
        time.sleep(0.01)  # ⏱️ 再生速度の調整 // Adjust speed of replay

# ✅ 再生終了後、すべてのサーボのトルクをオフ // After replay, turn off all servos
print("\n🛑 ポーズ再生完了 → 全サーボのトルクをオフ")
for sid in servo_ids.values():
    slave.StopServo(sid)
    print(f"[StopTorque] Servo ID {sid} を無効化しました")
