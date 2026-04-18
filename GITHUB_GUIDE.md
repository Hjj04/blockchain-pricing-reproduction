# GitHub 仓库创建指南

## 步骤1：在 GitHub 上创建远程仓库

1. 访问 https://github.com/new
2. 填写仓库信息：
   - **Repository name**: `blockchain-pricing-reproduction`
   - **Description**: 基于Stackelberg博弈的区块链车联网数据交易定价模型 - 复现与改进
   - **Visibility**: Private（团队协作）或 Public（开源）
   - **不要**勾选 "Initialize this repository with a README"（我们已经有了）
3. 点击 "Create repository"

## 步骤2：关联本地仓库到远程

```bash
cd /Volumes/Lenovo/学习/区块链技术导论/blockchain-pricing-reproduction

# 添加远程仓库（替换 <your-username> 为你的 GitHub 用户名）
git remote add origin https://github.com/<your-username>/blockchain-pricing-reproduction.git

# 推送代码
git push -u origin main
```

## 步骤3：邀请团队成员

1. 在 GitHub 仓库页面，点击 "Settings" → "Collaborators"
2. 点击 "Add people"
3. 输入队友的 GitHub 用户名或邮箱：
   - 吴玥霖
   - 姜博文
   - 陈可铭
4. 选择权限级别：**Write**（可以推送代码）

## 步骤4：团队成员克隆仓库

队友执行：
```bash
git clone https://github.com/<your-username>/blockchain-pricing-reproduction.git
cd blockchain-pricing-reproduction
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python test_all.py
```

## 步骤5：协作工作流

### 韩喆（你）的工作流
```bash
# 创建自己的开发分支
git checkout -b dev-hanzhe

# 做实验、调参、保存结果
# ... 修改 notebooks ...

# 提交更改
git add notebooks/
git commit -m "feat: 完成收敛性实验，调整参数使迭代次数从166降至30"

# 推送到远程
git push origin dev-hanzhe

# 在 GitHub 上创建 Pull Request，让队友 review
```

### 其他成员的工作流
```bash
# 陈可铭做改进
git checkout -b feature-improvements
# ... 编写改进代码 ...
git commit -m "feat: 实现多消费者竞争模型"
git push origin feature-improvements

# 姜博文更新文档
git checkout -b docs-paper
# ... 更新 README ...
git commit -m "docs: 添加论文引用和实验结果说明"
git push origin docs-paper
```

## 当前仓库状态

```bash
# 查看提交历史
git log --oneline

# 查看文件状态
git status

# 查看分支
git branch -a
```

## 注意事项

1. **不要直接在 main 分支工作**：创建自己的分支
2. **经常 pull**：`git pull origin main` 获取队友的更新
3. **提交前测试**：确保 `python test_all.py` 通过
4. **写清楚 commit message**：让队友知道你做了什么
5. **大文件不要提交**：图片结果可以放在 results/ 目录（已在 .gitignore 中）

## 推荐的 GitHub 仓库设置

### Branch Protection Rules（可选，防止误操作）
Settings → Branches → Add rule:
- Branch name pattern: `main`
- ✓ Require pull request reviews before merging
- ✓ Require status checks to pass before merging

### Issues（任务追踪）
可以在 GitHub Issues 中创建任务：
- Issue #1: 调整收敛参数使迭代次数接近论文
- Issue #2: 实现多消费者竞争改进模型
- Issue #3: 完成 Overleaf 论文初稿

### Projects（看板管理，可选）
Projects → New project → Board:
- Todo: 待完成的任务
- In Progress: 进行中
- Done: 已完成
