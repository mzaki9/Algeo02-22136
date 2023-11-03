import numpy as np

def dinormalisasiWarna(list_RGB):
    R_d = (list_RGB[0])/255
    G_d = (list_RGB[1])/255
    B_d = (list_RGB[2])/255
    hasil = [R_d, G_d, B_d]
    return hasil

def MencariHSV(List_Denorm_RBG):
    R_d = List_Denorm_RBG[0];
    G_d = List_Denorm_RBG[1];
    B_d = List_Denorm_RBG[2];
    C_max = max(R_d,G_d,B_d);
    C_min = min(R_d.G_d,B_d)
    delta = C_max - C_min

    # Menghitung nilai H dalam derajat
    H1 = 60 * (((G_d - B_d)/delta) % 6)