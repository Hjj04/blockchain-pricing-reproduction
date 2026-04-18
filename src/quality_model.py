# 数据质量评估模型：Haversine距离、空间/时间质量、综合质量因子
import numpy as np


def haversine_distance(lat1, lon1, lat2, lon2, R=6371.0):
    """计算两个经纬度坐标点之间的地表距离（km），公式(12)-(15)"""
    lat1, lon1, lat2, lon2 = map(np.asarray, [lat1, lon1, lat2, lon2])
    dlat = np.radians(lat1 - lat2)  # 公式(12)
    dlon = np.radians(lon1 - lon2)
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    # 公式(13)
    a = np.sin(dlat / 2)**2 + np.cos(phi2) * np.cos(phi1) * np.sin(dlon / 2)**2
    # 公式(14)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    # 公式(15)
    return R * c


def spatial_quality(position_diff, theta_p):
    """计算空间质量因子 Q_position∈[0,1]，公式(16)"""
    Q_pos = 1.0 - np.asarray(position_diff) / theta_p
    return np.clip(Q_pos, 0.0, 1.0)


def temporal_quality(timediff, theta_t):
    """计算时间质量因子 Q_timediff∈[0,1]，公式(17)"""
    Q_time = 1.0 - np.abs(np.asarray(timediff) - theta_t) / theta_t
    return np.clip(Q_time, 0.0, 1.0)


def compute_quality(owners_df, consumer, theta_p=10.0, theta_t=60.0, alpha=0.5):
    """计算所有数据所有者的综合质量因子 Q_i∈[0,1]"""
    lats = owners_df['latitude'].values
    lons = owners_df['longitude'].values
    times = owners_df['timestamp'].values

    # 公式(12)-(15): 地表距离
    dists = haversine_distance(lats, lons, consumer['latitude'], consumer['longitude'])
    # 公式(16): 空间质量
    Q_pos = spatial_quality(dists, theta_p)
    # 公式(17): 时间质量
    timediffs = np.abs(times - consumer['timestamp'])
    Q_time = temporal_quality(timediffs, theta_t)
    # 综合质量
    Q = alpha * Q_pos + (1 - alpha) * Q_time

    assert np.all(Q >= 0) and np.all(Q <= 1), f"Q值越界: {Q}"
    return Q
