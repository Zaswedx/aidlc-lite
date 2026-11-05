---
name: lite-2-design
description: AI-DLC Lite ② 설계. 승인된 스토리로 화면 설계 (design.md) 와 데이터 · 규칙 설계 (data-rules.md) 를 작성하고, 구현 순서를 state.md 에 넣은 뒤 승인을 받는다. 사용자가 /lite-2-design 로 직접 호출할 때만 사용.
disable-model-invocation: true
---

# /lite-2-design — ② 설계

- 공통 규칙: `.claude/skills/lite/rules.md` 를 먼저 읽고 따름
- 원래 AI-DLC 의 Application Design + Functional Design + NFR Requirements · Design 을 압축한 단계 (Functional Design 은 DB 가 있으므로 `data-rules.md` 로 분리)
- 입력: `aidlc-docs/requirements.md` (승인됨), `aidlc-docs/current-state.md`
- 산출물: `aidlc-docs/design.md`, `aidlc-docs/data-rules.md`
- ✅ 승인 2 (두 파일 함께)

## 절차

1. 스토리마다 바뀌는 화면 · API · 테이블을 코드에서 확인 (추측 금지, 파일 경로 기록)
2. `design.md` 작성 (화면 · API · NFR)
3. `data-rules.md` 작성 (스키마 · 마이그레이션 · 업무 규칙 · 검증 · 오류)
   - 업무 규칙 1개 = 테스트 1개 이상이 되도록 구체적으로 (경계값 포함)
   - 스키마 변경이 없으면 "변경 없음" 으로 명시하고 1 · 2절 생략
4. 구현 순서 결정 (의존 관계: 스키마 → API → 화면), state.md `③ 구현` 아래에 스토리 하위 항목 추가

   ```markdown
   - [ ] ③ 구현
     - [ ] US-01 <제목>
     - [ ] US-02 <제목>
   ```

5. audit 기록 → 승인 요청 (rules.md 5절 형식, 다음 스킬 = `/lite-3-build <첫 US-ID>`)
6. 승인 → state.md `② 설계` 체크, Current/Next/Status 갱신

## design.md 양식

```markdown
# 설계 (Design)

## 1. 화면
| 경로 (URL) | 신규/변경 | 구성 요소 | 상태 (로딩 · 빈 화면 · 오류) | 관련 스토리 |

## 2. 컴포넌트
| 이름 | 신규/변경/재사용 | 파일 | 역할 |

## 3. API
| 메서드 | 경로 | 신규/변경 | 요청 | 응답 | 오류 (코드 · 조건) | 관련 스토리 |

## 4. NFR 체크리스트
| 항목 | 기준 | 확인 방법 |
| --- | --- | --- |
| 반응형 | 360px · 1280px 에서 가로 스크롤 없음 | ④ 브라우저 확인 |
| 접근성 | 폼 label, 키보드 이동, 대비 | ④ 브라우저 확인 |
| 성능 | 목록 페이지네이션 · 이미지 크기 등 | |
| 보안 | 입력 검증 · 권한 · SQL 파라미터 바인딩 | 테스트 |
| SEO | title · meta (공개 페이지만) | |

## 5. 배포 대상
- (예: 기존 서버에 그대로 / 없음)
```

## data-rules.md 양식

```markdown
# 데이터 · 규칙 설계 (Data & Rules)

## 1. 스키마 변경
| 테이블 | 변경 (추가 · 수정 · 삭제) | 컬럼 · 타입 · 제약 · 기본값 | 이유 (스토리) |

## 2. 마이그레이션
- 방식: (current-state.md 의 기존 방식)
- 순서 · 되돌리기 방법:
- 기존 데이터 영향: (NULL 처리 · 기본값 채우기 · 변환)

## 3. 업무 규칙
| ID | 규칙 | 경계값 · 예시 | 위반 시 동작 | 관련 스토리 · AC |
| --- | --- | --- | --- | --- |
| BR-01 | | | 400 + 메시지 "..." | US-01 / AC-01-1 |

## 4. 입력 검증
| 필드 | 규칙 | 오류 메시지 | 화면 · API 둘 다? |

## 5. 오류 처리
| 상황 | 응답 코드 | 화면 표시 |
| --- | --- | --- |
| 없는 대상 | 404 | |
| 지금 상태에서 불가한 동작 | 409 | |
| 잘못된 값 | 400 | |
```
