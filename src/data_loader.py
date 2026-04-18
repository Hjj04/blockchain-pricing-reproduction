# 数据加载与预处理：加载EUA数据集，抽样数据所有者，创建消费者
import os
import numpy as np
import pandas as pd

# 真实EUA数据集默认路径（相对于项目根目录）
_DEFAULT_EUA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'eua-dataset',
                                 'users', 'users-melbcbd-generated.csv')


def load_eua_data(filepath=_DEFAULT_EUA_PATH):
    """加载EUA数据集CSV文件，返回包含 latitude, longitude, timestamp 列的 DataFrame。
    时间戳为合成数据（EUA数据集仅含坐标），论文未公布具体值。"""
    if filepath is not None and os.path.exists(filepath):
        df = pd.read_csv(filepath)
        # EUA Melbourne CBD CSV 列名: Latitude, Longitude（无时间戳）
        df = df.rename(columns={'Latitude': 'latitude', 'Longitude': 'longitude'})
        # 合成时间戳：EUA数据集无此字段，用随机值模拟（0~120分钟）
        rng = np.random.RandomState(0)
        df['timestamp'] = rng.uniform(0, 120, len(df))
        return df[['latitude', 'longitude', 'timestamp']]
    else:
        # Fallback：文件不存在时使用模拟数据
        if filepath is not None:
            print(f"警告: EUA数据文件不存在 ({filepath})，使用模拟数据")
        np.random.seed(0)
        n = 100
        df = pd.DataFrame({
            'latitude': np.random.uniform(-37.85, -37.75, n),
            'longitude': np.random.uniform(144.90, 145.00, n),
            'timestamp': np.random.uniform(0, 120, n)
        })
        return df


def sample_owners(df, n_owners=5, seed=42):
    """从DataFrame中随机抽样n_owners个数据所有者，并生成成本c_i∈[0.5, 2.0]"""
    rng = np.random.RandomState(seed)
    indices = rng.choice(len(df), size=n_owners, replace=False)
    owners = df.iloc[indices].reset_index(drop=True)
    owners['cost'] = rng.uniform(0.5, 2.0, n_owners)
    return owners


def create_consumer(lat, lon, time_point):
    """创建数据消费者字典"""
    return {'latitude': lat, 'longitude': lon, 'timestamp': time_point}
