"""
Beregning av midtdiameter (pitch diameter) for ISO metriske gjenger
med toleranse per ISO 965-1.

Støttede toleranseklasser:
  Utvendig (bolt): 6g (vanlig), 6h, 5g6g, 4g6g
  Innvendig (mutter): 6H (vanlig), 5H, 4H, 7H
"""

from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Toleranseverdier for midtdiameter (Td2) i µm, per stigning og IT-grad
# Kilde: ISO 965-1, tabell 3 og 4
# ---------------------------------------------------------------------------
_TD2_EXT = {
    4: {0.20:28, 0.25:30, 0.35:34, 0.40:36, 0.45:38, 0.50:40,
        0.70:45, 0.75:48, 0.80:50, 1.00:56, 1.25:63, 1.50:71,
        1.75:80, 2.00:85, 2.50:95, 3.00:106, 3.50:118, 4.00:132,
        4.50:140, 5.00:150},
    5: {0.20:36, 0.25:38, 0.35:42, 0.40:45, 0.45:48, 0.50:50,
        0.70:56, 0.75:60, 0.80:63, 1.00:71, 1.25:80, 1.50:90,
        1.75:100, 2.00:106, 2.50:118, 3.00:132, 3.50:150, 4.00:160,
        4.50:170, 5.00:180},
    6: {0.20:45, 0.25:48, 0.35:53, 0.40:56, 0.45:60, 0.50:63,
        0.70:71, 0.75:75, 0.80:80, 1.00:90, 1.25:100, 1.50:112,
        1.75:125, 2.00:132, 2.50:150, 3.00:170, 3.50:190, 4.00:200,
        4.50:212, 5.00:224},
}

_TD2_INT = {
    4: {0.20:36, 0.25:38, 0.35:42, 0.40:45, 0.45:48, 0.50:50,
        0.70:56, 0.75:60, 0.80:63, 1.00:71, 1.25:80, 1.50:90,
        1.75:100, 2.00:106, 2.50:118, 3.00:132, 3.50:150, 4.00:160,
        4.50:170, 5.00:180},
    5: {0.20:45, 0.25:48, 0.35:53, 0.40:56, 0.45:60, 0.50:63,
        0.70:71, 0.75:75, 0.80:80, 1.00:90, 1.25:100, 1.50:112,
        1.75:125, 2.00:132, 2.50:150, 3.00:170, 3.50:190, 4.00:200,
        4.50:212, 5.00:224},
    6: {0.20:56, 0.25:60, 0.35:67, 0.40:71, 0.45:75, 0.50:80,
        0.70:90, 0.75:95, 0.80:100, 1.00:112, 1.25:125, 1.50:140,
        1.75:160, 2.00:170, 2.50:190, 3.00:212, 3.50:236, 4.00:250,
        4.50:265, 5.00:280},
    7: {0.20:71, 0.25:75, 0.35:85, 0.40:90, 0.45:95, 0.50:100,
        0.70:112, 0.75:118, 0.80:125, 1.00:140, 1.25:160, 1.50:180,
        1.75:200, 2.00:212, 2.50:236, 3.00:265, 3.50:300, 4.00:315,
        4.50:335, 5.00:355},
}

# Grunnavvik (ei) i µm for utvendige toleranser (posisjon)
_EI_EXT = {"6g": -26, "6h": 0, "5g6g": -26, "4g6g": -26}
# IT-grad for midtdiameter, utvendig
_GRADE_EXT = {"6g": 6, "6h": 6, "5g6g": 5, "4g6g": 4}
# IT-grad for midtdiameter, innvendig (H-posisjon => EI = 0)
_GRADE_INT = {"6H": 6, "5H": 5, "4H": 4, "7H": 7}


@dataclass
class ThreadResult:
    """Returverdi fra beregningsfunksjonen."""
    # Nominelle verdier
    d_nom: float          # Nominell ytterdiameter [mm]
    pitch: float          # Stigning p [mm]
    d2_nom: float         # Nominell midtdiameter [mm]
    d1_nom: float         # Nominell kjernediameter [mm]

    # Utvendig gjenge (bolt)
    d2_max: float         # Midtdiameter maks [mm]
    d2_min: float         # Midtdiameter min [mm]
    d2_tol: float         # Toleransefelt [mm]
    ei: float             # Grunnavvik (ei) [mm]

    # Innvendig gjenge (mutter)
    D2_min: float         # Midtdiameter min [mm]
    D2_max: float         # Midtdiameter maks [mm]
    D2_tol: float         # Toleransefelt [mm]
    D1_min: float         # Kjernediameter min (mutter) [mm]

    # Klaering
    spill_min: float      # Minste spill mellom bolt og mutter [mm]
    spill_max: float      # Største spill [mm]

    def __str__(self) -> str:
        return (
            f"\n{'='*56}\n"
            f"  ISO metrisk gjenge  M{self.d_nom} x {self.pitch}\n"
            f"{'='*56}\n"
            f"  Nominell midtdiameter (d₂/D₂):   {self.d2_nom:.3f} mm\n"
            f"  Nominell kjernediameter:           {self.d1_nom:.3f} mm\n"
            f"\n  UTVENDIG GJENGE (bolt)\n"
            f"  {'-'*36}\n"
            f"  Grunnavvik (ei):   {self.ei*1000:+.0f} µm\n"
            f"  Toleransefelt:      {self.d2_tol*1000:.0f} µm\n"
            f"  d₂ maks:           {self.d2_max:.3f} mm\n"
            f"  d₂ min:            {self.d2_min:.3f} mm\n"
            f"\n  INNVENDIG GJENGE (mutter)\n"
            f"  {'-'*36}\n"
            f"  Grunnavvik (EI):   +0 µm\n"
            f"  Toleransefelt:      {self.D2_tol*1000:.0f} µm\n"
            f"  D₂ min:            {self.D2_min:.3f} mm\n"
            f"  D₂ maks:           {self.D2_max:.3f} mm\n"
            f"  D₁ min:            {self.D1_min:.3f} mm\n"
            f"\n  KLAERING (midtdiameter)\n"
            f"  {'-'*36}\n"
            f"  Spill min:          {self.spill_min*1000:.1f} µm\n"
            f"  Spill maks:         {self.spill_max*1000:.1f} µm\n"
            f"{'='*56}\n"
        )


