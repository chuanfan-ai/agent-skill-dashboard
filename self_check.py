#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import refresh_skills


def main() -> None:
    assert refresh_skills.format_bytes(1024) == "1.0K"
    data = refresh_skills.collect()
    assert isinstance(data.get("skills"), list)
    assert isinstance(data.get("clis"), list)
    assert isinstance(data.get("localTools"), list)
    assert "toolSummary" in data
    assert data["toolSummary"]["totalTools"] == len(data["localTools"])
    sample = {
        "name": "demo",
        "alias": "演示工具",
        "paths": [{"label": "项目", "path": str(Path(__file__).resolve())}],
    }
    item = refresh_skills.build_local_tool(sample)
    assert item["status"] == "可用"
    assert item["paths"][0]["exists"] is True
    json.dumps(data, ensure_ascii=False)
    print("self_check passed")


if __name__ == "__main__":
    main()
