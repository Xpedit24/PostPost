# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

Repository overview
- This repo contains standalone Python scripts that post-process CNC programs (Fanuc-style G/M-code). Each script targets a specific machine configuration and rewrites an input program in-place based on machine-specific rules.
- There are no external Python dependencies; only the standard library (os, re, math) is used.
- There is no existing README, linter config, or test suite.

Common commands (Windows PowerShell)
- List available scripts
  - Get-ChildItem -Name *.py

- Run a script (operates on fil.md in the repo directory)
  - python .\220LM.py
  - python .\12L.py
  - python .\700XLY.py
  - python .\M_fix.py  (interactive)

- Inspect what changed in fil.md after running a script (if repo is Git-initialized)
  - git --no-pager diff -- fil.md

- Discard changes to fil.md (restore last committed version)
  - git restore --source=HEAD -- fil.md

Notes on running the scripts
- Input file: Most scripts read and modify a file named fil.md in the repository root. Ensure the file contains the CNC program you want to transform.
- Program numbering: Each script scans a machine-specific directory (e.g., a P:\Produksjon\... path) to find the first available program number > 1000, and then sets the program header to O{that_number}.
- Machine directory: The directory_path variable is hardcoded per script. Update it in the script before running, or copy the script and adjust the path for your machine.
- Output: Scripts overwrite fil.md in place. Use Git to review or revert changes.
- Interactive generator: M_fix.py is interactive and prints out Fanuc macro lines for engraving characters based on the selected machine and input text; it does not modify files by itself.

Build, lint, and tests
- Build: Not applicable (pure Python scripts).
- Lint/format: No linter/formatter is configured in this repo.
- Tests: No test framework or tests are present. There is no single-test command configured.

High-level architecture and patterns
Across the machine-specific scripts (e.g., 12L.py, 220LM.py, 400L.py, 700LM.py, 700LY.py, 700XLY.py, 3100xly.py, NL3000.py), the overall processing pipeline is similar:

1) Program number allocation
   - find_first_available_number(directory):
     - Lists files in a given machine directory.
     - Extracts numeric basenames, filters to > 1000, then finds the first missing number in the sequence starting at 1001.
     - This value becomes the O-number in the program header.

2) Machine-specific rewrites (regex- and text-based)
   - Replace tool change tokens (e.g., T0100, T0200, …) with machine-specific motion or macro calls:
     - Examples: G00 Z300., G30 W0., or G65 P9029 A50. B1./B0. (with B1 on the first tool, B0 on subsequent ones).
   - Remove or normalize housekeeping lines:
     - Common removals include P11/P12 flags, M277/M278 (chamfering), M24/M25 (chip conveyor), Y0., G54, and certain G28/G30 retract patterns.
   - Insert or adjust machine macros based on measured envelope:
     - Several scripts compute the largest absolute X/Z coordinates in the program (sometimes excluding specific sentinel values like X191016), then inject a setup line such as:
       - G1901 D{rounded_x}. K2. L{rounded_z + 10}. E2.
     - Some scripts also insert coolant or spindle mode lines (e.g., M42, M43, or swap M03/M05 to M33/M35 when milling blocks are detected via P12).

3) Tool-range analysis and annotation
   - find_tool_ranges(content) identifies ranges of lines per tool by locating T-codes (outside parentheses) and using a machine-specific end marker. End markers vary per machine, for example:
     - G00 X300.
     - G28 U0. V0.
     - G30 U0.
   - insert_comment_before_operation(content, ranges) computes X/Z maxima and minima within each tool range and inserts a two-line comment right before the operation (typically 3–4 lines above the range start):
     - (X: MAX = <x_max>, MIN = <x_min>)
     - (Z: MAX = <z_max>, MIN = <z_min>)

4) Header rewrite and cleanup
   - The first lines of fil.md are replaced to include the % line and a program header like O{number} ().
   - Some scripts remove lines following an (OPERATION ...) marker if they match a retract pattern; details vary by machine.
   - The file is then written back to fil.md.

Machine-specific highlights (non-exhaustive)
- 12L.py / NL3000.py
  - End marker uses G00 X300.
  - Tool codes replaced with G00 Z300.
  - Removes P11, P12, chamfer on/off macros, chip conveyor macros; normalizes certain G28 to G00 X300.

- 220LM.py and "220 test.py"
  - End marker uses G30 U0.
  - Tool codes replaced with G30 W0.
  - Computes rounded X/Z to parameterize a G1901 line after G40 G80 G99 (often with L = rounded_z + 10).
  - Milling blocks (P12) may flip spindle commands to M33/M35; removes G17/G17.1, Y0., and M289; sometimes adjusts max spindle (e.g., G50 S2800 -> G50 S1500).

- 3100xly.py, 400L.py, 700LM.py, 700LY.py, 700XLY.py
  - Introduce G65 P9029 A50. with B1 for first tool and B0 thereafter (first occurrence enforcement across the file).
  - Insert G1901 with derived D/L values and sometimes add M42 (or M43 in 700XLY.py).
  - 700XLY.py additionally injects M24 after each tool change line (T...).

Interactive macro generator
- M_fix.py provides character-to-macro mapping for multiple machines (engraving workflows along X/Y/C axes, face/dia variants).
- Flow:
  1) Select a machine from a printed enumerated list.
  2) Enter text to engrave (supports A–Z, 0–9, some symbols, and localized letters like Æ/Ø/Å).
  3) The script prints machine header, per-character G65 macro lines, and a footer to stdout for copy/paste into a CNC program.

Operational cautions and environment notes
- These scripts are tailored for Windows and expect access to machine program directories like P:\Produksjon\CNCEdit\Programmer\.... Update directory_path variables in each script to match your environment.
- Many changes are regex-based and depend on formatting (e.g., G28 U0. V0. vs G28 U0.). If upstream program formatting differs, the intended normalization may not apply.
- The scripts overwrite fil.md. Keep your input under version control or make backups.

How Warp should operate here
- When asked to run a conversion for a given machine, ensure fil.md contains the program and the script’s directory_path is set correctly, then run the appropriate script and show the diff to the user.
- When asked to generate engraving macro text, run M_fix.py interactively and return the emitted header/body/footer.
- If a user requests parameterization (e.g., pass filename and machine directory as arguments), propose adding argument parsing to the relevant script(s) and implement only upon explicit request.
