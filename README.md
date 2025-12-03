# PostPost

Python utilities for post-processing Fanuc-style CNC programs for specific machines. Each script rewrites an input program in-place based on machine-specific rules (tool changes, retracts, macro calls, and header numbering).

Overview
- Standalone Python scripts (standard library only: os, re, math).
- Input file is typically fil.md at the repo root; scripts overwrite this file.
- Scripts compute the next available O-number (>1000) by scanning a machine program folder and update the program header accordingly.
- Machine selection is per-script; each file targets a specific machine/config.

Prerequisites
- Windows
- Python 3.x installed and available on PATH (python command)
- (Optional) Git, to review or revert local changes

Quick start (PowerShell)
1) Put the CNC program you want to transform into fil.md in this folder.
2) Open the script you plan to use and update the directory_path variable to the correct machine folder (e.g. P:\Produksjon\CNCEdit\Programmer\... ).
3) Run the script:
   - python .\220LM.py
   - python .\12L.py
   - python .\700XLY.py
   - python .\M_fix.py (interactive generator; prints output, does not modify files)
4) Review changes (if this repo is a Git repo):
   - git --no-pager diff -- fil.md
5) Revert fil.md to last commit if needed:
   - git restore --source=HEAD -- fil.md

Scripts (what they generally do)
- 12L.py, NL3000.py
  - Use G00 X300. as end marker in tool ranges; replace T**** with G00 Z300.
  - Remove P11/P12, chamfer on/off, chip conveyor macros; normalize certain G28 to G00 X300.

- 220LM.py and "220 test.py"
  - Use G30 U0. as end marker; replace T**** with G30 W0.
  - Compute envelope (rounded X/Z) and inject G1901 D{X}. K2. L{Z+10}. E2. after G40 G80 G99.
  - In milling blocks (P12), swap M03/M05 to M33/M35; remove G17/G17.1, Y0., M289; sometimes clamp spindle speed (e.g., G50 S2800 -> S1500).

- 3100xly.py, 400L.py, 700LM.py, 700LY.py, 700XLY.py
  - Replace tool codes with G65 P9029 A50. B1. for the first tool, then B0. for subsequent tools (enforced across the file).
  - Compute envelope and insert G1901 line; some add M42 or M43.
  - 700XLY.py also inserts M24 after each tool change (T...).

- M_fix.py (interactive macro text generator)
  - Print a numbered list of supported machine styles, prompt for selection, then prompt for text.
  - Emit header, per-character G65 macro lines (supports A–Z, 0–9, symbols, and local letters like Æ/Ø/Å), and a footer to stdout.

How it works (common pipeline)
1) Find next O-number: list files in the configured machine directory, filter numeric basenames >1000, choose the first gap from 1001.
2) Apply machine-specific regex/text rewrites: normalize retracts, remove housekeeping codes, swap spindle/coolant codes when needed.
3) Optionally analyze tool ranges: find T… to end marker, compute X/Z maxima/minima, and insert comment lines with extremes.
4) Rewrite header to % and O{number} () and save to fil.md.

Notes & cautions
- Scripts overwrite fil.md. Keep backups or use Git to manage changes.
- Regex-based transformations depend on exact formatting (e.g., "G28 U0. V0." vs "G28 U0."). If your input differs, some changes may not apply.
- Paths like P:\Produksjon\CNCEdit\Programmer\… must exist and be reachable from this machine.

Future improvements (optional)
- Add CLI arguments for input filename and machine directory (instead of editing directory_path and using fil.md).
- Add a small test corpus of input programs and expected outputs per machine.
