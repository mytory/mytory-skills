---
name: obsidian-vault
description: Obsidian 볼트에서 노트를 검색, 생성, 관리하며 위키링크와 색인 노트를 사용합니다. "Obsidian 노트 찾아줘", "볼트에 새 노트 만들어줘", "노트 정리해줘"라고 할 때 사용합니다.
---

# Obsidian 볼트

## 볼트 위치

`/mnt/d/Obsidian Vault/AI Research/`

대부분 루트에 평면적으로 배치.

## 네이밍 규칙

- **색인 노트**: 관련 주제 집계 (예: `Ralph Wiggum Index.md`, `Skills Index.md`, `RAG Index.md`)
- 모든 노트명은 **Title Case**
- 폴더로 정리하지 않음 — 대신 링크와 색인 노트 사용

## 링크

- Obsidian `[[wikilinks]]` 문법 사용: `[[노트 제목]]`
- 노트 하단에 의존성/관련 노트로 연결
- 색인 노트는 단순히 `[[wikilinks]]` 목록

## 작업 흐름

### 노트 검색

```bash
# 파일명으로 검색
find "/mnt/d/Obsidian Vault/AI Research/" -name "*.md" | grep -i "키워드"

# 내용으로 검색
grep -rl "키워드" "/mnt/d/Obsidian Vault/AI Research/" --include="*.md"
```

또는 볼트 경로에 직접 Grep/Glob 도구 사용.

### 새 노트 생성

1. 파일명에 **Title Case** 사용
2. 학습 단위로 내용 작성 (볼트 규칙에 따름)
3. 하단에 관련 노트로의 `[[wikilinks]]` 추가
4. 번호가 매겨진 시퀀스의 일부라면 계층적 번호 체계 사용

### 관련 노트 찾기

볼트 전체에서 `[[노트 제목]]`을 검색하여 백링크 찾기:

```bash
grep -rl "\\[\\[노트 제목\\]\\]" "/mnt/d/Obsidian Vault/AI Research/"
```

### 색인 노트 찾기

```bash
find "/mnt/d/Obsidian Vault/AI Research/" -name "*Index*"
```
