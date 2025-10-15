# GitHub项目多SSH密钥配置指南

本文档介绍如何为不同的GitHub项目配置不同的SSH密钥，避免密钥冲突。

## 概述

当需要在同一台机器上管理多个GitHub账户或项目时，可以为每个项目配置不同的SSH密钥。本文提供了完整的配置方案。

## SSH配置文件设置

### 1. 创建或编辑SSH配置文件

SSH配置文件位置：`~/.ssh/config`

### 2. 配置示例

```bash
# 个人项目配置
Host github-personal
  HostName github.com
  User git
  PreferredAuthentications publickey
  IdentityFile ~/.ssh/id_rsa-personal
  IdentitiesOnly yes

# 工作项目配置
Host github-work
  HostName github.com
  User git
  PreferredAuthentications publickey
  IdentityFile ~/.ssh/id_rsa-work
  IdentitiesOnly yes

# 原有项目配置（通过HTTPS over SSH）
Host github.com
  HostName ssh.github.com
  User git
  Port 443
  PreferredAuthentications publickey
  IdentityFile ~/.ssh/id_rsa-yxy
  IdentitiesOnly yes

# 新项目配置
Host github-metaforge
  HostName ssh.github.com
  User git
  Port 443
  PreferredAuthentications publickey
  IdentityFile ~/.ssh/id_rsa-metaforge
  IdentitiesOnly yes
```

## 项目配置步骤

### 步骤1：生成SSH密钥

为每个项目生成独立的SSH密钥：

```bash
# 为个人项目生成密钥
ssh-keygen -t rsa -b 4096 -C "your-personal-email@example.com" -f ~/.ssh/id_rsa-personal

# 为工作项目生成密钥
ssh-keygen -t rsa -b 4096 -C "your-work-email@example.com" -f ~/.ssh/id_rsa-work
```

### 步骤2：添加公钥到对应GitHub账户

将对应的公钥（`.pub`文件）添加到相应的GitHub账户设置中。

### 步骤3：配置项目Remote URL

对于需要使用不同SSH密钥的项目，需要更新其remote URL：

#### 情况A：新项目（使用SSH Host别名）

```bash
cd /path/to/your/project
git remote set-url origin git@github-personal:username/repository.git
```

#### 情况B：已有项目修改remote

```bash
cd /path/to/your/project
git remote -v  # 查看当前remote
git remote set-url origin git@github-work:username/repository.git
```

### 步骤4：验证配置

```bash
# 测试SSH连接
ssh -T git@github-personal
ssh -T git@github-work

# 验证git操作
git pull origin main
git push origin main
```

## 常见配置模式

### 模式1：基于Host别名

```bash
# 使用不同的Host别名
Host github-personal
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_rsa-personal

Host github-work
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_rsa-work
```

### 模式2：基于域名变体

```bash
# 使用域名变体
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_rsa

Host github-work.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_rsa-work
```

## 故障排除

### 问题1：SSH连接失败

```bash
# 检查SSH配置
ssh -Tv git@github-personal

# 检查权限
chmod 600 ~/.ssh/config
chmod 600 ~/.ssh/id_rsa-*
chmod 644 ~/.ssh/*.pub
```

### 问题2：Git仍然使用错误的密钥

确保在SSH配置中添加 `IdentitiesOnly yes`：

```bash
Host github-work
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_rsa-work
  IdentitiesOnly yes  # 重要：只使用指定的密钥
```

### 问题3：HTTPS代理问题

如果使用HTTPS over SSH（端口443）：

```bash
Host github.com
  HostName ssh.github.com
  Port 443
  User git
  IdentityFile ~/.ssh/id_rsa-yxy
```

## 最佳实践

1. **命名规范**：使用描述性的密钥文件名（如 `id_rsa-work`, `id_rsa-personal`）
2. **安全性**：为每个密钥设置强密码，并使用SSH agent管理
3. **权限控制**：确保私钥文件权限为600，公钥为644
4. **测试验证**：配置完成后立即测试SSH连接
5. **文档记录**：记录每个项目使用的SSH配置

## 快速参考

```bash
# 查看当前SSH配置
cat ~/.ssh/config

# 测试SSH连接
ssh -T git@github-hostname

# 查看Git remote
git remote -v

# 更新Git remote
git remote set-url origin git@hostname:user/repo.git
```