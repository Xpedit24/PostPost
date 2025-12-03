import os

# Definere oppslagsordbøker for hver maskin
fanuc_makroer = {
    "DOOSAN fres | x akse": {
     " ": "G65P6500A0.(MELLOMROM)",
    "A": "G65P6500A1.(A)",
    "B": "G65P6500A2.(B)",
    "C": "G65P6500A3.(C)",
    "D": "G65P6500A4.(D)",
    "E": "G65P6500A5.(E)",
    "F": "G65P6500A6.(F)",
    "G": "G65P6500A7.(G)",
    "H": "G65P6500A8.(H)",
    "I": "G65P6500A9.(I)",
    "J": "G65P6500A10.(J)",
    "K": "G65P6500A11.(K)",
    "L": "G65P6500A12.(L)",
    "M": "G65P6500A13.(M)",
    "N": "G65P6500A14.(N)",
    "O": "G65P6500A15.(O)",
    "P": "G65P6500A16.(P)",
    "Q": "G65P6500A17.(Q)",
    "R": "G65P6500A18.(R)",
    "S": "G65P6500A19.(S)",
    "T": "G65P6500A20.(T)",
    "U": "G65P6500A21.(U)",
    "V": "G65P6500A22.(V)",
    "W": "G65P6500A23.(W)",
    "X": "G65P6500A24.(X)",
    "Y": "G65P6500A25.(Y)",
    "Z": "G65P6500A26.(Z)",
    "Ø": "G65P6500A27.(Ø)",
    "Æ": "G65P6500A28.(Æ)",
    "Å": "G65P6500A29.(Å)",
    "-": "G65P6500A30.(-)",
    "/": "G65P6500A31.(/)",
    "(": "G65P6500A32.(()",
    ")": "G65P6500A33.())",
    "0": "G65P6500A34.(0)",
    "1": "G65P6500A35.(1)",
    "2": "G65P6500A36.(2)",
    "3": "G65P6500A37.(3)",
    "4": "G65P6500A38.(4)",
    "5": "G65P6500A39.(5)",
    "6": "G65P6500A40.(6)",
    "7": "G65P6500A41.(7)",
    "8": "G65P6500A42.(8)",
    "9": "G65P6500A43.(9)",
    "#": """
G65P6500A100.(TELLING X00) 
G65P6500A101.(TELLING 0X0) 
G65P6500A102.(TELLING 00X) 
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
N100 """,
},
    "DOOSAN fres | y akse": {
     " ": "G65P6501A0.(MELLOMROM)",
    "A": "G65P6501A1.(A)",
    "B": "G65P6501A2.(B)",
    "C": "G65P6501A3.(C)",
    "D": "G65P6501A4.(D)",
    "E": "G65P6501A5.(E)",
    "F": "G65P6501A6.(F)",
    "G": "G65P6501A7.(G)",
    "H": "G65P6501A8.(H)",
    "I": "G65P6501A9.(I)",
    "J": "G65P6501A10.(J)",
    "K": "G65P6501A11.(K)",
    "L": "G65P6501A12.(L)",
    "M": "G65P6501A13.(M)",
    "N": "G65P6501A14.(N)",
    "O": "G65P6501A15.(O)",
    "P": "G65P6501A16.(P)",
    "Q": "G65P6501A17.(Q)",
    "R": "G65P6501A18.(R)",
    "S": "G65P6501A19.(S)",
    "T": "G65P6501A20.(T)",
    "U": "G65P6501A21.(U)",
    "V": "G65P6501A22.(V)",
    "W": "G65P6501A23.(W)",
    "X": "G65P6501A24.(X)",
    "Y": "G65P6501A25.(Y)",
    "Z": "G65P6501A26.(Z)",
    "Ø": "G65P6501A27.(Ø)",
    "Æ": "G65P6501A28.(Æ)",
    "Å": "G65P6501A29.(Å)",
    "-": "G65P6501A30.(-)",
    "/": "G65P6501A31.(/)",
    "(": "G65P6501A32.(()",
    ")": "G65P6501A33.())",
    "0": "G65P6501A34.(0)",
    "1": "G65P6501A35.(1)",
    "2": "G65P6501A36.(2)",
    "3": "G65P6501A37.(3)",
    "4": "G65P6501A38.(4)",
    "5": "G65P6501A39.(5)",
    "6": "G65P6501A40.(6)",
    "7": "G65P6501A41.(7)",
    "8": "G65P6501A42.(8)",
    "9": "G65P6501A43.(9)",
    "#": """
G65P6501A100.(TELLING X00) 
G65P6501A101.(TELLING 0X0) 
G65P6501A102.(TELLING 00X) 
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
N100 """,
    },
    "PUMA  | skriver langs y  med y akse": {
     " ": "G65P6500A0.(MELLOMROM)",
    "A": "G65P6500A1.(A)",
    "B": "G65P6500A2.(B)",
    "C": "G65P6500A3.(C)",
    "D": "G65P6500A4.(D)",
    "E": "G65P6500A5.(E)",
    "F": "G65P6500A6.(F)",
    "G": "G65P6500A7.(G)",
    "H": "G65P6500A8.(H)",
    "I": "G65P6500A9.(I)",
    "J": "G65P6500A10.(J)",
    "K": "G65P6500A11.(K)",
    "L": "G65P6500A12.(L)",
    "M": "G65P6500A13.(M)",
    "N": "G65P6500A14.(N)",
    "O": "G65P6500A15.(O)",
    "P": "G65P6500A16.(P)",
    "Q": "G65P6500A17.(Q)",
    "R": "G65P6500A18.(R)",
    "S": "G65P6500A19.(S)",
    "T": "G65P6500A20.(T)",
    "U": "G65P6500A21.(U)",
    "V": "G65P6500A22.(V)",
    "W": "G65P6500A23.(W)",
    "X": "G65P6500A24.(X)",
    "Y": "G65P6500A25.(Y)",
    "Z": "G65P6500A26.(Z)",
    "Ø": "G65P6500A27.(Ø)",
    "Æ": "G65P6500A28.(Æ)",
    "Å": "G65P6500A29.(Å)",
    "-": "G65P6500A30.(-)",
    "/": "G65P6500A31.(/)",
    "(": "G65P6500A32.(()",
    ")": "G65P6500A33.())",
    "0": "G65P6500A34.(0)",
    "1": "G65P6500A35.(1)",
    "2": "G65P6500A36.(2)",
    "3": "G65P6500A37.(3)",
    "4": "G65P6500A38.(4)",
    "5": "G65P6500A39.(5)",
    "6": "G65P6500A40.(6)",
    "7": "G65P6500A41.(7)",
    "8": "G65P6500A42.(8)",
    "9": "G65P6500A43.(9)",
    "#": """
(UPDATE AND TEST COUNTERS) 
#149 = #3901
#520 = FIX[#149 / 100]
#521 = FIX[[#149 MOD 100] / 10]
#522 = [#149 MOD 10]
    
G65P6500A100.(TELLING X00) 
G65P6500A101.(TELLING 0X0) 
G65P6500A102.(TELLING 00X) 
N100  """
    },
    "PUMA  | skriver langs x med y akse": {
     " ": "G65P6501A0.(MELLOMROM)",
    "A": "G65P6501A1.(A)",
    "B": "G65P6501A2.(B)",
    "C": "G65P6501A3.(C)",
    "D": "G65P6501A4.(D)",
    "E": "G65P6501A5.(E)",
    "F": "G65P6501A6.(F)",
    "G": "G65P6501A7.(G)",
    "H": "G65P6501A8.(H)",
    "I": "G65P6501A9.(I)",
    "J": "G65P6501A10.(J)",
    "K": "G65P6501A11.(K)",
    "L": "G65P6501A12.(L)",
    "M": "G65P6501A13.(M)",
    "N": "G65P6501A14.(N)",
    "O": "G65P6501A15.(O)",
    "P": "G65P6501A16.(P)",
    "Q": "G65P6501A17.(Q)",
    "R": "G65P6501A18.(R)",
    "S": "G65P6501A19.(S)",
    "T": "G65P6501A20.(T)",
    "U": "G65P6501A21.(U)",
    "V": "G65P6501A22.(V)",
    "W": "G65P6501A23.(W)",
    "X": "G65P6501A24.(X)",
    "Y": "G65P6501A25.(Y)",
    "Z": "G65P6501A26.(Z)",
    "Ø": "G65P6501A27.(Ø)",
    "Æ": "G65P6501A28.(Æ)",
    "Å": "G65P6501A29.(Å)",
    "-": "G65P6501A30.(-)",
    "/": "G65P6501A31.(/)",
    "(": "G65P6501A32.(()",
    ")": "G65P6501A33.())",
    "0": "G65P6501A34.(0)",    
    "1": "G65P6501A35.(1)",
    "2": "G65P6501A36.(2)",
    "3": "G65P6501A37.(3)",
    "4": "G65P6501A38.(4)",
    "5": "G65P6501A39.(5)",
    "6": "G65P6501A40.(6)",
    "7": "G65P6501A41.(7)",
    "8": "G65P6501A42.(8)",
    "9": "G65P6501A43.(9)",
    "#": """
(UPDATE AND TEST COUNTERS) 
#149 = #3901
#520 = FIX[#149 / 100]
#521 = FIX[[#149 MOD 100] / 10]
#522 = [#149 MOD 10]
    
G65P6501A100.(TELLING X00) 
G65P6501A101.(TELLING 0X0) 
G65P6501A102.(TELLING 00X) 
N100  """
        },
    "PUMA  | skriver langs c  med y akse": {
     " ": "G65P6502A0.(MELLOMROM)",
    "A": "G65P6502A1.(A)",
    "B": "G65P6502A2.(B)",
    "C": "G65P6502A3.(C)",
    "D": "G65P6502A4.(D)",
    "E": "G65P6502A5.(E)",
    "F": "G65P6502A6.(F)",
    "G": "G65P6502A7.(G)",
    "H": "G65P6502A8.(H)",
    "I": "G65P6502A9.(I)",
    "J": "G65P6502A10.(J)",
    "K": "G65P6502A11.(K)",
    "L": "G65P6502A12.(L)",
    "M": "G65P6502A13.(M)",
    "N": "G65P6502A14.(N)",
    "O": "G65P6502A15.(O)",
    "P": "G65P6502A16.(P)",
    "Q": "G65P6502A17.(Q)",
    "R": "G65P6502A18.(R)",
    "S": "G65P6502A19.(S)",
    "T": "G65P6502A20.(T)",
    "U": "G65P6502A21.(U)",
    "V": "G65P6502A22.(V)",
    "W": "G65P6502A23.(W)",
    "X": "G65P6502A24.(X)",
    "Y": "G65P6502A25.(Y)",
    "Z": "G65P6502A26.(Z)",
    "Ø": "G65P6502A27.(Ø)",
    "Æ": "G65P6502A28.(Æ)",
    "Å": "G65P6502A29.(Å)",
    "-": "G65P6502A30.(-)",
    "/": "G65P6502A31.(/)",
    "(": "G65P6502A32.(()",
    ")": "G65P6502A33.())",
    "0": "G65P6502A34.(0)",    
    "1": "G65P6502A35.(1)",
    "2": "G65P6502A36.(2)",
    "3": "G65P6502A37.(3)",
    "4": "G65P6502A38.(4)",
    "5": "G65P6502A39.(5)",
    "6": "G65P6502A40.(6)",
    "7": "G65P6502A41.(7)",
    "8": "G65P6502A42.(8)",
    "9": "G65P6502A43.(9)",
    "#": """
(UPDATE AND TEST COUNTERS) 
#149 = #3901
#520 = FIX[#149 / 100]
#521 = FIX[[#149 MOD 100] / 10]
#522 = [#149 MOD 10]
    
G65P6502A100.(TELLING X00) 
G65P6502A101.(TELLING 0X0) 
G65P6502A102.(TELLING 00X) 
N100  """
      },
    "PUMA  | skriver langs c med c akse på face": {
     " ": "G65P6505A0.(MELLOMROM)",
    "A": "G65P6505A1.(A)",
    "B": "G65P6505A2.(B)",
    "C": "G65P6505A3.(C)",
    "D": "G65P6505A4.(D)",
    "E": "G65P6505A5.(E)",
    "F": "G65P6505A6.(F)",
    "G": "G65P6505A7.(G)",
    "H": "G65P6505A8.(H)",
    "I": "G65P6505A9.(I)",
    "J": "G65P6505A10.(J)",
    "K": "G65P6505A11.(K)",
    "L": "G65P6505A12.(L)",
    "M": "G65P6505A13.(M)",
    "N": "G65P6505A14.(N)",
    "O": "G65P6505A15.(O)",
    "P": "G65P6505A16.(P)",
    "Q": "G65P6505A17.(Q)",
    "R": "G65P6505A18.(R)",
    "S": "G65P6505A19.(S)",
    "T": "G65P6505A20.(T)",
    "U": "G65P6505A21.(U)",
    "V": "G65P6505A22.(V)",
    "W": "G65P6505A23.(W)",
    "X": "G65P6505A24.(X)",
    "Y": "G65P6505A25.(Y)",
    "Z": "G65P6505A26.(Z)",
    "Ø": "G65P6505A27.(Ø)",
    "Æ": "G65P6505A28.(Æ)",
    "Å": "G65P6505A29.(Å)",
    "-": "G65P6505A30.(-)",
    "/": "G65P6505A31.(/)",
    "(": "G65P6505A32.(()",
    ")": "G65P6505A33.())",
    "0": "G65P6505A34.(0)",    
    "1": "G65P6505A35.(1)",
    "2": "G65P6505A36.(2)",
    "3": "G65P6505A37.(3)",
    "4": "G65P6505A38.(4)",
    "5": "G65P6505A39.(5)",
    "6": "G65P6505A40.(6)",
    "7": "G65P6505A41.(7)",
    "8": "G65P6505A42.(8)",
    "9": "G65P6505A43.(9)",
    "#": """
(UPDATE AND TEST COUNTERS) 
#149 = #3901
#520 = FIX[#149 / 100]
#521 = FIX[[#149 MOD 100] / 10]
#522 = [#149 MOD 10]

G65P6505A100.(TELLING X00) 
G65P6505A101.(TELLING 0X0) 
G65P6505A102.(TELLING 00X) 
N100  """
      },
    "PUMA  | skriver langs c med c akse på dia": {
     " ": "G65P6506A0.(MELLOMROM)",
    "A": "G65P6506A1.(A)",
    "B": "G65P6506A2.(B)",
    "C": "G65P6506A3.(C)",
    "D": "G65P6506A4.(D)",
    "E": "G65P6506A5.(E)",
    "F": "G65P6506A6.(F)",
    "G": "G65P6506A7.(G)",
    "H": "G65P6506A8.(H)",
    "I": "G65P6506A9.(I)",
    "J": "G65P6506A10.(J)",
    "K": "G65P6506A11.(K)",
    "L": "G65P6506A12.(L)",
    "M": "G65P6506A13.(M)",
    "N": "G65P6506A14.(N)",
    "O": "G65P6506A15.(O)",
    "P": "G65P6506A16.(P)",
    "Q": "G65P6506A17.(Q)",
    "R": "G65P6506A18.(R)",
    "S": "G65P6506A19.(S)",
    "T": "G65P6506A20.(T)",
    "U": "G65P6506A21.(U)",
    "V": "G65P6506A22.(V)",
    "W": "G65P6506A23.(W)",
    "X": "G65P6506A24.(X)",
    "Y": "G65P6506A25.(Y)",
    "Z": "G65P6506A26.(Z)",
    "Ø": "G65P6506A27.(Ø)",
    "Æ": "G65P6506A28.(Æ)",
    "Å": "G65P6506A29.(Å)",
    "-": "G65P6506A30.(-)",
    "/": "G65P6506A31.(/)",
    "(": "G65P6506A32.(()",
    ")": "G65P6506A33.())",
    "0": "G65P6506A34.(0)",    
    "1": "G65P6506A35.(1)",
    "2": "G65P6506A36.(2)",
    "3": "G65P6506A37.(3)",
    "4": "G65P6506A38.(4)",
    "5": "G65P6506A39.(5)",
    "6": "G65P6506A40.(6)",
    "7": "G65P6506A41.(7)",
    "8": "G65P6506A42.(8)",
    "9": "G65P6506A43.(9)",
    "#": """
(UPDATE AND TEST COUNTERS) 
#149 = #3901
#520 = FIX[#149 / 100]
#521 = FIX[[#149 MOD 100] / 10]
#522 = [#149 MOD 10]

G65P6506A100.(TELLING X00) 
G65P6506A101.(TELLING 0X0) 
G65P6506A102.(TELLING 00X) 
N100  """
      },
    "PUMA  | skriver langs y med y akse ": {
     " ": "G65P6507A0.(MELLOMROM)",
    "A": "G65P6507A1.(A)",
    "B": "G65P6507A2.(B)",
    "C": "G65P6507A3.(C)",
    "D": "G65P6507A4.(D)",
    "E": "G65P6507A5.(E)",
    "F": "G65P6507A6.(F)",
    "G": "G65P6507A7.(G)",
    "H": "G65P6507A8.(H)",
    "I": "G65P6507A9.(I)",
    "J": "G65P6507A10.(J)",
    "K": "G65P6507A11.(K)",
    "L": "G65P6507A12.(L)",
    "M": "G65P6507A13.(M)",
    "N": "G65P6507A14.(N)",
    "O": "G65P6507A15.(O)",
    "P": "G65P6507A16.(P)",
    "Q": "G65P6507A17.(Q)",
    "R": "G65P6507A18.(R)",
    "S": "G65P6507A19.(S)",
    "T": "G65P6507A20.(T)",
    "U": "G65P6507A21.(U)",
    "V": "G65P6507A22.(V)",
    "W": "G65P6507A23.(W)",
    "X": "G65P6507A24.(X)",
    "Y": "G65P6507A25.(Y)",
    "Z": "G65P6507A26.(Z)",
    "Ø": "G65P6507A27.(Ø)",
    "Æ": "G65P6507A28.(Æ)",
    "Å": "G65P6507A29.(Å)",
    "-": "G65P6507A30.(-)",
    "/": "G65P6507A31.(/)",
    "(": "G65P6507A32.(()",
    ")": "G65P6507A33.())",
    "0": "G65P6507A34.(0)",    
    "1": "G65P6507A35.(1)",
    "2": "G65P6507A36.(2)",
    "3": "G65P6507A37.(3)",
    "4": "G65P6507A38.(4)",
    "5": "G65P6507A39.(5)",
    "6": "G65P6507A40.(6)",
    "7": "G65P6507A41.(7)",
    "8": "G65P6507A42.(8)",
    "9": "G65P6507A43.(9)",
    "#": """
(UPDATE AND TEST COUNTERS) 
#149 = #3901
#520 = FIX[#149 / 100]
#521 = FIX[[#149 MOD 100] / 10]
#522 = [#149 MOD 10]

G65P6507A100.(TELLING X00) 
G65P6507A101.(TELLING 0X0) 
G65P6507A102.(TELLING 00X) 
N100  """
      },
    "PUMA  | skriver langs z med c akse på dia" : {
     " ": "G65P6508A0.(MELLOMROM)",
    "A": "G65P6508A1.(A)",
    "B": "G65P6508A2.(B)",
    "C": "G65P6508A3.(C)",
    "D": "G65P6508A4.(D)",
    "E": "G65P6508A5.(E)",
    "F": "G65P6508A6.(F)",
    "G": "G65P6508A7.(G)",
    "H": "G65P6508A8.(H)",
    "I": "G65P6508A9.(I)",
    "J": "G65P6508A10.(J)",
    "K": "G65P6508A11.(K)",
    "L": "G65P6508A12.(L)",
    "M": "G65P6508A13.(M)",
    "N": "G65P6508A14.(N)",
    "O": "G65P6508A15.(O)",
    "P": "G65P6508A16.(P)",
    "Q": "G65P6508A17.(Q)",
    "R": "G65P6508A18.(R)",
    "S": "G65P6508A19.(S)",
    "T": "G65P6508A20.(T)",
    "U": "G65P6508A21.(U)",
    "V": "G65P6508A22.(V)",
    "W": "G65P6508A23.(W)",
    "X": "G65P6508A24.(X)",
    "Y": "G65P6508A25.(Y)",
    "Z": "G65P6508A26.(Z)",
    "Ø": "G65P6508A27.(Ø)",
    "Æ": "G65P6508A28.(Æ)",
    "Å": "G65P6508A29.(Å)",
    "-": "G65P6508A30.(-)",
    "/": "G65P6508A31.(/)",
    "(": "G65P6508A32.(()",
    ")": "G65P6508A33.())",
    "0": "G65P6508A34.(0)",    
    "1": "G65P6508A35.(1)",
    "2": "G65P6508A36.(2)",
    "3": "G65P6508A37.(3)",
    "4": "G65P6508A38.(4)",
    "5": "G65P6508A39.(5)",
    "6": "G65P6508A40.(6)",
    "7": "G65P6508A41.(7)",
    "8": "G65P6508A42.(8)",
    "9": "G65P6508A43.(9)",
    "#": """
(UPDATE AND TEST COUNTERS) 
#149 = #3901
#520 = FIX[#149 / 100]
#521 = FIX[[#149 MOD 100] / 10]
#522 = [#149 MOD 10]

G65P6508A100.(TELLING X00) 
G65P6508A101.(TELLING 0X0) 
G65P6508A102.(TELLING 00X) 
N100  """
      }
}

