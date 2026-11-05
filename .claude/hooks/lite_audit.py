"""UserPromptSubmit hook: 사용자 입력 원문을 aidlc-docs/audit.md 에 자동 기록 (AI-DLC Lite).

기록 조건: aidlc-docs/state.md 가 있거나, 입력에 /lite 스킬 호출이 있을 때
실패해도 입력을 막지 않음 (항상 exit 0), 표준 라이브러리만 사용
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True

TRIGGER = re.compile(r"/lite\b|ai-?dlc", re.I)
HEADER = "# AI-DLC Lite Audit Log\n\n"
FIELD = re.compile(r"\*\*Current Step\*\*:\s*(.+)")


def read_input() -> dict:
    raw = sys.stdin.buffer.read().decode("utf-8", errors="replace")
    try:
        return json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        return {}


def project_dir(data: dict) -> Path:
    return Path(os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or ".")


def current_step(docs: Path) -> str:
    state = docs / "state.md"
    if not state.is_file():
        return "시작 전"
    m = FIELD.search(state.read_text(encoding="utf-8", errors="replace"))
    return m.group(1).strip() if m else "확인 필요"


def main() -> None:
    data = read_input()
    prompt = data.get("prompt") or ""
    # Claude Code 가 만든 turn (작업 알림 등) 은 사람 입력이 아님
    if not prompt.strip() or prompt.lstrip().startswith("<"):
        return
    docs = project_dir(data) / "aidlc-docs"
    if not (docs / "state.md").is_file() and not TRIGGER.search(prompt):
        return

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    entry = (
        "## 사용자 입력 (hook 자동 기록)\n"
        f"**Timestamp**: {ts}\n"
        f'**User Input**: "{prompt}"\n'
        f"**Context**: {current_step(docs)} · UserPromptSubmit hook\n\n---\n\n"
    )
    docs.mkdir(exist_ok=True)
    audit = docs / "audit.md"
    with open(audit, "a", encoding="utf-8", newline="\n") as f:
        if audit.stat().st_size == 0:
            f.write(HEADER)
        f.write(entry)

    msg = (
        f"[aidlc-lite hook] 사용자 입력이 aidlc-docs/audit.md 에 기록됨 (Timestamp: {ts}). "
        f"audit 항목을 쓸 때 `**User Input**: (hook 기록 {ts})` 로 대신하고, "
        f"Timestamp 는 추측하지 말고 {ts} 사용.\n"
    )
    sys.stdout.buffer.write(msg.encode("utf-8"))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # hook 오류로 입력이 막히지 않게
        sys.stderr.write(f"lite_audit hook 오류: {e}\n")
    sys.exit(0)
