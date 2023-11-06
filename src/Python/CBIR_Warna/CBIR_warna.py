import numpy as np
import cv2
import time

def denormalisasiWarna(Matrix_RGB):
    hasil = Matrix_RGB / 255
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

def img_to_matrix_RGB(image_path):
    # Baca gambar menggunakan OpenCV
    img = cv2.imread(image_path)

    # Ubah format warna dari BGR ke RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img_rgb

def img_to_Matrix_HSV(img_path):
    # Mengubah img ke list RGB
    Matrix_RGB = img_to_matrix_RGB(img_path)

    # Menghitung List_Denorm_RGB
    Matrix_Denorm_RGB = denormalisasiWarna(Matrix_RGB)

    # Menghitung panjang baris dan kolom array_denorm_RGB
    len_baris, len_kolom, len_pixel = Matrix_Denorm_RGB.shape
    
    Matrix_HSV = np.zeros((len_baris, len_kolom, len_pixel))

    # Menghitung matriks HSV secara vektorisasi
    for i in range(len_baris):
        for j in range(len_kolom):
            R_d, G_d, B_d = Matrix_Denorm_RGB[i, j]
            Matrix_HSV[i, j, 0] = Hue(R_d, G_d, B_d)
            Matrix_HSV[i, j, 1] = Saturation(R_d, G_d, B_d)
            Matrix_HSV[i, j, 2] = Value(R_d, G_d, B_d)
    
    return Matrix_HSV

def cosinesim(vector_A, vector_B):
    # Hitung dot product antara dua vektor
    dot_product = np.dot(vector_A, vector_B)

    # Hitung norma Euclidean dari masing-masing vektor
    norm_A = np.linalg.norm(vector_A)
    norm_B = np.linalg.norm(vector_B)

    # Hitung cosine similarity
    similarity = dot_product / (norm_A * norm_B)

    return similarity

def quantify(h,s,v):
    # Mengubah range hsv
    # range h menjadi [0,7]
    # range s menjadi [0,2]
    # range v menjadi [0,2]
    if(h>=316):
        h = 0
    elif(h>=1 and h<= 25):
        h = 1
    elif(h>=26 and h<= 40):
        h = 2
    elif(h>=41 and h<= 120):
        h = 3
    elif(h>=121 and h<= 190):
        h = 4
    elif(h>=191 and h<= 270):
        h = 5
    elif(h>=271 and h<= 295):
        h = 6
    else:
        h = 7
    if(s>=0 and s<0.2):
        s = 0
    elif(s>=0.2 and s<0.7):
        s = 1
    else:
        s = 2
    if(v>=0 and v<0.2):
        v = 0
    elif(v>=0.2 and v<0.7):
        v = 1
    else:
        v = 2
    return h,s,v

def histogram(Matrix):
    Hist = np.zeros(14, dtype=int)

    # Pisahkan Matrix mejadi 3 matrix yang melambangkan H,S, dan V
    H_channel = Matrix[:,:,0]
    S_channel = Matrix[:,:,1]
    V_channel = Matrix[:,:,2]
    # Mencari panjang Matrix
    len_baris, len_kolom = H_channel.shape

    for i in range(len_baris):
        for j in range(len_kolom):
            Hist[round(H_channel[i,j])] += 1
            Hist[round(S_channel[i,j])+8] += 1
            Hist[round(V_channel[i,j])+11] += 1

    return Hist
def CBIR_Warna(img_path_1, img_path_2):
    # Mencari Matrix HSV dari img path
    Matrix1 = img_to_Matrix_HSV(img_path_1)
    Matrix2 = img_to_Matrix_HSV(img_path_2)

    # mengubah range HSV dengan fungsi quantify
    process_matrix(Matrix1)
    process_matrix(Matrix2)

    # Mengubah matrix menjadi matrix yang lebih kecil dengan menggunakan matrix slicing
    m_matrices = create_submatrices(Matrix1)
    n_matrices = create_submatrices(Matrix2)

    # Mencari histogram matrix nya
    VektorA = [histogram(matrix) for matrix in m_matrices]
    VektorB = [histogram(matrix) for matrix in n_matrices]

    # Mencari nilai cosine similarity
    similarities = [cosinesim(VektorA[i], VektorB[i]) for i in range(len(VektorA))]

    # Mencari nilai rata rata dari cosine Similarity
    result = sum(similarities) / len(similarities) * 100
    return round(result)

def process_matrix(matrix):
    len_baris, len_kolom, _ = matrix.shape

    for i in range(len_baris):
        for j in range(len_kolom):
            h, s, v = matrix[i, j]
            matrix[i, j] = quantify(h, s, v)

def create_submatrices(matrix):
    len_baris, len_kolom, _ = matrix.shape
    submatrices = []
    start_rows = [(i * len_baris) // 3 for i in range(3)]
    end_rows = [((i + 1) * len_baris) // 3 for i in range(3)]
    start_cols = [(j * len_kolom) // 3 for j in range(3)]
    end_cols = [((j + 1) * len_kolom) // 3 for j in range(3)]

    for i in range(3):
        for j in range(3):
            start_row = start_rows[i]
            end_row = end_rows[i]
            start_col = start_cols[j]
            end_col = end_cols[j]

            submatrix = matrix[start_row:end_row, start_col:end_col]
            submatrices.append(submatrix)

    return submatrices