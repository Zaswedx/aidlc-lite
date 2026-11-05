# AI-DLC Lite

Claude Code와 Codex에서 사용하는 공통 스킬입니다.

기존 코드와 DB가 있는 **간단한 웹 사이트**용으로 AI-DLC를 줄인 버전입니다.
원래 AI-DLC의 20개 stage를 **5단계와 승인 게이트 3개**로 압축했습니다.

```
⓪ 현황 파악 ─▶ ① 요구+스토리 ─[승인]─▶ ② 설계 ─[승인]─▶ ③ 구현 (스토리마다) ─▶ ④ 검증 ─[승인]─▶ 완료
```

## 1. 단계

| 단계 | 스킬 | 원래 stage (합쳐진 것) | 산출물 (`aidlc-docs/`) | 승인 |
| --- | --- | --- | --- | --- |
| ⓪ 현황 파악 | `/lite-0-current` | Workspace Detection + Reverse Engineering | `current-state.md`, `state.md` | - |
| ① 요구 + 스토리 | `/lite-1-requirements` | Requirements Analysis + User Stories | `requirements.md` | ✅ 1 |
| ② 설계 | `/lite-2-design` | Application Design + Functional Design + NFR Requirements · Design | `design.md`, `data-rules.md` | ✅ 2 |
| ③ 구현 | `/lite-3-build <US-ID>` | Code Generation (TDD 3세션 → 1세션) | 코드 · 테스트 | - |
| ④ 검증 | `/lite-4-verify` | Build and Test + 추적성 점검 ①② | `verification.md` | ✅ 3 |
| 상태 | `/lite` | `/aidlc` | - | - |

생략한 stage: Workflow Planning (흐름 고정), Units Generation (스토리 = 작업 단위), Infrastructure Design (배포 대상 1줄로 대체), Operations 7개 (④의 배포 체크리스트로 대체)

## 2. 설치 (대상 웹 프로젝트에 복사)

먼저 저장소를 내려받습니다.

```sh
git clone https://github.com/Zaswedx/aidlc-lite.git
cd aidlc-lite
```

조건: Git 저장소인 대상 프로젝트, `python` 명령으로 Python 3.8 이상 실행 가능, POSIX 셸 (Linux/macOS 또는 Git Bash). 훅을 지원하는 최신 Codex를 사용하세요.

### Claude Code

```sh
python install.py claude /path/to/project
```

### Codex

```sh
python install.py codex /path/to/project
```

두 도구를 함께 쓰면 같은 대상에 두 명령을 모두 실행하세요. 대상 프로젝트의 하위 폴더를 지정해도 Git 루트에 설치됩니다.

| 구성 | 공통 원본 | Claude Code 설치 위치 | Codex 설치 위치 |
| --- | --- | --- | --- |
| 스킬 6개 · 규칙 | `skills/` | `.claude/skills/` | `.agents/skills/` |
| Python 훅 2개 | `hooks/` | `.aidlc-lite/hooks/` | `.aidlc-lite/hooks/` |
| 도구별 설정 | `config/claude.json`, `config/codex.json` | `.claude/settings.json` | `.codex/hooks.json` |

설치기는 같은 이름의 Lite 스킬과 공통 훅을 갱신하고, 기존 설정의 다른 항목과 다른 훅은 보존합니다. 반복 설치해도 동일 훅을 중복 추가하지 않습니다. 이전 버전의 기본 Claude 훅 설정도 새 경로로 전환합니다. 직접 수정한 Lite 파일은 설치 전에 백업하세요.

1. `AGENTS-snippet.md` 내용을 대상 프로젝트의 `AGENTS.md` (Claude만 쓰면 `CLAUDE.md`도 가능) 끝에 한 번 붙여 넣기
2. 대상 프로젝트의 `.gitignore`에 `aidlc-docs/` 추가 (원문 입력 로그 공개 방지)
3. 에이전트를 대상 프로젝트에서 새로 시작
4. Codex는 프로젝트를 신뢰한 뒤 `/hooks`에서 설치된 훅을 검토·신뢰해야 자동 기록과 세션 복원이 동작

