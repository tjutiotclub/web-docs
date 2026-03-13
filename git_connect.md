# Git 通过 SSH 绑定 GitHub

本文档记录使用 SSH 将本地 Git 与 GitHub 账号绑定的完整流程。  
同样适用于 Gitee、GitCode 等其他 Git 托管平台。

---

第一步：确认 Git 已正确安装
----------------

在 PowerShell 中输入：

```powershell
git
```

如果能够看到 Git 的帮助信息或命令列表，说明 Git 已被系统识别，安装正常。

也可以使用指令

```powershell
git --version
```

指令返回例如

```powershell
git version 2.51.0.windows.1
```

---

## 第二步：生成 SSH 密钥

在终端输入：

```powershell
ssh-keygen -t ed25519 -C "你的邮箱"
```

注意：

* 邮箱填写为 **注册对应 Git 平台时使用的邮箱**

* 一路回车即可

* 默认会生成在：

```makefile
C:\Users\你的用户名\.ssh\
```

生成完成后通常会看到：

```makefile
id_ed25519       （私钥，自己保存，绝对不要上传）
id_ed25519.pub   （公钥，需要提交到 Git 平台）
```

---

## 第三步：将公钥添加到 GitHub 打开 GitHub

1. 进入 Settings

2. 找到 SSH and GPG keys

3. 选择 New SSH key

---

### 复制公钥内容

用记事本或 VS Code 打开：

```makefile
`C:\Users\你的用户名\.ssh\id_ed25519.pub`
```

**完整复制全部内容**，粘贴到 Key 中。

Title 可以随便写，例如：

```
`My Laptop`
```

点击 **Add SSH key**。

* * *

第四步：测试连接
--------

回到终端，输入：

```powershell
ssh -T git@github.com
```

第一次连接时会提示：

```powershell
Are you sure you want to continue connecting (yes/no)?
```

输入：

```powershell
yes
```

如果看到类似：

```powershell
Hi 用户名! You've successfully authenticated, but GitHub does not provide shell access.
```

说明 SSH 绑定成功。

* * *

常见问题
----

### 1. 可以多个平台共用一个密钥吗？

可以。

同一把 SSH 公钥可以同时添加到 GitHub、Gitee、GitCode 等多个平台。  
这不会产生冲突。

如果未来需要区分身份（比如公司 / 个人），再为不同用途单独生成密钥即可。 

### 2. 为什么不用 HTTPS？

HTTPS 方式每次推送通常需要登录或使用 Token。  
SSH 在配置完成后可以长期免密，更适合开发环境。
