---
name: lite-1-requirements
description: AI-DLC Lite ① 요구 + 스토리. 질문 5개 이내로 범위를 정하고 스토리 · 수용 기준 표를 requirements.md 에 작성한 뒤 승인을 받는다. 사용자가 /lite-1-requirements 로 직접 호출할 때만 사용.
argument-hint: "[요청 내용]"
disable-model-invocation: true
---

# /lite-1-requirements — ① 요구 + 스토리

- 공통 규칙: `.claude/skills/lite/rules.md` 를 먼저 읽고 따름
- 원래 AI-DLC 의 Requirements Analysis + User Stories 를 압축한 단계
- 입력: 사용자 요청 (`$ARGUMENTS` 또는 대화), `aidlc-docs/current-state.md`
- 산출물: `aidlc-docs/requirements.md`
- ✅ 승인 1

## 절차

1. 요청을 `current-state.md` 와 대조해 **유지 · 변경 · 추가 · 제외** 로 나눔
2. 모호한 점만 질문 (최대 5개, 선택지 + 추천안). 답을 받을 때까지 대기
   - 우선 확인할 것: 대상 사용자, 기존 기능 동작을 바꿔도 되는지, 기존 데이터 처리, 완료 판단 기준
3. `requirements.md` 작성 (아래 양식)
   - 스토리 1개 = ③ 구현 1회 분량 (화면 1~2개 또는 API 1~3개). 크면 나눔
   - 수용 기준은 테스트로 확인 가능한 문장 (숫자 · 상태 · 메시지를 구체적으로)
4. audit 기록 → 승인 요청 (rules.md 5절 형식, 다음 스킬 = `/lite-2-design`)
5. 승인 → state.md `① 요구 + 스토리` 체크, Current/Next/Status 갱신

## requirements.md 양식

```markdown
# 요구사항 (Requirements)

## 1. 목표
- (한두 줄)

## 2. 범위
| 구분 | 내용 |
| --- | --- |
| 유지 (바뀌면 안 됨) | |
| 변경 | |
| 추가 | |
| 제외 (이번에 안 함) | |

## 3. 스토리
| ID | 스토리 (누가 · 무엇을 · 왜) | 수용 기준 (AC) | 우선순위 | 영향 (화면 · API · 테이블) |
| --- | --- | --- | --- | --- |
| US-01 | | AC-01-1 ...<br>AC-01-2 ... | 높음 | |

## 4. 비기능 메모
- (성능 · 접근성 · 브라우저 · 보안 요구가 있으면)

## 5. 질문과 답
| # | 질문 | 답 |
```
