# 基线模型：随机定价模型和平均定价模型，用于图10对比实验
import numpy as np
from stackelberg_model import buyer_utility, seller_utility_with_competition, optimal_buy_quantity


def run_random_pricing(Q, c, p_max=10.0, x_min=0.0, x_max=15.0, max_iter=100, seed=None):
    """随机定价模型：每次迭代随机生成价格，购买量用消费者最优响应"""
    rng = np.random.RandomState(seed)
    N = len(Q)
    price_history = []
    quantity_history = []
    total_util_history = []

    for t in range(max_iter):
        p = np.array([rng.uniform(c[i], p_max) for i in range(N)])
        # 消费者最优响应：公式(29)
        x = np.clip(optimal_buy_quantity(Q, p), x_min, x_max)
        U_buyer = buyer_utility(Q, x, p)
        U_seller = seller_utility_with_competition(Q, x, p, c)
        price_history.append(p.copy())
        quantity_history.append(x.copy())
        total_util_history.append(np.sum(U_buyer) + np.sum(U_seller))

    return {
        'price_history': np.array(price_history),
        'quantity_history': np.array(quantity_history),
        'total_utility_history': np.array(total_util_history)
    }


def run_average_pricing(Q, c, p_max=10.0, x_min=0.0, x_max=15.0, max_iter=100, n_bids=10, seed=42):
    """平均定价模型：模拟多个消费者出价取均值定价，购买量用消费者最优响应"""
    rng = np.random.RandomState(seed)
    N = len(Q)
    price_history = []
    quantity_history = []
    total_util_history = []

    for t in range(max_iter):
        all_prices = np.zeros((n_bids, N))
        for b in range(n_bids):
            for i in range(N):
                # 出价与数据质量成正比
                all_prices[b, i] = min(rng.uniform(c[i], c[i] + Q[i]), p_max)

        p = np.mean(all_prices, axis=0)
        # 消费者最优响应：公式(29)
        x = np.clip(optimal_buy_quantity(Q, p), x_min, x_max)
        U_buyer = buyer_utility(Q, x, p)
        U_seller = seller_utility_with_competition(Q, x, p, c)
        price_history.append(p.copy())
        quantity_history.append(x.copy())
        total_util_history.append(np.sum(U_buyer) + np.sum(U_seller))

    return {
        'price_history': np.array(price_history),
        'quantity_history': np.array(quantity_history),
        'total_utility_history': np.array(total_util_history)
    }
