#!/usr/bin/env python3
"""make_audio.py - turn a two-host podcast script into an mp3. Free, offline, no API key.

Usage:
    python3 make_audio.py podcast.md podcast.mp3

Input format (one speaker per line):
    **DOC:** Fixed costs do not vote.
    **ROOK:** Wait, so if I already spent it, it still counts?

Engines, in order of preference:
    macOS   : say                (two system voices)
    Linux   : piper, then espeak-ng
Concatenation uses ffmpeg when present. If no engine is found, per-speaker text files are
written instead so the script can be pasted into NotebookLM or ElevenLabs.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

LINE = re.compile(r"^\s*\*\*([A-Za-z0-9 _'-]{1,24})\s*:?\*\*\s*:?\s*(.+?)\s*$")

MAC_VOICES = ["Alex", "Samantha", "Daniel", "Karen"]
ESPEAK_VOICES = ["en-us+m3", "en-us+f3"]


def parse(path):
    turns, speakers = [], []
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            m = LINE.match(raw)
            if not m:
                continue
            name, text = m.group(1).strip().upper(), m.group(2).strip()
            text = re.sub(r"\[[^\]]{0,40}\]", "", text)          # drop [laughs]
            text = re.sub(r"[*_`#]", "", text).strip()
            if not text:
                continue
            if name not in speakers:
                speakers.append(name)
            turns.append((name, text))
    return turns, speakers


def have(binary):
    return shutil.which(binary) is not None


def pick_engine():
    if sys.platform == "darwin" and have("say"):
        return "say"
    if have("piper"):
        return "piper"
    if have("espeak-ng"):
        return "espeak-ng"
    if have("espeak"):
        return "espeak"
    return None


def synth(engine, text, voice_index, wav_path):
    if engine == "say":
        voice = MAC_VOICES[voice_index % len(MAC_VOICES)]
        aiff = wav_path.replace(".wav", ".aiff")
        subprocess.run(["say", "-v", voice, "-o", aiff, text], check=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", aiff, wav_path], check=True)
        return
    if engine in ("espeak-ng", "espeak"):
        voice = ESPEAK_VOICES[voice_index % len(ESPEAK_VOICES)]
        subprocess.run([engine, "-v", voice, "-s", "168", "-w", wav_path, text], check=True)
        return
    if engine == "piper":
        model = os.environ.get("PIPER_MODEL")
        if not model:
            raise RuntimeError("piper found but PIPER_MODEL is not set to a .onnx voice path")
        proc = subprocess.run(
            ["piper", "--model", model, "--output_file", wav_path],
            input=text.encode("utf-8"), check=True,
        )
        return proc


def fallback(turns, speakers, out_mp3):
    base = os.path.splitext(out_mp3)[0]
    for name in speakers:
        path = f"{base}-{name.lower()}.txt"
        with open(path, "w", encoding="utf-8") as fh:
            for who, text in turns:
                if who == name:
                    fh.write(text + "\n\n")
        print(f"wrote {path}")
    print("\nNo local TTS engine found. Two options:")
    print("  1. Install one:  brew install espeak-ng   |   sudo apt install espeak-ng ffmpeg")
    print("  2. Paste the original markdown into NotebookLM or ElevenLabs. Free tiers cover 30 min.")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    src, out_mp3 = sys.argv[1], sys.argv[2]

    turns, speakers = parse(src)
    if not turns:
        print(f"ERROR: no '**NAME:** text' lines found in {src}", file=sys.stderr)
        sys.exit(2)

    words = sum(len(t.split()) for _, t in turns)
    print(f"{len(turns)} turns, {len(speakers)} speakers ({', '.join(speakers)}), {words} words")
    print(f"estimated runtime: {words / 155:.1f} minutes")

    engine = pick_engine()
    if engine is None or not have("ffmpeg"):
        if engine is None:
            print("no TTS engine found")
        else:
            print("ffmpeg not found, cannot concatenate audio")
        fallback(turns, speakers, out_mp3)
        sys.exit(0)

    print(f"engine: {engine}")
    tmp = tempfile.mkdtemp(prefix="walkin-")
    wavs = []
    for i, (name, text) in enumerate(turns):
        wav = os.path.join(tmp, f"{i:04d}.wav")
        try:
            synth(engine, text, speakers.index(name), wav)
            wavs.append(wav)
        except Exception as exc:                      # keep going, one bad line is not fatal
            print(f"  skipped turn {i} ({name}): {exc}", file=sys.stderr)
        if i % 25 == 0:
            print(f"  {i}/{len(turns)}")

    if not wavs:
        fallback(turns, speakers, out_mp3)
        sys.exit(0)

    listfile = os.path.join(tmp, "list.txt")
    with open(listfile, "w", encoding="utf-8") as fh:
        for w in wavs:
            fh.write(f"file '{w}'\n")

    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
         "-i", listfile, "-b:a", "96k", out_mp3],
        check=True,
    )
    size = os.path.getsize(out_mp3) / 1_000_000
    print(f"wrote {out_mp3} ({size:.1f} MB)")
    shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
