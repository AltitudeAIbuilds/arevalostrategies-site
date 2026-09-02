# The podcast: run of show and audio pipeline

Target 30 minutes. That is roughly 4,200 to 4,800 spoken words. Write to the word count, not to a
feeling.

## Run of show

| Segment | Minutes | Words | What happens |
| --- | --- | --- | --- |
| Cold open | 0-1 | ~150 | The curious host states the one question the chapter answers. No intro. |
| Framing | 1-4 | ~500 | Precise host lays out the three to five ideas and why this session exists. |
| Idea 1 | 4-10 | ~900 | Definition, the book's example with real numbers, one wrong guess and its correction. |
| Idea 2 | 10-16 | ~900 | Same shape. Different wrong guess. |
| Idea 3 | 16-22 | ~900 | Same shape. Hardest idea goes here, when attention is still holding. |
| Traps round | 22-27 | ~750 | Rapid fire. Curious host reads the wrong version, precise host corrects it. Six to eight of them. |
| Cold-call rehearsal | 27-29 | ~300 | Precise host asks the likely question. Curious host answers out loud, correctly, in one breath. |
| Close | 29-30 | ~150 | The three hooks, spoken. Nothing else. |

Ideas 4 and 5, if they exist, get 60 seconds each folded into the traps round. Do not extend the
runtime; extending it means it does not get finished on the walk.

## Script format

Plain markdown. One speaker per line, name in bold, no stage directions except sparse `[laughs]` or
`[pause]`. This format feeds the audio script directly.

```
**DOC:** Fixed costs do not vote. That is the whole chapter in five words.
**ROOK:** Wait, so if I already spent it, I still count it against the project?
**DOC:** No. Opposite. It already left the account.
**ROOK:** Right — so the only question is what it costs me from here forward.
```

## Fidelity rules

- Every number spoken must be in the source. Speak it once as an approximation, once exactly.
- Never let a wrong guess sit uncorrected across a segment break. Correct it inside the same segment.
- The final restatement after every correction belongs to the curious host, not the precise one.
- Read `voice.md` before writing a single line.

## Audio pipeline

`scripts/make_audio.py` converts the script to a two-voice mp3. Free, offline, no API key.

```bash
python3 scripts/make_audio.py podcast.md podcast.mp3
```

- Parses `**NAME:**` lines and alternates voices.
- Uses the system TTS: `say` on macOS, `espeak-ng` or `piper` on Linux. It reports which one it found.
- Falls back to writing per-speaker text files if no engine is present, so nothing is lost.

If the audio step fails, ship the script anyway and say so. NotebookLM or ElevenLabs will take the
markdown directly and the free tiers cover a 30 minute episode.
