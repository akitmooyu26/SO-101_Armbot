🤖 Armbot SO-101 – Master-Slave Robot Arm + Motion Replay

This is a Python-based robotic arm control system using Master–Slave teleoperation with motion recording & replay capabilities.
これはPythonで作られた、ロボットアームのマスター・スレーブ制御＋動作記録＆再生のプロジェクトです。

🎯 Features | 主な機能

🔁 Real-time Master–Slave control （リアルタイム制御）

💾 Record movements to CSV （CSVに動作を記録）

⏪ Replay saved poses anytime （保存した動作の再現）

🛡️ Servo safety limits & range mapping （サーボ範囲のマッピングと安全制御）

📴 Auto torque off after stop （終了時に自動でトルクOFF）


________________________________________________________________________________________________________________________

⚙️ How to Use | 使い方
① リアルタイム制御 + 録画

[python main.py]----> in terminal 

② 録画済みの動作を再生

[python replay.py]----> in terminal 


📂 Project Files | 構成

- main.py – Real-time Master–Slave control & recording
- replay.py – Motion replay from CSV
- poses/ – 保存した動作（CSVファイル）
- slave_writer.py, master_reader.py, mapping.py, recorder.py
- st3215.py – Servo 通信ライブラリ

🧰 Requirements | 実行環境

-Python 3.8+
-pyserial
-2 robotic arms (Master + Slave)
-ST3215-based servo motors



💡 Tips

-Use .stop_all_torque() after Ctrl+C to prevent jitter.
-Add a small time.sleep() between updates for stability.
-Adjust deadband or smoothing if needed (optional).


