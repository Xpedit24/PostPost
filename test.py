"""
Generator for Fanuc-makrokoder til skriftgravering (Doosan fres / Puma dreiebenk).

Refaktorert versjon: tegnkodene for hver maskin/akse bygges automatisk fra
programnummeret (P65xx), i stedet for å skrives ut manuelt for hvert
av de 44 tegnene for hver av de ni maskinkonfigurasjonene.
"""

# Rekkefølgen på tegnene tilsvarer A-verdiene 0-43 i "G65P....A<n>."
# (mellomrom = 0, A-Z = 1-26, Ø Æ Å = 27-29, - / ( ) = 30-33, 0-9 = 34-43)
TEGN_REKKEFOLGE = " ABCDEFGHIJKLMNOPQRSTUVWXYZØÆÅ-/()0123456789"


def doosan_teller(prog):
    """Tellerblokk for '#' (Doosan-stil: egne #600/#601/#602-tellere)."""
    return f"""
G65P{prog}A100.(TELLING X00) 
G65P{prog}A101.(TELLING 0X0) 
G65P{prog}A102.(TELLING 00X) 
(UPDATE AND TEST COUNTERS) 
#602=#602+1
IF[#602LT10.]GOTO100 
#602=0 
#601=#601+1
IF[#601LT10.]GOTO100 
#601=0 
#600=#600+1
IF[#600LT10.]GOTO100 
#600=0 
N100 """


def puma_teller(prog):
    """Tellerblokk for '#' (Puma-stil: leser dagens tellerverdi fra #3901)."""
    return f"""
(UPDATE AND TEST COUNTERS) 
#149 = #3901
#520 = FIX[#149 / 100]
#521 = FIX[[#149 MOD 100] / 10]
#522 = [#149 MOD 10]

G65P{prog}A100.(TELLING X00) 
G65P{prog}A101.(TELLING 0X0) 
G65P{prog}A102.(TELLING 00X) 
N100  """


def generer_tegnkoder(prog, teller_funksjon):
    """Bygger ordboken {tegn: G65-kode} for et gitt programnummer."""
    koder = {}
    for i, tegn in enumerate(TEGN_REKKEFOLGE):
        visningsnavn = "MELLOMROM" if tegn == " " else tegn
        koder[tegn] = f"G65P{prog}A{i}.({visningsnavn})"
    koder["#"] = teller_funksjon(prog)
    return koder


# ---------------------------------------------------------------------------
# Header / footer
# ---------------------------------------------------------------------------

BASIS_HEADER = """(A = CODE FOR NUMMMER ELLER BOKSTAV )
(OPS 0 STARTER PÅ 34 )
(SAA 1 STARTER PÅ 35, SAA FØLGER TRENDEN TIL 9 SOM ER 43)"""

BASIS_VARIABLER = """#100 = 0.1 ( DYBDE FOR ENGRAVERING ) 
#101 = 150. ( MATING I Z )
#102 = 150. ( MATING X OG Y ) 
#103 = 1. ( STOPP OVER NEXT LETTER )
#104 = 5. ( SKALERING)
#105 = 0.5 ( KLARING I Z)"""

PUMA_VARIABLER = """#106 = 1. (MELLOMROM MELLOM BOKSTAVER) 
#107 = 2.5 (MELLOMROM MELLOM ORD) """


def bygg_header(ekstra_linje="", puma=False):
    deler = [BASIS_HEADER]
    if ekstra_linje:
        deler.append(ekstra_linje)
    deler.append(BASIS_VARIABLER)
    if puma:
        deler.append(PUMA_VARIABLER)
    return "\n\n".join(deler)


# ---------------------------------------------------------------------------
# Maskinkonfigurasjoner
# ---------------------------------------------------------------------------

