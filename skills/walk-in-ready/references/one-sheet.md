# The two-page print PDF

Exactly two pages. Never three. Page three does not get printed, and the stapler is a lie.

This is the asset used *while somebody else is talking*. It gets scanned in two seconds, not read.

## Page 1: the table asset

- **Top third: the hooks.** All of them. Largest type on the page.
- **Middle: the three to five ideas.** One line each. The idea stated as a claim, then the
  say-out-loud sentence underneath in italics. Nothing else. No definitions, no examples.
- **Bottom: the traps table**, compressed to two columns: Wrong | Right. Drop the "why" column, it
  lives in the web guide.

## Page 2: the working asset

- **Formulas and worked arithmetic**, boxed, with every intermediate number shown.
- **The cold-call script**: three to five questions, each with a one-line spoken answer.
- **Six blank ruled lines at the bottom, labeled "what actually got said."** Class notes go here,
  which is why the sheet stays on the table instead of going in a bag.

## Build method

Write `one-sheet.html` with a print stylesheet, then render:

```bash
node scripts/qa.js one-sheet.html --pdf one-sheet.pdf --pages 2
```

`qa.js` renders with headless Chromium, exports the PDF, and **fails loudly if the output runs past
two pages.** If it reports three, cut content using the cut order below. Do not shrink the font below
9pt to force a fit; small type defeats the purpose of the asset. If it reports one page, there is
room for one more trap or one more worked problem.

## Print CSS that matters

```css
@page { size: letter; margin: 0.45in; }
body  { font-size: 10pt; line-height: 1.28; color: #000; }
.card { break-inside: avoid; }
h2    { break-after: avoid; }
table { width: 100%; border-collapse: collapse; font-size: 9.5pt; }
```

- No background fills behind large blocks. They drain ink and print grey.
- Rules and borders instead of shading for separation.
- Two columns on page 1 only if the hooks still clear 12pt.
- Never rely on color alone to distinguish anything. Assume black and white.

## The cut order (when it runs to three pages)

Cut in this order, top to bottom, until it fits:

1. The "why the mix-up happens" column
2. Prose around the worked problems, keeping the arithmetic
3. Traps beyond eight
4. Connections to prior sessions
5. The fifth core idea, demoted to a hook-only line

Never cut: the hooks, the say-out-loud lines, the blank note lines.
