# Stackelberg博弈定价模型核心：效用函数、最优购买量、梯度迭代算法(Algorithm 1)
import numpy as np


def buyer_utility(Q, x, p):
    """计算消费者效用 U_buyer,i = Q_i * ln(x_i+1) - x_i * p_i，公式(21/26)"""
    return Q * np.log(x + 1) - x * p


def seller_utility(Q, x, p, c):
    """计算卖家基础效用 U_seller,i = x_i * (p_i - c_i)，公式(18)"""
    return x * (p - c)


def seller_utility_with_competition(Q, x, p, c):
    """计算含竞争力的卖家效用 U_seller,i = W_i * x_i * (p_i - c_i)，公式(30)-(31)"""
    N = len(Q)
    w = Q / p                       # 性价比因子
    W = N * w / np.sum(w)           # 公式(30): 数据竞争力
    return W * x * (p - c)          # 公式(31)


def optimal_buy_quantity(Q, p):
    """计算消费者最优购买量 x_i* = Q_i/p_i - 1，公式(29)"""
    x = Q / p - 1.0
    return np.maximum(x, 0.0)


def seller_utility_y(Q, y, c, N):
    """用辅助变量 y_i=1/p_i 重写的卖家效用，公式(33)"""
    sum_Qy = np.sum(Q * y)
    share = (N * Q * y) / sum_Qy    # 市场份额
    surplus = Q * y - 1              # 购买量 x_i
    margin = 1.0 / y - c            # 价格利润 p_i - c_i
    return share * surplus * margin


def gradient_seller_utility_y(Q, y, c, i):
    """计算第i个所有者效用对y_i的偏导数，公式(34)"""
    N_val = len(Q)
    # S = Σ_{z≠i} (Q_z / Q_i) * y_z
    mask = np.arange(N_val) != i
    S = np.sum((Q[mask] / Q[i]) * y[mask])

    yi = y[i]
    Qi = Q[i]
    ci = c[i]

    # 公式(34): 分子 = Q_i*c_i*y_i² + (2*Q_i*c_i*y_i - Q_i - c_i)*S - 1
    numerator = Qi * ci * yi**2 + (2 * Qi * ci * yi - Qi - ci) * S - 1
    # 分母 = (S + y_i)²
    denominator = (S + yi)**2

    return -N_val * numerator / denominator


def run_stackelberg(Q, c, p_max=10.0, x_min=0.0, x_max=15.0, mu=0.01, max_iter=100, tol=1e-6):
    """Algorithm 1: Stackelberg纳什均衡梯度迭代算法"""
    N = len(Q)

    # 初始化：价格取成本与最高价的中间值
    p = (c + p_max) / 2.0
    y = 1.0 / p
    x = np.maximum(Q / p - 1.0, 0.0)

    price_history = []
    quantity_history = []
    buyer_util_history = []
    seller_util_history = []
    total_util_history = []
    converged = False

    for t in range(max_iter):
        # 记录当前状态
        price_history.append(p.copy())
        quantity_history.append(x.copy())
        U_buyer = buyer_utility(Q, x, p)
        U_seller = seller_utility_with_competition(Q, x, p, c)
        buyer_util_history.append(U_buyer.copy())
        seller_util_history.append(U_seller.copy())
        total_util_history.append(np.sum(U_buyer) + np.sum(U_seller))

        # 公式(29): 消费者最优购买量
        x_new = np.clip(optimal_buy_quantity(Q, p), x_min, x_max)

        # 公式(34): 梯度上升更新 y
        y_new = y.copy()
        for i in range(N):
            grad_i = gradient_seller_utility_y(Q, y, c, i)
            y_new[i] = y[i] + mu * grad_i  # 梯度上升（最大化效用）

        # clip y_i ∈ [1/p_max, 1/c_i]
        for i in range(N):
            y_new[i] = np.clip(y_new[i], 1.0 / p_max, 1.0 / c[i])

        p_new = 1.0 / y_new

        # 收敛判定
        if np.max(np.abs(y_new - y)) < tol:
            converged = True
            y, p, x = y_new, p_new, x_new
            price_history.append(p.copy())
            quantity_history.append(x.copy())
            U_buyer = buyer_utility(Q, x, p)
            U_seller = seller_utility_with_competition(Q, x, p, c)
            buyer_util_history.append(U_buyer.copy())
            seller_util_history.append(U_seller.copy())
            total_util_history.append(np.sum(U_buyer) + np.sum(U_seller))
            break

        y, p, x = y_new, p_new, x_new

    return {
        'price_history': np.array(price_history),
        'quantity_history': np.array(quantity_history),
        'buyer_utility_history': np.array(buyer_util_history),
        'seller_utility_history': np.array(seller_util_history),
        'total_utility_history': np.array(total_util_history),
        'converged': converged,
        'iterations': len(price_history)
    }
