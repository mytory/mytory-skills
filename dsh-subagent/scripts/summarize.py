#!/usr/bin/env python3
"""dsh --json 출력에서 메인이 읽을 요약만 뽑는다."""
import json
import sys

FINAL_LIMIT = 4000

out_path, err_path, code = sys.argv[1], sys.argv[2], sys.argv[3]
session = final = None
steps = tools = fresh = output = cached = context = 0

with open(out_path, encoding="utf-8", errors="replace") as lines:
    for line in lines:
        try:
            event = json.loads(line)
        except ValueError:
            continue
        kind = event.get("type")
        if kind == "session":
            session = event.get("sessionId")
        elif kind == "tool_call":
            tools += 1
        elif kind == "final":
            final = event.get("text")
        usage = event.get("usage")
        if kind == "status" and isinstance(usage, dict):
            steps += 1
            fresh += usage.get("inputTokens") or 0
            output += usage.get("outputTokens") or 0
            cached += usage.get("cacheReadTokens") or 0
            context = (usage.get("inputTokens") or 0) + (usage.get("cacheReadTokens") or 0)

print(f"exit={code} session={session}")
print(f"steps={steps} tools={tools} input={fresh} output={output} cache_read={cached} last_context={context}")
if not final or code != "0":
    print("최종 보고 없음 또는 실패. 오류 출력 끝부분:")
    with open(err_path, encoding="utf-8", errors="replace") as err:
        print("".join(err.readlines()[-8:])[:1500])
if final:
    print(final[:FINAL_LIMIT])
    if len(final) > FINAL_LIMIT:
        print(f"... {len(final) - FINAL_LIMIT}자 생략")
