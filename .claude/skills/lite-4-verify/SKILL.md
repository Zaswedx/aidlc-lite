---
name: lite-4-verify
description: AI-DLC Lite ④ 검증. 전체 빌드 · 테스트 (회귀 포함) · 브라우저 확인을 하고 스토리 ↔ 테스트 ↔ 화면 추적표를 verification.md 에 작성한 뒤 최종 승인을 받는다. 사용자가 /lite-4-verify 로 직접 호출할 때만 사용.
disable-model-invocation: true
---

# /lite-4-verify — ④ 검증

- 공통 규칙: `.claude/skills/lite/rules.md` 를 먼저 읽고 따름
- 원래 AI-DLC 의 Build and Test + 추적성 점검 ①② 를 압축한 단계 (배포가 있으면 배포 체크리스트 포함)
- 입력: `requirements.md`, `design.md`, `data-rules.md`, `current-state.md` (기준선), 코드 · 테스트
- 산출물: `aidlc-docs/verification.md`
- ✅ 승인 3 (최종)

## 절차

1. state.md 에 미완료 스토리가 있으면 목록을 보여주고 1️⃣ 구현 먼저 / 2️⃣ 미완료 상태로 검증 중 선택 요청
2. 실행: 빌드 · lint · 타입 검사 (있으면) · 전체 테스트
   - 기준선 대비 비교: 새로 실패한 테스트 = 회귀 → 이름 · 원인 기록 (고치지 말고 보고)
3. 브라우저 확인: 스토리마다 화면 1회 + design.md NFR 체크리스트 (360px · 1280px 너비, 키보드 이동)
   - Playwright · Chrome DevTools MCP 가 있으면 스크린샷을 `aidlc-docs/screens/` 에 저장, 없으면 사람이 확인할 항목 목록 제공
4. 추적표 작성: 모든 AC 에 테스트 또는 화면 확인이 1개 이상 있는지, 모든 BR 에 테스트가 있는지 대조
   - 빠진 항목 = "누락" 으로 표시 (지어내지 않음)
5. 배포 대상이 있으면 (design.md 5절) 배포 체크리스트 작성. 실제 배포 실행은 사람이 지시할 때만
6. `verification.md` 작성 → audit 기록 → 승인 요청 (rules.md 5절 형식, 승인 시 "완료")
7. 승인 → state.md `④ 검증` 체크, Current = 완료, Status = 완료

## verification.md 양식

```markdown
# 검증 (Verification)

## 1. 실행 결과
| 검사 | 명령 | 결과 |
| --- | --- | --- |
| 빌드 | | ✅ / ❌ |
| lint · 타입 | | |
| 테스트 | | 통과 n / 실패 n (기준선 대비 +n) |

## 2. 추적표
| 스토리 | AC · BR | 테스트 (파일::이름) | 화면 확인 (URL · 스크린샷) | 결과 |
| --- | --- | --- | --- | --- |
| US-01 | AC-01-1 | tests/...::test_... | /items · screens/us-01.png | ✅ |

## 3. NFR 체크리스트 결과
| 항목 | 결과 | 비고 |

## 4. 남은 문제
| 구분 (회귀 · 누락 · 버그) | 내용 | 제안 |

## 5. 배포 체크리스트 (해당 시)
- [ ] 빌드 산출물 생성
- [ ] 운영 DB 백업 → 마이그레이션 실행 (data-rules.md 2절 순서)
- [ ] 배포 · 실제 URL 에서 핵심 화면 확인
- [ ] 되돌리기 방법 확인
```