Codex의 수동 실행 정책은 각 스킬의 `agents/openai.yaml`에 있습니다. Claude의 `disable-model-invocation`은 설치 시 추가합니다. 다음 단계는 두 도구 모두 사람이 직접 호출합니다.

Codex의 ③ 구현은 Orca 없이 내장 서브에이전트에 작업을 위임합니다. 스토리 1개 안에서 구현 담당 최대 2개가 파일과 공유 자원을 나누어 작업하고, 구현 종료 후 별도 에이전트가 검토합니다. 주 에이전트가 지적 사항 해결과 전체 테스트·lint를 확인한 뒤 상태를 기록합니다. 분할하기 어려우면 순차 위임하고, 서브에이전트 기능을 사용할 수 없으면 알린 뒤 단독으로 진행합니다. 병렬 실행은 토큰 사용량이 늘어납니다.

## 3. 사용 순서

아래는 Claude Code 표기입니다. Codex에서는 `/` 대신 `$`로 호출합니다. 예: `$lite-0-current`, `$lite-1-requirements 회원 목록에 검색 추가`, `$lite-3-build US-01`. 인자는 호출 뒤의 사용자 메시지에서 읽습니다.

```text
/lite-0-current                         # 기존 코드 · DB · 테스트 기준선 파악
/lite-1-requirements 회원 목록에 검색 추가   # 질문 답변 → 승인
/lite-2-design                          # 화면 + 데이터·규칙 설계 → 승인
/lite-3-build US-01                     # 스토리마다 반복
/lite-3-build US-02
/lite-4-verify                          # 전체 테스트 · 브라우저 · 추적표 → 최종 승인
/lite                                   # 언제든 상태 확인
```

## 4. 자동 장치 (hook)

| hook | 시점 | 하는 일 |
| --- | --- | --- |
| `lite_audit.py` | 사용자 입력마다 | `aidlc-docs/state.md` 가 있거나 `/lite` 또는 `$lite` 호출이면 입력 원문을 `audit.md` 에 기록 |
| `lite_session.py` | 세션 시작 · 재개 · 압축 | 현재 단계 · 진행 수 · audit 마지막 항목을 에이전트에게 알려 이어서 진행 |

`lite_audit.py`는 사용자 입력 원문을 로컬 `aidlc-docs/audit.md`에 저장합니다. 비밀번호·토큰 등 민감한 정보를 입력하지 말고, 대상 프로젝트에서도 이 로그를 공개 저장소에 커밋하지 않도록 주의하세요.

원래 버전에 있던 추적 ID 검사, 커버리지 검사, 상태 표시줄 hook은 뺐습니다.

## 5. 원래 AI-DLC와 다른 점

| 항목 | 원래 | Lite |
| --- | --- | --- |
| stage 수 | 20 | 5 |
| 승인 횟수 | stage마다 (약 15회) | 3회 |
| 작업 단위 | Unit (U1, U2…) 별도 생성 | 스토리 (US-01…) 그대로 |
| 설계 문서 | Unit마다 FD · NFR Req · NFR Design · Infra | 프로젝트당 `design.md` + `data-rules.md` |
| TDD | red · green · refactor 3개 스킬, 세션 분리 | 로직만 테스트 먼저, 한 세션 |
| 추적성 점검 | 2회 (서브에이전트) | ④에서 추적표 1회 |
| 규칙 원본 | `.aidlc-rule-details/` | `skills/lite/rules.md` 한 파일 |

## 6. 검증 · 참고

```sh
python -m unittest discover -s tests -v
```

설치 설정 병합·재설치·이전 Claude 설정 이전, 양쪽 호출의 감사 로그, 하위 폴더에서 실행한 훅의 저장 위치와 세션 복원을 검사합니다. 실제 에이전트 세션에서 설치 후 스킬과 훅 인식을 확인하세요.

- [Codex 스킬 탐색 · 호출 · 정책](https://developers.openai.com/codex/skills)
- [Codex 훅 설정 · 신뢰](https://learn.chatgpt.com/docs/hooks)
