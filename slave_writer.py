from st3215 import ST3215  # ST3215 サーボ制御ライブラリのインポート // Import the ST3215 servo control library
import time

class SlaveWriter:
    def __init__(self, port, ids, limits):
        # スレーブ用の ST3215 インスタンスを作成 // Create ST3215 instance for Slave
        self.slave = ST3215(port)
        self.ids = ids            # サーボ名とIDの対応表 // Mapping of servo names to IDs
        self.limits = limits      # 各サーボの安全な位置範囲 // Safe movement limits for each servo

        # 🔛 初期化時にすべてのサーボのトルクをオン // Turn on torque for all servos during initialization
        for sid in self.ids.values():
            self.slave.StartServo(sid)
            print(f"[Init] StartServo {sid}")

    def write_positions(self, positions):
        # 🔁 指定された位置をスレーブサーボに送信 // Send given positions to each slave servo
        for name, pos in positions.items():
            if name in self.ids:
                sid = self.ids[name]
                min_pos, max_pos = self.limits[name]
                # ⛑️ 範囲外の位置はクランプ // Clamp the position within the safe range
                clamped = max(min_pos, min(max_pos, pos))
                self.slave.MoveTo(sid, clamped)  # 指定位置に移動 // Move to clamped position
                print(f"[Slave] {name:10s} (ID {sid}) => {clamped}")

    # === 全サーボのトルクをオフにする関数 ===
    # === Function to disable torque on all servos ===
    def stop_all_torque(self):
        print("[Torque] 全サーボのトルクをオフにします // Turn off torque on all servos")
        for sid in self.ids.values():
            self.slave.StopServo(sid)  # トルクオフ実行 // Execute torque off
            print(f"[Torque] Servo ID {sid} のトルクをオフにしました")
            time.sleep(0.1)  # 💡 通信安定のための待機 // Small delay for stable communication
