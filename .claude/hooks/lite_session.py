"""SessionStart hook: AI-DLC Lite 진행 상황을 대화 맥락에 주입.

주입 내용: state.md 요약 (현재 · 다음 단계, 진행 수) + audit.md 마지막 항목
state.md 가 없으면 아무것도 출력하지 않음, 항상 exit 0
"""

import json
import os
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True

STEP = re.compile(r"^- \[([ xX])\]", re.M)  # 들여쓰기 없는 항목 = 단계
SUB = re.compile(r"^\s+- \[([ xX])\]", re.M)  # 들여쓴 항목 = 스토리


def read_input() -> dict:
    raw = sys.stdin.buffer.read().decode("utf-8", errors="replace")
    try:
        return json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        return {}


def field(text: str, name: str) -> str:
    m = re.search(rf"\*\*{re.escape(name)}\*\*:\s*(.+)", text)
    return m.group(1).strip() if m else "확인 필요"


def count(pattern: re.Pattern, text: str) -> tuple:
    marks = pattern.findall(text)
    return sum(1 for x in marks if x.lower() == "x"), len(marks)


def last_audit_heading(docs: Path) -> str:
    audit = docs / "audit.md"
    if not audit.is_file():
        return ""
    heads = [ln[3:].strip() for ln in audit.read_text(encoding="utf-8", errors="replace").splitlines()
             if ln.startswith("## ") and "hook 자동 기록" not in ln]
    return heads[-1] if heads else ""


def main() -> None:
    data = read_input()
    docs = Path(os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or ".") / "aidlc-docs"
    state = docs / "state.md"
    if not state.is_file():
        return
    text = state.read_text(encoding="utf-8", errors="replace")
    done, total = count(STEP, text)
    s_done, s_total = count(SUB, text)
    lines = [
        f"[aidlc-lite hook] AI-DLC Lite 진행 중 (aidlc-docs/state.md, source={data.get('source') or 'startup'})",
        f"- 현재: {field(text, 'Current Step')} / 다음: {field(text, 'Next Step')}",
        f"- 상태: {field(text, 'Status')}",
        f"- 진행: 단계 {done}/{total}" + (f", 스토리 {s_done}/{s_total}" if s_total else ""),
    ]
    last = last_audit_heading(docs)
    if last:
        lines.append(f"- audit.md 마지막 항목: {last}")
    lines.append(
        "- 이어서 진행: state.md · audit.md 를 읽고 .claude/skills/lite/rules.md 규칙대로 재개 "
        "(승인 대기 중이면 승인 전 다음 단계 금지). 사용자는 `/lite` 로 상태 확인"
    )
    sys.stdout.buffer.write(("\n".join(lines) + "\n").encode("utf-8"))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        sys.stderr.write(f"lite_session hook 오류: {e}\n")
    sys.exit(0)
