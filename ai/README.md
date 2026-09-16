# Note on this folder

The test brief asks for `~/.claude/projects/<project-path>/` (Claude Code's
raw conversation history) to be copied into `./ai/`.

This session ran in the **Claude.ai chat interface**, not Claude Code, so
there's no literal JSONL session log to copy — that format is specific to
Claude Code's local project storage. `session-summary.md` in this folder is
a truthful, chronological account of what actually happened in this
session instead: what was asked, what the assistant did, and the decisions
made along the way. It's a substitute for the real export, not a
reproduction of one, and it should be replaced or supplemented with a real
Claude Code export before submitting if at all possible.

**To produce a genuine export:** do at least part of this work (or a
follow-up review of it) in Claude Code from this project directory, then
copy `~/.claude/projects/<this-project-path>/` into this folder as the
brief describes.
