import numpy as np
import cv2

def denormalisasiWarna(list_RGB):
    R_d = (list_RGB[0])/255
    G_d = (list_RGB[1])/255
    B_d = (list_RGB[2])/255
    hasil = [R_d, G_d, B_d]
    return hasil

def Hue(List_Denorm_RBG):
    R_d = List_Denorm_RBG[0]
    G_d = List_Denorm_RBG[1]
    B_d = List_Denorm_RBG[2]
    C_max = max(R_d,G_d,B_d)
    C_min = min(R_d.G_d,B_d)
    delta = C_max - C_min

    # Menghitung nilai H dalam derajat
    if (C_max == R_d):
        H = 60 * (((G_d - B_d)/delta) % 6)
        return H
    elif(C_max == G_d):
        H = 60 * (((B_d - R_d)/delta) + 2)
        return H
    elif(C_max == B_d):
        H = 60 * (((R_d - G_d)/delta) + 4)
        return H

def Saturation(List_denorm_RGB):
    R_d = List_Denorm_RBG[0]
    G_d = List_Denorm_RBG[1]
    B_d = List_Denorm_RBG[2]
    C_max = max(R_d,G_d,B_d)
    C_min = min(R_d.G_d,B_d)
    delta = C_max - C_min

    # Menghitung nilai H dalam derajat
    
    if (C_max == 0):
        return 0
    else:
        S = delta/C_max
        return S

def Value(List_denorm_RGB):
    R_d = List_Denorm_RBG[0]
    G_d = List_Denorm_RBG[1]
    B_d = List_Denorm_RBG[2]
    C_max = max(R_d,G_d,B_d)
    return C_max

def img_to_rgb_list(image_path):
    # Baca gambar menggunakan OpenCV
    img = cv2.imread(image_path)

    # Ubah format warna dari BGR ke RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Dapatkan matriks piksel RGB
    list_RGB = img_rgb.tolist()

    return list_RGB

def cosineSim(vector1, vector2):
    dotProduct = np.dot(vector1, vector2)
    A = np.sqrt(np.sum(vector1 ** 2))
    B = np.sqrt(np.sum(vector2 ** 2))
    return dotProduct / (A * B)

def img_to_VektorHSV(img_path):
    # Mengubah img ke RGB vektor
    List_RGB = img_to_rgb_list(img_path)

    # Menghitung List_Denorm_RGB
    List_Denorm_RGB = denormalisasiWarna(List_RGB)

    # Menghitung Hue
    H = Hue(List_Denorm_RGB)

    # Menghitung Saturation
    S = Saturation(List_Denorm_RGB)

    # Menghitung Value
    V = Value(List_Denorm_RGB)

    # Menyusun vektor HSV
    Vektor_HSV = np.array([H,S,V])

    return Vektor_HSV