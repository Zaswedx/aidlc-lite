# AI-DLC Lite

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

1. 이 폴더의 `.claude/skills/` 와 `.claude/hooks/` 를 대상 프로젝트의 `.claude/` 아래로 복사
2. `.claude/settings.json`
   - 대상 프로젝트에 없으면 그대로 복사
   - 이미 있으면 `hooks` 의 `UserPromptSubmit` · `SessionStart` 항목만 병합
3. `AGENTS-snippet.md` 내용을 대상 프로젝트의 `AGENTS.md` (또는 `CLAUDE.md`) 끝에 붙여 넣기
4. Claude Code를 대상 프로젝트에서 새로 시작 (hook · 스킬 인식)

조건: `python` 명령으로 Python 3.8 이상 실행 가능 (hook은 표준 라이브러리만 사용)

## 3. 사용 순서

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
| `lite_audit.py` | 사용자 입력마다 | `aidlc-docs/state.md` 가 있거나 `/lite` 호출이면 입력 원문을 `audit.md` 에 기록 |
| `lite_session.py` | 세션 시작 · 재개 · 압축 | 현재 단계 · 진행 수 · audit 마지막 항목을 Claude에게 알려 이어서 진행 |

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
| 규칙 원본 | `.aidlc-rule-details/` | `.claude/skills/lite/rules.md` 한 파일 |
