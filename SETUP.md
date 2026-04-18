# 环境搭建指南

## 1. 克隆仓库（待创建GitHub远程仓库后）

```bash
git clone <your-github-repo-url>
cd blockchain-pricing-reproduction
```

## 2. 创建虚拟环境

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows
```

## 3. 安装依赖

```bash
pip install -r requirements.txt
```

## 4. 验证安装

```bash
python test_all.py
```

预期输出：
```
✓ data_loader 通过
✓ quality_model 通过
✓ stackelberg_model 通过
✓ baseline_models 通过

===== 全部测试通过 =====
```

## 5. 启动 Jupyter Notebook

```bash
# 安装 Jupyter（如果还没安装）
pip install jupyter

# 启动 Jupyter
jupyter notebook
```

浏览器会自动打开，导航到 `notebooks/` 目录运行实验。

## 6. 数据集说明

EUA 数据集已包含在 `data/eua-dataset/` 目录中（git忽略）。如果缺失，请从以下地址克隆：

```bash
cd data
git clone https://github.com/PhuLai/eua-dataset.git
```

使用的文件：`data/eua-dataset/users/users-melbcbd-generated.csv`

## 常见问题

### Q: 提示 "externally-managed-environment" 错误
A: 使用虚拟环境（见步骤2），不要直接用系统Python安装包。

### Q: 找不到 numpy/pandas 等模块
A: 确保已激活虚拟环境（命令行前缀应显示 `(venv)`），然后重新安装依赖。

### Q: Jupyter 找不到虚拟环境的包
A: 在虚拟环境中安装 ipykernel：
```bash
pip install ipykernel
python -m ipykernel install --user --name=venv
```
然后在 Jupyter 中选择 "venv" 内核。

## 团队协作

### 分支策略
- `main`：稳定版本
- `dev-<name>`：个人开发分支（如 `dev-hanzhe`）
- `feature-<name>`：功能分支（如 `feature-improvements`）

### 提交规范
```bash
git commit -m "类型: 简短描述

详细说明（可选）"
```

类型：
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具相关
