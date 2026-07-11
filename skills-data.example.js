window.SKILL_DATA = {
  "generatedAt": "2026-07-11 00:00:00",
  "summary": {
    "totalFiles": 1,
    "activeFiles": 1,
    "candidateFiles": 0,
    "uniqueNames": 1,
    "duplicateNames": 0,
    "managedDuplicateNames": 0,
    "platformCounts": {
      "Codex 本地": 1
    },
    "sourceCounts": {
      "Codex 本地": 1
    },
    "statusCounts": {
      "可用": 1
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
      "platforms": [
        "Codex 本地"
      ],
      "sourceType": "Codex 本地",
      "status": "可用",
      "realPath": "~/example/.codex/skills/openai-docs/SKILL.md",
      "entryPaths": [
        "~/example/.codex/skills/openai-docs/SKILL.md"
      ],
      "isSymlinked": false,
      "risk": "低风险：主要是本地说明与流程触发",
      "updatedAt": "2026-07-11 00:00",
      "notes": "",
      "duplicates": [],
      "duplicateCount": 1
    }
  ],
  "cliSummary": {
    "totalCommands": 1,
    "availableCommands": 1,
    "missingCommands": 0,
    "sharedLikeCommands": 1,
    "statusCounts": {
      "可用": 1
    },
    "sourceCounts": {
      "系统内置": 1
    },
    "categoryCounts": {
      "开发协作": 1
    }
  },
  "clis": [
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
      "allPaths": [
        "/usr/bin/git"
      ],
      "version": "git version 2.x",
      "risk": "平时不占内存；只有运行命令时才会占用进程资源。",
      "notes": ""
    }
  ],
  "toolSummary": {
    "totalTools": 1,
    "availableTools": 1,
    "missingTools": 0,
    "modelOrEnvTools": 1,
    "statusCounts": {
      "可用": 1
    },
    "sourceCounts": {
      "本机配置": 1
    },
    "categoryCounts": {
      "OCR/视觉": 1
    }
  },
  "localTools": [
    {
      "id": "paddleocr-local",
      "name": "PaddleOCR",
      "alias": "本地 OCR 识别",
      "type": "Python 工具 + 模型",
      "category": "OCR/视觉",
      "purposeZh": "识别图片、PDF 截图、扫描件和票据中的文字。",
      "status": "可用",
      "sourceType": "本机配置",
      "sharedScope": "可被多个智能体共享，前提是智能体知道虚拟环境 Python 路径和模型目录。",
      "paths": [
        {
          "label": "模型目录",
          "path": "~/.paddlex/official_models",
          "exists": true,
          "sizeText": "177.0M"
        }
      ],
      "commands": [],
      "packages": [
        {
          "name": "paddleocr",
          "version": "3.7.0"
        }
      ],
      "version": "paddleocr 3.7.0",
      "sizeText": "模型约 177M",
      "primaryPath": "~/.paddlex/official_models",
      "risk": "模型文件只占磁盘；运行 OCR 时会占用 CPU/GPU、内存和磁盘读取。",
      "callExamples": [
        "python -m paddleocr --help"
      ],
      "notes": "",
      "updatedAt": "2026-07-11 00:00"
    }
  ]
};
