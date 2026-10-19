---
name: explain
description: Explain or summarize a text, note, formula, or concept for an intelligent 14-year-old reader, in plain sentences with the field's correct terms kept and defined at first use, and with no metaphors. Use when the user asks to "explain", "summarize", "eli14", "break this down", "what does this mean", or wants a passage, note, formula, or concept made understandable.
argument-hint: <thing, file, or passage>
allowed-tools: Read, Glob, Grep
---

# Explain plainly

Explain or summarize `$ARGUMENTS`. If it names a file or note, read it in full first. If it names something from the conversation, work from the conversation.

## Reader

An intelligent 14-year-old: quick, attentive, and with zero prior knowledge of the field. Skip no steps. Never condescend.

## Rules

- No metaphors, no analogies, no anthropomorphizing. Say what the thing is and does, never what it is like.
- Keep the correct termini. Define each term in one plain clause at its first use, then use exactly that term, never a synonym for it.
- Short sentences. One point per sentence.
- Lead with the point: one sentence stating what the thing is or what the text claims. Then the parts, in the order the reader needs them, each part built only from terms already defined.
- A summary states what the text claims, not what it is about.
- An example must be a real instance from the source, not an invented story.
- Stop when the thing is explained. No closing recap.
