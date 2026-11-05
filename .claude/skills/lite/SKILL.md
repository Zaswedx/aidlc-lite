---
name: lite
description: AI-DLC Lite 진행 상태 보기와 다음 단계 안내. 인자 없이 = 상태 보기, 단계 번호 (0~4) 를 주면 해당 단계 스킬 안내. 사용자가 /lite 로 직접 호출할 때만 사용.
argument-hint: "[status | 0 | 1 | 2 | 3 <US-ID> | 4]"
disable-model-invocation: true
---

# /lite — AI-DLC Lite 상태 보기

- 인자: `$ARGUMENTS`
- 공통 규칙 = [rules.md](rules.md)

## 흐름

```
⓪ 현황 파악 ─▶ ① 요구+스토리 ─[승인]─▶ ② 설계 ─[승인]─▶ ③ 구현 (스토리마다) ─▶ ④ 검증 ─[승인]─▶ 완료
```

| 번호 | 스킬 | 하는 일 |
| --- | --- | --- |
| 0 | `/lite-0-current` | 기존 코드 · DB · 테스트 현황 파악, state.md 생성 |
| 1 | `/lite-1-requirements` | 요구 + 스토리 + 수용 기준 |
| 2 | `/lite-2-design` | 화면 설계 + 데이터 · 규칙 설계 |
| 3 | `/lite-3-build <US-ID>` | 스토리 1개 구현 (로직은 테스트 먼저) |
| 4 | `/lite-4-verify` | 전체 테스트 · 브라우저 확인 · 추적표 |

## 동작

- 인자 없음 · `status`: `aidlc-docs/state.md` 를 읽기만 하고 아래 형식으로 출력 (파일 수정 · audit 기록 없음)

```markdown
# 🧭 AI-DLC Lite 상태

- 현재: [Current Step]
- 다음: [Next Step]
- 상태: [Status]
- 진행: [완료 단계 수] / 5, 스토리 [완료] / [전체]

- 이어서 진행: `/lite-[n]-[이름] [US-ID]`
```

- state.md 없음 → "AI-DLC Lite 시작 전" + `/lite-0-current` 안내
- 숫자 인자 → 해당 스킬 이름과 필요한 앞 산출물 존재 여부만 알려주고, 실행은 사용자가 그 스킬을 호출하도록 안내
