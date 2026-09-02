#!/usr/bin/env bash
# extract.sh — first pass on a source PDF.
# Extracts a text layer and reports whether the extraction is trustworthy.
# Usage: bash extract.sh reading.pdf [first_page] [last_page]

set -euo pipefail

SRC="${1:-}"
FIRST="${2:-}"
LAST="${3:-}"

if [ -z "$SRC" ] || [ ! -f "$SRC" ]; then
  echo "usage: bash extract.sh <file.pdf> [first_page] [last_page]" >&2
  exit 1
fi

OUT="${SRC%.*}.txt"
RANGE_ARGS=()
if [ -n "$FIRST" ]; then RANGE_ARGS+=(-f "$FIRST"); fi
if [ -n "$LAST" ];  then RANGE_ARGS+=(-l "$LAST");  fi

extracted=""

if command -v pdftotext >/dev/null 2>&1; then
  pdftotext -layout "${RANGE_ARGS[@]}" "$SRC" "$OUT"
  extracted="pdftotext"
elif python3 -c "import pypdf" >/dev/null 2>&1; then
  python3 - "$SRC" "$OUT" "${FIRST:-1}" "${LAST:-0}" <<'PY'
import sys
from pypdf import PdfReader
src, out, first, last = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
reader = PdfReader(src)
end = last if last else len(reader.pages)
with open(out, "w", encoding="utf-8") as fh:
    for i in range(first - 1, end):
        fh.write(f"\n\n===== page {i+1} =====\n\n")
        fh.write(reader.pages[i].extract_text() or "")
PY
  extracted="pypdf"
else
  echo "ERROR: no extractor found. Install poppler-utils (pdftotext) or 'pip install pypdf'." >&2
  exit 2
fi

# Page count
if command -v pdfinfo >/dev/null 2>&1; then
  PAGES=$(pdfinfo "$SRC" | awk '/^Pages:/{print $2}')
else
  PAGES=$(python3 -c "from pypdf import PdfReader;print(len(PdfReader('$SRC').pages))" 2>/dev/null || echo 0)
fi

CHARS=$(wc -c < "$OUT" | tr -d ' ')
SPAN=$PAGES
if [ -n "$FIRST" ] && [ -n "$LAST" ]; then SPAN=$((LAST - FIRST + 1)); fi
[ "$SPAN" -gt 0 ] 2>/dev/null || SPAN=1
PER=$((CHARS / SPAN))

echo "----------------------------------------"
echo "source        : $SRC"
echo "output        : $OUT"
echo "method        : $extracted"
echo "pages in file : $PAGES"
echo "pages read    : $SPAN"
echo "characters    : $CHARS"
echo "chars/page    : $PER"
echo "----------------------------------------"

if   [ "$PER" -gt 1200 ]; then
  echo "VERDICT: healthy text layer. Proceed."
elif [ "$PER" -gt 200 ]; then
  echo "VERDICT: partial extraction. Spot-check the output. OCR may be needed."
  echo "  ocrmypdf --force-ocr \"$SRC\" \"${SRC%.*}-ocr.pdf\""
else
  echo "VERDICT: no usable text layer. This is a scan. Run OCR before building anything."
  echo "  ocrmypdf --force-ocr \"$SRC\" \"${SRC%.*}-ocr.pdf\" && bash \"$0\" \"${SRC%.*}-ocr.pdf\""
  exit 3
fi

echo
echo "REMINDER: never load this PDF as page images to read it. Past ~100 pages the earliest"
echo "pages drop out of memory silently. Build from $OUT only."
