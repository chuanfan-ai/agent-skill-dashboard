#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
CONFIG_DIR = BASE_DIR / "config"
DEFAULT_ROOTS_FILE = CONFIG_DIR / "default-roots.json"
LOCAL_ROOTS_FILE = CONFIG_DIR / "local-roots.json"
ALIASES_FILE = CONFIG_DIR / "aliases.zh.json"
CLI_CATALOG_FILE = CONFIG_DIR / "cli-catalog.zh.json"
LOCAL_CLI_CATALOG_FILE = CONFIG_DIR / "local-cli-catalog.json"
OUTPUT_FILE = BASE_DIR / "skills-data.js"

PLATFORM_ORDER = [
    "Codex 本地",
    "Codex 插件缓存",
    "共享个人库",
    "Claude Code",
    "Cola 个人链接",
    "Cola 内置",
    "Trae CN",
    "OpenClaw",
    "WorkBuddy",
    "MiniMax",
    "候选库",
]

CATEGORIES = [
    ("内容写作", ["writer", "wechat", "title", "humanizer", "article", "khazix", "公众号"]),
    ("研究分析", ["analysis", "research", "aihot", "notion", "memory", "linear"]),
    ("演示文稿", ["ppt", "presentation", "slides", "hyperframes", "remotion"]),
    ("文档文件", ["doc", "pdf", "sheet", "xlsx", "spreadsheet", "template"]),
    ("开发部署", ["github", "gh-", "deploy", "vercel", "cloudflare", "netlify", "plugin", "cli"]),
    ("浏览器/桌面", ["browser", "chrome", "computer", "screenshot", "figma", "playwright"]),
    ("Google/Apple", ["gws-", "gmail", "calendar", "drive", "apple", "reminders", "notes"]),
    ("媒体生成", ["image", "video", "heygen", "speech", "transcribe", "avatar", "pet"]),
]

WORD_ALIAS = {
    "ai": "AI",
    "agent": "智能体",
    "app": "应用",
    "apps": "应用",
    "article": "文章",
    "audio": "音频",
    "avatar": "头像",
    "browser": "浏览器",
    "calendar": "日历",
    "chrome": "Chrome",
    "cli": "命令行",
    "code": "代码",
    "computer": "电脑",
    "creator": "创建器",
    "deploy": "部署",
    "doc": "文档",
    "docs": "文档",
    "drive": "云盘",
    "email": "邮件",
    "figma": "Figma",
    "fix": "修复",
    "gmail": "Gmail",
    "github": "GitHub",
    "image": "图片",
    "manager": "管理器",
    "memory": "记忆",
    "notion": "Notion",
    "pdf": "PDF",
    "plugin": "插件",
    "ppt": "PPT",
    "pptx": "PPT",
    "remotion": "Remotion",
    "research": "研究",
    "security": "安全",
    "sheet": "表格",
    "sheets": "表格",
    "skill": "技能",
    "skills": "技能",
    "speech": "语音",
    "template": "模板",
    "title": "标题",
    "transcribe": "转写",
    "video": "视频",
    "wechat": "微信",
    "website": "网站",
    "writer": "写作",
    "xlsx": "Excel",
}


def read_json(path: Path, fallback):
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def expand_path(raw: str) -> Path:
    expanded = os.path.expandvars(raw)
    expanded = expanded.replace("%USERPROFILE%", str(Path.home()))
    expanded = expanded.replace("%APPDATA%", os.environ.get("APPDATA", ""))
    return Path(expanded).expanduser()


def load_roots() -> list[dict]:
    roots = read_json(DEFAULT_ROOTS_FILE, [])
    local = read_json(LOCAL_ROOTS_FILE, [])
    return roots + local


def load_aliases() -> dict:
    return read_json(ALIASES_FILE, {})


def load_cli_catalog() -> list[dict]:
    catalog = read_json(CLI_CATALOG_FILE, [])
    local = read_json(LOCAL_CLI_CATALOG_FILE, [])
    return catalog + local


def walk_skill_files(root: Path, max_depth: int) -> list[Path]:
    if not root.exists():
        return []
    files = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=True):
        current = Path(dirpath)
        try:
            depth = len(current.relative_to(root).parts)
        except ValueError:
            depth = 0
        if depth > max_depth:
            dirnames[:] = []
            continue
        if "SKILL.md" in filenames:
            files.append(current / "SKILL.md")
    return files


