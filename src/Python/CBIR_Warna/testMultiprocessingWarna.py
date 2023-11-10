import numpy as np
import cv2
import time
import os
from multiprocessing import Pool

def img_to_matrix_RGB(image_path):
    # Baca gambar menggunakan OpenCV
    img = cv2.imread(image_path)

    # Ubah format warna dari BGR ke RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Konversi ke tipe data float
    img_rgb = img_rgb.astype(np.float32)

    img_rgb /= 255.0
    return img_rgb

def matrix_rgb_to_hist(image):
    # Membagi matrix image menjadi 3 matrix representasi rred, green, blue
    r,g,b = image[:,:,0], image[:,:,1], image[:,:,2]

    # Mencari cmax, cmin, delta
    cmax = np.max(image, axis=2)
    cmin = np.min(image, axis=2)
    delta = (cmax-cmin)

    # Inisialisasi matrix h,s,v
    h = np.zeros_like(r)
    s = np.zeros_like(r)
    v = np.zeros_like(r)

    # Membuat mask untuk r g b untuk h
    mask_r = np.logical_and(delta !=0, cmax==r)
    mask_g = np.logical_and(delta !=0, cmax==g)
    mask_b = np.logical_and(delta !=0, cmax==b)

    # Menghitung nilai h
    h[delta == 0] = 0
    h[mask_r] = 60*(((g[mask_r] -b[mask_r])/(delta[mask_r]))%6)
    h[mask_g] = 60*(((g[mask_g] -b[mask_g])/(delta[mask_g]))+2)
    h[mask_b] = 60*(((g[mask_b] -b[mask_b])/(delta[mask_b]))+4)

    # Hitung nilai s
    s[cmax == 0] = 0
    s[cmax != 0] = (delta[cmax != 0]) / (cmax[cmax != 0])


    # Hitung nilai v
    v = np.maximum.reduce([r,g,b])

    # Menggunakan procedure quantify
    quantify(h,s,v)

    # Mencari histogram h,s,v
    hist_h = cv2.calcHist([h],[0], None, [8], [0,7]).flatten()
    hist_s = cv2.calcHist([s],[0], None, [3], [0,2]).flatten()
    hist_v = cv2.calcHist([v],[0], None, [3], [0,2]).flatten()
    hist = np.concatenate((hist_h,hist_s,hist_v), axis=0)

    return hist

def quantify(h,s,v):
    # Quantify h
    h[h >= 316] = 0
    h[np.logical_and(h >= 1, h <= 25)] = 1
    h[np.logical_and(h >= 26, h <= 40)] = 2
    h[np.logical_and(h >= 41, h <= 120)] = 3
    h[np.logical_and(h >= 121, h <= 190)] = 4
    h[np.logical_and(h >= 191, h <= 270)] = 5
    h[np.logical_and(h >= 271, h <= 295)] = 6
    h[np.logical_and(h >= 296, h <= 315)] = 7

    # Quantify s
    s[s < 0.2] = 0
    s[np.logical_and(s >= 0.2, s < 0.7)] = 1
    s[s >= 0.7] = 2

    # Quantify v
    v[v < 0.2] = 0
    v[np.logical_and(v >= 0.2, v < 0.7)] = 1
    v[v >= 0.7] = 2

def create_submatrices(matrix):
    len_rows, len_cols, _ = matrix.shape

    # Tentukan batas indeks untuk pembagian
    row_splits = [0, len_rows // 3, 2 * len_rows // 3, len_rows]
    col_splits = [0, len_cols // 3, 2 * len_cols // 3, len_cols]

    # Inisialisasi daftar untuk menyimpan submatriks
    submatrices = []

    # Loop melalui bagian-bagian matriks dan potong sesuai batas indeks
    for i in range(3):
        for j in range(3):
            start_row, end_row = row_splits[i], row_splits[i + 1]
            start_col, end_col = col_splits[j], col_splits[j + 1]

            submatrix = matrix[start_row:end_row, start_col:end_col]
            submatrices.append(submatrix)

    return submatrices

def cosinesim(vector_A, vector_B):
    # Hitung dot product antara dua vektor
    dot_product = np.dot(vector_A, vector_B)

    # Hitung norma Euclidean dari masing-masing vektor
    norm_A = np.linalg.norm(vector_A)
    norm_B = np.linalg.norm(vector_B)

    # Hitung cosine similarity
    similarity = dot_product / (norm_A * norm_B)

    return similarity

def CBIR_Warna(img_path_1, img_path_2):
    Matrix1 = img_to_matrix_RGB(img_path_1)
    Matrix2 = img_to_matrix_RGB(img_path_2)

    m_matriks = create_submatrices(Matrix1)
    n_matriks = create_submatrices(Matrix2)

    vektor1 = [matrix_rgb_to_hist(matrix) for matrix in m_matriks]
    vektor2 = [matrix_rgb_to_hist(matrix) for matrix in n_matriks]

    similarity = [cosinesim(vektor1[i],vektor2[i]) for i in range(len(vektor1))]

    # Mencari nilai rata rata dari cosine Similarity
    result = sum(similarity) / len(similarity)
    return result

def process_image(args):
    image_name, dataset_path, reference_image_path = args
    image_path = os.path.join(dataset_path, image_name)
    similarity_score = CBIR_Warna(reference_image_path, image_path)
    return (image_name, similarity_score)

def main():
    reference_image_path = 'isi REFERENCE IMAGE'

    dataset_path = 'isi folder dataset'
    dataset_images = os.listdir(dataset_path)

    start_time = time.time()  

    with Pool() as p:
        results = p.map(process_image, [(image_name, dataset_path, reference_image_path) for image_name in dataset_images])

    end_time = time.time() 

    similarity_scores = {image_name: similarity_score for image_name, similarity_score in results}


    sorted_similarity_scores = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
    for image_name, similarity_score in sorted_similarity_scores:
        print(f"Image: {image_name}, Similarity: {similarity_score * 100:.2f}%")

    print("Execution Time: {:.2f} seconds".format(end_time - start_time)) 

if __name__ == "__main__":
    main()