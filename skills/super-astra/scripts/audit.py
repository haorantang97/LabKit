#!/usr/bin/env python3
"""Read-only candidate scan of explicitly supplied Markdown files/directories."""
import argparse
from collections import defaultdict
import hashlib
import json
import os
from pathlib import Path
import re
import sys

SKIP = {".git", "node_modules", ".venv", "__pycache__"}
RULES = {
    "unconditional-delegation": r"always.{0,30}(?:delegat|sub.?agent)|at any point you can parallelize|(?:必须|始终|一律).{0,15}(?:并行|子.?agent|子智能体)",
    "approval-every-step": r"(?:ask|approval|confirm).{0,30}(?:every|each) step|(?:每一步|所有操作).{0,15}(?:确认|批准)",
    "unbounded-verification": r"(?:always|after every).{0,35}(?:full test|all tests|entire test)|(?:每次|任何改动).{0,15}(?:全量测试|完整测试)",
    "hierarchy-claim": r"(?:override|ignore).{0,30}(?:system|developer|user) instructions|(?:覆盖|忽略).{0,15}(?:系统|开发者|用户)指令",
    "workflow-chain": r"(?:always|must).{0,25}(?:invoke|run|load).{0,25}(?:skill|review)|(?:必须|自动).{0,15}(?:调用|启动).{0,15}(?:技能|skill|评审)",
}


def scan(roots, max_files=1000):
    paths, gaps = [], []
    for raw in roots:
        path = Path(raw).expanduser().absolute()
        if not path.exists():
            gaps.append({"path": str(path), "reason": "missing"})
        elif path.is_file():
            paths.append(path)
        elif path.is_dir():
            def onerror(error):
                gaps.append({"path": str(error.filename), "reason": "unreadable directory"})
            for directory, dirs, files in os.walk(path, followlinks=False, onerror=onerror):
                for name in dirs:
                    child = Path(directory) / name
                    if child.is_symlink():
                        gaps.append({"path": str(child), "reason": "symlink directory not traversed; pass explicitly to scan"})
                dirs[:] = sorted(d for d in dirs if d not in SKIP and not (Path(directory) / d).is_symlink())
                paths.extend(Path(directory) / f for f in sorted(files) if f.endswith(".md"))
    paths = sorted(set(paths))
    if len(paths) > max_files:
        gaps.append({"reason": "file limit", "omitted": len(paths) - max_files})
        paths = paths[:max_files]
    files, findings = [], []
    names, hashes, resolved = defaultdict(list), defaultdict(list), defaultdict(list)
    for path in paths:
        try:
            if path.stat().st_size > 1024 * 1024:
                gaps.append({"path": str(path), "reason": "larger than 1 MiB"})
                continue
            data = path.read_bytes()
            text = data.decode("utf-8")
            digest = hashlib.sha256(data).hexdigest()
            files.append({"path": str(path), "resolved": str(path.resolve()), "sha256": digest})
            hashes[digest].append(str(path))
            resolved[str(path.resolve())].append(str(path))
            if path.name == "SKILL.md" and text.startswith("---\n"):
                front = text.split("\n---", 1)[0]
                match = re.search(r"(?m)^name:\s*['\"]?([^'\"\n]+)", front)
                if match:
                    names[match[1].strip()].append(str(path))
            for number, line in enumerate(text.splitlines(), 1):
                for rule, pattern in RULES.items():
                    if re.search(pattern, line, re.I):
                        findings.append({"path": str(path), "line": number, "rule": rule,
                                         "excerpt": line[:300], "status": "candidate-needs-context"})
        except (OSError, UnicodeError) as error:
            gaps.append({"path": str(path), "reason": type(error).__name__})
    return {
        "read_only": True,
        "coverage": "partial" if gaps else "requested-markdown-only",
        "limits": "Does not establish which instructions are active; patterns are candidates, including quoted examples. No findings is not proof of no conflicts.",
        "files": files, "gaps": gaps, "findings": findings,
        "duplicate_skill_names": {k: v for k, v in names.items() if len(v) > 1},
        "identical_content": [v for v in hashes.values() if len(v) > 1],
        "same_file_aliases": [v for v in resolved.values() if len(v) > 1],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="explicit files or directories; no default home scan")
    args = parser.parse_args()
    print(json.dumps(scan(args.paths), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
