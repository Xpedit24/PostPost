import pandas as pd
import math

# Definerer variabler for dimensjonene og maskinens timepris
ytre_diameter = 1000 # mm
indre_diameter = 39  # mm
høyde = 185           # mm
timepris = 1800  # Kr per time

V_fjernet_mm3 = math.pi * ((ytre_diameter / 2) ** 2 - (indre_diameter / 2) ** 2) * høyde
V_fjernet_cm3 = V_fjernet_mm3 / 1000

# Data for dreieskjær og DataFrame opprettelse
skjaer_data = [
    {"Type": "WNMG", "Kanter": 6, "Pris": 167, "MRR": 276},
    {"Type": "CP-B1208D-M5 4425", "Kanter": 4, "Pris": 271, "MRR": 413},
    {"Type": "CNMG120408-M5 TP1501", "Kanter": 4, "Pris": 143, "MRR": 398.4},
]
skjaer_df = pd.DataFrame(skjaer_data)

# Beregninger i DataFrame
skjaer_df['Pris_per_kant'] = skjaer_df['Pris'] / skjaer_df['Kanter']
skjaer_df['Kostnad_per_MRR'] = skjaer_df['Pris'] / skjaer_df['MRR']
skjaer_df['Estimert_tid_min'] = V_fjernet_cm3 / skjaer_df['MRR']
skjaer_df['Kostnad_for_fjerning'] = skjaer_df['Pris'] 

# Beregner kostnaden for maskintid
skjaer_df['Kostnad_maskintid'] = (skjaer_df['Estimert_tid_min'] / 60) * timepris

# Total kostnad for å fjerne materialet
skjaer_df['Total_kostnad'] = skjaer_df['Kostnad_for_fjerning'] + skjaer_df['Kostnad_maskintid']

# Identifiserer og printer det mest økonomiske skjæret
minste_kostnad_index = skjaer_df['Total_kostnad'].idxmin()
minste_kostnad_skjaer = skjaer_df.iloc[minste_kostnad_index]

print(f"Volum fjernet (cm^3): {V_fjernet_cm3:.2f}")
print(skjaer_df[['Type', 'Total_kostnad', 'Kostnad_for_fjerning', 'Kostnad_maskintid']])
print("\nMest kostnadseffektive skjær:")
print(minste_kostnad_skjaer)
