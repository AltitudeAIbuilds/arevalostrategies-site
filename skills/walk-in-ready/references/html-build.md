# The web guide: six sections and the CSS traps

One self-contained HTML file. No external scripts, no CDN calls, no build step. It has to open from a
phone on airplane mode.

## The six sections, in this order

1. **Memory hooks, all of them, at the top.** Big type. This block is designed to be photographed and
   read one-handed on the walk from the parking structure. Nothing above it. No preamble.
2. **The three to five core ideas.** One card each: exact definition (quoted from the source), the
   book's own example with its real numbers, and the say-out-loud sentence in a visually distinct
   block.
3. **The traps table.** Eight to ten rows: What people say | What is actually true | Why the mix-up
   happens.
4. **Worked problems.** Full arithmetic, every intermediate step visible. Answer alone is worthless.
5. **The cold-call script.** Three to five likely questions with a 20-second spoken answer each.
6. **Connections.** Four to six lines maximum tying this session to the prior one and to the case or
   problem set due this week. Then stop.

Six sections. Not seven. If something does not fit, it gets one line inside an existing section or it
gets cut.

## Layout rules

- Single column, max width around 780px, centered.
- Hooks section: font-size at least 1.5rem, generous line height, high contrast.
- Every card has a one-line title that states the idea, not the topic. "Sunk costs do not vote"
  beats "Sunk Cost."
- Say-out-loud lines get a left border, a tinted background, and italics. They must be findable in a
  half-second scan.
- Tables scroll inside their own `overflow-x:auto` container. The page body never scrolls sideways.

## The CSS traps (these are the ones that actually bite)

1. **Dark mode.** Define the full light palette on bare `:root`, then override tokens inside
   `@media (prefers-color-scheme: dark)`. Never give a color its only definition inside a media
   query. Set an explicit `background` on `body` or it inherits whatever the host paints.
2. **Print.** Add `@media print`: remove backgrounds behind large blocks, force `color:#000`, set
   `break-inside: avoid` on cards, and hide anything interactive. People print the guide even though
   the one-sheet exists.
3. **`position: sticky` inside a table** silently does nothing in several browsers. Do not use it.
4. **Long formulas** overflow on phones. Wrap them in `overflow-x:auto`, never `word-break: break-all`,
   which chops numbers mid-digit and creates a false value.
5. **`vh` units on mobile** shift when the browser chrome hides. Use `min-height:100svh` or nothing.
6. **Emoji as the only signal** fails in print and for screen readers. Always pair with a text label.
7. **Font stack:** system fonts only. `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`.
   A webfont that fails to load offline shifts the whole layout.

## Self-check before shipping

- [ ] Opens with no network
- [ ] Readable at arm's length on a phone, in sunlight (contrast ratio at least 7:1 on hooks)
- [ ] Prints without cutting a card in half
- [ ] Every number matches the fact-check pass
- [ ] Six sections, not seven
