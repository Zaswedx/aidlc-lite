<!-- 대상 프로젝트의 AGENTS.md (또는 CLAUDE.md) 끝에 아래 절을 붙여 넣으세요 -->

## AI-DLC Lite 진행 규칙

- 흐름: ⓪ 현황 파악 → ① 요구 + 스토리 → ② 설계 → ③ 구현 (스토리마다) → ④ 검증
- 스킬: `/lite` (상태), `/lite-0-current`, `/lite-1-requirements`, `/lite-2-design`, `/lite-3-build <US-ID>`, `/lite-4-verify`
- 공통 규칙: `.claude/skills/lite/rules.md`
- 문서는 `aidlc-docs/` 에만, 상태는 `aidlc-docs/state.md`
- 승인 게이트 3개 (① · ② · ④): 사람 승인 전 다음 단계 진행 금지
- 구현: API · DB · 업무 규칙 · 입력 검증은 테스트 먼저 (RED → GREEN → 정리), 화면은 구현 후 브라우저 확인
- DB 스키마 변경은 승인된 `aidlc-docs/data-rules.md` 에 있는 것만, 기존 마이그레이션 방식으로
- 기존 테스트 삭제 · skip 금지, 패키지 추가 · 운영 DB 작업은 사람에게 먼저 질문
