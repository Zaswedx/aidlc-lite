# AI-DLC Lite 공통 규칙 (모든 단계 스킬이 따름)

## 1. 위치

- 문서 = `aidlc-docs/` 만 (코드는 절대 `aidlc-docs/` 에 두지 않음)
- 상태 = `aidlc-docs/state.md`, 감사 로그 = `aidlc-docs/audit.md`

| 단계 | 산출물 | 승인 |
| --- | --- | --- |
| ⓪ 현황 파악 `/lite-0-current` | `current-state.md` | - (보고만) |
| ① 요구 + 스토리 `/lite-1-requirements` | `requirements.md` | ✅ 승인 1 |
| ② 설계 `/lite-2-design` | `design.md`, `data-rules.md` | ✅ 승인 2 |
| ③ 구현 `/lite-3-build <US-ID>` | 코드 · 테스트 | - (스토리마다 보고) |
| ④ 검증 `/lite-4-verify` | `verification.md` | ✅ 승인 3 |

## 2. 시작 전 확인

1. `aidlc-docs/state.md` 읽기 (없으면 ⓪ 이 아닌 단계는 진행하지 않고 `/lite-0-current` 먼저 제안)
2. 앞 단계 산출물 존재 확인. 없으면 2지선다로 묻고 고를 때까지 대기
   - 1️⃣ 앞 단계 먼저 실행 / 2️⃣ 가정하고 진행 (가정 목록을 보여주고 audit 에 기록)
3. 앞 단계가 승인 대기 상태면 진행하지 않음

## 3. 질문

- 한 번에 최대 5개, 번호 선택지 (A/B/C + "기타") 와 추천안을 함께 제시
- 코드 · 문서로 확인 가능한 사실은 묻지 않고 직접 확인
- 답은 해당 산출물의 "질문과 답" 절에 기록

## 4. 감사 기록 (audit.md)

- 사용자 입력 원문은 hook 이 자동 기록 → 직접 쓸 때는 `**User Input**: (hook 기록 <Timestamp>)`
- 단계 시작 · 승인 요청 · 승인 · 완료 때 항목 추가 (Timestamp 는 hook 이 알려준 현재 시각, 추측 금지)

```markdown
## <단계 이름> - <시작 | 승인 요청 | 승인 | 완료>
**Timestamp**: YYYY-MM-DDTHH:MM:SSZ
**User Input**: (hook 기록 YYYY-MM-DDTHH:MM:SSZ)
**AI Response**: <한두 줄 요약>
**Context**: <단계 · 스토리 ID · 바뀐 파일>

---
```

## 5. 승인 게이트 (①, ②, ④)

- 산출물 작성 후 아래 형식으로 끝내고, 사람이 승인할 때까지 다음 단계 진행 금지

```markdown
> **🔍 승인 요청 (Review Required)**: `aidlc-docs/<파일>` 를 검토해 주세요.
>
> 1️⃣ **수정 요청 (Request Changes)** - 고칠 내용을 알려주세요
> 2️⃣ **승인 (Approve)** - 다음 단계 `<다음 스킬>` 로 진행
```

- 수정 요청 → 고친 뒤 같은 형식으로 다시 승인 요청
- 승인 → state.md 체크 · audit 기록 후 다음 단계 안내 (자동으로 시작하지 않음)

## 6. 상태 갱신 (state.md)

- 단계 완료 시 `- [x]` 로 바꾸고 `Current Step` · `Next Step` · `Status` 갱신
- ③ 구현은 하위 항목 (스토리) 이 모두 `[x]` 일 때 상위 항목을 `[x]`

## 7. 기존 코드 · DB 보호

- 기존 테스트 삭제 · skip 처리 금지. 기존 테스트 기대값 변경은 이유를 보여주고 사람 승인 후
- DB 스키마 변경은 승인된 `data-rules.md` 에 있는 것만, 방식은 프로젝트 기존 마이그레이션 방식 따름
- SQL 문자열 조합 금지 (파라미터 바인딩)
- 패키지 추가 · 운영 DB 접근 · 데이터 삭제는 사람에게 먼저 질문
- 프로젝트 `AGENTS.md` / `CLAUDE.md` 의 규칙이 이 문서보다 우선
