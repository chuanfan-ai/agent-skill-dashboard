window.SKILL_DATA = {
  "generatedAt": "2026-06-28 00:00:00",
  "summary": {
    "totalFiles": 3,
    "activeFiles": 3,
    "candidateFiles": 0,
    "uniqueNames": 3,
    "duplicateNames": 0,
    "managedDuplicateNames": 0,
    "platformCounts": {
      "Codex 本地": 1,
      "Claude Code": 1,
      "Cola 内置": 1
    },
    "sourceCounts": {
      "Codex 本地": 1,
      "个人共享": 1,
      "Cola 内置": 1
    },
    "statusCounts": {
      "可用": 3
    },
    "actionableDuplicateNames": []
  },
  "skills": [
    {
      "id": "example-codex-skill",
      "name": "openai-docs",
      "alias": "OpenAI 文档查询",
      "purposeZh": "查询 OpenAI 官方文档、模型信息和 API 用法。",
      "description": "Use official OpenAI documentation when answering OpenAI product questions.",
      "category": "研究分析",
      "platforms": ["Codex 本地"],
      "sourceType": "Codex 本地",
      "status": "可用",
      "realPath": "~/example/.codex/skills/openai-docs/SKILL.md",
      "entryPaths": ["~/example/.codex/skills/openai-docs/SKILL.md"],
      "isSymlinked": false,
      "risk": "低风险：主要是本地说明与流程触发",
      "updatedAt": "2026-06-28 00:00",
      "notes": "",
      "duplicates": [],
      "duplicateCount": 1
    },
    {
      "id": "example-shared-skill",
      "name": "article-writer",
      "alias": "文章 写作",
      "purposeZh": "用于文章 写作相关任务。原始说明见详情。",
      "description": "Write long-form articles from briefs and references.",
      "category": "内容写作",
      "platforms": ["Claude Code"],
      "sourceType": "个人共享",
      "status": "可用",
      "realPath": "~/example/.agents/skills/article-writer/SKILL.md",
      "entryPaths": ["~/example/.claude/skills/article-writer/SKILL.md"],
      "isSymlinked": true,
      "risk": "低风险：主要是本地说明与流程触发",
      "updatedAt": "2026-06-28 00:00",
      "notes": "",
      "duplicates": [],
      "duplicateCount": 1
    },
    {
      "id": "example-cola-skill",
      "name": "pdf",
      "alias": "PDF 处理",
      "purposeZh": "读取、生成、拆分、合并、检查和渲染 PDF 文件。",
      "description": "Read, write, merge, split, and inspect PDF files.",
      "category": "文档文件",
      "platforms": ["Cola 内置"],
      "sourceType": "Cola 内置",
      "status": "可用",
      "realPath": "~/example/.cola/resources/skills/pdf/SKILL.md",
      "entryPaths": ["~/example/.cola/resources/skills/pdf/SKILL.md"],
      "isSymlinked": false,
      "risk": "按平台权限与登录状态执行",
      "updatedAt": "2026-06-28 00:00",
      "notes": "",
      "duplicates": [],
      "duplicateCount": 1
    }
  ],
  "cliSummary": {
    "totalCommands": 4,
    "availableCommands": 3,
    "missingCommands": 1,
    "sharedLikeCommands": 2,
    "statusCounts": {
      "可用": 3,
      "未找到": 1
    },
    "sourceCounts": {
      "用户全局": 1,
      "系统内置": 1,
      "Codex 运行时": 1,
      "未找到": 1
    },
    "categoryCounts": {
      "智能体": 2,
      "开发协作": 1,
      "包管理": 1
    }
  },
  "clis": [
    {
      "id": "claude",
      "command": "claude",
      "alias": "Claude Code CLI",
      "purposeZh": "启动或调用 Claude Code 命令行能力。",
      "category": "智能体",
      "status": "可用",
      "sourceType": "用户全局",
      "sharedScope": "通常可被多个智能体共享，前提是启动环境包含该 PATH。",
      "primaryPath": "~/.local/bin/claude",
      "allPaths": ["~/.local/bin/claude"],
      "version": "2.1.165 (Claude Code)",
      "risk": "平时不占内存；只有运行命令时才会占用进程资源。",
      "notes": ""
    },
    {
      "id": "git",
      "command": "git",
      "alias": "Git",
      "purposeZh": "管理本地和远端代码仓库。",
      "category": "开发协作",
      "status": "可用",
      "sourceType": "系统内置",
      "sharedScope": "通常可被多个智能体共享，前提是启动环境包含该 PATH。",
      "primaryPath": "/usr/bin/git",
      "allPaths": ["/usr/bin/git"],
      "version": "git version 2.x",
      "risk": "平时不占内存；只有运行命令时才会占用进程资源。",
      "notes": ""
    },
    {
      "id": "pnpm",
      "command": "pnpm",
      "alias": "pnpm",
      "purposeZh": "安装、运行和管理 Node.js 包。",
      "category": "包管理",
      "status": "可用",
      "sourceType": "Codex 运行时",
      "sharedScope": "主要由 Codex 当前运行时提供，其他智能体不一定能看到。",
      "primaryPath": "~/.cache/codex-runtimes/example/bin/pnpm",
      "allPaths": ["~/.cache/codex-runtimes/example/bin/pnpm"],
      "version": "11.x",
      "risk": "安装包时可能访问网络和修改项目依赖；平时不常驻内存。",
      "notes": ""
    },
    {
      "id": "coze",
      "command": "coze",
      "alias": "Coze CLI",
      "purposeZh": "调用 Coze 相关项目、生成、会话或文件能力。",
      "category": "智能体",
      "status": "未找到",
      "sourceType": "未找到",
      "sharedScope": "取决于当前 PATH 配置。",
      "primaryPath": "",
      "allPaths": [],
      "version": "",
      "risk": "可能访问 Coze 账号、云端项目或生成服务。",
      "notes": ""
    }
  ]
};
