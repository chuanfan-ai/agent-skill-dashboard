# Agent Skill Dashboard

一个本地智能体能力管理台，用来盘点 Codex、Claude Code、Cola、OpenClaw、Trae 等智能体工具里的 `SKILL.md`，当前环境可调用的 CLI，以及本机安装的 Python 工具、模型目录、虚拟环境和本地能力。

它解决的问题：

- skill 分散在多个工具、插件缓存和软链接目录里，很难知道到底装了什么。
- CLI 和 skill 的共享机制不同，需要看命令是否在 PATH 里、来自用户全局目录还是某个智能体运行时。
- PaddleOCR、Whisper、Ollama、Hugging Face 缓存、Python venv 这类本地能力既不是 skill，也不只是 CLI，需要单独登记。
- 很多说明是英文，不适合日常管理，需要中文别名和中文用途。
- 只复制路径不方便定位，需要能直接打开真实文件夹。

## 功能

- Skill / CLI / 本地工具 三页面切换。
- 搜索、筛选、卡片/表格视图。
- 自动识别 skill 真实位置、平台入口、软链接。
- CLI 页面展示命令路径、版本、来源类型、共享判断和运行风险。
- 本地工具页面展示模型目录、Python 虚拟环境、Python 包版本、占用空间、调用示例和共享判断。
- 页面内一键刷新数据。
- 页面内直接打开真实位置所在文件夹。
- macOS、Windows、Linux 都可用。

## 快速开始

需要 Python 3.9+。

macOS：

```bash
chmod +x start.command
./start.command
```

Windows：

双击 `start.bat`。

Linux：

```bash
chmod +x start.sh
./start.sh
```

启动后会打开浏览器。页面右上角的“刷新数据”会重新扫描本机 skill、CLI 和本地工具。

## 本地工具和模型

公开仓库不会提交你的真实机器清单。你自己的登记文件是：

```text
config/local-tools.json
```

第一次使用可以复制示例：

```bash
cp config/local-tools.example.json config/local-tools.json
```

示例：

```json
[
  {
    "id": "paddleocr-local",
    "name": "PaddleOCR",
    "alias": "本地 OCR 识别",
    "type": "Python 工具 + 模型",
    "category": "OCR/视觉",
    "purpose": "识别图片、PDF 截图、扫描件和票据中的文字。",
    "paths": [
      {"label": "模型目录", "path": "~/.paddlex/official_models"},
      {"label": "虚拟环境", "path": "~/my-project/.venv"}
    ],
    "packages": ["paddleocr", "paddlepaddle"],
    "versions": {
      "paddleocr": "3.7.0",
      "paddlepaddle": "3.3.1"
    },
    "callExamples": ["python -m paddleocr --help"]
  }
]
```

管理台也会自动发现这些常见位置：

- `~/.paddlex/official_models`
- `~/.ollama/models`
- `~/.cache/huggingface`
- `~/.cache/whisper`
- `~/.local/pipx/venvs`
- `~/.local/share/uv/tools`
- 常见 Python 虚拟环境目录里的 `pyvenv.cfg`

如果要扩大虚拟环境扫描范围，可以设置环境变量：

```bash
AGENT_TOOL_SCAN_ROOTS="/path/a:/path/b" python3 refresh_skills.py
```

Windows 用分号分隔路径。

## 配置 Skill 扫描路径

默认扫描这些常见目录：

- `~/.codex/skills`
- `~/.codex/plugins/cache`
- `~/.agents/skills`
- `~/.claude/skills`
- `~/.cola/skills`
- `~/.cola/resources/skills`
- `~/.trae-cn/skills`
- `~/.openclaw/skills`
- `~/.workbuddy/skills`
- `~/.codex/vendor_imports/skills`

自定义路径：

```bash
cp config/local-roots.example.json config/local-roots.json
```

然后编辑 `config/local-roots.json`。

## 中文别名和用途

编辑：

```text
config/aliases.zh.json
```

没有配置的 skill 会自动生成中文兜底别名，并用中文提示“原始说明见详情”。

## CLI 目录

默认 CLI 目录在：

```text
config/cli-catalog.zh.json
```

自定义 CLI：

```bash
cp config/local-cli-catalog.example.json config/local-cli-catalog.json
```

CLI 页面里的“共享判断”是根据路径推断的：

- `~/.local/bin`、系统目录、Homebrew 等：通常可被多个智能体共享，前提是启动时带着这些 PATH。
- Codex runtime / 插件缓存：通常不算所有智能体共享。
- 应用自带目录：取决于应用是否安装，以及 PATH 是否暴露。

## 数据文件

`skills-data.js` 是本机扫描结果，包含 skill、CLI、本地工具三类数据，默认不提交到 GitHub。

仓库里只保留：

- `skills-data.example.js`：示例数据
- `config/*.example.json`：示例配置
- `config/cli-catalog.zh.json`、`config/default-roots.json`、`config/aliases.zh.json`：可公开的默认配置

## 安全边界

- 扫描过程只读取 `SKILL.md`、配置文件、常见工具目录和 `pyvenv.cfg`。
- 不读取 `.env`、token、密钥文件。
- CLI 扫描只检查配置中的命令是否在 PATH 中，并尝试读取版本号。
- 本地工具扫描会统计已登记目录的大小，但不会删除、移动或上传文件。
- 页面里的“打开文件夹”只打开目录。

## 开发和验证

刷新数据：

```bash
python3 refresh_skills.py
```

运行最小自检：

```bash
python3 self_check.py
```

启动本地服务：

```bash
python3 server.py
```
