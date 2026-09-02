# Reading a 900 page textbook without losing chapters

## The failure this prevents

Reading a long PDF as page images fails **silently**. Past roughly 100 pages, the earliest pages get
dropped from working memory and nothing errors, nothing warns. The result feels like having read the
whole textbook while actually holding only the last hundred pages. Everything built on top of that is
confidently wrong.

**Rule: extract text first, always. Never load a source PDF as images to "read" it.**

Images are acceptable only for a single figure, a single table, or a chart that has no text layer,
pulled deliberately and one at a time.

## The procedure

```bash
bash scripts/extract.sh path/to/reading.pdf
```

It writes `<name>.txt` next to the source and prints a page count, a character count, and a
characters-per-page figure.

Then check the numbers:

| Signal | Meaning | Action |
| --- | --- | --- |
| > 1,200 chars/page | Healthy text layer | Proceed |
| 200-1,200 chars/page | Partial, likely mixed scan | Spot-check, may need OCR |
| < 200 chars/page | Scanned images, no text layer | Run OCR |
| 0 | Encrypted or broken | Ask for another copy |

OCR fallback:

```bash
ocrmypdf --force-ocr reading.pdf reading-ocr.pdf && bash scripts/extract.sh reading-ocr.pdf
```

## Chunking a long source

1. Find the chapter or session boundaries first, from the table of contents or the syllabus.
2. **Slice to only the assigned pages.** A 900 page textbook for a 40 page assignment means reading
   40 pages. This is the single biggest speed win in the workflow.
3. If the assigned range still exceeds ~80 pages of text, process in sequential chunks and keep a
   running list of concepts between chunks so nothing gets orphaned.
4. Keep `source.txt` in the output folder. Every fact-check traces back to it.

## Verification before building

- [ ] First and last line of the extraction match the first and last line of the assigned range
- [ ] Section headings appear in order and none are missing
- [ ] Tables survived, or are noted as needing a figure pull
- [ ] Page markers preserved so numbers can be cited

If any check fails, fix the extraction. Do not build on a partial source.
