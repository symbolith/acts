#!/usr/bin/env python3
import difflib
import io
import json
import subprocess
import sys
from functools import reduce
from pathlib import Path


def git(directory, *arguments):
    result = subprocess.run(["git", "-C", directory, *arguments], stdout=subprocess.PIPE)
    return result.stdout.decode() if result.returncode == 0 else sys.exit(result.returncode)


def content_blocks(transcript):
    with open(transcript, encoding="utf-8") as entries:
        for entry in filter(str.strip, entries):
            message = json.loads(entry).get("message")
            content = message.get("content") if isinstance(message, dict) else None
            if isinstance(content, list):
                yield from (block for block in content if isinstance(block, dict))


def replay(text, edit):
    if edit["name"] == "Write":
        return edit["input"]["content"]
    old, new = edit["input"]["old_string"], edit["input"]["new_string"]
    matches = text.count(old)
    if matches != 1 and not (matches and edit["input"].get("replace_all")):
        sys.exit(f"session-patch: {matches} matches in the committed text for the session edit {old!r}")
    return text.replace(old, new)


def unified_diff(before, after, path):
    lines = difflib.unified_diff(
        io.StringIO(before).readlines(),
        io.StringIO(after).readlines(),
        f"a/{path}",
        f"b/{path}",
    )
    return "".join(line if line.endswith("\n") else f"{line}\n\\ No newline at end of file\n" for line in lines)


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: session-patch.py <transcript> <file>")
    transcript, file = sys.argv[1], Path(sys.argv[2]).resolve()
    repository = Path(git(file.parent, "rev-parse", "--show-toplevel").strip())
    path = file.relative_to(repository).as_posix()
    committed = git(repository, "show", f"HEAD:{path}")
    blocks = list(content_blocks(transcript))
    failed = {
        block["tool_use_id"]
        for block in blocks
        if block.get("type") == "tool_result" and block.get("is_error")
    }
    edits = (
        block
        for block in blocks
        if block.get("type") == "tool_use"
        and block.get("name") in {"Edit", "Write"}
        and block["id"] not in failed
        and Path(block["input"]["file_path"]).resolve() == file
    )
    sys.stdout.write(unified_diff(committed, reduce(replay, edits, committed), path))


if __name__ == "__main__":
    main()
