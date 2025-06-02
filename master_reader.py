from st3215 import ST3215  # ST3215 サーボ制御ライブラリのインポート // Import ST3215 servo control library

class MasterReader:
    def __init__(self, port, ids, limits):
        # ST3215 インスタンスを初期化（マスター側） // Initialize ST3215 instance for Master
        self.master = ST3215(port)
        self.ids = ids          # 各サーボの名前とIDのマッピング // Mapping of servo names to their IDs
        self.limits = limits    # 各サーボの動作制限範囲 // Position limits for each servo

    def read_positions(self):
        positions = {}  # 読み取ったポジションを保存する辞書 // Dictionary to store read positions
        for name, sid in self.ids.items():
            pos = self.master.ReadPosition(sid)  # 各サーボから現在の位置を読み取る // Read position from each servo
            if pos is not None:
                positions[name] = pos  # 成功時、辞書に追加 // Store value if read was successful
            else:
                # 読み取り失敗時の警告表示 // Show warning if read failed
                print(f"[Warning] Master: ReadPosition failed for {name} (ID {sid})")
        return positions  # 全サーボの読み取り結果を返す // Return all read positions
