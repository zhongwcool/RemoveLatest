# RemoveLatest - 删除最新版本文件工具

一个用于自动识别并删除每个渠道子目录中最新版本文件的 Python 工具。

## 功能特性

- 🔍 **自动识别最新版本**：根据文件名中的版本号自动识别每个渠道子目录中的最新版本文件
- 📁 **多渠道支持**：自动遍历工作目录下的所有渠道子目录
- 🎯 **版本号解析**：支持文件名格式如 `Neptune_2025.1.1.exe` 或 `Mars_2025.1.1.exe`
- 💬 **交互式确认**：逐个显示最新版本文件，等待用户确认是否删除
- ⌨️ **快捷键操作**：回车键删除，ESC键跳过
- 📊 **详细信息显示**：显示渠道、文件名、版本号、文件大小和完整路径

## 使用方法

### 1. 环境要求

- Python 3.6 或更高版本
- Windows 操作系统（使用 `msvcrt` 库进行按键检测）
- 无需额外依赖包（使用 Python 标准库）

### 2. 配置设置

编辑 `removelatest.txt` 配置文件，设置工作目录：

```txt
# 使用英文键名格式
source=D:\work\RiderProjects\butter-knife-win\Publish
```

#### 配置说明

- **source**: 工作目录路径，程序会在此目录下查找所有子目录（渠道）
- 每个子目录代表一个渠道（如 `wxg`、`zhk`、`test` 等）
- 程序会在每个渠道目录中查找版本号最新的 `.exe` 文件

### 3. 文件命名格式

程序支持以下文件名格式：

- `Neptune_2025.1.1.exe` - 版本号格式：`_YYYY.M.M.exe`
- `Mars_2025.0.8.exe` - 版本号格式：`_YYYY.M.M.exe`
- `ButterKnife.exe` - 无版本号的文件会被忽略

版本号格式说明：
- `YYYY`: 年份（4位数字）
- `M`: 主版本号
- `M`: 次版本号

程序会比较版本号，找出每个渠道中版本号最大的文件。

### 4. 运行程序

直接运行 `main.py`：

```shell
python main.py
```

### 5. 交互操作

程序运行后会：

1. 显示工作目录
2. 扫描所有渠道子目录
3. 为每个渠道找出版本号最新的文件
4. 逐个显示文件信息：
   - 渠道名称
   - 文件名
   - 版本号
   - 文件大小（MB）
   - 完整路径
5. 等待用户操作：
   - **回车键**：删除该文件
   - **ESC键**：跳过该文件，不删除

### 6. 示例输出

```
工作目录: D:\work\RiderProjects\butter-knife-win\Publish

找到以下最新版本文件：

渠道: wxg
文件: Mars_2025.1.1.exe
版本: 2025.1.1
大小: 39.96 MB
路径: D:\work\RiderProjects\butter-knife-win\Publish\wxg\Mars_2025.1.1.exe

是否删除？[回车=删除, ESC=跳过]
```

## 打包

使用 **pyinstaller** 打包成 exe 文件，打开 **PyCharm** 的 `Terminal` 输入：

```shell
pyinstaller --onefile --name RemoveLatest --icon app.ico main.py
```

如果需要在 exe 文件名中添加版本号、版权、公司等版本信息，可以使用 `--version-file` 参数，例如：

```shell
pyinstaller --onefile --version-file version.txt --name RemoveLatest --icon app.ico main.py
```

## 注意事项

- ⚠️ **删除操作不可恢复**：删除的文件无法恢复，请谨慎操作
- 📝 **配置文件格式**：确保 `removelatest.txt` 中的 `source=` 配置正确
- 🔍 **版本号识别**：只有符合 `_YYYY.M.M.exe` 格式的文件才会被识别为版本文件
- 📁 **目录结构**：程序会自动识别工作目录下的所有子目录作为渠道

## 错误处理

- 如果工作目录不存在，程序会显示错误信息并退出
- 如果某个渠道目录中没有版本文件，该渠道会被跳过
- 如果删除文件时发生错误（如文件被占用），程序会显示错误信息但继续处理其他文件