def parse_frontmatter(path: Path) -> tuple[str, str]:
    text = path.read_text(errors="ignore")
    name = path.parent.name
    description = ""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        frontmatter = text[3:end] if end != -1 else ""
        lines = frontmatter.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith("name:"):
                name = line.split(":", 1)[1].strip().strip("\"'") or name
            elif line.startswith("description:"):
                value = line.split(":", 1)[1].strip()
                if value in {"|", ">", "|-", ">-"}:
                    parts = []
                    i += 1
                    while i < len(lines) and (lines[i].startswith(" ") or not lines[i].strip()):
                        parts.append(lines[i].strip())
                        i += 1
                    description = " ".join(part for part in parts if part)
                    continue
                description = value.strip("\"'")
            i += 1
    if not description:
        match = re.search(r"^#\s+(.+)", text, flags=re.MULTILINE)
        description = match.group(1).strip() if match else ""
    return name, re.sub(r"\s+", " ", description).strip()


def infer_category(name: str, description: str) -> str:
    blob = f"{name} {description}".lower()
    for category, needles in CATEGORIES:
        if any(needle in blob for needle in needles):
            return category
    return "其他"


def auto_alias(name: str) -> str:
    pieces = [piece for piece in re.split(r"[-_\s]+", name) if piece]
    translated = [WORD_ALIAS.get(piece.lower(), piece) for piece in pieces[:4]]
    alias = " ".join(translated).strip()
    return alias or name


