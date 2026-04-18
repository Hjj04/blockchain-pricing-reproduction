"""
运行方式：python test_all.py
作用：调用每个模块的函数，确认无报错
"""
import numpy as np
import sys
sys.path.insert(0, 'src')


def test_data_loader():
    from data_loader import load_eua_data, sample_owners, create_consumer
    df = load_eua_data()
    assert len(df) > 0
    owners = sample_owners(df, n_owners=5, seed=42)
    assert len(owners) == 5
    assert 'cost' in owners.columns
    consumer = create_consumer(-37.80, 144.95, 30.0)
    assert 'latitude' in consumer
    print("✓ data_loader 通过")


def test_quality_model():
    from quality_model import haversine_distance, spatial_quality, temporal_quality, compute_quality
    from data_loader import load_eua_data, sample_owners, create_consumer

    # 测试 Haversine
    d = haversine_distance(-37.80, 144.95, -37.81, 144.96)
    assert d > 0 and d < 5

    # 测试空间质量
    q = spatial_quality(5.0, 10.0)
    assert q == 0.5

    # 测试时间质量
    q = temporal_quality(60.0, 60.0)
    assert q == 1.0

    # 测试综合质量
    df = load_eua_data()
    owners = sample_owners(df, n_owners=5, seed=42)
    consumer = create_consumer(-37.80, 144.95, 30.0)
    Q = compute_quality(owners, consumer, 10.0, 60.0, 0.5)
    assert len(Q) == 5
    assert np.all(Q >= 0) and np.all(Q <= 1)
    print("✓ quality_model 通过")


def test_stackelberg():
    from stackelberg_model import (buyer_utility, seller_utility_with_competition,
                                    optimal_buy_quantity, run_stackelberg)
    Q = np.array([0.8, 0.6, 0.7, 0.5, 0.9])
    c = np.array([0.5, 1.0, 0.8, 1.2, 0.6])
    p = np.array([2.0, 3.0, 2.5, 3.5, 1.5])
    x = optimal_buy_quantity(Q, p)
    assert np.all(x >= 0)

    U_b = buyer_utility(Q, x, p)
    U_s = seller_utility_with_competition(Q, x, p, c)
    assert len(U_b) == 5
    assert len(U_s) == 5

    result = run_stackelberg(Q, c, mu=0.01, max_iter=50)
    assert 'price_history' in result
    assert result['price_history'].shape[1] == 5
    print("✓ stackelberg_model 通过")


def test_baselines():
    from baseline_models import run_random_pricing, run_average_pricing
    Q = np.array([0.8, 0.6, 0.7, 0.5, 0.9])
    c = np.array([0.5, 1.0, 0.8, 1.2, 0.6])

    res1 = run_random_pricing(Q, c, max_iter=10)
    assert len(res1['total_utility_history']) == 10

    res2 = run_average_pricing(Q, c, max_iter=10)
    assert len(res2['total_utility_history']) == 10
    print("✓ baseline_models 通过")


if __name__ == '__main__':
    test_data_loader()
    test_quality_model()
    test_stackelberg()
    test_baselines()
    print("\n===== 全部测试通过 =====")
