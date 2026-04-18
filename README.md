# 基于Stackelberg博弈的区块链车联网数据交易定价模型 - 复现与改进

本项目复现并改进论文《基于Stackelberg博弈的区块链车联网数据交易定价模型》（高春祺，李雷孝，杜金泽）。

## 项目结构

```
blockchain-pricing-reproduction/
├── src/                          # 核心算法模块
│   ├── data_loader.py           # 数据加载与预处理
│   ├── quality_model.py         # 数据质量评估模型
│   ├── stackelberg_model.py     # Stackelberg博弈定价模型（核心）
│   └── baseline_models.py       # 基线对比模型
├── notebooks/                    # 实验Notebook
│   ├── 01_convergence.ipynb     # 图8+9：价格与数量收敛性
│   ├── 02_quality_impact.ipynb  # 图7：数据质量对消费者效益的影响
│   ├── 03_model_comparison.ipynb # 图10：三种定价模型对比
│   └── 04_blockchain_sim.ipynb  # 图4+5+6：区块链性能模拟
├── data/                         # 数据目录
│   └── eua-dataset/             # EUA墨尔本CBD数据集
├── improvements/                 # 改进工作（待完成）
├── test_all.py                  # 单元测试
├── requirements.txt             # Python依赖
└── README.md                    # 本文件
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行测试

```bash
python test_all.py
```

### 3. 运行实验

```bash
# 启动 Jupyter
jupyter notebook

# 或批量执行
jupyter nbconvert --to notebook --execute notebooks/01_convergence.ipynb
jupyter nbconvert --to notebook --execute notebooks/02_quality_impact.ipynb
jupyter nbconvert --to notebook --execute notebooks/03_model_comparison.ipynb
jupyter nbconvert --to notebook --execute notebooks/04_blockchain_sim.ipynb
```

## 团队分工

- **吴玥霖**：核心模块开发（`src/` 目录）
- **韩喆**：实验复现与结果对齐（`notebooks/` 目录）
- **姜博文**：论文撰写与图表整合（Overleaf）
- **陈可铭**：创新方向调研与实现（`improvements/` 目录）

## 进度追踪

### 复现工作（截止周日晚）
- [x] 核心模块开发 - 吴玥霖
- [ ] 实验结果对齐 - 韩喆
- [ ] 论文框架搭建 - 姜博文
- [ ] 创新方向调研 - 陈可铭

### 改进工作（截止下周三）
- [ ] 改进方案设计 - 陈可铭
- [ ] 改进代码实现 - 待分配
- [ ] 改进实验验证 - 待分配

### 整合工作（截止下周四）
- [ ] 论文完整版 - 姜博文
- [ ] 代码优化与开源准备 - 韩喆

## 数据集说明

使用 EUA (Edge User Allocation) 数据集的墨尔本CBD部分：
- 来源：https://github.com/PhuLai/eua-dataset
- 文件：`users-melbcbd-generated.csv`
- 记录数：816条
- 字段：纬度、经度（时间戳为合成数据）

## 参考文献

高春祺, 李雷孝, 杜金泽. 基于Stackelberg博弈的区块链车联网数据交易定价模型[J]. 

## License

MIT License