MASKINER = [
    {
        "navn": "DOOSAN fres | X-akse",
        "prog": 6500,
        "teller": doosan_teller,
        "ekstra_header": "G65P6502A102.B0.02C15.D40.E1.F5.H0.5(TELLING 00X) ",
        "puma": False,
        "footer": "G00Z2.",
    },
    {
        "navn": "DOOSAN fres | Y-akse",
        "prog": 6501,
        "teller": doosan_teller,
        "ekstra_header": "",
        "puma": False,
        "footer": "G00Z2.",
    },
    {
        "navn": "PUMA | skriver langs Y med Y-akse (variant 1, G00Z2)",
        "prog": 6500,
        "teller": puma_teller,
        "ekstra_header": "",
        "puma": True,
        "footer": "G00Z2.",
    },
    {
        "navn": "PUMA | skriver langs X med Y-akse",
        "prog": 6501,
        "teller": puma_teller,
        "ekstra_header": "",
        "puma": True,
        "footer": "G00Z2.",
    },
    {
        "navn": "PUMA | skriver langs C med Y-akse",
        "prog": 6502,
        "teller": puma_teller,
        "ekstra_header": "",
        "puma": True,
        "footer": "G00Z2.",
    },
    {
        "navn": "PUMA | skriver langs C med C-akse på face",
        "prog": 6505,
        "teller": puma_teller,
        "ekstra_header": "",
        "puma": True,
        "footer": "G00Z2.",
    },
    {
        "navn": "PUMA | skriver langs C med C-akse på dia",
        "prog": 6506,
        "teller": puma_teller,
        "ekstra_header": "",
        "puma": True,
        "footer": "G00U2.",
    },
    {
        "navn": "PUMA | skriver langs Y med Y-akse (variant 2, G00U2)",
        "prog": 6507,
        "teller": puma_teller,
        "ekstra_header": "",
        "puma": True,
        "footer": "G00U2.",
    },
    {
        "navn": "PUMA | skriver langs Z med C-akse på dia",
        "prog": 6508,
        "teller": puma_teller,
        "ekstra_header": "",
        "puma": True,
        "footer": "G00U2.",
    },
]


# ---------------------------------------------------------------------------
# Programflyt
# ---------------------------------------------------------------------------

def velg_maskin():
    print("Liste over maskiner:")
    for idx, m in enumerate(MASKINER, start=1):
        print(f"{idx}. {m['navn']}")

    while True:
        valg = input("\nVelg en maskin (skriv inn nummeret): ").strip()
        if valg.isdigit() and 1 <= int(valg) <= len(MASKINER):
            return MASKINER[int(valg) - 1]
        print(f"Ugyldig valg. Skriv et tall mellom 1 og {len(MASKINER)}.")


def generer_output(tekst, tegnkoder):
    """Returnerer (liste med kodelinjer, sett med ukjente tegn)."""
    linjer = []
    ukjente = set()
    for bokstav in tekst:
        kode = tegnkoder.get(bokstav.upper())
        if kode is not None:
            linjer.append(kode)
        else:
            ukjente.add(bokstav)
    return linjer, ukjente


def main():
    maskin = velg_maskin()
    tegnkoder = generer_tegnkoder(maskin["prog"], maskin["teller"])
    header = bygg_header(maskin["ekstra_header"], maskin["puma"])
    footer = maskin["footer"]

    tekst = input("\nTekst (telling er # f.eks. 123-#): ")
    linjer, ukjente = generer_output(tekst, tegnkoder)

    if ukjente:
        ukjent_liste = ", ".join(repr(t) for t in sorted(ukjente))
        print(f"\n(Advarsel: følgende tegn finnes ikke i kodetabellen og ble hoppet over: {ukjent_liste})")

    resultat = "\n\n".join([header, *linjer, footer])

    print("\n" + resultat)

    try:
        import pyperclip
        # Sikre Windows-stil linjeskift (\r\n) slik at innliming i andre
        # programmer (f.eks. CNC-kontroller) bevarer linjeskiftene.
        resultat_for_utklipp = resultat.replace("\r\n", "\n").replace("\n", "\r\n")
        pyperclip.copy(resultat_for_utklipp)
        print("\n(Resultatet er kopiert til utklippstavlen - bruk Ctrl+V / høyreklikk-lim inn for å sette det inn.)")
    except ImportError:
        print("\n(Kunne ikke kopiere automatisk - pakken 'pyperclip' er ikke installert.")
        print(" Installer med: pip install pyperclip")
        print(" Merk teksten over manuelt og kopier med musen i stedet.)")


if __name__ == "__main__":
    main()