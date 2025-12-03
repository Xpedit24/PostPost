from __future__ import annotations
import math
from typing import Tuple, Dict, Any


def calculate_metric_thread(
    basic_diameter: float,
    pitch: float,
    tol_internal: Tuple[float, float] = (0.0, 0.0),
    tol_external: Tuple[float, float] = (0.0, 0.0),
) -> Dict[str, Any]:
    """
    Compute basic ISO metric thread geometry for a given basic diameter (mm) and pitch (mm).

    This implements the standard basic profile relationships (ISO 68-1 style):
    - H (fundamental triangle height) = (sqrt(3)/2) * pitch
    - Radial distance from major diameter to pitch diameter = (3/8) * H
    - External basic thread height (radial) = (5/8) * H
    - Internal basic thread height (radial) = (3/4) * H

    Notes
    - The basic pitch diameter (no allowance/tolerance) is the same offset from the
      basic major diameter for both external and internal threads: basic - (3/4) * H.
    - This function does not bake in any tolerance classes (e.g., 6H/6g). If you need a
      pitch diameter range, pass tolerances via `tol_internal` / `tol_external` as
      (plus_on_max, minus_on_min) in mm. If left at default, max = min = basic.

    Parameters
    - basic_diameter: Major diameter (mm). For an external thread, this is the nominal major
      diameter d; for an internal thread, this is the nominal major diameter D.
    - pitch: Thread pitch (mm).
    - tol_internal: Tuple (plus_on_max, minus_on_min) to create PD max/min for the nut.
    - tol_external: Tuple (plus_on_max, minus_on_min) to create PD max/min for the bolt.

    Returns
    - A dictionary containing rounded values (0.001 mm) for both internal and external basic geometry,
      including fundamental triangle height, thread heights, dedendums, and pitch diameters.

    Raises
    - ValueError if inputs are non-positive.
    """
    if pitch <= 0 or basic_diameter <= 0:
        raise ValueError("basic_diameter and pitch must be positive numbers")

    # Fundamental geometry
    H = math.sqrt(3.0) / 2.0 * pitch  # height of fundamental triangle
    radial_major_to_pitch = (3.0 / 8.0) * H  # radial distance major -> pitch

    # Basic pitch diameter (same basic offset for internal/external profiles)
    pd_basic = basic_diameter - 2.0 * radial_major_to_pitch  # = basic - (3/4) * H

    # External basic values (bolt)
    thread_height_external = (5.0 / 8.0) * H
    dedendum_external = (1.0 / 4.0) * H

    # Internal basic values (nut)
    thread_height_internal = (3.0 / 4.0) * H
    dedendum_internal = (3.0 / 8.0) * H

    # Apply optional pitch-diameter tolerances (if provided)
    int_pd_max = pd_basic + tol_internal[0]
    int_pd_min = pd_basic - tol_internal[1]
    ext_pd_max = pd_basic + tol_external[0]
    ext_pd_min = pd_basic - tol_external[1]

    r = lambda x: round(x, 3)  # default output resolution

    return {
        "Basic_diameter": round(basic_diameter, 3),
        "Pitch": round(pitch, 3),
        "Internal_thread": {
            "Height_of_fundamental_triangle": r(H),
            "Thread_Height": r(thread_height_internal),
            "Thread_dedendum": r(dedendum_internal),
            # Basic and range (range == basic if no tolerance supplied)
            "Pitch_diameter_basic": r(pd_basic),
            "Pitch_diameter_max": r(int_pd_max),
            "Pitch_diameter_min": r(int_pd_min),
        },
        "External_thread": {
            "Height_of_fundamental_triangle": r(H),
            "Thread_Height": r(thread_height_external),
            "Thread_dedendum": r(dedendum_external),
            # Basic and range (range == basic if no tolerance supplied)
            "Pitch_diameter_basic": r(pd_basic),
            "Pitch_diameter_max": r(ext_pd_max),
            "Pitch_diameter_min": r(ext_pd_min),
        },
    }


def format_thread_comment_block(
    basic_diameter: float,
    pitch: float,
    *,
    tol_internal: Tuple[float, float] = (0.0, 0.0),
    tol_external: Tuple[float, float] = (0.0, 0.0),
    internal_class: str = "6H6H",
    external_class: str = "6g6g",
    language: str = "no",
) -> str:
    """
    Return a multi-line CNC comment block (G-code style, in parentheses) with thread info
    for operators. Suitable for embedding directly into a program file.

    language:
      - "no": Norwegian labels (default)
      - "en": English labels
    """
    dims = calculate_metric_thread(
        basic_diameter, pitch, tol_internal=tol_internal, tol_external=tol_external
    )

    bd = dims["Basic_diameter"]
    p = dims["Pitch"]
    i_max = dims["Internal_thread"]["Pitch_diameter_max"]
    i_min = dims["Internal_thread"]["Pitch_diameter_min"]
    e_max = dims["External_thread"]["Pitch_diameter_max"]
    e_min = dims["External_thread"]["Pitch_diameter_min"]

    if language.lower() == "no":
        lines = [
            "(GJENGEDATA - METRISK)",
            f"(M{bd} X {p} - {internal_class} | M{bd} X {p} - {external_class})",
            f"(PITCHDIAMETER MAKS: {i_max} | PITCHDIAMETER MAKS: {e_max})",
            f"(PITCHDIAMETER MIN : {i_min} | PITCHDIAMETER MIN : {e_min})",
        ]
    else:
        lines = [
            "(THREAD DATA - METRIC)",
            f"(M{bd} X {p} - {internal_class} | M{bd} X {p} - {external_class})",
            f"(PITCH DIAMETER MAX: {i_max} | PITCH DIAMETER MAX: {e_max})",
            f"(PITCH DIAMETER MIN: {i_min} | PITCH DIAMETER MIN: {e_min})",
        ]

    return "\n".join(lines)


def insert_comment_after_program_header(content: str, comment_block: str) -> str:
    """
    Insert the given multi-line comment block right after the first program header.
    Expects a header of the form:
      %\n
      O#### (...)
    If not found, the comment is inserted at the top.
    """
    lines = content.splitlines()
    if not lines:
        return comment_block + "\n"

    # Try to find a line that starts with 'O' after a leading '%' line.
    insert_idx = 0
    if lines and lines[0].strip() == "%":
        # Look for O-number on second line
        if len(lines) > 1 and lines[1].lstrip().startswith("O"):
            insert_idx = 2  # after the O#### line
        else:
            insert_idx = 1
    else:
        # Look for any O#### line in the first few lines
        for i, ln in enumerate(lines[:10]):
            if ln.lstrip().startswith("O"):
                insert_idx = i + 1
                break

    new_lines = lines[:insert_idx] + [comment_block] + lines[insert_idx:]
    return "\n".join(new_lines)


if __name__ == "__main__":
    # Simple demo
    D = 10.0
    P = 1.5
    dims = calculate_metric_thread(D, P)
    print(dims)

    print()
    print("-- CNC operator comment (NO) --")
    print(format_thread_comment_block(D, P, language="no"))
    print()
    print("-- CNC operator comment (EN) --")
    print(format_thread_comment_block(D, P, language="en"))