def has_chinese(text: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", text))


def purpose_zh(name: str, description: str, alias_entry: dict | str) -> str:
    if isinstance(alias_entry, dict) and alias_entry.get("purpose"):
        return alias_entry["purpose"]
    if has_chinese(description):
        return description
    alias = alias_entry.get("alias") if isinstance(alias_entry, dict) else alias_entry
    alias = alias or auto_alias(name)
    return f"用于{alias}相关任务。原始说明见详情。"


def alias_zh(name: str, alias_entry: dict | str) -> str:
    if isinstance(alias_entry, dict):
        return alias_entry.get("alias") or auto_alias(name)
    if isinstance(alias_entry, str) and alias_entry:
        return alias_entry
    return auto_alias(name)


def infer_risk(name: str, description: str, platforms: list[str]) -> str:
    blob = f"{name} {description}".lower()
    risks = []
    if any(word in blob for word in ["gmail", "calendar", "drive", "notion", "github", "vercel", "deploy"]):
        risks.append("可能访问外部账户")
    if any(word in blob for word in ["browser", "chrome", "computer", "figma", "playwright"]):
        risks.append("可能操作浏览器或本机界面")
    if any(word in blob for word in ["create", "edit", "write", "deploy", "publish", "push", "send", "delete"]):
        risks.append("可能修改文件或外部状态")
    if not risks and ("Codex 插件缓存" in platforms or "Cola 内置" in platforms):
        risks.append("按平台权限与登录状态执行")
    return "；".join(risks) if risks else "低风险：主要是本地说明与流程触发"


def cli_source_type(path: str) -> str:
    normalized = path.replace("\\", "/")
    home = str(Path.home()).replace("\\", "/")
    if normalized.startswith(f"{home}/.local/bin/"):
        return "用户全局"
    if "/.cache/codex-runtimes/" in normalized or "/codex-primary-runtime/" in normalized:
        return "Codex 运行时"
    if normalized.startswith("/Applications/") or "/Contents/Resources/" in normalized:
        return "应用自带"
    if normalized.startswith("/usr/bin/") or normalized.startswith("/bin/") or normalized.startswith("/usr/sbin/"):
        return "系统内置"
    if normalized.startswith("/opt/homebrew/bin/") or normalized.startswith("/usr/local/bin/"):
        return "包管理器"
    if "AppData/" in normalized or "/Programs/" in normalized:
        return "用户应用"
    return "PATH 可见"


def cli_shared_scope(source_type: str) -> str:
    if source_type in {"用户全局", "系统内置", "包管理器"}:
        return "通常可被多个智能体共享，前提是启动环境包含该 PATH。"
    if source_type == "Codex 运行时":
        return "主要由 Codex 当前运行时提供，其他智能体不一定能看到。"
    if source_type in {"应用自带", "用户应用"}:
        return "随应用安装，其他智能体能否调用取决于 PATH 和应用是否存在。"
    return "取决于当前 PATH 配置。"


def which_all(command: str) -> list[str]:
    seen = set()
    results = []
    for raw_dir in os.environ.get("PATH", "").split(os.pathsep):
        if not raw_dir:
            continue
        base = Path(raw_dir).expanduser()
        candidates = [base / command]
        if os.name == "nt":
            pathext = os.environ.get("PATHEXT", ".EXE;.BAT;.CMD;.COM").split(";")
            candidates.extend(base / f"{command}{ext.lower()}" for ext in pathext)
            candidates.extend(base / f"{command}{ext.upper()}" for ext in pathext)
        for candidate in candidates:
            try:
                resolved = str(candidate.resolve())
            except OSError:
                resolved = str(candidate)
            if candidate.exists() and os.access(candidate, os.X_OK) and resolved not in seen:
                seen.add(resolved)
                results.append(str(candidate))
    return results


def read_version(path: str, version_args: list[str]) -> str:
    if not version_args:
        return ""
    try:
        result = subprocess.run(
            [path, *version_args],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=4,
            check=False,
        )
    except Exception:
        return ""
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return " / ".join(lines[:2])[:240]


def collect_clis() -> tuple[dict, list[dict]]:
    catalog = load_cli_catalog()
    items = []
    for entry in catalog:
        command = entry["command"]
        paths = which_all(command)
        primary = shutil.which(command) or (paths[0] if paths else "")
        all_paths = paths or ([primary] if primary else [])
        source_type = cli_source_type(primary) if primary else "未找到"
        version = read_version(primary, entry.get("versionArgs", ["--version"])) if primary else ""
        item = {
            "id": re.sub(r"[^a-zA-Z0-9_-]+", "-", command).strip("-"),
            "command": command,
            "alias": entry.get("alias") or auto_alias(command),
            "purposeZh": entry.get("purpose") or f"用于{entry.get('alias') or auto_alias(command)}相关命令行任务。",
            "category": entry.get("category") or "其他",
            "status": "可用" if primary else "未找到",
            "sourceType": source_type,
            "sharedScope": cli_shared_scope(source_type),
            "primaryPath": primary,
            "allPaths": all_paths,
            "version": version,
            "risk": entry.get("risk") or "平时不占内存；只有运行命令时才会占用进程资源。",
            "notes": entry.get("notes", ""),
        }
        items.append(item)
    items.sort(key=lambda item: (item["status"] != "可用", item["sourceType"], item["command"]))
    status_counts = Counter(item["status"] for item in items)
    source_counts = Counter(item["sourceType"] for item in items)
    category_counts = Counter(item["category"] for item in items)
    shared_count = sum(1 for item in items if item["sourceType"] in {"用户全局", "系统内置", "包管理器"})
    summary = {
        "totalCommands": len(items),
        "availableCommands": status_counts.get("可用", 0),
        "missingCommands": status_counts.get("未找到", 0),
        "sharedLikeCommands": shared_count,
        "statusCounts": dict(status_counts),
        "sourceCounts": dict(source_counts),
        "categoryCounts": dict(category_counts),
    }
    return summary, items


def choose_source_type(real_path: str, source_types: list[str]) -> str:
    normalized_path = real_path.replace("\\", "/")
    if "/.codex/skills/.system/" in normalized_path:
        return "Codex 系统"
    if "/.agents/skills/" in normalized_path and "个人共享" in source_types:
        return "个人共享"
    for preferred in ["Codex 系统", "Codex 插件", "Cola 内置", "个人共享", "Codex 本地"]:
        if preferred in source_types:
            return preferred
    return source_types[0]


def collect() -> dict:
    records: dict[str, dict] = {}
    roots = load_roots()
    aliases = load_aliases()

    for root in roots:
        platform = root["platform"]
        root_type = root.get("type", "active")
        source_type = root.get("sourceType") or ("候选未安装" if root_type == "candidate" else platform)
        max_depth = int(root.get("maxDepth", 8))
        for raw_path in root.get("paths", []):
            base = expand_path(raw_path)
            for file_path in walk_skill_files(base, max_depth):
                real_path = str(file_path.resolve())
                record = records.setdefault(
                    real_path,
                    {
                        "realPath": real_path,
                        "entryPaths": set(),
                        "platforms": set(),
                        "candidate": root_type == "candidate",
                        "sourceTypes": set(),
                    },
                )
                record["entryPaths"].add(str(file_path))
                record["platforms"].add(platform)
                record["sourceTypes"].add(source_type)
                record["candidate"] = record["candidate"] or root_type == "candidate"

    items = []
    for real_path, record in records.items():
        name, description = parse_frontmatter(Path(real_path))
        alias_entry = aliases.get(name, {})
        platforms = sorted(
            record["platforms"],
            key=lambda item: PLATFORM_ORDER.index(item) if item in PLATFORM_ORDER else 99,
        )
        entry_paths = sorted(record["entryPaths"])
        source_types = sorted(record["sourceTypes"])
        source_type = "候选未安装" if record["candidate"] else choose_source_type(real_path, source_types)
        stable_id = hashlib.sha1(real_path.encode("utf-8")).hexdigest()[:10]
        item = {
            "id": re.sub(r"[^a-zA-Z0-9_-]+", "-", f"{name}-{stable_id}").strip("-"),
            "name": name,
            "alias": alias_zh(name, alias_entry),
            "purposeZh": purpose_zh(name, description, alias_entry),
            "description": description,
            "category": infer_category(name, description),
            "platforms": platforms,
            "sourceType": source_type,
            "status": "候选未安装" if record["candidate"] else "可用",
            "realPath": real_path,
            "entryPaths": entry_paths,
            "isSymlinked": len(entry_paths) > 1 or any(Path(path).is_symlink() for path in entry_paths),
            "risk": infer_risk(name, description, platforms),
            "updatedAt": datetime.fromtimestamp(Path(real_path).stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
            "notes": "",
        }
        items.append(item)

    active_items = [item for item in items if item["status"] != "候选未安装"]
    name_counts = Counter(item["name"] for item in active_items)
    normalized = defaultdict(list)
    for item in active_items:
        normalized[item["name"]].append(item["realPath"])

    duplicate_status_by_name = {}
    for name, paths in normalized.items():
        if len(paths) <= 1:
            continue
        group = [item for item in active_items if item["name"] == name]
        source_types = {item["sourceType"] for item in group}
        platforms = {platform for item in group for platform in item["platforms"]}
        if len(source_types) == 1 and any("缓存" in value or "plugin" in value.lower() for value in source_types | platforms):
            duplicate_status_by_name[name] = "平台缓存"
        elif len(source_types) > 1 or len(platforms) > 1:
            duplicate_status_by_name[name] = "跨平台同名"
        else:
            duplicate_status_by_name[name] = "重复"

    for item in items:
        if item["status"] == "候选未安装":
            item["duplicates"] = []
            item["duplicateCount"] = 0
            continue
        duplicates = [path for path in normalized[item["name"]] if path != item["realPath"]]
        if duplicates:
            item["status"] = duplicate_status_by_name.get(item["name"], "重复")
            item["duplicates"] = duplicates
        else:
            item["duplicates"] = []
        item["duplicateCount"] = name_counts[item["name"]]

    items.sort(key=lambda item: (item["status"] == "候选未安装", item["sourceType"], item["name"], item["realPath"]))
    platform_counts = {
        platform: sum(1 for item in items if platform in item["platforms"] and item["status"] != "候选未安装")
        for platform in PLATFORM_ORDER
    }
    platform_counts = {key: value for key, value in platform_counts.items() if value}
    source_counts = Counter(item["sourceType"] for item in items)
    status_counts = Counter(item["status"] for item in items)
    actionable_duplicate_names = sorted(
        name for name, status in duplicate_status_by_name.items() if status == "重复"
    )

    cli_summary, clis = collect_clis()
    return {
        "generatedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "summary": {
            "totalFiles": len(items),
            "activeFiles": sum(1 for item in items if item["status"] != "候选未安装"),
            "candidateFiles": sum(1 for item in items if item["status"] == "候选未安装"),
            "uniqueNames": len({item["name"] for item in items if item["status"] != "候选未安装"}),
            "duplicateNames": len(actionable_duplicate_names),
            "managedDuplicateNames": sum(1 for status in duplicate_status_by_name.values() if status != "重复"),
            "platformCounts": platform_counts,
            "sourceCounts": dict(source_counts),
            "statusCounts": dict(status_counts),
            "actionableDuplicateNames": actionable_duplicate_names,
        },
        "skills": items,
        "cliSummary": cli_summary,
        "clis": clis,
    }


def main() -> None:
    data = collect()
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    OUTPUT_FILE.write_text(f"window.SKILL_DATA = {payload};\n", encoding="utf-8")
    print(f"写入 {OUTPUT_FILE}")
    print(json.dumps(data["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
