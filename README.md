# Agent Skill Dashboard

一个本地 skill 管理台，用来盘点 Codex、Claude Code、Cola、OpenClaw、Trae 等智能体工具里的 `SKILL.md`。

它解决的问题：

- skill 分散在多个工具、插件缓存和软链接目录里，很难知道到底装了什么。
- 同名 skill 可能是真重复，也可能只是平台缓存或跨平台同名。
- 很多 skill 的英文说明不适合日常管理，需要中文别名和中文用途。
- 只复制路径不方便定位，需要能直接打开真实文件夹。

## 功能

- 搜索、筛选、卡片/表格视图。
- 自动识别真实位置、平台入口、软链接。
- 标记可用、候选未安装、重复、平台缓存、跨平台同名。
- 中文别名和中文用途展示。
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

启动后会打开浏览器。页面右上角的“刷新数据”会重新扫描本机 skill，详情里的“打开文件夹”会打开真实位置所在目录。

## 配置扫描路径

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

示例：

```json
[
  {
    "platform": "My Custom Agent",
    "type": "active",
    "maxDepth": 8,
    "paths": [
      "~/my-agent/skills",
      "%USERPROFILE%\\.my-agent\\skills"
    ]
  }
]
```

## 中文别名和用途

编辑：

```text
config/aliases.zh.json
```

格式：

```json
{
  "my-skill-name": {
    "alias": "我的技能",
    "purpose": "用中文说明这个 skill 什么时候用。"
  }
}
```

没有配置的 skill 会自动生成中文兜底别名，并用中文提示“原始说明见详情”。

## 数据文件

`skills-data.js` 是本机扫描结果，默认不提交到 GitHub。

仓库里只保留：

- `skills-data.example.js`：示例数据
- `config/*.json`：默认配置和中文别名字典

## 安全边界

- 扫描过程只读取 `SKILL.md`，不会读取 `.env`、token 或密钥文件。
- 页面里的“打开文件夹”只打开目录，不会删除或移动文件。
- 清理重复 skill 前建议先归档，不要直接删除插件缓存或平台内置目录。

## 开发

刷新数据：

```bash
python3 refresh_skills.py
```

启动本地服务：

```bash
python3 server.py
```
