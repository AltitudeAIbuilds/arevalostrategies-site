# Walk-in Ready — Brian's build

Three assets from one reading, built from your own syllabus and materials. Personalized for Berkeley
Haas, cold call culture, and the way you actually work.

## What you get, per session

| Asset | File | The moment it is for |
| --- | --- | --- |
| Web guide | `guide.html` | The desk. Hooks at the top, big enough to photograph. |
| Podcast | `podcast.md` + `podcast.mp3` | The walk in, or the gym. Two hosts, one wrong on purpose. |
| Two-page PDF | `one-sheet.pdf` | The table, while somebody else is talking. |

Not redundant by accident. Three moments, three formats.

## Install (Claude Code, or Cowork in the desktop app)

```bash
cp -R skills/walk-in-ready ~/.claude/skills/
```

Then upload a syllabus or a reading and say:

> walk in ready, lecture 3

## Install (claude.ai in the browser)

1. Open `PROJECT-INSTRUCTIONS.md`.
2. Copy everything below the divider.
3. Paste it into the custom instructions of a new Claude Project. One Project per course.
4. Start a chat, upload the syllabus, say "set me up."

Lost in the browser version: the audio pipeline and the page checker, both of which need a terminal.
The full podcast script still gets produced. Paste it into NotebookLM or ElevenLabs for audio; the
free tiers cover a 30 minute episode.

## Your setup file

`walk-in-ready/my-setup.md` is already pre-filled with your profile: aviation and DoD acquisition
background, the real estate portfolio, Berkeley and Savannah geography, tone, career lens, and the
three things worth worrying about.

Three blocks are marked **CONFIRM** and need ten minutes from you:

1. **The pop culture layer** in section 1. Television, film, music, sports, games. Answer twice: the
   thing, and the structural job it can do. This is the fastest-recall memory layer and it is the
   only one that cannot be pre-filled.
2. **The syllabi** in section 3. Upload them and the table fills itself in.
3. **The AI policy** in section 8. Blocking. Paste the exact language per course before the first
   build in that course.

Host names in section 2 are proposals. Rename them in thirty seconds if they are wrong.

## Three rules the whole thing runs on

1. **Fewer things, stickier.** Six sections, three to five ideas, eight to ten traps. Hard caps.
2. **The mnemonic is the deliverable.** One hook per concept, never two. A hook must rebuild the
   idea, not just name it.
3. **10th grade reading level, graduate level ideas.** Only the wrapper gets easy.

## Three warnings

1. **Check the course AI policy first.** Prep from assigned readings is usually fine. Anything
   touching graded work usually is not. The syllabus is the only thing that counts.
2. **It gets things wrong.** There is a blocking fact-check step for a reason. Real runs have caught
   a backwards definition, a statistic attributed to the wrong company, and three linked rounding
   errors. Spot-check numbers against your own book.
3. **Never let it read a long PDF as images.** It fails silently past about 100 pages: the earliest
   pages drop out of memory and nothing errors. `scripts/extract.sh` handles this.

## Contents

```
README.md                    this file
PROJECT-INSTRUCTIONS.md      the paste-into-claude.ai version
walk-in-ready/
  SKILL.md                   the engine, and the order things happen in
  my-setup.md                your profile. Everything personal lives here
  references/
    setup.md                 the ten minute interview
    mnemonics.md             the eight types of memory hook
    voice.md                 how to write two hosts who sound like people
    html-build.md            the six section guide, and the CSS traps
    podcast-build.md         the run of show and the audio pipeline
    one-sheet.md             the two-page print PDF
    extraction.md            reading a 900 page textbook without losing chapters
    course-shapes.md         quantitative vs case vs performance courses
    notes-sheet.md           the running cheat sheet, if your exam allows one
  scripts/
    extract.sh               first pass on your PDFs
    make_audio.py            script to mp3, free, no API key
    qa.js                    renders the guide and checks it in both themes
```

## Dependencies (optional, install as needed)

```bash
# text extraction
sudo apt install poppler-utils        # or: brew install poppler
pip install pypdf ocrmypdf            # ocrmypdf only for scanned sources

# audio
sudo apt install espeak-ng ffmpeg     # macOS uses the built-in 'say', still needs ffmpeg

# page checking
npm i -D playwright
```

Nothing here is required to get the web guide and the podcast script. They only unlock the mp3 and
the two-page assertion.