def beregn_midtdiameter(
    d_nom: float,
    pitch: float,
    tol_utv: str = "6g",
    tol_inv: str = "6H",
) -> ThreadResult:
    """
    Beregner midtdiameter med toleranse for ISO metriske gjenger.

    Parametere
    ----------
    d_nom   : Nominell diameter i mm (f.eks. 16 for M16)
    pitch   : Stigning i mm (f.eks. 2.0 for M16 grovgjenge)
    tol_utv : Toleranseklasse utvendig gjenge. Gyldige: '6g', '6h', '5g6g', '4g6g'
    tol_inv : Toleranseklasse innvendig gjenge. Gyldige: '6H', '5H', '4H', '7H'

    Returnerer
    ----------
    ThreadResult med alle beregnede verdier.

    Eksempel
    --------
    >>> res = beregn_midtdiameter(16, 2.0)
    >>> print(res)
    """
    if tol_utv not in _EI_EXT:
        raise ValueError(
            f"Ugyldig utvendig toleranse '{tol_utv}'. "
            f"Gyldige: {list(_EI_EXT)}"
        )
    if tol_inv not in _GRADE_INT:
        raise ValueError(
            f"Ugyldig innvendig toleranse '{tol_inv}'. "
            f"Gyldige: {list(_GRADE_INT)}"
        )

    # Nominelle verdier (ISO 724)
    d2_nom = d_nom - 0.6495 * pitch    # Midtdiameter
    d1_nom = d_nom - 1.2269 * pitch    # Kjernediameter (bolt/mutter)

    # --- Utvendig gjenge ---
    ei = _EI_EXT[tol_utv] / 1000.0    # Grunnavvik i mm
    grade_e = _GRADE_EXT[tol_utv]
    Td2e = _hent_toleranse(pitch, _TD2_EXT, grade_e) / 1000.0

    d2_max = d2_nom + ei               # Øvre avvik (es = ei + Td2)
    d2_min = d2_max - Td2e            # Nedre avvik

    # --- Innvendig gjenge ---
    EI = 0.0                           # H-posisjon: grunnavvik = 0
    grade_i = _GRADE_INT[tol_inv]
    Td2i = _hent_toleranse(pitch, _TD2_INT, grade_i) / 1000.0

    D2_min = d2_nom + EI
    D2_max = D2_min + Td2i
    D1_min = d1_nom                    # Minste kjernediameter (mutter)

    # Klaering (mutter min - bolt maks = minste spill)
    spill_min = D2_min - d2_max
    spill_max = D2_max - d2_min

    return ThreadResult(
        d_nom=d_nom, pitch=pitch,
        d2_nom=round(d2_nom, 6), d1_nom=round(d1_nom, 6),
        d2_max=round(d2_max, 6), d2_min=round(d2_min, 6),
        d2_tol=round(Td2e, 6), ei=round(ei, 6),
        D2_min=round(D2_min, 6), D2_max=round(D2_max, 6),
        D2_tol=round(Td2i, 6), D1_min=round(D1_min, 6),
        spill_min=round(spill_min, 6), spill_max=round(spill_max, 6),
    )


def _hent_toleranse(pitch: float, tabell: dict, grade: int) -> float:
    """Slår opp toleranseverdi; interpolerer lineært ved ukjent stigning."""
    rad = tabell[grade]
    if pitch in rad:
        return rad[pitch]
    # Lineær interpolasjon mellom nærmeste naboer
    piches = sorted(rad.keys())
    for i in range(len(piches) - 1):
        p0, p1 = piches[i], piches[i + 1]
        if p0 < pitch < p1:
            t0, t1 = rad[p0], rad[p1]
            return t0 + (t1 - t0) * (pitch - p0) / (p1 - p0)
    raise ValueError(f"Stigning {pitch} mm er utenfor støttet område.")


# ---------------------------------------------------------------------------
# Eksempelkjøring
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # M16 x 2 med standard toleranse
    res = beregn_midtdiameter(16, 2.0)
    print(res)

    # M10 x 1.5 med fin toleranse
    res2 = beregn_midtdiameter(10, 1.5, tol_utv="5g6g", tol_inv="5H")
    print(res2)

    # Tilgang til enkeltverdi
    print(f"M16 bolt d2 maks: {res.d2_max:.3f} mm")
    print(f"M16 mutter D2 maks: {res.D2_max:.3f} mm")