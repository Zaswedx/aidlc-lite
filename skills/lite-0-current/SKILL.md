---
name: lite-0-current
description: AI-DLC Lite ⓪ 현황 파악. 기존 웹 사이트 코드 · DB 스키마 · 테스트 현황을 1~2페이지로 정리하고 state.md 를 만든다. 사용자가 lite-0-current 로 직접 호출할 때만 사용.
---

# /lite-0-current — ⓪ 현황 파악

- 공통 규칙: [공통 규칙](../lite/rules.md) (이 SKILL.md 기준 상대 경로) 를 먼저 읽고 따름
- 원래 AI-DLC 의 Workspace Detection + Reverse Engineering 을 압축한 단계
- 산출물: `aidlc-docs/current-state.md`, `aidlc-docs/state.md` (없으면 생성)
- 승인 게이트 없음 (보고 후 ① 안내)

## 절차

1. `state.md` 가 이미 있고 ⓪ 이 완료면 → 1️⃣ 유지 / 2️⃣ 다시 파악 중 선택 요청
2. 조사 (읽기 위주, 코드 수정 금지)
   - 설정 파일 (`package.json`, `pyproject.toml`, `requirements.txt`, `docker-compose*` 등) · `README` · `AGENTS.md`
   - 라우트 · 페이지 정의, API 핸들러, DB 접근 코드, 스키마 · 마이그레이션 · seed 파일
   - 문서와 코드가 다르면 코드를 기준으로 하고 "불일치" 로 기록
3. 실행 확인: 테스트 명령을 실제로 실행해 **기준선** (통과 · 실패 수, 실패 테스트 이름) 기록
   - 실행 명령을 알 수 없거나 실행에 외부 자원 (운영 DB 등) 이 필요하면 실행하지 말고 질문
4. `current-state.md` 작성 (아래 양식, 2페이지 이내)
5. `state.md` 생성 · 갱신 (아래 양식), audit 기록
6. 요약 5줄 이내 + "다음: `/lite-1-requirements`" 안내

## current-state.md 양식

```markdown
# 현황 (Current State)

## 1. 스택 · 명령
| 항목 | 값 |
| --- | --- |
| 언어 · 프레임워크 | |
| DB (종류 · 접속 위치) | |
| 실행 · 빌드 · 테스트 · lint 명령 | |

## 2. 구조
| 경로 | 역할 |

## 3. 화면 · 라우트
| 경로 (URL) | 화면 | 파일 |

## 4. API
| 메서드 | 경로 | 하는 일 | 파일 |

## 5. DB 스키마
| 테이블 | 주요 컬럼 (타입 · 제약) | 관계 |
- 마이그레이션 방식: (도구 · 위치 · 실행 명령, 없으면 "없음")
- seed · 테스트 DB 준비 방식:

## 6. 테스트 기준선
- 명령 · 실행 시각:
- 결과: 통과 n / 실패 n (실패 테스트 이름)

## 7. 위험 지점 · 불일치
- (건드리면 영향이 큰 곳, 문서와 코드가 다른 곳, 테스트가 없는 핵심 로직)
```

## state.md 양식

```markdown
# AI-DLC Lite State

- **Project**: <이름>
- **Started**: <Timestamp>
- **Current Step**: ⓪ 현황 파악
- **Next Step**: ① 요구 + 스토리
- **Status**: ⓪ 완료

## Progress
- [x] ⓪ 현황 파악
- [ ] ① 요구 + 스토리 (승인 1)
- [ ] ② 설계 (승인 2)
- [ ] ③ 구현
- [ ] ④ 검증 (승인 3)
```