# Definere en liste med navn (og maskiner)
navn_liste = ["DOOSAN fres | x akse", 
              "DOOSAN fres | y akse",
              "PUMA  | skriver langs y  med y akse", 
              "PUMA  | skriver langs x med y akse", 
              "PUMA  | skriver langs c  med y akse",
              "PUMA  | skriver langs c med c akse på face",
              "PUMA  | skriver langs c med c akse på dia",
              "PUMA  | skriver langs y med y akse ",
              "PUMA  | skriver langs z med c akse på dia",
              ]

# Definere en ordbok med headere og bunner for hver maskin
maskin_headere_bunner = {
    "DOOSAN fres | x akse": {
        "header": """
(A = CODE FOR NUMMMER ELLER BOKSTAV )
(OPS 0 STARTER PÅ 34 )
(SAA 1 STARTER PÅ 35, SAA FØLGER TRENDEN TIL 9 SOM ER 43)

G65P6502A102.B0.02C15.D40.E1.F5.H0.5(TELLING 00X) 

#100 = 0.1 ( DYBDE FOR ENGRAVERING ) 
#101 = 150. ( MATING I Z )
#102 = 150. ( MATING X OG Y ) 
#103 = 1. ( STOPP OVER NEXT LETTER )
#104 = 5. ( SKALERING)
#105 = 0.5 ( KLARING I Z)
""",

        "footer": """
G00Z2.
"""
    },
    "DOOSAN fres | y akse": {
        "header": 
    """
(A = CODE FOR NUMMMER ELLER BOKSTAV )
(OPS 0 STARTER PÅ 34 )
(SAA 1 STARTER PÅ 35, SAA FØLGER TRENDEN TIL 9 SOM ER 43)

#100 = 0.1 ( DYBDE FOR ENGRAVERING ) 
#101 = 150. ( MATING I Z )
#102 = 150. ( MATING X OG Y ) 
#103 = 1. ( STOPP OVER NEXT LETTER )
#104 = 5. ( SKALERING)
#105 = 0.5 ( KLARING I Z)
""",

        "footer": """
G00Z2.
"""
    },
    "PUMA  | skriver langs y  med y akse": {
        "header":"""
(A = CODE FOR NUMMMER ELLER BOKSTAV )
(OPS 0 STARTER PÅ 34 )
(SAA 1 STARTER PÅ 35, SAA FØLGER TRENDEN TIL 9 SOM ER 43)

#100 = 0.1 ( DYBDE FOR ENGRAVERING ) 
#101 = 150. ( MATING I Z )
#102 = 150. ( MATING X OG Y ) 
#103 = 1. ( STOPP OVER NEXT LETTER )
#104 = 5. ( SKALERING)
#105 = 0.5 ( KLARING I Z)
#106 = 1. (MELLOMROM MELLOM BOKSTAVER) 
#107 = 2.5 (MELLOMROM MELLOM ORD) 
""",

        "footer": """
G00Z2.
"""
    },
    "PUMA  | skriver langs x med y akse": {
        "header":    """
(A = CODE FOR NUMMMER ELLER BOKSTAV )
(OPS 0 STARTER PÅ 34 )
(SAA 1 STARTER PÅ 35, SAA FØLGER TRENDEN TIL 9 SOM ER 43)

#100 = 0.1 ( DYBDE FOR ENGRAVERING ) 
#101 = 150. ( MATING I Z )
#102 = 150. ( MATING X OG Y ) 
#103 = 1. ( STOPP OVER NEXT LETTER )
#104 = 5. ( SKALERING)
#105 = 0.5 ( KLARING I Z)
#106 = 1. (MELLOMROM MELLOM BOKSTAVER) 
#107 = 2.5 (MELLOMROM MELLOM ORD) 
""",

        "footer": """
G00Z2.
"""
    },
    "PUMA  | skriver langs c  med y akse": {
        "header":"""
(A = CODE FOR NUMMMER ELLER BOKSTAV )
(OPS 0 STARTER PÅ 34 )
(SAA 1 STARTER PÅ 35, SAA FØLGER TRENDEN TIL 9 SOM ER 43)

#100 = 0.1 ( DYBDE FOR ENGRAVERING ) 
#101 = 150. ( MATING I Z )
#102 = 150. ( MATING X OG Y ) 
#103 = 1. ( STOPP OVER NEXT LETTER )
#104 = 5. ( SKALERING)
#105 = 0.5 ( KLARING I Z)
#106 = 1. (MELLOMROM MELLOM BOKSTAVER) 
#107 = 2.5 (MELLOMROM MELLOM ORD) 
""",

        "footer": """
G00Z2. 
"""
    },
    "PUMA  | skriver langs c med c akse på face": {
        "header":"""
(A = CODE FOR NUMMMER ELLER BOKSTAV )
(OPS 0 STARTER PÅ 34 )
(SAA 1 STARTER PÅ 35, SAA FØLGER TRENDEN TIL 9 SOM ER 43)

#100 = 0.1 ( DYBDE FOR ENGRAVERING ) 
#101 = 150. ( MATING I Z )
#102 = 150. ( MATING X OG Y ) 
#103 = 1. ( STOPP OVER NEXT LETTER )
#104 = 5. ( SKALERING)
#105 = 0.5 ( KLARING I Z)
#106 = 1. (MELLOMROM MELLOM BOKSTAVER) 
#107 = 2.5(MELLOMROM MELLOM ORD) 
""",

        "footer": """
G00Z2. 
"""
    },
    "PUMA  | skriver langs c med c akse på dia": {
        "header":"""
(A = CODE FOR NUMMMER ELLER BOKSTAV )
(OPS 0 STARTER PÅ 34 )
(SAA 1 STARTER PÅ 35, SAA FØLGER TRENDEN TIL 9 SOM ER 43)

#100 = 0.1 ( DYBDE FOR ENGRAVERING ) 
#101 = 150. ( MATING I Z )
#102 = 150. ( MATING X OG Y ) 
#103 = 1. ( STOPP OVER NEXT LETTER )
#104 = 5. ( SKALERING)
#105 = 0.5 ( KLARING I Z)
#106 = 1. (MELLOMROM MELLOM BOKSTAVER) 
#107 = 2.5(MELLOMROM MELLOM ORD) 
""",

        "footer": """
G00U2. 
"""},
    "PUMA  | skriver langs y med y akse ": {
        "header":"""
(A = CODE FOR NUMMMER ELLER BOKSTAV )
(OPS 0 STARTER PÅ 34 )
(SAA 1 STARTER PÅ 35, SAA FØLGER TRENDEN TIL 9 SOM ER 43)

#100 = 0.1 ( DYBDE FOR ENGRAVERING ) 
#101 = 150. ( MATING I Z )
#102 = 150. ( MATING X OG Y ) 
#103 = 1. ( STOPP OVER NEXT LETTER )
#104 = 5. ( SKALERING)
#105 = 0.5 ( KLARING I Z)
#106 = 1. (MELLOMROM MELLOM BOKSTAVER) 
#107 = 2.5(MELLOMROM MELLOM ORD) 
""",

        "footer": """
G00U2. 
"""},
    "PUMA  | skriver langs z med c akse på dia" : {
        "header":"""
(A = CODE FOR NUMMMER ELLER BOKSTAV )
(OPS 0 STARTER PÅ 34 )
(SAA 1 STARTER PÅ 35, SAA FØLGER TRENDEN TIL 9 SOM ER 43)

#100 = 0.1 ( DYBDE FOR ENGRAVERING ) 
#101 = 150. ( MATING I Z )
#102 = 150. ( MATING X OG Y ) 
#103 = 1. ( STOPP OVER NEXT LETTER )
#104 = 5. ( SKALERING)
#105 = 0.5 ( KLARING I Z)
#106 = 1. (MELLOMROM MELLOM BOKSTAVER) 
#107 = 2.5(MELLOMROM MELLOM ORD) 
""",

        "footer": """
G00U2. 
"""
},
}
# Vise listen over navn/maskiner
print("Liste over maskiner:")
for idx, navn in enumerate(navn_liste, start=1):
    print(f"{idx}. {navn}")

# Spørre brukeren om navn/maskin
navn_valg = int(input("Velg en maskin (skriv inn nummeret): "))
navn = navn_liste[navn_valg - 1]
heading = maskin_headere_bunner[navn]["header"]
bunn = maskin_headere_bunner[navn]["footer"]
fanuc_makro = fanuc_makroer[navn]

# Spørre om tekst til merking
tekst = input("\nTekst (tellig er # fks 123-#): ")

# Generere makro-kommandoer basert på input
output = []
for bokstav in tekst:
    if bokstav.upper() in fanuc_makro:
        output.append(fanuc_makro[bokstav.upper()])

# Sette sammen ferdigstilt heading, tekst og bunn
print(f"\n{heading}")
for linje in output:
    print(linje)
print(bunn)