import numpy as np

def calculate_and_print_metric_thread(Basic_diameter, Pitch):
    """
    Calculate and print metric thread dimensions for both internal and external threads.

    Parameters:
    Basic_diameter (float): Major diameter of the thread (mm)
    Pitch (float): Pitch of the thread (mm)
    """
    
    # External thread calculations
    d = Basic_diameter
    P = Pitch
    H = np.sqrt(3)/2 * P
    h_s = 5/8 * H
    h_as = 3/8 * P
    d_2 = d - 2 * h_as
    d_1 = d - 2 * h_s
    F_cs = P / 8
    F_rs = P / 4

    # Tolerances for External Thread
    T_d6 = 180 * (P**2) ** (1/3) - 31.5 / (P**0.5)
    T_d2_6 = 90 * (P**0.4) * (d**0.1)
    T_d2_5 = 0.8 * T_d2_6

    # Internal thread calculations
    d = Basic_diameter
    P = Pitch
    H = np.sqrt(3)/2 * P
    h_n = 5/8 * H
    h_an = 1/4 * P
    D_1 = d - 2 * h_n
    D_2 = D_1 + 2 * h_an
    F_rn = P / 8
    F_cn = P / 4

    # Tolerances for Internal Thread
    T_D1_6 = 433 * P - 190 * (P**1.22)
    if P >= 1:
        T_D1_6 = 230 * (P**0.7)

    T_D2_6 = 1.32 * T_d2_6
    T_D2_5 = 1.06 * T_d2_6

    # Printing the results in the required format
    print(f"(INTERNAL                 | EXTERNAL)")
    print(f"(M{Basic_diameter} X {Pitch} - 6H6H         | M{Basic_diameter} X {Pitch} - 6g6g)") #todo fisk her
    print(f"(PITCH DIAMETER MAX: {D_2:.2f} | PITCH DIAMETER MAX: {d_2:.2f})")
    print(f"(PITCH DIAMETER MIN: {D_1:.2f} | PITCH DIAMETER MIN: {d_1:.2f})")

# Eksempel på bruk av funksjonen
calculate_and_print_metric_thread(10, 1)
