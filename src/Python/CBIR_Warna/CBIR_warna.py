import numpy as np
import cv2

def denormalisasiWarna(Array_RGB):
    hasil = Array_RGB / 255
    return hasil

def Hue(R_d, G_d, B_d):
    C_max = max(R_d, G_d, B_d)
    C_min = min(R_d, G_d, B_d)
    delta = C_max - C_min

    # Menghitung nilai H dalam derajat
    if (delta == 0):
        return 0
    elif C_max == R_d:
        H = 60 * (((G_d - B_d) / delta) % 6)
    elif C_max == G_d:
        H = 60 * (((B_d - R_d) / delta) + 2)
    elif C_max == B_d:
        H = 60 * (((R_d - G_d) / delta) + 4)
    return H

def Saturation(R_d, G_d, B_d):
    C_max = max(R_d, G_d, B_d)
    C_min = min(R_d, G_d, B_d)
    delta = C_max - C_min

    # Menghitung nilai H dalam derajat
    if C_max == 0:
        return 0
    else:
        S = delta / C_max
        return S

def Value(R_d, G_d, B_d):
    C_max = max(R_d, G_d, B_d)
    return C_max

def img_to_array_RGB(image_path):
    # Baca gambar menggunakan OpenCV
    img = cv2.imread(image_path)

    # Ubah format warna dari BGR ke RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Dapatkan matriks piksel RGB
    list_RGB = img_rgb.tolist()

    # Matrix RGB
    Matrix_RGB = np.array(list_RGB)

    return Matrix_RGB

def img_to_Matrix_HSV(img_path):
    # Mengubah img ke list RGB
    List_RGB = img_to_array_RGB(img_path)

    # Menghitung List_Denorm_RGB
    array_Denorm_RGB = denormalisasiWarna(List_RGB)

    # Menghitung matriks HSV secara vektorisasi
    Matrix_HSV = np.array([(Hue(*pixel), Saturation(*pixel), Value(*pixel)) for row in array_Denorm_RGB for pixel in row])

    return Matrix_HSV

def cosineSim(Matrix1, Matrix2):
    dotProduct = np.sum(np.dot(Matrix1[i], Matrix2[i]) for i in range(Matrix1.shape[0]))
    A = np.sqrt(np.sum(np.fromiter((np.sum(Matrix1[i] ** 2) for i in range(Matrix1.shape[0])), dtype=np.float64)))
    B = np.sqrt(np.sum(np.fromiter((np.sum(Matrix2[i] ** 2) for i in range(Matrix2.shape[0])), dtype=np.float64)))
    return dotProduct / (A * B) if (A * B) != 0 else np.nan

def CBIR_Warna(img_path_1, img_path_2):
    Matrix1 = img_to_Matrix_HSV(img_path_1)
    Matrix2 = img_to_Matrix_HSV(img_path_2)

    # Cari CBIR dengan cosineSim
    similarity = cosineSim(Matrix1, Matrix2)

    # Mengubah nilai similarity menjadi persen
    similarity = round(similarity * 100)
    return similarity