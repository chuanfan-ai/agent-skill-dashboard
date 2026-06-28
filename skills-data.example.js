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
  ]
};
