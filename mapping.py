def map_position(m_pos, m_min, m_max, s_min, s_max):
    """
    マスター側の位置をスレーブ側の範囲にマッピングする関数  
    Map the position value from Master range to Slave range.
    
    Parameters:
        m_pos (int): マスターからの現在の位置値 // Position value from Master
        m_min, m_max (int): マスターの範囲 // Master range
        s_min, s_max (int): スレーブの範囲 // Slave range

    Returns:
        s_pos (int): マッピング後のスレーブ用位置値 // Mapped position value for Slave
    """
    
    # 🚧 0除算を防ぐ // Prevent division by zero
    if m_max == m_min:
        return s_min

    # 🔁 マスター位置を [0,1] の比率に変換 // Convert master position to ratio [0,1]
    ratio = (m_pos - m_min) / (m_max - m_min)

    # 🧮 比率をスレーブ範囲にスケーリング // Scale ratio into slave's range
    s_pos = int(s_min + ratio * (s_max - s_min))

    # 🛡️ スレーブの範囲内に制限 // Clamp value to slave range
    s_pos = max(s_min, min(s_pos, s_max))
    
    return s_pos
