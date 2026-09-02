---
name: walk-in-ready
description: >-
  Brian's cold-call prep engine for Berkeley Haas. Turns a syllabus, reading, chapter, case, or slide
  deck into three non-redundant study assets: a one-page web guide for the desk, a two-host podcast
  script (and mp3) for the walk or the gym, and a two-page print PDF for the classroom table.
  Use this skill whenever Brian says "walk in ready", names a lecture, class session, case, or
  chapter and asks for prep, uploads a syllabus or course reading, or asks to be ready for a cold
  call, a case discussion, a quiz, or a midterm. Also trigger on "make me a guide", "one sheet",
  "cheat sheet", "notes sheet", "prep me for", or "podcast this chapter". Always consult this skill
  first for course prep because it carries his setup profile, the mnemonic rules, the fact-check
  gate, and the PDF extraction rule that prevents silent chapter loss. Do not build study material
  for Brian from general knowledge when this skill applies.
---

# Walk-in Ready

Three assets from one reading. Built for the three moments that actually happen: the desk, the walk,
and the table while somebody else is talking.

Brian's profile lives in `my-setup.md`. **Read that file before every build. No exceptions.**
If it does not exist, run the interview in `references/setup.md` first.

---

## The three rules

1. **Fewer things, stickier.** Cap: six sections, three to five core ideas per lecture, eight to ten
   traps. Everything else gets one line or gets cut. If it feels thin, it is working.
2. **The mnemonic is the deliverable.** One hook per concept. Never two. A hook must *rebuild* the
   idea from scratch, not just name it. Cover the definition: if you cannot reconstruct it from the
   hook alone, the hook is decoration and gets replaced.
3. **10th grade reading level, graduate level ideas.** Short sentences. Plain words. Only the
   wrapper gets easy so the ideas go in faster.

---

## Order of operations

Run these in order. Do not skip step 2 or step 6.

| # | Step | Reference | Gate |
| --- | --- | --- | --- |
| 1 | Read `my-setup.md` | — | Missing → run `references/setup.md` |
| 2 | Extract source text | `references/extraction.md` | **Never read a long PDF as images** |
| 3 | Classify the course shape | `references/course-shapes.md` | Quant vs case vs performance |
| 4 | Pull 3-5 core ideas + traps | this file, below | Hard cap enforced |
| 5 | Build hooks | `references/mnemonics.md` | One per concept, cover test |
| 6 | **Fact-check pass** | this file, below | Blocking. No output ships unchecked |
| 7 | Build the web guide | `references/html-build.md` | Six sections max |
| 8 | Build the podcast | `references/podcast-build.md` + `voice.md` | 30 min, two hosts |
| 9 | Build the two-page PDF | `references/one-sheet.md` | Exactly two pages |
| 10 | Update the notes sheet | `references/notes-sheet.md` | Only if the exam allows one |
| 11 | Report what you built | this file, below | Paths + the 3 things to memorize |

---

## Step 4: pulling the ideas

Rank candidate concepts by cold-call probability, not by page count. A concept scores high when:

- The professor named it in the syllabus objective for that session
- The reading defines it formally AND gives a worked example
- It has a counterintuitive result (the place people get it backwards)
- It connects to the case or problem set due that week

For each surviving concept, capture five fields. Missing any field means the concept is not ready:

1. **Exact definition** in the book's own words, quoted
2. **The book's own example, with its real numbers.** Never invent numbers
3. **The say-out-loud sentence.** One or two sentences Brian speaks if his name gets called
4. **The trap.** The specific way this gets confused with its neighbor
5. **The hook.** One memory device, per `references/mnemonics.md`

**Traps table:** eight to ten rows. Columns: What people say | What is actually true | Why the mix-up
happens. Traps come from the reading's own hedges, footnotes, and "note that" sentences.

**Worked problems:** show the arithmetic, not just the answer. Every intermediate number visible.

---

## Step 6: the fact-check pass (blocking)

Real runs have shipped a backwards definition of survivorship bias, a statistic attributed to the
wrong company, and three linked rounding errors. A memorable wrong answer is worse than no answer,
because it gets said with total confidence.

Before any file is written, re-open the extracted source and verify, line by line:

- [ ] Every definition matches the source wording, not a paraphrase drifting toward the opposite
- [ ] Every number traces to a page or paragraph in the source. Cite the page in a comment
- [ ] Every named company, person, study, or year is attributed to the right one
- [ ] Every arithmetic chain re-computed independently, end to end
- [ ] Every directional claim (increases / decreases / positive / negative) checked against the text
- [ ] Anything not in the source is labeled `[outside the reading]` or cut

Anything that cannot be traced to the source gets cut or flagged inline. Do not smooth over a gap.
Report the flags in the closing summary so Brian can spot-check against his own book.

---

## Step 11: the closing report

Keep it to this shape. Speed matters more than prose.

```
BUILT: <course> — <session>
Source: <file>, <N> pages extracted, <method>
Files:  guide.html | podcast.md (+ podcast.mp3) | one-sheet.pdf
Core ideas: 1) ... 2) ... 3) ...
Memorize these three hooks: ...
Flagged for spot-check: <items, with page refs>
Time to review: ~<N> minutes
```

---

## Output locations

```
~/walk-in-ready/<course-code>/<session>/
  guide.html          the desk asset
  podcast.md          the script
  podcast.mp3         if audio was run
  one-sheet.pdf       the print asset
  source.txt          extracted text, kept for the fact-check trail
  notes-sheet.md      cumulative, at the course level, if allowed
```

---

## Hard rules

- **Never read a source PDF as images past ~100 pages.** It fails silently: early pages drop out of
  memory and nothing errors. Extract text first. See `references/extraction.md`.
- **Never invent a number, a page reference, or an example.** Pull it or flag it.
- **Never produce graded work.** This builds prep from assigned readings. Check the AI policy in
  `my-setup.md` before every build, and stop if the request touches a graded deliverable.
- **Never exceed two pages on the one-sheet.** Page three does not get printed.
- **Never give one concept two hooks.** They cancel.
- **Respect the off-limits list in `my-setup.md` literally and permanently.**
