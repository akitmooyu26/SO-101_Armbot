import time
from master_reader import MasterReader  # 📥 Master からサーボ位置を読むクラス // Class to read servo positions from Master
from slave_writer import SlaveWriter    # 📤 Slave へサーボ位置を書き込むクラス // Class to write servo positions to Slave
from mapping import map_position        # 🎯 Master から Slave へのマッピング関数 // Mapping function from Master to Slave
from treash.recorder import PoseRecorder       # 💾 ポーズをCSVファイルに記録するクラス // Class to record poses into CSV

# 🔌 シリアルポートの設定 // Serial Port Configuration
MASTER_PORT = "COM5"
SLAVE_PORT = "COM8"

# 🧠 サーボIDのマッピング // Servo ID Mapping
servo_ids = {
    "base": 1,
    "shoulder": 2,
    "elbow": 3,
    "wrist": 4,
    "wrist_lift": 5,
    "gripper": 6,
}

# 📐 マスターとスレーブのサーボ位置制限 // Position limits for Master and Slave servos
master_limits = {
    "base": (800, 3350),
    "shoulder": (950, 3000),
    "elbow": (1050, 3000),
    "wrist": (1050, 3000),
    "wrist_lift": (1000, 3200),
    "gripper": (1400, 2550),
}
slave_limits = {
    "base": (850, 3280),
    "shoulder": (940, 3000),
    "elbow": (1000, 3060),
    "wrist": (1000, 2800),
    "wrist_lift": (930, 3080),
    "gripper": (1820, 3110),
}

# 🚀 オブジェクトの初期化 // Initialize Master, Slave, and Recorder objects
master = MasterReader(MASTER_PORT, servo_ids, master_limits)
slave = SlaveWriter(SLAVE_PORT, servo_ids, slave_limits)
recorder = PoseRecorder("poses/justTry.csv")  # 💾 ポーズをCSVに保存 // Save poses to CSV

print("\n🦾 Record_Pose (Ctrl+Cで停止)\n")  # ユーザー通知 // User Notification

try:
    while True:
        # 📥 Master から位置を取得 // Read positions from Master
        mpos = master.read_positions()
        spos = {}

        for name in servo_ids:
            if name in mpos:
                val = mpos[name]
                mmin, mmax = master_limits[name]
                smin, smax = slave_limits[name]

                # 🔒 制限範囲外の値をクランプ // Clamp values to avoid out-of-bounds
                margin = 10
                if val < mmin + margin:
                    print(f"[WARN] {name} 低すぎる → Clamp {val} → {mmin + margin}")
                    val = mmin + margin
                if val > mmax - margin:
                    print(f"[WARN] {name} 高すぎる → Clamp {val} → {mmax - margin}")
                    val = mmax - margin

                # 🔁 Master → Slave にマッピング // Map Master value to Slave range
                mapped = map_position(val, mmin, mmax, smin, smax)
                spos[name] = mapped

                print(f"[MAP] {name:10s}: {val:4d} (M) → {mapped:4d} (S)")

        # 📤 Slave へ位置を送信 // Send mapped positions to Slave
        slave.write_positions(spos)

        # 💾 Master と Slave の位置を記録 // Record both Master and Slave positions
        recorder.record(mpos, spos)

        # ⏱️ 実行頻度の調整 // Control the loop frequency
        time.sleep(0.1)  # 秒単位でスリープ // Sleep in seconds

except KeyboardInterrupt:
    # 🛑 Ctrl+C が押された場合の終了処理 // When Ctrl+C is pressed
    print("\n🛑 システム停止 (Ctrl+C)")
    recorder.close()
    slave.stop_all_torque()  # 全てのトルクを停止 // Stop all servo torque
    time.sleep(0.3)          # コマンド送信の待機時間 // Delay for command transmission
    print("[System] 全てのトルク停止コマンドを送信完了")
    slave.stop_all_torque()  # 念のためもう一度送信 // Send again just in case
